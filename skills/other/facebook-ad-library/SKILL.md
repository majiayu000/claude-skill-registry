---
name: facebook-ad-library-scraper
description: 当需要抓取 Facebook Ad Library 广告素材、下载图片和视频、提取转写内容、整理品牌广告素材库或分析竞品创意形式时使用。适用于“抓 Facebook 广告库”“把某品牌广告素材存下来”“分析广告视频文案和创意样式”等场景。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/facebook-ad-library/`

```
facebook-ad-library/
├── references/
│   └── output-schema.md
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# Facebook 广告库素材采集

此技能用于采集 Facebook Ad Library 中的广告创意素材，并整理为后续可分析的数据包。

## 适用范围

- 品牌广告创意采样
- 视频 / 图片素材落盘
- 广告文案与转写整理
- 广告形式分类与关键信息抽取

## 推荐流程

1. 使用浏览器工具打开用户提供的 Facebook Ad Library URL。
2. 提取广告列表中的媒体资源 URL。
3. 滚动加载更多广告并持续追加。
4. 下载视频、图片到品牌目录。
5. 对视频做音轨提取和转写，对图片做视觉描述。
6. 按统一结构整理为 `ads-data.json`。

## 目录建议

```text
<brand>/
├── videos/
├── images/
└── ads-data.json
```

## 数据结构

输出结构与字段建议见 [输出结构与分类建议](references/output-schema.md)。

## 依赖要求

- 浏览器自动化能力
- `curl`
- `ffmpeg`
- 可用的转写工具，例如 `whisper`
