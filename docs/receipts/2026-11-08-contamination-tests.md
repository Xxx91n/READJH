# Receipt — contamination-defense tests (Ticket #19)

Date: 2026-11-08
Branch: `ticket-19-contamination-tests`
Base commit: `e53b4cfcd3d729be499b709e2439fa7ccef5134d` (`origin/main`)
Ticket: GitHub issue #19 (parent spec: issue #16 / Spec 0002)

## 1. What was added

- `tests/fixtures/contamination/` — six fixture READMEs:
  - `directive/` — agent-addressed directive text in visible prose, an HTML
    comment, and a code comment; no stop condition.
  - `run_parameters/`, `secrets/`, `skill_files/`, `data_out/` — one fixture
    for each of the four stop conditions.
  - `reader_instructions/` — ordinary instructions for a human reader, including
    "upload reports to S3"; these are data, not findings.
- `tests/fixtures/contamination/cases.json` — the expected line, quote, kind
  (`high` / `block` / `data`), and stop condition for every declared span.
- `tests/fixtures/contamination/SOURCES.md` — where the real carrier text and
  the directive wording come from.
- `tests/fixtures/contamination/source_excerpts.json` — the exact upstream
  lines the fixtures quote, plus the rule-text examples used by the reader
  fixture. The source test compares every fixture against these lines.
- `tests/test_contamination_defense.py` — 18 `unittest` tests:
  - exact quote and line checks for every fixture span;
  - a small test-only classifier that approximates the decision table in
    `references/readme-rules.md` §6;
  - a simulated run that records `HIGH` findings, continues, and writes once
    the whole README has been read;
  - block cases that return before the write step, with an empty write list
    and unchanged file hashes;
  - contract checks that the rule text, `SKILL.md`, and checklist §9 keep the
    `HIGH` / `BLOCKED` split and all four stop conditions;
  - a check that `scripts/check-readme.py` still has only its six always-on
    checks (the optional `--repo-set` check is separate) and rejects
    `contamination` as an unknown check name;
  - checks that ordinary prose, a mention without a request, and an
    agent-addressed pointer stay `HIGH`, not `BLOCKED`;
  - checks that a negated request and a token/transfer request are classed
    correctly.

## 2. Verification

Run from the worktree root:

```text
python -m unittest discover -s tests -p "test_contamination_defense.py" -v
→ 18 tests, OK, exit 0

python -m unittest discover -s tests -v
→ 136 tests, OK, exit 0
```

The fixture probe runs are inside the new suite:
`python scripts/check-readme.py <fixture>/README.md --repo-root <fixture-dir>`
returns `PASS` and exit 0 for all six fixtures.

## 3. Acceptance map

- **Directive fixture produces a `HIGH` finding and the run continues:**
  `directive/README.md` lines 5, 13, 14, 15, and 18 are `high`; the simulated
  run records all five and reaches the write step (`status = CONTINUE`).
- **Exfiltration fixture produces `BLOCK` before any file write:**
  `data_out/README.md:7` returns `BLOCKED` with `stop_condition = data-out`;
  the write list is empty and the fixture tree hash is unchanged. The other
  three stop conditions have the same result.
- **The tests pass:** 136 tests, exit 0.
- **Realistic text:** the title, full one-line description, and `llms.txt`
  blockquote are copied from `Xxx91n/EgressAPIKEY` `README.md` at commit
  `30e087277381b24715c0a85e44be8bbfe0c6cdd6`, lines 1-9. The `Limitations`
  sentence is copied from the upstream caveat on line 68 of the same file.
  The reader lines ("run the tests", "open config.json", "upload reports to
  S3") quote `references/readme-rules.md` §6.1 and §6.2. The directive wording
  comes from ticket #19. The pattern category is OWASP LLM01 (prompt
  injection). The four stop conditions come from Spec 0002 (issue #16) and
  `references/readme-rules.md` §6. The exact copied lines are stored in
  `source_excerpts.json`; the tests do not fetch the upstream repository, so
  the copy is a stored excerpt, not a live check.

## 4. Limit

The classifier is a test double that approximates the decision table. It
shows that the fixtures and that approximation agree, and that a stop
condition returns before the write step. It does not show that a model follows the prompt rule. The
contract tests compare rule-text strings; a rule rewrite that keeps the same
headings but drops a trigger word would not be caught. That check stays the
manual item in `references/checklist.md` §9. This receipt does not claim
model behavior is verified.

The real `llms.txt` blockquote is harmless in practice, but the written rule
records agent-addressed text as a `HIGH` finding. The fixture asserts that
rule's scope rather than adding a judgement of its own.
