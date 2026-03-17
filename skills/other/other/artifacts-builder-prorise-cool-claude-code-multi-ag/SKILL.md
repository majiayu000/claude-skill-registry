---
name: artifacts-builder
description: 一套用于使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的多组件 claude.ai HTML 工件的工具集。适用于需要状态管理、路由或 shadcn/ui 组件的复杂工件，不适用于简单的单文件 HTML/JSX 工件。
license: Complete terms in LICENSE.txt
---

# Artifacts Builder

要构建强大的前端 claude.ai 工件，请按照以下步骤操作：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发您的工件
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件
4. 向用户展示工件
5. （可选）测试工件

**技术栈**: React 18 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

非常重要：为避免通常被称为 "AI slop" 的情况，请避免使用过多的居中布局、紫色渐变、统一的圆角和 Inter 字体。

## Quick Start

### Step 0: 询问主题配色规范（重要）

**在调用初始化脚本之前，必须先询问用户项目的主题配色规范。**

询问用户以下信息：
- **主色调**：项目使用什么主色调？（例如：蓝色、绿色、紫色、灰色等）
- **品牌色**：如果有具体的品牌色值（HSL、RGB 或十六进制），请提供
- **设计规范**：是否有完整的设计系统规范文件？（如果有，可以基于规范生成完整的主题配置）

如果用户提供了主题配色信息，在调用脚本时通过环境变量传递：
```bash
THEME_COLOR=blue bash scripts/init-artifact.sh <project-name>
```

支持的主题色：`slate`（默认灰色）、`blue`、`green`、`violet`

如果用户没有提供主题配色，使用默认的 `slate` 灰色主题。

### Step 1: Initialize Project

运行初始化脚本以创建新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
# 或指定主题色
THEME_COLOR=blue bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这将创建一个完全配置的项目，包含：
- ✅ React + TypeScript (通过 Vite)
- ✅ Tailwind CSS 3.4.1 和 shadcn/ui 主题系统
- ✅ 路径别名 (`@/`) 已配置
- ✅ 预安装 40+ shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖项
- ✅ Parcel 配置用于打包（通过 .parcelrc）
- ✅ Node 18+ 兼容性（自动检测并固定 Vite 版本）

### Step 2: Develop Your Artifact

要构建工件，请编辑生成的文件。请参阅下面的**常见开发任务**以获取指导。

### Step 3: Bundle to Single HTML File

要将 React 应用打包成单个 HTML 工件：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` - 一个自包含的工件，所有 JavaScript、CSS 和依赖项都已内联。此文件可以直接在 Claude 对话中作为工件共享。

**要求**：您的项目必须在根目录中有一个 `index.html`。

**脚本的作用**：
- 安装打包依赖项（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建支持路径别名的 `.parcelrc` 配置
- 使用 Parcel 构建（无源映射）
- 使用 html-inline 将所有资源内联到单个 HTML 中

### Step 4: Share Artifact with User

最后，在对话中与用户共享打包的 HTML 文件，以便他们可以将其作为工件查看。

### Step 5: Testing/Visualizing the Artifact (Optional)

注意：这是一个完全可选的步骤。仅在必要时或应要求时执行。

要测试/可视化工件，请使用可用工具（包括其他 Skills 或内置工具，如 Playwright 或 Puppeteer）。通常，避免提前测试工件，因为这会在请求和完成工件可见之间增加延迟。如果请求或出现问题，请在展示工件后进行测试。

## Reference

- **shadcn/ui components**: https://ui.shadcn.com/docs/components