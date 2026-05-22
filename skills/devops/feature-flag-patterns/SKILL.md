---
name: feature-flag-patterns
description: |
  機能フラグ（Feature Flag/Feature Toggle）による段階的リリースとA/Bテスト実装スキル。
  リスク管理とカナリアリリースを可能にし、本番環境での安全な機能展開を実現します。

  Anchors:
  • Feature Toggles (Pete Hodgson - Martin Fowler blog) / 適用: フラグ設計パターン / 目的: Release/Experiment/Ops/Permission Togglesの適切な使い分け
  • Continuous Delivery (Jez Humble) / 適用: デプロイ戦略 / 目的: デプロイと機能リリースの分離による安全性向上

  Trigger:
  Use when implementing feature flags, feature toggles, A/B testing, gradual rollouts, canary releases, or managing feature lifecycles.
  feature flag, feature toggle, A/B testing, canary release, gradual rollout, dark launch, percentage rollout, kill switch
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
tags:
  - deployment
  - release-management
  - feature-management
  - devops
---

# feature-flag-patterns

## 概要

機能フラグによる段階的リリースとA/Bテスト実装スキル。
デプロイと機能リリースを分離し、本番環境でのリスクを最小化する。

---

## ワークフロー

### Phase 1: フラグ設計

**目的**: 機能フラグの種類・スコープ・ライフサイクルを決定

**アクション**:

1. 機能要件から適切なフラグタイプを選択（Release/Experiment/Ops/Permission）
2. フラグのスコープを決定（global/user/organization/request）
3. ライフサイクル計画を策定（一時的 vs 長期的）
4. 必要なリソースレベル（Level 1-4）を判定

**Task**: `agents/design-flag.md` を参照

### Phase 2: フラグ実装

**目的**: 選択されたパターンに基づいてフラグを実装

**アクション**:

1. `assets/flag-template.ts` を使用してフラグ定義を作成
2. `references/implementation-patterns.md` でパターンを確認
3. フラグ評価ロジックを実装（クライアント/サーバー）
4. テストケースを作成（全状態をカバー）

**Task**: `agents/implement-flag.md` を参照

### Phase 3: 段階的ロールアウト

**目的**: 安全な段階的リリース戦略の実行

**アクション**:

1. `references/rollout-strategies.md` でロールアウト戦略を選択
2. パーセンテージベースまたはコホートベースの展開を実装
3. メトリクス収集とモニタリングを設定
4. ロールバック手順を準備

**Task**: `agents/rollout-flag.md` を参照

### Phase 4: フラグ管理とクリーンアップ

**目的**: フラグライフサイクル管理とテクニカルデット防止

**アクション**:

1. `scripts/audit-flags.mjs` でフラグ一覧を監査
2. 古いフラグや不要なフラグを特定
3. フラグ削除計画を策定
4. `scripts/log_usage.mjs` で使用記録を保存

**Task**: `agents/manage-flags.md` を参照

---

## Task仕様ナビ

| Task           | 起動タイミング | 入力           | 出力                   |
| -------------- | -------------- | -------------- | ---------------------- |
| design-flag    | Phase 1開始時  | 機能要件       | フラグ設計書           |
| implement-flag | Phase 2開始時  | フラグ設計書   | 実装コード＋テスト     |
| rollout-flag   | Phase 3開始時  | 実装コード     | ロールアウト計画＋設定 |
| manage-flags   | Phase 4開始時  | 既存フラグ一覧 | クリーンアップ計画     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                                 |
| -------------------------- | ------------------------------------ |
| フラグに有効期限を設定     | テクニカルデット防止                 |
| デフォルト値を安全な状態に | フラグサービス障害時の安全性確保     |
| フラグ評価ログを記録       | デバッグとトラブルシューティング支援 |
| 段階的ロールアウト実施     | リスク最小化（1%→10%→50%→100%）      |
| Kill Switchを準備          | 緊急時の即座な機能無効化             |
| フラグごとにオーナーを指定 | 責任の明確化とクリーンアップ促進     |

### 避けるべきこと

| 禁止事項                     | 問題点                                 |
| ---------------------------- | -------------------------------------- |
| フラグのネスト               | 複雑性の爆発的増加（2^n の組み合わせ） |
| ビジネスロジックへの埋め込み | コードの可読性低下                     |
| 無期限のフラグ保持           | テクニカルデットの蓄積                 |
| フラグなしでのテスト         | 全状態の検証漏れ                       |
| フラグ命名の不統一           | 管理の困難化                           |

---

## リソース参照

### references/（詳細知識）

| リソース                 | パス                                                                           | 読込条件             |
| ------------------------ | ------------------------------------------------------------------------------ | -------------------- |
| 基礎概念                 | [references/Level1_basics.md](references/Level1_basics.md)                     | 初回利用時           |
| 実装パターン             | [references/Level2_intermediate.md](references/Level2_intermediate.md)         | 実装時               |
| 高度な戦略               | [references/Level3_advanced.md](references/Level3_advanced.md)                 | 複雑なロールアウト時 |
| エキスパートパターン     | [references/Level4_expert.md](references/Level4_expert.md)                     | スケール・最適化時   |
| 実装パターン詳細         | [references/implementation-patterns.md](references/implementation-patterns.md) | Phase 2実行時        |
| ロールアウト戦略         | [references/rollout-strategies.md](references/rollout-strategies.md)           | Phase 3実行時        |
| フラグタイプリファレンス | [references/flag-types.md](references/flag-types.md)                           | フラグタイプ選択時   |
| アンチパターン集         | [references/anti-patterns.md](references/anti-patterns.md)                     | 設計レビュー時       |

### scripts/（決定論的処理）

| スクリプト                  | 機能                   |
| --------------------------- | ---------------------- |
| `scripts/audit-flags.mjs`   | フラグ一覧の監査と分析 |
| `scripts/validate-flag.mjs` | フラグ定義の検証       |
| `scripts/log_usage.mjs`     | フィードバック記録     |

### assets/（テンプレート）

| アセット                         | 用途                         |
| -------------------------------- | ---------------------------- |
| `assets/flag-template.ts`        | TypeScript フラグ定義        |
| `assets/flag-config-schema.json` | フラグ設定のJSON Schema      |
| `assets/rollout-plan.md`         | ロールアウト計画テンプレート |

---

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 1.0.0   | 2025-12-31 | 初版作成。18-skills.md完全準拠版。 |
