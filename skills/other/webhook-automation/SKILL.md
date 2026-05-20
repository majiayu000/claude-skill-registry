---
name: Webhook Automation
description: Build and manage webhook-based integrations for real-time event processing and API connections
version: 1.0.0
author: Claude Office Skills
category: integration
tags:
  - webhook
  - api
  - integration
  - automation
  - events
department: engineering
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: integration-mcp
  tools:
    - webhook_create
    - webhook_receive
    - http_request
    - transform_data
capabilities:
  - Webhook endpoint creation
  - Event processing
  - Data transformation
  - Multi-service orchestration
input:
  - Webhook payloads
  - API configurations
  - Transformation rules
  - Routing logic
output:
  - Processed events
  - API responses
  - Transformed data
  - Audit logs
languages:
  - en
related_skills:
  - etl-pipeline
  - api-integration
  - zapier-automation
---

# Webhook Automation

Comprehensive skill for building webhook-based integrations and real-time event processing.

## Core Concepts

### Webhook Architecture

```
WEBHOOK FLOW:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Source    │────▶│   Webhook   │────▶│   Handler   │
│   System    │     │   Endpoint  │     │   Logic     │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼───────┐
                    │                          │       │
                    ▼                          ▼       ▼
              ┌──────────┐              ┌──────────┐ ┌──────────┐
              │  Action  │              │  Action  │ │  Action  │
              │    A     │              │    B     │ │    C     │
              └──────────┘              └──────────┘ └──────────┘
```

### Webhook Types

```yaml
webhook_types:
  incoming:
    description: "Receive events from external services"
    use_cases:
      - Payment notifications (Stripe, PayPal)
      - Form submissions
      - CRM updates
      - CI/CD events
      
  outgoing:
    description: "Send events to external services"
    use_cases:
      - Notify external systems
      - Trigger workflows
      - Sync data
      - Alert integrations
```

## Webhook Endpoint Setup

### Basic Endpoint

```yaml
webhook_endpoint:
  url: "https://api.example.com/webhooks/incoming"
  method: POST
  
  authentication:
    type: signature
    header: "X-Signature-256"
    algorithm: "HMAC-SHA256"
    secret: "${WEBHOOK_SECRET}"
    
  validation:
    required_headers:
      - "Content-Type"
      - "X-Request-ID"
    content_types:
      - "application/json"
      - "application/x-www-form-urlencoded"
      
  response:
    success:
      status: 200
      body: { "received": true }
    error:
      status: 400
      body: { "error": "Invalid payload" }
```

### Signature Verification

```javascript
// Verify webhook signature
function verifySignature(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = 'sha256=' + hmac.update(payload).digest('hex');
  
  return crypto.timingSafeEqual(
    Buffer.from(digest),
    Buffer.from(signature)
  );
}

// Usage
app.post('/webhook', (req, res) => {
  const signature = req.headers['x-signature-256'];
  const payload = JSON.stringify(req.body);
  
  if (!verifySignature(payload, signature, process.env.WEBHOOK_SECRET)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  // Process webhook...
  processWebhook(req.body);
  res.status(200).json({ received: true });
});
```

## Event Processing

### Event Router

```yaml
event_router:
  routes:
    - event_type: "payment.succeeded"
      handler: processPayment
      actions:
        - update_order_status
        - send_confirmation_email
        - notify_fulfillment
        
    - event_type: "customer.created"
      handler: processNewCustomer
      actions:
        - create_crm_contact
        - send_welcome_email
        - assign_to_sales
        
    - event_type: "subscription.cancelled"
      handler: processChurn
      actions:
        - update_subscription_status
        - trigger_retention_flow
        - notify_customer_success
        
    - event_type: "*"
      handler: logUnhandled
      actions:
        - log_to_monitoring
```

### Payload Transformation

```yaml
transformations:
  - name: stripe_to_internal
    source: stripe_webhook
    target: internal_order
    mapping:
      id: "data.object.id"
      amount: "data.object.amount / 100"  # Cents to dollars
      currency: "data.object.currency | uppercase"
      customer_email: "data.object.receipt_email"
      created_at: "data.object.created | timestamp"
      metadata: "data.object.metadata"
      
  - name: github_to_slack
    source: github_webhook
    target: slack_message
    mapping:
      text: |
        *{{action | capitalize}} {{repository.name}}*
        {{#if pull_request}}
        PR: {{pull_request.title}}
        By: {{pull_request.user.login}}
        {{/if}}
      channel: "{{repository.name}}-notifications"
```

## Common Integrations

### Stripe Webhooks

```yaml
stripe_webhooks:
  endpoint_secret: "${STRIPE_WEBHOOK_SECRET}"
  
  events:
    - type: "checkout.session.completed"
      handler: |
        async function(event) {
          const session = event.data.object;
          await fulfillOrder(session);
          await sendReceipt(session.customer_email);
        }
        
    - type: "invoice.payment_failed"
      handler: |
        async function(event) {
          const invoice = event.data.object;
          await notifyCustomer(invoice);
          await createDunningTask(invoice);
        }
        
    - type: "customer.subscription.updated"
      handler: |
        async function(event) {
          const subscription = event.data.object;
          await syncSubscriptionStatus(subscription);
        }
```

### GitHub Webhooks

