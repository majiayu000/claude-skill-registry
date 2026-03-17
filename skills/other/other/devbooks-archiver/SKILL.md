---
name: devbooks-archiver
description: devbooks-archiver：归档阶段的唯一入口，负责完整的归档闭环（自动回写→规格合并→文档同步检查→变更包归档移动）。用户说"归档/archive/收尾/闭环/合并到真理"等时使用。
recommended_experts: ["System Architect", "Technical Writer"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
  - Bash
---

# DevBooks：归档器（Archiver）

## 渐进披露
### 基础层（必读）
目标：完成归档闭环（回写、合并、检查、归档移动）。
输入：<change-id>、<change-root>/<truth-root>、归档所需产物与证据。
输出：归档报告、更新后的 specs/architecture、归档后的变更包路径。
边界：不替代其他角色；不修改 tests/；未通过严格闸门不得归档。
证据：change-check.sh 严格检查输出、归档报告、归档后的目录位置。

### 进阶层（可选）
适用：需要明确回写范围、合并策略或文档同步处理时。

### 扩展层（可选）
适用：需要维护模式、上下文检测或归档报告模板时。

## 核心要点
- 归档阶段唯一入口：自动回写 → 规格/架构合并 → 文档检查 → 归档移动。
- 归档前必须通过 `change-check.sh <change-id> --mode strict`，失败即停止。
- 执行前完成配置发现并读取 `agents_doc` 规则文档。

## 参考资料
- `skills/devbooks-archiver/references/归档流程与规则.md`：绝对禁令、归档 7 步流程、回写范围、合并规则、报告模板与维护模式。
- `skills/devbooks-archiver/references/归档器提示词.md`：完整提示词与执行约束。

## 推荐 MCP 能力类型
- 代码检索（code-search）
- 引用追踪（reference-tracking）
- 影响分析（impact-analysis）
