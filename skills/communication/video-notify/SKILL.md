# Skill: Notification

## Status
enabled

## Purpose
異常検知結果に基づいて通知を行います。

## Entry point
```bash
make phase5-notify
# または
bash scripts/phase5-notify.sh <anomaly_detected: 0|1>
```

## Behavior

### GitHub Actions 環境
- 異常時: GitHub Issue を作成
- 正常時: Actions Summary にメトリクス集計を表示

### ローカル環境
- 標準出力にサマリーを表示

## Notes
- Issue 作成には gh CLI が必要
- 既存の同名 Issue がある場合はコメント追加
