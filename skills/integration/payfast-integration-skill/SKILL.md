---
name: payfast-integration
description: PayFast payment gateway integration specialist for FastAPI and Node.js. Use when debugging PayFast signature validation, ITN webhooks, sandbox-to-production migration, or implementing onsite/offsite/recurring billing. Covers MD5 signature generation, webhook security, PCI-DSS compliance, and production deployment checklists.
---

# PayFast Integration Specialist

Production-grade PayFast integration with systematic debugging workflows for FastAPI and Node.js applications.

## Diagnostic Interview

Before jumping to solutions, gather these critical details:

**Error Context:**
- Exact error message (include stack trace if available)
- When does it occur? (payment submission, ITN callback, signature validation)
- Environment: sandbox or production

**Integration Details:**
- Integration type: onsite, offsite, or recurring billing
- Framework: FastAPI or Node.js (which version?)
- Recent changes: code updates, PayFast dashboard settings, server migrations

**Configuration Status:**
- merchant_id and merchant_key verified against PayFast dashboard
- Passphrase set (required for recurring billing and signatures)
- Return/cancel/notify URLs publicly accessible (not localhost)

## Top 3 Failure Modes

### 1. MD5 Signature Mismatch

**Symptoms:**
- "Generated signature does not match" error
- Payment form rejected
- ITN validation fails

**⚠️ CRITICAL: PayFast Signature Requirements (NON-NEGOTIABLE)**

**Production Lesson Learned (Nov 5, 2025)**: PayFast signature mismatch caused 100% payment failure in production. Issue: empty passphrase was being included in signature generation when production mode doesn't use passphrases.

**Mandatory Signature Generation Steps:**

1. **✅ Sort keys alphabetically (a-z)** - EXACT alphabetical order required
2. **✅ URL encode values** - Spaces as `+`, not `%20`
3. **✅ Exclude empty values** - Do NOT include parameters with empty strings
4. **❌ NO passphrase in production mode** - Only use passphrase in sandbox if configured
5. **✅ MD5 hash the parameter string** - Use lowercase output

**Before vs After (Real Production Issue):**

```javascript
// ❌ WRONG: Including empty passphrase in production
const signature = generateSignature(paymentData, PAYFAST_CONFIG.passphrase);
// passphrase = "" gets included → signature mismatch

// ✅ CORRECT: No passphrase parameter in production
const signature = generateSignature(paymentData);
// Only actual payment parameters → signature valid
```

**Root Causes & Fixes:**

| Issue | Detection | Solution | Real Production Impact |
|-------|-----------|----------|----------------------|
| **Empty passphrase included** | Check if empty passphrase in signature params | Exclude passphrase entirely in production mode | ✅ **FIXED Nov 5** - 100% payment failure |
| **Wrong parameter order** | Compare param order to PayFast docs | Parameters MUST be alphabetically sorted (a-z) | Critical - always fails |
| **Trailing spaces in merchant_key** | Copy merchant_key, check length | Trim whitespace when storing credentials | Common copy-paste error |
| **Empty fields included** | Check for blank `value=""` fields | Exclude empty parameters from signature string | Causes intermittent failures |
| **Uppercase MD5 hash** | Check hash output casing | Use `.toLowerCase()` on hash | Always fails validation |
| **URL encoding inconsistent** | Special chars in item descriptions | Spaces as `+`, special chars URL encoded | Fails with special characters |

**Mandatory Pre-Integration Testing:**

```bash
# Step 1: Generate signature manually
□ Create parameter string with exact alphabetical order
□ Exclude empty values
□ Do NOT include passphrase in production
□ MD5 hash and convert to lowercase

# Step 2: Test with PayFast signature validator
□ Use PayFast's signature validation endpoint
□ Send test payment with known signature
□ Verify "Signature valid" response

# Step 3: Test with real payment amounts
□ Test with minimum amount (R5.00)
□ Test with decimal amounts (R85.50)
□ Test with large amounts (R1850.00)

# Step 4: Verify parameter ordering
□ Print parameter string before hashing
□ Confirm alphabetical order visually
□ Compare with PayFast documentation example
```

