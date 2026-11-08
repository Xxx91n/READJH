# Tickets

Implementation tickets live as GitHub issues at `Xxx91n/READJH` —
not as files in this directory. This file exists only to say that.

Spec 0001 wave (closed):

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

Spec 0002 wave (open, all `ready-for-agent`):

- [#17](https://github.com/Xxx91n/READJH/issues/17) — T1 Add plain-language rules to the language pass
- [#18](https://github.com/Xxx91n/READJH/issues/18) — T3 Rewrite GLOSSARY as the plain-language standard
- [#19](https://github.com/Xxx91n/READJH/issues/19) — T2 Test contamination defense
- [#20](https://github.com/Xxx91n/READJH/issues/20) — T5 Add native-first translation handoff
- [#21](https://github.com/Xxx91n/READJH/issues/21) — T4a Clean README, Chinese README, and AGENTS
- [#22](https://github.com/Xxx91n/READJH/issues/22) — T4d Clean docs/agents, docs/adr, and UPSTREAM
- [#23](https://github.com/Xxx91n/READJH/issues/23) — T4b Clean SKILL.md
- [#24](https://github.com/Xxx91n/READJH/issues/24) — T4c Clean references
- [#25](https://github.com/Xxx91n/READJH/issues/25) — T6 Add plain-language review checklist and fixtures

Dependency edges:

- #17, #18 — no blockers
- #19, #20 ← #17
- #21, #22 ← #18
- #23, #24 ← #17, #18, #20
- #25 ← #17, #19, #20, #21, #22, #23, #24

Parallel order:

- Start: #17 and #18.
- After #17: #19 and #20.
- After #18: #21 and #22.
- After #17, #18, #20: #23 and #24.
- Last: #25.
