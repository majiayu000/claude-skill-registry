---
name: wa-theme-factory
description: Generate Japanese-style (和風) CSS/design themes with CSS custom properties and Tailwind CSS support. 10 preset themes including 桜, 藍染, 紅葉, 雪月花, 茶室, 浮世絵, 禅, 祭, 未来, 和紙. Triggers on requests for 和風テーマ, 和風CSS, Japanese theme, 和風デザイントークン, テーマ生成.
---

# 和風テーマファクトリー

## 概要

日本の美意識に基づいた CSS テーマを生成するスキルです。10種類のプリセットテーマを提供し、CSS カスタムプロパティ（変数）と Tailwind CSS 互換の形式で出力します。各テーマは色彩・タイポグラフィ・余白・ボーダー・背景パターンを包括的に定義しています。

## プリセットテーマ一覧

| テーマ名 | ファイル | 雰囲気 | キーカラー |
|---|---|---|---|
| **桜** | [themes/sakura.md](themes/sakura.md) | 春の柔らかさ、優美 | ピンク・ラベンダー |
| **藍染** | [themes/aizome.md](themes/aizome.md) | 伝統・信頼・誠実 | インディゴ・ブルー |
| **紅葉** | [themes/momiji.md](themes/momiji.md) | 秋の豊穣、情趣 | レッド・ゴールド |
| **雪月花** | [themes/setsugekka.md](themes/setsugekka.md) | 冬の静寂、雅 | シルバーブルー・ゴールド |
| **茶室** | [themes/chashitsu.md](themes/chashitsu.md) | 侘寂・静寂・自然 | アース・抹茶 |
| **浮世絵** | [themes/ukiyoe.md](themes/ukiyoe.md) | 大胆・芸術・江戸 | ブルー・朱赤 |
| **禅** | [themes/zen.md](themes/zen.md) | ミニマル・静謐 | グレー・苔緑 |
| **祭** | [themes/matsuri.md](themes/matsuri.md) | 活気・祝祭・躍動 | 赤・金 |
| **未来** | [themes/mirai.md](themes/mirai.md) | サイバー・近未来 | ネオンパープル・シアン |
| **和紙** | [themes/washi.md](themes/washi.md) | 自然・有機的・温もり | ベージュ・モスグリーン |

## 用途別テーマ選択ガイド

### ビジネス用途

| シーン | 推奨テーマ | 理由 |
|---|---|---|
| コーポレートサイト | **藍染** | 信頼感と誠実さを表現。落ち着いた配色がプロフェッショナルな印象を与える |
| コンサルティング | **茶室** | 侘寂の美学が知性と落ち着きを伝える。クライアントへの安心感 |
| 士業・金融 | **禅** | ミニマルで格式ある印象。情報の可読性を最大化 |

### カジュアル用途

| シーン | 推奨テーマ | 理由 |
|---|---|---|
| ブログ・メディア | **桜** | 柔らかい色調が読者に親しみを与える。長時間の閲覧に適した配色 |
| イベント・キャンペーン | **祭** | 活気と祝祭感でユーザーの注目を集める。期間限定の華やかさ |
| ポートフォリオ | **和紙** | 自然な温もりが作品を引き立てる。クリエイターの個性を表現 |

### クリエイティブ用途

| シーン | 推奨テーマ | 理由 |
|---|---|---|
| アート・ギャラリー | **浮世絵** | 大胆な配色が芸術性を強調。視覚的インパクトが強い |
| ハンドメイド・クラフト | **和紙** | 有機的な質感が手仕事の温かみと共鳴する |
| デザインスタジオ | **禅** | 作品を際立たせる余白重視のデザイン |

### 季節テーマ

| 季節 | 推奨テーマ | 活用シーン |
|---|---|---|
| **春** | **桜** | 入学・入社シーズン、新生活キャンペーン |
| **夏** | **祭** | 夏祭り、サマーセール、花火大会 |
| **秋** | **紅葉** | 紅葉狩り、収穫祭、秋の味覚フェア |
| **冬** | **雪月花** | クリスマス、年末年始、冬のギフト |

### モダン・テック用途

| シーン | 推奨テーマ | 理由 |
|---|---|---|
| テックスタートアップ | **未来** | サイバーパンク調の配色が革新性を表現。ダークテーマで没入感 |
| SaaS ダッシュボード | **藍染** or **禅** | 長時間使用に耐える落ち着いた配色。データの視認性を確保 |
| ゲーム・エンタメ | **未来** | ネオンカラーが躍動感とワクワク感を演出 |

## テーマの使い方

### CSS カスタムプロパティの適用

各テーマファイルに定義された CSS カスタムプロパティを `:root` に設定します。

```css
/* テーマファイルから CSS 変数をコピーして使用 */
:root {
  /* 各テーマの変数をここに貼り付け */
}

/* 変数の使用例 */
body {
  background-color: var(--wa-bg);
  color: var(--wa-text);
  font-family: var(--wa-font-body);
}

h1, h2, h3 {
  color: var(--wa-primary);
  font-family: var(--wa-font-heading);
}

.btn-primary {
  background-color: var(--wa-primary);
  color: var(--wa-bg);
  border-radius: var(--wa-radius);
}

.btn-accent {
  background-color: var(--wa-accent);
  color: var(--wa-bg);
}

.card {
  background-color: var(--wa-surface);
  border: var(--wa-border);
  border-radius: var(--wa-radius);
  padding: var(--wa-spacing-lg);
}
```

### Tailwind CSS での使用

`tailwind.config.js` の `extend` にテーマの値を設定します。

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      // 各テーマファイルの Tailwind 設定をここにマージ
    }
  }
}
```

### テーマの切り替え

複数テーマをサポートする場合は `data-theme` 属性で切り替えます。

```css
[data-theme="sakura"] {
  --wa-primary: #FEDFE1;
  /* ... */
}

[data-theme="aizome"] {
  --wa-primary: #264348;
  /* ... */
}
```

```js
// JavaScript でのテーマ切り替え
document.documentElement.setAttribute('data-theme', 'sakura');
```

## CSS 変数の命名規則

すべてのテーマで共通の変数名を使用しています。

| 変数名 | 説明 |
|---|---|
| `--wa-primary` | メインカラー |
| `--wa-primary-light` | メインカラーの明るいバリエーション |
| `--wa-primary-dark` | メインカラーの暗いバリエーション |
| `--wa-accent` | アクセントカラー |
| `--wa-bg` | 背景色 |
| `--wa-surface` | カード・パネルの背景色 |
| `--wa-text` | メインテキスト色 |
| `--wa-text-muted` | 補助テキスト色 |
| `--wa-border` | ボーダースタイル |
| `--wa-radius` | 角丸の大きさ |
| `--wa-shadow` | ボックスシャドウ |
| `--wa-font-heading` | 見出し用フォント |
| `--wa-font-body` | 本文用フォント |
| `--wa-spacing-sm` | 小さい余白 |
| `--wa-spacing-md` | 中程度の余白 |
| `--wa-spacing-lg` | 大きい余白 |
| `--wa-spacing-xl` | 特大余白 |
| `--wa-transition` | トランジション設定 |

## 生成時の確認事項

テーマを選択・カスタマイズする前に、以下を確認してください：

1. **用途**: ビジネス / カジュアル / クリエイティブ / テック
2. **季節性**: 通年使用 / 季節限定
3. **ダークモード**: 対応が必要か
4. **フレームワーク**: 素の CSS / Tailwind / その他
5. **カスタマイズ**: プリセットそのまま / 色の調整が必要か
