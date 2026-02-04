---
name: ci-cd-generator
description: Generate CI/CD pipeline configurations for GitHub Actions, GitLab CI, Jenkins. Use when setting up automated build and deployment pipelines.
---

# CI/CD Generator Skill

CI/CDパイプラインの設定を生成するスキルです。

## 主な機能

- **GitHub Actions**: ワークフロー生成
- **GitLab CI**: .gitlab-ci.yml生成
- **CircleCI**: config.yml生成
- **Jenkins**: Jenkinsfile生成

## GitHub Actions例

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v3
      - name: Deploy to Production
        run: |
          # デプロイコマンド
```

## バージョン情報
- Version: 1.0.0
