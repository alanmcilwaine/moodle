#!/usr/bin/env python3
"""Tests for validate-course-packages.py.

Usage: test-validate-course-packages.py

Builds fixture course packages in temporary directories and drives the
validator in-process through its main(argv) entry point, capturing stdout and
stderr. Run from anywhere; the real-repo test chdirs to the repo root itself.
"""

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent

spec = importlib.util.spec_from_file_location(
    "validate_course_packages", TOOLS_DIR / "validate-course-packages.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def module_xml(names):
    questions = "".join(
        f'<question type="coderunner"><name><text>{name}</text></name></question>'
        for name in names
    )
    return f"<quiz>{questions}</quiz>"


def make_manifest(shortname="demo", modules=None, prototypes=None):
    manifest = {
        "course": {"fullname": "Demo", "shortname": shortname, "section": "Topics"},
        "modules": modules
        if modules is not None
        else [{"file": "mod-01.xml", "title": "Module 1", "from": 1, "to": 1, "questions": 1}],
    }
    if prototypes is not None:
        manifest["prototypes"] = prototypes
    return manifest


def write_package(courses_dir, name, manifest, files):
    pkg = Path(courses_dir) / name
    pkg.mkdir()
    text = manifest if isinstance(manifest, str) else json.dumps(manifest)
    (pkg / "manifest.json").write_text(text, encoding="utf-8")
    for filename, content in files.items():
        (pkg / filename).write_text(content, encoding="utf-8")
    return pkg


def write_valid_package(courses_dir, name="demo", shortname="demo"):
    return write_package(
        courses_dir,
        name,
        make_manifest(shortname=shortname),
        {"mod-01.xml": module_xml(["WAT 01.1: x"])},
    )


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.courses_dir = Path(self.tmp.name) / "courses"
        self.courses_dir.mkdir()

    def run_validator(self, args, cwd=None):
        out, err = io.StringIO(), io.StringIO()
        old_cwd = os.getcwd()
        try:
            if cwd is not None:
                os.chdir(cwd)
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = validator.main(args)
        finally:
            os.chdir(old_cwd)
        return code, out.getvalue(), err.getvalue()

    def check_fails(self, needle):
        code, out, err = self.run_validator([str(self.courses_dir)])
        self.assertEqual(1, code)
        self.assertIn(needle, err)
        self.assertEqual("", out)

    def test_minimal_valid_package_passes(self):
        write_valid_package(self.courses_dir)
        code, out, err = self.run_validator([str(self.courses_dir)])
        self.assertEqual(0, code)
        self.assertIn("1 course package valid: demo (1 module, 1 question)", out)
        self.assertEqual("", err)

    def test_real_repo_package_passes(self):
        code, out, err = self.run_validator(["courses"], cwd=REPO_ROOT)
        self.assertEqual(0, code, msg=err)
        self.assertIn("python (24 modules, 75 questions)", out)

    def test_invalid_json_fails(self):
        write_package(self.courses_dir, "demo", "{not json", {})
        self.check_fails("demo: manifest.json: invalid JSON")

    def test_missing_module_file_fails(self):
        write_package(self.courses_dir, "demo", make_manifest(), {})
        self.check_fails("demo: mod-01.xml: file does not exist")

    def test_question_count_mismatch_fails(self):
        manifest = make_manifest(
            modules=[{"file": "mod-01.xml", "title": "M1", "from": 1, "to": 1, "questions": 2}]
        )
        write_package(self.courses_dir, "demo", manifest, {"mod-01.xml": module_xml(["WAT 01.1: x"])})
        self.check_fails("declares 2 questions but contains 1")

    def test_duplicate_shortname_fails(self):
        write_valid_package(self.courses_dir, name="aaa", shortname="same")
        write_valid_package(self.courses_dir, name="bbb", shortname="same")
        self.check_fails("bbb: manifest.json: shortname 'same' is also used by package 'aaa'")

    def test_duplicate_question_name_fails(self):
        manifest = make_manifest(
            modules=[{"file": "mod-01.xml", "title": "M1", "from": 1, "to": 1, "questions": 2}]
        )
        files = {"mod-01.xml": module_xml(["WAT 01.1: x", "WAT 01.1: x"])}
        write_package(self.courses_dir, "demo", manifest, files)
        self.check_fails("question name 'WAT 01.1: x' appears in both")

    def test_path_traversal_file_fails(self):
        manifest = make_manifest(
            modules=[{"file": "../other.xml", "title": "M1", "from": 1, "to": 1, "questions": 1}]
        )
        write_package(self.courses_dir, "demo", manifest, {})
        self.check_fails("module file '../other.xml' must be a plain file name")

    def test_unreferenced_xml_fails(self):
        write_valid_package(self.courses_dir)
        (Path(self.courses_dir) / "demo" / "stray.xml").write_text("<quiz/>", encoding="utf-8")
        self.check_fails("demo: stray.xml: XML file is not referenced by the manifest")

    def test_wat_topic_outside_range_fails(self):
        files = {"mod-01.xml": module_xml(["WAT 02.1: x"])}
        write_package(self.courses_dir, "demo", make_manifest(), files)
        self.check_fails("outside the module range [1, 1]")

    def test_overlapping_wat_ranges_fail(self):
        manifest = make_manifest(
            modules=[
                {"file": "mod-01.xml", "title": "M1", "from": 1, "to": 2, "questions": 1},
                {"file": "mod-02.xml", "title": "M2", "from": 2, "to": 3, "questions": 1},
            ]
        )
        files = {
            "mod-01.xml": module_xml(["WAT 01.1: x"]),
            "mod-02.xml": module_xml(["WAT 02.1: y"]),
        }
        write_package(self.courses_dir, "demo", manifest, files)
        self.check_fails("WAT ranges [1, 2] and [2, 3] overlap")

    def test_directory_without_manifest_is_ignored(self):
        write_valid_package(self.courses_dir)
        (self.courses_dir / "not-a-course").mkdir()
        (self.courses_dir / "not-a-course" / "mod-01.xml").write_text("<quiz/>", encoding="utf-8")
        code, out, err = self.run_validator([str(self.courses_dir)])
        self.assertEqual(0, code)
        self.assertEqual("", err)

    def test_valid_prototype_passes(self):
        manifest = make_manifest(prototypes=["proto.xml"])
        files = {
            "mod-01.xml": module_xml(["WAT 01.1: x"]),
            "proto.xml": module_xml(["prototype helper"]),
        }
        write_package(self.courses_dir, "demo", manifest, files)
        code, out, err = self.run_validator([str(self.courses_dir)])
        self.assertEqual(0, code)
        self.assertEqual("", err)

    def test_unparseable_prototype_fails(self):
        manifest = make_manifest(prototypes=["proto.xml"])
        files = {
            "mod-01.xml": module_xml(["WAT 01.1: x"]),
            "proto.xml": "<quiz>broken",
        }
        write_package(self.courses_dir, "demo", manifest, files)
        self.check_fails("demo: proto.xml: invalid XML")

    def test_zero_packages_discovered_fails(self):
        code, out, err = self.run_validator([str(self.courses_dir)])
        self.assertEqual(1, code)
        self.assertIn("no course packages discovered", err)


if __name__ == "__main__":
    unittest.main()
