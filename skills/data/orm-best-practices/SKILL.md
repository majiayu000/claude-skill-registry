---
name: orm-best-practices
description: |
  ORMベストプラクティスの専門スキル。Drizzle ORMを活用したエンティティ設計、リレーション管理、パフォーマンス最適化を提供します。

  Anchors:
  • Designing Data-Intensive Applications (Martin Kleppmann) / 適用: データモデリング / 目的: 型安全なスキーマ定義とパフォーマンス最適化
  • Drizzle ORM Documentation / 適用: TypeScript ORM / 目的: 型推論とクエリビルダーの活用
  • High Performance MySQL (Baron Schwartz) / 適用: クエリ最適化 / 目的: N+1問題とインデックス戦略

  Trigger:
  Use when defining Drizzle ORM schemas, mapping entity relationships, optimizing database queries, solving N+1 problems, or implementing type-safe data access patterns.
  ORM, Drizzle, schema, relation, N+1, query builder, type-safe, entity mapping

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# ORM Best Practices

## 概要

Drizzle ORMを活用したデータベース操作のベストプラクティスを提供するスキル。型安全なスキーマ定義、クエリビルダーの効果的な使用、パフォーマンスを考慮した実装パターンを提供します。このスキルはデータベース設計段階から運用まで、ORMの最適な活用方法をガイドします。

詳細な手順や背景は `references/basics.md` を参照してください。

## ワークフロー

### Phase 1: スキーマ設計

**目的**: 型安全なスキーマ定義とリレーション設計

**アクション**:

1. `references/basics.md` でDrizzle ORM基礎を確認
2. `references/schema-definition.md` でテーブル定義パターンを参照
3. `references/relation-mapping.md` でリレーション設計を検討

**Task**: `agents/design-schema.md` を参照

### Phase 2: クエリ実装

**目的**: パフォーマンスを考慮したクエリ構築

**アクション**:

1. `references/query-builder-patterns.md` でクエリパターンを確認
2. `references/performance-patterns.md` でN+1問題対策を検討
3. 型安全なクエリビルダーを実装

**Task**: `agents/implement-queries.md` を参照

### Phase 3: 検証と最適化

**目的**: スキーマとクエリの品質確保

**アクション**:

1. `scripts/validate-schema.mjs` でスキーマの型安全性を確認
2. インデックス戦略とクエリ計画を検証
3. `scripts/log_usage.mjs` を実行して使用記録を保存

**Task**: `agents/validate-optimize.md` を参照

## Task仕様（ナビゲーション）

| Task              | 起動タイミング | 入力           | 出力                 |
| ----------------- | -------------- | -------------- | -------------------- |
| design-schema     | Phase 1開始時  | テーブル要件   | スキーマ定義コード   |
| implement-queries | Phase 2開始時  | スキーマ定義   | クエリ実装コード     |
| validate-optimize | Phase 3開始時  | 実装済みコード | 検証・最適化レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- **スキーマ設計**: テーブルリレーションと外部キー制約を明確に定義してから実装を開始
- **型安全性**: Drizzle ORMの型推論を活用し、TypeScriptの型チェックで実行時エラーを防止
- **クエリ設計**: クエリビルダーを使用し、手書きSQLではなく型安全なクエリを構築
- **パフォーマンス**: N+1問題を常に意識し、不要なクエリの重複実行を避ける
- **テスト**: スキーマ定義とクエリロジックをテストし、リグレッションを防止
- **ドキュメント**: スキーマの意図、リレーション、パフォーマンスへの配慮をコメントで記録

### 避けるべきこと

- **手書きSQL**: 文字列ベースのSQLではなく、クエリビルダーを使用して型安全性を確保
- **スキーマ無視**: スキーマ定義を軽視し、後からエンティティマッピングを修正
- **複雑なJOIN**: 過度に複雑なJOINはReadability と Maintainability を低下させるため、適切に分割
- **キャッシング無視**: パフォーマンスクリティカルなクエリにおいてキャッシング戦略を未検討
- **マイグレーション無計画**: スキーマ変更時にマイグレーション計画を立てず、本番で問題を引き起こす
- **インデックス設計無視**: 検索や結合に使用するカラムにインデックスを設定しない

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                             | 用途           |
| -------------- | -------------------------------------------------------------------------------- | -------------- |
| 基礎知識       | See [references/basics.md](references/basics.md)                                 | ORM基本概念    |
| スキーマ定義   | See [references/schema-definition.md](references/schema-definition.md)           | テーブル定義   |
| リレーション   | See [references/relation-mapping.md](references/relation-mapping.md)             | 関連設定       |
| クエリビルダー | See [references/query-builder-patterns.md](references/query-builder-patterns.md) | クエリ構築     |
| パフォーマンス | See [references/performance-patterns.md](references/performance-patterns.md)     | 最適化パターン |

### agents/（Task仕様）

| Task              | 用途             |
| ----------------- | ---------------- |
| design-schema     | スキーマ設計支援 |
| implement-queries | クエリ実装支援   |
| validate-optimize | 検証・最適化支援 |

### assets/（テンプレート）

| リソース | パス                        | 用途         |
| -------- | --------------------------- | ------------ |
| スキーマ | `assets/schema-template.md` | テーブル定義 |

## 変更履歴

| Version | Date       | Changes                                         |
| ------- | ---------- | ----------------------------------------------- |
| 1.1.0   | 2026-01-02 | description形式更新、agents/追加、basics.md作成 |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様準拠へ更新                      |
| 0.9.0   | 2025-12-24 | Spec alignment and required artifacts added     |
