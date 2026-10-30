---
name: readjh
description: >
  Orchestrates repository README governance across audit, improve, and rewrite
  runs with truth checks, front-page restructuring, de-AI prose cleanup, and
  static probe verification. Use when asked to audit, critique, improve,
  rewrite, de-AI, humanize, or verify a README, or to check cross-repo README
  skeleton isomorphism with --repo-set.
license: MIT
---

# READJH — README Governance Orchestration Skill

READJH is a thin **orchestration layer** for one-shot README governance. The
repository root is the skill itself (`SKILL.md`, `references/`, `scripts/`,
`UPSTREAM.md`, `NOTICE` — ADR-0002, no build step or adapter generator). It
sequences upstream executors through a **pointer contract**, applies
**orchestration layer** rules and **distilled rules** from `references/`, and
closes every run with machine **receipts** from `scripts/check-readme.py` plus
`references/checklist.md`.

The phase sequence depends on the run mode:

```text
audit:                      ROUTE → TRUTH → RESTRUCTURE → VERIFY
improve / rewrite (future): ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY
```

Deletion and migration always precede wording changes.

### Delivery Engineer Discipline (`jiahao` Core Rules)

Every run obeys five execution rules — no exceptions:

1. **Action First:** Run path checks and probe scripts before outputting prose.
   Never write preambles, plans, or essays before tool calls.
2. **Probing Over Guessing:** Ground truth comes only from running the probes
   (`scan-project.py`, `check-readme.py`) and reading real repository files
   (`file:line`). Reading a README and thinking "it looks fine" carries zero
   weight.
3. **Zero Rationalization on Red:** A missing required upstream file or a
   non-zero scanner/probe execution error halts the run as `BLOCKED`
   immediately. Never skip a required tool or invent excuses.
4. **No Receipt, No Claim:** Every pass assertion or finding requires a concrete
   **receipt** (`scan-project.py` output, `check-readme.py` check name and exit
   code, or `<file>:<line>`). AI-detector scores carry zero weight and are
   rejected.
5. **Plain Language and Three-Line Lock:** Write direct, plain sentences with no
   invented compound buzzwords. Lock the final reply to at most three lines
   (`[Conclusion]`, `[Receipts]`, `[Residual risk]`).

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
  name** exactly, and the loaded `SKILL.md` YAML frontmatter `name:` field must
  equal the canonical name too.
- **Required files check:** Every required file and directory listed in the
  table below for the active executor must exist inside `<skills-root>/<canonical-name>/`
  (for `readme-crafter-skill`: `SKILL.md`, `references/`, and
  `scripts/scan-project.py`; only `scripts/scan-project.sh` is optional).
- **Stop on miss (zero silent degradation):** If `<skills-root>/<canonical-name>/SKILL.md`
  is missing, its frontmatter `name:` mismatches, or any required file/directory
  inside it is missing, **stop the run immediately** as `BLOCKED` with the
  install instructions below. Never fall back to manual guesswork and **never
  write, create, or modify any file**.
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
commit hashes, install actions, and deviations:

| Canonical name | Upstream repository | Required files (`UPSTREAM.md`) | Role in pipeline |
|---|---|---|---|
| `readme-crafter-skill` | `linhai0872/readme-crafter-skill` (`https://github.com/linhai0872/readme-crafter-skill`) | `SKILL.md`, `references/`, `scripts/scan-project.py` (optional: `scripts/scan-project.sh`) | `TRUTH` & `RESTRUCTURE` (required by `audit`, `improve`, and `rewrite`) |
| `writing-humanize` | `risadams/ink-and-agency` (`skills/writing-humanize/`, `https://github.com/risadams/ink-and-agency`) | `SKILL.md`, `references/patterns.md`, `agents/openai.yaml` | `LANGUAGE` (required by `improve` and `rewrite`) |

### Stop-on-Miss Install Instructions

When a required executor or any of its required files cannot be resolved at the
five search roots, abort before touching any file and emit the three-line
`BLOCKED` report (§4) with the matching install action (`UPSTREAM.md`, which
also documents linking/renaming an existing non-canonical checkout):

