---
name: full-stack-integration-guardian
description: Detects and prevents frontend-backend integration issues including API response handling, type mismatches, null safety, and data transformation errors. Triggered when implementing new API endpoints, debugging API integration, or experiencing "Cannot read property of undefined" errors. Learns from real production incidents.
---

# Full-Stack Integration Guardian

**Mission:** Prevent frontend-backend integration failures through systematic validation of API contracts, data transformations, and type safety across the stack. This skill operates **proactively** - catching data flow issues before they cause runtime crashes.

## Activation Triggers

- User mentions "API not working" or "partners not showing"
- Frontend displaying blank/empty data despite successful API calls
- Console errors: `Cannot read property 'X' of undefined`
- TypeError: `X.toFixed is not a function` or similar
- API response structure mismatches
- Database DECIMAL/number type issues
- Implementing new backend-to-frontend data flow
- "Why is my data null?"

## Critical Patterns from Production Incidents

### 🔴 INCIDENT 1: API Wrapper Response Access Pattern

**Historical Failure:** Frontend accessed `response.data.partners` but API wrapper (`api.get()`) already unwraps responses

**Symptoms:**
```javascript
console.log('[Partners] Response:', response)  // {partners: Array(4)}
console.log('[Partners] Response data:', response.data)  // undefined
console.log('[Partners] No partners in response')
```

**Root Cause:**
- Custom API wrapper (`lib/api.ts`) uses Axios but unwraps the response
- Developer assumed standard Axios pattern: `response.data.partners`
- Actual pattern: API wrapper returns `response.partners` directly

**Red Flags to Scan For:**
- [ ] Custom API client wrappers that modify response structure
- [ ] Frontend accessing `response.data.X` when wrapper already unwraps
- [ ] Console showing successful data but code treating it as undefined
- [ ] Working API calls (HTTP 200) but UI shows "No data"

**Detection Method:**
```typescript
// 1. Read the API client wrapper (lib/api.ts or similar)
// 2. Check if it unwraps response.data automatically:
class ApiClient {
  async get(url: string) {
    const response = await axios.get(url)
    return response.data  // ⚠️ This unwraps! Frontend should NOT use .data again
  }
}

// 3. Check frontend usage
const response = await api.get('/endpoint')
if (response.data.items) {  // ❌ WRONG - .data already unwrapped
  setItems(response.data.items)
}

// ✅ CORRECT
const response = await api.get('/endpoint')
if (response.items) {  // Direct access
  setItems(response.items)
}
```

**Fix Template:**
```typescript
// BEFORE (Broken)
const partnersResponse = await api.get('/partners/admin/all')
setPartners(partnersResponse.data.partners || [])  // ❌ response.data is undefined

// AFTER (Working)
const response = await api.get('/partners/admin/all')
if (response?.partners) {  // ✅ Direct access with null safety
  setPartners(response.partners)
} else {
  setPartners([])
}
```

**Lessons Learned:**
1. **Always check API wrapper implementation** before assuming standard Axios pattern
2. **Add debug logging** to see actual response structure
3. **Use null-safe access patterns** (`response?.items`)
4. **Document API client behavior** in comments

---

### 🔴 INCIDENT 2: Database DECIMAL Types Return as Strings

**Historical Failure:** Sequelize returns MySQL DECIMAL columns as strings, causing `.toFixed()` to fail in React

**Symptoms:**
```javascript
TypeError: partner.total_revenue.toFixed is not a function
// Even after null check:
TypeError: (partner.total_revenue || 0).toFixed is not a function
```

**Root Cause:**
- MySQL `DECIMAL(10,2)` columns return as `"0.00"` (string) through Sequelize
- Frontend calls `.toFixed(2)` assuming number type
- Null check `|| 0` doesn't help because string `"0.00"` is truthy

**Red Flags to Scan For:**
- [ ] Backend models with DECIMAL/FLOAT/NUMERIC columns
- [ ] Frontend using `.toFixed()`, `.toLocaleString()`, math operations
- [ ] No explicit type conversion in backend API response
- [ ] TypeScript types showing `number` but runtime values are strings

**Detection Method:**
```typescript
// 1. Check backend models for DECIMAL fields
// backend/src/models/Partner.ts
Partner.init({
  total_revenue: {
    type: DataTypes.DECIMAL(10, 2),  // ⚠️ Returns string!
  }
})

// 2. Check backend controller response
res.json({
  partners: partners.map(p => ({
    total_revenue: p.total_revenue,  // ❌ Still a string "0.00"
  }))
})

// 3. Check frontend usage
<p>${partner.total_revenue.toFixed(2)}</p>  // ❌ Crashes if string
```

