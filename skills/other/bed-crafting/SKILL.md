---
name: bed-crafting
description: |
  ベッドの作成手順。羊を探して羊毛を集め、板材と組み合わせてベッドをクラフト。
  Use when: ベッドを作りたい、夜をスキップしたい、スポーン地点を設定したい、羊毛が必要な時。
---

# ベッド作成スキル

ベッドは夜をスキップし、リスポーン地点を設定する最重要アイテム。

## 必要素材

| アイテム | 数量 | 入手方法 |
|---------|------|---------|
| 羊毛 (wool) | 3個 | 羊を倒す or ハサミで刈る |
| 板材 (planks) | 3個 | 原木をクラフト |

## 手順

### 1. 羊を探す

```
minecraft_find_entities { entity_type: "sheep" }
```

**羊がいない場合:**
```
minecraft_explore_for_biome { target_biome: "plains", max_distance: 200 }
```

羊が多いバイオーム:
- plains, sunflower_plains, meadow
- forest, birch_forest
- snowy_plains

### 2. 羊を狩る

```
minecraft_fight { entity_name: "sheep" }
```

- 羊1匹 = 羊毛1個 + 羊肉1個
- **3匹必要**（同じ色推奨だが混色でもOK）

### 3. 木を集める

```
minecraft_find_block { block_name: "oak_log" }
minecraft_dig_block { x, y, z }
```

原木1個 → 板材4個なので、原木1個でOK

### 4. クラフト

```
# 板材を作る（作業台不要）
minecraft_craft { item_name: "oak_planks", count: 1 }

# ベッドを作る（作業台必要）
minecraft_craft { item_name: "bed", count: 1 }
```

**注意**: ベッドのクラフトには作業台が必要

### 5. ベッドを設置

```
minecraft_place_block { block_type: "bed", x, y, z }
```

- 平らな場所に2ブロック分のスペースが必要
- 屋根があると安全

### 6. 寝る

```
minecraft_sleep {}
```

- 夜（13000-23000 tick）のみ可能
- 近くにモンスターがいると寝れない

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 羊が見つからない | plainsバイオームへ移動 |
| 羊毛の色が違う | 混色でもベッドは作れる |
| 作業台がない | 板材4個でcraft |
| 寝れない | モンスターを倒すか離れる |
| 設置できない | 2ブロックの平らな場所を確保 |

## ベッドの重要性

1. **夜スキップ**: モンスタースポーンを回避
2. **リスポーン設定**: 死んでも近くで復活
3. **時間効率**: 探索・作業時間を最大化
