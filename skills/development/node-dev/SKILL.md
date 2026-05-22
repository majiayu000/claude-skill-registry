---
name: node-dev
description: React Flow 节点开发的完整指南。包含节点类型、Handles 连接规则、数据传递架构和开发模板。适用于创建新的自定义节点或修改现有节点。
---

# React Flow 节点开发技能 v2.0

> **更新日期**: 2026-01-23
> **版本**: v2.0.0
> **定位**: WinJin AIGC 项目的节点开发核心指南

---

## 节点类型分类

| 类型 | 颜色 | Handle 位置 | 示例 |
|------|------|-----------|------|
| **输入节点** | 蓝色 (#3b82f6) | Handle 在右侧 | APISettingsNode, CharacterLibraryNode |
| **处理节点** | 绿色 (#10b981) | Handle 在左右两侧 | VideoGenerateNode, PromptOptimizerNode |
| **输出节点** | 浅蓝 (#0ea5e9) | Handle 在左侧 | TaskResultNode, CharacterResultNode |

---

## Handles 连接规范 ⭐ 核心

### 输入端口到源节点类型的映射

| 目标端口 | Handle ID | 源节点类型 | 数据传递 | 用途 |
|---------|-----------|----------------|----------|------|
| `prompt-input` | 右侧 | textNode, promptOptimizerNode, narratorProcessorNode | connectedPrompt | 文本提示词输入和优化 |
| `character-input` | 右侧 | characterLibraryNode | connectedCharacters | 角色库数据传递 |
| `images-input` | 右侧 | referenceImageNode | connectedImages | 参考图片传递 |
| `api-config` | 右侧 | apiSettingsNode | apiConfig | API 配置连接 |
| `task-input` | 左侧 | videoGenerateNode, storyboardNode, characterCreateNode | taskId | 任务结果监听 |

### Handle 连接验证机制

```javascript
// ✅ App.jsx 中的验证逻辑
const validCharacterSourceTypes = ['characterLibraryNode'];
if (sourceNode && validCharacterSourceTypes.includes(sourceNode.type)) {
  newData.connectedCharacters = sourceNode.data.connectedCharacters;
} else {
  newData.connectedCharacters = undefined; // 静默失败
}
```

---

## 数据传递架构 ⭐ 重要

### 核心原则
**源节点直接更新目标节点，避免依赖父组件中转**

```javascript
// ✅ 正确：源节点直接更新目标节点
const edges = getEdges();
const outgoingEdges = edges.filter(e => e.source === nodeId);

setNodes((nds) =>
  nds.map((node) => {
    // 更新自己
    if (node.id === nodeId) {
      return { ...node, data: { ...node.data, selectedCharacters } };
    }
    // 直接更新目标节点（绕过 App.jsx）
    const isConnected = outgoingEdges.some(e => e.target === node.id);
    if (isConnected) {
      return { ...node, data: { ...node.data, connectedCharacters } };
    }
    return node;
  })
);
```

### 事件系统（异步数据）

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

---

## 节点开发最佳实践

### 1. useState 同步到 node.data

```javascript
// 初始化
const [manualPrompt, setManualPrompt] = useState(data.manualPrompt || '');

// 同步到 node.data
useEffect(() => {
  if (manualPrompt !== data.manualPrompt) {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === nodeId
          ? { ...node, data: { ...node.data, manualPrompt } }
          : node
      )
    );
  }
}, [manualPrompt, nodeId, setNodes, data.manualPrompt]);
```

### 2. useEffect 依赖最佳实践

```javascript
// ❌ 错误：依赖 data 对象
useEffect(() => {
  // ...
}, [data]); // data 每次都是新引用

// ✅ 正确：依赖具体值
useEffect(() => {
  // ...
}, [data.value]); // 只依赖实际变化的值
```

### 3. 防止节点内交互触发拖动

```jsx
{/* 使用 nodrag 类 */}
<textarea className="nodrag" />
<select className="nodrag">...</select>
<input className="nodrag" type="checkbox" />
<button className="nodrag">生成</button>
```

### 4. 双显示功能（角色引用）

```javascript
// 创建映射
const usernameToAlias = React.useMemo(() => {
  const map = {};
  connectedCharacters.forEach(char => {
    map[char.username] = char.alias || char.username;
  });
  return map;
}, [connectedCharacters]);

// 真实ID → 显示别名
const realToDisplay = (text) => {
  let result = text;
  Object.entries(usernameToAlias).forEach(([username, alias]) => {
    const regex = new RegExp(`@${username}(?=\\s|$|@)`, 'g');
    result = result.replace(regex, `@${alias}`);
  });
  return result;
};

// 显示别名 → 真实ID
const displayToReal = (text) => {
  let result = text;
  const sortedAliases = Object.entries(usernameToAlias)
    .sort((a, b) => b[1].length - a[1].length);
  sortedAliases.forEach(([username, alias]) => {
    const regex = new RegExp(`@${alias}(?=\\s|$|@)`, 'g');
    result = result.replace(regex, `@${username}`);
  });
  return result;
};

// Textarea 显示别名
<textarea
  value={realToDisplay(manualPrompt)}
  onChange={(e) => setManualPrompt(displayToReal(e.target.value))}
/>
```

---

## 节点开发工作流

### 场景1: 角色视频生成工作流

**节点组合**:
1. CharacterLibraryNode（选择角色）
2. VideoGenerateNode（输入提示词、生成视频）
3. TaskResultNode（显示结果）

**数据流**:
```
CharacterLibraryNode.selectedCharacters
    ↓ 连接
VideoGenerateNode.connectedCharacters
    ↓ API 调用
TaskResultNode.taskId
    ↓ 轮询
TaskResultNode.videoUrl
```

### 场景2: 优化工作流

**节点组合**:
1. TextNode（输入简单描述）
2. PromptOptimizerNode（AI 优化）
3. VideoGenerateNode（生成视频）

**数据流**:
```
TextNode.value
    ↓ 连接
PromptOptimizerNode.manualPrompt
    ↓ AI 优化
VideoGenerateNode.manualPrompt
    ↓ API 调用
TaskResultNode.taskId
```

### 场景3: 故事板工作流

**节点组合**:
1. TextNode（输入多个镜头描述）
2. StoryboardNode（拼接故事板格式）
3. TaskResultNode（显示结果）

**数据流**:
```
TextNode.value × N
    ↓ 连接
StoryboardNode.shots
    ↓ API 调用（故事板专用端点）
TaskResultNode.taskId
```

---

## 详细文档

### references/ 目录

- [节点架构](../03-node-development/references/node-architecture.md) - 完整的架构模式
- [Handle 连接](../03-node-development/references/handle-connections.md) - 连接规范详解
- [节点模板](../03-node-development/references/node-templates.md) - 代码模板库
- [节点功能参考手册](../03-node-development/node-reference/README.md) - 所有节点功能文档

### 相关文档

- [错误模式参考](../rules/error-patterns.md) - 节点相关错误
- [开发交接书](../../../用户输入文件夹/开发对话/开发交接书.md) - 版本记录

---

## 快速开始

### 新手入门（15分钟）
1. 阅读 [节点架构](../03-node-development/references/node-architecture.md) - 理解节点架构
2. 阅读 [Handle 连接](../03-node-development/references/handle-connections.md) - 学习连接规范
3. 浏览 [节点模板](../03-node-development/references/node-templates.md) - 使用代码模板

### 进阶开发者（20分钟）
1. 深入理解 [Handle 连接](../03-node-development/references/handle-connections.md) - 掌握连接验证
2. 精读 [节点功能参考手册](../03-node-development/node-reference/README.md) - 熟悉所有节点
3. 应用到实际开发 - 创建自定义节点

---

## 常见问题

### Q: 如何防止节点间数据传递丢失？

**A**: 使用**源节点直接更新目标节点**模式，绕过 App.jsx 的中转

### Q: useEffect 无限循环怎么办？

**A**:
1. 移除 `data` 从依赖数组
2. 使用 `useRef` 存储回调
3. 只依赖实际变化的值

### Q: 如何实现双显示功能？

**A**: 参考上面的"双显示功能"示例代码

---

**维护者**: WinJin AIGC Team
**最后更新**: 2026-01-23
**版本**: v2.0.0
