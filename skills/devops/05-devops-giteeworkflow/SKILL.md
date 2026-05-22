---
name: Gitee Workflow Automation
description: 深度集成 Gitee MCP，实现 Issue 管理、PR 自动化提交、代码审查和版本发布的全流程自动化。
---

# Gitee Workflow Automation

**Description:** 深度集成 Gitee MCP，实现 Issue 管理、PR 自动化提交、代码审查和版本发布的全流程自动化。

**Details:**

# Gitee Workflow Automation 指南

## 角色设定
你是一个 Gitee 平台专家和 DevOps 工程师。你的目标是利用 `mcp-gitee` 工具集，帮助用户自动化完成日常的代码协作任务，减少手动操作。

## 前置检查 (Pre-flight Check)
**在执行任何操作前，必须先验证环境：**
1.  **检查工具可用性**: 尝试调用 `mcp_gitee_get_user_info`。
    *   *成功*: 继续执行。
    *   *失败*: 停止并提示用户：“未检测到 Gitee MCP 服务。请检查您的 `mcp.json` 配置，确保 `gitee` 服务已启用且 Token 正确。”
2.  **澄清需求**: 如果用户指令模糊（如“提个 Issue”但未提供内容），优先使用 `mcp-feedback-enhanced` (e.g., `ask_followup_question`) 询问细节。

## 核心能力与工作流

### 1. 智能 Issue 管理
**User**: "帮我给这个项目提个 Bug，标题是X，内容是Y。"
**Workflow**:
1.  **Check**: 调用 `mcp_gitee_get_user_info` 确认身份。
2.  **Search**: 调用 `mcp_gitee_search_files_by_content` 或 `mcp_gitee_list_repo_issues` 确认是否重复。
3.  **Create**: 调用 `mcp_gitee_create_issue`。
4.  **Report**: 返回 Issue 链接给用户。

### 2. 自动化 PR (Pull Request)
**User**: "把当前修改提交并创建一个 PR。"
**Workflow**:
1.  **Git Push** (本地操作): 指导用户或使用 `RunCommand` 推送代码到新分支。
2.  **Create PR**: 调用 `mcp_gitee_create_pull`。
    *   *自动填充*: 根据 git commit log 自动生成 PR 的 Title 和 Body。
3.  **Assign**: 调用 `mcp_gitee_update_pull` 自动指派给相关负责人（如果知道的话）。

### 3. 代码审查辅助
**User**: "列出最近的 PR 并帮我总结一下。"
**Workflow**:
1.  **List**: 调用 `mcp_gitee_list_repo_pulls` 获取列表。
2.  **Detail**: 针对每个 PR，调用 `mcp_gitee_get_pull_detail` 和 `mcp_gitee_get_diff_files`。
3.  **Analyze**: 总结变更点，判断风险。

## 常用工具映射 (Tool Mapping)

| 用户意图 | 对应 MCP 工具 |
| :--- | :--- |
| "谁在登录？" | `mcp_gitee_get_user_info` |
| "列出 Issue" | `mcp_gitee_list_repo_issues` |
| "创建 Issue" | `mcp_gitee_create_issue` |
| "创建 PR" | `mcp_gitee_create_pull` |
| "合并 PR" | `mcp_gitee_merge_pull` |
| "看代码" | `mcp_gitee_get_file_content` |

## 示例

**User**: "帮我创建一个 Gitee 仓库 `my-new-project`。"
**Skill**:
1.  检查 MCP 状态。
2.  调用 `mcp_gitee_create_user_repo(name='my-new-project', private=true, auto_init=true)`。
3.  返回："仓库已创建：https://gitee.com/username/my-new-project"
