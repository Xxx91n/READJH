# Issue tracker

Tickets are **GitHub issues at `Xxx91n/READJH`**. There is no file-based
ticket queue; `docs/tickets/README.md` exists only to say this.

Spec 0001 wave (closed):

| # | title | blocked by |
|---|---|---|
| #1 | Skeleton docs: README, LICENSE, NOTICE, UPSTREAM.md, AGENTS.md, docs/agents, .gitattributes | — |
| #2 | check-readme.py static probe + pytest suite (Seam A) | — |
| #3 | references/: distilled readme-rules, de-ai-language, checklist | — |
| #4 | SKILL.md audit-mode spine (ROUTE→TRUTH→RESTRUCTURE→VERIFY) | #1, #2, #3 |
| #5 | Audit smoke run on 6F + scan-project.sh runtime check | #4 |
| #6 | improve/rewrite modes + LANGUAGE phase + ledger + .bak + dry-run | #4 |
| #7 | Acceptance run: six-repo audits + baseline + EgressAPIKEY dry-run | #5, #6 |

Spec 0002 wave (open, all created `ready-for-agent`):

| # | title | blocked by |
|---|---|---|
| #17 | T1 Add plain-language rules to the language pass | — |
| #18 | T3 Rewrite GLOSSARY as the plain-language standard | — |
| #19 | T2 Test contamination defense | #17 |
| #20 | T5 Add native-first translation handoff | #17 |
| #21 | T4a Clean README, Chinese README, and AGENTS | #18 |
| #22 | T4d Clean docs/agents, docs/adr, and UPSTREAM | #18 |
| #23 | T4b Clean SKILL.md | #17, #18, #20 |
| #24 | T4c Clean references | #17, #18, #20 |
| #25 | T6 Add plain-language review checklist and fixtures | #17, #19, #20, #21, #22, #23, #24 |

Parallel order:

- Start: #17 and #18.
- After #17: #19 and #20.
- After #18: #21 and #22.
- After #17, #18, #20: #23 and #24.
- Last: #25.

Rules for agents picking up work:

- Read the issue body **and all comments** before starting; resolution
  notes land as comments (e.g. the non-canonical-path diagnosis on #1).
- A closed issue is not proof a dependency is met — check that the
  upstream ticket's files/commits actually reached your baseline.
- Link work to the issue in the commit message or PR body.
- Do not file tracking issues as files under `docs/`; use `gh issue
  create --repo Xxx91n/READJH` for new work items.
