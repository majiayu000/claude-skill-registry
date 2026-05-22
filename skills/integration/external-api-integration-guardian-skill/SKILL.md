---
name: external-api-integration-guardian
description: Validates external API integrations before deployment. Prevents SDK method usage errors, API signature mismatches, wrong endpoint URLs, sandbox vs production mode issues, and breaking API changes. Use before integrating CloudConvert, PayFast, Stripe, or any external API. Based on real CloudConvert SDK and PayFast signature production failures.
---

# External API Integration Guardian

**Mission:** Prevent external API integration failures by validating SDK methods exist, testing API signatures independently, verifying endpoint URLs, checking sandbox vs production mode, and detecting breaking API changes before they reach production.

**Historical Context**: Created after CloudConvert SDK download() method didn't exist (Oct 2025) and PayFast signature mismatch caused 100% payment failure (Nov 5, 2025).

---

## Activation Triggers

- **MANDATORY: Before integrating ANY external API**
- Writing code that calls external APIs
- Using SDK methods from external libraries
- Signature generation for payment APIs
- Switching from sandbox to production mode
- Updating SDK versions
- API returning 401/403 errors
- "Method does not exist" TypeScript errors
- Signature mismatch errors
- External API integration failing in production

---

## 🔴 CRITICAL: SDK Method Validation (NON-NEGOTIABLE)

**Production Lesson Learned**: CloudConvert SDK `download()` method doesn't exist in official API. Using it caused all conversions to fail with "Download not available" errors.

### Rule 1: NEVER Assume SDK Methods Exist

**Validation Checklist (BEFORE writing code):**

```bash
# Step 1: Check official API documentation
□ Load official SDK documentation
□ Search for method you plan to use
□ Verify method exists in current SDK version
□ Check method signature and parameters
□ Verify return type matches your expectations

# Step 2: Check SDK source code
□ Open node_modules/@sdk-name/...
□ Search for method definition
□ Verify method is exported
□ Check TypeScript types if available

# Step 3: Test method in Node REPL
□ node
□ const SDK = require('@sdk-name')
□ console.log(typeof SDK.methodName)
□ Should output: "function" (not "undefined")
```

**Real Production Issue (CloudConvert - Oct 2025):**

```typescript
// ❌ BROKEN: Method doesn't exist in SDK
import CloudConvert from 'cloudconvert'

const cloudconvert = new CloudConvert(API_KEY)
const job = await cloudconvert.jobs.wait(jobId)

// Attempt to download using SDK method
const download = await job.download()  // ❌ Method doesn't exist
const stream = cloudconvert.download(download.url)  // ❌ Method doesn't exist

// Error: Property 'download' does not exist on type 'Job'
// Result: All conversions failing - "Download not available"

// ✅ FIXED: Use native Node.js https.get()
import https from 'https'
import fs from 'fs'

const job = await cloudconvert.jobs.wait(jobId)
const exportTask = job.tasks.find(t => t.operation === 'export/url')
const fileUrl = exportTask.result.files[0].url  // HTTPS URL from CloudConvert

// Download using native Node.js (always works)
await new Promise((resolve, reject) => {
  https.get(fileUrl, (response) => {
    const fileStream = fs.createWriteStream(outputPath)
    response.pipe(fileStream)
    fileStream.on('finish', () => {
      fileStream.close()
      resolve(outputPath)
    })
  }).on('error', reject)
})

// Result: Downloads working correctly
```

---

## SDK Method Validation Process

### Step 1: Documentation Review

**Before using ANY SDK method:**

```bash
# 1. Find official documentation
https://cloudconvert.com/api/v2/start
https://developers.payfast.co.za/docs#step_1_form_fields

# 2. Search for method in docs
Ctrl+F "download"
Ctrl+F "signature"

# 3. If method not in docs → Probably doesn't exist or is deprecated
```

### Step 2: SDK Source Code Inspection

