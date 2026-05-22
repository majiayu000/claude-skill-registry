---
name: api-documentation-best-practices
description: |
  OpenAPI、Swagger、RESTful APIドキュメンテーションのベストプラクティスを提供する専門スキル。

  Anchors:
  • 『RESTful Web APIs』（Leonard Richardson）/ 適用: REST APIドキュメンテーション / 目的: リソース設計とHTTP操作の標準化

  Trigger:
  OpenAPI/Swagger定義設計時、APIエンドポイント仕様書作成時、REST APIドキュメント整備時、認証仕様文書化時、エラーレスポンス標準化時、ドキュメントレビュー時に使用

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# API Documentation Best Practices

## 概要

OpenAPI、Swagger、RESTful APIドキュメンテーションのベストプラクティスを提供する専門スキル。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要な references/scripts/templates を特定

**Task**: `agents/analyze-documentation-context.md` を参照

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す

**Task**: `agents/create-documentation.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す

**Task**: `agents/validate-documentation.md` を参照

## Task仕様ナビ

| 種類                        | 説明                                                | リソース                                  | テンプレート                   |
| :-------------------------- | :-------------------------------------------------- | :---------------------------------------- | :----------------------------- |
| **基礎知識**                | OpenAPIドキュメンテーションの基本概念と設計パターン | `references/Level1_basics.md`             | -                              |
| **実装ガイド**              | RESTful API仕様書作成の実務テクニック               | `references/Level2_intermediate.md`       | `assets/endpoint-template.md`  |
| **応用手法**                | 複雑なAPI設計と高度なドキュメンテーション           | `references/Level3_advanced.md`           | -                              |
| **専門知識**                | API設計のエキスパートレベルの考察                   | `references/Level4_expert.md`             | -                              |
| **認証設計**                | OAuth2、JWT等の認証フロー文書化                     | `references/authentication-docs.md`       | -                              |
| **エンドポイント設計**      | リソース設計とHTTP操作の標準化                      | `references/endpoint-design.md`           | `assets/endpoint-template.md`  |
| **エラー定義**              | エラーレスポンスとステータスコード管理              | `references/error-documentation.md`       | -                              |
| **OpenAPI詳細**             | OpenAPI 3.x仕様の詳細ガイド                         | `references/openapi-guide.md`             | `assets/openapi-template.yaml` |
| **リクエスト/レスポンス例** | 実践的な例とサンプルコード                          | `references/request-response-examples.md` | -                              |
| **要求仕様索引**            | 要求仕様書との同期状態確認                          | `references/requirements-index.md`        | -                              |

## ベストプラクティス

### すべきこと

- REST APIの仕様書を作成する時は、リソース指向の設計原則に従う
- OpenAPI/Swagger定義を設計する時は、`references/openapi-guide.md` の標準フォーマットを参照する
- APIエンドポイントの詳細仕様を文書化する時は、`assets/endpoint-template.md` を使用する
- 認証フローを説明する時は、`references/authentication-docs.md` で推奨パターンを確認する
- エラーレスポンスを定義する時は、統一されたステータスコードとエラー構造を使用する
- リクエスト/レスポンス例は実際の運用ケースに基づいて作成する
- ドキュメントはバージョン管理対象とし、API変更時に同期を保つ

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける
- 認証仕様を不完全なまま進める（セキュリティリスク）
- エラー定義を曖昧にして、クライアント側の実装を困難にする
- OpenAPI仕様を部分的にしか定義しない（生成ツールやSDK生成が失敗する）
- レガシーな仕様書を放置する（古い情報が蔓延する）
- サンプルコードを更新しないまま放置する（実装と乖離する）
- HTTP操作の語義（GET/POST等）を無視した設計をする

## リソース参照

### 📚 学習リソース

| レベル            | 説明                   | ファイル                            |
| :---------------- | :--------------------- | :---------------------------------- |
| **レベル1: 基礎** | 基本的な概念と用語     | `references/Level1_basics.md`       |
| **レベル2: 実務** | 実装に必要な知識       | `references/Level2_intermediate.md` |
| **レベル3: 応用** | 応用的な手法と最適化   | `references/Level3_advanced.md`     |
| **レベル4: 専門** | エキスパート向けの考察 | `references/Level4_expert.md`       |

### 🔧 スクリプトツール

```bash
# OpenAPI仕様のバリデーション
node .claude/skills/api-documentation-best-practices/scripts/validate-openapi.mjs <openapi-file>

# スキル構造の検証
node .claude/skills/api-documentation-best-practices/scripts/validate-skill.mjs

# 使用記録と自動評価
node .claude/skills/api-documentation-best-practices/scripts/log_usage.mjs --help
```

### 📋 テンプレート

- `assets/endpoint-template.md` - エンドポイント仕様書テンプレート
- `assets/openapi-template.yaml` - OpenAPI 3.0.3定義テンプレート

### 📖 参考書籍

- 『RESTful Web APIs』（Leonard Richardson著）
  - リソース設計の原則
  - HTTP操作の正しい使い方
  - ステートレス設計のベストプラクティス

## 変更履歴

| Version | Date       | Changes                                                                                                                         |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 3.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加、name修正                                                                           |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様へ完全移行: YAML frontmatter (Anchors/Triggers/allowed-tools)、Task仕様ナビテーブル、リソース参照セクション拡充 |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added                                                                                     |
