---
name: artifact-management-gha
description: |
  GitHub Actions のアーティファクト管理（upload/download、ジョブ間共有、保持期間、クリーンアップ）の設計と実装を支援するスキル。
  データ受け渡しの設計、容量最適化、保管期間戦略を整理し、再現性の高い成果物管理を実現します。

  Anchors:
  • The Pragmatic Programmer / 適用: 成果物管理の実践的改善 / 目的: 確実な共有と品質維持
  • GitHub Actions Artifacts / 適用: upload/download仕様 / 目的: 正しい設定と制限理解
  • Lean Waste Reduction / 適用: 保持期間と容量管理 / 目的: ストレージ最適化

  Trigger:
  Use when designing or implementing GitHub Actions artifact upload/download flows, job-to-job data sharing, retention policies, or cleanup automation.
allowed-tools:
  - bash
  - node
---

# アーティファクト管理（GitHub Actions）

## 概要

GitHub Actions ワークフロー内で成果物を管理するための設計・実装・検証の手順を提供する。
必要な詳細は `references/` に外部化し、必要時にのみ参照する。

- ワークフロー例は `assets/artifact-workflow.yaml` を使用
- 仕様確認は `references/upload-artifact.md` と `references/download-artifact.md` を参照

## ワークフロー

### Phase 1: 目的と利用パターンの整理

**目的**: アーティファクトの用途と制約を明確化する

**アクション**:

1. `references/Level1_basics.md` で基礎概念を確認
2. ジョブ間/ワークフロー間の共有要件を整理
3. 期待される保持期間と容量制約を整理

**Task**: `agents/analyze-artifact-context.md`

### Phase 2: 設計と実装

**目的**: アップロード/ダウンロードのフローと保持戦略を設計する

**アクション**:

1. `assets/artifact-workflow.yaml` を基にフローを構成
2. `references/upload-artifact.md` でアップロード仕様を確認
3. `references/download-artifact.md` でダウンロード仕様を確認
4. `references/retention-optimization.md` で保持期間を決定

**Task**:

- `agents/design-artifact-flow.md`
- `agents/implement-artifact-steps.md`

### Phase 3: 検証と最適化

**目的**: 実装の信頼性とストレージ効率を確認する

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を検証
2. `scripts/cleanup-artifacts.mjs` で削除戦略を検討
3. `scripts/log_usage.mjs` で改善フィードバックを記録

**Task**: `agents/optimize-retention.md`

## Task仕様ナビ

| Task             | 役割                  | 入力               | 出力               | 参照先                                 | 実行タイミング |
| ---------------- | --------------------- | ------------------ | ------------------ | -------------------------------------- | -------------- |
| 利用パターン整理 | 目的と制約の整理      | ワークフロー要件   | 利用パターン要約   | `references/Level1_basics.md`          | Phase 1        |
| フロー設計       | upload/downloadの設計 | 利用パターン要約   | フロー設計メモ     | `assets/artifact-workflow.yaml`        | Phase 2 前半   |
| 実装手順整理     | 設定手順の明確化      | フロー設計メモ     | 実装チェックリスト | `references/upload-artifact.md`        | Phase 2 後半   |
| 保持最適化       | 保持期間と削除戦略    | 実装チェックリスト | 最適化メモ         | `references/retention-optimization.md` | Phase 3        |

## ベストプラクティス

### すべきこと

- 利用パターン（ジョブ間/ワークフロー間）を明確化する
- retention-days を目的に合わせて明示する
- アーティファクト名に識別子（SHA/Run ID）を含める
- 容量削減のために不要ファイルを除外する
- クリーンアップの方針を事前に決める

### 避けるべきこと

- 保持期間の無制限設定
- 古い成果物を参照するフロー設計
- 圧縮前の不要ファイル削除を省略する
- cleanup を手動運用だけに依存する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基本概念と最小チェック
- `references/Level2_intermediate.md`: 実装パターン
- `references/Level3_advanced.md`: 複数アーティファクト運用
- `references/Level4_expert.md`: 最適化とトラブルシュート
- `references/upload-artifact.md`: upload-artifact の仕様
- `references/download-artifact.md`: download-artifact の仕様
- `references/retention-optimization.md`: 保持期間と容量最適化
- `references/legacy-skill.md`: 旧版要約（移行時のみ参照）

### スクリプト

- `scripts/cleanup-artifacts.mjs`: アーティファクト削除の補助
- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/artifact-workflow.yaml`: ワークフロー例

## 変更履歴

| Version | Date       | Changes                                     |
| ------- | ---------- | ------------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備    |
| 1.0.1   | 2025-12-31 | 18-skills.md 仕様に準拠し、Task仕様ナビ追加 |
| 1.0.0   | 2025-12-24 | 初版作成                                    |
