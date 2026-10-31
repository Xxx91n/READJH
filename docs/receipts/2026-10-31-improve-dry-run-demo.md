# Receipts — write-mode runs (Ticket #6 acceptance, rework after PR #13 review)

Date: 2026-10-31 · Skill state: `SKILL.md` on `ticket-6-improve-rewrite-language`
(post-review rework; includes the `.bak` write-set, ledger re-base column, and
`--checks` contract changes) · Executor: READJH pipeline executed manually per
`SKILL.md` §3 phases. This document supersedes the first fixture demo, which is
kept at the bottom with its caveats.

## Run A — `improve --dry-run` on the real 6F repository (zero writes)

**Sample:** `D:\Aworker\6F\README.md` @ `cbfa75374a077729ddc6d8dab47f2bb194c4a3a7`,
in place inside its real repository (1113 files, LICENSE, `docs/`, `engine/`,
`.github/workflows/`, companion `README.zh-CN.md` all present). `--dry-run`:
plan and receipts only, no writes.

**ROUTE.** Mode `improve --dry-run`; `<repo-root>` = `D:\Aworker\6F` (inside a
Git worktree, `README.md` tracked and clean); tier `standard`; companion
`README.zh-CN.md` detected for lockstep. Baseline: SHA-256 snapshot of all
1113 files + `git status --porcelain --ignored` (4 ignored entries only).
Pointer contract resolved at trusted root `~/.agents/skills/`:
`readme-crafter-skill` 5/5 required files, `writing-humanize` 3/3
(frontmatter `name: writing-humanize`).

**TRUTH.**

```text
python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py D:\Aworker\6F
→ exit 0 (scan complete; "No obvious README-to-repo mismatches detected")
```

**RESTRUCTURE / LANGUAGE plans.** Same edit set as Run B below (executed
there); here it was listed only.

**VERIFY.**

```text
python -B scripts/check-readme.py D:\Aworker\6F\README.md --repo-root D:\Aworker\6F
→ exit 0 — PASS, 0 findings (all 6 single-repo checks; repo-set N/A)
Baseline re-compare: 1113-file SHA-256 snapshot identical; git status
--porcelain --ignored identical → zero writes; no .bak, no __pycache__.
```

Delivery report:

```text
[Conclusion]: PASS — improve --dry-run on D:\Aworker\6F\README.md (intensity tier: standard); plan produced, zero writes confirmed; migration ledger: none (dry-run — moves planned, not executed; see Run B).
[Receipts]: scan-project.py exit 0; check-readme.py exit 0 (0 findings); baseline tree + git status identical pre/post.
[Residual risk]: README commands never executed; plan not applied (dry-run).
```

## Run B — `improve` (real writes) on a disposable copy of 6F

**Sample:** the same 6F tree copied to
`C:\Users\Administrator\.zcode\tmp\6f-improve-run\` **without `.git`** —
deliberately exercising the `.bak` rollback path (non-Git `<repo-root>`).

**ROUTE.** Mode `improve` (no `--dry-run`); non-Git `<repo-root>` → file-tree
baseline (1113 files). `.bak` decision per SKILL.md RESTRUCTURE step 6:
write set = {`README.md`, `README.zh-CN.md`, `docs/versioning.md`} existing +
{`docs/architecture.md`, `docs/upstream-policy.md`, `.bak` files} new.
Non-Git → `.bak` created for **every existing write-set member** before the
first write:

```text
README.md.bak        README.zh-CN.md.bak        docs/versioning.md.bak
rollback: <path>.bak per write-set file (git cannot restore: no worktree);
new files docs/architecture.md, docs/upstream-policy.md recorded for deletion
```

**RESTRUCTURE (executed).** Ledger below. Over-complete sections moved out of
both READMEs in lockstep; relative link/image targets inside moved spans
re-based (`docs/…` → `../docs/…`) so they resolve to the same resources from
`docs/` depth; self-attestation converged (badge/preview facts merged into the
single NOTE block; `## Honesty notes` / `## 诚实注记` deleted in both files);
front-page tracker IDs (`#85②`, `D-204③④`, `D-205`, `D-034③`, `D-020`, `D-013`,
`D-037③`, `#51`, `A-044/A-045`) removed; companion sync stamp
`<!-- sync: 3246796f4021 -->` regenerated to `43778f51be65` (derived artifact
bound to the new English hash).

