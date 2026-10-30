#!/usr/bin/env python3
"""Seam A test suite for check-readme.py static probe CLI.

Tests the CLI contract and all seven checks against real-world derived fixtures:
1. dead local links
2. missing image paths
3. code-fence imbalance
4. badge URL domain sanity
5. boundary-phrase duplicate counting
6. honest-gap signal presence
7. --repo-set cross-repo README skeleton diff
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-readme.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"


def run_probe(*args, cwd=REPO_ROOT):
    cmd = [sys.executable, str(SCRIPT_PATH)] + list(args)
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestCheckReadmeCLI(unittest.TestCase):
    """Test CLI contract and execution."""

    def test_probe_script_exists(self):
        self.assertTrue(SCRIPT_PATH.is_file(), f"Probe script not found at {SCRIPT_PATH}")

    def test_help_flag(self):
        code, out, err = run_probe("--help")
        self.assertEqual(code, 0)
        self.assertIn("usage:", out.lower() + err.lower())

    def test_missing_file_argument(self):
        code, out, err = run_probe()
        self.assertNotEqual(code, 0)

    def test_nonexistent_readme_file(self):
        code, out, err = run_probe("nonexistent_readme_path_12345.md")
        self.assertNotEqual(code, 0)

    def test_nonexistent_manifest_returns_exit_2(self):
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(str(clean_readme), "--repo-set", "nonexistent_manifest_12345.txt")
        self.assertEqual(code, 2)
        self.assertIn("does not exist", err.lower())


class TestCleanFixture(unittest.TestCase):
    """Test that clean fixtures pass with exit 0 and zero findings."""

    def test_clean_fixture_passes(self):
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        clean_root = FIXTURES_DIR / "clean"
        code, out, err = run_probe(str(clean_readme), "--repo-root", str(clean_root))
        self.assertEqual(code, 0, f"Expected 0 exit, got {code}. Output:\n{out}\n{err}")
        self.assertIn("PASS", out)
        self.assertNotIn("FAIL", out)

    def test_clean_zh_fixture_passes(self):
        clean_readme = FIXTURES_DIR / "clean_zh" / "README.md"
        clean_root = FIXTURES_DIR / "clean_zh"
        code, out, err = run_probe(str(clean_readme), "--repo-root", str(clean_root))
        self.assertEqual(code, 0, f"Expected 0 exit, got {code}. Output:\n{out}\n{err}")
        self.assertIn("PASS", out)
        self.assertNotIn("FAIL", out)


class TestCheck1DeadLinks(unittest.TestCase):
    """Check 1: dead local links."""

    def test_dead_local_link_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_dead_link" / "README.md"
        dirty_root = FIXTURES_DIR / "dirty_dead_link"
        code, out, err = run_probe(str(dirty_readme), "--repo-root", str(dirty_root))
        self.assertNotEqual(code, 0, "Expected non-zero exit for dead local link")
        self.assertIn("dead-links", out)
        self.assertIn("docs/nonexistent.md", out)

    def test_link_with_title_and_standalone_image(self):
        """Verify links with titles resolve, and standalone images do not trigger dead-links."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            (td_path / "doc.md").write_text("# Doc\n", encoding="utf-8")
            rm = td_path / "README.md"
            rm.write_text(
                '# Title\n\n[Doc](doc.md "Document Title")\n\n[Angle](<doc.md>)\n\n![Image](missing.png)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(td_path))
            self.assertNotEqual(code, 0)
            self.assertIn("[missing-images]", out)
            self.assertNotIn("[dead-links]", out)

    def test_angle_bracket_dead_link_detected(self):
        """Verify that angle-bracket destinations with missing targets are detected."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            rm = td_path / "README.md"
            rm.write_text(
                '# Title\n\n[Bad](<missing_file.md>)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(td_path))
            self.assertNotEqual(code, 0)
            self.assertIn("[dead-links]", out)
            self.assertIn("missing_file.md", out)

    def test_badge_dead_link_target_detected(self):
        """Verify that [![Badge](img)](dead_local.md) is detected as a dead link."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            rm = td_path / "README.md"
            rm.write_text(
                "# Title\n\n[![Badge](https://img.shields.io/badge/ci-pass-green)](docs/missing.md)\n\n## Limitations\nOut of scope.\n",
                encoding="utf-8"
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(td_path))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("docs/missing.md", out)

    def test_nested_readme_relative_vs_root_relative_link(self):
        """Verify relative destinations in nested READMEs resolve against readme_dir, and leading-slash against repo_root."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            docs = root / "docs"
            docs.mkdir()
            # Root file exists, but does not exist inside docs/
            (root / "root_only.md").write_text("# Root\n", encoding="utf-8")
            (docs / "nested_target.md").write_text("# Nested\n", encoding="utf-8")

            nested_rm = docs / "README.md"
            nested_rm.write_text(
                "# Nested\n\n[Valid Relative](nested_target.md)\n\n[Valid Root](</root_only.md>)\n\n[Broken Relative](root_only.md)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(nested_rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("[dead-links]", out)
            self.assertIn("root_only.md", out)


class TestCheck2MissingImages(unittest.TestCase):
    """Check 2: missing image paths."""

    def test_missing_image_path_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_missing_image" / "README.md"
        dirty_root = FIXTURES_DIR / "dirty_missing_image"
        code, out, err = run_probe(str(dirty_readme), "--repo-root", str(dirty_root))
        self.assertNotEqual(code, 0, "Expected non-zero exit for missing image")
        self.assertIn("missing-images", out)
        self.assertIn("assets/readme/missing_hero.svg", out)

    def test_mixed_remote_and_local_srcset_detected(self):
        """Verify that a missing local candidate in a multi-candidate srcset is detected even if another candidate is remote."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            rm = td_path / "README.md"
            rm.write_text(
                '# Title\n\n<source srcset="https://example.com/logo.png 1x, missing_dark.png 2x">\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(td_path))
            self.assertNotEqual(code, 0)
            self.assertIn("[missing-images]", out)
            self.assertIn("missing_dark.png", out)


class TestCheck3CodeFenceBalance(unittest.TestCase):
    """Check 3: code-fence imbalance."""

    def test_unclosed_code_fence_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_code_fence" / "README.md"
        code, out, err = run_probe(str(dirty_readme))
        self.assertNotEqual(code, 0, "Expected non-zero exit for unclosed fence")
        self.assertIn("code-fences", out)
        self.assertTrue("unclosed" in out.lower() or "imbalance" in out.lower())


class TestCheck4BadgeDomainSanity(unittest.TestCase):
    """Check 4: badge URL domain sanity."""

    def test_placeholder_badge_domain_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_badge_domain" / "README.md"
        code, out, err = run_probe(str(dirty_readme))
        self.assertNotEqual(code, 0, "Expected non-zero exit for badge placeholder domain")
        self.assertIn("badge-domains", out)
        self.assertTrue("todo" in out.lower() or "username" in out.lower() or "placeholder" in out.lower())


class TestCheck5BoundaryDuplicates(unittest.TestCase):
    """Check 5: boundary-phrase duplicate counting."""

    def test_repeated_boundary_phrase_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_boundary_duplicates" / "README.md"
        code, out, err = run_probe(str(dirty_readme))
        self.assertNotEqual(code, 0, "Expected non-zero exit for boundary phrase duplicates")
        self.assertIn("boundary-duplicates", out)
        self.assertIn("out of scope", out.lower())

    def test_same_line_repeated_boundary_phrase_detected(self):
        """Verify that multiple boundary occurrences on the same line are detected."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            rm = Path(td) / "README.md"
            rm.write_text(
                "# Title\n\nFeature A is out of scope and feature B is out of scope.\n\n## Limitations\nSome limits.\n",
                encoding="utf-8"
            )
            code, out, err = run_probe(str(rm))
            self.assertNotEqual(code, 0)
            self.assertIn("boundary-duplicates", out)
            self.assertIn("appears 2 times", out)

    def test_repeated_chinese_boundary_phrase_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_zh" / "README.md"
        code, out, err = run_probe(str(dirty_readme))
        self.assertNotEqual(code, 0, "Expected non-zero exit for Chinese dirty fixture")
        self.assertIn("boundary-duplicates", out)
        self.assertIn("仅供参考", out)


class TestCheck6HonestGapPresence(unittest.TestCase):
    """Check 6: honest-gap signal presence."""

    def test_missing_honest_gap_detected(self):
        dirty_readme = FIXTURES_DIR / "dirty_no_honest_gap" / "README.md"
        code, out, err = run_probe(str(dirty_readme))
        self.assertNotEqual(code, 0, "Expected non-zero exit for missing honest gap signals")
        self.assertIn("honest-gaps", out)
        self.assertTrue("honest" in out.lower() or "completeness" in out.lower() or "gap" in out.lower())


class TestCheck7RepoSetSkeletonDiff(unittest.TestCase):
    """Check 7: --repo-set cross-repo README skeleton diff."""

    def test_repo_set_isomorphism_detected(self):
        manifest = FIXTURES_DIR / "repo_set" / "manifest_isomorphic.txt"
        target_readme = FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md"
        code, out, err = run_probe(str(target_readme), "--repo-set", str(manifest))
        self.assertNotEqual(code, 0, f"Expected non-zero exit for isomorphic repo set. Out:\n{out}")
        self.assertIn("skeleton", out.lower())
        self.assertIn("isomorphism", out.lower())

    def test_repo_set_divergent_passes(self):
        manifest = FIXTURES_DIR / "repo_set" / "manifest_divergent.txt"
        target_readme = FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md"
        code, out, err = run_probe(str(target_readme), "--repo-set", str(manifest))
        self.assertEqual(code, 0, f"Expected 0 exit for divergent repo set. Out:\n{out}\nErr:\n{err}")
        self.assertIn("PASS", out)
        self.assertIn("skeleton", out.lower())

    def test_repo_set_includes_target_readme(self):
        """Verify that the target CLI README is included in the skeleton comparison if not in manifest."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            # Manifest has only 1 repo
            man = td_path / "single_manifest.txt"
            man.write_text(str(FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md") + "\n", encoding="utf-8")
            # Target is repo_iso_b (not in manifest)
            target = FIXTURES_DIR / "repo_set" / "repo_iso_b" / "README.md"
            code, out, err = run_probe(str(target), "--repo-set", str(man))
            # With target included, we have 2 repos that are isomorphic -> should detect isomorphism!
            self.assertNotEqual(code, 0)
            self.assertIn("isomorphic", out.lower())
            self.assertIn("analysis (2 repos)", out)

    def test_unresolved_manifest_entry_reported(self):
        """Verify that manifest entries without a README produce a finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            man = td_path / "bad_manifest.txt"
            man.write_text("nonexistent_repo_dir\n" + str(FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md") + "\n", encoding="utf-8")
            target = FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md"
            code, out, err = run_probe(str(target), "--repo-set", str(man))
            self.assertNotEqual(code, 0)
            self.assertIn("repo-set", out)
            self.assertIn("has no README", out)


class TestStdlibOnly(unittest.TestCase):
    """Ensure scripts/check-readme.py has no third-party dependencies."""

    def test_no_external_imports(self):
        import ast

        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(SCRIPT_PATH))

        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_modules.add(node.module.split(".")[0])

        # Python standard library modules allowlist
        stdlib_names = {
            "__future__", "sys", "os", "re", "pathlib", "urllib", "json", "argparse",
            "difflib", "typing", "collections", "dataclasses", "enum",
            "itertools", "functools", "copy", "string", "hashlib",
            "io", "math", "unicodedata"
        }
        self.assertTrue(imported_modules, "Expected non-empty list of imports from check-readme.py")
        for mod in imported_modules:
            self.assertIn(mod, stdlib_names, f"Module '{mod}' is not in approved stdlib list")


if __name__ == "__main__":
    unittest.main()
