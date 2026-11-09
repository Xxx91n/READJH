# Spec 0001 — READJH, a thin layer that strings existing skills together

Issue: tasks are GitHub issues at `Xxx91n/READJH` (#1–#7); this file is the spec-level plan.
Status: accepted and closed. Tickets #1–#7 are closed.
Vocabulary: `GLOSSARY.md` at the repo root. Decisions respected: ADR-0001, ADR-0002. Follow-up spec: [Spec 0002](0002-plain-language-and-native-first-translation.md).

## Problem Statement

The user's six repositories have READMEs that read as machine-written. The problem is not banned words. It is structure: one README acts as a product page, a manual, a threat model, and a versioning policy at the same time; the same boundary is stated in several sections; several repos share almost the same section skeleton; machine marks are left in the file; abstract nouns chain together; and one sentence carries too many conditions.

Each existing skill covers one small part. `readme-crafter-skill` checks facts and structure, but it has no dedicated anti-AI language pass and does not look for repeated self-proof, cross-repo skeleton sameness, or machine marks. `writing-humanize` cleans language, but it does not know README limits and tries to add personality and keep a learnings journal, which are both wrong for README work. `humanize-readme` contradicts itself: it asks for added "honest gaps" while forbidding added content. The paper-side de-AI and anti-defensive rules are useful, but they carry academic context that READMEs do not need.

The user needs one entry point that strings these skills into one evidence-first README workflow. Nothing installable today does that.

## Solution

READJH is a thin layer that strings existing skills together. The repository root is the skill itself. It finds two upstream skills by fixed name, stops with install steps when one is missing, keeps its own README rules in `references/`, and closes every run with evidence from a static check script plus a human checklist. It does not invent a second set of rewriting rules beyond the gaps in that thin layer.

Five phases: ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY. Delete and move first, then change wording.

## User Stories

1. As a repo maintainer, I want one skill I can run on any README, so I do not have to put four tools together myself.
2. As a maintainer, I want `audit` mode to list problems and their priority without touching files, so I can review the list before any edit.
3. As a maintainer, I want `improve` mode to fix an existing README in small steps, so it keeps the structure and voice that already work.
4. As a maintainer, I want `rewrite` mode to rebuild a broken README from start to finish, so I can recover a README that is beyond patching.
5. As a maintainer, I want `--dry-run` on every mode, so I can see the plan before anything lands on disk.
6. As a maintainer, I want every README claim checked against what the repo can prove (manifest, CI, entry points, real `--help` output), so the README stops claiming things the repo cannot back up.
7. As a maintainer, I want claims the repo contradicts reported as findings, not silently fixed, so wrong facts show up as red lights.
8. As a maintainer, I want claims with no evidence deleted or marked as assumptions/TODO, so unproven marketing never ships.
9. As a maintainer, I want deep material (full API, threat model, versioning policy, release process) moved to `docs/` with a migration ledger in the delivery report, so the README stays a front page and nothing is dropped.
10. As a maintainer, I want each boundary and disclaimer stated once in the README, with repeats turned into one statement or a link, so the README stops repeating itself.
11. As a maintainer, I want leftover machine marks (pipeline comments, rule tags) found and removed, so the README carries no scaffolding.
12. As a maintainer, I want commands, code blocks, URLs, versions, error codes, badge rows, and legal/safety text left byte-for-byte alone through every language pass, so cleanup cannot corrupt facts.
13. As a maintainer, I want the language pass to run `writing-humanize` plus the rules picked out of upstream files, so AI patterns are removed at README strength, not generic-prose strength.
14. As a maintainer, I want a `lite` rewrite-strength level when the repo shows a strong personal voice or the user gives a writing sample, so the voice is not flattened.
15. As a maintainer, I want `standard` as the default rewrite-strength level, so I do not have to choose a level for an ordinary repo.
16. As a maintainer, I want the skill forbidden from inventing personality, gaps, or first-person stories the repo does not contain, so cleanup cannot fake authenticity.
17. As a maintainer, I want defensive long sentences turned into "fact + link", so boundaries stay precise and appear once.
18. As a maintainer, I want abstract-noun chains replaced with concrete things, so the README reads like a person who built the thing wrote it.
19. As a maintainer, I want a flat sentence rhythm flagged and broken by moving words, never by adding filler, so the cadence varies without padding.
20. As a maintainer with several repos, I want an optional multi-repo check for README skeletons that look like one mold, so my repos stop sharing one template.
21. As a maintainer, I want the multi-repo check off by default, so single-repo runs pay no extra cost.
22. As a maintainer, I want bilingual READMEs found and processed together with the same structure, so the English and Chinese versions do not drift.
23. As a maintainer, I want no second-language README created unless I ask, so the skill does not add files I did not want.
24. As a maintainer, I want Chinese text checked against Chinese human rhythm, not English defaults, so Chinese READMEs get the right style checks.
25. As a maintainer, I want a static check to verify links, images, code fences, badge targets, repeated boundary phrases, and gap signals, without running anything the README says, so I get evidence and no untrusted command runs.
26. As a maintainer, I want README commands listed as "needs manual verification" in the residual-risk line, so untested commands are never called tested.
27. As a maintainer, I want the delivery report capped at three lines (conclusion, evidence, residual risk), so reporting follows the same evidence-first rule.
28. As a maintainer, I want a `.bak` copy before edits when Git cannot roll back, so the original is never lost.
29. As an installer, I want missing upstream skills to stop the run with exact install steps, so a half-installed dependency never degrades a run silently.
30. As an installer, I want dependencies found by canonical name at documented search paths only, so a wrong skill with a similar name is never loaded.
31. As a user of another agent host, I want the skill to be plain markdown plus a python3 check script, so it runs on any Agent Skills host.
32. As a downstream packager, I want upstream licenses kept and each picked-out rule section credited, so redistribution stays legal and credit is kept.
33. As a maintainer, I want `writing-humanize`'s self-evolve journaling and personality injection explicitly suppressed when READJH runs it, so no out-of-repo writes or fake voice leak into README work.
34. As a maintainer, I want acceptance measured on real evidence (command truth, first-screen clarity, one statement per boundary, non-isomorphic skeletons, zero machine marks), never on AI-detector scores.

## Implementation Decisions

### Modules

- **SKILL.md** (model-invoked): frontmatter `name` and `description` carry the trigger words for README audit/improve/rewrite and de-AI requests. The body holds the five phases, the find-skills rules, the short no-touch and rewrite-strength rules inline, and the three-line report format.
- **references/readme-rules.md**: the README rules the thin layer owns: what no language pass may touch, one-statement boundaries, machine marks, skeleton sameness, no invented personality. Each rule carries its credit line.
- **references/de-ai-language.md**: rules handed to `writing-humanize`, picked from sepia professional/style passes and zh calibration, the English Kiterlin anti-defensive rules, academic-humanizer claim-to-evidence rules, and the usable humanize-readme rules. Ban tables keep their credit; rationale is rewritten.
- **references/checklist.md**: the human checklist for VERIFY.
- **scripts/check-readme.py**: stdlib-only python3 CLI. Arguments: README path, optional `--repo-root`, optional `--repo-set` manifest. Exit 0 when no blocking findings; nonzero with a findings list. Output is suitable as evidence.
- **UPSTREAM.md**: dependency table (canonical name, URL, license, required files, search paths), install steps, and deviation table.
- **NOTICE**: upstream credits and license texts (all MIT).
- **LICENSE**: MIT for READJH itself.
- **README.md**: what READJH is, install, quickstart, find-skills summary.
- **AGENTS.md** and **docs/agents/**: repo housekeeping.
- **docs/spec/** and **docs/tickets/**: spec and ticket tracker.
- **.gitattributes**: `* text=auto eol=lf`. The repo is LF-normalized.

### Interfaces

- **Find-skills rule**: canonical names `readme-crafter-skill` and `writing-humanize`; search order `.agents/skills/` → `~/.agents/skills/` → the standard roots in `UPSTREAM.md`; miss → stop and give install steps; never fall back to a similar name.
- **Check CLI**: `python3 scripts/check-readme.py <readme> [--repo-root <dir>] [--repo-set <manifest>]` → exit 0/nonzero plus findings on stdout.
- **Rule handoff**: `references/de-ai-language.md` and `references/readme-rules.md` are read into context at LANGUAGE, not run as skills.
- **Migration ledger**: a required section in the improve/rewrite report. It lists every moved span and its destination file.

### Do-not list

- No vendoring upstream repos.
- No name-based fallback for dependencies.
- `humanize-readme` never runs; it only contributes rules.
- No AI-detector score as acceptance.
- No running commands found inside a README.
- No invented personality, gaps, or first-person stories.
- No second-language README unless requested.
- No generator or adapter machinery (ADR-0002).

## Testing Decisions

Approved checkpoints:

- **Checkpoint A, the check script (primary, TDD)**: unit tests on the CLI contract and each check, using fixture READMEs. Test external behavior only: files and arguments in, findings and exit code out. Fixtures come from real upstream examples and the six target repos, not invented content.
- **Checkpoint B, the SKILL.md contract (light)**: frontmatter validity, phase and glossary term consistency, and find-skills text matching `UPSTREAM.md`. This is a lint checklist, not a test framework.
- **Checkpoint C, end-to-end acceptance**: run `audit` on the six repos plus one human-baseline README. Judge it on the research acceptance list, the check output, and the user's blind review.

What makes a good test here: binary checks against files on disk and declared contracts. Do not assert on prose style inside the skill documents; style is the rules' job. Do not test that picked-out files "match" upstream; the credit lines are the contract.

Prior art: none in this repo. The check script follows the static-inspection approach of `readme-crafter-skill/scripts/scan-project.py`.

## Out of Scope

- Writing new rewriting rules beyond the gaps in the thin layer. Upstream skills do that.
- Running or validating README-documented commands.
- Multi-host adapter builds (ADR-0002).
- Running the actual governance pass on the six repos. This spec builds the tool; repo-by-repo passes are separate work.
- AI-detector benchmarking.
- GitHub remote setup, issue migration, and publishing the skill anywhere.

## Further Notes

- Runtime checks carried to tickets: the real output of `scan-project.sh` under Git Bash on this host, and `writing-humanize`'s obedience to the picked-out rules in practice. Both are check-first tasks; a failed check stops the dependent work.
- Upstreams are not version-pinned. `UPSTREAM.md` records the upstream commit seen at authoring time; a drift note lives there, not in `SKILL.md`.
- The two `anti-defensive-writing` upstreams share a name. READJH picks out the English Kiterlin variant only and points to it by path, never by name.
