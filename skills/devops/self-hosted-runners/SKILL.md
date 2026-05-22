---
name: self-hosted-runners
description: |
  GitHub Actionsセルフホストランナーの設計、セットアップ、セキュリティ管理を行うスキル。
  インストールから運用、トラブルシューティングまでの完全なライフサイクル管理を提供する。

  Anchors:
  • GitHub Actions Documentation / 適用: セルフホストランナー公式仕様 / 目的: 正確なAPI使用と設定
  • CIS Benchmark for Linux / 適用: ランナーホストのセキュリティ / 目的: セキュリティ強化
  • The Pragmatic Programmer / 適用: 実践的改善 / 目的: 段階的な実装と継続的改善

  Trigger:
  Use when setting up self-hosted runners, configuring runner labels, implementing security measures, troubleshooting runner issues, or optimizing runner performance.
  self-hosted, runner, GitHub Actions, ephemeral, labels, security, setup, configuration
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Self-Hosted Runners

## 概要

GitHub Actionsセルフホストランナーの設計と管理を支援するスキル。ランナーのセットアップ、ラベル設計、セキュリティ強化、トラブルシューティングをカバーする。

## ワークフロー

```
plan-runner → setup-runner → secure-runner → validate-runner
```

### Phase 1: 計画

**目的**: ランナー要件を分析し、構成を計画する

**Task**: `agents/plan-runner.md` を参照

**アクション**:

1. ワークフロー要件の分析（OS、アーキテクチャ、依存関係）
2. ランナータイプの決定（永続/エフェメラル）
3. ラベル設計

### Phase 2: セットアップ

**目的**: ランナーをインストールし設定する

**Task**: `agents/setup-runner.md` を参照

**アクション**:

1. ランナーパッケージのインストール
2. GitHubへの登録
3. サービスとしての設定

### Phase 3: セキュリティ強化

**目的**: ランナーのセキュリティを強化する

**Task**: `agents/secure-runner.md` を参照

**アクション**:

1. 専用ユーザーでの実行設定
2. ファイアウォール設定
3. ログ監視設定

### Phase 4: 検証と記録

**目的**: ランナーの動作確認と記録

**アクション**:

1. テストワークフローでの動作確認
2. ステータス監視の設定
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task          | 責務             | 入力             | 出力             |
| ------------- | ---------------- | ---------------- | ---------------- |
| plan-runner   | 要件分析・計画   | ワークフロー要件 | ランナー構成計画 |
| setup-runner  | インストール設定 | 構成計画         | 稼働ランナー     |
| secure-runner | セキュリティ強化 | 稼働ランナー     | 強化済みランナー |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                           |
| ---------------------------- | ------------------------------ |
| 専用ユーザーで実行する       | 権限分離によるセキュリティ向上 |
| エフェメラルモードを検討する | クリーンな環境で毎回実行       |
| ラベルを適切に設計する       | ワークフローの柔軟性向上       |
| 定期的にアップデートする     | セキュリティパッチの適用       |
| ログ監視を設定する           | 問題の早期発見                 |

### 避けるべきこと

| 禁止事項                     | 問題点                     |
| ---------------------------- | -------------------------- |
| rootで実行する               | セキュリティリスクが高い   |
| パブリックリポジトリで使用   | 悪意あるコードの実行リスク |
| シークレットをランナーに保存 | 認証情報漏洩のリスク       |
| アップデートを怠る           | 脆弱性が放置される         |

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                           | 読込条件           |
| ------------ | -------------------------------------------------------------- | ------------------ |
| セットアップ | [references/runner-setup.md](references/runner-setup.md)       | インストール時     |
| ラベル設計   | [references/runner-labels.md](references/runner-labels.md)     | ラベル設計時       |
| セキュリティ | [references/runner-security.md](references/runner-security.md) | セキュリティ強化時 |

### scripts/（決定論的処理）

| スクリプト                        | 機能                   |
| --------------------------------- | ---------------------- |
| `scripts/log_usage.mjs`           | 使用記録と自動評価     |
| `scripts/check-runner-status.mjs` | ランナーステータス確認 |

### assets/（テンプレート）

| アセット                      | 用途                       |
| ----------------------------- | -------------------------- |
| `assets/runner-workflow.yaml` | ランナー使用ワークフロー例 |

## 変更履歴

| Version | Date       | Changes                                            |
| ------- | ---------- | -------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills仕様完全準拠、agents/を責務ベースに再構成 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に基づきリファクタリング           |
| 1.0.0   | 2025-12-24 | 初版                                               |
