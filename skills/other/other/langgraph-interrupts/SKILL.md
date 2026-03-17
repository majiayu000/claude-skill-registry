---
name: langgraph-interrupts
description: 人机交互与动态中断和断点：暂停执行以供人工审查和使用 Command 恢复
language: js
---

# langgraph-interrupts (JavaScript/TypeScript)

---
name: langgraph-interrupts
description: 人机交互与动态中断和断点 - 暂停执行以供人工审查和使用 Command 恢复
---

## 概述

中断通过暂停图执行以等待外部输入来实现人机交互模式。LangGraph 保存状态并无限期等待，直到您恢复执行。

**关键类型：**
- **动态中断**：在节点中调用的 `interrupt()` 函数
- **静态断点**：在编译时设置的 `interruptBefore`/`interruptAfter`

## 决策表：中断类型

| 类型 | 设置时机 | 使用场景 |
|------|----------|----------|
| 动态 (`interrupt()`) | 在节点代码内 | 基于逻辑的条件暂停 |
| 静态 (`interruptBefore`) | 在编译时 | 在特定节点之前调试/测试 |
| 静态 (`interruptAfter`) | 在编译时 | 在特定节点之后审查输出 |

## 代码示例

### 动态中断

```typescript
import { interrupt, Command } from "@langchain/langgraph";
import { MemorySaver } from "@langchain/langgraph";

const reviewNode = async (state) => {
  // 有条件地暂停以供审查
  if (state.needsReview) {
    // 暂停并向用户展示数据
    const userResponse = interrupt({
      action: "review",
      data: state.draft,
      question: "Approve this draft?",
    });

    // userResponse 来自 Command({ resume: ... })
    if (userResponse === "reject") {
      return { status: "rejected" };
    }
  }

  return { status: "approved" };
};

const checkpointer = new MemorySaver();

const graph = new StateGraph(State)
  .addNode("review", reviewNode)
  .addEdge(START, "review")
  .addEdge("review", END)
  .compile({ checkpointer });  // 必需！

// 初始调用 - 将暂停
const config = { configurable: { thread_id: "1" } };
const result = await graph.invoke(
  { needsReview: true, draft: "content" },
  config
);

// 检查中断
if ("__interrupt__" in result) {
  console.log(result.__interrupt__);  // 查看中断负载
}

// 使用用户决策恢复
const finalResult = await graph.invoke(
  new Command({ resume: "approve" }),  // 用户的响应
  config
);
```

### 静态断点

```typescript
const checkpointer = new MemorySaver();

const graph = new StateGraph(State)
  .addNode("step1", step1)
  .addNode("step2", step2)
  .addNode("step3", step3)
  .addEdge(START, "step1")
  .addEdge("step1", "step2")
  .addEdge("step2", "step3")
  .addEdge("step3", END)
  .compile({
    checkpointer,
    interruptBefore: ["step2"],  // 在 step2 之前暂停
    interruptAfter: ["step3"],   // 在 step3 之后暂停
  });

const config = { configurable: { thread_id: "1" } };

// 运行到第一个断点
await graph.invoke({ data: "test" }, config);

// 恢复（在下一个断点暂停）
await graph.invoke(null, config);  // null = 恢复

// 再次恢复
await graph.invoke(null, config);
```

### 工具审查模式

```typescript
import { interrupt, Command } from "@langchain/langgraph";

const toolExecutor = async (state) => {
  const toolCalls = state.messages.at(-1)?.tool_calls || [];
  const results = [];

  for (const toolCall of toolCalls) {
    // 为每个工具调用暂停
    const userDecision = interrupt({
      tool: toolCall.name,
      args: toolCall.args,
      question: "Execute this tool?",
    });

    let result;
    if (userDecision.type === "approve") {
      // 执行工具
      result = await executeTool(toolCall);
    } else if (userDecision.type === "edit") {
      // 使用编辑后的参数
      result = await executeTool(userDecision.args);
    } else {  // reject
      result = "Tool execution rejected";
    }

    // 存储结果
    results.push(new ToolMessage({
      content: result,
      tool_call_id: toolCall.id,
    }));
  }

  return { messages: results };
};

// 使用
const result = await graph.invoke({ messages: [...] }, config);

// 审查并批准
await graph.invoke(new Command({ resume: { type: "approve" } }), config);

// 或编辑参数
await graph.invoke(
  new Command({ resume: { type: "edit", args: { query: "modified" } } }),
  config
);

// 或拒绝
await graph.invoke(new Command({ resume: { type: "reject" } }), config);
```

### 在中断期间编辑状态

```typescript
const config = { configurable: { thread_id: "1" } };

// 运行到中断
await graph.invoke({ data: "test" }, config);

// 在恢复之前修改状态
await graph.updateState(config, { data: "manually edited" });

// 使用编辑后的状态恢复
await graph.invoke(null, config);
```

### 带中断的流式处理

```typescript
const config = {
  configurable: { thread_id: "1" },
  streamMode: ["updates", "messages"] as const,
};

for await (const [mode, chunk] of await graph.stream({ query: "test" }, config)) {
  if (mode === "updates") {
    if ("__interrupt__" in chunk) {
      // 处理中断
      const interruptInfo = chunk.__interrupt__[0].value;
      const userInput = await getUserInput(interruptInfo);

      // 恢复
      await graph.invoke(new Command({ resume: userInput }), config);
      break;
    }
  }
}
```

## 边界

### 您能够配置的

✅ 在节点中的任何位置调用 `interrupt()`
✅ 设置编译时断点
✅ 使用 `Command({ resume: ... })` 恢复
✅ 在中断期间编辑状态
✅ 在处理中断时流式传输
✅ 条件中断逻辑

### 您不能配置的

❌ 在没有检查点器的情况下中断
❌ 修改中断机制
❌ 在没有 thread_id 的情况下恢复

## 注意事项

### 1. 需要检查点器

```typescript
// ❌ 错误 - 没有检查点器
const graph = builder.compile();  // 没有持久化!
await graph.invoke(...);  // 中断不起作用

// ✅ 正确
const checkpointer = new MemorySaver();
const graph = builder.compile({ checkpointer });
```

### 2. 需要 Thread ID

```typescript
// ❌ 错误 - 没有 thread_id
await graph.invoke({ data: "test" });  // 无法恢复!

// ✅ 正确
const config = { configurable: { thread_id: "session-1" } };
await graph.invoke({ data: "test" }, config);
```

### 3. 使用 Command 恢复，而非对象

```typescript
// ❌ 错误 - 传递常规对象
await graph.invoke({ resumeData: "approve" }, config);  // 重新开始!

// ✅ 正确 - 使用 Command
import { Command } from "@langchain/langgraph";
await graph.invoke(new Command({ resume: "approve" }), config);
```

### 4. 始终使用 Await

```typescript
// ❌ 错误
const result = graph.invoke({}, config);
console.log(result);  // Promise!

// ✅ 正确
const result = await graph.invoke({}, config);
console.log(result);
```

## 相关链接

- [中断指南](https://docs.langchain.com/oss/javascript/langgraph/interrupts)
- [人机交互](https://docs.langchain.com/oss/javascript/langgraph/human-in-the-loop)
- [Command API](https://docs.langchain.com/oss/javascript/langgraph/graph-api#command)
