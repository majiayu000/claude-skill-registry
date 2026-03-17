---
name: doc-bootstrapping
description: 一键建立项目文档系统。初始化 Rule1, Memory 以及基于 Diátaxis 的目录结构。
---

# CNS Documentation Bootstrap

## Purpose
本技能旨在帮助开发者在启动新项目或重构现有项目时，快速建立符合 Antigravity 标准的「中央神经系统 (CNS)」文档体系。

## Protocol: One-Click Initialization
当接收到 "init project docs" 或类似的初始化请求时，请执行以下步骤：

1.  **Environment Check**: 确认当前工作目录。
2.  **Create Rule One**:
    - 将 `resources/rule-one-template.md` 写入 `.agent/rules/rule-one.md`。
    - 根据项目名称微调前缀。
3.  **Create Memory**:
    - 将 `resources/memory-template.md` 写入 `doc/memory.md`。
4.  **Scaffold Diátaxis**:
    - 创建 `doc/explanation/`, `doc/specs/`, `doc/how-to/`, `doc/tutorials/` 目录。
    - 写入对应的基础 `README.md`（参考 `resources/diataxis-blueprint.md`）。
5.  **Register Support Docs**:
    - 在 `doc/explanation/` 中创建 `system-dev.md`。

## Resource Files
- [Rule One Template](resources/rule-one-template.md)
- [Memory Template](resources/memory-template.md)
- [Diátaxis Blueprint](resources/diataxis-blueprint.md)
