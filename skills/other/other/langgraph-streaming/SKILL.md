---
name: langgraph-streaming
description: 从 LangGraph 流式传输实时更新：流式模式（values、updates、messages、custom、debug）用于响应式 UX
language: js
---

# langgraph-streaming (JavaScript/TypeScript)

---
name: langgraph-streaming
description: 从 LangGraph 流式传输实时更新 - 流式模式（values、updates、messages、custom、debug）用于响应式 UX
---

## 概述

LangGraph 的流式系统在图执行期间输出实时更新，对于响应式 LLM 应用程序至关重要。可以在生成时流式传输图状态、LLM 令牌或自定义数据。

## 决策表：流式模式

| 模式 | 流式传输的内容 | 使用场景 |
|------|----------------|----------|
| `values` | 每步后的完整状态 | 监控完整状态变化 |
| `updates` | 每步后的状态增量 | 跟踪增量更新 |
| `messages` | LLM 令牌 + 元数据 | 聊天 UI、令牌流式传输 |
| `custom` | 用户定义的数据 | 进度指示器、日志 |
| `debug` | 所有执行详情 | 调试、详细跟踪 |

## 代码示例

### 流式传输状态值

```typescript
import { StateGraph, START, END } from "@langchain/langgraph";

const process = async (state) => ({  count: state.count + 1 });

const graph = new StateGraph(State)
  .addNode("process", process)
  .addEdge(START, "process")
  .addEdge("process", END)
  .compile();

// 每步后流式传输完整状态
for await (const chunk of await graph.stream(
  { count: 0 },
  { streamMode: "values" }
)) {
  console.log(chunk);  // { count: 0 }, 然后 { count: 1 }
}
```

### 流式传输状态更新（增量）

```typescript
// 只流式传输变化
for await (const chunk of await graph.stream(
  { count: 0 },
  { streamMode: "updates" }
)) {
  console.log(chunk);  // { process: { count: 1 } }
}
```

### 流式传输 LLM 令牌

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "@langchain/core/messages";

const model = new ChatOpenAI({ model: "gpt-4" });

const llmNode = async (state) => {
  const response = await model.invoke(state.messages);
  return { messages: [response] };
};

const graph = new StateGraph(State)
  .addNode("llm", llmNode)
  .compile();

// 在生成时流式传输 LLM 令牌
for await (const chunk of await graph.stream(
  { messages: [new HumanMessage("Hello")] },
  { streamMode: "messages" }
)) {
  const [token, metadata] = chunk;
  if (token.content) {
    process.stdout.write(token.content);
  }
}
```

### 流式传输自定义数据

```typescript
import { LangGraphRunnableConfig } from "@langchain/langgraph";

const myNode = async (state, config: LangGraphRunnableConfig) => {
  const writer = config.writer;

  // 输出自定义更新
  writer?.("Processing step 1...");
  // 执行工作
  writer?.("Processing step 2...");
  // 更多工作
  writer?.("Complete!");

  return { result: "done" };
};

const graph = new StateGraph(State)
  .addNode("work", myNode)
  .compile();

for await (const chunk of await graph.stream(
  { data: "test" },
  { streamMode: "custom" }
)) {
  console.log(chunk);  // "Processing step 1...", 等
}
```

### 多种流式模式

```typescript
// 同时流式传输多种模式
for await (const [mode, chunk] of await graph.stream(
  { messages: [new HumanMessage("Hi")] },
  { streamMode: ["updates", "messages", "custom"] }
)) {
  console.log(`${mode}:`, chunk);
}
```

### 带子图的流式传输

```typescript
// 包含子图输出
for await (const chunk of await graph.stream(
  { data: "test" },
  {
    streamMode: "updates",
    subgraphs: true  // 也从嵌套图流式传输
  }
)) {
  console.log(chunk);
}
```

### 带中断的流式传输

```typescript
const config = {
  configurable: { thread_id: "1" },
  streamMode: ["messages", "updates"] as const,
  subgraphs: true
};

for await (const [metadata, mode, chunk] of await graph.stream(
  { query: "test" },
  config
)) {
  if (mode === "messages") {
    // 处理流式传输的 LLM 内容
    const [msg, _] = chunk;
    if (msg.content) {
      process.stdout.write(msg.content);
    }
  } else if (mode === "updates") {
    // 检查中断
    if ("__interrupt__" in chunk) {
      // 处理中断
      const interruptInfo = chunk.__interrupt__[0].value;
      // 获取用户输入并恢复
      break;
    }
  }
}
```

## 边界

### 您能够配置的

✅ 选择流式模式
✅ 同时流式传输多种模式
✅ 从节点输出自定义数据
✅ 从子图流式传输
✅ 将流式传输与中断结合

### 您不能配置的

❌ 修改流式传输协议
❌ 更改创建检查点的时机
❌ 更改令牌流式传输格式

## 注意事项

### 1. Messages 模式需要 LLM 调用

```typescript
// ❌ 错误 - 没有调用 LLM，没有流式传输
const node = async (state) => ({ output: "static text" });

for await (const chunk of await graph.stream({}, { streamMode: "messages" })) {
  console.log(chunk);  // 什么都没有!
}

// ✅ 正确 - 调用 LLM
const node = async (state) => {
  const response = await model.invoke(state.messages);  // LLM 调用
  return { messages: [response] };
};
```

### 2. 自定义模式需要 Writer

```typescript
// ❌ 错误 - 没有 writer，没有流式传输
const node = async (state) => {
  console.log("Processing...");  // 没有流式传输!
  return { data: "done" };
};

// ✅ 正确
import { LangGraphRunnableConfig } from "@langchain/langgraph";

const node = async (state, config: LangGraphRunnableConfig) => {
  config.writer?.("Processing...");  // 流式传输!
  return { data: "done" };
};
```

### 3. 流式模式是数组

```typescript
// ❌ 错误 - 单个字符串带逗号
await graph.stream({}, { streamMode: "updates, messages" });

// ✅ 正确 - 数组
await graph.stream({}, { streamMode: ["updates", "messages"] });
```

### 4. 始终 Await Stream

```typescript
// ❌ 错误 - 缺少 await
const stream = graph.stream({});
for await (const chunk of stream) {  // 错误!
  console.log(chunk);
}

// ✅ 正确
for await (const chunk of await graph.stream({})) {
  console.log(chunk);
}
```

## 相关链接

- [流式传输指南](https://docs.langchain.com/oss/javascript/langgraph/streaming)
- [流式模式](https://docs.langchain.com/oss/javascript/langgraph/streaming#supported-stream-modes)
