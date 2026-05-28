---
name: seo-optimization
description: |
  SEO最適化の専門スキル。Next.js Metadata APIを活用した検索エンジン対策、ソーシャルメディア最適化、構造化データマークアップを提供する。

  Anchors:
  • Google SEO Starter Guide / 適用: メタデータ設定と構造化データ / 目的: 検索可視性向上
  • Web Vitals Guide / 適用: パフォーマンス最適化 / 目的: ユーザー体験向上
  • Schema.org Documentation / 適用: 構造化データマークアップ / 目的: リッチリザルト対応

  Trigger:
  Use when implementing SEO optimization, setting up metadata, adding structured data markup, configuring OGP, or optimizing for search engines.
  SEO, metadata, OGP, Twitter Cards, structured data, JSON-LD, sitemap, robots.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# SEO最適化

## 概要

Next.js Metadata APIを活用したSEO最適化を実装するスキル。メタデータ設定、OGP/Twitter Cards、構造化データ、Sitemap/robots.txtをカバーする。

## ワークフロー

```
analyze-requirements → implement-metadata → validate-seo
```

### Phase 1: 要件分析

**目的**: SEO要件と対象ページを特定する

**Task**: `agents/requirements-analysis.md` を参照

**アクション**:

1. 対象ページの特定
2. 実装範囲の決定（Metadata/OGP/構造化データ）
3. 競合分析（任意）

### Phase 2: メタデータ実装

**目的**: SEO要素を実装する

**Task**: `agents/metadata-implementation.md` を参照

**アクション**:

1. Next.js Metadata API設定
2. OGP/Twitter Cardsメタタグ設定
3. JSON-LD構造化データ実装
4. Sitemap/robots.txt設定

### Phase 3: 検証と記録

**目的**: SEO設定の検証と記録

**アクション**:

1. メタデータの正確性を確認
2. Google Rich Results Testで構造化データを検証
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task                    | 責務           | 入力       | 出力               |
| ----------------------- | -------------- | ---------- | ------------------ |
| requirements-analysis   | 要件分析       | ページ情報 | SEO要件定義        |
| metadata-implementation | メタデータ実装 | SEO要件    | 実装済みメタデータ |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                        | 理由                     |
| ------------------------------- | ------------------------ |
| 各ページにユニークなtitleを設定 | 検索結果での識別性向上   |
| descriptionは160文字以内に      | 検索結果での切り捨て防止 |
| OGP画像は1200x630pxで用意       | SNS共有時の最適表示      |
| canonicalタグを設定する         | 重複コンテンツ問題の回避 |
| 構造化データを検証する          | エラーのない実装を保証   |

### 避けるべきこと

| 禁止事項                   | 問題点               |
| -------------------------- | -------------------- |
| タイトルの重複             | 検索エンジンの混乱   |
| キーワードスタッフィング   | ペナルティのリスク   |
| robots.txtでの完全ブロック | インデックス除外     |
| 構造化データのエラー放置   | リッチリザルト非表示 |

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                 | 読込条件         |
| -------------- | -------------------------------------------------------------------- | ---------------- |
| Metadata API   | [references/metadata-api-guide.md](references/metadata-api-guide.md) | メタデータ実装時 |
| OGP/Twitter    | [references/ogp-twitter-cards.md](references/ogp-twitter-cards.md)   | OGP設定時        |
| 構造化データ   | [references/structured-data.md](references/structured-data.md)       | JSON-LD実装時    |
| Sitemap/robots | [references/sitemap-robots.md](references/sitemap-robots.md)         | クローラー対策時 |

### scripts/（決定論的処理）

| スクリプト                | 機能               |
| ------------------------- | ------------------ |
| `scripts/log_usage.mjs`   | 使用記録と自動評価 |
| `scripts/analyze-seo.mjs` | SEO分析            |

### assets/（テンプレート）

| アセット                             | 用途                     |
| ------------------------------------ | ------------------------ |
| `assets/metadata-template.md`        | Metadata設定テンプレート |
| `assets/structured-data-template.md` | JSON-LDテンプレート      |

## 変更履歴

| Version | Date       | Changes                                            |
| ------- | ---------- | -------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills仕様完全準拠、agents/を責務ベースに再構成 |
| 1.0.0   | 2025-12-31 | 初版                                               |
