---
name: requirements-engineering
description: |
  カール・ウィーガーズの要求工学とIEEE 830に基づき、ステークホルダーニーズを抽出し、検証可能な要件に落とし込むための体系的なスキル。
  スコープ定義、要件抽出、仕様化、品質検証、合意形成までの一貫プロセスを提供する。

  Anchors:
  • 『Software Requirements』（Karl Wiegers） / 適用: 要件工学 / 目的: 品質要件の明確化
  • IEEE 830 / 適用: 要件仕様の構造 / 目的: 一貫したドキュメント化
  • ISO/IEC 25010 / 適用: 非機能要件分類 / 目的: 品質特性の網羅

  Trigger:
  Use when defining system requirements, eliciting stakeholder needs, validating requirement quality, or drafting requirements documents.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 要件エンジニアリング

## 概要

要件エンジニアリングの全工程（スコープ整理→要件抽出→仕様化→品質検証→合意形成）を、短いサイクルで反復できるように設計したスキル。
詳細な手順は `references/` に段階的に分割し、実務では `assets/requirements-document.md` を基準として成果物を統一する。

## ワークフロー

### Phase 1: スコープと前提の整理

**目的**: 目的・範囲・制約・ステークホルダーを確定し、作業の起点を作る

**アクション**:

1. 依頼背景とビジネス目的を確認する
2. ステークホルダーの一覧と役割を整理する
3. スコープ内/外を明示し、前提条件と制約を整理する
4. 既存資料の所在を `references/requirements-index.md` で確認する
5. 合意可能な成功指標を定義する

### Phase 2: 要件抽出（Elicitation）

**目的**: ニーズと課題を収集し、要件候補を漏れなく集める

**アクション**:

1. ヒアリング/ワークショップ/観察の計画を立てる
2. ステークホルダーの意図・問題・期待を記録する
3. 機能要件/非機能要件の候補を分類する
4. 衝突や重複を仮整理し、未確定事項を洗い出す

### Phase 3: 要件仕様化

**目的**: 要件を検証可能な形式に落とし込み、成果物を標準化する

**アクション**:

1. `assets/requirements-document.md` をベースに要件定義書を作成する
2. 要件IDを付与し、FR/NFRを明確に区分する
3. 受け入れ基準と依存関係を記述する
4. 優先度やリスクを明記し、合意候補を整理する

### Phase 4: 品質検証と合意

**目的**: 要件の品質を検証し、レビューで合意を得る

**アクション**:

1. `references/quality-criteria.md` と `references/completeness-checklist.md` で品質確認
2. `references/ambiguity-detection.md` で曖昧性を除去する
3. `scripts/validate-requirements.mjs` で自動検証を行う
4. レビュー結果を反映し、承認を取得する
5. `scripts/log_usage.mjs` で実行記録を残す

## Task仕様ナビ

| Phase   | Task                        | 入力                           | 出力                                 | リソース                              |
| ------- | --------------------------- | ------------------------------ | ------------------------------------ | ------------------------------------- |
| Phase 1 | scope-stakeholder-alignment | 依頼背景、既存資料             | スコープ定義、ステークホルダーマップ | agents/scope-stakeholder-alignment.md |
| Phase 2 | requirements-elicitation    | ステークホルダー一覧、前提条件 | 要件候補リスト、未確定事項           | agents/requirements-elicitation.md    |
| Phase 3 | requirements-specification  | 要件候補リスト、制約条件       | 要件定義書、要件ID一覧               | agents/requirements-specification.md  |
| Phase 4 | requirements-quality-review | 要件定義書、レビュー観点       | 品質レビュー結果、修正一覧           | agents/requirements-quality-review.md |

## ベストプラクティス

### すべきこと

1. **スコープの明確化**: スコープ内/外を初期に合意し、後続の混乱を防ぐ
2. **多面的な要件抽出**: ヒアリング、観察、既存資料の3経路で要求を集める
3. **IDと受け入れ基準の付与**: すべての要件にIDと検証条件を付ける
4. **品質チェックの二重化**: 自動検証と手動チェックリストを併用する
5. **合意と記録**: レビュー結果と修正履歴をログとして残す

### 避けるべきこと

1. **目的・前提の曖昧化**: 目的が定義されないまま要件を書き始める
2. **単一ステークホルダー依存**: 1人の意見だけで要件を固定する
3. **曖昧表現の放置**: 量的/質的曖昧性を残したまま合意しない
4. **品質検証のスキップ**: チェックリストと自動検証のどちらかを省略する
5. **承認記録の欠落**: 合意の証跡が残らない状態で実装へ進む

## リソース参照

### レベル別ガイド

- **references/Level1_basics.md**: 基礎理論と最低限の運用指針
- **references/Level2_intermediate.md**: リソース運用と実務プロセス
- **references/Level3_advanced.md**: モデリング、トレーサビリティ、リスク分析
- **references/Level4_expert.md**: フィードバックループと改善運用

### 特化リソース

- **references/ambiguity-detection.md**: 曖昧性パターンと除去技法
- **references/completeness-checklist.md**: 要件の完全性チェックリスト
- **references/quality-criteria.md**: 要件品質の評価基準
- **references/triage-framework.md**: 要件の優先度付けフレームワーク
- **references/requirements-index.md**: docs/00-requirements の索引

### テンプレート

- **assets/requirements-document.md**: 要件定義書の標準テンプレート

### スクリプト

- **scripts/validate-requirements.mjs**: 要件定義書の品質検証
- **scripts/validate-skill.mjs**: スキル構造の整合性確認
- **scripts/log_usage.mjs**: 使用記録と評価の更新

## 変更履歴

| Version | Date       | Changes                                                                            |
| ------- | ---------- | ---------------------------------------------------------------------------------- |
| 1.1.0   | 2026-01-02 | ワークフロー再設計、Task仕様ナビ追加、agents作成、参照パス整備、検証スクリプト更新 |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様に基づいた完全改定、Task仕様ナビの追加、Anchors/Triggerの統合      |
