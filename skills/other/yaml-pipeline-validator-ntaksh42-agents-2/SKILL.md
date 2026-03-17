---
name: yaml-pipeline-validator
description: Validate and lint Azure Pipelines YAML with best practices checks. Use when validating pipeline syntax or ensuring pipeline quality.
---

# YAML Pipeline Validator Skill

Azure Pipelinesの YAML検証を行うスキルです。

## 主な機能

- **構文検証**: YAMLシンタックスチェック
- **ベストプラクティス**: 推奨設定確認
- **セキュリティ**: シークレット露出チェック
- **パフォーマンス**: 最適化提案

## 検証項目

### 1. 必須フィールド

```yaml
# ❌ Bad: トリガーなし
pool:
  vmImage: 'ubuntu-latest'

# ✅ Good
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'
```

### 2. シークレット管理

```yaml
# ❌ Bad: ハードコード
steps:
  - script: echo "Password: MySecretPassword123"

# ✅ Good: 変数グループ使用
variables:
  - group: Secrets

steps:
  - script: echo "Password: $(SecretPassword)"
```

### 3. キャッシュ使用

```yaml
# ✅ Good: 依存関係キャッシュ
steps:
  - task: Cache@2
    inputs:
      key: 'npm | "$(Agent.OS)" | package-lock.json'
      path: $(npm_config_cache)

  - script: npm install
```

### 4. 並列実行

```yaml
# ✅ Good: 並列ジョブ
jobs:
  - job: TestLinux
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - script: npm test

  - job: TestWindows
    pool:
      vmImage: 'windows-latest'
    steps:
      - script: npm test
```

## Azure CLI検証

```bash
# YAML検証
az pipelines validate \
  --repository myrepo \
  --branch main \
  --path azure-pipelines.yml
```

## バージョン情報
- Version: 1.0.0
