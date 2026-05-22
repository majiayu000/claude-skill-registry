---
name: import-helper
description: 既存リソースを Terraform に import する。「import して」「リソース import」「既存リソース取り込み」「terraform import」「インポート」「既存インフラを管理」「import ガイド」「リソースを terraform で管理」などで起動。
allowed-tools: [Bash, Read, Write, Edit]
---

# Import Helper

既存の AWS/GCP/Azure リソースを Terraform の管理下に取り込む支援をします。

## 対応操作

| 操作 | トリガー例 |
|------|-----------|
| import ガイド | 「import して」「インポート」 |
| リソース指定 | 「EC2 を import」「S3 を import」 |
| 設定生成 | 「import 用の tf を作成」 |

## 実行手順

### 1. import 対象の確認

ユーザーにリソース情報を確認:

```
## Import 対象

import するリソースの情報を教えてください:

1. リソースタイプ（例: aws_instance, aws_s3_bucket）
2. リソース ID（例: i-1234567890abcdef0, my-bucket）
3. Terraform でのリソース名（例: main, web_server）
```

### 2. リソース設定ファイルの作成

import 前に空のリソース定義が必要:

```hcl
# {resource_type}.tf

resource "{resource_type}" "{resource_name}" {
  # import 後に terraform plan で確認し、属性を追加
}
```

例:

```hcl
# aws_instance.tf

resource "aws_instance" "web_server" {
  # import 後に terraform plan で確認し、属性を追加
}
```

### 3. import コマンドの生成

```bash
terraform import {resource_type}.{resource_name} {resource_id}
```

例:

```bash
# EC2 インスタンス
terraform import aws_instance.web_server i-1234567890abcdef0

# S3 バケット
terraform import aws_s3_bucket.data my-bucket-name

# IAM ロール
terraform import aws_iam_role.app my-role-name

# VPC
terraform import aws_vpc.main vpc-12345678

# セキュリティグループ
terraform import aws_security_group.web sg-12345678
```

### 4. import 実行

```bash
terraform import {resource_type}.{resource_name} {resource_id}
```

成功時:

```
{resource_type}.{resource_name}: Importing from ID "{resource_id}"...
{resource_type}.{resource_name}: Import prepared!
{resource_type}.{resource_name}: Refreshing state...

Import successful!

The resources that were imported are shown above.
```

### 5. 設定の同期

import 後、現在の state と設定ファイルを同期:

```bash
terraform plan
```

差分を確認し、設定ファイルを更新:

```
## Import 後の設定同期

terraform plan で以下の差分が検出されました:

{差分の内容}

この差分をなくすために、設定ファイルを更新してください。
```

### 6. 出力フォーマット

```
## Import 完了

### リソース
- タイプ: {resource_type}
- 名前: {resource_name}
- ID: {resource_id}

### 次のステップ

1. `terraform plan` で差分を確認
2. 設定ファイルに必要な属性を追加
3. 再度 `terraform plan` で差分がないことを確認

### 注意
import 後は設定ファイルと state の同期が必要です。
`terraform plan` で差分が出なくなるまで設定を調整してください。
```

## 主要リソースの import コマンド例

| リソース | コマンド |
|----------|---------|
| EC2 インスタンス | `terraform import aws_instance.NAME INSTANCE_ID` |
| S3 バケット | `terraform import aws_s3_bucket.NAME BUCKET_NAME` |
| IAM ロール | `terraform import aws_iam_role.NAME ROLE_NAME` |
| VPC | `terraform import aws_vpc.NAME VPC_ID` |
| サブネット | `terraform import aws_subnet.NAME SUBNET_ID` |
| セキュリティグループ | `terraform import aws_security_group.NAME SG_ID` |
| RDS インスタンス | `terraform import aws_db_instance.NAME DB_IDENTIFIER` |
| Lambda 関数 | `terraform import aws_lambda_function.NAME FUNCTION_NAME` |

## 注意事項

- ✅ import 前に空のリソース定義を作成
- ✅ import 後は必ず `terraform plan` で同期を確認
- ✅ 設定ファイルは state に合わせて更新
- ⚠️ import はリソースを変更しないが、設定ミスで次回 apply 時に変更される可能性
