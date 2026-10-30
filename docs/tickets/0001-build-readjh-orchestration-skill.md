# 0001 — Build the READJH orchestration skill

Status: ready-for-agent
Spec: [0001-readjh-orchestration-skill.md](../spec/0001-readjh-orchestration-skill.md)
Blocked by: nothing
Blocks: implementation tickets cut by /to-tickets

## Summary

Build the READJH orchestration skill in this repo per spec 0001: SKILL.md,
three references files, check-readme.py probe, UPSTREAM.md/NOTICE/LICENSE/
README.md, AGENTS.md + docs/agents housekeeping, .gitattributes.

## Acceptance (from spec)

- Probe script passes its unit tests (Seam A, TDD).
- SKILL.md contract checks pass (Seam B).
- `audit` mode produces a conforming report on at least one target repo
  without writing files (Seam C smoke).
- All "do-not" rules verifiable by reading SKILL.md.

## Open runtime items (probe-first)

- `scan-project.sh` real behavior under Git Bash on this host.
- `writing-humanize` obedience to distilled supplement rules.
