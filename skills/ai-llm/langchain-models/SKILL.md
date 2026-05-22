---
name: langchain-models
description: Initialize and use LangChain chat models - includes provider selection (OpenAI, Anthropic, Google), model configuration, and invocation patterns
language: js
---

# langchain-models (JavaScript/TypeScript)

## 概述

聊天模型是 LangChain 应用程序的核心。它们接收消息作为输入并返回 AI 生成的消息作为输出。LangChain 在多个提供商（OpenAI、Anthropic、Google 等）之间提供统一的接口。

**核心概念：**
- **initChatModel()**：任何提供商的通用初始化
- **特定提供商的类**：直接初始化（ChatOpenAI、ChatAnthropic 等）
- **消息**：结构化的输入/输出格式（HumanMessage、AIMessage 等）
- **调用模式**：invoke()、stream()、batch()

## 何时使用每个提供商

| 提供商 | 最适合 | 模型 | 优势 |
|----------|----------|--------|-----------|
| OpenAI | 通用、推理 | GPT-4.1、GPT-5 | 强大推理、大上下文 |
| Anthropic | 安全性、分析 | Claude Sonnet/Opus | 安全性、长上下文、视觉 |
| Google | 多模态、速度 | Gemini 2.5 | 快速、多模态、成本效益 |
| AWS Bedrock | 企业级、合规性 | 多个提供商 | 安全性、合规性、多样性 |
| Azure OpenAI | 企业级 OpenAI | GPT 模型 | 企业功能、SLA |

## 决策表

### 选择模型

| 用例 | 推荐模型 | 原因 |
|----------|------------------|-----|
| 复杂推理 | GPT-5、Claude Opus | 最佳逻辑能力 |
| 快速响应 | Gemini Flash、GPT-4.1-mini | 低延迟 |
| 视觉任务 | GPT-4.1、Claude Sonnet、Gemini | 多模态支持 |
| 长上下文 | Claude Opus、Gemini | 100k+ token 窗口 |
| 成本效益 | GPT-4.1-mini、Gemini Flash | 较低定价 |
| 企业级/合规性 | Azure OpenAI、AWS Bedrock | 安全功能 |

### 初始化方法

| 方法 | 何时使用 | 示例 |
|--------|-------------|---------|
| `initChatModel("provider:model")` | 在提供商之间快速切换 | `initChatModel("openai:gpt-4.1")` |
| 提供商类 | 需要特定于提供商的功能 | `new ChatOpenAI({ model: "gpt-4.1" })` |
| 带配置 | 需要自定义参数 | 温度、最大 token 等 |

## 代码示例

### 基本模型初始化

```typescript
import { initChatModel } from "langchain";

// 通用初始化 - 最简单的方法
const model = await initChatModel("openai:gpt-4.1");

// 或使用提供商简写
const model2 = await initChatModel("gpt-4.1"); // 默认为 OpenAI

// 设置 API 密钥（通常从环境变量）
process.env.OPENAI_API_KEY = "your-api-key";
const model3 = await initChatModel("openai:gpt-4.1");
```

### 特定于提供商的初始化

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatAnthropic } from "@langchain/anthropic";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

// OpenAI
const openai = new ChatOpenAI({
  model: "gpt-4.1",
  temperature: 0.7,
  maxTokens: 1000,
  apiKey: process.env.OPENAI_API_KEY,
});

