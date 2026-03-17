---
name: langgraph-workflows
description: 理解工作流 vs Agent、预定义 vs 动态模式，以及使用 Send API 的编排器-工作器模式
language: js
---

# langgraph-workflows (JavaScript/TypeScript)

---
name: langgraph-workflows
description: 理解工作流 vs Agent、预定义 vs 动态模式，以及使用 Send API 的编排器-工作器模式
---

## 概述

LangGraph 同时支持**工作流**（预定义路径）和**Agent**（动态决策）。理解何时使用每种模式对于有效的 Agent 设计至关重要。

**关键区别：**
- **工作流**：预定义的代码路径，按特定顺序操作
- **Agent**：动态，定义自己的流程和工具使用
- **混合**：结合确定性和 Agent 步骤

## 决策表：工作流 vs Agent

| 特征 | 工作流 | Agent | 混合 |
|----------------|----------|-------|--------|
| **控制流** | 固定、预定义 | 动态、模型驱动 | 混合 |
| **可预测性** | 高 | 低 | 中 |
| **复杂性** | 简单 | 复杂 | 可变 |
| **使用场景** | 顺序任务 | 开放式问题 | 结构化灵活性 |
| **示例** | ETL、验证 | 研究、问答 | 审查批准 |

## 核心模式

### 1. 预定义工作流

按固定路径顺序执行：
- 数据处理流水线
- 验证工作流
- 多步骤转换

### 2. 动态 Agent

模型决定下一步：
- ReAct Agent（推理 + 行动）
- 工具调用循环
- 自主任务完成

### 3. 编排器-工作器模式

一个协调器委托给多个工作器：
- Map-reduce 操作
- 并行处理
- 多 Agent 协作

## 代码示例

### 基本工作流（预定义）

```typescript
import { StateGraph, StateSchema, START, END } from "@langchain/langgraph";
import { z } from "zod";

const WorkflowState = new StateSchema({
  data: z.string(),
  validated: z.boolean(),
  processed: z.boolean(),
});

const validate = async (state: typeof WorkflowState.State) => {
  const isValid = state.data.length > 0;
  return { validated: isValid };
};

const process = async (state: typeof WorkflowState.State) => {
  return {
    data: state.data.toUpperCase(),
    processed: true,
  };
};

// 固定工作流: validate → process
const workflow = new StateGraph(WorkflowState)
  .addNode("validate", validate)
  .addNode("process", process)
  .addEdge(START, "validate")
  .addEdge("validate", "process")  // 始终转到 process
  .addEdge("process", END)
  .compile();

const result = await workflow.invoke({ data: "hello" });
console.log(result);  // { data: 'HELLO', validated: true, processed: true }
```

### 动态 Agent（模型驱动）

```typescript
import { ChatAnthropic } from "@langchain/anthropic";
import { tool } from "@langchain/core/tools";
import { AIMessage, ToolMessage } from "@langchain/core/messages";
import { StateGraph, StateSchema, MessagesValue, END, START } from "@langchain/langgraph";
import { z } from "zod";

const search = tool(async ({ query }) => `Results for: ${query}`, {
  name: "search",
  description: "Search for information",
  schema: z.object({ query: z.string() }),
});

const calculate = tool(async ({ expression }) => eval(expression).toString(), {
  name: "calculate",
  description: "Calculate a mathematical expression",
  schema: z.object({ expression: z.string() }),
});

const AgentState = new StateSchema({
  messages: MessagesValue,
});

const model = new ChatAnthropic({ model: "claude-sonnet-4-5-20250929" });
const tools = [search, calculate];
const modelWithTools = model.bindTools(tools);

const agentNode = async (state: typeof AgentState.State) => {
  const response = await modelWithTools.invoke(state.messages);
  return { messages: [response] };
};

const toolNode = async (state: typeof AgentState.State) => {
  const lastMessage = state.messages.at(-1);
  if (!lastMessage || !AIMessage.isInstance(lastMessage)) {
    return { messages: [] };
  }

  const toolsByName = { [search.name]: search, [calculate.name]: calculate };
  const result = [];

  for (const toolCall of lastMessage.tool_calls ?? []) {
    const tool = toolsByName[toolCall.name];
    const observation = await tool.invoke(toolCall);
    result.push(observation);
  }

  return { messages: result };
};

const shouldContinue = (state: typeof AgentState.State) => {
  const lastMessage = state.messages.at(-1);
  if (lastMessage && AIMessage.isInstance(lastMessage) && lastMessage.tool_calls?.length) {
    return "tools";
  }
  return END;
};

// 动态 agent: 模型决定何时停止
const agent = new StateGraph(AgentState)
  .addNode("agent", agentNode)
  .addNode("tools", toolNode)
  .addEdge(START, "agent")
  .addConditionalEdges("agent", shouldContinue, ["tools", END])
  .addEdge("tools", "agent")
  .compile();
```

