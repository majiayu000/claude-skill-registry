---
name: opentui
description: Comprehensive OpenTUI skill for building terminal user interfaces. Covers the core imperative API, React reconciler, and Solid reconciler. Use for any TUI development task including components, layout, keyboard handling, animations, and testing.
metadata:
   references: core, react, solid
---

# OpenTUI 平台技能

使用 OpenTUI 构建终端用户界面的综合技能。使用下面的决策树找到合适的框架和组件，然后加载详细的参考文档。

## 关键规则

**在所有 OpenTUI 代码中遵循这些规则：**

1. **使用 `create-tui` 创建新项目。** 参见框架 `REFERENCE.md` 快速入门。
2. **`create-tui` 选项必须在参数之前。** `bunx create-tui -t react my-app` 有效，`bunx create-tui my-app -t react` 无效。
3. **永远不要直接调用 `process.exit()`。** 使用 `renderer.destroy()`（参见 `core/gotchas.md`）。
4. **文本样式在 React/Solid 中需要嵌套标签。** 使用修饰符元素，而不是 props（参见 `components/text-display.md`）。

## 如何使用此技能

### 参考文件结构

框架参考文档遵循 5 文件模式。跨领域概念是单文件指南。

`./references/<framework>/` 中的每个框架包含：

| 文件 | 用途 | 何时阅读 |
|------|---------|--------------|
| `REFERENCE.md` | 概述、何时使用、快速入门 | **始终首先阅读** |
| `api.md` | 运行时 API、组件、钩子 | 编写代码时 |
| `configuration.md` | 设置、tsconfig、打包 | 配置项目时 |
| `patterns.md` | 常见模式、最佳实践 | 实现指导 |
| `gotchas.md` | 陷阱、限制、调试 | 故障排除时 |

`./references/<concept>/` 中的跨领域概念以 `REFERENCE.md` 为入口点。

### 阅读顺序

1. 从所选框架的 `REFERENCE.md` 开始
2. 然后阅读与任务相关的其他文件：
   - 构建组件 -> `api.md` + `components/<category>.md`
   - 设置项目 -> `configuration.md`
   - 布局/定位 -> `layout/REFERENCE.md`
   - 故障排除 -> `gotchas.md` + `testing/REFERENCE.md`

### 示例路径

```
./references/react/REFERENCE.md           # React 从这里开始
./references/react/api.md              # React 组件和钩子
./references/solid/configuration.md    # Solid 项目设置
./references/components/inputs.md      # Input、Textarea、Select 文档
./references/core/gotchas.md           # 核心调试技巧
```

### 运行时说明

OpenTUI 在 Bun 上运行，并使用 Zig 进行原生构建。阅读 `./references/core/gotchas.md` 了解运行时要求和构建指南。

## 快速决策树

### "我应该使用哪个框架？"

```
哪个框架？
├─ 我想要完全控制、最大性能、无框架开销
│  └─ core/ (命令式 API)
├─ 我了解 React，想要熟悉的组件模式
│  └─ react/ (React reconciler)
├─ 我想要细粒度响应性、最佳重渲染
│  └─ solid/ (Solid reconciler)
└─ 我正在 OpenTUI 之上构建库/框架
   └─ core/ (命令式 API)
```

### "我需要显示内容"

```
显示内容？
├─ 纯文本或样式文本 -> components/text-display.md
├─ 带边框/背景的容器 -> components/containers.md
├─ 可滚动内容区域 -> components/containers.md (scrollbox)
├─ ASCII 艺术横幅/标题 -> components/text-display.md (ascii-font)
├─ 带语法高亮的代码 -> components/code-diff.md
├─ 差异查看器（统一/拆分） -> components/code-diff.md
└─ 带诊断的行号 -> components/code-diff.md
```

### "我需要用户输入"

```
用户输入？
├─ 单行文本字段 -> components/inputs.md (input)
├─ 多行文本编辑器 -> components/inputs.md (textarea)
├─ 从列表中选择（垂直） -> components/inputs.md (select)
├─ 基于标签的选择（水平） -> components/inputs.md (tab-select)
└─ 自定义键盘快捷键 -> keyboard/REFERENCE.md
```

