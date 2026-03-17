---
name: langchain-tool-calling
description: 聊天模型如何调用工具 - 包括 bindTools、工具选择策略、并行工具调用和工具消息处理
language: js
---

# langchain-tool-calling (JavaScript/TypeScript)

## 概述

工具调用允许聊天模型请求执行外部函数。模型根据用户输入决定调用哪些工具，然后将结果传回模型以进行进一步推理。这是代理行为的基础。

**核心概念：**
- **bindTools()**：将工具绑定到模型
- **工具调用**：模型请求执行工具（在 AIMessage.tool_calls 中）
- **工具消息**：传回模型的结果（ToolMessage）
- **工具选择**：控制模型可以使用的工具

## 何时使用工具调用

| 场景 | 使用工具调用？ | 原因 |
|----------|------------------|------|
| 需要外部数据（API、数据库） | ✅ 是 | 模型无法直接访问外部数据 |
| 带操作的多步推理 | ✅ 是 | 模型根据结果决定下一步操作 |
| 简单问答 | ❌ 否 | 不需要工具 |
| 预定工作流 | ⚠️ 可能 | 考虑模型是否需要决定步骤 |

## 决策表

### 工具选择策略

| 策略 | 使用时机 | 示例 |
|----------|-------------|---------|
| `"auto"`（默认） | 模型决定是否/使用哪个工具 | 通用目的 |
| `"any"` | 强制模型使用至少一个工具 | 提取、分类 |
| `"tool_name"` | 强制特定工具 | 当您知道需要哪个工具时 |
| `"none"` | 防止工具使用 | 工具执行后 |

### 处理工具调用

| 模式 | 使用时机 | 示例 |
|---------|-------------|---------|
| 手动执行 | 代理外部 | 测试、自定义工作流 |
| 代理循环 | 生产使用 | createAgent 自动处理 |
| 并行执行 | 多个独立工具 | 天气 + 新闻查询 |

## 代码示例

### 基本工具调用

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "langchain";
import { z } from "zod";

// 定义工具
const getWeather = tool(
  async ({ location }: { location: string }) => {
    return `${location}的天气：晴天，72°F`;
  },
  {
    name: "get_weather",
    description: "获取位置的当前天气",
    schema: z.object({
      location: z.string().describe("城市名称"),
    }),
  }
);

// 将工具绑定到模型
const model = new ChatOpenAI({ model: "gpt-4.1" });
const modelWithTools = model.bindTools([getWeather]);

// 模型将决定调用工具
const response = await modelWithTools.invoke(
  "旧金山的天气怎么样？"
);

// 检查模型是否调用了工具
console.log(response.tool_calls);
// [{
//   name: "get_weather",
//   args: { location: "San Francisco" },
//   id: "call_abc123"
// }]
```

### 手动执行工具调用

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "langchain";
import { ToolMessage } from "langchain";

const getTool = tool(
  async ({ location }) => `${location}的天气：晴天`,
  {
    name: "get_weather",
    description: "获取天气",
    schema: z.object({ location: z.string() }),
  }
);

const model = new ChatOpenAI({ model: "gpt-4.1" });
const modelWithTools = model.bindTools([getTool]);

// 步骤 1：模型决定调用工具
const messages = [{ role: "user", content: "纽约的天气怎么样？" }];
const response1 = await modelWithTools.invoke(messages);

// 步骤 2：执行工具
const toolResults = [];
for (const toolCall of response1.tool_calls || []) {
  const result = await getTool.invoke(toolCall);
  toolResults.push(result); // 这是一个 ToolMessage
}

// 步骤 3：将结果传回模型
messages.push(response1); // 添加带有工具调用的 AI 消息
messages.push(...toolResults); // 添加工具结果

const response2 = await modelWithTools.invoke(messages);
console.log(response2.content); // 使用工具结果的最终答案
```

### 工具选择：强制工具使用

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "langchain";

const extractInfo = tool(
  async ({ name, email }) => ({ name, email }),
  {
    name: "extract_info",
    description: "提取姓名和邮箱",
    schema: z.object({
      name: z.string(),
      email: z.string(),
    }),
  }
);

const model = new ChatOpenAI({ model: "gpt-4.1" });

// 强制模型使用此特定工具
const modelWithTools = model.bindTools([extractInfo], {
  tool_choice: "extract_info", // 必须使用此工具
});

const response = await modelWithTools.invoke(
  "联系人：John Doe (john@example.com)"
);

