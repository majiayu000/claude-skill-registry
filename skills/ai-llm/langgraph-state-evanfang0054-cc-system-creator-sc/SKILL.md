---
name: langgraph-state
description: 在 LangGraph 中管理状态：模式、reducer、通道和消息传递，用于协调 Agent 执行
language: js
---

# langgraph-state (JavaScript/TypeScript)

---
name: langgraph-state
description: 在 LangGraph 中管理状态 - 模式、reducer、通道和消息传递，用于协调 Agent 执行
---

## 概述

状态是 LangGraph 中的核心数据结构，在整个图执行期间持久存在。正确的状态管理对于构建可靠的 Agent 至关重要。

**核心概念：**
- **StateSchema**：定义状态结构和类型
- **Reducers**：控制如何应用状态更新（ReducedValue）
- **通道（Channels）**：低级状态管理原语
- **消息传递**：节点如何通过状态更新进行通信

## 决策表：状态更新策略

| 需求 | 解决方案 | 使用场景 |
|------|----------|----------|
| 覆盖值 | 普通 Zod 模式 | 简单字段如字符串 |
| 追加到列表 | `ReducedValue` 与 concat | 日志、累积数据 |
| 自定义逻辑 | 自定义 reducer 函数 | 复杂合并、验证 |
| 消息 | `MessagesValue` | 聊天应用程序 |

## 代码示例

### 基本状态管理

```typescript
import { StateGraph, StateSchema, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  input: z.string(),
  processed: z.string(),
  count: z.number(),
});

const process = async (state: typeof State.State) => {
  return {
    processed: state.input.toUpperCase(),
    count: state.count + 1,
  };
};

const graph = new StateGraph(State)
  .addNode("process", process)
  .addEdge(START, "process")
  .addEdge("process", END)
  .compile();

const result = await graph.invoke({ input: "hello", count: 0 });
console.log(result);  // { input: 'hello', processed: 'HELLO', count: 1 }
```

### 带Reducer 的消息

```typescript
import { StateSchema, MessagesValue, StateGraph, START, END } from "@langchain/langgraph";
import { HumanMessage, AIMessage } from "@langchain/core/messages";

const MessagesState = new StateSchema({
  messages: MessagesValue,
});

const addResponse = async (state: typeof MessagesState.State) => {
  const lastMessage = state.messages.at(-1);
  const userMsg = lastMessage?.content || "";
  return {
    messages: [new AIMessage({ content: `Response to: ${userMsg}` })],
  };
};

const graph = new StateGraph(MessagesState)
  .addNode("respond", addResponse)
  .addEdge(START, "respond")
  .addEdge("respond", END)
  .compile();

const result = await graph.invoke({
  messages: [new HumanMessage({ content: "Hello!" })],
});
console.log(result.messages.length);  // 2 (原始 + 响应)
```

### 使用 ReducedValue 的自定义 Reducer

```typescript
import { StateSchema, ReducedValue, START, END, StateGraph } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  metadata: new ReducedValue(
    z.record(z.string(), z.any()).default(() => ({})),
    {
      inputSchema: z.record(z.string(), z.any()),
      reducer: (current, update) => ({ ...current, ...update }),
    }
  ),
  data: z.string(),
});

const updateMetadata = async (state: typeof State.State) => {
  return { metadata: { timestamp: "2024-01-01" } };
};

const graph = new StateGraph(State)
  .addNode("update", updateMetadata)
  .addEdge(START, "update")
  .addEdge("update", END)
  .compile();

const result = await graph.invoke({
  metadata: { user: "alice" },
  data: "test",
});
// metadata 被合并: { user: "alice", timestamp: "2024-01-01" }
```

### 使用 ReducedValue 的列表累积

```typescript
import { StateSchema, ReducedValue } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  items: new ReducedValue(
    z.array(z.string()).default(() => []),
    {
      inputSchema: z.array(z.string()),
      reducer: (current, update) => current.concat(update),
    }
  ),
});

const addItems = async (state: typeof State.State) => {
  return { items: ["new_item"] };
};

const graph = new StateGraph(State)
  .addNode("add", addItems)
  .addEdge(START, "add")
  .addEdge("add", END)
  .compile();

const result = await graph.invoke({ items: ["old1", "old2"] });
console.log(result.items);  // ['old1', 'old2', 'new_item']
```

