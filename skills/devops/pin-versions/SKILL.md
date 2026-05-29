---
name: pin-versions
description: 依存関係のバージョン固定。package.json や Terraform Provider を編集したら必ず実行。
---

# Pin Versions

依存関係のバージョンを固定するスキル。

## 重要

**package.json や Terraform Provider ファイルを編集した場合は、必ずこのルールに従ってバージョンを固定すること。**

## 対象ファイル

- `**/package.json` - npm/pnpm パッケージ
- `**/*.tf` (providers.tf, versions.tf) - Terraform Provider

## ルール

### package.json

バージョン指定には `^` や `~` を使用せず、固定バージョンを指定する。

```json
// NG
"dependencies": {
  "react": "^19.0.0",
  "next": "~15.0.0"
}

// OK
"dependencies": {
  "react": "19.0.0",
  "next": "15.0.0"
}
```

**例外**:
- `workspace:*` - モノレポ内のパッケージ参照は許可

### Terraform Provider

`~>` や `>=` を使用せず、固定バージョンを指定する。

```hcl
// NG
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      version = "~> 5.0"
    }
  }
}

// OK
terraform {
  required_version = "1.14.3"
  required_providers {
    aws = {
      version = "5.82.2"
    }
  }
}
```

## 確認コマンド

```bash
# package.json の ^ や ~ を検索
grep -r '"\^' apps/*/package.json packages/*/package.json
grep -r '"~' apps/*/package.json packages/*/package.json

# Terraform の ~> や >= を検索
grep -rE '"~>|">=' infra/terraform --include="*.tf"
```

## 手順

1. ファイルを編集
2. 上記の確認コマンドでバージョン指定を確認
3. `^` や `~` があれば固定バージョンに修正
4. `pnpm install` で lockfile を更新（package.json の場合）
5. `pnpm check` で問題がないことを確認

## 理由

- 再現性の確保: 同じバージョンで常にビルドできる
- 予期しない破壊的変更の防止
- CI/CD での一貫性
