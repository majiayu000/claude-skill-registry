---
name: azure-repos-helper
description: Manage Azure Repos including branches, pull requests, and code reviews. Use when working with Azure Repos or managing repository operations.
---

# Azure Repos Helper Skill

Azure Reposでのリポジトリ管理を支援するスキルです。

## 主な機能

- **リポジトリ操作**: クローン、プッシュ、プル
- **ブランチポリシー**: PR必須、レビュー必須
- **コードレビュー**: PR作成、レビュー
- **ブランチ管理**: ブランチ戦略
- **Git操作**: Azure DevOps特有の操作

## ブランチポリシー設定

### main ブランチ保護

```json
{
  "isEnabled": true,
  "isBlocking": true,
  "type": {
    "id": "fa4e907d-c16b-4a4c-9dfa-4906e5d171dd"
  },
  "settings": {
    "minimumApproverCount": 2,
    "creatorVoteCounts": false,
    "allowDownvotes": false,
    "resetOnSourcePush": true,
    "requireVoteOnLastIteration": true,
    "blockLastPusherVote": true
  }
}
```

### ビルド検証

```json
{
  "isEnabled": true,
  "isBlocking": true,
  "type": {
    "id": "0609b952-1397-4640-95ec-e00a01b2c241"
  },
  "settings": {
    "buildDefinitionId": 123,
    "displayName": "PR Build Validation",
    "validDuration": 720,
    "queueOnSourceUpdateOnly": true
  }
}
```

## PR作成（Azure CLI）

```bash
# PR作成
az repos pr create \
  --repository MyRepo \
  --source-branch feature/new-feature \
  --target-branch main \
  --title "新機能: ユーザー認証" \
  --description "JWT認証を実装しました" \
  --reviewers user1@example.com user2@example.com \
  --work-items 123 456

# PRリスト取得
az repos pr list \
  --repository MyRepo \
  --status active

# PR承認
az repos pr update \
  --id 123 \
  --status approved

# PRマージ
az repos pr update \
  --id 123 \
  --status completed \
  --merge-commit-message "Merged PR 123: Add user authentication"
```

## .gitattributes

```
# Auto detect text files and perform LF normalization
* text=auto

# Source code
*.cs     text diff=csharp
*.java   text diff=java
*.py     text diff=python
*.js     text
*.ts     text

# Binary files
*.png    binary
*.jpg    binary
*.dll    binary
*.exe    binary
```

## バージョン情報
- Version: 1.0.0