### 使用通道 API

```typescript
import { StateGraph, LastValue, BinaryOperatorAggregate } from "@langchain/langgraph";

interface State {
  counter: number;
  logs: string[];
}

const graph = new StateGraph<State>({
  channels: {
    counter: new BinaryOperatorAggregate<number>(
      (x, y) => x + y,
      () => 0
    ),
    logs: new BinaryOperatorAggregate<string[]>(
      (x, y) => x.concat(y),
      () => []
    ),
  },
});
```

### 部分状态更新

```typescript
import { StateSchema, StateGraph, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  field1: z.string(),
  field2: z.string(),
  field3: z.string(),
});

const updateField1 = async (state: typeof State.State) => {
  // 只更新 field1，其他不变
  return { field1: "updated" };
};

const updateField2 = async (state: typeof State.State) => {
  // 只更新 field2
  return { field2: "also updated" };
};

const graph = new StateGraph(State)
  .addNode("node1", updateField1)
  .addNode("node2", updateField2)
  .addEdge(START, "node1")
  .addEdge("node1", "node2")
  .addEdge("node2", END)
  .compile();

const result = await graph.invoke({
  field1: "original1",
  field2: "original2",
  field3: "original3",
});
// field1: "updated", field2: "also updated", field3: "original3"
```

## 边界

### 您能够配置的

✅ 使用 Zod 定义自定义状态模式
✅ 通过 ReducedValue 添加 reducer
✅ 创建自定义 reducer 函数
✅ 使用内置通道
✅ 使用 MessagesValue 进行聊天
✅ 部分状态更新
✅ 嵌套状态结构

### 您不能配置的

❌ 编译后更改状态模式
❌ 在节点函数外访问状态
❌ 直接修改状态（必须返回更新）
❌ 在不同图之间共享状态

## 注意事项

### 1. 忘记为 Arrays 添加 Reducer

```typescript
// ❌ 错误 - 数组将被覆盖
const State = new StateSchema({
  items: z.array(z.string()),  // 没有 reducer!
});

// 节点 1 返回: { items: ["A"] }
// 节点 2 返回: { items: ["B"] }
// 最终状态: { items: ["B"] }  // A 丢失!

// ✅ 正确
import { ReducedValue } from "@langchain/langgraph";

const State = new StateSchema({
  items: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
});
// 最终状态: { items: ["A", "B"] }
```

### 2. 状态更新必须返回 Partial

```typescript
// ❌ 错误 - 返回整个状态对象
const myNode = async (state: typeof State.State) => {
  state.field = "updated";
  return state;  // 不要这样做!
};

// ✅ 正确 - 返回部分更新
const myNode = async (state: typeof State.State) => {
  return { field: "updated" };
};
```

### 3. 默认值

```typescript
// ❌ 有风险 - 没有默认处理
const State = new StateSchema({
  count: z.number(),  // 如果是 undefined 怎么办?
});

const increment = async (state: typeof State.State) => {
  return { count: state.count + 1 };  // 如果 count undefined 可能出错
};

// ✅ 更好 - 在模式中使用默认值
const State = new StateSchema({
  count: z.number().default(0),
});
```

### 4. 始终 Await 节点

```typescript
// ❌ 错误 - 忘记 await
const result = graph.invoke({ input: "test" });
console.log(result.output);  // undefined (Promise!)

// ✅ 正确
const result = await graph.invoke({ input: "test" });
console.log(result.output);  // 可以工作!
```

## 相关链接

- [StateSchema 指南](https://docs.langchain.com/oss/javascript/langgraph/graph-api#schema)
- [通道 API](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api#channels-api)
- [ReducedValue](https://docs.langchain.com/oss/javascript/releases/changelog#standard-json-schema-support)
