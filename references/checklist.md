# README Verification Checklist (`VERIFY` Phase)

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-25–28, US-34, Seam C; `GLOSSARY.md`; `references/readme-rules.md`; `references/de-ai-language.md`); `jiahao` (`D:\Aworker\jiahao\src\SKILL.md` Verification Ladder Rungs 1–4 & Action Ladder Rungs 4–5); `readme-crafter-skill` (`https://github.com/linhai0872/readme-crafter-skill`, `references/quality-checklist.md` & `references/repo-integrity.md` @ `08db7782836c542d9b597860da33fcc159e36433`); `writing-humanize` (`https://github.com/risadams/ink-and-agency`, `skills/writing-humanize/references/patterns.md` @ `e1f0a00e06d55c00502e0ccbea79ab453e7fb118`); `sepia` (`D:\Aworker\research\ALL\.agents\skills\sepia\references\professional-pass.md`, `style-pass.md`, `languages/zh.md` @ `365185bec8c5eae8711ebd56b4f4556759f685b2`); `anti-defensive-writing` (`https://github.com/Kiterlin/anti-defensive-writing`, English Kiterlin variant at `D:\Aworker\research\ALL\vendor\anti-defensive\SKILL.md` @ `365185bec8c5eae8711ebd56b4f4556759f685b2`, disambiguated by path from unused `D:\Aworker\research\ALL\vendor\anti-defensive-skill\`); `academic-humanizer` (`https://github.com/AIScientists-Dev/academic-humanizer`, `D:\Aworker\research\ALL\vendor\academic-humanizer\SKILL.md` @ `365185bec8c5eae8711ebd56b4f4556759f685b2`); `humanize-readme` (`https://github.com/b4r7x/agent-skills`, `humanize-readme/references/slop-patterns.md` @ `292bad1458a30384e9e6eb3d46ba24428d7c5618`).

Run this binary assertion checklist during `VERIFY` (and as the diagnostic rubric in `audit` mode). Every item requires a concrete **receipt** (`scripts/check-readme.py` output, repository `file:line`, or diff ledger entry). Vibe scores and AI-detector percentages carry zero weight and are rejected.

---

## 1. Machine Receipts and Probe Gate

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-25, US-26, US-34); `jiahao` (`D:\Aworker\jiahao\src\SKILL.md` Verification Ladder Rungs 1–2 & R1/R5).

