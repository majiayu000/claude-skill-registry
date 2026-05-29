# Skill: Metrics Collection

## Status
enabled

## Purpose
実行結果を JSONL 形式で継続的に記録します。

## Entry point
```bash
make phase5-metrics
# または
bash scripts/phase5-metrics.sh <phase> <status> <duration> [eval_score]
```

## Output
- `data/phase5/metrics/metrics.jsonl`

## Notes
- jq 不要（Pure bash で JSON 生成）
- GitHub Actions 実行時は workflow_run_id も記録
