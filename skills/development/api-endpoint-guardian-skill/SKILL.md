---
name: api-endpoint-guardian
description: Prevents API endpoint failures through systematic design validation and error handling review. Use when adding new endpoints, debugging API errors, implementing authentication, or preparing for production deployment. Catches missing validation, inconsistent error responses, authentication gaps, rate limiting issues, and documentation problems.
---

# API Endpoint Guardian

**Mission:** Ensure API endpoints are secure, consistent, well-documented, and production-ready through offensive validation and best practice enforcement.

## Activation Triggers

- Adding new API endpoints
- API design reviews
- Authentication/authorization issues
- Error handling inconsistencies
- Rate limiting implementation
- API documentation needs
- Client integration errors
- Production API failures

## Framework Awareness

This skill understands:
- **Express.js** - Routing, middleware, error handling
- **TypeScript** - Type safety for requests/responses
- **REST** - Resource naming, HTTP methods, status codes
- **Authentication** - JWT, session, OAuth patterns
- **Validation** - Request/response schemas

## Scan Methodology

### 1. Initial Context Gathering

**Ask if not provided:**
- "Show me the new endpoint code (controller + route)"
- "What's the endpoint purpose?" (CRUD, action, query)
- "Who can access this?" (public, authenticated, admin)
- "What request/response formats are expected?"
- "Are there rate limits or quotas?"

### 2. Critical Endpoint Scan

Execute ALL checks in this section.

#### 🔴 CRITICAL: Route Definition & HTTP Method

**Historical Failure:** Used GET for delete action, browser prefetch deleted data

**Scan for:**
- [ ] HTTP method matches action (GET=read, POST=create, PUT/PATCH=update, DELETE=delete)
- [ ] Resource naming follows REST conventions (`/api/users/:id` not `/api/get-user`)
- [ ] Plural nouns for collections (`/api/batch/upload` → `/api/batches`)
- [ ] Nested resources show relationships (`/api/users/:userId/batches`)
- [ ] No verbs in URL (action in HTTP method, not path)

**Red flags:**
```typescript
// ❌ WRONG METHOD - Deletes on GET
router.get('/api/delete-user/:id', deleteUser)

// ❌ WRONG METHOD - Creates on GET
router.get('/api/create-job', createJob)

// ❌ VERB IN URL - Should be POST /api/users
router.post('/api/create-user', createUser)

// ❌ SINGULAR NOUN - Should be /api/batches
router.post('/api/batch/upload', uploadBatch)

// ❌ INCONSISTENT - Should nest under /api/batches/:id
router.get('/api/batch-status/:id', getBatchStatus)
```

**Optimization:**
```typescript
// ✅ CORRECT - Idempotent GET
router.get('/api/batches/:id', getBatchStatus)

// ✅ CORRECT - POST for creation
router.post('/api/batches', uploadBatch)

// ✅ CORRECT - DELETE for deletion
router.delete('/api/batches/:id', cancelBatch)

// ✅ CORRECT - Nested resource
router.get('/api/users/:userId/batches', getUserBatches)

// ✅ CORRECT - Resource naming
router.get('/api/batches/:id/download', downloadBatchZip)
```

#### 🔴 CRITICAL: Authentication & Authorization

**Historical Failure:** Forgot auth middleware, anyone could delete users

**Scan for:**
- [ ] Authentication middleware applied to protected routes
- [ ] Authorization checks for user-specific resources
- [ ] Admin-only routes have role/permission checks
- [ ] Public routes explicitly marked (no middleware = intentional?)
- [ ] User ID from token matches resource owner
- [ ] Guest access clearly defined

**Authentication Patterns:**
```typescript
// ❌ MISSING AUTH - Anyone can delete
router.delete('/api/batches/:id', cancelBatch)

// ❌ NO OWNERSHIP CHECK - User A can delete User B's batch
export const cancelBatch = async (req: Request, res: Response) => {
  const batch = await BatchJob.findByPk(req.params.id)
  await batch.destroy()  // No check if req.user.id === batch.user_id
}

// ✅ AUTH REQUIRED
router.delete('/api/batches/:id', authMiddleware, cancelBatch)

// ✅ OWNERSHIP VERIFICATION
export const cancelBatch = async (req: Request, res: Response) => {
  const batch = await BatchJob.findByPk(req.params.id)

  if (!batch) {
    return res.status(404).json({ error: 'Batch not found' })
  }

  if (batch.user_id !== req.user!.id) {
    return res.status(403).json({ error: 'Access denied' })
  }

  await batch.destroy()
}

// ✅ ADMIN ONLY
router.get('/api/admin/users', authMiddleware, requireAdmin, getUsers)

// ✅ PUBLIC (Explicitly documented)
// No auth required - PayFast webhook
router.post('/api/payfast/webhook', payfastWebhook)
```

