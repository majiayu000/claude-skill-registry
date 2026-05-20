---
name: deepagents-hitl
description: 在 Deep Agents 中实现人工审批工作流，使用 interruptOn 参数对敏感工具操作进行人工干预。
language: js
---

# deepagents-hitl (JavaScript/TypeScript)

## 概述

HITL 中间件为工具调用添加人工监督。执行暂停以等待人工决策：**批准**、**编辑**或**拒绝**。

需要 checkpointer 在中断期间保存状态。

## 基本设置

```typescript
import { createDeepAgent } from "deepagents";
import { MemorySaver } from "@langchain/langgraph";

const agent = await createDeepAgent({
  interruptOn: {
    write_file: true,  // 允许所有决策
    execute_sql: { allowedDecisions: ["approve", "reject"] },  // 不允许编辑
    read_file: false,  // 无中断
  },
  checkpointer: new MemorySaver()  // 必需
});
```

## 决策表

| 工具类型 | 配置 | 决策 | 使用场景 |
|-----------|--------|-----------|----------|
| 破坏性 | `true` | 批准/编辑/拒绝 | write_file、delete |
| 关键 | `{allowedDecisions: [...]}` | 仅批准/拒绝 | deploy、SQL |
| 安全 | `false` | 无 | read_file |

## 代码示例

### 示例 1：基本审批

```typescript
import { createDeepAgent } from "deepagents";
import { MemorySaver } from "@langchain/langgraph";
import { Command } from "@langchain/langgraph";

const agent = await createDeepAgent({
  interruptOn: { write_file: true },
  checkpointer: new MemorySaver()
});

const config = { configurable: { thread_id: "session-1" } };

// 步骤 1：调用（触发中断）
let result = await agent.invoke({
  messages: [{ role: "user", content: "将配置写入 /prod.yaml" }]
}, config);

// 步骤 2：检查中断
const state = await agent.getState(config);
if (state.next) {
  const interrupt = state.tasks[0];
  console.log("中断:", interrupt);
}

// 步骤 3：批准
await agent.updateState(config, {
  messages: [
    new Command({
      resume: {
        decisions: [{ type: "approve" }]
      }
    })
  ]
});

// 步骤 4：继续
result = await agent.invoke(null, config);
```

### 示例 2：执行前编辑

```typescript
const agent = await createDeepAgent({
  interruptOn: { execute_sql: true },
  checkpointer: new MemorySaver()
});

const config = { configurable: { thread_id: "session-1" } };

// 调用
await agent.invoke({
  messages: [{ role: "user", content: "删除旧用户" }]
}, config);

// 编辑 SQL
await agent.updateState(config, {
  messages: [
    new Command({
      resume: {
        decisions: [{
          type: "edit",
          args: {
            query: "DELETE FROM users WHERE last_login < '2020-01-01' LIMIT 100"
          }
        }]
      }
    })
  ]
});

// 继续
await agent.invoke(null, config);
```

### 示例 3：拒绝并提供反馈

```typescript
const agent = await createDeepAgent({
  interruptOn: { deploy_code: true },
  checkpointer: new MemorySaver()
});

const config = { configurable: { thread_id: "session-1" } };

await agent.invoke({
  messages: [{ role: "user", content: "部署到生产环境" }]
}, config);

// 拒绝
await agent.updateState(config, {
  messages: [
    new Command({
      resume: {
        decisions: [{
          type: "reject",
          message: "测试尚未通过"
        }]
      }
    })
  ]
});

await agent.invoke(null, config);
```

### 示例 4：自定义中间件

```typescript
import { createAgent, humanInTheLoopMiddleware } from "langchain";
import { MemorySaver } from "@langchain/langgraph";

const agent = createAgent({
  model: "gpt-4",
  tools: [deployTool, sendEmailTool],
  middleware: [
    humanInTheLoopMiddleware({
      interruptOn: {
        deploy_to_prod: {
          allowedDecisions: ["approve", "reject"],
          description: "🚨 生产环境部署需要审批"
        },
        send_email: {
          description: "📧 邮件草稿已准备好审核"
        },
      },
    }),
  ],
  checkpointer: new MemorySaver(),
});
```

## 边界

### Agent 可以配置的内容
✅ 哪些工具需要审批
✅ 每个工具允许的决策类型
✅ 自定义中断描述
✅ Checkpointer 实现

### Agent 不能配置的内容
❌ HITL 协议结构
❌ 跳过 checkpointer 要求
❌ 中断时不保存状态

## 注意事项

### 1. Checkpointer 是必需的
```typescript
// ❌ 错误
await createDeepAgent({ interruptOn: { write_file: true } });

// ✅ 必须提供 checkpointer
await createDeepAgent({
  interruptOn: { write_file: true },
  checkpointer: new MemorySaver()
});
```

### 2. 需要 Thread ID
```typescript
// ❌ 没有 thread_id 无法恢复
await agent.invoke({...});
await agent.updateState(...);  // 哪个会话？

// ✅ 使用一致的 thread_id
const config = { configurable: { thread_id: "session-1" } };
await agent.invoke({...}, config);
await agent.updateState(config, ...);
```

### 3. 在调用之间检查状态
```typescript
// 中断发生在 invoke() 调用之间

// 步骤 1: invoke() -> 中断
await agent.invoke({...}, config);

// 步骤 2: 检查状态
const state = await agent.getState(config);
if (state.next) {
  // 处理中断
}

// 步骤 3: 恢复
await agent.updateState(config, {...});
await agent.invoke(null, config);
```

## 完整文档
- [人工干预指南](https://docs.langchain.com/oss/javascript/langchain/human-in-the-loop)
- [HITL 中间件](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#human-in-the-loop)
- [Deep Agents HITL](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
