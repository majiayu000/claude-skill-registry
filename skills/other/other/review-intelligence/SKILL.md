---
name: trustpilot-review-intelligence
description: 当需要抓取 Trustpilot 评论、分析评分分布、提炼正负面主题、生成竞品口碑洞察或为广告与转化文案提供评论情报时使用。适用于“抓某品牌 Trustpilot 评论”“分析差评主题”“导出评论 CSV/JSON”“做口碑竞品研究”等场景，脚本位于 `scripts/tpscraper.js`。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/review-intelligence/`

```
review-intelligence/
├── scripts/
│   └── tpscraper.js
├── package.json
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# Trustpilot 评论情报采集

此技能用于从 Trustpilot 抓取品牌评论，并将评论转化为可行动的口碑情报。

## 输入参数

开始前确认：

- `domain`
- `client`，可选
- `--search`，可选关键词过滤
- `--max`
- `--pages`

## 依赖安装

首次使用前，在当前目录执行：

```bash
npm install
```

## 执行方式

```bash
node scripts/tpscraper.js --domain "<domain>" [--searchTerm "<term>"] [--maxreviews <N>] [--maxpages <N>]
```

如果用户需要按客户归档，先建目录，再移动或复制输出。

## 输出结果

- `trustpilot_<name>.json`
- `trustpilot_<name>.csv`

## 抓取后必须完成的分析

1. 星级分布
2. 正面高频主题
3. 负面高频主题
4. 3 星评论中的“差一点就满意”的改进机会
5. 可直接用于 PPC / Landing Page 的卖点与避坑点

## 分析要求

- 只给总结不够，必须给主题归纳。
- 负面主题要能回到具体评论证据。
- 如果用户是做竞品调研，要额外指出“对方被夸什么、被骂什么、我方可以怎么反打”。
