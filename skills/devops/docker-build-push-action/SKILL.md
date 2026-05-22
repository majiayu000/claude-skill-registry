---
name: docker-build-push-action
description: |
  GitHub ActionsでのDockerビルド/プッシュを設計・実装するスキル。
  レジストリ認証、キャッシュ戦略、マルチプラットフォーム対応を整理する。

  Anchors:
  • docker/build-push-action / 適用: ビルドとプッシュ / 目的: 自動化
  • BuildKit / 適用: キャッシュ最適化 / 目的: ビルド高速化
  • Registry Authentication / 適用: 認証設計 / 目的: 安全な配布

  Trigger:
  Use when configuring GitHub Actions for Docker build and push, managing registry auth, or optimizing BuildKit cache.
  docker build push action, buildx, registry auth, github actions docker
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# docker-build-push-action

## 概要

GitHub ActionsでのDockerビルド/プッシュを体系化し、キャッシュと認証設計を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: ビルド対象とレジストリ要件を明確化する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/build-push-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-build-push-requirements.md` を参照

### Phase 2: ワークフロー設計

**目的**: ビルド/プッシュのワークフローを設計する。

**アクション**:

1. `references/build-push-syntax.md` で構文を確認する。
2. `references/registry-auth.md` で認証方針を整理する。
3. `assets/registry-checklist.md` で設計観点を揃える。

**Task**: `agents/design-workflow-configuration.md` を参照

### Phase 3: 実装と設定

**目的**: workflow とキャッシュ設定を実装する。

**アクション**:

1. `assets/docker-workflow.yaml` を参照して実装する。
2. `references/Level2_intermediate.md` でキャッシュ設定を確認する。
3. 設定メモを作成する。

**Task**: `agents/implement-build-push-pipeline.md` を参照

### Phase 4: 検証と運用

**目的**: Dockerfileとワークフローの検証を行う。

**アクション**:

1. `scripts/analyze-dockerfile.mjs` で分析する。
2. `assets/workflow-evaluation-template.md` で結果を整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-build-push-workflow.md` を参照

## Task仕様ナビ

| Task                            | 起動タイミング | 入力      | 出力                       |
| ------------------------------- | -------------- | --------- | -------------------------- |
| analyze-build-push-requirements | Phase 1開始時  | 目的/制約 | 要件メモ、対象一覧         |
| design-workflow-configuration   | Phase 2開始時  | 要件メモ  | ワークフロー設計、認証方針 |
| implement-build-push-pipeline   | Phase 3開始時  | 設計方針  | 実装メモ、設定案           |
| validate-build-push-workflow    | Phase 4開始時  | 実装メモ  | 検証レポート、改善提案     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項             | 理由                   |
| -------------------- | ---------------------- |
| キャッシュを設定する | ビルド時間を短縮できる |
| 認証をSecretsで管理  | セキュリティを保つ     |
| タグ戦略を統一する   | リリースが追跡しやすい |
| 検証結果を記録する   | 改善が継続する         |

### 避けるべきこと

| 禁止事項             | 問題点           |
| -------------------- | ---------------- |
| 資格情報の埋め込み   | 漏洩リスクが高い |
| キャッシュ無効化     | CIが遅くなる     |
| 非推奨アクション使用 | 更新リスクが高い |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                       | 機能                         |
| -------------------------------- | ---------------------------- |
| `scripts/analyze-dockerfile.mjs` | Dockerfile分析               |
| `scripts/log_usage.mjs`          | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`     | スキル構造の検証             |

### references/（詳細知識）

| リソース     | パス                                                                   | 読込条件   |
| ------------ | ---------------------------------------------------------------------- | ---------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)             | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時     |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)         | 実装時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)             | 改善時     |
| 構文ガイド   | [references/build-push-syntax.md](references/build-push-syntax.md)     | 設計時     |
| 認証ガイド   | [references/registry-auth.md](references/registry-auth.md)             | 認証設計時 |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)   | 仕様確認時 |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                     | 用途                 |
| -------------------------------------------- | -------------------- |
| `assets/build-push-requirements-template.md` | 要件整理テンプレート |
| `assets/registry-checklist.md`               | 認証チェック         |
| `assets/workflow-evaluation-template.md`     | 検証テンプレート     |
| `assets/docker-workflow.yaml`                | ワークフロー例       |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
