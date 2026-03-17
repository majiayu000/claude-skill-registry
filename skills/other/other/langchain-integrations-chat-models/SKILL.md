---
name: langchain-chat-models
description: 使用 LangChain 中的聊天模型集成指南，包括 OpenAI、Anthropic、Google、Azure 和 Bedrock
language: js
---

# langchain-chat-models (JavaScript/TypeScript)

## 概述

LangChain 中的聊天模型为与各种 LLM 提供商交互提供了统一接口。它们接受消息序列作为输入，并返回 AI 生成的消息作为输出。聊天模型支持工具调用、结构化输出和流式传输等功能。

### 核心概念

- **聊天模型**：接受消息（具有角色：system、user、assistant）并返回生成的响应
- **提供商**：提供 LLM API 的不同 AI 公司（OpenAI、Anthropic、Google、Azure、Bedrock 等）
- **工具调用**：模型可以根据用户查询调用函数/工具
- **流式传输**：实时逐令牌响应生成
- **结构化输出**：模型可以返回特定格式的响应（JSON、TypeScript 类型）

## 提供商选择决策表

| 提供商 | 最适合 | 模型示例 | 包 | 主要特性 |
|----------|----------|----------------|---------|--------------|
| **OpenAI** | 通用、函数调用 | gpt-4、gpt-4-turbo、gpt-3.5-turbo | `@langchain/openai` | 强大的函数调用、视觉、快速 |
| **Anthropic** | 长上下文、安全性、分析 | claude-3-opus、claude-3-sonnet、claude-3-haiku | `@langchain/anthropic` | 200k 上下文、工具使用、提示缓存 |
| **Google GenAI** | 多模态、免费层 | gemini-pro、gemini-pro-vision | `@langchain/google-genai` | 视觉、提供免费层 |
| **Azure OpenAI** | 企业、合规性 | gpt-4、gpt-35-turbo（Azure 部署） | `@langchain/openai` | 企业 SLA、数据驻留 |
| **AWS Bedrock** | AWS 生态系统、多样性 | claude、llama、titan 模型 | `@langchain/aws` | 多个模型、AWS 集成 |
| **Google Vertex AI** | GCP 生态系统、企业 | gemini-pro、palm 模型 | `@langchain/google-vertexai` | 企业功能、GCP 集成 |

### 何时选择每个提供商

**选择 OpenAI 如果：**
- 您需要强大的函数/工具调用能力
- 您希望快速的响应时间
- 您正在构建通用应用程序

**选择 Anthropic 如果：**
- 您需要非常长的上下文窗口（100k-200k 令牌）
- 安全性和宪法 AI 原则很重要
- 您想要高质量的分析和推理

**选择 Azure OpenAI 如果：**
- 您需要企业 SLA 和支持
- 数据驻留和合规性至关重要
- 您已经在使用 Microsoft Azure

**选择 AWS Bedrock 如果：**
- 您在 AWS 生态系统中
- 您希望访问多个模型提供商
- 您需要多样性（Claude、Llama、Titan 等）

**选择 Google（GenAI 或 Vertex）如果：**
- 您需要强大的多模态能力
- 您在 GCP 生态系统中
- 您希望访问 Gemini 模型

## 代码示例

### OpenAI 聊天模型

```typescript
import { ChatOpenAI } from "@langchain/openai";

// 基本初始化
const model = new ChatOpenAI({
  modelName: "gpt-4",
  temperature: 0.7,
  openAIApiKey: process.env.OPENAI_API_KEY, // 如果在 env 中设置则可选
});

// 调用模型
const response = await model.invoke([
  { role: "system", content: "你是一个有用的助手。" },
  { role: "user", content: "什么是 LangChain？" }
]);

console.log(response.content);

// 流式响应
const stream = await model.stream("给我讲个故事");
for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

### Anthropic 聊天模型

```typescript
import { ChatAnthropic } from "@langchain/anthropic";

const model = new ChatAnthropic({
  modelName: "claude-3-opus-20240229",
  temperature: 0.7,
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  maxTokens: 1024,
});

// 长上下文使用
const response = await model.invoke([
  { role: "user", content: "分析这个长文档..." }
]);

