---
name: git-workflow
description: Git 工作流专家。规范化版本控制，确保提交历史清晰可追溯。支持 Conventional Commits 规范、Pull Request 最佳实践、分支管理策略和自动化工作流。
metadata:
  short-description: Git 工作流与版本控制
  keywords:
    - git-workflow
    - Git
    - 版本控制
    - Conventional Commits
    - Pull Request
    - 分支管理
    - 提交规范
  category: 版本控制
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Git Workflow - Git 工作流专家

## 核心理念

**良好的 Git 实践** 是团队协作的基础：

```
┌─────────────────────────────────────────────────────────┐
│  规范提交 → 清晰历史 → 易于回溯 → 高效协作              │
└─────────────────────────────────────────────────────────┘
```

**核心原则**：
- ✅ **提交历史即文档**
- ✅ **原子提交，单一职责**
- ✅ **清晰的可追溯性**
- ✅ **易于 Code Review**

---

## 何时使用本技能

在以下场景时激活：

- 需要 Git 提交（commit）
- 创建 Pull Request / Merge Request
- 代码分支管理
- 版本发布
- 提到"git"、"提交"、"分支"、"PR"

---

## Conventional Commits 规范

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth2 login` |
| `fix` | Bug 修复 | `fix(api): resolve timeout issue` |
| `docs` | 文档变更 | `docs(readme): update installation` |
| `style` | 代码格式 | `style(lint): fix indentation` |
| `refactor` | 重构 | `refactor(utils): extract validator` |
| `perf` | 性能优化 | `perf(db): add query index` |
| `test` | 测试相关 | `test(user): add login tests` |
| `chore` | 构建/工具 | `chore(deps): upgrade to v2.0` |
| `revert` | 回滚提交 | `revert: feat(auth)` |

### 提交示例

```bash
# 简单提交
feat(auth): add JWT token validation

# 完整提交
feat(payment): integrate Stripe payment gateway

Implement credit card payment processing using Stripe API.
Add webhook handling for payment status updates.

- Add Stripe client initialization
- Implement payment intent creation
- Add webhook endpoint for status updates
- Handle payment success/failure scenarios

Closes #123
Related #456
```

---

## 提交最佳实践

### 1. 原子提交原则

```bash
# ❌ 不好的做法：一次提交多个变更
git commit -m "feat: add user feature and fix bugs and update docs"

# ✅ 好的做法：每个提交一个职责
git commit -m "feat(user): add registration"
git commit -m "fix(auth): resolve session timeout"
git commit -m "docs(readme): update examples"
```

### 2. 提交大小控制

| 类型 | 行数变化 | 建议 |
|------|----------|------|
| **小型** | < 100 行 | ✅ 理想 |
| **中型** | 100-400 行 | ⚠️ 可接受 |
| **大型** | > 400 行 | ❌ 应拆分 |

### 3. 提交信息质量

```bash
# ❌ 不好的提交信息
git commit -m "update"
git commit -m "fix bug"
git commit -m "wip"

