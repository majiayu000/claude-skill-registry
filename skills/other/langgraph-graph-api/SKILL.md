---
name: langgraph-graph-api
description: 使用 StateGraph、节点、边、START/END 节点和 Command API 构建图，结合控制流与状态更新
language: js
---

# langgraph-graph-api (JavaScript/TypeScript)

---
name: langgraph-graph-api
description: 使用 StateGraph、节点、边、START/END 节点和 Command API 构建图，结合控制流与状态更新
---

## 概述

LangGraph Graph API 允许您将 Agent 工作流定义为由**节点**（函数）和**边**（控制流）组成的有向图。这提供了对 Agent 编排的细粒度控制。

**核心组件：**
- **StateGraph**：构建有状态图的主要类
- **节点**：执行工作并更新状态的函数
- **边**：定义执行顺序（静态或条件）
- **START/END**：标记图入口和出口点的特殊节点
- **Command**：结合状态更新与动态路由

## 决策表：边类型

| 需求 | 边类型 | 何时使用 |
|------|-----------|-------------|
| 始终转到同一节点 | `addEdge()` | 固定、确定性流 |
| 基于状态路由 | `addConditionalEdges()` | 动态分支逻辑 |
| 扩散到多个节点 | `Send` API | Map-reduce、并行执行 |
| 更新状态并路由 | `Command` | 在单个节点中组合逻辑 |

## 核心概念

### 1. 图执行模型

LangGraph 使用受 Google Pregel 启发的**消息传递**模型：
- 执行以**超级步**（离散迭代）进行
- 并行节点属于同一超级步
- 顺序节点属于不同的超级步
- 当所有节点不活跃且没有消息在传输时，图结束

### 2. 节点

**节点**是异步函数，它们：
- 接收当前状态作为输入
- 执行计算或副作用
- 返回状态更新（部分或全部）

```typescript
const myNode = async (state: State): Promise<Partial<State>> => {
  // 节点只是异步函数!
  return { key: "updated_value" };
};
```

### 3. 边

| 边类型 | 描述 | 示例 |
|-----------|-------------|---------|
| **静态** | 始终路由到同一节点 | `addEdge("A", "B")` |
| **条件** | 基于状态/逻辑路由 | `addConditionalEdges("A", router)` |
| **动态 (Send)** | 扩散到多个节点 | `new Send("worker", {...})` |
| **Command** | 状态更新 + 路由 | `new Command({ goto: "B" })` |

### 4. 特殊节点

- **START**：图的入口点（虚拟节点）
- **END**：终端节点（图停止）

## 代码示例

### 带静态边的基本图

```typescript
import { StateGraph, StateSchema, START, END } from "@langchain/langgraph";
import { z } from "zod";

// 1. 定义状态
const State = new StateSchema({
  input: z.string(),
  output: z.string(),
});

// 2. 定义节点
const processInput = async (state: typeof State.State) => {
  return { output: `Processed: ${state.input}` };
};

const finalize = async (state: typeof State.State) => {
  return { output: state.output.toUpperCase() };
};

// 3. 构建图
const graph = new StateGraph(State)
  .addNode("process", processInput)
  .addNode("finalize", finalize)
  .addEdge(START, "process")       // 入口点
  .addEdge("process", "finalize")  // 静态边
  .addEdge("finalize", END)        // 出口点
  .compile();

// 4. 执行
const result = await graph.invoke({ input: "hello" });
console.log(result.output);  // "PROCESSED: HELLO"
```

### 条件边（分支）