**Fix Template:**

**Backend Fix (Preferred):**
```typescript
// backend/src/controllers/partner.controller.ts
res.status(200).json({
  partners: partners.map((partner) => ({
    id: partner.id,
    name: partner.name,
    total_revenue: parseFloat(partner.total_revenue_generated?.toString() || '0'),  // ✅
    total_commission_earned: parseFloat(partner.total_commission_earned?.toString() || '0'),
    pending_commission: parseFloat(partner.getPendingCommission()?.toString() || '0'),
    total_signups: partner.total_signups || 0,  // ✅ Already number
  }))
})
```

**Frontend Defensive Fix (Backup):**
```typescript
// app/admin/partners/page.tsx
<div>
  <p>Revenue</p>
  <p>${(Number(partner.total_revenue) || 0).toFixed(2)}</p>  {/* ✅ Convert first */}
</div>

// Or with type checking
<div>
  <p>Revenue</p>
  <p>${(typeof partner.total_revenue === 'string'
      ? parseFloat(partner.total_revenue)
      : partner.total_revenue || 0).toFixed(2)}</p>
</div>
```

**Lessons Learned:**
1. **Convert DECIMAL to numbers in backend** - single source of truth
2. **Never assume database types match TypeScript types**
3. **Test with real database data** - mock data won't reveal string types
4. **Add defensive frontend parsing** as backup layer
5. **Document type conversions** in API documentation

---

### 🟡 INCIDENT 3: Null/Undefined Fields Causing Rendering Crashes

**Historical Pattern:** Database returns null for optional fields, frontend doesn't handle gracefully

**Symptoms:**
```javascript
TypeError: Cannot read property 'name' of null
TypeError: partner.promo_codes.map is not a function  // null.map()
```

**Root Cause:**
- Database allows NULL for optional foreign keys
- Backend returns `null` instead of empty arrays/default values
- Frontend assumes all fields exist

**Red Flags to Scan For:**
- [ ] Database schema with nullable columns
- [ ] Backend not providing defaults for null values
- [ ] Frontend using `.map()`, `.filter()`, `.length` without null checks
- [ ] Optional chaining (`?.`) used inconsistently

**Fix Template:**

**Backend (Data Normalization):**
```typescript
// backend/src/controllers/partner.controller.ts
res.status(200).json({
  partners: partners.map((partner) => ({
    id: partner.id,
    name: partner.name || 'Unknown',  // ✅ Default string
    total_signups: partner.total_signups || 0,  // ✅ Default number
    promo_codes: partner.promo_codes?.map(c => c.code) || [],  // ✅ Default array
    conversion_rate: partner.getConversionRate()?.toFixed(2) + '%' || '0%',  // ✅ Safe call
  }))
})
```

**Frontend (Defensive Rendering):**
```typescript
// app/admin/partners/page.tsx
{partners.map((partner) => (
  <div key={partner.id}>
    <h3>{partner.name || 'Unknown Partner'}</h3>
    <p>Signups: {partner.total_signups || 0}</p>
    <p>Conversions: {partner.total_conversions || 0}</p>
    <p>Rate: {partner.conversion_rate || '0%'}</p>

    {/* Array handling */}
    {(partner.promo_codes || []).length > 0 && (
      <div>
        {partner.promo_codes.map(code => <span key={code}>{code}</span>)}
      </div>
    )}
  </div>
))}
```

**Lessons Learned:**
1. **Normalize data in backend** - frontend should receive clean data
2. **Use `|| defaultValue` pattern** for primitives (strings, numbers)
3. **Use `|| []` pattern** for arrays before `.map()`
4. **Use optional chaining** (`?.`) for nested objects
5. **Provide TypeScript types** that reflect actual nullability

---

## Systematic Scan Checklist

When implementing new backend-to-frontend data flow, validate **ALL** these checkpoints:

### 1. API Client Architecture
- [ ] Does project use a custom API client wrapper? (Check `lib/api.ts`, `services/api.ts`)
- [ ] Does wrapper unwrap `response.data` automatically?
- [ ] Are all frontend calls using correct access pattern?
- [ ] Is response structure documented?

### 2. Backend Data Types
- [ ] Identify all DECIMAL/FLOAT/NUMERIC database columns
- [ ] Check if backend converts them to actual numbers
- [ ] Verify boolean columns return `true`/`false` (not `1`/`0`)
- [ ] Ensure date columns are ISO strings or proper Date objects

