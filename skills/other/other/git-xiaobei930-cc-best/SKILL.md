---
name: git
description: "Git version control best practices: branching, commits, merging, conflict resolution, PR workflows. Use when managing branches, creating commits, merging code, or resolving conflicts."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Git 工作流技能

本技能提供 Git 版本控制的最佳实践。

## 快速参考

- **推荐分支模型**: GitHub Flow（main + feature 分支 + PR）
- **提交规范**: Conventional Commits（`<type>(<scope>): <subject>`）
- **合并策略**: 功能分支 → Squash Merge，同步主分支 → Rebase，长期分支 → Merge

## 触发条件

`git`, `commit`, `branch`, `merge`, `rebase`, `PR`, `pull request`, `conflict`, `stash`

## 工作流程

1. 检查状态: `git status && git branch -a && git log --oneline -5`
2. 选择操作:

| 场景         | 执行流程                                                  |
| ------------ | --------------------------------------------------------- |
| 创建功能分支 | `git checkout -b feature/xxx` → 开发 → 提交               |
| 提交代码     | `git add` → `git commit` → 验证                           |
| 合并代码     | `git checkout main` → `git merge` → 推送                  |
| 解决冲突     | 查看冲突 → 手动解决 → `git add` → `git rebase --continue` |
| 创建 PR      | 推送分支 → `gh pr create` → 等待审查                      |

3. 执行后验证: `git status`, `git log --oneline -3`

## 分支命名规范

```
feature/add-user-auth     # 功能分支
fix/login-validation      # Bug 修复
hotfix/security-patch     # 热修复
release/v1.2.0            # 发布
refactor/database-layer   # 重构
```

## 提交类型

| 类型     | 说明      | 示例                        |
| -------- | --------- | --------------------------- |
| feat     | 新功能    | feat(auth): 添加 OAuth 登录 |
| fix      | Bug 修复  | fix(cart): 修复价格计算错误 |
| docs     | 文档更新  | docs(readme): 更新安装说明  |
| refactor | 重构      | refactor(api): 重构用户服务 |
| test     | 测试      | test(user): 添加注册测试    |
| chore    | 构建/工具 | chore(deps): 更新依赖       |
| perf     | 性能优化  | perf(query): 优化搜索查询   |

## 合并策略选择

| 场景            | 推荐策略     |
| --------------- | ------------ |
| 功能分支 → main | Squash Merge |
| main → 功能分支 | Rebase       |
| 长期分支同步    | Merge        |

## 最佳实践

1. 小而频繁的提交，每个做一件事
2. 有意义的提交信息，说明为什么
3. 经常从主分支同步
4. PR 前自检（lint、test、review）
5. 不提交敏感信息
6. 合并后删除功能分支

## 子文件索引

| 文件                                           | 内容              |
| ---------------------------------------------- | ----------------- |
| [commands-reference.md](commands-reference.md) | 常用 Git 命令参考 |
| [pr-workflow.md](pr-workflow.md)               | Pull Request 流程 |
| [hooks-guide.md](hooks-guide.md)               | Git Hooks 指南    |
| [delegation.md](delegation.md)                 | 委派到专业 Agent  |

---

> **记住**: Git 是协作的基石——清晰的分支策略和提交规范让团队协作事半功倍。