**Signature Validation Endpoint (for testing):**
```bash
# Test your signature generation
curl -X POST https://www.payfast.co.za/eng/query/validate \
  -d "merchant_id=YOUR_ID" \
  -d "signature=YOUR_GENERATED_SIGNATURE" \
  -d "amount=85.00"
```

**Verification Script:**
See `scripts/validate_signature.py` for standalone signature validator.

**Real Production Test Results (Nov 5, 2025):**
```
=== Before Fix ===
Generated Signature: a1b2c3d4e5f6 (with empty passphrase)
PayFast Expected: c857dc1297ea380cd431307f75d42bea
Result: ❌ Signature mismatch - 100% payment failure

=== After Fix ===
Generated Signature: c857dc1297ea380cd431307f75d42bea (no passphrase)
PayFast Expected: c857dc1297ea380cd431307f75d42bea
Result: ✅ Signatures match - payments working
```

### 2. ITN (Instant Transaction Notification) Webhook Failures

**Symptoms:**
- Payment succeeds but order not updated
- "ITN not received" in PayFast logs
- 307 redirect or non-200 response
- Empty `req.body` in webhook handler

**Root Causes & Fixes:**

| Issue | Detection | Solution |
|-------|-----------|----------|
| **Not returning 200 OK** | Check webhook logs for status code | Webhook MUST return `200` before any async processing |
| **notify_url redirects (307)** | Test URL with curl | Use exact URL (no trailing slash mismatch), ensure HTTPS |
| **localhost URL** | Check if notify_url uses localhost | Use ngrok/tunneling for dev or deploy to accessible server |
| **Body parsing middleware missing** | Check if `req.body` populated | FastAPI: use `Form(...)`, Node.js: `express.urlencoded()` |
| **Source IP not from PayFast** | Log incoming IP in webhook | Verify IP in PayFast ranges (see Security Checks below) |
| **Signature validation failing** | Log received vs computed signature | Apply same signature logic as payment submission |

**Advisory Security Checks:**
Consider implementing these ITN validations:
- Verify source IP belongs to PayFast (range: `197.97.145.144/28`)
- Validate signature matches received data
- Confirm payment amount matches order total
- Check payment status is `COMPLETE` before fulfilling order

**Testing Script:**
See `scripts/test_itn_endpoint.py` to simulate PayFast ITN callbacks.

### 3. Configuration & Environment Issues

**Symptoms:**
- Works in sandbox, fails in production
- "Invalid merchant_id or merchant_key"
- Recurring billing signature errors

**Root Causes & Fixes:**

| Issue | Detection | Solution |
|-------|-----------|----------|
| **Sandbox creds in production** | Check if merchant_id is 10000100 (sandbox) | Switch to live merchant_id and merchant_key from PayFast dashboard |
| **merchant_id vs merchant_key swapped** | Double-check credential assignment | merchant_id is numeric, merchant_key is alphanumeric |
| **Passphrase not set** | Check PayFast dashboard Settings | Required for recurring billing; set in Integration > Security |
| **Recurring billing not enabled** | Test subscription payment | Enable in PayFast dashboard Settings > Integrations |
| **CURL disabled on server** | Test: `curl --version` | Contact hosting provider to enable CURL/outbound requests |
| **Firewall blocks PayFast IPs** | Check server firewall logs | Whitelist PayFast IP ranges |

## Systematic Debugging Workflow

**Step 1: Isolate Failure Point**
- **Client-side?** Check browser console for JS errors, form submission logs
- **Server-side?** Check application logs for exceptions in payment initiation
- **Gateway?** Check PayFast dashboard transaction logs for rejection reason
- **Webhook?** Check ITN logs for delivery failures or 5xx errors

**Step 2: Verify Configuration**
Run this checklist:
```
□ merchant_id matches PayFast dashboard (case-sensitive)
□ merchant_key matches PayFast dashboard (no spaces)
□ Passphrase set in PayFast dashboard if using signatures
□ Environment matches credentials (sandbox vs production)
□ notify_url publicly accessible (test with curl)
□ return_url and cancel_url use HTTPS
```

