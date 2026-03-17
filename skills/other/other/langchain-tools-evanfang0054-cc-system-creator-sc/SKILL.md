---
name: langchain-tools
description: 在 LangChain 中定义和使用工具 - 包括工具装饰器、自定义工具、内置工具和工具模式
language: js
---

# langchain-tools (JavaScript/TypeScript)

## 概述

工具是代理可以执行的函数，用于执行获取数据、运行代码或查询数据库等操作。工具具有描述其用途和参数的模式，帮助模型理解何时以及如何使用它们。

**核心概念：**
- **tool()**：从函数创建工具的装饰器
- **模式**：定义工具参数的 Zod 模式
- **描述**：帮助模型理解何时使用工具
- **内置工具**：用于常见任务的预制工具

## 何时定义自定义工具

| 场景 | 创建自定义工具？ | 原因 |
|----------|---------------------|------|
| 特定领域的逻辑 | ✅ 是 | 对您的应用来说是独特的 |
| 第三方 API 集成 | ✅ 是 | 需要自定义集成 |
| 数据库查询 | ✅ 是 | 您的模式/数据 |
| 通用工具（搜索、计算） | ⚠️ 可能 | 先检查现有工具 |
| 文件操作 | ⚠️ 可能 | 存在内置文件系统工具 |

## 决策表

### 工具定义方法

| 方法 | 使用时机 | 示例 |
|--------|-------------|---------|
| `tool()` 配合函数 | 简单工具 | 基本转换 |
| `tool()` 配合模式 | 复杂参数 | 多个类型化字段 |
| `StructuredTool` | 完全控制 | 自定义错误处理 |
| 内置工具 | 常见操作 | 搜索、代码执行 |

## 代码示例

### 基本工具定义

```typescript
import { tool } from "langchain";
import { z } from "zod";

// 简单工具
const calculator = tool(
  async ({ operation, a, b }: { operation: string; a: number; b: number }) => {
    if (operation === "add") return a + b;
    if (operation === "multiply") return a * b;
    throw new Error(`未知操作：${operation}`);
  },
  {
    name: "calculator",
    description: "执行数学计算。当您需要计算数字时使用此工具。",
    schema: z.object({
      operation: z.enum(["add", "subtract", "multiply", "divide"]).describe("数学运算"),
      a: z.number().describe("第一个数字"),
      b: z.number().describe("第二个数字"),
    }),
  }
);

// 与代理一起使用
const result = await calculator.invoke({
  operation: "add",
  a: 5,
  b: 3,
});
console.log(result); // "8"
```

### 带详细模式的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

const searchDatabase = tool(
  async ({ query, limit, filters }) => {
    // 您的数据库搜索逻辑
    return `找到 ${limit} 条结果：${query}`;
  },
  {
    name: "search_database",
    description: "搜索客户数据库中符合条件的记录",
    schema: z.object({
      query: z.string().describe("搜索查询（关键词或客户姓名）"),
      limit: z.number().default(10).describe("返回的最大结果数"),
      filters: z.object({
        status: z.enum(["active", "inactive", "pending"]).optional(),
        created_after: z.string().optional().describe("ISO 日期字符串"),
      }).optional(),
    }),
  }
);
```

### 异步工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

const fetchWeather = tool(
  async ({ location }: { location: string }) => {
    // 异步 API 调用
    const response = await fetch(
      `https://api.weather.com/v1/location/${location}`
    );
    const data = await response.json();
    return `温度：${data.temp}°F，条件：${data.conditions}`;
  },
  {
    name: "get_weather",
    description: "获取位置的当前天气条件",
    schema: z.object({
      location: z.string().describe("城市名称或邮政编码"),
    }),
  }
);
```

### 带错误处理的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

const divisionTool = tool(
  async ({ numerator, denominator }) => {
    if (denominator === 0) {
      throw new Error("不能除以零");
    }
    return numerator / denominator;
  },
  {
    name: "divide",
    description: "将两个数字相除",
    schema: z.object({
      numerator: z.number(),
      denominator: z.number(),
    }),
  }
);

// 错误将被捕获并作为 ToolMessage 返回
```

### 带副作用的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";
import fs from "fs/promises";