### 3. Null Safety
- [ ] List all nullable database columns
- [ ] Verify backend provides defaults for null values
- [ ] Check frontend uses null-safe operators (`?.`, `||`)
- [ ] Ensure arrays default to `[]` not `null`

### 4. Type Consistency
- [ ] TypeScript interfaces match actual API response structure
- [ ] No `any` types in API response handling
- [ ] Frontend types match backend response types
- [ ] Shared type definitions if using monorepo

### 5. Error Handling
- [ ] Frontend catches API errors gracefully
- [ ] Loading states prevent rendering undefined data
- [ ] Empty states show when data is `[]` vs error vs loading
- [ ] Console errors provide actionable debugging info

### 6. Testing Strategy
- [ ] Test with real database data (not just mocks)
- [ ] Test with null/empty database values
- [ ] Test with edge cases (empty arrays, zero numbers)
- [ ] Console logging removed or behind debug flag

---

## Auto-Scan Report Template

When user asks "why isn't my data showing?" or you detect integration issues:

```
═══════════════════════════════════════════════
🔗 FULL-STACK INTEGRATION SCAN
═══════════════════════════════════════════════

📊 ANALYSIS SCOPE
• API Endpoint: /api/partners/admin/all
• Frontend: app/admin/partners/page.tsx
• Backend: backend/src/controllers/partner.controller.ts
• Database: partners table (MySQL)

🚨 CRITICAL ISSUES FOUND: [count]

❌ ISSUE 1: API Response Access Pattern Mismatch
   File: app/admin/partners/page.tsx:113
   Problem: Accessing response.data.partners but API wrapper unwraps response
   Evidence:
     console.log(response)  // {partners: Array(4)}
     console.log(response.data)  // undefined

   Impact: Frontend receives data but code treats as undefined

   Fix:
   - BEFORE: setPartners(partnersResponse.data.partners || [])
   - AFTER:  setPartners(response.partners || [])

   Affected Lines: page.tsx:113-123

❌ ISSUE 2: DECIMAL Type Returned as String
   File: backend/src/controllers/partner.controller.ts:368
   Problem: total_revenue_generated is DECIMAL, returns as "0.00" string
   Evidence: Frontend calls .toFixed() causing TypeError

   Database Schema:
     total_revenue_generated DECIMAL(10,2)  // ⚠️ Returns string!

   Fix:
   - Add: parseFloat(partner.total_revenue_generated?.toString() || '0')
   - Also fix: total_commission_earned, pending_commission

   Affected Fields: 3 DECIMAL columns

⚠️  WARNING: Null Safety Issues
   • promo_codes can be null, frontend uses .map()
   • conversion_rate calculation not null-safe
   • Recommendation: Add || [] for arrays, || 0 for numbers

💡 OPTIMIZATIONS:
   • Add TypeScript interfaces for API responses
   • Create shared types between frontend/backend
   • Add API response logging in development
   • Document API client wrapper behavior

═══════════════════════════════════════════════
INTEGRATION HEALTH: 6/10
═══════════════════════════════════════════════

🎯 ACTION PLAN:
1. Fix API response access pattern (5 min)
2. Convert DECIMAL types to numbers in backend (10 min)
3. Add null safety to array/number fields (15 min)
4. Remove debug console.log statements (5 min)
5. Test with real database edge cases

Estimated Fix Time: 35 minutes
Risk if not fixed: HIGH (users see blank pages)

═══════════════════════════════════════════════
```

---

## Prevention Strategies

### For New API Endpoints

**Backend Checklist:**
```typescript
// 1. Convert DECIMAL to numbers
const response = {
  revenue: parseFloat(record.revenue?.toString() || '0'),
  commission: parseFloat(record.commission?.toString() || '0'),
}

// 2. Provide defaults for nulls
const response = {
  name: record.name || 'Unknown',
  tags: record.tags || [],
  metadata: record.metadata || {},
}

// 3. Ensure consistent date format
const response = {
  created_at: record.created_at?.toISOString(),  // ISO 8601
}

// 4. Document response structure
/**
 * GET /api/partners/admin/all
 * Returns: { partners: Partner[] }
 * Partner shape: { id, name, total_revenue: number, ... }
 */
```

