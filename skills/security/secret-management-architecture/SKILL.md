---
name: secret-management-architecture
description: |
  シークレット管理アーキテクチャの設計・実装スキル。
  Vault/KMS/Secrets Manager統合、キーローテーション、アクセス制御マトリクスを体系的に設計する。
  シークレット分類からライフサイクル管理まで、エンタープライズグレードの機密情報管理戦略を提供。

  Anchors:
  • Clean Architecture (Robert C. Martin) / 適用: 依存関係ルール / 目的: シークレット管理層の分離
  • Zero Trust Architecture (NIST SP 800-207) / 適用: 認証・認可 / 目的: 最小権限アクセス
  • OWASP Secrets Management Cheat Sheet / 適用: 実装パターン / 目的: セキュリティベストプラクティス
  • HashiCorp Vault Best Practices / 適用: Vault統合 / 目的: シークレットバックエンド設計

  Trigger:
  Use when designing secret management architecture, integrating Vault/KMS, planning key rotation, or creating access control matrices.
  secret management, vault integration, key rotation, access control, KMS, secrets manager, credential management
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Secret Management Architecture

## 概要

シークレット管理アーキテクチャスキルは、環境変数、HashiCorp Vault、AWS KMS、AWS Secrets Managerなど複数のシークレット保管・管理システムを統合し、エンタープライズグレードの機密情報管理戦略を設計・実装する。

**主要機能**:

- **分類とガバナンス**: シークレット重要度別の保護レベル設計
- **ライフサイクル管理**: 生成・配布・ローテーション・廃棄の一連プロセス
- **アクセス制御**: RBAC/ABACによる最小権限実装
- **バックエンド統合**: Vault/KMS/Secrets Managerの統合アーキテクチャ
- **監査とコンプライアンス**: アクセスログと監査証跡の確保

## ワークフロー

```
analyze-requirements → classify-secrets → design-architecture
                                                  ↓
validate-architecture ← integrate-backend ← design-access-control
                                                  ↑
                                          design-rotation
```

### Task 1: 要件分析（analyze-requirements）

シークレット管理の要件を分析し、スコープと制約を明確化する。

**Task**: `agents/analyze-requirements.md` を参照

### Task 2: シークレット分類（classify-secrets）

シークレットを重要度・用途別に分類し、保護レベルを決定する。

**Task**: `agents/classify-secrets.md` を参照

### Task 3: アーキテクチャ設計（design-architecture）

シークレット管理の全体アーキテクチャを設計する。

**Task**: `agents/design-architecture.md` を参照

### Task 4: ローテーション戦略（design-rotation）

キーローテーション戦略と自動化フローを設計する。

**Task**: `agents/design-rotation.md` を参照

### Task 5: アクセス制御設計（design-access-control）

RBAC/ABACベースのアクセス制御マトリクスを設計する。

**Task**: `agents/design-access-control.md` を参照

### Task 6: バックエンド統合（integrate-backend）

Vault/KMS/Secrets Managerとの統合設計を行う。

**Task**: `agents/integrate-backend.md` を参照

### Task 7: アーキテクチャ検証（validate-architecture）

設計されたアーキテクチャがセキュリティ要件を満たすことを検証する。

**Task**: `agents/validate-architecture.md` を参照

## Task仕様（ナビゲーション）

| Task                  | 責務                   | 入力               | 出力                   |
| --------------------- | ---------------------- | ------------------ | ---------------------- |
| analyze-requirements  | 要件分析               | ビジネス要件       | 要件定義書             |
| classify-secrets      | シークレット分類       | シークレット一覧   | 分類マトリクス         |
| design-architecture   | アーキテクチャ設計     | 要件・分類結果     | アーキテクチャ設計書   |
| design-rotation       | ローテーション戦略設計 | アーキテクチャ     | ローテーション計画書   |
| design-access-control | アクセス制御設計       | アーキテクチャ     | アクセス制御マトリクス |
| integrate-backend     | バックエンド統合設計   | アーキテクチャ     | 統合設計書             |
| validate-architecture | アーキテクチャ検証     | 全設計ドキュメント | 検証レポート           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照
**注記**: 1 Task = 1 責務。複数責務を1ファイルに入れない。

