---
name: firecrawl-web-extraction
description: 当需要使用 Firecrawl 完成网页搜索、单页抓取、结构化提取、截图、URL 映射、整站 crawl 或 JavaScript 渲染页面内容提取时使用。适用于“搜索并抓网页内容”“提取某个 URL 的主体内容”“把网页字段按 schema 抽出来”“批量抓文档站”以及需要 Firecrawl CLI 的场景。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/firecrawl/`

```
firecrawl/
├── references/
│   └── command-cheatsheet.md
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# Firecrawl 网页抓取与映射

此技能用于已经明确要走 Firecrawl 的场景。Firecrawl 适合把网页内容变成适合模型处理的 Markdown、结构化 JSON 或整站抓取结果。

## 使用原则

1. 没有 URL 时先 `search`。
2. 已有 URL 时先 `scrape`。
3. 站点很大时先 `map` 找到正确页面，再精确抓取。
4. 需要大范围批量抓取时再 `crawl`。
5. 只有在必须交互时才升级到浏览器模式。

## 执行前检查

先确认 Firecrawl CLI 可用：

```bash
firecrawl --status
```

若未安装或未登录，读取 [Firecrawl 命令速查](references/command-cheatsheet.md) 中的安装与认证部分。

## 常见路线

### 路线 1：搜索后抓取

适用于不知道具体 URL，只知道主题、产品名或文档站关键字。

### 路线 2：直接抓单页

适用于已明确目标 URL，只需要正文、链接、HTML 或截图。

### 路线 3：站点映射

适用于文档站、博客、知识库、目录型站点，先找目标子路径再抓取。

### 路线 4：整站 crawl

适用于批量采集某一站点栏目或文档集合。

## 输出习惯

- 默认写入工作目录下的 `.firecrawl/`。
- 尽量使用 `-o` 输出到文件，而不是把大块结果直接塞进上下文。
- 读取 Firecrawl 输出时，优先用预览和搜索，不要一次性读完整个大文件。

## 何时不该用 Firecrawl

- 任务需要深度登录、复杂点击流和多步表单时。
- 站点高度依赖交互且浏览器模式更直接时。
- 只需少量 DOM 操作而现有 Playwright / 浏览器工具更稳时。
