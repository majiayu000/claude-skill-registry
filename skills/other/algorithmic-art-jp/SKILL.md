---
name: algorithmic-art-jp
description: Japanese algorithmic and generative art skill covering traditional pattern generation (wagara), calligraphy simulation, zen garden generators, and mathematical patterns from Japanese art. Triggers on requests for 和柄生成, ジェネラティブアート, アルゴリズミックアート, 伝統紋様パターン, Japanese generative art.
---

# 日本のアルゴリズミック・ジェネラティブアートスキル

## 概要

日本の伝統的な紋様・技法をアルゴリズムで再現するジェネラティブアートスキルです。和柄パターン生成、書道シミュレーション、枯山水ジェネレーター、日本美術に由来する数理パターンをコードで表現します。出力は p5.js、Canvas API、SVG に対応します。

## 和柄パターン生成

### 市松模様（いちまつもよう）

```javascript
function drawIchimatsu(ctx, cols, rows, cellSize, color1, color2) {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      ctx.fillStyle = (x + y) % 2 === 0 ? color1 : color2;
      ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
    }
  }
}
```

### 麻の葉（あさのは）

```javascript
function drawAsanoha(ctx, cx, cy, size) {
  /* 正六角形の中心から6本の線を放射し、各三角形内に菱形を描画 */
  const angles = [0, 60, 120, 180, 240, 300];
  const vertices = angles.map(a => ({
    x: cx + size * Math.cos(a * Math.PI / 180),
    y: cy + size * Math.sin(a * Math.PI / 180)
  }));
  /* 外枠の六角形 */
  drawPolygon(ctx, vertices);
  /* 中心から各頂点への放射線 */
  vertices.forEach(v => drawLine(ctx, cx, cy, v.x, v.y));
  /* 各三角形の中線を追加して麻の葉形状を完成 */
  for (let i = 0; i < 6; i++) {
    const mid = midpoint(vertices[i], vertices[(i + 1) % 6]);
    drawLine(ctx, cx, cy, mid.x, mid.y);
    drawLine(ctx, mid.x, mid.y, vertices[i].x, vertices[i].y);
    drawLine(ctx, mid.x, mid.y, vertices[(i + 1) % 6].x, vertices[(i + 1) % 6].y);
  }
}
```

### 青海波（せいがいは）

```javascript
function drawSeigaiha(ctx, startX, startY, radius, rows, cols) {
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const offsetX = (row % 2 === 0) ? 0 : radius;
      const x = startX + col * radius * 2 + offsetX;
      const y = startY + row * radius * 0.7;
      /* 同心円の波紋を3〜4層描画 */
      for (let i = 4; i > 0; i--) {
        ctx.beginPath();
        ctx.arc(x, y, radius * (i / 4), Math.PI, 0, false);
        ctx.strokeStyle = `rgba(0, 80, 150, ${0.2 + i * 0.15})`;
        ctx.stroke();
      }
    }
  }
}
```

### その他の和柄

| 紋様名 | 説明 | 基本図形 |
|--------|------|----------|
| **七宝（しっぽう）** | 円を1/4ずつ重ねた連続模様 | 円の交差 |
| **亀甲（きっこう）** | 正六角形の連続配置 | 正六角形 |
| **鱗（うろこ）** | 正三角形の交互配置 | 正三角形 |
| **矢絣（やがすり）** | 矢羽根を交互に並べた模様 | 平行四辺形 + 三角形 |
| **紗綾形（さやがた）** | 卍を斜めに崩した連続模様 | 折れ線の反復 |

各パターンは `drawPattern(ctx, type, x, y, size, options)` のような統一インターフェースで呼び出す設計を推奨します。

## 書道シミュレーション

### 筆のダイナミクス

```javascript
class BrushSimulator {
  constructor(options = {}) {
    this.pressure = options.pressure || 0.5;    /* 筆圧 (0-1) */
    this.speed = options.speed || 1.0;          /* 速度 */
    this.angle = options.angle || Math.PI / 4;  /* 筆の傾き */
    this.inkAmount = options.inkAmount || 1.0;  /* 墨量 (0-1) */
    this.bristleCount = options.bristleCount || 8;
  }

  /* 筆圧による線幅の変化 */
  getWidth() {
    return this.pressure * 20 + 2;
  }

  /* 墨量の減少（かすれの再現） */
  consumeInk(distance) {
    this.inkAmount = Math.max(0, this.inkAmount - distance * 0.001);
    return this.inkAmount;
  }
}
```

### 墨の流れシミュレーション

```javascript
function simulateInkFlow(ctx, x, y, amount) {
  /* 紙のにじみ: 放射状に不均一に広がる */
  const particles = 50;
  for (let i = 0; i < particles; i++) {
    const angle = Math.random() * Math.PI * 2;
    const dist = Math.random() * amount * 10;
    const px = x + Math.cos(angle) * dist;
    const py = y + Math.sin(angle) * dist;
    const alpha = Math.max(0.02, amount * 0.3 - dist * 0.01);
    ctx.fillStyle = `rgba(10, 10, 10, ${alpha})`;
    ctx.fillRect(px, py, 1, 1);
  }
}
```

