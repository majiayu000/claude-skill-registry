---
name: claude-code-tips
description: 自动从网络收集 Claude Code 的最新使用技巧、功能更新和最佳实践。当用户需要了解 Claude Code 的新功能、使用技巧、高级用法或 Claude Agent SDK 开发时使用此skill。支持本地缓存，避免重复搜索。
license: MIT
allowed-tools: [WebSearch, WebFetch, mcp__fetch__fetch, Read, Write]
metadata:
  version: "2.1.0"
  category: development
  tags: claude-code,tips,tricks,best-practices,cache,agent-sdk
---

# Claude Code 使用技巧收集器

## 概述
这个 skill 专门用于收集和整理 Claude Code 的最新使用技巧、功能更新和最佳实践。它从多个来源自动搜索、筛选和总结 Claude Code 相关的实用信息。

**核心特性**：
- 自动从网络搜索最新信息
- 本地缓存机制，避免重复搜索
- 增量更新，只获取新内容
- 分类存储，便于查阅

## 使用时机
当用户提出以下需求时，使用此 skill：
- "Claude Code 有什么新功能"
- "如何更好地使用 Claude Code"
- "Claude Code 的使用技巧"
- "Claude Code 最佳实践"
- "Claude Code 高级用法"
- "Claude Code 快捷键和命令"
- "Claude Agent SDK 怎么用"
- "Agent SDK 开发范例"
- "如何创建自定义 Agent"
- "Claude Agent SDK 文档"
- 类似的 Claude Code 学习需求

## 目录结构

**数据存储位置**：项目根目录下的 `claude-code-tips/` 目录

```
项目根目录/
├── claude-code-tips/          # 数据存储目录（新增）
│   ├── data/                  # 数据文件
│   │   ├── index.json        # 索引文件
│   │   ├── new_features.md   # 新功能
│   │   ├── core_tips.md      # 核心技巧
│   │   ├── best_practices.md # 最佳实践
│   │   ├── shortcuts.md      # 快捷命令
│   │   ├── skills_plugins.md # 技能和插件
│   │   ├── mcp_servers.md    # MCP 服务器
│   │   ├── agent_sdk.md      # Agent SDK 开发
│   │   └── troubleshooting.md # 故障排除
│   └── archive/               # 归档目录
│       └── {year}/           # 按年份归档
└── .claude/
    └── skills/
        └── claude-code-tips/
            └── SKILL.md       # 本文件（技能定义）
```

## 执行流程

### 步骤 0: 检查本地缓存（重要）
在开始任何搜索之前，必须先检查本地缓存。

**操作步骤**：
1. 读取项目根目录下的 `claude-code-tips/data/index.json` 文件
2. 检查用户请求的类别是否已经有缓存数据
3. 检查上次更新时间，判断是否需要刷新（默认7天内有效）
4. 如果缓存有效，直接返回缓存内容
5. 如果缓存过期或不存在，才进行网络搜索

**缓存有效期规则**：
- `new_features`: 3天（快速更新的功能）
- `core_tips`: 7天（核心技巧相对稳定）
- `best_practices`: 14天（最佳实践变化较慢）
- `shortcuts`: 30天（快捷命令很少变化）
- `skills_plugins`: 7天（插件更新频率中等）
- `mcp_servers`: 7天（MCP 服务器更新频率中等）
- `agent_sdk`: 7天（SDK 文档更新频率中等）
- `troubleshooting`: 30天（故障排除内容相对稳定）

**示例缓存检查逻辑**：
```python
# 伪代码示例
index = read_json("data/index.json")
category = determine_category(user_query)

if index["categories"][category]["last_search"]:
    last_update = parse_date(index["categories"][category]["last_search"])
    days_since = (today - last_update).days

    cache_valid_days = get_cache_valid_days(category)
    if days_since < cache_valid_days:
        # 缓存有效，返回缓存内容
        return read_file(f"data/{index['categories'][category]['file']}")
```

### 步骤 1: 分析用户请求
根据用户的问题，确定需要搜索的类别：

**类别判断关键词**：
- "新功能"、"更新"、"最新" → `new_features`
- "技巧"、"技巧"、"窍门" → `core_tips`
- "最佳实践"、"建议"、"推荐" → `best_practices`
- "快捷键"、"命令"、"别名" → `shortcuts`
- "技能"、"插件"、"skill" → `skills_plugins`
- "MCP"、"服务器" → `mcp_servers`
- "Agent SDK"、"agent"、"SDK 开发"、"自定义 Agent" → `agent_sdk`
- "问题"、"错误"、"故障" → `troubleshooting`

