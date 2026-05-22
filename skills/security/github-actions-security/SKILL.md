---
name: github-actions-security
description: |
  GitHub Actionsワークフローのセキュリティ強化スキル。Repository/Environment Secretsの安全管理、ログマスキング、品質ゲート統合、CI/CDパイプラインの脅威対策を行う。

  Anchors:
  • OWASP Top 10 CI/CD Security Risks / 適用: リスク評価・脅威特定 / 目的: 業界標準に基づくリスク優先度決定
  • GitHub Actions Security Hardening Guide / 適用: ワークフロー実装 / 目的: 公式ベストプラクティス準拠
  • Threat Modeling (Adam Shostack) / 適用: STRIDE脅威分析 / 目的: 体系的なセキュリティ設計

  Trigger:
  Use when securing GitHub Actions workflows, configuring Environment/Repository Secrets, implementing log masking, adding quality gates to CI/CD pipelines, or performing threat modeling on workflows.
  github actions security, secrets management, log masking, quality gate, CI/CD security, threat modeling
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# GitHub Actions Security

## 概要

GitHub Actionsワークフローのセキュリティを包括的に強化するスキル。Environment SecretsとRepository Secretsの安全な管理、機密情報のログマスキング、CI/CDパイプラインへの品質ゲート統合、脅威モデリングに基づくセキュリティ設計を行う。

## ワークフロー

### Phase 1: セキュリティ診断

**目的**: ワークフローのセキュリティリスクを評価

**アクション**:

1. 対象ワークフローを特定し、シークレット利用箇所を洗い出す
2. OWASP CI/CD Top 10に基づくリスク評価を実施
3. 既存のセキュリティ対策の有効性を確認

**Task**: `agents/diagnose-security.md` を参照

### Phase 2: セキュリティ実装

**目的**: 具体的なセキュリティ対策を実装

**アクション**:

1. Environment/Repository Secretsを適切に設定
2. ログマスキング（add-mask）を実装
3. 品質ゲート（脆弱性スキャン、SAST/DAST）を統合
4. 権限を最小権限の原則に基づいて設定

**Task**: `agents/implement-security.md` を参照

### Phase 3: 検証と監査

**目的**: セキュリティ実装の有効性を検証

**アクション**:

1. `scripts/validate-workflow-security.mjs` で自動検証
2. 脅威モデリングレポートを作成
3. 残存リスクと対応計画を記録

**Task**: `agents/validate-security.md` を参照

## Task仕様ナビ

| Task               | 起動タイミング | 入力                   | 出力                         |
| ------------------ | -------------- | ---------------------- | ---------------------------- |
| diagnose-security  | Phase 1開始時  | ワークフローYAML       | リスク評価レポート           |
| implement-security | Phase 2開始時  | リスク評価レポート     | セキュア化されたワークフロー |
| validate-security  | Phase 3開始時  | セキュア化ワークフロー | 検証レポート、脅威モデル     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- すべてのシークレットをEnvironment/Repository Secretsで管理する
- `add-mask` を使用してログ出力時に機密情報をマスキングする
- ワークフローの実行権限を最小権限の原則に基づいて設定する
- 外部アクションは信頼できるもののみ使用し、バージョンを固定する
- CI/CDパイプラインに脆弱性スキャン、依存関係チェックを統合する
- 本番環境デプロイには手動承認フローを設定する

### 避けるべきこと

- ワークフロー内に平文でシークレットを記述しない
- 信頼できないリポジトリからのアクションを使用しない
- `secrets.GITHUB_TOKEN` を不必要な権限で使用しない
- ログマスキングなしでシークレット値を出力しない
- 品質ゲートなしで本番デプロイを実行しない

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                               | 内容             |
| -------------- | ------------------------------------------------------------------ | ---------------- |
| 基礎知識       | See [references/basics.md](references/basics.md)                   | セキュリティ概念 |
| 実装パターン   | See [references/patterns.md](references/patterns.md)               | 具体的な実装例   |
| 脅威モデリング | See [references/threat-modeling.md](references/threat-modeling.md) | STRIDE分析手法   |

### scripts/（決定論的処理）

| スクリプト                       | 用途               | 使用例                                                           |
| -------------------------------- | ------------------ | ---------------------------------------------------------------- |
| `validate-workflow-security.mjs` | ワークフロー検証   | `node scripts/validate-workflow-security.mjs .github/workflows/` |
| `log_usage.mjs`                  | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"`  |

### assets/（テンプレート）

| テンプレート                 | 用途                           |
| ---------------------------- | ------------------------------ |
| `secure-deploy-template.yml` | セキュアなデプロイワークフロー |

## 変更履歴

| Version | Date       | Changes                                                    |
| ------- | ---------- | ---------------------------------------------------------- |
| 3.1.0   | 2026-01-05 | CI/CDカバレッジ統合で使用、Secrets管理・権限設計の実績追加 |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、構造再編成                       |
| 2.0.0   | 2025-12-31 | Anchors/Trigger統合、Task仕様ナビ追加                      |
| 1.0.0   | 2025-12-24 | 初版                                                       |
