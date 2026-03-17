---
name: audit-prod
description: Production smoke test — navigate key pages, check console errors, network failures, and report findings
disable-model-invocation: true
---

# Production Audit

Automated smoke test of production (`bricktrack.au`) using Playwright MCP.

## Test Matrix

Run each check and record results:

### 1. Homepage & Marketing Pages
- Navigate to `https://bricktrack.au`
- Check console messages (error level)
- Check network requests for 4xx/5xx responses
- Verify page loads without blank screen
- Take screenshot

### 2. Auth Flow
- Navigate to `https://bricktrack.au/sign-in`
- Verify sign-in page renders correctly
- Check for console errors
- Take screenshot

### 3. Dashboard (if authenticated session available)
- Navigate to `https://bricktrack.au/dashboard`
- Check for console errors
- Check for slow network requests (>3s)
- Verify data loads (not stuck on loading skeletons)
- Take screenshot

### 4. Key Feature Pages
For each page, check console errors and network failures:
- `/properties` — property list
- `/transactions` — transaction list
- `/documents` — document list
- `/settings` — settings page

### 5. Meta & SEO
- Check `<title>` tag is set
- Check favicon loads (no 404)
- Check `<meta name="description">` exists
- Check Open Graph tags exist

### 6. Performance Indicators
- Note any network requests >2 seconds
- Note any blocked/failed resource loads
- Note total page weight if available

## Report Format

```
## Production Audit Report — {date}

### Summary
- Pages checked: X/Y passed
- Console errors: X found
- Network failures: X found
- Overall: ✅ PASS / ❌ FAIL

### Details
| Page | Status | Console Errors | Network Issues | Notes |
|------|--------|---------------|----------------|-------|
| /    | ✅/❌   | 0             | 0              |       |
| ...  | ...    | ...           | ...            | ...   |

### Action Items
- [ ] Issue 1...
- [ ] Issue 2...
```

## Notification
```bash
curl -s -X POST "https://ntfy.sh/property-tracker-claude" \
  -d "Production audit complete — see report" \
  -H "Title: Audit" -H "Priority: default"
```
