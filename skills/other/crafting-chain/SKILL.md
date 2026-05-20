---
name: crafting-chain
description: |
  minecraft_craft_chainツールで素材収集→中間素材→最終製品まで自動クラフト。autoGather=trueで不足素材も自動収集。
  ALWAYS use when: ピッケルを作りたい、斧が必要、かまどを作る、松明が欲しい、道具をクラフトしたい時。
  minecraft_craftを何度も呼ぶ代わりに、このスキルでwooden_pickaxe/stone_pickaxe/iron_pickaxe/furnace/torch等を一発作成。
---

# クラフトチェーンスキル

複雑なレシピを自動で実行する高レベルスキル。

## 使用方法

```
minecraft_craft_chain {
  username: "BotName",
  target: "wooden_pickaxe",
  autoGather: true  // 不足素材を自動収集
}
```

## 対応レシピ

### 基本ツール
- `wooden_pickaxe`: oak_log → oak_planks → stick → 木のピッケル
- `stone_pickaxe`: stick + cobblestone → 石のピッケル
- `iron_pickaxe`: stick + iron_ore → iron_ingot → 鉄のピッケル

### インフラ
- `crafting_table`: oak_log → oak_planks → クラフト台
- `furnace`: cobblestone × 8 → かまど
- `torch`: coal + stick → 松明 × 4

## 自動実行される処理

1. **レシピ解析** - ターゲットに必要な全ステップを計算
2. **材料確認** - インベントリの現在の所持数をチェック
3. **不足分収集** - autoGather=trueなら自動で素材採集
4. **順次クラフト** - 依存関係に従って順番にクラフト
5. **精錬処理** - 必要なら自動でかまどを使用

## autoGather パラメータ

- `true`: 不足素材を自動で収集（推奨）
- `false`: 手持ちの素材のみでクラフト

## クラフトチェーン例

### wooden_pickaxe (autoGather=true)
```
1. oak_log が 1個必要 → 自動で木を伐採
2. oak_planks をクラフト (oak_log × 1 → oak_planks × 4)
3. stick をクラフト (oak_planks × 1 → stick × 4)
4. wooden_pickaxe をクラフト (oak_planks × 3 + stick × 2)
```

### iron_pickaxe (autoGather=true)
```
1. iron_ore が 3個必要 → 自動で鉱石採掘
2. かまどで精錬 (iron_ore × 3 → iron_ingot × 3)
3. stick が 2個必要 → 木材からクラフト
4. iron_pickaxe をクラフト
```

## Tips

- **autoGather推奨**: 素材不足を気にせず実行可能
- **事前確認**: インベントリに素材があれば即座にクラフト
- **チェーン中断**: 素材が見つからない場合は中断して報告
- **進捗確認**: 各ステップの成否を返り値で確認可能

## 対応予定の追加レシピ

独自のクラフトチェーンを定義したい場合は、`src/tools/high-level-actions.ts` の `craftingChains` オブジェクトに追加可能。

## エラー対応

- `No crafting chain defined`: 未対応レシピ → 低レベルツールで手動クラフト
- `Failed to gather XXX`: 素材が見つからない → 範囲拡大または手動収集
- `Crafting chain aborted`: 途中で失敗 → 進捗を確認して残りを手動実行
