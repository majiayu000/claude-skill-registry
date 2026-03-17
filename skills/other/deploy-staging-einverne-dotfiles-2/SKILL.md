---
name: deploy-staging
description: 将当前分支部署到测试环境。当用户要求部署、发布到测试或在 staging 环境测试时使用
---

# 部署到测试环境

## 前置条件检查

执行部署前，必须验证：

1. 当前分支所有变更已提交
   - 运行 `git status` 检查
   - 如有未提交内容，提示用户先提交

2. 所有测试通过
   - 运行 `npm test`
   - 如测试失败，停止部署并报告失败原因

3. 代码已推送到远程仓库
   - 运行 `git push`
   - 确保远程分支是最新状态

## 部署流程

1. 构建生产版本
   ```bash
   npm run build:staging
   ```

2. 运行部署脚本
   ```bash
   ./scripts/deploy-staging.sh
   ```

3. 等待部署完成
   - 显示部署进度
   - 捕获并显示错误信息

4. 验证部署
   ```bash
   curl -f https://staging.example.com/health
   ```

5. 报告部署结果
   - 成功：提供访问链接
   - 失败：显示错误日志和回滚建议

## 错误处理

如果部署失败：
1. 保存错误日志到 `.logs/deploy-staging-{timestamp}.log`
2. 建议用户检查日志
3. 提供回滚命令：`./scripts/rollback-staging.sh`

## 部署后检查

部署成功后，提醒用户验证：
- 关键功能是否正常
- 数据库迁移是否成功
- 静态资源是否加载正常
