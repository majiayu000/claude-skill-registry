---
name: ci-cd
description: CI/CD 流水线配置
version: 1.0.0
author: terminal-skills
tags: [devops, ci-cd, jenkins, gitlab, github-actions]
---

# CI/CD 流水线配置

## 概述
Jenkins、GitLab CI、GitHub Actions 等 CI/CD 工具配置技能。

## GitHub Actions

### 基础工作流
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

### 矩阵构建
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### Docker 构建与推送
```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: user/app:${{ github.sha }}
```

### 部署到 Kubernetes
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: build
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      
      - name: Deploy
        run: |
          kubectl set image deployment/app app=user/app:${{ github.sha }}
          kubectl rollout status deployment/app
```

## GitLab CI

### 基础配置
```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

test:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  only:
    - main
  environment:
    name: production
    url: https://app.example.com
```

### 多环境部署
```yaml
.deploy_template: &deploy_template
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context $KUBE_CONTEXT
    - kubectl set image deployment/app app=$DOCKER_IMAGE

deploy_staging:
  <<: *deploy_template
  variables:
    KUBE_CONTEXT: staging
  environment:
    name: staging
  only:
    - develop

deploy_production:
  <<: *deploy_template
  variables:
    KUBE_CONTEXT: production
  environment:
    name: production
  only:
    - main
  when: manual
```

## Jenkins

### Jenkinsfile（声明式）
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "user/app:${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = credentials('docker-hub')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        
        stage('Docker Push') {
            steps {
                sh "echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin"
                sh "docker push ${DOCKER_IMAGE}"
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh "kubectl set image deployment/app app=${DOCKER_IMAGE}"
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend channel: '#deployments', message: "Build ${BUILD_NUMBER} succeeded"
        }
        failure {
            slackSend channel: '#deployments', message: "Build ${BUILD_NUMBER} failed"
        }
    }
}
```

### Jenkinsfile（脚本式）
```groovy
node {
    stage('Checkout') {
        checkout scm
    }
    
    stage('Build') {
        sh 'npm ci'
        sh 'npm run build'
    }
    
    stage('Test') {
        try {
            sh 'npm test'
        } finally {
            junit 'test-results/*.xml'
        }
    }
    
    if (env.BRANCH_NAME == 'main') {
        stage('Deploy') {
            sh 'kubectl apply -f k8s/'
        }
    }
}
```

## 通用模式

### 语义化版本发布
```yaml
# GitHub Actions
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Get version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT
      
      - name: Build
        run: npm run build
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

### 缓存依赖
```yaml
# GitHub Actions
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# GitLab CI
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
```

### 并行测试
```yaml
# GitHub Actions
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

### 条件执行
```yaml
# GitHub Actions
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."

# GitLab CI
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
    - if: $CI_COMMIT_TAG
      when: always
```

## 常见场景

### 场景 1：PR 检查
```yaml
name: PR Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

### 场景 2：定时任务
```yaml
name: Scheduled Job

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨2点

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running cleanup..."
```

### 场景 3：手动触发
```yaml
name: Manual Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 构建失败 | 查看日志、本地复现 |
| 权限问题 | 检查 secrets、token |
| 缓存失效 | 检查 cache key |
| 超时 | 增加 timeout、优化步骤 |
