---
name: mui-helper
description: MUI (Material-UI) 组件库使用指南和参考文档。在需要使用 MUI 组件开发 UI 时自动触发：(1) 创建或修改使用 Material-UI 的 UI 组件，(2) 解决 MUI 组件实现问题，(3) 查询 MUI 组件属性和 API，(4) 实现 MUI 布局和主题定制，(5) 在 MUI 版本间迁移或自定义组件行为。
---

# MUI Helper

## 什么时候使用这个 Skill

当以下场景时，自动触发此 Skill：

1. 创建或修改使用 Material-UI 的 UI 组件
2. 解决 MUI 组件实现问题
3. 查询 MUI 组件属性和 API
4. 实现 MUI 布局和主题定制
5. 在 MUI 版本间迁移或自定义组件行为

## 使用前必须查阅文档

### 重要提醒
**在使用任何 MUI 组件或功能前，必须先查阅官方文档，找到对应组件或主题的具体 URL，仔细阅读官方文档后才能开始开发。**

### 为什么必须查阅文档
1. 每个 MUI 组件都有独特的 API 和属性
2. 官方文档包含正确的使用示例和最佳实践
3. 避免常见的错误用法和性能问题
4. 确保代码符合 MUI 的设计规范

### 查阅文档的步骤

#### 第一步：访问文档索引
访问 MUI 官方文档索引：https://mui.com/material-ui/llms.txt

该文件包含所有组件和功能的目录，按以下分类组织：
- Components：所有组件列表
- Customization：主题定制相关
- Guides：使用指南
- Integrations：框架集成
- Migration：版本迁移

#### 第二步：找到具体的 URL
在文档索引中找到你需要的组件或功能，例如：
- `React Button component` → `https://mui.com/material-ui/react-button.md`
- `Dark mode` → `https://mui.com/material-ui/customization/dark-mode.md`
- `Next.js integration` → `https://mui.com/material-ui/integrations/nextjs.md`

#### 第三步：获取具体 URL 并阅读
使用 `webfetch` 工具获取文档内容，仔细阅读：
- 组件的 Props 和 API
- 示例代码
- 注意事项和限制
- 常见问题

#### 第四步：基于文档开发
确保完全理解文档内容后，再进行开发。

## 查阅文档示例

### 场景 1：使用 Button 组件
1. 访问文档索引：https://mui.com/material-ui/llms.txt
2. 在 Components 部分找到 `React Button component`
3. 获取 URL：`https://mui.com/material-ui/react-button.md`
4. 使用 `webfetch` 获取该 URL 的文档内容
5. 阅读 Props 说明（variant, color, size, disabled 等）
6. 查看示例代码
7. 根据文档正确使用组件

### 场景 2：自定义主题
1. 访问文档索引：https://mui.com/material-ui/llms.txt
2. 在 Customization 部分找到 `Theming`
3. 获取 URL：`https://mui.com/material-ui/customization/theming.md`
4. 使用 `webfetch` 获取该 URL 的文档内容
5. 阅读 `createTheme` 的配置选项
6. 了解如何定义 palette, typography 等
7. 根据文档创建主题

### 场景 3：解决组件问题
1. 访问文档索引：https://mui.com/material-ui/llms.txt
2. 找到相关组件文档
3. 使用 `webfetch` 获取文档内容
4. 检查常见问题部分
5. 查看是否有 API 变更或废弃警告
6. 参考官方建议的解决方案

## 外部资源

- [官方文档](https://mui.com/material-ui/)
- [文档索引](https://mui.com/material-ui/llms.txt)
- [组件 API 搜索](https://mui.com/material-ui/api/all/)
- [示例项目](https://mui.com/material-ui/getting-started/example-projects.md)
