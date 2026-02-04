---
name: github-commit-push
description: GitHub 代码提交与推送 - 完整的 git commit 和 push 工作流，包含远程仓库配置、冲突处理和 SSH 推送。
metadata:
  tags: git, github, commit, push, ssh, version-control
---

# GitHub Commit & Push

完整的 GitHub 代码提交与推送工作流。处理从本地提交到远程推送的完整流程，包括远程仓库配置、历史合并冲突解决和 SSH 推送。

## ✨ Features

- 🔗 **自动配置 Remote** - 自动添加 GitHub 远程仓库
- 📝 **规范提交信息** - 遵循 Conventional Commits 规范
- 🔀 **智能合并** - 自动处理 unrelated histories 冲突
- 🔐 **SSH 推送** - 使用 SSH 密钥安全推送
- 📊 **提交状态检查** - 查看变更文件和提交历史

## 前置要求

```bash
# 确保已安装 git
git --version

# 确保已配置 GitHub SSH 密钥
ls ~/.ssh/id_*.pub
# 如果没有，先生成 SSH key：
# ssh-keygen -t ed25519 -C "your_email@example.com"
```

## 快速开始

### 1. 检查当前状态

```bash
cd your-project
git status
git remote -v
```

### 2. 配置远程仓库（如果没有）

```bash
# 添加 GitHub 远程仓库（SSH 方式）
git remote add origin git@github.com:username/repo.git

# 或者使用 HTTPS（需要 token）
git remote add origin https://github.com/username/repo.git
```

### 3. 提交更改

```bash
# 查看变更
git diff --cached --stat

# 添加文件
git add <file>

# 提交（遵循 Conventional Commits）
git commit -m "type(scope): description

详细说明...

fixes #123"
```

### 4. 推送到远程

```bash
# 先获取远程更新
git fetch origin

# 检查是否有冲突
git log HEAD..origin/main --oneline

# 合并远程更改（如果有）
git pull origin main --allow-unrelated-histories --no-rebase

# 推送
git push origin main
```

## 完整工作流脚本

创建 `scripts/commit-and-push.sh`：

```bash
#!/bin/bash

# GitHub Commit & Push 脚本
# 用法: ./commit-and-push.sh "commit message" [branch]

set -e

COMMIT_MSG="${1:-Update files}"
BRANCH="${2:-main}"
REMOTE_URL="${3:-}"

echo "🚀 GitHub Commit & Push"
echo "======================"

# 1. 检查是否在 git 仓库
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 当前目录不是 git 仓库"
    exit 1
fi

# 2. 检查远程仓库
if ! git remote -v > /dev/null 2>&1; then
    if [ -z "$REMOTE_URL" ]; then
        echo "❌ 未配置远程仓库，请提供仓库 URL"
        echo "用法: $0 'commit msg' branch 'git@github.com:user/repo.git'"
        exit 1
    fi
    echo "🔗 添加远程仓库..."
    git remote add origin "$REMOTE_URL"
fi

echo "📍 当前分支: $(git branch --show-current)"
echo "🌐 远程仓库: $(git remote get-url origin)"

# 3. 检查是否有变更
if git diff --cached --quiet && git diff --quiet; then
    echo "⚠️  没有要提交的变更"
    exit 0
fi

# 4. 显示将要提交的文件
echo ""
echo "📁 变更文件:"
git status --short

# 5. 添加所有变更
echo ""
echo "➕ 添加文件..."
git add -A

# 6. 提交
echo ""
echo "💾 提交更改..."
git commit -m "$COMMIT_MSG"
echo "✅ 提交成功: $COMMIT_MSG"

# 7. 获取远程更新
echo ""
echo "📥 获取远程更新..."
git fetch origin

# 8. 检查是否需要合并
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse origin/$BRANCH 2>/dev/null || echo "null")

if [ "$REMOTE" != "null" ] && [ "$LOCAL" != "$REMOTE" ]; then
    echo "🔀 需要合并远程更改..."
    if git merge-base --is-ancestor origin/$BRANCH HEAD 2>/dev/null; then
        echo "⚡ 本地领先远程，直接推送"
    else
        echo "🔀 合并远程更改..."
        git pull origin $BRANCH --allow-unrelated-histories --no-rebase || {
            echo "❌ 合并冲突，请手动解决"
            exit 1
        }
    fi
fi

# 9. 推送
echo ""
echo "📤 推送到远程..."
git push origin $BRANCH
echo ""
echo "✅ 推送成功！"
echo "🔗 查看: $(git remote get-url origin | sed 's/\.git$//' | sed 's/git@github.com:/https:\/\/github.com\//')"
```

## 常用命令速查

### 提交规范

```bash
# feat: 新功能
git commit -m "feat(auth): add login with OAuth"

# fix: 修复
git commit -m "fix(api): handle null pointer exception"

# docs: 文档
git commit -m "docs(readme): update installation guide"

# refactor: 重构
git commit -m "refactor(utils): simplify date formatting"

# chore: 杂项
git commit -m "chore(deps): update dependencies"
```

### 处理常见问题

**问题 1：未配置 remote**
```bash
fatal: 'origin' does not appear to be a git repository

# 解决
git remote add origin git@github.com:username/repo.git
```

**问题 2：unrelated histories**
```bash
fatal: refusing to merge unrelated histories

# 解决
git pull origin main --allow-unrelated-histories --no-rebase
```

**问题 3：需要身份验证**
```bash
fatal: could not read Username for 'https://github.com'

# 解决 - 切换到 SSH
git remote set-url origin git@github.com:username/repo.git
```

**问题 4：权限拒绝**
```bash
Permission denied (publickey)

# 解决 - 检查 SSH key
ssh -T git@github.com
# 如果没有 key，生成并添加到 GitHub
ssh-keygen -t ed25519 -C "email@example.com"
cat ~/.ssh/id_ed25519.pub
# 然后复制到 GitHub Settings -> SSH Keys
```

## 最佳实践

1. **频繁提交**：小步快跑，每次提交完成一个逻辑单元
2. **写好提交信息**：遵循 Conventional Commits 规范
3. **先 pull 后 push**：避免覆盖他人更改
4. **使用 SSH**：比 HTTPS 更安全方便
5. **检查状态**：提交前使用 `git status` 和 `git diff` 检查

## 自动化脚本

创建 `.clawdhub/manifest.json`：

```json
{
  "id": "github-commit-push",
  "name": "GitHub Commit & Push",
  "version": "1.0.0",
  "description": "Complete git commit and push workflow for GitHub",
  "author": "xdrshjr",
  "tags": ["git", "github", "commit", "push"],
  "entry": "scripts/commit-and-push.sh"
}
```

## 使用示例

```bash
# 进入项目目录
cd ~/clawd

# 查看状态
git status

# 添加远程（如果没有）
git remote add origin git@github.com:xdrshjr/JR-Agent-Skills.git

# 添加文件
git add skills/remotion-synced-video/SKILL.md

# 提交
git commit -m "docs(remotion-synced-video): add audio sync best practices

- Add measure-audio.sh script for duration measurement
- Update index.tsx to use dynamic duration calculation
- Add troubleshooting for audio-visual sync issues"

# 获取远程更新并合并
git pull origin main --allow-unrelated-histories --no-rebase

# 推送
git push origin main
```

---

**Pro Tip**: 使用 SSH 方式配置 remote 可以避免每次推送都输入密码，推荐所有 GitHub 仓库都使用 SSH 方式。