---
name: deepagents-memory
description: 在 Deep Agents 中实现长期内存，使用 StoreBackend、CompositeBackend 和 InMemoryStore 进行跨会话的持久化数据存储。
language: js
---

# deepagents-memory (JavaScript/TypeScript)

## 概述

**短期（StateBackend）**：仅单会话
**长期（StoreBackend）**：跨会话持久化
**混合（CompositeBackend）**：两者结合

## 长期内存设置

```typescript
import { createDeepAgent, CompositeBackend, StateBackend, StoreBackend } from "deepagents";
import { InMemoryStore } from "@langchain/langgraph";

const store = new InMemoryStore();

const agent = await createDeepAgent({
  backend: (config) => new CompositeBackend(
    new StateBackend(config),
    { "/memories/": new StoreBackend(config) }
  ),
  store
});

// /memories/* 文件跨会话持久化
// 其他文件是临时的
```

## 代码示例

### 示例 1：跨会话的用户偏好

```typescript
import { createDeepAgent, CompositeBackend, StateBackend, StoreBackend } from "deepagents";
import { InMemoryStore } from "@langchain/langgraph";

const store = new InMemoryStore();

const agent = await createDeepAgent({
  backend: (config) => new CompositeBackend(
    new StateBackend(config),
    { "/memories/": new StoreBackend(config) }
  ),
  store
});

// 会话 1：保存偏好
const config1 = { configurable: { thread_id: "thread-1" } };
await agent.invoke({
  messages: [{
    role: "user",
    content: "将我的编码风格保存到 /memories/style.txt：TypeScript、async/await、Jest"
  }]
}, config1);

// 会话 2：访问偏好
const config2 = { configurable: { thread_id: "thread-2" } };
await agent.invoke({
  messages: [{
    role: "user",
    content: "阅读我的偏好并编写一个用户获取函数"
  }]
}, config2);
// Agent 阅读 /memories/style.txt
```

### 示例 2：在工具中直接使用 Store

```typescript
import { tool } from "langchain";
import { createAgent } from "langchain";
import { InMemoryStore } from "@langchain/langgraph";
import { z } from "zod";

const getUserPreference = tool(
  async ({ key }) => {
    const value = await store.get(["user_prefs"], key);
    return value ? String(value) : "未找到";
  },
  {
    name: "get_user_preference",
    description: "获取用户偏好",
    schema: z.object({ key: z.string() }),
  }
);

const saveUserPreference = tool(
  async ({ key, value }) => {
    await store.put(["user_prefs"], key, { value });
    return `已保存 ${key}=${value}`;
  },
  {
    name: "save_user_preference",
    description: "保存用户偏好",
    schema: z.object({ key: z.string(), value: z.string() }),
  }
);

const store = new InMemoryStore();

const agent = createAgent({
  model: "gpt-4",
  tools: [getUserPreference, saveUserPreference],
  store
});

// 第一次会话
await agent.invoke({
  messages: [{ role: "user", content: "记住我偏好深色模式" }]
});

// 第二次会话
await agent.invoke({
  messages: [{ role: "user", content: "我偏好什么 UI 主题？" }]
});
```

### 示例 3：项目知识库

```typescript
const agent = await createDeepAgent({
  backend: (config) => new CompositeBackend(
    new StateBackend(config),
    {
      "/memories/": new StoreBackend(config),
      "/workspace/": new StateBackend(config),
    }
  ),
  store: new InMemoryStore()
});

// 构建知识
await agent.invoke({
  messages: [{
    role: "user",
    content: "在 /memories/db-schema.md 中记录数据库架构"
  }]
}, { configurable: { thread_id: "thread-1" } });

// 后续使用知识
await agent.invoke({
  messages: [{
    role: "user",
    content: "编写一个迁移来为用户添加邮箱"
  }]
}, { configurable: { thread_id: "thread-2" } });
```

## 决策表

| 模式 | 后端 | 使用场景 |
|---------|---------|----------|
| 全部临时 | StateBackend | 单会话任务 |
| 全部持久化 | StoreBackend | 记住所有内容 |
| 混合 | CompositeBackend | `/memories/` 持久化，其余临时 |

## 边界

### Agent 可以做的事情
✅ 将文件保存到持久化存储
✅ 跨会话访问持久化文件
✅ 混合临时和持久化存储
✅ 使用 Store 命名空间/键模式

### Agent 不能做的事情
❌ 没有 Store 访问内存
❌ 跨会话持久化 StateBackend 文件
❌ 在没有共享 Store 的情况下在 agent 之间共享内存

## 注意事项

### 1. StoreBackend 需要 Store

```typescript
// ❌ 缺少 store
await createDeepAgent({
  backend: (config) => new StoreBackend(config)
});

// ✅ 提供 store
await createDeepAgent({
  backend: (config) => new StoreBackend(config),
  store: new InMemoryStore()
});
```

### 2. 路径前缀很重要

```typescript
// ❌ 不持久化（路径错误）
await agent.invoke({
  messages: [{ role: "user", content: "保存到 /prefs.txt" }]
});

// ✅ 持久化（匹配 /memories/ 路由）
await agent.invoke({
  messages: [{ role: "user", content: "保存到 /memories/prefs.txt" }]
});
```

### 3. InMemoryStore 不持久化

```typescript
// ❌ 重启时丢失
const store = new InMemoryStore();

// ✅ 生产环境使用持久化存储
import { PostgresStore } from "@langchain/langgraph";
const store = new PostgresStore({ connectionString: "postgresql://..." });
```

### 4. 路由使用最长前缀匹配

```typescript
const backend = (config) => new CompositeBackend(
  new StateBackend(config),
  {
    "/mem/": new StoreBackend(config),
    "/mem/temp/": new StateBackend(config),  // 更具体
  }
);

// /mem/file.txt -> StoreBackend
// /mem/temp/file.txt -> StateBackend（更长的匹配）
```

## 完整文档

- [长期内存](https://docs.langchain.com/oss/javascript/deepagents/long-term-memory)
- [后端](https://docs.langchain.com/oss/javascript/deepagents/backends)
- [内存概述](https://docs.langchain.com/oss/javascript/concepts/memory)
- [LangGraph Store](https://docs.langchain.com/oss/javascript/langgraph/add-memory)
