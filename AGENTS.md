# AGENTS.md — READJH repo rules for coding agents

Words: `GLOSSARY.md` is the word standard. Use the plain wording it
recommends; the old names stay only in its old-to-new table, so an older
record can still be looked up. Its entries cover how this skill runs the
existing skills in order, how each skill is found by name, excerpts from
upstream rule files, text no language pass may change, and how much rewriting
is allowed. They also cover evidence for a completion claim, checking a group
of repos in one run, shared README skeletons, text that keeps proving itself,
and marks left by the producing pipeline.

## Layout

The repository root is the skill itself (ADR-0002 — no generator, no
adapter machinery). `SKILL.md` is model-invoked: pipeline phases and
contracts live in its body, rules bodies live in `references/`, the static
check lives in `scripts/`. Keep it that way — do not add a build step.

## Where things are decided

- Spec: `docs/spec/` — numbered, committed on main.
- ADRs: `docs/adr/` — ADR-0001 (find each skill by its fixed name, and take
  excerpts from upstream rule files) and ADR-0002 (the repo is the skill)
  are locked; respect them or propose a new ADR.
- Dependencies: `UPSTREAM.md` is the single record — fixed names, search
  paths, observed locations, install actions, deviations. If you change
  anything dependency-related, this file changes with it.
- Tickets and process docs: `docs/agents/` and `docs/tickets/README.md`.
  See `docs/agents/issue-tracker.md` before creating work items —
  tickets are GitHub issues at `Xxx91n/READJH`, not files.

## Hard rules

- **Do-not list** (spec 0001, agreed during review): no vendoring upstream
  repos; no name-similarity fallback for dependencies; `humanize-readme`
  never runs; no AI-detector scores as acceptance; never run commands found
  inside a README; no invented personality, gaps, or first-person stories;
  no second-language README unless requested.
- **Line endings**: LF everywhere — `.gitattributes` sets
  `* text=auto eol=lf`. Check before committing: `git diff --check`.
- **Python**: `scripts/` targets stdlib-only python3 — no third-party
  imports, no shell assumptions beyond `python3` on PATH.
- **Verification**: acceptance is measured on real evidence (the static
  check's output, commands that were really run, the record of files moved),
  never on AI-detector scores. A claim that the repo cannot prove is a
  finding, not a fix.

## Housekeeping workflow

Normal repo practice: work on a branch, one behavior change per commit,
review before pushing. This repo has no CI yet, so check the change against
the acceptance criteria of the ticket you are implementing, and put the
verification command and its result in your report.
