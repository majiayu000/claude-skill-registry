---
name: deepagents-skills
description: 在 Deep Agents 中创建和使用自定义技能，实现渐进式披露、SKILL.md 格式和 Agent Skills 协议。
language: js
---

# deepagents-skills (JavaScript/TypeScript)

## 概述

技能通过**渐进式披露**提供专门功能：agent 仅在相关时加载内容。

**流程：** 匹配（查看描述）→ 读取（加载 SKILL.md）→ 执行（遵循指令）

## 技能 vs 内存

| 技能 | 内存（AGENTS.md） |
|--------|-------------------|
| 按需加载 | 始终加载 |
| 任务特定 | 一般偏好 |
| 大型文档 | 紧凑上下文 |

## 使用技能

### 使用 FilesystemBackend

```typescript
import { createDeepAgent, FilesystemBackend } from "deepagents";
import { MemorySaver } from "@langchain/langgraph";

const agent = await createDeepAgent({
  backend: new FilesystemBackend({ rootDir: ".", virtualMode: true }),
  skills: ["./skills/"],
  checkpointer: new MemorySaver()
});

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "什么是 LangGraph？如果可用，使用 langgraph-docs 技能。"
  }]
});
```

### 使用 StoreBackend

```typescript
import { createDeepAgent, StoreBackend, type FileData } from "deepagents";
import { InMemoryStore } from "@langchain/langgraph";

const store = new InMemoryStore();

function createFileData(content: string): FileData {
  const now = new Date().toISOString();
  return {
    content: content.split("\n"),
    created_at: now,
    modified_at: now,
  };
}

const skillUrl = "https://raw.githubusercontent.com/.../SKILL.md";
const response = await fetch(skillUrl);
const skillContent = await response.text();

await store.put(
  ["filesystem"],
  "/skills/langgraph-docs/SKILL.md",
  createFileData(skillContent)
);

const agent = await createDeepAgent({
  backend: (config) => new StoreBackend(config),
  store,
  skills: ["/skills/"]
});
```

### 使用 StateBackend

```typescript
import { createDeepAgent, type FileData } from "deepagents";
import { MemorySaver } from "@langchain/langgraph";

function createFileData(content: string): FileData {
  const now = new Date().toISOString();
  return { content: content.split("\n"), created_at: now, modified_at: now };
}

const skillContent = `---
name: python-testing
description: Pytest 最佳实践
---
# Python 测试技能
...`;

const skillsFiles: Record<string, FileData> = {
  "/skills/python-testing/SKILL.md": createFileData(skillContent)
};

const agent = await createDeepAgent({
  skills: ["/skills/"],
  checkpointer: new MemorySaver()
});

await agent.invoke({
  messages: [{ role: "user", content: "我应该如何编写测试？" }],
  files: skillsFiles
});
```

## SKILL.md 格式

```markdown
---
name: fastapi-docs
description: FastAPI 最佳实践和模式
---

# FastAPI 文档技能

## 何时使用
使用 FastAPI 端点时。

## 指令
始终使用异步处理程序：
\`\`\`typescript
app.get("/users/:id", async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user);
});
\`\`\`
```

## 注意事项

### 1. 技能需要后端

```typescript
// ❌ 无后端
await createDeepAgent({ skills: ["./skills/"] });

// ✅ 提供后端
await createDeepAgent({
  backend: new FilesystemBackend({ rootDir: ".", virtualMode: true }),
  skills: ["./skills/"]
});
```

### 2. 需要 Frontmatter

```markdown
# ❌ 缺少
# 我的技能

# ✅ 包含
---
name: my-skill
description: 这做什么
---
# 我的技能
```

### 3. 具体描述

```markdown
# ❌ 模糊
description: 有用的技能

# ✅ 具体
description: 使用 Jest 和模拟模式的 TypeScript 测试
```

## 完整文档

- [技能指南](https://docs.langchain.com/oss/javascript/deepagents/skills)
- [Agent Skills 协议](https://docs.langchain.com/oss/javascript/langchain/multi-agent/skills)
