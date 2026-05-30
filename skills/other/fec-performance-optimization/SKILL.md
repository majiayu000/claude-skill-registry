---
name: fec-performance-optimization
description: Use when diagnosing or improving frontend performance, Core Web Vitals, bundle size, runtime rendering cost, network waterfalls, memory leaks, long tasks, Lighthouse findings, or performance budgets; Chinese triggers include 性能优化, 页面卡顿, 首屏慢, 包体积, Web Vitals.
---

# 前端性能优化

## Purpose

用可度量的方式定位前端性能瓶颈，并把优化建议收敛到用户主路径、构建产物和运行时证据。

## Procedure

1. 锁定体验目标
   - 明确问题属于首屏加载、交互延迟、滚动卡顿、内存上涨、网络瀑布、包体积，还是视觉稳定性。
   - 记录路由、设备、网络条件、浏览器、复现步骤和当前可用指标。
   - 没有指标时先建立基线，不直接给出“优化一切”的泛化建议。

2. 建立度量基线
   - 读取项目脚本、构建配置、依赖和已有性能报告。
   - 对页面体验优先使用 Lighthouse、Performance trace、React Profiler、Vue Devtools、Memory snapshot 或 RUM 数据。
   - 对包体优先看构建产物、source map、依赖重复、首屏 chunk 和动态 import 边界。
   - 对运行时卡顿优先看长任务、重复渲染、昂贵计算、同步循环、布局抖动和大列表。

3. 分层定位
   - 加载层：关键 CSS、字体、图片、脚本阻塞、预加载和缓存。
   - 渲染层：不稳定 key、过宽 Context、无意义 effect、重复计算、组件树过大。
   - 数据层：串行请求、重复请求、过大 payload、缺少分页或缓存策略。
   - 主线程：JSON/CSV 解析、图片处理、复杂排序过滤、同步压缩和大对象深拷贝。
   - 资源层：事件监听、定时器、订阅、WebGL/Canvas 资源和对象 URL 未释放。

4. 形成优化方案
   - 每个建议必须绑定位置、影响、改法和验证方式。
   - 优先处理高频主路径和 P95 体验；低频后台任务不抢占首屏预算。
   - 先做低风险高收益改动，如懒加载、去重、缓存、尺寸预留、虚拟列表、稳定引用和释放资源。
   - 对会牺牲可维护性的技巧，必须说明收益证据和替代方案。

5. 验证回归
   - 重新运行受影响构建、测试和性能采集命令。
   - 对比优化前后指标或产物体积。
   - 确认 loading、empty、error、offline、reduced-motion 和移动端状态未被优化破坏。

## Budgets

| Area | Default Target | Notes |
| ---- | -------------- | ----- |
| LCP | 约 2.5s 内 | 以核心页面、目标地区网络和真实设备为准 |
| CLS | 低于 0.1 | 媒体、广告、异步内容需要预留空间 |
| INP | 约 200ms 内 | 优先拆分长任务和降低交互路径重渲染 |
| Initial JS | 遵循项目预算 | 没有预算时先报告当前 gzip / brotli 体积 |
| Main thread | 避免连续长任务 | 大计算考虑分片、缓存或 Worker |

## Checks

- 首屏资源是否包含非首屏组件、图表、编辑器、地图或全量图标库。
- 图片是否有明确尺寸、合适格式、懒加载和首屏优先级。
- 列表、表格、时间线是否需要虚拟化或分页。
- 搜索、筛选、排序是否在热路径重复 O(n*m) 扫描。
- 请求是否可并行、可缓存、可取消、可复用。
- 监听、订阅、定时器、AbortController、Object URL、Canvas/WebGL 资源是否对称清理。

## Constraints

- 不做没有目标和证据的过早优化。
- 不靠关闭功能、删除状态反馈或降低可访问性来换性能分数。
- 不为一次 Lighthouse 分数牺牲真实用户主路径。
- 不引入大型新依赖解决小问题；先利用项目已有工具和浏览器能力。
- 不把后端、网络和浏览器侧问题混为一谈；前端能验证的部分要单独列证据。

## Expected Output

输出性能分析报告，包含基线、指标或观察证据、瓶颈位置、优先级、改法、验证命令和剩余风险。报告保存为 `reports/performance-review-YYYY-MM-DD-HHmmss.md`。