**Frontend Checklist:**
```typescript
// 1. Check API wrapper pattern
const response = await api.get('/endpoint')
console.log('[Debug] Response structure:', response)  // Temporarily

// 2. Use null-safe access
if (response?.items) {
  setItems(response.items)
}

// 3. Provide defaults
setRevenue((response.revenue || 0).toFixed(2))
setTags(response.tags || [])

// 4. Type the response
interface PartnerResponse {
  partners: Array<{
    id: string
    name: string
    total_revenue: number  // Not string!
    promo_codes: string[]  // Not null!
  }>
}
const response = await api.get<PartnerResponse>('/partners/admin/all')
```

---

## Quick Diagnostic Commands

```bash
# 1. Check API wrapper implementation
cat lib/api.ts | grep "response.data"

# 2. Find DECIMAL columns in models
grep -r "DECIMAL\|FLOAT\|NUMERIC" backend/src/models/

# 3. Find .toFixed() usage in frontend
grep -r "\.toFixed\|\.toLocaleString" app/ components/

# 4. Check for unsafe array access
grep -r "\.map\|\.filter" app/ | grep -v "|| \[\]"

# 5. Test API response structure
curl http://localhost:3006/api/endpoint | jq .
```

---

## Cross-Skill Integration

**When Database Migration Guardian is active:**
- Validate that DECIMAL columns are handled in API layer
- Flag nullable columns that need defaults in backend

**When React/Next.js Guardian is active:**
- Ensure components handle loading/error/empty states
- Validate TypeScript types match runtime data

**When API Endpoint Guardian is active:**
- Verify consistent response structure across endpoints
- Check error responses return expected format

---

## Key Principles

1. **Backend owns data normalization** - convert types, provide defaults
2. **Frontend defends against unexpected data** - null checks, type guards
3. **Always test with real database data** - mocks hide type mismatches
4. **Document API wrapper behavior** - prevent response.data confusion
5. **Use TypeScript strictly** - types should reflect reality
6. **Log response structure during development** - catch issues early

---

## Incident Response Protocol

When user reports "data not showing":

1. **Verify API call succeeds** (check Network tab, backend logs)
2. **Log actual response structure** (console.log full response)
3. **Check API wrapper implementation** (does it unwrap response.data?)
4. **Identify type mismatches** (DECIMAL as string, null as number)
5. **Apply fixes in order**: Backend normalization → Frontend defense
6. **Remove debug logging** after fix confirmed

**Response Time Target:** 30-45 minutes from report to fix

---

## Success Metrics

✅ **Integration is healthy when:**
- API calls return HTTP 200 AND data displays in UI
- No "Cannot read property" errors in console
- No TypeError for .toFixed(), .map(), etc.
- Real database nulls/zeros handled gracefully
- Frontend types match backend response structure
- Debug logging present only in development

❌ **Integration needs attention when:**
- Successful API calls but blank UI
- Console shows data structure but code accesses wrong path
- Type errors on number methods (.toFixed, Math operations)
- Crashes when database returns null
- TypeScript types don't match runtime data

---

## 🔴 INCIDENT 4: Double API Prefix Bug (Nov 2024)

**Real Production Incident:** Partner Applications page showed "No pending applications found" despite database having 10 applications.

**Symptoms:**
```typescript
// Frontend successfully called API
const response = await api.get('/api/partner-applications?status=pending')

// Backend logs showed ZERO incoming requests
// Network tab would show 404 error (if checked)
// Frontend showed empty state with no errors
```

**Root Cause:**
```typescript
// lib/api.ts - Custom API wrapper
class ApiClient {
  async get(endpoint: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api${endpoint}`, {
      // ↑ Already adds /api prefix!
    })
    return await response.json()
  }
}

// app/admin/partner-applications/page.tsx - Component
const response = await api.get(`/api/partner-applications?status=${filter}`)
                                 ↑ Should NOT have /api here!

// Resulted in: http://localhost:3006/api/api/partner-applications → 404
```

**Investigation Breakthrough:**
1. ✅ Verified database has 10 applications
2. ✅ Backend API endpoint exists at `/api/partner-applications`
3. ❌ **Backend logs showed ZERO API requests** ← Critical clue!
4. 🔍 This meant frontend wasn't calling API correctly
5. 🎯 Analyzed API wrapper → Found automatic `/api` prefix

**Fix:**
```typescript
// BEFORE (404 error)
const response = await api.get('/api/partner-applications?status=pending')
await api.post('/api/partner-applications/approve', body)

