---
name: dev-workflow
description: Enforces the standard development workflow for the fund-portfolio-bot project: read docs first, propose a small scoped design, respect version scope, and limit code changes. Use when implementing, modifying, or refactoring functionality in this repository.
---

# Development workflow for fund-portfolio-bot

## When to use

Use this Skill when the user asks to:

- Implement a new feature or command
- Modify existing behavior
- Fix a bug by changing code
- Refactor a small part of the system

## Quick checklist (before coding)

1. Confirm the task is in scope for the current roadmap version.
2. Identify which modules and files are likely to be affected.
3. Plan to change at most 1–3 files in a single iteration.

## Standard workflow

1. **Read relevant context**

   - Skim these docs if they are relevant:
     - `docs/architecture.md`（架构与分层，含 ASCII 图）
     - `docs/roadmap.md`（版本范围）
     - `docs/settlement-rules.md`（业务规则，涉及结算逻辑时）
     - `CLAUDE.md` 第 3 节（编码规范核心约束）
   - 打开 `src/` 下相关代码，先理解当前实现，而不是直接改。

   **工具选择（MCP 使用决策）：**

   - 需要理解现有架构或跨模块流程？
     - 优先用 **Explore subagent** 探索代码库
     - 跨项目/多目录/复杂搜索时，建议配合 **Code-Index MCP**

   - 需要系统性推演方案或评审架构？
     - 建议用 **Sequential-Thinking MCP** 进行分步推理

   - 需要外部技术调研/最新最佳实践？
     - 建议用 **Exa MCP** 获取最新资料

2. **用中文总结任务边界**

   写一个不超过 10 条的中文要点列表，说明：

   - 用户想要什么（功能、行为改变）
   - 会影响到系统的哪些部分（模块 / 文件）
   - 明确哪些是本次 **不做的**：
     - 例如：AI 功能、盘中估值、大规模历史导入、大重构

3. **检查版本范围**

   - 查阅 `docs/roadmap.md`，确认当前版本（例如 v0.2 / v0.3）。
   - 明确标注：本需求是
     - ✅ 属于当前版本范围，或者
     - ⏭ 需要放到后续版本（说明原因，例如 roadmap 已标为 v0.3+）。
   - 如果超出范围，优先提出一个 **最小在范围内** 的替代方案，而不是悄悄做太多。

4. **提出具体修改计划**

   在写代码前，给出一个尽量精简的计划，包括：

   - 本次只修改的文件列表（1–3 个为宜），带路径
   - 每个文件中要：
     - 新增 / 修改 哪些类或函数
     - 是否引入新的类型、枚举或配置项

   等用户确认或微调这个计划后再开始编码。

5. **小步实现**

   在计划获得确认后：

   - 只改计划里列出的文件和位置。
   - 保持改动聚焦当前任务。
   - 避免：
     - 大范围重构或全局重命名
     - 一次修改太多无关文件
     - 未经明确同意就引入新的外部依赖或底层技术栈变更

6. **收尾检查**

   完成代码修改后：

   - 如果项目有现成测试，运行或至少描述需要哪些测试。
   - 用简短要点重新总结每个文件的改动。
   - 根据改动类型，提示需要更新的文档：
     - 新增组件 / 流程 → 建议更新 `docs/architecture.md`
     - 完成 roadmap 条目 → 建议更新 `docs/roadmap.md`
     - 重要技术决策 → 建议记录到 `docs/coding-log.md`
     - 环境 / 配置变化 → 建议更新 `docs/operations-log.md`
