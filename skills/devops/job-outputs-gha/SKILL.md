---
name: job-outputs-gha
description: |
  GitHub Actionsのジョブ出力管理スキル。ジョブ間でのデータ共有、outputs定義、
  依存関係設定、条件分岐、マトリックス戦略での出力集約を提供。

  Anchors:
  • Continuous Delivery / 適用: ジョブ間データフロー設計 / 目的: 信頼性の高いパイプライン構築
  • GitHub Actions公式ドキュメント / 適用: outputs/needs構文 / 目的: 正確な実装パターン適用

  Trigger:
  Use when sharing data between GitHub Actions jobs, defining job outputs,
  setting up job dependencies with needs keyword, implementing conditional workflows,
  or aggregating outputs from matrix strategies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# ジョブ出力管理（GitHub Actions）

## 概要

GitHub Actionsワークフロー内でジョブ間のデータ共有を効率的に実装するスキル。
outputs定義、needs依存関係、条件分岐、マトリックス戦略での出力集約を通じて、
複雑なワークフローオーケストレーションを実現します。

## ワークフロー

### Phase 1: 要件分析とデータフロー設計

**目的**: ジョブ間のデータフロー要件を明確化

**アクション**:

1. ワークフロー内のジョブ依存関係を特定（どのジョブがどのジョブの出力を必要とするか）
2. [references/Level1_basics.md](references/Level1_basics.md) でジョブ出力の基本概念を確認
3. データフローダイアグラムを作成し、ジョブ間の依存関係を可視化
4. 出力データの型と形式を定義（文字列、JSON、真偽値など）

**Task参照**:

- [agents/analyze-workflow.md](agents/analyze-workflow.md): ワークフロー分析タスク

### Phase 2: outputs定義の実装

**目的**: ジョブ出力を正確に定義・設定

**アクション**:

1. 各ジョブで必要な outputs を定義 → [references/Level2_intermediate.md](references/Level2_intermediate.md)
2. ステップ出力を GITHUB_OUTPUT に書き込む実装パターンを適用
3. needs キーワードで依存関係を設定
4. 条件分岐が必要な場合は [references/conditional-outputs.md](references/conditional-outputs.md) を参照

**Task参照**:

- [agents/implement-outputs.md](agents/implement-outputs.md): outputs実装タスク

**テンプレート**:

- [assets/job-outputs-template.yaml](assets/job-outputs-template.yaml): 基本的なジョブ出力テンプレート

### Phase 3: マトリックス戦略と出力集約

**目的**: 複数ジョブからの出力を効率的に集約

**アクション**:

1. マトリックス戦略を使用する場合、[references/Level3_advanced.md](references/Level3_advanced.md) で集約パターンを確認
2. JSON形式での出力集約を実装
3. 後続ジョブでの出力参照パターンを確認 → [references/output-consumption.md](references/output-consumption.md)
4. 必要に応じて [assets/matrix-outputs-template.yaml](assets/matrix-outputs-template.yaml) を使用

**Task参照**:

- [agents/aggregate-outputs.md](agents/aggregate-outputs.md): 出力集約タスク

### Phase 4: 検証と最適化

**目的**: ジョブ出力の信頼性と効率性を確保

**アクション**:

1. テストワークフロー実行で出力が正しく伝播することを確認
2. [references/Level4_expert.md](references/Level4_expert.md) でトラブルシューティングパターンを確認
3. デバッグログで outputs の値を検証
4. `scripts/log_usage.mjs --result success` でフィードバック記録

**Task参照**:

- [agents/validate-outputs.md](agents/validate-outputs.md): 検証タスク

## Task仕様ナビ

本スキルの実装は以下のTaskと参照リソースを組み合わせて進めます:

| 目的                 | Task                        | 参照リソース                      | 用途                                   |
| -------------------- | --------------------------- | --------------------------------- | -------------------------------------- |
| **ワークフロー分析** | agents/analyze-workflow.md  | references/Level1_basics.md       | データフロー要件の特定                 |
| **outputs実装**      | agents/implement-outputs.md | references/Level2_intermediate.md | ジョブ出力の定義と設定                 |
| **出力集約**         | agents/aggregate-outputs.md | references/Level3_advanced.md     | マトリックス戦略での出力集約           |
| **検証とデバッグ**   | agents/validate-outputs.md  | references/Level4_expert.md       | トラブルシューティングとパフォーマンス |
| **条件分岐パターン** | -                           | references/conditional-outputs.md | 条件付き出力の実装                     |
| **出力参照パターン** | -                           | references/output-consumption.md  | 後続ジョブでの出力利用                 |
| **needs依存関係**    | -                           | references/needs-dependencies.md  | ジョブ依存関係の詳細設定               |

## ベストプラクティス

### すべきこと

- Phase 1 でデータフロー全体を設計してから実装に進む（後戻りを防ぐ）
- outputs は明示的に定義し、型を明確にする（文字列、JSON、真偽値）
- GITHUB_OUTPUT を使用して出力を設定（deprecated な set-output コマンドは避ける）
- マトリックス戦略では toJSON/fromJSON を活用して出力を集約
- デバッグ時は outputs の値をログに出力して確認
- 循環依存を避け、DAG（有向非巡回グラフ）構造を維持

### 避けるべきこと

- 環境変数で代替しようとする（スコープが異なり、ジョブ間共有には不適切）
- set-output コマンドを使用（deprecated、セキュリティリスクあり）
- 大容量データをジョブ出力で渡す（サイズ制限1MB、アーティファクトを使用）
- outputs のタイポ（実行時エラーが検出されにくい）
- needs なしで出力を参照（依存関係が明示されず、実行順序が不定）
- 条件分岐で未定義の出力を参照（空文字列チェックを必ず実装）

## リソース参照

### 参照資料

- [references/Level1_basics.md](references/Level1_basics.md): ジョブ出力の基礎概念
- [references/Level2_intermediate.md](references/Level2_intermediate.md): 実装パターンと事例
- [references/Level3_advanced.md](references/Level3_advanced.md): マトリックス戦略と出力集約
- [references/Level4_expert.md](references/Level4_expert.md): 最適化とトラブルシューティング
- [references/conditional-outputs.md](references/conditional-outputs.md): 条件付き出力パターン
- [references/output-consumption.md](references/output-consumption.md): 出力参照パターン
- [references/needs-dependencies.md](references/needs-dependencies.md): needs依存関係詳細

### スクリプト

**validate-outputs.mjs**: ワークフロー内のジョブ出力を検証

```bash
node scripts/validate-outputs.mjs --help
node scripts/validate-outputs.mjs --workflow .github/workflows/ci.yml
```

**log_usage.mjs**: フィードバックループ用（Phase 4 で実行）

```bash
node scripts/log_usage.mjs --result success --phase "Phase 4" --notes "ジョブ出力実装完了"
```

**validate-skill.mjs**: スキル構造検証

```bash
node scripts/validate-skill.mjs
```

### テンプレート

- [assets/job-outputs-template.yaml](assets/job-outputs-template.yaml): 基本的なジョブ出力ワークフロー
- [assets/matrix-outputs-template.yaml](assets/matrix-outputs-template.yaml): マトリックス戦略での出力集約例
- [assets/conditional-outputs-template.yaml](assets/conditional-outputs-template.yaml): 条件付き出力の実装例

## 変更履歴

| Version | Date       | Changes                                           |
| ------- | ---------- | ------------------------------------------------- |
| 1.0.0   | 2025-12-31 | 初版作成、18-skills.md 仕様準拠、Task仕様ナビ実装 |
