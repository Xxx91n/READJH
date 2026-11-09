#!/usr/bin/env python3
"""Ticket #25 — plain-language review checklist and fixtures.

These tests check fixed artifacts, not prose quality:

1. The manual review items are present in `references/checklist.md` §9.
2. The fixtures hold four sentences, three dashes, and two before/after
   pairs, and every quoted span appears in its recorded source line after
   markdown and whitespace are normalised.
3. The dry-run record holds real before/after spans, the contamination
   findings, and the zero-write evidence.

The author's review of the dry-run is not part of this file. It is a manual
decision, so no test locks its result.
"""

import json
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "plain_language"
CASES_PATH = FIXTURES_DIR / "cases.json"
SOURCES_PATH = FIXTURES_DIR / "SOURCES.md"
CHECKLIST_PATH = REPO_ROOT / "references" / "checklist.md"
DRY_RUN_RECORD_PATH = (
    REPO_ROOT / "docs" / "receipts" / "2026-11-09-plain-language-review-dry-run.md"
)

REQUIRED_CHECKLIST_ITEMS = (
    "One idea per sentence:",
    "Long sentences:",
    "Hard words and banned terms:",
    "Translationese:",
    "Punctuation:",
    "Contamination defense:",
    "Translation handoff:",
    "Translation prompt:",
    "No detector:",
)

REQUIRED_HANDOFF_PHRASES = (
    "all six fields",
    "references/translate-prompt.md",
    "new clean window",
)


def load_cases():
    """Return the fixture data as a dict."""
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def normalise_source_text(text):
    """Strip markdown marks and collapse whitespace before comparing."""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def live_source_span(source, row):
    """Read the cited commit line(s) when the working copy is on this machine.

    Returns None when the repo or commit is not available, so the test can
    skip instead of depending on absolute paths.
    """
    if source["repo"].startswith("Xxx91n/"):
        repo = REPO_ROOT
    else:
        repo = Path(source["repo"])
    if not repo.is_dir():
        return None
    try:
        shown = subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{source['commit']}:{row['file']}"],
            text=True,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    lines = shown.splitlines()
    start = row.get("line", row.get("line_start"))
    end = row.get("line_end", start)
    if start < 1 or end > len(lines) or end < start:
        return None
    return "\n".join(lines[start - 1:end])


class TestChecklistContract(unittest.TestCase):
    """The manual checklist covers the eight items in ticket #25."""

    def test_checklist_has_every_required_item(self):
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        section = text.split("## 9.", 1)[1]
        for item in REQUIRED_CHECKLIST_ITEMS:
            self.assertIn(item, section, f"checklist §9 is missing {item!r}")

    def test_checklist_bans_old_terms_and_avoided_wording(self):
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn("no wording that its entry says to avoid", text)
        self.assertIn("references/de-ai-language.md` §2.4", text)

    def test_checklist_requires_author_choices_for_dashes(self):
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "each dash was kept by the author or replaced with the symbol the author chose",
            text,
        )

    def test_checklist_requires_recorded_contamination_findings(self):
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn("recorded as a `HIGH` finding", text)

    def test_checklist_requires_the_handoff_block_fields(self):
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        for phrase in REQUIRED_HANDOFF_PHRASES:
            self.assertIn(phrase, text)