**Step 3: Test Signature Generation**
Use `scripts/validate_signature.py` to:
- Generate reference signature from sample data
- Compare with your application's signature output
- Identify parameter ordering or encoding issues

**Step 4: Test Webhook Reception**
Use `scripts/test_itn_endpoint.py` to:
- Send mock ITN payload to your endpoint
- Verify 200 response returned immediately
- Check if order status updates correctly

**Step 5: Check Logs Systematically**
- **Application logs:** Exceptions, signature mismatches, validation errors
- **PayFast ITN logs:** Dashboard > Integrations > View ITN Log
- **Server access logs:** Confirm ITN POST requests arriving
- **Network traces:** Use browser DevTools or Wireshark for API calls

## Framework-Specific Patterns

**FastAPI:** See `references/fastapi-patterns.md` for:
- Pydantic models for payment requests
- Async webhook handlers
- Signature validation middleware
- Type-safe configuration management

**Node.js:** See `references/nodejs-patterns.md` for:
- Express route setup
- Body parsing middleware
- Signature generation utilities
- Error handling patterns

## Sandbox-to-Production Migration

**Repeatable Workflow:**

**Step 1: Export Sandbox Configuration**
```bash
# Document current working sandbox setup
□ merchant_id (sandbox): __________
□ merchant_key (sandbox): __________
□ Passphrase (if set): __________
□ Test transaction IDs: __________
□ Working notify_url pattern: __________
```

**Step 2: Update PayFast Dashboard (Production)**
- Navigate to Settings > Integration
- Set passphrase (copy from sandbox if consistent)
- Configure notify_url with production domain
- Enable recurring billing if needed
- Save and note new production credentials

**Step 3: Update Application Configuration**
```bash
□ Update merchant_id to production value
□ Update merchant_key to production value
□ Change API endpoint: sandbox.payfast.co.za → payfast.co.za
□ Update notify_url to production domain
□ Verify HTTPS certificate valid on all URLs
```

**Step 4: Validation Checklist**
```bash
□ Run scripts/validate_signature.py with production creds
□ Test small transaction (minimum amount)
□ Verify ITN callback received and processed
□ Check order status updates correctly
□ Confirm email notifications sent (if enabled)
□ Test edge cases: cancelled payment, failed payment
```

**Step 5: Monitoring Setup**
Consider implementing:
- Alert on ITN failures (non-200 responses)
- Log signature mismatches for analysis
- Track transaction completion rate
- Monitor webhook response times
- Set up PayFast dashboard email notifications

## Security Best Practices

**Advisory Recommendations:**

**PCI-DSS Compliance:**
- Never log full card numbers or CVV codes
- Use HTTPS for all payment-related endpoints
- Implement rate limiting on payment submission endpoints
- Store credentials in environment variables, not code

**Signature Validation:**
- Always validate ITN signatures before processing
- Use timing-safe comparison for signature checks
- Regenerate signature server-side; never trust client values

**Webhook Security:**
- Consider source IP validation (PayFast IPs only)
- Implement idempotency checks to prevent duplicate processing
- Return 200 immediately, process async to avoid timeouts
- Log all ITN payloads for audit trail

**Data Handling:**
- Validate amount precision (2 decimal places for ZAR)
- Check currency matches expected value (ZAR)
- Sanitize user input in item descriptions
- Use database transactions for order state updates

## Code Snippet Guidelines

When providing code examples:
- Include inline comments explaining PayFast-specific requirements
- Flag security risks explicitly (e.g., exposed keys, weak validation)
- Show error handling for network failures and signature mismatches
- Demonstrate idempotent webhook processing patterns
- Provide both sync and async examples where applicable

## Production Resilience

**Recommended Monitoring:**
- Webhook delivery success rate (target: >99%)
- Average ITN processing time (target: <500ms)
- Signature validation failure rate (investigate if >1%)
- Payment-to-order completion rate (identify drop-offs)

**Alerting Triggers:**
- Webhook returning non-200 status
- Repeated signature mismatches from same user
- ITN not received within 5 minutes of payment
- Unusual spike in failed transactions