// AFTER (Success)
const response = await api.get('/partner-applications?status=pending')
await api.post('/partner-applications/approve', body)
```

**Red Flags to Scan For:**
- [ ] Backend logs show no API requests despite frontend making calls
- [ ] Network tab shows 404 for `/api/api/...` double prefix
- [ ] Custom API wrapper adds URL prefixes automatically
- [ ] Inconsistent endpoint patterns across codebase
- [ ] No errors in console but data never loads

**Prevention:**
```typescript
// Document API wrapper behavior clearly
/**
 * API Client Wrapper
 *
 * IMPORTANT: This wrapper automatically adds '/api' prefix to all endpoints.
 *
 * ✅ CORRECT USAGE:
 *   api.get('/users')          → GET /api/users
 *   api.post('/login', data)   → POST /api/login
 *
 * ❌ WRONG USAGE:
 *   api.get('/api/users')      → GET /api/api/users (404)
 *   api.post('/api/login')     → POST /api/api/login (404)
 */
class ApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3006'

  async get(endpoint: string): Promise<any> {
    // Ensure endpoint doesn't start with /api to prevent double prefix
    const cleanEndpoint = endpoint.startsWith('/api/')
      ? endpoint.replace('/api/', '/')
      : endpoint

    const response = await fetch(`${this.baseUrl}/api${cleanEndpoint}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return await response.json()
  }
}
```

**Debugging Checklist:**
```bash
# 1. Check backend logs first!
tail -f backend.log | grep "GET /api/"

# 2. If no logs, frontend isn't calling API
# Check API wrapper implementation
cat lib/api.ts | grep "baseUrl\|fetch"

# 3. Search for all API calls
grep -r "api.get\|api.post" app/ components/

# 4. Verify no double /api/ prefix
grep -r "api.get('/api/" app/ components/
```

**Lessons Learned:**
1. **Backend logs are the first diagnostic tool** - No logs = frontend bug
2. **API wrappers are abstraction leaks** - Must understand wrapper behavior
3. **Double prefix is a common pattern** - Check wrapper + call site
4. **Document wrapper behavior in JSDoc** - Prevent future misuse
5. **Add URL validation in wrapper** - Auto-strip duplicate prefixes

**Time to Fix:** 15 minutes (once backend logs revealed no requests)

---

## 🔴 INCIDENT 5: Component Library Selector Mismatch (Nov 2024)

**Real E2E Test Failure:** Playwright test looked for `select[name="tier"]` but element was never found, causing timeout.

**Symptoms:**
```typescript
// Test code
await page.waitForSelector('select[name="tier"]', { timeout: 10000 })
// TimeoutError: Timeout 10000ms exceeded waiting for selector

// Error context showed combobox role, not select element
// Screenshot showed approval dialog with tier dropdown visible
```

**Root Cause:**
```typescript
// Component uses Shadcn UI Select (not native HTML select)
<Select name="tier" value={formData.tier}>
  <SelectTrigger>
    <SelectValue />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="silver">Silver</SelectItem>
  </SelectContent>
</Select>

// Renders as:
<button role="combobox" aria-label="Partner Tier">Silver</button>
<div role="listbox" hidden>
  <div role="option" data-value="silver">Silver</div>
</div>

// NOT:
<select name="tier">
  <option value="silver">Silver</option>
</select>
```

**Investigation Method:**
1. ✅ Test opened approval dialog successfully
2. ✅ Screenshot showed tier field visible
3. ❌ `error-context.md` showed combobox role, not select
4. 🎯 Realized Shadcn components use ARIA roles

**Fix:**
```typescript
// BEFORE (Native HTML selector)
await page.waitForSelector('select[name="tier"]')
await page.selectOption('select[name="tier"]', 'silver')

// AFTER (ARIA role selector)
const tierCombobox = page.getByRole('combobox', { name: /partner tier/i })
await tierCombobox.waitFor({ state: 'visible', timeout: 10000 })
await tierCombobox.click()
await page.waitForSelector('[role="listbox"]', { timeout: 5000 })
await page.getByRole('option', { name: /silver/i }).click()
```

**Red Flags to Scan For:**
- [ ] Using Shadcn, Radix, or similar component libraries
- [ ] Tests using element selectors (`select`, `input`, `button`)
- [ ] Tests timing out despite element visible in screenshots
- [ ] Error context shows `role="combobox"` or `role="listbox"`
- [ ] Component library documentation mentions "accessible components"

**Component Library Selector Guide:**

| Component | Native HTML | Shadcn/Radix Renders As | Test Selector |
|-----------|-------------|-------------------------|---------------|
| Select | `<select>` | `<button role="combobox">` | `getByRole('combobox')` |
| Checkbox | `<input type="checkbox">` | `<button role="checkbox">` | `getByRole('checkbox')` |
| Radio | `<input type="radio">` | `<button role="radio">` | `getByRole('radio')` |
| Dialog | `<div>` | `<div role="dialog">` | `getByRole('dialog')` |
| Switch | `<input type="checkbox">` | `<button role="switch">` | `getByRole('switch')` |

**Testing Pattern:**
```typescript
// ✅ GOOD - Semantic, accessible, component-agnostic
await page.getByRole('combobox', { name: /tier/i }).click()
await page.getByRole('option', { name: /silver/i }).click()
await page.getByRole('button', { name: /approve/i }).click()

// ❌ BAD - Brittle, implementation-specific
await page.locator('select[name="tier"]').selectOption('silver')
await page.locator('button.btn-primary').click()
await page.locator('#approve-button').click()
```

**Debugging Checklist:**
```bash
# 1. Check component library usage
grep -r "from '@radix-ui\|from 'shadcn'" components/

# 2. Find tests using element selectors
grep -r "select\[name=\|input\[name=" e2e/ tests/

# 3. Check error-context.md for actual HTML
cat test-results/*/error-context.md | grep "role="

# 4. Verify component renders with ARIA roles
grep -r "role=\"combobox\|role=\"listbox\"" node_modules/@radix-ui/
```

**Prevention:**
```typescript
// Add component testing documentation
/**
 * SHADCN UI TESTING GUIDE
 *
 * All Shadcn components render with ARIA roles for accessibility.
 * Use role-based selectors, not element selectors.
 *
 * Select Component:
 * ✅ page.getByRole('combobox', { name: /tier/i })
 * ❌ page.locator('select[name="tier"]')
 *
 * Dialog Component:
 * ✅ page.getByRole('dialog', { name: /approve/i })
 * ❌ page.locator('.modal-dialog')
 *
 * Button Component:
 * ✅ page.getByRole('button', { name: /submit/i })
 * ✅ page.locator('button:has-text("Submit")')  // Also works
 * ❌ page.locator('#submit-btn')
 */
```

**Lessons Learned:**
1. **Component libraries render ARIA roles, not native elements**
2. **Use `getByRole()` for better test resilience**
3. **Check error-context.md for actual HTML structure**
4. **Semantic selectors are more maintainable than CSS selectors**
5. **Read component library docs for rendered HTML**

**Time to Fix:** 10 minutes (once error-context.md revealed combobox role)

---

## Updated Investigation Methodology (Nov 2024)

Based on recent production incidents, follow this **exact order** when debugging "data not showing":

### 1. **Backend Logs First** 🚨 CRITICAL
```bash
# Check if API requests are reaching backend
tail -f backend.log | grep "/api/endpoint"

# If NO LOGS → Frontend bug (not calling API correctly)
# If LOGS → Backend bug (API called but not working)
```

**This single check saves 50% of debugging time.**

### 2. **Database Verification**
```sql
-- Verify data exists
SELECT COUNT(*) FROM table_name WHERE status = 'pending';

-- If 0 rows → Data problem
-- If >0 rows → Integration problem
```

### 3. **API Wrapper Analysis**
```typescript
// Read API client implementation
// Check:
// - Does it add /api prefix?
// - Does it unwrap response.data?
// - What headers does it add?
// - How does it handle errors?
```

### 4. **Frontend Response Handling**
```typescript
// Add temporary debug logging
const response = await api.get('/endpoint')
console.log('[DEBUG] Full response:', response)
console.log('[DEBUG] response.data:', response.data)
console.log('[DEBUG] Expected data:', response.items || response.data?.items)
```

### 5. **Skills Pattern Matching**
- Check if issue matches known incidents
- Apply fix templates if pattern matches
- Document new patterns if not in skill

### 6. **Component/Test Validation**
```bash
# If E2E test failing:
# 1. Check test screenshots
# 2. Read error-context.md for actual HTML
# 3. Verify selectors match rendered elements
# 4. Use role-based selectors for component libraries
```

**Estimated Debug Time by Following This Order:**
- Double API prefix: 15 minutes
- Response access pattern: 10 minutes
- Component selector: 10 minutes
- Database types: 20 minutes
- Null safety: 15 minutes

**Total saved vs. random debugging: 2-3 hours**
