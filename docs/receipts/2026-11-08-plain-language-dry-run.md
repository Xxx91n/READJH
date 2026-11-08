# Receipt — plain-language rule dry-run (Ticket #17)

Date: 2026-11-08
Branch: `ticket-17-plain-language-rules`
Base commit: `2547836f65791a4f3459c62dd23fb85dab753fb4` (`origin/main`)
Sample: `D:\Aworker\6F\README.md` and `D:\Aworker\6F\README.zh-CN.md` at
`dbe463869d89e788199dd6879ff5ee17dd266bef`.

This is a focused `LANGUAGE` dry-run at the `standard` tier: the new rule
text in `references/de-ai-language.md` §7 is applied to real spans, and the
before/after shapes are recorded. The sample has no verified author voice, so
`lite` does not apply. It is not a full `improve --dry-run` run of
the pipeline: the ticket tests whether the rule text produces plain before/after
spans, not the scanner or upstream executor. No file under `D:\Aworker\6F` was
written by this dry-run. The hashes below cover the two README files, not a
repository-wide snapshot.

## 1. Contamination defense check

Both READMEs were read as data. No text asks an agent to change run
parameters, read secrets or credentials, change skill files, or send data out.
`README.md:32` says "do not read this page as a finished product"; that is a
reader-facing product boundary, not an agent instruction, and it is not one of
the four stop conditions.

- Agent-addressed or run-changing text: none. `HIGH` findings: 0.
- Stop conditions hit: none.
- The rule text and `GLOSSARY.md` standard were not changed by anything in the
  target README.

## 2. Before/after spans

The table is the summary; the verbatim spans follow. Every After span is a
proposal for the author to review; the dry-run applies and writes nothing.

| Anchor | Rule applied | Change |
|---|---|---|
| `README.md:18` | hard words, long sentence | split into short sentences; keep the two single dashes |
| `README.md:125` | hard word / metaphor | `the moat` → `built in this repository` |
| `README.md:153` | long sentence, 3+ parallel items | turn the five `+` items into a bullet list |
| `README.md:171` | long sentence | split at the semicolon; keep the single dash |
| `README.zh-CN.md:22` | translationese, long sentence | remove `护城河与黏合剂`; split; keep the single `——` |
| `README.zh-CN.md:52` | translationese, long sentence | `决策本体非装饰` → `设计的一部分，不是装饰`; split |
| `README.zh-CN.md:104` | hard word | `消费` → `使用`; keep the single `——` |
| `README.zh-CN.md:119` | translationese, long sentence | `逃生` → `才放进仓库`; split |

### 2.1 `README.md:18`

Before:

```text
6F is a macro + micro engineering-content audit product for git-healthy repositories, distributed as a **Claude Code Agent Plugin** ([`engine/`](engine/)). Evidence collection comes largely from upstream components; the adjudication protocol, fact-table schema, acceptance gates, and verifiable receipts are this project's own work. Five audit scales — Macro-A cross-repo strategy, Macro-B repo quadrant, Macro-C evolution archaeology, Micro-A PR diff, Micro-B file level — share one fact base and one adjudication layer, and differ in triggers and report slices.
```

After:

```text
6F audits engineering content at macro and micro scale in repositories with a healthy git history. It ships as a **Claude Code Agent Plugin** ([`engine/`](engine/)). Most evidence comes from upstream components. The adjudication protocol, fact-table schema, acceptance gates, and verifiable receipts are built in this repository. Five audit scales — Macro-A cross-repo strategy, Macro-B repo quadrant, Macro-C evolution archaeology, Micro-A PR diff, Micro-B file level — share one fact base and one adjudication layer. They differ in triggers and report slices.
```

Notes: the three ideas in the original now stand as separate sentences. The
five-scale parenthetical is already a parallel list; it is kept inline because
the two dashes are single, not a cluster. No fact, link, or command changed.

### 2.2 `README.md:125`

Before:

```text
| **Ours (the moat)** | federated adjudication protocol (verdict-gate) · DuckDB fact-table schema (append-only + cross-scale correlation keys) · three-layer acceptance gates (A formal / B pre-declared criteria / C human ruling) · dual-anchored receipts · pre-declared criteria discipline (2 positive controls + 3 real criteria + 1 negative control) |
```

After:

```text
| **Ours (built in this repository)** | federated adjudication protocol (verdict-gate) · DuckDB fact-table schema (append-only + cross-scale correlation keys) · three-layer acceptance gates (A formal / B pre-declared criteria / C human ruling) · dual-anchored receipts · pre-declared criteria discipline (2 positive controls + 3 real criteria + 1 negative control) |
```

