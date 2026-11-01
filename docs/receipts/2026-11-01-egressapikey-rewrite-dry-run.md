# `rewrite --dry-run` — `EgressAPIKEY` (Ticket #7, full-mode dry-run)

> `rewrite` mode with `--dry-run` (`ROUTE → TRUTH → RESTRUCTURE → LANGUAGE →
> VERIFY`, `SKILL.md` §3) on `D:\Aworker\EgressAPIKEY`. Plan and receipts only —
> zero writes, no `.bak`, no `docs/` migration executed. Builds on the same-day
> `audit` receipt (`docs/receipts/2026-11-01-egressapikey-audit.md`).

- **Run date:** 2026-11-01.
- **Target:** `D:\Aworker\EgressAPIKEY` — HEAD `4826153df3d192d44baa6072f5e43a2e26a9d38e` (`main`), Git worktree `true`; `README.md` + companion `README_CN.md`, both tracked and clean.
- **Mode:** `rewrite --dry-run`; **intensity tier `lite`** (verified author voice — see audit §ROUTE); `--repo-set` not passed.

## `ROUTE`

Write mode resolves both executors (audit receipt §1, re-verified):

| Check | Result |
|---|---|
| `readme-crafter-skill` | resolved at root #3, 5/5 required files |
| `writing-humanize` | resolved at root #3 — canonical dir; frontmatter `name: writing-humanize`; `references/patterns.md` + `agents/openai.yaml` present (re-verified 2026-11-01) |
| Self-write guard | resolved `<readme>` = target repo's `README.md`; write-set members (README.md, README_CN.md, `docs/architecture/ARCHITECTURE.md`) are not skill or upstream paths → proceed |
| Baseline (fresh capture for this run) | `files=33801 tree_sha256=03808456ed37a10e21fc1b9ddb3aa4efed5992bccc643be9782a2b458d8c1841`; `git status --porcelain --ignored` = 13 ignored entries (same list as audit receipt) |
| Rollback decision (planned, not created) | would be **git path**: `<repo-root>` is a worktree and both READMEs are tracked+clean; `docs/architecture/ARCHITECTURE.md` exists (tracked — verify at apply time) → no `.bak`; recorded as *would* apply per §3 step 6 dry-run rule |

## `TRUTH`

Inherited from the same-day audit (same HEAD, same tree hash): `scan-project.py` exit 0 — 0 real mismatches; claims verified (`RESIN_PROXY_TRANSPORT_*` at `sidecar.rs:498-507`, `allocation_policy` trio at `strategy_engine.rs:696-701`, `include_intel_mac` at `ci.yml:31,227`, `v1.2.0` manifest, `14200` at `headless_security.rs`, `resin/` in `.gitignore:94`). Findings carried: no HIGH; the generation-trace MEDIUMs + the literal-placeholder/unbacked-floor LOWs (audit §3) — all resolved by the plan below.

## `RESTRUCTURE` plan (not executed)

**New skeleton** (application-hub posture; install promoted above the fold):

1. Title + one-liner (keep verbatim), badges (freeze zone — byte-identical), `English | 简体中文` nav, `llms.txt` note + `Formerly ai-api-route` (keep — receipts), hero picture block (freeze).
2. `## What & why` — one paragraph: keeps the product sentence + the CONNECT-tunnel justification; collapses the triple `fetch_resin.sh`/`resin/` explanation into the single authoritative statement carried by Third-party notices (delete the `:23` and `:25` restatements, keep one).
3. `## Download` — promoted ahead of Features (first-screen rule); content verbatim (verified claims only).
4. `## Features` — deduplicated bullets (the Mode A/B two-mode explanation keeps its `:84-85` form; `Zero adaptation` bullet keeps Mode-A scope).
5. `## Quick start (development)` — verbatim (commands are freeze zone).
6. `## Screenshots` — the plain pending sentence kept; **all five scaffolding comments deleted** (`README.md:95-100`, `README_CN.md:95-100`).
7. `## Architecture` — the rendered SVG image kept + 2-line summary + link to `docs/architecture/ARCHITECTURE.md`; the `<details>` mermaid source block **migrated** (ledger below).
8. `## Documentation` table, `## Compliance notice`, `## Third-party notices` (becomes the single `fetch_resin` statement site), `## Contributing` (deduplicated: single `CONTRIBUTING.md` pointer), `## License` — kept.
9. `<!-- synced-with: … -->` anchors **deleted** at the top of both files (unowned, §3 whitelist fails) — the bilingual discipline is maintained by the lockstep edit, not by an anchor no tool reads.

