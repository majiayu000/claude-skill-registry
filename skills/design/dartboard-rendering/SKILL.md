---
name: dartboard-rendering
description: ダーツボード描画の実装知識とベストプラクティス。p5.jsを使用した描画順序、レイヤリング、座標系の扱いに関する専門知識を提供します。実装・テスト・レビュー時に参照してください。
allowed-tools: Read
---

# Dartboard Rendering Knowledge

ダーツボード描画に関する実装パターンとベストプラクティスを定義します。

## 描画順序の原則

### 基本原則: 外側から内側へ、下レイヤーから上レイヤーへ

ダーツボードは以下の順序で描画することで、正しいレイヤリングを実現します:

```
1. 背景クリア
2. ダブルリング（170mm円全体、赤/緑交互）
3. アウターシングル（162mm円全体、黒/ベージュ交互）
4. トリプルリング（107mm円全体、赤/緑交互）
5. インナーシングル（99mm円全体、黒/ベージュ交互）
6. ★ 外側スパイダー（放射線 + リング境界の同心円）
7. アウターブル（緑色、半径7.95mm）
8. インナーブル（赤色、半径3.175mm）
9. ★ ブル用スパイダー（ブル境界の同心円）
10. セグメント番号
```

### スパイダー（ワイヤー境界線）の2ステップ描画

**重要**: スパイダーは必ず2ステップに分けて描画する

#### 問題: 一度に描画すると色が被る

```typescript
// ❌ 悪い例: 全てのスパイダーを一度に描画
drawAllRings();
drawAllSpiders();  // 放射線がブルの色に被る！
drawBull();
```

#### 解決策: スパイダーを分割描画

```typescript
// ✅ 良い例: スパイダーを2ステップに分ける
drawAllRings();
drawSpiderOuter();  // 1. 放射線 + リング境界の同心円
drawBull();         // ブルエリアの色を塗る
drawSpiderBull();   // 2. ブル境界の同心円
```

**理由**:
- 放射線がブルエリアの色を塗る**前**に描画されないと、放射線が色に被って見えなくなる
- ブル境界の円はブルエリアの色を塗った**後**に描画しないと、境界線が見えない

## セグメント境界の角度計算

### 問題: セグメントの真ん中に配置されてしまう

```typescript
// ❌ 悪い例: セグメントの真ん中に配置される
const angle = -Math.PI / 2 + i * SEGMENT_ANGLE;
```

### 解決策: 0.5個分ずらす

```typescript
// ✅ 良い例: セグメント境界に配置される
const angle = -Math.PI / 2 + (i - 0.5) * SEGMENT_ANGLE;
```

**理由**:
- `drawRingSegments()` 関数が `(index - 0.5) * SEGMENT_ANGLE` を使用してセグメントを描画している
- スパイダーの放射線も同じ計算式を使うことで、セグメント境界に正確に配置される

## 座標系の分離原則

### 物理座標（mm）vs 画面座標（pixel）

**鉄則**: ビジネスロジックは必ず物理座標で処理し、描画時のみ画面座標に変換する。

```typescript
// ✅ 良い例
const physicalRadius = BOARD_PHYSICAL.rings.doubleOuter; // 170mm
const screenRadius = transform.physicalDistanceToScreen(physicalRadius);
p5.circle(center.x, center.y, screenRadius * 2);

// ❌ 悪い例
const radius = 170; // 物理座標？画面座標？不明確
p5.circle(center.x, center.y, radius * 2);
```

### CoordinateTransform クラスの使用

```typescript
// 座標変換の例
const center = transform.getCenter();              // ボード中心の画面座標
const radius = transform.physicalDistanceToScreen(170);  // 物理→画面
const width = transform.physicalDistanceToScreen(1.5);   // 線幅も変換
```

## p5.js 描画最適化

### 描画状態の設定はループ外で

```typescript
// ✅ 良い例: 共通設定はループ外で一度だけ
p5.noStroke();  // ループ外で設定
SEGMENTS.forEach(() => {
  p5.fill(color);
  p5.arc(...);
});

// ❌ 悪い例: 毎回設定する
SEGMENTS.forEach(() => {
  p5.noStroke();  // 20回呼ばれる（無駄）
  p5.fill(color);
  p5.arc(...);
});
```

## 実装パターン

### drawSpiderOuter() - 外側スパイダー

```typescript
export function drawSpiderOuter(p5: p5Types, transform: CoordinateTransform): void {
  // 1. 放射線（セグメント境界）: 20本
  //    - ボード中心からboardEdge（225mm）まで
  //    - (i - 0.5) * SEGMENT_ANGLE でセグメント境界に配置

  // 2. リング境界の同心円: 4本
  //    - ダブル外側（170mm）
  //    - ダブル内側（162mm）
  //    - トリプル外側（107mm）
  //    - トリプル内側（99mm）
}
```

### drawSpiderBull() - ブル用スパイダー

```typescript
export function drawSpiderBull(p5: p5Types, transform: CoordinateTransform): void {
  // ブル境界の同心円: 2本
  //    - アウターブル（7.95mm）
  //    - インナーブル（3.175mm）
}
```

## テスト時の考慮事項

### 描画順序の検証

```typescript
// 放射線→同心円の順序を検証
const allCalls = [...lineSpy.mock.invocationCallOrder, ...circleSpy.mock.invocationCallOrder];
const lineCalls = lineSpy.mock.invocationCallOrder;
const circleCalls = circleSpy.mock.invocationCallOrder;

// 最後の放射線 < 最初の同心円
expect(Math.max(...lineCalls)).toBeLessThan(Math.min(...circleCalls));
```

### 後方互換性の保持

```typescript
/**
 * @deprecated drawSpiderOuter と drawSpiderBull を個別に呼び出すことを推奨
 */
export function drawSpider(p5: p5Types, transform: CoordinateTransform): void {
  drawSpiderOuter(p5, transform);
  drawSpiderBull(p5, transform);
}
```

## よくある間違いと対策

### 1. 描画順序の間違い

**間違い**: スパイダーを一度に全て描画
**対策**: スパイダーを2ステップに分ける（外側→ブル塗り→ブル用）

### 2. 座標系の混在

**間違い**: 物理座標と画面座標が混在
**対策**: 常に物理座標で計算し、描画直前に変換

### 3. セグメント境界のずれ

**間違い**: `i * SEGMENT_ANGLE` でセグメント中央に配置
**対策**: `(i - 0.5) * SEGMENT_ANGLE` で境界に配置

### 4. 描画最適化の不足

**間違い**: ループ内で毎回描画状態を設定
**対策**: 共通設定はループ外で一度だけ

## 使用方法

このskillは以下のコンテキストで参照してください：

1. **テスト作成時**: test-writerサブエージェントで描画順序やスパイダー分割を考慮
2. **実装時**: implementサブエージェントで正しい描画パターンを適用
3. **レビュー時**: review-fileサブエージェントで描画順序の正しさを検証

**このドメイン知識を常に参照し、ダーツボード描画に関わる実装やテストを作成してください。**
