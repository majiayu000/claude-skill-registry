---
name: railway-secrets-management
description: |
  Railwayプラットフォーム上でのシークレット管理を専門とするスキル。環境変数設定、シークレットローテーション、アクセス制御を体系的に支援し、セキュアで運用しやすいデプロイメント環境を実現します。

  Anchors:
  • Web Application Security (Andrew Hoffman) / 適用: 脅威モデリングとリスク評価 / 目的: セキュアなシークレット管理設計
  • Railway Documentation / 適用: Variables API・Service Variables / 目的: Railway固有機能の理解と活用
  • The Twelve-Factor App / 適用: 環境変数による設定管理 / 目的: クラウドネイティブな設定パターン

  Trigger:
  Use when configuring Railway secrets, rotating credentials, designing access control, managing environment-specific variables, or implementing secure secret management practices on Railway platform.
  Keywords: railway secrets, environment variables, secret rotation, railway variables api, service variables, railway security, credential management
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Railway Secrets Management

## 概要

Railwayプラットフォーム上でのシークレット管理を専門とするスキル。環境変数の設定、シークレットのローテーション、アクセス制御の設計を通じて、セキュアで運用しやすいデプロイメント環境を実現します。

## ワークフロー

### Phase 1: 設計・計画

**目的**: シークレット管理の要件を分析し、設定戦略を決定する

**Task**: `agents/design-secret-strategy.md`

**入力**:

- アプリケーションの環境構成（dev/staging/prod）
- 必要なシークレットの種類（API Keys, DB credentials等）
- アクセス制御要件

**出力**:

- シークレット管理戦略書
- 環境別設定マトリクス
- ローテーションポリシー
- 権限マトリクス

**実行タイミング**: Railway環境の初期セットアップ時、セキュリティ要件の見直し時

### Phase 2: 実装

**目的**: Railway Variables APIを使用してシークレットを設定・管理する

**Task**: `agents/implement-secrets.md`

**入力**:

- Phase 1の設計書
- 実際のシークレット値（セキュア管理下）
- 環境識別子

**出力**:

- 設定済みのRailway Variables
- 自動化スクリプト
- 設定完了レポート

**実行タイミング**: 初期セットアップ時、新規シークレット追加時

### Phase 3: 運用・ローテーション

**目的**: シークレットの定期的なローテーションとアクセス監査を実施する

**Task**: `agents/rotate-and-audit.md`

**入力**:

- 既存のシークレット設定
- ローテーションポリシー
- アクセスログ

**出力**:

- ローテーション実施レポート
- 監査レポート
- 改善提案

**実行タイミング**: 定期ローテーション時（90日ごと）、セキュリティインシデント後

## Task仕様

| Task                   | 起動タイミング | 入力                   | 出力                   |
| ---------------------- | -------------- | ---------------------- | ---------------------- |
| design-secret-strategy | Phase 1開始時  | アプリケーション要件   | シークレット管理戦略書 |
| implement-secrets      | Phase 2開始時  | 設計書・シークレット値 | 設定完了レポート       |
| rotate-and-audit       | Phase 3開始時  | ローテーションポリシー | 監査レポート           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

- [agents/design-secret-strategy.md](agents/design-secret-strategy.md)
- [agents/implement-secrets.md](agents/implement-secrets.md)
- [agents/rotate-and-audit.md](agents/rotate-and-audit.md)

## ベストプラクティス

### すべきこと

- 環境ごとに異なるシークレットを使用する（dev/staging/prod分離）
- シークレットをコードリポジトリにコミットしない
- Railway Service Variablesを活用してサービス固有の設定を管理
- 定期的なシークレットローテーションを実施（最低90日ごと）
- アクセス権限を最小限に制限（Principle of Least Privilege）
- シークレット変更時は監査ログを確認

### 避けるべきこと

- ハードコードされたシークレットをソースコードに含める
- 全環境で同一のシークレットを使い回す
- ローテーション計画なしでシークレットを運用する
- シークレットをプレーンテキストでログに出力する
- 不要になったシークレットを削除せず放置する

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                   | 内容                    |
| -------------------- | ---------------------------------------------------------------------- | ----------------------- |
| 基礎知識             | [references/Level1_basics.md](references/Level1_basics.md)             | Railway Variablesの基礎 |
| 実務パターン         | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 環境別設定パターン      |
| ローテーション自動化 | [references/Level3_advanced.md](references/Level3_advanced.md)         | 自動化スクリプト設計    |
| 高度なセキュリティ   | [references/Level4_expert.md](references/Level4_expert.md)             | エンタープライズ設計    |

### scripts/（決定論的処理）

| スクリプト           | 用途         | 使用例                                                       |
| -------------------- | ------------ | ------------------------------------------------------------ |
| `log_usage.mjs`      | 使用履歴記録 | `node scripts/log_usage.mjs --result success --phase design` |
| `validate-skill.mjs` | 構造検証     | `node scripts/validate-skill.mjs`                            |

## 変更履歴

| Version | Date       | Changes                                                 |
| ------- | ---------- | ------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠: agents/作成、ワークフロー強化 |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠: Trigger英語化、Anchors追加        |
| 1.0.0   | 2025-12-24 | 初版: 基本構造とリソース整備                            |
