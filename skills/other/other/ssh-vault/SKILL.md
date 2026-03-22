---
name: ssh-vault
description: "Execute SSH commands on remote hosts via SSH Vault MCP. Use when: user asks to run commands on vault-managed hosts, or when in a Discord channel mapped to a vault host. NOT for: hosts with direct SSH access or openclaw nodes. Ask user for their vault URL if not known. Requires env vars: SSH_VAULT_URL (vault endpoint), SSH_VAULT_AGENT_PRIVATE_KEY and SSH_VAULT_AGENT_PUBLIC_KEY (Ed25519 agent keypair for request signing). The private key is used only for signing vault API requests — never reuse keys tied to other services."
---

# SSH Vault

Execute SSH commands on remote hosts through a self-hosted SSH Vault instance.

User has deployed SSH Vault via Docker. Ask for their vault URL if not known.

Required env vars:
- `SSH_VAULT_URL` — vault URL
- `SSH_VAULT_AGENT_PRIVATE_KEY` — agent Ed25519 private key (base64)
- `SSH_VAULT_AGENT_PUBLIC_KEY` — agent Ed25519 public key (base64)
Fingerprint is auto-derived from public key.

## Docker Setup (user-managed)

```bash
docker run -d -p 3001:3001 \
  -v vault-data:/app/data \
  -v vault-config:/app/config \
  qsobad/ssh-vault-mcp:latest
```

- `/app/config/config.yml` — auto-created with localhost defaults if missing
- `/app/data` — encrypted vault storage
- Set `SSH_VAULT_ORIGIN env var for custom origin (e.g. https://ssh.example.com))

## Execution

```bash
node scripts/vault.mjs exec <host> <command> [timeout]
```

**Happy path (has session):** returns `{ stdout, stderr, exitCode }` immediately.

**No session:** returns `needsApproval`:
```json
{ "needsApproval": true, "approvalUrl": "...", "listenUrl": "...", "execRequestId": "..." }
```

### Approval Flow

1. Show `approvalUrl` to user — opens `/approve-exec` page showing host + command
2. User authenticates with **Master Password + Passkey** → vault unlocks, command executes
3. Listen on `listenUrl` (SSE) for result:
   ```
   data: {"status":"pending"}
   data: {"status":"approved"}
   data: {"status":"executing"}
   data: {"status":"completed","stdout":"...","stderr":"...","exitCode":0,"sessionId":"..."}
   ```
4. Save `sessionId` to `/tmp/ssh-vault-session.json` — subsequent commands skip approval

Shell metacharacters (`&&`, `;`, `|`, `$()`, backticks) are all allowed in commands.

## Other Commands

```bash
node scripts/vault.mjs status              # Vault lock status
node scripts/vault.mjs session             # Cached session info
node scripts/vault.mjs register            # Register agent
node scripts/vault.mjs check-unlock <id>   # Check unlock & get session
node scripts/vault.mjs hosts               # List hosts (needs session)
```

## Adding Hosts

Hosts can be added by agent via API — user provides credential (password/key) during approval:
```bash
node scripts/vault.mjs request-host <name> <ip> <user> [port] [authType]
```

## Error Handling

- `needsApproval` → show approvalUrl, listen SSE
- `Host not found` → check with `hosts`
- `Agent not registered` → run `register`