- **`readme-crafter-skill` (Windows `cmd` / POSIX `sh`):**
  ```cmd
  mkdir "%USERPROFILE%\.agents\repos" "%USERPROFILE%\.agents\skills" 2>nul
  git clone https://github.com/linhai0872/readme-crafter-skill "%USERPROFILE%\.agents\repos\readme-crafter-skill"
  mklink /J "%USERPROFILE%\.agents\skills\readme-crafter-skill" "%USERPROFILE%\.agents\repos\readme-crafter-skill"
  ```
  ```sh
  mkdir -p "$HOME/.agents/repos" "$HOME/.agents/skills"
  git clone https://github.com/linhai0872/readme-crafter-skill "$HOME/.agents/repos/readme-crafter-skill"
  ln -s "$HOME/.agents/repos/readme-crafter-skill" "$HOME/.agents/skills/readme-crafter-skill"
  ```
- **`writing-humanize` (Windows `cmd` / POSIX `sh`, or copy `skills/writing-humanize/` to `<skills-root>/writing-humanize/`):**
  ```cmd
  mkdir "%USERPROFILE%\.agents\repos" "%USERPROFILE%\.agents\skills" 2>nul
  git clone https://github.com/risadams/ink-and-agency "%USERPROFILE%\.agents\repos\ink-and-agency"
  mklink /J "%USERPROFILE%\.agents\skills\writing-humanize" "%USERPROFILE%\.agents\repos\ink-and-agency\skills\writing-humanize"
  ```
  ```sh
  mkdir -p "$HOME/.agents/repos" "$HOME/.agents/skills"
  git clone https://github.com/risadams/ink-and-agency "$HOME/.agents/repos/ink-and-agency"
  ln -s "$HOME/.agents/repos/ink-and-agency/skills/writing-humanize" "$HOME/.agents/skills/writing-humanize"
  ```
- **Verification after install:** confirm `<skills-root>/<canonical-name>/SKILL.md`
  exists, its frontmatter `name:` equals `<canonical-name>`, and all required
  files in the table above exist.

---

## 2. Inline Orchestration Rules (`GLOSSARY.md`)

Full rule bodies and attributions live in `references/readme-rules.md` and
`references/de-ai-language.md`.

### Freeze Zone (`references/readme-rules.md` §1)

A **freeze zone** is any README region that no language pass (`writing-humanize`
or **distilled rules**) may alter, reword, reformat, or delete:

1. **Commands and code:** fenced code blocks, inline commands, CLI flags, and
   environment variable names.
2. **Links and paths:** URLs, local file paths, markdown link targets, query
   strings, and anchors.
3. **Exact identifiers and metrics:** version strings, commit hashes, benchmark
   numbers, and error or exit codes.
4. **Badges:** markdown and HTML badge rows and their target URLs.
5. **Legal and safety boundaries:** `LICENSE` notices, `NOTICE` attributions,
   security boundary statements, and compliance text.
6. **Direct quotations:** quoted command transcripts and speaker quotes inside
   `"..."` or `「...」`.

**Phase boundary:** If a **freeze zone** span contradicts the repository (such
as a flag missing from the CLI parser or a dead local link), `TRUTH` reports it
as a finding with its `file:line` **receipt**. `LANGUAGE` never mutates a
**freeze zone** span.

### Intensity Tiers and No-Invented-Personality Rule (`references/readme-rules.md` §5)

| Intensity tier | Selection condition | Scope |
|---|---|---|
| `lite` | The repository shows a verified human author voice (in commits, issues, or existing docs) or the user supplies an author writing sample. | Preserve the author's sentence rhythm, punctuation, contractions, and register. Flag or strip only clustered AI vocabulary, chatbot turn wrappers, and repeated **self-attestation**. |
| `standard` | Default when no verified author voice or writing sample is present. | Apply `writing-humanize` plus `references/de-ai-language.md`: replace abstract-noun chains with concrete nouns, split overloaded sentences, recast defensive caveats into `fact + link`, and vary uniform sentence rhythm by moving words without filler. |

