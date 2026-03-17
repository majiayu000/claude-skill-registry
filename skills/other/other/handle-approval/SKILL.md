---
name: handle-approval
description: Manage human-in-the-loop approval workflow for sensitive actions like payments, email sending, social media posts, and file operations. Creates structured approval requests, monitors approval status in /Approved and /Rejected folders, executes approved actions safely, and maintains complete audit logs. Use when any action requires approval, user mentions "check approvals", "pending approval", "approve this", "what needs approval", or before executing sensitive operations like payments, emails, or social posts.
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# Handle Approval Skill

Manages the **Human-in-the-Loop (HITL)** approval workflow - the safety layer for all sensitive actions.

---

## Core Responsibilities

1. **Create Approval Requests**: Generate structured approval files for sensitive actions
2. **Monitor Approval Status**: Check `Vault/Approved` and `Vault/Rejected` folders for human decisions
3. **Execute Approved Actions**: Safely execute actions once approved
4. **Maintain Audit Trail**: Log all approval decisions and outcomes
5. **Enforce Security Rules**: Ensure compliance with approval thresholds

---

## When This Skill Activates

**Trigger phrases:**
- "check approvals"
- "handle pending approvals"
- "what needs my approval"
- "approve this"
- "check approval status"
- "pending approvals"

**Auto-activates when:**
- Any action requires human approval
- Monitoring approval folders for decisions
- Before executing potentially risky operations

---

## Core Workflow

### Phase 1: Creating Approval Requests

When a skill needs approval (e.g., `process-emails`, `post-to-linkedin`):

1. **Determine Action Type**
   - Identify category: `payment`, `email`, `social`, `file`, or `other`
   - Check [approval-thresholds.md](./reference/approval-thresholds.md) to confirm approval needed
   - Verify action aligns with `Vault/Business_Goals.md` and `Vault/Company_Handbook.md`

2. **Create Approval Request File**
   - Filename format: `APPROVAL_[TYPE]_[DESCRIPTION]_[DATE].md`
   - Example: `APPROVAL_EMAIL_ClientA_Invoice_2026-01-11.md`
   - Save in `Vault/Pending_Approval` folder
   - Use [approval-template.md](./reference/approval-template.md)

3. **Include Critical Information**
   - **Action Summary**: One-line clear description
   - **Details**: Action type, target, reason, source
   - **Parameters**: All required values (recipient, amount, content, etc.)
   - **Draft/Preview**: Show what will be sent/posted
   - **Risks**: What could go wrong
   - **Expiration**: When approval expires (24-72 hours based on action type)
   - **Instructions**: How to approve (move to `Vault/Approved`) or reject (move to `Vault/Rejected`)

4. **Log to Dashboard**
   - Update `Vault/Dashboard.md` with approval request created
   - Include timestamp, action type, priority

See [approval-template.md](./reference/approval-template.md) for complete format.

---

### Phase 2: Monitoring Approval Status

Run when user asks to "check approvals" or periodically:

1. **Scan `Vault/Pending_Approval` Folder**
   - List all pending approval files
   - Check for expired approvals (past expiration timestamp)
   - Report summary (count by priority)

2. **Check `Vault/Approved` Folder**
   - Find newly approved files
   - For each: validate format, re-check parameters, proceed to execution

3. **Check `Vault/Rejected` Folder**
   - Find newly rejected files
   - Read rejection reason (human adds at bottom)
   - Log to Dashboard, move to `Vault/Done`

4. **Handle Expired Approvals**
   - Move to `Vault/Rejected` with "EXPIRED - No decision made" note
   - Log expiration to Dashboard

**Helper Script:**
```bash
python .claude/skills/handle-approval/scripts/check_approval_status.py [--json]
```

---

### Phase 3: Executing Approved Actions

**CRITICAL: Only execute if file is in `Vault/Approved` folder and passes validation**

1. **Validate Approval File**
   - Confirm proper structure and required sections
   - Check not expired
   - Verify all parameters present and valid
   - Confirm action type supported

2. **Re-Validate Parameters**
   - Check against [security-rules.md](./reference/security-rules.md)
   - Verify recipient/target still valid
   - Confirm amounts within limits (for payments)
   - Check for duplicates (prevent double-execution)

3. **Execute Action by Type**
   - **Email**: Use Email MCP server
   - **Social Media**: Use platform-specific MCP (LinkedIn, Twitter, etc.)
   - **Payment**: Use Banking/Payment MCP
   - **File**: Perform file operation
   - Capture result (success/failure, confirmation ID, errors)

4. **Log Execution**
   - Add to approval file Execution Log section
   - Include timestamp, result, confirmation IDs, errors
   - Mark executed_by: "claude_code"

5. **Move to `Vault/Done`**
   - Archive completed approval
   - Update `Vault/Dashboard.md`

