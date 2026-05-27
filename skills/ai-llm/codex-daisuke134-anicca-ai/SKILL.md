---
name: codex
description: "OpenAI Codex CLI（read-only sandbox）を汎用セカンドオピニオンとして実行する。Use when 設計相談、バグ調査、コードレビュー、文章校閲、セカンドオピニオンが必要な場面。キーワード: codex, codexに聞いて, セカンドオピニオン, 別視点."
---

# Codex 汎用セカンドオピニオン

Codex CLI を read-only sandbox で実行し、OpenAI 側のセカンドオピニオンを得る。
Claude のレート制限に影響しない（OpenAI トークンを消費）。

## codex-review との違い

| スキル | 用途 | 反復修正 |
|--------|------|---------|
| `/codex`（本スキル） | 汎用相談（設計・バグ・校閲） | なし（1回実行） |
| `/codex-review` | レビューゲート（blocking/advisory） | あり（ok: true まで反復） |

## 実行コマンド

```bash
codex exec --full-auto --sandbox read-only --cd "$(pwd)" "<相談内容>"
```

| パラメータ | 役割 |
|-----------|------|
| `--full-auto` | 確認なしで自動実行 |
| `--sandbox read-only` | 読み取り専用（ファイル変更しない） |
| `--cd "$(pwd)"` | 現在のプロジェクトディレクトリを対象 |

## 4つのモード

ユーザーの依頼内容に応じて、適切なプロンプトを構成して実行する。

### 1. コードレビュー

```bash
codex exec --full-auto --sandbox read-only --cd "$(pwd)" \
  "以下のファイルをレビューし、改善点を指摘せよ: <ファイルパス>"
```

### 2. 設計相談

```bash
codex exec --full-auto --sandbox read-only --cd "$(pwd)" \
  "以下の設計について意見を述べよ。代替案があれば提示せよ: <設計内容>"
```

### 3. バグ調査

```bash
codex exec --full-auto --sandbox read-only --cd "$(pwd)" \
  "以下のエラーの原因を調査し、修正案を提示せよ: <エラー内容>"
```

### 4. 文章校閲

```bash
codex exec --full-auto --sandbox read-only --cd "$(pwd)" \
  "以下のファイルの文章を校閲し、改善点を指摘せよ: <ファイルパス>"
```

## 使用例

```
/codex この設計で問題ないかレビューして
/codex src/auth.ts をセキュリティの観点でチェックして
/codex このエラーの原因を調べて: TypeError: Cannot read property 'id' of undefined
/codex この記事を校閲して: articles/draft.md
```

## 注意事項

| 項目 | 内容 |
|------|------|
| 安全性 | read-only sandbox のためファイル変更なし |
| コスト | OpenAI API トークンを消費（Claude 側は消費しない） |
| 前提 | `codex` CLI がインストール済みであること |
| 出力 | 自由形式（codex-review のような JSON スキーマは不要） |
