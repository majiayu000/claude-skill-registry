---
name: documentation
description: ドキュメントの作成・編集・確認を行う際に使用。Docusaurus構成、コンテンツ構造、ローカルプレビュー、OpenAPI仕様書に役立つ。
---

# ドキュメント開発ガイド

## 概要

idp-serverのドキュメントはDocusaurusで構築。日英対応。

- **公開URL**: https://hirokazu-kobayashi-koba-hiro.github.io/idp-server/
- **フレームワーク**: Docusaurus 3.x

---

## ディレクトリ構造

```
documentation/
├── docs/                           # メインコンテンツ
│   ├── content_01_intro/          # イントロダクション
│   ├── content_02_quickstart/     # クイックスタート
│   ├── content_03_concepts/       # コンセプト・設計思想
│   ├── content_04_protocols/      # プロトコル仕様
│   ├── content_05_how-to/         # 設定・構築ガイド
│   ├── content_06_developer-guide/ # 開発者ガイド
│   ├── content_07_reference/      # リファレンス
│   ├── content_08_ops/            # 運用・デプロイ
│   ├── content_09_project/        # プロジェクト情報
│   ├── content_10_ai_developer/   # AI開発者向け詳細リファレンス
│   ├── content_11_learning/       # 学習コンテンツ・チュートリアル
│   ├── content_20_testing/        # テスト関連
│   ├── document-index.md          # ドキュメントガイド（読者別）
│   └── introduction.md            # はじめに
│
├── openapi/                        # OpenAPI仕様書
│   ├── control-plane/             # 管理API仕様
│   └── application-plane/         # OAuth/OIDC API仕様
│
├── architecture/                   # アーキテクチャ図
├── blog/                          # ブログ記事
├── src/                           # Docusaurusカスタムコンポーネント
├── static/                        # 静的ファイル（画像等）
├── docusaurus.config.js           # Docusaurus設定
├── sidebars.js                    # サイドバー設定
└── package.json
```

---

## コンテンツカテゴリ

| カテゴリ | 対象読者 | 内容 |
|---------|---------|------|
| **content_01_intro** | 全員 | プロジェクト概要、技術概要、機能一覧 |
| **content_02_quickstart** | 全員 | 環境構築、初回起動 |
| **content_03_concepts** | 開発者/運用者 | 設計思想、アーキテクチャ概念 |
| **content_04_protocols** | 開発者 | OAuth 2.0/OIDC/CIBA/FAPI仕様 |
| **content_05_how-to** | 構築担当者 | 段階的な設定ガイド |
| **content_06_developer-guide** | 開発者 | 実装ガイド、コード解説 |
| **content_07_reference** | 開発者 | APIリファレンス |
| **content_08_ops** | 運用者 | デプロイ、監視、運用 |
| **content_09_project** | コントリビューター | 貢献ガイド、ロードマップ |
| **content_10_ai_developer** | AI/開発者 | 詳細な内部実装リファレンス |
| **content_11_learning** | 学習者 | 技術基礎（OAuth/OIDC/FIDO/JWT/PostgreSQL/K8s等） |
| **content_20_testing** | 開発者/QA | テスト戦略、テストガイド |

---

## ローカルプレビュー

### 起動

```bash
cd documentation
npm install
npm run start
```

### 日本語版

```bash
npm run start -- --locale ja
```

### ビルド

```bash
npm run build
```

---

## ドキュメント作成

### ファイル命名規則

```
{カテゴリ}-{連番}-{説明}.md

例:
- quickstart-01-getting-started.md
- concept-02-multi-tenant.md
- developer-03-token-endpoint.md
```

### Front Matter

```markdown
---
sidebar_position: 1
title: ページタイトル
description: ページの説明（SEO用）
---

# 見出し

本文...
```

### サイドバー順序

`sidebar_position` で順序を制御:

```markdown
---
sidebar_position: 1  # 1番目に表示
---
```

---

## 開発者ガイド構造

```
content_06_developer-guide/
├── 01-getting-started/            # 開発環境構築
├── 02-control-plane/              # 管理API実装ガイド
├── 03-application-plane/          # OAuth/OIDC実装ガイド
├── 04-implementation-guides/      # 機能別実装ガイド
├── 05-configuration/              # 設定ガイド
├── 06-patterns/                   # 共通実装パターン
├── 07-troubleshooting/            # トラブルシューティング
├── 08-reference/                  # リファレンス
└── learning-paths/                # 学習パス
    ├── 01-beginner.md
    ├── 02-control-plane-track.md
    ├── 03-application-plane-track.md
    └── 04-full-stack-track.md
```

---

## AI開発者向けドキュメント

`content_10_ai_developer/` はClaude Code向けの詳細リファレンス:

| ファイル | 内容 |
|---------|------|
| `ai-10-use-cases.md` | EntryService実装パターン |
| `ai-11-core.md` | Coreモジュール詳細 |
| `ai-12-adapters.md` | アダプター実装 |
| `ai-21-extension-fapi.md` | FAPI拡張 |
| `ai-31-extension-ciba.md` | CIBA拡張 |
| `ai-41-extension-ida.md` | 身元確認拡張 |

---

## OpenAPI仕様書

```
openapi/
├── control-plane/
│   ├── organization-api.yaml      # 組織管理API
│   ├── tenant-api.yaml            # テナント管理API
│   ├── client-api.yaml            # クライアント管理API
│   └── user-api.yaml              # ユーザー管理API
│
└── application-plane/
    ├── oauth-api.yaml             # OAuth 2.0 API
    ├── oidc-api.yaml              # OpenID Connect API
    └── ciba-api.yaml              # CIBA API
```

### OpenAPI編集

```bash
# Lint
npx @redocly/cli lint openapi/control-plane/organization-api.yaml

# プレビュー
npx @redocly/cli preview-docs openapi/control-plane/organization-api.yaml
```

---

## 多言語対応

### ディレクトリ構造

```
documentation/
├── docs/                  # デフォルト（英語）
└── i18n/
    └── ja/
        └── docusaurus-plugin-content-docs/
            └── current/   # 日本語版
```

### 翻訳追加

```bash
# 翻訳ファイル生成
npm run write-translations -- --locale ja
```

---

## コマンド一覧

```bash
# 開発サーバー起動
npm run start

# 日本語版
npm run start -- --locale ja

# ビルド
npm run build

# ビルド結果プレビュー
npm run serve

# 翻訳ファイル生成
npm run write-translations -- --locale ja

# OpenAPI Lint
npx @redocly/cli lint openapi/**/*.yaml
```

---

## よく編集するファイル

| 目的 | ファイル |
|------|---------|
| サイドバー構成変更 | `sidebars.js` |
| サイト設定変更 | `docusaurus.config.js` |
| トップページ編集 | `src/pages/index.js` |
| 新規ドキュメント追加 | `docs/content_XX_*/` |
| OpenAPI編集 | `openapi/` |

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `/onboarding` | プロジェクト全体像・学習ロードマップ |
| `/architecture` | アーキテクチャ詳細 |
| `/control-plane` | 管理API実装 |
