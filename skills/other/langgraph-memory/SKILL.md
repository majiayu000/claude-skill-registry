---
name: langgraph-memory
description: LangGraph 中的内存：短期（线程范围）vs 长期（跨线程）内存，使用检查点器和存储
language: js
---

# langgraph-memory (JavaScript/TypeScript)

---
name: langgraph-memory
description: LangGraph 中的内存 - 短期（线程范围）vs 长期（跨线程）内存，使用检查点器和存储
---

## 概述

LangGraph 为 Agent 提供两种类型的内存：
- **短期内存**：线程范围，通过检查点器管理
- **长期内存**：跨线程，通过存储管理

## 决策表：内存类型

| 类型 | 范围 | 持久化 | 使用场景 |
|------|-------|-------------|----------|
| 短期 | 单个线程 | 通过检查点器 | 对话历史 |
| 长期 | 跨线程 | 通过存储 | 用户偏好、事实 |

## 代码示例

### 短期内存（线程范围）

```typescript
import { MemorySaver, StateGraph, StateSchema, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  messages: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
});

const respond = async (state: typeof State.State) => {
  // 访问对话历史
  const history = state.messages;
  return { messages: [`I remember ${history.length} messages`] };
};

const checkpointer = new MemorySaver();

const graph = new StateGraph(State)
  .addNode("respond", respond)
  .addEdge(START, "respond")
  .addEdge("respond", END)
  .compile({ checkpointer });

// 第一轮
const config = { configurable: { thread_id: "user-1" } };
await graph.invoke({ messages: ["Hello"] }, config);

// 第二轮 - 记住第一轮
await graph.invoke({ messages: ["How are you?"] }, config);
// 响应: "I remember 3 messages" (Hello, 响应, How are you?)
```

### 长期内存（跨线程）

```typescript
import { InMemoryStore } from "@langchain/langgraph";

// 创建长期内存存储
const store = new InMemoryStore();

// 保存用户偏好（在所有线程中可用）
const userId = "alice";
const namespace = [userId, "preferences"];

await store.put(
  namespace,
  "language",
  { preference: "short, direct responses" }
);

// 在任何线程中检索
const getUserPrefs = async (state, config) => {
  const store = config.store;
  const userId = state.userId;
  const namespace = [userId, "preferences"];

  const prefs = await store.get(namespace, "language");
  return { preferences: prefs };
};

// 使用存储编译
const graph = builder.compile({
  checkpointer,
  store,
});

// 在不同线程中使用
const thread1 = { configurable: { thread_id: "thread-1" } };
const thread2 = { configurable: { thread_id: "thread-2" } };

// 两个线程访问相同的长期内存
await graph.invoke({ userId: "alice" }, thread1);  // 获取偏好
await graph.invoke({ userId: "alice" }, thread2);  // 相同的偏好
```

### 存储操作

```typescript
import { InMemoryStore } from "@langchain/langgraph";

const store = new InMemoryStore();

// Put（创建/更新）
await store.put(
  ["user-123", "facts"],
  "location",
  { city: "San Francisco", country: "USA" }
);

// Get
const item = await store.get(["user-123", "facts"], "location");
console.log(item);  // { city: 'San Francisco', country: 'USA' }

// 带过滤器搜索
const results = await store.search(
  ["user-123", "facts"],
  { filter: { country: "USA" } }
);

// Delete
await store.delete(["user-123", "facts"], "location");
```

### 在节点中访问存储

```typescript
import { BaseStore } from "@langchain/langgraph";

const myNode = async (state, config: { store: BaseStore }) => {
  const store = config.store;
  const namespace = [state.userId, "memories"];

  // 检索过去的记忆
  const memories = await store.search(namespace, { query: "preferences" });

  // 保存新记忆
  await store.put(
    namespace,
    "new_fact",
    { fact: "User likes TypeScript" }
  );

  return { processed: true };
};

const graph = builder.compile({
  checkpointer,
  store,
});
```

### 组合短期和长期内存

```typescript
const smartNode = async (state, config) => {
  const store = config.store;

  // 短期：对话上下文
  const recentMessages = state.messages.slice(-5);  // 最近 5 条消息

  // 长期：用户档案
  const userId = state.userId;
  const profile = await store.get([userId, "profile"], "info");

  // 使用两者生成个性化响应
  const response = await generateResponse(recentMessages, profile);

  return { messages: [response] };
};

const graph = new StateGraph(State)
  .addNode("respond", smartNode)
  .addEdge(START, "respond")
  .addEdge("respond", END)
  .compile({ checkpointer, store });
```

### 持久化存储（生产环境）

```typescript
import { PostgresStore } from "@langchain/langgraph-checkpoint-postgres";

// 在生产环境中使用 PostgreSQL
const store = await PostgresStore.fromConnString(
  "postgresql://user:pass@localhost/db"
);

const graph = builder.compile({
  checkpointer,
  store,
});
```

## 边界

### 您能够配置的

✅ 使用检查点器进行短期内存
✅ 使用存储进行长期内存
✅ 命名空间组织
✅ 搜索和过滤记忆
✅ 通过 config 在节点中访问存储
✅ 选择存储后端

### 您不能配置的

❌ 跨线程共享短期内存
❌ 修改内存序列化格式
❌ 存储机制内部

## 注意事项

### 1. 短期需要检查点器

```typescript
// ❌ 错误 - 没有检查点器，没有内存
const graph = builder.compile();  // 消息丢失!

// ✅ 正确
const checkpointer = new MemorySaver();
const graph = builder.compile({ checkpointer });
```

### 2. 长期需要存储

```typescript
// ❌ 错误 - 试图在没有存储的情况下共享数据
// 仅靠检查点器无法访问来自其他线程的数据!

// ✅ 正确 - 使用存储
const store = new InMemoryStore();
const graph = builder.compile({ checkpointer, store });
```

### 3. 通过 Config 访问存储

```typescript
// ❌ 错误 - 存储不可用
const myNode = async (state) => {
  store.put(...);  // ReferenceError!
};

// ✅ 正确 - 通过 config 访问
const myNode = async (state, config) => {
  const store = config.store;
  await store.put(...);
};
```

### 4. InMemoryStore 不用于生产环境

```typescript
// ❌ 错误 - 重启时数据丢失
const store = new InMemoryStore();  // 仅内存!

// ✅ 正确 - 使用持久化后端
import { PostgresStore } from "@langchain/langgraph-checkpoint-postgres";
const store = await PostgresStore.fromConnString("postgresql://...");
```

### 5. 始终 Await 存储操作

```typescript
// ❌ 错误
const item = store.get(namespace, key);
console.log(item);  // Promise!

// ✅ 正确
const item = await store.get(namespace, key);
console.log(item);
```

## 相关链接

- [内存概览](https://docs.langchain.com/oss/javascript/concepts/memory)
- [短期内存](https://docs.langchain.com/oss/javascript/langchain/short-term-memory)
- [长期内存](https://docs.langchain.com/oss/javascript/langchain/long-term-memory)
- [存储参考](https://docs.langchain.com/oss/javascript/langgraph/persistence#memory-store)
