---
name: parallel-subagent-batch-merge
description: "Use when generating 50+ structured items with parallel Claude Code subagents and merging outputs into one file."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---
# 並列サブエージェントのバッチ生成とマルチフォーマットマージ

**Extracted:** 2026-02-11
**Context:** Claude Code で大量データを並列サブエージェントで生成し、出力を1つのファイルに統合する場面

## Problem

Claude Code のサブエージェント（Task tool）を大量並列起動すると、以下の問題が発生する:

1. **出力フォーマットの不統一** — 同じプロンプトでも、エージェントごとに出力構造が異なる
   - 辞書型: `{ "id": { ...data } }`
   - リスト+id: `[{ "id": "...", "data": {...} }]`
   - リスト+別名: `[{ "questionId": "...", "data": {...} }]`
2. **構文エラーの混入** — `:=` 、trailing comma 等の JSON 構文エラー
3. **型の揺れ** — `relatedConcepts` が `string` のはずが `array` で返る等
4. **コンテンツ重複** — 同じ説明文が複数選択肢にコピーされる

## Solution

### 1. バッチ分割: ヘルパースクリプトで入力を標準化

```python
# prepare_batches.py: 入力データを N 件ずつのテキストファイルに分割
# → 各サブエージェントが1ファイルだけ読めばよい
batches = [items[i:i+BATCH_SIZE] for i in range(0, len(items), BATCH_SIZE)]
```

- バッチサイズ 20 が実績あり（コンテキスト窓との兼ね合い）
- 最終バッチは端数になるので注意

### 2. 並列起動: 全バッチを `run_in_background=true` で同時起動

```
# 21バッチ × Sonnet subagent を同時起動
for batch in 1..21:
    Task(subagent_type="general-purpose", model="sonnet",
         run_in_background=true, prompt=f"Read batch_{batch}.txt ...")
```

- 出力先を `batch_XX_output.json` で分離（書き込み競合の回避）
- 全エージェント完了後にマージ

### 3. 正規化マージ: 3種フォーマットを統一

```python
def normalize_batch(batch_data):
    """辞書型・リスト型どちらでも { id: data } に正規化"""
    if isinstance(batch_data, dict):
        return batch_data
    elif isinstance(batch_data, list):
        result = {}
        for item in batch_data:
            qid = item.get("id") or item.get("questionId")
            data = item.get("enhancedExplanation", item)
            result[qid] = data
        return result
```

### 4. 型修正: 期待する型に強制変換

```python
# relatedConcepts: String? なのに array で返ってきた場合
if isinstance(val, list):
    val = "".join(val) if val else None
```

### 5. 構文エラー修正: JSON parse 前に既知パターンを置換

```python
raw = raw.replace(':="', ': "')  # := → : のタイポ修正
```

### 6. 品質検証: 重複検出 + 自動修正

```python
# contrastTable の point 重複チェック
points = [e["point"] for e in contrast_table]
if len(set(points)) < len(points):
    # → 手動で固有テキストに差し替え
```

## Key Metrics (実績)

| 項目 | 数値 |
|------|------|
| 対象データ | 408問 |
| バッチ数 | 21（20問×20 + 8問×1） |
| 並列エージェント | 21（全同時起動） |
| フォーマット種類 | 3種（辞書14 / リスト+id 2 / リスト+questionId 5） |
| 構文エラー | 1件（batch_21: `:=`） |
| 型の揺れ | 8件（batch_21: relatedConcepts が配列） |
| コンテンツ重複 | 7問（contrastTable point 重複） |
| 最終結果 | 全408問マージ成功、検証 ALL GREEN |

## When to Use

- Claude Code で **50件以上** のデータを構造化生成するとき
- 各項目が **独立** しており並列処理可能なとき
- 出力が **JSON** で、スキーマが明確なとき
- `claude-code-self-generation-over-api.md` の判断で「Claude Code 直接生成」を選択した後の実行パターン

## Gotcha: キー名不統一の検出と正規化

LLMバッチ生成では、同じフィールドに対してバッチごとに異なるキー名が出力される（例: `choice` / `choiceLabel` / `option`）。

### 検出

```python
key_sets = set()
for item in data['items']:
    for entry in item.get('nested', []):
        key_sets.add(tuple(sorted(entry.keys())))
print(f'Unique key patterns: {len(key_sets)}')
for ks in sorted(key_sets):
    print(f'  {ks}')
```

### 正規化

```python
for entry in item.get('nested', []):
    normalized = {}
    normalized['choice'] = entry.get('choice') or entry.get('choiceLabel') or entry.get('option', '')
    normalized['point'] = entry.get('point') or entry.get('reason', '')
    # ...
```

### 検証

```python
bad = [(item['id'], set(e.keys()))
       for item in data['items']
       for e in item.get('nested', [])
       if set(e.keys()) != EXPECTED_KEYS]
assert not bad, f'Still inconsistent: {bad}'
```

## Anti-patterns

- バッチサイズが大きすぎる（50+）→ エージェントのコンテキスト消費で品質低下
- マージスクリプトが特定フォーマットだけ想定 → 必ず全フォーマットに対応する
- 検証なしでマージ完了とする → `validate` スクリプトを必ず実行
- 重複エラーを無視する → UIで同じテキストが並ぶと著しく品質低下
- キー名不統一を見逃す → Swift Codable等の厳格なデコーダで即座にクラッシュ
