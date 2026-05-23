---
name: notion-content
description: Create content records in Notion database after publishing articles. Use when user provides article title and publishing links (zhihu, weixin, baidu, sohu, toutiao, x.com). Auto-detects platform from URL, fills publish date. Trigger on "/notion-content", "notion记录", "内容入库", or when user says they published an article with links.
---

# Notion Content Manager

Create content records in Notion "内容中心" database after publishing articles to various platforms.

## Usage

User provides:
- **Title**: Article title (required)
- **Links**: One or more published article URLs (required)

Example input:
```
/notion-content
标题：《AI编程实战指南》
链接：
https://zhuanlan.zhihu.com/p/123456
https://mp.weixin.qq.com/s/abcdef
```

## Workflow

1. Parse user input to extract title and links
2. Run the script:
```bash
python scripts/notion_content.py --title "文章标题" --links "url1" "url2" "url3"
```
3. Report results to user

## Script Location

`scripts/notion_content.py` - handles all business logic:
- Platform detection from URL domain
- Duplicate link checking
- Notion API calls
- Error handling

## Environment Setup

Requires `.env` file in skill directory with:
```
NOTION_TOKEN=secret_xxxxx
```

## Supported Platforms

| Platform | URL Pattern |
|----------|-------------|
| 知乎 | zhihu.com |
| 百家号 | baijiahao.baidu.com |
| 搜狐号 | sohu.com |
| 头条号 | toutiao.com |
| 公众号 | mp.weixin.qq.com |
| X文章 | x.com, twitter.com |
