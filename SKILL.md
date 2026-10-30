---
name: readjh
description: >
  Orchestrates repository README governance across audit, improve, and rewrite
  runs using receipt-backed truth checks, front-page restructuring, de-AI prose
  cleanup, and static probe verification. Use when asked to audit, critique,
  improve, rewrite, de-AI, humanize, or verify a README, or to check cross-repo
  README skeleton isomorphism with --repo-set.
license: MIT
---

# READJH — README Governance Orchestration Skill

READJH is a thin **orchestration layer** for one-shot README governance. The
repository root is the skill itself (`SKILL.md`, `references/`, `scripts/`,
`UPSTREAM.md`, `NOTICE` — ADR-0002, no build step or host adapter generator).
It sequences upstream executors through a **pointer contract**, applies
README-specific **orchestration layer** rules and **distilled rules** from
`references/`, and closes every run with machine-checkable **receipts** from
`scripts/check-readme.py` plus a binary assertion checklist
(`references/checklist.md`).

The pipeline runs five phases in strict sequence:

```text
ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY
```

Deletion and structural migration always precede wording changes. Every
completion claim requires a concrete **receipt**; AI-detector scores carry zero
weight and are never accepted.

---

## 1. Pointer Contract Resolution

READJH resolves its two upstream executable skills **by canonical name only**,
at fixed search roots, non-recursively (`UPSTREAM.md`, ADR-0001):

```text
<skills-root>/<canonical-name>/SKILL.md
```

### Search Order (First Hit Wins)

1. `$AGENT_SKILLS_DIR` — environment override; when set it takes precedence
   over every default root below
