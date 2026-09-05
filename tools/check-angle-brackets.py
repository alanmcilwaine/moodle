#!/usr/bin/env python3
"""Flag expected output that Moodle's XML import would mangle.

Usage: check-angle-brackets.py <file.xml> [...]

Moodle treats angle brackets in an expected value as HTML. When two such
sequences sit on adjacent lines, the newline between them is collapsed on
import, and the question then fails against output that is actually correct.
This was found the hard way: `print(type(x))` on two consecutive lines produced
`<class 'tuple'>` and `<class 'int'>`, and the stored expected value lost the
newline between them.

Print `type(x).__name__` rather than `type(x)`. It reads better anyway.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Two angle-bracket sequences separated only by whitespace.
DANGEROUS = re.compile(r"<[^>\n]+>\s*\n\s*<[^>\n]+>")
ANY_TAG = re.compile(r"<[A-Za-z/!][^>\n]*>")


def main(paths: list[str]) -> int:
    errors = 0
    warnings = 0
    checked = 0

    for path in paths:
        for question in ET.parse(path).getroot().findall("question"):
            if question.get("type") != "coderunner":
                continue
            name = (question.findtext("name/text") or "unnamed").strip()
            cases = question.find("testcases")
            if cases is None:
                continue
            for index, case in enumerate(cases, start=1):
                expected = case.findtext("expected/text") or ""
                checked += 1
                if DANGEROUS.search(expected):
                    errors += 1
                    print(
                        f"BREAKS {Path(path).name}: {name} test {index}\n"
                        f"    two angle-bracket lines in a row. The newline between them "
                        f"is lost on import.\n"
                        f"    Print type(x).__name__ instead of type(x)."
                    )
                elif ANY_TAG.search(expected):
                    warnings += 1
                    print(
                        f"RISK   {Path(path).name}: {name} test {index}\n"
                        f"    expected output contains angle brackets. It survives today, "
                        f"but stays fragile."
                    )

    print(f"\n{checked} test cases checked, {errors} broken, {warnings} fragile")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