```typescript
import { StateGraph, StateSchema, ConditionalEdgeRouter, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  query: z.string(),
  route: z.string(),
  result: z.string().optional(),
});

const classify = async (state: typeof State.State) => {
  if (state.query.toLowerCase().includes("weather")) {
    return { route: "weather" };
  }
  return { route: "general" };
};

const weatherNode = async (state: typeof State.State) => {
  return { result: "Sunny, 72°F" };
};

const generalNode = async (state: typeof State.State) => {
  return { result: "General response" };
};

// 路由器函数
const routeQuery: ConditionalEdgeRouter<typeof State, "weather" | "general"> = (state) => {
  return state.route as "weather" | "general";
};

const graph = new StateGraph(State)
  .addNode("classify", classify)
  .addNode("weather", weatherNode)
  .addNode("general", generalNode)
  .addEdge(START, "classify")
  // 基于状态的条件边
  .addConditionalEdges(
    "classify",
    routeQuery,
    ["weather", "general"]  // 可能的目标
  )
  .addEdge("weather", END)
  .addEdge("general", END)
  .compile();

const result = await graph.invoke({ query: "What's the weather?" });
```

### 使用 Command 进行状态 + 路由

```typescript
import { StateGraph, StateSchema, Command, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  count: z.number(),
  result: z.string(),
});

const nodeA = async (state: typeof State.State) => {
  const newCount = state.count + 1;

  if (newCount > 5) {
    // 转到 nodeC
    return new Command({
      update: { count: newCount, result: "Going to C" },
      goto: "nodeC"
    });
  } else {
    // 转到 nodeB
    return new Command({
      update: { count: newCount, result: "Going to B" },
      goto: "nodeB"
    });
  }
};

const nodeB = async (state: typeof State.State) => {
  return { result: `B executed, count=${state.count}` };
};

const nodeC = async (state: typeof State.State) => {
  return { result: `C executed, count=${state.count}` };
};

const graph = new StateGraph(State)
  .addNode("nodeA", nodeA, { ends: ["nodeB", "nodeC"] })  // 指定可能的路由
  .addNode("nodeB", nodeB)
  .addNode("nodeC", nodeC)
  .addEdge(START, "nodeA")
  .addEdge("nodeB", END)
  .addEdge("nodeC", END)
  .compile();

const result1 = await graph.invoke({ count: 0 });
console.log(result1.result);  // "B executed, count=1"

const result2 = await graph.invoke({ count: 5 });
console.log(result2.result);  // "C executed, count=6"
```

### 使用 Send API 的 Map-Reduce

```typescript
import { StateGraph, StateSchema, Send, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  items: z.array(z.string()),
  results: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
  final: z.string().optional(),
});

const fanOut = (state: typeof State.State) => {
  // 将每个项目发送到工作节点
  return state.items.map(item =>
    new Send("worker", { item })
  );
};

const worker = async (state: { item: string }) => {
  // 处理单个项目
  return { results: [`Processed: ${state.item}`] };
};

const aggregate = async (state: typeof State.State) => {
  // 合并结果
  return { final: state.results.join(", ") };
};

const graph = new StateGraph(State)
  .addNode("worker", worker)
  .addNode("aggregate", aggregate)
  .addConditionalEdges(START, fanOut, ["worker"])
  .addEdge("worker", "aggregate")
  .addEdge("aggregate", END)
  .compile();

const result = await graph.invoke({ items: ["A", "B", "C"] });
console.log(result.final);  // "Processed: A, Processed: B, Processed: C"
```

### 带循环的图

```typescript
import { StateGraph, StateSchema, ConditionalEdgeRouter, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  count: z.number(),
  maxIterations: z.number(),
});

const increment = async (state: typeof State.State) => {
  return { count: state.count + 1 };
};

const shouldContinue: ConditionalEdgeRouter<typeof State, "increment"> = (state) => {
  if (state.count >= state.maxIterations) {
    return END;
  }
  return "increment";
};

const graph = new StateGraph(State)
  .addNode("increment", increment)
  .addEdge(START, "increment")
  .addConditionalEdges("increment", shouldContinue, ["increment", END])
  .compile();

const result = await graph.invoke({ count: 0, maxIterations: 5 });
console.log(result.count);  // 5
```

### 带选项的编译