```bash
# Open SDK source code
cd node_modules/@sentry/node
grep -r "startTransaction" .

# If found → Check if it's exported
# If not found → Method doesn't exist, use alternative

# Check TypeScript definitions
cat node_modules/@sentry/node/build/types/index.d.ts | grep startTransaction
```

### Step 3: Runtime Method Existence Check

```typescript
// Before using method, check if it exists
if (typeof Sentry.startTransaction === 'function') {
  // Safe to use
  const transaction = Sentry.startTransaction(...)
} else {
  // Method doesn't exist - use alternative
  console.warn('Sentry.startTransaction not available, using breadcrumbs')
  Sentry.addBreadcrumb(...)
}
```

### Step 4: Fallback to Native APIs

**Always have a fallback for critical operations:**

```typescript
// CloudConvert Example: Download fallback
const downloadFile = async (url: string, outputPath: string) => {
  // Try SDK method first (if it exists)
  if (typeof cloudconvert.download === 'function') {
    try {
      await cloudconvert.download(url, outputPath)
      return
    } catch (error) {
      console.warn('SDK download failed, using native fallback')
    }
  }

  // Fallback to native https.get() (always works)
  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      const fileStream = fs.createWriteStream(outputPath)
      response.pipe(fileStream)
      fileStream.on('finish', () => {
        fileStream.close()
        resolve(outputPath)
      })
    }).on('error', reject)
  })
}
```

---

## 🔴 CRITICAL: API Signature Validation (NON-NEGOTIABLE)

**Production Lesson Learned**: PayFast signature mismatch due to empty passphrase parameter caused 100% payment failure (Nov 5, 2025).

### Rule 2: Test Signatures BEFORE Integration

**Signature Testing Workflow:**

```bash
# Step 1: Read signature algorithm from docs
□ What hash algorithm? (MD5, SHA256, HMAC-SHA256)
□ What parameter ordering? (alphabetical, custom, specific)
□ What URL encoding? (spaces as +, %20, or unencoded)
□ Is passphrase/salt required?
□ Where does passphrase go? (appended, prepended, in params)

# Step 2: Generate test signature manually
□ Use known test data from API docs
□ Generate signature following exact algorithm
□ Compare with API's expected signature

# Step 3: Test with API's signature validator
□ Many payment APIs have signature validation endpoints
□ POST test data + signature
□ Verify API responds with "signature valid"

# Step 4: Test in production with real data
□ Generate signature from real payment data
□ Log parameter string BEFORE hashing
□ Compare with API's expected signature
□ Only deploy if signatures match 100%
```

**Real Production Issue (PayFast - Nov 5, 2025):**

```javascript
// ❌ BROKEN: Including empty passphrase
const generateSignature = (paymentData, passphrase) => {
  let paramString = Object.keys(paymentData)
    .sort()  // Alphabetical ordering
    .map(key => `${key}=${encodeURIComponent(paymentData[key])}`)
    .join('&')

  // Problem: Empty passphrase gets included
  if (passphrase) {  // Empty string is falsy, but "" != undefined
    paramString += `&passphrase=${passphrase}`
  }
  // Even though passphrase is "", truthy check may fail depending on how it's set
  // Result: &passphrase= gets appended → signature mismatch

  return crypto.createHash('md5').update(paramString).digest('hex')
}

// PayFast production doesn't use passphrase
const signature = generateSignature(paymentData, "")  // Empty passphrase
// Generated: a1b2c3d4e5f6 (with passphrase)
// Expected: c857dc1297ea380cd431307f75d42bea (without passphrase)
// Result: Signature mismatch - 100% payment failure

// ✅ FIXED: Exclude passphrase entirely in production
const generateSignature = (paymentData) => {
  let paramString = Object.keys(paymentData)
    .sort()  // Alphabetical ordering
    .map(key => `${key}=${encodeURIComponent(paymentData[key])}`)
    .join('&')

  // NO passphrase parameter for production

  return crypto.createHash('md5').update(paramString).digest('hex').toLowerCase()
}

const signature = generateSignature(paymentData)  // No passphrase
// Generated: c857dc1297ea380cd431307f75d42bea
// Expected: c857dc1297ea380cd431307f75d42bea
// Result: ✅ Signature match - payments working
```

