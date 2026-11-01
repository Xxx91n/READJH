# Audit — `boxing` (Ticket #7, six-repo acceptance run)

> `audit` mode (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`, `SKILL.md` §3) on
> `D:\Aworker\crx\boxing` (remote `git@codeberg:Xxx91n/boxing.git`; the
> GitHub remote is a mirror). Diagnose-only: zero writes.

- **Run date:** 2026-11-01, Git Bash, Windows host.
- **Target:** HEAD `84983ac0ed1324d66889e656ea9827a95c6eda2b`, branch `feat/97-privacy-disclosure-alignment` (not `main` — audited state recorded verbatim). Git worktree `true`.
- **Primary README:** `README.md` (180 lines, EN); **companion localized README:** none at root — 13 localized READMEs live under `docs/i18n/` linked from an owned `README-I18N` block.
- **Run parameters:** mode `audit`; `--repo-set` not passed (check 7 `N/A`); **intensity tier `lite`** — verified author voice: terse hand-written conventional commits with ticket references (`915122c` "harden transfer - refuse opaque redirects and cap GET bodies", `f225bdf` "only write credential envelopes on genuine changes").

## 1. `ROUTE`

| Check | Result |
|---|---|
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `.agents/skills/` absent in target → trust gate not triggered |
| Root #3 `readme-crafter-skill` | canonical dir; frontmatter `name:` exact; 5/5 required files |
| README tracked/clean | `ls-files --error-unmatch` ok; `status --porcelain` empty for `README.md` |
| Baseline | `files=8409 tree_sha256=f678cb7d66e080e231c9599c942bca6718fc1c1b313315510611aaca5c93da14`; `git status --porcelain --ignored` — 19 entries to `boxing-pre.txt` (6 untracked `temp_*.json` files + 13 ignored: `.codegraph/`, `.zcode/`, `dev-*/`, `dist/`, `node_modules/`, `ntp/ntp.css`, `pages-artifact/`, `playwright-report/`, `test-results/`, `test/tests/_last-test.log`, `tools/callgraph-scan.mjs`, `tools/fix-audit.js`) |

## 2. `TRUTH`

```text
$ python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py "D:/Aworker/crx/boxing"
exit 0 — README INTEGRITY SIGNALS: 0 missing local refs (~21+ refs incl. all i18n files);
LICENSE + package.json license Apache-2.0 agree;
RISK SUMMARY: "No obvious README-to-repo mismatches detected by the scanner".
```

- **Project type:** Browser extension (Manifest V3, new-tab page). **Distribution posture:** Published Package (Edge Add-ons + Firefox Add-ons published; source build documented; store rollout tracked in docs).
- **Claim verification (verified):** 14 languages = English + 13 localized READMEs under `docs/i18n/` (`zh_CN zh_TW ja ko fr de es pt_BR ru ar hi th vi` — 13 files counted, README badge `i18n-14%20languages` consistent); license Apache-2.0 (`LICENSE` ↔ `package.json` ↔ badge); WebDAV private/loopback refusal implemented (`ntp/sync-engine.js`, `ntp/utils.js`, `ntp/i18n.js`); `.npmrc` pins registry + `min-release-age` (README npm floor claim `:147`); `npm ci`/`npm run build` scripts (`package.json:8-14`); install/store links all resolve locally; the "no `.xpi`/`.crx` on Releases" policy is a documented boundary stated once (`:80-87,111-113` — the second mention restates it inside a NOTE, a deliberate emphasis rather than a defect).
- **README commands not executed:** `npm ci`, `npm run build`, `npm install`, `npx playwright install firefox chromium`, `npm run dev:*`, `npm test` (`README.md:101-168`) — `"needs manual verification"`.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| — | **None.** All material claims bound to `file:line` receipts; zero contradicted or unbacked claims found. | — |

## 3. `RESTRUCTURE` (diagnose-only, `lite` tier)

| Severity | Finding | Receipt |
|---|---|---|
| LOW | **Front-page scope:** the WebDAV privacy policy reads as a mini threat-model (`:131-139` — SSRF rationale, opt-in mechanics, credential-key design). The project treats privacy as a front-page selling point deliberately; `lite` keeps author structure. Noted only. | `README.md:129-140` |
| LOW | **Boilerplate closer:** "Contributions are welcome!" (`:174`) — harmless single line; flagged for completeness, no rewrite demanded at `lite`. | `README.md:174` |
| N/A — verified | No generation traces: the `README-I18N` block is owned (13/13 files resolve + `TRANSLATIONS.md`); no `PLACEHOLDER`/`SLOT`/pipeline comments; no chatbot wrappers; no tracker IDs; badges workflow-backed. Skeleton fits a store-published extension (logo → one-liner → proof screenshot → differences → install → privacy). | full-file read |

`lite`-scoped language tells: none — prose is direct, specific, and honest ("Credential storage is obfuscation, not user-keyed encryption" `:139` is exemplary calibrated language).

## 4. `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/crx/boxing/README.md" --repo-root "D:/Aworker/crx/boxing"
exit 0 — all 6 single-repo checks PASS, 0 findings. (repo-set: N/A)
```

Checklist (§§1–8): §1 PASS; §2 PASS; §3 PASS (first screen: logo + one-liner + store badges + proof screenshot); §4 PASS (each boundary stated once — the .xpi/.crx note is an emphasized single policy, not a duplicated boundary); §5 `N/A`; §6 PASS; §7 PASS; §8 PASS (zero writes).

**Zero-write verification:** post-run `files=8409 tree_sha256=f678cb7d…3da14` — identical; `git status --porcelain --ignored` identical to `boxing-pre.txt` (19 entries).

## 5. Three-line delivery report

```text
[Conclusion]: PASS — audit on D:/Aworker/crx/boxing/README.md (intensity tier: lite); audit completed; findings: HIGH 0 / MEDIUM 0 / LOW 2; 0 files modified.
[Receipts]: scan-project.py -> exit 0 (0 mismatches); check-readme.py README.md -> exit 0 (6/6 PASS), repo-set: N/A; no HIGH/MEDIUM/LOW claim defects; LOW (diagnosis-only): privacy section reads threat-model-dense (:129-140), boilerplate closer (:174); snapshot 8409 files identical pre/post.
[Residual risk]: README commands need manual verification — npm ci/build/install, npx playwright install, npm run dev:*, npm test; external store/badge endpoints unfetched offline; on feat/97 branch not main.
```

## 6. Discrepancies

None observed this run.
