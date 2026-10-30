# Spec 0001 — READJH orchestration skill

Issue: tickets are GitHub issues at `Xxx91n/READJH` (#1–#7); spec-level plan is this file
Status: ready-for-agent (spec stage, implementation tickets cut by /to-tickets)
Vocabulary: `GLOSSARY.md` at repo root. Decisions respected: ADR-0001, ADR-0002.

## Problem Statement

The user's six repositories ship READMEs that read as AI-generated — not from
banned words, but from structural tells: over-completeness (a README acting as
product page + reference manual + threat model + versioning policy),
self-attestation repeated in several sections, near-identical skeletons across
repos, leftover generation traces, dense abstract-noun chains, and sentences
carrying too many boundary conditions.

Existing skills each cover one fragment. `readme-crafter-skill` handles facts
and structure but has no dedicated anti-AI language pass and does not hunt
self-attestation, cross-repo isomorphism, or generation traces.
`writing-humanize` cleans language but knows nothing about README constraints
and tries to inject personality and keep a learnings journal — both wrong for
README work. `humanize-readme` contradicts itself (it demands added "honest
gaps" while forbidding added content). Paper-side de-AI and anti-defensive
skills hold useful rules but carry academic context READMEs do not need.

The user needs a single entry point that orchestrates these into one
evidence-first README governance pipeline, and nothing they can install today
does that.

## Solution

READJH is a thin orchestration skill — the repo root itself is the skill. It
sequences upstream executable skills through a pointer contract, supplies the
README-specific orchestration rules no upstream provides as its own
`references/` files, and closes every run with machine-checkable receipts
from a static probe script, plus a human checklist. It owns no rewriting
rules of its own beyond the orchestration layer gaps.

Five phases: ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY. Deletion and
migration always precede wording changes.

## User Stories

1. As a repo maintainer, I want to invoke one skill on any README, so that I get a governed rewrite without assembling four tools myself.
2. As a maintainer, I want `audit` mode to diagnose and prioritize without touching files, so that I can review findings before any edit.
3. As a maintainer, I want `improve` mode to surgically upgrade an existing README, so that structure and voice I already have are preserved where sound.
4. As a maintainer, I want `rewrite` mode for a full rebuild, so that a broken README can be redone end to end.
5. As a maintainer, I want `--dry-run` on every mode, so that I can see the plan before anything lands on disk.
6. As a maintainer, I want every README claim checked against repository-native evidence (manifest, CI, entry points, real `--help` output), so that the README stops asserting things the repo cannot prove.
7. As a maintainer, I want claims contradicted by the repo reported as findings instead of silently fixed, so that wrong facts surface as red lights.
8. As a maintainer, I want claims with no evidence omitted or marked as assumptions/TODO, so that unverifiable marketing never ships.
9. As a maintainer, I want deep material (full API, threat model, versioning policy, release process) migrated to `docs/` with a migration ledger in the delivery report, so that the README stays a front page and nothing is silently dropped.
10. As a maintainer, I want each boundary and disclaimer stated exactly once in the README with repeats converging to one statement or a link, so that self-attestation stops repeating.
11. As a maintainer, I want leftover generation traces (pipeline comments, rule tags) flagged and removed, so that the README carries no scaffolding marks.
12. As a maintainer, I want commands, code blocks, URLs, versions, error codes, badge rows, and legal/safety text frozen through every language pass, so that cleanup cannot corrupt facts.
13. As a maintainer, I want the language pass to run `writing-humanize` plus distilled supplement rules, so that AI patterns are removed at README intensity rather than generic-prose intensity.
14. As a maintainer, I want `lite` intensity when the repo shows a strong personal voice or supplies an author writing sample, so that voice is not flattened.
15. As a maintainer, I want `standard` intensity as the default, so that no intensity decision is required for ordinary repos.
16. As a maintainer, I want the skill forbidden from inventing personality, honest gaps, or first-person stories not present in the repo, so that cleanup cannot manufacture authenticity.
17. As a maintainer, I want defensive long sentences recast as "fact + link", so that boundaries survive precisely and once.
18. As a maintainer, I want abstract-noun chains replaced by concrete referents, so that the README reads as written by a person who built the thing.
19. As a maintainer, I want uniform sentence rhythm flagged and broken by moving words (never by adding filler), so that cadence varies without padding.
20. As a maintainer running several repos, I want optional repo-set mode checking README skeleton isomorphism across repos, so that my repos stop sharing one template.
21. As a maintainer, I want the repo-set check off by default, so that single-repo runs pay no extra cost.
22. As a maintainer, I want bilingual READMEs detected and processed in lockstep with structure kept aligned, so that EN and zh variants do not drift.
23. As a maintainer, I want no second-language README created unless I ask, so that the skill does not sprawl files.
24. As a maintainer, I want Chinese text to get the zh-calibrated style checks from the distilled sepia rules, so that Chinese READMEs are held to Chinese human rhythm, not English defaults.
25. As a maintainer, I want a static probe to verify links, images, code-fence balance, badge targets, boundary-phrase duplicates, and honest-gap signals — without executing anything the README says, so that receipts exist and untrusted commands never run.
26. As a maintainer, I want README commands flagged as "needs manual verification" in the residual-risk line, so that untested commands are never claimed as tested.
27. As a maintainer, I want the delivery report capped at three lines — conclusion, receipts, residual risk — so that reporting itself follows the evidence-first discipline.
28. As a maintainer, I want a `.bak` kept before edits when git cannot roll back, so that the original is never lost.
29. As an installer, I want missing upstream skills to stop the run with exact install instructions, so that a half-installed dependency never degrades a run silently.
30. As an installer, I want dependency resolution by canonical name at documented search paths only, so that a wrong skill with a similar name is never loaded.
31. As a user of a different agent host, I want the skill to be plain markdown plus a python3 probe, so that it runs on any Agent Skills host.
32. As a downstream packager, I want upstream licenses preserved and each distilled rule section attributed, so that redistribution stays compliant and creditable.
33. As a maintainer, I want `writing-humanize`'s self-evolve journaling and personality injection explicitly suppressed when invoked through READJH, so that no out-of-repo writes or fabricated voice leak into README work.
34. As a maintainer, I want acceptance measured on real receipts — command truth, first-screen clarity, single-statement boundaries, non-isomorphic skeletons, zero generation traces — never on AI-detector scores.

## Implementation Decisions

### Modules

- **SKILL.md** (model-invoked): frontmatter `name`, `description` carrying trigger
  phrasing for README audit/improve/rewrite and de-AI requests; body holds the
  five-phase pipeline, pointer-contract resolution block, freeze-zone and
  intensity rules inline (short), and the three-line report format.
- **references/readme-rules.md**: orchestration-layer rules — freeze-zone
  definition, self-attestation convergence, generation-trace detection,
  skeleton-isomorphism definition, no-invented-personality rule; each rule
  carries its upstream/research attribution line.
- **references/de-ai-language.md**: supplement rules handed to
  `writing-humanize` — distilled subsets of sepia professional-pass +
  style-pass + zh calibration, anti-defensive-writing (EN)
  defensive→positive-scope transform, academic-humanizer claim↔evidence
  discipline, and the salvageable humanize-readme rules (burstiness,
  suspicious-completeness, real-gap signals). Ban tables verbatim with
  attribution; rationale rewritten; overlapping patterns merged with multiple
  attributions.
- **references/checklist.md**: the human verification checklist for VERIFY.
- **scripts/check-readme.py**: stdlib-only python3 CLI. Arguments: target
  README path, optional `--repo-root`, optional `--repo-set` manifest file for
  cross-repo skeleton diff. Exit 0 when no blocking findings; nonzero with a
  findings list. Emits structured text suitable as a receipt.
- **UPSTREAM.md**: dependency table (canonical name, upstream URL, license,
  required files, search paths), install contract, and the deviation table
  recording READJH's two suppressions of writing-humanize.
- **NOTICE**: upstream credits and license texts (all MIT).
- **LICENSE**: MIT, READJH itself.
- **README.md**: what READJH is, install, quickstart, pointer contract summary.
- **AGENTS.md** + **docs/agents/** (issue-tracker, triage-labels, domain):
  repo housekeeping files — declared extra artifacts, approved in grilling.
- **docs/spec/**, **docs/tickets/**: file-based spec and ticket tracker; ticket
  numbers are filenames until a remote exists.
- **.gitattributes**: `* text=auto eol=lf` — the repo is LF-normalized; current
  files are LF.

### Interfaces

- Pointer contract: canonical names `readme-crafter-skill`, `writing-humanize`;
  search order `.agents/skills/` → `~/.agents/skills/` → standard skill roots
  listed in `UPSTREAM.md`; miss → stop + install instructions; never
  name-similarity fallback.
- Probe CLI contract: `python3 scripts/check-readme.py <readme> [--repo-root
  <dir>] [--repo-set <manifest>]` → exit 0/nonzero + findings on stdout.
- Supplement-rules handoff: `references/de-ai-language.md` and
  `references/readme-rules.md` are read into context at LANGUAGE phase, not
  invoked as skills.
- Migration ledger: required section in the improve/rewrite delivery report
  listing every moved span and its destination file.

### Do-not list (locked in grilling)

- No vendoring upstream repos; no name-based fallback for dependencies.
- `humanize-readme` never executes; it contributes rules only.
- No AI-detector score as an acceptance signal.
- No executing commands found inside a README.
- No invented personality, gaps, or first-person stories.
- No second-language README unless requested.
- No generator/adapter machinery (ADR-0002).

## Testing Decisions

Approved seams:

- **Seam A — probe script (primary, TDD)**: unit tests on
  `check-readme.py`'s CLI contract and per-check behavior with fixture
  READMEs. Test external behavior only: inputs (files on disk + args) →
  outputs (findings + exit code). Fixture READMEs derive from real upstream
  examples and the six target repos, not invented content.
- **Seam B — SKILL.md contract (light)**: frontmatter validity, phase/glossary
  term consistency, pointer-contract text matching `UPSTREAM.md`. A lint
  checklist, not a test framework.
- **Seam C — end-to-end acceptance**: run `audit` mode on the six repos
  (6F, EgressAPIKEY, mcp-for-maya, env-manager, boxing, jiahao) plus one
  human-baseline README (ripgrep or user-designated). Judged on the research
  acceptance list + probe output + the user's blind review.

What makes a good test here: binary checks against files on disk and declared
contracts. No assertions on prose style inside the skill documents — style is
the rules' job, not a test's. No testing that distilled files "match"
upstream: attribution lines are the contract.

Prior art: none in this repo (greenfield). The probe's check style follows
the static-inspection approach of `readme-crafter-skill/scripts/scan-project.py`.

## Out of Scope

- Authoring new rewriting rules beyond the orchestration layer's gaps — that
  is upstream skills' job.
- Executing or validating README-documented commands.
- Multi-host adapter builds (ADR-0002).
- Running the actual governance pass on the six repos — this spec builds the
  tool; repo-by-repo passes are separate work.
- AI-detector benchmarking.
- GitHub remote setup, issue migration, and publishing the skill anywhere.

## Further Notes

- Runtime validation items carried to implementation tickets: real output of
  `scan-project.sh` under Git Bash on this host; `writing-humanize`'s
  obedience to distilled supplement rules in practice. Both are probe-first
  tasks; a failed probe stops the dependent work.
- Upstreams are not version-pinned. `UPSTREAM.md` records the upstream commit
  hash observed at authoring time; a drift note lives there, not in SKILL.md.
- The two `anti-defensive-writing` upstreams share a name; READJH distills
  the English Kiterlin variant only and references it by path, never by name.
