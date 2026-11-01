# Audit — `jiahao` (Ticket #7, six-repo acceptance run)

> `audit` mode (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`, `SKILL.md` §3) on
> `D:\Aworker\jiahao` (remote `https://github.com/Xxx91n/jiahao.git`; a `gb-local`
> mirror also configured). Diagnose-only: zero writes.

- **Run date:** 2026-11-01, Git Bash, Windows host.
- **Target:** HEAD `3f17d4216945bc0d086feae8f8fc95b1eea8e48c`, branch `feat/config-dir-per-host-116` (not `main` — audited state recorded verbatim). Git worktree `true`.
- **Primary README:** `README.md` (102 lines, EN); **companion:** `README-zh-CN.md` (102 lines, zh — lockstep).
- **Run parameters:** mode `audit`; `--repo-set` not passed (check 7 `N/A`); **intensity tier `lite`** — verified author voice: zh conventional-commit prose with review-turn register (`3f17d421` "复审两条 nit——变量顺序对齐代码…", `868c81b6` "真机验证回填…").

## 1. `ROUTE`

| Check | Result |
|---|---|
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `.agents/skills/` absent in target → trust gate not triggered |
| Root #3 `readme-crafter-skill` | canonical dir; frontmatter `name:` exact; 5/5 required files |
| README tracked/clean | `ls-files --error-unmatch` ok; `status --porcelain` empty for both READMEs |
| Baseline | `files=8403 tree_sha256=bbe43b883732da292a27b020e6545e7fbedc9e2cd629f9a1c9b34446f08dcd9b`; `git status --porcelain --ignored` = 7 ignored entries to `jiahao-pre.txt` (`.codegraph/`, `.scratch/`, `bench/research/__pycache__/`, `jiahao-mcp/node_modules/`, `node_modules/`, `private/bench-corpus/`, `release-artifacts/`) |

## 2. `TRUTH`

```text
$ python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py "D:/Aworker/jiahao"
exit 0 — README INTEGRITY SIGNALS: 102 lines, 0 missing local refs;
LICENSE & TRUST: "package.json license: MIT — Risk: metadata claims a license but no license file exists";
RISK SUMMARY: "License metadata exists but no root license file was found".
```

- **Project type:** Agent/AI tool (agent-skill + MCP + multi-host adapter bundles). **Distribution posture:** Published Package (npm `npx skills add`, host plugin marketplaces).
- **Claim verification (verified):** `src/SKILL.md` exists (`README.md:23`); all linked adapter READMEs/dirs resolve (scanner 0 missing: `adapters/{antigravity,claude-code,codebuddy,codex,qoder,workbuddy}`); `scripts/install.js` exists (`:69`); verification commands map to `package.json` scripts (`npm test`, `build-adapters.js --check`, `check-drift.js`, `check:whitespace`, `check:links`, `release:gate` — all in `package.json`); MIT license declared in `package.json:5`.
- **README commands not executed:** `npx skills add …`, `node scripts/install.js init -y`, `codebuddy/claude/codex/agy/zcode plugin install` variants, `npm test`, `node scripts/build-adapters.js --check`, `node scripts/check-drift.js`, `npm run check:whitespace`, `npm run check:links`, `npm run release:gate` (`README.md:31-98`) — `"needs manual verification"`.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| **HIGH** | `README.md:100-102` declares `License: MIT` and `package.json:5` claims MIT, but **no LICENSE file exists at repo root** (`ls LICENSE*` empty; `git ls-files` filtered for `licen` finds only `docs/assets/badge-license.svg`). The README's license statement is unbacked by a file — the claim itself matches `package.json` so it is not self-contradictory, but the repository cannot ship what it declares. | `README.md:102` vs `ls` + `package.json:5` + scanner output |

## 3. `RESTRUCTURE` (diagnose-only, `lite` tier)

