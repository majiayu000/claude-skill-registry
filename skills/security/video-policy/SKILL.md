# Skill: Governance Policy Checks

## Status
enabled

## Purpose
Secrets 漏れと `.env` の追跡を防止します。

## Entry point
```bash
make phase4-policy
```

## Checks
1. `.env` が git で追跡されていないか
2. `.gitignore` に `.env` パターンがあるか
3. 既知の secrets パターン（API keys等）の検出

## Notes
- ripgrep がインストールされている場合、詳細スキャンを実行
- 検出された場合は即座にローテーション推奨
