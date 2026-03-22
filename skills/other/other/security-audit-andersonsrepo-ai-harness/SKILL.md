---
name: security-audit
description: Automated security posture check of the AI Harness system. Checks credentials, tokens, file permissions, git hygiene, heartbeat health, and configuration drift.
user-invocable: true
argument-hint: "[full|credentials|git|heartbeat|config]"
context: fork
agent: ops
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
model: sonnet
---

# Security Audit

Automated self-assessment of the AI Harness security posture.

## Live System State
!`ls -la bridges/discord/.env 2>/dev/null || echo "(no .env file)"`
!`ls -la bridges/discord/harness.db 2>/dev/null | awk '{print $1, $5, $9}'`
!`git status --short 2>/dev/null | head -20`
!`launchctl list | grep com.aiharness 2>/dev/null || echo "(no launchd agents)"`
!`sqlite3 bridges/discord/harness.db "SELECT provider, expires_at FROM oauth_tokens" 2>/dev/null || echo "(no oauth tokens)"`

## Check Modules

Parse `$ARGUMENTS` to determine scope. Default is `full` (all checks).

### Credential Safety (`credentials` or `full`)

1. **OAuth token expiry**: Query `oauth_tokens` table — check if any `expires_at` is within 7 days or already expired
2. **Encryption key present**: Check if `OAUTH_ENCRYPTION_KEY` is set in `.env` (don't print the value, just confirm presence/absence)
3. **Refresh token encryption**: Query a token row — check if `refresh_token` field looks encrypted (contains `:` separators for `iv:tag:ciphertext` format) vs plaintext
4. **.env file permissions**: Check `bridges/discord/.env` has restrictive permissions (should be 600 or 640, not world-readable)
5. **No secrets in logs**: Grep heartbeat log files for common secret patterns (API keys, tokens, passwords): `grep -ril "sk-\|Bearer \|password=" heartbeat-tasks/logs/ 2>/dev/null`

Report: token status, encryption status, file permissions, any leaked secrets in logs.

### Git Hygiene (`git` or `full`)

1. **No .env committed**: `git ls-files | grep -i '\.env'` — should return nothing
2. **No credentials in tracked files**: `git ls-files | xargs grep -l "sk-\|PRIVATE KEY\|password\s*=" 2>/dev/null` — should return nothing
3. **Gitignore coverage**: Check that `.env`, `harness.db`, `*.state.json`, `.bot.pid`, `vault-embeddings.json` are in `.gitignore`
4. **No large binaries tracked**: `git ls-files | xargs -I{} sh -c 'test -f "{}" && wc -c < "{}"' 2>/dev/null | sort -rn | head -5` — flag files over 1MB
5. **Uncommitted sensitive changes**: Check `git diff --name-only` for any `.env`, credential, or key files

Report: pass/fail for each check with file paths if issues found.

### Heartbeat Health (`heartbeat` or `full`)

1. **All configs have plists**: Compare `heartbeat-tasks/*.json` (excluding .state.json, .example, projects.json) against `~/Library/LaunchAgents/com.aiharness.heartbeat.*.plist` — flag any missing
2. **All plists loaded**: Check `launchctl list | grep com.aiharness` — flag any with non-zero exit codes
3. **Failure counts**: Read all `.state.json` files — flag any with `consecutive_failures > 0`
4. **Stale tasks**: Flag any task whose `last_run` is more than 3x its schedule interval ago
5. **Auto-paused tasks**: Check all config JSONs for `"enabled": false` — flag with reason

Report: task-by-task status table.

### Configuration Drift (`config` or `full`)

1. **Agent tool restrictions match docs**: Read `bridges/discord/agent-loader.ts` and verify all agents listed in `.claude/agents/` have corresponding restriction entries (or are explicitly unrestricted)
2. **MCP servers registered**: Check `~/.claude/Config/mcp-config.json` — verify vault, harness, projects, outlook, linkedin servers are registered
3. **Global guardrails intact**: Read `task-runner.ts` for `GLOBAL_DISALLOWED_TOOLS` — verify rm -rf, force push, DROP, DELETE FROM, kill -9 are all blocked
4. **Channel configs consistent**: Query `channel_configs` table — verify course channels have `education` agent, project channels have valid agents
5. **PID file stale**: Check `.bot.pid` — is the PID actually alive?

Report: pass/fail for each check.

## Output Format

```
=== AI Harness Security Audit ===

Credentials:
  OAuth tokens:      OK (2 tokens, nearest expiry: 14 days)
  Encryption key:    OK (present in .env)
  Token encryption:  OK (iv:tag:ciphertext format)
  .env permissions:  OK (640)
  Secrets in logs:   OK (none found)

Git:
  .env not tracked:  OK
  No credentials:    OK
  Gitignore:         OK (5/5 patterns present)
  Large files:       OK (none over 1MB)

Heartbeat:
  Plists present:    OK (21/21)
  All loaded:        OK (21/21, exit 0)
  Failures:          OK (0 tasks with failures)
  Stale tasks:       WARN (daily-digest last ran 36h ago)

Config:
  Agent restrictions: OK (9 agents, 4 restricted)
  MCP servers:        OK (5/5 registered)
  Global guardrails:  OK (6 rules intact)
  Channel configs:    OK (4 course channels → education)
  PID file:           OK (PID 12345 alive)

Overall: HEALTHY (1 warning)
```

For issues, list each with severity (CRITICAL/WARN/INFO) and suggested fix.
