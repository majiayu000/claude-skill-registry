---
name: news-daily
description: Daily AI and tech news aggregator that fetches summarizes and pushes news from authoritative tech sites. Sources include 机器之心 36氪 TechCrunch The Verge and MIT Technology Review. Use when user asks for daily tech/AI news or scheduled news delivery is needed or news aggregation and summarization from multiple sources is required or setting up automated news push notifications to Telegram/WhatsApp.
---

# News Daily

## Overview

Automated daily news aggregation and delivery system for AI and frontier technology news. Fetches articles from authoritative sources, extracts key information, generates AI-powered summaries of 3-5 top stories, and delivers them via scheduled push notifications.

**Key Features:**
- Multi-source news aggregation from 5 authoritative tech sites
- AI-powered summarization (3-5 top stories daily)
- Scheduled push notifications (Morning: 8:00, Afternoon: 13:00, Evening: 18:00)
- Telegram and WhatsApp delivery support
- Efficient content processing with web_fetch and web_search tools

## Quick Start

### Manual News Fetch and Push

For immediate news delivery:

```bash
# Fetch and summarize news (outputs to console)
scripts/news-fetcher.sh

# Fetch, summarize, and push to Telegram
scripts/news-fetcher.sh --push telegram

# Fetch, summarize, and push to WhatsApp
scripts/news-fetcher.sh --push whatsapp
```

### Scheduled Delivery

For automated daily delivery, set up cron jobs (see [Cron Configuration](#cron-configuration) below).

## Workflow

### 1. News Fetching

The `scripts/news-fetcher.sh` script performs these steps:

1. **Fetch from multiple sources** using web_fetch or web_search
2. **Extract article data** (title, summary, link, publication time)
3. **Filter for AI/tech relevance** based on keywords and categories
4. **Deduplicate** articles across sources

### 2. AI Summarization

After fetching, the script:

1. **Sorts by recency and relevance**
2. **Selects top 3-5 articles** for the day
3. **Generates concise summaries** using the prompt in `scripts/news-summarizer.md`
4. **Formats output** with source attribution and timestamps

### 3. Push Delivery

Formatted news is delivered via:

- **Telegram**: Uses `message` tool with Telegram channel
- **WhatsApp**: Uses `message` tool with WhatsApp channel

## News Sources

Configured in `scripts/news-sources.conf`:

- **机器之心** (https://www.jiqizhixin.com/) - Leading Chinese AI tech media
- **36氪** (https://36kr.com/) - Tech startup and venture capital news
- **TechCrunch** (https://techcrunch.com/) - Global tech industry news
- **The Verge** (https://www.theverge.com/) - Consumer tech and digital culture
- **MIT Technology Review** (https://www.technologyreview.org/) - Emerging technology insights

Each source is configured with:
- Base URL
- Article selectors (CSS/XPath)
- Fetch method (web_search or web_fetch)
- Priority and reliability score

## Cron Configuration

For scheduled delivery, add to crontab (`crontab -e`):

```bash
# Morning news - 8:00 AM
0 8 * * * /home/aa/clawd/skills/news-daily/news-daily/scripts/news-fetcher.sh --push telegram >> /home/aa/clawd/logs/news-morning.log 2>&1

# Afternoon news - 1:00 PM
0 13 * * * /home/aa/clawd/skills/news-daily/news-daily/scripts/news-fetcher.sh --push telegram >> /home/aa/clawd/logs/news-afternoon.log 2>&1

# Evening news - 6:00 PM
0 18 * * * /home/aa/clawd/skills/news-daily/news-daily/scripts/news-fetcher.sh --push telegram >> /home/aa/clawd/logs/news-evening.log 2>&1
```

**Time zones:** Adjust hours based on your local timezone. Crontab uses server local time.

**Logs:** Ensure log directory exists:
```bash
mkdir -p /home/aa/clawd/logs
```

**Interactive setup:** Use the cron setup script for guided configuration:
```bash
scripts/cron-setup.sh
```

## Configuration

### Push Channel Configuration

Edit `scripts/config.sh` to set your default push channel:

```bash
# Default push channel: telegram or whatsapp
DEFAULT_CHANNEL="telegram"

# Telegram chat ID (optional, overrides default)
TELEGRAM_CHAT_ID=""

# WhatsApp contact ID (optional, overrides default)
WHATSAPP_CONTACT_ID=""
```

### News Source Customization

Edit `scripts/news-sources.conf` to:
- Add/remove news sources
- Adjust article selectors
- Configure fetch methods
- Set source priorities

### Summary Customization

Edit `scripts/news-summarizer.md` to adjust:
- Summary length
- Selection criteria
- Output format
- Language style

## Output Format

Example news summary output:

```
📰 每日科技早报 | 2025-01-31

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 GPT-5 即将发布：OpenAI 宣布将于下月推出最新模型
来源：机器之心 | 2小时前
https://www.jiqizhixin.com/article/xxxx

摘要：OpenAI 确认 GPT-5 将于下月正式发布，新模型在推理能力和多模态理解方面有显著提升...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 NASA 宣布新一代火星探测器任务
来源：The Verge | 5小时前
https://www.theverge.com/xxxx

摘要：NASA 公布了新一代火星探测器的详细计划，预计将于 2028 年发射...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 DeepMind 新算法突破蛋白质折叠预测瓶颈
来源：MIT Technology Review | 8小时前
https://www.technologyreview.org/xxxx

摘要：DeepMind 的 AlphaFold 3 在蛋白质结构预测准确率上达到新高度...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 今日共收集 127 篇文章，精选 3 条重点新闻
```

## Troubleshooting

### News fetch fails

- Check internet connectivity
- Verify source URLs in `news-sources.conf` are accessible
- Review logs in `/home/aa/clawd/logs/`

### Push notification fails

- Verify channel configuration in `config.sh`
- Check `message` tool is properly configured
- Ensure Telegram/WhatsApp credentials are valid

### Cron jobs not running

- Check crontab with `crontab -l`
- Verify script paths are absolute
- Check cron logs: `grep CRON /var/log/syslog`
- Ensure script has execute permissions: `chmod +x scripts/news-fetcher.sh`

## Resources

### scripts/news-fetcher.sh
Main script that orchestrates fetching, summarization, and pushing. Accepts arguments:
- `--push <channel>`: Push to specified channel (telegram/whatsapp)
- `--sources <list>`: Comma-separated list of sources to fetch
- `--articles <n>`: Number of articles to summarize (default: 3-5)

### scripts/news-summarizer.md
Prompt template for AI-powered news summarization. Includes instructions for:
- Article selection criteria
- Summary formatting
- Source attribution
- Language style (Chinese/English)

### scripts/news-sources.conf
Configuration file defining news sources, their URLs, and fetch parameters.

### scripts/config.sh
Global configuration for channels, log paths, and defaults.

### scripts/cron-setup.sh
Interactive cron job setup script for easy configuration.

### scripts/fetch_news.py
Python implementation for news fetching with support for:
- Multiple source configurations
- Keyword-based filtering
- Deduplication
- JSON export

### INSTALL.md
Detailed installation and setup guide with troubleshooting.
