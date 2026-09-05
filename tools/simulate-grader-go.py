#!/usr/bin/env python3
"""Simulate the Go CodeRunner templates against authored course files.

Mirrors courses/go/prototype-go-program.xml and prototype-go-testwriter.xml
exactly: same harness generation, same banned-word scan, same per-test
execution. Change them together.

Usage: simulate-grader-go.py [--go /path/to/go] courses/go/topic-NN.xml ...
Exit 1 on any mismatch. Also runs gofmt -l and go vet over every sample answer,
per the course spec's production-idiom gate.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def text_of(node) -> str:
    if node is None:
        return ""
    t = node.find("text")
    if t is not None:
        return t.text or ""
    return node.text or ""


def build_harness(testcodes: list[str]) -> str:
    parts = [
        'package main\n\nimport (\n\t"fmt"\n\t"os"\n)\n\nvar _ = fmt.Sprint\n\nfunc main() {\n\tswitch os.Args[1] {\n'
    ]
    for i, code in enumerate(testcodes):
        parts.append(f'\tcase "{i}":\n')
        parts.append(code)
        parts.append("\n")
    parts.append("\t}\n}\n")
    return "".join(parts)


GOCACHE = Path.home() / ".cache/moodle-go"
GO_DIR = Path(__file__).resolve().parent.parent / "courses/go"
PROTOTYPES = (GO_DIR / "prototype-go-program.xml", GO_DIR / "prototype-go-testwriter.xml")


def check_block(path: Path) -> str:
    template = text_of(ET.parse(path).getroot().find("question/template")) or ""
    start = template.index("# --- checks begin ---")
    end = template.index("# --- checks end ---")
    return template[start:end]


def load_check_rules():
    """Execute the rule-check block out of the prototype templates so the
    simulator and both live graders share one implementation. Each prototype
    carries the block verbatim, so a difference between them is drift."""
    blocks = {path.name: check_block(path) for path in PROTOTYPES}
    if len(set(blocks.values())) != 1:
        raise SystemExit("check block differs between " + " and ".join(blocks))
    ns = {"re": re}
    exec(next(iter(blocks.values())), ns)
    return ns["check_rules"]


check_rules = None


def rule_params(q, name: str, problems: list[str]):
    params = q.findtext("templateparams") or ""
    if not params.strip():
        return [], [], []
    try:
        d = json.loads(params)
    except json.JSONDecodeError:
        problems.append(f"{name}: templateparams is not valid JSON")
        return [], [], []
    return d.get("banned", "").split(), d.get("required", "").split(), d.get("limit", "").split()


def banned_hits(q, answer: str, name: str, problems: list[str]) -> None:
    global check_rules
    if check_rules is None:
        check_rules = load_check_rules()
    failure = check_rules(answer, *rule_params(q, name, problems))
    if failure:
        problems.append(f"{name}: sample answer fails its own rules, {failure}")


def grade_question(q, go: str, fname: str) -> list[str]:
    if q.get("type") != "coderunner":
        return []
    if (q.findtext("prototypetype") or "").strip() == "1":
        return []
    ctype = (q.findtext("coderunnertype") or "").strip()
    if ctype == "go_program":
        return grade_program(q, go)
    if ctype == "go_testwriter":
        return grade_testwriter(q, go)
    return []


def grade_program(q, go: str) -> list[str]:
    problems = []
    name = text_of(q.find("name"))
    answer = text_of(q.find("answer")) or (q.findtext("answer") or "")
    if not answer.strip():
        return [f"{name}: no sample answer"]

    banned_hits(q, answer, name, problems)

    cases = q.find("testcases").findall("testcase")
    testcodes = [text_of(c.find("testcode")) for c in cases]
    stdins = [text_of(c.find("stdin")) for c in cases]
    expecteds = [text_of(c.find("expected")) for c in cases]

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "student.go").write_text(answer)
        (d / "tests.go").write_text(build_harness(testcodes))
        env = {
            "GOCACHE": str(GOCACHE),
            "GOMAXPROCS": "1",
            "PATH": "/usr/bin:/bin",
            "HOME": str(d),
        }
        cp = subprocess.run(
            [go, "build", "-p=1", "-o", "prog", "student.go", "tests.go"],
            cwd=d, env=env, capture_output=True, text=True,
        )
        if cp.returncode != 0:
            return problems + [f"{name}: sample answer does not compile:\n{cp.stderr}"]

        gofmt = str(Path(go).parent / "gofmt") if "/" in go else "gofmt"
        fmt_out = subprocess.run([gofmt, "-l", "student.go"],
                                 cwd=d, env=env, capture_output=True, text=True)
        if fmt_out.stdout.strip():
            problems.append(f"{name}: sample answer is not gofmt-clean")
        vet = subprocess.run([go, "vet", "-p=1", "student.go", "tests.go"],
                             cwd=d, env=env, capture_output=True, text=True)
        if vet.returncode != 0:
            problems.append(f"{name}: go vet fails:\n{vet.stderr}")

        for i, (code, stdin_text, expected) in enumerate(zip(testcodes, stdins, expecteds)):
            if code.strip() == "// rules":
                got = "rules ok"
            else:
                r = subprocess.run(["./prog", str(i)], cwd=d, input=stdin_text,
                                   env=env, capture_output=True, text=True)
                got = r.stdout + (r.stderr if r.returncode != 0 else "")
            if got.rstrip("\n") != expected.rstrip("\n"):
                problems.append(
                    f"{name} test {i + 1}: expected {expected!r}, got {got!r}"
                )
    return problems


def grade_testwriter(q, go: str) -> list[str]:
    problems = []
    name = text_of(q.find("name"))
    answer = text_of(q.find("answer")) or (q.findtext("answer") or "")
    if not answer.strip():
        return [f"{name}: no sample answer"]

    banned_hits(q, answer, name, problems)

    cases = q.find("testcases").findall("testcase")
    variants = [text_of(c.find("extra")) for c in cases]
    expecteds = [text_of(c.find("expected")) for c in cases]

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        env = {
            "GOCACHE": str(GOCACHE),
            "GOMAXPROCS": "1",
            "PATH": "/usr/bin:/bin",
            "HOME": str(d),
        }
        for i, impl in enumerate(variants):
            v = d / f"v{i}"
            v.mkdir()
            (v / "go.mod").write_text("module wat\n\ngo 1.27\n")
            (v / "impl.go").write_text(impl)
            (v / "impl_test.go").write_text(answer)

        cp = subprocess.run([go, "test", "-p=1", "-vet=off", "-run", "^$", "."],
                            cwd=d / "v0", env=env, capture_output=True, text=True)
        if cp.returncode != 0:
            return problems + [f"{name}: sample answer does not compile:\n{cp.stderr}"]

        gofmt = str(Path(go).parent / "gofmt") if "/" in go else "gofmt"
        fmt_out = subprocess.run([gofmt, "-l", "impl_test.go"],
                                 cwd=d / "v0", env=env, capture_output=True, text=True)
        if fmt_out.stdout.strip():
            problems.append(f"{name}: sample answer is not gofmt-clean")
        vet = subprocess.run([go, "vet", "-p=1", "."],
                             cwd=d / "v0", env=env, capture_output=True, text=True)
        if vet.returncode != 0:
            problems.append(f"{name}: go vet fails:\n{vet.stderr}")

        for i, expected in enumerate(expecteds):
            r = subprocess.run([go, "test", "-p=1", "-vet=off", "."], cwd=d / f"v{i}",
                               env=env, capture_output=True, text=True)
            got = "PASS" if r.returncode == 0 else "FAIL"
            if got != expected.strip():
                problems.append(
                    f"{name} variant {i + 1}: expected {expected.strip()!r}, got {got!r}"
                )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", default="go")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    failures = 0
    for fname in args.files:
        tree = ET.parse(fname)
        for q in tree.getroot().findall("question"):
            for p in grade_question(q, args.go, fname):
                print(f"{fname}: {p}")
                failures += 1
    if failures:
        print(f"{failures} problem(s)")
        return 1
    print("all Go questions simulate clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
