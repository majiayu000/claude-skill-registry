---
name: foreign-key-constraints
description: |
  外部キー制約と参照整合性をC.J. Dateの理論に基づいて設計するスキル。CASCADE動作の戦略的選択、循環参照の検出・解消、ソフトデリート整合性を提供。SQLite/Turso + Drizzle ORM環境に最適化。

  Anchors:
  • An Introduction to Database Systems（C.J. Date） / 適用: FK設計 / 目的: 理論的に正しい制約設計
  • The Pragmatic Programmer（Hunt, Thomas） / 適用: 実装品質 / 目的: 保守性の高い設計

  Trigger:
  Use when designing foreign key relationships, selecting CASCADE behavior, detecting circular references, integrating soft delete patterns, or reviewing database schema integrity.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
---

# 外部キー制約設計

## 概要

外部キー制約と参照整合性の設計を、C.J. Dateの理論的基礎とThe Pragmatic Programmerの実用的指針に基づいて支援。CASCADE動作の戦略的選択、循環参照の検出と解消、ソフトデリートとの整合性確保を実現。

## ワークフロー

### Phase 1: 設計レビュー

**目的**: FK制約設計の妥当性を確認し、問題を早期発見

**アクション**:

1. データベーススキーマ定義を確認
2. テーブル関係性を分析
3. FK制約の妥当性を評価

**Task**: [agents/design-review.md](agents/design-review.md) を参照

### Phase 2: CASCADE動作の選択

**目的**: ビジネスルールに合致したCASCADE動作を選択

**アクション**:

1. [references/cascade-patterns.md](references/cascade-patterns.md) でパターンを確認
2. 親子テーブルの関係性を分析
3. 適切なCASCADE設定を決定

**Task**: [agents/cascade-selection.md](agents/cascade-selection.md) を参照

### Phase 3: 循環参照の検出

**目的**: 循環参照を検出し、解消策を提案

**アクション**:

1. FK制約の依存関係グラフを構築
2. 循環参照を検出
3. 解消策を優先順位付きで提案

**Task**: [agents/circular-detection.md](agents/circular-detection.md) を参照

### Phase 4: ソフトデリート統合

**目的**: ソフトデリートとFK制約の整合性確保

**アクション**:

1. ソフトデリート対象テーブルを特定
2. FK制約との整合性を設計
3. クエリ実装パターンを適用

**Task**: [agents/soft-delete-integration.md](agents/soft-delete-integration.md) を参照

## Task仕様ナビ

| Task                                                                   | 用途               | 入力         | 出力               |
| ---------------------------------------------------------------------- | ------------------ | ------------ | ------------------ |
| [agents/design-review.md](agents/design-review.md)                     | 設計レビュー       | スキーマ定義 | 妥当性評価レポート |
| [agents/cascade-selection.md](agents/cascade-selection.md)             | CASCADE選択        | 関係性・要件 | 推奨CASCADE設定    |
| [agents/circular-detection.md](agents/circular-detection.md)           | 循環参照検出       | FK依存グラフ | 循環リスト・解消策 |
| [agents/soft-delete-integration.md](agents/soft-delete-integration.md) | ソフトデリート統合 | 削除ポリシー | 実装パターン       |

## ベストプラクティス

### すべきこと

- FK制約追加前に設計レビューを実施
- CASCADE動作はパターンから選択
- 循環参照を定期的に検証
- ソフトデリート導入時はPhase 4を必ず実行

### 避けるべきこと

- 理論的根拠なしにCASCADEを多用する
- 循環参照を確認せずにFK制約を追加
- ソフトデリートとハードデリートの整合性確認を怠る
- 深い階層のCASCADEをパフォーマンス考慮なしに設定

## リソース参照

### references/（詳細知識）

| リソース        | パス                                                             | 内容                            |
| --------------- | ---------------------------------------------------------------- | ------------------------------- |
| CASCADEパターン | [references/cascade-patterns.md](references/cascade-patterns.md) | 各CASCADE動作のパターン・実装例 |

### scripts/（検証・記録）

| スクリプト             | 用途       | 使用例                                               |
| ---------------------- | ---------- | ---------------------------------------------------- |
| check-fk-integrity.mjs | 整合性検証 | `node scripts/check-fk-integrity.mjs --schema <dir>` |
| log_usage.mjs          | 利用記録   | `node scripts/log_usage.mjs --result success`        |

### assets/（テンプレート）

| テンプレート           | 用途                 |
| ---------------------- | -------------------- |
| fk-design-checklist.md | FK設計チェックリスト |

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 2.1.0   | 2026-01-02 | 18-skills.md仕様に完全準拠。references/整理・簡素化 |
| 2.0.0   | 2025-12-31 | Task-basedワークフロー追加                          |
| 1.0.0   | 2025-12-24 | 初版作成                                            |
