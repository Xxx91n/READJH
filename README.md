# READJH

An orchestration skill for README governance. One entry point sequences
upstream skills across `audit`, `improve`, and `rewrite` — every claim in the
result is checked against what the repository can actually verify with a
receipt.

The repository root is the skill itself: `SKILL.md` plus `references/`
(rules), `scripts/` (a stdlib-only python3 probe), and this skeleton
(`README.md`, `LICENSE`, `NOTICE`, `UPSTREAM.md`, `AGENTS.md`,
`docs/agents/`). Plain markdown and python3 — no build step, no host
adapter (ADR-0002).

## What it does

Phase sequence by run mode:

- `audit`: `ROUTE → TRUTH → RESTRUCTURE → VERIFY` (diagnose-only)
- `improve` / `rewrite`: `ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY`

- **ROUTE** locks the run parameters (`audit` diagnoses only; `improve`
  surgically upgrades, `rewrite` rebuilds — both pass through `LANGUAGE`,
  and every mode accepts `--dry-run`).
- **TRUTH** checks each README claim against repo-native receipts —
  manifest, CI config, entry points, and scanner output. Contradicted
  claims become findings, not silent fixes; unverifiable claims are
  omitted or marked.
- **RESTRUCTURE** keeps the README a front page: in `audit` mode it diagnoses
  deep material that belongs in `docs/`, repeated self-attestation, generation
  traces, and prose tells; in `improve` and `rewrite` it moves deep material to
  `docs/` under a migration ledger.
- **LANGUAGE** (`improve` and `rewrite`) runs upstream `writing-humanize` plus
  distilled README-scoped rules, inside freeze zones and intensity tiers that
  stop cleanup from corrupting facts or flattening a real voice.
- **VERIFY** emits machine-checkable receipts from the static probe and
  a human checklist, and caps the delivery report at three lines:
  conclusion, receipts, residual risk.

## Dependencies

READJH owns only the orchestration layer. It invokes two upstream skills
by **pointer contract** — canonical name at fixed search paths, missing
means stop with install instructions, never name-similarity fallback:

| canonical name | upstream | role |
|---|---|---|
| `readme-crafter-skill` | [linhai0872/readme-crafter-skill](https://github.com/linhai0872/readme-crafter-skill) | TRUTH/RESTRUCTURE: facts and structure |
| `writing-humanize` | [risadams/ink-and-agency](https://github.com/risadams/ink-and-agency) (`skills/writing-humanize/`) | LANGUAGE: prose pass |

Four more upstreams contribute **distilled rules** to `references/` and
are never executed: `sepia` (zh calibration, professional/style passes),
`anti-defensive-writing` (EN, Kiterlin), `academic-humanizer`
(claim↔evidence), `humanize-readme` (salvageable rules only).

Full table, observed machine locations, install actions, and the two
deliberate suppressions of `writing-humanize`:
[UPSTREAM.md](UPSTREAM.md). Credits and licenses: [NOTICE](NOTICE).

## Install

Point your Agent Skills host at this repository root — the root is the
skill. Then make the two executors resolvable at
`<skills-root>/<canonical-name>/SKILL.md` per the install actions in
`UPSTREAM.md`; on the authoring machine `readme-crafter-skill` sits at a
non-canonical path and `writing-humanize` is not yet installed.

## Quickstart

Once installed, invoke the skill by name on a repository:

- `audit` — findings and priorities, touches nothing; supports
  optional `--repo-set <manifest>` for cross-repository skeleton isomorphism
  (`--dry-run` is satisfied by default in `audit` mode).
- `improve` — surgical upgrade of an existing README; `.bak` kept when git
  cannot roll back.
- `rewrite` — full rebuild for a README beyond repair.
- `--dry-run` is supported on every mode: plan and receipts only, zero file
  writes (no edits, no `docs/` migration, no `.bak`).

## Layout

```
SKILL.md            # the skill (model-invoked); pipeline + contracts
references/         # orchestration-layer rules + distilled supplements
scripts/            # check-readme.py — static probe, stdlib-only python3
UPSTREAM.md         # dependencies, pointer contract, deviations
NOTICE              # upstream credits and licenses
docs/spec/          # specification docs
docs/adr/           # architecture decisions
docs/agents/        # repo housekeeping for agent operators
docs/tickets/       # pointer to the GitHub issue tracker
```

## Status

Early development; tickets live as GitHub issues (see `docs/agents/`).
License: MIT — see [LICENSE](LICENSE).