// Anthropic
const anthropic = new ChatAnthropic({
  model: "claude-sonnet-4-5-20250929",
  temperature: 0,
  maxTokens: 2000,
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Google
const google = new ChatGoogleGenerativeAI({
  model: "gemini-2.5-flash-lite",
  temperature: 0.5,
  apiKey: process.env.GOOGLE_API_KEY,
});
```

### 简单调用

```typescript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-4.1");

// 字符串输入（转换为 HumanMessage）
const response = await model.invoke("什么是 LangChain？");
console.log(response.content);

// 消息数组输入
const response2 = await model.invoke([
  { role: "user", content: "你好！" }
]);
console.log(response2.content);
```

### 流式响应

```typescript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-4.1");

// 在 token 到达时流式传输
const stream = await model.stream("解释量子计算");

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

### 批处理

```typescript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-4.1");

// 并行处理多个输入
const results = await model.batch([
  "什么是 AI？",
  "什么是 ML？",
  "什么是 LangChain？"
]);

results.forEach((result, i) => {
  console.log(`答案 ${i + 1}：`, result.content);
});
```

### 多轮对话

```typescript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-4.1");

// 构建对话历史
const messages = [
  { role: "system", content: "您是一个有用的助手。" },
  { role: "user", content: "法国的首都是什么？" },
];

const response1 = await model.invoke(messages);
messages.push({ role: "assistant", content: response1.content });

// 继续对话
messages.push({ role: "user", content: "它的人口是多少？" });
const response2 = await model.invoke(messages);

console.log(response2.content); // 知道我们在谈论巴黎
```

### 模型配置选项

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  model: "gpt-4.1",

  // 控制随机性（0 = 确定性，1 = 创造性）
  temperature: 0.7,

  // 限制响应长度
  maxTokens: 500,

  // 替代采样方法
  topP: 0.9,

  // 惩罚重复
  frequencyPenalty: 0.5,
  presencePenalty: 0.5,

  // 在这些字符串处停止生成
  stop: ["\n\n", "END"],

  // 请求超时
  timeout: 30000, // 30 秒

  // 失败时的最大重试次数
  maxRetries: 3,
});
```

### Azure OpenAI

```typescript
import { ChatOpenAI } from "@langchain/openai";

const azure = new ChatOpenAI({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiInstanceName: "your-instance-name",
  azureOpenAIApiDeploymentName: "your-deployment-name",
  azureOpenAIApiVersion: "2024-02-15-preview",
});
```

### AWS Bedrock

```typescript
import { ChatBedrock } from "@langchain/aws";

// 来自环境变量或 ~/.aws/credentials 的 AWS 凭证
const bedrock = new ChatBedrock({
  model: "anthropic.claude-3-5-sonnet-20240620-v1:0",
  region: "us-east-1",
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});
```

### 模型选择助手

```typescript
import { initChatModel } from "langchain";

function getModel(task: string) {
  const modelMap = {
    reasoning: "openai:gpt-5",
    fast: "google-genai:gemini-2.5-flash-lite",
    vision: "openai:gpt-4.1",
    long_context: "anthropic:claude-sonnet-4-5-20250929",
    cost_effective: "openai:gpt-4.1-mini",
  };

  return initChatModel(modelMap[task] || "openai:gpt-4.1");
}

// 使用
const reasoningModel = await getModel("reasoning");
const fastModel = await getModel("fast");
```

### 错误处理

```typescript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-4.1");

try {
  const response = await model.invoke("你好！");
  console.log(response.content);
} catch (error) {
  if (error.status === 429) {
    console.error("超过速率限制");
  } else if (error.status === 401) {
    console.error("无效的 API 密钥");
  } else {
    console.error("错误：", error.message);
  }
}
```

### 检查模型功能

```typescript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-4.1");

// 检查模型是否支持功能
console.log("支持流式传输：", typeof model.stream === "function");
console.log("支持工具调用：", typeof model.bindTools === "function");
console.log("支持结构化输出：", typeof model.withStructuredOutput === "function");
```

## 边界

### 您可以配置什么

✅ **模型选择**：来自任何提供商的任何支持的模型
✅ **温度**：控制随机性（0-1）
✅ **最大 Token**：限制响应长度
✅ **停止序列**：定义停止生成的位置
✅ **超时/重试**：控制请求行为
✅ **API 密钥**：每个模型或来自环境变量
✅ **特定于提供商的选项**：每个提供商都有独特的功能

### 您不能配置什么

❌ **模型训练数据**：模型是预训练的
❌ **模型架构**：无法修改内部结构
❌ **Token 成本**：由提供商设置
❌ **速率限制**：由提供商设置（可以使用队列管理）
❌ **模型功能**：视觉/工具支持是特定于模型的

## 注意事项

### 1. 找不到 API 密钥

```typescript
// ❌ 问题：缺少 API 密钥
const model = await initChatModel("openai:gpt-4.1");
await model.invoke("你好"); // 错误：找不到 API 密钥

