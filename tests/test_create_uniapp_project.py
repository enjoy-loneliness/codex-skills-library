from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "uniapp-project-builder"
    / "scripts"
    / "create_uniapp_project.py"
)
SPEC = importlib.util.spec_from_file_location("create_uniapp_project", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UniAppProjectSecurityTests(unittest.TestCase):
    def test_generated_vite_config_is_localhost_only(self) -> None:
        config = MODULE.vite_config(5100)
        self.assertIn("host: '127.0.0.1'", config)
        self.assertNotIn("host: '0.0.0.0'", config)
        self.assertNotIn("allow: ['..']", config)

    def test_generated_request_does_not_authenticate_absolute_urls(self) -> None:
        request = MODULE.request_js()
        self.assertIn("const isAbsoluteUrl = /^https?:\\/\\//i.test(url);", request)
        self.assertIn("if (!noAuth && !isAbsoluteUrl && appStore.token)", request)

    def test_force_refuses_unmarked_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "unmarked"
            target.mkdir()
            marker = target / "keep.txt"
            marker.write_text("keep", encoding="utf-8")

            with self.assertRaises(SystemExit):
                MODULE.ensure_empty_or_force(target.resolve(), True)

            self.assertTrue(marker.is_file())

    def test_force_replaces_marked_generated_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            creation_parent = Path(temp_dir) / "projects"
            creation_parent.mkdir()
            target = creation_parent / "generated"
            target.mkdir()
            for marker in ("package.json", "manifest.json", "pages.json"):
                (target / marker).write_text("{}", encoding="utf-8")
            (target / "old.txt").write_text("old", encoding="utf-8")

            MODULE.ensure_empty_or_force(target.resolve(), True, creation_parent)

            self.assertTrue(target.is_dir())
            self.assertEqual(list(target.iterdir()), [])

    def test_force_refuses_marked_target_outside_creation_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            creation_parent = root / "projects"
            creation_parent.mkdir()
            target = root / "sibling-project"
            target.mkdir()
            for marker in ("package.json", "manifest.json", "pages.json"):
                (target / marker).write_text("{}", encoding="utf-8")

            with self.assertRaises(SystemExit):
                MODULE.ensure_empty_or_force(target.resolve(), True, creation_parent)

            self.assertTrue(target.is_dir())

    def test_force_refuses_git_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            creation_parent = Path(temp_dir) / "projects"
            creation_parent.mkdir()
            target = creation_parent / "existing-repository"
            target.mkdir()
            (target / ".git").mkdir()
            for marker in ("package.json", "manifest.json", "pages.json"):
                (target / marker).write_text("{}", encoding="utf-8")

            with self.assertRaises(SystemExit):
                MODULE.ensure_empty_or_force(target.resolve(), True, creation_parent)

            self.assertTrue((target / ".git").is_dir())

    def test_force_refuses_current_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir).resolve()
            for marker in ("package.json", "manifest.json", "pages.json"):
                (target / marker).write_text("{}", encoding="utf-8")
            original_cwd = Path.cwd()
            os.chdir(target)
            try:
                with self.assertRaises(SystemExit):
                    MODULE.ensure_empty_or_force(target, True)
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
