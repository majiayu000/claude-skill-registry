---
name: git
description: "Git version control best practices: branching, commits, merging, conflict resolution, PR workflows. Use when managing branches, creating commits, merging code, or resolving conflicts."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Git 工作流技能

本技能提供 Git 版本控制的最佳实践。

## 快速参考

- **核心职责**: 提供 Git 版本控制的分支策略、提交规范、合并流程和冲突解决最佳实践
- **推荐分支模型**: GitHub Flow（main + feature 分支 + PR）
- **提交规范**: Conventional Commits（`<type>(<scope>): <subject>`）
- **合并策略**: 功能分支用 Squash Merge，同步主分支用 Rebase，长期分支用 Merge
- **子文件引用**:
  - [commands-reference.md](commands-reference.md) — 常用 Git 命令参考
  - [pr-workflow.md](pr-workflow.md) — Pull Request 流程
  - [hooks-guide.md](hooks-guide.md) — Git Hooks 指南
  - [delegation.md](delegation.md) — 委派到专业 Agent

<!-- 详细内容 -->

## 目录

- [触发条件](#触发条件)
- [Workflow | 工作流程](#workflow--工作流程)
- [分支策略](#分支策略)
- [提交规范 (Conventional Commits)](#提交规范-conventional-commits)
- [常用命令](#常用命令)
- [合并策略](#合并策略)
- [冲突解决](#冲突解决)
- [Pull Request 流程](#pull-request-流程)
- [Git Hooks](#git-hooks)
- [.gitignore 最佳实践](#gitignore-最佳实践)
- [最佳实践](#最佳实践)
- [快速场景指南 | Quick Scenarios](#快速场景指南--quick-scenarios)
- [委派到专业 Agent | Delegation to Agents](#委派到专业-agent--delegation-to-agents)

## 触发条件

当用户提及以下关键词时自动激活：`git`, `commit`, `branch`, `merge`, `rebase`, `cherry-pick`, `PR`, `pull request`, `conflict`, `stash`, `gitflow`, `conventional commits`

常见场景：

- 管理 Git 分支
- 创建提交
- 处理合并
- 解决冲突
- 代码审查

## Workflow | 工作流程

### 1. 检查当前状态

```bash
git status
git branch -a
git log --oneline -5
```

根据状态确定下一步操作。

### 2. 选择操作类型

| 场景         | 执行流程                                    |
| ------------ | ------------------------------------------- |
| 创建功能分支 | `git checkout -b feature/xxx` → 开发 → 提交 |
| 提交代码     | `git add` → `git commit` → 验证             |
| 合并代码     | `git checkout main` → `git merge` → 推送    |
| 解决冲突     | 查看冲突 → 手动解决 → 标记解决 → 继续       |
| 创建 PR      | 推送分支 → `gh pr create` → 等待审查        |

### 3. 执行并验证

- 执行命令前确认当前分支和状态
- 执行后验证结果：`git status`, `git log --oneline -3`
- 确保无未提交的修改或冲突

### 4. 完成确认

```
✅ Git 操作完成！

📊 当前状态:
   分支: [当前分支名]
   最新提交: [commit message]

⚠️ 提醒:
   - 功能完成后记得创建 PR
   - 合并前确保通过所有测试
   - 定期从 main 分支同步更新
```

## 分支策略

### Git Flow

```
main (生产)
  │
  └── develop (开发)
        │
        ├── feature/xxx (功能分支)
        ├── release/x.x (发布分支)
        └── hotfix/xxx (热修复)
```

### GitHub Flow（推荐）

```
main (始终可部署)
  │
  └── feature/xxx (功能分支)
        │
        └── PR → Code Review → Merge
```

### 分支命名规范

```bash
# 功能分支
feature/add-user-auth
feature/JIRA-123-payment-integration

# Bug 修复
fix/login-validation
bugfix/JIRA-456-cart-total

# 热修复
hotfix/security-patch

# 发布
release/v1.2.0

# 重构
refactor/database-layer
```

## 提交规范 (Conventional Commits)

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型

| 类型     | 说明      | 示例                         |
| -------- | --------- | ---------------------------- |
| feat     | 新功能    | feat(auth): 添加 OAuth 登录  |
| fix      | Bug 修复  | fix(cart): 修复价格计算错误  |
| docs     | 文档更新  | docs(readme): 更新安装说明   |
| style    | 格式调整  | style: 格式化代码            |
| refactor | 重构      | refactor(api): 重构用户服务  |
| perf     | 性能优化  | perf(query): 优化搜索查询    |
| test     | 测试      | test(user): 添加用户注册测试 |
| chore    | 构建/工具 | chore(deps): 更新依赖        |
| ci       | CI 配置   | ci: 添加 GitHub Actions      |

### 示例

```bash
# 简单提交
git commit -m "feat(user): 添加用户头像上传功能"

# 带详情的提交
git commit -m "fix(payment): 修复支付金额精度问题

- 使用 Decimal 替代 float 处理金额
- 添加金额格式化工具函数
- 更新相关测试用例

Closes #123"

# 破坏性变更
git commit -m "feat(api)!: 重构 API 响应格式

BREAKING CHANGE: API 响应格式从 {data} 改为 {success, data, error}"
```

## 常用命令

> 详细内容参见 [commands-reference.md](commands-reference.md)

## 合并策略

### Merge（合并提交）

```bash
# 创建合并提交
git checkout main
git merge feature/xxx

# 优点：保留完整历史
# 缺点：历史线复杂
```

### Rebase（变基）

```bash
# 变基到 main
git checkout feature/xxx
git rebase main

# 优点：线性历史
# 缺点：改写历史，需要强制推送
```

### Squash Merge（压缩合并）

```bash
# 压缩为单个提交
git checkout main
git merge --squash feature/xxx
git commit -m "feat: 完成用户功能"

# 优点：干净的主分支历史
# 缺点：丢失详细提交记录
```

### 选择策略

| 场景            | 推荐策略     |
| --------------- | ------------ |
| 功能分支 → main | Squash Merge |
| main → 功能分支 | Rebase       |
| 长期分支同步    | Merge        |
| 发布分支        | Merge        |

## 冲突解决

### 解决步骤

```bash
# 1. 拉取最新代码
git fetch origin

# 2. 合并/变基
git rebase origin/main
# 遇到冲突

# 3. 查看冲突文件
git status

# 4. 编辑冲突文件
# 手动解决 <<<<<<< ======= >>>>>>> 标记

# 5. 标记已解决
git add resolved-file.ts

# 6. 继续变基
git rebase --continue

# 或放弃变基
git rebase --abort
```

### 冲突标记

```
<<<<<<< HEAD
当前分支的代码
=======
合并分支的代码
>>>>>>> feature/xxx
```

### VS Code 冲突解决

- Accept Current Change (保留当前)
- Accept Incoming Change (保留传入)
- Accept Both Changes (保留两者)
- Compare Changes (比较差异)

## Pull Request 流程

> 详细内容参见 [pr-workflow.md](pr-workflow.md)

## Git Hooks

> 详细内容参见 [hooks-guide.md](hooks-guide.md)

## .gitignore 最佳实践

```gitignore
# 依赖
node_modules/
venv/
__pycache__/

# 构建输出
dist/
build/
*.egg-info/

# 环境变量
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# 日志
*.log
logs/

# 测试覆盖率
coverage/
.coverage

# 缓存
.cache/
.pytest_cache/
```

## 最佳实践

1. **小而频繁的提交** - 每个提交做一件事
2. **有意义的提交信息** - 说明为什么，不只是什么
3. **保持分支更新** - 经常从主分支同步
4. **PR 前自检** - lint、test、review
5. **不要提交敏感信息** - 使用环境变量
6. **使用 .gitignore** - 忽略不需要的文件
7. **定期清理分支** - 合并后删除
8. **备份重要操作** - 变基前创建备份分支
9. **团队约定** - 统一的分支和提交规范
10. **利用 Git Hooks** - 自动化检查

## 快速场景指南 | Quick Scenarios

### 日常开发

```bash
# 开始新功能
git checkout main && git pull
git checkout -b feature/my-feature

# 提交工作
git add -A && git commit -m "feat: add new feature"

# 推送并创建 PR
git push -u origin feature/my-feature
gh pr create --fill
```

### 紧急修复

```bash
# 从 main 创建热修复分支
git checkout main && git pull
git checkout -b hotfix/critical-fix

# 修复并提交
git add -A && git commit -m "fix: critical bug"

# 快速合并
git checkout main && git merge hotfix/critical-fix
git push origin main
```

### 冲突解决

```bash
# 更新分支遇到冲突
git fetch origin
git rebase origin/main
# 手动解决冲突文件
git add <resolved-files>
git rebase --continue
```

## 委派到专业 Agent | Delegation to Agents

> 详细内容参见 [delegation.md](delegation.md)

> **记住**: Git 是协作的基石——清晰的分支策略和提交规范让团队协作事半功倍。
