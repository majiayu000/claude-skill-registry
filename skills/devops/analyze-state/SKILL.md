---
name: analyze-state
description: Terraform state を分析・操作する。「state 確認」「state list」「state show」「リソース一覧」「state の移動」「state mv」「state rm」「terraform state」「state 操作」「リソースの状態」「state pull」などで起動。
allowed-tools: [Bash, Read]
context: fork
agent: shiiman-terraform:state-troubleshooter
---

# State Analyzer

Terraform state ファイルの分析と操作を支援します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| 一覧表示 | 「state list」「リソース一覧」 | `terraform state list` |
| 詳細表示 | 「state show」「リソース詳細」 | `terraform state show` |
| リモート取得 | 「state pull」「state 取得」 | `terraform state pull` |
| 移動 | 「state mv」「リソース移動」 | `terraform state mv` |
| 削除 | 「state rm」「state から削除」 | `terraform state rm` |

## 実行手順

### 1. 操作の判定

ユーザーの発話から操作を判定:

- **一覧系**: 「list」「一覧」「確認」→ `state list`
- **詳細系**: 「show」「詳細」「内容」→ `state show`
- **取得系**: 「pull」「取得」「ダウンロード」→ `state pull`
- **移動系**: 「mv」「移動」「rename」→ `state mv`
- **削除系**: 「rm」「削除」「remove」→ `state rm`

### 2. state list

```bash
terraform state list
```

出力例:

```
aws_instance.web
aws_security_group.web
aws_vpc.main
```

### 3. state show

```bash
terraform state show {resource_address}
```

出力例:

```
# aws_instance.web:
resource "aws_instance" "web" {
    ami                          = "ami-12345678"
    instance_type                = "t3.micro"
    ...
}
```

### 4. state pull

```bash
terraform state pull
```

リモートバックエンドから state をダウンロードして表示。

### 5. state mv（手動実行を案内）

**重要**: state mv はリソースのアドレスを変更する危険な操作のため、自動実行は禁止されています。

ユーザーに手動実行を案内:

```
## State 移動

以下のコマンドを手動で実行してください:

terraform state mv {source} {destination}

⚠️ 注意:
- この操作は state を変更します
- 実行前に terraform state list で現在の状態を確認してください
- 間違った移動は terraform state mv で戻せます
```

### 6. state rm（手動実行を案内）

**重要**: state rm はリソースを state から削除する危険な操作のため、自動実行は禁止されています。

ユーザーに手動実行を案内:

```
## State 削除

以下のコマンドを手動で実行してください:

terraform state rm {resource_address}

⚠️ 注意:
- 実際のインフラリソースは削除されません
- state から削除すると Terraform の管理外になります
- 再度管理するには import が必要です
```

### 7. 出力フォーマット

**state list**:

```
## State リソース一覧

| # | リソースアドレス |
|---|-----------------|
| 1 | aws_instance.web |
| 2 | aws_security_group.web |
| ... | ... |

合計: {N} リソース
```

**state show**:

```
## リソース詳細: {resource_address}

### 主要属性

| 属性 | 値 |
|------|-----|
| id | {id} |
| ... | ... |

### 全属性

{terraform state show の出力}
```

## よくある使い方

### リソースのリネーム

```bash
# 旧名から新名に移動
terraform state mv aws_instance.old_name aws_instance.new_name
```

### モジュール化

```bash
# ルートからモジュール内に移動
terraform state mv aws_instance.web module.web.aws_instance.main
```

### state から除外

```bash
# 管理対象外にする
terraform state rm aws_instance.legacy
```

## 注意事項

- ✅ `state list` / `state show` / `state pull` は読み取り専用で安全
- ⚠️ `state mv` / `state rm` は state を変更する操作
- ⚠️ `state rm` は実リソースを削除しない（Terraform 管理外になるだけ）
- ❌ 確認なしで `state mv` / `state rm` を実行しない
