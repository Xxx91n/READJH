# Acceptance report — Ticket #7 (`Xxx91n/READJH#7`)

> Seam C of `docs/spec/0001-readjh-orchestration-skill.md`: `audit` mode on all
> six target repos, a human-baseline comparison against `BurntSushi/ripgrep`,
> and a full-mode (`rewrite`) `--dry-run` on EgressAPIKEY. Run date 2026-11-01.
> Reports live in `docs/receipts/`; **nothing was written to any target repo.**

## 1. Run inventory

| # | Repo | README | Companion | HEAD (audited) | Tier | Probe result | Report |
|---|---|---|---|---|---|---|---|
| 1 | `6F` | 187 ln | `README.zh-CN.md` (205) | `cbfa7537` main | lite | exit 0 + exit 0 | `docs/receipts/2026-11-01-6f-audit.md` |
| 2 | `EgressAPIKEY` | 140 ln | `README_CN.md` (140) | `4826153d` main | lite | exit 0 + exit 0 | `docs/receipts/2026-11-01-egressapikey-audit.md` |
| 3 | `mcp-for-maya` | 358 ln | `README.zh-CN.md` (382) | `108807c` gitbutler/workspace | lite | exit 0 + exit 0 | `docs/receipts/2026-11-01-mcp-for-maya-audit.md` |
| 4 | `env-manager` | 253 ln | none (i18n block → 10 files in `docs/i18n/`) | `c60102da` main | lite | exit 0 | `docs/receipts/2026-11-01-env-manager-audit.md` |
| 5 | `boxing` | 180 ln | none (i18n block → 13 files in `docs/i18n/`) | `84983ac` feat/97 | lite | exit 0 | `docs/receipts/2026-11-01-boxing-audit.md` |
| 6 | `jiahao` | 102 ln | `README-zh-CN.md` (102) | `3f17d421` feat/config-dir-per-host-116 | lite | exit 1 + exit 1 (honest-gaps) | `docs/receipts/2026-11-01-jiahao-audit.md` |
| 7 | `ripgrep` (baseline) | 541 ln | none | `91f5d22` master (shallow) | lite | exit 1 (2 dead fragments) | `docs/receipts/2026-11-01-ripgrep-baseline-audit.md` |
| — | `EgressAPIKEY` `rewrite --dry-run` | 140 ln | lockstep plan | `4826153d` | lite | plan + exit 0 ×2 | `docs/receipts/2026-11-01-egressapikey-rewrite-dry-run.md` |

All seven repos ran `audit` at `lite` — every one carries a verified human
author voice (bilingual/review-turn commit prose or, for ripgrep, a
first-person-authored README). `scan-project.py` exited 0 on all seven
(complete scans). Zero writes confirmed per repo by identical pre/post
SHA-256 tree snapshots and identical `git status --porcelain --ignored`.

## 2. Findings summary

| Repo | HIGH | MEDIUM | LOW | Headline findings |
|---|---|---|---|---|
| 6F | 2 | 4 | 2 | README denies implemented `audit` subcommand (`README.md:164` vs `cli.ts`); honesty boundary restated 5×; tracker IDs on front page; docs-worthy spans |
| EgressAPIKEY | 0 | 2 | 4 | unowned `synced-with` anchors (:1 both files); readme-crafter scaffolding comments (`:95-101` both files) |
| mcp-for-maya | 0 | 3 | 5 | unowned zh `synced-with` anchor; front-page issue IDs (`#2`–`#7`, `D-163`); docs-worthy spans (tools reference, versioning/roadmap) |
| env-manager | 0 | 1 | 4 | clustered marketing vocabulary (`"Adapts seamlessly to every environment"`, `"modern, lightweight"`) |
| boxing | 0 | 0 | 2 | clean — the healthiest README of the set |
| jiahao | 1 | 2 | 2 | `License: MIT` claimed but **no LICENSE file at root**; runbook over-completeness (`:37-78`) |
| ripgrep (baseline) | 0 | 0 | 1 | two real dead fragment links (`FAQ.md#complete`, `FAQ.md#posix4ever`); zero AI tells |

## 3. Human-baseline comparison

| Dimension | ripgrep (human baseline) | The six target repos |
|---|---|---|
| Probe findings | `dead-links` FAIL ×2 — real broken fragments | 6/7 probe-clean; jiahao `honest-gaps` false negative |
| AI vocabulary clusters | none | env-manager (marketing tagline); others clean |
| Self-attestation | none | 6F (5×), jiahao trust boundary (4×, load-bearing) |
| Generation traces | none | EgressAPIKEY + mcp-for-maya (unowned `synced-with` + scaffolding comments) |
| Front-page scope | 270-line per-distro install matrix — kept as CLI convention | jiahao runbook prose, mcp-for-maya version policy, 6F contract tables flagged |
| Honest-gap signals | "Why shouldn't I use ripgrep?" — model honest-gap section | boxing/jiahao state real boundaries; 6F over-attests instead |
| Distinctive human fingerprints | candid caveats ("Please file a bug report!", the snap N.B., "single benchmark is never enough") | boxing ("obfuscation, not user-keyed encryption") and mcp-for-maya (self-dated external comparison) come closest |

