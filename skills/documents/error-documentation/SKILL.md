---
name: error-documentation
description: |
  Comprehensive error documentation patterns for APIs, libraries, and systems.
  Covers error catalogs, troubleshooting guides, recovery procedures, and
  runbook creation to improve developer experience and reduce support burden.

  Anchors:
  • The Pragmatic Programmer (Hunt, Thomas) / 適用: error communication / 目的: clear actionable messages
  • Site Reliability Engineering (Google) / 適用: runbook patterns / 目的: operational excellence
  • API Design Patterns (JJ Geewax) / 適用: error response design / 目的: consistent error contracts

  Trigger:
  Use when documenting API errors, creating error catalogs, writing troubleshooting guides,
  designing runbooks, standardizing error responses, improving error discoverability.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Error Documentation

## 概要

エラードキュメンテーションの包括的なパターンとベストプラクティスを提供するスキル。
API、ライブラリ、システムのエラーカタログ、トラブルシューティングガイド、
リカバリー手順、ランブックの作成を通じて、開発者体験を向上させます。

## ワークフロー

### Phase 1: 分析と計画

**目的**: エラードキュメンテーションの範囲と要件を明確にする

**Task**: `agents/analysis-task.md` を参照

**入力**:

- システム/API仕様
- 既存エラー実装コード
- ユーザーフィードバック/サポートチケット

**出力**:

- エラータイプの分類
- ドキュメンテーション範囲の決定
- 優先順位付けされたエラーリスト

**アクション**:

1. `references/error-catalog-patterns.md` でエラードキュメンテーションの基礎を確認
2. システムの全エラー発生箇所を特定
3. エラーの重要度と頻度を評価

### Phase 2: エラーカタログ作成

**目的**: 構造化されたエラーカタログを作成する

**Task**: `agents/catalog-creation-task.md` を参照

**入力**:

- Phase 1のエラーリスト
- エラーコード体系
- 既存ドキュメント

**出力**:

- 統一されたエラーカタログ
- エラーコード索引
- カテゴリー別エラーリスト

**アクション**:

1. `references/error-catalog-patterns.md` でカタログ構造パターンを学習
2. `assets/error-catalog-template.md` をベースに作成
3. 各エラーに対して統一フォーマットで記述

### Phase 3: トラブルシューティングガイド作成

**目的**: 実用的なトラブルシューティング手順を文書化する

**Task**: `agents/troubleshooting-task.md` を参照

**入力**:

- エラーカタログ
- 過去のサポート事例
- 一般的な問題パターン

**出力**:

- トラブルシューティングガイド
- 診断フローチャート
- FAQセクション

**アクション**:

1. `references/error-catalog-patterns.md` で診断パターンを確認
2. トラブルシューティングガイドを作成
3. 診断フローを設計

### Phase 4: ランブック作成

**目的**: オペレーショナルな対応手順を標準化する

**Task**: `agents/runbook-task.md` を参照

**入力**:

- クリティカルエラーリスト
- エスカレーションポリシー
- インシデント対応履歴

**出力**:

- エラー対応ランブック
- エスカレーションフロー
- 復旧手順書

**アクション**:

1. `references/error-catalog-patterns.md` でランブックパターンを確認
2. 運用ランブックを作成
3. エスカレーションフローを設計

### Phase 5: 検証と改善

**目的**: ドキュメントの品質を確保し継続的改善を行う

**アクション**:

1. ドキュメント構造を検証
2. 網羅性チェック（全エラーコードがドキュメント化されているか）
3. リンク切れチェック
4. `scripts/log_usage.mjs` で使用状況を記録

## Task仕様ナビゲーション

### 分析タスク

- **ファイル**: `agents/analysis-task.md`
- **役割**: システムアーキテクト
- **入力**: システム仕様、エラーコード
- **出力**: エラー分類、ドキュメント計画
- **参照**: `references/error-classification.md`

### カタログ作成タスク

- **ファイル**: `agents/catalog-creation-task.md`
- **役割**: テクニカルライター
- **入力**: エラーリスト、コード体系
- **出力**: エラーカタログ
- **参照**: `references/catalog-structures.md`

### トラブルシューティングタスク

- **ファイル**: `agents/troubleshooting-task.md`
- **役割**: サポートエンジニア
- **入力**: エラーカタログ、サポート事例
- **出力**: トラブルシューティングガイド
- **参照**: `references/diagnostic-patterns.md`

### ランブック作成タスク

- **ファイル**: `agents/runbook-task.md`
- **役割**: SREエンジニア
- **入力**: クリティカルエラー、対応履歴
- **出力**: 運用ランブック
- **参照**: `references/sre-runbook-patterns.md`

## ベストプラクティス

### すべきこと

- 各エラーに一意のコードを割り当てる
- エラーメッセージは「何が起きたか」「なぜ起きたか」「どう対処するか」を含める
- 検索可能なキーワードを含める
- 実際のエラー例を提供する
- 関連エラーへのクロスリファレンスを設置
- 頻度の高いエラーを優先的にドキュメント化
- 定期的にドキュメントを更新

### 避けるべきこと

- 技術用語だけの説明（コンテキストを提供）
- 「エラーが発生しました」のような曖昧な表現
- 解決策のないエラー説明
- 古いエラーコードの放置
- 一貫性のないフォーマット
- ユーザー視点の欠如

## リソース参照

### references/（詳細知識）

| リソース                    | 用途                         |
| --------------------------- | ---------------------------- |
| `error-catalog-patterns.md` | エラーカタログ構造とパターン |

### scripts/（決定論的処理）

| スクリプト      | 用途               | 使用例                                                          |
| --------------- | ------------------ | --------------------------------------------------------------- |
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 5"` |

### assets/（テンプレート）

| テンプレート                | 用途                       |
| --------------------------- | -------------------------- |
| `error-catalog-template.md` | エラーカタログテンプレート |

## メトリクスと改善

スキルの使用状況は `LOGS.md` に記録されます。
メトリクスの詳細は `EVALS.json` を参照してください。

### 主要メトリクス

- エラーカタログの網羅率
- トラブルシューティング成功率
- ドキュメント参照頻度
- サポートチケット削減率

## 変更履歴

| Version | Date       | Changes                                |
| ------- | ---------- | -------------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、Level1-4削除 |
| 1.0.0   | 2025-12-31 | 初版作成                               |