class TestFixtureContract(unittest.TestCase):
    """The fixtures hold the prototype's four/three/two examples."""

    def setUp(self):
        self.data = load_cases()

    def test_counts_are_four_three_two(self):
        self.assertEqual(self.data["meta"]["counts"], {"sentences": 4, "dashes": 3, "pairs": 2})
        self.assertEqual(len(self.data["sentences"]), 4)
        self.assertEqual(len(self.data["dashes"]), 3)
        self.assertEqual(len(self.data["pairs"]), 2)

    def test_sentence_languages_are_two_en_and_two_zh(self):
        langs = [row["lang"] for row in self.data["sentences"]]
        self.assertEqual(langs.count("en"), 2)
        self.assertEqual(langs.count("zh"), 2)

    def test_dash_languages_are_two_en_and_one_zh(self):
        langs = [row["lang"] for row in self.data["dashes"]]
        self.assertEqual(langs.count("en"), 2)
        self.assertEqual(langs.count("zh"), 1)

    def test_pairs_cover_both_languages(self):
        langs = [row["lang"] for row in self.data["pairs"]]
        self.assertEqual(sorted(langs), ["en", "zh"])

    def test_every_quote_appears_in_its_recorded_source_line(self):
        rows = []
        rows.extend(self.data["sentences"])
        rows.extend(self.data["dashes"])
        rows.extend(self.data["pairs"])
        for row in rows:
            quote = row.get("raw") or row.get("before") or row.get("text")
            self.assertIsNotNone(quote, f"{row['id']} has no quoted span")
            self.assertIn(
                normalise_source_text(quote),
                normalise_source_text(row["source_line"]),
                f"{row['id']} quote does not appear in its recorded source line",
            )

    def test_every_source_is_recorded(self):
        sources = self.data["sources"]
        rows = (
            self.data["sentences"] + self.data["dashes"] + self.data["pairs"]
        )
        for row in rows:
            self.assertIn(row["source"], sources, f"{row['id']} names an unknown source")
            source = sources[row["source"]]
            self.assertIn("commit", source)
            self.assertIn("date", source)
            self.assertRegex(source["commit"], r"^[0-9a-f]{7,40}$")

    def test_source_file_and_line_are_recorded(self):
        for row in self.data["sentences"]:
            self.assertIn("file", row)
            self.assertIn("line", row)
        for row in self.data["dashes"]:
            self.assertIn("file", row)
            self.assertIn("line", row)
        for row in self.data["pairs"]:
            self.assertIn("file", row)
            self.assertTrue("line" in row or ("line_start" in row and "line_end" in row))

    def test_dashes_offer_five_author_choices(self):
        expected = ["comma", "period", "colon", "parentheses", "keep"]
        for row in self.data["dashes"]:
            self.assertEqual(row["options"], expected, f"{row['id']} options changed")
            self.assertIn("—", row["text"])

    def test_pairs_carry_a_before_and_after(self):
        for row in self.data["pairs"]:
            self.assertNotEqual(
                normalise_source_text(row["before"]),
                normalise_source_text(row["after"]),
                f"{row['id']} has no change",
            )
            self.assertTrue(row["after"].strip(), f"{row['id']} has an empty after span")

    def test_sources_file_names_the_commits(self):
        text = SOURCES_PATH.read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for source in self.data["sources"].values():
            self.assertIn(source["commit"], text, "SOURCES.md is missing a commit")
        self.assertIn("prototype/plain-readme", text)
        self.assertIn("None of them was written for this test", flat)
        self.assertIn("after markdown links, bold, and code marks are stripped", flat)

    def test_live_sources_match_when_the_working_copy_is_present(self):
        """When the cited repo is here, the recorded line matches it."""
        rows = []
        rows.extend(self.data["sentences"])
        rows.extend(self.data["dashes"])
        rows.extend(self.data["pairs"])
        checked = 0
        for row in rows:
            span = live_source_span(self.data["sources"][row["source"]], row)
            if span is None:
                continue
            checked += 1
            self.assertEqual(
                normalise_source_text(row["source_line"]),
                normalise_source_text(span),
                f"{row['id']} recorded source line differs from the live commit",
            )
        if checked == 0:
            self.skipTest("none of the cited working copies is on this machine")


class TestDryRunRecord(unittest.TestCase):
    """The dry-run record holds real spans and zero-write evidence."""

    def setUp(self):
        self.text = DRY_RUN_RECORD_PATH.read_text(encoding="utf-8")

    def test_record_names_one_real_repo_at_a_pinned_commit(self):
        self.assertIn("D:/Aworker/EgressAPIKEY", self.text)
        self.assertIn("30e087277381b24715c0a85e44be8bbfe0c6cdd6", self.text)

    def test_record_has_before_and_after_spans(self):
        self.assertGreaterEqual(self.text.count("Before:"), 4)
        self.assertGreaterEqual(self.text.count("After:"), 4)

    def test_record_records_the_contamination_findings(self):
        self.assertIn("README.md:9", self.text)
        self.assertIn("README_CN.md:9", self.text)
        self.assertIn("HIGH", self.text)

    def test_record_records_zero_writes(self):
        self.assertIn(
            "66d37cd9381e051979b2138325d9607fd430db211a753d27dad760c67edbdf7c",
            self.text,
        )
        self.assertIn(
            "84bfc5f931083ddb3d9f5e41f3d74638c74744ece2693e22de707208126ea9f2",
            self.text,
        )
        self.assertIn("empty", self.text)

    def test_record_uses_no_ai_detector_score(self):
        self.assertIn("No AI-detector score", self.text)


if __name__ == "__main__":
    unittest.main()