**What the comparison demonstrates:** the pipeline does not flag honest
human prose as AI — ripgrep's only findings are two genuinely dead links it
should catch. Meanwhile it discriminates real defects in AI-flavored READMEs:
stale claims (6F HIGH), generation scaffolding (EgressAPIKEY), unowned sync
anchors (both `synced-with` cases), tracker noise (mcp-for-maya), marketing
clusters (env-manager), and a metadata-vs-repo license gap (jiahao). Blind
review can check: each finding carries `<readme>:<line>` + repo `file:line`
receipts a reviewer can verify independently.

## 4. `writing-humanize` obedience (spec open item — closed where exercised)

Assessed in `docs/receipts/2026-11-01-egressapikey-rewrite-dry-run.md`:
trusted-root resolution PASS; suppression 1 (no journaling) PASS; suppression
2 (no personality injection) PASS; distilled-override discipline PASS; freeze
zone PASS; `humanize-readme` never executed PASS. Residual: full
`standard`-tier live application was demonstrated in ticket-6 Run B; this
ticket exercises it at `lite` scope only.

## 5. Probe/tool gap findings (D-series, filed not patched)

| Repo | Gap |
|---|---|
| EgressAPIKEY | scanner counts a comment-interior literal path (`assets/readme/<name>.png`) the probe correctly skips — granularity difference, consistent |
| env-manager | scanner flags provider-auth env vars vs a deliberately absent `.env.example` |
| jiahao | `honest-gaps` vocabulary misses the repo's honest idiolect ("declared-unverified", "not live-probed") — a probe coverage gap, not a README gap |
| ripgrep | scanner misses unconventional `LICENSE-MIT`+`UNLICENSE`+`COPYING` naming |
| all | `repo-set: N/A` is not printed by `check-readme.py` when the flag is absent (carried from ticket-5 D4) |

## 6. Acceptance criteria coverage

- [x] **Six audit reports + one baseline comparison produced** — §1 table; seven per-repo receipt files.
- [x] **Each report carries probe receipts and its residual-risk line** — every receipt file: verbatim scanner/probe commands + exit codes + a §5 three-line report with `[Residual risk]`.
- [x] **EgressAPIKEY full-mode dry-run shows the migration ledger and no frozen-zone edits planned** — `2026-11-01-egressapikey-rewrite-dry-run.md`: 2-entry migration ledger (mermaid details blocks, EN+zh), explicit freeze-zone inventory, "zero freeze-zone edits planned".
- [x] **Acceptance report files under `docs/` (not committed to target repos)** — all files under `docs/receipts/`; zero-write verified per repo (identical pre/post tree hashes + git status).
- [x] **`writing-humanize` obedience to distilled rules assessed where exercised** — §4 + the dry-run receipt's assessment table.

## 7. Cross-ticket note — last implementation ticket

Ticket #7 is the last numbered ticket in the spec's acceptance seam (#1–#7).
The branch `ticket-7-acceptance-run` is cut from `origin/main` (`99bb6e1`),
which contains the merged code of all prior tickets (#2 probe, #3 references,
#4 audit spine, #5 smoke run, #6 write modes). Combined-behavior verification
is this acceptance run itself: the full pipeline (`ROUTE→TRUTH→RESTRUCTURE→
LANGUAGE→VERIFY`) executed end-to-end on real repositories with the merged
SKILL.md + references + probe. Spec-level open items from §Further Notes:
`scan-project.sh` runtime record closed in ticket-5's receipt; `writing-humanize`
obedience assessed in §4 above.

## 8. Residual risks

- README commands in all seven repos were never executed (static-safety rule) — every receipt lists them as `"needs manual verification"`.
- External URLs (badges, store pages, registries, blogs) were not fetched.
- `mcp-for-maya` and `boxing`/`jiahao` were audited on feature/workspace branches at recorded HEADs — findings bind to those commits, not to current `main`.
- `repo-set` cross-repo skeleton check (check 7) was not exercised — it is opt-in per spec US-21 and no `--repo-set` manifest was passed; the six skeletons were compared qualitatively instead (each fits its own project-type posture; none is isomorphic).
- Blind review is the user's — the per-repo receipts + this comparison are the material.