2. `./.agents/skills/` — project-local, relative to the target repository
3. `~/.agents/skills/` — user root (`C:\Users\<user>\.agents\skills\` on Windows)
4. `~/.claude/skills/` — Claude-style host root
5. `~/.codex/skills/` — Codex-style host root

### Resolution Rules

- **Exact canonical match:** The directory name **must equal the canonical
  name** byte-for-byte, and the loaded `SKILL.md` YAML frontmatter `name:`
  field must equal the canonical name too.
- **Stop on miss (zero silent degradation):** A missing or mismatched
  dependency **stops the run immediately** with the install instructions below.
  READJH never degrades to built-in guesswork and **never writes, creates, or
  modifies any file** when a required dependency fails resolution.
- **No name-similarity fallback:** A directory that merely contains the
  canonical name — nested deeper (such as
  `git/readme/readme-crafter-skill-main/`), suffixed (`-main`), or prefixed —
  does **not** resolve.
- **Distilled rules are read, never invoked as skills:**
  `references/readme-rules.md`, `references/de-ai-language.md`, and
  `references/checklist.md` live in this skill's `references/` directory and
  are read into context directly. `humanize-readme` contributes **distilled
  rules** only (`references/de-ai-language.md` §6) and is **never executed**.

### Pointer-Contract Dependencies

`UPSTREAM.md` is the single record for observed machine locations, upstream
commit hashes, install actions, and deviations. At run time, READJH resolves
these two executors through the **pointer contract** above:

| Canonical name | Upstream repository | Required files | Role in pipeline |
|---|---|---|---|
| `readme-crafter-skill` | `linhai0872/readme-crafter-skill` (`https://github.com/linhai0872/readme-crafter-skill`) | `SKILL.md`, `references/`, `scripts/` (`scripts/scan-project.py`; optional `scan-project.sh`) | `TRUTH` & `RESTRUCTURE` (required by `audit`, `improve`, and `rewrite`) |
| `writing-humanize` | `risadams/ink-and-agency` (`skills/writing-humanize/`, `https://github.com/risadams/ink-and-agency`) | `SKILL.md`, `references/patterns.md`, `agents/openai.yaml` | `LANGUAGE` (required by `improve` and `rewrite`) |

### Stop-on-Miss Install Instructions

When a required executor cannot be resolved at any of the five search roots,
abort before touching any file and emit the three-line report (§4) together
with the matching install action from `UPSTREAM.md`:

- **Acquire `readme-crafter-skill` on a fresh machine (or junction/rename an existing non-canonical checkout per `UPSTREAM.md`):**
  ```cmd
  mkdir "%USERPROFILE%\.agents\repos" 2>nul
  git clone https://github.com/linhai0872/readme-crafter-skill "%USERPROFILE%\.agents\repos\readme-crafter-skill"
  mklink /J "%USERPROFILE%\.agents\skills\readme-crafter-skill" "%USERPROFILE%\.agents\repos\readme-crafter-skill"
  ```
- **Acquire `writing-humanize` (or copy `skills/writing-humanize/` to `<skills-root>\writing-humanize\` per `UPSTREAM.md`):**
  ```cmd
  mkdir "%USERPROFILE%\.agents\repos" 2>nul
  git clone https://github.com/risadams/ink-and-agency "%USERPROFILE%\.agents\repos\ink-and-agency"
  mklink /J "%USERPROFILE%\.agents\skills\writing-humanize" "%USERPROFILE%\.agents\repos\ink-and-agency\skills\writing-humanize"
  ```
- **Post-install verification:** confirm `<skills-root>\<canonical-name>\SKILL.md`
  exists and its frontmatter `name:` equals `<canonical-name>`.

---

## 2. Inline Orchestration Rules (`GLOSSARY.md`)

Full rule bodies and attributions live in `references/readme-rules.md` and
`references/de-ai-language.md`. These core contracts bind every phase:

### Freeze Zone (`references/readme-rules.md` §1)

A **freeze zone** is any README region that no language pass (`writing-humanize`
or **distilled rules**) may alter, reword, reformat, or delete:

1. **Commands and code:** fenced code blocks, inline command spans, CLI flags,
   and environment variable names.
2. **Links and paths:** URLs, local file paths, markdown link targets, query
   strings, and anchors.
3. **Exact identifiers and metrics:** version strings, commit hashes, benchmark
   numbers, and error or exit codes.
4. **Badges:** markdown and HTML badge rows and their target URLs.
5. **Legal and safety boundaries:** `LICENSE` notices, `NOTICE` attributions,
   cryptographic/security boundary statements, and compliance text.
6. **Direct quotations:** quoted command transcripts and speaker quotes inside
   `"..."` or `「...」`.

**Phase boundary:** If a **freeze zone** span contradicts the repository (for
example, a flag absent from the CLI parser or a dead local link), `TRUTH`
reports it as a finding with its `file:line` **receipt**. `LANGUAGE` never
mutates a **freeze zone** span.

### Intensity Tiers and No-Invented-Personality Rule (`references/readme-rules.md` §5)

| Intensity tier | Selection condition | Scope |
|---|---|---|
| `lite` | The repository already shows a verified human author voice (in commits, issues, or existing docs) or the user supplies an author writing sample. | Preserve the author's sentence rhythm, punctuation habits, contractions, and register. Flag or strip only clustered AI vocabulary, chatbot turn wrappers, and repeated **self-attestation**. |
| `standard` | Default when no verified author voice or writing sample is present. | Apply the full `writing-humanize` catalog plus `references/de-ai-language.md`: collapse abstract-noun chains, split clause-stacked sentences, recast defensive caveats into `fact + link`, and vary uniform sentence rhythm by moving words without adding filler. |

**Hard prohibitions (both intensity tiers):**

- **No invented personality, gaps, or stories:** Neither **intensity tier** may
  insert fabricated first-person stories (`"I built this because..."`), casual
  banter, or unverified limitations / `"honest gaps"` not backed by a
  repository **receipt**.
- **Two `writing-humanize` suppressions (`UPSTREAM.md`):** Whenever
  `writing-humanize` is invoked, suppress (1) **self-evolve journaling** (never
  write to `~/.ink-and-agency/` or outside the target repository) and (2)
  **personality injection** (ignore `writing-humanize` Step 5 / `PERSONALITY AND
  SOUL`).
- **Static safety:** Never execute commands documented inside a target README.
- **Bilingual discipline:** Detect existing bilingual README pairs (such as
  `README.md` + `README-ZH.md` or `README.zh-CN.md`) and process them in
  lockstep with aligned section structure; apply the Chinese (`zh`) calibration
  rules (`references/de-ai-language.md` §3) to Chinese prose; never create a
  second-language README unless the user explicitly asks.

---

## 3. Audit-Mode Spine (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`)

In `audit` mode, READJH diagnoses and prioritizes README defects end to end
without writing or modifying any files in the target repository.

### Phase 1: `ROUTE`

1. **Lock run parameters:**
   - Run mode: `audit` (read-only diagnosis; `--dry-run` is naturally satisfied
     because `audit` performs zero writes).
   - Target path: `<readme>` (defaults to `<repo-root>/README.md`) and
     `<repo-root>` (defaults to the parent directory of `<readme>`).
   - Optional **repo-set mode**: enabled only when the user passes
     `--repo-set <manifest>`; off by default on single-repository runs.
2. **Select intensity tier:**
   - Sample repository commit messages, issues, or user-provided prose samples.
     Select `lite` when a distinct author voice is verified; otherwise select
     `standard`.
3. **Detect language and companion files:**
   - Record the primary language of `<readme>` and any existing localized
     companion README so `TRUTH` and `RESTRUCTURE` check them in lockstep.
4. **Enforce the pointer contract (§1):**
   - Resolve `readme-crafter-skill` using the search order and canonical match
     rules in §1. If resolution fails, apply the §1 stop-on-miss gate
     immediately (zero file writes; emit the §4 three-line blocked report with
     the §1 install instructions).

**Completion criterion:** Run mode (`audit`), target `<readme>`, `<repo-root>`,
**intensity tier** (`lite` | `standard`), **repo-set mode** state, and the
resolved canonical path `<skills-root>/readme-crafter-skill/SKILL.md` are
confirmed.

### Phase 2: `TRUTH`

1. **Load upstream executor and gather repository facts:**
   - Read the resolved `<skills-root>/readme-crafter-skill/SKILL.md` and its
     `references/repo-integrity.md`.
   - Run `readme-crafter-skill`'s project scanner (`scripts/scan-project.sh
     <repo-root>` or `python3 scripts/scan-project.py <repo-root>`) when
     available, and inspect repository-native sources directly: package
     manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`),
     lockfiles, CI workflows (`.github/workflows/`), entry points, root exports,
     `.env.example`, config schemas, and `LICENSE`.
   - **Never execute commands documented inside `<readme>`.** Record any README
     command that cannot be statically confirmed against manifests or scripts
     for disclosure as `"needs manual verification"` in `[Residual risk]`.
