---
description: SEO优化技能，提升网站搜索引擎可见性
triggers:
  - keywords: [seo, 搜索, search, 优化, optimize, meta]
---

# SEO 优化技能

## 基础 Meta 标签

每个页面应包含：

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="页面描述，150字符以内">
    <meta name="keywords" content="关键词1, 关键词2, 关键词3">
    <meta name="author" content="陈栢成">
    <title>页面标题 - 陈栢成</title>

    <!-- Open Graph -->
    <meta property="og:title" content="页面标题">
    <meta property="og:description" content="页面描述">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://bayzhen.github.io/path">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="页面标题">
    <meta name="twitter:description" content="页面描述">
</head>
```

## 结构化数据

文章页可添加 JSON-LD：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "文章标题",
  "author": {
    "@type": "Person",
    "name": "陈栢成"
  },
  "datePublished": "2026-01-01",
  "description": "文章描述"
}
</script>
```

## URL 规范

- 使用小写字母和连字符
- 避免特殊字符和中文
- 保持简短有意义
- 示例：`/articles/claude-code/01-getting-started.html`

## 图片优化

- 添加 `alt` 属性描述图片内容
- 使用描述性文件名
- 考虑添加 `loading="lazy"` 延迟加载

## 内部链接

- 使用绝对路径 `/articles/...`
- 相关文章相互链接
- 系列文章包含上下篇导航
