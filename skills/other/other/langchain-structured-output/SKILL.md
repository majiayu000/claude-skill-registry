---
name: langchain-structured-output
description: 使用 Zod 模式、类型安全响应和自动验证从 LangChain 代理和模型获取结构化的验证输出
language: js
---

# langchain-structured-output (JavaScript/TypeScript)

## 概述

结构化输出将非结构化的模型响应转换为经过验证的、类型化的数据。不是解析自由文本，而是获得符合您模式的 JSON 对象——非常适合数据提取、构建表单或与下游系统集成。

**核心概念：**
- **responseFormat**：定义预期的输出模式
- **Zod 验证**：具有自动验证的类型安全模式
- **withStructuredOutput()**：用于直接结构化输出的模型方法
- **工具策略**：对于不支持原生功能的模型，底层使用工具调用

## 决策表

### 何时使用结构化输出

| 使用场景 | 使用结构化输出？ | 原因 |
|----------|------------------|------|
| 提取联系信息、日期等 | ✅ 是 | 可靠的数据提取 |
| 表单填写 | ✅ 是 | 验证所有必填字段 |
| API 集成 | ✅ 是 | 类型安全的响应 |
| 分类任务 | ✅ 是 | 枚举验证 |
| 开放式问答 | ❌ 否 | 自由文本即可 |
| 创意写作 | ❌ 否 | 不要限制创造力 |

### 模式选项

| 模式类型 | 使用时机 | 示例 |
|---------|---------|------|
| Zod 模式 | TypeScript 项目（推荐） | `z.object({...})` |
| JSON 模式 | 互操作性 | `{ type: "object", properties: {...} }` |
| 联合类型 | 多种可能的格式 | `z.union([schema1, schema2])` |

## 代码示例

### 使用代理的基本结构化输出

```typescript
import { createAgent } from "langchain";
import { z } from "zod";

const ContactInfo = z.object({
  name: z.string(),
  email: z.string().email(),
  phone: z.string(),
});

const agent = createAgent({
  model: "gpt-4.1",
  responseFormat: ContactInfo,
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "提取：John Doe, john@example.com, (555) 123-4567"
  }],
});

console.log(result.structuredResponse);
// { name: 'John Doe', email: 'john@example.com', phone: '(555) 123-4567' }
```

### 模型直接结构化输出

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const MovieSchema = z.object({
  title: z.string().describe("电影标题"),
  year: z.number().describe("上映年份"),
  director: z.string(),
  rating: z.number().min(0).max(10),
});

const model = new ChatOpenAI({ model: "gpt-4.1" });
const structuredModel = model.withStructuredOutput(MovieSchema);

const response = await structuredModel.invoke("告诉我《盗梦空间》");
console.log(response);
// { title: "Inception", year: 2010, director: "Christopher Nolan", rating: 8.8 }
```

### 复杂嵌套模式

```typescript
import { z } from "zod";

const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string(),
  zip: z.string(),
});

const PersonSchema = z.object({
  name: z.string(),
  age: z.number().int().positive(),
  email: z.string().email(),
  address: AddressSchema,
  tags: z.array(z.string()),
});

const agent = createAgent({
  model: "gpt-4.1",
  responseFormat: PersonSchema,
});
```

### 枚举和字面量类型

```typescript
import { z } from "zod";

const ClassificationSchema = z.object({
  category: z.enum(["urgent", "normal", "low"]),
  sentiment: z.enum(["positive", "neutral", "negative"]),
  confidence: z.number().min(0).max(1),
});

const agent = createAgent({
  model: "gpt-4.1",
  responseFormat: ClassificationSchema,
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "分类：这非常重要，而且我很高兴！"
  }],
});
// { category: "urgent", sentiment: "positive", confidence: 0.95 }
```

### 可选字段和默认值

```typescript
import { z } from "zod";

const EventSchema = z.object({
  title: z.string(),
  date: z.string(),
  location: z.string().optional(),
  attendees: z.array(z.string()).default([]),
  confirmed: z.boolean().default(false),
});
```

### 联合类型（多种模式）

```typescript
import { z } from "zod";

const EmailSchema = z.object({
  type: z.literal("email"),
  to: z.string().email(),
  subject: z.string(),
});

const PhoneSchema = z.object({
  type: z.literal("phone"),
  number: z.string(),
  message: z.string(),
});

