# Skill: Input Validation

## Status
enabled

## Purpose
入力パラメータ（phase, mode, reason）を検証します。

## Entry point
```bash
make phase6-validate PHASE=<phase> MODE=<mode> REASON='<reason>'
# または
bash scripts/phase6-validate.sh <phase> <mode> <reason>
```

## Valid Values

### phase
- `phase2`
- `phase3`
- `phase4`

### mode
- `dry-run`
- `execute`

### reason
- 3文字以上の任意文字列

## Exit Codes
- `0`: 全パラメータ有効
- `1`: 1つ以上のパラメータが無効

## Notes
- ローカル / CI 共通仕様
- 不正値は即座に拒否
