---
description: Git工作流规范，用于版本控制和发布
triggers:
  - keywords: [git, commit, push, 提交, 发布, deploy]
---

# Git 工作流技能

## 提交规范

### 提交信息格式

```
<type>: <subject>

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Type 类型

- `Add` - 新增文章或功能
- `Update` - 更新现有内容
- `Fix` - 修复问题
- `Refactor` - 重构代码/结构
- `Style` - 样式调整
- `Docs` - 文档更新

### 示例

```bash
# 新增文章
git commit -m "Add Claude Code hooks tutorial"

# 更新内容
git commit -m "Update navigation links on homepage"

# 修复问题
git commit -m "Fix broken link in article index"
```

## 工作流程

### 1. 查看状态
```bash
git status
git diff
```

### 2. 暂存更改
```bash
# 暂存特定文件
git add articles/new-article.html

# 暂存所有更改（谨慎使用）
git add .
```

### 3. 提交
```bash
git commit -m "$(cat <<'EOF'
Add new article about topic

Detailed description if needed.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### 4. 推送
```bash
git push
```

## 注意事项

- 不要提交 `Docs/` 目录（源文档）
- 检查 `.gitignore` 确保敏感文件被忽略
- 推送前确认所有链接正确
- GitHub Pages 会自动部署 `Main` 分支
