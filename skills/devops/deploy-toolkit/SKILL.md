---
name: deploy-toolkit
description: 部署工具包，4种部署方式、环境配置、部署测试、CI/CD流程
---

# 部署工具包

## 何时使用

当你需要：部署应用、配置环境、触发CI/CD、检查部署状态

## 4种部署方式

方式1 - 本地部署:
  pnpm deploy:app --app=admin-app
  bash scripts/shell/utils/deploy-app-local.sh admin-app

方式2 - 静态资源部署:
  pnpm deploy:static:all
  pnpm deploy:static:app --app=system-app

方式3 - K8s部署:
  pnpm deploy:k8s:all
  pnpm deploy:k8s:app --app=admin-app
  bash scripts/shell/utils/deploy-incremental-k8s.sh

方式4 - BPS部署（一键部署所有）:
  pnpm bps:all
  bash scripts/shell/utils/bps-all.sh

## 构建+部署组合

一键构建部署:
  pnpm build-deploy:app --app=admin-app
  pnpm build-deploy:all

K8s构建部署:
  pnpm build-deploy:k8s:all
  pnpm build-deploy:k8s:app --app=admin-app

静态资源构建部署:
  pnpm build-deploy:static:all
  pnpm build-deploy:static:app --app=system-app

## 部署环境

测试环境:
  - 域名: *.bellis.com.cn
  - 配置: docker/test/*.conf

生产环境:
  - 域名: *.bellis.com.cn
  - 配置: docker/prod/*.conf

## 部署测试

运行部署测试:
  pnpm test:deployment:all
  pnpm test:deployment:app --app=admin-app
  node scripts/commands/test/deployment-test.mjs

## CI/CD流程

GitHub Actions:
  - .github/workflows/deploy-*.yml
  - 自动触发: 推送到main/develop
  - 手动触发: workflow_dispatch

Jenkins:
  - jenkins/ 目录包含配置
  - 触发: 推送到指定分支

## 部署配置

应用部署配置:
  scripts/config/deploy.config.js

OSS配置（CDN部署需要）:
  环境变量:
    ALI_OSS_REGION
    ALI_OSS_BUCKET  
    ALI_OSS_ACCESS_KEY_ID
    ALI_OSS_ACCESS_KEY_SECRET

## 常见部署任务

部署单个应用到测试环境:
  pnpm build:app --app=admin-app
  pnpm deploy:app --app=admin-app

部署所有应用:
  pnpm build-deploy:all

静态资源部署:
  pnpm build-deploy:static:all

K8s增量部署:
  pnpm build-deploy:k8s:app --app=system-app

## 部署验证

检查部署状态:
  pnpm test:deployment:all

访问应用:
  测试环境: https://admin.bellis.com.cn
  生产环境: https://admin.bellis.com.cn

## 常见问题

Q: 部署失败怎么办?
A: 查看CI/CD日志，检查配置，运行部署测试

Q: 静态资源404?
A: 检查CDN配置，运行 pnpm deploy:static

Q: K8s部署卡住?
A: 检查Pod状态: kubectl get pods

Q: 如何回滚?
A: Git回滚到上一个tag，重新部署
