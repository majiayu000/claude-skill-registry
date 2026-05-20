---
name: langchain-agents
description: Create and use LangChain agents with createAgent - includes agent loops, ReAct pattern, tool execution, and state management
language: js
---

# langchain-agents (JavaScript/TypeScript)

## 概述

代理（Agents）结合语言模型和工具来创建可以推理任务、决定使用哪些工具并迭代地朝着解决方案工作的系统。`createAgent()` 函数提供了基于 LangGraph 构建的生产就绪的代理实现。

**核心概念：**
- **代理循环（Agent Loop）**：模型决定 → 调用工具 → 观察结果 → 重复直到完成
- **ReAct 模式**：推理和行动（Reasoning and Acting）- 代理推理要做什么，然后通过调用工具来行动
- **基于图的运行时**：代理在具有节点（模型、工具、中间件）和边的 LangGraph 图上运行

## 何时使用代理

| 场景 | 使用代理？ | 原因 |
|----------|-----------|-----|
| 需要调用外部 API/数据库 | ✅ 是 | 代理可以动态选择调用哪些工具 |
| 有决策点的多步骤任务 | ✅ 是 | 代理循环处理迭代推理 |
| 简单的提示-响应 | ❌ 否 | 直接使用聊天模型 |
| 预定义的工作流 | ❌ 否 | 改用 LangGraph 工作流 |
| 需要工具调用但不迭代 | ⚠️ 可能 | 考虑直接使用 model.bindTools() |

## 决策表

### 选择代理配置

| 需求 | 配置 | 示例 |
|------|---------------|---------|
| 带工具的基本代理 | `createAgent({ model, tools })` | 搜索、计算器、天气 |
| 自定义系统指令 | 添加 `systemPrompt` | 特定领域的行为 |
| 敏感操作的人工批准 | 添加 `humanInTheLoopMiddleware` | 数据库写入、电子邮件 |
| 跨会话持久化 | 添加 `checkpointer` | 多轮对话 |
| 结构化输出格式 | 添加 `responseFormat` | 提取联系信息、解析表单 |

### 工具策略

| 工具类型 | 何时使用 | 示例 |
|-----------|-------------|---------|
| 静态工具 | 工具在执行期间不变 | 搜索、天气、计算器 |
| 动态工具 | 工具依赖于运行时状态 | 用户特定的 API |
| 内置工具 | 需要常用功能 | 文件系统、代码执行 |
| 自定义工具 | 特定于领域的操作 | 您的业务逻辑 |

## 代码示例

### 带工具的基本代理

```typescript
import { createAgent } from "langchain";
import { tool } from "langchain";

// 定义工具
const searchTool = tool(
  async ({ query }: { query: string }) => {
    // 您的搜索实现
    return `${query} 的搜索结果`;
  },
  {
    name: "search",
    description: "在网络上搜索信息",
    schema: z.object({
      query: z.string().describe("搜索查询"),
    }),
  }
);

const weatherTool = tool(
  async ({ location }: { location: string }) => {
    return `${location} 的天气：晴，72°F`;
  },
  {
    name: "get_weather",
    description: "获取某个地点的当前天气",
    schema: z.object({
      location: z.string().describe("城市名称"),
    }),
  }
);

// 创建代理
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, weatherTool],
});

// 调用代理
const result = await agent.invoke({
  messages: [
    { role: "user", content: "旧金山的天气怎么样？" }
  ],
});

console.log(result.messages[result.messages.length - 1].content);
```

### 带系统提示的代理

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, calculatorTool],
  systemPrompt: `您是一个有用的研究助手。
使用搜索工具时始终引用您的来源。
执行计算时展示您的工作过程。`,
});
```

### 代理循环执行流程

```typescript
// 代理在循环中运行：
// 1. 模型接收用户消息
// 2. 模型决定调用工具（或完成）
// 3. 工具执行并返回结果
// 4. 结果返回给模型
// 5. 重复直到模型决定完成

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, weatherTool],
});

// 这个单个 invoke() 调用处理整个循环
const result = await agent.invoke({
  messages: [
    {
      role: "user",
      content: "搜索法国的首都，然后获取其天气"
    }
  ],
});

// 代理自动：
// - 调用搜索工具查找首都
// - 接收 "巴黎"
// - 调用巴黎的天气工具
// - 接收天气数据
// - 用最终答案响应
```

### 流式传输代理进度

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
});

// 使用 updates 模式流式传输以查看每个步骤
for await (const chunk of await agent.stream(
  { messages: [{ role: "user", content: "搜索 LangChain" }] },
  { streamMode: "updates" }
)) {
  console.log("步骤:", chunk);
}

// 使用 messages 模式流式传输 LLM token
for await (const chunk of await agent.stream(
  { messages: [{ role: "user", content: "搜索 LangChain" }] },
  { streamMode: "messages" }
)) {
  const [token, metadata] = chunk;
  if (token.content) {
    process.stdout.write(token.content);
  }
}
```

### 带持久化的代理

```typescript
import { createAgent } from "langchain";
import { MemorySaver } from "@langchain/langgraph";

const checkpointer = new MemorySaver();

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
  checkpointer,
});

// 第一次对话
const config = { configurable: { thread_id: "user-123" } };
await agent.invoke({
  messages: [{ role: "user", content: "我的名字是 Alice" }]
}, config);

// 后续对话 - 代理记得
await agent.invoke({
  messages: [{ role: "user", content: "我的名字是什么？" }]
}, config);
// 响应："您的名字是 Alice"
```

### 并行调用多个工具

```typescript
// 模型可以同时调用多个工具
const agent = createAgent({
  model: "gpt-4.1",
  tools: [weatherTool, newsToolTool],
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "获取纽约的天气和旧金山的最新新闻"
  }],
});

// 代理可能会在单个步骤中并行调用两个工具
```