const ContactSchema = z.union([EmailSchema, PhoneSchema]);

const agent = createAgent({
  model: "gpt-4.1",
  responseFormat: ContactSchema,
});
// 模型根据输入选择使用哪种模式
```

### 数组提取

```typescript
import { z } from "zod";

const TaskListSchema = z.object({
  tasks: z.array(z.object({
    title: z.string(),
    priority: z.enum(["high", "medium", "low"]),
    dueDate: z.string().optional(),
  })),
});

const agent = createAgent({
  model: "gpt-4.1",
  responseFormat: TaskListSchema,
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "提取任务：1. 修复 bug（高优先级，明天到期）2. 更新文档"
  }],
});
```

### 包含原始 AIMessage

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const schema = z.object({ name: z.string(), age: z.number() });

const model = new ChatOpenAI({ model: "gpt-4.1" });
const structuredModel = model.withStructuredOutput(schema, {
  includeRaw: true,
});

const response = await structuredModel.invoke("人员：Alice，30岁");
console.log(response);
// {
//   raw: AIMessage { ... },
//   parsed: { name: "Alice", age: 30 }
// }
```

### 错误处理

```typescript
import { createAgent } from "langchain";
import { z } from "zod";

const StrictSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(120),
});

const agent = createAgent({
  model: "gpt-4.1",
  responseFormat: StrictSchema,
});

try {
  const result = await agent.invoke({
    messages: [{ role: "user", content: "邮箱：invalid，年龄：-5" }],
  });
} catch (error) {
  console.error("验证失败：", error);
  // 模型将重试或返回错误
}
```

## 边界

### 您可以配置的内容

✅ **模式结构**：任何有效的 Zod 模式
✅ **字段验证**：类型、范围、正则表达式等
✅ **可选与必填**：控制字段存在性
✅ **嵌套对象**：复杂的层次结构
✅ **数组**：项目列表
✅ **枚举**：受限的值

### 您无法配置的内容

❌ **模型推理**：无法控制模型如何生成数据
❌ **保证 100% 准确性**：模型仍可能出错
❌ **在上下文缺少数据时强制有效数据**：模型无法编造缺失信息

## 常见陷阱

### 1. 错误访问响应

```typescript
// ❌ 问题：访问错误的属性
const result = await agent.invoke(input);
console.log(result.response);  // undefined!

// ✅ 解决方案：使用 structuredResponse
console.log(result.structuredResponse);
```

### 2. 缺少描述

```typescript
// ❌ 问题：没有字段描述
const schema = z.object({
  date: z.string(),  // 什么格式？
  amount: z.number(),  // 什么单位？
});

// ✅ 解决方案：添加描述
const schema = z.object({
  date: z.string().describe("YYYY-MM-DD 格式的日期"),
  amount: z.number().describe("美元金额"),
});
```

### 3. 过度约束

```typescript
// ❌ 问题：对模型来说太严格
const schema = z.object({
  code: z.string().regex(/^[A-Z]{2}-\d{4}-[A-Z]{3}$/),  // 太具体！
});

// ✅ 解决方案：后处理验证或使用更宽松的模式
const schema = z.object({
  code: z.string().describe("格式：XX-0000-XXX（字母和数字）"),
});
```

### 4. 不处理验证错误

```typescript
// ❌ 问题：没有错误处理
const result = await agent.invoke(input);
const data = result.structuredResponse;  // 可能抛出异常！

// ✅ 解决方案：try/catch 或检查错误
try {
  const result = await agent.invoke(input);
  const data = result.structuredResponse;
} catch (error) {
  console.error("获取结构化输出失败：", error);
}
```

### 5. 混淆 responseFormat 和 tools

```typescript
// ❌ 问题：错误地使用 responseFormat 和 tools
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
  responseFormat: MySchema,  // 仅从最终响应中提取
});
// 工具先运行，然后从最终响应中提取模式

// ✅ 如果您需要工具 + 结构化最终输出，这是正确的
// 只需理解这个流程
```

## 文档链接

- [结构化输出概述](https://docs.langchain.com/oss/javascript/langchain/structured-output)
- [模型结构化输出](https://docs.langchain.com/oss/javascript/langchain/models)
- [代理结构化输出](https://docs.langchain.com/oss/javascript/langchain/agents)
