# Domain

READJH governs READMEs: it diagnoses, surgically improves, or fully
rewrites a repository README so the result reads as written by a person
who built the thing — and asserts only what the repo can prove.

## The problem it solves

AI-generated READMEs fail on structure, not vocabulary: over-complete
coverage (product page + manual + threat model in one file),
self-attestation repeated across sections, identical skeletons across a
maintainer's repos, leftover generation traces, abstract-noun chains,
and boundary conditions packed into single sentences. Existing skills
each fix a fragment; none run the whole evidence-first pipeline.

## Core concepts (full definitions: `GLOSSARY.md`)

- **Orchestration layer** — the part READJH owns: routing, ordering,
  constraints, README-specific rules. Not upstream rule bodies.
- **Pointer contract** — executable upstreams resolved by canonical name
  at fixed paths; miss = stop with install instructions.
- **Distilled rules** — upstream rule subsets in `references/` with
  per-section attribution; supplements, never invoked skills.
- **Freeze zone** — text no language pass may touch: commands, code,
  URLs, versions, error codes, badges, legal/safety text.
- **Intensity tier** — `lite` (verified author voice) or `standard`
  (default); neither may fabricate personality.
- **Receipt** — machine-checkable evidence for a completion claim;
  AI-detector scores do not count.
- **Skeleton isomorphism** — near-identical README section skeletons shared
  across repos; checked only in opt-in repo-set mode.
- **Self-attestation** — a claim stated more than once is a defect; it
  converges to one statement or a link.
- **Generation trace** — scaffolding marks left in the README (rule
  comments, phase tags).

## The five phases

ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY. Deletion and migration
always precede wording changes. Modes: `audit` (no writes), `improve`
(surgical), `rewrite` (full rebuild); every mode honors `--dry-run`.

## Boundaries

- The probe is static: it never executes commands a README documents.
- Upstream executors are invoked; upstream rule bodies are distilled.
  READJH does not author new rewriting rules beyond orchestration gaps.
- Chinese READMEs get zh-calibrated checks from distilled sepia rules.
  Bilingual work is native-first: the current window finishes the native
  README, then hands translation to a new clean window; no second-language
  README is created unless requested.
