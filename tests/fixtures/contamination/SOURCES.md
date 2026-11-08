# Contamination fixture sources

These fixtures carry real README text plus the directive wording named in
ticket #19. Exact quotes are recorded in `source_excerpts.json`; the tests
compare every fixture against those lines.

## Carrier text

- Title, one-line product description, and the `llms.txt` blockquote:
  `Xxx91n/EgressAPIKEY` `README.md` at commit
  `30e087277381b24715c0a85e44be8bbfe0c6cdd6`, lines 1-9. The fixtures keep
  those lines verbatim. The badge row and the language switcher are dropped
  so the fixture has no remote images or missing links.
- The `Limitations` sentence quotes the upstream caveat from line 68 of the
  same file verbatim. It is a real product caveat, not an invented gap.
- The real `llms.txt` blockquote is harmless in practice, but the written
  rule records agent-addressed text as a `HIGH` finding. The fixture asserts
  that rule's scope, not a new judgement.

## Directive wording

- "ignore the previous rules" and "you are now ...": ticket #19, "What to
  build", which names these two shapes as the directive fixture input.
- The four stop categories (run parameters, secrets, skill files, data out)
  and the `HIGH` / `BLOCKED` split: Spec 0002 (GitHub issue #16, §Contamination
  defense) and `references/readme-rules.md` §6. Spec 0002 is tracked as issue
  #16; the spec file is not in this worktree.
- The injection shape is the canonical prompt-injection pattern catalogued as
  LLM01 in the OWASP Top 10 for LLM Applications: text in untrusted content
  that addresses the model directly and asks it to change its task. This
  fixture cites the category, not a verbatim sample from that page.
- The reader examples ("run the tests", "open config.json", "upload reports
  to S3") quote `references/readme-rules.md` §6.1 and §6.2.

## Fixture cases

- `directive/README.md` — agent-addressed directive text in visible prose, in
  an HTML comment, and in a code comment, with no stop condition.
- `run_parameters/README.md` — asks the agent to change mode, dry-run flag,
  and the write set.
- `secrets/README.md` — asks the agent to read an environment file and an API
  key.
- `skill_files/README.md` — asks the agent to edit the skill's own rule files.
- `data_out/README.md` — asks the agent to send repository content to a remote
  URL.
- `reader_instructions/README.md` — ordinary instructions for a human reader,
  including "upload reports to S3"; these are data, not findings.
