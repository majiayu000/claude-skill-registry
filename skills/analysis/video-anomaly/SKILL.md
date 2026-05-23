# Skill: Anomaly Detection

## Status
enabled

## Purpose
直近 N 件のメトリクスを分析し、異常を検出します。

## Entry point
```bash
make phase5-anomaly
```

## Detection Rules

1. **失敗率 > 20%** → 異常
2. **実行時間が前期間の 2 倍以上** → 異常
3. **評価スコアが前期間より低下** → 異常

## Exit Codes
- `0`: 正常
- `1`: 異常検出

## Notes
- 詳細分析には Python3 が必要
- データ不足時は正常扱い
