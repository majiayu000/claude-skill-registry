---
name: vitepress
description: 处理 VitePress 站点配置、构建和部署相关任务。使用时涉及站点配置、主题定制、构建优化、部署配置时。
---

# VitePress 站点管理助手

## 项目技术栈
- **VitePress**: 1.6.3 (静态站点生成)
- **Vue**: 3.5.13 (前端框架)
- **Vite**: 5.0.3 (构建工具)
- **包管理**: pnpm (依赖管理)
- **部署**: GitHub Pages (路径: `/xf-blog/`)

## 配置管理

### 主题配置
- **组件位置**: `docs/.vitepress/theme/components/`
- **自定义组件**:
  - `Archive.vue` - 归档页面
  - `ArticleMetadata.vue` - 文章元数据
  - `Tag.vue` - 标签组件
  - `WordCloud.vue` - 词云组件
  - `layout/` - 布局相关组件

### UI 组件库
- **Arco Design Vue**: 2.57.0 (主要 UI 组件库)
- **AntV G2Plot**: 2.4.31 (图表可视化)
- **自动导入**: unplugin-vue-components 配置

### Markdown 增强
- **数学公式**: markdown-it-mathjax3 (MathJax 渲染)
- **图表**: Mermaid 9.3.0 + vitepress-plugin-mermaid
- **脚注**: markdown-it-footnote
- **自定义元素**: 支持 MathJax 数学公式标签

### 侧边栏配置
侧边栏配置位于 `docs/.vitepress/config/sidebar.ts`：
```typescript
export const sidebar = {
  '/ai/': [
    {
      text: 'AI相关',
      collapsible: true,
      collapsed: false,
      items: [
        { text: '工具汇总', link: '/ai/tools/2026/01/18/AI编程工具汇总对比' }
      ]
    }
  ]
}
```

### 导航配置
- **主导航**: `docs/.vitepress/config/nav.ts`
- **侧边栏**: 分类页面导航
- **大纲**: 页面右侧目录 (level: 'deep')
- **多语言**: 支持中文界面

## 构建和部署

### 本地开发
```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev docs

# 预览构建结果
pnpm preview docs
```

### 生产构建
```bash
# 构建生产版本
pnpm build docs

# GitHub Pages 自动部署流程:
# 1. 推送到 main 分支
# 2. GitHub Actions 触发构建
# 3. 自动部署到 pages 分支
# 4. 访问地址: https://rockyflux.github.io/xf-blog/
```

### Algolia 搜索索引
```bash
# 索引文档到 Algolia (索引名: xfblog)
pnpm run index:algolia

# 脚本位置: scripts/index-algolia.js
# 配置: ALGOLIA_APP_ID, ALGOLIA_API_KEY, ALGOLIA_INDEX_NAME
```

## 站点功能特性

### 评论系统
- **Gitalk**: 集成 GitHub Issues 作为评论系统
- **配置**: 支持 GitHub OAuth 应用
- **组件**: `layout/Comment.vue`

### 社交链接
- **GitHub**: https://github.com/rockyflux/xf-blog
- **Gitee**: 码云镜像
- **自定义图标**: 支持 SVG 图标

### 搜索功能
- **Algolia**: 云端搜索服务 (xfblog 索引)
- **本地搜索**: 备选离线搜索
- **搜索配置**: `docs/.vitepress/config/search/`

### 编辑链接
- **GitHub 编辑**: 直接跳转到源码编辑页面
- **文本**: "不妥之处，敬请雅正"

## 内容组织规范

### 文档路径结构
```
docs/
├── ai/tools/2026/01/18/文章标题.md    # AI工具文章
├── dev-tools/editor/2026/01/15/文章标题.md  # 开发工具
├── tutorials/教程名称.md              # 教程文档
└── index.md                         # 首页
```

### Frontmatter 规范
```yaml
---
title: 文章标题
description: 简短描述
date: 2026-01-18
tags: [标签1, 标签2]
author: 箫风
---
```

## 常见任务

### 添加新文章
1. **确定分类**: 选择合适的目录 (`ai/`, `dev-tools/`, `tutorials/` 等)
2. **创建文件**: 按日期格式 `YYYY/MM/DD/标题.md`
3. **添加元数据**: 完整的 frontmatter
4. **更新侧边栏**: 在 `config/sidebar.ts` 中添加条目
5. **测试显示**: `pnpm dev` 预览效果
6. **提交发布**: 推送到 main 分支自动部署

### 添加新分类
1. **创建目录**: 在 `docs/` 下创建分类目录
2. **添加侧边栏**: 在 `config/sidebar.ts` 中配置
3. **创建索引**: 添加 `index.md` 文件
4. **更新导航**: 如需要，在 `config/nav.ts` 中添加

### 自定义主题组件
1. **组件位置**: `docs/.vitepress/theme/components/`
2. **自动导入**: 已配置 unplugin-vue-components
3. **样式定制**: `theme/styles/` 目录
4. **测试验证**: 本地预览后构建测试

### 更新搜索索引
```bash
# 索引新内容到 Algolia
pnpm run index:algolia

# 检查索引状态
# 访问 Algolia 控制台或搜索测试
```

## 故障排除

### 构建失败
- **依赖问题**: 检查 `pnpm install` 是否成功
- **版本冲突**: 查看 `pnpm-lock.yaml` 和 `package.json`
- **配置文件**: 验证 `config.ts` 和主题配置语法
- **构建日志**: 查看完整的错误信息

### 页面显示异常
- **路径问题**: 检查链接是否使用 `/xf-blog/` 前缀
- **图片路径**: 确保图片在 `docs/public/` 目录
- **Markdown 语法**: 验证代码块和表格格式
- **组件导入**: 检查自定义组件是否正确注册

### 搜索功能异常
- **Algolia 配置**: 验证 API Key 和索引名称
- **索引脚本**: 检查 `scripts/index-algolia.js`
- **权限问题**: 确认 Algolia 管理权限
- **网络问题**: 检查 Algolia 服务状态

### 数学公式不显示
- **MathJax 配置**: 检查 `config/markdown.ts`
- **自定义元素**: 确认 `mjx-*` 标签在允许列表
- **插件加载**: 验证 vitepress-plugin-mermaid

### 评论系统异常
- **Gitalk 配置**: 检查 OAuth 应用设置
- **GitHub Issues**: 确认仓库权限
- **组件加载**: 验证 Comment.vue 组件