**Hard guardrails (both intensity tiers):**

- **No invented personality, gaps, or stories:** Never insert fabricated
  first-person stories (`"I built this because..."`), casual banter, or
  unverified limitations / `"honest gaps"` lacking a repository **receipt**.
- **Two `writing-humanize` suppressions (`UPSTREAM.md`):** Whenever
  `writing-humanize` runs, suppress (1) **self-evolve journaling** (never write
  to `~/.ink-and-agency/` or outside the target repository) and (2)
  **personality injection** (ignore `writing-humanize` Step 5 / `PERSONALITY AND
  SOUL`).
- **Static safety:** Never execute commands documented inside a target README.
- **Bilingual discipline:** Detect existing bilingual README pairs (such as
  `README.md` + `README-ZH.md` or `README.zh-CN.md`) and process them in
  lockstep with aligned section structure; apply Chinese (`zh`) calibration
  rules (`references/de-ai-language.md` §3) to Chinese prose; never create a
  second-language README unless requested.

---

## 3. Audit-Mode Spine (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`)

In `audit` mode, READJH diagnoses and ranks README defects without writing or
modifying any files.

### Phase 1: `ROUTE`

1. **Lock run parameters:**
   - Run mode: `audit` (zero writes; `--dry-run` is satisfied by default).
   - Target path: `<readme>` (defaults to `<repo-root>/README.md`) and
     `<repo-root>` (defaults to the parent directory of `<readme>`).
   - Optional **repo-set mode**: enabled only when `--repo-set <manifest>` is
     passed; off by default.
2. **Select intensity tier:**
   - Check repository commits, issues, or writing samples supplied by the user.
     Select `lite` when a distinct author voice is verified; otherwise select
     `standard`.
3. **Detect language and companion files:**
   - Record the primary language of `<readme>` and any existing localized
     companion README so `TRUTH` and `RESTRUCTURE` check them in lockstep.
4. **Enforce the pointer contract (§1):**
   - Resolve `readme-crafter-skill` using the search order, canonical match
     rules, and required-files check in §1. On any miss, apply the §1
     stop-on-miss gate immediately (zero file writes; emit the §4 `BLOCKED`
     report naming the missing path in `[Receipts]` and the §1 install commands
     in `[Residual risk]`).

**Completion criterion:** Run mode (`audit`), `<readme>`, `<repo-root>`,
**intensity tier** (`lite` | `standard`), **repo-set mode** state, and verified
paths to `readme-crafter-skill/{SKILL.md,references/,scripts/scan-project.py}`
are locked.

### Phase 2: `TRUTH`

1. **Run upstream project scanner and inspect repository files:**
   - Read `<skills-root>/readme-crafter-skill/SKILL.md` and
     `<skills-root>/readme-crafter-skill/references/repo-integrity.md`.
   - Execute the required scanner:
     ```bash
     python3 -X utf8 <skills-root>/readme-crafter-skill/scripts/scan-project.py <repo-root>
     ```
     (Optional: also run `bash <skills-root>/readme-crafter-skill/scripts/scan-project.sh <repo-root>`
     when `bash` is available.) If `scan-project.py` exits non-zero, stop
     immediately as `BLOCKED` and report the exact error output in `[Receipts]`.
   - Inspect repository manifests (`package.json`, `pyproject.toml`,
     `Cargo.toml`, `go.mod`), lockfiles, CI workflows (`.github/workflows/`),
     entry points, root exports, `.env.example`, and `LICENSE`.
   - **Never execute commands documented inside `<readme>`.** Record any README
     command not confirmed against manifests or scripts as `"needs manual
     verification"` in `[Residual risk]`.
2. **Classify project type and distribution posture:**
   - Record the repository's **Project Type** (CLI Tool, Library/SDK,
     Application, Research Project, etc.) and **Distribution Posture**
     (Published Package, Source-first Repository, Hybrid, or Product/Monorepo
     Hub) per `readme-crafter-skill`.
