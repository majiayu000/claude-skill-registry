---
name: error-message-design
description: |
  ユーザーフレンドリーなエラーメッセージの設計を専門とするスキル。
  エラーコード体系、多言語対応（i18n）、アクション指向のメッセージ設計を提供。

  Anchors:
  - The Pragmatic Programmer / 適用: 実践的改善 / 目的: 品質維持
  - Nielsen Norman Group UX Guidelines / 適用: エラーメッセージ設計 / 目的: ユーザビリティ向上

  Trigger:
  Use when designing error messages, creating error code systems, implementing i18n for errors, or building user-friendly error responses.
  error message, error code, i18n, user-friendly, validation error, API error response
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Error Message Design

## 概要

ユーザーフレンドリーなエラーメッセージの設計を専門とするスキル。
エラーコード体系、多言語対応（i18n）、アクション指向のメッセージ設計を
通じて、ユーザー体験を向上させる。

## ワークフロー

### Phase 1: エラーメッセージ設計

**目的**: エラータイプを分類し、メッセージを設計する

**アクション**:

1. エラー発生シナリオを分析
2. エラーコード体系を設計
3. ユーザー向けメッセージを作成
4. 多言語対応を考慮

**Task**: `agents/design-error-messages.md` を参照

### Phase 2: エラーシステム実装

**目的**: 設計に基づきエラーシステムを実装する

**アクション**:

1. エラークラス/型を定義
2. メッセージカタログを実装
3. i18n翻訳リソースを作成
4. エラーハンドラーを実装

**Task**: `agents/implement-error-messages.md` を参照

### Phase 3: 検証と記録

**目的**: エラーメッセージの品質を検証する

**アクション**:

1. `scripts/validate-error-messages.mjs` で検証
2. ユーザビリティチェックを実施
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                     | 起動タイミング | 入力                 | 出力                 |
| ------------------------ | -------------- | -------------------- | -------------------- |
| design-error-messages    | 設計時         | エラー要件           | エラーメッセージ仕様 |
| implement-error-messages | 実装時         | エラーメッセージ仕様 | エラーシステム実装   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## エラーメッセージの3原則

### 1. 何が起きたかを説明

**悪い例**: "Error occurred"
**良い例**: "Your session has expired"

### 2. なぜ起きたかを説明

**悪い例**: "Invalid input"
**良い例**: "The email address format is incorrect"

### 3. どうすれば解決できるかを説明

**悪い例**: "Please try again"
**良い例**: "Please enter a valid email (example: user@domain.com)"

## ベストプラクティス

### すべきこと

- ユーザーが理解できる言葉を使用
- 具体的なアクションを提示
- エラーコードで問い合わせを容易に
- 多言語対応を考慮した設計

### 避けるべきこと

- 技術用語の露出（SQLException, NullPointer等）
- スタックトレースの表示
- ユーザーを責める表現
- 曖昧な表現（「問題が発生しました」）

## リソース参照

### agents/（Task仕様書）

| Task | パス                                                                         | 用途           |
| ---- | ---------------------------------------------------------------------------- | -------------- |
| 設計 | See [agents/design-error-messages.md](agents/design-error-messages.md)       | メッセージ設計 |
| 実装 | See [agents/implement-error-messages.md](agents/implement-error-messages.md) | システム実装   |

### references/（詳細知識）

| リソース           | パス                                                                             | 用途               |
| ------------------ | -------------------------------------------------------------------------------- | ------------------ |
| ユーザーメッセージ | See [references/user-friendly-messages.md](references/user-friendly-messages.md) | メッセージ設計指針 |
| エラーコード体系   | See [references/error-code-system.md](references/error-code-system.md)           | コード設計         |
| i18n対応           | See [references/i18n-error-handling.md](references/i18n-error-handling.md)       | 多言語対応         |
| APIレスポンス      | See [references/api-error-responses.md](references/api-error-responses.md)       | レスポンス形式     |

### scripts/（決定論的処理）

| スクリプト                    | 用途               | 使用例                                        |
| ----------------------------- | ------------------ | --------------------------------------------- |
| `validate-error-messages.mjs` | メッセージ検証     | `node scripts/validate-error-messages.mjs`    |
| `log_usage.mjs`               | フィードバック記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート               | 用途                           |
| -------------------------- | ------------------------------ |
| `error-system-template.ts` | エラーシステム実装テンプレート |

## 変更履歴

| Version | Date       | Changes                                            |
| ------- | ---------- | -------------------------------------------------- |
| 2.0.0   | 2026-01-01 | agents追加、Level1-4削除、18-skills.md仕様完全準拠 |
| 1.0.0   | 2025-12-24 | 初版作成                                           |
