# Audit — `mcp-for-maya` (Ticket #7, six-repo acceptance run)

> `audit` mode (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`, `SKILL.md` §3) on
> `D:\Aworker\maya\maya-mcp-server` (remote `git@github-Xxx91n:Xxx91n/mcp-for-maya.git`).
> Diagnose-only: zero writes.

- **Run date:** 2026-11-01, Git Bash, Windows host.
- **Target:** HEAD `108807c7937a3c18a07893de749e4cc27f42b9c2` — branch `gitbutler/workspace` (a GitButler workspace commit; audited state recorded verbatim, transient branch name noted). Git worktree `true`.
- **Primary README:** `README.md` (358 lines, EN); **companion:** `README.zh-CN.md` (382 lines, zh — lockstep).
- **Run parameters:** mode `audit`; `--repo-set` not passed (check 7 `N/A`); **intensity tier `lite`** — verified author voice: hand-written conventional-commit prose with precise scope language (`a71406d` "add opt-in safe_mode AST gate plumbing", `0403231` "say every payload, not the payload"), plus repo docs in the same register.

## 1. `ROUTE`

| Check | Result |
|---|---|
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `.agents/skills/` absent in target → trust gate not triggered |
| Root #3 `readme-crafter-skill` | canonical dir; frontmatter `name:` exact; 5/5 required files |
| README tracked/clean | `ls-files --error-unmatch` ok; `status --porcelain` empty for both READMEs |
| Baseline | `files=12665 tree_sha256=96553a66955fb651ba85b3942052a78fdcb5b0151bb9926db8f5c67471880d96`; `git status --porcelain --ignored` = ignored entries only (`.venv/`, `dist/`, `__pycache__` trees, `mypy-report.txt`, `ruff-report.json`, `dist_audit/` — 15 shown) |

## 2. `TRUTH`

```text
$ python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py "D:/Aworker/maya/maya-mcp-server"
exit 0 — README INTEGRITY SIGNALS: 358 lines, 0 missing local refs (1 local ref: README.zh-CN.md);
LICENSE present; "No obvious README-to-repo mismatches detected by the scanner".
```

- **Project type:** Library/SDK + application server (MCP server, PyPI-published). **Distribution posture:** Published Package (`pip install mcp-for-maya`, `uvx mcp-for-maya` — PyPI badge + `pip` install claim; package name `mcp-for-maya` in `pyproject.toml:6`, version `0.7.0` matching latest tag `v0.7.0`).
- **Claim verification (verified):** 25 MCP tools — counted exactly: 25 `@mcp.tool(annotations=TOOL_ANNOTATIONS[...])` registrations across `*_tools.py`, the name set matches the README's tool list 1:1 (`scene_snapshot` … `write_module`, all 25). `requires-python >=3.10` (`pyproject.toml:11` ↔ `README.md:336`). Env vars `MAYA_MCP_INCLUDE_PORTS`/`EXCLUDE_PORTS`/`DISABLE_*`/`VP2_BOTTOM_UP` all present in `src/maya_mcp_server/` (`grep -o MAYA_MCP_*`). Poly Haven host allowlist + md5 + size caps real (`src/maya_mcp_server/polyhaven.py:4-13,36-43`). `server.json` `io.github.Xxx91n/mcp-for-maya` matches the `<!-- mcp-name: ... -->` comment (`README.md:1` ↔ `server.json:3`). MIT license (`LICENSE` ↔ pyproject + badge). `maya_setup_guide`/`add_session`/`list_sessions` in the registered tool set. `scene_review` 11-check table (`README.md:295-309`) ↔ `validator_module.py:406` `scene_review_with_validators` + `scene_tools.py:889` (check names match; per-check weights are doc-level, spot-consistent).
- **README commands not executed:** `pip install mcp-for-maya`, `uvx mcp-for-maya`, `uv tool install git+https://…`, `pip install -e .`, `uv sync --frozen`, `python -m pytest tests/ -q`, `ruff check`, `mypy src`, `python -m maya_mcp_server -vv`, `cmds.commandPort(...)` (`README.md:80-94,116-134,344-350`) — `"needs manual verification"`.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| LOW | CoS "−65.8%" figure correctly scoped to the paper (`README.md:274` self-disclaims "the paper's measurement, not a benchmark of this project") — well-calibrated; noted as a positive claim-discipline example, no defect. | `README.md:274` |
| LOW | Blender-mcp comparison "measured 2026-09" (`README.md:45`) is an external-facts claim with no in-repo artifact — unbacked but self-dated; MEDIUM-adjacent, kept LOW because it names its measurement date. | `README.md:45` |

## 3. `RESTRUCTURE` (diagnose-only, `lite` tier)

| Severity | Finding | Receipt |
|---|---|---|
| MEDIUM | **Generation trace — unowned `synced-with` anchor (zh companion only, asymmetric):** `README.zh-CN.md:2` carries `<!-- synced-with: README.md @ 8402e3b — … -->`; no sync script owns it (same whitelist test as EgressAPIKEY). The EN file carries `mcp-name` (registry-owned via `server.json`) but no synced-with marker — asymmetric pair. | `README.zh-CN.md:2`; `server.json:3` for `mcp-name` ownership |
| MEDIUM | **Front-page issue/tracker IDs:** `#2`, `#31`, `#3`, `#4`, `#5`, `#6`, `#7`, `#7 real-machine checklist`, `D-163` appear in prose (`README.md:53,291,326,330`); §2 rule 4 — roadmap/issue numbers belong in the issue tracker or `docs/`, not front-page sentences (the roadmap paragraph duplicates what GitHub issues already are). | `README.md:53,291,326,330` |
| MEDIUM | **Over-complete span:** full semver versioning policy + roadmap (`README.md:320-330`) and the Tools Reference command catalog (`README.md:198-270`) are manual material — `lines 198-270 + 320-330 → recommended docs/` (the repo already has `docs/` with a threat model; the README correctly links rather than duplicates it). | `README.md:198-270,320-330` |
| LOW | **Emoji-decorated capability matrix** (`🧊🎨🎬🛡️🧠📋⚡👁️🔌📦📤🔎`): borderline — genuinely enumerable categories, but the emoji icons are decorative per `sepia` professional-pass #6 / `humanize-readme` fake-bullet list; flagged LOW at `lite` (author style preserved). | `README.md:59-72` |
| LOW | **Repeated safety boundary (2 mentions):** "safety net, not a boundary against a malicious client" at `README.md:24` (WARNING block) and `README.md:315,317` (Trust & Privacy) — three touches of one boundary; the first two are arguably the statement + its details section, the third (`:317` "misuse guardrails, not a hostile-agent boundary") re-states it again. Just under the convergence threshold; noted. | `README.md:24,315,317` |
| Whitelisted | `<!-- mcp-name: io.github.Xxx91n/mcp-for-maya -->` — owned by the MCP registry convention via `server.json`; kept. | `README.md:1`, `README.zh-CN.md:1` |

`lite`-scoped language tells: none — prose is direct, concrete, claim-calibrated ("an honest three-tier comparison" is the author's own voice, kept).

## 4. `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/maya/maya-mcp-server/README.md" --repo-root "D:/Aworker/maya/maya-mcp-server"
exit 0 — all 6 single-repo checks PASS, 0 findings.
$ python -B scripts/check-readme.py "D:/Aworker/maya/maya-mcp-server/README.zh-CN.md" --repo-root "D:/Aworker/maya/maya-mcp-server"
exit 0 — all 6 PASS, 0 findings. (repo-set: N/A)
```

Checklist (§§1–8): §1 PASS; §2 PASS (claims bound; tool count verified exactly); §3 PASS (name/one-liner/badges/install all above the fold); §4 Partial (safety boundary stated ~3×, LOW); §5 `N/A`; §6 FAIL→findings (unowned zh `synced-with`); §7 PASS; §8 PASS (zero writes).

**Zero-write verification:** post-run `files=12665 tree_sha256=96553a66…80d96` — identical; `git status --porcelain --ignored` identical.

## 5. Three-line delivery report

```text
[Conclusion]: FAIL — audit on D:/Aworker/maya/maya-mcp-server/README.md (intensity tier: lite); audit completed; findings: HIGH 0 / MEDIUM 3 / LOW 5; 0 files modified.
[Receipts]: scan-project.py -> exit 0 (0 mismatches); check-readme.py README.md -> exit 0, README.zh-CN.md -> exit 0 (6/6 PASS), repo-set: N/A; MEDIUM: unowned zh synced-with anchor (zh:2); MEDIUM: front-page issue IDs (#2,#31,#3-#7,D-163 at :53,291,326,330); MEDIUM: docs-worthy spans (Tools Reference :198-270, versioning+roadmap :320-330); LOW: literal 25-tool count verified vs claim, blender comparison unbacked (dated), emoji matrix (:59-72), safety boundary x3 (:24,315,317), GitButler workspace HEAD; snapshot 12665 files identical pre/post.
[Residual risk]: README commands need manual verification — pip/uvx install, uv sync --frozen, pytest/ruff/mypy, commandPort calls; remote raw.githubusercontent assets and PyPI/registry endpoints unfetched offline; blender-mcp "measured 2026-09" comparison unverifiable in-repo.
```

## 6. Discrepancies

| # | Severity | Discrepancy |
|---|---|---|
| D1 | LOW | `README.zh-CN.md` carries the `synced-with` anchor while `README.md` carries only `mcp-name` — the pair is structurally consistent but the sync marker is one-sided (the mirror references the authoritative file). Consistent with a manual-sync convention; flagged MEDIUM as an unowned anchor, not a structural defect. |