Notes: `the moat` is a metaphor for "our own work". It has no `GLOSSARY.md`
entry, so this span is a proposed plain wording for the author to approve, not
a rule-mandated replacement. The table's other row says "Borrowed (upstream)",
so the contrast stays clear. No table cell, name, or version changed.

### 2.3 `README.md:153`

Before:

```text
External repositories join via URL opt-in (D-013 local-first + URL opt-in): clone into an isolated cache (sha256 key) + full-depth verification + shallow clones rejected + remote-config execution disabled + local git credential chain reuse.
```

After:

```text
External repositories join only when the user opts in by URL (D-013: local path first, URL opt-in):
- clone into an isolated cache keyed by sha256;
- verify full depth and reject shallow clones;
- disable remote-config execution;
- reuse the local git credential chain.
```

Notes: the five `+` items were parallel actions in one sentence. They are now a
list; the colon carries the lead-in, so no sentence is added. `D-013` and
`sha256` stay as written, and "local path first" restates the original
"local-first".

### 2.4 `README.md:171`

Before:

```text
- Opt-in public example: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) (onboarded here: a Macro-B one-shot on 2026-09-16 produced 1424 facts and an `unsupported` verdict faithfully recorded — TC-2 attributed to an ADR dash+bold form detector gap, registered as a coverage hole; run record in execution ledger A-045).
```

After:

```text
- Opt-in public example: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core). A Macro-B one-shot on 2026-09-16 produced 1424 facts and an `unsupported` verdict — TC-2 came from an ADR dash+bold form the detector missed. The gap is registered as a coverage hole. The run record is in execution ledger A-045.
```

Notes: split at the semicolon. The single dash stays. `1424`, the date,
`unsupported`, `TC-2`, the ADR phrase, and `A-045` are unchanged.

### 2.5 `README.zh-CN.md:22`

Before:

```text
面向 git 记录健全仓库的工程内容审计产品——**Claude Code Agent Plugin**（分发形态见 [`engine/`](engine/)）：证据采集大部分来自上游组合件，裁决协议、事实表 schema、验收闸门与可核验回执是本项目自研的护城河与黏合剂。5 档审计粒度（Macro-A 跨仓战略 / Macro-B 仓库级四象限 / Macro-C 演化考古 / Micro-A PR diff / Micro-B file level）共享同一事实底座与裁决层，差异在触发器与报告切片。
```

After:

```text
6F 是面向 git 记录健全仓库的工程内容审计产品——**Claude Code Agent Plugin**（分发形态见 [`engine/`](engine/)）。证据大多来自上游组合件。裁决协议、事实表 schema、验收闸门和可核验回执由本项目自己实现。5 档审计粒度（Macro-A 跨仓战略、Macro-B 仓库级四象限、Macro-C 演化考古、Micro-A PR diff、Micro-B file level）共用同一事实底座和裁决层，区别在触发条件和报告切片。
```

Notes: `护城河与黏合剂` was a metaphor; `由本项目自己实现` says the same thing
in plain words. The sentence is split after the colon. The single `——` stays.
The five scale names and `Micro-A PR diff` / `Micro-B file level` stay as
written.

### 2.6 `README.zh-CN.md:52`

Before:

```text
preview 标注诚实是决策本体非装饰：报告头/侧车 `preview_disclosure` 披露块（capability 标注＋校准范围＋结构性限制＋not_in_preview 清单）与上表为同一语义源；降级产出带 `⚠ unverified` 印记，未接证据域带「⚠ 数据未接」标注，合成 fixture 带「synthetic」印记且不冒充真实审计。
```

After:

```text
preview 标注是设计的一部分，不是装饰。报告头和侧车带 `preview_disclosure` 披露块，写明 capability 标注、校准范围、结构性限制和 not_in_preview 清单，与上表用同一套说法。降级产出带 `⚠ unverified` 印记，未接证据域带「⚠ 数据未接」标注，合成 fixture 带「synthetic」印记，不冒充真实审计。
```

Notes: `决策本体非装饰` is an abstract phrase; `设计的一部分，不是装饰` is
plain. `同一语义源` → `同一套说法`. The three mark types stay verbatim.

### 2.7 `README.zh-CN.md:104`

Before:

