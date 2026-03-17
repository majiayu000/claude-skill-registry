---
name: fft-debug
description: Diagnose and resolve FFT_nano runtime issues across container execution, provider credentials, Telegram/WhatsApp routing, scheduler behavior, and per-group logs/state.
---

# FFT Debug

Use this skill for incident triage and deterministic debugging of FFT_nano host and container paths.

## Guardrails

- Never use destructive git commands unless explicitly requested.
- Preserve unrelated worktree changes.
- Keep admin/coder controls in main chat only; do not bypass main-chat restrictions.

## Fast Triage

1. Confirm single instance lock:
   - `ls -la data/fft_nano.lock`
2. Check startup/runtime logs:
   - `tail -n 200 logs/fft_nano.log`
   - `tail -n 200 logs/fft_nano.error.log`
3. Check per-group container logs:
   - `ls -la groups/<group>/logs`
   - `tail -n 200 groups/<group>/logs/*`
4. Inspect registration + IPC state:
   - `cat data/registered_groups.json`
   - `find data/ipc -maxdepth 3 -type f`

## Common Failure Modes

- Provider key missing: Pi reports no models available.
- Wrong `PI_API`/`PI_MODEL`: model/provider not found.
- Multiple bot instances: Telegram getUpdates conflict.
- Apple Container networking timeout on macOS.

## Recommended Debug Commands

- Build/runtime checks:
  - `npm run typecheck`
  - `npm test`
- Dry-run routing check (no live model call):
  - `FFT_NANO_DRY_RUN=1 ./scripts/start.sh dev telegram-only`
- Runtime detail logging:
  - `LOG_LEVEL=debug ./scripts/start.sh dev telegram-only`

## Telegram Debug Path

- Verify bot token present at runtime.
- In bot DM: `/id`, `/status`, `/help`.
- Admin checks in main chat only: `/tasks`, `/groups`, `/panel`, `/coder`, `/coder-plan`.
- If `/main <secret>` fails, verify `TELEGRAM_ADMIN_SECRET` and restart.

## Container Runtime Debug

- macOS Apple Container:
  - `container system status`
  - `container system stop && container system start`
- Linux Docker:
  - `docker info`
  - `docker ps`

## Database/State Debug

- SQLite file location: `store/messages.db`
- Router state: `data/router_state.json`
- Group registry: `data/registered_groups.json`
- Per-group Pi state: `data/pi/<group>/.pi/`
