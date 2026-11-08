#!/usr/bin/env python3
"""Contract tests for the native-first translation handoff (issue #20).

These tests check two fixed artifacts, not prose quality:
1. references/translate-prompt.md exists and carries all eight required items.
2. SKILL.md carries the fixed handoff block and states that the current
   window never translates.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = REPO_ROOT / "references" / "translate-prompt.md"
SKILL_PATH = REPO_ROOT / "SKILL.md"

# The eight required items from issue #20 (parent spec #16), in order.
REQUIRED_RULE_LABELS = [
    "Native first.",
    "One-to-one structure.",
    "Ask when a term has no good equivalent.",
    "No jargon and no translationese.",
    "Keep facts fixed.",
    "New clean window only.",
    "Natural native wording.",
    "Return a correspondence table.",
]

# Fields every handoff block must fill in (issue #20, parent spec #16).
REQUIRED_HANDOFF_LABELS = [
    "[Native language]:",
    "[Native README]:",
    "[Translate to]:",
    "[Files to translate]:",
    "[Translation prompt]:",
    "[Next step]:",
]

HANDOFF_BLOCK = re.compile(r"```text\n(\[Native language\].*?)\n```", re.DOTALL)


class TestTranslatePromptContract(unittest.TestCase):
    """The prompt file must exist and carry all eight required items."""

    def test_prompt_file_exists(self):
        self.assertTrue(PROMPT_PATH.is_file(), f"Prompt file not found at {PROMPT_PATH}")

    def test_prompt_has_all_eight_rules_in_order(self):
        text = PROMPT_PATH.read_text(encoding="utf-8")
        rules = re.findall(r"^\d+\. \*\*([^*]+)\*\*", text, re.MULTILINE)
        self.assertEqual(
            rules,
            REQUIRED_RULE_LABELS,
            "translate-prompt.md must list the eight required rules in order; "
            f"found {rules!r}",
        )

    def test_prompt_has_fill_in_fields(self):
        text = PROMPT_PATH.read_text(encoding="utf-8")
        for label in (
            "Native language:",
            "Native README:",
            "Translate to:",
            "Files to translate:",
        ):
            self.assertIn(label, text, f"translate-prompt.md is missing {label!r}")

    def test_prompt_requires_a_new_clean_window(self):
        text = " ".join(PROMPT_PATH.read_text(encoding="utf-8").lower().split())
        self.assertIn("new, clean window", text)
        self.assertIn("never in the window that wrote the native readme", text)

    def test_prompt_keeps_code_and_facts_fixed(self):
        text = PROMPT_PATH.read_text(encoding="utf-8")
        self.assertIn("Do not change code, commands, links, versions", text)


class TestHandoffBlockContract(unittest.TestCase):
    """SKILL.md must carry the fixed block and the no-translation rule."""

    def test_skill_references_the_prompt_path(self):
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("references/translate-prompt.md", text)

    def test_handoff_block_is_fixed_and_complete(self):
        text = SKILL_PATH.read_text(encoding="utf-8")
        match = HANDOFF_BLOCK.search(text)
        self.assertIsNotNone(
            match,
            "SKILL.md must contain a fenced ```text handoff block starting with "
            "[Native language]:",
        )
        block = match.group(1)
        for label in REQUIRED_HANDOFF_LABELS:
            self.assertIn(label, block, f"handoff block is missing {label!r}")
        self.assertIn("Open a new, clean window", block)
        self.assertIn("This window never translates.", block)

    def test_handoff_waits_for_approval(self):
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("only after the user approves the native README", text)

    def test_current_window_never_translates(self):
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("It never translates.", text)
        self.assertIn("Never translate in this window", text)


if __name__ == "__main__":
    unittest.main()
