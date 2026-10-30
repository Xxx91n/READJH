# READJH

A thin orchestration skill for one-shot README governance and rewrite. It sequences
existing upstream skills under an evidence-first discipline; it owns no rewriting
rules of its own except the README-specific gaps upstream skills leave uncovered.

## Language

**Orchestration Layer (编排层)**:
The part of READJH that is ours: routing, ordering, constraints, and the
README-specific rules no upstream skill provides. Excludes upstream rule bodies.
_Avoid_: our rules, custom logic

**Pointer Contract (指针契约)**:
A dependency declared by canonical skill name, resolved at fixed search paths.
Missing dependency means stop with install instructions, never name-based fallback.
_Avoid_: auto-discovery, soft dependency

**Distilled Rules (蒸馏规则)**:
Subsets of upstream rule files extracted into our own `references/`, with
per-section source attribution. Used as supplements, never as invoked skills.
_Avoid_: vendored copy, borrowed rules

**Freeze Zone (冻结区)**:
README regions no language pass may alter: commands, code blocks, URLs, versions,
error codes, badge rows, legal and safety boundary text.
_Avoid_: protected text, locked section

**Intensity Tier (强度档)**:
How much language rewriting is permitted: `lite` for repos with a verified author
voice or strong personal style, `standard` otherwise. Neither tier may invent
personality or limitations the repo does not contain.
_Avoid_: mode, level

**Repo-Set Mode (仓库集模式)**:
Optional cross-repository check for skeleton isomorphism over a user-supplied
set of repositories. Off by default.
_Avoid_: batch mode, fleet check

**Receipt (凭证)**:
Machine-checkable evidence backing a completion claim: probe script output,
verified command results, a diff ledger. Inherited from jiahao; detector scores
do not count.
_Avoid_: proof, evidence

**Skeleton Isomorphism (结构同构)**:
Multiple repositories sharing near-identical README section skeletons, hero
blocks, or badge density — an AI tell independent of wording.
_Avoid_: template reuse, sameness

**Self-Attestation (自证)**:
Text that re-proves its own honesty or verified status. A claim stated more than
once in a README is a defect; it converges to one statement or a link.
_Avoid_: defensive repetition, over-justification

**Generation Trace (生成痕迹)**:
Leftover markers of the producing pipeline inside the README, such as rule
comments or phase tags (e.g. `readme-crafter rule`).
_Avoid_: AI residue, metadata leak
