---
name: react-native-best-practices
description: "提供 React Native 性能优化指南，涵盖 FPS、TTI、打包体积、内存泄漏、重渲染与动画。适用于涉及 Hermes 优化、JS 线程阻塞、桥接开销、FlashList、原生模块或调试卡顿与掉帧的任务。"
license: MIT
---

# React Native 最佳实践

React Native 应用性能优化指南，涵盖 JavaScript/React、原生（iOS/Android）与打包优化。基于 Callstack 的「React Native 优化终极指南」。

## 技能格式

每个参考文件遵循混合格式，用于快速查找与深度理解：
- **快速模式**：错误/正确代码片段用于即时模式匹配
- **快速命令**：Shell 命令用于流程/度量技能
- **快速配置**：配置片段用于设置聚焦技能
- **快速参考**：摘要表用于概念技能
- **深度探索**：完整上下文，包含何时使用、先决条件、逐步、常见陷阱

**影响评级**：CRITICAL（立即修复）、HIGH（显著改进）、MEDIUM（值得优化）

## 何时应用

在以下场景参考这些指南：
- 调试慢/卡顿 UI 或动画
- 调查内存泄漏（JS 或原生）
- 优化应用启动时间（TTI）
- 减少打包或应用大小
- 编写原生模块（Turbo Modules）
- 分析 React Native 性能
- 审查 React Native 代码性能

## 优先级排序指南

| 优先级 | 类别 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | FPS 与重渲染 | 关键 | `js-*` |
| 2 | 打包体积 | 关键 | `bundle-*` |
| 3 | TTI 优化 | 高 | `native-*`, `bundle-*` |
| 4 | 原生性能 | 高 | `native-*` |
| 5 | 内存管理 | 中高 | `js-*`, `native-*` |
| 6 | 动画 | 中 | `js-*` |

## 速查

### 关键：FPS 与重渲染

**先分析**：
```bash
# 打开 React Native DevTools
# 在 Metro 中按 'j'，或摇动设备 → "Open DevTools"
```

**常见修复**：
- 用 FlatList/FlashList 替换 ScrollView 用于列表
- 使用 React Compiler 进行自动 memoization
- 使用原子状态（Jotai/Zustand）减少重渲染
- 对昂贵计算使用 `useDeferredValue`

### 关键：打包体积

**分析打包**：
```bash
npx react-native bundle \
 --entry-file index.js \
 --bundle-output output.js \
 --platform ios \
 --sourcemap-output output.js.map \
 --dev false --minify true

npx source-map-explorer output.js --no-border-checks
```

**常见修复**：
- 避免 barrel 导入（从源直接导入）
- 移除不必要的 Intl polyfills（Hermes 有原生支持）
- 启用 tree shaking（Expo SDK 52+ 或 Re.Pack）
- 为 Android 原生代码启用 R8

### 高：TTI 优化

**度量 TTI**：
- 使用 `react-native-performance` 用于标记
- 仅度量冷启动（排除热/预热）

**常见修复**：
- 在 Android 上禁用 JS 打包压缩（启用 Hermes mmap）
- 使用原生导航（react-native-screens）
- 用 `InteractionManager` 延迟非关键工作

### 高：原生性能

**分析原生**：
- iOS：Xcode Instruments → Time Profiler
- Android：Android Studio → CPU Profiler

**常见修复**：
- 对重型原生工作使用后台线程
- 优先异步而非同步 Turbo Module 方法
- 对跨平台性能关键代码使用 C++

## 参考

完整文档与代码示例在 `references/`：

**JavaScript/React (`js-*`)**：js-lists-flatlist-flashlist（CRITICAL：用虚拟化列表替换 ScrollView）、js-profile-react、js-measure-fps、js-memory-leaks、js-atomic-state、js-concurrent-react、js-react-compiler、js-animations-reanimated、js-uncontrolled-components。  
**原生 (`native-*`)**：native-turbo-modules、native-sdks-over-polyfills、native-measure-tti、native-threading-model、native-profiling、native-platform-setup、native-view-flattening、native-memory-patterns、native-memory-leaks、native-android-16kb-alignment（CRITICAL：第三方库对齐用于 Google Play）。  
**打包 (`bundle-*`)**：bundle-barrel-exports（CRITICAL：避免 barrel 导入）、bundle-analyze-js（CRITICAL：JS 打包可视化）、bundle-tree-shaking、bundle-analyze-app、bundle-r8-android、bundle-hermes-mmap、bundle-native-assets、bundle-library-size、bundle-code-splitting。

## 问题 → 技能映射

| 问题 | 从...开始 |
|------|----------|
| 应用感觉慢/卡顿 | js-measure-fps.md → js-profile-react.md |
| 太多重渲染 | js-profile-react.md → js-react-compiler.md |
| 慢启动（TTI） | native-measure-tti.md → bundle-analyze-js.md |
| 应用体积大 | bundle-analyze-app.md → bundle-r8-android.md |
| 内存增长 | js-memory-leaks.md 或 native-memory-leaks.md |
| 动画掉帧 | js-animations-reanimated.md |
| 列表滚动卡顿 | js-lists-flatlist-flashlist.md |
| TextInput 延迟 | js-uncontrolled-components.md |
| 原生模块慢 | native-turbo-modules.md → native-threading-model.md |
| 原生库对齐问题 | native-android-16kb-alignment.md |

## 归因

基于 Callstack 的「React Native 优化终极指南」。
