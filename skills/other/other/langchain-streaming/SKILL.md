---
name: langchain-streaming
description: Stream outputs from LangChain agents and models - includes stream modes, token streaming, progress updates, and real-time feedback
language: js
---

# langchain-streaming (JavaScript/TypeScript)

## 概述

流式传输让您能够在 LangChain 代理和模型运行时实时显示更新。您可以逐步显示输出，而不是等待完整的响应，从而改善用户体验，特别是对于长时间运行的操作。

**核心概念：**
- **流式模式（Stream Modes）**：不同类型的数据流（values、updates、messages、custom）
- **Token 流式传输**：生成时的 LLM token
- **代理进度**：每个代理步骤后的状态更新
- **自定义更新**：用户定义的进度信号

## 何时使用流式传输

| 场景 | 流式传输？ | 原因 |
|----------|---------|-----|
| 长模型响应 | ✅ 是 | 在生成时显示 token |
| 多步骤代理任务 | ✅ 是 | 通过步骤显示进度 |
| 长时间运行的工具 | ✅ 是 | 提供进度更新 |
| 简单快速请求 | ⚠️ 可能 | 开销可能不值得 |
| 后端批处理 | ❌ 否 | 没有用户等待更新 |

## 决策表

### 流式模式选择

| 模式 | 何时使用 | 返回 |
|------|----------|---------|
| `"values"` | 需要每步后的完整状态 | 完整状态对象 |
| `"updates"` | 仅需要变化的内容 | 状态增量 |
| `"messages"` | 需要 LLM token 流 | [token, metadata] 元组 |
| `"custom"` | 需要自定义进度信号 | 用户定义的数据 |
| 多个模式 | 需要组合数据 | 模式数组 |

## 代码示例

### 基本模型 Token 流式传输

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ model: "gpt-4.1" });

// 在 token 到达时流式传输
const stream = await model.stream("用简单的术语解释量子计算");

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
// 输出渐进出现："量子" "计算" "是" ...
```

### 代理进度流式传输

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, calculatorTool],
});

// 使用 "updates" 模式流式传输代理步骤
for await (const chunk of await agent.stream(
  { messages: [{ role: "user", content: "搜索 AI 新闻并总结" }] },
  { streamMode: "updates" }
)) {
  console.log("步骤:", JSON.stringify(chunk, null, 2));
}
// 显示每个步骤：模型调用、工具执行、最终响应
```

### 组合流式传输（消息 + 更新）

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
});

// 流式传输 LLM token 和代理进度
for await (const [mode, chunk] of await agent.stream(
  { messages: [{ role: "user", content: "研究 LangChain" }] },
  { streamMode: ["updates", "messages"] }
)) {
  if (mode === "messages") {
    // LLM token 流
    const [token, metadata] = chunk;
    if (token.content) {
      process.stdout.write(token.content);
    }
  } else if (mode === "updates") {
    // 代理步骤更新
    console.log("\n步骤更新:", chunk);
  }
}
```

### 使用 Values 模式流式传输

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [weatherTool],
});

// 在每步后获取完整状态
for await (const state of await agent.stream(
  { messages: [{ role: "user", content: "天气怎么样？" }] },
  { streamMode: "values" }
)) {
  console.log("当前消息数:", state.messages.length);
  console.log("最后一条消息:", state.messages[state.messages.length - 1].content);
}
```

### 来自工具的自定义进度更新

```typescript
import { tool } from "langchain";
import { z } from "zod";

const processData = tool(
  async ({ data }, { runtime }) => {
    const total = data.length;

    for (let i = 0; i < total; i += 100) {
      // 发出自定义进度更新
      await runtime.stream_writer.write({
        type: "progress",
        data: {
          processed: i,
          total: total,
          percentage: (i / total) * 100,
        },
      });

      // 进行实际处理
      await processChunk(data.slice(i, i + 100));
    }

    return "处理完成";
  },
  {
    name: "process_data",
    description: "处理数据并提供进度更新",
    schema: z.object({
      data: z.array(z.any()),
    }),
  }
);

// 流式传输自定义更新
for await (const [mode, chunk] of await agent.stream(
  { messages: [{ role: "user", content: "处理这些数据" }] },
  { streamMode: ["custom", "updates"] }
)) {
  if (mode === "custom") {
    console.log(`进度：${chunk.data.percentage}%`);
  }
}
```

### 在 Web 应用程序中流式传输

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
});

// Express.js 端点
app.post("/api/chat", async (req, res) => {
  // 为服务器发送事件设置标头
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  try {
    for await (const [mode, chunk] of await agent.stream(
      { messages: req.body.messages },
      { streamMode: ["messages", "updates"] }
    )) {
      if (mode === "messages") {
        const [token, metadata] = chunk;
        if (token.content) {
          // 向客户端发送 token
          res.write(`data: ${JSON.stringify({ type: "token", content: token.content })}\n\n`);
        }
      } else if (mode === "updates") {
        // 向客户端发送步骤更新
        res.write(`data: ${JSON.stringify({ type: "step", data: chunk })}\n\n`);
      }
    }

    res.write("data: [DONE]\n\n");
    res.end();
  } catch (error) {
    res.write(`data: ${JSON.stringify({ type: "error", message: error.message })}\n\n`);
    res.end();
  }
});
```

### 流式传输中的错误处理

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [riskyTool],
});

try {
  for await (const chunk of await agent.stream(
    { messages: [{ role: "user", content: "执行风险操作" }] },
    { streamMode: "updates" }
  )) {
    // 检查更新中的错误
    if ("__error__" in chunk) {
      console.error("流式传输错误:", chunk.__error__);
      break;
    }

    console.log("更新:", chunk);
  }
} catch (error) {
  console.error("流式传输错误:", error);
}
```

