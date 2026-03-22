---
name: crawl4ai-pipeline-builder
description: 当需要使用 Crawl4AI 进行多 URL 抓取、Markdown 生成、结构化抽取、CLI 批量 crawl、会话复用、内容过滤或无 LLM 的 schema 提取流水线时使用。适用于“批量抓多个页面”“把文档站转成 markdown”“用 CSS schema 抽结构化数据”“做可复用的 crawl pipeline”等场景。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/crawl4ai/`

```
crawl4ai/
├── references/
│   ├── cli-and-sdk-quick-ref.md
│   └── extraction-strategies.md
├── scripts/
│   ├── basic_crawler.py
│   ├── batch_crawler.py
│   ├── extraction_pipeline.py
│   └── google_search.py
├── requirements.txt
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# Crawl4AI 抓取流水线

此技能用于明确要走 `crawl4ai` 的场景。它适合批量抓取、Markdown 化、结构化提取和可编排的 Python / CLI 抓取流水线。

## 先装环境

```bash
pip install crawl4ai
crawl4ai-setup
```

## 接口选择

- 快速任务：优先 `crwl` CLI
- 可编排自动化：使用 Python SDK
- 结构化提取：优先 CSS / XPath schema，只有规则不稳定时才考虑 LLM

## 推荐流程

1. 快速试跑时，先看 [CLI 与 SDK 速览](references/cli-and-sdk-quick-ref.md)。
2. 设计抽取方案时，优先看 [抽取与批量策略](references/extraction-strategies.md)。
3. 直接复用 `scripts/` 下的样例脚本，而不是从零手写。

## 自带脚本

- `scripts/basic_crawler.py`
- `scripts/batch_crawler.py`
- `scripts/extraction_pipeline.py`
- `scripts/google_search.py`

## 使用规则

- 先用 CLI 或最小脚本验证，再做批量化。
- 优先 CSS schema 提取，避免不必要的 LLM 成本。
- 需要会话、滚动或等待条件时，再补 browser/crawler 配置。
