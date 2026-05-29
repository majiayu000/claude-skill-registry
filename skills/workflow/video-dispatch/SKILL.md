# Skill: Execution Dispatch

## Status
enabled

## Purpose
validate → guard → phase 実行の順で処理を行います。

## Entry point
```bash
make phase6-run PHASE=<phase> MODE=<mode> REASON='<reason>'
# または
bash scripts/phase6-dispatch.sh <phase> <mode> <reason>
```

## Execution Flow

1. **Validate**: 入力パラメータを検証
2. **Guard**: 実行条件をチェック
3. **Execute**: 対象Phaseを実行
4. **Record**: 履歴とメトリクスに記録

## Phase Mapping

| Phase | Command |
|-------|---------|
| phase2 | (placeholder) |
| phase3 | make phase3-all |
| phase4 | make phase4-ci-local |

## Exit Codes
- `0`: 正常終了
- `1`: バリデーション/ガード/実行のいずれかで失敗

## Notes
- 既存 Make / Script を再利用
- execute モードのみ Phase5 metrics に記録
- 履歴は常に data/phase6/execution-history.log に記録