---

## API Signature Generation Best Practices

### 1. Log Parameter String BEFORE Hashing

```typescript
const generateSignature = (paymentData) => {
  const paramString = Object.keys(paymentData)
    .sort()
    .map(key => `${key}=${paymentData[key]}`)
    .join('&')

  // ✅ CRITICAL: Log parameter string in development
  if (process.env.NODE_ENV === 'development') {
    console.log('[Signature] Parameter string:', paramString)
  }

  const signature = crypto.createHash('md5').update(paramString).digest('hex')

  // ✅ CRITICAL: Log signature in development
  if (process.env.NODE_ENV === 'development') {
    console.log('[Signature] Generated signature:', signature)
  }

  return signature
}
```

### 2. Test Against Known Values

```typescript
// Unit test for signature generation
describe('PayFast Signature', () => {
  it('generates correct signature for known data', () => {
    const testData = {
      merchant_id: '10000100',
      merchant_key: '46f0cd694581a',
      amount: '50.00',
      item_name: 'Test Product'
    }

    const signature = generateSignature(testData)

    // Expected signature from PayFast documentation
    const expected = 'c857dc1297ea380cd431307f75d42bea'

    expect(signature).toBe(expected)
  })
})
```

### 3. Signature Algorithm Documentation

**Document signature algorithm in code:**

```typescript
/**
 * Generates PayFast payment signature
 *
 * Algorithm:
 * 1. Sort keys alphabetically (a-z)
 * 2. URL encode values (spaces as +, not %20)
 * 3. Exclude empty values
 * 4. Join with &: key1=value1&key2=value2
 * 5. MD5 hash the string
 * 6. Convert to lowercase
 * 7. NO passphrase in production mode
 *
 * Example:
 * Input: { merchant_id: "123", amount: "50.00" }
 * String: amount=50.00&merchant_id=123
 * MD5: c857dc1297ea380cd431307f75d42bea
 *
 * @param paymentData Payment parameters
 * @returns MD5 signature (lowercase)
 */
const generateSignature = (paymentData: PaymentData): string => {
  // Implementation...
}
```

---

## 🔴 CRITICAL: Sandbox vs Production Mode Validation

### Rule 3: Verify Correct Mode Before Deployment

**Mode Validation Checklist:**

```bash
# Development/Staging (Sandbox Mode)
□ CLOUDCONVERT_SANDBOX=true
□ PAYFAST_MODE=sandbox
□ PAYFAST_MERCHANT_ID=10000100 (sandbox ID)
□ API endpoints use sandbox URLs
□ Test credit cards work

# Production (Live Mode)
□ CLOUDCONVERT_SANDBOX=false  # ✅ CRITICAL
□ PAYFAST_MODE=production  # ✅ CRITICAL
□ PAYFAST_MERCHANT_ID=25263515 (live merchant ID)
□ API endpoints use production URLs
□ Real payments processed
```

**Common Sandbox vs Production Errors:**

```typescript
// ❌ WRONG: Sandbox mode in production
if (process.env.CLOUDCONVERT_SANDBOX === 'true') {
  // Still using sandbox API in production!
  // Conversions will fail or be limited
}

// ❌ WRONG: Production credentials with sandbox endpoint
const PAYFAST_URL = 'https://sandbox.payfast.co.za'
// Using production merchant_id with sandbox URL → fails

// ✅ CORRECT: Environment-based configuration
const CLOUDCONVERT_SANDBOX = process.env.CLOUDCONVERT_SANDBOX === 'true'
const PAYFAST_URL = process.env.PAYFAST_MODE === 'production'
  ? 'https://www.payfast.co.za'
  : 'https://sandbox.payfast.co.za'
```

---

## API Endpoint URL Validation

