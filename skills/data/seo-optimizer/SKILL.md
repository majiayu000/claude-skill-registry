---
name: seo-optimizer
description: Analyze and optimize web pages for SEO including meta tags, structured data, and performance. Use when improving website SEO or analyzing search optimization.
---

# SEO Optimizer Skill

SEO最適化の提案を行うスキルです。

## 概要

Webページのメタデータ、構造化データ、コンテンツをSEOの観点から分析・最適化します。

## 主な機能

- **メタタグ最適化**: title、description、OGタグ
- **構造化データ**: JSON-LD、Schema.org
- **セマンティックHTML**: 適切なタグ使用
- **パフォーマンス**: Core Web Vitals
- **モバイル対応**: レスポンシブデザイン
- **内部リンク**: サイト構造の最適化
- **画像最適化**: alt、サイズ、形式

## 使用方法

```
以下のHTMLをSEO最適化：
[HTML]

チェック項目:
- メタタグ
- 構造化データ
- セマンティックHTML
```

## 最適化例

### メタタグ

**最適化前**:
```html
<head>
  <title>Home</title>
</head>
```

**最適化後**:
```html
<head>
  <!-- 基本メタタグ -->
  <title>高品質なWebサービス | 会社名 - 信頼できるソリューション</title>
  <meta name="description" content="会社名では、高品質なWebサービスを提供しています。信頼性と使いやすさを兼ね備えた、お客様のビジネスを加速するソリューションです。">
  <meta name="keywords" content="Webサービス, クラウド, SaaS, ビジネスツール">

  <!-- Open Graph (Facebook, LinkedIn) -->
  <meta property="og:title" content="高品質なWebサービス | 会社名">
  <meta property="og:description" content="会社名では、高品質なWebサービスを提供しています。">
  <meta property="og:image" content="https://example.com/og-image.jpg">
  <meta property="og:url" content="https://example.com">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="会社名">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="高品質なWebサービス | 会社名">
  <meta name="twitter:description" content="会社名では、高品質なWebサービスを提供しています。">
  <meta name="twitter:image" content="https://example.com/twitter-image.jpg">
  <meta name="twitter:site" content="@company">

  <!-- その他 -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://example.com">
</head>
```

### 構造化データ

**記事ページ**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "初心者のためのSEO完全ガイド",
  "description": "SEOの基礎から実践まで、初心者でもわかりやすく解説します。",
  "image": "https://example.com/article-image.jpg",
  "author": {
    "@type": "Person",
    "name": "山田太郎"
  },
  "publisher": {
    "@type": "Organization",
    "name": "会社名",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2024-06-15",
  "dateModified": "2024-06-20"
}
</script>
```

**商品ページ**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "高性能ノートPC",
  "image": "https://example.com/laptop.jpg",
  "description": "最新のプロセッサを搭載した高性能ノートパソコン",
  "brand": {
    "@type": "Brand",
    "name": "ブランド名"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product/laptop",
    "priceCurrency": "JPY",
    "price": "128000",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "24"
  }
}
</script>
```

### セマンティックHTML

**最適化前**:
```html
<div class="header">
  <div class="nav">...</div>
</div>
<div class="main">
  <div class="article">...</div>
</div>
```

**最適化後**:
```html
<header>
  <nav aria-label="メインナビゲーション">...</nav>
</header>
<main>
  <article>
    <h1>記事タイトル</h1>
    <p>...</p>
  </article>
</main>
<footer>...</footer>
```

### 見出し構造

**最適化前**:
```html
<h1>サイト名</h1>
<h3>セクション1</h3>
<h2>セクション2</h2>
```

**最適化後**:
```html
<h1>ページタイトル（1ページに1つ）</h1>
<h2>主要セクション1</h2>
  <h3>サブセクション1-1</h3>
  <h3>サブセクション1-2</h3>
<h2>主要セクション2</h2>
  <h3>サブセクション2-1</h3>
```

### 画像最適化

**最適化前**:
```html
<img src="photo.jpg">
```

**最適化後**:
```html
<img
  src="photo-800w.webp"
  srcset="photo-400w.webp 400w,
          photo-800w.webp 800w,
          photo-1200w.webp 1200w"
  sizes="(max-width: 600px) 400px,
         (max-width: 900px) 800px,
         1200px"
  alt="東京タワーの夜景写真"
  width="800"
  height="600"
  loading="lazy">
```

## チェックリスト

### On-Page SEO

- [ ] 適切なタイトルタグ（50-60文字）
- [ ] メタディスクリプション（150-160文字）
- [ ] H1タグ（1ページに1つ）
- [ ] 見出し階層（H1 → H2 → H3）
- [ ] 画像のalt属性
- [ ] 内部リンク
- [ ] Canonical URL
- [ ] モバイルフレンドリー
- [ ] ページ速度
- [ ] HTTPS

### 構造化データ

- [ ] JSON-LD形式
- [ ] 適切なスキーマタイプ
- [ ] 必須プロパティ
- [ ] バリデーション通過

### コンテンツ

- [ ] ユニークで価値あるコンテンツ
- [ ] 適切なキーワード密度
- [ ] 読みやすい文章
- [ ] 内部リンク
- [ ] 外部リンク（信頼できるソース）

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
このページをSEO最適化：
[HTML]

改善項目:
- メタタグ
- 構造化データ
- 画像最適化
```

SEO最適化されたHTMLが生成されます！
