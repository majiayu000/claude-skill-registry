---
name: cursor-agent-opener
description: 自动打开新的 Cursor Chat 对话，用于并行执行子级 skills
---

# Cursor Chat 自动打开器

## 何时使用此技能

当你需要：
- **自动打开新的 Chat 对话**（不是新窗口，是当前窗口中的新 Chat）
- 并行处理多个任务（主对话 + 新 Chat）
- 隔离不同任务的上下文
- 让子级 skills 独立执行，实现并行子任务
- 复杂任务分解为多个独立的子任务

## 快速使用

### 方法1：使用脚本（推荐）

```bash
# 打开新的 Chat 对话（在当前窗口）
pnpm cursor:agent

# 或直接运行脚本
node scripts/commands/tools/open-cursor-agent.mjs

# 带初始提示
node scripts/commands/tools/open-cursor-agent.mjs "处理新功能开发" "请帮我实现用户登录功能"
```

### 方法2：手动操作（最可靠）

**快捷键方式**：
1. 按 `Ctrl+L` (Windows) 或 `Cmd+L` (Mac) 打开 Chat 面板
2. 点击 Chat 面板右上角的 **"+ New Chat"** 或 **"+"** 按钮

**命令面板方式**：
1. 按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac)
2. 输入 "New Chat" 或 "Cursor: New Chat"
3. 选择打开新的 Chat 对话

## 使用场景

### 场景1：并行处理多个任务

**主对话**：正在处理 bug 修复
**新 Chat**：同时处理新功能开发

```bash
# 在主对话中执行
pnpm cursor:agent
# 然后在新 Chat 中输入任务描述
```

### 场景2：隔离上下文

**主对话**：讨论架构设计
**新 Chat**：实现具体功能

这样可以避免上下文混淆，每个 Chat 有独立的对话历史。

### 场景3：快速切换任务

当需要临时处理其他任务时，打开新的 Chat，完成后可以关闭或保留，不影响主对话。

### 场景4：多步骤任务分解

- **Chat 1**：需求分析和设计
- **Chat 2**：前端实现
- **Chat 3**：后端实现
- **Chat 4**：测试和优化

每个 Chat 专注于一个方面，避免上下文过长。

## 技术实现

### 自动发送快捷键

在 Windows 系统上，脚本会自动：
1. 查找 Cursor 窗口
2. 激活 Cursor 窗口
3. 发送 Ctrl+L 快捷键打开 Chat 面板
4. 提示用户点击 "+ New Chat" 按钮

```javascript
import { openCursorAgent } from './scripts/commands/tools/open-cursor-agent.mjs';

// 自动打开新 Chat（会发送 Ctrl+L）
await openCursorAgent({
  context: '处理新功能开发',
  initialPrompt: '请帮我实现用户登录功能'
});
```

### 并行执行集成

在 skills 中使用并行执行：

```javascript
import { executeSubTasksInParallel, openChatForChildSkill } from './scripts/commands/skills/parallel-executor.mjs';

// 批量执行子任务
await executeSubTasksInParallel('parent-skill', executionId, taskInfo, [
  { skillName: 'child-skill-1', description: '任务1' },
  { skillName: 'child-skill-2', description: '任务2' }
]);
```

### 安装 Cursor CLI

如果 Cursor CLI 未安装：

**Windows**:
1. 打开 Cursor 设置
2. 启用 "Command Line Interface"
3. 或手动将 Cursor 添加到 PATH

**Mac/Linux**:
```bash
curl https://cursor.com/install -fsS | bash
```

### 验证安装

```bash
# 检查版本
cursor --version

# 检查 agent 命令
cursor-agent --help
```

## 注意事项

1. **首次使用需要登录**：
   ```bash
   cursor-agent login
   ```

2. **新窗口行为**：
   - 默认在新窗口中打开
   - 可以手动切换到 agent 标签

3. **上下文隔离**：
   - 新 agent 页面有独立的对话历史
   - 不会影响主对话的上下文

4. **项目路径**：
   - 脚本会自动使用当前项目路径
   - 确保在项目根目录执行

## 集成到 Skills 系统

可以在其他 skills 中调用此功能：

```javascript
// 在 skill 执行过程中打开新的 agent 页面
import { openCursorAgent } from '../../tools/open-cursor-agent.mjs';

// 当需要并行处理时
if (needParallelProcessing) {
  await openCursorAgent({
    context: `处理 ${taskName} 任务`,
    newWindow: true
  });
}
```

## 常见问题

**Q: 命令执行失败？**
A: 检查 Cursor CLI 是否已安装并添加到 PATH

**Q: 打开的不是 agent 页面？**
A: 在新窗口中手动点击 "Chat" 或 "Agent" 标签

**Q: 如何关闭新打开的页面？**
A: 直接关闭窗口，或使用 Cursor 的窗口管理功能

## 相关技能

- `scripts-navigator` - 查找和运行脚本
- `dev-workflow` - 开发工作流（可以并行处理）
