# Audit smoke run — `6F` (Ticket #5)

> Implements `Xxx91n/READJH#5`. A full `audit`-mode run (`ROUTE → TRUTH →
> RESTRUCTURE → VERIFY`, `SKILL.md` §3) on the `6F` repository plus the runtime
> validation record for `scan-project.sh` under Git Bash on this host — the
> first open runtime item in `docs/spec/0001-readjh-orchestration-skill.md`
> (§Further Notes). Diagnose-only: zero writes to `D:\Aworker\6F`.

- **Run date:** 2026-10-31 (UTC+8), Git Bash `GNU bash, 5.3.15`, Windows host.
- **Target:** `D:\Aworker\6F` — HEAD `cbfa75374a077729ddc6d8dab47f2bb194c4a3a7`
  (`main`), Git worktree `true`, remote `https://github.com/Xxx91n/6F.git`.
- **Primary README:** `D:\Aworker\6F\README.md` (187 lines, English,
  canonical); **companion:** `D:\Aworker\6F\README.zh-CN.md` (205 lines, derived
  zh — checked in lockstep).
- **Run parameters:** mode `audit`; `--repo-set` not passed (single-repo,
  check 7 `N/A`); **intensity tier `lite`** — the repo exhibits a verified
  author voice (bilingual hand-written governance docs and commit messages,
  e.g. `cbfa7537`), so per `references/readme-rules.md` §5.1 only clustered AI
  vocabulary, chatbot turn wrappers, and repeated **self-attestation** are
  diagnosed under the language pass.

## 1. `ROUTE` — pointer contract receipts

`readme-crafter-skill` resolved at root #3 `~/.agents/skills/` via the junction
created per `UPSTREAM.md` Install actions:

