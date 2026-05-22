---
name: docker-best-practices
description: |
  Dockerfile最適化、セキュリティ、マルチステージビルドを体系化するスキル。
  イメージ最適化とローカル開発環境の設計を支援する。

  Anchors:
  • Dockerfile Best Practices / 適用: レイヤー最適化 / 目的: ビルド効率向上
  • Image Security / 適用: 最小権限 / 目的: セキュリティ強化
  • Multi-stage Builds / 適用: ビルド分離 / 目的: イメージ最小化

  Trigger:
  Use when optimizing Dockerfiles, improving image security, or designing local development container setups.
  dockerfile optimization, image security, multi-stage build, docker compose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# docker-best-practices

## 概要

Dockerfile最適化からセキュリティ強化、ローカル開発環境の設計までを整理する。

## ワークフロー

### Phase 1: 要件整理

**目的**: コンテナ化の目的と制約を明確化する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/docker-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-docker-requirements.md` を参照

### Phase 2: Dockerfile設計

**目的**: Dockerfileとビルド戦略を設計する。

**アクション**:

1. `references/dockerfile-optimization.md` で最適化方針を確認する。
2. `references/multi-stage-builds.md` でビルド分離を整理する。
3. `assets/dockerfile-review-checklist.md` で設計観点を揃える。

**Task**: `agents/design-dockerfile-plan.md` を参照

### Phase 3: 実装と環境整備

**目的**: コンテナ設定と開発環境を整備する。

**アクション**:

1. `assets/nodejs-dockerfile-template.dockerfile` を参照して実装する。
2. `assets/docker-compose-template.yml` を参照して開発環境を整える。
3. `references/image-security.md` でセキュリティ方針を確認する。

**Task**: `agents/implement-container-setup.md` を参照

### Phase 4: 検証と運用

**目的**: イメージ品質を検証し記録を更新する。

**アクション**:

1. `scripts/analyze-image.mjs` で検証する。
2. `assets/image-evaluation-template.md` で結果を整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-image-quality.md` を参照

## Task仕様ナビ

| Task                        | 起動タイミング | 入力      | 出力                       |
| --------------------------- | -------------- | --------- | -------------------------- |
| analyze-docker-requirements | Phase 1開始時  | 目的/制約 | 要件メモ、対象範囲         |
| design-dockerfile-plan      | Phase 2開始時  | 要件メモ  | Dockerfile設計、最適化方針 |
| implement-container-setup   | Phase 3開始時  | 設計方針  | 実装方針、環境構成         |
| validate-image-quality      | Phase 4開始時  | 実装方針  | 検証レポート、改善提案     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                 |
| -------------------------- | -------------------- |
| マルチステージビルドを使う | イメージを小さくする |
| 非root実行を徹底する       | セキュリティを高める |
| キャッシュを活用する       | ビルド時間を短縮する |
| 検証結果を記録する         | 改善が継続する       |

### 避けるべきこと

| 禁止事項               | 問題点               |
| ---------------------- | -------------------- |
| 不要ファイルを含める   | イメージが肥大化する |
| セキュリティ検証を省略 | リスクが増える       |
| 目的外のツール導入     | 運用が複雑化する     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/analyze-image.mjs`  | イメージ分析                 |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証             |

### references/（詳細知識）

| リソース             | パス                                                                           | 読込条件   |
| -------------------- | ------------------------------------------------------------------------------ | ---------- |
| レベル1 基礎         | [references/Level1_basics.md](references/Level1_basics.md)                     | 要件整理時 |
| レベル2 実務         | [references/Level2_intermediate.md](references/Level2_intermediate.md)         | 設計時     |
| レベル3 応用         | [references/Level3_advanced.md](references/Level3_advanced.md)                 | 実装時     |
| レベル4 専門         | [references/Level4_expert.md](references/Level4_expert.md)                     | 改善時     |
| Dockerfile最適化     | [references/dockerfile-optimization.md](references/dockerfile-optimization.md) | 設計時     |
| イメージセキュリティ | [references/image-security.md](references/image-security.md)                   | 実装時     |
| マルチステージ       | [references/multi-stage-builds.md](references/multi-stage-builds.md)           | 設計時     |
| ローカル開発         | [references/local-development.md](references/local-development.md)             | 環境整備時 |
| 要求仕様索引         | [references/requirements-index.md](references/requirements-index.md)           | 仕様確認時 |
| 旧スキル             | [references/legacy-skill.md](references/legacy-skill.md)                       | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                       | 用途                   |
| ---------------------------------------------- | ---------------------- |
| `assets/docker-requirements-template.md`       | 要件整理テンプレート   |
| `assets/dockerfile-review-checklist.md`        | Dockerfileチェック     |
| `assets/image-evaluation-template.md`          | 検証テンプレート       |
| `assets/nodejs-dockerfile-template.dockerfile` | Dockerfileテンプレート |
| `assets/docker-compose-template.yml`           | Composeテンプレート    |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
