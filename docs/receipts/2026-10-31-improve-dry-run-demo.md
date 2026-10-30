# Receipt — improve `--dry-run` demo (Ticket #6 acceptance)

Date: 2026-10-31 · Skill state: `SKILL.md` @ commit `4e56969` (ticket-6-improve-rewrite-language)
Demo executor: READJH pipeline executed manually per `SKILL.md` §3 phases, `--dry-run` modifier.

## Sample

Real-world sample, not invented: `D:\Aworker\6F\README.md` at 6F commit
`cbfa75374a077729ddc6d8dab47f2bb194c4a3a7`, copied to a non-Git fixture
directory so the demo touches nothing in the source repository:

```text
fixture: C:\Users\Administrator\.zcode\tmp\readjh-demo-fixture\README.md
baseline sha256: 3246796f40215ebc2d2ab6884e2f96e5a3c9f410a048ffa139077b70e46b859b
```

## ROUTE (locked parameters)

- Run mode: `improve` + `--dry-run` (plan only, zero writes expected).
- Target: `<fixture>/README.md`; `<repo-root>`: the fixture directory
  (parent-of-readme resolution; `git rev-parse --is-inside-work-tree` → not a
  repository).
- Git state: non-Git `<repo-root>`, single file → `.bak` rule (RESTRUCTURE
  step 6) **would apply** on a real run; in `--dry-run` no `.bak` is created.
- Intensity tier: `standard` (no verified author voice in the sample).
- Bilingual: the sample references a `README.zh-CN.md` companion (absent in
  the fixture) — lockstep noted in the plan.
