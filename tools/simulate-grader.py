#!/usr/bin/env python3
"""Run CodeRunner questions locally the way the python3 combinator template does.

Usage: simulate-grader.py <file.xml> [...]

CodeRunner's built-in python3 prototype is a combinator template. It builds ONE
program from the student answer followed by every test case, separated by a
marker, runs it once, then splits the output back into per-test results. Code at
module level therefore runs once for the whole question, not once per test case.

This script reproduces that exactly, so an authoring mistake shows up here
instead of after an import into Moodle.
"""

import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

SEPARATOR = "#<ab@17943918#@>#"
TIMEOUT_SECONDS = 15


def escape_py(text: str) -> str:
    """Reproduce Twig's py escaper, which CodeRunner applies to STUDENT_ANSWER."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def build_program(answer: str, testcodes: list[str]) -> str:
    # The real template inserts a second copy of the answer as a string literal.
    # A test that reads the whole source file sees both copies, so the simulator
    # has to include it or it disagrees with the sandbox.
    parts = [
        answer,
        "",
        f'__student_answer__ = """{escape_py(answer)}"""',
        "",
        f'SEPARATOR = "{SEPARATOR}"',
        "",
    ]
    for index, code in enumerate(testcodes):
        parts.append(code)
        if index != len(testcodes) - 1:
            parts.append("print(SEPARATOR)")
    return "\n".join(parts) + "\n"


def run(program: str) -> tuple[str, str, int]:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as handle:
        handle.write(program)
        path = handle.name
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        return result.stdout, result.stderr, result.returncode
    finally:
        Path(path).unlink(missing_ok=True)


def check_question(question: ET.Element) -> list[str]:
    name = (question.findtext("name/text") or "unnamed").strip()
    answer = question.findtext("answer") or ""
    if not answer.strip():
        return [f"{name}: no sample answer"]

    cases = question.find("testcases")
    if cases is None or len(cases) == 0:
        return [f"{name}: no test cases"]

    testcodes = [(case.findtext("testcode/text") or "") for case in cases]
    expecteds = [(case.findtext("expected/text") or "") for case in cases]

    stdout, stderr, code = run(build_program(answer, testcodes))
    if code != 0:
        tail = stderr.strip().splitlines()[-1] if stderr.strip() else f"exit {code}"
        return [f"{name}: the program crashed. {tail}"]

    segments = stdout.split(SEPARATOR + "\n")
    if len(segments) != len(testcodes):
        return [
            f"{name}: produced {len(segments)} output segments for {len(testcodes)} test cases"
        ]

    problems = []
    for index, (segment, expected) in enumerate(zip(segments, expecteds), start=1):
        got = segment.rstrip("\n")
        want = expected.rstrip("\n")
        if got != want:
            problems.append(
                f"{name}: test {index} mismatch\n"
                f"    expected: {want!r}\n"
                f"    actual:   {got!r}"
            )
    return problems


def main(paths: list[str]) -> int:
    if not paths:
        print(__doc__, file=sys.stderr)
        return 2

    failures = 0
    total = 0
    for path in paths:
        root = ET.parse(path).getroot()
        questions = [q for q in root.findall("question") if q.get("type") == "coderunner"]
        for question in questions:
            total += 1
            problems = check_question(question)
            for problem in problems:
                print(f"FAIL {Path(path).name}: {problem}")
            failures += bool(problems)

    passed = total - failures
    print(f"{passed}/{total} questions pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
