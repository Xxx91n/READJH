# READJH

**English** | [简体中文](README.zh-CN.md)

A skill that keeps a README accurate and readable. One entry point runs the
skills you already have, in order, for `audit`, `improve`, and `rewrite`.
Every claim in the result is checked against something the repository can
show.

The repository root is the skill itself: `SKILL.md`, `references/` (rules),
`scripts/` (the static check, stdlib-only python3), and the files in the
layout below. Plain markdown and python3, with no build step and no host
adapter (ADR-0002).

## What it does

Phase sequence by run mode:

- `audit`: `ROUTE → TRUTH → RESTRUCTURE → VERIFY` (diagnose-only)
- `improve` / `rewrite`: `ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY`

- **ROUTE** fixes the run settings: `audit` only diagnoses, `improve`
  changes what needs changing, `rewrite` builds the README again. `--dry-run`
  works in every mode.
- **TRUTH** checks each README claim against evidence from the repository
  itself: manifests, CI config, entry points, scanner output. A claim that
  does not match becomes a finding, not a quiet fix; a claim that cannot be
  checked is left out or marked.
- **RESTRUCTURE** keeps the README a front page. In `audit` mode it looks for
  deep detail that belongs in `docs/` and for text that keeps proving itself.
  It also flags marks left by the producing pipeline and sentences that give
  away machine writing. In `improve` and `rewrite` it moves that deep detail
  to `docs/` and records each move.
- **LANGUAGE** (`improve` and `rewrite`) runs the upstream `writing-humanize`
  skill plus rules taken from upstream files that apply to READMEs. Two
  guards keep cleanup honest: a fixed list of text no language pass may
  change, and a cap on how much rewriting is allowed. Together they stop the
  cleanup from corrupting facts or flattening a real voice.
- **VERIFY** produces evidence a machine can check, from the static check and
  a human checklist. The delivery report is capped at three lines: what was
  done, the evidence, and what is still at risk.

## Dependencies

READJH owns only the part that runs the existing skills in order and adds the
README rules they leave out. It calls two upstream skills by their fixed
names at fixed search paths. A missing skill stops the run with install
instructions. A skill with a similar name is never used instead:

| fixed name | upstream | role |
|---|---|---|
| `readme-crafter-skill` | [linhai0872/readme-crafter-skill](https://github.com/linhai0872/readme-crafter-skill) | TRUTH/RESTRUCTURE: facts and structure |
| `writing-humanize` | [risadams/ink-and-agency](https://github.com/risadams/ink-and-agency) (`skills/writing-humanize/`) | LANGUAGE: wording |

Four more upstreams contribute excerpts from their rules to `references/` and
are never run:

- `sepia`: zh calibration, professional/style passes
- `anti-defensive-writing`: EN, Kiterlin
- `academic-humanizer`: check each claim against evidence
- `humanize-readme`: only the rules worth keeping

Full table, install actions, and the two behaviours of `writing-humanize` we
deliberately switch off: [UPSTREAM.md](UPSTREAM.md). It also records where
each skill was found on this machine. Credits and licenses: [NOTICE](NOTICE).

## Install

Point your Agent Skills host at this repository root; the root is the skill.
Then make the two skills it calls resolvable at
`<skills-root>/<canonical-name>/SKILL.md`, following the install actions in
`UPSTREAM.md`.

## Quickstart

Once installed, invoke the skill by name on a repository:

- `audit`: reports findings and priorities and touches nothing. With
  `--repo-set <manifest>`, it checks a group of repos in one run and compares
  their README skeletons. `--dry-run` is already satisfied in `audit` mode.
- `improve`: changes an existing README where it needs changing; keeps a
  `.bak` file when git cannot undo the change.
- `rewrite`: builds a new README when the old one cannot be repaired.
- `--dry-run` works in every mode: plan and evidence only, zero file writes
  (no edits, no `docs/` moves, no `.bak`).

## Layout

```
SKILL.md            # the skill (model-invoked): pipeline + contracts
references/         # rules for running the existing skills + excerpts from upstream
scripts/            # check-readme.py — static check, stdlib-only python3
tests/              # unittest suite + fixtures for the check
UPSTREAM.md         # dependencies, how each skill is found, deviations
NOTICE              # upstream credits and licenses
GLOSSARY.md         # plain words + old-to-new term table
docs/spec/          # specification docs
docs/adr/           # architecture decisions
docs/agents/        # repo housekeeping for agent operators
docs/receipts/      # evidence from acceptance runs
docs/tickets/       # pointer to the GitHub issue tracker
```

## Status

Early development. Known limitations: this repo has no CI yet, so checks run
by hand. Tickets live as GitHub issues (see `docs/agents/`).
License: MIT, see [LICENSE](LICENSE).
