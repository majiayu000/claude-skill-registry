---
name: langchain-tools
description: LangChain 工具集成使用指南，包括预构建工具包、Tavily、Wikipedia 和自定义工具
language: js
---

# langchain-tools (JavaScript/TypeScript)

## 概述

工具使 LLM 能够与外部系统交互、执行计算、搜索网络、查询数据库等。它们将模型能力扩展到文本生成之外，使 Agent 真正具备可执行性。

### 核心概念

- **工具（Tools）**：Agent 可以调用的函数，用于执行特定任务
- **工具调用（Tool Calling）**：模型根据用户查询决定何时以及如何使用工具
- **工具包（Toolkits）**：相关工具的集合
- **工具模式（Tool Schema）**：使用 Zod 或 JSON Schema 描述工具参数

## 工具选择决策表

| 工具/工具包 | 最适用于 | 包 | 主要特性 |
|--------------|----------|---------|--------------|
| **Tavily 搜索** | 网络搜索 | `@langchain/community` | AI 优化的搜索 API |
| **Wikipedia** | 百科全书查询 | `@langchain/community` | Wikipedia API 访问 |
| **计算器（Calculator）** | 数学运算 | `@langchain/community` | 表达式求值 |
| **DuckDuckGo 搜索** | 注重隐私的搜索 | `@langchain/community` | 无需 API 密钥 |
| **浏览器工具** | 网页自动化 | `@langchain/community` | 无头浏览器 |
| **向量存储工具** | 语义搜索 | 基于向量存储 | 查询您自己的数据 |
| **自定义工具** | 您的特定需求 | `@langchain/core/tools` | 定义任何函数 |

### 何时选择各工具

**选择 Tavily 如果：**
- 您需要高质量的网络搜索
- 您希望获得 AI 优化的结果
- 您正在构建研究/RAG 应用程序

**选择 Wikipedia 如果：**
- 您需要百科全书式知识
- 需要事实性信息
- 免费，无需 API 密钥

**选择自定义工具如果：**
- 您有特定的业务逻辑
- 您需要集成专有系统
- 内置工具无法满足您的需求

## 代码示例

### Tavily 搜索工具

```typescript
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";

// 初始化 Tavily（需要 API 密钥）
const searchTool = new TavilySearchResults({
  maxResults: 3,
  apiKey: process.env.TAVILY_API_KEY,
});

// 直接使用
const results = await searchTool.invoke("Latest AI news");
console.log(results);

// 与 Agent 一起使用
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const model = new ChatOpenAI({ modelName: "gpt-4" });
const agent = createReactAgent({
  llm: model,
  tools: [searchTool],
});

const response = await agent.invoke({
  messages: [{ role: "user", content: "What's new in AI today?" }]
});
```

### Wikipedia 工具

```typescript
import { WikipediaQueryRun } from "@langchain/community/tools/wikipedia_query_run";

const wikipediaTool = new WikipediaQueryRun({
  topKResults: 3,
  maxDocContentLength: 4000,
});

// 查询 Wikipedia
const result = await wikipediaTool.invoke("Artificial Intelligence");
console.log(result);
```

### 计算器工具

```typescript
import { Calculator } from "@langchain/community/tools/calculator";

const calculator = new Calculator();

// 执行计算
const result = await calculator.invoke("sqrt(144) + 5 * 3");
console.log(result); // "27"

// 在 Agent 中用于数学问题
const mathAgent = createReactAgent({
  llm: model,
  tools: [calculator],
});
```

### DuckDuckGo 搜索（无需 API 密钥）

```typescript
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";

const searchTool = new DuckDuckGoSearch({
  maxResults: 5,
});

const results = await searchTool.invoke("LangChain framework");
```

### 使用 Zod 模式的自定义工具

```typescript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

// 定义自定义工具
const weatherTool = tool(
  async ({ location, unit = "celsius" }) => {
    // 您的实现
    const data = await fetchWeather(location, unit);
    return `The weather in ${location} is ${data.temp}°${unit === "celsius" ? "C" : "F"}`;
  },
  {
    name: "get_weather",
    description: "Get the current weather for a location. Use this when users ask about weather.",
    schema: z.object({
      location: z.string().describe("The city name, e.g., 'San Francisco'"),
      unit: z.enum(["celsius", "fahrenheit"]).optional().describe("Temperature unit"),
    }),
  }
);

// 与 Agent 一起使用
const agent = createReactAgent({
  llm: model,
  tools: [weatherTool],
});

const response = await agent.invoke({
  messages: [{ role: "user", content: "What's the weather in London?" }]
});
```

### 自定义工具 - 基于类

```typescript
import { StructuredTool } from "@langchain/core/tools";
import { z } from "zod";

class DatabaseQueryTool extends StructuredTool {
  name = "database_query";
  description = "Query the customer database for information";

  schema = z.object({
    customerId: z.string().describe("Customer ID to look up"),
  });

  async _call({ customerId }: { customerId: string }): Promise<string> {
    // 您的数据库逻辑
    const customer = await db.getCustomer(customerId);
    return JSON.stringify(customer);
  }
}

const dbTool = new DatabaseQueryTool();
```

### 将向量存储作为工具

