---
name: canvas-design-jp
description: Japanese-inspired canvas and graphic design skill for HTML5 Canvas and SVG, covering traditional aesthetics (ma, wabi-sabi, yugen), calligraphy, washi textures, traditional patterns, and seasonal motifs. Triggers on requests for 和風デザイン, Canvas描画, SVGイラスト, 日本画風, Japanese-inspired graphics.
---

# 和風Canvas・グラフィックデザインスキル

## 概要

HTML5 Canvas および SVG を用いて、日本の伝統美学にもとづくグラフィック表現を実現するスキルです。間・侘寂・幽玄の美学原則から、書道要素、和紙テクスチャ、伝統紋様、四季のモチーフまでを網羅します。

## 和風美学の原則

### 間（ま） — 余白の美

```javascript
/* 間を意識したレイアウト: 要素間に十分な余白を設ける */
const MA_RATIO = 0.618; /* 黄金比に近い余白比率 */

function applyMa(canvasWidth, contentWidth) {
  const margin = (canvasWidth - contentWidth) * MA_RATIO;
  return { left: margin, right: canvasWidth - contentWidth - margin };
}
```

- 描画要素を画面全体に詰め込まない
- 余白そのものが「意味のある空間」として機能する
- 要素の密度に緩急をつけ、視線の休息点を作る

### 侘寂（わびさび） — 不完全の美

- 完全な対称を避け、わずかなゆらぎを加える
- テクスチャに経年変化・自然な劣化を表現する
- 色彩は彩度を抑え、灰みを帯びた中間色を使う

### 幽玄（ゆうげん） — 奥深い余韻

- 半透明のレイヤーで奥行きと神秘性を演出する
- グラデーションで境界をぼかし、曖昧さを表現する
- 全体を見せず、一部を隠すことで想像力を喚起する

## 書道要素（Calligraphy Elements）

### 筆ストロークのシミュレーション

```javascript
function drawBrushStroke(ctx, points, options = {}) {
  const { maxWidth = 12, minWidth = 2, opacity = 0.85 } = options;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  for (let i = 1; i < points.length; i++) {
    const speed = distance(points[i], points[i - 1]);
    const pressure = Math.max(minWidth, maxWidth - speed * 0.1);

    /* 筆のかすれ（kasure）: 速度が速いと透明度が下がる */
    ctx.globalAlpha = Math.max(0.3, opacity - speed * 0.005);
    ctx.lineWidth = pressure;

    ctx.beginPath();
    ctx.moveTo(points[i - 1].x, points[i - 1].y);
    ctx.lineTo(points[i].x, points[i].y);
    ctx.stroke();
  }
  ctx.globalAlpha = 1.0;
}
```

### 墨（すみ）グラデーション効果

```javascript
function createSumiGradient(ctx, x, y, radius) {
  const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
  gradient.addColorStop(0, 'rgba(10, 10, 10, 0.9)');   /* 濃墨 */
  gradient.addColorStop(0.4, 'rgba(30, 30, 30, 0.6)'); /* 中墨 */
  gradient.addColorStop(0.7, 'rgba(60, 60, 60, 0.3)'); /* 淡墨 */
  gradient.addColorStop(1, 'rgba(100, 100, 100, 0)');   /* にじみ */
  return gradient;
}
```

### 筆順アニメーション

- SVG の `stroke-dasharray` + `stroke-dashoffset` でパスを順に描画
- 各画のタイミングを `animation-delay` で制御
- 筆の入り・抜きは `stroke-width` のアニメーションで表現

## 和紙テクスチャ（Washi Paper Textures）

### 手続き的な紙テクスチャ生成

```javascript
function generateWashiTexture(ctx, width, height) {
  const imageData = ctx.createImageData(width, height);
  for (let i = 0; i < imageData.data.length; i += 4) {
    const noise = Math.random() * 20 - 10;
    const base = 240; /* 生成紙色（きなり） */
    imageData.data[i]     = base + noise - 5;  /* R */
    imageData.data[i + 1] = base + noise - 8;  /* G */
    imageData.data[i + 2] = base + noise - 15; /* B */
    imageData.data[i + 3] = 255;
  }
  /* 繊維の筋をランダムに追加 */
  addFiberLines(imageData, width, height);
  ctx.putImageData(imageData, 0, 0);
}
```

