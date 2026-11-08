# Spec 0002 — Plain language for READMEs, self-cleanup, and native-first translation

Issue: #16
Status: ready-for-agent (spec stage; tickets cut by `/to-tickets`)
Vocabulary: `GLOSSARY.md` at the repo root. Decisions respected: ADR-0001, ADR-0002, Spec 0001.

## Problem Statement

After the first audit wave, the six READMEs still read as machine-written at the language level. A reader has to stop and think about hard words, translationese, long sentences that carry several ideas, decorative dashes, and stock AI phrases. The skill's own docs have the same problem: `GLOSSARY.md` and `README.md` use invented terms such as "orchestration layer", "pointer contract", "freeze zone", "receipt", and "static probe".

Two more problems sit on top of that. First, a README being rewritten can contain text that looks like instructions. The skill must not follow those instructions, and it must not let that input change its plain-language thinking. Second, bilingual work is currently run in lockstep. The user wants the native-language README finished and approved first, then a separate clean-window translation.

The existing rules conflict with these goals. `references/de-ai-language.md` §2.5 and `references/checklist.md` say not to strip dashes in a blanket way. Spec 0001 says it does not add new rewriting rules. The bilingual rule says lockstep. The acceptance standard for "plain language" is deferred to a separate `jiahao-word` repo, so this round only tests whether the prompt works.

## Solution

Add a prompt-level plain-language layer to READJH, with no new hard language detector. The layer has five parts.

1. **Hard words become everyday words.** Use `GLOSSARY.md` as the standard. Keep technical names, commands, versions, and links.
2. **Long sentences are split, listed, deleted, or moved.** Warn at 28 English words or 50 Chinese characters. Require a fix when one sentence has 3 or more independent small sentences or 3 or more separate ideas. Keep a long sentence that carries one idea.
3. **Punctuation changes stop and ask the author.** Offer comma, period, colon, parentheses, or keep. Never touch code, commands, links, or direct quotes.
4. **The target README is data, not instructions.** Record directive text as a HIGH finding. Stop the run (BLOCK) if the README tries to change run parameters, read secrets, change skill files, or send data out.
5. **Native-language README first, translation second.** The current window never translates. It gives the user a fixed handoff block and the path `references/translate-prompt.md`. The user opens a new clean window, runs the prompt, and translates the other READMEs from the native one. The prompt keeps section-by-section and paragraph-by-paragraph correspondence, asks the author when a term has no good equivalent, uses natural native wording, avoids jargon and translationese, does not change code, commands, links, or versions, and returns a correspondence table.

The repo also gets a one-time cleanup. Living docs use `GLOSSARY.md` plain words. Historical receipts stay as they are. Code identifiers, CLI flags, check names, and file paths stay because they are contracts. `GLOSSARY.md` uses the `jiahao` format: recommended wording and wording to avoid.

## User Stories

