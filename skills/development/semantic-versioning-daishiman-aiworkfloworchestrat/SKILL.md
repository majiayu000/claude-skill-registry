---
name: semantic-versioning
description: |
  セマンティックバージョニング（semver）に基づく依存関係変更の影響予測と対応戦略を専門とするスキル。
  依存パッケージのバージョンアップ時の破壊的変更検出、影響分析、移行戦略立案を支援する。

  Anchors:
  • Semantic Versioning 2.0.0 Specification / 適用: バージョン番号の解釈 / 目的: 変更の性質を正確に判断
  • The Pragmatic Programmer / 適用: リスク軽減と段階的移行 / 目的: 安全なアップグレード
  • Keep a Changelog / 適用: 変更履歴の解析 / 目的: 破壊的変更の特定

  Trigger:
  Use when managing package dependency updates, analyzing version compatibility, detecting breaking changes, planning migration strategies, or assessing upgrade risks.
  semver, dependency, version, breaking change, migration, upgrade, compatibility, package update
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Semantic Versioning

## 概要

セマンティックバージョニング（semver）に基づく依存関係変更の影響予測と対応戦略を専門とするスキル。バージョンアップ時の破壊的変更検出、影響分析、移行戦略立案をカバーする。

## ワークフロー

```
analyze-impact → plan-migration → execute-upgrade → validate-results
```

### Phase 1: 影響分析

**目的**: バージョン変更の影響範囲を特定する

**Task**: `agents/analyze-impact.md` を参照

**アクション**:

1. 現在のバージョンと更新対象バージョンを確認
2. CHANGELOGやリリースノートを分析
3. 破壊的変更を特定

### Phase 2: 移行計画

**目的**: 安全な移行戦略を策定する

**Task**: `agents/plan-migration.md` を参照

**アクション**:

1. 破壊的変更への対応方法を決定
2. 段階的移行計画を作成
3. テスト戦略を策定

### Phase 3: 実行と検証

**目的**: 移行を実行し、成功を検証する

**アクション**:

1. 依存関係を更新
2. テストスイートを実行
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task           | 責務     | 入力             | 出力             |
| -------------- | -------- | ---------------- | ---------------- |
| analyze-impact | 影響分析 | バージョン情報   | 破壊的変更リスト |
| plan-migration | 移行計画 | 破壊的変更リスト | 移行計画書       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                           |
| ---------------------------- | ------------------------------ |
| CHANGELOGを必ず確認する      | 破壊的変更の事前把握           |
| 段階的にアップグレードする   | 問題の特定が容易               |
| テストカバレッジを確保する   | 回帰の早期発見                 |
| ロックファイルをコミットする | 再現可能なビルドの保証         |
| 0.x.xバージョンは慎重に扱う  | 破壊的変更がいつでも起こりうる |

### 避けるべきこと

| 禁止事項                         | 問題点               |
| -------------------------------- | -------------------- |
| メジャーバージョンを無確認で更新 | 破壊的変更による障害 |
| 複数依存を同時にアップグレード   | 問題の特定が困難     |
| テストなしでのアップグレード     | 回帰バグの見逃し     |
| 自動マージを有効にする           | 破壊的変更の見逃し   |

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                               | 読込条件         |
| -------------- | ---------------------------------------------------------------------------------- | ---------------- |
| Semver仕様     | [references/semver-specification.md](references/semver-specification.md)           | バージョン解釈時 |
| 破壊的変更検出 | [references/breaking-change-detection.md](references/breaking-change-detection.md) | 影響分析時       |
| 移行戦略       | [references/migration-strategies.md](references/migration-strategies.md)           | 移行計画時       |
| バージョン範囲 | [references/version-range-patterns.md](references/version-range-patterns.md)       | 範囲指定時       |

### scripts/（決定論的処理）

| スクリプト                           | 機能               |
| ------------------------------------ | ------------------ |
| `scripts/log_usage.mjs`              | 使用記録と自動評価 |
| `scripts/analyze-version-impact.mjs` | バージョン影響分析 |

### assets/（テンプレート）

| アセット                                | 用途                           |
| --------------------------------------- | ------------------------------ |
| `assets/upgrade-assessment-template.md` | アップグレード評価テンプレート |

## 変更履歴

| Version | Date       | Changes                                            |
| ------- | ---------- | -------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills仕様完全準拠、agents/を責務ベースに再構成 |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様に基づきリファクタリング           |
| 1.0.0   | 2025-12-24 | 初版                                               |
