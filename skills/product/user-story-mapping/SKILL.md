---
name: user-story-mapping
description: |
  ユーザーストーリーマッピングの専門スキル。
  バックボーン設計、リリース計画、ストーリー分割を提供します。

  Anchors:
  • 『User Story Mapping: Discover the Whole Story, Build the Right Product』（Jeff Patton）/ 適用: 要件可視化 / 目的: プロダクト理解
  • 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）/ 適用: 実践的改善 / 目的: 品質維持

  Trigger:
  ユーザーストーリーマッピング実施、要件可視化、バックログ整理、プロダクト開発計画立案時に使用

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# ユーザーストーリーマッピングスキル

## 概要

ユーザーストーリーマッピングは、ユーザー視点から要件を体系的に構造化し、プロダクト開発の価値提供の流れを可視化する手法です。エピック、ユーザーストーリー、タスクの階層構造を明確にし、優先順位付けを通じて効果的なバックログを構築します。

このスキルを活用することで、チーム全体が共通の理解を持ち、MVPから段階的な機能展開まで、戦略的なプロダクト開発が実現できます。

詳細な実行手順は、`references/Level1_basics.md`（基本構造）および`references/Level2_intermediate.md`（実務適用）を参照してください。

## ワークフロー

### Phase 1: 要件と対象範囲の定義

**目的**: マッピング対象となるプロダクト要件と制約条件を明確にする

**Task**: `agents/requirements-scoping.md`

**入力**:

- プロダクト概要、ステークホルダー情報

**出力**:

- マッピング仕様書（ペルソナ、機能領域、制約を含む）

**アクション**:

1. マッピング対象のプロダクト概要を把握する
2. ペルソナ（ユーザー種別）を定義する
3. プロダクトの主要機能領域を列挙する
4. 技術制約、スケジュール制約などを整理する
5. `assets/backlog-priority-template.md` の構造を確認する

**期待成果物**:

- マッピング対象の仕様書（ペルソナ、機能領域、制約を含む）

**完了条件**:

- [ ] ペルソナが最低3種類以上定義されている
- [ ] 主要機能領域が5つ以上列挙されている
- [ ] 制約条件が明確に記述されている

### Phase 2: ストーリーマップの構築

**目的**: ユーザージャーニーに沿ってエピック、ストーリー、タスクを階層的に構造化する

**Task**: `agents/story-map-construction.md`

**入力**:

- マッピング仕様書（Phase 1の出力）

**出力**:

- ユーザーストーリーマップ（エピック→ストーリー→タスク構造）

**アクション**:

1. ペルソナごとのユーザージャーニーを描く
2. 各ジャーニーにおける主要なエピック（大きな機能単位）を特定する
3. エピックをユーザーストーリーに分割する
4. 各ストーリーを実装可能なタスクまで細分化する
5. `assets/epic-template.md` と `assets/user-story-template.md` に従って記述する

**期待成果物**:

- 完全なユーザーストーリーマップ（エピック→ストーリー→タスク）
- マッピング図または構造化ドキュメント

**完了条件**:

- [ ] すべてのペルソナのジャーニーがマップされている
- [ ] エピックが明確に境界分けされている
- [ ] 各ストーリーが「As a [role], I want to [action], so that [benefit]」形式で記述されている
- [ ] マップ全体の一貫性が確認されている

### Phase 3: 優先順位付けと妥当性検証

**目的**: マップの妥当性を検証し、実装順序を決定する

**Task**: `agents/prioritization-validation.md`

**入力**:

- ユーザーストーリーマップ（Phase 2の出力）

**出力**:

- 優先順位付きバックログ、MVP定義書、リリース計画

**アクション**:

1. 各ストーリーのビジネス価値を評価する
2. 実装コストを見積もる
3. 優先順位付けアルゴリズム（MoSCoW法、RICE法など）を適用する
4. MVPに含まれるストーリーを特定する
5. リリース計画を段階化する（Phase 1、2、3...）
6. ステークホルダーとの検証を実施する

**期待成果物**:

- 優先順位付けされたバックログ
- MVP定義書
- リリース計画（段階化されたロードマップ）

**完了条件**:

- [ ] すべてのストーリーに優先度が付与されている
- [ ] MVPスコープが明確に定義されている
- [ ] リリース段階が明記されている
- [ ] ステークホルダー承認が得られている

### Phase 4: 記録と評価

