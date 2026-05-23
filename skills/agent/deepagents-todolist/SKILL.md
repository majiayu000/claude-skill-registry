---
name: deepagents-todolist
description: Using TodoListMiddleware for task planning and tracking progress with the write_todos tool in Deep Agents for complex multi-step workflows.
language: js
---

# deepagents-todolist (JavaScript/TypeScript)

## 概述

TodoListMiddleware 通过 `write_todos` 工具为代理提供任务规划和进度跟踪功能。它自动包含在每个深度代理中，帮助代理将复杂的多步骤任务分解为可管理的部分。

## 何时使用 TodoList 中间件

| 使用 TodoList 的场景 | 跳过 TodoList 的场景 |
|------------------|-------------------|
| 需要协调的复杂多步骤任务 | 简单的单动作任务 |
| 进度可见性很重要的长时间运行操作 | 快速操作（< 3 步） |
| 可能需要计划调整的任务 | 固定的、预定义的工作流 |

## 基本用法

### 默认配置（自动包含）

```typescript
import { createDeepAgent } from "deepagents";

// TodoListMiddleware 默认包含在内
const agent = await createDeepAgent({});

// 代理将自动使用 write_todos 处理复杂任务
const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "创建一个 TypeScript 网络爬虫，提取产品数据，存储到数据库中，并生成报告。"
  }]
});
```

### 自定义 TodoList 中间件

```typescript
import { createAgent, todoListMiddleware } from "langchain";

const agent = createAgent({
  model: "claude-sonnet-4-5-20250929",
  middleware: [
    todoListMiddleware({
      systemPrompt: `使用 write_todos 工具来规划您的工作：
      1. 将任务分解为 3-5 个主要步骤
      2. 开始时将任务标记为 'in_progress'
      3. 完成后将任务标记为 'completed'
      4. 如果计划发生变化，更新列表
      `,
    }),
  ],
});
```

## 决策表：Todo List 模式

| 任务类型 | Todo List 策略 | 示例 |
|-----------|-------------------|---------|
| 顺序步骤 | 预先创建所有待办事项，按顺序完成 | 构建应用：设置 → 编码 → 测试 → 部署 |
| 探索式任务 | 根据需要添加待办事项 | 研究：初始搜索 → 后续跟进 → 综合 |
| 并行工作 | 允许多个 "in_progress" 项目 | 数据处理：提取 + 转换 + 加载 |

## 代码示例

### 示例 1：顺序任务分解

```typescript
import { createDeepAgent } from "deepagents";

const agent = await createDeepAgent({});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: `为待办事项应用创建 REST API：
    1. 设计数据模型
    2. 实现 CRUD 端点
    3. 添加身份验证
    4. 编写测试
    5. 创建 API 文档
    `
  }]
});

// 代理的内部规划（通过 write_todos）：
// [
//   { content: "为 Todo 项目设计数据模型", status: "pending" },
//   { content: "实现 CRUD 端点（GET、POST、PUT、DELETE）", status: "pending" },
//   { content: "添加 JWT 身份验证中间件", status: "pending" },
//   { content: "编写单元测试和集成测试", status: "pending" },
//   { content: "生成 OpenAPI 文档", status: "pending" }
// ]
```

### 示例 2：自定义 TodoList 指令

```typescript
import { createAgent, todoListMiddleware } from "langchain";
import { tool } from "langchain";
import { z } from "zod";

const runTests = tool(
  async ({ testSuite }: { testSuite: string }) => {
    return `${testSuite} 中的测试已通过`;
  },
  {
    name: "run_tests",
    description: "运行测试套件",
    schema: z.object({ testSuite: z.string() }),
  }
);

const deployCode = tool(
  async ({ environment }: { environment: string }) => {
    return `已部署到 ${environment}`;
  },
  {
    name: "deploy_code",
    description: "将代码部署到环境",
    schema: z.object({ environment: z.string() }),
  }
);

const agent = createAgent({
  model: "gpt-4",
  tools: [runTests, deployCode],
  middleware: [
    todoListMiddleware({
      systemPrompt: `对于部署任务，始终：
      1. 创建带有安全检查的待办事项列表
      2. 在部署前运行测试
      3. 在继续之前将每个步骤标记为已完成
      `,
    }),
  ],
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "将应用程序部署到生产环境"
  }]
});
```

### 示例 3：访问 Todo 状态

```typescript
import { createDeepAgent } from "deepagents";

const agent = await createDeepAgent({});

const result = await agent.invoke(
  {
    messages: [{
      role: "user",
      content: "创建数据处理流水线"
    }]
  },
  { configurable: { thread_id: "session-1" } }
);

// 从最终状态访问待办事项列表
const todos = result.todos || [];
for (const todo of todos) {
  console.log(`[${todo.status}] ${todo.content}`);
}
```

## 边界

### 代理可以使用 TodoLists 做什么

✅ 创建具有自定义内容和结构的待办事项列表
✅ 更新待办事项状态（pending → in_progress → completed）
✅ 在工作进展时添加新的待办事项
✅ 删除变得不相关的待办事项
✅ 重新组织或重新确定待办事项的优先级
✅ 对任何任务复杂度级别使用待办事项

### 代理不能做什么

❌ 将工具名称从 `write_todos` 更改
❌ 使用自定义状态值（必须是 pending/in_progress/completed）
❌ 在没有 thread_id 的情况下访问来自其他线程的待办事项
❌ 在 createDeepAgent 中禁用 TodoListMiddleware（始终包含）
❌ 跨多个代理共享待办事项（每个代理有自己的状态）

## 注意事项

### 1. TodoList 是有状态的 - 需要 Thread ID

```typescript
// ❌ 没有 thread_id 的待办事项列表不会持久化
await agent.invoke({ messages: [{ role: "user", content: "任务 1" }] });
await agent.invoke({ messages: [{ role: "user", content: "任务 2" }] });

// ✅ 使用 thread_id 进行持久化
const config = { configurable: { thread_id: "user-session" } };
await agent.invoke({ messages: [{ role: "user", content: "任务 1" }] }, config);
await agent.invoke({ messages: [{ role: "user", content: "任务 2" }] }, config);
```

### 2. TodoList 中间件始终存在

```typescript
// 您无法从 createDeepAgent 中移除 TodoListMiddleware
// ❌ 这不会移除 TodoList
const agent = await createDeepAgent({ middleware: [] });  // TodoList 仍然包含

// ✅ 如果需要完全控制，使用 LangChain 的 createAgent
import { createAgent } from "langchain";

const agent2 = createAgent({
  model: "gpt-4",
  middleware: []  // 完全没有中间件
});
```

### 3. TodoList 对于简单任务是可选的

```typescript
// 代理不会总是对简单任务使用 write_todos

// 简单任务 - 代理可能不会创建待办事项
const result1 = await agent.invoke({
  messages: [{ role: "user", content: "2+2 等于几？" }]
});
// 状态中没有待办事项

// 复杂任务 - 代理可能会创建待办事项
const result2 = await agent.invoke({
  messages: [{ role: "user", content: "构建一个网络爬虫并分析数据" }]
});
// 状态中存在待办事项
```

## 完整文档

- [TodoList 中间件指南](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in)
- [Agent Harness 功能](https://docs.langchain.com/oss/javascript/deepagents/harness)
- [TodoListMiddleware 参考](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#to-do-list)
