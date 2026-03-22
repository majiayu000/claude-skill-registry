---
name: ghapp
description: Give your AI agents and automations their own GitHub (App) identity. Authenticate using GitHub Apps so every commit, PR, and action is attributed to the bot — not your personal account.
homepage: https://github.com/operator-kit/ghapp-cli
metadata: {"clawdbot":{"emoji":"🔑","requires":{"bins":["ghapp"]},"install":[{"id":"brew","kind":"brew","formula":"operator-kit/tap/ghapp","bins":["ghapp"],"label":"Install ghapp (brew)"},{"id":"bash","kind":"bash","command":"curl -sSL https://raw.githubusercontent.com/operator-kit/ghapp-cli/main/install.sh | bash","bins":["ghapp"],"label":"Install ghapp (bash)"}]}}
---

# ghapp

Use `ghapp` to authenticate as a GitHub App and use `git`/`gh` with installation tokens. Requires a GitHub App with App ID, Installation ID, and a private key (.pem).

Setup (once) — interactive
- `ghapp setup` — prompts for App ID, Installation ID, key path; optionally configures git+gh auth

Setup (once) — non-interactive (scripted/LLM)
- `ghapp config set --app-id 123 --installation-id 456 --private-key-path /path/to/key.pem`
- Or with keyring: `ghapp config set --app-id 123 --installation-id 456 --import-key /path/to/key.pem`
- Then: `ghapp auth configure --gh-auth shell-function`

Post-setup
- `ghapp auth configure` — configure git credential helper, gh CLI auth, and git identity (if skipped during setup)
- `ghapp auth status` — show current auth config and diagnostics

Common commands
- Get token: `ghapp token` (cached; `--no-cache` for fresh)
- Configure auth: `ghapp auth configure [--gh-auth shell-function|path-shim|none]`
- Check status: `ghapp auth status`
- Reset auth: `ghapp auth reset [--remove-key]`
- Config: `ghapp config set`, `ghapp config get [key]`, `ghapp config path`
- Self-update: `ghapp update`
- Version: `ghapp version`

gh auth modes
- `--gh-auth shell-function` — wraps `gh` via shell function injecting fresh token per call (recommended)
- `--gh-auth path-shim` — installs wrapper binary as `gh` earlier in PATH (CI/containers)
- `--gh-auth none` — only writes `hosts.yml` (token expires ~1hr)

Notes
- After setup+auth configure, `git clone/push/pull` and `gh` commands work transparently — no manual tokens.
- SSH-style URLs (`git@github.com:...`) are auto-rewritten to HTTPS.
- Commits are attributed to the app's bot account (e.g., `myapp[bot]`).
- Tokens are cached locally; `ghapp token` returns in <10ms on cache hit.
- Config lives at `~/.config/ghapp/config.yaml`.
- Env overrides: `GHAPP_APP_ID`, `GHAPP_INSTALLATION_ID`, `GHAPP_PRIVATE_KEY_PATH`, `GHAPP_NO_UPDATE_CHECK=1`.
- Private key can be stored on disk (default) or imported into OS keyring with `--import-key`.
