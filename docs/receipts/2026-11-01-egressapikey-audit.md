# Audit — `EgressAPIKEY` (Ticket #7, six-repo acceptance run)

> `audit` mode (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`, `SKILL.md` §3) on
> `D:\Aworker\EgressAPIKEY`. Diagnose-only: zero writes to the target.

- **Run date:** 2026-11-01, Git Bash, Windows host.
- **Target:** `D:\Aworker\EgressAPIKEY` — HEAD `4826153df3d192d44baa6072f5e43a2e26a9d38e` (`main`), Git worktree `true`.
- **Primary README:** `README.md` (140 lines, English); **companion:** `README_CN.md` (140 lines, zh — lockstep).
- **Run parameters:** mode `audit`; `--repo-set` not passed (check 7 `N/A`); **intensity tier `lite`** — verified author voice in hand-written conventional-commit prose with review-turn style (e.g. `3baff964` "docs: address #41 review — plural ticket pointer…", `d166a959` "cite GLOSSARY.md by term and attribute only the floor").

## 1. `ROUTE`

| Check | Result |
|---|---|
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `D:\Aworker\EgressAPIKEY\.agents\skills\` absent → project-local trust gate not triggered |
| Root #3 `~/.agents/skills/readme-crafter-skill` | dir name exact; `SKILL.md` frontmatter `name:` exact; 5/5 required files present |
| Root #3 `~/.agents/skills/writing-humanize` (resolved for the later dry-run) | dir name exact; frontmatter `name: writing-humanize` exact; `references/patterns.md` + `agents/openai.yaml` present |
| Roots #4/#5 | `~/.claude/skills/` (gitbutler, jiahao), `~/.codex/skills/` (atomcode-research, gitbutler) — neither carries a canonical-name candidate; root #3 hits first anyway |
| README tracked/clean | `git ls-files --error-unmatch -- README.md` ok; `status --porcelain` empty for both READMEs |
| Baseline | `files=33801 tree_sha256=03808456ed37a10e21fc1b9ddb3aa4efed5992bccc643be9782a2b458d8c1841`; `git status --porcelain --ignored` = 13 ignored entries (`.codegraph/`, `.npmrc`, `.opencode/`, `.scratch/`, `bench-results/`, `dist/`, `node_modules/`, `resin/`, 2× `src-tauri/binaries/resin-*.exe`, `src-tauri/gen/`, `target/`, `tsconfig.tsbuildinfo`) |

## 2. `TRUTH`

```text
$ python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py "D:/Aworker/EgressAPIKEY"
exit 0 — README INTEGRITY SIGNALS: README.md 140 lines; Missing local refs: assets/readme/<name>.png;
LICENSE & TRUST: LICENSE file present, package.json license GPL-3.0-or-later.
```

- **Project type:** Desktop / web application (Tauri 2 + React 19, headless twin). **Distribution posture:** Product/Monorepo Hub (packaged installers + source-first dev path; `@egressapikey/server` explicitly not on npm).
- **Claim verification (verified):** Tauri 2/React 19 (`package.json` deps `@tauri-apps/api ^2`, `react ^19`); license GPL-3.0-or-later (`package.json` `license` ↔ `LICENSE`); `scripts/fetch_resin.sh` pulls binary pinned by `docs/RESIN_UPSTREAM_MANIFEST.yaml` `version: "v1.2.0"` ↔ `scripts/fetch_resin.sh:9-16`; `resin/` gitignored (`.gitignore:94`); `include_intel_mac` dispatch input (`.github/workflows/ci.yml:31,227`); headless `http://127.0.0.1:14200` (`src-tauri/src/headless_security.rs:471-489`); `RESIN_PROXY_TRANSPORT_*` env vars (`src-tauri/src/sidecar.rs:498-507`); `allocation_policy` values BALANCED/PREFER_LOW_LATENCY/PREFER_IDLE_IP (`crates/resin-core/src/strategy_engine.rs:696-701`); entry-port range `:18000…` (`crates/resin-core/src/db.rs:729-739`); Mode A/Mode B dual data plane and Mode-B plain-HTTP buffering caveat (`CHANGELOG.md` round-8 IMP-1/A-001 entry, `README.md:85-91`); `docs/` links all resolve (scanner + probe `dead-links` PASS).
- **README commands not executed:** `pnpm install && pnpm build`, `cargo build --release -p egressapikey-app --bin egressapikey-headless --features headless`, `bash scripts/fetch_resin.sh`, `pnpm tauri dev` (`README.md:72-77,108-113`) — flagged `"needs manual verification"`.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| LOW | `assets/readme/<name>.png` flagged "missing" by the scanner — the literal path lives inside a SLOT instruction comment (`README.md:96,99-101`), not a real reference; context for the generation-trace findings below, not a defect of its own. | `scan-project.py` output; `README.md:96-100` |
| LOW | "Node.js 20+" prereq has no `engines` field in `package.json` (repo has none); claim is consistent with `@types/node ^22` and Tauri v2 prerequisites link — unbacked by an in-repo floor, not contradicted. | `README.md:106` vs `package.json` (no `engines`) |

## 3. `RESTRUCTURE` (diagnose-only, `lite` tier)

| Severity | Finding | Receipt |
|---|---|---|
| MEDIUM | **Generation traces — unowned `synced-with` anchors:** `<!-- synced-with: README_CN.md @ 0de816af… -->` / `<!-- synced-with: README.md @ 0de816af… -->` at the top of both files. The whitelist (`references/readme-rules.md` §3) requires a script or sync tool that owns the anchor — `grep -rn "synced" scripts/ .github/ e2e/` and a repo-wide hash/README-harness search found no owner. Flag and remove. | `README.md:1`, `README_CN.md:1` |
| MEDIUM | **Generation traces — readme-crafter scaffolding comments:** `<!-- PLACEHOLDER: … (readme-crafter rule). -->`, `<!-- Drop-in: replace each comment block … -->`, three `<!-- SLOT … -->` comments, and the zh mirrors `<!-- 占位 -->` / `<!-- 投放 -->` / three `SLOT` comments. Skill scaffolding left in the rendered file; §3 says remove the comments and state the missing-asset absence once (the italic `_Screenshots pending …_` line already does). | `README.md:95-101`; `README_CN.md:95-101` |
| LOW | **Repeated span, not a boundary:** the `scripts/fetch_resin.sh` + gitignored-`resin/` explanation is stated three times (`README.md:23`, `README.md:25`, `README.md:136`; zh `:23/:25/:136`). The §2 self-attestation rule covers repeated *boundaries*, not facts — flagged LOW redundancy, first statement authoritative. | `README.md:23,25,136` |
| N/A — verified | Compliance/legal boundary stated once at the end (`README.md:126-128`); singular, positive-scope, correct location. Not a finding. | `README.md:126-128` |
| N/A — verified | No tracker/decision IDs, no chatbot wrappers, no cutoff disclaimers, no clustered AI vocabulary found (`lite` scope). Skeleton fits an application hub posture (hero → what/why → modes → download → features → docs table); install path sits mid-page but the Download section precedes Features. | full-file reads |

## 4. `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/EgressAPIKEY/README.md" --repo-root "D:/Aworker/EgressAPIKEY"
exit 0 — dead-links PASS, missing-images PASS, code-fences PASS, badge-domains PASS, boundary-duplicates PASS, honest-gaps PASS; repo-set: N/A.

$ python -B scripts/check-readme.py "D:/Aworker/EgressAPIKEY/README_CN.md" --repo-root "D:/Aworker/EgressAPIKEY"
exit 0 — same six checks PASS; 0 findings.
```

Checklist (`references/checklist.md` §§1–8): §1 PASS (probe + scanner receipts, no AI-detector, zero README commands run); §2 PASS (claims bound to `file:line`; Node-20 floor LOW-noted); §3 PASS (first screen: name + one-liner + badges + download before the fold ends); §4 PASS for boundaries (single compliance statement) with the LOW fact-repetition noted; §5 `N/A` (no `--repo-set`; skeleton fits posture); §6 **FAIL → findings** (unowned `synced-with` + PLACEHOLDER/SLOT/Drop-in scaffolding); §7 PASS (`lite` scope clean); §8 PASS (audit, zero writes, three-line report below).

**Zero-write verification:** post-run `files=33801 tree_sha256=03808456ed37a10e21fc1b9ddb3aa4efed5992bccc643be9782a2b458d8c1841` — identical; `git status --porcelain --ignored` identical (13 ignored entries).

## 5. Three-line delivery report

```text
[Conclusion]: FAIL — audit on D:/Aworker/EgressAPIKEY/README.md (intensity tier: lite); audit completed; findings: HIGH 0 / MEDIUM 2 / LOW 4; 0 files modified.
[Receipts]: scan-project.py -> exit 0 (1 literal-placeholder ref inside a comment); check-readme.py README.md -> exit 0 (6/6 PASS), README_CN.md -> exit 0 (6/6 PASS), repo-set: N/A; MEDIUM: unowned synced-with anchors (README.md:1, README_CN.md:1); MEDIUM: readme-crafter scaffolding comments (README.md:95-101, README_CN.md:95-101); LOW: scanner literal-placeholder ref (:96-100), Node-20 floor unbacked (:106), repeated fetch_resin span (:23,25,136), shallow-scan caveat; tree snapshot 33801 files identical pre/post, git status identical.
[Residual risk]: README commands need manual verification — pnpm install/build, cargo build --release …egressapikey-headless, bash scripts/fetch_resin.sh, pnpm tauri dev; external shields.io badge URLs and github.com release/RESIN links unfetched offline.
```

## 6. Discrepancies (SKILL.md ↔ observed behavior)

| # | Severity | Discrepancy |
|---|---|---|
| D1 | LOW | The probe's `dead-links` passes while the scanner counts `assets/readme/<name>.png` "missing" — the probe correctly skips links inside HTML comments while `scan-project.py` counts comment-interior refs. Consistent behavior, different granularity; noted so the scanner count isn't mistaken for a real broken link. |