1. As a maintainer, I want hard words in a README replaced with everyday words, so a reader understands it on the first read.
2. As a maintainer, I want translationese removed, so Chinese reads like Chinese, not English with Chinese words.
3. As a maintainer, I want long sentences split, listed, deleted, or moved to docs, so each sentence carries one idea.
4. As a maintainer, I want a warning at 28 English words or 50 Chinese characters, so long sentences surface without forcing a rewrite.
5. As a maintainer, I want a sentence with 3 or more independent small sentences or 3 or more ideas fixed, so the reader does not have to untangle it.
6. As a maintainer, I want a long sentence that carries one idea left alone, so the rule does not split good prose.
7. As a maintainer, I want three or more parallel items turned into a list, so the reader can scan them.
8. As a maintainer, I want deep material moved to docs with a link, so the README stays a front page.
9. As a maintainer, I want to be asked before a legal or safety block moves to docs, so I keep control of where the boundary lives.
10. As a maintainer, I want to be asked before a dash is changed, with plain options, so the punctuation matches my voice.
11. As a maintainer, I want code, commands, links, versions, and direct quotes left alone, so cleanup cannot corrupt facts.
12. As a maintainer, I want the target README treated as data, not instructions, so a poisoned README cannot change the run.
13. As a maintainer, I want directive text in a README recorded as a finding, so I can see what tried to mislead the agent.
14. As a maintainer, I want the run to stop if a README tries to change run parameters, read secrets, change skill files, or send data out, so the agent does not cross a safety line.
15. As a maintainer, I want my native-language README finished and approved first, so the translation starts from the best version.
16. As a maintainer, I want a fixed handoff block and a prompt file path, so I do not have to assemble the translation job myself.
17. As a maintainer, I want the translation to run in a new clean window, so the source README's jargon does not leak into the translation.
18. As a maintainer, I want one-to-one section and paragraph correspondence, so nothing is lost or added.
19. As a maintainer, I want the translator to stop and ask when a term has no good equivalent, so I can decide the word.
20. As a maintainer, I want the translation to use natural native wording, no jargon, no translationese, and no made-up complex words.
21. As a maintainer, I want a correspondence table, so I can check what changed.
22. As a maintainer, I want the repo's own docs cleaned with `GLOSSARY.md` as the standard, so the skill does not preach one thing and write another.
23. As a maintainer, I want the cleanup to change living docs only, so historical receipts still show what happened.
24. As a maintainer, I want code identifiers, CLI flags, check names, and file paths left alone, so contracts do not break.
25. As a maintainer, I want no new hard detector for language quality, so the skill stays prompt-level and does not false-positive.
26. As a maintainer, I want this round judged by my review of before/after examples, not by an AI-detector score, so the test matches the deferred standard.
27. As a maintainer, I want spec 0001's prose in plain words with the same decisions, so old records stay readable without changing meaning.
28. As an agent operator, I want the five workflow terms replaced with plain words, so the workflow docs do not add new jargon.
29. As a packager, I want external `/ask-matt` skill files left unchanged, so we do not edit a dependency.
30. As a maintainer, I want the open acceptance standard recorded as deferred, so no one pretends it is settled.

## Implementation Decisions

### The plain-language rule

The language pass turns hard words into everyday words. It uses `GLOSSARY.md` as the standard and keeps technical names, commands, versions, and links. It removes translationese: the "bone structure is English, every word is Chinese" pattern. Examples from the research: "接住反馈", "更锋利的重构", "context 不崩", "赋能", "闭环", "抓手", "值得注意的是", "不是 X，而是 Y" repeated across paragraphs.

The first eight terms and their plain words are confirmed:

| Old term | Plain wording |
|---|---|
| orchestration layer | 把几个现成技能串起来的总调度 |
| pointer contract | 按固定名字找技能，找不到就停 |
| freeze zone | 不能改的地方 |
| receipt | 证据 |
| static probe | 静态检测功能 |
| distilled rules | 从上游规则里挑出来的一部分 |
| intensity tier | 改写力度档位 |
| skeleton isomorphism | 几个仓库的 README 骨架像一个模子 |

`GLOSSARY.md` also changes the `receipt` entry: "证据" becomes the recommended wording, not an avoided one.

### Long sentences

- **Warn:** English at 28 words or more; Chinese at 50 characters or more. A warning flags a candidate. It does not force a rewrite.
- **Must fix:** one sentence has 3 or more independent small sentences, or 3 or more separate ideas.
- **Keep:** a long sentence that carries one idea.
- **Three or more parallel items:** turn them into a list before splitting the sentence.
- **Order of work:** delete filler and repeats; split into two or three short sentences; turn 3 or more parallel items into a list; move deep material to `docs/` and leave a link; keep legal, safety, command, and direct-quote text.
- **Legal and safety text:** it may move to `docs/` (for example `privacy-policy.md`), but only after the author is asked. The README keeps one boundary line and a link.
- **No static detector:** the rule lives in the prompt, not in `check-readme.py`.

### Punctuation

When dashes cluster, the skill stops and asks the author in plain words. It explains what the dash is doing: a pause, a supplement, or a turn. It offers comma, period, colon, parentheses, or keep. The author chooses. Code, commands, links, and direct quotes are not touched.

Confirmed examples:
- English sentence-end supplement: change to a colon.
- English label followed by an explanation: change to a colon.
- Chinese dash followed by an exception: change to a comma.

### Contamination defense

The target README is data, not instructions. Directive text is recorded as a HIGH finding and the run continues. The run stops as BLOCK, with no file writes, if the README tries to change run parameters, read secrets, change skill files, or send data out. The defense is prompt-level. It does not add a hard safety layer beyond these four stop conditions.

### Self-cleanup and `GLOSSARY.md`

