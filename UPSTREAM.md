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

1. `./.agents/skills/` — project-local, relative to the target repository
2. `~/.agents/skills/` — user-level (`C:\Users\<user>\.agents\skills\` on Windows)
3. `~/.claude/skills/` — Claude-style host root
4. `~/.codex/skills/` — Codex-style host root
5. `$AGENT_SKILLS_DIR` — environment override, when the host defines one

Rules, inherited from ADR-0001:

- The directory name **must equal the canonical name** exactly, and the loaded
  `SKILL.md` frontmatter `name:` must equal it too.
- A missing dependency **stops the run** with the install instructions in the
  table below. READJH never degrades silently.
- **No name-similarity fallback.** A directory that merely contains the name —
  nested deeper, suffixed (`-main`), prefixed — does not resolve. That is the
  wrong-skill risk the contract exists to prevent.

## Dependency table

### Executors (resolved through the pointer contract)

| canonical name | upstream URL | license | required files | search paths | observed location (2026-10-30) | state |
|---|---|---|---|---|---|---|
| `readme-crafter-skill` | https://github.com/linhai0872/readme-crafter-skill | MIT | `SKILL.md`, `references/`, `scripts/` (probe: `scripts/scan-project.py`; optional `scan-project.sh`) | contract list above | `C:\Users\Administrator\.agents\skills\git\readme\readme-crafter-skill-main\` | installed, **non-canonical** — nested two levels deep with a `-main` suffix, so the pointer contract does not find it; junction/rename needed (see Install actions) |
| `writing-humanize` | https://github.com/risadams/ink-and-agency (`skills/writing-humanize/`) | MIT (skill `license:` field; repo LICENSE MIT, fork notice credits mattpocock/skills) | `SKILL.md`, `references/patterns.md`, `agents/openai.yaml` | contract list above | — | **not installed locally**; clone required (see Install actions) |

Upstream commits observed at authoring time: `readme-crafter-skill`
`08db7782836c542d9b597860da33fcc159e36433`, `ink-and-agency`
`e1f0a00e06d55c00502e0ccbea79ab453e7fb118`. Upstreams are not version-pinned;
re-check the contract and this table when either repo moves.

### Distilled rule sources (read into context, never invoked)

| canonical name | upstream URL | license | required files | search paths | observed location (2026-10-30) | state |
|---|---|---|---|---|---|---|
| `sepia` | local mirror only — no canonical public upstream recorded | MIT (`license:` field in SKILL.md) | `SKILL.md`, `references/professional-pass.md`, `references/style-pass.md`, `references/languages/` (zh calibration) | n/a — distilled, not resolved | `D:\Aworker\research\ALL\.agents\skills\sepia\`, mirror commit `365185bec8c5eae8711ebd56b4f4556759f685b2` | present — source of truth for distilled rules; **no runtime dep** |
| `anti-defensive-writing` (EN, Kiterlin) | https://github.com/Kiterlin/anti-defensive-writing | MIT | `SKILL.md` | n/a — distilled | `D:\Aworker\research\ALL\vendor\anti-defensive\`, mirror commit `365185bec8c5eae8711ebd56b4f4556759f685b2` | present — distilled only. Disambiguate **by path**: a second same-named source exists at `vendor\anti-defensive-skill\` and is not used |
| `academic-humanizer` | https://github.com/AIScientists-Dev/academic-humanizer | MIT | `SKILL.md` | n/a — distilled | `D:\Aworker\research\ALL\vendor\academic-humanizer\`, mirror commit `365185bec8c5eae8711ebd56b4f4556759f685b2` | present — distilled only |
| `humanize-readme` | https://github.com/b4r7x/agent-skills (`humanize-readme/`) | MIT | `SKILL.md` (rules reference only — **never executed**, see deviations) | n/a — not resolved, read at the upstream repo | — | not installed locally; rules reference only. Upstream commit `292bad1458a30384e9e6eb3d46ba24428d7c5618` |

## Install actions

What a fresh machine needs so the contract resolves:

- **`readme-crafter-skill`** — already present but at a non-canonical path.
  Make `<skills-root>\readme-crafter-skill` resolve to the existing tree; do not
  re-clone. Either of:
  - junction (Windows):
    `mklink /J "C:\Users\Administrator\.agents\skills\readme-crafter-skill" "C:\Users\Administrator\.agents\skills\git\readme\readme-crafter-skill-main"`
  - or rename the directory in place to `readme-crafter-skill` at the skills
    root (loses the `git\readme` grouping).
- **`writing-humanize`** — not installed. Clone the repo to a stable location
  (junctions into temp dirs break on cleanup) and expose only the skill
  directory at the canonical name:
  ```
  git clone https://github.com/risadams/ink-and-agency "%USERPROFILE%\.agents\repos\ink-and-agency"
  mklink /J "C:\Users\Administrator\.agents\skills\writing-humanize" "%USERPROFILE%\.agents\repos\ink-and-agency\skills\writing-humanize"
  ```
  Any equivalent copy of `skills/writing-humanize/` to
  `<skills-root>\writing-humanize\` satisfies the contract.

After either action, verify resolution: the file
`<skills-root>\<canonical-name>\SKILL.md` must exist and its frontmatter `name:`
must equal the canonical name.

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
