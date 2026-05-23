---
name: librarian
description: |
  Web research agent for documentation, web search, and code search.
  Use when: querying docs, searching latest tech info, code search via grep.app.
  网络研究专家，专注于外部信息检索。
---

# Librarian 网络研究专家

## 角色定位

**Librarian** 是网络研究专家，专注于**外部信息检索**：
- 📖 **文档查询**：查询官方文档和技术资料（context7）
- 🌐 **网络搜索**：搜索最新技术动态和解决方案（Exa）
- 🔗 **代码搜索**：通过 grep.app 搜索开源代码库
- 📄 **网页抓取**：深度阅读技术文章（firecrawl）

**重要**：本地代码搜索请使用 Claude 的 **Explore 代理**。

## 触发场景

| 场景 | 示例 |
|------|------|
| 文档查询 | "React useEffect 的最佳实践" |
| 网络搜索 | "TypeScript 5.5 的新特性" |
| 问题诊断 | "为什么 Zod 报这个错误" |
| 代码搜索 | "TanStack Query 的 useQuery 实现" |
| 外部源码 | "lodash 的 debounce 是如何实现的" |

## 不适用场景

| 场景 | 正确选择 |
|------|----------|
| 本地代码搜索 | 使用 Claude 的 **Explore 代理** |
| 代码修改 | 使用 **Coder** |
| 前端开发 | 使用 **Frontend** |

## 工具参考

| 参数 | 默认值 | 说明 |
|------|--------|------|
| PROMPT | - | 网络研究任务描述（必填） |
| cd | - | 工作目录（必填） |
| sandbox | read-only | 沙箱策略（只读） |
| timeout | 120 | 空闲超时（秒） |
| max_duration | 600 | 总时长上限（秒） |
| max_retries | 1 | 自动重试次数 |

## 研究能力

Librarian 通过 Gemini CLI 配置的 MCP 提供网络研究能力：

| MCP | 功能 | 示例场景 |
|-----|------|----------|
| **context7** | 官方文档查询 | "React useEffect 最佳实践" |
| **exa** | 网络搜索 | "TypeScript 5.5 新特性" |
| **Playwright** | 浏览器自动化 | "抓取需要 JS 渲染的页面" |
| **grep** | 代码搜索 (grep.app) | "TanStack Query 的 useQuery 实现" |
| **firecrawl** | 网页抓取 | "深入阅读某篇技术文章" |

## 请求分类

| 类型 | 触发词 | 执行策略 |
|------|--------|----------|
| **TYPE A: 概念/用法** | "如何使用...", "最佳实践..." | context7 + exa |
| **TYPE B: 外部源码** | "X 是如何实现的" | gh clone + 分析 |
| **TYPE C: 问题诊断** | "为什么报错...", "怎么解决..." | exa + gh issues |
| **TYPE D: 综合研究** | 复杂/模糊请求 | 全部工具并行 |

## Prompt 模板

### 文档查询

```
请查询以下技术问题：
**问题**：[具体问题]
**技术栈**：[相关库/框架]
**期望**：[官方文档链接/代码示例]
```

### 问题诊断

```
请帮我研究以下问题：
**错误信息**：[错误内容]
**技术栈**：[相关库/框架/版本]
**期望**：[解决方案/官方 issue 链接]
```

### 综合研究

```
请研究以下主题：
**主题**：[研究主题]
**背景**：[项目上下文]
**需要**：[证据/链接/代码示例]
```

## 返回值

```json
// 成功
{
  "success": true,
  "tool": "librarian",
  "SESSION_ID": "uuid-string",
  "result": "<analysis>...</analysis>\n<results>...</results>",
  "duration": "0m45s"
}

// 失败
{
  "success": false,
  "tool": "librarian",
  "error": "错误信息",
  "error_kind": "idle_timeout | timeout | ..."
}
```

## 输出格式

Librarian 返回结构化结果：

```
<analysis>
**字面请求**: [用户说的话]
**实际需求**: [用户真正想知道什么]
**请求类型**: [TYPE A/B/C/D]
</analysis>

<results>
<evidence>
[带永久链接的证据]
</evidence>

<answer>
[直接回答用户的实际需求]
</answer>

<uncertainty>
[如果有任何不确定的地方]
</uncertainty>
</results>
```

## 范围边界

Librarian 是 **只读网络研究者**：

| 禁止操作 | 替代方案 |
|----------|----------|
| 本地代码搜索 | 使用 Claude 的 Explore 代理 |
| 创建/修改文件 | 使用 Coder |
| 前端开发 | 使用 Frontend |

如果用户请求本地代码搜索，请告知使用 Claude 的 Explore 代理。