**Deletions:** `synced-with` anchors (:1 both files); `<!-- PLACEHOLDER … readme-crafter rule -->` + `<!-- Drop-in … -->` + 3× `<!-- SLOT … -->` comments + zh mirrors (`:95-100` both files); the two redundant `fetch_resin` restatements (`README.md:23` partial, `README_CN.md` mirror); the duplicated "read CONTRIBUTING.md" tail inside `:132`.

**Companion `README_CN.md`:** identical plan in lockstep (zh mirrors of every move/delete above).

**Migration ledger (planned):**

| Moved span (heading, `<readme>` lines) | Destination file | Re-based targets (`original → new`) | Inbound anchor remaps (`original → new`) |
|---|---|---|---|
| `<details>` Mermaid source block (README.md:38–64) | `docs/architecture/ARCHITECTURE.md` (existing — merged append) | `assets/readme/architecture.svg → ../assets/readme/architecture.svg` (the `<code>` path mention inside `summary` travels verbatim; only the relative link/image targets re-base) | none (no inbound links to the details block) |
| `<details>` Mermaid source block (README_CN.md:38–64) | `docs/architecture/ARCHITECTURE.md` (zh section) | same re-base as EN | none |

## `LANGUAGE` plan (Phase 4 step 5 — `writing-humanize` invoked at `lite` scope)

**Invocation contract:** `writing-humanize` read from the trusted root #3 path; `references/de-ai-language.md` (§§1–6 incl. §3 zh for the companion) + `references/readme-rules.md` (§§1–5) read into context. **Suppression 1 (journaling):** no `~/.ink-and-agency/` or `.ink-and-agency/` write — plan records it, nothing created. **Suppression 2 (personality):** Step 5 / `PERSONALITY AND SOUL` ignored — no invented voice, gaps, or stories anywhere in the plan.

**Freeze-zone inventory (byte-identical through LANGUAGE):** badges row (:7), fenced bash blocks (`:71-78`, `:108-113`), mermaid fence inside the migrated details block, inline code spans (`Platform.Account`, `scripts/fetch_resin.sh`, `RESIN_PROXY_TRANSPORT_*`, `include_intel_mac`, version `v1.2.0`, port `14200`, `:18000…:18049`), all URLs and link/image targets incl. `srcset`, the compliance and license text, direct quotes.

**29-pattern + distilled-rules scan result (lite scope, on surviving prose):** writing-humanize patterns #20–22 (chatbot/cutoff artifacts): 0 hits; #7 clustered AI vocabulary: 0 hits; §2 self-attestation repeats: the boundary set is already single-stated (compliance `:126-128`, the Mode-B buffering caveat `:69`, `not published to npm` `:69`) — converged by RESTRUCTURE deletions, no residual; distilled §1 patterns (negative parallelism, throat-clearing, `-ing` tails, rule-of-three, connective stacking): 0 actionable hits at `lite`.

**Per-span plan:**

| Anchor (`<readme>:lines`) | Tier-allowed transform | Intended before → after shape |
|---|---|---|
| `README.md:5` (one-liner) | keep | accurate, plain — no transform |
| `README.md:23-25` (What & why) | lite-scope convergence (structural at RESTRUCTURE) | two paragraphs → one; the `fetch_resin` mechanics sentence appears once, anchored to the THIRD_PARTY statement site |
| `README.md:29-36` (mode table) | keep | factual, already tight |
| `README.md:84-91` (features) | keep + structural dedup | bullets kept; `Zero adaptation` keeps Mode-A scope (verified caveat) |
| `README.md:102` (screenshots pending) | keep | the one plain sentence survives verbatim — the comments around it were the defect |
| `README.md:126-136` (compliance + third-party) | keep | legal/boundary text — freeze-adjacent, single-stated |
| `README_CN.md` mirrors of all above | same, lockstep | identical decisions; §3 zh calibration scan found no actionable tells at `lite` |

