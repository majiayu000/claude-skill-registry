---
name: authentication-docs
description: |
  API認証ドキュメント（OAuth 2.0/PKCE、API Key、JWT、トークン管理）の作成と図解を支援するスキル。
  認証フローの説明、トークン取得手順、セキュリティ注意点をわかりやすく整理します。

  Anchors:
  • OAuth 2.0 Simplified / 適用: フロー図解 / 目的: 正確な説明と用語整理
  • Web Application Security / 適用: セキュリティ注意点 / 目的: 安全な認証ドキュメント
  • API Documentation Best Practices / 適用: ドキュメント構成 / 目的: 読みやすさの担保

  Trigger:
  Use when writing authentication docs, creating OAuth flow diagrams, documenting token management, or preparing quickstart guides for API auth.
allowed-tools:
  - bash
  - node
---

# API認証ドキュメント作成スキル

## 概要

認証フローの図解、トークン取得手順、セキュリティ注意点を整理して、読み手が実装できる状態にする。
必要な詳細は `references/` に外部化し、必要時に参照する。

- クイックスタートは `assets/auth-quickstart.md`
- 図解は `assets/oauth2-diagrams.md`

## ワークフロー

### Phase 1: 目的と対象フローの整理

**目的**: 認証方式とドキュメントの対象範囲を明確化する

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認
2. 対象フロー（OAuth/API Key/JWT）を整理
3. 読者の前提知識を整理

**Task**: `agents/define-doc-scope.md`

### Phase 2: 図解と手順の作成

**目的**: フロー図解と実装手順を作成する

**アクション**:

1. `references/oauth2-flows.md` でフロー仕様を確認
2. `assets/oauth2-diagrams.md` で図解を作成
3. `references/token-management.md` でトークン説明を補強
4. `assets/auth-quickstart.md` をベースに手順を作成

**Task**:

- `agents/create-flow-diagrams.md`
- `agents/write-quickstart.md`

### Phase 3: セキュリティ確認と仕上げ

**目的**: セキュリティ注意点と品質チェックを行う

**アクション**:

1. `references/security-best-practices.md` で注意点を確認
2. `scripts/test-auth-endpoint.sh` でサンプルを検証
3. `scripts/log_usage.mjs` で改善記録を残す

**Task**: `agents/review-security-notes.md`

## Task仕様ナビ

| Task                 | 役割                 | 入力         | 出力               | 参照先                                  | 実行タイミング |
| -------------------- | -------------------- | ------------ | ------------------ | --------------------------------------- | -------------- |
| 範囲定義             | 対象フローの整理     | 要件情報     | スコープメモ       | `references/Level1_basics.md`           | Phase 1        |
| 図解作成             | OAuthフロー図作成    | スコープメモ | Mermaid図          | `assets/oauth2-diagrams.md`             | Phase 2 前半   |
| 手順作成             | クイックスタート作成 | 図解/要件    | ガイド本文         | `assets/auth-quickstart.md`             | Phase 2 後半   |
| セキュリティレビュー | 注意点の整理         | ガイド本文   | セキュリティ注意点 | `references/security-best-practices.md` | Phase 3        |

## ベストプラクティス

### すべきこと

- 読者の前提知識を明確にする
- フロー図と手順を必ずセットで提示する
- トークンの有効期限と更新手順を明記する
- セキュリティ注意点を別セクションで整理する

### 避けるべきこと

- シークレットや実キーを例に含める
- 図解のみで説明を省略する
- 方式を限定して他方式の選択肢を隠す

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基本概念
- `references/Level2_intermediate.md`: 実務手順
- `references/Level3_advanced.md`: 高度な設計
- `references/Level4_expert.md`: 複合フロー
- `references/oauth2-flows.md`: OAuthフロー詳細
- `references/token-management.md`: トークン管理
- `references/security-best-practices.md`: セキュリティ指針
- `references/legacy-skill.md`: 旧版要約（移行時のみ参照）

### スクリプト

- `scripts/generate-auth-flow-diagram.sh`: 図生成補助
- `scripts/test-auth-endpoint.sh`: エンドポイント確認
- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/auth-quickstart.md`: クイックスタート
- `assets/oauth2-diagrams.md`: 図解テンプレ

## 変更履歴

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備 |
| 1.0.0   | 2025-12-24 | 初版作成                                 |