### 编排器-工作器模式

```typescript
import { StateGraph, StateSchema, Send, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

const OrchestratorState = new StateSchema({
  tasks: z.array(z.string()),
  results: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
  summary: z.string().optional(),
});

const orchestrator = (state: typeof OrchestratorState.State) => {
  // 将任务扩散到工作器
  return state.tasks.map(task => new Send("worker", { task }));
};

const worker = async (state: { task: string }) => {
  const result = `Completed: ${state.task}`;
  return { results: [result] };
};

const synthesize = async (state: typeof OrchestratorState.State) => {
  const summary = `Processed ${state.results.length} tasks`;
  return { summary };
};

const graph = new StateGraph(OrchestratorState)
  .addNode("worker", worker)
  .addNode("synthesize", synthesize)
  .addConditionalEdges(START, orchestrator, ["worker"])
  .addEdge("worker", "synthesize")
  .addEdge("synthesize", END)
  .compile();

const result = await graph.invoke({
  tasks: ["Task A", "Task B", "Task C"],
});
console.log(result.summary);  // "Processed 3 tasks"
```

### 混合：带 Agent 步骤的工作流

```typescript
import { StateGraph, StateSchema, START, END } from "@langchain/langgraph";
import { z } from "zod";

const HybridState = new StateSchema({
  input: z.string(),
  validated: z.boolean(),
  agentResponse: z.string().optional(),
  finalized: z.boolean(),
});

const validate = async (state: typeof HybridState.State) => {
  return { validated: true };
};

const agentProcess = async (state: typeof HybridState.State) => {
  // 动态 agent 逻辑在这里
  const response = `Agent processed: ${state.input}`;
  return { agentResponse: response };
};

const finalize = async (state: typeof HybridState.State) => {
  return { finalized: true };
};

// 混合: validate → agent → finalize
const hybrid = new StateGraph(HybridState)
  .addNode("validate", validate)      // 工作流
  .addNode("agent", agentProcess)     // Agent
  .addNode("finalize", finalize)      // 工作流
  .addEdge(START, "validate")
  .addEdge("validate", "agent")
  .addEdge("agent", "finalize")
  .addEdge("finalize", END)
  .compile();
```

### Map-Reduce 示例

```typescript
import { StateGraph, StateSchema, Send, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

const MapReduceState = new StateSchema({
  documents: z.array(z.string()),
  summaries: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
  finalSummary: z.string().optional(),
});

const mapDocuments = (state: typeof MapReduceState.State) => {
  return state.documents.map(doc => new Send("summarize", { doc }));
};

const summarize = async (state: { doc: string }) => {
  const summary = `Summary of: ${state.doc.slice(0, 50)}...`;
  return { summaries: [summary] };
};

const reduce = async (state: typeof MapReduceState.State) => {
  const finalSummary = state.summaries.join(" | ");
  return { finalSummary };
};

const graph = new StateGraph(MapReduceState)
  .addNode("summarize", summarize)
  .addNode("reduce", reduce)
  .addConditionalEdges(START, mapDocuments, ["summarize"])
  .addEdge("summarize", "reduce")
  .addEdge("reduce", END)
  .compile();

const result = await graph.invoke({
  documents: ["Doc 1 content...", "Doc 2 content...", "Doc 3 content..."],
});
```