2. **Classify project type and distribution posture:**
   - Determine the repository's **Project Type** (CLI Tool, Library/SDK,
     Application, Research Project, etc.) and **Distribution Posture**
     (Published Package, Source-first Repository, Hybrid, or Product/Monorepo
     Hub) per `readme-crafter-skill`.
3. **Verify every README claim against repository receipts:**
   - Cross-check every install command, CLI flag, environment variable, code
     import, version requirement, badge, benchmark metric, and **freeze zone**
     span against repository `file:line` anchors.
   - Rank every truth discrepancy by severity:
     - **`HIGH` (Contradicted claim):** `<readme>` states a fact, command, flag,
       export, path, or registry publication contradicted by the repository.
       Record `<readme>:<line>` alongside the contradicting `<repo-file>:<line>`
       **receipt**. Never silently patch contradicted facts.
     - **`MEDIUM` (Unbacked claim):** `<readme>` makes an empirical,
       performance, or capability claim (`references/de-ai-language.md` §5)
       with no repository **receipt**. Flag for deletion or explicit `TODO`
       marking.
     - **`LOW` (Imprecise or stale non-blocking detail):** Minor metadata or
       wording drift where the underlying capability exists.

**Completion criterion:** Every factual claim and **freeze zone** span in
`<readme>` is either matched to a repository `file:line` **receipt** or logged
as a `HIGH` / `MEDIUM` / `LOW` finding, with zero README commands executed.

### Phase 3: `RESTRUCTURE` (Diagnose-Only in `audit` Mode)

1. **Load orchestration and distilled rule files:**
   - Read `references/readme-rules.md` (§§1–5) and
     `references/de-ai-language.md` (§§1–6, loading §3 whenever `<readme>`
     contains Chinese text).
2. **Diagnose front-page boundary and over-completeness (`references/readme-rules.md` §4.1):**
   - Evaluate the 30-second first screen (`readme-crafter-skill` Checks #1, #3,
     #4: project name, artifact type, plain-language problem solved, and
     shortest verified install/run path).
   - Identify deep reference sections inside `<readme>` that belong in `docs/`
     (exhaustive CLI/API tables, threat models, security boundary matrices,
     versioning policies, contributor runbooks). Record each candidate move as
     `source heading (lines X–Y) → recommended docs/<file>.md` without touching
     files.
3. **Diagnose self-attestation repeats (`references/readme-rules.md` §2 & `references/de-ai-language.md` §4):**
   - Flag every boundary, preview disclosure, or operational caveat stated more
     than once across `<readme>`, standalone honesty-proclaiming sections,
     multi-clause negative disclaimers that should be recast as `fact + link`,
     and internal issue/decision IDs leaked onto the front page.
4. **Diagnose generation traces (`references/readme-rules.md` §3):**
   - Flag leftover skill or placeholder HTML comments (`<!-- PLACEHOLDER ... -->`,
     `<!-- SLOT ... -->`, `<!-- Drop-in ... -->`, `<!-- self-evolve:start -->`),
     pipeline tags (`[ROUTE]`, `[TRUTH]`, `[LANGUAGE]`), chatbot turn wrappers,
     and knowledge-cutoff disclaimers.
   - Check surviving HTML comments against the repository ownership whitelist
     (`references/readme-rules.md` §3): only generator boundaries or sync
     anchors actively read/written or owned by an existing repository script or
     companion file are allowed.
