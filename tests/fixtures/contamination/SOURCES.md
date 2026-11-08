# Contamination fixture sources

These fixtures carry real README text plus the directive wording named in
ticket #19. The goal is a realistic page, not a synthetic paragraph that
exists only for the test.

## Carrier text

- Repository text and the agent-facing `llms.txt` line: `Xxx91n/EgressAPIKEY`
  `README.md` at commit `30e087277381b24715c0a85e44be8bbfe0c6cdd6`, lines 1-9.
  The fixture keeps the title, the one-line product description, and the
  "AI / automation agents" blockquote verbatim; the badge row and the language
  switcher are dropped so the fixture has no remote images or missing links.
- The "Limitations" sentence is derived from the `Mode A` boundary in the same
  README, shortened to one sentence.

## Directive wording

- "ignore the previous rules" and "you are now ...": ticket #19, "What to
  build", which names these two shapes as the directive fixture input.
- The four stop categories (run parameters, secrets, skill files, data out)
  and the `HIGH` / `BLOCKED` split: `docs/spec/0002-plain-language-and-native-first-translation.md`
  (§Contamination defense) and `references/readme-rules.md` §6.
- The injection shape is the canonical prompt-injection pattern catalogued as
  LLM01 in the OWASP Top 10 for LLM Applications: text in untrusted content
  that addresses the model directly and asks it to change its task.

## Fixture cases

- `directive/README.md` — agent-addressed directive text, no stop condition.
- `run_parameters/README.md` — asks the agent to change mode, dry-run flag,
  and the write set.
- `secrets/README.md` — asks the agent to read an environment file and an API
  key.
- `skill_files/README.md` — asks the agent to edit the skill's own rule files.
- `data_out/README.md` — asks the agent to send repository content to a remote
  URL.
- `reader_instructions/README.md` — ordinary instructions for a human reader,
  including "upload ... to the team S3 bucket"; these are data, not findings.
