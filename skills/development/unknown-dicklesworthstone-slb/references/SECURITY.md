# SLB Security Design — Reference

## Table of Contents
- [Defense in Depth](#defense-in-depth)
- [Execution Verification Gates](#execution-verification-gates)
- [Cryptographic Guarantees](#cryptographic-guarantees)
- [Fail-Closed Behavior](#fail-closed-behavior)
- [Emergency Override](#emergency-override)
- [Safety Note](#safety-note)

---

## Defense in Depth (6 Layers)

1. **Pattern-based classification** — Commands categorized by risk tier
2. **Peer review requirement** — Another agent must approve
3. **Command hash binding** — SHA-256 prevents modification
4. **Approval TTL** — Approvals expire after 10-30 minutes
5. **Execution verification gates** — 5 checks before execution
6. **Audit logging** — All actions logged with full context

---

## Execution Verification Gates

Before any command executes, five gates must pass:

| Gate | Check |
|------|-------|
| **1. Status** | Request must be in APPROVED state |
| **2. Expiry** | Approval TTL must not have elapsed |
| **3. Hash** | SHA-256 hash of command must match (tamper detection) |
| **4. Tier** | Risk tier must still match (patterns may have changed) |
| **5. First-Executor** | Atomic claim prevents race conditions |

---

## Cryptographic Guarantees

- **Command binding**: SHA-256 hash verified at execution
- **Review signatures**: HMAC using session keys
- **Session keys**: Generated per-session, never stored in plaintext

---

## Fail-Closed Behavior

- **Daemon unreachable** → Block dangerous commands (hook)
- **Parse error** → Upgrade tier by one level
- **Approval expired** → Require new approval
- **Hash mismatch** → Reject execution

---

## Emergency Override

For true emergencies, humans can bypass with extensive logging:

```bash
# Interactive (prompts for confirmation)
slb emergency-execute "rm -rf /tmp/broken" --reason "System emergency: disk full"

# Non-interactive (requires hash acknowledgment)
HASH=$(echo -n "rm -rf /tmp/broken" | sha256sum | cut -d' ' -f1)
slb emergency-execute "rm -rf /tmp/broken" --reason "Emergency" --yes --ack $HASH
```

**Safeguards**: Mandatory reason, hash acknowledgment, extensive logging, optional rollback capture.

---

## Safety Note

SLB adds friction and peer review for dangerous actions. It does NOT replace:
- Least-privilege credentials
- Environment safeguards
- Proper access controls
- Backup strategies

Use SLB as **defense in depth**, not your only protection.

---

## Flywheel Integration

| Tool | Integration |
|------|-------------|
| **Agent Mail** | Notify reviewers via inbox; track audit trails |
| **BV** | Track SLB requests as beads |
| **CASS** | Search past SLB decisions across sessions |
| **DCG** | DCG blocks automatically; SLB adds peer review layer |
| **NTM** | Coordinate review across agent terminals |
