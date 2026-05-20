---
name: langgraph-overview
description: 理解 LangGraph：用于构建有状态、长期运行 Agent 的低级编排框架，具有持久执行、流式传输和人机交互能力
language: js
---

# langgraph-overview (JavaScript/TypeScript)

---
name: langgraph-overview
description: 理解 LangGraph - 用于构建有状态、长期运行 Agent 的低级编排框架，具有持久执行、流式传输和人机交互能力
---

## 概述

LangGraph 是一个低级编排框架和运行时，用于构建、管理和部署长期运行的、有状态的 Agent。它受到 Klarna、Replit 和 Elastic 等公司的信任，用于生产 Agent 工作负载。

**关键特性：**
- **低级控制**：直接控制 Agent 编排，无需高级抽象
- **有状态执行**：内置状态管理和持久化
- **生产就绪**：持久执行、流式传输、人机交互和容错能力
- **框架无关**：可独立使用或与 LangChain 组件配合使用

### 何时使用 LangGraph

LangGraph 非常适合当您需要：
- 对 Agent 编排的细粒度控制
- 长期、有状态 Agent 的持久执行
- 结合确定性和 Agent 步骤的复杂工作流
- Agent 部署的生产基础设施
- 人机交互工作流
- 多次交互间的持久状态

### 何时不使用 LangGraph

当您满足以下条件时考虑替代方案：
- 需要使用预构建架构快速开始 → 使用 **LangChain agents**
- 希望使用包含完整功能（自动压缩、虚拟文件系统）→ 使用 **Deep Agents**
- 有简单的、无状态的 LLM 工作流 → 使用 **LangChain LCEL**
- 不需要状态持久化或复杂编排

## 决策表：选择正确的工具

| 需求 | 使用 LangGraph | 使用 LangChain | 使用 Deep Agents |
|------------|---------------|---------------|-----------------|
| 快速原型开发 | ❌ | ✅ | ✅ |
| 自定义编排逻辑 | ✅ | ❌ | ⚠️ (有限) |
| 持久执行 | ✅ | ⚠️ (通过 LangGraph) | ✅ |
| 人机交互 | ✅ | ⚠️ (通过 LangGraph) | ✅ |
| 状态持久化 | ✅ | ❌ | ✅ |
| 生产部署 | ✅ | ⚠️ (与 LangGraph 一起使用) | ✅ |
| 学习曲线 | 高 | 低 | 中 |

## 核心概念

### 1. 基于图的执行模型

LangGraph 将 Agent 工作流建模为**图**，具有三个核心组件：

- **状态（State）**：表示应用程序当前快照的共享数据结构
- **节点（Nodes）**：编码 Agent 逻辑并更新状态的函数
- **边（Edges）**：决定下一个执行哪个节点（可以是有条件的或固定的）

### 2. 核心能力

| 能力 | 描述 |
|-----------|-------------|
| **持久执行** | Agent 在故障中持久存在并从检查点恢复 |
| **流式传输** | 执行期间的实时更新（状态、令牌、自定义数据） |
| **人机交互** | 暂停执行以供人工审查和干预 |
| **持久化** | 线程级别和跨线程的状态管理 |
| **时间旅行** | 从执行历史中的任何检查点恢复 |

### 3. 消息传递模型

受 Google 的 Pregel 系统启发：
- 执行以离散的"超级步"进行
- 节点在超级步内并行执行
- 顺序节点属于不同的超级步
- 当所有节点不活跃时图终止

## 代码示例

### 基本 LangGraph Agent

```typescript
import { ChatAnthropic } from "@langchain/anthropic";
import { tool } from "@langchain/core/tools";
import { SystemMessage, HumanMessage, AIMessage, ToolMessage } from "@langchain/core/messages";
import { StateGraph, StateSchema, MessagesValue, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

// 1. 定义工具
const multiply = tool(({ a, b }) => a * b, {
  name: "multiply",
  description: "Multiply two numbers",
  schema: z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  }),
});

const add = tool(({ a, b }) => a + b, {
  name: "add",
  description: "Add two numbers",
  schema: z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  }),
});

// 2. 使用工具初始化模型
const model = new ChatAnthropic({
  model: "claude-sonnet-4-5-20250929",
  temperature: 0,
});

const toolsByName = { [add.name]: add, [multiply.name]: multiply };
const tools = Object.values(toolsByName);
const modelWithTools = model.bindTools(tools);

// 3. 定义状态
const MessagesState = new StateSchema({
  messages: MessagesValue,
  llmCalls: new ReducedValue(
    z.number().default(0),
    { reducer: (x, y) => x + y }
  ),
});

// 4. 定义节点
const llmCall = async (state) => {
  const response = await modelWithTools.invoke([
    new SystemMessage("You are a helpful assistant."),
    ...state.messages,
  ]);
  return {
    messages: [response],
    llmCalls: 1,
  };
};

const toolNode = async (state) => {
  const lastMessage = state.messages.at(-1);

  if (lastMessage == null || !AIMessage.isInstance(lastMessage)) {
    return { messages: [] };
  }

  const result = [];
  for (const toolCall of lastMessage.tool_calls ?? []) {
    const tool = toolsByName[toolCall.name];
    const observation = await tool.invoke(toolCall);
    result.push(observation);
  }
  return { messages: result };
};

// 5. 定义路由逻辑
const shouldContinue = (state) => {
  const lastMessage = state.messages.at(-1);

  if (!lastMessage || !AIMessage.isInstance(lastMessage)) {
    return END;
  }

  if (lastMessage.tool_calls?.length) {
    return "toolNode";
  }
  return END;
};

// 6. 构建和编译图
const agent = new StateGraph(MessagesState)
  .addNode("llmCall", llmCall)
  .addNode("toolNode", toolNode)
  .addEdge(START, "llmCall")
  .addConditionalEdges("llmCall", shouldContinue, ["toolNode", END])
  .addEdge("toolNode", "llmCall")
  .compile();

// 7. 调用 agent
const result = await agent.invoke({
  messages: [new HumanMessage("What is 3 * 4?")],
});

for (const message of result.messages) {
  console.log(`[${message._getType()}]: ${message.content}`);
}
```

