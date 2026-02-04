---
description: HTML文章编写规范，用于创建符合本站风格的技术文章
triggers:
  - keywords: [文章, article, 写, write, 创建, create, 新建]
  - paths: ["articles/**/*.html"]
---

# HTML 文章编写技能

## 文章页模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章标题 - 陈栢成</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.8; color: #333; background-color: #f5f5f5; }
        nav { background: #2c3e50; padding: 15px 0; position: sticky; top: 0; z-index: 100; }
        nav ul { max-width: 900px; margin: 0 auto; padding: 0 20px; list-style: none; display: flex; gap: 30px; }
        nav a { color: #ecf0f1; text-decoration: none; font-weight: 500; }
        nav a:hover { color: #3498db; }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        .breadcrumb { margin-bottom: 20px; font-size: 0.9em; }
        .breadcrumb a { color: #3498db; text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        .breadcrumb span { color: #95a5a6; }
        article { background: #fff; padding: 50px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        article h1 { font-size: 2em; color: #2c3e50; margin-bottom: 15px; }
        .article-meta { color: #95a5a6; font-size: 0.9em; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #ecf0f1; }
        .tag { display: inline-block; background: #ecf0f1; color: #7f8c8d; padding: 2px 8px; border-radius: 3px; font-size: 0.85em; margin-right: 5px; }
        article h2 { font-size: 1.4em; color: #2c3e50; margin: 35px 0 15px; padding-bottom: 8px; border-bottom: 1px solid #ecf0f1; }
        article h3 { font-size: 1.15em; color: #34495e; margin: 25px 0 10px; }
        article p { margin-bottom: 15px; }
        article ul, article ol { margin: 15px 0 15px 25px; }
        article li { margin-bottom: 8px; }
        article code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 0.9em; }
        article pre { background: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 8px; overflow-x: auto; margin: 20px 0; font-size: 0.85em; line-height: 1.5; }
        article pre code { background: none; padding: 0; color: inherit; }
        article a { color: #3498db; text-decoration: none; }
        article a:hover { text-decoration: underline; }
        .nav-links { display: flex; justify-content: space-between; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ecf0f1; }
        .nav-links a { color: #3498db; text-decoration: none; }
        .nav-links a:hover { text-decoration: underline; }
        @media (max-width: 600px) { article { padding: 30px 20px; } article h1 { font-size: 1.6em; } }
    </style>
</head>
<body>
    <nav><ul><li><a href="/">首页</a></li><li><a href="/resume.html">简历</a></li><li><a href="/articles/">文章</a></li></ul></nav>
    <div class="container">
        <div class="breadcrumb">
            <a href="/articles/">文章</a> <span>/</span>
            <a href="/articles/系列名/">系列标题</a> <span>/</span>
            文章标题
        </div>
        <article>
            <h1>文章标题</h1>
            <div class="article-meta">
                <span class="tag">标签1</span>
                <span class="tag">标签2</span>
            </div>

            <h2>1. 章节标题</h2>
            <p>正文内容...</p>

            <div class="nav-links">
                <a href="上一篇.html">← 上一篇: 标题</a>
                <a href="下一篇.html">下一篇: 标题 →</a>
            </div>
        </article>
    </div>
</body>
</html>
```

## 系列索引页模板

索引页用于展示系列文章列表，参考 `articles/claude-code/index.html` 的结构。

## 注意事项

1. **内联样式**：本站不使用外部 CSS，所有样式内联在 `<style>` 标签中
2. **响应式**：包含 `@media (max-width: 600px)` 移动端适配
3. **导航链接**：系列文章需要包含上一篇/下一篇导航
4. **面包屑**：清晰展示当前位置层级
5. **代码块**：使用深色背景 `#2c3e50`
