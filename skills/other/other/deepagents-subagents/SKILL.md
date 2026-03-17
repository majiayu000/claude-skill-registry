---
name: deepagents-subagents
description: 在 Deep Agents 中使用 SubAgentMiddleware 启动子代理进行任务委托、上下文隔离和专门工作。
language: js
---

# deepagents-subagents (JavaScript/TypeScript)

## 概述

SubAgentMiddleware 通过 `task` 工具实现任务委托。优势：上下文隔离、专业化、token 效率、并行执行。

**默认子代理**："通用型" - 自动可用，具有与主代理相同的工具/配置。

## 定义子代理

### 基于字典的子代理

```typescript
import { createDeepAgent } from "deepagents";
import { tool } from "langchain";
import { z } from "zod";

const searchPapers = tool(
  async ({ query }) => `找到 10 篇关于 ${query} 的论文`,
  {
    name: "search_papers",
    description: "搜索学术论文",
    schema: z.object({ query: z.string() }),
  }
);

const agent = await createDeepAgent({
  subagents: [
    {
      name: "research",
      description: "研究学术论文并提供摘要",
      systemPrompt: "你是一个研究助手。提供简洁的摘要。",
      tools: [searchPapers],
      model: "claude-sonnet-4-5-20250929",  // 可选
    }
  ]
});

const result = await agent.invoke({
  messages: [{ role: "user", content: "研究关于 transformers 的最新论文" }]
});
```

### CompiledSubAgent（自定义图）

```typescript
import { createDeepAgent, CompiledSubAgent } from "deepagents";

const weatherGraph = createWeatherGraph();  // 你的自定义 LangGraph

const weatherSubagent = new CompiledSubAgent({
  name: "weather",
  description: "获取天气预报",
  runnable: weatherGraph
});

const agent = await createDeepAgent({
  subagents: [weatherSubagent]
});
```

## 代码示例

### 示例 1：研究子代理

```typescript
import { createDeepAgent } from "deepagents";
import { tool } from "langchain";
import { z } from "zod";

const webSearch = tool(
  async ({ query }) => `搜索结果：${query}`,
  {
    name: "web_search",
    description: "搜索网络",
    schema: z.object({ query: z.string() }),
  }
);

const agent = await createDeepAgent({
  subagents: [
    {
      name: "researcher",
      description: "进行网络研究并汇编发现",
      systemPrompt: "彻底搜索，保存到 /research/，返回摘要",
      tools: [webSearch],
    }
  ]
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "研究电动汽车的市场趋势"
  }]
});
```

### 示例 2：具有 HITL 的子代理

```typescript
import { createDeepAgent } from "deepagents";
import { MemorySaver } from "@langchain/langgraph";

const agent = await createDeepAgent({
  subagents: [
    {
      name: "code-deployer",
      description: "将代码部署到生产环境",
      systemPrompt: "安全地部署代码并进行所有检查",
      tools: [runTests, deployToProd],
      interruptOn: { deploy_to_prod: true },  // 需要审批
    }
  ],
  checkpointer: new MemorySaver()  // 必需
});
```

### 示例 3：具有自定义技能的子代理

```typescript
const agent = await createDeepAgent({
  skills: ["/main-skills/"],
  subagents: [
    {
      name: "python-expert",
      description: "Python 代码审查和重构",
      systemPrompt: "审查 Python 代码以获得最佳实践",
      tools: [readCode, suggestImprovements],
      skills: ["/python-skills/"],  // 子代理特定
    }
  ]
});
// 自定义子代理默认不继承主技能
// 通用子代理确实继承主技能
```

## 边界

### Agent 可以配置的内容
✅ 子代理名称、描述、工具
✅ 每个子代理的不同模型
✅ 子代理特定的提示、中间件、技能
✅ 子代理工具的 HITL

### Agent 不能配置的内容
❌ 更改 `task` 工具名称
❌ 使子代理有状态
❌ 在子代理之间共享状态
❌ 删除默认的通用子代理

## 注意事项

### 1. 子代理是无状态的
```typescript
// ❌ 子代理不记得之前的调用
await agent.invoke({messages: [{role: "user", content: "研究 X"}]});
await agent.invoke({messages: [{role: "user", content: "你发现了什么？"}]});
// 每次都是新的子代理

// ✅ 主代理维护对话内存
```

### 2. 自定义子代理不继承技能
```typescript
// ❌ 子代理不会有主技能
await createDeepAgent({
  skills: ["/main-skills/"],
  subagents: [{ name: "helper", ... }]
});

// ✅ 明确提供技能
await createDeepAgent({
  skills: ["/main-skills/"],
  subagents: [{
    name: "helper",
    skills: ["/helper-skills/"],
    ...
  }]
});
```

### 3. 子代理中断需要主 Checkpointer
```typescript
// ❌ 缺少 checkpointer
await createDeepAgent({
  subagents: [{
    name: "deployer",
    interruptOn: { deploy: true }
  }]
});

// ✅ 主代理上的 Checkpointer
await createDeepAgent({
  subagents: [{
    name: "deployer",
    interruptOn: { deploy: true }
  }],
  checkpointer: new MemorySaver()
});
```

## 完整文档
- [子代理指南](https://docs.langchain.com/oss/javascript/deepagents/subagents)
- [SubAgent 中间件](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#subagent)
- [任务委托](https://docs.langchain.com/oss/javascript/deepagents/harness#task-delegation-subagents)