```typescript
import { createRetrieverTool } from "langchain/tools/retriever";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

// 创建向量存储
const vectorStore = await MemoryVectorStore.fromTexts(
  ["LangChain is a framework...", "Agents use tools..."],
  [{}, {}],
  new OpenAIEmbeddings()
);

// 转换为工具
const retrieverTool = createRetrieverTool(
  vectorStore.asRetriever(),
  {
    name: "knowledge_base",
    description: "Search the knowledge base for information about LangChain",
  }
);

// 在 Agent 中使用
const agent = createReactAgent({
  llm: model,
  tools: [retrieverTool],
});
```

### 多工具示例

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
import { Calculator } from "@langchain/community/tools/calculator";
import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

// 定义工具
const searchTool = new TavilySearchResults({ maxResults: 3 });
const calculator = new Calculator();

const customTool = tool(
  async ({ query }) => {
    // 您的自定义逻辑
    return `Custom result for: ${query}`;
  },
  {
    name: "custom_lookup",
    description: "Look up custom information",
    schema: z.object({
      query: z.string().describe("The query to look up"),
    }),
  }
);

// 创建具有多个工具的 Agent
const agent = createReactAgent({
  llm: new ChatOpenAI({ modelName: "gpt-4" }),
  tools: [searchTool, calculator, customTool],
});

// Agent 将选择适当的工具
const response = await agent.invoke({
  messages: [{
    role: "user",
    content: "Search for the population of Tokyo and calculate if it doubled"
  }]
});
```

### 带错误处理的工具

```typescript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const apiTool = tool(
  async ({ endpoint }) => {
    try {
      const response = await fetch(`https://api.example.com/${endpoint}`);
      if (!response.ok) {
        return `API error: ${response.statusText}`;
      }
      const data = await response.json();
      return JSON.stringify(data);
    } catch (error) {
      return `Failed to call API: ${error.message}`;
    }
  },
  {
    name: "api_call",
    description: "Call external API",
    schema: z.object({
      endpoint: z.string().describe("API endpoint to call"),
    }),
  }
);
```

## 边界

### Agent 能够做的

✅ **使用预构建工具**
- Tavily 搜索、Wikipedia、计算器
- DuckDuckGo、网页浏览器
- 任何来自 LangChain 社区的工具

✅ **创建自定义工具**
- 使用 Zod 模式定义函数
- 实现基于类的工具
- 将检索器转换为工具

✅ **组合多个工具**
- 给 Agent 提供多个工具的访问权限
- 让模型选择适当的工具
- 链式工具调用

✅ **处理工具响应**
- 解析工具输出
- 在对话中使用结果
- 错误处理

### Agent 不能做的

❌ **安全地执行任意代码**
- 不能运行不受信任的代码
- 代码执行需要沙箱环境

❌ **绕过身份验证**
- 工具需要正确的 API 密钥
- 没有凭据无法访问受保护的资源

❌ **保证工具选择**
- 模型决定使用哪个工具
- 无法强制使用特定工具（除非通过提示）

❌ **使用模型不支持的工具**
- 并非所有模型都支持工具调用
- 需要 GPT-4、Claude 3 或类似模型

## 注意事项

### 1. **需要 API 密钥**

```typescript
// ❌ 缺少 API 密钥
const tool = new TavilySearchResults();
await tool.invoke("query"); // 错误!

// ✅ 提供 API 密钥
const tool = new TavilySearchResults({
  apiKey: process.env.TAVILY_API_KEY,
});
```

**修复方法**：在环境变量中设置所需的 API 密钥。

### 2. **模型必须支持工具**

```typescript
// ❌ 模型不支持工具调用
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo-instruct" });
// 此模型不支持工具!

// ✅ 使用支持工具的模型
const model = new ChatOpenAI({ modelName: "gpt-4" });
const modelWithTools = model.bindTools([myTool]);
```

**修复方法**：使用支持函数调用的模型（GPT-4、Claude 3 等）。

### 3. **工具描述很重要**

```typescript
// ❌ 描述不清晰
const tool = tool(
  async ({ x }) => x * 2,
  {
    name: "tool1",
    description: "A tool", // 太模糊!
    schema: z.object({ x: z.number() }),
  }
);

// ✅ 清晰、具体的描述
const tool = tool(
  async ({ number }) => number * 2,
  {
    name: "double_number",
    description: "Multiply a number by 2. Use this when the user wants to double a value.",
    schema: z.object({
      number: z.number().describe("The number to double"),
    }),
  }
);
```

**修复方法**：编写清晰的描述，帮助模型知道何时使用该工具。

### 4. **模式验证**

```typescript
// ❌ 没有模式验证
const tool = tool(
  async ({ location }) => {
    // 假设 location 是字符串，但没有验证
    return location.toUpperCase(); // 可能崩溃!
  },
  {
    name: "format_location",
    description: "Format location",
    schema: z.object({ location: z.any() }), // 太宽松
  }
);

// ✅ 正确的模式
const tool = tool(
  async ({ location }) => {
    return location.toUpperCase();
  },
  {
    name: "format_location",
    description: "Format location name to uppercase",
    schema: z.object({
      location: z.string().describe("Location name"),
    }),
  }
);
```

**修复方法**：使用特定的 Zod 模式确保类型安全。

## 相关资源

### 官方文档
- [LangChain JS 工具](https://js.langchain.com/docs/integrations/tools/)
- [自定义工具指南](https://js.langchain.com/docs/how_to/custom_tools/)
- [Tavily](https://docs.tavily.com/)

### 包安装
```bash
# 社区工具
npm install @langchain/community

# 核心工具
npm install @langchain/core

# 特定集成
npm install @langchain/openai  # 用于基于 OpenAI 的工具
```
