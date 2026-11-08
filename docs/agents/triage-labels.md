# Triage labels

Labels actually configured on `Xxx91n/READJH` (via `gh label list`), with
how this repo uses them.

## Workflow labels

- **`ready-for-agent`** — spec stage complete, an agent may implement
  without further clarification. The spec-0001 ticket wave (#1–#7) was
  created with this label. **Implementation removes it when work starts** —
  an issue that keeps it looks grabbable and risks duplicate assignment.
- **`question`** — blocked on a human decision; do not implement.

## GitHub defaults in use

- **`bug`** — the skill or static check produces wrong results (e.g. a
  check fires on valid content, the skill lookup finds the wrong file).
- **`documentation`** — changes to README, UPSTREAM.md, references, or
  docs/agents prose.
- **`enhancement`** — new checks, new modes, scope additions to the
  pipeline.
- **`duplicate`, `invalid`, `wontfix`** — standard close-out semantics.
- **`good first issue`, `help wanted`** — open calls for contributors.

## Not used

`accessibility` exists on the repo but has no current meaning for
README-tooling work; do not apply it as a generic label.

## Triage practice

- Every open issue carries at most one status signal:
  `ready-for-agent` (grabbable) or `question` (blocked) or neither
  (in progress / under human review).
- Which ticket blocks which is recorded in `docs/agents/issue-tracker.md`,
  not encoded as labels.
