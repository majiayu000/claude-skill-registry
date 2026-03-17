---
name: mcp-builder
description: 创建高质量 MCP（Model Context Protocol）服务器的指南，使 LLM 能够通过精心设计的工具与外部服务交互。在构建 MCP 服务器以集成外部 API 或服务时使用，无论是在 Python (FastMCP) 还是 Node/TypeScript (MCP SDK) 中。
license: Complete terms in LICENSE.txt
---

# MCP 服务器开发指南

## 概述

创建 MCP（Model Context Protocol）服务器，使 LLM 能够通过精心设计的工具与外部服务交互。MCP 服务器的质量通过它如何有效地使 LLM 完成现实世界任务来衡量。

---

# 流程

## 🚀 高级工作流程

创建高质量 MCP 服务器涉及四个主要阶段：

### 阶段 1：深入研究和规划

#### 1.1 理解现代 MCP 设计

**API 覆盖率 vs. 工作流工具：**
平衡全面的 API 端点覆盖与专门的工作流工具。工作流工具对于特定任务可能更方便，而全面的覆盖率为代理提供了组合操作的灵活性。性能因客户端而异——一些客户端受益于组合基本工具的代码执行，而其他客户端使用更高级别的工作流效果更好。如果不确定，优先考虑全面的 API 覆盖率。

**工具命名和可发现性：**
清晰、描述性的工具名称帮助代理快速找到正确的工具。使用一致的前缀（例如，`github_create_issue`、`github_list_repos`）和面向操作的命名。

**上下文管理：**
代理受益于简洁的工具描述以及过滤/分页结果的能力。设计返回集中、相关数据的工具。一些客户端支持代码执行，这可以帮助代理高效地过滤和处理数据。

**可操作的错误消息：**
错误消息应该通过具体建议和后续步骤引导代理找到解决方案。

#### 1.2 学习 MCP 协议文档

**浏览 MCP 规范：**

从站点地图开始查找相关页面：`https://modelcontextprotocol.io/sitemap.xml`

然后使用 `.md` 后缀获取特定页面的 markdown 格式（例如，`https://modelcontextprotocol.io/specification/draft.md`）。

需要查看的关键页面：
- 规范概述和架构
- 传输机制（可流式 HTTP、stdio）
- 工具、资源和提示定义

#### 1.3 学习框架文档

**推荐技术栈：**
- **语言**：TypeScript（高质量 SDK 支持，在许多执行环境中具有良好兼容性，例如 MCPB。此外，AI 模型擅长生成 TypeScript 代码，受益于其广泛使用、静态类型和良好的 lint 工具）
- **传输**：远程服务器使用可流式 HTTP，使用无状态 JSON（相对于有状态会话和流式响应，更易于扩展和维护）。本地服务器使用 stdio。

**加载框架文档：**

- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 核心指南

**对于 TypeScript（推荐）：**
- **TypeScript SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) - TypeScript 模式和示例

**对于 Python：**
- **Python SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 指南](./reference/python_mcp_server.md) - Python 模式和示例

#### 1.4 规划您的实现

**理解 API：**
查看服务的 API 文档以识别关键端点、身份验证要求和数据模型。根据需要使用网络搜索和 WebFetch。

**工具选择：**
优先考虑全面的 API 覆盖率。列出要实现的端点，从最常见的操作开始。

---

### 阶段 2：实现

#### 2.1 设置项目结构

有关项目设置，请参见特定语言的指南：
- [⚡ TypeScript 指南](./reference/node_mcp_server.md) - 项目结构、package.json、tsconfig.json
- [🐍 Python 指南](./reference/python_mcp_server.md) - 模块组织、依赖项

#### 2.2 实现核心基础设施

创建共享实用程序：
- 带身份验证的 API 客户端
- 错误处理帮助程序
- 响应格式化（JSON/Markdown）
- 分页支持

#### 2.3 实现工具

对于每个工具：

**输入架构：**
- 使用 Zod (TypeScript) 或 Pydantic (Python)
- 包含约束和清晰的描述
- 在字段描述中添加示例

**输出架构：**
- 尽可能为结构化数据定义 `outputSchema`
- 在工具响应中使用 `structuredContent`（TypeScript SDK 功能）
- 帮助客户端理解和处理工具输出

**工具描述：**
- 功能的简洁总结
- 参数描述
- 返回类型架构

**实现：**
- I/O 操作使用 Async/await
- 带有可操作消息的正确错误处理
- 在适用的地方支持分页
- 使用现代 SDK 时返回文本内容和结构化数据

**注释：**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### 阶段 3：审查和测试

#### 3.1 代码质量

审查以下内容：
- 无重复代码（DRY 原则）
- 一致的错误处理
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建和测试

**TypeScript：**
- 运行 `npm run build` 验证编译
- 使用 MCP Inspector 测试：`npx @modelcontextprotocol/inspector`

**Python：**
- 验证语法：`python -m py_compile your_server.py`
- 使用 MCP Inspector 测试

有关详细的测试方法和质量检查清单，请参见特定语言的指南。

---

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面的评估来测试其有效性。

**加载 [✅ 评估指南](./reference/evaluation.md) 以获取完整的评估指南。**

#### 4.1 理解评估目的

使用评估来测试 LLM 是否可以有效地使用您的 MCP 服务器回答现实的、复杂的问题。

#### 4.2 创建 10 个评估问题

要创建有效的评估，请遵循评估指南中概述的流程：

1. **工具检查**：列出可用工具并了解其功能
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建 10 个复杂、现实的问题
4. **答案验证**：自己解决每个问题以验证答案

#### 4.3 评估要求

确保每个问题是：
- **独立的**：不依赖于其他问题
- **只读的**：仅需要非破坏性操作
- **复杂的**：需要多次工具调用和深入探索
- **现实的**：基于人类关心的真实用例
- **可验证的**：可以通过字符串比较验证的单一、清晰答案
- **稳定的**：答案不会随时间改变

#### 4.4 输出格式

创建具有此结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找关于使用动物代号的 AI 模型发布的讨论。一个模型需要特定的安全名称，格式为 ASL-X。为以斑点野猫命名的模型确定的数字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

### 核心 MCP 文档（首先加载）
- **MCP 协议**：从 `https://modelcontextprotocol.io/sitemap.xml` 的站点地图开始，然后使用 `.md` 后缀获取特定页面
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON vs Markdown）
  - 分页最佳实践
  - 传输选择（可流式 HTTP vs stdio）
  - 安全和错误处理标准

### SDK 文档（在阶段 1/2 期间加载）
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取

### 特定语言的实现指南（在阶段 2 期间加载）
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包括：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 的工具注册
  - 完整的工作示例
  - 质量检查清单

- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南，包括：
  - 项目结构
  - Zod 架构模式
  - 使用 `server.registerTool` 的工具注册
  - 完整的工作示例
  - 质量检查清单

### 评估指南（在阶段 4 期间加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包括：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估
