---
name: langgraph-persistence
description: 在 LangGraph 中实现持久化和检查点：保存状态、恢复执行、线程 ID 和检查点器库
language: js
---

# langgraph-persistence (JavaScript/TypeScript)

---
name: langgraph-persistence
description: 在 LangGraph 中实现持久化和检查点 - 保存状态、恢复执行、线程 ID 和检查点器库
---

## 概述

LangGraph 的持久化层通过在每个超级步检查点图状态来实现持久执行。这解锁了人机交互、内存、时间旅行和容错能力。

**核心组件：**
- **检查点器（Checkpointer）**：保存/加载图状态
- **线程 ID（Thread ID）**：检查点序列的标识符
- **检查点（Checkpoints）**：每步的状态快照

## 决策表：检查点器选择

| 检查点器 | 使用场景 | 持久化 | 生产就绪 |
|--------------|----------|-------------|------------------|
| `MemorySaver` | 测试、开发 | 仅内存 | ❌ 否 |
| `SqliteSaver` | 本地开发 | SQLite 文件 | ⚠️ 单用户 |
| `PostgresSaver` | 生产环境 | PostgreSQL | ✅ 是 |

## 代码示例

### 使用 MemorySaver 的基本持久化

```typescript
import { MemorySaver, StateGraph, StateSchema, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  messages: z.array(z.string()),
});

const addMessage = async (state: typeof State.State) => {
  return { messages: [...state.messages, "Bot response"] };
};

// 创建检查点器
const checkpointer = new MemorySaver();

// 使用检查点器编译
const graph = new StateGraph(State)
  .addNode("respond", addMessage)
  .addEdge(START, "respond")
  .addEdge("respond", END)
  .compile({ checkpointer });  // 启用持久化

// 第一次使用 thread_id 调用
const config = { configurable: { thread_id: "conversation-1" } };
const result1 = await graph.invoke({ messages: ["Hello"] }, config);
console.log(result1.messages.length);  // 2

// 第二次调用 - 状态已持久化
const result2 = await graph.invoke({ messages: ["How are you?"] }, config);
console.log(result2.messages.length);  // 4 (之前的 + 新的)
```

### SQLite 持久化

```typescript
import { SqliteSaver } from "@langchain/langgraph-checkpoint-sqlite";

// 创建 SQLite 检查点器
const checkpointer = SqliteSaver.fromConnString("checkpoints.db");

const graph = new StateGraph(State)
  .addNode("process", processNode)
  .addEdge(START, "process")
  .addEdge("process", END)
  .compile({ checkpointer });

// 使用 thread_id
const config = { configurable: { thread_id: "user-123" } };
const result = await graph.invoke({ data: "test" }, config);
```

### PostgreSQL 持久化

```typescript
import { PostgresSaver } from "@langchain/langgraph-checkpoint-postgres";

// 创建 Postgres 检查点器
const checkpointer = await PostgresSaver.fromConnString(
  "postgresql://user:pass@localhost/db"
);

const graph = new StateGraph(State)
  .addNode("process", processNode)
  .addEdge(START, "process")
  .addEdge("process", END)
  .compile({ checkpointer });

const config = { configurable: { thread_id: "thread-1" } };
const result = await graph.invoke({ data: "test" }, config);
```

### 检索状态

```typescript
// 获取当前状态
const config = { configurable: { thread_id: "conversation-1" } };
const currentState = await graph.getState(config);
console.log(currentState.values);  // 当前状态
console.log(currentState.next);    // 下一个要执行的节点

// 获取状态历史
const history = await graph.getStateHistory(config);
for await (const state of history) {
  console.log("Step:", state.values);
}
```

### 从检查点恢复

```typescript
import { MemorySaver, StateGraph, START, END } from "@langchain/langgraph";

const checkpointer = new MemorySaver();

const step1 = async (state) => ({ data: "step1" });
const step2 = async (state) => ({ data: state.data + "_step2" });

const graph = new StateGraph(State)
  .addNode("step1", step1)
  .addNode("step2", step2)
  .addEdge(START, "step1")
  .addEdge("step1", "step2")
  .addEdge("step2", END)
  .compile({
    checkpointer,
    interruptBefore: ["step2"],  // 在 step2 之前暂停
  });

const config = { configurable: { thread_id: "1" } };

// 运行到断点
await graph.invoke({ data: "start" }, config);

// 恢复执行
await graph.invoke(null, config);  // null 从检查点继续
```

