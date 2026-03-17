---
name: survival
description: |
  サバイバル行動を自動実行。minecraft_survival_routineツールで食料確保・シェルター建築・ツール作成を一括処理。
  ALWAYS use when: お腹が空いた、HPが低い、食料がない、ピッケルがない、シェルターがない、夜になった、生存の基本行動が必要な時。
  低レベルツール(move_to, dig_block等)を個別に呼ぶ前に、まずこのスキルを使うこと。
---

# サバイバルルーチンスキル

生存に必要な基本行動を自動で実行する高レベルスキル。

## 初日（Phase 0/1）プロトコル — この順番で1つずつ呼べ

MCPタイムアウト(60秒)のため、1ツール1ステップ。順番を守れ。

| ステップ | ツール | 目的 |
|---------|--------|------|
| 1 | `minecraft_validate_survival_environment` | 環境確認（食料源の有無） |
| 2 | `minecraft_gather_resources` (oak_log x10) | 木材収集 |
| 3 | `minecraft_craft_chain` (wooden_pickaxe) | 木ピッケル作成（作業台も自動） |
| 4 | `minecraft_craft_chain` (wooden_sword) | 剣作成 |
| 5 | `minecraft_survival_routine` (food) | 食料確保（狩猟） |
| 6 | `minecraft_gather_resources` (cobblestone x32) | 石収集 |
| 7 | `minecraft_upgrade_tools` (stone) | 石ツール一式 |
| 8 | `minecraft_establish_base` | 作業台・かまど・チェスト・シェルター設置 |

**各ステップは独立して完結する。失敗したら次に進め（完璧を求めるな）。**

---

## 通常のサバイバルルーチン

```
minecraft_survival_routine {
  username: "BotName",
  priority: "auto"  // or "food", "shelter", "tools"
}
```

### autoモードのしきい値（プロアクティブ）

| 条件 | 選択される優先度 |
|------|----------------|
| 腹具合 < **15**/20 | food（危機になる前に動く） |
| HP < 10 AND 腹具合 < 18 | food（HP低い時は食料最優先） |
| ピッケルなし | tools |
| その他 | shelter |

**food < 10 まで待つな。15 を切ったら即食料確保。**

---

## 優先度モード

### food（食料確保）
1. インベントリに食料があれば即食べる
2. **チェストから食料を取得**（優先）
   - `minecraft_list_chest` で最寄りのチェスト内容を確認
   - 食料アイテムがあれば `minecraft_take_from_chest` で取得
3. チェストに食料がない場合のみ、近くの動物を探索（牛、豚、鶏、羊）
4. 動物を狩猟（生肉でも食べる — 腐った肉も飢餓よりマシ）
5. かまどがあれば肉を調理

### shelter（シェルター建築）
1. ベッドの有無を確認
2. ベッドがなければ材料収集（羊毛 + 板材）
3. 小型シェルターを自動建築

### tools（ツール作成）
1. ピッケルがなければクラフト
2. 斧がなければクラフト
3. シャベルがなければクラフト

---

## HP/食料しきい値の行動ガイド

| HP | 腹具合 | すべきこと |
|----|--------|-----------|
| 20 | < 15 | `survival_routine {priority: "food"}` |
| < 10 | 任意 | 即 `minecraft_eat` → フリーズしたら `survival_routine {priority: "food"}` |
| < 4 | 任意 | 即 `minecraft_flee` → 食べる → シェルターへ |

**HPが低くてもリスポーンするな。食料で回復せよ。**

---

## 食料の選好順（調理前提にするな）

1. 調理済み肉（cooked_beef等）← 最高効率
2. 生肉（beef, porkchop, chicken等）← 十分に有効
3. パン・農作物 ← あれば使う
4. 腐った肉（rotten_flesh）← 飢餓死よりマシ。緊急時OK
5. 釣り（fishing_rod必要）← 代替手段

---

## エラー対応

- `No food sources found`: まずチェストを確認（`minecraft_list_chest`）。なければ64ブロック以内の動物を探す。それも無ければ釣りか腐った肉。
- `No suitable building materials`: resource-gatheringで木材や石を収集
- `Crafting failed`: 素材不足 → 収集してから再実行

---

## サーバー制限への対応

- **動物がスポーンしない**: チェストから食料を取得するのが唯一の方法
- **アイテムドロップ無効**: ブロックを壊しても何も落ちない場合、チェストの既存アイテムのみ使用可能

このような環境では、**チェストアクセスツール**が生存の鍵となります：
1. `minecraft_list_chest` - 最寄りチェストの内容確認
2. `minecraft_take_from_chest` - 食料・道具の取得
3. `minecraft_store_in_chest` - 不要品の保管
