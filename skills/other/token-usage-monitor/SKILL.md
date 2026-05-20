---
name: token-usage-monitor
description: Build and share a visual dashboard for OpenClaw token usage, model cost comparison, and recent model change timeline. Use when user asks token usage check, model cost tracking, or usage comparison.
metadata: {"openclaw":{"emoji":"📊","os":["darwin","linux"],"requires":{"bins":["bash","python3"]}}}
---

# Token Usage Monitor

Use this skill when the user asks things like:
- "token usage check"
- "model usage compare"
- "cost by model"
- "토큰 사용량 확인"
- "모델 변경 이력"

## Command

Run:

```bash
bash "$HOME/openclaw_pro/workspace/scripts/publish_token_dashboard.sh" --profile jarvis --hours 720 --model-changes 20
```

## Response format

After running the command:
1. Return the `DASHBOARD_URL` first.
2. Return `SUMMARY` in one short line.
3. Return up to 8 items from `MODEL_CHANGES_START ... MODEL_CHANGES_END`.
4. If no model changes exist, say that clearly.

## Rules

- Do not expose secrets.
- If generation fails, report one concrete reason and one retry command.
- Keep response concise and actionable.