### 步骤 2: 搜索最新信息（仅在缓存过期时）
如果缓存过期或不存在，使用 WebSearch 工具搜索。

**搜索关键词策略**：

按类别搜索：
```
# 新功能
"Claude Code" new features 2025
"Claude Code" changelog updates
anthropic claude-code release notes

# 核心技巧
"Claude Code" tips tricks 2025
"Claude Code" productivity hacks
"Claude Code" efficient workflow

# 最佳实践
"Claude Code" best practices guide
"Claude Code" workflow optimization
"Claude Code" project setup

# 快捷命令
"Claude Code" CLI commands reference
"Claude Code" keyboard shortcuts
"Claude Code" slash commands

# 技能插件
"Claude Code" skills marketplace
"Claude Code" custom skills
"Claude Code" plugin development

# MCP 服务器
"Claude Code" MCP servers list
"Claude Code" MCP best practices
Model Context Protocol claude-code

# Agent SDK 开发
"Claude Agent SDK" documentation 2025
"Claude Agent SDK" examples tutorial
"Claude Agent SDK" custom agent development
Anthropic agent SDK guide
"Claude Agent SDK" quickstart
"Claude Agent SDK" Python examples
"Claude Agent SDK" TypeScript examples

# 故障排除
"Claude Code" troubleshooting
"Claude Code" common errors
"Claude Code" not working
```

### 步骤 3: 更新本地缓存
将搜索到的内容整理后保存到本地文件。

**操作步骤**：
1. 整理搜索结果，按类别分组
2. 生成结构化的 markdown 内容
3. 写入到对应的 `.md` 文件
4. 更新 `index.json` 中的时间戳和计数
5. 将旧内容归档到 `archive/` 目录

**示例更新逻辑**：
```python
# 项目根目录路径（需要根据实际情况确定）
PROJECT_ROOT = get_project_root()
DATA_DIR = f"{PROJECT_ROOT}/claude-code-tips/data"

# 更新数据文件
content = format_markdown(results)
write_file(f"{DATA_DIR}/{category_file}", content)

# 更新索引
index["categories"][category]["last_search"] = today.isoformat()
index["categories"][category]["count"] += len(new_items)
index["search_history"].append({
    "date": today.isoformat(),
    "category": category,
    "items_found": len(new_items)
})
write_file(f"{DATA_DIR}/index.json", json.dumps(index, indent=2))
```

### 步骤 4: 返回结果给用户
从缓存文件中读取内容并返回给用户。

**输出格式**：
```markdown
# Claude Code {类别名称}
*最后更新：{更新日期}*

---

{缓存内容}

---

**信息来源**: 网络搜索 + 本地缓存
**下次更新建议**: {下次更新的日期}
```

## 信息来源

### 官方资源
- Anthropic 官方文档: https://docs.anthropic.com/claude/docs/claude-code
- Claude Code GitHub: https://github.com/anthropics/claude-code
- Claude Agent SDK 文档: https://docs.anthropic.com/en/docs/build-with-claude/agents
- Claude Agent SDK GitHub: https://github.com/anthropics/anthropic-sdk-python
- Anthropic 官方博客
- Claude Code 发布说明

### 社区资源
- GitHub Discussions
- Stack Overflow
- Reddit (r/Claude, r/artificial)
- Twitter/X 上的官方账号
- 技术博客和教程

### 中文资源
- 中文技术社区
- 微博、知乎等平台
- 中文技术博客
- 开发者社区的 Claude Code 讨论

## 数据文件格式

### index.json 格式
```json
{
  "last_updated": "2025-01-09",
  "categories": {
    "new_features": {
      "file": "new_features.md",
      "last_search": "2025-01-09T10:30:00",
      "count": 15
    },
    "agent_sdk": {
      "file": "agent_sdk.md",
      "last_search": "2025-01-09T10:30:00",
      "count": 20
    },
    ...
  },
  "search_history": [
    {
      "date": "2025-01-09T10:30:00",
      "category": "new_features",
      "items_found": 5
    }
  ]
}
```

### 内容文件格式示例 (new_features.md)
```markdown
# Claude Code 新功能

*最后更新：2025-01-09*
*数据来源：网络搜索*

---

## 最新功能

### 功能名称
**发现日期**：2025-01-08
**来源**：Anthropic 官方博客

#### 功能描述
简明的功能描述（2-3句话）

#### 使用方法
具体的步骤或命令示例

#### 示例
```bash
# 示例命令
claude-code new-feature-example
```

#### 注意事项
使用时需要注意的点

---

## 历史功能
（归档的功能列表）
```

