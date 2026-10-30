# Issue tracker

Tickets are **GitHub issues at `Xxx91n/READJH`**. There is no file-based
ticket queue; `docs/tickets/README.md` exists only to say this.

Current tickets (spec 0001 wave, all created `ready-for-agent`):

| # | title | blocked by |
|---|---|---|
| #1 | Skeleton docs: README, LICENSE, NOTICE, UPSTREAM.md, AGENTS.md, docs/agents, .gitattributes | — |
| #2 | check-readme.py static probe + pytest suite (Seam A) | — |
| #3 | references/: distilled readme-rules, de-ai-language, checklist | — |
| #4 | SKILL.md audit-mode spine (ROUTE→TRUTH→RESTRUCTURE→VERIFY) | #1, #2, #3 |
| #5 | Audit smoke run on 6F + scan-project.sh runtime check | #4 |
| #6 | improve/rewrite modes + LANGUAGE phase + ledger + .bak + dry-run | #4 |
| #7 | Acceptance run: six-repo audits + baseline + EgressAPIKEY dry-run | #5, #6 |

Rules for agents picking up work:

- Read the issue body **and all comments** before starting; resolution
  notes land as comments (e.g. the non-canonical-path diagnosis on #1).
- A closed issue is not proof a dependency is met — check that the
  upstream ticket's files/commits actually reached your baseline.
- Link work to the issue in the commit message or PR body.
- Do not file tracking issues as files under `docs/`; use `gh issue
  create --repo Xxx91n/READJH` for new work items.
