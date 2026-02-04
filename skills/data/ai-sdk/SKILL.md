---
name: ai-sdk
description: 回答 AI SDK 相关问题并协助构建 AI 功能。适用于：(1) 询问 generateText、streamText、ToolLoopAgent、tools 等 API；(2) 构建 AI 智能体、聊天机器人或文本生成；(3) 关于 AI 提供方（OpenAI、Anthropic 等）、流式、tool calling、结构化输出的问题。
---

## AI SDK 文档

需要最新信息时：

### 若使用 ai@6.0.34 及以上

在 `node_modules/ai/` 中搜索打包文档与源码：

1. **文档**：`grep "你的查询" node_modules/ai/docs/`
2. **源码**：`grep "你的查询" node_modules/ai/src/`

查找具体文件：

- `glob "node_modules/ai/docs/**/*.mdx"` 文档
- `glob "node_modules/ai/src/**/*.ts"` 源码

提供方包（`@ai-sdk/openai`、`@ai-sdk/anthropic` 等）在各自 `node_modules/@ai-sdk/.../docs/` 下也有文档。

**不确定时，升级到最新版 AI SDK。**

### 否则

1. 搜索文档：`https://ai-sdk.dev/api/search-docs?q=你的查询`
2. 返回结果包含以 `.md` 结尾的链接
3. 直接请求这些 `.md` URL 获取纯文本内容（如 `https://ai-sdk.dev/docs/agents/building-agents.md`）

用以上方式获取当前 API、示例与用法。

常见错误与排查见 [Common Errors Reference](references/common-errors.md)。  
Vercel AI Gateway 用法见 [AI Gateway Reference](references/ai-gateway.md)。

## 提供方相关信息（ai@6.0.34+）

关于具体提供方（OpenAI、Anthropic、Google 等）时，搜索对应包：

1. **提供方文档**：`grep "你的查询" node_modules/@ai-sdk/.../docs/`
2. **提供方源码**：`grep "你的查询" node_modules/@ai-sdk/.../src/`

查找提供方文件：

- `glob "node_modules/@ai-sdk/.../docs/**/*.mdx"` 文档
- `glob "node_modules/@ai-sdk/.../src/**/*.ts"` 源码

`providerOptions` 等提供方专属配置尤其需查阅各自包文档，各提供方选项不同。