### 内容文件格式示例 (agent_sdk.md)
```markdown
# Claude Agent SDK 开发指南

*最后更新：2025-01-09*
*数据来源：网络搜索*

---

## 快速开始

### 安装 SDK
**来源**：官方文档

#### Python 安装
```bash
pip install anthropic
```

#### TypeScript 安装
```bash
npm install @anthropic-ai/sdk
```

---

## 核心概念

### Agent 架构
- Agent 基础结构
- Loop 处理流程
- 工具集成

### 关键组件
- **Agent**: 核心代理类
- **Loop**: 执行循环控制器
- **Tool**: 工具函数接口
- **RunConfig**: 运行配置

---

## 开发范例

### 基础 Agent 示例
**语言**：Python
**难度**：入门

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 自定义 Agent 示例
**语言**：Python
**难度**：中级

```python
from anthropic_loop import Agent, Loop, Tool

# 自定义工具
def my_tool(input: str) -> str:
    return f"处理结果: {input}"

# 创建 Agent
agent = Agent(
    model="claude-3-5-sonnet-20241022",
    tools=[my_tool]
)

# 运行 Loop
loop = Loop(agent)
result = loop.run("请使用工具处理这个请求")
```

### 高级 Agent 架构
**语言**：TypeScript
**难度**：高级

```typescript
import { Agent, Tool, LoopConfig } from '@anthropic-ai/sdk';

// 多工具 Agent
const agent = new Agent({
  model: 'claude-3-5-sonnet-20241022',
  tools: [
    new Tool({ name: 'search', execute: searchHandler }),
    new Tool({ name: 'calculate', execute: calcHandler })
  ],
  config: {
    maxIterations: 10,
    timeout: 30000
  }
});
```

---

## 常见用例

### 1. 任务型 Agent
处理特定任务的 Agent 设计模式

### 2. 对话型 Agent
对话管理和上下文保持

### 3. 代码助手 Agent
代码生成和审查工具

### 4. 研究型 Agent
信息收集和分析工具

---

## 最佳实践

### 错误处理
```python
try:
    response = agent.run(user_input)
except APIError as e:
    logger.error(f"API 错误: {e}")
except ToolError as e:
    logger.error(f"工具错误: {e}")
```

### 性能优化
- 批量处理请求
- 缓存常用响应
- 异步执行工具

### 安全考虑
- API 密钥管理
- 输入验证
- 输出过滤

---

## 参考资源

- [官方文档](https://docs.anthropic.com/en/docs/build-with-claude/agents)
- [GitHub 仓库](https://github.com/anthropics/anthropic-sdk-python)
- [API 参考](https://docs.anthropic.com/en/api/messages)

---

## 更新日志

### 2025-01-09
- 添加 Loop 架构文档
- 新增 TypeScript 示例
- 更新最佳实践指南
```

### 内容文件格式示例 (new_features.md)
```markdown
# Claude Code 新功能

*最后更新：2025-01-09*
*数据来源：网络搜索*

---

## 最新功能

### 功能名称
**发现日期**：2025-01-08
**来源**：Anthropic 官方博客

#### 功能描述
简明的功能描述（2-3句话）

#### 使用方法
具体的步骤或命令示例

#### 示例
```bash
# 示例命令
claude-code new-feature-example
```

#### 注意事项
使用时需要注意的点

---

## 历史功能
（归档的功能列表）
```

## 质量标准

### 信息筛选标准
- **时效性**：优先选择最近3个月内的信息
- **权威性**：优先选择官方来源和知名社区
- **实用性**：选择对实际使用有帮助的技巧
- **准确性**：确保信息的准确性，避免过时内容

### 内容质量要求
- **清晰性**：用简洁明了的语言描述
- **完整性**：提供完整的步骤和示例
- **可操作性**：确保技巧可以直接应用
- **价值性**：突出对用户的实际价值

### 缓存管理标准
- **定期更新**：根据类别设置合理的缓存有效期
- **版本控制**：重要变更前先备份旧数据
- **清理归档**：定期清理过期数据到归档目录
- **索引维护**：保持索引文件的准确性

## 用户命令支持

用户可以通过以下命令控制缓存行为：