- [ ] **Static probe executed:** `python3 scripts/check-readme.py <readme> [--repo-root <dir>]` ran and returned exit 0 (or in `audit` mode, every nonzero finding is recorded with its check name and line number).
- [ ] **Seven static checks accounted for:**
  1. Dead local markdown links (`[text](path)` resolves on disk)
  2. Missing local image paths (`![alt](path)` and `<img src="...">` resolve on disk)
  3. Code-fence balance (every opening ```` ``` ```` or `~~~` closes cleanly)
  4. Badge URL domain sanity (shields/workflow URLs are well-formed and match the repo)
  5. Boundary-phrase duplicate counting (repeated caveats flagged)
  6. Honest-gap signal presence (real platform/runtime boundaries checked)
  7. Cross-repo skeleton diff (when `--repo-set <manifest>` is passed)
- [ ] **Static-only safety:** zero commands documented inside the target README were executed by the probe or agent during the run.
- [ ] **Untested commands disclosed:** any README command not verified against repository scripts is named in the delivery report's residual-risk line as `"needs manual verification"`.
- [ ] **No AI-detector scores:** zero AI-detector tools or scores are cited as a **receipt**.

---

## 2. Facts Preserved and Freeze Zone Intact

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-6–8, US-12; `references/readme-rules.md` §1, §6); `readme-crafter-skill` (`https://github.com/linhai0872/readme-crafter-skill`, `references/quality-checklist.md` Checks #2, #5–9, #13 & `references/repo-integrity.md` §1–6 @ `08db7782836c542d9b597860da33fcc159e36433`); `academic-humanizer` (`D:\Aworker\research\ALL\vendor\academic-humanizer\SKILL.md` Layer 3 & Layer 4 @ `365185bec8c5eae8711ebd56b4f4556759f685b2`).

- [ ] **Freeze zone byte-identical across `LANGUAGE`:** fenced code blocks, inline commands and flags, URLs, file paths, version strings, error codes, badge rows, direct quotations, and legal/safety boundary text were not altered by any language pass.
- [ ] **Command and manifest parity:** every install, build, test, and run command matches the repository's actual manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `.github/workflows/`).
- [ ] **Distribution posture honesty:** package-registry install commands (`npm install <pkg>`, `pip install <pkg>`, `cargo install <pkg>`) appear only when registry publication is verified in the repo; source-first repos lead with `clone → install → run`; hybrid framework/playground repos separate running the local app from consuming the package.
- [ ] **Public surface parity:** code examples import only symbols exported from the root package entry point, never unexported internal paths.
- [ ] **Configuration parity:** environment variables, flags, and default endpoints match `.env.example` or the configuration schema in code.
- [ ] **Claim↔evidence match (`academic-humanizer` Layer 4):** every empirical or performance claim cites its benchmark/test location and uses a verb no stronger than the measurement; contradicted claims were reported as findings (never silently rewritten); unbacked claims were deleted or marked `TODO`.

---

## 3. 30-Second First Screen and Front-Page Scope

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-9, US-34; `references/readme-rules.md` §4.1); `readme-crafter-skill` (`https://github.com/linhai0872/readme-crafter-skill`, `references/quality-checklist.md` Checks #1, #3, #4, #11 & `references/style-guide.md` §1 @ `08db7782836c542d9b597860da33fcc159e36433`); `humanize-readme` (`https://github.com/b4r7x/agent-skills`, `humanize-readme/references/slop-patterns.md` §What Good Human READMEs Have / Don't Need @ `292bad1458a30384e9e6eb3d46ba24428d7c5618`).

- [ ] **30-second first screen:** without scrolling past the first screen, a stranger can identify (a) the project name, (b) what kind of artifact it is (CLI, library, desktop app, plugin, skill), (c) the concrete problem it solves in plain language, and (d) the shortest path to install and first run.
- [ ] **Scan test:** reading only headings and code blocks communicates what the project does and how to run it.
- [ ] **Front-page boundary enforced:** deep reference material (full API tables, threat models, secret-boundary matrices, monotonic versioning rules, upstream lock policies, release checklists) is moved out of `README.md` into `docs/` and linked.
- [ ] **Migration ledger complete:** if `improve` or `rewrite` moved any span to `docs/`, every moved section (`source heading + line range → destination file path`) is listed in the delivery report's migration ledger with zero silent drops.

---

## 4. One-Statement Boundaries (Self-Attestation Convergence)

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-10, US-17, US-34; `references/readme-rules.md` §2); `anti-defensive-writing` (`https://github.com/Kiterlin/anti-defensive-writing`, English Kiterlin variant at `D:\Aworker\research\ALL\vendor\anti-defensive\SKILL.md` @ `365185bec8c5eae8711ebd56b4f4556759f685b2` — disambiguated by path from unused `D:\Aworker\research\ALL\vendor\anti-defensive-skill\`).

- [ ] **Single statement per boundary:** each scope limit, preview status, or operational caveat is stated **once** in the README; duplicates across hero callouts, capability tables, demo notes, and closing sections are deleted or replaced with a link.
- [ ] **Positive scope (`fact + link`):** defensive disclaimers (`"We do not claim..."`, `"This is not intended to..."`, `"Do not read this page as..."`) are rewritten into positive scope statements with a link to the contract or doc file.
- [ ] **No self-congratulatory honesty section:** standalone sections that exist only to re-assert the README's truthfulness (such as a closing `"Honesty notes"` section repeating earlier caveats) are removed.
- [ ] **No internal tracker noise:** internal ticket numbers, round tags, and decision IDs (`#85②`, `D-204③④`, `A-044`) do not appear in front-page prose.

---

## 5. Non-Isomorphic Skeletons

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-20, US-21, US-34; `references/readme-rules.md` §4.2); `readme-crafter-skill` (`https://github.com/linhai0872/readme-crafter-skill`, `SKILL.md` §Core Philosophy #3 & `references/style-guide.md` @ `08db7782836c542d9b597860da33fcc159e36433`); `sepia` (`D:\Aworker\research\ALL\.agents\skills\sepia\references\professional-pass.md` `SLOPSHAPE-2026` & Check #8 @ `365185bec8c5eae8711ebd56b4f4556759f685b2`).

- [ ] **Project-specific section sequence:** the heading sequence matches this repository's project type and distribution posture (CLI leads with command + output; library leads with install + minimal import snippet; desktop/web app leads with visual/download + run path).
- [ ] **Repo-set mode (when `--repo-set <manifest>` is enabled):** `scripts/check-readme.py --repo-set <manifest>` confirms that repositories of different types do not share an isomorphic heading skeleton, identical hero block, or uniform badge row. (Mark `N/A` on single-repo runs where `repo-set mode` is off by default.)

---

## 6. Zero Generation Traces

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-11, US-34; `references/readme-rules.md` §3); `writing-humanize` (`https://github.com/risadams/ink-and-agency`, `skills/writing-humanize/references/patterns.md` Patterns #20–22 @ `e1f0a00e06d55c00502e0ccbea79ab453e7fb118`); `sepia` (`D:\Aworker\research\ALL\.agents\skills\sepia\references\professional-pass.md` Check #1 @ `365185bec8c5eae8711ebd56b4f4556759f685b2`).

- [ ] **No skill or placeholder HTML comments:** zero `<!-- PLACEHOLDER: ... (readme-crafter rule) -->`, `<!-- SLOT ... -->`, `<!-- Drop-in: ... -->`, or `<!-- self-evolve:start -->` comments remain in the file.
- [ ] **Repo comments verified against scripts:** any remaining HTML comment (`<!-- acknowledgments:start -->`, `<!-- README-I18N:START -->`, `<!-- synced-with: ... -->`) is backed by an existing script or companion file in the repository.
- [ ] **No chatbot or cutoff phrasing:** zero conversational openers/closers (`"Great question!"`, `"I hope this helps!"`, `"Let me know if..."`) or knowledge-cutoff disclaimers remain.

---

## 7. Voice Preserved and De-AI Language Audit

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-13–16, US-18–19, US-22–24, US-33–34; `UPSTREAM.md` §Deviation table; `references/readme-rules.md` §5; `references/de-ai-language.md`); `writing-humanize` (`https://github.com/risadams/ink-and-agency`, `skills/writing-humanize/SKILL.md` & `skills/writing-humanize/references/patterns.md` Patterns #1–29 @ `e1f0a00e06d55c00502e0ccbea79ab453e7fb118`); `sepia` (`D:\Aworker\research\ALL\.agents\skills\sepia\references\style-pass.md` §2–7 & `references\languages\zh.md` §1–5 @ `365185bec8c5eae8711ebd56b4f4556759f685b2`); `humanize-readme` (`https://github.com/b4r7x/agent-skills`, `humanize-readme/references/slop-patterns.md` @ `292bad1458a30384e9e6eb3d46ba24428d7c5618`).

- [ ] **Intensity tier honored (`lite` vs. `standard`):** `lite` preserved the author's verified voice and habits; `standard` stripped clustered AI tells to plain, concrete prose.
- [ ] **No fabricated personality or gaps:** zero invented first-person stories (`"I built this because..."`), casual filler, or unverified limitations (`"Not tested on Windows"`) were added (`writing-humanize` personality injection and `humanize-readme` gap invention suppressed).
- [ ] **No out-of-repo writes:** `writing-humanize` self-evolve journaling (`~/.ink-and-agency/learnings/` or `.ink-and-agency/`) did not run or write any file.
- [ ] **Sentence rhythm and edit tests (`sepia` `style-pass.md` §4–5):** runs of three or more near-equal sentences were broken by moving/splitting/merging words without adding filler; every added phrase passes the deletion test and every replacement passes the reversion test.
- [ ] **Chinese and bilingual rules (when applicable):** Chinese prose checked against `references/de-ai-language.md` §3 (no connective stacking, no `進行/加以/予以` verb padding, no `綜上所述/值得一提的是`); bilingual README pairs updated in lockstep with aligned structure; no unrequested second-language README created.

### Cross-reference to `writing-humanize/references/patterns.md` (29 patterns)

Use this lookup table during `VERIFY` to confirm `writing-humanize`'s 29 patterns were applied with READJH's README-specific overrides:

| Pattern # in `writing-humanize/references/patterns.md` | Pattern name | READJH `VERIFY` rule |
|---|---|---|
| #1, #2, #4 | Undue Emphasis on Significance / Notability / Promotional Language | **Enforce:** cut legacy/trend puffery and ad-copy adjectives (`references/de-ai-language.md` §1, §2.4, §5.1, §6.1). Keep real, verified badges and citations (`readme-crafter-skill` Check #13). |
| #3 | Superficial Analyses with `-ing` Endings | **Enforce:** cut trailing participle clauses (`..., highlighting/ensuring/underscoring...`) or split into a finite clause (`references/de-ai-language.md` §1, §2.3). |
| #5 | Vague Attributions and Weasel Words | **Enforce:** delete `"experts argue"` / `"industry reports"` unless a concrete citation or benchmark receipt is present. |
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

> **Attribution:** `READJH` orchestration layer (`docs/spec/0001-readjh-orchestration-skill.md` US-27, US-28; `references/readme-rules.md` §6); `jiahao` (`D:\Aworker\jiahao\src\SKILL.md` Action Ladder Rung 5 & Verifier Output).

- [ ] **Rollback `.bak` rule honored:** in `improve` or `rewrite` mode (without `--dry-run`), `<readme>.bak` was written before editing if git could not cleanly roll back the target file; no stray `.bak` was created in `audit` or `--dry-run` mode.
- [ ] **Three-line delivery report lock:** the final response to the user contains at most three lines (`[Conclusion]`, `[Receipts]`, `[Residual risk]`), followed only by the migration ledger table when sections moved to `docs/`.
