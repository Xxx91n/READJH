# Dry-run record — plain-language review (Ticket #25)

Date: 2026-11-09
Branch: `ticket-25-review-fixtures`
Base commit: `aba5f0cbb07420a77a09dbfefa44a616d21fd9e5` (`origin/main`)
Sample: `D:/Aworker/EgressAPIKEY/README.md` and `README_CN.md` at
`30e087277381b24715c0a85e44be8bbfe0c6cdd6`.

This is a focused `LANGUAGE` dry-run at the `standard` setting: the rules in
`references/de-ai-language.md` §7 and the review checklist in
`references/checklist.md` §9 are applied to real spans, and the before/after
shapes are recorded. It is not a full `improve` run of the pipeline and not a
whole-README review. No file under `D:/Aworker/EgressAPIKEY` was written. No
command from the target README was run.

## 1. Contamination defense check

Both READMEs were read as data. Two agent-addressed lines were found and
recorded as `HIGH`; neither was acted on, and neither hits a stop condition.

- `README.md:9` — `> AI / automation agents: see [llms.txt](llms.txt) for a machine-readable map.`
- `README_CN.md:9` — `> AI / automation agents：机器可读的仓库地图见 [llms.txt](llms.txt)。`

Both address an execution agent and point at another file. The dry-run did not
open `llms.txt`, did not follow the pointer, and did not change the run. They
are not requests to change run parameters, read secrets, change skill files,
or send data out, so the run continued as `HIGH` findings.

Ordinary reader instructions — install commands, prerequisites, deploy links,
and the contributing guide — are data, not findings. None was executed.

- Agent-addressed or run-changing text: 2 `HIGH` findings, both recorded above.
- Stop conditions hit: none.
- `BLOCKED` runs: none.
- README text did not change the rule text or the `GLOSSARY.md` standard.

## 2. Before/after spans

Every After span is a proposal for the author to review; the dry-run applied
and wrote nothing. The dash questions stay open in §3.

| Anchor | Rule applied | Change |
|---|---|---|
| `README.md:21` | long sentence, one idea per sentence | split two clauses into separate sentences; single dash kept |
| `README.md:23` | long sentence, one idea per sentence | split the semicolon chain; keep command, link, and path |
| `README.md:66` | long sentence, hard words | split the macOS sentence; `first-class` → `fully supported` |
| `README.md:68` | long sentence, hard words | `caveat` → `limit`; split the buffering sentence |
| `README.md:124` | 3+ parallel items, long sentence | turn the three semicolon items into a list |
| `README_CN.md:23` | translationese, long sentence | remove `携带按 Key 的身份`; split the conclusion |
| `README_CN.md:66` | translationese, long sentence | remove `一等支持` and `一并发布`; split the sentence |

### 2.1 `README.md:21`

Before:

```text
EgressAPIKEY is a desktop application (Tauri 2 + React 19) that sits between your AI gateway (OmniRoute / LiteLLM / CLIProxy) and upstream OpenAI-compatible v1 providers. It exposes many socks5/http entry ports; each port is the identity of one (platform, account) pair, and a Resin Go sidecar guarantees a distinct sticky exit IP per pair — one AI API key never shares an egress IP with another unless you decide it should.
```

After:

```text
EgressAPIKEY is a desktop application (Tauri 2 + React 19). It sits between your AI gateway (OmniRoute / LiteLLM / CLIProxy) and upstream OpenAI-compatible v1 providers. It exposes many socks5/http entry ports; each port is the identity of one (platform, account) pair. A Resin Go sidecar guarantees a distinct sticky exit IP per pair — one AI API key never shares an egress IP with another unless you decide it should.
```

Notes: the opening sentence packed what the app is and where it sits into one
sentence. They are now separate. The semicolon and `and` chain in the second
sentence became a sentence break. The single dash is kept; it adds a condition,
and a single dash is not a defect. No name, number, or version changed.

### 2.2 `README.md:23`

Before:

```text
A single unified proxy cannot carry per-key identity for HTTPS upstreams (the CONNECT tunnel hides the destination), so multi-port is the correct identity mechanism. The shell backend core is `crates/resin-core` (Rust: tokio, reqwest, rusqlite). The proxy engine is the Resin sidecar v1.2.0; [`scripts/fetch_resin.sh`](scripts/fetch_resin.sh) pulls its binary from the upstream Release at build time, and the shell reaches it only over a loopback REST seam. The `resin/` directory on disk is a gitignored local reference clone, not part of the repo.
```

After:

