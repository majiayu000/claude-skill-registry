---
name: swagger-ui
description: |
  Swagger UI を用いた OpenAPI ドキュメントの公開・統合を支援するスキル。静的HTML/React/Next.js/サーバー埋め込みの構成を整理し、安全なAPI Explorerを構築する。

  Anchors:
  • OpenAPI Specification / 適用: API仕様互換 / 目的: 定義の一貫性確保
  • Swagger UI Documentation / 適用: UI構成 / 目的: 設定項目の正確な適用
  • OWASP ASVS / 適用: 公開・認証設計 / 目的: セキュリティ要件の確認

  Trigger:
  Use when embedding or publishing Swagger UI, configuring OpenAPI docs, or securing API explorer access.
  swagger ui, openapi docs, api explorer, swagger config, authentication
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Swagger UI

## 概要

OpenAPI 仕様を可視化し、インタラクティブな API Explorer を提供するためのスキル。配布形態とセキュリティ要件を整理し、安定した公開運用を支援する。

詳細は `references/Level1_basics.md` から段階的に参照する。

## ワークフロー

### Phase 1: 統合方式の整理

**目的**: 配布形態とアクセス制御を決定する。

**アクション**:

1. 静的/React/Next.js/サーバー統合の方式を選定する。
2. 認証・CORS・公開範囲の要件を整理する。
3. OpenAPI 互換性を確認する。

### Phase 2: 実装

**目的**: 設定と埋め込みを実装する。

**アクション**:

1. `assets/swagger-ui-standalone.html` または React/Next.js テンプレートを適用する。
2. `assets/swagger-ui-config.json` に設定を反映する。
3. 必要に応じて `scripts/setup-swagger-ui.sh` を実行する。

### Phase 3: 検証

**目的**: UI表示と設定の妥当性を確認する。

**アクション**:

1. `scripts/validate-swagger-config.mjs` で設定を検証する。
2. 認証や公開範囲の動作確認を行う。
3. 公開時の注意点を整理する。

## Task仕様ナビ

| Phase | Task            | 目的                             | 入力           | 出力         |
| ----- | --------------- | -------------------------------- | -------------- | ------------ |
| 1     | 統合方式整理    | 配布形態とセキュリティ要件を整理 | ユーザー要求   | 統合方針メモ |
| 2     | Swagger UI 実装 | UIと設定を整備                   | 統合方針メモ   | 実装結果     |
| 3     | 設定検証        | 設定と公開範囲を検証             | Swagger UI設定 | 検証レポート |

## ベストプラクティス

### すべきこと

- `url` または `urls` を明示して仕様書の場所を固定する。
- 認証方式と公開範囲を事前に決める。
- 本番は CORS と CSP を確認する。
- OpenAPI のバージョン互換性を確認する。

### 避けるべきこと

- 認証なしで社内APIを公開しない。
- 設定ファイルの未検証のまま公開しない。
- 仕様書と UI の不整合を放置しない。

## リソース/スクリプト参照

### references/

- `references/Level1_basics.md`: 基礎指針
- `references/Level2_intermediate.md`: 実務パターン
- `references/Level3_advanced.md`: 高度な設計指針
- `references/Level4_expert.md`: 専門領域の注意点
- `references/integration-options.md`: 統合方式比較
- `references/security-hardening.md`: セキュリティ設計
- `references/openapi-compatibility.md`: OpenAPI互換性
- `references/swagger-ui-configuration.md`: Swagger UI設定
- `references/cicd-integration.md`: CI/CD統合
- `references/redoc-configuration.md`: ReDoc比較

### assets/

- `assets/swagger-ui-standalone.html`: スタンドアロンテンプレート
- `assets/swagger-ui-react.tsx`: Reactテンプレート
- `assets/swagger-ui-nextjs.tsx`: Next.jsテンプレート
- `assets/swagger-ui-config.json`: 設定ファイル
- `assets/swagger-config.json`: 追加設定例

### scripts/

- `scripts/validate-swagger-config.mjs`: 設定検証
- `scripts/setup-swagger-ui.sh`: セットアップ補助

## 変更履歴

| Version | Date       | Changes                               |
| ------- | ---------- | ------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md 仕様に準拠した構造へ更新 |
