---
name: fec-web-workers
description: 用于将昂贵的浏览器工作移出主线程，涉及 Web Workers、SharedWorker、worker 池、Comlink、transferable objects、Vite/Webpack worker 集成或 UI 响应性修复。不要用于轻量同步工作或 DOM 操作；中文触发词包括 Web Worker、后台线程、主线程阻塞。
---

# Web Workers

## 用途

把昂贵计算移出主线程，保持输入、滚动和动画响应。

## 流程

1. 先确认瓶颈：任务超过约 10ms、用户输入延迟明显、FPS 下滑或大文件解析/图像处理/加密计算才考虑 Worker。
2. 选择通信模型：简单任务用 `postMessage`，函数式 RPC 用 Comlink，大量并行小任务用 Worker pool，跨 Tab 同步用 SharedWorker。
3. 设计消息协议：请求/响应类型、错误类型、取消或超时策略都要明确。
4. 传大对象时优先 Transferable Objects；不要让结构化克隆吞掉 Worker 带来的收益。
5. 在组件或页面卸载时 `terminate()`，并通过 Profiler、Performance 面板或 FPS 指标验证主线程改善。

## 详细参考

- 需要原生 Worker 文件、构建工具导入、React 生命周期封装和清理示例时，加载 [references/basic-worker.md](references/basic-worker.md)。
- 需要 Transferable Objects、Comlink、Worker pool、SharedWorker、CSP 和 SharedArrayBuffer 注意事项时，加载 [references/advanced-workers.md](references/advanced-workers.md)。

## 约束

- Worker 内不能访问 DOM、`window`、`document`、`alert()` 或同步 `localStorage`。
- 高频通信可能比主线程计算更慢；先测量再拆分。
- Worker 文件必须同源加载，并受 `worker-src` CSP 限制。
- 大型二进制数据优先 transfer，transfer 后原引用会失效。
- 每个 Worker 有独立 JS 堆，必须主动管理生命周期和内存。

## 预期输出

计算密集型操作在后台线程执行，主线程输入和滚动恢复流畅，错误与取消路径明确，Worker 在卸载时被终止且无内存泄漏。
