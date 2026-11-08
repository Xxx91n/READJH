# Finding skills by name, and taking excerpts from upstream rule files

READJH runs upstream skills it does not own. Two integration options were
weighed. One was to copy every upstream file into this repo, which would make it
self-contained. The other was to declare each dependency by name and find it at
run time. That is lighter, but rule files stay in other repos. Those files carry
context that is not about READMEs.

Decided: split by role. The two executable skills
(`readme-crafter-skill`, `writing-humanize`) are found by their fixed
names at fixed search paths. If one is missing, the run stops with
install instructions; it never falls back to a skill with a similar name.
The three rule sources (`sepia` professional/style passes,
`anti-defensive-writing` EN, `academic-humanizer` claim↔evidence) are taken as
excerpts into our own `references/` files with per-section attribution. The
usable rules in `humanize-readme` are taken the same way. README work needs
only parts of them, and their upstream files link to each other heavily and
carry paper-writing context that would pollute README scope.

Rejected: copying everything (heavy, drags in sepia's model-fingerprint
layer and fiction material, duplicates upstreams already on this machine);
pointing at everything (supplementary rules would stay behind files we
cannot control and cannot trim to README scope).

Consequence: upstream skills can update independently. Our excerpt
sections carry attribution lines that must be re-synced by hand if
upstreams change — an accepted cost, recorded in `UPSTREAM.md`.
