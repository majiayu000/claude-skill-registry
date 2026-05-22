---
name: infrastructure-as-code
description: |
  Infrastructure as Code（IaC）の原則に基づく構成管理の自動化を専門とするスキル。
  環境変数管理、Secret管理、Railway統合を中心に、再現可能で安全なインフラ構成を実現します。

  Anchors:
  • 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）/ 適用: 設定の外部化・DRY原則・エラーの早期検出 / 目的: 保守性とセキュリティの両立
  • IaC 4原則（宣言的定義・べき等性・バージョン管理・不変インフラ）/ 適用: インフラ構成全体 / 目的: 再現可能性の確保

  Trigger:
  Use when designing environment variables, managing secrets, configuring Railway deployments, or setting up infrastructure as code for Next.js/Electron projects.
  Keywords: railway.json, .env.example, environment variables, GitHub Secrets, Railway Secrets, Turso integration, infrastructure automation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Infrastructure as Code

## 概要

Infrastructure as Codeの原則に基づく構成管理の自動化を専門とするスキル。
環境変数管理、Secret管理、Railway統合を中心に、再現可能なインフラ構成を実現します。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 環境変数設計

**目的**: プロジェクトの環境変数構成を設計し、.env.exampleを整備

**アクション**:

1. 必要な環境変数を洗い出し
2. 命名規則と分類を決定
3. バリデーションルールを定義
4. `assets/env-example-template.txt` をベースに.env.example作成

**Task**: `agents/environment-design.md` を参照

### Phase 2: シークレット管理

**目的**: GitHub Secrets/Railway Secretsの安全な管理戦略を実装

**アクション**:

1. シークレット分類（開発/ステージング/本番）
2. ローテーション戦略の策定
3. アクセス制御の設定

**Task**: `agents/secret-manager.md` を参照

### Phase 3: Railway統合構成

**目的**: Railway.jsonとデプロイ構成の最適化

**アクション**:

1. `assets/railway-json-template.json` をベースに設定
2. 環境別ビルド/スタートコマンド定義
3. `scripts/validate-env.mjs` で検証

**Task**: `agents/railway-configurator.md` を参照

### Phase 4: 検証と完了

**目的**: 構成の整合性確認と記録

**アクション**:

1. `agents/railway-validator.md` で検証実行
2. 環境間の差分レポート作成
3. `scripts/log_usage.mjs` で記録

## ベストプラクティス

### すべきこと

- Railway構成を設計・最適化する時
- 環境変数とSecretの管理戦略を設計する時
- 複数環境間の構成差分を最小化する時
- ローカル開発環境とクラウド環境を同期する時

### 避けるべきこと

- シークレットをソースコードにハードコード
- 環境変数のバリデーションを省略
- 環境間の設定差分を文書化せずに運用

## Task仕様ナビ

| Task             | 起動タイミング | 入力             | 出力                 | 参照エージェント                 |
| ---------------- | -------------- | ---------------- | -------------------- | -------------------------------- |
| 環境変数設計     | Phase 1開始時  | プロジェクト要件 | .env.example         | `agents/environment-design.md`   |
| シークレット管理 | Phase 2開始時  | 機密情報リスト   | シークレット管理計画 | `agents/secret-manager.md`       |
| Railway構成      | Phase 3開始時  | 環境変数設計書   | railway.json         | `agents/railway-configurator.md` |
| 構成検証         | Phase 4開始時  | 全構成ファイル   | 検証レポート         | `agents/railway-validator.md`    |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## リソース参照

### references/（詳細知識）

| リソース   | パス                              | 内容             |
| ---------- | --------------------------------- | ---------------- |
| 基礎知識   | references/Level1_basics.md       | IaC基本概念      |
| 実務ガイド | references/Level2_intermediate.md | 環境変数管理実践 |
| 高度な技法 | references/Level3_advanced.md     | マルチ環境戦略   |
| 専門知識   | references/Level4_expert.md       | セキュリティ強化 |

### scripts/（決定論的処理）

| スクリプト       | 用途         | 使用例                                        |
| ---------------- | ------------ | --------------------------------------------- |
| validate-env.mjs | 環境変数検証 | `node scripts/validate-env.mjs`               |
| log_usage.mjs    | 使用記録     | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート               | 用途                    |
| -------------------------- | ----------------------- |
| env-example-template.txt   | .env.example雛形        |
| railway-json-template.json | Railway構成テンプレート |

## コマンドリファレンス

### リソース読み取り

```bash
cat .claude/skills/infrastructure-as-code/references/Level1_basics.md
cat .claude/skills/infrastructure-as-code/references/Level2_intermediate.md
cat .claude/skills/infrastructure-as-code/references/Level3_advanced.md
cat .claude/skills/infrastructure-as-code/references/Level4_expert.md
cat .claude/skills/infrastructure-as-code/references/environment-variables.md
cat .claude/skills/infrastructure-as-code/references/iac-principles.md
cat .claude/skills/infrastructure-as-code/references/legacy-skill.md
cat .claude/skills/infrastructure-as-code/references/railway-integration.md
cat .claude/skills/infrastructure-as-code/references/secrets-management.md
```

### スクリプト実行

```bash
node .claude/skills/infrastructure-as-code/scripts/log_usage.mjs --help
node .claude/skills/infrastructure-as-code/scripts/validate-env.mjs --help
node .claude/skills/infrastructure-as-code/scripts/validate-skill.mjs --help
```

### テンプレート参照

```bash
cat .claude/skills/infrastructure-as-code/assets/env-example-template.txt
cat .claude/skills/infrastructure-as-code/assets/railway-json-template.json
```

## 変更履歴

| Version | Date       | Changes                                        |
| ------- | ---------- | ---------------------------------------------- |
| 2.1.0   | 2026-01-02 | ワークフローをPhase別に再構成、agents/参照追加 |
| 2.0.0   | 2026-01-02 | 18-skills.md完全準拠、Task仕様ナビ追加         |
| 1.0.0   | 2025-12-24 | 初版                                           |
