#!/usr/bin/env python3
"""Validate course packages before setup-course.sh ships them to Moodle.

Usage: validate-course-packages.py [courses-dir]   (default: courses)

A course package is a directory under courses-dir that holds a manifest.json.
Directories without one are ignored. The manifest declares a course object, an
optional list of prototype XML files, and a nonempty list of modules. Each
module names a Moodle XML file of coderunner questions, the WAT topic range it
covers as [from, to], and the number of questions it must contain.

Every violation prints one line to stderr, prefixed with the package directory
name. Packages are checked in sorted order, checks run in a fixed order, and
files are visited sorted, so the output is deterministic. One run reports
every violation it can reach; only an unreadable manifest stops a package
early. Exit 0 means every discovered package is valid. Discovering zero
packages is an error.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath, PureWindowsPath

WAT_NAME = re.compile(r"^WAT (\d+)\.(\d+):")


def is_plain_basename(value):
    """A file value must name a file inside the package, nothing else."""
    if not value or "/" in value or "\\" in value or value in (".", ".."):
        return False
    if PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute():
        return False
    return not PureWindowsPath(value).drive


def coderunner_questions(root):
    return [q for q in root.findall("question") if q.get("type") == "coderunner"]


def question_names(root):
    """Stripped names of the coderunner questions in a parsed quiz file."""
    return [((q.findtext("name/text")) or "").strip() for q in coderunner_questions(root)]


def parse_xml_file(pkg_dir, filename, fail):
    path = pkg_dir / filename
    if not path.is_file():
        fail(f"{filename}: file does not exist")
        return None
    try:
        return ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        fail(f"{filename}: invalid XML: {exc}")
        return None


def is_int(value):
    # bool is a subclass of int; True is not a WAT topic or a question count.
    return type(value) is int


def validate_package(pkg_dir, shortnames, errors):
    """Check one package and append (package, message) errors.

    shortnames maps each shortname already claimed to the package that claimed
    it. Returns (name, module count, question count) for the summary line.
    """
    name = pkg_dir.name

    def fail(message):
        errors.append((name, message))

    # 1. The manifest parses as JSON. Nothing else is reachable if it does not.
    try:
        manifest = json.loads((pkg_dir / "manifest.json").read_text(encoding="utf-8"))
    except OSError as exc:
        fail(f"manifest.json: cannot read: {exc}")
        return None
    except json.JSONDecodeError as exc:
        fail(f"manifest.json: invalid JSON: {exc}")
        return None
    if not isinstance(manifest, dict):
        fail("manifest.json: top level must be a JSON object")
        return None

    # 2. The course object carries three nonempty strings.
    course = manifest.get("course")
    if not isinstance(course, dict):
        fail("manifest.json: 'course' must be an object")
        course = {}
    for field in ("fullname", "shortname", "section"):
        if not isinstance(course.get(field), str) or not course[field].strip():
            fail(f"manifest.json: course.{field} must be a nonempty string")
    shortname = course.get("shortname")

    # 3. The shortname is unique across all discovered packages.
    if isinstance(shortname, str) and shortname.strip():
        if shortname in shortnames:
            fail(
                f"manifest.json: shortname '{shortname}' is also used by "
                f"package '{shortnames[shortname]}'"
            )
        else:
            shortnames[shortname] = name

    # 4. Prototypes are file names that exist and parse as XML.
    prototypes = manifest.get("prototypes", [])
    if not isinstance(prototypes, list):
        fail("manifest.json: 'prototypes' must be a list")
        prototypes = []
    prototype_files = []
    for entry in prototypes:
        if not isinstance(entry, str) or not entry:
            fail(f"manifest.json: prototype entries must be nonempty strings, got {entry!r}")
        else:
            prototype_files.append(entry)
    roots = {}
    for value in sorted(set(prototype_files)):
        if is_plain_basename(value):
            roots[value] = parse_xml_file(pkg_dir, value, fail)

    # 5. Modules are well formed.
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        fail("manifest.json: 'modules' must be a nonempty list")
        modules = []
    for index, module in enumerate(modules):
        where = f"manifest.json: modules[{index}]"
        if not isinstance(module, dict):
            fail(f"{where} must be an object")
            continue
        if not isinstance(module.get("file"), str) or not module["file"]:
            fail(f"{where}.file must be a nonempty string")
        if not isinstance(module.get("title"), str) or not module["title"].strip():
            fail(f"{where}.title must be a nonempty string")
        for field in ("from", "to"):
            if not is_int(module.get(field)):
                fail(f"{where}.{field} must be an int")
        if is_int(module.get("from")) and is_int(module.get("to")):
            if module["from"] > module["to"]:
                fail(f"{where}: from ({module['from']}) exceeds to ({module['to']})")
        if not is_int(module.get("questions")):
            fail(f"{where}.questions must be an int")
        elif module["questions"] < 1:
            fail(f"{where}.questions must be a positive int")

    module_files = [
        m["file"]
        for m in modules
        if isinstance(m, dict) and isinstance(m.get("file"), str) and m["file"]
    ]

    # 6. Every referenced file value is a plain basename.
    for value in sorted(set(prototype_files)):
        if not is_plain_basename(value):
            fail(f"manifest.json: prototype '{value}' must be a plain file name, not a path")
    for value in sorted(set(module_files)):
        if not is_plain_basename(value):
            fail(f"manifest.json: module file '{value}' must be a plain file name, not a path")

    # 7. WAT ranges within the package do not overlap. Sorted by lower bound,
    # any overlap shows up between consecutive ranges.
    ranged = sorted(
        (m["from"], m["to"])
        for m in modules
        if isinstance(m, dict)
        and is_int(m.get("from"))
        and is_int(m.get("to"))
        and m["from"] <= m["to"]
    )
    for (lo1, hi1), (lo2, hi2) in zip(ranged, ranged[1:]):
        if lo2 <= hi1:
            fail(f"manifest.json: WAT ranges [{lo1}, {hi1}] and [{lo2}, {hi2}] overlap")

    # 8. Every module file exists and parses as XML.
    for value in sorted(set(module_files)):
        if is_plain_basename(value) and value not in roots:
            roots[value] = parse_xml_file(pkg_dir, value, fail)

    def modules_by_file():
        keyed = [
            m
            for m in modules
            if isinstance(m, dict) and isinstance(m.get("file"), str) and m["file"]
        ]
        return sorted(keyed, key=lambda m: m["file"])

    # 9. Each module file holds exactly its declared number of questions.
    for module in modules_by_file():
        root = roots.get(module["file"])
        if root is None or not is_int(module.get("questions")):
            continue
        actual = len(coderunner_questions(root))
        if actual != module["questions"]:
            fail(
                f"{module['file']}: declares {module['questions']} questions "
                f"but contains {actual}"
            )

    # 10. Question names are unique across every file in the package.
    seen = {}
    for value in sorted(roots):
        if roots[value] is None:
            continue
        for qname in question_names(roots[value]):
            if not qname:
                continue
            if qname in seen:
                fail(f"question name '{qname}' appears in both {seen[qname]} and {value}")
            else:
                seen[qname] = value

    # 11. Module question names carry a WAT topic inside the module's range.
    for module in modules_by_file():
        root = roots.get(module["file"])
        if root is None or not is_int(module.get("from")) or not is_int(module.get("to")):
            continue
        for qname in question_names(root):
            match = WAT_NAME.match(qname)
            if not match:
                fail(
                    f"{module['file']}: question name '{qname}' does not match "
                    f"'WAT <topic>.<n>: <title>'"
                )
                continue
            topic = int(match.group(1))
            if not module["from"] <= topic <= module["to"]:
                fail(
                    f"{module['file']}: question '{qname}' is topic {topic}, "
                    f"outside the module range [{module['from']}, {module['to']}]"
                )

    # 12. Every XML file in the package directory is referenced by the manifest.
    referenced = set(prototype_files) | set(module_files)
    for path in sorted(pkg_dir.glob("*.xml")):
        if path.name not in referenced:
            fail(f"{path.name}: XML file is not referenced by the manifest")

    total = sum(m["questions"] for m in modules if isinstance(m, dict) and is_int(m.get("questions")))
    return name, len(modules), total


def plural(count, word):
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def main(argv):
    if len(argv) > 1:
        print("usage: validate-course-packages.py [courses-dir]", file=sys.stderr)
        return 1
    courses_dir = Path(argv[0]) if argv else Path("courses")

    packages = []
    if courses_dir.is_dir():
        packages = sorted(
            (d for d in courses_dir.iterdir() if d.is_dir() and (d / "manifest.json").is_file()),
            key=lambda d: d.name,
        )
    if not packages:
        print(f"no course packages discovered in {courses_dir}", file=sys.stderr)
        return 1

    errors = []
    summaries = []
    shortnames = {}
    for pkg_dir in packages:
        summary = validate_package(pkg_dir, shortnames, errors)
        if summary is not None:
            summaries.append(summary)

    for pkg_name, message in errors:
        print(f"{pkg_name}: {message}", file=sys.stderr)
    if errors:
        return 1

    details = ", ".join(
        f"{name} ({plural(modules, 'module')}, {plural(questions, 'question')})"
        for name, modules, questions in summaries
    )
    print(f"{plural(len(summaries), 'course package')} valid: {details}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