// 模型总是调用 extract_info
console.log(response.tool_calls[0].args);
// { name: "John Doe", email: "john@example.com" }
```

### 工具选择：强制任意工具

```typescript
// 强制模型使用至少一个工具（任意一个）
const modelWithTools = model.bindTools(
  [tool1, tool2, tool3],
  { tool_choice: "any" }
);

// 模型必须调用至少一个工具，不能仅用文本响应
const response = await modelWithTools.invoke("处理这些数据");
```

### 并行工具调用

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "langchain";

const getWeather = tool(
  async ({ location }) => `${location}的天气：晴天`,
  {
    name: "get_weather",
    description: "获取天气",
    schema: z.object({ location: z.string() }),
  }
);

const getNews = tool(
  async ({ topic }) => `关于${topic}的最新新闻`,
  {
    name: "get_news",
    description: "获取新闻",
    schema: z.object({ topic: z.string() }),
  }
);

const model = new ChatOpenAI({ model: "gpt-4.1" });
const modelWithTools = model.bindTools([getWeather, getNews]);

const response = await modelWithTools.invoke(
  "获取纽约的天气和关于 AI 的新闻"
);

// 模型可能并行调用两个工具
console.log(response.tool_calls);
// [
//   { name: "get_weather", args: { location: "NYC" }, id: "call_1" },
//   { name: "get_news", args: { topic: "AI" }, id: "call_2" }
// ]
```

### 工具消息结构

```typescript
import { ToolMessage } from "langchain";

// 工具消息链接回请求它们的工具调用
const toolMessage = new ToolMessage({
  content: "巴黎的天气：晴天，72°F",
  tool_call_id: "call_abc123", // 必须匹配 AIMessage tool_call id
  name: "get_weather", // 工具名称
});

// 或通过 tool.invoke() 自动创建
const result = await getTool.invoke({
  name: "get_weather",
  args: { location: "Paris" },
  id: "call_abc123",
});
// result 是具有正确结构的 ToolMessage
```

### 处理工具错误

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "langchain";
import { ToolMessage } from "langchain";

const riskyTool = tool(
  async ({ data }) => {
    if (!data) throw new Error("缺少数据");
    return "成功";
  },
  {
    name: "risky_tool",
    description: "可能失败的工具",
    schema: z.object({ data: z.string().optional() }),
  }
);

const model = new ChatOpenAI({ model: "gpt-4.1" });
const modelWithTools = model.bindTools([riskyTool]);

const response = await modelWithTools.invoke("处理这个");

// 带错误处理执行工具
const toolResults = [];
for (const toolCall of response.tool_calls || []) {
  try {
    const result = await riskyTool.invoke(toolCall);
    toolResults.push(result);
  } catch (error) {
    // 将错误作为工具消息返回
    toolResults.push(
      new ToolMessage({
        content: `错误：${error.message}`,
        tool_call_id: toolCall.id,
        name: toolCall.name,
      })
    );
  }
}
```

### 提供商特定的内置工具

```typescript
import { ChatOpenAI } from "@langchain/openai";

// OpenAI 有内置工具
const model = new ChatOpenAI({
  model: "gpt-4.1",
  // 启用代码解释器
  tools: [{ type: "code_interpreter" }],
});

// Anthropic 有内置工具
import { ChatAnthropic } from "@langchain/anthropic";

const claude = new ChatAnthropic({
  model: "claude-sonnet-4-5-20250929",
  // 这些是提供商参数，不是 bindTools()
});
```

### 条件工具绑定

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ model: "gpt-4.1" });

function getModelWithTools(userRole: string) {
  const tools = [publicTool];

  if (userRole === "admin") {
    tools.push(adminTool);
  }

  return model.bindTools(tools);
}

// 不同用户获得不同的工具
const adminModel = getModelWithTools("admin");
const userModel = getModelWithTools("user");
```

### 对话中的工具调用

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "langchain";

const searchTool = tool(
  async ({ query }) => `${query}的搜索结果`,
  {
    name: "search",
    description: "搜索网络",
    schema: z.object({ query: z.string() }),
  }
);

const model = new ChatOpenAI({ model: "gpt-4.1" });
const modelWithTools = model.bindTools([searchTool]);

const messages = [
  { role: "user", content: "搜索 LangChain" },
];

// 第一次调用：模型决定使用工具
const response1 = await modelWithTools.invoke(messages);
messages.push(response1);

// 执行工具
for (const toolCall of response1.tool_calls || []) {
  const result = await searchTool.invoke(toolCall);
  messages.push(result);
}

// 第二次调用：模型使用工具结果
const response2 = await modelWithTools.invoke(messages);
console.log(response2.content); // 基于搜索结果的答案