### Rule 4: Verify Correct Endpoint URLs

**Common URL Issues:**

```typescript
// ❌ WRONG: Hardcoded sandbox URL
const API_URL = 'https://sandbox.api.com/v2'

// ❌ WRONG: Missing /v2 in endpoint
const API_URL = 'https://api.cloudconvert.com'
// Should be: https://api.cloudconvert.com/v2

// ❌ WRONG: HTTP instead of HTTPS
const API_URL = 'http://api.payfast.co.za'
// Should be: https://www.payfast.co.za

// ✅ CORRECT: Environment-based URL selection
const API_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.cloudconvert.com/v2'
  : 'https://api.sandbox.cloudconvert.com/v2'
```

**URL Validation Script:**

```bash
#!/bin/bash
# scripts/validate-api-urls.sh

echo "=== Validating API Endpoint URLs ==="

# Check CloudConvert API
curl -s -o /dev/null -w "%{http_code}" https://api.cloudconvert.com/v2/users/me \
  -H "Authorization: Bearer $CLOUDCONVERT_API_KEY"

if [ $? -eq 200 ]; then
  echo "✅ CloudConvert API: Accessible"
else
  echo "❌ CloudConvert API: Failed (check API key and URL)"
  exit 1
fi

# Check PayFast API
PAYFAST_URL="https://www.payfast.co.za/eng/query/validate"
curl -s -o /dev/null -w "%{http_code}" $PAYFAST_URL

if [ $? -eq 200 ]; then
  echo "✅ PayFast API: Accessible"
else
  echo "❌ PayFast API: Failed"
  exit 1
fi

echo "=== All API endpoints validated ==="
```

---

## Breaking API Changes Detection

### Rule 5: Monitor API Changelog Before Updating SDKs

**SDK Update Checklist:**

```bash
# Before updating SDK version
□ Read SDK changelog on GitHub
□ Check for BREAKING CHANGES section
□ Review deprecated methods
□ Check removed methods
□ Test updated SDK in development FIRST

# Common breaking changes
□ Method renamed (startTransaction → captureTransaction)
□ Method removed (download() removed entirely)
□ Parameter order changed
□ Return type changed
□ Authentication method changed
```

**Example: Sentry SDK v7 → v8 Breaking Changes**

```typescript
// Sentry v7 (Old)
const transaction = Sentry.startTransaction({
  op: 'batch.processing',
  name: 'Process Batch'
})
transaction.startChild({ op: 'conversion' })
transaction.finish()

// Sentry v8 (New) - startTransaction() removed
// ❌ Error: Property 'startTransaction' does not exist

// Use breadcrumbs instead
Sentry.addBreadcrumb({
  category: 'performance',
  message: 'Batch processing started',
  data: { operation: 'batch.processing' }
})
```

**How to Detect Breaking Changes:**

```bash
# Check SDK changelog
npm show @sentry/node versions  # List all versions
npm view @sentry/node@8.0.0 --json | jq .changelog

# Check GitHub releases
https://github.com/getsentry/sentry-javascript/releases

# Search for breaking changes
grep -i "breaking" CHANGELOG.md
grep -i "removed" CHANGELOG.md
grep -i "deprecated" CHANGELOG.md
```

---

## External API Integration Testing Strategy

### Phase 1: Documentation Review

```bash
□ Read official API documentation thoroughly
□ Understand authentication method
□ Note rate limits and quotas
□ Identify required vs optional parameters
□ Review error codes and meanings
□ Check for webhook requirements
```

### Phase 2: Independent Testing (Before Integration)

```bash
# Test API with curl (before writing code)
curl -X POST https://api.example.com/v2/resource \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# Expected: 200 OK with response
# If 401: API key issue
# If 403: Permission issue
# If 404: Wrong endpoint URL
```

### Phase 3: SDK Method Validation

```bash
# List all SDK methods
node -e "const SDK = require('@sdk-name'); console.log(Object.keys(SDK))"

# Test specific method exists
node -e "const SDK = require('@sdk-name'); console.log(typeof SDK.methodName)"
# Should output: "function" (not "undefined")
```

