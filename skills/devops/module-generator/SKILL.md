---
name: module-generator
description: Terraform モジュールを生成・管理する。「モジュール作成」「モジュール生成」「新しいモジュール」「module 作って」「モジュール構造」「tf モジュール」「terraform モジュール追加」「モジュールのテンプレート」「モジュール scaffold」などで起動。
allowed-tools: [Bash, Read, Write, Edit]
context: fork
agent: shiiman-terraform:module-designer
---

# Module Generator

Terraform モジュールのスキャフォールドを生成します。

## 対応操作

| 操作 | トリガー例 |
|------|-----------|
| モジュール作成 | 「モジュール作成」「module 作って」 |
| 構造確認 | 「モジュール構造」「module 一覧」 |
| テンプレート | 「モジュールテンプレート」 |

## 実行手順

### 1. モジュール情報の確認

```
## モジュール作成

作成するモジュールの情報を教えてください:

1. モジュール名（例: vpc, ec2, rds）
2. 作成場所（デフォルト: modules/）
3. 用途（例: VPC ネットワーク構築、EC2 インスタンス作成）
```

### 2. ディレクトリ構造の作成

```bash
mkdir -p modules/{module_name}
```

### 3. ファイルの生成

#### main.tf

```hcl
# {Module Name} Module
#
# {用途の説明}

# TODO: リソース定義を追加
```

#### variables.tf

```hcl
# 入力変数

variable "name" {
  description = "リソースの名前プレフィックス"
  type        = string
}

variable "environment" {
  description = "環境名（dev, stg, prod）"
  type        = string
  default     = "dev"
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
  default     = {}
}

# TODO: 必要な変数を追加
```

#### outputs.tf

```hcl
# 出力値

# TODO: 出力値を追加
# output "id" {
#   description = "リソースの ID"
#   value       = aws_xxx.main.id
# }
```

#### versions.tf

```hcl
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}
```

#### README.md

```markdown
# {Module Name} Module

{用途の説明}

## 使い方

\`\`\`hcl
module "{module_name}" {
  source = "./modules/{module_name}"

  name        = "example"
  environment = "dev"
  tags = {
    Project = "example"
  }
}
\`\`\`

## 入力変数

| 変数 | 説明 | 型 | デフォルト | 必須 |
|------|------|-----|----------|------|
| name | リソースの名前プレフィックス | string | - | ✅ |
| environment | 環境名 | string | dev | |
| tags | リソースに付与するタグ | map(string) | {} | |

## 出力値

| 出力 | 説明 |
|------|------|
| (TODO) | |

## 依存関係

- Terraform >= 1.0.0
- AWS Provider >= 5.0.0
\`\`\`
```

### 4. 出力フォーマット

```
## モジュール作成完了

### 作成されたファイル

modules/{module_name}/
├── main.tf          # リソース定義
├── variables.tf     # 入力変数
├── outputs.tf       # 出力値
├── versions.tf      # バージョン制約
└── README.md        # ドキュメント

### 次のステップ

1. `main.tf` にリソース定義を追加
2. `variables.tf` に必要な変数を追加
3. `outputs.tf` に出力値を追加
4. `README.md` を更新

### 使い方

\`\`\`hcl
module "{module_name}" {
  source = "./modules/{module_name}"

  name        = "example"
  environment = "dev"
}
\`\`\`
```

## モジュール設計のベストプラクティス

### 命名規則

- モジュール名は小文字とハイフン（例: `vpc-network`）
- 変数名は小文字とアンダースコア（例: `instance_type`）

### 変数設計

- 必須変数は `default` を設定しない
- オプション変数は適切なデフォルト値を設定
- `description` は必ず記載
- `type` は必ず指定

### 出力設計

- モジュール外から参照される値は必ず出力
- `description` は必ず記載
- センシティブな値は `sensitive = true`

## 注意事項

- ✅ モジュールは再利用可能な単位で設計
- ✅ 変数と出力には必ず description を記載
- ✅ README.md で使い方を文書化
- ⚠️ モジュール内でハードコードを避ける
