---
name: web-artifacts-builder
description: 用于使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的、多组件的 claude.ai HTML artifact 的工具套件。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifact - 不适用于简单的单文件 HTML/JSX artifact。
license: 完整条款见 LICENSE.txt
---

# Web Artifacts 生成器 (Web Artifacts Builder)

要构建强大的前端 claude.ai artifact，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发你的 artifact
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件
4. 向用户展示 artifact
5. (可选) 测试 artifact

**技术栈**: React 18 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## 设计与风格指南

非常重要：为了避免通常被称为“AI 废话 (AI slop)”的设计，请避免过度使用居中布局、紫色渐变、统一的圆角和 Inter 字体。

## 快速上手

### 第 1 步：初始化项目

运行初始化脚本以创建一个新的 React 项目：
```bash
bash scripts/init-artifact.sh <项目名称>
cd <项目名称>
```

这将创建一个配置齐全的项目，包含：
- ✅ React + TypeScript (通过 Vite)
- ✅ 带有 shadcn/ui 主题系统的 Tailwind CSS 3.4.1
- ✅ 已配置路径别名 (`@/`)
- ✅ 预装了 40 多个 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖项
- ✅ 配置了 Parcel 用于打包 (通过 .parcelrc)
- ✅ Node 18+ 兼容性 (自动检测并固定 Vite 版本)

### 第 2 步：开发你的 Artifact

要构建 artifact，请编辑生成的文件。请参阅下面的**常见开发任务**获取指导。

### 第 3 步：打包为单个 HTML 文件

要将 React 应用打包成单个 HTML artifact：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` —— 一个包含所有内联 JavaScript、CSS 和依赖项的自包含 artifact。此文件可以直接作为 artifact 在 Claude 对话中分享。

**要求**: 你的项目根目录下必须有一个 `index.html`。

**脚本作用**:
- 安装打包依赖项 (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- 创建支持路径别名的 `.parcelrc` 配置
- 使用 Parcel 构建 (不包含 source maps)
- 使用 html-inline 将所有资产内联到单个 HTML 中

### 第 4 步：与用户分享 Artifact

最后，在对话中与用户分享打包好的 HTML 文件，以便他们将其作为 artifact 查看。

### 第 5 步：测试/预览 Artifact (可选)

注意：这是一个完全可选的步骤。仅在必要或有要求时执行。

要测试/预览 artifact，请使用可用工具（包括其他 Skill 或内置工具如 Playwright 或 Puppeteer）。通常情况下，避免预先测试 artifact，因为这会增加请求与看到成品 artifact 之间的延迟。如果用户要求或出现问题，请在展示 artifact 后再进行测试。

## 参考资料

- **shadcn/ui 组件**: https://ui.shadcn.com/docs/components