## ベストプラクティス

### すべきこと

- **事前分析**: `references/classification-framework.md` でシークレット分類基準を確認
- **段階的導入**: 開発→ステージング→本番の順で段階的に導入
- **最小権限**: Principle of Least Privilegeを実装し、RBACを設計
- **ライフサイクル**: 生成・配布・ローテーション・廃棄の全フェーズを定義
- **監査ログ**: すべてのアクセスと変更を監査ログに記録
- **バックアップ**: 重要なシークレット設定のバックアップと災害復旧手順を確立
- **テスト検証**: `scripts/validate-architecture.mjs` でアーキテクチャ整合性を検証

### 避けるべきこと

- **ハードコード**: コードにシークレットをハードコードしない
- **ログ出力**: シークレットをログファイルやスタックトレースに出力しない
- **バージョン管理**: シークレットをGitリポジトリにコミットしない
- **単一バックエンド**: 単一の管理システムに依存しない、冗長性を確保
- **無制限アクセス**: 必要最小限の権限のみ付与
- **ローテーションなし**: 定期的なローテーション計画なしでの運用
- **監査なし**: アクセスログや変更履歴の監査機能なしでの運用
- **環境混在**: 開発環境と本番環境のシークレットを混在させない

## リソース参照

### references/（詳細知識）

**注記**: references/ は責務/ドメイン単位で分割し、1ファイル=1責務を基本とする。

| リソース                                                                  | 説明                           | 対象タスク            |
| ------------------------------------------------------------------------- | ------------------------------ | --------------------- |
| See [classification-framework.md](references/classification-framework.md) | シークレット分類フレームワーク | classify-secrets      |
| See [architecture-patterns.md](references/architecture-patterns.md)       | アーキテクチャパターン         | design-architecture   |
| See [rotation-strategies.md](references/rotation-strategies.md)           | ローテーション戦略             | design-rotation       |
| See [access-control-patterns.md](references/access-control-patterns.md)   | アクセス制御パターン           | design-access-control |
| See [vault-integration.md](references/vault-integration.md)               | Vault統合パターン              | integrate-backend     |
| See [kubernetes-secrets.md](references/kubernetes-secrets.md)             | Kubernetes Secrets管理         | integrate-backend     |
| See [compliance-checklist.md](references/compliance-checklist.md)         | コンプライアンスチェックリスト | validate-architecture |

### scripts/（決定論的処理）

| スクリプト                  | 用途               | 使用例                                                              |
| --------------------------- | ------------------ | ------------------------------------------------------------------- |
| `validate-architecture.mjs` | アーキテクチャ検証 | `node scripts/validate-architecture.mjs --config architecture.yaml` |
| `log_usage.mjs`             | 使用記録           | `node scripts/log_usage.mjs --result success --phase "Task 7"`      |

### assets/（テンプレート）

| テンプレート                | 用途                   | 対象               |
| --------------------------- | ---------------------- | ------------------ |
| `env-template.md`           | 環境変数設定のサンプル | 開発環境構築       |
| `rotation-plan-template.md` | ローテーション計画書   | ライフサイクル管理 |
| `inventory-template.md`     | シークレット棚卸し表   | 監査・管理         |
| `access-matrix-template.md` | アクセス制御マトリクス | アクセス制御設計   |

## 変更履歴

| Version | Date       | Changes                                                   |
| ------- | ---------- | --------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠: Task分離、責務ベースreferences/ |
| 1.1.0   | 2025-12-31 | YAML frontmatter改善、Task仕様ナビ追加                    |
| 1.0.0   | 2025-12-24 | 初版作成                                                  |
