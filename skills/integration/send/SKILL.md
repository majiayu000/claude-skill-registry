---
name: send
description: Emit a message or event to an external system with policy enforcement and approval gates. Use when publishing messages, calling APIs, sending notifications, or triggering external workflows. REQUIRES EXPLICIT APPROVAL.
argument-hint: "[destination] [message] [protocol] [--approved]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: prompt
          prompt: |
            OUTBOUND COMMUNICATION SAFETY CHECK

            Command: {{tool_input.command}}

            This skill sends data to external systems. Verify:
            1. Destination is in the approved allowlist
            2. No sensitive data (API keys, passwords, PII) in payload
            3. User has explicitly approved this send operation
            4. Checkpoint exists for state recovery
            5. Rate limits are not being exceeded

            CRITICAL: External sends are IRREVERSIBLE.

            Reply ALLOW only if ALL conditions are verified.
            Reply BLOCK with specific violation if any check fails.
          once: false
        - type: command
          command: |
            # Block if trying to send to localhost or internal networks without approval
            CMD="{{tool_input.command}}"
            if echo "$CMD" | grep -qE "(curl|wget|http)" && echo "$CMD" | grep -qE "(127\.0\.0\.1|localhost|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01]))"; then
              echo "BLOCK: Internal network access requires explicit approval"
              exit 1
            fi
            exit 0
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            echo "[SEND] $(date -u +%Y-%m-%dT%H:%M:%SZ) | Command: {{tool_input.command}} | Status: {{tool_output.exit_code}}" >> .audit/send-operations.log 2>/dev/null || true
---

## Intent

Send a message, event, or payload to an external destination with full policy enforcement, approval gates, and audit trail. This capability handles external side effects that cannot be undone.

**CRITICAL: This capability requires explicit user approval before execution.**

**Success criteria:**
- Message delivered to destination successfully
- All policy constraints verified before sending
- Approval gate passed (explicit user confirmation)
- Complete audit trail of what was sent
- Delivery confirmation obtained where possible

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `destination` | Yes | string | Target endpoint, queue, API, or address |
| `message` | Yes | object | Payload to send |
| `protocol` | Yes | string | Communication protocol (http, grpc, smtp, amqp, etc.) |
| `approval_token` | Yes | string | Token confirming user approved this send (MANDATORY) |
| `checkpoint_ref` | Yes | string | Reference to checkpoint before send (MANDATORY) |
| `constraints` | No | object | Rate limits, size limits, allowed destinations |
| `timeout` | No | integer | Send timeout in milliseconds |
| `retry_policy` | No | object | Retry configuration on failure |

## Procedure

1) **Verify approval**: Confirm explicit user approval exists
   - Check `approval_token` is valid and recent
   - BLOCK send if approval is missing or expired
   - Log approval verification for audit

2) **Verify checkpoint**: Confirm recovery point exists
   - Validate `checkpoint_ref` references valid checkpoint
   - BLOCK send if checkpoint is missing
   - External sends are irreversible - checkpoint is for state recovery

3) **Validate destination**: Ensure target is permitted
   - Check destination against allowlist if defined
   - Verify destination format matches protocol
   - Block sends to disallowed destinations

4) **Apply constraints**: Enforce policy limits
   - Check rate limits have not been exceeded
   - Verify message size within bounds
   - Validate message format against schema
   - Apply `constrain` capability rules

5) **Prepare payload**: Format message for transmission
   - Serialize according to protocol requirements
   - Add required headers/metadata
   - Generate message ID for tracking
   - Record payload summary (not full content if sensitive)

6) **Execute send**: Transmit to destination
   - Use appropriate protocol handler
   - Capture response or confirmation
   - Handle timeouts gracefully
   - Retry according to policy if configured

7) **Verify delivery**: Confirm successful transmission
   - Check response status/acknowledgment
   - Log delivery confirmation
   - Capture any error responses

8) **Audit trail**: Record complete send operation
   - What was sent (summary, not sensitive content)
   - Where it was sent
   - When it was sent
   - Delivery status
   - Approval reference

## Output Contract

Return a structured object:

```yaml
sent:
  destination: string  # Where message was sent
  payload_type: string  # Type of content sent
  payload_summary: string  # Non-sensitive summary of payload
  timestamp: string  # ISO timestamp of send
  message_id: string | null  # Tracking ID if available
delivery:
  status: sent | queued | failed  # Delivery outcome
  confirmation: string | null  # Delivery receipt or acknowledgment
  retry_count: integer  # Number of retry attempts
  response_code: integer | null  # HTTP status or protocol response
  error: string | null  # Error message if failed
constraints_applied:
  - constraint: string  # What constraint was checked
    enforced: boolean  # Whether it passed
    details: string | null  # Additional context
approval:
  token: string  # Approval token used
  timestamp: string  # When approval was given
  scope: string  # What was approved
confidence: 0..1  # Confidence in successful delivery
evidence_anchors: ["log:timestamp", "api:response"]
assumptions: []  # Explicit assumptions
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `sent` | object | Details of what was sent |
| `delivery` | object | Outcome of send operation |
| `constraints_applied` | array | Policy checks performed |
| `approval` | object | Approval gate information |
| `confidence` | number | 0.0-1.0 based on delivery confirmation |
| `evidence_anchors` | array | Logs, responses, confirmations |
| `assumptions` | array | Explicit assumptions (e.g., "network stable") |

## Examples

### Example 1: API Webhook Notification

**Input:**
```yaml
destination: "https://api.partner.com/webhooks/order-updates"
message:
  event: "order.completed"
  order_id: "ORD-12345"
  timestamp: "2024-01-15T10:30:00Z"
  customer_notified: true
