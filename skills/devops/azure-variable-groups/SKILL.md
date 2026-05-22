---
name: azure-variable-groups
description: Manage Azure Pipeline variable groups and library secrets. Use when organizing pipeline variables or managing configuration.
---

# Azure Variable Groups Skill

Azure Pipelinesの変数グループを管理するスキルです。

## 主な機能

- **変数グループ作成**: 共通変数管理
- **Key Vault連携**: シークレット管理
- **環境別変数**: Dev/Staging/Prod
- **パイプライン連携**: 変数グループ使用

## 変数グループ作成

### Azure CLI

```bash
# 変数グループ作成
az pipelines variable-group create \
  --name "Production-Variables" \
  --variables \
    DATABASE_HOST="prod-db.database.windows.net" \
    DATABASE_NAME="proddb" \
    API_URL="https://api.production.example.com" \
  --authorize true

# Key Vaultリンク変数グループ
az pipelines variable-group create \
  --name "Production-Secrets" \
  --variables \
    ConnectionString \
    ApiKey \
  --authorize true

# 変数追加
az pipelines variable-group variable create \
  --group-id 1 \
  --name "NEW_VARIABLE" \
  --value "new-value"
```

## パイプラインでの使用

```yaml
variables:
  - group: Production-Variables
  - group: Production-Secrets

stages:
  - stage: Deploy
    jobs:
      - job: DeployJob
        steps:
          - script: |
              echo "Database: $(DATABASE_HOST)"
              echo "API: $(API_URL)"
            displayName: 'Use Variables'
```

## Key Vault統合

```yaml
# Key Vaultから変数取得
variables:
  - group: KeyVault-Secrets

steps:
  - task: AzureKeyVault@2
    inputs:
      azureSubscription: 'Azure-Connection'
      KeyVaultName: 'MyKeyVault'
      SecretsFilter: '*'
      RunAsPreJob: true
```

## 環境別変数管理

```yaml
# Dev環境
variables:
  - ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/develop') }}:
    - group: Dev-Variables
  
# Prod環境
  - ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    - group: Prod-Variables
```

## バージョン情報
- Version: 1.0.0
