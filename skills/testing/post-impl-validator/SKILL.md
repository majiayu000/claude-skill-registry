---
name: post-impl-validator
description: |
  実装完了後のテスト、lint、ベストプラクティスレビューを自動実行するスキル。
  以下の状況で使用:
  (1) ユーザーが「実装完了」「完了」「できた」「終わった」「実装した」などと発言した時
  (2) ユーザーが明示的に「/post-impl-validator」を実行した時
  (3) ファイル編集後に「コミットして」「PRを作成」などと依頼された時
---

# Post-Implementation Validator

実装完了後のテスト、lint、ベストプラクティスレビューを自動実行する。

## ワークフロー

1. 変更ファイル検出 → `scripts/detect-changes.sh` を実行
2. プロジェクト判定 → パスパターンから適用ツールを決定
3. Lint実行 → エラー時は自動修正を試行（最大3回）
4. テスト実行 → 失敗時は修正を提案
5. ベストプラクティスレビュー → references/ を参照してチェック

## プロジェクト別コマンドマッピング

### Go

- パスパターン: `**/*.go`
- テスト: デフォルトは `go test -shuffle on -race -cover ./...`
- Lint: デフォルトは `go vet ./...`
- 自動修正: デフォルトは非対応（手動修正が必要）
- ベストプラクティス: `references/go-best-practices.md` を参照

**環境変数でカスタムコマンドを指定可能:**
- `GO_TEST_CMD`: テストコマンド（例: `make test`）
- `GO_TEST_FLAGS`: テストフラグ（GO_TEST_CMD未指定時のみ有効）
- `GO_LINT_CMD`: Lintコマンド（例: `golangci-lint run`）
- `GO_FIX_CMD`: 自動修正コマンド（例: `gofmt -w . && goimports -w .`）

### TypeScript/React

- パスパターン: `**/*.{ts,tsx}`
- テスト: package.json から自動検出、または環境変数で指定
- Lint: package.json から自動検出、または環境変数で指定
- 自動修正: package.json から自動検出、または環境変数で指定
- ベストプラクティス: `references/typescript-react-best-practices.md` を参照

**環境変数でカスタムコマンドを指定可能:**
- `TS_TEST_CMD`: テストコマンド（例: `pnpm test`）
- `TS_LINT_CMD`: Lintコマンド（例: `pnpm run lint`）
- `TS_FIX_CMD`: 自動修正コマンド（例: `pnpm run lint:fix`）

### Terraform

- パスパターン: `**/*.tf`
- テスト: デフォルトは `terraform validate`
- Lint: デフォルトは `terraform fmt -check -recursive`
- 自動修正: デフォルトは `terraform fmt -recursive`
- ベストプラクティス: `references/terraform-best-practices.md` を参照

**環境変数でカスタムコマンドを指定可能:**
- `TF_TEST_CMD`: テストコマンド（例: `terratest`）
- `TF_LINT_CMD`: Lintコマンド（例: `tflint`）
- `TF_FIX_CMD`: 自動修正コマンド（例: `terraform fmt -recursive`）

## 自動修正ループ

エラー発生時の自動修正フロー:

1. 自動修正コマンドを実行
2. Lint/テストを再実行
3. 成功すれば終了、失敗なら1に戻る
4. 最大3回リトライ後、ユーザーに手動対応を依頼

## 処理順序

複数プロジェクトに変更がある場合、以下の順序で処理:

1. Terraform (インフラ) - 最優先
2. Go (バックエンド)
3. TypeScript/React (フロントエンド)

## 出力形式

### 成功時

```
## Post-Implementation Validator 結果

### テスト: PASS
- 全 X テストがパス

### Lint: PASS
- エラーなし

### ベストプラクティス: PASS
- 全項目クリア
```

### 問題検出時

```
## Post-Implementation Validator 結果

### テスト: FAIL
- 失敗テスト: X件
- [エラー詳細]

### Lint: FAIL (自動修正済み)
- 修正ファイル: X件

### ベストプラクティス: WARNING
- [ ] 問題1
- [ ] 問題2

### 推奨アクション
1. ...
```

## スクリプト

- `scripts/detect-changes.sh` - 変更ファイルを検出しJSON形式で出力
- `scripts/run-lint.sh <project> <workdir>` - プロジェクト別にLint実行
- `scripts/run-tests.sh <project> <workdir>` - プロジェクト別にテスト実行
- `scripts/auto-fix.sh <project> <workdir>` - 自動修正を試行

## ベストプラクティス参照

変更ファイルの言語/フレームワークに応じて以下を参照:

- **Go**: `references/go-best-practices.md`
- **TypeScript/React**: `references/typescript-react-best-practices.md`
- **Terraform**: `references/terraform-best-practices.md`
