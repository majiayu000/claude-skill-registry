---
name: azure-service-connections
description: Configure Azure DevOps service connections for deployments. Use when setting up cloud service integrations or deployment credentials.
---

# Azure Service Connections Skill

Azure DevOpsサービス接続を管理するスキルです。

## 主な機能

- **Azure接続**: Azure Resource Manager
- **GitHub接続**: リポジトリ連携
- **Docker Hub**: コンテナレジストリ
- **Kubernetes**: AKSクラスター

## Azure Resource Manager接続

### サービスプリンシパル作成

```bash
# サービスプリンシパル作成
az ad sp create-for-rbac \
  --name "azure-devops-sp" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}

# 出力
{
  "appId": "xxx",
  "displayName": "azure-devops-sp",
  "password": "yyy",
  "tenant": "zzz"
}
```

### Pipeline設定

```yaml
resources:
  - type: ServiceConnection
    name: Azure-Production
    serviceConnection: 'Azure-Prod-Connection'

steps:
  - task: AzureCLI@2
    inputs:
      azureSubscription: 'Azure-Prod-Connection'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az group list
```

## GitHub接続

```yaml
resources:
  repositories:
    - repository: source-repo
      type: github
      endpoint: GitHub-Connection
      name: myorg/myrepo

trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - checkout: source-repo
  - script: echo "Building from GitHub"
```

## Docker Registry

```yaml
resources:
  containers:
    - container: build-container
      image: myregistry.azurecr.io/build:latest
      endpoint: Docker-Registry-Connection

steps:
  - script: |
      docker build -t myapp:$(Build.BuildId) .
      docker push myapp:$(Build.BuildId)
```

## バージョン情報
- Version: 1.0.0
