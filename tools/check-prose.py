#!/usr/bin/env python3
"""Extract the teaching prose from WAT questions and run the writing checker on it.

Usage: check-prose.py <file.xml> [...]

Each question's `questiontext` is HTML. This script strips the markup, drops the
code samples and the three standard blocks, writes what is left to a scratch
markdown file, and runs the technical-writing checker over it.

Code inside `pre` and `code` is not prose and is skipped. The Rules, Predict and
AI protocol blocks are fixed text, so they are skipped too and only report once.
"""

import html
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

CHECKER = Path("/home/alan/.claude/skills/technical-writing/.venv/bin/python")
CHECK_SCRIPT = Path("/home/alan/.claude/skills/technical-writing/check.py")

BLOCK_MARKERS = ("<b>Rules</b>", "<b>Before you click Check</b>", "<b>AI protocol</b>")


def strip_blocks(markup: str) -> str:
    """Remove the three standard blocks, which are fixed text."""
    for marker in BLOCK_MARKERS:
        index = markup.find(marker)
        while index != -1:
            start = markup.rfind("<div", 0, index)
            end = markup.find("</div>", index)
            if start == -1 or end == -1:
                break
            markup = markup[:start] + markup[end + len("</div>") :]
            index = markup.find(marker)
    return markup


def to_prose(markup: str) -> str:
    """Turn question HTML into plain prose the checker can read."""
    text = strip_blocks(markup)
    text = re.sub(r"<pre>.*?</pre>", "", text, flags=re.S)
    text = re.sub(r"<code>.*?</code>", "CODE", text, flags=re.S)
    text = re.sub(r"<li>", "\n- ", text)
    text = re.sub(r"</(p|ul|ol|li|h\d)>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def check(prose: str) -> list[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
        handle.write(prose + "\n")
        path = handle.name
    try:
        result = subprocess.run(
            [str(CHECKER), str(CHECK_SCRIPT), path],
            capture_output=True,
            text=True,
            cwd=CHECK_SCRIPT.parent,
        )
        output = result.stdout.strip()
        if output == "clean" or not output:
            return []
        return [line for line in output.splitlines() if "finding" not in line]
    finally:
        Path(path).unlink(missing_ok=True)


def main(paths: list[str]) -> int:
    if not CHECKER.exists():
        print(f"checker not found at {CHECKER}", file=sys.stderr)
        return 2

    total = 0
    flagged = 0
    for path in paths:
        for question in ET.parse(path).getroot().findall("question"):
            if question.get("type") != "coderunner":
                continue
            total += 1
            name = (question.findtext("name/text") or "unnamed").strip()
            prose = to_prose(question.findtext("questiontext/text") or "")
            findings = check(prose)
            if findings:
                flagged += 1
                print(f"\n{Path(path).name}  {name}")
                for finding in findings:
                    print(f"    {finding}")

    print(f"\n{total - flagged}/{total} questions clean")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
