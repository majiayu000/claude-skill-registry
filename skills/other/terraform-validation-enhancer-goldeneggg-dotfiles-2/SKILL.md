---
name: terraform-validation-enhancer
description: |
  Terraform構成の依存関係管理とバリデーションを評価・強化するスキル
  Terraform 1.14以上を対象に、variable validation、depends_on/lifecycle、precondition/postcondition、check blockの現状評価と改善提案を実施
  (1) 既存Terraform構成の評価・診断
  (2) バリデーション不足の自動検出と修正提案
  (3) ベストプラクティス適用
  (4) セキュリティ・可用性要件の検証が必要な場合に使用。
---

# Terraform Validation Enhancer

Terraform構成の依存関係管理とバリデーションを体系的に評価・強化します。

## 概要

このスキルはTerraform 1.14以上の構成に対して以下を実施:

1. **現状評価**: variable validation、depends_on、lifecycle、precondition/postcondition、check blockの使用状況を分析
2. **問題検出**: 不足しているバリデーションや不適切な依存関係設定を特定
3. **修正提案**: 具体的な改善コードと実装ガイダンスを提供
4. **ベストプラクティス適用**: Terraform 1.14の新機能を活用した推奨パターンを提案

## ワークフロー

### ステップ1: 構成の分析

まず、analyze_terraform.pyスクリプトを使用してTerraform構成を分析します。

```bash
python3 ~/.claude/skills/terraform-validation-enhancer/scripts/analyze_terraform.py <terraform_directory>
```

このスクリプトは以下をJSON形式で出力:

- バリデーションが不足している変数
- lifecycleブロックが推奨されるリソース
- precondition/postconditionが有用なリソース
- check blockの追加候補

### ステップ2: 評価結果の確認

分析結果を確認し、以下の観点で優先度を判断:

1. **Critical (警告)**: セキュリティやデータ保護に関わる問題
   - センシティブな変数に`sensitive = true`が未設定
   - 本番DBリソースに`prevent_destroy`が未設定

2. **Important (推奨)**: 可用性や運用品質に関わる問題
   - 重要な変数にvalidationブロックが未設定
   - ダウンタイムリスクのあるリソースに`create_before_destroy`が未設定

3. **Nice to have (提案)**: コード品質向上に寄与
   - data sourceへのprecondition追加
   - check blockによる実行時検証

### ステップ3: 修正の実施

優先度に基づいて修正を実施します。具体的なパターンは`{このSKILL.mdのDIR}/references/validation-patterns.md`を参照してください。

#### 3.1 Variable Validation の追加

```hcl
# Before
variable "instance_count" {
  type        = number
  description = "Number of instances"
}

# After
variable "instance_count" {
  type        = number
  description = "Number of instances"

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

#### 3.2 Lifecycle Block の追加

```hcl
# Before
resource "aws_db_instance" "production" {
  # ... configuration
}

# After
resource "aws_db_instance" "production" {
  # ... configuration

  lifecycle {
    prevent_destroy = true  # 本番DBの誤削除を防止
  }
}
```

#### 3.3 Precondition/Postcondition の追加

```hcl
# Before
data "aws_ami" "app" {
  most_recent = true
  # ...
}

# After
data "aws_ami" "app" {
  most_recent = true
  # ...

  lifecycle {
    precondition {
      condition     = self.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }
  }
}
```

#### 3.4 Check Block の追加

```hcl
check "security_compliance" {
  data "aws_s3_bucket" "example" {
    bucket = aws_s3_bucket.example.id
  }

  assert {
    condition     = data.aws_s3_bucket.example.server_side_encryption_configuration != null
    error_message = "S3 bucket must have encryption enabled."
  }

  assert {
    condition     = data.aws_s3_bucket.example.versioning[0].enabled == true
    error_message = "S3 bucket must have versioning enabled."
  }
}
```

### ステップ4: 検証

修正後、以下を実行して構成の妥当性を確認:

```bash
# 構成の検証
terraform init
terraform validate

# planで変更内容を確認
terraform plan

# 再度分析スクリプトを実行して改善を確認
python3 ~/.claude/skills/terraform-validation-enhancer/scripts/analyze_terraform.py <terraform_directory>
```

## 評価観点の詳細

### Variable Validation

- 全ての公開変数に適切なvalidationが設定されているか
- センシティブな変数に`sensitive = true`が設定されているか
- error_messageが具体的で理解しやすいか

**詳細**: `{このSKILL.mdのDIR}/references/validation-patterns.md#variable-validation-patterns`

