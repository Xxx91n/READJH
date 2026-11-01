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

    def test_path_traversal_outside_repo_root_detected(self):
        """Verify that a link attempting directory traversal outside the repo root is rejected."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text("# Test\n\n[Outside](..)\n\n## Limitations\nNone.\n", encoding="utf-8")
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("..", out)

    def test_angle_bracket_anchor_link_not_flagged(self):
        """Verify that angle-bracket anchor links <#section> are ignored and not flagged as dead links."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text("# Test\n\n[Section](<#limitations>)\n\n## Limitations\nNone.\n", encoding="utf-8")
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0)
            self.assertNotIn("Dead local link", out)
            self.assertIn("- dead-links: PASS", out)

    def test_scheme_relative_urls_ignored(self):
        """Verify that scheme-relative URLs starting with // are treated as external and not dead links."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "doc.md").write_text("# Doc\n", encoding="utf-8")
            rm = root / "README.md"
            rm.write_text("# Test\n\n[External](//github.com/foo/bar)\n[Valid Local](/doc.md)\n\n## Limitations\nNone.\n", encoding="utf-8")
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0)
            self.assertNotIn("Dead local link", out)
            self.assertIn("- dead-links: PASS", out)


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

    def test_srcset_url_with_comma_parsed_correctly(self):
        """Verify that commas inside srcset URLs do not split into false local image candidates."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            rm = td_path / "README.md"
            rm.write_text(
                '# Title\n\n<source srcset="https://cdn.example.org/logo,large.png 1x, missing_dark.png 2x">\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(td_path))
            self.assertNotEqual(code, 0)
            self.assertIn("[missing-images]", out)
            self.assertIn("missing_dark.png", out)
            self.assertNotIn("large.png", out)

    def test_scheme_relative_image_ignored(self):
        """Verify that scheme-relative image sources starting with // are ignored as external."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            (td_path / "local.png").write_text("", encoding="utf-8")
            rm = td_path / "README.md"
            rm.write_text(
                '# Title\n\n<img src="//cdn.example.org/img.png">\n![Local](local.png)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(td_path))
            self.assertEqual(code, 0)
            self.assertNotIn("Missing local image", out)
            self.assertIn("- missing-images: PASS", out)


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

    def test_angle_bracket_placeholder_badge_detected(self):
        """Verify that placeholder badge URLs enclosed in angle brackets are properly detected."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# Test\n\n[![Status](<https://example.com/badge.svg>)](<https://example.com>)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("badge-domains", out)
            self.assertIn("example.com", out)


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

    def test_manifest_duplicate_entries_deduplicated(self):
        """Verify that duplicate entries in manifest do not trigger self-comparison false positives."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            man = td_path / "dup_manifest.txt"
            div_c = str(FIXTURES_DIR / "repo_set" / "repo_div_c" / "README.md")
            iso_a = str(FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md")
            # Write duplicate paths
            man.write_text(f"{div_c}\n{div_c}\n{iso_a}\n", encoding="utf-8")
            target = FIXTURES_DIR / "clean" / "README.md"
            code, out, err = run_probe(str(target), "--repo-set", str(man))
            # Clean + div_c + iso_a are divergent, duplicates should be filtered out
            self.assertEqual(code, 0)
            self.assertNotIn("isomorphic", out.lower())
            self.assertIn("analysis (3 repos)", out)


class TestChecksSubset(unittest.TestCase):
    """--checks CLI contract: subset selection, empty rejection, dedup."""

    def test_comma_only_checks_rejected(self):
        """--checks ,, selects no checks and must exit 2, not PASS."""
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(str(clean_readme), "--repo-root", str(FIXTURES_DIR / "clean"), "--checks", ",,")
        self.assertEqual(code, 2, f"Expected exit 2 for empty selection, got {code}. Out:\n{out}")
        self.assertIn("no checks", err.lower())

    def test_empty_string_checks_rejected(self):
        """--checks '' (explicit empty) is a selection error, exit 2."""
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(str(clean_readme), "--repo-root", str(FIXTURES_DIR / "clean"), "--checks", "")
        self.assertEqual(code, 2)

    def test_unknown_check_name_rejected(self):
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(str(clean_readme), "--repo-root", str(FIXTURES_DIR / "clean"), "--checks", "dead-links,bogus")
        self.assertEqual(code, 2)
        self.assertIn("bogus", err)

    def test_subset_runs_only_selected(self):
        """--checks dead-links,missing-images runs exactly those two; others not evaluated."""
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(
            str(clean_readme), "--repo-root", str(FIXTURES_DIR / "clean"),
            "--checks", "dead-links,missing-images",
        )
        self.assertEqual(code, 0, f"Out:\n{out}\nErr:\n{err}")
        self.assertIn("- dead-links: PASS", out)
        self.assertIn("- missing-images: PASS", out)
        self.assertIn("Checks not selected: code-fences", out)
        self.assertNotIn("- honest-gaps: PASS", out)
        self.assertNotIn("- code-fences: PASS", out)

    def test_default_still_runs_all(self):
        """Omitting --checks keeps the default: every check evaluated."""
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(str(clean_readme), "--repo-root", str(FIXTURES_DIR / "clean"))
        self.assertEqual(code, 0)
        for chk in ("dead-links", "missing-images", "code-fences", "badge-domains", "boundary-duplicates", "honest-gaps"):
            self.assertIn(f"- {chk}: PASS", out)

    def test_subset_with_repo_set(self):
        """--repo-set still runs when a --checks subset is given."""
        manifest = FIXTURES_DIR / "repo_set" / "manifest_divergent.txt"
        target_readme = FIXTURES_DIR / "repo_set" / "repo_iso_a" / "README.md"
        code, out, err = run_probe(
            str(target_readme), "--repo-set", str(manifest),
            "--checks", "dead-links",
        )
        self.assertEqual(code, 0, f"Out:\n{out}\nErr:\n{err}")
        self.assertIn("- repo-set: PASS", out)
        self.assertNotIn("- honest-gaps: PASS", out)

    def test_duplicate_names_deduped(self):
        """--checks dead-links,dead-links is accepted once, not an error."""
        clean_readme = FIXTURES_DIR / "clean" / "README.md"
        code, out, err = run_probe(
            str(clean_readme), "--repo-root", str(FIXTURES_DIR / "clean"),
            "--checks", "dead-links,dead-links",
        )
        self.assertEqual(code, 0, f"Out:\n{out}\nErr:\n{err}")
        self.assertIn("- dead-links: PASS", out)


class TestFragmentLinks(unittest.TestCase):
    """dead-links fragment validation: same-file and cross-file anchors."""

    def test_same_file_broken_fragment_detected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Gone](#missing-section)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("missing-section", out)

    def test_same_file_valid_fragment_passes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#limitations)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_cross_file_broken_fragment_detected(self):
        """file.md#anchor: file exists but the anchor does not."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "doc.md").write_text("# Doc\n\n## Exists\n", encoding="utf-8")
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Bad](doc.md#gone-anchor)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("gone-anchor", out)

    def test_cross_file_valid_fragment_passes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "doc.md").write_text("# Doc\n\n## Target Section\n", encoding="utf-8")
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Good](doc.md#target-section)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_explicit_curly_anchor_id(self):
        """{#custom} is not a GitHub-rendered id; #custom must FAIL, the
        GitHub slug of the full heading text must pass."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Bad](#custom)\n\n## Section Name {#custom}\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("#custom", out)

    def test_curly_id_github_slug_passes(self):
        """GitHub slugs the {#id} text into the anchor: #section-name-custom."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Good](#section-name-custom)\n\n## Section Name {#custom}\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_fenced_a_id_not_a_real_anchor(self):
        """An <a id> inside a fenced code block is rendered code, not an anchor."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[Bad](#install)\n\n```html\n<a id="install"></a>\n```\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("install", out)

    def test_commented_a_id_not_a_real_anchor(self):
        """An id attribute inside an HTML comment does not render an anchor."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[Bad](#ghost)\n\n<!-- <a id="ghost"></a> -->\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("dead-links", out)
            self.assertIn("ghost", out)

    def test_duplicate_heading_suffix_anchors(self):
        """Duplicate headings get GitHub -1/-2 suffixes; links to them pass."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[First](#runtime-view)\n[Second](#runtime-view-1)\n\n## Runtime view\n\nEnglish.\n\n## Runtime View\n\n中文.\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_duplicate_heading_missing_suffix_fails(self):
        """A -2 anchor with only two same-slug headings fails."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Bad](#runtime-view-2)\n\n## Runtime view\n\n## Runtime view\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("runtime-view-2", out)

    def test_indented_atx_heading_slug(self):
        """ATX headings indented 1-3 spaces still produce anchors."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#setup)\n\n   ## Setup\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_setext_heading_slug(self):
        """Setext headings (text + --- underline) produce anchors."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#setup)\n\nSetup\n-----\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_underscore_preserved_in_slug(self):
        """Underscores inside code spans and names are kept in anchors."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[A](#my_func-internals)\n[B](#_private-notes)\n\n## `my_func` internals\n\n## _private notes\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_html_a_id_anchor_resolves(self):
        """<a id='...'> anchors count as valid fragment targets."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<a id="install"></a>\n\n[Go](#install)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_cjk_heading_slug(self):
        """CJK heading slug: GitHub keeps CJK chars and slugs {#id} text into
        the anchor — #能力矩阵-capability-matrix."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#能力矩阵-capability-matrix)\n\n## 能力矩阵 {#capability-matrix}\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_angle_bracket_anchor_still_not_flagged(self):
        """<#section> in angle brackets with valid anchor passes (regression)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# Test\n\n[Section](<#limitations>)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0)
            self.assertIn("- dead-links: PASS", out)

    def test_data_id_attribute_is_not_an_anchor(self):
        """<span data-id="ghost"> has no id attribute — #ghost must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[Bad](#ghost)\n\n<span data-id="ghost"></span>\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("ghost", out)

    def test_plain_text_id_equals_is_not_an_anchor(self):
        """Bare text id="ghost" outside any HTML tag is not an anchor."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[Bad](#ghost)\n\nSet id="ghost" in your config.\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("ghost", out)

    def test_inline_comment_in_heading_keeps_anchor(self):
        """## Setup <!-- note --> still renders a #setup target."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#setup)\n\n## Setup <!-- internal note -->\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_unclosed_comment_inside_fence_does_not_swallow(self):
        """An unclosed <!-- inside a fenced block is code, not a comment —
        headings after the fence still produce anchors."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#real)\n\n```html\n<!-- unclosed example\n```\n\n## Real\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_digit_led_setext_heading_slug(self):
        """2026 Overview + === underline is a valid Setext heading."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#2026-overview)\n\n2026 Overview\n=============\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_ordered_list_marker_not_setext_text(self):
        """'1. Item' + === is a list marker line, not heading text."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Bad](#1-item)\n\n1. Item\n=======\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("1-item", out)

    def test_commented_out_dead_link_not_flagged(self):
        """A dead link inside an HTML comment is not rendered — no finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n<!-- [Gone](missing.md) -->\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_id_inside_attribute_value_is_not_an_anchor(self):
        """title='id="ghost"' is a value, not an id attribute — must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Bad](#ghost)\n\n<span title='id=\"ghost\"'></span>\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("ghost", out)

    def test_div_name_attribute_is_not_an_anchor(self):
        """name= anchors only on <a>; <div name='ghost'> must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[Bad](#ghost)\n\n<div name="ghost"></div>\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("ghost", out)

    def test_comment_marker_inside_inline_code_does_not_swallow(self):
        """`<!--` inside backticks is literal — a real dead link after it
        must still FAIL (no false PASS)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nType `<!--` to start a comment.\n\n[Bad](missing.md)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_comment_marker_inside_multibacktick_code(self):
        """Same guard for `` ... `` spans — dead link after still FAILs."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nExample ``<!-- x -->`` inline.\n\n[Bad](missing.md)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_link_inside_inline_code_not_flagged(self):
        """`[x](missing.md)` inside backticks is rendered code — no finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nUse `[Example](missing.md)` as the syntax.\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_image_inside_inline_code_not_flagged(self):
        """`![x](missing.png)` inside backticks is rendered code — no finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nUse `![alt](missing.png)` as the syntax.\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "missing-images"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- missing-images: PASS", out)

    def test_a_id_inside_inline_code_not_an_anchor(self):
        """`<a id="x">` inside backticks is code — the fragment must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\nMarkup: `<a id="ghost"></a>`\n\n[Bad](#ghost)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("ghost", out)

    def test_marker_led_setext_heading_slug(self):
        """**Note** + === is a valid Setext heading — #note resolves."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#note)\n\n**Note**\n========\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_dash_word_setext_heading_slug(self):
        """-foo + === is Setext text (- is not followed by a space)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#-foo)\n\n-foo\n====\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_unordered_list_marker_not_setext_text(self):
        """'- Item' + === is a list marker line, not heading text."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Bad](#item)\n\n- Item\n======\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertNotEqual(code, 0)
            self.assertIn("#item", out)

    def test_mixed_case_fragment_resolves(self):
        """#Limitations resolves to ## Limitations — GitHub matches
        fragments case-insensitively."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#Limitations)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(str(rm), "--repo-root", str(root))
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_escaped_backticks_do_not_open_code_span(self):
        """\\`[x](missing.md)\\` renders a real link — the dead link FAILs."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n\\`[Bad](missing.md)\\`\n\\`![M](missing.png)\\`\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root),
                "--checks", "dead-links,missing-images",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)
            self.assertIn("missing.png", out)

    def test_unmatched_backtick_cannot_pair_across_paragraphs(self):
        """A stray ` in one paragraph cannot pair with ` in a later one —
        the links/images between them stay rendered and FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n`unmatched\n\n[Bad](missing.md)\n![M](missing.png)\n\n`later`\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root),
                "--checks", "dead-links,missing-images",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)
            self.assertIn("missing.png", out)

    def test_unmatched_backtick_does_not_stop_later_spans(self):
        """After an unmatched `, a later ``...`` code span is still
        recognized — its code example is not a real link (no false FAIL)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n`unmatched\n\nUse ``[Example](missing.md)`` as syntax.\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_fence_markers_inside_comments_do_not_pair(self):
        """``` inside two closed HTML comments is comment text — it must
        not pair up and blank the real links between the comments."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n<!--\n```\n-->\n\n[Bad](missing.md)\n![M](missing.png)\n\n<!--\n```\n-->\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root),
                "--checks", "dead-links,missing-images,code-fences",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)
            self.assertIn("missing.png", out)

    def test_escaped_comment_marker_is_literal(self):
        """\\<!-- is an escaped '<', not a comment — later links stay real."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n\\<!-- hidden -->\n\n[Bad](missing.md)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_bare_unclosed_fence_detected(self):
        """``` + body + EOF: the opener must not self-close — code-fences
        reports the unclosed fence."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n```\nexample\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "code-fences"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("code-fences", out)

    def test_bare_fence_hides_code_body(self):
        """``` ... ``` bare fences: the link/image inside is code, not a
        real resource — no false FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n```\n[Example](missing.md)\n![Example](missing.png)\n```\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root),
                "--checks", "dead-links,missing-images,code-fences",
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_closing_fence_at_eof_without_newline(self):
        """A closing ``` as the final line (no trailing LF) still closes
        the fence — no false unclosed finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n```text\n[Example](missing.md)\n```",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root),
                "--checks", "dead-links,code-fences",
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_backslash_before_span_closer_is_literal(self):
        """`x\\` closes at the second backtick — backslashes do not escape
        inside a code span, so the real dead link after it FAILs."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n`x\\` [Bad](missing.md) ![M](missing.png) `y`\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root),
                "--checks", "dead-links,missing-images",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)
            self.assertIn("missing.png", out)

    def test_span_cannot_pair_across_heading_boundary(self):
        """A stray ` in a paragraph cannot pair with ` after a heading —
        the heading is a separate block, so it stays a heading and its
        anchor resolves (no swallowed heading → false FAIL)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n`unmatched text\n## Real Heading\nmore ` text\n\n[Go](#real-heading)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_span_cannot_pair_across_setext_equals(self):
        """`unmatched / === / link `x` — the === line is a Setext underline
        (new block), so the stray ` can't hide the real dead link."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n`unmatched\n===\n[Bad](missing.md) `later`\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_ordered_marker_2_does_not_break_span(self):
        """'2.' cannot interrupt a paragraph (only '1.' can per GFM) — a
        multi-line span containing a 2.-led line stays code: no finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nUse `example\n2. [Example](missing.md)\nend` here.\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_ordered_marker_1_breaks_span(self):
        """'1.' CAN interrupt a paragraph — the stray ` pairs nothing, so
        the real link on the 1. line is checked and FAILs."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nUse `example\n1. [Bad](missing.md)\nend` here.\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_unclosed_inline_comment_is_literal(self):
        """An inline <!-- (not at a line start) that never closes within
        its block is literal text — the real link after it FAILs."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nText <!-- unclosed inline\n\n[Bad](missing.md)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_multiline_inline_comment_within_block_still_hides(self):
        """A mid-line comment that DOES close within its block still
        hides its contents — commented dead link produces no finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\nText <!-- [Gone](missing.md) --> more\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_img_tag_heading_slug(self):
        """## <img src=...> Features renders as 'Features' — #features
        resolves; the img tag text never enters the slug."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[Go](#features)\n\n## <img src="icon.png" width="20"> Features\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_autolink_heading_slug(self):
        """## Setup <https://example.com> — the autolink renders as link
        text 'https://example.com' → slug 'setup-httpsexamplecom'."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#setup-httpsexamplecom)\n\n## Setup <https://example.com>\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_comment_block_tail_heading_not_markdown(self):
        """<!-- note --> ## Ghost: text after a block comment's --> is raw
        HTML, not a heading — #ghost must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n<!-- note --> ## Ghost\n\n[Go](#ghost)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("ghost", out)

    def test_comment_block_tail_link_not_markdown(self):
        """<!-- note --> [x](missing.md): the tail is raw HTML — the
        pseudo-link there produces no dead-links finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n<!-- note --> [Example](missing.md)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_comment_block_tail_anchor_still_counts(self):
        """<!-- note --> <a id="real">: a real HTML anchor in the tail is
        still a valid fragment target — #real resolves."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<!-- note --> <a id="real"></a>\n\n[Go](#real)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_code_span_underscores_kept_in_slug(self):
        """## `__init__` renders underscores literally → #__init__."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n[Go](#__init__)\n\n## `__init__`\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- dead-links: PASS", out)

    def test_comment_block_tail_html_link_is_real(self):
        """<!-- note --> <a href="missing.md">API</a>: the tail is raw
        HTML — a real <a> there is a real link and must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<!-- note --> <a href="missing.md">API</a>\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_comment_block_tail_html_image_is_real(self):
        """<!-- note --> <img src="missing.png">: a real <img> in the tail
        is a real image reference and must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<!-- note --> <img src="missing.png">\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "missing-images"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.png", out)

    def test_comment_block_tail_source_srcset_is_real(self):
        """<!-- note --> <source srcset="missing.png 1x">: srcset
        candidates in the tail are checked and must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<!-- note --> <source srcset="missing.png 1x">\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "missing-images"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.png", out)

    def test_comment_block_tail_markdown_image_still_invisible(self):
        """<!-- note --> ![x](missing.png): markdown syntax in the tail is
        not parsed — no missing-images finding."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n<!-- note --> ![x](missing.png)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "missing-images"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            self.assertIn("- missing-images: PASS", out)

    def test_unclosed_block_comment_reported(self):
        """An unclosed line-start <!-- hides the rest of the document on
        GitHub — code-fences must FAIL, not silently pass."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<!-- note\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "code-fences"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("Unclosed HTML comment", out)

    def test_backtick_info_string_is_not_a_fence(self):
        """A line like ```x``` is an inline code span, not a fence opener:
        code-fences must PASS and the following dead link must still FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n```x``` inline\n\n[dead](missing.md)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "code-fences"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("missing.md", out)

    def test_explicit_id_does_not_shift_heading_slugs(self):
        """<a id="setup"> plus two '## Setup' headings: GitHub generates
        #setup and #setup-1 — #setup-1 resolves and #setup-2 must FAIL
        (the slugger deduplicates against heading slugs only)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<a id="setup"></a>\n\n## Setup\nx\n\n## Setup\ny\n\n'
                'See [a](#setup-1) and [b](#setup-2).\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("#setup-2", out)
            self.assertNotIn("no anchor '#setup-1'", out)

    def test_angle_destination_with_title_fragment(self):
        """[x](<file.md#frag> "Title"): the fragment is 'frag', not 'frag>' —
        a valid fragment must PASS, not false-FAIL on the trailing '>'."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            doc = root / "doc.md"
            rm.write_text(
                '# T\n\nSee [x](<doc.md#frag> "Title").\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            doc.write_text("# Frag\n", encoding="utf-8")
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_angle_fragment_link_with_title(self):
        """[x](<#limitations> "T"): an anchor-only <...> destination with a
        title is still a same-document fragment — resolves, not dead."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\nSee [x](<#limitations> "T").\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_angle_fragment_link_with_title_dead(self):
        """[x](<#nope> "T"): the same shape still FAILs when the fragment
        does not exist — title stripping must not skip validation."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\nSee [x](<#nope> "T").\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("#nope", out)

    def test_angle_image_src_with_title(self):
        """![x](<i.png> "t"): an angle-bracket image src with a title resolves
        like a normal src — PASS, not a false missing-images FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            (root / "i.png").write_bytes(b"x")
            rm.write_text(
                '# T\n\n![x](<i.png> "t")\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "missing-images"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_angle_badge_url_with_title_still_validated(self):
        """[![x](<//localhost/badge> "t")](y): a scheme-relative badge URL in
        angle brackets is still host-validated — localhost must FAIL."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n[![x](<//localhost/badge> "t")](https://example.org)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "badge-domains"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("localhost", out)

    def test_line_start_span_wrapping_link_and_image(self):
        """```[Example](missing.md) ![M](missing.png)``` on its own line is
        a code span (a backtick info string cannot contain backticks), so
        the sample link/image inside are code, not real resources — PASS."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n```[Example](missing.md) ![M](missing.png)```\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links,missing-images"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_line_start_span_matches_prefixed_shape(self):
        """The same span with a 'Use ' prefix already stayed code; the
        line-start shape must behave identically (no path findings)."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\nUse ```[Example](missing.md) ![M](missing.png)```\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links,missing-images"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_line_start_span_does_not_mask_real_links(self):
        """```[Example](missing.md)``` followed by a real dead link: only
        the real link is reported — the span hides its own code sample
        but must not swallow or hide what follows."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n```[Example](missing.md)```\n\n[real](real-missing.md)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links,missing-images"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("real-missing.md", out)
            self.assertNotIn("'missing.md'", out)

    def test_combining_marks_kept_in_slug(self):
        """## हिन्दी: GitHub's slugger keeps Unicode combining marks — the
        #हिन्दी link resolves and the mark-stripped #हनद variant fails.
        A bare [^\\w\\- ] filter would strip the marks and invert both."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n## हिन्दी\nx\n\n[a](#हिन्दी) and [b](#हनद).\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("हनद", out)
            self.assertNotIn("'#हिन्दी'", out)

    def test_stray_less_than_does_not_hide_anchor(self):
        """'Node < 20' before <a name="legacy">: a tag match must not span
        across the stray '<' to the tag's '>' — the anchor is still
        registered and [x](#legacy) resolves."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\nNode < 20 is unsupported.\n\n<a name="legacy"></a>\n\n'
                '[x](#legacy)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_quoted_less_than_in_attribute_keeps_anchor(self):
        """<a title="Node < 20" id="legacy">: a '<' inside a quoted
        attribute value is legal raw-HTML — the tag is still one tag, the
        id registers, and [x](#legacy) must resolve."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<a title="Node < 20" id="legacy"></a>\n\n[x](#legacy)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_quoted_less_than_single_quotes_keeps_anchor(self):
        """<a name='legacy' title='a < b'>: same protection with
        single-quoted values — the anchor registers."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                "# T\n\n<a name='legacy' title='a < b'></a>\n\n[x](#legacy)\n\n## Limitations\nNone.\n",
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_quoted_less_than_multiline_tag_keeps_anchor(self):
        """A tag spanning newlines with '<' inside a quoted attribute is
        still one tag — the id registers."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<a title="Node < 20"\n   id="legacy"></a>\n\n[x](#legacy)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertEqual(code, 0, f"Out:\n{out}")

    def test_attribute_value_still_cannot_fake_anchor(self):
        """<span title='id="ghost"'>: the quote-aware boundary must not
        resurrect the old attr-value forgery — #ghost still FAILs."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rm = root / "README.md"
            rm.write_text(
                '# T\n\n<span title=\'id="ghost"\'></span>\n\n[x](#ghost)\n\n## Limitations\nNone.\n',
                encoding="utf-8",
            )
            code, out, err = run_probe(
                str(rm), "--repo-root", str(root), "--checks", "dead-links"
            )
            self.assertNotEqual(code, 0)
            self.assertIn("#ghost", out)


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
