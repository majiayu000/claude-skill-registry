---
name: few-shot-learning-patterns
description: |
  Few-Shot Learning（少数例示学習）のパターンとベストプラクティスを提供するスキル。効果的な例示の設計、構造化、配置により、AIの出力品質を大幅に向上させます。

  • The Pragmatic Programmer / 適用: 例示パターン設計の品質基準 / 目的: 実践的改善と一貫性維持
  • Few-Shot戦略 / 適用: 段階的複雑度設計と最適shot数決定 / 目的: AIの学習効率最大化

  Trigger:
  Use when you need to design effective example patterns for AI learning, standardize output formats, or improve task performance beyond zero-shot capabilities. Keywords: few-shot, examples, prompting, output consistency, pattern learning.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Few-Shot Learning Patterns

## 概要

Few-Shot Learning（少数例示学習）のパターンとベストプラクティスを提供するスキル。効果的な例示の設計、構造化、配置により、AIの出力品質を大幅に向上させます。

このスキルは以下のシナリオで活用されます：

- **出力形式の統一**: AIに特定の形式やスタイルを学習させたい時
- **パターン学習の加速**: Zero-Shotでは不十分な複雑なタスク対応
- **品質向上**: 一貫性のある高品質な出力の確保
- **ドメイン固有タスク**: 業界別、言語別、領域別パターンの最適化

詳細な実装手順や背景知識は、レベル別リソースを参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要な references/scripts/templates を特定

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す

## Task仕様ナビ

このスキルを効果的に活用するためのTask仕様リファレンス：

| レベル      | 対象タスク           | 説明                                           | 推奨リソース                                         | 活用シーン                                     |
| ----------- | -------------------- | ---------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------- |
| **Level 1** | 基礎的なFew-Shot設計 | 単純な1-3例の例示パターンの構築                | Level1_basics.md                                     | 初めてFew-Shotを導入する場合、基本的な形式学習 |
| **Level 2** | 実務的なFew-Shot実装 | 3-5例の構造化された例示セットの作成            | Level2_intermediate.md, example-design-principles.md | 実際のプロジェクトでの導入、パターンの最適化   |
| **Level 3** | 高度なFew-Shot戦略   | 複数ドメイン向け最適化、shot数の動的調整       | Level3_advanced.md, shot-count-strategies.md         | 複雑なタスク、複数パターンの統合               |
| **Level 4** | エキスパート最適化   | 専門領域向けカスタマイズ、パフォーマンス最大化 | Level4_expert.md, domain-specific-patterns.md        | 高度な要件、業界別カスタマイズ                 |

**選択基準**:

- **出力品質の判断**: 現在の結果が「満足できない」→ Level 2 へ、「不十分」→ Level 3 へ
- **タスク複雑度**: 単一形式 → Level 1, 複数パターン → Level 2-3, ドメイン固有 → Level 3-4
- **運用規模**: 個人利用 → Level 1-2, チーム利用 → Level 2-3, 本番環境 → Level 3-4

## ベストプラクティス

### すべきこと

- **例示の質を重視する**: 誤った例や曖昧な例を避け、高品質で明確な例示を3-5個準備
- **段階的な複雑度設定**: シンプルな例から複雑な例へ段階的に進め、パターン認識を促進
- **実際のビジネスケース**: 実務で想定される入力と出力を使用し、現実的な学習を実現
- **メタデータの明示**: 例示の意図や注意点をコメントで明記し、AIの理解を深める
- **ドメイン固有パターン**: 業界別、言語別、フォーマット別にカスタマイズした例示を用意
- **段階的な改善**: 初版（1-3例）から始め、結果を検証しながら例示を増やす
- **コンテキスト情報の包含**: 例示にタスク背景や制約条件を含める

### 避けるべきこと

- **不適切な例示**: 誤った例やアンチパターンを含める（例外的な説明が必要）
- **一貫性の欠如**: 例示ごとに異なるスタイルやフォーマットで混乱を招く
- **過度な複雑化**: 初期段階で5例以上の複雑な例を提供して認知負荷を高める
- **コンテキスト不足**: 例示の背景や意図を説明せずにAIに示す
- **検証なしの運用**: Few-Shotの効果を検証せず本番環境に投入する
- **静的な例示セット**: 実績に基づかずに例示を作成し、継続的な改善を行わない
- **言語混在**: 同一タスク内で複数言語の例示を無秩序に混在させる

## リソース参照

### 学習リソース（段階的ガイド）

| リソース                              | 用途                                 | 対象レベル |
| ------------------------------------- | ------------------------------------ | ---------- |
| **references/Level1_basics.md**       | Few-Shotの基本概念と最小構成パターン | レベル1    |
| **references/Level2_intermediate.md** | 実務的な実装とパターン最適化         | レベル2    |
| **references/Level3_advanced.md**     | 高度な戦略と複雑なシナリオ対応       | レベル3    |
| **references/Level4_expert.md**       | エキスパート向けカスタマイズと最適化 | レベル4    |

### ドメイン別リソース

- **references/domain-specific-patterns.md**: 業界別、領域別のFew-Shotパターン集
- **references/example-design-principles.md**: 効果的な例示設計の原則と手法
- **references/shot-count-strategies.md**: 最適な例示数（shot数）の決定戦略

### テンプレート集

- **assets/basic-few-shot.md**: 基本的なFew-Shotプロンプトテンプレート
- **assets/advanced-few-shot.md**: 高度な用途向けテンプレート

### スクリプトとツール

```bash
# スキル構造の検証
node .claude/skills/few-shot-learning-patterns/scripts/validate-skill.mjs --help

# 使用記録と自動評価
node .claude/skills/few-shot-learning-patterns/scripts/log_usage.mjs --help
```

### 参考文献

- **references/legacy-skill.md**: 旧バージョンのSKILL.mdと変更履歴
- 『The Pragmatic Programmer』: 実践的改善と品質維持の原則

## 変更履歴

| Version   | Date       | 変更内容                                                                                                                                         |
| --------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1.1.0** | 2025-12-31 | 18-skills.md仕様に準拠 - frontmatter最適化（Anchors/Trigger追加、allowed-tools定義）、Task仕様ナビ追加、ベストプラクティス充実、リソース参照整理 |
| 1.0.0     | 2025-12-24 | 初期リリース - Spec alignment and required artifacts added                                                                                       |

### バージョン1.1.0の主要な改善

- **YAML frontmatter の最適化**
  - `name`, `description`(Anchors/Trigger), `allowed-tools` の明確化
  - バージョンとレベル情報の更新

- **Task仕様ナビの追加**
  - レベル別タスク分類（Level 1-4）
  - 選択基準の明示

- **ベストプラクティスの充実**
  - すべきこと：7項目に拡充
  - 避けるべきこと：7項目に拡充

- **リソース参照の構造化**
  - 学習リソース、ドメイン別リソース、テンプレート集に分類
  - スクリプト実行例の追加
