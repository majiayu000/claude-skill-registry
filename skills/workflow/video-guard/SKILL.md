# Skill: Execution Guard

## Status
enabled

## Purpose
実行条件をチェックし、安全でない場合はブロックします。

## Entry point
```bash
make phase6-guard PHASE=<phase> MODE=<mode> REASON='<reason>'
# または
bash scripts/phase6-guard.sh <phase> <mode> <reason>
```

## Checks

### 1. Reason Check (execute mode only)
- reason が空でないこと
- 3文字以上であること

### 2. Cooldown Check (execute mode only)
- 同一Phaseの直近実行から30分経過していること
- 環境変数 `PHASE6_COOLDOWN_MINUTES` で変更可能

### 3. Anomaly Check
- Phase5メトリクスの直近失敗率が20%以下であること
- execute: ブロック / dry-run: 警告のみ

## Exit Codes
- `0`: 全チェック通過
- `1`: ブロック（実行不可）

## Notes
- 判定根拠は標準出力に表示
- dry-run モードではチェックが緩和される
