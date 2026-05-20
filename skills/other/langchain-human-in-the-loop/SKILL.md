---
name: langchain-human-in-the-loop
description: Add human oversight to LangChain agents using HITL middleware - includes interrupts, approval workflows, edit/reject decisions, and checkpoints
language: js
---

# langchain-human-in-the-loop (JavaScript/TypeScript)

## 概述

人工在环（Human-in-the-Loop，HITL）让您可以向代理工具调用添加人工监督。当代理提出敏感操作（如数据库写入或发送电子邮件）时，执行会暂停以供人工批准、编辑或拒绝。

**核心概念：**
- **humanInTheLoopMiddleware**：暂停执行以供人工决策
- **中断**（Interrupts）：代理等待人工输入的检查点
- **决策**（Decisions）：批准、编辑或拒绝工具调用
- **检查点**（Checkpointer）：跨中断持久化所必需的

## 何时使用 HITL

| 场景 | 使用 HITL？ | 原因 |
|----------|-----------|-----|
| 数据库写入 | ✅ 是 | 防止数据损坏 |
| 发送电子邮件/消息 | ✅ 是 | 发送前审查 |
| 金融交易 | ✅ 是 | 执行前确认 |
| 删除数据 | ✅ 是 | 防止意外丢失 |
| 只读操作 | ❌ 否 | 低风险 |
| 内部计算 | ❌ 否 | 无外部影响 |

## 决策表

### HITL 决策类型

| 决策 | 效果 | 何时使用 |
|----------|--------|-------------|
| `approve` | 按原样执行工具 | 工具调用看起来正确 |
| `edit` | 修改参数然后执行 | 需要更改参数 |
| `reject` | 不执行，提供反馈 | 工具调用错误 |

## 代码示例

### 基本 HITL 设置

```typescript
import { createAgent, humanInTheLoopMiddleware } from "langchain";
import { MemorySaver } from "@langchain/langgraph";
import { tool } from "langchain";
import { z } from "zod";

const sendEmail = tool(
  async ({ to, subject, body }) => {
    // 发送电子邮件逻辑
    return `已发送电子邮件到 ${to}`;
  },
  {
    name: "send_email",
    description: "发送电子邮件",
    schema: z.object({
      to: z.string().email(),
      subject: z.string(),
      body: z.string(),
    }),
  }
);

const agent = createAgent({
  model: "gpt-4.1",
  tools: [sendEmail],
  checkpointer: new MemorySaver(),  // HITL 所必需
  middleware: [
    humanInTheLoopMiddleware({
      interruptOn: {
        send_email: {
          allowedDecisions: ["approve", "edit", "reject"],
        },
      },
    }),
  ],
});
```

### 使用中断运行

```typescript
import { Command } from "@langchain/langgraph";

const config = { configurable: { thread_id: "session-1" } };

// 步骤 1：代理运行直到需要调用工具
const result1 = await agent.invoke({
  messages: [{ role: "user", content: "发送电子邮件到 john@example.com 说你好" }]
}, config);

// 检查中断
if ("__interrupt__" in result1) {
  const interrupt = result1.__interrupt__[0];
  console.log("等待批准:", interrupt.value);

  // 中断包含：{toolCall: {...}, allowedDecisions: [...]}
}

// 步骤 2：人工批准
const result2 = await agent.invoke(
  new Command({
    resume: {
      decisions: [{ type: "approve" }],
    },
  }),
  config
);

// 工具现在执行，代理完成
console.log(result2.messages[result2.messages.length - 1].content);
```

### 编辑工具参数

```typescript
const config = { configurable: { thread_id: "session-2" } };

// 代理想要发送电子邮件
const result1 = await agent.invoke({
  messages: [{ role: "user", content: "给 Alice 发送关于会议的电子邮件" }]
}, config);

// 人工编辑参数
const result2 = await agent.invoke(
  new Command({
    resume: {
      decisions: [{
        type: "edit",
        args: {
          to: "alice@company.com",  // 修正的电子邮件
          subject: "项目会议 - 已更新",  // 更好的主题
          body: "...",  // 编辑的正文
        },
      }],
    },
  }),
  config
);
```

### 带反馈的拒绝

```typescript
const config = { configurable: { thread_id: "session-3" } };

// 代理想要删除记录
const result1 = await agent.invoke({
  messages: [{ role: "user", content: "删除旧的客户数据" }]
}, config);

// 人工拒绝
const result2 = await agent.invoke(
  new Command({
    resume: {
      decisions: [{
        type: "reject",
        feedback: "未经经理批准无法删除客户数据",
      }],
    },
  }),
  config
);

// 代理接收反馈并可以尝试替代方法
```

