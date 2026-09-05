#!/usr/bin/env python3
"""Flag expected output a learner cannot discover from the question.

Usage: check-expected-strings.py <file.xml> [...]

Grading is an exact string match, so every literal string a test expects must
be discoverable before submission: in the question text, in the starter code,
or in an example test's expected output. A non-example test that expects text
appearing nowhere in those places forces the learner to guess.

The comparison is per word. A word counts as a defect only when it appears in
the question's own sample answer (so the author typed it, and the learner must
too) but nowhere in what the learner can see: the question text, the starter
code, any test input, or an example test's expected output. Words the answer
never writes are computed from inputs or produced by the Go runtime, and are
exempt. The // rules test case is skipped: its output comes from the
prototype, not the learner.
"""

import html
import re
import sys
import xml.etree.ElementTree as ET

TAG = re.compile(r"<[^>]+>")
SKELETON_KEEP = re.compile(r"[^A-Za-z0-9 ]+")

# Numbers and Go's boolean keywords are language constants the learner's code
# computes; they are never typed as output strings.
DERIVABLE = {"true", "false"}


def skeleton(text):
    return " ".join(SKELETON_KEEP.sub(" ", text).split())


def text_of(question, path):
    node = question.find(path)
    if node is None:
        return ""
    text_node = node.find("text")
    if text_node is not None:
        return text_node.text or ""
    return node.text or ""


def main(paths):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    flagged = 0
    for path in paths:
        for question in ET.parse(path).getroot().findall("question"):
            if question.get("type") != "coderunner":
                continue
            name = (text_of(question, "name") or "unnamed").strip()

            visible = [text_of(question, "questiontext"), question.findtext("answerpreload") or ""]
            testcases = question.find("testcases")
            if testcases is None:
                continue
            cases = testcases.findall("testcase")
            for case in cases:
                if case.get("useasexample") == "1":
                    visible.append(text_of(case, "expected"))
                # Test inputs are fair game: the learner's code can derive
                # output words from them.
                visible.append(text_of(case, "testcode"))
                visible.append(text_of(case, "stdin"))
            corpus = set(skeleton(html.unescape(" ".join(visible))).split())
            typed = set(skeleton(text_of(question, "answer")).split())

            for index, case in enumerate(cases, start=1):
                if (text_of(case, "testcode") or "").strip() == "// rules":
                    continue
                if case.get("useasexample") == "1":
                    continue
                expected = text_of(case, "expected")
                for line in expected.split("\n"):
                    missing = [w for w in skeleton(html.unescape(line)).split()
                               if w not in corpus and w in typed
                               and not w.isdigit() and w not in DERIVABLE]
                    if missing:
                        flagged += 1
                        print(f"{path}: {name} test {index}")
                        print(f"    expected line: {line!r}")
                        print(f"    undiscoverable: {' '.join(missing)}")
    print(f"\n{flagged} undiscoverable expected string(s)")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