### 金箔（きんぱく）効果

```javascript
function drawGoldLeaf(ctx, x, y, size) {
  /* 不均一な金箔の貼り付けを表現 */
  const gradient = ctx.createLinearGradient(x, y, x + size, y + size);
  gradient.addColorStop(0, '#C5A355');
  gradient.addColorStop(0.3, '#E8D48B');
  gradient.addColorStop(0.5, '#F5E6A3');
  gradient.addColorStop(0.7, '#D4B456');
  gradient.addColorStop(1, '#B8933E');
  ctx.fillStyle = gradient;
  /* ランダムな多角形で金箔の輪郭を描画 */
  drawIrregularPolygon(ctx, x, y, size);
}
```

### 雲母（きらら）の煌めき

- 微細なハイライトポイントをランダム配置
- `globalCompositeOperation: 'screen'` で光の重なりを表現
- マウス位置に応じて煌めきの角度を変化させる

## 日本の伝統紋様

### 家紋（かもん）描画ヘルパー

- 基本図形の組み合わせ（円、菱形、巴）で家紋を構成
- SVG `<use>` で回転対称パターンを効率的に生成
- 代表的な家紋: 丸に三つ葉葵、五三の桐、十六菊

### 組子（くみこ）幾何学パターン

```javascript
function drawKumikoPattern(ctx, x, y, size, depth) {
  if (depth === 0) return;
  /* 正三角形の分割を再帰的に描画 */
  drawTriangleGrid(ctx, x, y, size);
  /* 各三角形の中心に装飾パターンを配置 */
  const subSize = size / 2;
  drawKumikoPattern(ctx, x, y, subSize, depth - 1);
  /* 麻の葉や胡麻柄などのバリエーション */
}
```

## 四季のモチーフ（Seasonal Motifs）

### 桜の花びらアニメーション（春）

```javascript
function createSakuraPetal(ctx, x, y, size, rotation) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rotation);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.bezierCurveTo(size * 0.3, -size * 0.5,
                     size * 0.7, -size * 0.5, size, 0);
  ctx.bezierCurveTo(size * 0.7, size * 0.15,
                     size * 0.3, size * 0.15, 0, 0);
  ctx.fillStyle = 'rgba(255, 183, 197, 0.8)';
  ctx.fill();
  ctx.restore();
}
/* 花びらの落下: 重力 + 風 + 回転のパラメータで自然な動きを実現 */
```

### 紅葉の落ち葉（秋）

- 楓の葉の形状をベジェ曲線で描画（5つの突起）
- 色のグラデーション: 緑 → 黄 → 橙 → 赤 → 茶
- ひらひらと舞う動き: Y軸回転 + 横揺れ + 重力

### 雪の結晶（冬）

- 六角形の対称性を利用した再帰的描画
- 結晶のサイズ・形状にランダム性を加える
- 降雪アニメーション: 風の影響と積雪表現

### 花火（夏）

- パーティクルシステムで火花を放射状に拡散
- 尺玉・菊・牡丹・柳など日本花火の種類を再現
- 色の変化と残像効果で臨場感を演出

## 配色の参考（日本の伝統色）

| 色名 | HEX | 用途例 |
|------|------|--------|
| 紅（くれない） | #D7003A | アクセント、花 |
| 藍（あい） | #165E83 | 背景、水 |
| 鶯（うぐいす） | #928C36 | 葉、自然 |
| 朱（しゅ） | #EB6101 | 鳥居、秋 |
| 藤（ふじ） | #A48EC5 | 花、優雅さ |
| 墨（すみ） | #1C1C1C | 書道、文字 |
| 金（きん） | #C5A355 | 装飾、金箔 |

## 生成時の確認事項

1. **出力形式**: Canvas API / SVG / p5.js のいずれか
2. **アニメーション**: 静止画かアニメーションか、フレームレートの要件
3. **サイズ**: 出力解像度、Retina対応の必要性
4. **テーマ**: 季節・行事・特定の美学原則の指定
5. **パフォーマンス**: パーティクル数やテクスチャ解像度の上限
