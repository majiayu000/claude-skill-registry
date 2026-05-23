---
name: release-automation
description: 发布自动化工具，全自动发布流程、CHANGELOG更新、Git标签管理
---

# 发布自动化

## 何时使用

当你需要：发布新版本、更新CHANGELOG、创建Git标签、推送到远程

## 全自动发布（推荐）

命令:
  node scripts/commands/release/push.mjs --auto --version=1.0.11 --tag-message="版本描述"

或自动计算版本号（从package.json递增）:
  node scripts/commands/release/push.mjs --auto

或交互式模式:
  pnpm release:push

## 发布流程

自动完成以下步骤:
1. 检查当前分支（建议在develop）
2. 检查工作区状态
3. 拉取最新代码
4. 更新package.json版本号
5. 创建release/v1.0.X分支
6. 推送release分支到远程
7. 合并到main分支
8. 创建Git标签
9. 自动更新CHANGELOG.md
10. 合并回develop分支
11. 推送所有更改（main、develop、tag）
12. 清理release分支

## 版本号规范

语义化版本（Semantic Versioning）:
  - MAJOR.MINOR.PATCH
  - 1.0.10 → 1.0.11（补丁版本）
  - 1.0.11 → 1.1.0（次版本）
  - 1.1.0 → 2.0.0（主版本）

## CHANGELOG更新

自动生成:
  node scripts/commands/tools/update-changelog.mjs 1.0.11

预览（不修改文件）:
  pnpm changelog:preview

CHANGELOG会自动:
  - 从Git commit提取变更
  - 识别包标签（如feat(shared-core)）
  - 识别Breaking Changes
  - 按类型分类（新增、修复、重构等）

## Commit规范

使用Conventional Commits:
  - feat: 新功能
  - fix: 修复
  - refactor: 重构
  - docs: 文档
  - chore: 构建/工具
  - test: 测试
  - perf: 性能优化

示例:
  feat(admin-app): 添加用户管理模块
  fix(shared-core): 修复日志工具编码问题
  refactor(scripts): 完成scripts架构重构

## 命令行参数

--auto: 全自动模式，跳过所有交互
--version=X.Y.Z: 指定版本号
--tag-message="描述": 指定标签消息
--skip-pull: 跳过拉取代码
--skip-merge-to-main: 跳过合并到main
--skip-merge-back: 跳过合并回develop
--skip-cleanup: 跳过清理release分支

## 注意事项

1. 在develop分支运行
2. 确保工作区干净（或使用--auto自动处理）
3. 版本号必须递增
4. 标签消息会显示在CHANGELOG中

## 常见问题

Q: 如何发布hotfix?
A: 在main分支创建hotfix分支，修复后发布

Q: 版本号写错了怎么办?
A: 删除标签重新发布:
   git tag -d v1.0.11
   git push origin --delete v1.0.11

Q: CHANGELOG没更新?
A: 手动运行: node scripts/commands/tools/update-changelog.mjs 1.0.11
