---
name: claude-code-dev
description: Claude Code Plugin 开发专家。当用户要创建 Plugin、Skill、Subagent、Slash command、Hook 时触发。也用于解答 Claude Code 开发相关问题。触发词：创建 plugin、写 skill、写 agent、创建 hook、写 command、插件开发。
---

# Claude Code Plugin 开发

开发 Claude Code Plugin 及其组件（Skill、Subagent、Command、Hook）。

## 核心原则

1. **先搜索官方文档**：在创建任何组件前，先搜索最新的官方文档
2. **遵循官方规范**：严格按照文档中的文件格式和最佳实践
3. **精简高效**：只包含必要内容，避免冗余

## 官方文档地址

所有开发相关文档都在 `code.claude.com/docs/en/` 下：

| 主题 | 搜索关键词 |
|------|-----------|
| Plugin 总览 | site:code.claude.com plugin structure |
| Skill | site:code.claude.com skill SKILL.md |
| Subagent | site:code.claude.com sub-agents |
| Slash Command | site:code.claude.com slash-commands |
| Hooks | site:code.claude.com hooks |

## 开发流程

### 创建 Plugin

1. 搜索官方文档获取最新结构
2. 创建目录结构：
   ```
   plugin-name/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── agents/
   ├── skills/
   ├── commands/
   ├── hooks/
   └── README.md
   ```

### 创建 Skill

1. 核心文件：`skill-name/SKILL.md`
2. frontmatter 必填：`name`、`description`
3. description 要包含触发条件

### 创建 Subagent

1. 文件位置：`.claude/agents/agent-name.md`
2. frontmatter：`name`、`description`、`tools`（可选）、`model`（可选）、`skills`（可选）

### 创建 Hook

1. 10 种事件：PreToolUse、PostToolUse、PermissionRequest、UserPromptSubmit、Stop、SubagentStop、PreCompact、SessionStart、SessionEnd、Notification
2. 配置文件：`hooks/hooks.json`
3. exit code 2 = 阻止操作

## 参考插件

搜索：`site:github.com anthropics claude-code plugins`
- ralph-wiggum：迭代循环
- pr-review-toolkit：多 agent 协作
- plugin-dev：插件开发工具