### Phase 4: Integration Testing

```typescript
// Test integration with mock data
describe('CloudConvert Integration', () => {
  it('converts PDF to DOCX', async () => {
    const result = await cloudconvert.convert(
      'test.pdf',
      'output.docx',
      'docx'
    )

    expect(result.status).toBe('completed')
    expect(fs.existsSync(result.outputPath)).toBe(true)
  })

  it('handles API errors gracefully', async () => {
    // Test with invalid API key
    const cloudconvertInvalid = new CloudConvert('invalid_key')

    await expect(
      cloudconvertInvalid.convert('test.pdf', 'output.docx', 'docx')
    ).rejects.toThrow('401')
  })
})
```

### Phase 5: Production Validation

```bash
# After deployment, test with real data
□ Make test API call with production credentials
□ Verify response is correct
□ Check response time is acceptable
□ Monitor error rate in first hour
□ Verify webhooks are received (if applicable)
```

---

## Common External API Pitfalls

### Pitfall 1: Trusting SDK Documentation Over Reality

**Problem**: SDK docs say method exists, but it doesn't
**Solution**: Always check source code and test in REPL

### Pitfall 2: Not Handling API Rate Limits

**Problem**: Making too many requests → 429 Too Many Requests
**Solution**: Implement rate limiting and exponential backoff

```typescript
const retryWithBackoff = async (fn, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (error.statusCode === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000  // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay))
      } else {
        throw error
      }
    }
  }
}
```

### Pitfall 3: Not Validating Webhook Signatures

**Problem**: Webhooks can be spoofed if signatures not validated
**Solution**: Always validate webhook signatures

```typescript
const validateWebhookSignature = (payload, signature, secret) => {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex')

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  )
}
```

### Pitfall 4: Assuming APIs Are Always Available

**Problem**: External APIs have downtime
**Solution**: Implement circuit breaker pattern

```typescript
class CircuitBreaker {
  private failureCount = 0
  private lastFailureTime = 0
  private readonly threshold = 5
  private readonly timeout = 60000  // 1 minute

  async call(fn) {
    if (this.isOpen()) {
      throw new Error('Circuit breaker is open')
    }

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  private isOpen() {
    return this.failureCount >= this.threshold &&
           Date.now() - this.lastFailureTime < this.timeout
  }

  private onSuccess() {
    this.failureCount = 0
  }

  private onFailure() {
    this.failureCount++
    this.lastFailureTime = Date.now()
  }
}
```

---

## Pre-Integration Checklist

**Before integrating ANY external API:**

- [ ] Read official API documentation completely
- [ ] Test API with curl/Postman before writing code
- [ ] Verify SDK methods exist (check source code)
- [ ] Test signature generation independently
- [ ] Check sandbox vs production mode requirements
- [ ] Verify endpoint URLs are correct
- [ ] Implement error handling for all API calls
- [ ] Implement rate limiting and retries
- [ ] Validate webhook signatures (if applicable)
- [ ] Test with production credentials in staging
- [ ] Monitor API changelog for breaking changes

---

## Key Principles

1. **Never assume SDK methods exist** - Always verify
2. **Test signatures independently** - Before full integration
3. **Use native fallbacks for critical operations** - Don't rely solely on SDKs
4. **Validate sandbox vs production mode** - Before every deployment
5. **Monitor API changelogs** - Breaking changes happen
6. **Test with real credentials before production** - In staging environment

---

## When to Escalate

- API has no official documentation
- SDK is unmaintained (last update >1 year ago)
- API requires complex OAuth flow
- API has no sandbox environment
- Webhook signature algorithm is unclear
- API rate limits are very restrictive
- API requires IP whitelisting
- Payment integration (PCI-DSS compliance required)

---

**Skill Version**: 1.0.0
**Created**: November 10, 2025
**Last Updated**: November 10, 2025
