---
name: building
description: |
  minecraft_build_structureツールでシェルター・壁・プラットフォーム・塔を自動建築。place_blockを何十回も呼ぶ必要なし。
  ALWAYS use when: 拠点を作りたい、シェルターが必要、壁を建てたい、塔を作りたい、モブから身を守る建物が欲しい時。
  個別にplace_blockを繰り返す代わりに、このスキルで構造物を一括建築。
---

# 自動建築スキル

定型的な建築物を自動で構築する高レベルスキル。

## 使用方法

```
minecraft_build_structure {
  username: "BotName",
  type: "shelter",  // or "wall", "platform", "tower"
  size: "medium",   // or "small", "large"
  materials: "cobblestone"  // 省略時は自動選択
}
```

## 建築タイプ

### 1. shelter（シェルター）
- 4面の壁 + 床 + 屋根
- ドア用の開口部あり
- サイズ別寸法:
  - small: 3×3×3
  - medium: 5×5×4
  - large: 7×7×5

### 2. wall（壁）
- 直線の壁を建築
- 防御や区画分けに使用

### 3. platform（プラットフォーム）
- 平らな床面
- 高所作業台や着陸場所に

### 4. tower（塔）
- 垂直に伸びる塔
- 見張り台や高所移動に

## 自動実行される処理

1. **地面整地** - 凹凸を自動で平坦化
2. **材料確認** - インベントリから適切な建材を選択
3. **ブロック配置** - 設計図に従って自動配置
4. **エラー処理** - 配置失敗箇所を記録

## 建材の自動選択

優先順位（インベントリ20個以上あるもの）:
1. cobblestone
2. planks (oak_planks等)
3. stone
4. dirt
5. wood

## Tips

- **材料準備**: 建築前に十分な建材を用意（目安: small=50個, medium=150個, large=300個）
- **地形整地**: 自動で地面を平らにしてから建築開始
- **夜間避難**: shelterは夜間の避難所として即座に使用可能
- **カスタマイズ**: 完成後に手動で窓やドアを追加可能

## サイズ別目安

| サイズ | ブロック数 | 建築時間 | 用途 |
|-------|-----------|---------|------|
| small | ~50 | 30秒 | 緊急避難所 |
| medium | ~150 | 1分 | 基本拠点 |
| large | ~300 | 2分 | メイン拠点 |

## エラー対応

- `No suitable building materials`: 建材不足 → resource-gatheringで収集
- `Placement failed`: 配置できない位置 → 別の場所に移動