- "刷新缓存" - 强制刷新所有类别
- "刷新 [类别]" - 刷新指定类别
- "查看缓存状态" - 显示当前缓存状态
- "清除缓存" - 清除所有缓存数据
- "导出缓存" - 将缓存导出为单个文件

## 执行步骤（完整流程）

当用户请求 Claude Code 技巧时：

### 第一阶段：检查缓存
1. **读取索引文件**
   ```
   使用 Read 工具读取项目根目录下的 claude-code-tips/data/index.json
   ```

2. **判断请求类别**
   ```
   根据用户输入确定类别
   ```

3. **检查缓存有效性**
   ```
   比较当前时间和上次更新时间
   判断是否在缓存有效期内
   ```

4. **返回缓存或继续搜索**
   ```
   如果缓存有效：读取并返回缓存文件
   如果缓存过期：继续执行后续步骤
   ```

### 第二阶段：搜索和更新（仅在需要时）
1. **执行网络搜索**
   ```
   使用 WebSearch 搜索最新信息
   ```

2. **访问官方资源**
   ```
   使用 WebFetch 访问官方文档
   ```

3. **整理和分类**
   ```
   按类别分组
   按重要性排序
   提取关键信息
   ```

4. **更新本地缓存**
   ```
   生成 markdown 内容
   写入对应的 .md 文件
   更新 index.json
   归档旧数据
   ```

### 第三阶段：返回结果
1. **格式化输出**
   ```
   使用清晰的 markdown 格式
   添加更新时间戳
   包含缓存状态信息
   ```

2. **提供可操作建议**
   ```
   突出立即可用的技巧
   提供具体步骤
   标注难度级别
   ```

3. **提示下次更新时间**
   ```
   告知用户缓存有效期
   建议下次更新的时间
   ```

## 注意事项

### 缓存管理
1. **避免过度刷新**：尊重缓存有效期，减少不必要的网络请求
2. **数据一致性**：确保索引文件和内容文件同步更新
3. **存储优化**：定期归档旧数据，保持文件大小合理
4. **错误处理**：网络搜索失败时，仍然可以返回缓存内容

### 信息质量
1. **信息验证**：确保信息的准确性和时效性
2. **版本兼容**：注意 Claude Code 的版本差异
3. **环境差异**：考虑不同操作系统的差异
4. **安全提醒**：提醒用户注意安全和隐私

### 用户体验
1. **快速响应**：优先返回缓存，快速响应用户
2. **清晰提示**：明确告知用户数据来源和更新时间
3. **增量显示**：先返回缓存，再后台更新（如果需要）
4. **可定制性**：允许用户调整缓存有效期

## 示例对话

**用户**: "Claude Code 有什么新功能？"

**执行流程**：
1. 检查项目根目录下的 `claude-code-tips/data/index.json`
2. 发现 `new_features` 上次更新是 2 天前
3. 缓存有效（3天期内），直接返回 `claude-code-tips/data/new_features.md` 内容

**用户**: "刷新一下新功能"

**执行流程**：
1. 强制刷新标记
2. 执行网络搜索
3. 更新项目根目录下的 `claude-code-tips/data/new_features.md`
4. 更新 `claude-code-tips/data/index.json`
5. 返回最新内容

**用户**: "Claude Agent SDK 怎么用？有什么开发范例？"

**执行流程**：
1. 检查项目根目录下的 `claude-code-tips/data/index.json`
2. 发现 `agent_sdk` 上次更新是 10 天前
3. 缓存过期（超过7天），执行网络搜索
4. 搜索关键词："Claude Agent SDK" documentation 2025, "Claude Agent SDK" examples tutorial
5. 访问官方文档：https://docs.anthropic.com/en/docs/build-with-claude/agents
6. 整理搜索结果，更新 `claude-code-tips/data/agent_sdk.md`
7. 更新 `claude-code-tips/data/index.json`
8. 返回最新内容，包括安装指南、核心概念、开发范例等

**用户**: "如何创建一个自定义的 Claude Agent？"

**执行流程**：
1. 确定类别为 `agent_sdk`
2. 检查缓存，发现是 3 天前更新的
3. 缓存有效，直接返回 `claude-code-tips/data/agent_sdk.md` 中关于自定义 Agent 的部分
4. 重点展示「自定义 Agent 示例」和「高级 Agent 架构」部分

---

现在您可以开始为用户提供 Claude Code 的最新技巧和功能了！记住：**总是先检查缓存，再决定是否搜索**。