```typescript
import { MemorySaver } from "@langchain/langgraph";

const checkpointer = new MemorySaver();

const graph = new StateGraph(State)
  .addNode("nodeA", nodeA)
  .addEdge(START, "nodeA")
  .addEdge("nodeA", END)
  .compile({
    checkpointer,                    // 启用持久化
    interruptBefore: ["nodeA"],      // 在节点之前设置断点
    interruptAfter: ["nodeA"],       // 在节点之后设置断点
  });
```

## 边界

### Agent 能够配置的

✅ 定义自定义节点（任何异步函数）
✅ 在节点之间添加静态边
✅ 添加带自定义逻辑的条件边
✅ 使用 Command 进行组合的状态/路由
✅ 使用条件终止创建循环
✅ 使用 Send API 扩散（map-reduce）
✅ 设置断点（interruptBefore/After）
✅ 自定义状态模式
✅ 指定检查点器用于持久化

### Agent 不能配置的

❌ 修改 START/END 节点行为
❌ 更改超级步执行模型
❌ 修改消息传递协议
❌ 覆盖图编译逻辑
❌ 绕过状态更新机制

## 注意事项

### 1. 必须先编译再执行

```typescript
// ❌ 错误
const builder = new StateGraph(State).addNode("node", func);
await builder.invoke({ input: "test" });  // 错误!

// ✅ 正确
const graph = builder.compile();
await graph.invoke({ input: "test" });
```

### 2. 条件边目标必须存在

```typescript
// ❌ 错误 - "missingNode" 未添加到图中
const router = (state) => "missingNode";

builder.addConditionalEdges("nodeA", router, ["missingNode"]);

// ✅ 正确 - 添加所有可能的目标
builder.addNode("missingNode", func);
builder.addConditionalEdges("nodeA", router, ["missingNode"]);
```

### 3. Command 需要 `ends` 参数

```typescript
// ❌ 错误 - 未指定 ends
const nodeA = async (state) => {
  return new Command({ goto: "nodeB" });
};

builder.addNode("nodeA", nodeA);  // 使用 Command 时出错!

// ✅ 正确 - 指定可能的目标
builder.addNode("nodeA", nodeA, { ends: ["nodeB", "nodeC"] });
```

### 4. 循环需要退出条件

```typescript
// ❌ 错误 - 无限循环
builder
  .addEdge("nodeA", "nodeB")
  .addEdge("nodeB", "nodeA");  // 无路可出!

// ✅ 正确 - 到 END 的条件边
const shouldContinue = (state) => {
  if (state.count > 10) return END;
  return "nodeB";
};

builder.addConditionalEdges("nodeA", shouldContinue, ["nodeB", END]);
```

### 5. Send API 需要 Reducer

```typescript
// ❌ 错误 - 结果将被覆盖
const State = new StateSchema({
  results: z.array(z.string()),  // 没有 reducer!
});

// ✅ 正确 - 使用 ReducedValue
import { ReducedValue } from "@langchain/langgraph";

const State = new StateSchema({
  results: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
});
```

### 6. START 是虚拟的，不能作为目标

```typescript
// ❌ 错误 - 无法路由回 START
builder.addEdge("nodeA", START);  // 错误!

// ✅ 正确 - 使用命名的入口节点代替
builder.addNode("entry", entryFunc);
builder.addEdge(START, "entry");
builder.addEdge("nodeA", "entry");  // 可以
```

### 7. 始终使用 Await

```typescript
// ❌ 错误 - 忘记 await
const result = graph.invoke({ input: "test" });
console.log(result.output);  // undefined (Promise!)

// ✅ 正确
const result = await graph.invoke({ input: "test" });
console.log(result.output);  // 可以工作!
```

## 相关链接

- [图 API 参考 (JavaScript)](https://docs.langchain.com/oss/javascript/langgraph/graph-api)
- [使用图 API](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api)
- [Command 文档](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api#combine-control-flow-and-state-updates-with-command)
- [Send API 指南](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api#map-reduce-and-the-send-api)
- [条件分支](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api#create-and-control-loops)
