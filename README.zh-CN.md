# READJH

[English](README.md) | **简体中文**

READJH 是一个 README 治理编排技能。一个入口把上游技能串成 `audit`、
`improve`、`rewrite` 三种模式 —— 结果里的每条声明都要拿仓库里的真实
凭据核对。

仓库根目录就是技能本体：`SKILL.md`、`references/`（规则）、`scripts/`
（一个只用标准库的 python3 静态探针），以及下方 Layout 列出的骨架文件。
纯 markdown 加 python3 —— 没有构建步骤，没有宿主适配层（ADR-0002）。

## 它做什么

各模式的阶段顺序：

- `audit`：`ROUTE → TRUTH → RESTRUCTURE → VERIFY`（只诊断）
- `improve` / `rewrite`：`ROUTE → TRUTH → RESTRUCTURE → LANGUAGE → VERIFY`

- **ROUTE** 锁定运行参数 —— `audit` 只诊断，`improve` 做外科手术式升级，
  `rewrite` 整体重写。每个模式都支持 `--dry-run`。
- **TRUTH** 把 README 里的每条声明对着仓库原生凭据核对：manifest、CI
  配置、入口文件、扫描器输出。被证伪的声明记为 finding，不做静默修补；
  无法核实的声明删除或标记。
- **RESTRUCTURE** 守住首页边界。`audit` 模式下它诊断该迁去 `docs/` 的
  深层材料、重复的自我声明、生成痕迹和行文破绽；`improve` 和 `rewrite`
  模式下它把这些材料迁到 `docs/`，逐条记入迁移台账。
- **LANGUAGE**（`improve` 和 `rewrite`）跑上游 `writing-humanize`，
  叠加 README 领域的提炼规则；冻结区护栏和强度档位防止语言润色改坏
  事实、磨平真实文风。
- **VERIFY** 用静态探针加人工清单产出机器可查的凭据，交付报告封顶
  三行：结论、凭据、残余风险。

## 依赖

READJH 只持有编排层。两个上游技能按指针契约调用 —— 按规范名在固定
路径下查找；找不到就停下并给出安装指令；不做名字相似度兜底：

| 规范名 | 上游仓库 | 职责 |
|---|---|---|
| `readme-crafter-skill` | [linhai0872/readme-crafter-skill](https://github.com/linhai0872/readme-crafter-skill) | TRUTH/RESTRUCTURE：事实与结构 |
| `writing-humanize` | [risadams/ink-and-agency](https://github.com/risadams/ink-and-agency)（`skills/writing-humanize/`） | LANGUAGE：行文润色 |

另有四个上游只向 `references/` 贡献提炼规则，从不执行：`sepia`
（中文校准、职业/文风检查）、`anti-defensive-writing`（英文，
Kiterlin）、`academic-humanizer`（声明↔凭据纪律）、`humanize-readme`
（仅可抢救的规则）。

完整表格、机器上的实际位置、安装步骤，以及对 `writing-humanize` 的
两处刻意抑制，见 [UPSTREAM.md](UPSTREAM.md)。致谢与许可证见
[NOTICE](NOTICE)。

## 安装

把你的 Agent Skills 宿主指向本仓库根目录 —— 根目录就是技能本身。
再按 `UPSTREAM.md` 里的安装步骤，让两个执行器能在
`<skills-root>/<canonical-name>/SKILL.md` 解析到。

## 快速上手

装好后按名字对仓库调用技能：

- `audit` —— 输出 finding 和优先级，不动任何文件；支持
  `--repo-set <manifest>` 做跨仓库骨架同构检查（`audit` 模式默认已
  满足 `--dry-run`）。
- `improve` —— 对现有 README 做外科手术式升级；git 无法回滚时保留
  `.bak`。
- `rewrite` —— 对无法修补的 README 整体重写。
- `--dry-run` 适用于所有模式：只出计划和凭据，零文件写入（不改文件、
  不迁移 `docs/`、不建 `.bak`）。

## 目录结构

```
SKILL.md            # 技能本体（模型调用）：流程 + 契约
references/         # 编排层规则 + 提炼补充规则
scripts/            # check-readme.py —— 静态探针，只用标准库的 python3
tests/              # 探针的 unittest 测试与 fixtures
UPSTREAM.md         # 依赖、指针契约、偏差记录
NOTICE              # 上游致谢与许可证
GLOSSARY.md         # 领域术语 + 禁用同义词
docs/spec/          # 规格文档
docs/adr/           # 架构决策记录
docs/agents/        # 给 agent 操作者的仓库维护说明
docs/receipts/      # 验收运行凭据
docs/tickets/       # 指向 GitHub issue 跟踪器
```

## 状态

早期开发中；任务以 GitHub issue 形式跟踪（见 `docs/agents/`）。
许可证：MIT —— 见 [LICENSE](LICENSE)。