### 紙のにじみ効果

- 紙の繊維方向に沿った異方性拡散をシミュレート
- 湿度パラメータでにじみの度合いを制御
- 和紙・半紙・画仙紙など紙の種類でにじみ特性を変化

## 枯山水（かれさんすい）ジェネレーター

### 砂紋（さもん）パターン

```javascript
function drawSandRipples(ctx, stones, width, height, lineSpacing = 8) {
  for (let y = 0; y < height; y += lineSpacing) {
    ctx.beginPath();
    for (let x = 0; x < width; x++) {
      let offsetY = 0;
      /* 各石からの影響を計算（距離に反比例する力場） */
      stones.forEach(stone => {
        const dx = x - stone.x;
        const dy = y - stone.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < stone.radius * 4) {
          /* 石の周囲で砂紋が同心円状に湾曲 */
          offsetY += (stone.radius * 2) / Math.max(dist, 1) *
                     Math.sin(dist / stone.radius * Math.PI);
        }
      });
      if (x === 0) ctx.moveTo(x, y + offsetY);
      else ctx.lineTo(x, y + offsetY);
    }
    ctx.strokeStyle = 'rgba(160, 150, 130, 0.5)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }
}
```

### 石の配置アルゴリズム

```javascript
function placeStones(count, width, height) {
  /* 奇数配置の原則（1, 3, 5, 7）*/
  /* 三角形構図を基本とし、不等辺三角形で自然さを出す */
  const stones = [];
  const goldenAngle = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < count; i++) {
    const r = Math.sqrt(i / count) * Math.min(width, height) * 0.35;
    const theta = i * goldenAngle;
    stones.push({
      x: width / 2 + r * Math.cos(theta),
      y: height / 2 + r * Math.sin(theta),
      radius: 15 + Math.random() * 25,
      type: ['tall', 'flat', 'round'][i % 3]
    });
  }
  return stones;
}
```

### 苔のパッチ

- パーリンノイズで不規則な領域を生成
- 石の根元付近に高い確率で配置
- 色相を微妙に変化させて自然な苔の色合いを表現

## 日本美術の数理パターン

### 組子（くみこ）幾何学的分割

```javascript
function kumikoSubdivision(ctx, polygon, depth, pattern) {
  if (depth === 0) { drawFill(ctx, polygon); return; }
  const subPolygons = subdivide(polygon, pattern);
  /* pattern: 'asanoha', 'goma', 'sakura', 'izutsu' */
  subPolygons.forEach(sub =>
    kumikoSubdivision(ctx, sub, depth - 1, pattern));
}
```

### 折り紙の展開図（クリースパターン）

- 山折り・谷折りの線を色分けして描画
- 川崎の定理（頂点周りの角度条件）に基づく折り線の検証
- 折り畳み状態のアニメーション

### 浮世絵スタイルの波（神奈川沖浪裏風）

```javascript
function drawUkiyoeWave(ctx, baseX, baseY, amplitude, wavelength) {
  ctx.beginPath();
  for (let x = 0; x < wavelength; x++) {
    const t = x / wavelength;
    /* 急峻な波頭と緩やかな谷の非対称波形 */
    const y = baseY - amplitude * (
      Math.pow(Math.sin(t * Math.PI), 0.6) *
      (1 + 0.3 * Math.sin(t * Math.PI * 6)) /* 波頭の飛沫 */
    );
    if (x === 0) ctx.moveTo(baseX + x, y);
    else ctx.lineTo(baseX + x, y);
  }
  ctx.strokeStyle = '#1B3F8B';
  ctx.lineWidth = 2;
  ctx.stroke();
  /* 波頭の白い飛沫をパーティクルで追加 */
}
```

## コード出力フォーマット

| フォーマット | 用途 | 特徴 |
|-------------|------|------|
| **p5.js** | インタラクティブ作品、プロトタイピング | `setup()` / `draw()` 構造、簡潔な記述 |
| **Canvas API** | Webアプリ組み込み、パフォーマンス重視 | ネイティブAPI、細かい制御が可能 |
| **SVG** | 印刷物、スケーラブル出力 | ベクター形式、CSS アニメーション対応 |

## 生成時の確認事項

1. **紋様の種類**: 和柄名またはカテゴリ（幾何学系 / 自然系 / 書道系）
2. **出力形式**: p5.js / Canvas API / SVG
3. **インタラクティブ性**: 静的生成かリアルタイム操作か
4. **カラーパレット**: 伝統色指定 / モノクロ / カスタム
5. **パラメータ**: タイル数、再帰深度、アニメーション速度など
