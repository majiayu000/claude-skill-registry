---
name: tf-executor
description: Terraform コマンドを実行する。「terraform plan」「terraform apply」「tf init」「tf plan」「tf apply」「terraform して」「tf 実行」「インフラ適用」「プラン確認」などで起動。
allowed-tools: [Bash, Read]
---

# Terraform Executor

Terraform コマンドの実行を支援します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| 初期化 | 「init して」「terraform init」 | `terraform init` |
| 計画 | 「plan して」「プラン確認」 | `terraform plan` |
| 適用 | 「apply して」「適用して」 | `terraform apply` |
| 検証 | 「validate」「検証して」 | `terraform validate` |
| フォーマット | 「fmt」「フォーマット」 | `terraform fmt` |
| 出力確認 | 「output」「出力確認」 | `terraform output` |
| バージョン | 「version」「バージョン」 | `terraform version` |

## 実行手順

### 1. 意図の判定

ユーザーの発話から操作を判定:

- **初期化系**: 「init」「初期化」→ `terraform init`
- **計画系**: 「plan」「プラン」「確認」→ `terraform plan`
- **適用系**: 「apply」「適用」「実行」→ `terraform apply`
- **検証系**: 「validate」「検証」→ `terraform validate`
- **フォーマット系**: 「fmt」「フォーマット」→ `terraform fmt`

### 2. 事前確認

```bash
# Terraform バージョン確認
terraform version

# ワーキングディレクトリの .tf ファイル確認
ls *.tf 2>/dev/null || ls **/*.tf 2>/dev/null
```

### 3. コマンド実行

**init**:

```bash
terraform init
```

**plan**:

```bash
terraform plan -no-color
```

**apply**:

```bash
# ユーザー確認後
terraform apply
```

**validate**:

```bash
terraform validate
```

**fmt**:

```bash
terraform fmt -check -recursive -diff
```

**output**:

```bash
terraform output
```

### 4. 出力フォーマット

```
## Terraform 実行結果

### コマンド
terraform {command}

### 結果
{コマンドの出力}

### サマリー
{成功/失敗と簡潔な説明}
```

## 注意事項

- ✅ plan は安全な読み取り操作
- ✅ apply は必ずユーザー確認を取る
- ❌ `-auto-approve` は使用しない
- ❌ `destroy` は直接実行しない（ユーザーに手動実行を案内）
