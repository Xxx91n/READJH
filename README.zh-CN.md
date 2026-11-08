# READJH

[English](README.md) | **简体中文**

READJH 管 README 写得准不准、读起来顺不顺。它按顺序把你已有的几个技能
串起来，跑 `audit`、`improve`、`rewrite` 三种任务。结果里的每条说法，
都要拿仓库里查得到的东西核对。

仓库根目录就是技能本体：`SKILL.md`、`references/`（规则）、`scripts/`
（静态检测功能，只用标准库的 python3），加上下面「目录结构」里列的文件。
纯 markdown 加 python3，不用构建，也没有宿主适配层（ADR-0002）。

## 它做什么

各模式的阶段顺序：

- `audit`：`ROUTE → TRUTH → RESTRUCTURE → VERIFY`（只检查）
- `improve` / `rewrite`：`ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY`

- **ROUTE** 定下这次怎么跑：`audit` 只检查，`improve` 只改需要改的地方，
  `rewrite` 重写整份。每个模式都支持 `--dry-run`。
- **TRUTH** 把 README 里的每条说法对着仓库里查得到的东西核对：manifest、
  CI 配置、入口文件、扫描器输出。对不上的记成一条问题，不偷偷改掉；
  查不了的，删掉或者标出来。
- **RESTRUCTURE** 让 README 只当首页。`audit` 模式下，它找出哪些深层
  内容该放进 `docs/`，也找出反复给自己作证的话。它还会标出生成时留下
  的痕迹和一看就像机器写的句子。`improve` 和 `rewrite` 模式下，它把这些
  深层内容搬到 `docs/`，每搬一次都记下来。
- **LANGUAGE**（`improve` 和 `rewrite`）跑上游 `writing-humanize`，
  再加上从上游规则里挑出来、只适用 README 的那部分。改写时守两道线：
  有些字句一律不许碰，改写力度也有上限，免得润色改坏事实、磨平真正
  的文风。
- **VERIFY** 先跑静态检测功能，再过一遍人工检查清单，产出机器能核对的
  证据。交付报告最多三行：做了什么、证据、还剩哪些风险。

## 依赖

READJH 只负责把几个现成技能串起来，再补上它们没覆盖的 README 规则。
两个上游技能按固定名字在固定路径下查找。找不到就停下，告诉你怎么装。
不拿名字相近的技能顶上：

| 固定名字 | 上游仓库 | 做什么 |
|---|---|---|
| `readme-crafter-skill` | [linhai0872/readme-crafter-skill](https://github.com/linhai0872/readme-crafter-skill) | TRUTH/RESTRUCTURE：事实与结构 |
| `writing-humanize` | [risadams/ink-and-agency](https://github.com/risadams/ink-and-agency)（`skills/writing-humanize/`） | LANGUAGE：行文润色 |

另有四个上游只把一部分规则放进 `references/`，从不运行：

- `sepia`：中文校准、职业/文风检查
- `anti-defensive-writing`：英文，Kiterlin
- `academic-humanizer`：每条说法都要对得上证据
- `humanize-readme`：只收还能用的规则

完整的表、这些技能在机器上的实际位置、怎么装，以及对
`writing-humanize` 两处故意关掉的行为，见
[UPSTREAM.md](UPSTREAM.md)。致谢和许可证见 [NOTICE](NOTICE)。

## 安装

把你的 Agent Skills 宿主指向本仓库根目录；根目录就是技能本身。
再按 `UPSTREAM.md` 里的安装步骤，让这个技能要调用的两个
上游技能能在 `<skills-root>/<canonical-name>/SKILL.md` 找到。

## 快速上手

装好后按名字对仓库调用技能：

- `audit`：报出问题和优先级，不动任何文件；支持
  `--repo-set <manifest>`，一次看一组仓库，比对它们的 README 骨架
  像不像一个模子（`audit` 模式里，`--dry-run` 的要求默认就满足了）。
- `improve`：只改现有 README 里需要改的地方；git 回滚不了时留一个
  `.bak`。
- `rewrite`：README 修不动了，就整份重写。
- `--dry-run` 所有模式都能用：只给计划和证据，不写文件（不改文件、
  不搬 `docs/`、不建 `.bak`）。

## 目录结构

```
SKILL.md            # 技能本体（模型调用）：流程 + 约定
references/         # 几个技能怎么串起来的规则 + 从上游挑出来的补充规则
scripts/            # check-readme.py —— 静态检测功能，只用标准库的 python3
tests/              # 静态检测的 unittest 测试与 fixtures
UPSTREAM.md         # 依赖、技能按什么名字找、偏差记录
NOTICE              # 上游致谢与许可证
GLOSSARY.md         # 大白话用词标准 + 旧词到新词对照表
docs/spec/          # 规格文档
docs/adr/           # 架构决策记录
docs/agents/        # 给 agent 操作者的仓库维护说明
docs/receipts/      # 验收跑出来的证据
docs/tickets/       # 指向 GitHub issue 跟踪器
```

## 状态

还在早期开发。已知的局限：这个仓库还没有 CI，检查只能手动跑。
任务都记在 GitHub issue 上（见 `docs/agents/`）。
许可证：MIT，见 [LICENSE](LICENSE)。