- Pointer contract (both executors, trusted root #3 `~/.agents/skills/`):
  - `readme-crafter-skill`: `SKILL.md`, `references/repo-integrity.md`,
    `scripts/scan-project.py`, `scripts/scan_project_readme.py`,
    `scripts/scan_project_support.py` — all present (5/5 OK).
  - `writing-humanize`: `SKILL.md`, `references/patterns.md`,
    `agents/openai.yaml` — all present (3/5→3/3 OK); frontmatter `name: writing-humanize`.
    Installed 2026-10-31 per `UPSTREAM.md` install action (clone
    `risadams/ink-and-agency` @ `e1f0a00e06d55c00502e0ccbea79ab453e7fb118`,
    junction to canonical name).

## TRUTH receipts

```text
python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py <fixture>
→ exit 0 (scan complete; "missing local files" findings recorded)
```

Claim checks in the fixture context: `version 0.3.0`, `Node >= 22.18`,
marketplace install commands, badge rows — no manifests/LICENSE/workflows
exist in the single-file fixture, so repository-native verification is
deferred to the full-repo run (`6F` context). Recorded as fixture-context
caveat, not as README defects.

## RESTRUCTURE plan (dry-run — listed, not executed)

1. Over-completeness migrations (`references/readme-rules.md` §4.1), each with
   a migration-ledger entry:

   | Moved span (heading, lines) | Destination file |
   |---|---|
   | `## Runtime view` (lines 111–120) | `docs/architecture.md` |
   | `## Ownership boundary` (lines 122–127) | `docs/authority.md` |
   | `## Upstream components` + lock-discipline note (lines 97–109) | `docs/upstream-policy.md` |
   | `## Contracts` (lines 129–133) | `docs/upstream-policy.md` |
   | `0.x semantics` paragraph (line 49) | `docs/versioning.md` (already exists — merge, no new file) |

2. Self-attestation convergence: preview status restated at lines 29 (badge),
   33 (NOTE), 37, 47, and `## Honesty notes` (183–187, "Preview means
   preview"). Plan: converge to the single authoritative NOTE block; delete
   `## Honesty notes`, merging unique facts (badge mounting date, line 185)
   once.
3. Generation traces: `<!-- acknowledgments:start — GENERATED ... -->`
   (lines 166–181) — whitelist check requires the owning script
   (`engine/scripts/gen-acknowledgments.mjs`); absent in the fixture, present
   in the real repo → kept in full-repo context, flagged in fixture-only runs.
4. `.bak` rule: non-Git fixture → `README.md.bak` **would** be created before
   the first write on a real (non-dry) run.

## LANGUAGE plan (Phase 4 step 5, `standard` tier, dry-run)

Invocation receipts: `writing-humanize/SKILL.md` + `references/patterns.md`
read from trusted root; suppression targets confirmed in upstream text —
`PERSONALITY AND SOUL` (Step 5, line 61) and `Self-Evolve Loop` (line 193)
both suppressed; supplement rules `references/de-ai-language.md` §§1–6 +
`references/readme-rules.md` §§1–5 read into context. No file outside
`<repo-root>` written; no personality/gap/story added.

| Anchor | Transform | Before → after shape |
|---|---|---|
| line 18 | abstract-noun chain → concrete referents | "self-built moat and glue" → name the actual artifacts (adjudication protocol, fact-table schema, gates) |
| line 26 | defensive → `fact + link` (de-ai-language §4) | "Frankness — … label themselves" → one scope sentence + link to disclosure block |
| line 33 | split overloaded boundary sentence; freeze-zone spans (`claude plugin marketplace add Xxx91n/6F`, `/plugin install 6f@xxx91n`) stay byte-identical | one boundary per sentence |
| line 47 | self-attestation → plain statement | "Honest preview labeling is a decision, not decoration" → state where `preview_disclosure` lives |
| lines 183–187 | (RESTRUCTURE) section delete; LANGUAGE keeps remaining unique facts once | see convergence above |

Freeze-zone inventory for this sample: badge rows (8–14), fenced blocks
(55–58, 66–74, 80–85, 113–120, 156–160), script-owned acknowledgments block
(166–181), inline zh command/path spans.

## VERIFY receipts

```text
python -B scripts/check-readme.py <fixture>/README.md --repo-root <fixture>
→ exit 1 — FAIL: 24 blocking findings, all dead-links (22) + missing-images (2),
  all caused by the single-file fixture (LICENSE, README.zh-CN.md, engine/,
  docs/, examples/, .github/ absent). checks 1–7: code-fences PASS,
  badge-domains PASS, boundary-duplicates PASS, honest-gaps PASS,
  repo-set N/A.
Baseline re-compare: sha256 unchanged (3246796f…), directory listing = [README.md]
→ zero writes; no `.bak`, no `__pycache__`.
```

## Delivery report

```text
[Conclusion]: FAIL — improve --dry-run on <fixture>/README.md (intensity tier: standard); plan produced, zero writes; 24 blocking probe findings, all fixture-context dead links/images.
[Receipts]: scan-project.py exit 0; check-readme.py exit 1 (24 findings, fixture-context); writing-humanize resolved 3/3 required files, both suppressions held; baseline sha256 3246796f… matched pre/post; migration ledger + wording plan recorded above.
[Residual risk]: fixture-context findings vanish in the full 6F repo; claims (version, Node floor, marketplace commands) need manual verification against the real repository before any non-dry improve run.

| Moved span (heading, `<readme>` lines) | Destination file |
|---|---|
| (planned — dry-run) `## Runtime view` (111–120) | `docs/architecture.md` |
| (planned — dry-run) `## Ownership boundary` (122–127) | `docs/authority.md` |
| (planned — dry-run) `## Upstream components` (97–109) | `docs/upstream-policy.md` |
| (planned — dry-run) `## Contracts` (129–133) | `docs/upstream-policy.md` |
| (planned — dry-run) `0.x semantics` (49) | `docs/versioning.md` |
```

## Acceptance mapping

- `SKILL.md` covers all three modes plus `--dry-run` — §3 spine + §5 summary table.
- LANGUAGE phase names the pointer-contract invocation and supplement files — §3 Phase 4 step 1.
- Freeze-zone enforced text in the phase — §3 Phase 4 step 2 (inline list + fail-VERIFY rule).
- Migration ledger required in delivery report for `docs/` moves — §4 Report Rules.
- Both suppressions in the invocation contract — §3 Phase 4 step 1 (deviation #1 journaling, #2 personality).
- Demo: this document — plan produced, zero writes proven by SHA-256 match.
