---
name: web_browser
description: "**网页浏览器**。用于访问 URL 获取内容，或生成网页摘要。"
triggers:
- 访问
- browse
- 打开网页
- 查看网页
- 网页
- 阅读
- read
- summarize
---

# Web Browser (浏览器)

你是一个可以访问互联网的浏览器代理。

## 核心能力

1.  **访问网页 (Action: visit)**: 获取网页的原始文本内容 (HTML 已转换为 Markdown)。
2.  **生成摘要 (Action: summarize)**: 智能提取网页核心内容并生成摘要。

## 执行指令 (SOP)

当用户请求访问链接时，请提取以下参数调用内置脚本：

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `action` | string | 否 | 操作类型: `visit` (默认), `summarize` |
| `url` | string | 是 | 目标网页 URL (如果用户没提供 http 前缀，请保留原样，脚本会自动补全) |

### 意图映射示例

**1. 阅读网页**
- 用户输入: "看看这个网页写了什么: example.com"
- 提取参数:
  ```json
  { "action": "visit", "url": "example.com" }
  ```

**2. 总结网页**
- 用户输入: "总结这篇文章的核心观点 https://..."
- 提取参数:
  ```json
  { "action": "summarize", "url": "https://..." }
  ```

## 注意事项

- **内容截断**: 为了防止 Token 溢出，返回的网页内容可能会被截断。
- **动态渲染**: 目前可能不支持极度依赖 JS 的 SPA 页面（除非使用 Playwright MCP，但此技能为轻量级实现）。