// 继续对话
messages.push(response2);
messages.push({ role: "user", content: "告诉我更多" });

const response3 = await modelWithTools.invoke(messages);
// 如果需要，模型可以再次调用工具
```

## 边界

### 您可以配置的内容

✅ **哪些工具可用**：bindTools([tool1, tool2])
✅ **工具选择策略**：auto、any、特定工具、none
✅ **工具执行逻辑**：自定义错误处理、重试
✅ **工具参数**：通过工具模式
✅ **多个工具调用**：模型可以调用多个工具

### 您无法配置的内容

❌ **强制模型推理**：无法控制模型如何决定
❌ **工具调用顺序**：模型决定（可以并行调用）
❌ **阻止所有工具调用**：使用 tool_choice 或不绑定工具
❌ **在模型生成后修改工具调用**：工具调用是不可变的

## 常见陷阱

### 1. 忘记传回工具结果

```typescript
// ❌ 问题：没有将工具结果传回模型
const response1 = await modelWithTools.invoke(messages);
const toolResult = await tool.invoke(response1.tool_calls[0]);
// 缺少：将结果传回模型！

// ✅ 解决方案：始终传回结果
messages.push(response1); // 带有工具调用的 AI 消息
messages.push(toolResult); // 工具结果
const response2 = await modelWithTools.invoke(messages);
```

### 2. 工具调用 ID 不匹配

```typescript
// ❌ 问题：错误的 tool_call_id
const response = await modelWithTools.invoke("获取天气");
const toolMessage = new ToolMessage({
  content: "晴天",
  tool_call_id: "wrong_id", // 不匹配！
  name: "get_weather",
});

// ✅ 解决方案：使用工具调用中的正确 ID
const toolMessage = new ToolMessage({
  content: "晴天",
  tool_call_id: response.tool_calls[0].id, // 正确的 ID
  name: "get_weather",
});

// 或使用自动处理此问题的 tool.invoke()
const toolMessage = await getTool.invoke(response.tool_calls[0]);
```

### 3. 不检查工具调用

```typescript
// ❌ 问题：假设模型总是调用工具
const response = await modelWithTools.invoke("你好");
await tool.invoke(response.tool_calls[0]); // 如果没有工具调用会出错！

// ✅ 解决方案：检查工具调用是否存在
if (response.tool_calls && response.tool_calls.length > 0) {
  for (const toolCall of response.tool_calls) {
    await tool.invoke(toolCall);
  }
} else {
  // 模型在不调用工具的情况下响应
  console.log(response.content);
}
```

### 4. 多次绑定工具

```typescript
// ❌ 问题：绑定工具会覆盖之前的绑定
const model = new ChatOpenAI({ model: "gpt-4.1" });
const withTool1 = model.bindTools([tool1]);
const withTool2 = withTool1.bindTools([tool2]); // 只有 tool2！

// ✅ 解决方案：一次性绑定所有工具
const withBothTools = model.bindTools([tool1, tool2]);
```

### 5. 异步工具执行未等待

```typescript
// ❌ 问题：未等待异步工具
const toolResults = response.tool_calls.map(async (tc) => {
  return await tool.invoke(tc); // 返回 Promise！
});
messages.push(...toolResults); // 推送的是 Promise，不是结果！

// ✅ 解决方案：使用 Promise.all 或 for...of
const toolResults = await Promise.all(
  response.tool_calls.map(tc => tool.invoke(tc))
);
messages.push(...toolResults);

// 或使用 for...of
const toolResults = [];
for (const toolCall of response.tool_calls) {
  const result = await tool.invoke(toolCall);
  toolResults.push(result);
}
```

### 6. 工具选择混淆

```typescript
// ❌ 问题：使用错误的工具选择语法
const model = new ChatOpenAI({ model: "gpt-4.1" });
model.bindTools([tool], "required"); // 错误！

// ✅ 解决方案：使用正确的选项格式
model.bindTools([tool], { tool_choice: "any" }); // 强制任意工具
model.bindTools([tool], { tool_choice: "tool_name" }); // 强制特定工具
model.bindTools([tool]); // tool_choice: "auto"（默认）
```

## 文档链接

- [工具调用概述](https://docs.langchain.com/oss/javascript/langchain/models)
- [消息中的工具调用](https://docs.langchain.com/oss/javascript/langchain/messages)
- [工具指南](https://docs.langchain.com/oss/javascript/langchain/tools)
- [OpenAI 工具调用](https://docs.langchain.com/oss/javascript/integrations/chat/openai)
