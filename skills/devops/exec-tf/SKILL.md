---
name: exec-tf
description: Terraform コマンドを実行する。「terraform plan」「terraform apply」「tf init」「tf plan」「tf apply」「terraform して」「tf 実行」「インフラ適用」「プラン確認」「validate」「検証」などで起動。
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

# 初期化状態確認
ls -la .terraform 2>/dev/null
```

`.tf` ファイルがない場合はエラーメッセージを表示して終了。

`.terraform` がない場合:

```
⚠️ Terraform が初期化されていません。
先に `terraform init` を実行してください。

「init して」と言うか、以下を実行:
terraform init
```

---

## Plan 操作

### オプション

| オプション | 説明 |
|------------|------|
| `--target <resource>` | 特定リソースのみ plan |
| `--out <file>` | plan ファイルを出力 |
| `--destroy` | destroy plan を実行 |

### plan 実行

**標準 plan**:

```bash
terraform plan -no-color
```

**オプション付き**:

```bash
# 特定リソースのみ
terraform plan -target=<resource> -no-color

# plan ファイル出力
terraform plan -out=<file> -no-color

# destroy plan
terraform plan -destroy -no-color
```

### plan 結果解析

plan 出力を解析し、以下の情報を抽出:

- 追加されるリソース（`+`）
- 変更されるリソース（`~`）
- 削除されるリソース（`-`）
- 再作成されるリソース（`-/+` または `+/-`）

### plan 出力フォーマット

```
## Plan 結果

| 種類 | 数 | リソース |
|------|-----|----------|
| 🟢 追加 | {N} | {リソース一覧} |
| 🟡 変更 | {N} | {リソース一覧} |
| 🔴 削除 | {N} | {リソース一覧} |
| ⚠️ 再作成 | {N} | {リソース一覧} |

### 変更サマリー

Plan: {add} to add, {change} to change, {destroy} to destroy.

### 破壊的変更（要注意）

{force replacement が発生するリソースがあれば警告}

- `aws_db_instance.main` - force replacement（engine_version の変更）
- ...
```

### 破壊的変更の検出

以下のパターンを検出して警告:

- `# ... must be replaced` - リソースの再作成
- `# ... will be destroyed` - リソースの削除
- `forces replacement` - 属性変更による再作成

```
⚠️ 破壊的変更が検出されました

以下のリソースが再作成または削除されます:
- {リソース名}: {理由}

apply 前に内容を確認してください。
```

---

## Apply 操作

### 重要な安全規則

- ❌ **`-auto-approve` は絶対に使用しない**
- ✅ 必ずユーザー確認を取ってから apply を実行
- ✅ 破壊的変更がある場合は特に注意を促す

### オプション

| オプション | 説明 |
|------------|------|
| `<plan-file>` | plan ファイルを指定して apply |
| `--target <resource>` | 特定リソースのみ apply |

### apply 実行手順

#### 1. plan 実行（plan ファイルがない場合）

plan ファイルが指定されていない場合、先に plan を実行:

```bash
terraform plan -no-color
```

#### 2. 変更内容の確認と警告

plan 結果を解析し、以下を表示:

```
## Apply 確認

### 変更内容

| 種類 | 数 | リソース |
|------|-----|----------|
| 🟢 追加 | {N} | {リソース一覧} |
| 🟡 変更 | {N} | {リソース一覧} |
| 🔴 削除 | {N} | {リソース一覧} |
| ⚠️ 再作成 | {N} | {リソース一覧} |

{破壊的変更がある場合}
### ⚠️ 警告: 破壊的変更

以下のリソースが削除または再作成されます:
- {リソース名}: {理由}

データ損失の可能性があります。十分に確認してください。
```

#### 3. ユーザー確認

**必ずユーザーに確認を求める**:

```
上記の変更を適用してよろしいですか？

- 「はい」または「apply して」で実行
- 「いいえ」または「キャンセル」で中止
```

#### 4. apply 実行

ユーザーの承認後のみ実行:

**plan ファイルなし**:

```bash
terraform apply -no-color
```

インタラクティブに `yes` を入力する必要があるため、ユーザーに案内:

```
terraform apply を実行します。
確認プロンプトで「yes」を入力してください。
```

**plan ファイルあり**:

```bash
terraform apply -no-color <plan-file>
```

plan ファイルからの apply は確認プロンプトなしで実行される。

#### 5. 結果レポート

```
## Apply 完了

### 適用結果

| 種類 | 数 |
|------|-----|
| 追加 | {N} |
| 変更 | {N} |
| 削除 | {N} |

### 出力値

{terraform output の結果（あれば）}

### 次のステップ

- `terraform state list` で作成されたリソースを確認
- `terraform output` で出力値を確認
```

### apply エラー時の対応

#### State ロックエラー

```
Error: Error acquiring the state lock
```

対応:

```
⚠️ State がロックされています

別のプロセスが terraform を実行中の可能性があります。
- 他のターミナルで terraform が実行中でないか確認
- CI/CD パイプラインが実行中でないか確認

どうしても解除が必要な場合:
terraform force-unlock <LOCK_ID>

※ force-unlock は危険な操作です。必ず原因を確認してから実行してください。
```

#### リソース競合エラー

```
Error: Resource already exists
```

対応:

```
⚠️ リソースが既に存在します

対処方法:
1. import で既存リソースを取り込む
2. リソース名を変更して新規作成
3. 既存リソースを削除してから apply

「import して」と言うと import の手順を案内します。
```

---

## Validate 操作

### オプション

| オプション | 説明 |
|------------|------|
| `--fix` | フォーマットの自動修正を実行 |

### validate 実行手順

#### 1. フォーマットチェック

```bash
terraform fmt -check -recursive -diff
```

#### 2. `--fix` 指定時のフォーマット修正

```bash
terraform fmt -recursive -write=true
```

```
## フォーマット修正

以下のファイルを修正しました:
- main.tf
- variables.tf

修正完了
```

#### 3. 構文検証

```bash
terraform validate
```

成功時:

```
Success! The configuration is valid.
```

#### 4. validate 結果レポート

**成功時**:

```
## 検証結果: ✅ 成功

### フォーマット
{フォーマット問題なし / N 件の問題あり}

### 構文検証
✅ 設定は有効です

{--fix なしでフォーマット問題がある場合}
フォーマットを修正するには、自然言語で依頼してください。例:
「Terraform のフォーマットを修正して」「フォーマットを直して」「フォーマットを自動修正して」
```

**エラー時**:

```
## 検証結果: ❌ エラー

### フォーマット
{フォーマットの差分}

### 構文検証
❌ {エラー数} 件のエラー

| ファイル | 行 | エラー |
|----------|-----|--------|
| main.tf | 2 | Missing required argument "ami" |
| ... | ... | ... |

### 修正方法

{エラーごとの修正方法を提案}
```

### validate よくあるエラーと修正方法

| エラー | 原因 | 修正方法 |
|--------|------|----------|
| Missing required argument | 必須属性がない | 属性を追加 |
| Reference to undeclared resource | リソース参照エラー | リソース名を確認 |
| Invalid reference | 参照構文エラー | 構文を確認 |
| Unsupported attribute | 存在しない属性 | プロバイダのドキュメントを確認 |
| Cycle detected | 循環参照 | depends_on を見直し |

---

## その他の操作

**output**:

```bash
terraform output
```

**version**:

```bash
terraform version
```

## 出力フォーマット

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
- ✅ validate は読み取り専用で安全な操作
- ✅ apply は必ずユーザー確認を取る
- ✅ 破壊的変更がある場合は特に慎重に
- ✅ `--out` で plan ファイルを保存すると apply 時に同じ変更が適用される
- ❌ `-auto-approve` は使用しない
- ❌ `destroy` は直接実行しない（ユーザーに手動実行を案内）
- ❌ plan 結果を見ずに apply しない
- ❌ 確認なしで apply を実行しない