### 动态工具（依赖于运行时）

```typescript
import { createAgent } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: (state) => {
    // 工具可以依赖于当前状态
    const userId = state.config?.configurable?.user_id;
    return [
      getUserSpecificTool(userId),
      commonTool,
    ];
  },
});
```

### 代理中的错误处理

```typescript
import { createAgent, wrapToolCall } from "langchain";

// 自定义错误处理中间件
const errorHandler = wrapToolCall({
  name: "ErrorHandler",
  wrapToolCall: async (toolCall, handler) => {
    try {
      return await handler(toolCall);
    } catch (error) {
      return {
        ...toolCall,
        content: `工具错误：${error.message}`,
      };
    }
  },
});

const agent = createAgent({
  model: "gpt-4.1",
  tools: [riskyTool],
  middleware: [errorHandler],
});
```

## 边界

### 代理可以配置什么

✅ **模型**：任何聊天模型（OpenAI、Anthropic、Google 等）
✅ **工具**：自定义工具、内置工具、动态工具
✅ **系统提示**：代理行为的指令
✅ **中间件**：人工在环、错误处理、日志记录
✅ **检查点**：跨对话的内存/持久化
✅ **响应格式**：结构化输出模式
✅ **最大迭代次数**：防止无限循环

### 代理不能配置什么

❌ **直接图结构**：直接使用 LangGraph 进行自定义流程
❌ **工具执行顺序**：模型决定调用哪些工具
❌ **中断模型决策**：只能在工具执行前中断
❌ **多个模型**：一个代理 = 一个模型（使用子代理实现多个）

## 注意事项

### 1. 代理不停止（无限循环）

```typescript
// ❌ 问题：没有明确的停止条件
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
});

await agent.invoke({
  messages: [{ role: "user", content: "持续搜索直到完美" }]
});

// ✅ 解决方案：设置最大迭代次数
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
  maxIterations: 10, // 在 10 次工具调用后停止
});
```

### 2. 工具未被调用

```typescript
// ❌ 问题：模糊的工具描述
const badTool = tool(
  async ({ input }: { input: string }) => "result",
  {
    name: "tool",
    description: "做些事情", // 太模糊了！
    schema: z.object({ input: z.string() }),
  }
);

// ✅ 解决方案：清晰、具体的描述
const goodTool = tool(
  async ({ query }: { query: string }) => "result",
  {
    name: "web_search",
    description: "在网络上搜索关于某个主题的当前信息。当您需要训练中没有的最新数据时使用此工具。",
    schema: z.object({
      query: z.string().describe("搜索查询（2-10 个词）"),
    }),
  }
);
```

### 3. 状态未持久化

```typescript
// ❌ 问题：没有检查点
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
});

// 每次 invoke 都是隔离的 - 没有内存
await agent.invoke({ messages: [{ role: "user", content: "嗨，我是 Bob" }] });
await agent.invoke({ messages: [{ role: "user", content: "我的名字是什么？" }] });
// 代理不记得 "Bob"

// ✅ 解决方案：添加检查点和 thread_id
import { MemorySaver } from "@langchain/langgraph";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
  checkpointer: new MemorySaver(),
});

const config = { configurable: { thread_id: "session-1" } };
await agent.invoke({ messages: [{ role: "user", content: "嗨，我是 Bob" }] }, config);
await agent.invoke({ messages: [{ role: "user", content: "我的名字是什么？" }] }, config);
// 代理记得："您的名字是 Bob"
```

### 4. 消息与状态混淆

```typescript
// 代理状态包含不仅仅是消息
const result = await agent.invoke({
  messages: [{ role: "user", content: "你好" }]
});

// ✅ 访问完整的对话历史
console.log(result.messages); // 所有消息的数组

// ✅ 访问结构化输出（如果配置了）
console.log(result.structuredResponse);

// ❌ 不要尝试直接访问 result.content
// console.log(result.content); // undefined！
```

### 5. 工具结果必须是可序列化的

```typescript
// ❌ 问题：返回不可序列化的对象
const badTool = tool(
  async () => {
    return new Date(); // Date 对象默认情况下不是 JSON 可序列化的
  },
  { name: "get_time", description: "获取当前时间" }
);

// ✅ 解决方案：返回可序列化的数据
const goodTool = tool(
  async () => {
    return new Date().toISOString(); // 字符串是可序列化的
  },
  { name: "get_time", description: "获取当前时间" }
);
```

### 6. 流式模式很重要

```typescript
// 不同的流式模式显示不同的信息

// "values" - 每步后的完整状态
for await (const chunk of await agent.stream(input, { streamMode: "values" })) {
  console.log(chunk.messages); // 到目前为止的所有消息
}

// "updates" - 仅每步中变化的内容
for await (const chunk of await agent.stream(input, { streamMode: "updates" })) {
  console.log(chunk); // 仅仅是增量
}

// "messages" - LLM token 流
for await (const chunk of await agent.stream(input, { streamMode: "messages" })) {
  const [token, metadata] = chunk;
  console.log(token.content); // 每个 token
}
```

## 文档链接

- [代理概述](https://docs.langchain.com/oss/javascript/langchain/agents)
- [createAgent API 参考](https://docs.langchain.com/oss/javascript/releases/langchain-v1)
- [LangGraph 概念](https://docs.langchain.com/oss/javascript/langgraph/workflows-agents)
- [工具调用指南](https://docs.langchain.com/oss/javascript/langchain/tools)
- [流式传输指南](https://docs.langchain.com/oss/javascript/langchain/streaming/overview)
- [人工在环](https://docs.langchain.com/oss/javascript/langchain/human-in-the-loop)
