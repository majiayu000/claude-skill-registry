# Skill: Regression Evaluation (Lightweight)

## Status
enabled

## Purpose
評価データセットのカバレッジと最低限のゲートを確認し、明らかな回帰を検出します。

## Entry point
```bash
make phase4-eval
```

## Gates
1. 評価データが10件以上
2. 3ストリーム（voc, market_competitor, techsec）を含む

## Data
- Location: `data/phase4/eval/sample_eval.jsonl`
- Format: JSONL (1行1レコード)

## Notes
- プロダクトに合わせて評価データを拡張してください
- 新しいストリームを追加する場合はゲートも更新
