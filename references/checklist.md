# README Verification Checklist (`VERIFY` Phase)

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-25–28, US-34, Seam C; `GLOSSARY.md`; `references/readme-rules.md`; `references/de-ai-language.md`); `jiahao` (`D:\Aworker\jiahao\src\SKILL.md` Verification Ladder Rungs 1–4 & Action Ladder Rungs 4–5); `readme-crafter-skill` (`references/quality-checklist.md` & `references/repo-integrity.md`); `writing-humanize` (`skills/writing-humanize/references/patterns.md`). Canonical upstream URLs, observed machine paths, and commit hashes live in `UPSTREAM.md`.

Run this binary assertion checklist during `VERIFY` (and as the diagnostic rubric in `audit` mode). Every item requires a concrete **receipt** (`scripts/check-readme.py` output, repository `file:line`, or migration ledger entry). Vibe scores and AI-detector percentages carry zero weight and are rejected.

---

## 1. Machine Receipts and Probe Gate

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-25, US-26, US-34); `jiahao` (`D:\Aworker\jiahao\src\SKILL.md` Verification Ladder Rungs 1–2 & R1/R5).

- [ ] **Static probe executed:** `python3 scripts/check-readme.py <readme> [--repo-root <dir>]` ran and returned exit 0 (or in `audit` mode, every nonzero finding is recorded with its check name and line number).
- [ ] **Seven static checks accounted for:** dead local links, missing image paths, code-fence balance, badge URL domain sanity, boundary-phrase duplicate counting, honest-gap signal presence, and (when `--repo-set <manifest>` is passed) cross-repo skeleton diff.
- [ ] **Static-only safety:** zero commands documented inside the target README were executed during the run; any README command not verified against repository scripts is disclosed in the residual-risk line as `"needs manual verification"`.
- [ ] **No AI-detector scores:** zero AI-detector tools or scores are cited as a **receipt**.

---