protocol: "http"
approval_token: "approve-send-2024-01-15-001"
checkpoint_ref: "checkpoint-2024-01-15-001"
constraints:
  rate_limit: "100/hour"
  allowed_domains: ["api.partner.com"]
```

**Output:**
```yaml
sent:
  destination: "https://api.partner.com/webhooks/order-updates"
  payload_type: "order.completed event"
  payload_summary: "Order completion notification for ORD-12345"
  timestamp: "2024-01-15T10:30:15Z"
  message_id: "msg-abc123"
delivery:
  status: sent
  confirmation: "HTTP 200 OK, body: {\"received\": true}"
  retry_count: 0
  response_code: 200
  error: null
constraints_applied:
  - constraint: "rate_limit: 100/hour"
    enforced: true
    details: "Current rate: 45/hour"
  - constraint: "allowed_domains"
    enforced: true
    details: "api.partner.com is in allowlist"
approval:
  token: "approve-send-2024-01-15-001"
  timestamp: "2024-01-15T10:30:00Z"
  scope: "Send order notification to partner API"
confidence: 0.95
evidence_anchors:
  - "log:2024-01-15T10:30:15Z:send-success"
  - "api:response:200-OK"
assumptions:
  - "Partner API is available and processing webhooks"
```

**Evidence pattern:** HTTP response code and body confirmation, timestamped log entry.

---

### Example 2: Email Notification (with failure)

**Input:**
```yaml
destination: "smtp://mail.company.com:587"
message:
  to: "user@example.com"
  subject: "Action Required: Review pending"
  body: "You have 3 items awaiting review..."
protocol: "smtp"
approval_token: "approve-email-2024-01-15-002"
checkpoint_ref: "checkpoint-2024-01-15-002"
timeout: 30000
```

**Output:**
```yaml
sent:
  destination: "smtp://mail.company.com:587"
  payload_type: "email"
  payload_summary: "Email to user@example.com regarding pending review"
  timestamp: "2024-01-15T11:00:05Z"
  message_id: null
delivery:
  status: failed
  confirmation: null
  retry_count: 3
  response_code: null
  error: "Connection timeout after 30s - SMTP server unreachable"
constraints_applied:
  - constraint: "recipient_validation"
    enforced: true
    details: "Email format valid"
approval:
  token: "approve-email-2024-01-15-002"
  timestamp: "2024-01-15T11:00:00Z"
  scope: "Send review notification email"
confidence: 0.0
evidence_anchors:
  - "log:2024-01-15T11:00:05Z:smtp-timeout"
  - "error:connection-refused"
assumptions:
  - "SMTP server should be available on port 587"
next_actions:
  - "Verify SMTP server status"
  - "Check network connectivity"
  - "Retry with backup mail server if available"
```

## Verification

- [ ] Approval token is valid and not expired
- [ ] Checkpoint reference exists
- [ ] Destination passes policy validation
- [ ] All constraints were checked before send
- [ ] Delivery status is accurately reported
- [ ] Audit trail is complete

**Verification tools:** Read (for logs), Bash (for health checks)

## Safety Constraints

- `mutation`: true
- `requires_checkpoint`: true
- `requires_approval`: true
- `risk`: high

**Capability-specific rules:**
- NEVER send without explicit user approval (CRITICAL)
- NEVER send without a valid checkpoint reference
- ALWAYS validate destination against policy before sending
- ALWAYS log what was sent for audit (sanitize sensitive data)
- DO NOT retry indefinitely - respect retry limits
- BLOCK sends to destinations not in allowlist when list is defined
- If approval token is missing, REQUEST approval before proceeding
- Never send credentials, API keys, or secrets in payloads

**APPROVAL GATE REQUIREMENT:**
Before any send operation, the user must explicitly approve:
1. What will be sent (summary)
2. Where it will be sent (destination)
3. Why it is being sent (context)

The approval must be captured with a token that is referenced in this operation.

## Composition Patterns

**Commonly follows:**
- `constrain` - Apply policy limits before sending (REQUIRED)
- `checkpoint` - Create recovery point before external send (REQUIRED)
- `plan` - Sends are typically part of a larger plan
- `transform` - Format data before sending

**Commonly precedes:**
- `audit` - Record what was sent for compliance
- `verify` - Confirm delivery where possible
- `receive` - May expect response from destination

**Anti-patterns:**
- NEVER send without `constrain` check (policy bypass)
- NEVER send without `checkpoint` (no state recovery)
- NEVER send without explicit approval (unauthorized action)
- NEVER retry failed sends indefinitely (resource exhaustion)

**Workflow references:**
- See `reference/composition_patterns.md#anti-patterns` for send safety rules
- See `reference/composition_patterns.md#digital-twin-sync-loop` for send in sync context