---

### Phase 4: Error Handling

**If execution fails:**

1. **Capture Error Details**
   - Full error message and code
   - Timestamp of failure

2. **Log to Approval File**
   - Add error to Execution Log section
   - Mark status: "failed"

3. **DO NOT Move to `Vault/Done`**
   - Keep in `Vault/Pending_Approval` for human review
   - Allows retry or rejection decision

4. **Alert User**
   - Update Dashboard with high-priority error
   - Include next steps

5. **Never Auto-Retry**
   - Financial/communication actions must not auto-retry
   - Always require fresh approval after failure

---

## Security Safeguards

### Before Creating Approval:
- ✅ Action not in auto-approve list
- ✅ Aligns with `Vault/Business_Goals.md`
- ✅ Follows `Vault/Company_Handbook.md` rules
- ✅ All parameters valid

### Before Executing Approval:
- ✅ File in `Vault/Approved` folder
- ✅ Not expired
- ✅ Parameters pass security validation
- ✅ Action type supported
- ✅ MCP server available

### Never Execute If:
- ❌ File in `Vault/Pending_Approval`
- ❌ Approval expired
- ❌ Parameters violate security rules
- ❌ MCP server unavailable
- ❌ Any validation fails

See [security-rules.md](./reference/security-rules.md) for complete policies.

---

## Reference Files

**Progressive disclosure - load on demand:**

1. **[approval-thresholds.md](./reference/approval-thresholds.md)**
   - What requires approval vs auto-approve
   - Thresholds by action type (email, payment, social, files)
   - Conditional approval rules

2. **[approval-template.md](./reference/approval-template.md)**
   - Standard format for approval requests
   - Template variations by action type
   - Required vs optional sections

3. **[security-rules.md](./reference/security-rules.md)**
   - Security validation rules
   - Never auto-approve list
   - Expiration policies
   - Rate limiting

4. **[troubleshooting.md](./reference/troubleshooting.md)**
   - Common issues and solutions
   - Error message reference
   - Debugging workflow

---

## Helper Scripts

### check_approval_status.py

**Purpose:** Scan approval folders and generate status report

**Usage:**
```bash
# Human-readable output (may have encoding issues on Windows)
python .claude/skills/handle-approval/scripts/check_approval_status.py

# JSON output (recommended for Windows, programmatic parsing)
python .claude/skills/handle-approval/scripts/check_approval_status.py --json

# Specify vault path
python .claude/skills/handle-approval/scripts/check_approval_status.py --vault-path Vault/
```

**Output:**
- Summary: Count of pending, approved, rejected, expired
- Pending approvals with priority and age
- Actions awaiting execution
- Recently rejected items
- Expired approvals

---

## Integration with Other Skills

**Skills that call handle-approval:**
- `process-emails` → Creates approval for sending emails
- `post-to-linkedin` → Creates approval for social posts
- `process-tasks` → May create approval for sensitive file operations

**Workflow:**
```
1. Skill determines action needs approval
2. Calls handle-approval to create approval request
3. handle-approval creates file in `Vault/Pending_Approval`
4. Human manually moves to `Vault/Approved` or `Vault/Rejected`
5. User invokes handle-approval to check status
6. handle-approval executes approved actions
```

---

## Dashboard Logging

All approval activity logged to `Vault/Dashboard.md`:

```markdown
### [Timestamp] - Approval Activity

**Request Created:**
- Type: [email/payment/social/file]
- Action: [Description]
- Status: Pending Approval
- File: Vault/Pending_Approval/[filename]

**Approval Executed:**
- Type: [email/payment/social/file]
- Result: Success/Failed
- Details: [Confirmation ID or error]

**Approval Rejected:**
- Type: [email/payment/social/file]
- Reason: [Human's rejection reason]
```

---

## Success Criteria

This skill works correctly when:

✅ All sensitive actions create approval requests
✅ Approval files properly formatted and complete
✅ Approved actions execute successfully with logs
✅ Rejected actions logged and archived
✅ Expired approvals handled automatically
✅ Dashboard maintains complete audit trail
✅ Zero unauthorized actions
✅ No duplicate or partial executions

---

## Common Issues

See [troubleshooting.md](./reference/troubleshooting.md) for complete guide.

**Quick fixes:**
- **Action not executing**: Verify file in `Vault/Approved` (not `Vault/Pending_Approval`)
- **MCP server error**: Check server running and authenticated
- **Expired prematurely**: Verify timestamps in UTC (ISO 8601 with Z)
- **Can't find approvals**: Check filename matches `APPROVAL_*.md` pattern
- **Encoding errors (Windows)**: Use `--json` flag with check_approval_status.py

---

*Skill Version: 2.1 (Updated for Vault structure)*
*Last Updated: 2026-01-11*
*Branch: feat/silver-core-workflows*