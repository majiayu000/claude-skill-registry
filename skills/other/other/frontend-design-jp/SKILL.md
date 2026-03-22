---
name: frontend-design-jp
description: Japanese frontend and web design skill covering typography, vertical writing, form handling, accessibility (JIS X 8341-3), and common Japanese UI patterns. Triggers on requests for 日本語Webデザイン, フロントエンド, 和文タイポグラフィ, Japanese web design.
---

# 日本語フロントエンド・Webデザインスキル

## 概要

日本語Webサイト・Webアプリケーションのフロントエンド設計を支援するスキルです。和文タイポグラフィ、縦書きCSS、全角・半角フォーム処理、JIS X 8341-3アクセシビリティ対応、日本語Web特有のUIパターンをカバーします。

## 日本語Webタイポグラフィ

### フォントスタック

```css
/* ゴシック体（本文向け） */
font-family: "游ゴシック体", "Yu Gothic", YuGothic,
  "ヒラギノ角ゴ Pro", "Hiragino Kaku Gothic Pro",
  "Noto Sans JP", "メイリオ", Meiryo, sans-serif;

/* 明朝体（見出し・長文向け） */
font-family: "游明朝体", "Yu Mincho", YuMincho,
  "ヒラギノ明朝 Pro", "Hiragino Mincho Pro",
  "Noto Serif JP", serif;
```

### フォント機能設定

```css
/* プロポーショナル詰め（見出し向け） */
font-feature-settings: "palt" 1;

/* 字幅半角詰め（表組み・UIラベル向け） */
font-feature-settings: "halt" 1;

/* カーニングとリガチャの組み合わせ */
font-feature-settings: "palt" 1, "kern" 1;
```

### 行間・字間の最適値

| 用途 | line-height | letter-spacing |
|------|-------------|----------------|
| 本文（長文） | 1.8〜2.0 | 0.05em〜0.1em |
| 本文（短文） | 1.7〜1.8 | 0.04em〜0.08em |
| 見出し | 1.3〜1.5 | 0.02em〜0.05em |
| キャプション | 1.5〜1.7 | 0.03em〜0.06em |
| UI ラベル | 1.4〜1.6 | 0.02em |

## 縦書きCSS

### 基本設定

```css
.vertical-text {
  writing-mode: vertical-rl;       /* 右から左への縦書き */
  text-orientation: mixed;         /* 漢字は正立、英数字は横倒し */
  -webkit-writing-mode: vertical-rl;
}

/* 縦中横（縦書き中の2桁数字を横並びに） */
.tcy {
  text-combine-upright: all;
  -webkit-text-combine: horizontal;
}

/* 英数字を正立表示 */
.upright {
  text-orientation: upright;
}
```

### 縦書きレイアウトの注意事項
- `height` でコンテンツ領域を制御（横書きの `width` に相当）
- `overflow-x: auto` で横スクロールを許可
- 句読点・括弧はフォント側の縦書きグリフに依存する

## 全角・半角フォーム処理

### 入力値のバリデーションと変換

```javascript
/* 全角カタカナバリデーション */
const isFullWidthKatakana = (str) => /^[ァ-ヶー]+$/.test(str);

/* 半角英数バリデーション */
const isHalfWidthAlphanumeric = (str) => /^[a-zA-Z0-9]+$/.test(str);

/* 全角→半角変換（英数字） */
const toHalfWidth = (str) =>
  str.replace(/[Ａ-Ｚａ-ｚ０-９]/g, (s) =>
    String.fromCharCode(s.charCodeAt(0) - 0xFEE0));

/* 半角カタカナ→全角カタカナ変換 */
const toFullWidthKatakana = (str) =>
  str.normalize("NFKC");
```

### IME制御

```html
<!-- 日本語入力を推奨 -->
<input type="text" inputmode="text" style="ime-mode: active;"
       placeholder="お名前（全角）">

<!-- 半角英数入力を推奨 -->
<input type="email" inputmode="email" style="ime-mode: inactive;"
       placeholder="メールアドレス（半角）">
```

### 郵便番号 → 住所自動入力

```html
<input type="text" id="zipcode" inputmode="numeric"
       pattern="\d{3}-?\d{4}" placeholder="123-4567">
<script>
/* YubinBango.js や zipcloud API を利用 */
/* https://zipcloud.ibsnet.co.jp/api/search?zipcode=1234567 */
</script>
```

## JIS X 8341-3 アクセシビリティ

### 日本語固有のWCAG配慮事項

| 項目 | 対応方法 |
|------|----------|
| ルビ（ふりがな） | `<ruby>` + `<rp>` + `<rt>` を使用 |
| ルビのスクリーンリーダー対応 | `aria-label` で読み方を補足 |
| 漢字の読み上げ | 固有名詞には `lang` 属性で読みを指定 |
| フォントサイズ | 最小 16px（日本語は画数が多いため） |
| コントラスト比 | 本文 4.5:1 以上、大きな文字 3:1 以上 |
| リンクテキスト | 「こちら」「ここ」を避け、具体的な文言を使用 |

### ルビ（ふりがな）の実装

```html
<ruby>
  難読漢字<rp>（</rp><rt>なんどくかんじ</rt><rp>）</rp>
</ruby>

<!-- アクセシビリティ強化版 -->
<ruby aria-label="東京都（とうきょうと）">
  東京都<rp>（</rp><rt>とうきょうと</rt><rp>）</rp>
</ruby>
```

## 日本語Web UIパターン

### ハンバーガーメニュー（日本語ラベル付き）

```html
<button class="hamburger" aria-expanded="false" aria-label="メニューを開く">
  <span class="hamburger__icon"></span>
  <span class="hamburger__label">メニュー</span>
</button>
```

### 和暦対応日付ピッカー

```javascript
/* Intl.DateTimeFormat で和暦表示 */
const jpDate = new Intl.DateTimeFormat('ja-JP-u-ca-japanese', {
  era: 'long', year: 'numeric', month: 'long', day: 'numeric'
}).format(new Date());
/* 例: "令和6年3月4日" */
```

### 住所入力フォーム

```html
<form>
  <label>郵便番号
    <input type="text" name="zipcode" inputmode="numeric"
           autocomplete="postal-code" placeholder="123-4567">
  </label>
  <label>都道府県
    <select name="prefecture" autocomplete="address-level1">
      <option value="">選択してください</option>
      <option value="北海道">北海道</option>
      <option value="青森県">青森県</option>
      <!-- ...47都道府県 -->
    </select>
  </label>
  <label>市区町村
    <input type="text" name="city" autocomplete="address-level2">
  </label>
  <label>番地・建物名
    <input type="text" name="address" autocomplete="street-address">
  </label>
</form>
```

## 設計時の確認事項

1. **対象ブラウザ**: 日本市場ではiOS Safari のシェアが高い点に注意
2. **フォント**: Webフォント使用時はサブセット化でファイルサイズを削減
3. **文字コード**: UTF-8 を使用（Shift_JIS の外部データ連携がある場合は変換処理を追加）
4. **レスポンシブ**: 日本語は折り返し位置に注意（`word-break: break-all` の適用範囲を限定）
5. **テスト**: 実機での日本語フォント表示確認を推奨
