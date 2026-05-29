---
name: boundary-value-analysis
description: |
  境界値分析と同値分割によるテストケース設計を体系化するスキル。
  入力領域の分類、境界値抽出、エッジケース追加、組み合わせ最適化を行い、最小のテスト数で検証精度を高める。

  Anchors:
  • The Pragmatic Programmer / 適用: テスト設計 / 目的: 実践的改善と品質維持
  • Software Testing (Glenford J. Myers) / 適用: 境界値設計 / 目的: 代表値選定の明確化
  • Rapid Software Testing (James Bach) / 適用: 探索的テスト / 目的: エッジケースの発見

  Trigger:
  Use when designing test cases, validating input boundaries, applying equivalence partitioning, or optimizing test coverage.
allowed-tools:
  - bash
  - node
---

# Boundary Value Analysis

## 概要

境界値分析と同値分割を使って、入力領域ごとのテストケースを設計する。
詳細は `references/` に外部化し、必要時に参照する。

- テスト設計テンプレ: `assets/test-case-design-template.md`

## ワークフロー

### Phase 1: 入力領域の整理

**目的**: 入力範囲と制約を明確にする

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認
2. `references/boundary-value-fundamentals.md` を参照
3. 入力パラメータ、範囲、制約を整理

**Task**: `agents/analyze-input-domain.md`

### Phase 2: 同値クラスと境界値設計

**目的**: 同値クラスと境界値を定義する

**アクション**:

1. `references/equivalence-partitioning.md` を参照
2. 有効/無効クラスを定義
3. 境界値（下限/上限/±1）を抽出

**Task**: `agents/define-equivalence-classes.md`

### Phase 3: テストケース生成

**目的**: テストケースを具体化する

**アクション**:

1. `assets/test-case-design-template.md` を使用
2. `references/edge-cases-catalog.md` でエッジケースを追加
3. 複数パラメータは `references/combination-strategies.md` を参照
4. 必要に応じて `scripts/boundary-test-generator.mjs` を使用

**Task**: `agents/generate-boundary-tests.md`

### Phase 4: 検証と記録

**目的**: カバレッジを検証し記録する

**アクション**:

1. `references/Level3_advanced.md` を参考に妥当性を確認
2. `scripts/validate-skill.mjs` で構造検証
3. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-boundary-coverage.md`

## Task仕様ナビ

| Task           | 役割            | 入力             | 出力             | 参照先                                      | 実行タイミング |
| -------------- | --------------- | ---------------- | ---------------- | ------------------------------------------- | -------------- |
| 入力整理       | 範囲/制約整理   | 仕様/要件        | 入力整理メモ     | `references/boundary-value-fundamentals.md` | Phase 1        |
| 同値クラス設計 | 有効/無効定義   | 入力整理メモ     | 同値クラス表     | `references/equivalence-partitioning.md`    | Phase 2        |
| テスト生成     | 境界/エッジ抽出 | 同値クラス表     | テストケース一覧 | `assets/test-case-design-template.md`       | Phase 3        |
| 検証           | カバレッジ確認  | テストケース一覧 | 検証メモ         | `references/Level3_advanced.md`             | Phase 4        |

## ベストプラクティス

### すべきこと

- 入力範囲と制約を明記する
- 同値クラスを有効/無効で分ける
- 境界値は下限/上限/±1を必ず含める
- エッジケースを追加する

### 避けるべきこと

- 同値クラスと境界値の根拠を省略する
- エラーパスのテストを省く
- 組み合わせ爆発を無計画に増やす

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: 実務適用
- `references/Level3_advanced.md`: 併用戦略
- `references/Level4_expert.md`: 監査/最適化
- `references/boundary-value-fundamentals.md`: 境界値分析の基礎
- `references/equivalence-partitioning.md`: 同値分割
- `references/edge-cases-catalog.md`: エッジケース集
- `references/combination-strategies.md`: 組み合わせ戦略
- `references/legacy-skill.md`: 旧版要約（移行時のみ）

### スクリプト

- `scripts/boundary-test-generator.mjs`: テストケース生成
- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/test-case-design-template.md`: テスト設計テンプレ

## 変更履歴

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠               |
| 1.0.0   | 2025-12-24 | 初版作成                                 |
