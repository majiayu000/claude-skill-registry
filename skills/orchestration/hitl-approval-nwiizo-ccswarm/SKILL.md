# HITL (Human-in-the-Loop) Approval Workflow

Multi-step workflow for human approval integration in ccswarm agent operations.

## Overview

This skill guides you through implementing and using human-in-the-loop approval mechanisms for high-risk agent operations.

## When HITL is Required

### High-Risk Operations
- File deletions
- Database modifications
- External API calls
- Configuration changes
- Deployment actions

### Risk Levels
| Level | Action | HITL Required |
|-------|--------|---------------|
| Low | Read operations | No |
| Medium | Local file writes | Optional |
| High | External modifications | Yes |
| Critical | Production changes | Always |

## Implementation

### 1. HITL Configuration

```json
// ccswarm.json
{
  "hitl": {
    "enabled": true,
    "risk_threshold": 3,
    "auto_approve_patterns": [
      "*.md",
      "docs/*",
      "*.test.rs"
    ],
    "always_require": [
      ".env*",
      "Cargo.toml",
      "production/*"
    ],
    "timeout_seconds": 300
  }
}
```

### 2. Approval Request Format

```rust
pub struct ApprovalRequest {
    pub id: Uuid,
    pub agent_id: String,
    pub operation: OperationType,
    pub target: String,
    pub risk_score: u8,
    pub context: String,
    pub timeout: Duration,
}

pub enum ApprovalStatus {
    Pending,
    Approved { by: String, at: DateTime<Utc> },
    Rejected { by: String, reason: String },
    TimedOut,
}
```

## Workflow

### 1. Request Approval

```bash
# Agent requests approval
ccswarm hitl request \
  --operation "delete" \
  --target "src/legacy/old_module.rs" \
  --reason "Removing deprecated module" \
  --risk-score 4

# Output: Approval request ID: abc123
```

### 2. Review Pending Requests

```bash
# List pending approvals
ccswarm hitl list

# View details
ccswarm hitl show abc123
```

### 3. Approve/Reject

```bash
# Approve with comment
ccswarm hitl approve abc123 --comment "Verified module is unused"

# Reject with reason
ccswarm hitl reject abc123 --reason "Module still referenced in tests"
```

### 4. Check Status

```bash
# Check approval status
ccswarm hitl status abc123
```

## TUI Integration

The HITL system integrates with ccswarm's TUI:

```
┌─────────────────────────────────────────┐
│ Pending Approvals (2)                   │
├─────────────────────────────────────────┤
│ [!] abc123 - Delete old_module.rs       │
│     Risk: 4/5  Agent: backend-agent     │
│     Requested: 2 min ago                │
│                                         │
│ [!] def456 - Modify Cargo.toml          │
│     Risk: 3/5  Agent: devops-agent      │
│     Requested: 5 min ago                │
├─────────────────────────────────────────┤
│ [A]pprove  [R]eject  [D]etails  [Q]uit  │
└─────────────────────────────────────────┘
```

## Best Practices

### For Agents
1. Always provide clear context
2. Calculate accurate risk scores
3. Break large operations into smaller requests
4. Handle timeout gracefully

### For Reviewers
1. Review operation context thoroughly
2. Check affected files/systems
3. Verify agent has appropriate scope
4. Document approval/rejection reasons

## Notifications

### Slack Integration
```bash
# Configure webhook
ccswarm config set hitl.slack_webhook "https://hooks.slack.com/..."

# Notifications sent for:
# - New high-risk requests
# - Approaching timeouts
# - Auto-approved operations
```

### Email Notifications
```bash
ccswarm config set hitl.email "team@example.com"
```

## Audit Trail

All HITL decisions are logged:

```bash
# View audit log
ccswarm hitl audit --last 24h

# Export for compliance
ccswarm hitl audit --format json > hitl_audit.json
```

## Emergency Override

For critical situations:

```bash
# Emergency approval (requires sudo/admin)
ccswarm hitl emergency-approve abc123 \
  --reason "Production incident mitigation" \
  --admin-key $ADMIN_KEY
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `timeout_seconds` | 300 | Time before request expires |
| `risk_threshold` | 3 | Risk level requiring HITL |
| `max_pending` | 10 | Max pending per agent |
| `auto_reject_timeout` | false | Auto-reject on timeout |
