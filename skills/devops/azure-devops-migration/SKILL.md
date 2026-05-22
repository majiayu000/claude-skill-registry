---
name: azure-devops-migration
description: Plan and execute Azure DevOps migrations between organizations or projects. Use when migrating Azure DevOps resources or consolidating projects.
---

# Azure DevOps Migration Skill

他のCI/CDツールからAzure DevOpsへの移行を支援するスキルです。

## 主な機能

- **GitHub Actions → Azure Pipelines**: YAML変換
- **Jenkins → Azure Pipelines**: Jenkinsfile変換
- **GitLab CI → Azure Pipelines**: .gitlab-ci.yml変換

## GitHub Actions → Azure Pipelines

### GitHub Actions

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
```

### Azure Pipelines

```yaml
trigger:
  - '*'

pool:
  vmImage: 'ubuntu-latest'

steps:
  - checkout: self
  - task: NodeTool@0
    inputs:
      versionSpec: '18'
  - script: npm install
  - script: npm test
```

## Jenkins → Azure Pipelines

### Jenkinsfile

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

### Azure Pipelines

```yaml
stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - script: npm install
          - script: npm run build

  - stage: Test
    jobs:
      - job: TestJob
        steps:
          - script: npm test
```

## バージョン情報
- Version: 1.0.0
