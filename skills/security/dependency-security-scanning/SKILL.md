---
name: dependency-security-scanning
description: |
  依存関係の脆弱性スキャン、CVE評価、レポート作成を体系化するスキル。
  SCAの運用と修正計画の整理を支援する。

  Anchors:
  • OWASP Dependency-Check / 適用: 依存スキャン / 目的: 検出の標準化
  • CVSS v3.1 Specification / 適用: 重大度評価 / 目的: 優先度の整合性
  • Web Application Security / 適用: 脅威評価 / 目的: リスク判定の一貫性

  Trigger:
  Use when scanning dependencies for vulnerabilities, evaluating CVE reports, producing audit reports, or planning remediation.
  dependency scan, CVE, CVSS, SCA, supply chain security, audit report
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# dependency-security-scanning

## 概要

依存関係の脆弱性スキャンから評価・レポート・修正計画までを一貫して支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 監査範囲とスキャン条件を整理する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/scan-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-scan-requirements.md` を参照

### Phase 2: スキャン実行

**目的**: 依存関係の脆弱性を検出する。

**アクション**:

1. `scripts/run-dependency-scan.mjs` を実行する。
2. `references/Level2_intermediate.md` でツールの使い分けを確認する。
3. 検出結果を整理する。

**Task**: `agents/scan-executor.md` を参照

### Phase 3: CVE評価

**目的**: 検出結果を評価し、優先度を付ける。

**アクション**:

1. `references/cve-evaluation-guide.md` で評価基準を確認する。
2. 影響範囲と優先度を記録する。
3. `references/Level3_advanced.md` を参照する。

**Task**: `agents/cve-evaluator.md` を参照

### Phase 4: レポートと修正計画

**目的**: 監査レポートと修正計画を作成する。

**アクション**:

1. `assets/dependency-audit-report-template.md` でレポートを作成する。
2. `assets/remediation-plan-template.md` で修正計画を整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/report-generator.md` と `agents/remediation-planner.md` を参照

## Task仕様ナビ

| Task                      | 起動タイミング | 入力           | 出力               |
| ------------------------- | -------------- | -------------- | ------------------ |
| analyze-scan-requirements | Phase 1開始時  | 監査範囲       | 要件メモ、制約一覧 |
| scan-executor             | Phase 2開始時  | リポジトリ情報 | スキャン結果       |
| cve-evaluator             | Phase 3開始時  | スキャン結果   | 優先度付き評価     |
| report-generator          | Phase 4開始時  | 評価結果       | 監査レポート       |
| remediation-planner       | Phase 4開始時  | 評価結果       | 修正計画           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項             | 理由               |
| -------------------- | ------------------ |
| 監査範囲を明示する   | 漏れを防止できる   |
| CVSS評価を記録する   | 優先度が明確になる |
| レポートを共有する   | 説明責任を果たせる |
| 修正計画を明文化する | 実行が容易になる   |

### 避けるべきこと

| 禁止事項         | 問題点           |
| ---------------- | ---------------- |
| 結果を放置する   | リスクが残る     |
| 優先度なしで修正 | 効果が薄い       |
| 根拠を記録しない | 追跡が困難       |
| 自動化を省略する | 継続監査が難しい |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                        | 機能                         |
| --------------------------------- | ---------------------------- |
| `scripts/run-dependency-scan.mjs` | 依存関係スキャン             |
| `scripts/validate-skill.mjs`      | スキル構造検証               |
| `scripts/log_usage.mjs`           | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                     | 読込条件   |
| ------------ | ------------------------------------------------------------------------ | ---------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)               | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | スキャン時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)           | 評価時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)               | 運用時     |
| CVE評価      | [references/cve-evaluation-guide.md](references/cve-evaluation-guide.md) | 評価時     |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)     | 仕様確認時 |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                 | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                     | 用途                 |
| -------------------------------------------- | -------------------- |
| `assets/dependency-audit-report-template.md` | 監査レポート         |
| `assets/scan-requirements-template.md`       | 要件整理テンプレート |
| `assets/remediation-plan-template.md`        | 修正計画テンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