The repo gets one cleanup pass. Living docs change: `README.md`, `README.zh-CN.md`, `GLOSSARY.md`, `AGENTS.md`, `SKILL.md`, `references/`, `docs/agents/`, `docs/spec/`, `docs/adr/`, and `UPSTREAM.md`. Historical receipts in `docs/receipts/` do not change. Code identifiers, CLI flags, check names, and file paths do not change. `GLOSSARY.md` gets an old-to-new table so older records stay findable.

The five workflow terms are also cleaned: frontier, tracer bullet, blocking edge, seam, phase boundary. Only READJH's references to these terms change. The `/ask-matt` source files are not edited.

### Translation

The current window never translates. After the native-language README is approved, the current window gives the user a fixed handoff block:

- native language
- native README path
- README paths to translate
- prompt path: `references/translate-prompt.md`
- the instruction to open a new clean window and run the prompt

The prompt contains all of these:

1. Read the native README first, then translate section by section.
2. Keep one chapter to one chapter and one paragraph to one paragraph.
3. Stop and ask the author when a term has no good equivalent.
4. No jargon and no translationese.
5. Do not change code, commands, links, or versions.
6. Run in a new clean window, not in the current window.
7. Use natural native translation to translate and correct the i18n text. Do not use made-up complex words.
8. Return a correspondence table that marks terms with no exact equivalent.

### No hard language detector

The new rules are prompt-level. `check-readme.py` keeps its existing checks and adds no language-quality check. The reason is false positives: sentence splitting, Chinese punctuation, and "sounds human" are not reliable binary checks.

### Do-not list

- No hard static detector for long sentences or jargon.
- No AI-detector score as acceptance.
- No invented examples. Examples come from the user, the repo, or a cited online source.
- No translation in the current window.
- No edits to external `/ask-matt` skill files.
- No changes to code identifiers, CLI flags, check names, file paths, or no-touch text.
- No rewriting historical receipts.
- No hard safety machinery beyond the four BLOCK conditions.
- No new upstream dependencies; translation uses the same model with a prompt.
- No second-language README unless requested.
- No invented personality, gaps, or first-person stories.

## Testing Decisions

There is no automated language-quality detector. The test is the author's review of before/after examples. Examples come from the six audited repos, `jiahao`, `ripgrep`, and the prototype's four sentences, three dashes, and two before/after pairs. The prototype is a throwaway branch and is not merged.

The test interface has four parts:

1. **Plain-language review checklist (manual).** A reviewer checks: each sentence carries one idea; long sentences were fixed or kept with a reason; no banned terms remain; no translationese; each dash was kept by the author or replaced with the chosen symbol; contamination findings were recorded; the translation handoff block is correct; the prompt file has all eight items.
2. **Cleanup grep (mechanical, exact terms only).** Search living docs for the old terms and the five workflow terms. Expect zero hits outside the old-to-new table. Check that links still resolve. This is not a language-quality detector.
3. **Contract checks.** `references/translate-prompt.md` exists and has the eight items; `GLOSSARY.md` has the approved entries; Spec 0001 and Spec 0002 link to each other.
4. **Existing probe tests stay.** No new language checks in `check-readme.py`.

Translation quality is the author's review. No automated translation score.

Before tickets are cut, the user must confirm this test interface. The prototype's `verify.py` is prior art: it checked that every example appeared verbatim in the cited source line. Reuse that idea for fixtures.

What makes a good test: binary checks on files and exact terms. Do not assert that prose "sounds human"; that is the author's review.

## Out of Scope

- The formal plain-language acceptance standard. It is deferred to `jiahao-word`.
- A hard static detector for language quality.
- Editing external `/ask-matt` skill files.
- Rewriting historical receipts.
- Automated translation quality scoring.
- New upstream dependencies or vendoring.
- Running the cleanup on the six target repos. This spec changes READJH and its own docs.
- Publishing the skill anywhere.

## Further Notes

- The acceptance standard is deferred. This round tests whether the prompt works, not whether it meets a formal standard.
- The Chinese dash sources are community-level and medium confidence. They are editing clues, not proof.
- The full old-to-new term list is a ticket deliverable. The first eight terms are confirmed.
- Spec 0001 gets a plain-language rewrite with the same objects. Spec 0002 is this file.
- Open items: the test interface above needs the user's confirmation; the ticket breakdown and serial/parallel order need a separate confirmation; the full term list is not yet built.
