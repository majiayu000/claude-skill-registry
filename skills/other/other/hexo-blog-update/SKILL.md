---
name: hexo-blog-update
description: Standardized workflow for creating and publishing Hexo blog posts with local preview and deployment.
version: 1.0
---

# Hexo 博客更新 Skill

Standardized workflow for creating, editing, and publishing Hexo blog posts.

## When to Use

Use this skill when you need to:
- Create a new blog post
- Edit existing blog posts
- Preview blog locally before publishing
- Deploy blog to production

## Prerequisites

- Node.js installed (>= 14)
- Hexo CLI installed globally (`npm install -g hexo-cli`)
- Blog repository cloned locally
- Git configured with SSH key for deployment

## Workflow

### Step 1: Create New Post

```bash
# Navigate to blog directory
cd /path/to/blog

# Create new post
hexo new post "文章标题"

# Or use npm script
npm run new "文章标题"
```

Post will be created at: `source/_posts/文章标题.md`

### Step 2: Edit Post Content

Edit the generated markdown file with the following structure:

```markdown
---
title: 文章标题
date: YYYY-MM-DD HH:MM:SS
categories:
- 分类1
- 分类2
tags:
- 标签1
- 标签2
---

文章摘要内容，会显示在首页列表中...

<!--more-->

## 正文标题

正文内容...

## 另一个标题

更多内容...
```

**Important Rules**:
- ✅ Use `<!--more-->` to separate excerpt from full content
- ✅ Set proper categories and tags
- ✅ Use Chinese for Chinese blogs
- ✅ Keep front matter (YAML between ---) at the top

### Step 3: Local Preview

```bash
# Start local server
hexo server

# Or with npm
npm run server
```

Access at: http://localhost:4000

**Preview Checklist**:
- [ ] Post appears in list with correct title
- [ ] Excerpt shows correctly (before `<!--more-->`)
- [ ] Full content displays properly
- [ ] Categories and tags are correct
- [ ] No formatting errors

### Step 4: Deploy to Production

```bash
# Deploy (clean + generate + deploy)
npm run release-blog

# Or manually
hexo clean && hexo generate && hexo deploy
```

**Deployment Output**:
```
INFO  Deploy done: git
To github.com:username/username.github.io.git
   xxx...xxx  HEAD -> master
```

## Standard Post Template

```markdown
---
title: 文章标题
date: 2026-02-11 17:20:00
categories:
- 分类1
- 分类2
tags:
- 标签1
- 标签2
- 标签3
---

文章摘要，显示在首页列表中。简要介绍文章内容和价值。

<!--more-->

## 前言

详细介绍背景...

## 主要内容

### 小节1

内容...

### 小节2

内容...

## 总结

总结要点...

---

*相关链接*:
- [链接描述](url)
```

## Common Commands Reference

| Command | Description |
|---------|-------------|
| `hexo new post "标题"` | Create new post |
| `hexo new draft "标题"` | Create draft post |
| `hexo publish draft "标题"` | Publish draft |
| `hexo server` | Start local server |
| `hexo clean` | Clean cache and generated files |
| `hexo generate` | Generate static files |
| `hexo deploy` | Deploy to remote |
| `npm run release-blog` | Full deploy pipeline |

## File Structure

```
blog/
├── source/
│   └── _posts/
│       └── 文章标题.md      # Post files
├── themes/                    # Theme directory
├── _config.yml               # Site config
├── package.json              # Scripts & dependencies
└── public/                   # Generated output (auto)
```

## Best Practices

### Do's
✅ Always preview before deploying
✅ Use meaningful categories and tags
✅ Include `<!--more-->` for proper excerpt
✅ Check date format (YYYY-MM-DD HH:MM:SS)
✅ Verify deployment success message

### Don'ts
❌ Don't modify public/ directory directly
❌ Don't forget to set categories/tags
❌ Don't skip local preview
❌ Don't use special characters in filenames

## Troubleshooting

### Post not showing in list
- Check if file is in `source/_posts/`
- Verify front matter format
- Run `hexo clean` and regenerate

### Deployment fails
- Check SSH key configuration
- Verify git remote is correct
- Ensure network connectivity

### Formatting issues
- Use standard Markdown syntax
- Verify YAML front matter syntax
- Check theme compatibility

## Example Session

**User**: Create a new blog post about AI tools

**Agent**:
```
Step 1: Create post
$ hexo new post "推荐的 AI 开发工具"
INFO  Created: source/_posts/推荐的-AI-开发工具.md

Step 2: Edit content
[Edit file with proper structure and <!--more-->]

Step 3: Preview
$ hexo server
INFO  Hexo is running at http://localhost:4000/
[Verify post displays correctly]

Step 4: Deploy
$ npm run release-blog
INFO  Deploy done: git
```

## Version History

- v1.0 (2026-02-11) - Initial release
  - Standard 4-step workflow
  - Chinese blog format support
  - Common commands reference
