# Skill: CI Scheduling (GitHub Actions)

## Status
enabled

## Purpose
Phase2/Phase3 を定期実行およびオンデマンドで実行します。

## Files
- `.github/workflows/phase2-scheduled.yml`
- `.github/workflows/phase3-scheduled.yml`

## Schedule
- Phase2: 毎日 01:00 UTC
- Phase3: 毎日 01:30 UTC

## Notes
- GitHub Secrets の設定で配信/LLM を有効化
- Secrets 未設定時は安全にスキップ