### 带持久化的 Agent

```typescript
import { MemorySaver } from "@langchain/langgraph";

// 创建检查点器用于状态持久化
const checkpointer = new MemorySaver();

// 使用检查点器编译
const agent = new StateGraph(MessagesState)
  .addNode("llmCall", llmCall)
  .addNode("toolNode", toolNode)
  .addEdge(START, "llmCall")
  .addConditionalEdges("llmCall", shouldContinue, ["toolNode", END])
  .addEdge("toolNode", "llmCall")
  .compile({ checkpointer });  // 添加检查点器

// 第一轮对话
const config = { configurable: { thread_id: "1" } };
await agent.invoke(
  { messages: [new HumanMessage("Hi, I'm Alice")] },
  config
);

// 第二轮 - agent 记住上下文
await agent.invoke(
  { messages: [new HumanMessage("What's my name?")] },
  config
);
```

### 流式传输 Agent 响应

```typescript
// 流式传输状态更新
for await (const chunk of await agent.stream(
  { messages: [new HumanMessage("Calculate 5 + 3")] },
  { streamMode: "updates" }
)) {
  console.log(chunk);
}

// 流式传输 LLM 令牌
for await (const chunk of await agent.stream(
  { messages: [new HumanMessage("Hello!")] },
  { streamMode: "messages" }
)) {
  console.log(chunk);
}

// 多种流式模式
for await (const [mode, chunk] of await agent.stream(
  { messages: [new HumanMessage("Help me")] },
  { streamMode: ["updates", "messages"] }
)) {
  console.log(`${mode}:`, chunk);
}
```

## 边界

### Agent 能够配置/控制的

✅ **节点逻辑**：将任何异步函数定义为节点
✅ **状态模式**：自定义状态结构和 reducer
✅ **控制流**：添加条件边、循环、分支
✅ **持久化层**：选择检查点器（MemorySaver、SQLite、Postgres）
✅ **流式模式**：配置要流式传输的数据
✅ **中断**：在任何点添加人机交互
✅ **递归限制**：控制最大执行步数
✅ **工具和模型**：使用任何 LLM 或工具提供程序

### Agent 不能配置/控制的

❌ **核心图执行模型**：基于 Pregel 的运行时是固定的
❌ **超级步行为**：无法更改节点的批处理方式
❌ **消息传递协议**：内部通信是预定义的
❌ **检查点模式**：内部检查点格式是固定的
❌ **图编译**：无法修改编译逻辑

## 注意事项

### 1. 持久化需要 Thread ID

```typescript
// ❌ 错误 - 使用检查点器但没有 thread_id
await agent.invoke({ messages: [...] });  // 状态未持久化!

// ✅ 正确 - 始终提供 thread_id
await agent.invoke(
  { messages: [...] },
  { configurable: { thread_id: "user-123" } }
);
```

### 2. 状态更新需要适当的 Reducer

```typescript
// ❌ 错误 - 消息将被覆盖，而不是追加
const BadState = new StateSchema({
  messages: z.array(BaseMessageSchema),  // 没有 reducer!
});

// ✅ 正确 - 使用 MessagesValue 进行自动消息处理
import { MessagesValue } from "@langchain/langgraph";

const GoodState = new StateSchema({
  messages: MessagesValue,  // 正确处理消息更新
});
```

### 3. 使用前必须编译

```typescript
// ❌ 错误 - StateGraph 不可执行
const builder = new StateGraph(State).addNode("node", func);
await builder.invoke(...);  // 错误!

// ✅ 正确 - 必须先编译
const graph = builder.compile();
await graph.invoke(...);
```

### 4. 无限循环需要终止

```typescript
// ❌ 错误 - 没有退出条件的循环
builder
  .addEdge("nodeA", "nodeB")
  .addEdge("nodeB", "nodeA");  // 无限循环!

// ✅ 正确 - 添加到 END 的条件边
const shouldContinue = (state) => {
  if (state.count > 10) {
    return END;
  }
  return "nodeB";
};

builder.addConditionalEdges("nodeA", shouldContinue);
```

### 5. 需要 Async/Await

```typescript
// ❌ 错误 - 忘记 await
const result = agent.invoke(...);  // 返回 Promise!
console.log(result.messages);  // undefined

// ✅ 正确 - 始终 await
const result = await agent.invoke(...);
console.log(result.messages);  // 可以工作!
```

## 安装

```bash
# npm
npm install @langchain/langgraph

# yarn
yarn add @langchain/langgraph

# pnpm
pnpm add @langchain/langgraph

# 与 LangChain 一起使用（可选但常见）
npm install @langchain/core

# 生产持久化
npm install @langchain/langgraph-checkpoint-postgres
```

## 相关链接

- [LangGraph 概览 (JavaScript)](https://docs.langchain.com/oss/javascript/langgraph/overview)
- [LangGraph 快速入门](https://docs.langchain.com/oss/javascript/langgraph/quickstart)
- [图 API 参考](https://docs.langchain.com/oss/javascript/langgraph/graph-api)
- [持久化指南](https://docs.langchain.com/oss/javascript/langgraph/persistence)
- [流式传输指南](https://docs.langchain.com/oss/javascript/langgraph/streaming)
- [LangGraph v1 发布说明](https://docs.langchain.com/oss/javascript/releases/langgraph-v1)
