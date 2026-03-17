---
name: shadcnui-helper
description: shadcn/ui 组件库的安装、配置、组件实现、主题定制与排障指南。在 React/Next.js/Vite/Remix 等项目中需要：(1) 初始化或升级 shadcn/ui，(2) 查阅组件 API 与示例，(3) 定制 themes/tokens/暗色模式，(4) 解决 Radix/Tailwind 集成问题，(5) 确保交互与可访问性一致时自动触发。
---

# shadcn/ui Helper

## 什么时候用
- 要在 React/Next.js/Vite/Remix/Astro 框架中接入或升级 shadcn/ui
- 需要通过 CLI 安装组件、查看 props/依赖、调试交互或主题
- Tailwind、Radix、暗黑模式等集成出现冲突，或需要排查 SSR/CSR、Hydration、TS 配置问题

## 必须先看文档
1. 访问唯一入口 `https://ui.shadcn.com/llms.txt`（官方索引）。
2. 在索引里搜索所需主题或组件，复制对应 Markdown URL。
3. 用 `webfetch <URL>` 拉取内容，完整阅读依赖、props、slot、可访问性提示，再开始实现。
4. 如果实现中遇到新问题，重新回到索引查找相关条目，切勿凭记忆编写。

## 示例流程

### 示例 1：安装 Button 组件
1. 打开 `llms.txt`，找到 Button 条目并获取 URL。
2. `webfetch` 阅读 Button 文档，确认依赖（如 `lucide-react`）与 variant/size props。
3. 运行 `npx shadcn-ui@latest add button`，检查 `components/` 和 `lib/` 新文件。
4. 在页面中引用新组件，按文档测试 hover/focus/disabled 状态。

### 示例 2：开启暗色主题
1. 在 `llms.txt` 搜索 Dark mode/Theming 两个条目，分别 `webfetch` 阅读。
2. 按文档更新 `components.json`（如 `style: "default"`）、`tailwind.config.ts`、`globals.css` 中的 CSS 变量。
3. 为根节点添加 `class="dark"` 的切换逻辑，验证浅色/深色模式与 token 映射。
4. 若有自定义 tokens，再回到索引寻找 Theming 文档的延伸章节确认写法。