### 不同策略的多个工具

```typescript
import { humanInTheLoopMiddleware } from "langchain";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [sendEmail, readEmail, deleteEmail],
  checkpointer: new MemorySaver(),
  middleware: [
    humanInTheLoopMiddleware({
      interruptOn: {
        send_email: {
          allowedDecisions: ["approve", "edit", "reject"],
        },
        delete_email: {
          allowedDecisions: ["approve", "reject"],  // 无编辑
        },
        read_email: false,  // 读取无 HITL
      },
    }),
  ],
});
```

### 使用 HITL 流式传输

```typescript
const config = { configurable: { thread_id: "session-4" } };

// 流式传输直到中断
for await (const [mode, chunk] of await agent.stream(
  { messages: [{ role: "user", content: "发送报告给团队" }] },
  { ...config, streamMode: ["updates", "messages"] }
)) {
  if (mode === "messages") {
    const [token, metadata] = chunk;
    if (token.content) {
      process.stdout.write(token.content);
    }
  } else if (mode === "updates") {
    if ("__interrupt__" in chunk) {
      console.log("\n等待批准...");
      break;  // 处理中断
    }
  }
}

// 批准后继续流式传输
for await (const [mode, chunk] of await agent.stream(
  new Command({ resume: { decisions: [{ type: "approve" }] } }),
  { ...config, streamMode: ["messages"] }
)) {
  // 继续流式传输
}
```

### 自定义中断逻辑

```typescript
import { createMiddleware } from "langchain";

const customHITL = createMiddleware({
  name: "CustomHITL",
  wrapToolCall: async (toolCall, handler, runtime) => {
    // 自定义逻辑决定是否需要中断
    if (toolCall.name === "database_write") {
      const value = toolCall.args.value;

      if (value > 1000) {
        // 为大值中断
        const decision = await runtime.interrupt({
          toolCall,
          reason: "大型数据库写入需要批准",
        });

        if (decision.type === "approve") {
          return await handler(toolCall);
        } else if (decision.type === "edit") {
          return await handler({ ...toolCall, args: decision.args });
        } else {
          throw new Error(decision.feedback || "已拒绝");
        }
      }
    }

    // 不需要中断
    return await handler(toolCall);
  },
});
```

## 边界

### 您可以配置什么

✅ **哪些工具需要批准**：每个工具的策略
✅ **允许的决策类型**：批准、编辑、拒绝
✅ **自定义中断逻辑**：条件中断
✅ **反馈消息**：解释拒绝原因
✅ **修改的参数**：编辑工具参数

### 您不能配置什么

❌ **跳过检查点**：HITL 需要持久化
❌ **执行后中断**：必须在中断前
❌ **强制模型不调用工具**：HITL 在模型决定后响应
❌ **修改模型的决策**：仅工具执行

## 注意事项

### 1. 缺少检查点

```typescript
// ❌ 问题：没有检查点
const agent = createAgent({
  model: "gpt-4.1",
  tools: [sendEmail],
  middleware: [humanInTheLoopMiddleware({...})],  // 错误！
});

// ✅ 解决方案：始终添加检查点
import { MemorySaver } from "@langchain/langgraph";

const agent = createAgent({
  model: "gpt-4.1",
  tools: [sendEmail],
  checkpointer: new MemorySaver(),  // 必需
  middleware: [humanInTheLoopMiddleware({...})],
});
```

### 2. 没有 thread_id

```typescript
// ❌ 问题：缺少 thread_id
await agent.invoke(input);  // 没有配置！

// ✅ 解决方案：始终提供 thread_id
await agent.invoke(input, {
  configurable: { thread_id: "user-123" }
});
```

### 3. 错误的恢复语法

```typescript
// ❌ 问题：错误的恢复格式
await agent.invoke({
  resume: { decisions: [...] }  // 错误！
});

// ✅ 解决方案：使用 Command
import { Command } from "@langchain/langgraph";

await agent.invoke(
  new Command({
    resume: { decisions: [{ type: "approve" }] }
  }),
  config
);
```

### 4. 不检查中断

```typescript
// ❌ 问题：未检测到中断
const result = await agent.invoke(input, config);
console.log(result.messages);  // 可能未完成！

// ✅ 解决方案：检查 __interrupt__
if ("__interrupt__" in result) {
  // 处理人工决策
} else {
  // 代理完成
}
```

## 文档链接

- [人工在环指南](https://docs.langchain.com/oss/javascript/langchain/human-in-the-loop)
- [HITL 中间件](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in)
- [LangGraph 中断](https://docs.langchain.com/oss/javascript/langgraph/interrupts)
