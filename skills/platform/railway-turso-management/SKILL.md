---
name: railway-turso-management
description: |
  Railway環境でのTursoデータベース管理を専門とするスキル。
  環境グループ設計、Variables vs Secrets分類、Turso統合設定、
  Railway CLI活用、一時ファイルセキュリティの実装パターンを提供。

  Anchors:
  • 『The Pragmatic Programmer』（Hunt/Thomas）/ 適用: 設定管理・自動化 / 目的: 実践的な環境構築
  • 12-Factor App / 適用: 環境変数設計 / 目的: 設定と認証情報の分離
  • Railway公式ドキュメント / 適用: サービス設定 / 目的: プラットフォーム固有の最適化

  Trigger:
  Use when setting up Railway project secrets, configuring environment groups, integrating Turso database, using Railway CLI for local development, or securing log output.
  railway, turso, database, secrets, variables, environment, cli, libsql

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Railway Turso Database Management

## 概要

Railway環境でのTursoデータベース管理を専門とするスキル。環境グループ設計からTurso統合、CLI活用、セキュリティ確保まで、クラウドネイティブなデータベース運用の実装パターンを提供します。

## ワークフロー

### Phase 1: 要件と環境の整理

**目的**: Railway環境とTurso統合の要件を明確化する

**アクション**:

1. Railway環境グループの構成を確認（development/staging/production）
2. Turso接続情報（URL、トークン）の管理方法を決定
3. Variables vs Secretsの分類基準を適用

**Task**: `agents/analyze-environment.md` を参照

### Phase 2: シークレット設計

**目的**: 適切なシークレット管理戦略を設計する

**アクション**:

1. 機密情報（トークン、認証情報）をSecrets変数として設定
2. 非機密設定（URL、オプション）をVariables変数として設定
3. 環境グループ間での変数継承を設計

**Task**: `agents/design-secrets.md` を参照

### Phase 3: 統合実装

**目的**: Turso + Railway統合を実装する

**アクション**:

1. Turso CLIでデータベースを作成
2. Railway環境変数に接続情報を設定
3. libSQLクライアント設定を実装

**Task**: `agents/implement-integration.md` を参照

### Phase 4: 検証とセキュリティ

**目的**: 設定の正確性とセキュリティを確認する

**アクション**:

1. 接続テストを実行
2. ログ出力にシークレットが含まれないか確認
3. 環境間の分離を検証

**Task**: `agents/validate-security.md` を参照

## Task仕様ナビ

| Task                  | 起動タイミング | 入力                | 出力               |
| --------------------- | -------------- | ------------------- | ------------------ |
| analyze-environment   | Phase 1開始時  | Railwayプロジェクト | 環境要件書         |
| design-secrets        | Phase 2開始時  | 環境要件書          | シークレット設計書 |
| implement-integration | Phase 3開始時  | シークレット設計書  | 統合コード         |
| validate-security     | Phase 4開始時  | 統合コード          | 検証レポート       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                            | 理由                             |
| ----------------------------------- | -------------------------------- |
| Secretsに認証トークンを保存         | 暗号化されログに表示されない     |
| Variablesに接続URLを保存            | 非機密かつデバッグ時に参照可能   |
| 環境グループで共通設定を管理        | 重複を避け一貫性を確保           |
| Railway CLI経由でローカル開発       | 本番同等の環境変数で動作確認可能 |
| libSQL createClient でURL/Token分離 | セキュアな接続設定               |

### 避けるべきこと

| 禁止事項                         | 問題点                           |
| -------------------------------- | -------------------------------- |
| トークンをVariablesに保存        | ログに平文で表示される可能性     |
| 一時ファイルに認証情報を書き出す | ファイルシステム経由で漏洩リスク |
| console.logで接続情報を出力      | Railway Logsに記録される         |
| 環境変数のハードコード           | 環境間での切り替えが困難         |

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                               | 読込条件           |
| ------------ | ------------------------------------------------------------------ | ------------------ |
| 基礎ガイド   | [references/basics.md](references/basics.md)                       | 初回セットアップ時 |
| シークレット | [references/secrets-guide.md](references/secrets-guide.md)         | シークレット設計時 |
| Turso統合    | [references/turso-integration.md](references/turso-integration.md) | Turso接続設定時    |

### scripts/（決定論的処理）

| スクリプト              | 機能                 |
| ----------------------- | -------------------- |
| `scripts/log_usage.mjs` | スキル使用履歴の記録 |

## 変更履歴

| Version | Date       | Changes                                         |
| ------- | ---------- | ----------------------------------------------- |
| 3.1.0   | 2026-01-02 | agents/追加、references/再編成（18-skills準拠） |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、Task仕様ナビ追加      |
| 1.0.0   | 2025-12-24 | 初版                                            |
