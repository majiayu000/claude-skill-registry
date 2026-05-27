---
name: codex
description: OpenAI Codex CLIを使用したコードレビュー、分析、コードベースへの質問を実行する。使用場面: (1) PRセルフレビュー、(2) コードベース全体の分析、(3) 実装に関する質問、(4) バグの調査、(5) リファクタリング提案。トリガー: "codex", "コードレビュー", "レビューして", "分析して", "/codex"
---

# Codex

OpenAI Codex CLIを使用してコードレビュー・分析を実行するスキル。

## 実行コマンド

```bash
codex exec --full-auto --sandbox read-only --cd <project_directory> "<request>"
```

## パラメータ

| パラメータ | 説明 |
|-----------|------|
| `--full-auto` | 完全自動モードで実行 |
| `--sandbox read-only` | 読み取り専用サンドボックス（安全な分析用） |
| `--cd <dir>` | 対象プロジェクトのディレクトリ |
| `"<request>"` | 依頼内容（日本語可） |

## 使用例

### PRセルフレビュー（主要ユースケース）

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "このPRの変更をレビューして、以下の観点で問題を指摘してください：
- 型安全性（any型、型アサーション）
- セキュリティ（OWASP Top 10）
- テストの有無
- コード規約違反
指摘は🔴必須/🟡推奨/💡提案に分類してください"
```

### コード分析

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "このプロジェクトのコードをレビューして、改善点を指摘してください"
```

### バグ調査

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "認証処理でエラーが発生する原因を調査してください"
```

### リファクタリング提案

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "このコンポーネントのリファクタリング案を提案してください"
```

## PRセルフレビューとしての使用

PR作成後のセルフレビューでは、以下の手順で実行する：

### 1. PR差分の確認

```bash
gh pr diff
```

### 2. Codexでレビュー実行

```bash
codex exec --full-auto --sandbox read-only --cd $(pwd) "このPRの変更をレビューして、CLAUDE.mdの品質基準に照らして問題を指摘してください。
指摘は以下に分類してください：
- 🔴必須: セキュリティ問題、any型使用、テスト欠如、ESLintエラー
- 🟡推奨: 型アサーションの改善、命名規則違反、パフォーマンス改善
- 💡提案: リファクタリング提案、より良いパターン"
```

### 3. 指摘への対応

| 分類 | 対応 |
|------|------|
| 🔴必須 | 必ず修正 |
| 🟡推奨 | 可能な限り修正 |
| 💡提案 | 任意で検討 |

🔴必須・🟡推奨の指摘がなくなるまで修正を繰り返す（最大3回）

## 実行手順

1. ユーザーから依頼内容を受け取る
2. 対象プロジェクトのディレクトリを特定する（デフォルト: 現在のworktree）
3. 上記コマンド形式でCodexを実行
4. 結果をユーザーに報告

## 注意事項

- `--sandbox read-only` により、コードの変更は行われない（安全）
- 結果は読み取り専用で分析結果のみ出力
- 日本語でのリクエストに対応
- 大規模なコードベースでも効率的に分析可能