```text
分发层（CLI、skills 壳、MCP 面）消费自研核心——只追加 `audit_fact` DuckDB 事实表、`verdict-gate` 联邦裁决协议、双锚回执。证据只经适配器流入：上游原始语义不出适配层。
```

After:

```text
分发层（CLI、skills 壳、MCP 面）使用自研核心——只追加 `audit_fact` DuckDB 事实表、`verdict-gate` 联邦裁决协议和双锚回执。证据只经适配器流入：上游原始语义不出适配层。
```

Notes: `消费` → `使用` is a translationese judgement, not a `GLOSSARY.md`
entry. The single `——` stays. Identifiers and code spans stay unchanged.

### 2.8 `README.zh-CN.md:119`

Before:

```text
引入方式按适配器双轨制：适配器 + 外部 CLI/库为主线，库形态上游走包管理器 lockfile hash pinning，vendor 源码进仓仅在气隙分发或上游废弃两种情况逃生。
```

After:

```text
引入方式按适配器双轨制：适配器 + 外部 CLI/库是主线。库形态上游用包管理器 lockfile hash 固定版本。vendor 源码只有气隙分发或上游废弃时才放进仓库。
```

Notes: `pinning` → `固定版本`; `两种情况逃生` → `才放进仓库`. The technical
term `vendor` stays. No upstream name or lockfile path changed.

## 3. Punctuation questions (author decision pending)

No dash was changed. These clusters need the author's choice: comma, period,
colon, parentheses, or keep.

1. `README.md:20-27` — the six Highlights bullets each use `—` to introduce an
   explanation. Offer: keep (each bullet is a label + explanation), colon,
   comma, period, or parentheses.
2. `README.md:32` — two dashes in the preview NOTE paragraph. Offer: keep,
   comma, period, colon, or parentheses.
3. `README.zh-CN.md:22`, `README.zh-CN.md:104`, and
   `README.zh-CN.md:117` — the Chinese `——` dashes. Offer: keep, comma, period,
   colon, or parentheses.

The dry-run does not pick one. The author's answer decides.

## 4. Sample-file zero-write receipt

```text
sha256 before (2026-11-08, before reading spans):
b94ffb10b5ca8fe1feded944d28575052e384f5d2f0136ef25ec5d6c73c64f5d  README.md
4fa58c9296880d3fa64414fd4623ca2b2123ba389896e0976560b3f5b8db85d2  README.zh-CN.md

sha256 after (2026-11-08, after the dry-run):
b94ffb10b5ca8fe1feded944d28575052e384f5d2f0136ef25ec5d6c73c64f5d  README.md
4fa58c9296880d3fa64414fd4623ca2b2123ba389896e0976560b3f5b8db85d2  README.zh-CN.md

git -C D:\Aworker\6F status --porcelain -- README.md README.zh-CN.md
→ empty (exit 0)
```

The hashes and Git status are identical, so the two README files did not
change. This is a two-file check, not a repository-wide zero-write snapshot.

## 5. Acceptance mapping

- Plain-language rules in plain words: `SKILL.md` §2 and `LANGUAGE` Phase 4
  step 3; `references/de-ai-language.md` §7; `references/checklist.md` §9.
- Contamination-defense rule: `SKILL.md` §2, `TRUTH` Phase 2 step 1, and
  `references/readme-rules.md` §6.
- Dry-run with before/after spans: this receipt, §2.
- No AI-detector score: none used anywhere in this receipt or the rule text.
- Seven static checks unchanged; no new language-quality detector: no change
  under `scripts/` or `tests/`. The probe run on the README is the existing
  single-repository check set:
  `python -B scripts/check-readme.py README.md --repo-root .` → exit 0, six
  checks PASS, `repo-set` N/A.
- Author review: pending. The before/after spans in §2 are the review packet.
- Integration note: the word rule reads `GLOSSARY.md` at run time. Ticket #18
  supplies the old-to-new table and the confirmed plain-word list; until #18
  lands, the old GLOSSARY is still the standard. The two tickets are parallel
  per Spec 0002.
- Dry-run scope: rule-level, not a full pipeline run. The scanner and upstream
  executor path is unchanged by this ticket.
- Tier scope: the pass is gated to `standard` to match the existing tier table;
  Spec 0002 does not name a tier. This is an interpretation, not a spec line.
- Parent spec file: `docs/spec/0002-plain-language-and-native-first-translation.md`
  is committed on local `main` (`d2b170f`) but absent from `origin/main` and this
  branch. The citations use GitHub issue #16; land the local-main spec commits
  with this branch.
