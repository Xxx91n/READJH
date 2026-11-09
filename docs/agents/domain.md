# Domain

READJH governs READMEs: it diagnoses, surgically improves, or fully
rewrites a repository README so the result reads as written by a person
who built the thing, and asserts only what the repo can prove.

## The problem it solves

AI-generated READMEs fail on structure, not vocabulary. They often show:

- too much coverage (product page, manual, and threat model in one file)
- a text that keeps proving itself across sections
- identical skeletons across a maintainer's repos
- marks left by the producing pipeline
- abstract-noun chains
- boundary conditions packed into single sentences

Existing skills each fix a fragment; none run the whole evidence-first
pipeline.

## Core concepts (full definitions: `GLOSSARY.md`)

- **The part that runs the existing skills in order**: routing, ordering,
  constraints, and README-specific rules. It does not include the rule
  bodies of upstream skills.
- **Find each skill by its fixed name; stop if it is missing**: the run
  looks for each executable skill at fixed paths. If one is missing, it
  stops with install instructions.
- **Excerpts taken from upstream rule files**: only the parts README work
  needs go into `references/`, and each section names its source. They are
  supplements, never skills that get called.
- **Text that no language pass may change**: commands, code, URLs,
  versions, error codes, badges, and legal or safety text.
- **How much rewriting is allowed**: `lite` when the repo has a verified
  author voice, `standard` by default. Neither one may invent personality.
- **Evidence**: something a machine can check for a completion claim.
  AI-detector scores do not count.
- **Several repos' READMEs share the same skeleton**: near-identical
  section skeletons across repos. This is checked only when the user asks
  for a group of repos in one run.
- **A text that keeps proving itself**: a claim stated more than once is a
  defect. Cut it to one statement or a link.
- **Marks left by the producing pipeline**: rule comments, phase tags, and
  other scaffolding left in the README.

## The five phases

ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY. Deletion and migration
always precede wording changes. Modes: `audit` (no writes), `improve`
(surgical), `rewrite` (full rebuild); every mode honors `--dry-run`.

## Boundaries

- The static check only reads: it never executes commands a README
  documents.
- Upstream skills are called; their rule bodies are used as excerpts.
  Spec 0002 adds READJH's own plain-language and translation rules; no other
  new rewriting rules are added.
- Chinese READMEs get zh-calibrated checks from excerpts of sepia. The
  native-language README is finished first; translation runs later in a new
  clean window. No second-language README is created unless requested.