# ✅ 好的提交信息
git commit -m "fix(auth): resolve JWT validation error"
git commit -m "feat(api): add rate limiting middleware"
git commit -m "docs(guide): explain authentication flow"
```

---

## 分支管理策略

### 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| **功能** | `feature/*` | `feature/user-auth` |
| **修复** | `bugfix/*` | `bugfix/login-timeout` |
| **热修复** | `hotfix/*` | `hotfix/security-patch` |
| **发布** | `release/*` | `release/v1.2.0` |
| **实验** | `experiment/*` | `experiment/new-ui` |

### 分支工作流

```
main (生产)
  ↑
  ├── release/v1.2.0 (发布准备)
  │     ↑
  │     ├── feature/user-auth (功能开发)
  │     ├── feature/payment-api (功能开发)
  │     └── bugfix/login-issue (Bug 修复)
  │
  └── hotfix/security-patch (紧急修复)
```

### 分支最佳实践

```bash
# 1. 从 main 创建功能分支
git checkout main
git pull origin main
git checkout -b feature/user-auth

# 2. 开发并提交
git add .
git commit -m "feat(auth): add login endpoint"

# 3. 同步上游变更
git fetch origin main
git rebase origin/main

# 4. 推送到远程
git push origin feature/user-auth

# 5. 创建 Pull Request
# (通过 GitHub/GitLab 界面)
```

---

## Pull Request 最佳实践

### PR 标题格式

与 Conventional Commits 保持一致：

```markdown
feat(auth): add OAuth2 login support

fix(api): resolve timeout issue

docs(readme): update installation guide
```

### PR 描述模板

```markdown
## 📝 变更类型
- [x] ✨ feat 新功能
- [ ] 🐛 fix Bug修复
- [ ] ♻️  refactor 重构
- [ ] 📚 docs 文档
- [ ] 💄 style 代码格式
- [ ] ⚡ perf 性能优化
- [ ] ✅ test 测试
- [ ] 🔧 chore 构建/工具

## 🎯 变更说明
<!-- 简要描述这个 PR 的目的和实现方式 -->

这个 PR 实现了用户认证功能，包括：
- JWT token 生成和验证
- 登录/登出端点
- 中间件保护路由

## 🔄 变更内容
<!-- 列出主要的文件变更 -->

- `src/auth/login.py` - 登录逻辑
- `src/auth/middleware.py` - 认证中间件
- `tests/test_auth.py` - 测试用例

## 🧪 测试
<!-- 描述测试情况 -->

- [x] 添加了单元测试
- [x] 添加了集成测试
- [x] 手动测试通过
- [ ] 性能测试通过

## ✅ 检查清单
<!-- 完成前确认 -->

- [x] 代码符合团队规范
- [x] 自我审查完成
- [x] 注释充分且准确
- [x] 文档已更新
- [x] 测试覆盖充分
- [x] 无合并冲突

## 📸 截图/演示
<!-- 如果适用，添加截图或 GIF -->

![登录界面](screenshots/login.png)

## 🔗 相关链接
- Closes #123
- Related #456
- Depends on #789

## ⚠️ 注意事项
<!-- 审查者需要注意的事项 -->

需要特别注意 JWT secret 的配置，已在 .env.example 中说明。
```

### PR 审查响应

```markdown
## 审查反馈

### 需要修改
- [ ] 安全问题：SQL 注入风险 (user_service.py:45)
- [ ] 性能问题：N+1 查询 (api.py:78)

### 建议改进
- [ ] 命名：`d()` → `double_value()` (utils.py:12)
- [ ] 注释：补充复杂逻辑说明 (payment.py:34)

### LGTM with suggestions
- [ ] 可以合并，但建议后续优化
```

---

## Git Hooks 自动化

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 运行 linter
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ Lint failed, please fix before committing"
    exit 1
fi

# 运行测试
npm test
if [ $? -ne 0 ]; then
    echo "❌ Tests failed, please fix before committing"
    exit 1
fi

echo "✅ Pre-commit checks passed"
```

### Commit Message Hook

```bash
#!/bin/bash
# .git/hooks/commit-msg

# 验证提交信息格式
commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore|revert)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format"
    echo "✅ Expected format: <type>(<scope>): <subject>"
    exit 1
fi

echo "✅ Commit message format valid"
```

---

## 常见操作

### 修改最后一次提交

```bash
# 添加遗漏的文件
git add forgotten_file.py

# 修改提交信息
git commit --amend

# 修改提交内容但不改信息
git commit --amend --no-edit
```

### 撤销提交

```bash
# 撤销最后一次提交（保留变更）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃变更）
git reset --hard HEAD~1

# 撤销多次提交
git reset --soft HEAD~3
```

### 交互式变基

```bash
# 变基最近 3 个提交
git rebase -i HEAD~3

# 命令：
# pick  - 保留提交
# reword - 修改提交信息
# edit - 编辑提交
# squash - 合并到前一个提交
# drop - 删除提交
```

### 解决合并冲突

```bash
# 1. 开始变基
git rebase origin/main

# 2. 遇到冲突时
git status  # 查看冲突文件

# 3. 手动解决冲突
# 编辑冲突文件，删除 <<<<<<< ======= >>>>>>> 标记

# 4. 标记冲突已解决
git add <resolved-files>

# 5. 继续变基
git rebase --continue

# 6. 如果需要放弃
git rebase --abort
```

---

## 验证清单

提交或 PR 前，检查：

- [ ] 提交信息符合 Conventional Commits 规范
- [ ] 每个提交职责单一
- [ ] 提交大小合理（< 400 行）
- [ ] 分支命名符合规范
- [ ] 无敏感信息泄露
- [ ] 关联 Issue/PR
- [ ] 代码已通过测试
- [ ] 文档已更新

---

## 相关参考

- [Git 工作流规范](../references/git-workflow.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