**目的**: スキル使用実績を記録し、継続的改善に貢献する

**背景**: スキルの成長には使用データの蓄積が不可欠

**ゴール**: 実行記録が保存され、メトリクスが更新された状態

**読み込むスキル**: なし

**アクション**:

1. 使用したスキルの `scripts/log_usage.mjs` を実行

   ```bash
   node .claude/skills/user-story-mapping/scripts/log_usage.mjs \
     --result success \
     --phase "ストーリーマップの構築" \
     --agent "req-analyst"
   ```

2. スクリプトが自動的に以下を実行:
   - LOGS.md に実行記録を追記
   - EVALS.json のメトリクスを更新
   - レベルアップ条件をチェック
   - 条件充足時にSKILL.mdのlevelを更新
   - CHANGELOG.mdに記録

**期待成果物**:

- 更新されたLOGS.md
- 更新されたEVALS.json
- （条件充足時）更新されたSKILL.mdとCHANGELOG.md

**完了条件**:

- [ ] log_usage.mjsがexit code 0で終了
- [ ] LOGS.mdに新規エントリが追記されている

## Task仕様（ナビゲーション）

| Task                         | 役割                 | 参照先                                |
| ---------------------------- | -------------------- | ------------------------------------- |
| requirements-scoping.md      | 要件と対象範囲の定義 | `agents/requirements-scoping.md`      |
| story-map-construction.md    | ストーリーマップ構築 | `agents/story-map-construction.md`    |
| prioritization-validation.md | 優先順位付けと検証   | `agents/prioritization-validation.md` |

## ベストプラクティス

### すべきこと

- ペルソナを具体的かつ多様に定義する（最低3種類以上）
- ユーザーの痛点と価値を常に意識する
- エピック、ストーリー、タスクの階層を厳密に区分する
- 定期的にステークホルダーと検証する
- 優先順位付けの根拠を明確に記述する
- MVPスコープを早期に定義し、段階的な展開を計画する

### 避けるべきこと

- ビジネス視点のみでユーザー視点を無視する
- 機能要件をストーリーとして直接記述する（ユーザーゴールが欠ける）
- マッピング段階で詳細な技術仕様を決定する
- 優先順位付けの基準を曖昧なままにする
- 一度定義したストーリーを定期的に見直さない
- リソース、スケジュール制約を無視して過度に詳細化する

## リソース参照

### レベル別ガイド

- **`references/Level1_basics.md`**: ユーザーストーリーの基本構造、ペルソナ定義、GWT形式の理解
- **`references/Level2_intermediate.md`**: マッピング実務、優先順位付けアルゴリズム、複数ペルソナ間の調整
- **`references/Level3_advanced.md`**: Progressive Disclosure、トークン最適化、複数チーム間の効率的なマッピング
- **`references/Level4_expert.md`**: フィードバックループ設計、スキル自己進化の仕組み、評価基準の改善

### スクリプト実行リファレンス

```bash
# 実行記録の追記とレベル評価
node .claude/skills/user-story-mapping/scripts/log_usage.mjs --result success --phase "ストーリーマップ構築"

# スキル構造の検証
node .claude/skills/user-story-mapping/scripts/validate-skill.mjs

# ヘルプ表示
node .claude/skills/user-story-mapping/scripts/log_usage.mjs --help
```

### テンプレート参照

- **`assets/user-story-template.md`**: ユーザーストーリー作成用テンプレート（GWT形式、受け入れ基準を含む）
- **`assets/epic-template.md`**: エピック定義テンプレート（ビジネス目標、包含ストーリーを含む）
- **`assets/backlog-priority-template.md`**: バックログ優先順位付けテンプレート（RICE法、MoSCoW法対応）

## 関連スキル

- **`.claude/skills/backlog-management/SKILL.md`**: バックログの段階的な構造化と管理手法（ストーリーマップの実装化に活用）
- **`.claude/skills/requirement-analysis/SKILL.md`**: 複雑な要件分析と合意形成（マッピング前の要件整理に活用）
- **`.claude/skills/user-story-writing/SKILL.md`**: より詳細なストーリー記述技法

## 変更履歴

| Version | Date       | Changes                                         |
| ------- | ---------- | ----------------------------------------------- |
| 2.1.0   | 2026-01-01 | agents/作成、Task仕様書追加、ワークフロー簡素化 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様準拠、Phase別ワークフロー追加   |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added     |