// 使用工具
const modelWithTools = model.bindTools([
  {
    name: "get_weather",
    description: "获取位置的天气",
    input_schema: {
      type: "object",
      properties: {
        location: { type: "string" }
      },
      required: ["location"]
    }
  }
]);
```

### Azure OpenAI 聊天模型

```typescript
import { AzureChatOpenAI } from "@langchain/openai";

const model = new AzureChatOpenAI({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiInstanceName: process.env.AZURE_OPENAI_API_INSTANCE_NAME,
  azureOpenAIApiDeploymentName: process.env.AZURE_OPENAI_API_DEPLOYMENT_NAME,
  azureOpenAIApiVersion: "2024-02-01",
  temperature: 0.7,
});

const response = await model.invoke("你好，你好吗？");
```

### AWS Bedrock 聊天模型

```typescript
import { ChatBedrockConverse } from "@langchain/aws";

const model = new ChatBedrockConverse({
  model: "anthropic.claude-3-sonnet-20240229-v1:0",
  region: "us-east-1",
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

const response = await model.invoke("什么是 AWS Bedrock？");
```

### Google Generative AI

```typescript
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

const model = new ChatGoogleGenerativeAI({
  modelName: "gemini-pro",
  apiKey: process.env.GOOGLE_API_KEY,
  temperature: 0.7,
});

const response = await model.invoke("解释量子计算");
```

### 使用 initChatModel（推荐）

```typescript
import { initChatModel } from "langchain/chat_models/universal";

// 根据环境自动选择模型
const model = await initChatModel("gpt-4", {
  modelProvider: "openai",
  temperature: 0.7,
});

// 或使用 Bedrock
const bedrockModel = await initChatModel(
  "anthropic.claude-3-sonnet-20240229-v1:0",
  { modelProvider: "bedrock" }
);
```

### 工具调用示例

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";
import { tool } from "@langchain/core/tools";

// 定义工具
const weatherTool = tool(
  async ({ location }) => {
    return `${location}的天气：晴朗，72°F`;
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
const model = new ChatOpenAI({
  modelName: "gpt-4",
}).bindTools([weatherTool]);

const response = await model.invoke("旧金山的天气怎么样？");
console.log(response.tool_calls); // 模型将建议调用天气工具
```

## 边界

### 代理可以做什么

✅ **初始化任何支持的聊天模型提供商**
- 安装所需的包（`@langchain/openai`、`@langchain/anthropic` 等）
- 使用 API 密钥和参数配置模型

✅ **配置模型参数**
- 设置 temperature、max tokens、top_p、frequency_penalty
- 配置流式传输、超时和重试设置

✅ **使用模型进行文本生成**
- 发送消息并接收响应
- 逐令牌流式传输响应
- 使用系统提示和多轮对话

✅ **实现工具/函数调用**
- 将工具绑定到支持它的模型
- 解析工具调用响应
- 执行工具并返回结果

✅ **在提供商之间切换**
- 使用 initChatModel 编写与提供商无关的代码
- 通过更新配置更改提供商

### 代理不能做什么

❌ **创建新的模型提供商**
- 无法添加对未列出的 LLM 提供商的支持
- 必须使用现有的 LangChain 集成

❌ **绕过提供商要求**
- 无法在没有部署名称的情况下使用 Azure OpenAI
- 无法跳过所需的身份验证凭据

❌ **修改模型能力**
- 无法为不支持工具调用的模型添加工具调用
- 无法将上下文窗口扩展到提供商限制之外

❌ **在没有正确设置的情况下访问模型**
- 无法在没有有效 API 密钥的情况下使用提供商
- 无法绕过计费/配额限制

## 常见陷阱

### 1. **API 密钥和环境变量**

```typescript
// ❌ 错误：硬编码 API 密钥
const model = new ChatOpenAI({
  openAIApiKey: "sk-..."  // 永远不要提交这个！
});

// ✅ 正确：使用环境变量
const model = new ChatOpenAI({
  openAIApiKey: process.env.OPENAI_API_KEY
});
```

**修复**：始终使用环境变量或安全密钥管理系统。

### 2. **Azure OpenAI 配置复杂性**

```typescript
// ❌ 不完整：缺少必填字段
const model = new AzureChatOpenAI({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
});

// ✅ 完整：所有必填字段
const model = new AzureChatOpenAI({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiInstanceName: "my-instance",
  azureOpenAIApiDeploymentName: "gpt-4-deployment",
  azureOpenAIApiVersion: "2024-02-01",
});
```

**修复**：Azure 需要实例名称、部署名称和 API 版本。

### 3. **模型名称变化**

```typescript
// 不同提供商有不同的模型命名约定
// OpenAI
const openai = new ChatOpenAI({ modelName: "gpt-4" });

// Bedrock（包括提供商前缀）
const bedrock = new ChatBedrockConverse({
  model: "anthropic.claude-3-sonnet-20240229-v1:0"
});

// Anthropic（直接模型名称）
const anthropic = new ChatAnthropic({
  modelName: "claude-3-opus-20240229"
});
```

**修复**：查看提供商文档以获取正确的模型标识符。

### 4. **工具调用支持**

```typescript
// ❌ 并非所有模型都支持工具调用
const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo-instruct" });
// 这个旧模型不支持工具！

// ✅ 使用支持工具的模型
const model = new ChatOpenAI({ modelName: "gpt-4" });
const withTools = model.bindTools([myTool]);
```

**修复**：在绑定工具之前验证模型是否支持函数/工具调用。GPT-4、GPT-3.5-turbo、Claude 3 和 Gemini Pro 都支持工具。

### 5. **速率限制和配额**

```typescript
// ❌ 没有重试逻辑
const model = new ChatOpenAI();
const response = await model.invoke("你好"); // 可能因速率限制而失败

// ✅ 配置重试
const model = new ChatOpenAI({
  maxRetries: 3,
  timeout: 30000, // 30 秒
});
```

**修复**：配置重试逻辑并优雅地处理速率限制错误。

### 6. **上下文窗口限制**

```typescript
// ❌ 超过上下文限制
const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo" }); // 4k 上下文
const longText = "...".repeat(10000);
await model.invoke(longText); // 会失败！

// ✅ 为长上下文使用适当的模型
const model = new ChatOpenAI({ modelName: "gpt-4-turbo" }); // 128k 上下文
// 或
const model = new ChatAnthropic({
  modelName: "claude-3-opus-20240229" // 200k 上下文
});
```

**修复**：为您的用例选择具有适当上下文窗口的模型。

### 7. **流式与非流式**

```typescript
// ❌ 错误地混合使用流式和非流式
const response = await model.stream("你好");
console.log(response.content); // 不起作用！response 是异步可迭代对象

// ✅ 正确处理流式传输
const stream = await model.stream("你好");
for await (const chunk of stream) {
  console.log(chunk.content);
}

// 或使用 invoke 进行非流式
const response = await model.invoke("你好");
console.log(response.content);
```

**修复**：使用 `invoke()` 获得完整响应，使用 `stream()` 进行逐令牌传输。

## 链接和资源

### 官方文档
- [LangChain JS 聊天模型概述](https://js.langchain.com/docs/integrations/chat/)
- [OpenAI 集成](https://js.langchain.com/docs/integrations/chat/openai)
- [Anthropic 集成](https://js.langchain.com/docs/integrations/chat/anthropic)
- [Azure OpenAI 集成](https://js.langchain.com/docs/integrations/chat/azure)
- [AWS Bedrock 集成](https://js.langchain.com/docs/integrations/chat/bedrock)
- [Google GenAI 集成](https://js.langchain.com/docs/integrations/chat/google_generativeai)

### 提供商文档
- [OpenAI API 文档](https://platform.openai.com/docs/introduction)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [Azure OpenAI 服务](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Google AI Studio](https://ai.google.dev/)

### 包安装
```bash
# OpenAI
npm install @langchain/openai

# Anthropic
npm install @langchain/anthropic

# AWS (Bedrock)
npm install @langchain/aws

# Google
npm install @langchain/google-genai
npm install @langchain/google-vertexai
```