### Resource Dependencies

- `depends_on`は本当に必要か（暗黙的依存で十分でないか）
- モジュール間の依存関係が明確に表現されているか
- 循環依存が発生していないか

**詳細**: `{このSKILL.mdのDIR}/references/validation-patterns.md#resource-dependencies-depends_on`

### Lifecycle Management

- 本番環境リソースに`prevent_destroy`が設定されているか
- ダウンタイムを避けるため`create_before_destroy`が適切に使用されているか
- `ignore_changes`の使用が正当化されているか

**詳細**: `{このSKILL.mdのDIR}/references/validation-patterns.md#lifecycle-management`

### Preconditions and Postconditions

- 重要なdata sourceにpreconditionが設定されているか
- リソース作成の前提条件がpreconditionで検証されているか
- リソースの重要な属性がpostconditionで検証されているか

**詳細**: `{このSKILL.mdのDIR}/references/validation-patterns.md#preconditions-and-postconditions`

### Check Blocks

- インフラの稼働状態を検証するcheck blockが存在するか
- セキュリティ要件を検証するcheck blockが存在するか
- 環境別の要件がcheck blockで検証されているか

**詳細**: `{このSKILL.mdのDIR}/references/validation-patterns.md#check-blocks`

## リファレンス

### Terraform 1.14 ドキュメント

詳細な構文とオプションは`{このSKILL.mdのDIR}/references/terraform-v1.14-docs.md`を参照してください。以下のセクションが含まれます:

- Variable Validation の完全な仕様
- Check Blocks の使用方法
- Depends On の詳細
- Lifecycle の全オプション
- Custom Conditions (precondition/postcondition)

### バリデーションパターン集

実践的なコード例とベストプラクティスは`{このSKILL.mdのDIR}/references/validation-patterns.md`を参照してください。以下が含まれます:

- 値の範囲チェック、文字列パターンマッチ等のvalidationパターン
- 明示的依存関係、モジュール間依存等のdepends_onパターン
- リソース再作成防止、新規リソース作成後の置換等のlifecycleパターン
- Data source、resource、outputのprecondition/postconditionパターン
- インフラ検証、セキュリティコンプライアンス等のcheck blockパターン

## スクリプト

### analyze_terraform.py

Terraform構成ファイルを解析し、改善点を特定します。

**使用方法**:

```bash
python3 ~/.claude/skills/terraform-validation-enhancer/scripts/analyze_terraform.py <terraform_directory>
```

**出力例**:

```json
{
  "summary": {
    "total_files": 5,
    "total_issues": 12,
    "by_severity": {
      "warning": 3,
      "suggestion": 6,
      "info": 3
    },
    "by_category": {
      "validation": 4,
      "lifecycle": 3,
      "condition": 3,
      "check": 2
    }
  },
  "issues": [
    {
      "file": "variables.tf",
      "line": 10,
      "severity": "warning",
      "category": "validation",
      "message": "Variable 'instance_count' lacks validation block",
      "suggestion": "Consider adding validation block to ensure input correctness"
    }
  ]
}
```

## 使用上の注意

1. **Terraform バージョン**: このスキルはTerraform 1.14以上を対象としています
2. **段階的適用**: 一度に全ての修正を適用せず、優先度に基づいて段階的に実施してください
3. **テスト**: 修正後は必ず`terraform plan`で影響を確認してください
4. **チーム合意**: 大規模な変更はチームで合意を得てから実施してください

## トラブルシューティング

### analyze_terraform.py実行時のエラー

- **権限エラー**: スクリプトに実行権限を付与 (`chmod +x {このSKILL.mdのDIR}/scripts/analyze_terraform.py`)
- **Python バージョン**: Python 3.7以上が必要

### 誤検知への対処

スクリプトの検出は推奨事項です。プロジェクト固有の理由で適用しない判断も有効です。その場合は:

1. 理由をコメントで文書化
2. チーム内で合意を記録
3. 将来のレビューで再評価

## 関連ドキュメント

- [Terraform Language Documentation](https://developer.hashicorp.com/terraform/language)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
