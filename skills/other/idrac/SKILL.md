---
name: idrac
description: |
  Monitor and manage Dell PowerEdge servers via iDRAC Redfish API (iDRAC 8/9).

  Use when asked to:
  - Check server hardware status, health, or temperatures
  - Query CPU, memory, storage/RAID details
  - Monitor system sensors (fans, voltage, thermal)
  - Perform power operations (status, on, off, graceful shutdown, force restart)
  - Check BIOS/firmware versions or system inventory
  - View system event logs (SEL) or lifecycle controller logs
  - Get hardware inventory or serial numbers

  Requires: curl, jq. Optional: 1Password CLI (op) for credential hydration.
  Writes: ~/.config/idrac-skill/config (user-created), ~/.idrac-credentials (cached credentials, mode 600).
  Network: connects to user-configured iDRAC IP only (HTTPS, TLS verification disabled for self-signed certs).

  Helper script: scripts/idrac.sh (relative to this skill)
  Configuration: ~/.config/idrac-skill/config
metadata: { "openclaw": { "emoji": "🖥️", "requires": { "bins": ["curl", "jq"] }, "os": ["darwin", "linux"] } }
---

# iDRAC Skill

Monitor and manage Dell PowerEdge servers via iDRAC Redfish API.

## First-Time Setup

Create a config file at `~/.config/idrac-skill/config`:

```bash
mkdir -p ~/.config/idrac-skill
cat > ~/.config/idrac-skill/config <<'EOF'
# iDRAC connection settings
IDRAC_IP="<your-idrac-ip>"

# Credential source: "1password" | "file" | "env"
CREDS_SOURCE="file"

# For CREDS_SOURCE="1password":
#   OP_ITEM="<1password-item-name>"
#
# For CREDS_SOURCE="file":
#   Create ~/.idrac-credentials with contents: username:password
#   chmod 600 ~/.idrac-credentials
#
# For CREDS_SOURCE="env":
#   Export IDRAC_USER and IDRAC_PASS
EOF
```

## Authentication

The helper script supports three credential sources:

| Source | Config | How It Works |
|--------|--------|--------------|
| **1password** | `OP_ITEM="item-name"` | Pulls username:password via `op` CLI, caches to `~/.idrac-credentials` |
| **file** | (default) | Reads `~/.idrac-credentials` (format: `user:pass`, mode 600) |
| **env** | — | Uses `$IDRAC_USER` and `$IDRAC_PASS` environment variables |

## Helper Script

Location: `scripts/idrac.sh` (relative to this skill directory)

```bash
idrac.sh test            # Test connectivity and authentication
idrac.sh status          # System summary (model, power, CPU, memory)
idrac.sh health          # Health checks (temps, fans, power)
idrac.sh power           # Current power state
idrac.sh inventory       # Full hardware inventory
idrac.sh logs            # Recent system event log entries (last 10)
idrac.sh thermal         # Detailed temperature and fan status
idrac.sh storage         # RAID/disk status
idrac.sh reset-types     # Available power reset types
```

## Workflow

1. **Load config** from `~/.config/idrac-skill/config`
2. **Hydrate credentials** (JIT pattern) if needed
3. **Determine operation type:**
   - **Read-only** (status, health, logs, inventory) → Execute directly
   - **Destructive** (power off, restart, BIOS changes) → Confirm with user first
4. **Query Redfish API** via curl + Basic Auth (or session token for batch ops)
5. **Parse JSON** with jq
6. **Surface findings** to user in natural language
7. **Never expose credentials** in responses

## Endpoint Reference

For raw Redfish API endpoints (system info, thermal, storage, network, logs, power ops, BIOS, firmware, session auth, Dell OEM attributes):

→ See [references/endpoints.md](references/endpoints.md)

## Security Notes

- **Never log or display credentials** — use `--silent` and pipe to jq
- **Credential file** must be mode 600 (`chmod 600 ~/.idrac-credentials`)
- **TLS verification disabled** (`-k`) — iDRAC uses self-signed certs (acceptable for private networks)
- **Power operations are destructive** — confirm with user before executing shutdown/restart

## Compatibility

Works with Dell iDRAC 8 (Redfish 1.0–1.4) and iDRAC 9 (Redfish 1.6+). Covers PowerEdge 13th gen (R630/R730) through current gen. See endpoints reference for version-specific notes.

**Note:** iDRAC 8 API responses can take 5–10s per call. The `test` command makes 4 sequential calls (~30–40s total). Set exec timeouts accordingly. iDRAC 9 is significantly faster.
