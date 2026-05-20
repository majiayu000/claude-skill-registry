---
name: web-artifacts-builder
description: 使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的、多组件 claude.ai HTML artifacts 的工具套件。用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifacts - 不适用于简单的单文件 HTML/JSX artifacts。
license: Complete terms in LICENSE.txt
---

# Web Artifacts Builder

要构建强大的前端 claude.ai artifacts，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码开发您的 artifact
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包到单个 HTML 文件中
4. 向用户显示 artifact
5. （可选）测试 artifact

**技术栈**：React 18 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## 设计和风格指南

非常重要：为了避免通常被称为"AI 废料"的内容，避免使用过多的居中布局、紫色渐变、统一的圆角和 Inter 字体。

## 快速入门

### 步骤 1：初始化项目

运行初始化脚本以创建新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这将创建一个完全配置的项目，包括：
- ✅ React + TypeScript（通过 Vite）
- ✅ Tailwind CSS 3.4.1 与 shadcn/ui 主题系统
- ✅ 配置的路径别名（`@/`）
- ✅ 预装 40+ shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖项
- ✅ 配置的 Parcel 打包（通过 .parcelrc）
- ✅ Node 18+ 兼容性（自动检测并固定 Vite 版本）

### 步骤 2：开发您的 Artifact

要构建 artifact，请编辑生成的文件。有关指导，请参见下面的**常见开发任务**。

### 步骤 3：打包到单个 HTML 文件

要将 React 应用程序打包到单个 HTML artifact：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` - 一个自包含的 artifact，所有 JavaScript、CSS 和依赖项都内联。此文件可以直接在 Claude 对话中作为 artifact 共享。

**要求**：您的项目必须在根目录中有一个 `index.html`。

**脚本的作用**：
- 安装打包依赖项（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建带有路径别名支持的 `.parcelrc` 配置
- 使用 Parcel 构建（无源映射）
- 使用 html-inline 将所有资源内联到单个 HTML 中

### 步骤 4：与用户共享 Artifact

最后，在与用户的对话中共享打包的 HTML 文件，以便他们可以将其作为 artifact 查看。

### 步骤 5：测试/可视化 Artifact（可选）

注意：这是完全可选的步骤。仅在必要或被请求时执行。

要测试/可视化 artifact，请使用可用工具（包括其他 Skills 或内置工具，如 Playwright 或 Puppeteer）。一般来说，避免预先测试 artifact，因为它会增加请求和完成的 artifact 可以被看到之间的延迟。如果被请求或出现问题，稍后在呈现 artifact 后再进行测试。

## 参考

- **shadcn/ui 组件**：https://ui.shadcn.com/docs/components
