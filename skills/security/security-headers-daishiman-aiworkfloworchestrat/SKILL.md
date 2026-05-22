---
name: security-headers
description: |
  HTTPセキュリティヘッダー設定の専門スキル。
  CSP、HSTS、X-Frame-Options、CSRF対策などの設計・実装・検証を体系的に提供する。
  Next.js/Express/Nginx等の環境に対応した具体的な実装パターンを含む。

  Anchors:
  • OWASP Secure Headers Project / 適用: ヘッダー設定基準 / 目的: 業界標準準拠
  • Web Application Security (Andrew Hoffman) / 適用: 脅威モデリング / 目的: 攻撃ベクトル理解
  • MDN Web Docs - HTTP Headers / 適用: ディレクティブ仕様 / 目的: 正確な構文

  Trigger:
  Use when implementing security headers, configuring CSP, setting up CSRF protection, or hardening HTTP responses.
  security headers, CSP, Content-Security-Policy, HSTS, X-Frame-Options, CSRF, XSS prevention, セキュリティヘッダー
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# セキュリティヘッダー

## 概要

Webアプリケーションのセキュリティヘッダー設定パターンを体系的に提供するスキル。Content Security Policy（CSP）、HSTS、X-Frame-Options、CSRF対策などの設計・実装・検証までを一貫してサポートする。

## ワークフロー

```
analyze-requirements → implement-headers → validate-headers
```

### Task 1: 要件分析（analyze-requirements）

プロジェクトのセキュリティ要件を分析し、必要なヘッダーを特定する。

**Task**: `agents/analyze-requirements.md` を参照

### Task 2: ヘッダー実装（implement-headers）

要件に基づいて適切なセキュリティヘッダーを実装する。

**Task**: `agents/implement-headers.md` を参照

### Task 3: ヘッダー検証（validate-headers）

実装されたセキュリティヘッダーの正確性と有効性を検証する。

**Task**: `agents/validate-headers.md` を参照

## Task仕様（ナビゲーション）

| Task                 | 責務         | 入力             | 出力             |
| -------------------- | ------------ | ---------------- | ---------------- |
| analyze-requirements | 要件分析     | プロジェクト情報 | セキュリティ要件 |
| implement-headers    | ヘッダー実装 | セキュリティ要件 | 設定ファイル     |
| validate-headers     | ヘッダー検証 | 設定ファイル     | 検証レポート     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- プロジェクトの技術スタックに適したヘッダー設定方法を選択する
- CSPは段階的に導入し、report-onlyモードで影響を確認する
- SameSite Cookie属性を活用してCSRF対策の基盤とする
- HSTSは十分なテスト後にpreloadを有効化する
- 設定後は必ず検証スクリプトで動作確認を行う

### 避けるべきこと

- `unsafe-inline`や`unsafe-eval`を安易に使用しない
- セキュリティヘッダーを無闘に厳しく設定して正常な機能を破損させない
- HSTSをテスト環境でpreload付きで有効化しない
- Origin/Referer検証のみに依存したCSRF対策を行わない
- 設定内容を検証なしに本番環境にデプロイしない

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                                   | 用途                       |
| ------------ | ---------------------------------------------------------------------- | -------------------------- |
| ヘッダー種類 | See [references/header-types.md](references/header-types.md)           | 各ヘッダーの機能と設定方法 |
| CSP設定      | See [references/csp-configuration.md](references/csp-configuration.md) | CSPディレクティブ詳細      |
| CSRF対策     | See [references/csrf-prevention.md](references/csrf-prevention.md)     | CSRF防御の多層戦略         |

### scripts/（決定論的処理）

| スクリプト                      | 用途               | 使用例                                             |
| ------------------------------- | ------------------ | -------------------------------------------------- |
| `validate-security-headers.mjs` | ヘッダー設定の検証 | `node scripts/validate-security-headers.mjs <url>` |
| `log_usage.mjs`                 | フィードバック記録 | `node scripts/log_usage.mjs --result success`      |

### assets/（テンプレート）

| テンプレート                          | 用途                              |
| ------------------------------------- | --------------------------------- |
| `nextjs-security-headers-template.js` | Next.js用セキュリティヘッダー設定 |

## 変更履歴

| Version | Date       | Changes                                                                |
| ------- | ---------- | ---------------------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠マイグレーション（Task分離、責務ベースreferences） |
| 1.1.0   | 2025-12-31 | 日本語化、Trigger/Anchor追加                                           |
| 1.0.0   | 2025-12-24 | 初版作成                                                               |
