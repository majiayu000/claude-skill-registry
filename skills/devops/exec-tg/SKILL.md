---
name: exec-tg
description: Terragrunt コマンドを実行する。「terragrunt run-all」「tg plan-all」「tg apply-all」「terragrunt init」「tg init」「terragrunt して」「tg plan」「run-all apply」「モジュール一括適用」「terragrunt 実行」などで起動。
allowed-tools: [Bash, Read]
---

# Terragrunt Executor

Terragrunt コマンドの実行を支援します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| 初期化 | 「tg init」「terragrunt init」 | `terragrunt init` |
| 計画 | 「tg plan」「terragrunt plan」 | `terragrunt plan` |
| 適用 | 「tg apply」「terragrunt apply」 | `terragrunt apply` |
| 一括初期化 | 「run-all init」「全体 init」 | `terragrunt run-all init` |
| 一括計画 | 「run-all plan」「全体 plan」 | `terragrunt run-all plan` |
| 一括適用 | 「run-all apply」「全体 apply」 | `terragrunt run-all apply` |
| 依存グラフ | 「依存関係」「graph」 | `terragrunt graph-dependencies` |
| 出力確認 | 「output」「出力確認」 | `terragrunt output` |

## 実行手順

### 1. 意図の判定

ユーザーの発話から操作を判定:

- **単一モジュール**: 「tg plan」「terragrunt apply」→ 単一モジュール操作
- **複数モジュール**: 「run-all」「全体」「一括」→ `run-all` 操作
- **依存関係**: 「依存」「graph」→ `graph-dependencies`

### 2. 事前確認

```bash
# Terragrunt バージョン確認
terragrunt --version

# terragrunt.hcl の存在確認
ls terragrunt.hcl 2>/dev/null || ls **/terragrunt.hcl 2>/dev/null
```

### 3. コマンド実行

**単一モジュール**:

```bash
# init
terragrunt init

# plan
terragrunt plan

# apply（ユーザー確認後）
terragrunt apply
```

**複数モジュール（run-all）**:

```bash
# init
terragrunt run-all init

# plan
terragrunt run-all plan

# apply（ユーザー確認後）
terragrunt run-all apply
```

**依存関係の確認**:

```bash
terragrunt graph-dependencies
```

### 4. 出力フォーマット

```
## Terragrunt 実行結果

### コマンド
terragrunt {command}

### 対象モジュール
{モジュール一覧（run-all の場合）}

### 結果
{コマンドの出力}

### サマリー
{成功/失敗と簡潔な説明}
```

## run-all の注意事項

`run-all` は複数のモジュールを一括で操作するため:

- ✅ `run-all plan` で全体の変更内容を確認
- ✅ 依存関係に基づいて適切な順序で実行される
- ❌ `run-all apply` は本番環境では慎重に
- ❌ `run-all destroy` は直接実行しない

## 注意事項

- ✅ plan は安全な読み取り操作
- ✅ apply は必ずユーザー確認を取る
- ❌ `-auto-approve` は使用しない
- ❌ `destroy` / `run-all destroy` は直接実行しない