### 并行知识库路由器

```typescript
import { StateGraph, StateSchema, Send, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

const RouterState = new StateSchema({
  query: z.string(),
  sources: z.array(z.string()),
  results: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
  final: z.string().optional(),
});

const classify = async (state: typeof RouterState.State) => {
  const query = state.query.toLowerCase();
  const sources: string[] = [];

  if (query.includes("code")) sources.push("github");
  if (query.includes("doc")) sources.push("notion");
  if (query.includes("message")) sources.push("slack");

  return { sources };
};

const routeToSources = (state: typeof RouterState.State) => {
  return state.sources.map(source => new Send(source, { query: state.query }));
};

const queryGithub = async (state: { query: string }) => {
  return { results: [`GitHub: ${state.query}`] };
};

const queryNotion = async (state: { query: string }) => {
  return { results: [`Notion: ${state.query}`] };
};

const querySlack = async (state: { query: string }) => {
  return { results: [`Slack: ${state.query}`] };
};

const synthesize = async (state: typeof RouterState.State) => {
  return { final: state.results.join(" + ") };
};

const graph = new StateGraph(RouterState)
  .addNode("classify", classify)
  .addNode("github", queryGithub)
  .addNode("notion", queryNotion)
  .addNode("slack", querySlack)
  .addNode("synthesize", synthesize)
  .addEdge(START, "classify")
  .addConditionalEdges("classify", routeToSources, ["github", "notion", "slack"])
  .addEdge("github", "synthesize")
  .addEdge("notion", "synthesize")
  .addEdge("slack", "synthesize")
  .addEdge("synthesize", END)
  .compile();
```

## 边界

### 您能够配置的

✅ 选择工作流 vs Agent 模式
✅ 混合确定性和 Agent 步骤
✅ 使用 Send API 进行并行执行
✅ 定义自定义编排器逻辑
✅ 控制工作器节点行为
✅ 使用 reducer 聚合结果

### 您不能配置的

❌ 更改 Send API 消息传递模型
❌ 绕过工作器状态隔离
❌ 修改并行执行机制
❌ 在运行时覆盖 reducer 行为

## 注意事项

### 1. Send 需要工作器状态隔离

```typescript
// ❌ 错误 - 工作器共享状态，导致冲突
const State = new StateSchema({
  sharedCounter: z.number(),  // 所有工作器修改相同的计数器!
});

// ✅ 正确 - 每个工作器获得隔离的输入
const worker = async (state: { task: string }) => {
  // state 对此工作器是隔离的
  return { results: [process(state.task)] };
};
```

### 2. Send 需要累加器 Reducer

```typescript
// ❌ 错误 - 最后一个工作器覆盖所有其他工作器
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

### 3. 工作流可能过于僵化

```typescript
// ❌ 反模式 - 过于僵化的工作流
.addEdge("validate", "process")  // 始终继续，没有错误处理

// ✅ 更好 - 添加条件逻辑
const routeAfterValidate = (state) => {
  if (!state.validated) return "errorHandler";
  return "process";
};

.addConditionalEdges("validate", routeAfterValidate, ["process", "errorHandler"]);
```

### 4. 始终 Await 异步节点

```typescript
// ❌ 错误 - 忘记 await
const result = graph.invoke({ data: "test" });
console.log(result.output);  // undefined!

// ✅ 正确
const result = await graph.invoke({ data: "test" });
console.log(result.output);  // 可以工作!
```

## 相关链接

- [工作流和 Agent (JavaScript)](https://docs.langchain.com/oss/javascript/langgraph/workflows-agents)
- [Send API 指南](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api#map-reduce-and-the-send-api)
- [Map-Reduce 示例](https://docs.langchain.com/oss/javascript/langgraph/use-graph-api#map-reduce-and-the-send-api)