### "我需要布局/定位"

```
布局？
├─ Flexbox 样式布局（行、列、换行） -> layout/REFERENCE.md
├─ 绝对定位 -> layout/patterns.md
├─ 响应终端大小 -> layout/patterns.md
├─ 内容居中 -> layout/patterns.md
└─ 复杂嵌套布局 -> layout/patterns.md
```

### "我需要动画"

```
动画？
├─ 基于时间轴的动画 -> animation/REFERENCE.md
├─ 缓动函数 -> animation/REFERENCE.md
├─ 属性过渡 -> animation/REFERENCE.md
└─ 循环动画 -> animation/REFERENCE.md
```

### "我需要处理输入"

```
输入处理？
├─ 键盘事件（按键、释放） -> keyboard/REFERENCE.md
├─ 焦点管理 -> keyboard/REFERENCE.md
├─ 粘贴事件 -> keyboard/REFERENCE.md
├─ 鼠标事件 -> components/containers.md
└─ 文本选择 -> components/text-display.md
```

### "我需要测试我的 TUI"

```
测试？
├─ 快照测试 -> testing/REFERENCE.md
├─ 交互测试 -> testing/REFERENCE.md
├─ 测试渲染器设置 -> testing/REFERENCE.md
└─ 调试测试 -> testing/REFERENCE.md
```

### "我需要调试/故障排除"

```
故障排除？
├─ 运行时错误、崩溃 -> <framework>/gotchas.md
├─ 布局问题 -> layout/REFERENCE.md + layout/patterns.md
├─ 输入/焦点问题 -> keyboard/REFERENCE.md
└─ 复现 + 回归测试 -> testing/REFERENCE.md
```

### 故障排除索引

- 终端清理、崩溃 -> `core/gotchas.md`
- 文本样式未应用 -> `components/text-display.md`
- 输入焦点/快捷键 -> `keyboard/REFERENCE.md`
- 布局错位 -> `layout/REFERENCE.md`
- 不稳定的快照 -> `testing/REFERENCE.md`

有关组件命名差异和文本修饰符，请参见 `components/REFERENCE.md`。

## 产品索引

### 框架
| 框架 | 入口文件 | 描述 |
|-----------|------------|-------------|
| Core | `./references/core/REFERENCE.md` | 命令式 API、所有原语 |
| React | `./references/react/REFERENCE.md` | 声明式 TUI 的 React reconciler |
| Solid | `./references/solid/REFERENCE.md` | 声明式 TUI 的 SolidJS reconciler |

### 跨领域概念
| 概念 | 入口文件 | 描述 |
|---------|------------|-------------|
| 布局 | `./references/layout/REFERENCE.md` | Yoga/Flexbox 布局系统 |
| 组件 | `./references/components/REFERENCE.md` | 按类别分类的组件参考 |
| 键盘 | `./references/keyboard/REFERENCE.md` | 键盘输入处理 |
| 动画 | `./references/animation/REFERENCE.md` | 基于时间轴的动画 |
| 测试 | `./references/testing/REFERENCE.md` | 测试渲染器和快照 |

### 组件类别
| 类别 | 入口文件 | 组件 |
|----------|------------|------------|
| 文本与显示 | `./references/components/text-display.md` | text、ascii-font、styled text |
| 容器 | `./references/components/containers.md` | box、scrollbox、borders |
| 输入 | `./references/components/inputs.md` | input、textarea、select、tab-select |
| 代码与差异 | `./references/components/code-diff.md` | code、line-number、diff |

## 资源

**仓库**: https://github.com/anomalyco/opentui
**核心文档**: https://github.com/anomalyco/opentui/tree/main/packages/core/docs
**示例**: https://github.com/anomalyco/opentui/tree/main/packages/core/src/examples
**精选列表**: https://github.com/msmps/awesome-opentui