5. **Diagnose skeleton isomorphism and prose tells (`references/readme-rules.md` §4.2, §5 & `references/de-ai-language.md`):**
   - Check whether the heading skeleton fits the repository's Project Type and
     Distribution Posture rather than a generic boilerplate outline.
   - Outside the **freeze zone**, catalog prose tells under the active
     **intensity tier** (`lite` or `standard`): clustered ban-list vocabulary,
     abstract-noun chains, trailing `-ing` clauses, uniform sentence-length
     runs (3+ sentences), and Chinese (`zh`) calibration tells.

**Completion criterion:** All structural, **self-attestation**, **generation
trace**, **skeleton isomorphism**, and language findings are recorded with
severity (`HIGH` / `MEDIUM` / `LOW`) and `<readme>:<line>` anchors; zero files
are modified.

### Phase 4: `VERIFY`

1. **Run the static probe (`scripts/check-readme.py`):**
   - Execute:
     ```bash
     python3 <readjh-root>/scripts/check-readme.py <readme> --repo-root <repo-root> [--repo-set <manifest>]
     ```
   - Capture the exit code (`0` = pass, `1` = blocking findings, `2` = usage
     error) and stdout **receipt** covering all seven checks:
     1. `dead-links` — dead local markdown and HTML links (including badge link targets)
     2. `missing-images` — missing local markdown images, `<img>`, and `<source srcset>` paths
     3. `code-fences` — unclosed or mismatched backtick/tilde code fences
     4. `badge-domains` — placeholder or invalid badge URL hosts
     5. `boundary-duplicates` — repeated boundary/disclaimer phrases (**self-attestation** count)
     6. `honest-gaps` — presence of repo-grounded limitation/caveat/non-goal signals
     7. `repo-set` — cross-repo **skeleton isomorphism** comparison when `--repo-set <manifest>` is supplied
2. **Walk the binary verification checklist (`references/checklist.md`):**
   - Evaluate `references/checklist.md` §§1–8 against the probe output and the
     `TRUTH` / `RESTRUCTURE` findings.
   - Confirm that zero files were written or modified in the target repository
     (and no `.bak` or out-of-repo files were created).
3. **Emit the three-line delivery report (§4).**

**Completion criterion:** `scripts/check-readme.py` has been executed, its
stdout **receipt** and exit code are captured, `references/checklist.md` items
are evaluated, working-tree cleanliness is verified, and the three-line report
is emitted.

---

## 4. Three-Line Delivery Report Format

Every READJH run — whether a completed `audit` or a run halted by a missing
**pointer contract** dependency — closes with a report locked to **at most
three lines** (`docs/spec/0001-readjh-orchestration-skill.md` US-27,
`references/checklist.md` §8):

```text
[Conclusion]: <PASS | FAIL | BLOCKED> — <mode> on <target> (intensity tier: <lite|standard>); <summary of outcome or HIGH/MEDIUM/LOW finding counts>.
[Receipts]: <probe command + exit code + per-check results; severity-ranked findings (HIGH / MEDIUM / LOW) with <readme>:line and <repo-file>:line anchors — or checked canonical search paths 1..5 when BLOCKED>.
[Residual risk]: <README commands flagged "needs manual verification" (never executed), unverified external targets, or required UPSTREAM.md install commands when BLOCKED>.
```

### Report Rules

- **Strict three-line cap:** The final response contains only `[Conclusion]`,
  `[Receipts]`, and `[Residual risk]` (in `improve` / `rewrite` runs that move
  material to `docs/`, only the migration ledger table may follow).
- **No receipt, no claim:** Every finding or pass assertion in `[Conclusion]`
  must be backed by a command exit code, probe check name, or `file:line`
  anchor in `[Receipts]`.
- **Untested README commands:** Because READJH never executes commands inside a
  target README, `[Residual risk]` must list any README commands not verified
  against repository scripts as `"needs manual verification"`.

---

## 5. Future Phases Stub (`improve` and `rewrite` Modes — Ticket #6)

`improve` mode (surgical README upgrade), `rewrite` mode (full README rebuild),
and the active `LANGUAGE` execution phase (`writing-humanize` invocation via
the **pointer contract**, **distilled rules** handoff from
`references/de-ai-language.md` and `references/readme-rules.md`, **freeze
zone** enforcement during edits, `docs/` migration ledger emission, `.bak`
rollback file creation when git cannot roll back cleanly, and `--dry-run` plan
generation for write modes) are tracked in Ticket #6 (`Xxx91n/READJH#6`) and
build directly on the resolution block and audit spine above.
