---
name: deepagents-overview
description: 理解 Deep Agents 框架 - 它们是什么、如何使用 createDeepAgent 创建，以及 agent harness 架构，包括内置的规划、文件系统和子代理中间件。
language: js
---

# deepagents-overview (JavaScript/TypeScript)

## 什么是 Deep Agents？

Deep Agents 是一个基于 LangChain 和 LangGraph 构建的自有代理框架，专为复杂的多步骤任务而设计。它们"开箱即用"，具有内置功能：

- **任务规划**：TodoListMiddleware 用于分解复杂任务
- **上下文管理**：具有可插拔后端的文件系统工具
- **任务委托**：SubAgent 中间件用于启动专用代理
- **长期内存**：通过 Store 跨会话持久化存储
- **人工干预**：敏感操作的审批工作流

Deep Agents 使用"agent harness"架构 - 与其他框架相同的核心工具调用循环，但具有预配置的中间件和工具。

## 何时使用 Deep Agents

| 使用 Deep Agents 当 | 使用 LangChain 的 createAgent 当 |
|---------------------|-----------------------------------|
| 需要规划的多步骤任务 | 简单、单一用途的任务 |
| 需要文件管理的大上下文 | 上下文适合单个提示 |
| 需要专用子代理 | 单个代理足够 |
| 跨会话持久化内存 | 临时的单会话工作 |
| CLI 或编码助手用例 | 简单 API 或聊天应用 |

## 创建 Deep Agent

### 基本代理创建

```typescript
import { createDeepAgent } from "deepagents";

// 具有默认设置的最小代理
const agent = await createDeepAgent({});

// 调用代理
const result = await agent.invoke({
  messages: [
    { role: "user", content: "东京的天气怎么样？" }
  ]
});
```

### 具有自定义工具的代理

```typescript
import { createDeepAgent } from "deepagents";
import { tool } from "langchain";
import { z } from "zod";

const getWeather = tool(
  ({ city }) => `${city} 总是晴天！`,
  {
    name: "get_weather",
    description: "获取给定城市的天气",
    schema: z.object({
      city: z.string(),
    }),
  }
);

const agent = await createDeepAgent({
  tools: [getWeather],
  systemPrompt: "你是一个有用的天气助手"
});

const result = await agent.invoke({
  messages: [
    { role: "user", content: "东京的天气怎么样？" }
  ]
});
```

### 具有自定义模型的代理

```typescript
import { createDeepAgent } from "deepagents";
import { ChatOpenAI } from "@langchain/openai";

// 使用 provider:model 格式
const agent = await createDeepAgent({
  model: "openai:gpt-4"
});

// 或传递模型实例
const model = new ChatOpenAI({ model: "gpt-4", temperature: 0 });
const agent2 = await createDeepAgent({
  model
});
```

## Agent Harness 架构

Deep Agents 在创建时自动附加中间件：

```typescript
import { createDeepAgent } from "deepagents";

// 此代理自动具有：
// - TodoListMiddleware（任务规划）
// - FilesystemMiddleware（文件操作）
// - SubAgentMiddleware（任务委托）
// - SummarizationMiddleware（历史管理）
// - AnthropicPromptCachingMiddleware（缓存）
// - PatchToolCallsMiddleware（工具调用修复）
const agent = await createDeepAgent({});
```

### 内置工具

每个 deep agent 都可以访问：

1. **规划工具**：`write_todos` - 跟踪多步骤任务
2. **文件系统工具**：`ls`、`read_file`、`write_file`、`edit_file`、`glob`、`grep`
3. **子代理工具**：`task` - 将工作委托给专用代理

## 配置选项

```typescript
import { createDeepAgent, FilesystemBackend } from "deepagents";
import { MemorySaver, InMemoryStore } from "@langchain/langgraph";

const agent = await createDeepAgent({
  name: "my-assistant",            // 可选：代理名称
  model: "claude-sonnet-4-5-20250929",  // 要使用的模型
  tools: [customTool1, customTool2],    // 附加工具
  systemPrompt: "自定义指令",   // 自定义系统提示
  middleware: [customMiddleware],        // 附加中间件
  subagents: [researchAgent, codeAgent], // 自定义子代理
  backend: new FilesystemBackend({ rootDir: "." }),  // 存储后端
  interruptOn: { write_file: true },     // 人工干预配置
  skills: ["/path/to/skills/"],     // 技能目录
  checkpointer: new MemorySaver(),  // 中断所需
  store: new InMemoryStore()        // 用于长期内存
});
```

