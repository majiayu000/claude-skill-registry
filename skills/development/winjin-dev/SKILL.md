---
name: winjin-dev
description: WinJin AIGC 项目开发规范和最佳实践。包含 Sora2 API 集成、React Flow 节点开发、双平台差异处理。每次功能开发后必须更新此 skill。
---

# WinJin AIGC 项目开发技能 v2.0

> **更新日期**: 2026-01-23
> **版本**: v2.0.0 (精简版，-50%)
> **定位**: WinJin AIGC 项目的核心开发规范

---

## 项目概述

WinJin AIGC 是一个基于 Electron + Express 的 AI 视频生成工具，支持 Sora2 视频生成、角色创建、可视化节点工作流编辑器。

**技术栈**:
- 后端: Express.js + Node.js
- 前端: React 19 + React Flow 11.x
- 构建: Vite 7.x
- 双平台: 聚鑫 + 贞贞

---

## 🔄 Skill 更新机制

此 skill 需要随着项目开发持续更新。**每次开发新功能或修复 Bug 后**，都必须更新此 skill 和相关文档。

### 快速更新指南

```
新增功能或修复 Bug 后：
├─ 1. 在 SKILL.md 中添加新的错误模式或规范
├─ 2. 在 references/ 中添加详细说明（可选）
├─ 3. 运行 git add/commit 提交变更
└─ 4. 告诉团队成员 skill 已更新
```

---

## 核心开发规范 ⭐ 必读

### 1. API 端点路径 ⚠️ 重要

**规则**: 所有前端 API 调用必须使用完整路径 `/api/{endpoint}`

```javascript
// ❌ 错误：缺少前缀
fetch(`${API_BASE}/task/${taskId}`)  // 404 Not Found

// ✅ 正确：完整路径
fetch(`${API_BASE}/api/task/${taskId}`)  // 200 OK
```

### 2. Sora2 API 注意事项 ⭐

#### 模型名称差异
- **聚鑫平台**: 只支持 `sora-2-all`
- **贞贞平台**: 支持 `sora-2` 和 `sora-2-pro`
- **后端自动选择**: `model || (platformType === 'JUXIN' ? 'sora-2-all' : 'sora-2')`

#### 角色创建
```javascript
// ❌ 错误：传递 model 参数会导致 404
await axios.post('/sora/v1/characters', {
  model: 'sora-2',  // ❌ 删除此行
  url: videoUrl,
  timestamps: '1,3'
});

// ✅ 正确：不传递 model 参数
await axios.post('/sora/v1/characters', {
  url: videoUrl,
  timestamps: '1,3'
});

// ✅ 推荐：使用 from_task 参数
await axios.post('/sora/v1/characters', {
  from_task: taskId,
  timestamps: '1,3'
});
```

#### 角色引用格式
```javascript
// 所有平台统一使用 @username 格式（不带花括号）
const prompt = '@6f2dbf2b3.zenwhisper 在工地上干活';
// ❌ 不要使用 @{username}
```

#### 轮询间隔
```javascript
// ✅ 正确：30秒间隔
const POLL_INTERVAL = 30000;

// ❌ 错误：5秒间隔会导致 429 错误
const POLL_INTERVAL = 5000;
```

---

## React Flow 节点开发 ⭐

### useNodeId() Hook
```javascript
// ❌ 错误：data.id 是 undefined
const dispatchEvent = () => {
  window.dispatchEvent(new CustomEvent('video-task-created', {
    detail: { sourceNodeId: data.id } // ❌ undefined
  }));
};

// ✅ 正确：使用 useNodeId()
import { useNodeId } from 'reactflow';
const nodeId = useNodeId(); // ✅ 获取节点 ID
```

### useEffect 依赖数组
```javascript
// ❌ 错误：nodes 在依赖中会导致无限循环
useEffect(() => {
  setNodes((nds) => nds.map((node) => ({ ...node, data: newData })));
}, [edges, nodes, setNodes]);

// ✅ 正确：只依赖 edges 和 setNodes
useEffect(() => {
  setNodes((nds) => nds.map((node) => ({ ...node, data: newData })));
}, [edges, setNodes]);
```

### 节点间数据传递 ⭐ 核心

**✅ 正确模式**: 源节点直接更新目标节点
```javascript
const edges = getEdges();
const outgoingEdges = edges.filter(e => e.source === nodeId);

setNodes((nds) =>
  nds.map((node) => {
    // 更新自己
    if (node.id === nodeId) {
      return { ...node, data: { ...node.data, selectedCharacters } };
    }
    // ⭐ 直接更新目标节点（绕过 App.jsx）
    const isConnected = outgoingEdges.some(e => e.target === node.id);
    if (isConnected) {
      return { ...node, data: { ...node.data, connectedCharacters } };
    }
    return node;
  })
);
```

