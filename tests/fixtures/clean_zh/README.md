# 中文测试仓库 (基于 6F / EgressAPIKEY 真实中文片段)

宏观与微观工程内容审计工具。

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Xxx91n/6F/ci.yml)](https://github.com/Xxx91n/6F/actions/workflows/ci.yml)

## 架构说明

系统运行于两种数据面模式：
- 模式 A：前置转发器
- 模式 B：引擎直连

```bash
python3 scripts/scan.py
```

详见 [文档](docs/arch_zh.md)。

> **合规提示**：本工具仅供合法研究与学习使用。

## 局限性与已知问题

目前仅支持单机模式运行，分布式集群调度暂不在本阶段范围。

## 许可证

基于 [LICENSE](LICENSE) 发布。
