---
name: x-report-generator
description: 使用Playwright浏览器爬取X(Twitter)真实数据，分析统计信息，生成精美的HTML报告面板并导出为高清图片。
metadata:
  short-description: X数据分析报告生成器
source:
  repository: https://github.com/AmineDiro/twitter-scraper
  license: MIT
---

# X Report Generator Tool

## Description
使用Playwright浏览器自动化技术爬取X(Twitter)平台的真实数据，进行数据分析和统计，生成精美的HTML可视化报告面板，并将其渲染为高清图片。

## Features
- 🔍 关键词搜索推文（真实爬取）
- 👤 用户推文分析
- 📊 数据统计分析（互动量、时间分布、情感分析等）
- 🎨 精美HTML报告面板（深色/浅色主题）
- 🖼️ HTML转高清PNG图片导出
- 🍪 支持Cookies登录状态保存

## Trigger
- `/x-report` command
- 用户需要分析X平台数据
- 用户想生成社交媒体报告

## Usage

```bash
# 首次使用：登录并保存cookies
python scripts/x_report_generator.py login --cookies cookies.json

# 搜索关键词并生成报告
python scripts/x_report_generator.py search "AI" --limit 50 --output report.png --cookies cookies.json

# 分析用户推文
python scripts/x_report_generator.py user "elonmusk" --limit 30 --output user_report.png

# 使用浅色主题
python scripts/x_report_generator.py search "Python" --theme light --output report.png

# 仅生成HTML（不转图片）
python scripts/x_report_generator.py search "coding" --html-only --output report.html

# 显示浏览器窗口（调试用）
python scripts/x_report_generator.py search "test" --no-headless --output report.png
```

## Requirements

```bash
pip install playwright
playwright install chromium
```

## 报告内容

- 📈 推文总数、点赞、转发、评论、浏览统计
- ⏰ 24小时发布时间分布图
- 😊 情感分析（正面/中性/负面）
- 🏷️ 热门标签云
- 👥 活跃用户 TOP 5
- 🔥 热门推文展示

## Tags
`twitter`, `x`, `scraper`, `report`, `analytics`, `visualization`, `playwright`, `html-to-image`

## Compatibility
- Codex: ✅
- Claude Code: ✅