## 决策表：要自定义哪个中间件

| 如果你需要... | 使用此中间件 | 何时自定义 |
|------------------|-------------------|------------------|
| 跟踪复杂的多步骤任务 | todoListMiddleware | 默认工作；需要时自定义提示 |
| 管理文件上下文 | createFilesystemMiddleware | 更改后端或工具描述 |
| 委托专门工作 | createSubAgentMiddleware | 添加具有特定工具的自定义子代理 |
| 防止上下文溢出 | summarizationMiddleware | 默认工作；自定义摘要策略 |
| 缓存提示（Anthropic） | anthropicPromptCachingMiddleware | 默认自动工作 |
| 添加人工审批 | humanInTheLoopMiddleware | 配置哪些工具需要审批 |
| 按需加载技能 | skillsMiddleware | 提供技能目录 |
| 访问持久化内存 | memoryMiddleware | 提供 Store 实例 |

## 边界

### Agent 可以配置的内容

✅ 模型选择和参数
✅ 附加的自定义工具
✅ 系统提示自定义
✅ 后端存储策略
✅ 哪些工具需要审批
✅ 具有专用工具的自定义子代理
✅ 技能目录和内容
✅ 中间件顺序和配置

### Agent 不能配置的内容

❌ 核心中间件移除（TodoList、Filesystem、SubAgent 始终存在）
❌ write_todos、task 或文件系统工具名称
❌ 基本工具调用循环
❌ LangGraph 的运行时执行模型
❌ Agent Skills 协议格式

## 注意事项

### 1. 中断需要 Checkpointer

```typescript
// ❌ 如果设置了 interruptOn 将会出错
const agent = await createDeepAgent({
  interruptOn: { write_file: true }
});

// ✅ Checkpointer 是必需的
import { MemorySaver } from "@langchain/langgraph";

const agent = await createDeepAgent({
  interruptOn: { write_file: true },
  checkpointer: new MemorySaver()
});
```

### 2. 持久化内存需要 Store

```typescript
// ❌ StoreBackend 需要 Store
import { StoreBackend } from "deepagents";

const agent = await createDeepAgent({
  backend: (config) => new StoreBackend(config)
});

// ✅ 传递 Store 实例
import { InMemoryStore } from "@langchain/langgraph";

const agent = await createDeepAgent({
  backend: (config) => new StoreBackend(config),
  store: new InMemoryStore()
});
```

### 3. 技能需要后端设置

```typescript
// ❌ 没有正确的后端技能不会加载
const agent = await createDeepAgent({
  skills: ["/path/to/skills/"]
});

// ✅ 使用 FilesystemBackend 进行本地技能
import { FilesystemBackend } from "deepagents";

const agent = await createDeepAgent({
  backend: new FilesystemBackend({ rootDir: ".", virtualMode: true }),
  skills: ["./skills/"]
});
```

### 4. 有状态对话需要 Thread ID

```typescript
// ❌ 没有 thread_id 每次调用都是隔离的
await agent.invoke({ messages: [{ role: "user", content: "嗨" }] });
await agent.invoke({ messages: [{ role: "user", content: "我说了什么？" }] });

// ✅ 使用一致的 thread_id 保持对话连续性
const config = { configurable: { thread_id: "user-123" } };
await agent.invoke({ messages: [{ role: "user", content: "嗨" }] }, config);
await agent.invoke({ messages: [{ role: "user", content: "我说了什么？" }] }, config);
```

### 5. 默认模型是 Anthropic Claude

```typescript
// 默认使用 claude-sonnet-4-5-20250929
const agent = await createDeepAgent({});

// 需要 ANTHROPIC_API_KEY 环境变量
// 如果使用 OpenAI 模型，设置 OPENAI_API_KEY
process.env.ANTHROPIC_API_KEY = "your-key";
```

### 6. 等待 createDeepAgent

```typescript
// ❌ 缺少 await
const agent = createDeepAgent({});

// ✅ createDeepAgent 是异步的
const agent = await createDeepAgent({});
```

## 完整文档

- [Deep Agents 概述](https://docs.langchain.com/oss/javascript/deepagents/overview)
- [Agent Harness 功能](https://docs.langchain.com/oss/javascript/deepagents/harness)
- [自定义 Deep Agents](https://docs.langchain.com/oss/javascript/deepagents/customization)
- [Deep Agents 快速入门](https://docs.langchain.com/oss/javascript/deepagents/quickstart)
