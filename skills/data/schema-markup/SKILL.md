---
name: schema-markup
description: "添加、修复或优化站点上的 schema 与结构化数据时使用。触发词：schema markup、structured data、JSON-LD、rich snippets、schema.org、FAQ schema、product schema、breadcrumb schema。整体 SEO 见 seo-audit。"
license: MIT
---

# Schema 与结构化数据

实现 schema.org 标记，帮助搜索引擎理解内容并争取富结果。

## 前置了解

页面类型与主内容、可能的富结果；现有 schema 与报错；目标富结果与业务价值。

## 原则

1. **准确优先**：schema 如实反映页面内容，不标记不存在的内容，内容变更时同步更新。  
2. **用 JSON-LD**：放入 `<head>` 或 `</body>` 前，便于维护。  
3. **遵循 Google 指南**：仅用其支持的标记，避免 spam，满足富结果资格。  
4. **全部校验**：上线前测试，用 Search Console 监控，及时修错。

## 常见类型与必填项

| 类型 | 用途 | 必填 |
|------|------|------|
| **Organization** | 品牌/关于页 | name, url；建议 logo, sameAs, contactPoint |
| **WebSite** + SearchAction | 首页、站内搜索框 | name, url；搜索框用 potentialAction |
| **Article/BlogPosting** | 博客、新闻 | headline, image, datePublished, author |
| **Product** | 产品页 | name, image, offers（含 price、availability） |
| **SoftwareApplication** | SaaS/应用页 | name, offers 或免费标识 |
| **FAQPage** | FAQ 页 | mainEntity（Question/Answer 数组） |
| **HowTo** | 教程 | name, step 数组 |
| **BreadcrumbList** | 面包屑 | itemListElement（ListItem + position, name, item） |
| **LocalBusiness** | 本地商户 | name, address 等 |
| **Event** | 活动/会议 | name, startDate, location 或 eventAttendanceMode |

Review/AggregateRating 仅用于真实用户评价，不得自评。

## 同页多类型

用 `@graph` 组合多种 schema，通过 `@id` 相互引用（如 Organization → WebSite → BreadcrumbList）。

## 校验与工具

- [Google Rich Results Test](https://search.google.com/test/rich-results)  
- [validator.schema.org](https://validator.schema.org/)  
- Search Console 增强功能报告  

常见错误：缺必填属性、日期非 ISO 8601、URL 非完整、枚举值不符、与页面内容不一致。

## 实现方式

静态站：模板中直接插入 JSON-LD。  
动态站（React、Next 等）：服务端渲染组件输出 JSON-LD。  
CMS/WordPress：Yoast、Rank Math、Schema Pro 等插件或主题/自定义字段。

## 相关技能

seo-audit、programmatic-seo、analytics-tracking。