**事件系统**: 用于跨节点通信（taskId 等异步数据）
```javascript
// 发送节点
window.dispatchEvent(new CustomEvent('video-task-created', {
  detail: { sourceNodeId: nodeId, taskId: id }
}));

// 接收节点
useEffect(() => {
  const handleVideoCreated = (event) => {
    const { sourceNodeId, taskId } = event.detail;
    if (data.connectedSourceId === sourceNodeId) {
      setTaskId(taskId);
    }
  };
  window.addEventListener('video-task-created', handleVideoCreated);
  return () => window.removeEventListener('video-task-created', handleVideoCreated);
}, [data.connectedSourceId]);
```

### UI设计模式：避免触发模式 ⭐

**原则**: 非必要不要使用触发模式（点击按钮才显示输入框）

**❌ 错误模式**（反人性）:
```javascript
// 用户需要点击"编辑"按钮才能看到输入框
<button onClick={() => setEditing(true)}>✏️ 编辑</button>
{isEditing && (
  <textarea value={text} onChange={(e) => setText(e.target.value)} />
)}
```

**✅ 正确模式**（直接编辑）:
```javascript
// ✅ 直接显示输入框，用户可以立即编辑
<textarea
  value={text}
  onChange={(e) => setText(e.target.value)}
  placeholder="输入提示词..."
/>
```

---

## 代码风格

- **缩进**: 2 空格
- **引号**: 单引号 `'`
- **分号**: 必须使用
- **命名**: camelCase / PascalCase / kebab-case

---

## 高频错误（Top 12）⭐ 必读

| 错误 | 类型 | 核心问题 |
|------|------|----------|
| **错误1** | API | 双平台任务ID不兼容 |
| **错误6** | API | 轮询间隔太短（429错误） |
| **错误16** | React Flow | 节点间数据传递错误 |
| **错误17** | API | API 端点路径缺少前缀 |
| **错误37** | React Flow | TaskResultNode 任务ID竞态条件 |
| **错误48** | Character | 优化节点错误使用双显示功能 |
| **错误51** | React Flow | TaskResultNode 轮询 interval 竞态条件 |
| **错误53** | Storage | NarratorProcessorNode 优化结果刷新后丢失 |
| **错误54** | React Flow | VideoGenerateNode getNodes() 快照延迟 |
| **错误56** | React Flow | API 配置节点平台选择刷新后丢失 |

**查看完整错误模式**: [`.claude/rules/error-patterns.md`](../rules/error-patterns.md)

---

## 开发提示（精选）⭐

### 1. 节点开发优先级 ⭐⭐⭐

1. **使用 useNodeId()**: 不要依赖 `data.id`（undefined）
2. **useEffect 依赖**: 避免依赖 `nodes`（会导致无限循环）
3. **节点间数据传递**: 源节点直接更新目标节点（不要依赖 App.jsx）
4. **事件系统**: 用于异步数据传递（taskId 等）
5. **getEdges 解构**: `useReactFlow()` 必须包含 `getEdges`

### 2. API 调用优先级 ⭐⭐⭐

1. **API 路径**: 前端必须使用完整路径 `/api/{endpoint}`
2. **双平台兼容**: 聚鑫返回 `id`，贞贞返回 `task_id`
3. **轮询间隔**: 使用 30 秒（避免 429 错误）
4. **角色创建**: 不传 `model` 参数，优先使用 `from_task`

### 3. 角色引用优先级 ⭐⭐⭐

1. **格式**: 使用 `@username`（不带花括号）
2. **空格要求**: `@username ` 后面必须加空格
3. **优化节点**: 始终使用真实ID（`@ebfb9a758.sunnykitte`）
4. **视频生成节点**: 双显示（输入框显示别名，API使用真实ID）
5. **不描述外观**: Sora2 会使用角色真实外观，只需描述活动

---

## 详细文档

### references/ 目录

- [API 规范](../01-fundamentals/references/api-platforms.md) - 双平台差异详解
- [错误模式参考](../rules/error-patterns.md) - 56个错误完整列表
- [开发交接书](../../../用户输入文件夹/开发对话/开发交接书.md) - 版本记录、功能列表

---

## 必须更新的文档

| 文档 | 何时更新 | 更新内容 |
|------|----------|----------|
| `SKILL.md` | 每次开发 | 新增错误模式、API 规范 |
| [base.md](../rules/base.md) | API 变更 | 技术规范、端点定义 |
| [error-patterns.md](../rules/error-patterns.md) | 新错误 | 添加错误模式 |
| [开发交接书.md](../../../用户输入文件夹/开发对话/开发交接书.md) | 每次开发 | 版本号、功能列表 |

---

**维护者**: WinJin AIGC Team
**最后更新**: 2026-01-23
**版本**: v2.0.0
