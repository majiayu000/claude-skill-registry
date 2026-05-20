---
name: web-artifacts-builder-jp
description: Simplified Japanese web artifacts builder skill for creating single-file HTML applications with Japanese UI components, i18n settings, and responsive design. Triggers on requests for Webアーティファクト, 単一HTMLファイル, HTMLツール作成, 日本語Webアプリ.
---

# Webアーティファクト構築支援スキル

## 概要

単一HTMLファイルで完結するWebアーティファクト（ミニアプリ・ツール・デモ）の構築を支援するスキルです。HTML + CSS + JavaScript を1ファイルにまとめ、日本語UIコンポーネントやi18n設定を組み込みます。

## 基本構成

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>アプリ名</title>
  <style>
    /* CSS をここに記述 */
  </style>
</head>
<body>
  <!-- HTML をここに記述 -->
  <script>
    // JavaScript をここに記述
  </script>
</body>
</html>
```

### 単一ファイルの原則

- 外部ファイルへの依存を最小限にする
- CDN経由のライブラリ読み込みは許可（Tailwind CSS, Alpine.js 等）
- 画像はBase64エンコードまたはSVGインラインで埋め込む

## 日本語UIコンポーネント

### 和暦日付ピッカー

```javascript
function toWareki(date) {
  return new Intl.DateTimeFormat('ja-JP-u-ca-japanese', {
    era: 'long', year: 'numeric', month: 'long', day: 'numeric'
  }).format(date);
}
// 例: "令和8年3月4日"
```

### 都道府県セレクター

```html
<select id="prefecture" name="prefecture">
  <option value="">都道府県を選択</option>
  <optgroup label="北海道・東北">
    <option value="01">北海道</option>
    <option value="02">青森県</option>
    <!-- ...東北各県 -->
  </optgroup>
  <optgroup label="関東">
    <option value="13">東京都</option>
    <!-- ...関東各都県 -->
  </optgroup>
  <!-- ...全47都道府県をグループ分けして配置 -->
</select>
```

### 郵便番号検索フォーム

```javascript
async function searchAddress(zipcode) {
  const code = zipcode.replace("-", "");
  const res = await fetch(
    `https://zipcloud.ibsnet.co.jp/api/search?zipcode=${code}`
  );
  const data = await res.json();
  if (data.results) {
    const addr = data.results[0];
    return {
      prefecture: addr.address1, // 都道府県
      city: addr.address2,       // 市区町村
      town: addr.address3        // 町域
    };
  }
  return null;
}
```

### ふりがな自動入力

```html
<label>氏名 <input type="text" id="name" placeholder="山田 太郎"></label>
<label>ふりがな <input type="text" id="furigana" placeholder="やまだ たろう"></label>
<script>
// compositionイベントを利用してIME入力中の読みを取得
const nameInput = document.getElementById("name");
const furiganaInput = document.getElementById("furigana");
nameInput.addEventListener("compositionupdate", (e) => {
  // 変換前のひらがな入力をふりがなフィールドに反映
  furiganaInput.value += e.data;
});
</script>
```

## i18n設定

### 必須のHTML設定

```html
<!-- 言語設定 -->
<html lang="ja">

<!-- 文字コード -->
<meta charset="UTF-8">

<!-- OGP 日本語設定 -->
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="アプリ名">
<meta property="og:description" content="アプリの説明文">
```

### 日本語ロケール対応

```javascript
// 日付フォーマット
new Intl.DateTimeFormat('ja-JP').format(date); // "2026/3/4"

// 数値フォーマット（カンマ区切り）
new Intl.NumberFormat('ja-JP').format(1234567); // "1,234,567"

// 通貨フォーマット
new Intl.NumberFormat('ja-JP', {
  style: 'currency', currency: 'JPY'
}).format(1000); // "￥1,000"
```

## フォント読み込み

### Google Fonts: Noto Sans JP

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap"
      rel="stylesheet">
<style>
  body {
    font-family: "Noto Sans JP", sans-serif;
  }
</style>
```

### フォント読み込みの注意点

- `display=swap` で FOIT（Flash of Invisible Text）を防止
- 使用するウェイトのみを指定してファイルサイズを削減
- `preconnect` でDNS解決を先行させる

## レスポンシブ対応の基本設定

```css
/* ベースのレスポンシブ設定 */
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "Noto Sans JP", sans-serif;
  line-height: 1.8;
  padding: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

/* モバイルファースト: タブレット以上 */
@media (min-width: 768px) {
  body { padding: 2rem; }
}

/* 日本語テキストの折り返し */
p, li, td {
  word-break: normal;
  overflow-wrap: break-word;
}

/* フォームの入力欄（iOSでのズーム防止: 16px以上） */
input, select, textarea {
  font-size: 16px;
}
```

## 生成時の確認事項

1. **用途**: ツール / デモ / プロトタイプ / ダッシュボード
2. **外部依存**: CDN利用の可否、使用ライブラリの指定
3. **データ永続化**: localStorage / IndexedDB の使用有無
4. **対象デバイス**: PC中心 / モバイル中心 / 両対応
