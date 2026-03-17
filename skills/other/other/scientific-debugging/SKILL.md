---
name: scientific-debugging
description: 科学调试专家 - 观察(Observe) -> 假设(Hypothesize) -> 实验(Experiment) -> 修复(Fix)
---

# Scientific Debugger Skill (v2.0)

> **Role**: 拒绝"猜测驱动开发"。像科学家一样思考，用实验数据定位根因。

---

## 核心协议 (The Protocol)

### 1. 观察 (Observe)
- **收集现场**: 用户报告了什么？错误堆栈是什么？
- **环境确认**: 本地服务器是否运行？
- **现象复现**: *必须* 使用 `browser_subagent` 复现问题 (Visual Proof)。

### 2. 假设 (Hypothesize)
基于观察，提出 1-3 个可能的根因假设：
- H1: DOM 事件未冒泡 (Event)
- H2: 状态更新被闭包捕获 (State)
- H3: 样式层叠导致的遮挡 (CSS)

### 3. 实验 (Experiment)
设计最小化实验验证假设：
- **Console Log**: 在关键路径打点。
- **Browser Interaction**: 模拟用户行为序列。
- **Code Inspection**: 检查 `view_code_item`.

### 4. 修复与验证 (Fix & Verify)
- **最小化修复**: 只改根因，不附带重构。
- **回归测试**: 再次运行 `browser_subagent` 确认修复且无副作用。

---

## 调试策略库

| 问题类型 | 推荐工具 | 重点检查 |
|----------|----------|----------|
| **UI 无响应/交互失效** | `browser_subagent` | `pointer-events`, `z-index`, `onClick` vs `onFocus` |
| **状态不同步** | `console.log` + React DevTools | Zustand Selectors, React Query Cache Key |
| **样式错乱** | `browser_subagent` (Screenshot) | Tailwind Classes, CSS Variables |
| **网络错误** | Network Tab (via Browser) | CORS, 404/500, Payload Format |

---

## 资源索引

| 资源文件 | 用途 |
|----------|------|
| [browser-test-guide.md](resources/browser-test-guide.md) | 浏览器测试通过指南 |
| [root-cause-patterns.md](resources/root-cause-patterns.md) | 常见根因模式库 |

---

## 强制要求

1.  **No Blind Fixes**: 禁止在未复现问题前修改代码。
2.  **Visual Evidence**: 对于 UI Bug，必须看截图证明。
3.  **Logs are Cheap**: 大胆加日志，但修好后记得删。
