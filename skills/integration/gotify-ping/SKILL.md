---
name: gotify-ping
description: Send a Gotify push before requesting human input
---

# Gotify Ping Skill

Use this before asking the human for input so they get a phone notification.

## Prereqs

- Gotify token is provided via sops-nix at `/run/secrets/gotify/token`.
- Optional env overrides:
  - `GOTIFY_URL` (default: https://gotify.ablz.au)
  - `GOTIFY_TOKEN_FILE` (default: /run/secrets/gotify/token)
  - `GOTIFY_PRIORITY` (default: 5)

## Quick Command

```bash
gotify-ping "Codex needs input" "Please check the session; I need a decision."
```

## Notes

- The `gotify-ping` command comes from `scripts/gotify-ping.sh` and is installed into PATH via Home Manager.
- If the token file is missing or unreadable, the command exits with an error.
