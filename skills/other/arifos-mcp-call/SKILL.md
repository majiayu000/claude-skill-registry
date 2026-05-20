---
name: arifos-mcp-call
description: Invoke arifOS constitutional MCP tools (000-999 pipeline, F1-F13 enforced)
user-invocable: true
---

# arifOS MCP Caller v2 — Constitutional Anchor-First

**Runtime:** 42-tool constitutional kernel (not 13)  
**Requirement:** `init_anchor` MUST be called before `arifOS_kernel`  
**Floors:** F1-F13 enforced via sBERT ML layer  

## Constitutional Tool Contract

| Stage | Tool | Purpose |
|-------|------|---------|
| **000_INIT** | `init_anchor` | **REQUIRED FIRST** — Bootstrap session, bind actor_id, risk tier |
| **333→888** | `arifOS_kernel` | Full pipeline: reason → memory/heart → critique → forge → judge |
| **888_JUDGE** | `apex_judge` | Cross-check decisions |
| **999_VAULT** | `vault_seal` | Persist to VAULT999 |

## CLI Usage (via arifos bridge)

```bash
# 1. Bootstrap anchor (REQUIRED before kernel)
arifos anchor

# 2. Call kernel with dry-run first
arifos kernel '{"query":"Analyze this","dry_run":true,"actor_id":"arif"}'

# 3. Full execution (after verification)
arifos kernel '{"query":"Execute task","actor_id":"arif","risk_tier":"medium"}'

# Evidence & Memory
arifos search '{"query":"AI governance Malaysia"}'
arifos ingest '{"url":"https://example.com/doc"}'
arifos memory '{"operation":"search","content":"What is Floor F2?"}'

# System & Audit
arifos health
arifos vital
arifos audit

# AgentZero
arifos engineer
arifos validate
arifos holdcheck
```

## F13 Sovereignty Handling

If the kernel returns `requires_human: true` or `verdict: "HOLD_888"`:
- **STOP execution**
- **Prompt user for confirmation**
- **Do not proceed until explicit "do it"**

Exit code 88 = HOLD_888 (sovereign approval required).

## Direct HTTP (advanced)

```bash
# Health & discovery
curl -s http://arifosmcp_server:8080/health | jq

# List all 42 tools
curl -s -X POST http://arifosmcp_server:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Anchor session (000_INIT)
curl -s -X POST http://arifosmcp_server:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "init_anchor",
      "arguments": {
        "actor_id": "arif",
        "risk_tier": "low",
        "session_id": "test-001"
      }
    }
  }'

# Kernel call (after anchor)
curl -s -X POST http://arifosmcp_server:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "arifOS_kernel",
      "arguments": {
        "query": "Explain F1-F13 in 3 bullets",
        "actor_id": "arif",
        "risk_tier": "low",
        "dry_run": true
      }
    }
  }'
```

## Golden Test Pair (Acceptance)

Run these to verify OpenClaw ↔ arifOS wiring:

**Test A — Bootstrap:**
```bash
arifos anchor
# Expect: {"ok": true, "status": "anchored"}
```

**Test B — Kernel Dry-Run:**
```bash
arifos kernel '{"query":"Test","dry_run":true}'
# Expect: 000→999 pipeline simulated, no external execution
```

**Test C — F13 Hold:**
```bash
arifos kernel '{"query":"Drop production database"}'
# Expect: {"verdict": "HOLD_888", "status": "AWAITING_SOVEREIGN_APPROVAL"}
```

## Migration from v1

- **Tool name:** `arifOS.kernel` → `arifOS_kernel` (underscore)
- **Anchor required:** Was optional, now mandatory
- **Tool count:** 13 → 42 (implementation detail, don't hard-code)
- **Floors:** sBERT ML enforcement now active

## References

- Full contract: `/mnt/arifos/AGENTS.md` (v2 reality-sealed)
- PyPI: https://pypi.org/project/arifos/
- Runtime: `arifos-aaa-mcp v2026.03.14-VALIDATED`

## F13 Human-in-the-Loop Handling

When `arifOS_kernel` returns `requires_human: true` or `verdict: "HOLD_888"`:

### Response Schema
```json
{
  "requires_human": true,
  "verdict": "HOLD_888",
  "status": "SABAR",
  "machine_status": "BLOCKED",
  "authority": {
    "human_required": true,
    "approval_scope": ["arifOS_kernel:execute"]
  },
  "errors": [{
    "code": "F13_SOVEREIGNTY_HOLD",
    "message": "High-risk execution requires sovereign approval.",
    "remediation": {
      "action": "REQUEST_HUMAN_APPROVAL",
      "ui_prompt": "This action requires your explicit approval.",
      "risk_summary": "..."
    }
  }],
  "payload": {
    "hold_reason": "...",
    "proceed_conditions": ["human_verbal_confirmation", "explicit_allow_execution"]
  }
}
```

### OpenClaw Handler Logic

1. **STOP** — Do not proceed automatically when `requires_human: true`
2. **SURFACE** — Show user: `payload.hold_reason` + `errors[0].remediation.risk_summary`
3. **WAIT** — For explicit "do it" or "hold" from sovereign (F13)
4. **RESUME** — If "do it", re-call with `allow_execution: true` + `human_confirmed: true`

### Exit Codes
- `88` = HOLD_888 (human approval required)
- `1` = Error
- `0` = Success

### Example Flow
```bash
# 1. Dry-run first (safe)
arifos kernel '{"query":"Delete database","dry_run":true}'
# Returns: HOLD_888 with requires_human: true

# 2. User reviews risk, replies "do it"

# 3. Execute with approval
arifos kernel '{"query":"Delete database","allow_execution":true,"human_confirmed":true}'
```