| Check | Result |
|---|---|
| `~/.agents/skills/readme-crafter-skill/SKILL.md` frontmatter `name:` | `readme-crafter-skill` (exact canonical match) |
| Required files present | `SKILL.md`, `references/repo-integrity.md`, `scripts/scan-project.py`, `scripts/scan_project_readme.py`, `scripts/scan_project_support.py` — all OK (`scripts/scan-project.sh` also present) |
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `D:\Aworker\6F\.agents\skills\` absent → project-local trust gate not triggered |
| Junction | `C:\Users\Administrator\.agents\skills\readme-crafter-skill` → `C:\Users\Administrator\.agents\skills\git\readme\readme-crafter-skill-main` (LinkType Junction, created 2026-10-31; target dir is not a Git checkout — captured zip-style copy, revision noted in `UPSTREAM.md`) |

`writing-humanize` is not required by `audit` mode and was not resolved.

## 2. `scan-project.sh` runtime record (spec open item)

Two runs captured on this host:

| Case | Command | Exit | Behavior |
|---|---|---|---|
| `python3` on PATH (`/c/Program Files/PyManager/python3`, Python 3.11.9) | `bash ~/.agents/skills/readme-crafter-skill/scripts/scan-project.sh D:/Aworker/6F` | `0` | `exec python3 …scan-project.py` path taken; stdout **byte-identical** to the direct `python3 -s -E -B -X utf8 scan-project.py D:/Aworker/6F` run (diff = empty) |
| `python3` stripped from PATH | `PATH=/tmp/nopython:/usr/bin:/bin bash …/scan-project.sh D:/Aworker/6F` | `0` | `FALLBACK MODE` report — `Inventory: limited shell fallback`; only `[EXISTS] README.md` and `[EXISTS] License file` signals; prints "python3 was not found" banner |

## 3. `TRUTH` receipts

```text
$ python3 -s -E -B -X utf8 "C:/Users/Administrator/.agents/skills/readme-crafter-skill/scripts/scan-project.py" "D:/Aworker/6F"
exit 0 — README INTEGRITY SIGNALS: README.md 187 lines, all local refs resolve,
0 missing refs / unresolved imports / env-var mismatches; README RISK SUMMARY:
"No obvious README-to-repo mismatches detected by the scanner".
```

- **Project type:** Agent or AI Tool (Claude Code Agent Plugin —
  `.claude-plugin/marketplace.json` + `engine/.claude-plugin/plugin.json`).
- **Distribution posture:** Product/Monorepo Hub — marketplace-installable
  plugin plus source-first engine (`engine/package.json`, `engine/dist/`).
- **Claim-by-claim verification (claims checked, anchors verified):**
  `LICENSE` = Apache-2.0 (`README.md:9`); `version 0.3.0` (`README.md:10` ↔
  `engine/package.json:3` + `marketplace.json`); `Node ≥ 22.18` (`README.md:11,53`
  ↔ `engine/package.json` `engines`); marketplace install
  `6f@xxx91n` (`README.md:12,57-58` ↔ `.claude-plugin/marketplace.json` +
  `engine/README.md:35-36`); `engine-ci.yml` workflow + `paths: engine/**`
  (`README.md:13,87` ↔ `.github/workflows/engine-ci.yml:4-6`); `dist/cli.js`
  bundle ships (`README.md:60` ↔ `engine/dist/cli.js` 298,989 B +
  `engine/CHANGELOG.md` #59); `selftest` / `doctor --fix` / `mcp facts` /
  `repo add` / `demo [--list]` (`README.md:60,149,156-160` ↔
  `engine/src/cli.ts:36,39,46,123,246`); CodeLore `0.28.0` + Scorecard `planned`
  + lock-table `evaluating` row `codelore-sqlite-dump` (`README.md:103-104,107`
  ↔ `engine/upstream-lock.yaml:28,71,91`); gsd-core 1424-facts run record
  (`README.md:162` ↔ `docs/archive/decisions/architecture-recovery-ledger.md` A-045);
  all 12 linked local paths resolve (`scan-project.py` + manual spot-check).
- **README commands not executed (static-safety rule):** `/plugin …` install
  lines, `npm install && npm test && npm run selftest` (`README.md:80-84,157,174`),
  `node dist/cli.js …` (`README.md:60,149,158-159,174-176`) — flagged
  `"needs manual verification"` in the delivery report, never run.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| **HIGH** | `README.md:164` claims *"no fictional `audit` subcommand is claimed … the packaged first-class command surface is not frozen"* and says external-repo audits "currently run as in-repo scripts" — but `engine/src/cli.ts:143` implements a first-class `audit <path> [--scale S] [--out] [--json] [--refresh]` plus `audit file …`, the CLI usage banner (`cli.ts:286`) advertises both, and `engine/CHANGELOG.md` `tracker #28` records "#53/D-060 audit 一等命令". README is stale by at least one release. | `README.md:164` vs `engine/src/cli.ts:143-144`, `engine/src/cli.ts:286`, `engine/CHANGELOG.md` tracker #28/#53 |
| LOW | "1424 facts" gsd-core claim (`README.md:162`) is backed by `architecture-recovery-ledger.md` A-045 — verified, no defect; retained as a LOW footnote for the claim-ledger only. | `README.md:162` ↔ `docs/archive/decisions/architecture-recovery-ledger.md` A-045 |
| LOW | `dist/cli.js` measured size differs from `CHANGELOG.md` #59's historical `153,604B` note (298,989 B at HEAD) — the README itself quotes no size, so no contradiction; recorded only as context for the claim ledger. | `wc -c engine/dist/cli.js` = 298,989 |

No other contradicted claims found; `scan-project.py` reported zero mismatches.

## 4. `RESTRUCTURE` receipts (diagnose-only, `lite` tier)

Whitelisted repo-owned markers verified (not generation traces):
`<!-- acknowledgments:start/end — GENERATED by engine/scripts/gen-acknowledgments.mjs -->`
and `<!-- canonical: README.md | owner: Xxx91n -->` / `<!-- sync: 3246796f4021 -->`
are actively written by `engine/scripts/gen-acknowledgments.mjs:148` and checked
by `engine/test/contracts/73-check.mjs:20,86` — kept per
`references/readme-rules.md` §3 whitelist. No `PLACEHOLDER`/`SLOT`/pipeline-tag
or chatbot-wrapper comments exist in either README.

| Severity | Finding | Receipt |
|---|---|---|
| **HIGH** | **Self-attestation** — the preview/honesty boundary is restated 5 times across the front page: hero note (`README.md:33`), capability-matrix footnote (`README.md:47`), `0.x` semantics (`README.md:49`), demo honesty (`README.md:149-150`), and the standalone `"Honesty notes"` section (`README.md:183-187`, incl. *"preview means preview"*). This is the exact pattern `references/readme-rules.md` §2 names as its motivating example (restating "preview means preview" in hero note, matrix, demo, closing honesty section). | `README.md:33,47,49,149-150,183-187`; zh mirror `README.zh-CN.md:38,53,55,165-166,201-205` |
| MEDIUM | **Standalone honesty-proclaiming section** — `## Honesty notes` (`README.md:183-187`) exists only to re-assert truthfulness; §2 rule 3 calls for removal with unique facts merged (its badge-dating fact is unique). | `README.md:183-187` |
| MEDIUM | **Internal tracker IDs on the front page** — `#85②`, `D-204③④`, `D-034③`, `D-205`, `D-020`, `D-037③`, `D-013`, `A-044/A-045`, `#110/#106/#111` class references leak into README prose; §2 rule 4 says they belong in `docs/`/`CHANGELOG.md`. | `README.md:33,39,41-44,99,107,154,162,164`; same in `README.zh-CN.md` |
| MEDIUM | **Defensive disclaimers not recast** — `README.md:33` *"do not read this page as a finished product"*, `README.md:150`/`179` *"they do not impersonate real audits"*, `README.md:163` external-drift caveat: multi-clause negative disclaimers that §2 rule 2 wants as `fact + link`. | `README.md:33,150,163,179` |
| MEDIUM | **Over-completeness vs `docs/`** — full upstream-lock status matrix (`README.md:99-107`), `0.x` versioning policy (`README.md:49`), ownership-boundary/contract tables (`README.md:124-133`) restate material that lives in `engine/upstream-lock.yaml` and `docs/versioning.md`. Deliberately labeled "engineering layer" (`README.md:187`), but per `references/readme-rules.md` §4.1 the span `Upstream components/Ownership/Contracts (lines 97-133) → recommended docs/` migration is flagged. | `README.md:49,97-133` |
| LOW | **30-second first screen weak** — the shortest install path (`## Install`, line 51) sits below a 90-word jargon-dense one-liner (`README.md:18`) and a 6-bullet highlights block; a stranger reads the preview caveat before the install command. `lite` keeps the author's structure; flagged as diagnosis only. | `README.md:18-60` |
| LOW | **zh date typo** — `README.zh-CN.md:38` dates the status note `2026-10-05` identically to EN — actually consistent; no defect (recorded as verified, not a finding). | — |

`lite`-scoped language tells: no clustered AI vocabulary, no chatbot wrappers,
no second-person openers in EN; the repeated **self-attestation** above is the
only `lite`-scope language defect. No generation traces outside whitelisted
repo-owned anchors. Heading skeleton fits a Product/Monorepo-Hub posture
(hub navigation tables + engine deep-links) — not a generic template.

## 5. `VERIFY` receipts

```text
$ python3 -B "D:/Aworker/READJH/scripts/check-readme.py" "D:/Aworker/6F/README.md" --repo-root "D:/Aworker/6F"
exit 0 — dead-links PASS, missing-images PASS, code-fences PASS,
         badge-domains PASS, boundary-duplicates PASS, honest-gaps PASS; 0 findings.

$ python3 -B "D:/Aworker/READJH/scripts/check-readme.py" "D:/Aworker/6F/README.zh-CN.md" --repo-root "D:/Aworker/6F"
exit 0 — same six checks PASS; 0 findings. (check 7 repo-set: N/A — single-repo run)
```

Checklist (`references/checklist.md` §§1–8) evaluated:

| § | Item | Result |
|---|---|---|
| 1 | Machine receipts / probe gate | PASS — `scan-project.py` exit 0, `check-readme.py` exit 0 ×2, zero README commands executed, no AI-detector scores |
| 2 | Facts preserved / freeze zone | **FAIL → finding** — one contradicted claim (`audit` subcommand) recorded as HIGH; all other claims matched `file:line` receipts |
| 3 | 30-second first screen | **Partial** — project/type/problem/install all present but install path below the fold (LOW finding) |
| 4 | One-statement boundaries | **FAIL → finding** — preview boundary restated 5× (HIGH); tracker IDs + negative disclaimers (MEDIUM) |
| 5 | Non-isomorphic skeleton | PASS — `repo-set` N/A (single-repo); skeleton fits hub posture |
| 6 | Zero generation traces | PASS — `acknowledgments`/`canonical`/`sync` anchors verified repo-owned (`gen-acknowledgments.mjs`, `73-check.mjs`) |
| 7 | Voice / de-AI (`lite`) | PASS except repeated self-attestation already filed under §4; zero invented personality/gaps (audit is read-only) |
| 8 | Rollback + three-line report | PASS — no `.bak` needed (audit, zero writes); delivery report emitted in §7 |

**Zero-write verification:** file-tree snapshot of `D:\Aworker\6F` (excluding
`.git/`) before and after the run:

- before: `1113` files, `tree_sha256 = ff32c55b1d031e9704c321abb08ee250a327c9137e1da047c39ad0cbff6c94f6`
- after: `1113` files, `tree_sha256 = ff32c55b1d031e9704c321abb08ee250a327c9137e1da047c39ad0cbff6c94f6` — **identical** (0 new / 0 removed / 0 changed)
- `git --no-optional-locks -C D:/Aworker/6F status --porcelain --ignored -- .`
  identical before/after (4 ignored entries: `.code-tmp/`, `.scratch/`,
  `engine/node_modules/`, `engine/test/fixtures/contracts/21-guard-run.log`)

## 6. Findings — `SKILL.md` expectations vs. real behavior (filed, not patched)

Per the ticket's acceptance criteria, every expectation↔behavior gap observed
is recorded as a finding, not silently corrected:

| # | Severity | Discrepancy | Receipt |
|---|---|---|---|
| D1 | LOW | `SKILL.md` §3 TRUTH implies a `2`-class execution error ("exit `2`") for the scanner, but upstream `scan-project.py` has no `exit 2` path — invalid directory returns `1` (same code as a findings exit in SKILL.md's own "exit 1 with findings" contract), and the shell fallback also returns `1`. Distinguishing "scan with findings" from "invalid root" must be done by output shape, not exit code alone. | `scan-project.py:main` (`return 1` / `return 0`), `scan-project.sh:17` (`exit 1`) |
| D2 | LOW | `scan-project.sh` fallback prints a **degraded** report yet exits `0` — indistinguishable from a full scan by exit code. READJH never invokes the `.sh` wrapper (§1 runs `scan-project.py` directly), so the pipeline is protected, but the wrapper's contract is documented here as the runtime item asked. | `scan-sh-fallback` run above (exit `0`, `FALLBACK MODE`) |
| D3 | LOW | Ticket names the runtime item `scan-project.sh`; `SKILL.md`/UPSTREAM required-files list `scan-project.py` (+ `scan_project_readme.py`, `scan_project_support.py`) and never mention the `.sh` wrapper. The wrapper exists upstream and delegates to the `.py`; no action needed beyond this note. | `scripts/scan-project.sh:9-11` (`exec python3 … scan-project.py`) |
| D4 | LOW | `check-readme.py` omits `repo-set` from its printed check list when `--repo-set` is not passed — the §3 VERIFY contract documents `repo-set: N/A` output, so the report here writes `N/A` by hand. | `check-readme.py` stdout shows 6 checks only |
| D5 | INFO | Host note: `python3` resolves under Git Bash via PyManager shim (`/c/Program Files/PyManager/python3`, 3.11.9); no `python`-only host degradation was needed this run. | `command -v python3` |

## 7. Three-line delivery report (as emitted by the run)

```text
[Conclusion]: FAIL — audit on D:/Aworker/6F/README.md (intensity tier: lite); audit completed and found 2 HIGH, 4 MEDIUM, 3 LOW findings (zh mirror carries the same HIGH/MEDIUM set; 0 files modified).
[Receipts]: scan-project.py "D:/Aworker/6F" -> exit 0 (0 README-to-repo mismatches); check-readme.py README.md -> exit 0 (6/6 checks PASS), README.zh-CN.md -> exit 0 (6/6 PASS), repo-set: N/A; HIGH: README.md:164 denies a first-class `audit` subcommand that cli.ts:143 implements; HIGH: preview/honesty boundary restated 5x (README.md:33,47,49,149-150,183-187); MEDIUM: standalone honesty section (183-187), tracker IDs on front page (33,39,107,154,164), negative disclaimers (33,150,163), docs-worthy depth blocks (49,97-133); LOW: install path below first fold (18-60), 1424-facts and dist-size claims verified as context only; <repo-root> snapshot unchanged (1113 files, ff32c55b…, git status match).
[Residual risk]: README commands need manual verification — `npm install && npm test` (README.md:82-84), `node dist/cli.js selftest` (:60), `/plugin marketplace add/install` (:56-57), `repo add` (:158-159), `demo` (:149); external shields.io badge URLs and the github.com/actions badge target unfetched offline.
```

## 8. Acceptance criteria coverage

- [x] Audit run completes on 6F without editing its files — §5 zero-write verification.
- [x] Report follows the three-line format and lists findings by severity — §7 + §§3-4 tables.
- [x] Probe output attached as receipt — §2, §3, §5 verbatim command + output + exit codes.
- [x] `scan-project.sh` real behavior on this host documented — §2 (ran clean under Git Bash with `python3` present; shell fallback verified degraded-but-exit-0).
- [x] SKILL.md↔behavior discrepancies filed as findings — §6 D1–D5.
