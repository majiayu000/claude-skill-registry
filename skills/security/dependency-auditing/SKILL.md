---
name: dependency-auditing
description: |
  依存関係の脆弱性検出、評価、修正計画を体系化するスキル。
  CVSS評価と修正優先度を整理し、継続的な監査を支援する。

  Anchors:
  • CVSS v3.1 Specification / 適用: 重大度評価 / 目的: 優先度の整合性
  • The Pragmatic Programmer / 適用: 自動化と継続改善 / 目的: 監査の継続性
  • OWASP Dependency-Check / 適用: 依存監査 / 目的: 脆弱性検出の標準化

  Trigger:
  Use when auditing dependencies, evaluating vulnerability reports, prioritizing remediation, or integrating security scans into CI/CD.
  dependency audit, CVE, GHSA, CVSS, npm audit, pnpm audit, security scanning
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# dependency-auditing

## 概要

依存関係の脆弱性を検出し、評価と修正計画を策定する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 監査範囲と制約を整理する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/audit-checklist.md` で監査要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-audit-requirements.md` を参照

### Phase 2: 脆弱性検出

**目的**: 依存関係の脆弱性を検出する。

**アクション**:

1. `scripts/security-audit.mjs` を実行する。
2. `references/vulnerability-detection.md` でツールの使い分けを確認する。
3. 結果を `assets/vulnerability-assessment-template.md` に整理する。

**Task**: `agents/vulnerability-detection.md` を参照

### Phase 3: リスク評価

**目的**: 脆弱性の重大度と優先度を評価する。

**アクション**:

1. `references/cvss-scoring-guide.md` で評価基準を確認する。
2. 影響範囲と優先度を記録する。
3. `references/remediation-strategies.md` を参照する。

**Task**: `agents/risk-assessment.md` を参照

### Phase 4: 修正計画と運用

**目的**: 修正計画を整理し、運用記録を残す。

**アクション**:

1. `assets/remediation-plan-template.md` で計画を作成する。
2. `references/ci-cd-integration.md` で自動化方針を確認する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/remediation-planning.md` を参照

## Task仕様ナビ

| Task                       | 起動タイミング | 入力           | 出力                 |
| -------------------------- | -------------- | -------------- | -------------------- |
| analyze-audit-requirements | Phase 1開始時  | 監査範囲       | 要件メモ、制約一覧   |
| vulnerability-detection    | Phase 2開始時  | リポジトリ情報 | 脆弱性一覧、検出結果 |
| risk-assessment            | Phase 3開始時  | 脆弱性一覧     | 優先度付き評価       |
| remediation-planning       | Phase 4開始時  | 評価結果       | 修正計画、運用メモ   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項           | 理由               |
| ------------------ | ------------------ |
| 監査範囲を明示する | 漏れを防げる       |
| CVSS評価を記録する | 優先度が明確になる |
| 修正計画を整理する | 実行が容易になる   |
| 自動化を組み込む   | 継続監査ができる   |

### 避けるべきこと

| 禁止事項             | 問題点           |
| -------------------- | ---------------- |
| 監査結果を放置する   | リスクが残る     |
| 優先度なしで対応する | リソースが散る   |
| 修正根拠を残さない   | 追跡が困難       |
| 自動化を省略する     | 監査が継続しない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/security-audit.mjs` | 依存監査                     |
| `scripts/validate-skill.mjs` | スキル構造検証               |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                           | 読込条件   |
| ------------ | ------------------------------------------------------------------------------ | ---------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                     | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)         | 検出時     |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)                 | 評価時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                     | 運用時     |
| 脆弱性検出   | [references/vulnerability-detection.md](references/vulnerability-detection.md) | 検出時     |
| CVSS評価     | [references/cvss-scoring-guide.md](references/cvss-scoring-guide.md)           | 評価時     |
| 修正戦略     | [references/remediation-strategies.md](references/remediation-strategies.md)   | 計画時     |
| CI/CD統合    | [references/ci-cd-integration.md](references/ci-cd-integration.md)             | 自動化時   |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)           | 仕様確認時 |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                       | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                      | 用途                   |
| --------------------------------------------- | ---------------------- |
| `assets/audit-checklist.md`                   | 監査チェックリスト     |
| `assets/vulnerability-assessment-template.md` | 脆弱性評価テンプレート |
| `assets/remediation-plan-template.md`         | 修正計画テンプレート   |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
