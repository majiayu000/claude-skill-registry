---
name: unit-test-remote
description: 仅在最终的 /speckit.verify 步骤用于统一验证代码正确性；实现阶段禁止调用。
---

# 远程单元测试 Skill (unit-test-remote)

## 使用范围（Usage Scope）

IMPORTANT: This skill MUST ONLY be used in the final verification step (e.g., `/speckit.verify`). DO NOT invoke during `/speckit.implement` or `/speckit.implement_v2`, nor in any intermediate implementation tasks.

重要：本 Skill 仅允许在最终验证步骤（如 `/speckit.verify` 或其他统一 verify gate）中使用，用于在合入前统一验证代码正确性。实现阶段（包括 `/speckit.implement`、`/speckit.implement_v2` 以及其他实现子任务）禁止调用本 Skill。

## 负面触发器（Negative Triggers）

在以下上下文或提示中，Coco / Agent 应视为**不应调用**本 Skill 的强信号：

- 提示或系统 Prompt 中出现“implement”、“implement_v2”、“实现过程”、“实现任务”、“开发阶段”等描述；
- 当前命令为 `/speckit.implement` 或 `/speckit.implement_v2`；
- 对话目标聚焦于“编写或修改代码/单测”，而**不是**“在所有实现完成后做最终验证”。

若检测到上述信号，即便用户未明确说明，也应避免调用 `unit-test-remote`，并提示将统一在 `/speckit.verify` 阶段执行远程 UT。

## 核心功能

本 Skill 封装了对 Bits UT Remote MCP 的调用，提供了一个标准化的接口来远程执行单元测试。它只能作为最终验证（verify gate）中的一部分，用于在合入前集中判断当前改动是否可以通过单元测试门禁。

## 行为概要

1.  **参数校验**：检查调用方提供的参数是否完整、合法，例如 `test_kind`、`working_directory`、`package_path` 等。
2.  **构造命令**：根据输入参数，拼装出 `~/.bits-ut/utd remote_test ...` 命令。
3.  **执行测试**：在指定的 `working_package`（仓库根目录）下执行该命令，并实时捕获输出。
4.  **解析结果**：
    -   实时解析 `bits-ut` 返回的 JSON 流，提取 `Output` 字段中的有效日志。
    -   如果测试失败，提取失败用例的详细日志（从 `=== RUN` 到 `--- FAIL` 的完整块）。
    -   如果测试成功，提取 `ok ...` 成功信息。
5.  **返回结构化输出**：
    -   **`exit_code`**: `0` 表示成功，非 `0` 表示失败。
    -   **`output`**: 经过提炼的日志摘要，包含失败用例详情、成功包信息以及日志文件路径提示。

## 成功标准

- **`exit_code == 0`**：这是唯一的成功标准。任何非零的 `exit_code` 都意味着测试未通过或执行出错。

## 失败处理

- 如果 `exit_code != 0`，当前的 **验证步骤必须被视为未通过**，不得将相关改动合入主分支或发布。
- Coco 或上层 Agent 应：
    1.  **提取失败日志**：从 `output` 中解析出导致失败的测试用例名称和详细日志。
    2.  **制定修复计划**：基于失败日志，明确地规划下一步的修复动作（例如“修改某文件的某行代码以修复断言失败”）。
    3.  **迭代修复**：重新进入代码实现阶段或补充/修正单测，执行修复计划。
    4.  **重新运行测试**：修复完成后，通过 `/speckit.verify` 再次调用本 Skill，直至 `exit_code == 0`。

> 更多技术细节、参数说明与最佳实践，请参见同目录下的 `reference.md`。
