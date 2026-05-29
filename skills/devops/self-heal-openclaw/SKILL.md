---
name: self-heal-openclaw
description: Auto-recover OpenClaw when health goes offline, gateway token mismatch (1008) appears, Telegram stops replying, or browser/control-ui disconnects. Runs safe first-pass repair and optional deep cleanup.
---

# Self-Heal OpenClaw

Use this skill when OpenClaw is unstable, for example:
- `health offline` or `Gateway not reachable`
- `token_mismatch` / `1008 unauthorized`
- Telegram channel is connected but no replies are sent
- Browser/Copilot shows disconnected while gateway should be local

## Default action (safe repair)
Run:

```bash
bash scripts/self_heal_openclaw.sh --profile jarvis
```

This performs non-destructive recovery:
1. Does **not** touch token/config by default (stability-first mode)
2. Ensures LaunchAgent is installed
3. Restarts only if health fails twice in a row (with 30-minute cooldown)
4. Runs health and channel probe checks

If token mismatch is explicitly confirmed (`1008 unauthorized`), run:

```bash
bash scripts/self_heal_openclaw.sh --profile jarvis --sync-token
```

This additionally syncs:
- `gateway.remote.token` <- `gateway.auth.token`
- `$HOME/openclaw_pro/gateway.token`

## Deep cleanup (only when safe repair fails)
Run:

```bash
bash scripts/self_heal_openclaw.sh --profile jarvis --deep-clean
```

`--deep-clean` additionally removes stuck local session cache under:
- `~/.openclaw-jarvis/agents/main/sessions/*.jsonl`
- `~/.openclaw-jarvis/agents/main/sessions/sessions.json`

## After repair checklist
- Confirm `openclaw --profile jarvis health` is OK
- Confirm `openclaw --profile jarvis channels status --probe` is OK
- If web still fails, re-enter token in Control UI from `$HOME/openclaw_pro/gateway.token`
