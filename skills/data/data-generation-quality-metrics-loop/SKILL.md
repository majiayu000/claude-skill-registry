---
name: data-generation-quality-metrics-loop
description: "Use when validating auto-generated data quality through iterative generate-measure-fix loops with quantitative metrics."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---
# Data Generation Quality Metrics Loop

**Extracted:** 2026-02-11
**Context:** 大量のデータを自動生成するスクリプトの品質を、定量メトリクスで反復改善するパターン。

## Problem

データ生成スクリプトの出力品質を、少数のスポットチェックだけで判断すると問題を見逃す。
例: 411問の構造化データ生成で、スポットチェック5問はOKだが全体の23%にイントロ文が混入していた。

## Solution

### 1. 定量メトリクスを定義する

生成物の品質を数値で測定できるチェック項目を設計:

```python
# 例: 構造化解説データの品質メトリクス
metrics = {
    "intro_contamination": "イントロ文('問う問題')がpointに含まれる件数",
    "long_points": "150文字以上のpoint数",
    "empty_points": "5文字以下のpoint数",
    "empty_key_fields": "必須フィールドが空の件数",
}
```

### 2. 生成→測定→修正のループを回す

```
生成 v1 → メトリクス測定 → 問題特定 → 原因分析 → 修正 → 生成 v2 → ...
```

具体例（本セッション）:
- v1: イントロ混入 373/1641 (23%) → イントロ除去ロジック追加
- v2: イントロ混入 88/1641 (5%) → 正規表現パターン拡張
- v3: イントロ混入 2/1641 (0.1%) → OCR分断対応
- v4: イントロ混入 1/1641 (0.06%) → 許容範囲（ソースデータ起因）

### 3. メトリクス測定スクリプトは独立させる

生成スクリプトとは別に、品質チェック用の計測コードを用意:

```python
# 生成後に毎回実行
python3 -c "
import json
with open('data.json') as f: data = json.load(f)
# ... メトリクス計算 ...
print(f'Issue A: {count_a}/{total} ({pct_a}%)')
print(f'Issue B: {count_b}/{total} ({pct_b}%)')
"
```

### 4. 止め時の判断基準を持つ

- 0%は目指さない（ソースデータ起因の問題は修正不可能）
- 1%以下になったら残件の個別調査に切り替える
- 手動修正が必要なケースはデータ品質イシューとして記録

## When to Use

- JSONデータの一括変換・拡充
- テストデータの自動生成
- マイグレーションスクリプトの出力検証
- 任意の「入力→変換→出力」パイプラインの品質保証