// ✅ 解决方案：设置环境变量
process.env.OPENAI_API_KEY = "sk-...";
const model = await initChatModel("openai:gpt-4.1");

// 或直接传递
import { ChatOpenAI } from "@langchain/openai";
const model = new ChatOpenAI({
  model: "gpt-4.1",
  apiKey: "sk-...",
});
```

### 2. 模型名称拼写错误

```typescript
// ❌ 问题：错误的模型名称
const model = await initChatModel("gpt4"); // 错误！

// ✅ 解决方案：使用正确的格式
const model = await initChatModel("openai:gpt-4.1");
// 或提供商简写
const model2 = await initChatModel("gpt-4.1");
```

### 3. 响应内容访问

```typescript
// ❌ 问题：错误的属性访问
const response = await model.invoke("你好");
console.log(response); // AIMessage 对象，不是字符串

// ✅ 解决方案：访问 .content 属性
console.log(response.content); // "你好！我可以帮您吗？"

// 或使用 .toString()
console.log(response.toString());
```

### 4. 流式传输需要异步迭代

```typescript
// ❌ 问题：未等待流
const stream = model.stream("你好");
console.log(stream); // Promise，不是 chunks

// ✅ 解决方案：使用 for await
const stream = await model.stream("你好");
for await (const chunk of stream) {
  console.log(chunk.content);
}
```

### 5. 温度混淆

```typescript
// ❌ 问题：错误的温度范围
const model = new ChatOpenAI({
  temperature: 10, // 太高了！应该是 0-1
});

// ✅ 解决方案：使用 0-1 范围
const deterministic = new ChatOpenAI({ temperature: 0 }); // 始终相同
const balanced = new ChatOpenAI({ temperature: 0.7 }); // 默认
const creative = new ChatOpenAI({ temperature: 1 }); // 最大随机性
```

### 6. Token 限制

```typescript
// ❌ 问题：输入 + 输出超过模型限制
const longText = "...50,000 个词...";
const model = await initChatModel("gpt-4.1"); // 128k 上下文
await model.invoke(longText); // 可能成功

const model2 = await initChatModel("gpt-4.1-mini"); // 16k 上下文
await model2.invoke(longText); // 错误：上下文太长

// ✅ 解决方案：检查输入长度或使用更大的上下文模型
import { encoding_for_model } from "tiktoken";

const enc = encoding_for_model("gpt-4.1");
const tokens = enc.encode(longText);
console.log(`输入 tokens：${tokens.length}`);

if (tokens.length > 100000) {
  // 使用具有 200k 上下文的 Claude
  const model = await initChatModel("anthropic:claude-opus-4");
}
```

### 7. 特定于提供商的功能

```typescript
// ❌ 问题：对错误的模型使用特定于提供商的功能
const google = await initChatModel("google-genai:gemini-2.5-flash");
google.bindTools([tool]); // 可能无法以相同的方式工作

// ✅ 解决方案：检查每个提供商的文档
// OpenAI 有特定的工具调用格式
// Anthropic 有特定的工具调用格式
// Google 有特定的工具调用格式

// 使用 initChatModel 以获得可移植性，但要注意差异
```

## 文档链接

- [聊天模型概述](https://docs.langchain.com/oss/javascript/langchain/models)
- [OpenAI 集成](https://docs.langchain.com/oss/javascript/integrations/chat/openai)
- [Anthropic 集成](https://docs.langchain.com/oss/javascript/integrations/chat/anthropic)
- [Google 集成](https://docs.langchain.com/oss/javascript/integrations/chat/google_generative_ai)
- [所有聊天模型集成](https://docs.langchain.com/oss/javascript/integrations/chat/index)
- [模型提供商概述](https://docs.langchain.com/oss/javascript/integrations/providers/all_providers)
