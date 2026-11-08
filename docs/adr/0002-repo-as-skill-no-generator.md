# Repo-as-skill, no adapter generator

jiahao ships one behavior contract compiled into twelve host formats via
`src/` + `adapters/` + a build script, because its content genuinely differs
per host (hooks, config surfaces, file conventions).

READJH has no per-host variant: the part that runs the existing skills in
order is plain markdown instructions plus one python script. A generator
would add a build step, a drift checker, and golden-test maintenance to
produce identical output.

Decided: the repository root is the skill itself (`SKILL.md`, `references/`,
`scripts/`, `NOTICE`, `UPSTREAM.md`). Single context; `GLOSSARY.md` at root.

Consequence: if a host ever needs a materially different READJH (e.g. a
host-specific install manifest), revisit this ADR before adding a generator.
