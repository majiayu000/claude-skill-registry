---
name: firecrawl
description: 多功能网页抓取和数据提取工具，支持同步抓取、搜索、网站地图获取和异步爬取
tool_name: firecrawl
category: web-crawling
priority: 7
tags: ["web-scraping", "data-extraction", "crawling", "automation","firecrawl"]
version: 1.0
---

# 工具调用示例（Firecrawl）

`firecrawl` 是一个多功能网页抓取和数据提取工具，通过 `mode` 参数调用不同功能。其 `parameters` 结构是嵌套的。

**✅ 正确的调用结构:**
```json
{"mode": "<功能模式>", "parameters": {"<参数名>": "<参数值>"}}
```

**💡 重要提示:**
- `scrape`、`search`、`map` 是同步操作，立即返回结果
- `crawl`、`extract` 是异步操作，返回 `job_id` 用于后续状态检查
- 所有参数都必须在 `parameters` 对象内，不要放在顶层
- URL 必须以 `http://` 或 `https://` 开头

## 功能模式详解

### ➡️ 示例 1: 抓取单个网页 (`scrape`)

**✅ 正确示例:**
```json
{
  "mode": "scrape", 
  "parameters": {
    "url": "https://docs.firecrawl.dev/",
    "formats": ["markdown"]  // 可选：["markdown", "html"]，默认 markdown
  }
}
```

### ➡️ 示例 2: 网页搜索 (`search`)

**✅ 正确示例:**
```json
{
  "mode": "search", 
  "parameters": {
    "query": "人工智能最新发展",
    "limit": 5
  }
}
```

### ➡️ 示例 3: 获取网站地图 (`map`)

**✅ 正确示例:**
```json
{
  "mode": "map", 
  "parameters": {
    "url": "https://example.com"
  }
}
```

### ➡️ 示例 4: 异步爬取网站 (`crawl`)

**✅ 正确示例:**
```json
{
  "mode": "crawl", 
  "parameters": {
    "url": "https://firecrawl.dev", 
    "limit": 5
  }
}
```
*此调用会返回一个 `job_id`，用于后续查询。*

### ➡️ 示例 5: 结构化数据提取 (`extract`)

**✅ 正确示例:**
```json
{
  "mode": "extract", 
  "parameters": {
    "urls": ["https://news.example.com/article"],
    "prompt": "提取文章标题、作者和发布时间",
    "schema": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"}, 
        "publish_time": {"type": "string"}
      }
    }
  }
}
```

### ➡️ 示例 6: 检查异步任务状态 (`check_status`)

**✅ 正确示例:**
```json
{
  "mode": "check_status", 
  "parameters": {
    "job_id": "some-unique-job-identifier"
  }
}
```

## ❌ 错误示例 (请避免以下常见错误)

- **缺少 `mode` 参数:** `{"parameters": {"url": "..."}}`
- **缺少嵌套的 `parameters` 对象:** `{"mode": "scrape", "url": "..."}`
- **将参数放在顶层:** `{"url": "..."}` 
- **使用无效的 URL 格式:** `{"mode": "scrape", "parameters": {"url": "example.com"}}` (缺少协议)
- **错误的参数类型:** `{"mode": "extract", "parameters": {"urls": "https://example.com"}}` (urls 应该是数组)