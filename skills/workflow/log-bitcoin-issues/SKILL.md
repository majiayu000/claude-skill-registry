---
name: log-bitcoin-issues
description: |
  Run /check-bitcoin, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-bitcoin instead if you want to fix issues immediately.
---

# /log-bitcoin-issues

Run Bitcoin integration audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-bitcoin` to audit Bitcoin integration
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-bitcoin` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-bitcoin` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/bitcoin" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P0] Hot wallet key stored in repo" \
  --body "$(cat <<'EOF'
## Problem
Bitcoin hot wallet private key committed in repo. Critical loss risk.

## Impact
- Funds theft
- Full wallet compromise
- Irreversible loss

## Location
`config/bitcoin.ts`

## Suggested Fix
Run `/fix-bitcoin` or move key to secret store and rotate.

---
Created by `/log-bitcoin-issues`
EOF
)" \
  --label "priority/p0,domain/bitcoin,type/bug"
```

### 4. Issue Format

**Title:** `[P{0-3}] Bitcoin issue description`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/bitcoin`
- `type/bug` | `type/enhancement` | `type/chore`

**Body:**
```markdown
## Problem
What's wrong with Bitcoin integration

## Impact
Business/security/user impact

## Location
File:line if applicable

## Suggested Fix
Code snippet or skill to run

---
Created by `/log-bitcoin-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Private key in code/repo | P0 |
| No confirmation checks | P0 |
| Wrong network (mainnet/testnet) | P0 |
| Address reuse | P1 |
| No reorg handling | P1 |
| No double-spend/mempool checks | P1 |
| No fee estimation/bumping | P2 |
| Single node/provider dependency | P2 |
| Missing monitoring/alerts | P2 |
| Advanced features (RBF/CPFP/PSBT) | P3 |

## Output

After running:
```
Bitcoin Issues Created:
- P0: 2 (keys, confirmations)
- P1: 3 (reorg, reuse, mempool)
- P2: 3 (fees, redundancy, alerts)
- P3: 1 (advanced features)

Total: 9 issues created
View: gh issue list --label domain/bitcoin
```

## Related

- `/check-bitcoin` - The primitive (audit only)
- `/fix-bitcoin` - Fix Bitcoin issues
- `/bitcoin` - Full Bitcoin lifecycle
- `/bitcoin-health` - Node and webhook diagnostics
- `/groom` - Full backlog grooming
