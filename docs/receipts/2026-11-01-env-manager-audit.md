# Audit — `env-manager` (Ticket #7, six-repo acceptance run)

> `audit` mode (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`, `SKILL.md` §3) on
> `D:\Aworker\env-manager` (remote `git@github-Xxx91n:Xxx91n/env-manager.git`).
> Diagnose-only: zero writes.

- **Run date:** 2026-11-01, Git Bash, Windows host.
- **Target:** HEAD `c60102daf091fc80f187f0545190ec11e102448e` (`main`), Git worktree `true`.
- **Primary README:** `README.md` (253 lines, EN); **companion localized README:** none at root — the README instead carries an owned `<!-- README-I18N:START/END -->` block linking 10 localized files under `docs/i18n/` (all 10 exist; per §3 of `readme-rules.md` this is a repo-owned block, not a companion README processed in lockstep).
- **Run parameters:** mode `audit`; `--repo-set` not passed (check 7 `N/A`); **intensity tier `lite`** — verified author voice: bilingual (zh+EN) conventional-commit prose with review-turn register (`aee72952` "…（#183 审查返修）", `b8fa7c0a` "复审返修——清掉旧结局名…", `cfae30df` "…（#161 CodeRabbit 返修）").

## 1. `ROUTE`

| Check | Result |
|---|---|
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `.agents/skills/` absent in target → trust gate not triggered |
| Root #3 `readme-crafter-skill` | canonical dir; frontmatter `name:` exact; 5/5 required files |
| README tracked/clean | `ls-files --error-unmatch` ok; `status --porcelain` empty for `README.md` |
| Baseline | `files=29706 tree_sha256=06cdcd28088e95f511af86b8e6066ec66f97f2d7c6a865cc643047736786a77e`; `git status --porcelain --ignored` — 24 entries captured verbatim to `env-manager-pre.txt` (one **untracked** `?? .workbuddy/` plus 23 ignored: `.codegraph/`, `.env_bak/`, `.keys/`, `.test-backups/`, `.test-logs/`, `.zcode/`, `StrykerOutput/`, `bin/`, `dist/`, `frontend/.vitest-*.log`, `frontend/node_modules/`, `frontend/src-tauri/{bin,gen,target}/`, `node_modules/`, `obj/`, `release/`, `scripts/hooks/gh-script-v9/dist/`) |

## 2. `TRUTH`

```text
$ python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py "D:/Aworker/env-manager"
exit 0 — README INTEGRITY SIGNALS: 253 lines, 0 missing local refs (34+ refs resolve);
LICENSE present, package.json license: —;
RISK SUMMARY: "README mentions env vars missing from env example: API_KEY, OP_SERVICE_ACCOUNT_TOKEN, VAULT_TOKEN".
```

- **Project type:** Desktop application + CLI dual-mode (.NET 10 C# CLI + Rust service + Tauri 2/Svelte GUI). **Distribution posture:** Product/Monorepo Hub (MSI/portable/CLI-only releases; source build path documented).
- **Claim verification (verified):** license Apache-2.0 (`LICENSE` ↔ badge `License-Apache--2.0` ↔ `README.md:253`); Tauri 2 (`README.md:22,23` ↔ `frontend/` Tauri source); .NET 10 (build prereq `README.md:151` ↔ badge); `AGENTS.cli.md` exists and `AgentsCommand.cs` implements `agents` (`scripts/../src` — `AgentsCommand.cs` present; `README.md:58,71-75`); 8 secret providers table (`README.md:206-218`) ↔ `docs/secret-providers-guide.md`; `README-I18N:START/END` block ↔ all 10 files under `docs/i18n/` (`README.zh_CN.md`, `ja`, `ko`, `de`, `fr`, `es`, `pt`, `ru`, `ar`); demo/gallery assets all resolve (scanner 0 missing; 24+ gallery PNGs + hero.gif + demo.gif); CLI verbs in usage block match documented commands (`list`/`get`/`set`/`profile …`/`path health`/`backup`/`restore`/`export-state`/`audit verify`/`service status` ↔ `docs/cli-commands.md`).
- **README commands not executed:** `env-manager-cli.exe …` block (`README.md:158-181`), `npm ci`, `node scripts/build.mjs --arch x64`, `node scripts/demo/capture.mjs` (`README.md:43,144-149`) — `"needs manual verification"`.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| LOW | Scanner flags `API_KEY`, `OP_SERVICE_ACCOUNT_TOKEN`, `VAULT_TOKEN` "missing from env example" — they are provider **auth methods** in the provider table, not app runtime env vars, and no `.env.example` exists by design; the flag is a scanner-context artifact, recorded as LOW per §5 D1-style discrepancy rather than a README defect. | `scan-project.py` output; `README.md:165,213,216` |
| LOW | "18+ commands" (`README.md:58`) — `AGENTS.cli.md` exists and the agents command is implemented; the exact count is doc-level (the manual is the authority). Verified-present, count unverified. | `README.md:58` ↔ `AGENTS.cli.md`, `AgentsCommand.cs` |

## 3. `RESTRUCTURE` (diagnose-only, `lite` tier)

| Severity | Finding | Receipt |
|---|---|---|
| MEDIUM | **Clustered AI-vocabulary / marketing inflation:** `"Adapts seamlessly to every environment."` tagline in quotes (`:17` — `seamlessly` is on every ban list), `"A modern, lightweight … manager"` opener (`:15` — `modern`/`lightweight` are zero-information adjectives), "one variable, every environment — chameleon variants" alt text (`:34`). `lite` scope: clustered ban-list words — flagged, author register otherwise kept. | `README.md:15,17,34` |
| LOW | **Boundary restated 2×:** the code-signing/SmartScreen boundary appears as a WARNING block (`:83-84`) and is reasserted inside the Security prose (`:86` context) — mild; the WARNING block is the single statement, surrounding text elaborates rather than duplicates. Just under the §2 threshold; noted. | `README.md:83-88` |
| LOW | **Front-page scope:** the secret-boundary table (`:90-110`) is the strongest section but occupies the pre-Install fold — arguably the project's security story *is* the product; kept LOW, `lite` preserves author structure. | `README.md:90-112` |
| N/A — verified | No `PLACEHOLDER`/`SLOT`/pipeline tags, no chatbot wrappers, no cutoff disclaimers, no unowned HTML comments. The i18n START/END block is owned (10/10 files resolve). Skeleton fits an application product page (hero → demos → features → install → usage → docs). | full-file read |

## 4. `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/env-manager/README.md" --repo-root "D:/Aworker/env-manager"
exit 0 — all 6 single-repo checks PASS, 0 findings. (repo-set: N/A)
```

Checklist (§§1–8): §1 PASS; §2 PASS (claims bound; the 3 env-var flags contextualized); §3 PASS (first screen: logo + one-liner + badges + nav + install anchors); §4 PASS-with-note (boundary once, mild restatement LOW); §5 `N/A`; §6 PASS (no generation traces; i18n block owned); §7 FAIL-at-lite-scope (clustered marketing vocabulary, MEDIUM); §8 PASS (zero writes).

**Zero-write verification:** post-run `files=29706 tree_sha256=06cdcd28…a77e` — identical; `git status --porcelain --ignored` identical to `env-manager-pre.txt` (24 entries incl. the pre-existing `?? .workbuddy/`).

## 5. Three-line delivery report

```text
[Conclusion]: FAIL — audit on D:/Aworker/env-manager/README.md (intensity tier: lite); audit completed; findings: HIGH 0 / MEDIUM 1 / LOW 4; 0 files modified.
[Receipts]: scan-project.py -> exit 0 (3 provider-auth env vars flagged vs absent .env.example — context artifact); check-readme.py README.md -> exit 0 (6/6 PASS), repo-set: N/A; MEDIUM: clustered marketing vocabulary ("Adapts seamlessly to every environment" :17, "modern, lightweight" :15); LOW: 18+-command count doc-level (:58), boundary restated ~2x (:83-88), boundary table pre-Install fold (:90-112), provider-auth env-var scanner flag (context artifact vs absent .env.example); context notes (not findings): untracked .workbuddy/ in baseline; snapshot 29706 files identical pre/post.
[Residual risk]: README commands need manual verification — env-manager-cli.exe verbs, npm ci, node scripts/build.mjs, demo capture script; external shields.io + dotnet.microsoft.com links unfetched offline; "18+ commands" count asserted by AGENTS.cli.md not re-counted.
```

## 6. Discrepancies

| # | Severity | Discrepancy |
|---|---|---|
| D1 | LOW | `scan-project.py` reports provider-auth env vars as "missing from env example" when the repo ships no `.env.example` by design — same class of context-artifact as Ticket-#5's D-series: the scan is complete and exit 0, but the flag needs README-side interpretation (auth-method table entries, not app env vars). |