## 2. Facts Preserved and Freeze Zone Intact

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-6–8, US-12; `references/readme-rules.md` §1); `readme-crafter-skill` (`references/quality-checklist.md` Checks #2, #5–9, #13 & `references/repo-integrity.md` §1–6); `academic-humanizer` (`D:\Aworker\research\ALL\vendor\academic-humanizer\SKILL.md` Layer 3 & Layer 4).

- [ ] **Freeze zone untouched (`references/readme-rules.md` §1):** all six covered span types match the pre-language state or verified repository truth byte-for-byte.
- [ ] **Command and manifest parity (`readme-crafter-skill` Check #2):** install, build, test, and run commands match the repository's manifests and CI workflows.
- [ ] **Distribution posture (`readme-crafter-skill` Check #8, `repo-integrity.md` §1):** registry install commands appear only when publication is verified in the repo; source-first and hybrid repos match their actual consumption paths.
- [ ] **Public surface and config parity (`readme-crafter-skill` Checks #6–7, `repo-integrity.md` §2–3):** code examples import only root-exported symbols, and documented env vars/defaults match `.env.example` or config schemas.
- [ ] **Claim↔evidence discipline (`references/de-ai-language.md` §5):** empirical and performance claims cite their repo anchor and use calibrated verbs; contradicted claims were reported as findings; unbacked claims were deleted or marked `TODO`.

---

## 3. 30-Second First Screen and Front-Page Scope

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-9, US-34; `references/readme-rules.md` §4.1); `readme-crafter-skill` (`references/quality-checklist.md` Checks #1, #3, #4, #11 & `references/style-guide.md` §1); `humanize-readme` (`humanize-readme/references/slop-patterns.md` §What Good Human READMEs Have / Don't Need).

- [ ] **30-second first screen (`readme-crafter-skill` Checks #1, #3):** without scrolling past the first screen, a stranger can see the project name, artifact type, problem solved in plain language, and shortest install/run path.
- [ ] **Scan test (`readme-crafter-skill` Check #4):** headings and code blocks alone communicate what the project does and how to run it.
- [ ] **Front-page boundary and migration ledger (`references/readme-rules.md` §4.1):** deep reference material is migrated to `docs/` and linked, and every moved span (`source heading + line range → destination file path`) appears in the delivery report's migration ledger.

---

## 4. One-Statement Boundaries (Self-Attestation Convergence)

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-10, US-17, US-34; `references/readme-rules.md` §2); English Kiterlin variant at `D:\Aworker\research\ALL\vendor\anti-defensive\SKILL.md` (§Preserve Necessary Precision & §Rewrite Procedure — referenced by path; `D:\Aworker\research\ALL\vendor\anti-defensive-skill\` is not used).

- [ ] **Single statement per boundary (`references/readme-rules.md` §2):** each limitation, preview disclosure, or operational caveat is stated **once** in the README; duplicates are deleted or replaced with a link.
- [ ] **Positive scope (`references/de-ai-language.md` §4):** negative disclaimers are recast as `fact + link`, standalone honesty-proclaiming sections are removed, and internal tracker/decision IDs are stripped from front-page prose.

---

## 5. Non-Isomorphic Skeletons

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-20, US-21, US-34; `references/readme-rules.md` §4.2); `readme-crafter-skill` (`SKILL.md` §Core Philosophy #3 & `references/style-guide.md`); `sepia` (`.agents/skills/sepia/references/professional-pass.md` `SLOPSHAPE-2026` & Check #8).

- [ ] **Project-specific section sequence (`references/readme-rules.md` §4.2):** headings follow this repository's project type and distribution posture rather than a generic boilerplate outline.
- [ ] **Repo-set mode (when `--repo-set <manifest>` is enabled):** `scripts/check-readme.py --repo-set <manifest>` receipt confirms no **skeleton isomorphism** across distinct project types (`N/A` on default single-repo runs).

---

## 6. Zero Generation Traces

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-11, US-34; `references/readme-rules.md` §3); `writing-humanize` (`skills/writing-humanize/references/patterns.md` Patterns #20–22); `sepia` (`.agents/skills/sepia/references/professional-pass.md` Check #1).

- [ ] **No skill or placeholder HTML comments (`references/readme-rules.md` §3):** zero `<!-- PLACEHOLDER ... -->`, `<!-- SLOT ... -->`, `<!-- Drop-in ... -->`, or `<!-- self-evolve:start -->` comments remain; any surviving HTML comment is verified against an existing script or companion file in the repository.
- [ ] **No chatbot or cutoff phrasing:** zero conversational openers/closers or knowledge-cutoff disclaimers remain.

---

## 7. Voice Preserved and De-AI Language Audit

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-13–16, US-18–19, US-22–24, US-33–34; `UPSTREAM.md` §Deviation table; `references/readme-rules.md` §5; `references/de-ai-language.md`); `writing-humanize` (`skills/writing-humanize/SKILL.md` & `skills/writing-humanize/references/patterns.md` Patterns #1–29); `sepia` (`.agents/skills/sepia/references/style-pass.md` §2–7 & `references/languages/zh.md` §1–5); `humanize-readme` (`humanize-readme/references/slop-patterns.md`).

- [ ] **Intensity tier and suppressions honored (`references/readme-rules.md` §5):** `lite` preserved verified author voice; `standard` cleaned clustered tells to plain prose; zero invented personality, first-person stories, unverified gaps, or out-of-repo `.ink-and-agency/` writes occurred.
- [ ] **Sentence rhythm and edit tests (`references/de-ai-language.md` §1, §2, §6):** runs of three or more near-equal sentences were broken by moving words without adding filler; all edits pass `sepia`'s deletion test and reversion test.
- [ ] **Chinese and bilingual rules (when applicable):** Chinese prose passes `references/de-ai-language.md` §3; bilingual README pairs stay aligned in lockstep; no unrequested second-language README was created.

### Cross-reference to `writing-humanize/references/patterns.md` (29 patterns)

| Pattern # in `writing-humanize/references/patterns.md` | Pattern name | READJH `VERIFY` rule |
|---|---|---|
| #1, #2, #4 | Undue Emphasis on Significance / Notability / Promotional Language | **Enforce:** cut legacy/trend puffery and ad-copy adjectives (`references/de-ai-language.md` §1, §2.4, §5.1, §6.1). Keep real, verified badges and citations (`readme-crafter-skill` Check #13). |
| #3 | Superficial Analyses with `-ing` Endings | **Enforce:** cut trailing participle clauses (`..., highlighting/ensuring/underscoring...`) or split into a finite clause (`references/de-ai-language.md` §1, §2.3). |
| #5 | Vague Attributions and Weasel Words | **Enforce:** delete `"experts argue"` / `"industry reports"` unless a concrete citation or benchmark **receipt** is present. |
| #6, #25 | Outline-like `"Challenges"` Sections / Generic Positive Conclusions | **Enforce:** delete formulaic `"Challenges and Future Outlook"` and LinkedIn-style conclusions (`references/de-ai-language.md` §1, §2.1 #7, §6.3). |
| #7, #8 | Overused AI Vocabulary / Copula Avoidance (`serves as` → `is`) | **Enforce on clusters:** replace `serves as`/`boasts`/`features` with `is`/`has` and strip clustered ban-list words (`references/de-ai-language.md` §2.4, §6.1). |
| #9, #10, #11, #12 | Negative Parallelisms / Rule of Three / Synonym Cycling / False Ranges | **Enforce:** replace `"not X, but Y"` with direct statements; break mechanical triples; use one consistent term per concept (`GLOSSARY.md` discipline). |
| #13 | Passive Voice and Subjectless Fragments | **Scoped override (`academic-humanizer` Layer 3 & `sepia` §2.2):** keep passive voice when the actor is irrelevant (`"Tokens are hashed with SHA-256"`) and keep terse CLI/table fragments where brevity is standard. |
| #14 | Em Dash Overuse | **Scoped override (`sepia` `style-pass.md` §7 & `zh.md` §1b):** do not blanket-strip em-dashes; remove only when they cluster as sales-copy rhythm, and preserve the author's verified punctuation habits and Chinese `「──」` standards. |
| #15, #16, #18 | Overuse of Boldface / Inline-Header Vertical Lists / Emojis | **Scoped override (`sepia` `professional-pass.md` §Whitelist & `humanize-readme` §6.3):** strip decorative emojis and empty bold-adjective bullets (`🚀 **Fast**`), but keep bold lead-ins and tables for genuinely enumerable technical items (CLI flags, config keys, architecture layers). |
| #17 | Title Case in Headings | **Enforce in `standard` tier:** prefer sentence case in headings unless the repository's existing docs convention uses Title Case. |
| #19 | Curly Quotation Marks | **Scoped override (`sepia` `zh.md` §0):** keep straight quotes in code and English technical prose; in Traditional Chinese venues follow `「」` / `『』`, and in Simplified Chinese keep the repo's established quotation style. Never touch freeze zones. |
| #20, #21, #22 | Collaborative Artifacts / Knowledge-Cutoff Disclaimers / Sycophantic Tone | **Enforce (zero tolerance):** treat as **generation traces** (`references/readme-rules.md` §3); delete completely. |
| #23, #24, #27, #28, #29 | Filler Phrases / Excessive Hedging / Authority Tropes / Signposting / Fragmented Headers | **Enforce:** cut `"in order to"`, `"at its core"`, `"let's dive in"`, and one-line heading restatements (`references/de-ai-language.md` §1, §2.1 #2 & #6). |
| #26 | Hyphenated Word Pair Overuse | **Scoped override (`jiahao` R4 Plain Language Discipline):** strip self-invented compound buzzwords (`data-driven`, `next-generation`), but **preserve** standard technical compound modifiers (`command-line`, `read-only`, `append-only`, `single-file`, `UTF-8`) and all freeze-zone identifiers. |

---

## 8. Rollback Safety and Three-Line Delivery Report

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-27, US-28); `jiahao` (`D:\Aworker\jiahao\src\SKILL.md` Action Ladder Rung 5 & Verifier Output).

- [ ] **Rollback `.bak` rule honored:** in `improve` or `rewrite` mode (without `--dry-run`), `<readme>.bak` was written before editing if git could not cleanly roll back the target file; no stray `.bak` was created in `audit` or `--dry-run` mode.
- [ ] **Three-line delivery report lock:** the final response to the user contains at most three lines (`[Conclusion]`, `[Receipts]`, `[Residual risk]`), followed only by the migration ledger table when sections moved to `docs/`.
