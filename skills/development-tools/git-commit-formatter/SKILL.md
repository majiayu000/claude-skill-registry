---
name: git-commit-formatter
description: 生成符合 Conventional Commits 规范的 Git 提交信息。当用户要求生成提交、创建 commit 或写提交信息时使用
---

# Git 提交信息格式化器

## 任务说明

分析暂存区的代码变更，生成符合 Conventional Commits 规范的提交信息。

## 规范说明

提交信息格式：`<type>(<scope>): <subject>`

类型定义：
- feat: 新功能
- fix: 修复缺陷
- docs: 文档更新
- style: 代码格式调整（不影响逻辑）
- refactor: 重构代码
- perf: 性能优化
- test: 测试相关
- build: 构建系统或依赖更新
- ci: CI 配置更新
- chore: 其他不修改源代码的更改

## 执行步骤

1. 运行 `git diff --cached` 查看暂存的变更
2. 分析文件变更，识别主要修改类型
3. 确定影响范围（scope）
4. 生成简洁的主题（subject），限制在 50 字符内
5. 如有重大变更，添加 BREAKING CHANGE 说明

## 质量标准

必须遵守：
- subject 使用动词开头，现在时态
- subject 不以句号结尾
- scope 用括号包裹，可选但建议提供
- 如有详细说明，body 每行不超过 72 字符

## 示例输出

```
feat(auth): 实现 JWT 令牌认证

- 添加 JWT 生成和验证逻辑
- 实现令牌刷新机制
- 添加相关单元测试
```