```text
A single unified proxy cannot carry per-key identity for HTTPS upstreams (the CONNECT tunnel hides the destination), so multi-port is the correct identity mechanism. The shell backend core is `crates/resin-core` (Rust: tokio, reqwest, rusqlite). The proxy engine is the Resin sidecar v1.2.0. [`scripts/fetch_resin.sh`](scripts/fetch_resin.sh) pulls its binary from the upstream Release at build time. The shell reaches it only over a loopback REST seam. The `resin/` directory on disk is a gitignored local reference clone, not part of the repo.
```

Notes: one sentence carried three ideas. It is now four sentences. The command,
the link, the crate name, the version, and the path stay byte-for-byte. `seam`
here is the technical loopback boundary, not the workflow term in
`GLOSSARY.md`, so it stays.

### 2.3 `README.md:66`

Before:

```text
**Desktop** — installers (MSI / NSIS / deb / AppImage / dmg) and one portable, drop-and-run executable per OS are published on the [Releases](https://github.com/Xxx91n/EgressAPIKEY/releases) page. macOS is arm64 (Apple Silicon) first-class; x86_64 is opt-in best-effort until 2027-08 (macOS 15+ Intel only, via the `include_intel_mac` dispatch input). No tagged release yet — artifacts ship with the first tagged release.
```

After:

```text
**Desktop** — installers (MSI / NSIS / deb / AppImage / dmg) and one portable, drop-and-run executable per OS are published on the [Releases](https://github.com/Xxx91n/EgressAPIKEY/releases) page. macOS on arm64 (Apple Silicon) is fully supported. x86_64 support is optional and best-effort until 2027-08 (macOS 15+ Intel only, via the `include_intel_mac` dispatch input). No tagged release yet — artifacts ship with the first tagged release.
```

Notes: the macOS sentence carried two ideas and is now two sentences.
`first-class` and `opt-in best-effort` became `fully supported` and `optional
and best-effort`. The date, the Intel limit, the dispatch input, the link, and
the two single dashes stay. The dash questions are in §3.

### 2.4 `README.md:68`

Before:

