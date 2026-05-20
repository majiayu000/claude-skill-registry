---
name: subagent-creator
description: 创建具有自定义系统提示和工具配置的专业化 Claude Code 子代理。当用户要求创建新的子代理、自定义代理、专业助手，或为 Claude Code 配置特定任务的 AI 工作流时使用。
---

# 子代理创建器

为 Claude Code 创建专业化的 AI 子代理，以处理特定任务和自定义的提示访问权限。

## 子代理文件格式

子代理是存储在以下位置的带 YAML 前置内容的 Markdown 文件：

- **项目**: `.claude/agents/` (较高优先级)
- **用户**: `~/.claude/agents/` (较低优先级)

### 结构

```markdown
---
name: 子代理名称
description: 使用此子代理的时机 (包含"use proactively"以实现自动委派)
tools: 工具1, 工具2, 工具3  # 可选 - 如果省略则继承所有工具
model: sonnet               # 可选 - sonnet/opus/haiku/inherit
permissionMode: default     # 可选 - default/acceptEdits/bypassPermissions/plan
skills: 技能1, 技能2        # 可选 - 自动加载技能
---

系统提示放在这里。定义角色、职责和行为。
```

### 配置字段

| 字段 | 必需 | 描述 |
|-------|----------|-------------|
| `name` | 是 | 小写字母加连字符 |
| `description` | 是 | 用途和使用时机（自动委派的关键） |
| `tools` | 否 | 逗号分隔的工具列表（省略以继承所有） |
| `model` | 否 | `sonnet`、`opus`、`haiku` 或 `inherit` |
| `permissionMode` | 否 | `default`、`acceptEdits`、`bypassPermissions`、`plan` |
| `skills` | 否 | 要自动加载的技能 |

## 创建工作流程

1. **收集需求**：询问子代理的用途、使用时机和所需能力
2. **选择范围**：项目 (`.claude/agents/`) 或用户 (`~/.claude/agents/`)
3. **定义配置**：名称、描述、工具、模型
4. **编写系统提示**：明确的角色、职责和输出格式
5. **创建文件**：将 `.md` 文件写入适当位置

## 编写有效的子代理

### 描述最佳实践

`description` 字段对于自动委派至关重要：

```yaml
# 良好 - 具体的触发条件
description: 代码审查专家。在编写或修改代码后主动使用。

# 良好 - 清晰的用例
description: 专门处理错误、测试失败和异常行为的调试专家。

# 不佳 - 过于模糊
description: 帮助处理代码
```

### 系统提示指南

1. **明确定义角色**："你是[特定专家角色]"
2. **列出调用时的操作**：首先做什么
3. **指定职责**：子代理处理什么
4. **包含指导原则**：约束和最佳实践
5. **定义输出格式**：如何组织响应

### 工具选择

- **只读任务**：`Read、Grep、Glob、Bash`
- **代码修改**：`Read、Write、Edit、Grep、Glob、Bash`
- **完全访问**：省略 `tools` 字段

完整工具列表请参见 [references/available-tools.md](references/available-tools.md)。

## 子代理示例

完整示例请参见 [references/examples.md](references/examples.md)：

- 代码审查员
- 调试专家
- 数据科学家
- 测试运行器
- 文档编写者
- 安全审计员

## 模板

从 [assets/subagent-template.md](assets/subagent-template.md) 复制以开始新的子代理。

## 快速开始示例

创建一个代码审查子代理：

```bash
mkdir -p .claude/agents
```

写入 `.claude/agents/code-reviewer.md`：

```markdown
---
name: code-reviewer
description: 审查代码质量和安全性。在代码更改后主动使用。
tools: Read, Grep, Glob, Bash
model: inherit
---

你是一位资深代码审查员。

被调用时：
1. 运行 git diff 查看更改
2. 审查修改的文件
3. 按优先级报告问题

重点关注：
- 代码可读性
- 安全漏洞
- 错误处理
- 最佳实践
```