3. **Check every README claim against repository receipts:**
   - Match each install command, CLI flag, environment variable, code import,
     version requirement, badge, metric, and **freeze zone** span against
     repository `file:line` anchors.
   - Rank every truth defect by severity:
     - **`HIGH` (Contradicted claim):** `<readme>` states a fact, command, flag,
       export, path, or registry publication contradicted by the repository.
       Record `<readme>:<line>` and the contradicting `<repo-file>:<line>`
       **receipt**. Never silently rewrite contradicted facts.
     - **`MEDIUM` (Unbacked claim):** `<readme>` states an empirical,
       performance, or capability claim (`references/de-ai-language.md` §5)
       with no repository **receipt**. Flag for deletion or `TODO`.
     - **`LOW` (Stale minor detail):** Minor metadata or wording drift where the
       underlying capability exists.

**Completion criterion:** `scan-project.py` exited `0`, and every factual claim
and **freeze zone** span in `<readme>` is matched to a `<repo-file>:<line>`
**receipt** or logged as a `HIGH` / `MEDIUM` / `LOW` finding with zero README
commands executed.

### Phase 3: `RESTRUCTURE` (Diagnose-Only in `audit` Mode)

1. **Load orchestration and distilled rule files:**
   - Read `references/readme-rules.md` (§§1–5) and
     `references/de-ai-language.md` (§§1–6, including §3 when `<readme>`
     contains Chinese text).
2. **Diagnose front-page boundary (`references/readme-rules.md` §4.1):**
   - Check the 30-second first screen (`readme-crafter-skill` Checks #1, #3,
     #4: project name, artifact type, plain-language problem solved, and
     shortest verified install/run path).
   - Flag deep reference sections packed into `<readme>` that belong in `docs/`
     (full CLI/API tables, threat models, security matrices, versioning
     policies, release runbooks) as `source heading (lines X–Y) → recommended
     docs/<file>.md` without touching files.
3. **Diagnose self-attestation repeats (`references/readme-rules.md` §2 & `references/de-ai-language.md` §4):**
   - Flag every boundary, preview caveat, or disclaimer stated more than once,
     standalone sections that only proclaim honesty, negative disclaimers that
     should be `fact + link`, and internal issue/decision IDs on the front page.
4. **Diagnose generation traces (`references/readme-rules.md` §3):**
   - Flag leftover skill or placeholder HTML comments (`<!-- PLACEHOLDER ... -->`,
     `<!-- SLOT ... -->`, `<!-- Drop-in ... -->`, `<!-- self-evolve:start -->`),
     pipeline tags (`[ROUTE]`, `[TRUTH]`, `[LANGUAGE]`), chatbot turn wrappers,
     and cutoff disclaimers.
   - Check surviving HTML comments against the ownership whitelist
     (`references/readme-rules.md` §3): keep only generator boundaries or sync
     anchors actively read, written, or owned by an existing repository script
     or companion file.
5. **Diagnose skeleton isomorphism and language tells (`references/readme-rules.md` §4.2, §5 & `references/de-ai-language.md`):**
   - Check whether the heading skeleton fits the repository's Project Type and
     Distribution Posture rather than a generic template.
   - Outside the **freeze zone**, log prose tells under the active **intensity
     tier** (`lite` or `standard`): clustered ban-list words, abstract-noun
     chains, trailing `-ing` clauses, uniform sentence runs (3+ near-equal
     sentences), and Chinese (`zh`) calibration tells.

**Completion criterion:** All structural, **self-attestation**, **generation
trace**, **skeleton isomorphism**, and language findings are logged with
severity (`HIGH` / `MEDIUM` / `LOW`) and `<readme>:<line>` anchors; zero files
are modified.

### Phase 4: `VERIFY`

