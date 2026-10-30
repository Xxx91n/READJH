# UPSTREAM.md — dependencies, pointer contract, deviations

READJH owns only the orchestration layer. Every other capability is an upstream
component resolved at run time or distilled into `references/`. This file is the
single record of those components: where they come from, how they are resolved,
where they sit on the authoring machine, and how READJH deviates from them.

## Pointer contract (executors)

The two executable skills are resolved **by canonical name only**, at fixed
search roots, non-recursively:

```
<skills-root>/<canonical-name>/SKILL.md
```

Search order, first hit wins:

1. `$AGENT_SKILLS_DIR` — environment override; when set it takes precedence
   over every default root below
2. `./.agents/skills/` — project-local, relative to the target repository
3. `~/.agents/skills/` — user-level (`C:\Users\<user>\.agents\skills\` on Windows)
4. `~/.claude/skills/` — Claude-style host root
5. `~/.codex/skills/` — Codex-style host root

Rules, inherited from ADR-0001:

- The directory name **must equal the canonical name** exactly, and the loaded
  `SKILL.md` frontmatter `name:` must equal it too.
- Every file listed under **required files** in the table below must exist inside
  `<skills-root>/<canonical-name>/` before the skill is accepted.
- **Project-local executable trust gate (root #2 `./.agents/skills/` and any
  `$AGENT_SKILLS_DIR` inside the target repository):** Because `TRUTH` reads
  upstream instructions (`SKILL.md`, `references/repo-integrity.md`) and
  executes `readme-crafter-skill/scripts/scan-project.py`,
  a project-local skill directory inside the target repository is never trusted
  implicitly:
  1. Without explicit user authorization for that project-local tree, READJH
     **never executes code or loads `SKILL.md` / `references/` from the
     project-local directory**. If a verified user-level installation exists at
     roots #3–#5 (`~/.agents/skills/`, `~/.claude/skills/`, `~/.codex/skills/`),
     READJH reads and executes (`python3 -s -E -B -X utf8`) directly from that
     trusted user-level installation instead; if no trusted user-level
     installation resolves, the run stops immediately as `BLOCKED`.
  2. Even when the user explicitly authorizes a project-local skill for the
     current run, READJH verifies `SKILL.md`, `references/repo-integrity.md`,
     and every file in `scripts/` (confirming no extra `.py` or `.pth` modules
     exist in `scripts/` beyond `scan-project.py`, `scan_project_readme.py`,
     and `scan_project_support.py`) and runs Python with environment and user
     site-packages disabled (`python3 -s -E -B -X utf8`).
- A missing, incomplete, or untrusted dependency **stops the run** with the
  install instructions in the table below. READJH never degrades silently.
- **No name-similarity fallback.** A directory that merely contains the name —
  nested deeper, suffixed (`-main`), prefixed — does not resolve. That is the
  wrong-skill risk the contract exists to prevent.

## Dependency table

### Executors (resolved through the pointer contract)

| canonical name | upstream URL | license | required files | search paths | observed location (2026-10-30) | state |
|---|---|---|---|---|---|---|
| `readme-crafter-skill` | https://github.com/linhai0872/readme-crafter-skill | MIT | `SKILL.md`, `references/repo-integrity.md` (in `references/`), `scripts/scan-project.py`, `scripts/scan_project_readme.py`, `scripts/scan_project_support.py` | contract list above | `C:\Users\Administrator\.agents\skills\git\readme\readme-crafter-skill-main\`, resolved at canonical `C:\Users\Administrator\.agents\skills\readme-crafter-skill` via junction (created 2026-10-31 for Ticket #5) | installed — canonical junction in place; target is a captured copy (not a Git checkout), so no live revision hash; contract resolution verified 2026-10-31 |
| `writing-humanize` | https://github.com/risadams/ink-and-agency (`skills/writing-humanize/`) | MIT (skill `license:` field; repo LICENSE MIT, fork notice credits mattpocock/skills) | `SKILL.md`, `references/patterns.md`, `agents/openai.yaml` | contract list above | `C:\Users\Administrator\.agents\repos\ink-and-agency\` @ `e1f0a00e06d55c00502e0ccbea79ab453e7fb118`, resolved at canonical `C:\Users\Administrator\.agents\skills\writing-humanize` via junction (created 2026-10-31 for Ticket #6) | installed — canonical junction in place; contract resolution verified 2026-10-31 (frontmatter `name:` + 3/3 required files) |

Upstream commits observed at authoring time: `readme-crafter-skill`
`08db7782836c542d9b597860da33fcc159e36433`, `ink-and-agency`
`e1f0a00e06d55c00502e0ccbea79ab453e7fb118`. **Revision policy:** the fresh-machine
install commands below check out these recorded commits for reproducible setup,
whereas runtime pointer-contract resolution checks canonical directory name,
`SKILL.md` frontmatter `name:`, required files, and the project-local trust gate
without enforcing a fixed Git commit hash on trusted user-level installations
(roots #3–#5). Re-check the contract and update this table when intentionally
advancing either upstream checkout.

### Distilled rule sources (read into context, never invoked)

| canonical name | upstream URL | license | required files | search paths | observed location (2026-10-30) | state |
|---|---|---|---|---|---|---|
| `sepia` | local mirror only — no canonical public upstream recorded | MIT (`license:` field in SKILL.md) | `SKILL.md`, `references/professional-pass.md`, `references/style-pass.md`, `references/languages/` (zh calibration) | n/a — distilled, not resolved | `D:\Aworker\research\ALL\.agents\skills\sepia\`, mirror commit `365185bec8c5eae8711ebd56b4f4556759f685b2` | present — source of truth for distilled rules; **no runtime dep** |
| `anti-defensive-writing` (EN, Kiterlin) | https://github.com/Kiterlin/anti-defensive-writing | MIT | `SKILL.md` | n/a — distilled | `D:\Aworker\research\ALL\vendor\anti-defensive\`, mirror commit `365185bec8c5eae8711ebd56b4f4556759f685b2` | present — distilled only. Disambiguate **by path**: a second same-named source exists at `vendor\anti-defensive-skill\` and is not used |
| `academic-humanizer` | https://github.com/AIScientists-Dev/academic-humanizer | MIT | `SKILL.md` | n/a — distilled | `D:\Aworker\research\ALL\vendor\academic-humanizer\`, mirror commit `365185bec8c5eae8711ebd56b4f4556759f685b2` | present — distilled only |
| `humanize-readme` | https://github.com/b4r7x/agent-skills (`humanize-readme/`) | MIT | `SKILL.md` (rules reference only — **never executed**, see deviations) | n/a — not resolved, read at the upstream repo | — | not installed locally; rules reference only. Upstream commit `292bad1458a30384e9e6eb3d46ba24428d7c5618` |

## Install actions

What a fresh machine needs so the contract resolves:

- **`readme-crafter-skill`** — on a fresh machine, acquire the upstream repo,
  check out the recorded commit (`08db7782836c542d9b597860da33fcc159e36433`),
  and expose its root at the canonical name:
  ```cmd
  mkdir "%USERPROFILE%\.agents\repos" "%USERPROFILE%\.agents\skills" 2>nul
  git clone https://github.com/linhai0872/readme-crafter-skill "%USERPROFILE%\.agents\repos\readme-crafter-skill" && git -C "%USERPROFILE%\.agents\repos\readme-crafter-skill" checkout 08db7782836c542d9b597860da33fcc159e36433 && mklink /J "%USERPROFILE%\.agents\skills\readme-crafter-skill" "%USERPROFILE%\.agents\repos\readme-crafter-skill"
  ```
  ```sh
  mkdir -p "$HOME/.agents/repos" "$HOME/.agents/skills" && \
  git clone https://github.com/linhai0872/readme-crafter-skill "$HOME/.agents/repos/readme-crafter-skill" && \
  git -C "$HOME/.agents/repos/readme-crafter-skill" checkout 08db7782836c542d9b597860da33fcc159e36433 && \
  ln -s "$HOME/.agents/repos/readme-crafter-skill" "$HOME/.agents/skills/readme-crafter-skill"
  ```
  On the authoring machine the tree already exists at a non-canonical path and
  the junction below was applied on 2026-10-31 (Ticket #5) — recorded here as
  already done; the options remain documented for a fresh machine:
  - junction (Windows):
    `mklink /J "%USERPROFILE%\.agents\skills\readme-crafter-skill" "%USERPROFILE%\.agents\skills\git\readme\readme-crafter-skill-main"`
    *(already created — `Get-Item` reports LinkType Junction → `…\git\readme\readme-crafter-skill-main`)*
  - or rename the directory in place to `readme-crafter-skill` at the skills
    root (loses the `git\readme` grouping).
- **`writing-humanize`** — acquire the upstream repo, check out the recorded
  commit (`e1f0a00e06d55c00502e0ccbea79ab453e7fb118`), and expose only the
  skill directory at the canonical name. On the authoring machine this was
  applied on 2026-10-31 (Ticket #6): cloned to
  `%USERPROFILE%\.agents\repos\ink-and-agency`, junction created. The options
  remain documented for a fresh machine:
  ```cmd
  mkdir "%USERPROFILE%\.agents\repos" "%USERPROFILE%\.agents\skills" 2>nul
  git clone https://github.com/risadams/ink-and-agency "%USERPROFILE%\.agents\repos\ink-and-agency" && git -C "%USERPROFILE%\.agents\repos\ink-and-agency" checkout e1f0a00e06d55c00502e0ccbea79ab453e7fb118 && mklink /J "%USERPROFILE%\.agents\skills\writing-humanize" "%USERPROFILE%\.agents\repos\ink-and-agency\skills\writing-humanize"
  ```
  ```sh
  mkdir -p "$HOME/.agents/repos" "$HOME/.agents/skills" && \
  git clone https://github.com/risadams/ink-and-agency "$HOME/.agents/repos/ink-and-agency" && \
  git -C "$HOME/.agents/repos/ink-and-agency" checkout e1f0a00e06d55c00502e0ccbea79ab453e7fb118 && \
  ln -s "$HOME/.agents/repos/ink-and-agency/skills/writing-humanize" "$HOME/.agents/skills/writing-humanize"
  ```
  Any equivalent copy of `skills/writing-humanize/` to
  `<skills-root>/writing-humanize/` satisfies the contract.

After either action, verify resolution: the file
`<skills-root>/<canonical-name>/SKILL.md` must exist, its frontmatter `name:`
must equal the canonical name, and all required files listed in the table above
(`references/repo-integrity.md`, `scripts/scan-project.py`, etc.) must exist.

## Deviation table

READJH deviates from `writing-humanize` upstream behavior in exactly two ways,
suppressed by the orchestration layer whenever it invokes the skill:

| upstream behavior | what upstream does | READJH deviation | why |
|---|---|---|---|
| self-evolve journaling | `writing-humanize` can maintain a learnings journal across runs | suppressed — no out-of-repo state is written during a READJH run | a README pass must not leak writes outside the target repository |
| personality injection | `writing-humanize` may inject voice/personality to humanize text | suppressed — voice is preserved, never fabricated | spec do-not list: no invented personality, honest gaps, or first-person stories the repo does not contain |

`humanize-readme` is a rules source only (burstiness, suspicious-completeness,
real-gap signals distilled into `references/de-ai-language.md`). It is never
executed: its own contract is internally contradictory — it demands added
"honest gaps" while forbidding added content — so READJH takes the rules and
rejects the runner.

## Drift note

Distilled `references/` files carry per-section attribution lines. When an
upstream source changes, the corresponding distilled section must be re-synced
by hand — an accepted cost of the pointer-vs-vendor split (ADR-0001). There is
no automated drift check; the commit hashes above are the audit trail.
