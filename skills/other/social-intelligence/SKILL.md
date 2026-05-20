---
name: x-topic-intelligence
description: 当需要在 X/Twitter 上围绕某个主题收集热门帖子、趋势讨论、KOL 内容、钩子写法、回复驱动内容或社媒情报数据集时使用。适用于内容调研、舆情研究、话题扫描、社媒竞品观察和内容机会分析等场景，优先快速模式，深入采集时再做多轮 DOM 抓取。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/social-intelligence/`

```
social-intelligence/
├── references/
│   └── search-rounds.md
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# X / Twitter 主题情报采集

此技能用于围绕一个主题系统性收集 X/Twitter 内容，并输出结构化情报。

## 先确认主题

开始前明确：

- `topic`
- 目标：快速看趋势，还是系统建数据集
- 时间范围：24h / 7d / 自定义
- 语言

## 模式选择

- 快速概览：适合先看热点和大致方向。
- 全量采集：适合建立 JSONL / Markdown 数据集、拆解 KOL 与内容模式。

更细的轮次设计见 [采集模式与轮次](references/search-rounds.md)。

## 标准输出

输出目录建议为当前工作目录下的 `x-collect-data/`：

- `intel.jsonl`
- `intel.md`

## 输出要求

每条记录建议包含：

- 帖子 URL
- 文本摘要
- `intel_type`
- 账号
- 点赞 / 转推 / 回复 / 浏览
- 角度总结
- 内容形式
- `key_takeaway`

## 使用原则

- 不要只抓“爆款”，还要抓“高回复争议内容”与“KOL 发布内容”。
- 先做一个快速轮次判断主题热度，再决定是否进入全量采集。
- 输出里必须保留原帖引用线索，方便回溯。