**LANGUAGE (executed, `standard` tier).** `writing-humanize` catalog +
`references/de-ai-language.md` applied outside freeze zones only:
abstract-noun chain at the intro ("self-built moat and glue" → names the
artifacts), defensive sentence split, meta-honesty claim recast as plain
disclosure statement, zh pass kept in lockstep. **Both suppressions held:**
no `~/.ink-and-agency/learnings/` or `.ink-and-agency/` file exists anywhere
(verified by `find`), and no personality/story was injected. Freeze-zone
integrity: badge row count identical pre/post (5 shields.io refs), all fenced
blocks, URLs, versions, commands byte-identical.

**VERIFY.**

```text
python -B scripts/check-readme.py <fixture>/README.md --repo-root <fixture>          → exit 0, 0 findings
python -B scripts/check-readme.py <fixture>/README.zh-CN.md --repo-root <fixture>    → exit 0, 0 findings
python -B scripts/check-readme.py <fixture>/docs/architecture.md    --repo-root <fixture> --checks dead-links,missing-images,code-fences → exit 0
python -B scripts/check-readme.py <fixture>/docs/upstream-policy.md --repo-root <fixture> --checks dead-links,missing-images,code-fences → exit 0
python -B scripts/check-readme.py <fixture>/docs/versioning.md      --repo-root <fixture> --checks dead-links,missing-images,code-fences → exit 0

(re-run after each round of probe hardening — fragment validation in
dead-links, code-fences in the destination subset, and the round-4/5
rendered-content fixes: all five files still clean)
```

Write-set check (tree diff vs baseline) — **exactly** the intended set:

```text
modified:  README.md, README.zh-CN.md, docs/versioning.md
created:   docs/architecture.md, docs/upstream-policy.md,
           README.md.bak, README.zh-CN.md.bak, docs/versioning.md.bak
unexpected diffs: none; no __pycache__/*.pyc.
```

Delivery report:

```text
[Conclusion]: PASS — improve on disposable 6F copy (intensity tier: standard); 6 ledger moves, self-attestation converged, tracker IDs removed, wording pass applied; all probes clean.
[Receipts]: rollback: .bak per write-set file (non-Git); 5 probe runs exit 0; tree diff = write set only; both suppressions held (no .ink-and-agency writes, no injected personality).
[Residual risk]: npm/selftest commands never executed (needs manual verification); Git rollback path planned not exercised; zh sync stamp regenerated by hand, engine gen script not re-run.
```

### Migration ledger (Run B)

| Moved span (heading, `<readme>` lines) | Destination file | Re-based targets (`original → new`) |
|---|---|---|
| `## Architecture: three layers` (README.md 91–95) | `docs/architecture.md` (new) | `docs/assets/architecture.svg → ../docs/assets/architecture.svg` |
| `## Runtime view` (README.md 111–120) | `docs/architecture.md` | none |
| `## Ownership boundary` (README.md 122–127) | `docs/architecture.md` | none |
| `## Upstream components` + status note + dual-track paragraph (README.md 97–109) | `docs/upstream-policy.md` (new) | `engine/upstream-lock.yaml → ../engine/upstream-lock.yaml`; `docs/versioning.md → ../docs/versioning.md` |
| `## Contracts` (README.md 129–133) | `docs/upstream-policy.md` | none |
| `0.x semantics` paragraph (README.md 49) | `docs/versioning.md` (existing — merged, `.bak` taken) | none |
| `## 组合件架构（三层）` (README.zh-CN.md 100–105) | `docs/architecture.md` (zh section) | `docs/assets/architecture.svg → ../docs/assets/architecture.svg` |
| `## Runtime View` (README.zh-CN.md 122–132) | `docs/architecture.md` (zh section) | none |
| `## 所有权边界` (README.zh-CN.md 134–140) | `docs/architecture.md` (zh section) | none |
| `## 上游清单` + 状态注 + 双轨段 (README.zh-CN.md 107–120) | `docs/upstream-policy.md` (zh section) | `engine/upstream-lock.yaml → ../engine/upstream-lock.yaml`; `docs/versioning.md → ../docs/versioning.md` |
| `## 契约声明` (README.zh-CN.md 142–147) | `docs/upstream-policy.md` (zh section) | none |
| `0.x 语义` paragraph (README.zh-CN.md 55) | dropped — content already in `docs/versioning.md` §1 (front page keeps pointer line) | none |

## Run C — `rewrite --dry-run` on the READJH README (plan only)

**Sample:** `D:\Aworker\READJH\README.md` at HEAD (real repo, real context).
`--dry-run`: rebuild plan only.

