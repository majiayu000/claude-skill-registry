---
name: ci-cd-builder
description: CI/CD 流水线配置指南。当用户需要配置 GitHub Actions、GitLab CI、自动化测试、自动部署或持续集成/持续部署流程时使用此技能。
---

# CI/CD Builder

帮助开发者快速搭建高效的持续集成和持续部署流水线。

## 支持平台

- GitHub Actions（主要）
- GitLab CI/CD
- Jenkins
- CircleCI

## GitHub Actions 模板

### Node.js 项目

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
```

### Docker 构建与推送

```yaml
  docker:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

##常用配置片段

### 缓存依赖

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### 条件执行

```yaml
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

### Secrets 使用

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## 最佳实践

1. **快速反馈**：测试任务并行执行
2. **缓存优化**：缓存依赖减少构建时间
3. **安全存储**：敏感信息使用 Secrets
4. **版本锁定**：固定 Action 版本号
5. **失败通知**：配置 Slack/邮件通知

## 参考资源

- GitHub Actions 文档: https://docs.github.com/en/actions
- GitLab CI 文档: https://docs.gitlab.com/ee/ci/