#### 🔴 CRITICAL: CORS Configuration (PRODUCTION DEPLOYMENT MANDATORY)

**Historical Failure:** v1.1.1 hotfix (Nov 9, 2025) - CORS missing production domain caused 100% authentication failure for 15 minutes

**Production Lesson Learned**: Deployed to production without including production domain (https://pdflab.pro) in CORS origins. All API calls from frontend were blocked with "Not allowed by CORS" error. Required emergency hotfix v1.1.1.

**⚠️ MANDATORY: CORS Pre-Deployment Checklist (NON-NEGOTIABLE)**

**Before ANY Production Deployment:**
```bash
# Step 1: List ALL CORS origins in server.ts
□ localhost:3000 (development)
□ localhost:3002 (alternative dev port)
□ https://pdflab.pro (PRODUCTION - MANDATORY)
□ http://pdflab.pro (production HTTP fallback)
□ https://staging.pdflab.pro (staging - if exists)

# Step 2: Verify CORS configuration code
□ Check CORS_ORIGIN environment variable includes production domain
□ Verify CORS middleware applied BEFORE routes
□ Test CORS preflight OPTIONS requests
□ Check CORS credentials setting matches frontend

# Step 3: Test from production domain BEFORE deployment
□ Use browser DevTools → Network tab
□ Check for "Access-Control-Allow-Origin" header in response
□ Verify no CORS errors in console
□ Test API call from https://pdflab.pro

# Step 4: Production verification (AFTER deployment)
□ Open https://pdflab.pro in browser
□ Try login from production domain
□ Check Network tab for CORS errors
□ Verify API calls succeed (not 500 errors)
```

**Real Production Issue (Nov 9, 2025):**
```typescript
// ❌ BROKEN: Missing production domain (v1.1.0)
const corsOrigins = process.env['CORS_ORIGIN']?.split(',') || [
  'http://localhost:3000',
  'http://localhost:3002'
  // Missing: 'https://pdflab.pro'
]

app.use(cors({
  origin: (origin, callback) => {
    if (corsOrigins.includes(origin) || process.env.NODE_ENV === 'development') {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))  // ← Blocks production!
    }
  }
}))

// Result: 100% authentication failure in production
// Error: "Error: Not allowed by CORS" (500 status)
// Impact: All users blocked for 15 minutes until v1.1.1 hotfix

// ✅ FIXED: Production domains included (v1.1.1)
const corsOrigins = process.env['CORS_ORIGIN']?.split(',') || [
  'http://localhost:3000',
  'http://localhost:3002',
  'https://pdflab.pro',      // ← MANDATORY for production
  'http://pdflab.pro'        // ← HTTP fallback
]

app.use(cors({
  origin: (origin, callback) => {
    if (corsOrigins.includes(origin)) {
      callback(null, true)
    } else {
      console.warn(`[CORS] Blocked request from origin: ${origin}`)
      callback(new Error('Not allowed by CORS'))
    }
  },
  credentials: true  // If using cookies/auth headers
}))

// Result: Production working, authentication successful
```

**CORS Testing Commands:**
```bash
# Test CORS from production domain
curl -H "Origin: https://pdflab.pro" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type,Authorization" \
     -X OPTIONS \
     https://pdflab.pro/api/auth/login

# Expected response headers:
Access-Control-Allow-Origin: https://pdflab.pro
Access-Control-Allow-Methods: GET,POST,PUT,DELETE
Access-Control-Allow-Headers: Content-Type,Authorization
Access-Control-Allow-Credentials: true

# If missing → CORS NOT CONFIGURED CORRECTLY
```

#### 🔴 CRITICAL: Express Trust Proxy (PRODUCTION DEPLOYMENT MANDATORY)

**Historical Failure:** v1.1.1 hotfix (Nov 9, 2025) - Trust proxy not enabled caused rate limiter ValidationError

**Production Lesson Learned**: Production uses Nginx reverse proxy, but Express `trust proxy` setting was false. This caused express-rate-limit to throw ValidationError because X-Forwarded-For header was set but Express didn't trust it. Rate limiting broken in production.

**⚠️ MANDATORY: Trust Proxy Configuration (NON-NEGOTIABLE for Production)**

**Before ANY Deployment Behind Reverse Proxy (Nginx/Apache/CloudFlare):**
```typescript
// Step 1: Enable trust proxy IMMEDIATELY after creating Express app
const app = express()
const PORT = parseInt(process.env.PORT || '3006')

// ✅ CRITICAL: Enable trust proxy for production (behind Nginx)
app.set('trust proxy', true)  // ← MANDATORY for reverse proxy deployments

// Step 2: Verify rate limiting works
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  // Now works correctly with X-Forwarded-For header
})

app.use('/api/', apiLimiter)
```

**Real Production Issue (Nov 9, 2025):**
```typescript
// ❌ BROKEN: Trust proxy not enabled (v1.1.0)
const app = express()
// Missing: app.set('trust proxy', true)

// Rate limiter fails with:
// ValidationError: The 'X-Forwarded-For' header is set but the Express
// 'trust proxy' setting is false

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
})
app.use('/api/', apiLimiter)  // ← Throws ValidationError in production

// Result: Rate limiting broken, misleading client IPs in logs
// Nginx sets X-Forwarded-For header, but Express doesn't trust it

// ✅ FIXED: Trust proxy enabled (v1.1.1)
const app = express()
app.set('trust proxy', true)  // ← ADDED - Now trusts Nginx headers

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
})
app.use('/api/', apiLimiter)  // ← Now works correctly

// Result: Rate limiting working, correct client IPs logged
```

**Trust Proxy Checklist:**
```bash
# Step 1: Identify if behind reverse proxy
□ Using Nginx? → Requires trust proxy
□ Using Apache? → Requires trust proxy
□ Using CloudFlare? → Requires trust proxy
□ Using AWS ALB/ELB? → Requires trust proxy
□ Direct to internet? → Do NOT enable trust proxy

# Step 2: Verify X-Forwarded headers
curl -I https://pdflab.pro/api/health
# Check for: X-Forwarded-For, X-Forwarded-Proto, X-Forwarded-Host

# Step 3: Test rate limiting works
for i in {1..10}; do
  curl https://pdflab.pro/api/health
done
# Should work without ValidationError

# Step 4: Verify correct client IPs in logs
docker logs pdflab-backend-prod | grep "IP:"
# Should show real client IPs, not proxy IP
```

**Production Deployment Checklist (CORS + Trust Proxy):**
- [ ] CORS origins include production domain(s)
- [ ] Trust proxy enabled if behind Nginx/Apache/CloudFlare
- [ ] Test API call from production domain BEFORE deployment
- [ ] Verify rate limiting works in production
- [ ] Check browser DevTools Network tab for CORS errors
- [ ] Monitor logs for "Not allowed by CORS" warnings
- [ ] Verify X-Forwarded-For headers trusted correctly

#### 🔴 CRITICAL: Request Validation

**Historical Failure:** Missing file validation allowed 10GB upload, crashed server

**Scan for:**
- [ ] Required fields validated (401 if missing)
- [ ] Data types validated (string, number, enum)
- [ ] File uploads validated (size, type, count)
- [ ] Enum values validated against allowed list
- [ ] Input sanitization for XSS/injection
- [ ] Array/object structure validation

**Validation Patterns:**
```typescript
// ❌ NO VALIDATION - Accepts anything
export const uploadBatch = async (req: Request, res: Response) => {
  const files = req.files
  const operationType = req.body.operation_type
  // No checks - could be undefined, wrong type, etc.
}

// ✅ COMPREHENSIVE VALIDATION
export const uploadBatch = async (req: Request, res: Response) => {
  // 1. File validation
  const files = req.files as Express.Multer.File[]
  if (!files || files.length === 0) {
    return res.status(400).json({
      error: 'No files uploaded',
      message: 'Please provide at least one file'
    })
  }

  // 2. Enum validation
  const operation_type = req.body.operation_type as BatchOperationType
  if (!Object.values(BatchOperationType).includes(operation_type)) {
    return res.status(400).json({
      error: 'Invalid operation type',
      message: 'Operation type must be one of: convert, compress, merge'
    })
  }

  // 3. Count validation
  const maxBatchSize = req.user!.getMaxBatchSize()
  if (files.length > maxBatchSize) {
    return res.status(400).json({
      error: 'Too many files',
      message: `Your ${req.user!.plan} plan supports up to ${maxBatchSize} files`,
      upgrade_required: true
    })
  }

  // 4. File size validation
  const maxFileSize = req.user!.getMaxFileSize()
  const oversizedFile = files.find(file => file.size > maxFileSize)
  if (oversizedFile) {
    return res.status(413).json({
      error: 'File too large',
      file_name: oversizedFile.originalname,
      file_size: oversizedFile.size,
      max_file_size: maxFileSize
    })
  }
}

// ✅ TYPE VALIDATION with Zod (recommended)
import { z } from 'zod'

const uploadBatchSchema = z.object({
  operation_type: z.enum(['convert', 'compress', 'merge']),
  batch_name: z.string().optional(),
  output_format: z.enum(['pptx', 'docx', 'xlsx', 'png']).optional(),
  compression_level: z.enum(['good', 'recommended', 'extreme']).optional()
})

export const uploadBatch = async (req: Request, res: Response) => {
  // Validate with Zod
  const validation = uploadBatchSchema.safeParse(req.body)
  if (!validation.success) {
    return res.status(400).json({
      error: 'Validation failed',
      details: validation.error.errors
    })
  }

  const { operation_type, batch_name } = validation.data
}
```

#### 🟡 HIGH: Error Response Consistency

**Historical Issue:** Some endpoints returned strings, some objects, broke client parsing

**Scan for:**
- [ ] Consistent error format across all endpoints
- [ ] HTTP status codes match error type (400=bad request, 401=unauthorized, 403=forbidden, 404=not found, 500=server error)
- [ ] Error messages are user-friendly
- [ ] Error responses include helpful context
- [ ] Stack traces NOT exposed in production

**Error Response Standard:**
```typescript
// ❌ INCONSISTENT
res.status(400).send('Bad request')  // String
res.status(404).json({ error: 'Not found' })  // Object
res.status(500).json({ message: 'Error', code: 500 })  // Different format

// ✅ CONSISTENT - Always same shape
interface ErrorResponse {
  error: string           // Short error type
  message: string         // User-friendly message
  details?: any          // Additional context
  upgrade_required?: boolean
  cta?: { text: string, url: string }
}

// Example usage:
res.status(400).json({
  error: 'Invalid file type',
  message: 'Only PDF files are supported',
  details: { uploaded_type: 'image/jpeg', supported_types: ['application/pdf'] }
})

res.status(401).json({
  error: 'Authentication required',
  message: 'Please log in to access this feature',
  cta: { text: 'Log In', url: '/login' }
})

res.status(413).json({
  error: 'File too large',
  message: `Your ${user.plan} plan supports files up to ${maxSizeMB}MB`,
  upgrade_required: true,
  cta: { text: 'Upgrade Plan', url: '/pricing' }
})
```

**Status Code Guide:**
- `200 OK` - Success with response body
- `201 Created` - Resource created (return resource)
- `204 No Content` - Success with no response body
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict (duplicate email)
- `413 Payload Too Large` - File/request too big
- `422 Unprocessable Entity` - Semantic validation error
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Unexpected server error
- `503 Service Unavailable` - Temporarily unavailable

#### 🟡 HIGH: Response Format Consistency

**Scan for:**
- [ ] Success responses follow consistent structure
- [ ] List endpoints include pagination metadata
- [ ] Timestamps in ISO 8601 format
- [ ] IDs are strings (UUIDs) not numbers
- [ ] Nested objects use consistent naming (snake_case or camelCase)

**Response Patterns:**
```typescript
// ✅ SINGLE RESOURCE
res.status(200).json({
  batch_id: '123e4567-e89b-12d3-a456-426614174000',
  batch_name: 'My Batch',
  status: 'processing',
  progress: 60,
  created_at: '2025-11-09T10:30:00Z'
})

// ✅ LIST WITH PAGINATION
res.status(200).json({
  batches: [
    { batch_id: '...', batch_name: '...' },
    { batch_id: '...', batch_name: '...' }
  ],
  pagination: {
    page: 1,
    limit: 20,
    total: 45,
    total_pages: 3
  }
})

// ✅ CREATION RESPONSE (201)
res.status(201).json({
  message: 'Batch created successfully',
  batch_id: '123e4567-e89b-12d3-a456-426614174000',
  status: 'pending',
  conversion_job_ids: ['...', '...'],
  created_at: '2025-11-09T10:30:00Z'
})
```

#### 🟠 MEDIUM: Rate Limiting

**Scan for:**
- [ ] Rate limits applied to expensive operations
- [ ] Different limits for auth vs guest users
- [ ] Rate limit headers returned (X-RateLimit-Limit, X-RateLimit-Remaining)
- [ ] 429 status code when rate limited
- [ ] Retry-After header included

**Rate Limiting Patterns:**
```typescript
import rateLimit from 'express-rate-limit'

// ✅ GLOBAL RATE LIMIT
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests',
    message: 'Please try again later',
    retry_after: 900 // seconds
  },
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false
})

app.use('/api/', apiLimiter)

// ✅ ENDPOINT-SPECIFIC LIMIT
const uploadLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 10, // 10 uploads per hour
  message: {
    error: 'Upload limit exceeded',
    message: 'You can upload 10 batches per hour on your plan',
    upgrade_required: true
  }
})

router.post('/api/batches', authMiddleware, uploadLimiter, uploadBatch)

// ✅ USER-BASED RATE LIMIT
const getUserRateLimit = (user: User) => {
  switch (user.plan) {
    case 'free': return 10
    case 'starter': return 50
    case 'pro': return 200
    case 'enterprise': return 1000
  }
}
```

#### 🟠 MEDIUM: Documentation

**Scan for:**
- [ ] JSDoc comments on all public endpoints
- [ ] Request/response types documented
- [ ] Authentication requirements documented
- [ ] Example requests included
- [ ] Error responses documented

**Documentation Pattern:**
```typescript
/**
 * Upload multiple files for batch processing
 *
 * @route POST /api/batches
 * @access Private (requires authentication)
 * @ratelimit 10 uploads per hour
 *
 * @body {File[]} files - 2-50 PDF files (plan-dependent)
 * @body {string} operation_type - 'convert' | 'compress' | 'merge'
 * @body {string} [batch_name] - Optional custom name
 * @body {string} [output_format] - Required if operation_type='convert'
 * @body {string} [compression_level] - Required if operation_type='compress'
 *
 * @returns {201} Batch created successfully
 * @returns {400} Validation error
 * @returns {401} Not authenticated
 * @returns {413} File too large
 * @returns {429} Rate limit exceeded
 *
 * @example
 * const formData = new FormData()
 * formData.append('files', file1)
 * formData.append('files', file2)
 * formData.append('operation_type', 'convert')
 * formData.append('output_format', 'pptx')
 *
 * fetch('/api/batches', {
 *   method: 'POST',
 *   headers: { 'Authorization': `Bearer ${token}` },
 *   body: formData
 * })
 */
export const uploadBatch = async (req: Request, res: Response) => {
  // Implementation
}
```

### 3. Production Pre-Flight Checklist

Before deploying new endpoints:

**Security:**
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks for user-specific resources
- [ ] Input validation prevents injection attacks
- [ ] File uploads validated and sanitized
- [ ] Secrets not logged or returned in responses
- [ ] CORS configured correctly

**Performance:**
- [ ] Database queries optimized (use EXPLAIN)
- [ ] Pagination for list endpoints
- [ ] Rate limiting applied
- [ ] Large operations run async (batch processing)
- [ ] Caching strategy defined

**Reliability:**
- [ ] Error handling for all failure modes
- [ ] Graceful degradation if dependencies fail
- [ ] Timeout handling for long operations
- [ ] Retry logic for transient failures
- [ ] Rollback strategy for partial failures

**Monitoring:**
- [ ] Logging at info/warn/error levels
- [ ] Metrics tracked (request count, duration, errors)
- [ ] Alerting configured for error rates
- [ ] Performance baselines established

### 4. Common API Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| "Cannot set headers after sent" | Calling `res.json()` twice | Use `return res.json()` to exit function |
| "User is not authenticated" | Missing auth middleware | Add `authMiddleware` to route |
| "Cannot read property 'id' of undefined" | `req.user` undefined | Check `req.user` exists before accessing |
| "Validation error" | Missing required field | Add validation before processing |
| "Too many requests" | Rate limit exceeded | Implement exponential backoff on client |
| "CORS error" | Origin not allowed | Add origin to CORS whitelist |

### 5. API Versioning Strategy

**When to version:**
- Breaking changes to request/response format
- Removing fields
- Changing data types
- Renaming endpoints

**Versioning Patterns:**
```typescript
// ✅ URL VERSIONING (Recommended for REST)
router.post('/api/v1/batches', uploadBatch)
router.post('/api/v2/batches', uploadBatchV2)  // Breaking changes

// ✅ HEADER VERSIONING
app.use((req, res, next) => {
  const version = req.headers['api-version'] || 'v1'
  req.apiVersion = version
  next()
})

// ✅ DEPRECATION WARNING
res.set('X-API-Deprecated', 'true')
res.set('X-API-Sunset', '2026-01-01')
res.json({
  warning: 'This endpoint is deprecated. Use /api/v2/batches instead.',
  sunset_date: '2026-01-01'
})
```

## Output Format: Auto-Scan Report

```
═══════════════════════════════════════════════
🛡️ API ENDPOINT GUARDIAN - SCAN RESULTS
═══════════════════════════════════════════════

📊 SCAN SCOPE
• Endpoint: POST /api/batch/upload
• Controller: uploadBatchFiles
• Authentication: Required
• Rate Limit: None configured

🚨 CRITICAL FINDINGS: 2
1. Authentication not verified in controller
   • Risk: Bypass possible if middleware removed
   • Fix: Add `if (!req.user) return res.status(401)...`

2. No file count validation
   • Risk: Upload 1000 files, crash server
   • Fix: Check files.length against plan limits

⚠️  HIGH PRIORITY: 3
1. Inconsistent error responses
   • Some return strings, some objects
   • Fix: Standardize to { error, message, details }

2. No rate limiting
   • Risk: API abuse, DDoS vulnerability
   • Fix: Add uploadLimiter middleware

3. Missing request validation
   • operation_type not validated against enum
   • Fix: Use Zod schema validation

💡 OPTIMIZATIONS: 4
1. Add JSDoc documentation
2. Return 201 Created instead of 200 OK
3. Include batch_id in response headers (Location)
4. Add pagination to batch history endpoint

═══════════════════════════════════════════════
API DESIGN SCORE: 7/10
═══════════════════════════════════════════════
✅ HTTP method correct (POST for creation)
✅ Authentication middleware applied
⚠️  Missing ownership verification
⚠️  No rate limiting
❌ Request validation incomplete
❌ Error responses inconsistent

PRODUCTION READINESS: BLOCKED
Critical issues must be resolved before deployment

NEXT ACTIONS:
1. Add file count validation
2. Verify req.user exists in controller
3. Standardize error response format
4. Add rate limiting middleware

═══════════════════════════════════════════════
```

## Quick Reference: Middleware Order

```typescript
// ✅ CORRECT ORDER
router.post(
  '/api/batches',
  cors(),                          // 1. CORS first
  apiLimiter,                      // 2. Rate limiting
  authMiddleware,                  // 3. Authentication
  requirePermission('batch.create'), // 4. Authorization
  upload.array('files', 50),       // 5. File upload
  validateRequest(uploadSchema),   // 6. Validation
  uploadBatch                      // 7. Controller
)

// ❌ WRONG ORDER - Auth after validation (security gap)
router.post('/api/batches',
  validateRequest(uploadSchema),  // Processes untrusted input first!
  authMiddleware,
  uploadBatch
)
```

## Key Principles

1. **Fail fast** - Validate early, return errors immediately
2. **Consistent errors** - Always same format
3. **Auth first** - Check authentication before anything else
4. **Validate everything** - Never trust client input
5. **Document thoroughly** - Future you will thank you
6. **Version carefully** - Breaking changes need new version
7. **Monitor everything** - You can't fix what you can't see

## When to Escalate

- Complex authorization rules (RBAC, ABAC)
- GraphQL endpoint design
- Websocket API patterns
- Microservices communication
- API gateway configuration
- OAuth/SSO integration