### 带超时的流式传输

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [slowTool],
});

async function streamWithTimeout(timeoutMs: number) {
  const timeout = setTimeout(() => {
    throw new Error(`流式传输在 ${timeoutMs}ms 后超时`);
  }, timeoutMs);

  try {
    for await (const chunk of await agent.stream(
      { messages: [{ role: "user", content: "做一些慢操作" }] },
      { streamMode: "updates" }
    )) {
      clearTimeout(timeout);
      console.log(chunk);

      // 为下一个块重置超时
      timeout.setTimeout(() => {
        throw new Error(`流式传输在 ${timeoutMs}ms 后超时`);
      }, timeoutMs);
    }
  } finally {
    clearTimeout(timeout);
  }
}
```

### 缓冲 Token 以供显示

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ model: "gpt-4.1" });

let buffer = "";
const stream = await model.stream("写一篇长文章");

for await (const chunk of stream) {
  buffer += chunk.content;

  // 每 10 个字符或完整单词更新一次 UI
  if (buffer.length >= 10 || chunk.content.includes(" ")) {
    console.log(buffer);
    buffer = "";
  }
}

// 刷新剩余缓冲区
if (buffer) {
  console.log(buffer);
}
```

## 边界

### 您可以配置什么

✅ **流式模式**：选择要流式传输的数据
✅ **多个模式**：结合不同的流式类型
✅ **自定义更新**：发出用户定义的进度数据
✅ **块处理**：根据需要处理每个块
✅ **错误处理**：捕获和处理流式传输错误

### 您不能配置什么

❌ **块大小**：由模型/提供商确定
❌ **块时间**：提供商发送时到达
❌ **保证顺序**：异步流可能不同
❌ **修改过去的块**：块是不可变的

## 注意事项

### 1. 未等待流式传输

```typescript
// ❌ 问题：缺少 await
const stream = agent.stream(input, { streamMode: "updates" });
for await (const chunk of stream) {  // 错误：stream 是 Promise！
  console.log(chunk);
}

// ✅ 解决方案：等待流式传输初始化
const stream = await agent.stream(input, { streamMode: "updates" });
for await (const chunk of stream) {
  console.log(chunk);
}
```

### 2. 错误地访问内容

```typescript
// ❌ 问题：messages 模式的错误属性
for await (const chunk of await agent.stream(input, { streamMode: "messages" })) {
  console.log(chunk.content);  // undefined！
}

// ✅ 解决方案：messages 模式返回 [token, metadata] 元组
for await (const chunk of await agent.stream(input, { streamMode: "messages" })) {
  const [token, metadata] = chunk;
  console.log(token.content);  // 正确！
}
```

### 3. 流式模式混淆

```typescript
// ❌ 问题：使用错误的模式进行 token 流式传输
for await (const chunk of await agent.stream(input, { streamMode: "updates" })) {
  console.log(chunk.content);  // 不是 updates 的工作方式！
}

// ✅ 解决方案：使用 "messages" 模式进行 token 流式传输
for await (const chunk of await agent.stream(input, { streamMode: "messages" })) {
  const [token, metadata] = chunk;
  console.log(token.content);
}
```

### 4. 提前退出流式传输

```typescript
// ❌ 问题：没有正确清理
for await (const chunk of await agent.stream(input)) {
  if (someCondition) {
    break;  // 流式传输可能无法正确清理
  }
}

// ✅ 解决方案：使用 try/finally 或显式清理
const stream = await agent.stream(input);
try {
  for await (const chunk of stream) {
    if (someCondition) {
      break;
    }
  }
} finally {
  // 如果需要，进行清理
}
```

### 5. 混合流式模式

```typescript
// ❌ 问题：未处理不同的模式
for await (const chunk of await agent.stream(
  input,
  { streamMode: ["updates", "messages"] }
)) {
  console.log(chunk);  // 这是哪种模式？
}

// ✅ 解决方案：解构模式
for await (const [mode, chunk] of await agent.stream(
  input,
  { streamMode: ["updates", "messages"] }
)) {
  if (mode === "messages") {
    const [token, metadata] = chunk;
    console.log(token.content);
  } else if (mode === "updates") {
    console.log("步骤:", chunk);
  }
}
```

## 文档链接

- [流式传输概述](https://docs.langchain.com/oss/javascript/langchain/streaming/overview)
- [LangGraph 流式传输](https://docs.langchain.com/oss/javascript/langgraph/streaming)
- [模型流式传输](https://docs.langchain.com/oss/javascript/langchain/models)
- [人工在环流式传输](https://docs.langchain.com/oss/javascript/langchain/human-in-the-loop)
