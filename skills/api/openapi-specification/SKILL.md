---
name: openapi-specification
description: |
  OpenAPI仕様の専門スキル。
  API定義、スキーマ設計、ドキュメント生成を提供します。

  Anchors:
  • 『OpenAPI Specification』（Linux Foundation） / 適用: API仕様設計 / 目的: REST API標準化
  • 『RESTful API設計のベストプラクティス』（複数出典） / 適用: エンドポイント設計 / 目的: 一貫性確保

  Trigger:
  OpenAPI仕様書作成時、API定義ドキュメント作成時、Swagger仕様設計時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# OpenAPI Specification スキル

## 概要

OpenAPI 3.x仕様に準拠したAPI仕様書の設計と作成を専門とするスキル。RESTful APIの設計原則に基づいて、セキュアで保守性の高いAPI仕様書を作成します。エンドポイント設計、スキーマ定義、認証・認可設定、エラーハンドリング、およびドキュメント生成を統合的に実施します。

詳細な手順や背景は `references/` ディレクトリを参照してください。

## ワークフロー

### Phase 1: 要件定義

**目的**: API仕様の要件を明確化

**アクション**:

1. `references/basics.md` でOpenAPI基本構造を確認
2. エンドポイント数、認証方式、レート制限を定義
3. 既存API仕様の有無を確認（更新か新規作成か判定）

### Phase 2: 仕様設計

**目的**: OpenAPI仕様書を設計・作成

**アクション**:

1. `agents/design-api.md` を参照して設計を実施
2. `assets/openapi-base-template.yaml` をベースに仕様書を作成
3. `references/schema-design-patterns.md` でスキーマ設計
4. `references/security-schemes.md` でセキュリティ構成

**Task**: `agents/design-api.md` を参照

### Phase 3: 検証

**目的**: 仕様書の検証と記録

**アクション**:

1. `agents/validate-spec.md` を参照して検証を実施
2. `scripts/validate-openapi.mjs` で構文チェック
3. セキュリティ設定とベストプラクティスを確認

**Task**: `agents/validate-spec.md` を参照

## Task仕様（ナビゲーション）

| Task          | 起動タイミング | 入力           | 出力           |
| ------------- | -------------- | -------------- | -------------- |
| design-api    | Phase 2開始時  | API要件        | 仕様書ドラフト |
| validate-spec | Phase 3開始時  | 仕様書ドラフト | 検証済み仕様書 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **新規OpenAPI仕様書を作成する時**: `openapi-base-template.yaml` をテンプレートとして使用し、info、servers、paths、componentsの全セクションを網羅する
- **既存OpenAPI仕様書を更新する時**: 変更前後の仕様差異を明確にし、破壊的変更がないか検証する
- **エンドポイントやスキーマを設計する時**: `schema-design-patterns.md` と `openapi-structure.md` を参照して一貫性を保つ
- **OpenAPI構文エラーを解決する時**: `validate-openapi.mjs` で具体的なエラー箇所を特定してから修正する
- **セキュリティスキームを設定する時**: `security-schemes.md` のベストプラクティスを遵守し、全エンドポイントに適切な認証を適用する
- **Level別の学習**: 基礎（Level1）→実務（Level2）→応用（Level3）→専門（Level4）の順で進める
- **版管理**: API仕様の更新履歴をCHANGELOG.mdで記録し、ユーザーに影響を通知する

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける
- セキュリティスキーム設定を後付けしない（設計段階から組み込む）
- 複数のエンドポイント間で不一貫なスキーマ定義を避ける
- エラーレスポンスの定義をスキップしない
- `required` フィールドの指定を曖昧にしない
- セキュリティ関連の設定をハードコード化しない（環境ごとに切り替え可能にする）
- OpenAPI仕様の検証をスキップして本番環境にデプロイしない

## リソース参照

### references/（詳細知識）

| リソース         | パス                                                                             | 用途             |
| ---------------- | -------------------------------------------------------------------------------- | ---------------- |
| 基礎知識         | See [references/basics.md](references/basics.md)                                 | OpenAPI基本構造  |
| 構造ガイド       | See [references/openapi-structure.md](references/openapi-structure.md)           | 全セクション仕様 |
| スキーマパターン | See [references/schema-design-patterns.md](references/schema-design-patterns.md) | スキーマ設計     |
| セキュリティ     | See [references/security-schemes.md](references/security-schemes.md)             | 認証・認可設定   |

### assets/（テンプレート）

| リソース           | パス                                | 用途         |
| ------------------ | ----------------------------------- | ------------ |
| ベーステンプレート | `assets/openapi-base-template.yaml` | 仕様書ベース |
| エンドポイント     | `assets/endpoint-template.yaml`     | 個別パス定義 |

## 変更履歴

| Version | Date       | Changes                      |
| ------- | ---------- | ---------------------------- |
| 1.2.0   | 2026-01-02 | agents/追加、Level構造を統合 |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様に準拠       |
| 1.0.0   | 2025-12-24 | 初期実装                     |
