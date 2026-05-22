---
name: check-security
description: Terraform のセキュリティをチェックする。「セキュリティチェック」「シークレット検出」「セキュリティ監査」「tf セキュリティ」「state のシークレット」「機密情報確認」「セキュリティスキャン」「脆弱性チェック」「ハードコード検出」などで起動。
allowed-tools: [Bash, Read, Grep, Glob]
context: fork
agent: shiiman-terraform:security-checker
---

# Security Checker

Terraform 設定とstateのセキュリティチェックを行います。

## 対応操作

| 操作 | トリガー例 |
|------|-----------|
| 全体スキャン | 「セキュリティチェック」「監査」 |
| コード検査 | 「ハードコード検出」「コード内シークレット」 |
| State 検査 | 「state のシークレット」「state 監査」 |
| IAM 検査 | 「IAM チェック」「権限確認」 |
| ネットワーク検査 | 「SG チェック」「ネットワーク監査」 |

## 実行手順

### 1. コード内のシークレット検出

```bash
# AWS キーのパターン検出（AKIA, ASIA, AIDA, AROA 等に対応）
grep -rnE "A(KIA|SIA|IDA|ROA|IPA|GPA|3T)[0-9A-Z]{16}" *.tf **/*.tf 2>/dev/null

# シークレットキーのパターン検出
grep -rn "aws_secret_access_key\s*=" *.tf **/*.tf 2>/dev/null

# パスワードのハードコード検出
grep -rn "password\s*=\s*\"" *.tf **/*.tf 2>/dev/null

# API キーのハードコード検出
grep -rn "api_key\s*=\s*\"" *.tf **/*.tf 2>/dev/null
```

### 2. State 内のシークレット検出

```bash
# State ファイルの確認
terraform state pull | grep -i "password\|secret\|key\|token" 2>/dev/null
```

### 3. IAM ポリシーの過剰権限検出

```bash
# AdministratorAccess の使用
grep -rn "AdministratorAccess\|arn:aws:iam::aws:policy/AdministratorAccess" *.tf **/*.tf 2>/dev/null

# ワイルドカード権限
grep -rn '"Action"\s*:\s*"\*"\|"Resource"\s*:\s*"\*"' *.tf **/*.tf 2>/dev/null

# 全リソースアクセス
grep -rn '"*"' *.tf **/*.tf 2>/dev/null | grep -i "action\|resource"
```

### 4. ネットワークセキュリティ検出

```bash
# 0.0.0.0/0 からの SSH 許可
grep -B5 -A5 "0.0.0.0/0" *.tf **/*.tf 2>/dev/null | grep -i "22\|ssh"

# 0.0.0.0/0 からの全ポート許可
grep -B5 -A5 'from_port\s*=\s*0' *.tf **/*.tf 2>/dev/null

# パブリック S3 バケット
grep -rn "acl\s*=\s*\"public" *.tf **/*.tf 2>/dev/null
```

### 5. 暗号化設定の確認

```bash
# 暗号化なしの EBS
grep -B10 "aws_ebs_volume\|aws_instance" *.tf **/*.tf 2>/dev/null | grep -v "encrypted\s*=\s*true"

# 暗号化なしの RDS
grep -B10 "aws_db_instance" *.tf **/*.tf 2>/dev/null | grep -v "storage_encrypted\s*=\s*true"

# 暗号化なしの S3
grep -B10 "aws_s3_bucket" *.tf **/*.tf 2>/dev/null | grep -v "server_side_encryption"
```

### 6. 出力フォーマット

```
## セキュリティチェック結果

### 概要

| カテゴリ | 検出数 | 重要度 |
|----------|--------|--------|
| シークレット | {N} | 🔴 高 |
| IAM 過剰権限 | {N} | 🔴 高 |
| ネットワーク | {N} | 🟡 中 |
| 暗号化 | {N} | 🟡 中 |

### 🔴 高リスク

#### シークレットのハードコード

| ファイル | 行 | 問題 |
|----------|-----|------|
| main.tf | 15 | AWS アクセスキーがハードコード |
| ... | ... | ... |

**修正方法**: 環境変数または AWS Secrets Manager を使用

#### IAM 過剰権限

| ファイル | 行 | 問題 |
|----------|-----|------|
| iam.tf | 20 | AdministratorAccess の使用 |
| ... | ... | ... |

**修正方法**: 最小権限の原則に従って権限を制限

### 🟡 中リスク

#### ネットワークセキュリティ

| ファイル | 行 | 問題 |
|----------|-----|------|
| sg.tf | 10 | 0.0.0.0/0 から SSH 許可 |
| ... | ... | ... |

**修正方法**: 特定の IP 範囲に制限

#### 暗号化未設定

| ファイル | 行 | 問題 |
|----------|-----|------|
| storage.tf | 5 | EBS 暗号化が無効 |
| ... | ... | ... |

**修正方法**: `encrypted = true` を設定

### 推奨事項

1. シークレットは AWS Secrets Manager または環境変数で管理
2. IAM ポリシーは最小権限の原則に従う
3. セキュリティグループは必要最小限のポートのみ許可
4. すべてのストレージで暗号化を有効化
```

## セキュリティベストプラクティス

### シークレット管理

```hcl
# ❌ 悪い例
resource "aws_db_instance" "main" {
  password = "hardcoded-password"  # ハードコード
}

# ✅ 良い例
resource "aws_db_instance" "main" {
  password = var.db_password  # 変数から取得
}

# または
data "aws_secretsmanager_secret_version" "db" {
  secret_id = "db-password"
}
```

### IAM ポリシー

```hcl
# ❌ 悪い例
resource "aws_iam_role_policy" "admin" {
  policy = jsonencode({
    Statement = [{
      Action   = "*"
      Resource = "*"
    }]
  })
}

# ✅ 良い例
resource "aws_iam_role_policy" "limited" {
  policy = jsonencode({
    Statement = [{
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```

## 注意事項

- ✅ セキュリティチェックは読み取り専用で安全
- ✅ 定期的にセキュリティ監査を実行
- ✅ CI/CD パイプラインにセキュリティチェックを組み込む
- ⚠️ 検出結果は誤検知の可能性もあるため、内容を確認
