---
name: deepagents-filesystem
description: 使用 FilesystemMiddleware 实现虚拟文件系统、后端（State、Store、Filesystem、Composite）和 Deep Agents 的上下文管理。
language: js
---

# deepagents-filesystem (JavaScript/TypeScript)

## 概述

FilesystemMiddleware 通过可插拔后端系统提供文件操作，解决上下文工程挑战。工具包括：`ls`、`read_file`、`write_file`、`edit_file`、`glob`、`grep`。

## 后端类型

### StateBackend（默认）
在 agent 状态中的临时存储 - 仅在单个会话内持久化。

```typescript
import { createDeepAgent } from "deepagents";

const agent = await createDeepAgent({});
// 默认 StateBackend - 文件仅存在于会话中
```

### FilesystemBackend（本地磁盘）
```typescript
import { createDeepAgent, FilesystemBackend } from "deepagents";

const agent = await createDeepAgent({
  backend: new FilesystemBackend({
    rootDir: ".",
    virtualMode: true  // 安全性：限制路径
  })
});
```

### StoreBackend（持久化）
```typescript
import { createDeepAgent, StoreBackend } from "deepagents";
import { InMemoryStore } from "@langchain/langgraph";

const store = new InMemoryStore();

const agent = await createDeepAgent({
  backend: (config) => new StoreBackend(config),
  store
});
```

### CompositeBackend（混合）
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
```

## 决策表

| 使用场景 | 后端 | 原因 |
|----------|---------|-----|
| 临时文件 | StateBackend | 默认，无需设置 |
| 本地开发 | FilesystemBackend | 直接磁盘访问 |
| 跨会话内存 | StoreBackend | 在会话间持久化 |
| 混合存储 | CompositeBackend | 混合临时 + 持久化 |

## 代码示例

### 示例 1：管理大上下文
```typescript
const agent = await createDeepAgent({});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "搜索 TypeScript 最佳实践并保存结果以供分析"
  }]
});
// Agent: 搜索 -> write_file -> 压缩上下文 -> 需要时 read_file
```

### 示例 2：长期内存
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
await agent.invoke({
  messages: [{ role: "user", content: "保存我的偏好：简洁解释到 /memories/prefs.txt" }]
}, { configurable: { thread_id: "thread-1" } });

// 会话 2：访问偏好
await agent.invoke({
  messages: [{ role: "user", content: "阅读我的偏好并解释 async/await" }]
}, { configurable: { thread_id: "thread-2" } });
```

### 示例 3：自定义工具描述
```typescript
import { createAgent, createFilesystemMiddleware } from "langchain";

const agent = createAgent({
  model: "claude-sonnet-4-5-20250929",
  middleware: [
    createFilesystemMiddleware({
      systemPrompt: "将中间结果保存到 /workspace/",
      customToolDescriptions: {
        read_file: "阅读你之前编写的文件。对大文件使用 offset/limit。",
        write_file: "保存数据以避免上下文溢出。",
      }
    }),
  ],
});
```

## 边界

### Agent 可以配置的内容
✅ 后端类型和配置
✅ 自定义工具描述
✅ 文件路径和组织
✅ 文件操作的人工审批

### Agent 不能配置的内容
❌ 工具名称
❌ 禁用文件系统工具
❌ 访问 virtual_mode 限制外的路径

## 注意事项

### 1. StateBackend 文件不会跨会话持久化
```typescript
// ❌ 会话更改时文件丢失
await agent.invoke({messages: [{role: "user", content: "写入 /notes.txt"}]},
  {configurable: {thread_id: "thread-1"}});
await agent.invoke({messages: [{role: "user", content: "读取 /notes.txt"}]},
  {configurable: {thread_id: "thread-2"}});
// 文件未找到！

// ✅ 使用相同的 thread_id 或 StoreBackend
```

### 2. FilesystemBackend 安全性
```typescript
// ❌ 不安全
new FilesystemBackend({ rootDir: "/project", virtualMode: false })

// ✅ 安全
new FilesystemBackend({ rootDir: "/project", virtualMode: true })
```

### 3. StoreBackend 需要 Store
```typescript
// ❌ 缺少 store
await createDeepAgent({ backend: (config) => new StoreBackend(config) });

// ✅ 提供 store
await createDeepAgent({
  backend: (config) => new StoreBackend(config),
  store: new InMemoryStore()
});
```

## 完整文档
- [Filesystem Middleware](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#filesystem-middleware)
- [Backends 指南](https://docs.langchain.com/oss/javascript/deepagents/backends)
- [长期内存](https://docs.langchain.com/oss/javascript/deepagents/long-term-memory)