```yaml
github_webhooks:
  secret: "${GITHUB_WEBHOOK_SECRET}"
  
  events:
    - type: "push"
      branches: ["main", "develop"]
      handler: |
        async function(event) {
          await triggerCI(event.repository, event.ref);
          await notifyTeam(event.commits);
        }
        
    - type: "pull_request"
      actions: ["opened", "synchronize"]
      handler: |
        async function(event) {
          await runTests(event.pull_request);
          await requestReview(event.pull_request);
        }
        
    - type: "issues"
      actions: ["opened"]
      handler: |
        async function(event) {
          await triageIssue(event.issue);
          await assignOwner(event.issue);
        }
```

### Slack Webhooks

```yaml
slack_webhooks:
  incoming:
    # Receive slash commands and interactions
    signing_secret: "${SLACK_SIGNING_SECRET}"
    
    events:
      - type: "slash_command"
        command: "/deploy"
        handler: handleDeployCommand
        
      - type: "interactive_message"
        callback_id: "approval_*"
        handler: handleApproval
        
  outgoing:
    # Send messages to Slack
    webhook_url: "${SLACK_WEBHOOK_URL}"
    
    templates:
      alert:
        blocks:
          - type: section
            text: "🚨 *Alert:* {{message}}"
          - type: context
            elements:
              - type: mrkdwn
                text: "Source: {{source}} | Time: {{timestamp}}"
```

## Error Handling

### Retry Strategy

```yaml
retry_config:
  enabled: true
  
  policy:
    max_attempts: 5
    initial_delay: 1000  # ms
    max_delay: 60000  # ms
    backoff_multiplier: 2
    
  retry_on:
    status_codes: [408, 429, 500, 502, 503, 504]
    exceptions: ["ECONNRESET", "ETIMEDOUT"]
    
  dead_letter:
    enabled: true
    destination: "failed_webhooks_queue"
    retention_days: 7
```

### Error Logging

```yaml
error_handling:
  logging:
    level: error
    include:
      - request_id
      - event_type
      - payload_hash
      - error_message
      - stack_trace
      - retry_count
      
  alerting:
    on_failure:
      - type: slack
        channel: "#webhook-alerts"
        threshold: 5  # failures per minute
        
    on_dead_letter:
      - type: pagerduty
        severity: warning
```

## Webhook Testing

### Test Payload Generator

```yaml
test_payloads:
  stripe_payment:
    type: "checkout.session.completed"
    data:
      object:
        id: "cs_test_123"
        amount_total: 2000
        currency: "usd"
        customer_email: "test@example.com"
        payment_status: "paid"
        
  github_push:
    ref: "refs/heads/main"
    repository:
      name: "my-repo"
      full_name: "org/my-repo"
    commits:
      - id: "abc123"
        message: "Test commit"
        author:
          name: "Test User"
```

### Webhook Debugging

```yaml
debugging:
  tools:
    - name: "Request Bin"
      url: "https://requestbin.com"
      use: "Capture and inspect payloads"
      
    - name: "ngrok"
      command: "ngrok http 3000"
      use: "Expose local server"
      
    - name: "Webhook.site"
      url: "https://webhook.site"
      use: "Quick webhook testing"
      
  logging:
    enabled: true
    log_payloads: true
    log_headers: true
    mask_secrets: true
```

## Security Best Practices

### Security Checklist

```yaml
security:
  authentication:
    - Verify webhook signatures
    - Use HTTPS only
    - Rotate secrets regularly
    
  validation:
    - Validate payload schema
    - Check timestamp freshness
    - Verify source IP if possible
    
  processing:
    - Idempotent handlers
    - Rate limiting
    - Timeout protection
    
  storage:
    - Encrypt secrets at rest
    - Audit logging
    - No sensitive data in URLs
```

### IP Allowlisting

```yaml
ip_allowlist:
  stripe:
    - "3.18.12.63"
    - "3.130.192.231"
    # ... more IPs
    
  github:
    - "192.30.252.0/22"
    - "185.199.108.0/22"
    # ... more ranges
    
  slack:
    - "54.159.240.0/22"
    # ... more ranges
```

## Monitoring

### Metrics Dashboard

```
WEBHOOK METRICS - LAST 24 HOURS
═══════════════════════════════════════

Received:      12,456
Processed:     12,398 (99.5%)
Failed:           58 (0.5%)
Retried:         123

BY SOURCE:
Stripe     ████████████░░░░ 5,230
GitHub     ██████████░░░░░░ 4,120
Slack      ████░░░░░░░░░░░░ 1,850
Other      ███░░░░░░░░░░░░░ 1,256

LATENCY (p99):
Processing: 245ms
Response:   52ms

ERROR BREAKDOWN:
Timeout:       25
Invalid Sig:   18
Parse Error:   10
Rate Limited:   5
```

## Best Practices

1. **Respond Quickly**: Return 200 immediately, process async
2. **Idempotency**: Handle duplicate events gracefully
3. **Verify Signatures**: Always validate webhook authenticity
4. **Log Everything**: Maintain audit trail
5. **Retry Logic**: Implement exponential backoff
6. **Dead Letters**: Don't lose failed events
7. **Rate Limiting**: Protect against flood attacks
8. **Monitoring**: Alert on failures and latency
