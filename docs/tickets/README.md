# Tickets

Implementation tickets live as GitHub issues at `Xxx91n/READJH` —
not as files in this directory. This file exists only to say that.

Current tickets (all `ready-for-agent`):

- [#1](https://github.com/Xxx91n/READJH/issues/1) — Skeleton docs: README, LICENSE, NOTICE, UPSTREAM.md, AGENTS.md, docs/agents, .gitattributes
- [#2](https://github.com/Xxx91n/READJH/issues/2) — check-readme.py static probe + pytest suite (Seam A)
- [#3](https://github.com/Xxx91n/READJH/issues/3) — references/: distilled readme-rules, de-ai-language, checklist
- [#4](https://github.com/Xxx91n/READJH/issues/4) — SKILL.md audit-mode spine (ROUTE→TRUTH→RESTRUCTURE→VERIFY)
- [#5](https://github.com/Xxx91n/READJH/issues/5) — Audit smoke run on 6F + scan-project.sh runtime check
- [#6](https://github.com/Xxx91n/READJH/issues/6) — improve/rewrite modes + LANGUAGE phase + ledger + .bak + dry-run
- [#7](https://github.com/Xxx91n/READJH/issues/7) — Acceptance run: six-repo audits + baseline + EgressAPIKEY dry-run

Dependency edges:

- #1, #2, #3 — no blockers (parallel wave)
- #4 ← #1, #2, #3
- #5 ← #4
- #6 ← #4
- #7 ← #5, #6