## `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/EgressAPIKEY/README.md" --repo-root "D:/Aworker/EgressAPIKEY"
exit 0 — all 6 single-repo checks PASS, 0 findings (pre-change probe; dry-run edits nothing).
$ python -B scripts/check-readme.py "D:/Aworker/EgressAPIKEY/README_CN.md" --repo-root "D:/Aworker/EgressAPIKEY"
exit 0 — same. (repo-set: N/A)
```

Zero-write verification: post-run `files=33801 tree_sha256=03808456ed37a10e21fc1b9ddb3aa4efed5992bccc643be9782a2b458d8c1841` — identical to this run's baseline; `git status --porcelain --ignored` identical (13 entries). No `.bak`, no `docs/` file created (ledger is plan-only).

## Three-line delivery report

```text
[Conclusion]: PASS — rewrite --dry-run on D:/Aworker/EgressAPIKEY/README.md (intensity tier: lite); full rebuild plan produced — 2 ledger moves planned, 4 deletion classes, skeleton reordered (Download above the fold), per-span LANGUAGE plan empty-of-edits at lite scope (all surviving spans verified keep); findings carried from audit resolved in plan: HIGH 0 / MEDIUM 2 / LOW 4; zero writes.
[Receipts]: scan-project.py exit 0; check-readme.py README.md + README_CN.md -> exit 0 (6/6 PASS both), repo-set: N/A; both writing-humanize suppressions recorded (no journaling write, no personality injection); freeze-zone inventory complete — zero freeze-zone edits planned; snapshot 33801 files identical pre/post.
[Residual risk]: executed rewrite not performed (dry-run); README commands need manual verification (pnpm/cargo/fetch_resin/tauri dev); external badge/release/RESIN links unfetched offline; ledger destination docs/architecture/ARCHITECTURE.md exists — merge point to re-verify at apply time.
```

## `writing-humanize` obedience to distilled rules (spec open item — assessed where exercised)

The spec's second runtime item is `writing-humanize`'s obedience to READJH's
distilled supplement rules in practice. Assessed on this dry-run (the only
`writing-humanize` exercise in this ticket) plus the ticket-6 Run B runtime
receipt (`docs/receipts/2026-10-31-improve-dry-run-demo.md`):

| Contract point | Exercised | Result |
|---|---|---|
| Read from trusted root only (never project-local) | pointer-contract resolution | PASS — root #3, frontmatter `name:` exact, 3/3 required files |
| Suppression 1 — no self-evolve journaling | this run's plan + Run B's executed write pass | PASS — no `~/.ink-and-agency/` or `.ink-and-agency/` artifact anywhere (Run B verified by `find`; this run wrote nothing) |
| Suppression 2 — no personality injection (Step 5 ignored) | LANGUAGE plan | PASS — plan invents zero voice/gaps/stories; `lite` keeps author register |
| Distilled rules read into context, stricter rules override upstream | pattern scan | PASS — the §1 merged-pattern scan plus §3 zh calibration ran on both READMEs; upstream-only behaviors (e.g. blanket em-dash strip, passive-voice removal) were not applied because the distilled scoped overrides (`checklist.md` §7 table) kept them out of scope |
| Freeze zone respected | plan inventory | PASS — every planned edit lands outside freeze-zone spans; the two ledger moves re-base link targets at RESTRUCTURE only, recorded verbatim in the ledger |
| `humanize-readme` never executed | rules-source only | PASS — not invoked anywhere; contributes §6 distilled rules only |

Residual: `writing-humanize`'s 29-pattern catalog is exercised here at `lite`
scope (cluster/vocab/wrapper checks) — the full `standard`-tier application was
demonstrated in Run B's executed pass; a future acceptance round could add a
`standard`-tier live run for completeness.
