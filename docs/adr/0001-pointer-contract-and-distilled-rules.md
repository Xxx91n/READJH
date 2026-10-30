# Pointer contract for executors, distilled rules for references

READJH orchestrates upstream skills it does not own. Two integration options
were weighed: vendor every upstream file into this repo (self-contained), or
declare every dependency as a pointer resolved at run time (light, but rules
files scatter across other repos and carry non-README context).

Decided: split by role. The two executable skills
(`readme-crafter-skill`, `writing-humanize`) are invoked through a pointer
contract — canonical name at fixed search paths, missing means stop with
install instructions, never name-based fallback. The three rule sources
(`sepia` professional/style passes, `anti-defensive-writing` EN,
`academic-humanizer` claim↔evidence, plus `humanize-readme`'s salvageable
rules) are distilled into our own `references/` files with per-section
attribution, because README work needs only subsets of them and their
upstream files interlink heavily and embed paper-writing context that would
pollute README scope.

Rejected: full vendoring (heavy, drags in sepia's model-fingerprint layer and
fiction material, duplicates upstreams already on this machine); full
pointing (supplementary rules would stay behind files we cannot control and
cannot trim to README scope).

Consequence: upstream executors can update independently; our distilled
rules carry attribution lines that must be re-synced by hand if upstreams
change — accepted cost, recorded in `UPSTREAM.md`.