1. **Run the static probe (`scripts/check-readme.py`):**
   - Execute:
     ```bash
     python3 <readjh-root>/scripts/check-readme.py <readme> --repo-root <repo-root> [--repo-set <manifest>]
     ```
   - Capture the exit code (`0` = pass, `1` = blocking findings in `<readme>`,
     `2` = CLI/usage error → `BLOCKED`) and stdout **receipt** covering **all
     applicable checks** (checks 1–6 on single-repository runs; check 7 enabled
     only when `--repo-set <manifest>` is supplied, otherwise `N/A`):
     1. `dead-links` — dead local markdown and HTML links (including badge link targets)
     2. `missing-images` — missing local markdown images, `<img>`, and `<source srcset>` paths
     3. `code-fences` — unclosed or mismatched backtick/tilde code fences
     4. `badge-domains` — placeholder or invalid badge URL hosts
     5. `boundary-duplicates` — repeated boundary/disclaimer phrases (**self-attestation** count)
     6. `honest-gaps` — presence of repository-backed limitation/caveat/non-goal signals
     7. `repo-set` — cross-repo **skeleton isomorphism** diff when `--repo-set <manifest>` is supplied (`N/A` on single-repository runs)
2. **Walk the binary verification checklist (`references/checklist.md`):**
   - Evaluate `references/checklist.md` §§1–8 against the probe **receipt** and
     the `TRUTH` / `RESTRUCTURE` findings.
   - Confirm that zero files were written or modified in the target repository
     (and no `.bak` or out-of-repo files were created).
3. **Emit the three-line delivery report (§4).**

**Completion criterion:** `scripts/check-readme.py` has run, its stdout
**receipt** and exit code are recorded, `references/checklist.md` items are
evaluated, zero target writes are confirmed, and the three-line report is
emitted.

---

## 4. Three-Line Delivery Report Format

Every READJH run — whether a completed `audit` (`PASS` / `FAIL`) or a run
halted by a missing dependency or broken probe (`BLOCKED`) — closes with a
reply locked to **at most three lines** (`docs/spec/0001-readjh-orchestration-skill.md`
US-27, `references/checklist.md` §8):

```text
[Conclusion]: <PASS | FAIL | BLOCKED> — <mode> on <target> (intensity tier: <lite|standard>); <outcome summary and HIGH/MEDIUM/LOW finding counts>.
[Receipts]: <scan-project.py + check-readme.py commands, exit codes, and applicable check results; severity-ranked findings (HIGH / MEDIUM / LOW) with <readme>:line and <repo-file>:line anchors — or checked canonical paths 1..5 and missing required path when BLOCKED>.
[Residual risk]: <README commands flagged "needs manual verification" (never executed), unverified external URLs, or required UPSTREAM.md install commands when BLOCKED>.
```

### Report Rules

- **Strict three-line cap:** Output only `[Conclusion]`, `[Receipts]`, and
  `[Residual risk]` (in future `improve` / `rewrite` runs that move sections to
  `docs/`, only the migration ledger table may follow).
- **Distinguish `FAIL` from `BLOCKED`:** When `ROUTE`, `scan-project.py`, and
  `check-readme.py` execute cleanly (`exit 0` or `exit 1`) and uncover defects
  in `<readme>`, the audit itself succeeded and reports `FAIL` with findings in
  `[Receipts]`. Report `BLOCKED` only when a **pointer contract** dependency or
  required file is missing, or when a scanner/probe fails to execute (`exit 2`
  or runtime crash).
- **Untested README commands:** Because READJH never executes commands inside a
  target README, `[Residual risk]` must list any README commands not verified
  against repository scripts as `"needs manual verification"`.

---

## 5. Future Phases Stub (`improve` and `rewrite` Modes — Ticket #6)

`improve` mode (surgical README upgrade), `rewrite` mode (full README rebuild),
and the `LANGUAGE` phase (`writing-humanize` invocation via the **pointer
contract**, **distilled rules** handoff from `references/de-ai-language.md` and
`references/readme-rules.md`, **freeze zone** enforcement during edits, `docs/`
migration ledger, `.bak` rollback file creation when git cannot roll back, and
`--dry-run` plan output for write modes) are tracked in Ticket #6
(`Xxx91n/READJH#6`).