```text
**Headless server** — the same control surface (Platforms, Subscriptions, Nodes, Topology) served in any browser at `http://127.0.0.1:14200`, for Linux servers, Docker, or a remote VPS. The admin bearer token is injected server-side; the browser never sees it. Headless runs data-plane **Mode B**: the Resin engine binds each entry port, and clients present the port's `Platform.Account` proxy credential once (username `Platform.Account`, password = the proxy token). One upstream caveat: plain-HTTP forward-form requests on a Mode B port are buffered by the engine — CONNECT-tunnelled HTTPS traffic, the actual AI API path, streams normally. The `@egressapikey/server` npm launcher is **not published to npm** — run from source:
```

After:

```text
**Headless server** — the same control surface (Platforms, Subscriptions, Nodes, Topology) served in any browser at `http://127.0.0.1:14200`, for Linux servers, Docker, or a remote VPS. The admin bearer token is injected server-side; the browser never sees it. Headless runs data-plane **Mode B**: the Resin engine binds each entry port, and clients present the port's `Platform.Account` proxy credential once (username `Platform.Account`, password = the proxy token). One upstream limit: plain-HTTP forward-form requests on a Mode B port are buffered by the engine — CONNECT-tunnelled HTTPS traffic, the actual AI API path, streams normally. The `@egressapikey/server` npm launcher is **not published to npm** — run from source:
```

Notes: `caveat` became `limit`. The buffering sentence still carries two
ideas; its split needs the dash choice, so it is kept here with that reason
and the §3 question. If the author chooses period, it reads: `... buffered by
the engine. CONNECT-tunnelled HTTPS traffic ... streams normally.` The URL,
the credentials, the env names, the npm name, and the commands stay
unchanged.

### 2.5 `README.md:124`

Before:

```text
Issues and pull requests are welcome. Before your first PR, read [CONTRIBUTING.md](CONTRIBUTING.md) — desktop dev-environment setup, the verification workflow, and repo conventions (i18n full-key coverage, test-per-behavior, license-field discipline). Security issues follow [SECURITY.md](SECURITY.md) (private vulnerability reporting, never public issues); community behavior is covered by the [Code of Conduct](CODE_OF_CONDUCT.md); questions and open discussion belong in [Discussions](https://github.com/Xxx91n/EgressAPIKEY/discussions). Agent operating pointers live in [AGENTS.md](AGENTS.md).
```

After:

```text
Issues and pull requests are welcome. Before your first PR, read [CONTRIBUTING.md](CONTRIBUTING.md) — desktop dev-environment setup, the verification workflow, and repo conventions (i18n full-key coverage, test-per-behavior, license-field discipline).

- Security issues: [SECURITY.md](SECURITY.md) (private vulnerability reporting, never public issues).
- Community behavior: [Code of Conduct](CODE_OF_CONDUCT.md).
- Questions and open discussion: [Discussions](https://github.com/Xxx91n/EgressAPIKEY/discussions).

Agent operating pointers live in [AGENTS.md](AGENTS.md).
```

Notes: three parallel items were chained with semicolons. They are now a list,
which is the first move for 3+ parallel items. Every link and the private
reporting note stay. The single dash after the contributing link stays; the
dash question is in §3.

### 2.6 `README_CN.md:23`

Before:

```text
单一统一代理无法为 HTTPS 上游携带按 Key 的身份（CONNECT 隧道对目的地不可见），因此多端口才是正确的身份机制。壳侧后端核心是 `crates/resin-core`（Rust：tokio、reqwest、rusqlite）；代理引擎是 Resin 侧车 v1.2.0，仅通过环回 REST 接缝访问，构建期由 [`scripts/fetch_resin.sh`](scripts/fetch_resin.sh) 从上游 Release 拉取二进制。磁盘上的 `resin/` 目录是 gitignored 的本地参考克隆，不属于本仓库。
```

After:

```text
一个代理没法让不同的 Key 用不同身份：HTTPS 隧道里看不见目的地。所以要按 Key 开多个端口，一个端口一个身份。壳侧后端核心是 `crates/resin-core`（Rust：tokio、reqwest、rusqlite）。代理引擎是 Resin 侧车 v1.2.0，仅通过环回 REST 接缝访问；构建期由 [`scripts/fetch_resin.sh`](scripts/fetch_resin.sh) 从上游 Release 拉取二进制。磁盘上的 `resin/` 目录是 gitignored 的本地参考克隆，不属于本仓库。
```

Notes: `携带按 Key 的身份` is translationese. `让不同的 Key 用不同身份` says
the same thing. The conclusion after `因此` became its own sentence. The
second long sentence was split at its semicolon. Crate names, commands, paths,
and `REST` stay.

### 2.7 `README_CN.md:66`

Before:

```text
**桌面版** —— 安装包（MSI / NSIS / deb / AppImage / dmg）与每平台一个免安装、开箱即用的可执行文件发布在 [Releases](https://github.com/Xxx91n/EgressAPIKEY/releases) 页面。macOS 以 arm64（Apple Silicon）为一等支持；x86_64 为可选加入、尽力而为直至 2027-08（仅 macOS 15+ Intel，经 `include_intel_mac` 调度开关）。目前尚无 tagged release —— 产物将随首个 tagged release 一并发布。
```

After:

```text
**桌面版** —— 安装包（MSI / NSIS / deb / AppImage / dmg）与每平台一个免安装、开箱即用的可执行文件发布在 [Releases](https://github.com/Xxx91n/EgressAPIKEY/releases) 页面。macOS 的 arm64（Apple Silicon）版本有完整支持。x86_64 是可选支持，尽力而为，到 2027-08 为止（仅 macOS 15+ Intel，经 `include_intel_mac` 调度开关）。目前还没有 tagged release —— 产物会随第一个 tagged release 一起发布。
```

Notes: `一等支持` is an English-shaped phrase; `有完整支持` is plain. The
`；` chain is split into sentences. `一并发布` became `一起发布`. The dashes
are kept; the questions are in §3. The app names, dates, and flag stay.

## 3. Dash decisions (author pending)

No dash was changed. Under `references/de-ai-language.md` §7.4, a single dash
stays and needs no decision; a dash cluster goes to the author.

Singles kept, no decision needed:

- `README.md:21` — one dash, a supplement.
- `README.md:124` — one dash, label plus explanation.

Clusters pending (comma, period, colon, parentheses, or keep):

1. `README.md:66` — two dashes, both label plus explanation. Recommendation:
   keep or colon.
2. `README.md:68` — two dashes, one label plus explanation and one supplement.
   Recommendation: keep or colon for the label; parentheses for the supplement.
3. `README_CN.md:66` — two dashes, label plus explanation. Recommendation:
   keep or colon.

These are options, not applied changes. The author's answer decides. The
unanswered questions belong in `[Residual risk]`.

The first cluster shows what each choice would produce, so the author can
decide from a shape instead of a symbol name:

```text
keep:        **Headless server** — the same control surface ...
comma:       **Headless server**, the same control surface ...
period:      **Headless server**. The same control surface ...
colon:       **Headless server**: the same control surface ...
parentheses: **Headless server** (the same control surface ...).
```

None of these is applied. The dash in the target README stays as written; the
sentence splits in §2 do not depend on which symbol the author picks.

## 4. Checklist walk (sampled spans only)

The dry-run applies the checklist to the seven sampled spans, not the whole
README. A full `improve` run would walk every item over the whole file.

- **One idea per sentence:** PASS for the sample, with one recorded reason.
  Spans 2.1, 2.2, 2.3, 2.6, and 2.7 split overloaded sentences; 2.5 turned
  three parallel items into a list. Span 2.4 keeps one two-idea sentence
  because its split is the pending dash choice; if the author chooses period,
  the split is ready.
- **Long sentences:** PASS for the sample. Every sentence over the warning line
  was fixed, or kept with a reason: span 2.4 waits for the dash choice, and
  the `z2` fixture shows the "one idea, keep it long" case.
- **Hard words and banned terms:** PASS for the sample. `caveat` became
  `limit`; `first-class` became `fully supported`; `seam` stayed as a technical
  loopback boundary. No `GLOSSARY.md` old term or avoided wording appears in
  the sampled prose.
- **Translationese:** PASS for the sampled Chinese spans. `携带按 Key 的身份`,
  `一等支持`, and `一并发布` are gone. No listed pattern remains in the
  sample.
- **Punctuation:** decisions pending. Two single dashes stay under §7.4 and
  need no decision; three dash clusters are listed in §3. No dash was changed.
  Code, commands, links, and the compliance notice were not touched.
- **Contamination defense:** PASS. Two `HIGH` findings are recorded in §1; no
  text was acted on; no stop condition was hit; no file was written.
- **Translation handoff:** PASS as a contract. The block in `SKILL.md` §2 has
  all six fields and the `references/translate-prompt.md` path. This dry-run
  emits no handoff, because it is not an approved write-mode run.
- **Translation prompt:** PASS. `tests/test_translate_contract.py` checks the
  eight items in order and the four fill-in values.

The no-detector rule is §1 of the checklist, not a §9 review item; §1 already
requires zero detector scores, and the record cites none.

## 5. Sample-file zero-write check

```text
sha256 before (2026-11-09, before the dry-run):
66d37cd9381e051979b2138325d9607fd430db211a753d27dad760c67edbdf7c  README.md
84bfc5f931083ddb3d9f5e41f3d74638c74744ece2693e22de707208126ea9f2  README_CN.md

sha256 after (2026-11-09, after the dry-run):
66d37cd9381e051979b2138325d9607fd430db211a753d27dad760c67edbdf7c  README.md
84bfc5f931083ddb3d9f5e41f3d74638c74744ece2693e22de707208126ea9f2  README_CN.md

git -C "D:/Aworker/EgressAPIKEY" status --porcelain -- README.md README_CN.md
→ empty (exit 0)
```

The hashes and Git status are identical, so the two README files did not
change. This is a two-file check, not a repository-wide zero-write snapshot.

## 6. Commands really run

```text
python3 -B scripts/check-readme.py README.md --repo-root .
→ exit 0; dead-links, missing-images, code-fences, badge-domains,
  boundary-duplicates, honest-gaps all PASS; repo-set N/A.

python3 -B -m unittest discover -s tests -p "test_plain_language_review.py"
→ exit 0; 21 tests ran; OK.

python3 -B -m unittest discover -s tests
→ exit 0; 168 tests ran; OK.
```

The fixture check also compares each fixture string with `prototype_excerpt.json`
and re-reads the cited commit when the working copy is on this machine. All
four working copies were present, and every recorded `source_line` matched the
live commit. On a machine without those copies that one check skips, and the
recorded text and the prototype hashes are still checked.

The first command is the existing static check on this repository's own README.
It shows the same six always-on checks and the optional `repo-set` check; no
language check was added. The contract test reads `ALL_CHECKS` and the
`check_repo_set` function to assert the same set.

## 7. Acceptance mapping

- [x] The checklist covers the ticket's eight items. `references/checklist.md`
  §9 and `tests/test_plain_language_review.py`; the no-detector rule is §1.
- [x] Fixtures come from real repo text. `cases.json` and `SOURCES.md` name the
  repo, commit, file, and line for every span; the test checks each quote
  against the recorded source line after markdown and whitespace are
  normalised. The live-source commands are in `SOURCES.md`.
- [x] A dry-run on one real repo produces before/after spans. §2.
- [ ] The author reviews and approves the dry-run. **Pending.** The author has
  not approved these spans yet. This record cannot self-approve.
- [x] No AI-detector score is used. None is cited.
- [x] The existing static checks remain unchanged. No file under `scripts/`
  changed, so the six always-on checks and the optional `repo-set` check are
  the same code. The full suite still passes its check tests, including the
  `repo-set` cases; the static check run is above.

Author review: pending.