```text
scan-project.py D:\Aworker\READJH   → exit 0 (no README-to-repo mismatches)
check-readme.py README.md           → exit 0, 0 findings
git status --porcelain --ignored pre/post → identical (zero writes; the two
" M" entries are this ticket's uncommitted rework edits, present pre-run)
```

Plan (not executed): rebuild `README.md` to the skill/tool skeleton — name +
one-liner, install/prereqs, three modes + `--dry-run` quickstart, phase flow,
docs map (spec/ADR/UPSTREAM/GLOSSARY pointers). Freeze-zone inventory for the
rebuild: fenced command blocks (`python3 scripts/check-readme.py …`), file
paths (`SKILL.md`, `references/`, `docs/spec/…`), badge row, version/SHA
strings, LICENSE text — each stays byte-identical through any wording pass.
**Not demonstrated:** an executed (non-dry) `rewrite`; that remains unverified.

## Original fixture demo (superseded, kept with caveats)

First demo: `improve --dry-run` on a single-file copy of the same 6F README in
a non-Git fixture (`C:\Users\Administrator\.zcode\tmp\readjh-demo-fixture\`,
baseline SHA-256 `3246796f40…b859b`, unchanged pre/post — zero writes). The
plan produced there was sound, but the fixture lacked repository context, so
`check-readme.py` reported **exit 1 / 24 blocking findings** (22 dead links +
2 missing images: `LICENSE`, `README.zh-CN.md`, `engine/`, `docs/`,
`examples/`, `.github/` absent). Run A above re-runs the same plan in real
repo context — probe exit 0, 0 findings — confirming all 24 were
fixture-context. Also not demonstrated by that demo: real writes, `.bak`
creation, ledger execution, runtime suppression behavior — all covered by
Run B now.

## Post-review probe hardening receipts (rounds 2–4)

- `check-readme.py --checks ",,"` and `--checks ""` → **exit 2** (explicit
  empty selection rejected; omitted flag = all checks); unknown names →
  exit 2; duplicates de-duplicated.
- `dead-links` validates fragments **to GitHub's rendering semantics**:
  same-file `#anchor` and `file.md#anchor` resolved against
  GitHub-slugified heading anchors (indented ATX + Setext incl. digit-led
  and marker-char-led text + duplicate `-1`/`-2` suffixes, `{#id}` text
  folded into the slug per GFM) plus `id`/`name` attributes parsed
  attribute-by-attribute on real HTML tags — `data-id=`, `id=` inside
  another attribute's value, bare text `id=`, `name=` on non-`<a>` tags,
  and fenced/inline-code/commented attributes do not count. Inline
  comments no longer erase heading text; `<!--` inside code spans is
  literal and cannot swallow later content. Underscores inside
  names/code spans are preserved. Links and images inside HTML comments
  or inline code are skipped entirely (not rendered).
- Run B's five probed files re-checked with
  `--checks dead-links,missing-images,code-fences` → all exit 0.
- Unit tests: `python -m unittest discover -s tests` → **72 tests OK**
  (38 total new across rounds 2–5: `--checks` subset/empty/dedup/repo-set
  combination + fragment same-file/cross-file/dup-suffix/indented-ATX/
  Setext/CJK/underscore cases, incl. negative fixtures for fenced,
  inline-code, and commented `id`/`name` attributes, attribute-value
  `id=`, `data-id`, bare-text `id=`, `#custom` curlies, list-marker
  Setext exclusions; positives for inline-comment headings,
  unclosed-comment-in-fence, code-span `<!--` literals, digit- and
  marker-led Setext, and commented/inline-code dead links and images).

## Acceptance mapping

- `SKILL.md` covers all three modes plus `--dry-run` — §3 spine + §5 table.
- LANGUAGE phase: pointer-contract invocation + named supplement files —
  §3 Phase 4 step 1; resolved in Runs A/B (3/3 required files).
- Freeze-zone in-phase rule text — §3 Phase 4 step 2; held in Run B
  (badge/command/URL diffs empty).
- Migration ledger required for `docs/` moves — §4 Report Rules; Run B ledger
  above, now with the re-based-target column.
- Both `writing-humanize` suppressions in the invocation contract — §3 Phase 4
  step 1; **runtime-held in Run B** (no journal files; no injected voice).
- Demo: `improve --dry-run` plan + zero writes — **Run A** (real repo, probe
  clean, tree identical). Executed-write receipt — **Run B**; `rewrite` —
  plan-level only (Run C), executed `rewrite` not demonstrated.