const writeFile = tool(
  async ({ filepath, content }) => {
    await fs.writeFile(filepath, content, "utf-8");
    return `成功将 ${content.length} 个字符写入 ${filepath}`;
  },
  {
    name: "write_file",
    description: "将内容写入文件。小心使用，因为这会修改文件系统。",
    schema: z.object({
      filepath: z.string().describe("文件路径"),
      content: z.string().describe("要写入的内容"),
    }),
  }
);
```

### 带外部依赖的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";
import axios from "axios";

const githubSearch = tool(
  async ({ query, language }) => {
    const response = await axios.get(
      "https://api.github.com/search/repositories",
      {
        params: { q: `${query} language:${language}`, sort: "stars" },
        headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` },
      }
    );

    const repos = response.data.items.slice(0, 5);
    return repos.map(r => `${r.full_name} (⭐ ${r.stargazers_count})`).join("\n");
  },
  {
    name: "search_github",
    description: "搜索 GitHub 仓库",
    schema: z.object({
      query: z.string().describe("搜索查询"),
      language: z.string().optional().describe("编程语言过滤器"),
    }),
  }
);
```

### 带复杂返回类型的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

const analyzeText = tool(
  async ({ text }) => {
    return JSON.stringify({
      word_count: text.split(/\s+/).length,
      char_count: text.length,
      sentences: text.split(/[.!?]+/).length,
      avg_word_length: text.split(/\s+/).reduce((sum, w) => sum + w.length, 0) / text.split(/\s+/).length,
    });
  },
  {
    name: "analyze_text",
    description: "分析文本统计信息",
    schema: z.object({
      text: z.string().describe("要分析的文本"),
    }),
  }
);
```

### 带运行时配置的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

function createDatabaseTool(connectionString: string) {
  return tool(
    async ({ query }) => {
      // 使用 connectionString 连接到数据库
      const results = await db.query(query);
      return JSON.stringify(results);
    },
    {
      name: "query_database",
      description: "在数据库上执行 SQL 查询",
      schema: z.object({
        query: z.string().describe("要执行的 SQL 查询"),
      }),
    }
  );
}

// 创建具有特定配置的工具
const prodDbTool = createDatabaseTool(process.env.PROD_DB_URL);
const devDbTool = createDatabaseTool(process.env.DEV_DB_URL);
```

### 多个相关工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

// 工具包模式：一组相关工具
const emailTools = {
  send: tool(
    async ({ to, subject, body }) => {
      // 发送邮件逻辑
      return `邮件已发送至 ${to}`;
    },
    {
      name: "send_email",
      description: "发送邮件消息",
      schema: z.object({
        to: z.string().email(),
        subject: z.string(),
        body: z.string(),
      }),
    }
  ),

  read: tool(
    async ({ folder, limit }) => {
      // 读取邮件逻辑
      return `从 ${folder} 检索了 ${limit} 封邮件`;
    },
    {
      name: "read_emails",
      description: "从文件夹读取邮件",
      schema: z.object({
        folder: z.string().default("inbox"),
        limit: z.number().default(10),
      }),
    }
  ),
};

// 使用所有邮件工具
const agent = createAgent({
  model: "gpt-4.1",
  tools: Object.values(emailTools),
});
```

### 带响应格式验证的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

const getUser = tool(
  async ({ userId }) => {
    const user = await db.users.findById(userId);

    // 将结构化数据作为 JSON 字符串返回
    return JSON.stringify({
      id: user.id,
      name: user.name,
      email: user.email,
      created: user.createdAt.toISOString(),
    });
  },
  {
    name: "get_user",
    description: "通过 ID 获取用户信息",
    schema: z.object({
      userId: z.string().describe("要查找的用户 ID"),
    }),
  }
);
```

### 带流式更新的工具

```typescript
import { tool } from "langchain";
import { z } from "zod";

