---
name: resource-gathering
description: |
  minecraft_gather_resourcesツールで木材・石・鉱石を自動で探索・採掘・回収。find_block→move_to→dig_blockを手動で繰り返す必要なし。
  ALWAYS use when: 木を集めたい、丸石が必要、鉱石を掘りたい、素材が足りない、oak_log/cobblestone/iron_ore等のブロックを収集する時。
  個別にfind_block→move_to→dig_blockと呼ぶ代わりに、このスキルを使うこと。
---

# リソース自動収集スキル

指定したアイテムを自動で収集する完全自動化スキル。

## 使用可能なツール

Game Agentは以下の基本ツールを組み合わせてリソース収集を実行します：

- `minecraft_find_block(block_name, max_distance)` - ブロックを検索
- `minecraft_move_to(x, y, z)` - ブロックの位置へ移動
- `minecraft_dig_block(x, y, z, auto_collect)` - ブロックを採掘
- `minecraft_collect_items()` - ドロップアイテムを収集
- `minecraft_get_inventory()` - インベントリ確認
- `minecraft_equip(item_name, destination)` - ツール装備

## 使用手順

### 1. 木材収集の例

```typescript
// 1. 原木を探す
minecraft_find_block({ block_name: "oak_log", max_distance: 32 })
// → 座標を取得: (x, y, z)

// 2. 斧を装備
minecraft_equip({ item_name: "diamond_axe", destination: "hand" })

// 3. 原木まで移動
minecraft_move_to({ x, y, z })

// 4. 採掘
minecraft_dig_block({ x, y, z, auto_collect: true })

// 5. インベントリ確認
minecraft_get_inventory()
// → oak_log の数を確認

// 6. 目標数に達するまで 1-5 を繰り返し
```

### 2. 鉱石収集の例

```typescript
// 1. 石炭鉱石を探す
minecraft_find_block({ block_name: "coal_ore", max_distance: 32 })

// 2. ピッケルを装備
minecraft_equip({ item_name: "diamond_pickaxe", destination: "hand" })

// 3. 移動して採掘
minecraft_move_to({ x, y, z })
minecraft_dig_block({ x, y, z, auto_collect: true })
```

## ワークフロー

1. **ブロック検索**: `minecraft_find_block()` で目標ブロックの座標取得
2. **ツール確認**: インベントリから適切なツールを確認・装備
3. **移動**: `minecraft_move_to()` でブロックへ移動
4. **採掘**: `minecraft_dig_block()` でブロック破壊
5. **収集**: `minecraft_collect_items()` でアイテム拾得（auto_collect: false の場合）
6. **確認**: `minecraft_get_inventory()` で目標数チェック
7. **繰り返し**: 目標数に達するまで 1-6 を繰り返す

## 対応ブロック例

| カテゴリ | ブロック名 |
|---------|-----------|
| 木材 | oak_log, birch_log, spruce_log |
| 石材 | cobblestone, stone, andesite |
| 鉱石 | coal_ore, iron_ore, gold_ore, diamond_ore |
| 食料 | wheat, carrot, potato |

## Tips

- **ツール準備**: 鉱石採掘にはピッケルが必要
- **範囲拡大**: 見つからない場合は maxDistance を増やす
- **複数アイテム**: 1回の呼び出しで複数種類を収集可能
- **効率化**: 近くのブロックから優先的に採掘

## エラー対応

- `No XXX found within Y blocks`: 範囲内にブロックがない
  - → 別の場所へ移動: `minecraft_move_to(new_x, new_y, new_z)`
  - → 検索範囲を拡大: `max_distance` を増やす

- `Failed to dig block`: 適切なツールがない、またはツールが壊れた
  - → ツールをクラフト: `minecraft_craft({ item_name: "wooden_pickaxe" })`
  - → 既存のツールを装備: `minecraft_equip({ item_name: "iron_pickaxe" })`

- `No items collected`: ドロップアイテムを拾えない
  - → サーバー設定問題（コード修正では解決不可能）
  - → 代替策: インベントリから直接確認

## 注意事項

**サーバー設定の制約**:
現在のMinecraftサーバーではアイテムピックアップが無効化されている可能性があります。
`minecraft_dig_block(auto_collect: true)` や `minecraft_collect_items()` が
"No items collected" を返す場合、これはコードの問題ではなく**サーバー設定の問題**です。

回避策:
- インベントリ内のアイテム数で採掘成功を判断
- チェスト経由でアイテム移動
