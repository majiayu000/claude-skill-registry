---
name: taiwan-job-platform-scraper
description: 当需要抓取台湾求职平台的职位列表、跨站汇总 104、CakeResume、Yourator 的岗位信息，或按关键词和地点整理职位样本时使用。适用于“搜前端工程师职位”“整理台湾招聘市场样本”“对比多个求职平台结果”等场景。
---

<!-- AUTO-GENERATED-RESOURCE-MAP:START -->

### Resource Map

> 基准路径: `.claude/skills/scraping-specialist/references/domains/job-platforms/`

```
job-platforms/
├── references/
│   └── platforms-and-output.md
└── SKILL.md
```

<!-- AUTO-GENERATED-RESOURCE-MAP:END -->

# 台湾求职平台职位采集

此技能用于跨多个台湾求职平台抓取职位列表，并将结果整理成统一结构。

## 支持平台

- 104 人力银行
- CakeResume
- Yourator

平台 URL 与结果结构建议见 [平台与输出说明](references/platforms-and-output.md)。

## 输入要求

开始前提取：

- 关键词
- 平台范围，默认全部
- 地点，可选
- 薪资要求，可选

## 执行流程

1. 针对每个平台构造搜索 URL。
2. 使用浏览器工具逐个平台抓取第一页职位列表。
3. 提取统一字段。
4. 保存为 `data/jobs-YYYY-MM-DD.json`。
5. 以 Markdown 汇总给用户。

## 统一字段

- `title`
- `company`
- `location`
- `salary`
- `url`
- `source`

## 注意事项

- 逐个平台顺序采集，避免同时开启多个复杂浏览器任务。
- 默认先抓第一页样本。
- 如果用户明确需要翻页，再扩展分页。