| Severity | Finding | Receipt |
|---|---|---|
| MEDIUM | **Over-completeness:** lines 37–74 are runbook material — per-host install recipes, live-probe run narratives, profile semantics, upgrade runbooks — on the front page. `lines 37-74 → recommended docs/` (install guide / verification-status matrix); the honest run-record prose is the project's signature but belongs in `docs/evidence/` style pages it already links to. | `README.md:37-78` |
| MEDIUM | **Density/length violations inside runbook prose:** `README.md:47` and `README.md:61` are single paragraphs of ~400 and ~600 words respectively carrying multiple host verdicts — clause-stacked blocks the `sepia` professional-pass #2 density check flags even at `lite`. | `README.md:47,61` |
| MEDIUM | **Probe-vocabulary gap:** `check-readme.py` `honest-gaps` blocks (exit 1) on a README saturated with real boundaries stated in a vocabulary the check does not match ("declared-unverified", "not live-probed", "retired") — a probe coverage gap; the README defect it signals does not exist here. See D1. | `check-readme.py` exit 1; `README.md:35,45,47,49,59-61` |
| LOW | **Repeated trust-boundary statement:** "rules version has no enforcement" is stated at `:27`, `:35`, `:45`, `:49` (four touches, each load-bearing for a different host path) — just under the convergence threshold; the README deliberately repeats it per host. | `README.md:27,35,45,49` |
| N/A — verified | No generation traces, no chatbot wrappers, no unowned comments; the prose is aggressively honest (its declared-unverified vocabulary is the project's doctrine). Skeleton fits an agent-tool README (logo → one-liner → ladder → install → verification → license). | full-file read |

## 4. `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/jiahao/README.md" --repo-root "D:/Aworker/jiahao"
exit 1 — dead-links/missing-images/code-fences/badge-domains/boundary-duplicates PASS;
honest-gaps FAIL: "No honest-gap signals found (suspicious completeness…)". repo-set: N/A.

$ python -B scripts/check-readme.py "D:/Aworker/jiahao/README-zh-CN.md" --repo-root "D:/Aworker/jiahao"
exit 1 — same single honest-gaps finding.
```

The `honest-gaps` finding is a **probe-vocabulary false negative**: the README is saturated with real repo-grounded boundaries — "declared-unverified", "not live-probed", "not for merge", "retired", "not a hostile-agent boundary", explicit unprobed-path lists (`README.md:35,45,47,49,59-61`). None of the vocabulary strings the check matches on covers this idiolect. Recorded as a blocking finding per the probe contract and as a D-series probe gap below — both true at once.

Checklist (§§1–8): §1 PASS (with the honest-gaps exit-1 recorded); §2 FAIL→HIGH (license claim unbacked); §3 PASS (first screen: logo + name + one-liner + install); §4 PASS-with-note (trust boundary ×4, load-bearing); §5 `N/A`; §6 PASS; §7 FAIL-at-lite-scope (density/runbook over-completeness, MEDIUM); §8 PASS (zero writes).

**Zero-write verification:** post-run `files=8403 tree_sha256=bbe43b88…3da9b` — identical; `git status --porcelain --ignored` identical (7 entries).

## 5. Three-line delivery report

```text
[Conclusion]: FAIL — audit on D:/Aworker/jiahao/README.md (intensity tier: lite); audit completed; findings: HIGH 1 / MEDIUM 3 / LOW 1; probe exit 1 (honest-gaps); 0 files modified.
[Receipts]: scan-project.py -> exit 0 ("license metadata but no license file"); check-readme.py README.md -> exit 1 (honest-gaps FAIL — false negative vs the README's declared-unverified boundaries), README-zh-CN.md -> exit 1 (same), repo-set: N/A; HIGH: License: MIT claimed but no LICENSE file at root (README.md:102 vs package.json:5); MEDIUM: runbook over-completeness (:37-78), 400-600-word paragraphs (:47,:61), probe-vocabulary gap (D1); LOW: trust boundary x4 (:27,35,45,49); snapshot 8403 files identical pre/post.
[Residual risk]: README commands need manual verification — npx skills add, install.js init, all plugin install paths, npm test/release:gate; external raw.githubusercontent + github.com links unfetched offline; on feat/config-dir-per-host-116 branch not main.
```

## 6. Discrepancies

| # | Severity | Discrepancy |
|---|---|---|
| D1 | MEDIUM | `check-readme.py` `honest-gaps` fires on a README that is exceptionally honest about its boundaries — the check's signal vocabulary ("limitations", "caveats", "non-goals", "trade-offs", "known issues") does not match this project's honest idiolect ("declared-unverified", "not live-probed", "retired", "not a hostile-agent boundary"). The probe is the receipt, and it blocked — so the run is FAIL — but the finding is a probe coverage gap, not a README gap. Filed for a future probe-vocabulary ticket. |