const processLargeFile = tool(
  async ({ filepath }, { runtime }) => {
    const totalLines = 1000;

    for (let i = 0; i < totalLines; i += 100) {
      // 流式进度更新
      await runtime.stream_writer.write({
        type: "progress",
        data: { processed: i, total: totalLines },
      });

      // 处理块
      await processChunk(i, i + 100);
    }

    return "处理完成";
  },
  {
    name: "process_file",
    description: "处理大文件并提供进度更新",
    schema: z.object({
      filepath: z.string(),
    }),
  }
);
```

## 边界

### 您可以配置的内容

✅ **函数逻辑**：任何 JavaScript/TypeScript 代码
✅ **参数**：通过带描述的 Zod 模式
✅ **名称和描述**：指导模型的工具选择
✅ **返回值**：任何可序列化的数据（字符串、JSON 等）
✅ **异步操作**：工具可以是异步的
✅ **错误处理**：抛出错误或返回错误消息

### 您无法配置的内容

❌ **何时模型调用工具**：模型根据上下文决定
❌ **工具调用顺序**：模型确定执行流程
❌ **参数值**：模型根据模式生成
❌ **来自模型的响应格式**：工具返回，模型解释

## 常见陷阱

### 1. 工具描述不当

```typescript
// ❌ 问题：描述模糊
const badTool = tool(
  async ({ data }) => "result",
  {
    name: "tool",
    description: "对数据做某事", // 太模糊！
    schema: z.object({ data: z.string() }),
  }
);

// ✅ 解决方案：具体、可操作的描述
const goodTool = tool(
  async ({ query }) => searchDatabase(query),
  {
    name: "search_customers",
    description: "按姓名、邮箱或 ID 搜索客户数据库。返回包含联系信息的客户记录。当用户询问客户数据时使用此工具。",
    schema: z.object({
      query: z.string().describe("要搜索的客户姓名、邮箱或 ID"),
    }),
  }
);
```

### 2. 缺少参数描述

```typescript
// ❌ 问题：没有字段描述
const badSchema = z.object({
  query: z.string(),
  limit: z.number(),
});

// ✅ 解决方案：描述每个字段
const goodSchema = z.object({
  query: z.string().describe("搜索词或关键词"),
  limit: z.number().describe("要返回的最大结果数（1-100）"),
});
```

### 3. 不可序列化的返回值

```typescript
// ❌ 问题：返回复杂对象
const badTool = tool(
  async () => new Date(), // Date 不可序列化！
  { name: "get_time", description: "获取时间", schema: z.object({}) }
);

// ✅ 解决方案：返回字符串或 JSON
const goodTool = tool(
  async () => new Date().toISOString(),
  { name: "get_time", description: "获取当前时间", schema: z.object({}) }
);

// 或序列化对象
const dataTool = tool(
  async () => JSON.stringify({ timestamp: Date.now(), user: getCurrentUser() }),
  { name: "get_data", description: "获取数据", schema: z.object({}) }
);
```

### 4. 没有模式的工具

```typescript
// ❌ 问题：没有模式
const badTool = tool(
  async (input: any) => "result",
  { name: "tool", description: "一个工具" }
  // 缺少模式！
);

// ✅ 解决方案：始终提供模式
const goodTool = tool(
  async ({ input }) => "result",
  {
    name: "tool",
    description: "一个工具",
    schema: z.object({ input: z.string() }), // 清晰的模式
  }
);
```

### 5. 忘记异步

```typescript
// ❌ 问题：未等待异步操作
const badTool = tool(
  ({ url }) => {
    fetch(url); // 未等待！
    return "完成";
  },
  {
    name: "fetch_url",
    description: "获取 URL",
    schema: z.object({ url: z.string() }),
  }
);

// ✅ 解决方案：使用 async/await
const goodTool = tool(
  async ({ url }) => {
    const response = await fetch(url);
    const data = await response.text();
    return data;
  },
  {
    name: "fetch_url",
    description: "获取 URL 内容",
    schema: z.object({ url: z.string().url() }),
  }
);
```

### 6. 带空格或特殊字符的工具名称

```typescript
// ❌ 问题：无效的工具名称
const badTool = tool(
  async () => "result",
  {
    name: "Get Weather!", // 不允许特殊字符
    description: "获取天气",
    schema: z.object({}),
  }
);

// ✅ 解决方案：使用 snake_case 或 camelCase
const goodTool = tool(
  async () => "result",
  {
    name: "get_weather", // 有效名称
    description: "获取天气",
    schema: z.object({}),
  }
);
```

## 文档链接

- [工具概述](https://docs.langchain.com/oss/javascript/langchain/tools)
- [工具集成](https://docs.langchain.com/oss/javascript/integrations/tools/index)
- [自定义工具指南](https://docs.langchain.com/oss/javascript/integrations/chat/openai)
