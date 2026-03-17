---
name: financial_research
display_name: 金融投研
description: 面向股票/行业/宏观的金融研究技能，结合结构化金融数据（OpenBB/AkShare）与多源信息验证，生成带引用与免责声明的研究报告。
version: 1.0.0
author: system
tags: [finance, research, stock, valuation, sentiment, 报告, 投研, 财报, 估值, A股, 美股]
allowed_tools: [financial_data, web_search, read_url, browser_open, browser_snapshot, browser_click, browser_fill, browser_screenshot, browser_close, create_document, mem_retain, mem_delete, mem_summarize, mem_pin, mem_list_blocks]
max_iterations: 30
timeout: 600
enabled: true
match_threshold: 0.65
priority: 12
---

## 使用指南

- 适用场景：个股研究、行业研究、估值分析、情绪分析
- 数据来源：OpenBB（美股/全球）、AkShare（A股），并结合网页来源交叉验证
- 合规要求：禁止买卖建议、禁止价格预测，报告必须包含免责声明

## 工作流程
1. 明确研究对象（股票代码/行业）与重点问题
2. 调用 `financial_data` 获取报价/财报/估值等结构化数据
3. 使用 `web_search`/`read_url` 获取新闻与背景资料并记录引用
4. 进行财务分析、估值分析与情绪评估
5. 生成结构化研究报告，附上引用与免责声明

## 输出格式
- Executive Summary（2-3 句）
- Company/Industry Overview
- Financial Analysis（指标表格 + 解释）
- Valuation Analysis（相对/历史/同业）
- Market Sentiment（新闻/资金流/舆情）
- Risk Factors（3-5 条）
- References（带编号）
- Disclaimer（必选）