### 更新状态

```typescript
// 在恢复之前修改状态
const config = { configurable: { thread_id: "1" } };

// 更新状态
await graph.updateState(config, { data: "manually_updated" });

// 使用更新后的状态恢复
await graph.invoke(null, config);
```

### 线程管理

```typescript
// 不同的线程维护独立的状态
const thread1Config = { configurable: { thread_id: "user-alice" } };
const thread2Config = { configurable: { thread_id: "user-bob" } };

// Alice 的对话
await graph.invoke({ messages: ["Hi from Alice"] }, thread1Config);

// Bob 的对话（独立状态）
await graph.invoke({ messages: ["Hi from Bob"] }, thread2Config);

// Alice 的状态与 Bob 的隔离
```

### 子图中的检查点器

```typescript
import { MemorySaver, StateGraph, START } from "@langchain/langgraph";

// 只有父图需要检查点器
const subgraphNode = async (state) => ({ data: "subgraph" });

const subgraph = new StateGraph(State)
  .addNode("process", subgraphNode)
  .addEdge(START, "process")
  .compile();  // 不需要检查点器

// 带检查点器的父图
const checkpointer = new MemorySaver();

const parent = new StateGraph(State)
  .addNode("subgraph", subgraph)
  .addEdge(START, "subgraph")
  .compile({ checkpointer });  // 传播到子图
```

## 边界

### 您能够配置的

✅ 选择检查点器实现
✅ 指定线程 ID
✅ 在任何检查点检索状态
✅ 在调用之间更新状态
✅ 设置暂停断点
✅ 访问状态历史
✅ 从任何检查点恢复

### 您不能配置的

❌ 检查点格式/模式（内部）
❌ 检查点时机（每个超级步）
❌ 线程 ID 结构（仅限任意字符串）

## 注意事项

### 1. 持久化需要 Thread ID

```typescript
// ❌ 错误 - 没有 thread_id，状态未保存
await graph.invoke({ data: "test" });  // 执行后丢失!

// ✅ 正确 - 始终提供 thread_id
const config = { configurable: { thread_id: "session-1" } };
await graph.invoke({ data: "test" }, config);
```

### 2. MemorySaver 不用于生产环境

```typescript
// ❌ 错误 - 重启时数据丢失
const checkpointer = new MemorySaver();  // 仅内存!

// ✅ 正确 - 使用持久化存储
import { PostgresSaver } from "@langchain/langgraph-checkpoint-postgres";
const checkpointer = await PostgresSaver.fromConnString("postgresql://...");
```

### 3. 恢复需要 null 输入

```typescript
// ❌ 错误 - 提供输入会重新开始
await graph.invoke({ new: "data" }, config);  // 从头重新开始

// ✅ 正确 - 使用 null 恢复
await graph.invoke(null, config);  // 从检查点恢复
```

### 4. 始终 Await 异步操作

```typescript
// ❌ 错误 - 忘记 await
const result = graph.invoke({ data: "test" }, config);
console.log(result.values);  // undefined!

// ✅ 正确
const result = await graph.invoke({ data: "test" }, config);
console.log(result.values);  // 可以工作!
```

### 5. 检查点器必须在编译时传递

```typescript
// ❌ 错误 - 检查点器在编译后
const graph = builder.compile();
graph.checkpointer = checkpointer;  // 太晚了!

// ✅ 正确 - 在编译时传递
const graph = builder.compile({ checkpointer });
```

## 相关链接

- [持久化指南](https://docs.langchain.com/oss/javascript/langgraph/persistence)
- [检查点器库](https://docs.langchain.com/oss/javascript/langgraph/persistence#checkpointer-libraries)
- [线程管理](https://docs.langchain.com/oss/javascript/langgraph/persistence#threads)
