---
name: playwright-network-analyzer
description: |
  Monitors and analyzes network traffic during browser automation workflows using Playwright MCP tools.
  Use when investigating API behavior, debugging failed requests, performance analysis, or checking
  network activity during user flows. Triggers on "analyze network requests", "check API calls",
  "monitor network traffic", "debug API errors", or "performance analysis". Works with Playwright
  browser automation (browser_navigate, browser_network_requests, browser_click, browser_fill_form).

---

# Playwright Network Analyzer

## Quick Start

Analyze network traffic during a user login flow:

```
You: "Analyze network requests during login to example.com with user@test.com"

Claude invokes playwright-network-analyzer skill:
1. Navigates to example.com/login
2. Clears previous network requests
3. Fills login form and submits
4. Captures all network requests
5. Generates report showing:
   - 2 failed API calls (401, 500)
   - 3 slow requests (>1s)
   - Total: 15 requests (8 API, 7 static)
```

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Workflow Steps
4. Analysis Categories
5. Supporting Files
6. Expected Outcomes
7. Requirements
8. Utility Scripts
9. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- "Analyze network requests during [workflow]"
- "Check API calls on [page/feature]"
- "Monitor network traffic while [action]"
- "Debug API errors in [feature]"
- "Performance analysis for [user flow]"
- "Show me network activity when [scenario]"

### Implicit Triggers
- Investigating why a feature fails intermittently
- Checking if API endpoints return expected status codes
- Validating third-party integrations (analytics, CDNs)
- Verifying authentication flows
- Debugging CORS or network errors

### Debugging Triggers
- "Why is this page slow?"
- "Is the API call working?"
- "Are there failed requests?"
- "What endpoints are being called?"

## What This Skill Does

1. **Automated Network Monitoring** - Captures all HTTP requests during browser workflows
2. **Request Categorization** - Separates API calls from static resources (images, CSS, JS)
3. **Error Detection** - Identifies failed requests (4xx, 5xx status codes)
4. **Performance Analysis** - Flags slow requests (>1s response time)
5. **Pattern Recognition** - Detects repeated requests, missing resources, CORS issues
6. **Structured Reporting** - Generates categorized reports with actionable insights

## Workflow Steps

### Step 1: Navigate to Application

Use `browser_navigate` to load the target page:

```
Navigate to: https://app.example.com/dashboard
Wait for page load completion
```

### Step 2: Clear Previous Network Requests

Call `browser_network_requests` to establish baseline:

```
Action: Read and clear existing requests
Purpose: Start with clean slate for accurate analysis
```

### Step 3: Execute User Workflow

Perform the user actions to monitor:

```
Examples:
- Click login button → Fill form → Submit
- Navigate to products → Add to cart → Checkout
- Upload file → Wait for processing → Download result
- Search → Filter results → Click item
```

Use these tools as needed:
- `browser_click` - Click buttons, links, elements
- `browser_fill_form` - Enter form data
- `browser_type` - Type text into inputs
- `browser_wait_for` - Wait for elements or text

### Step 4: Capture All Network Requests

Call `browser_network_requests` after workflow completes:

```
Options:
- includeStatic: true/false (include images, CSS, JS)
- urlPattern: filter by URL substring
- limit: max requests to return
```

### Step 5: Filter and Categorize

Use the analysis script to process requests:

```bash
python scripts/analyze_network.py requests.json \
  --threshold 1000 \
  --report report.md
```

**Categories:**
- **Failed Requests** - 4xx (client errors), 5xx (server errors)
- **API Calls** - Endpoints returning JSON/XML (exclude static resources)
- **Slow Requests** - Response time >1s (configurable threshold)
- **Static Resources** - Images, CSS, JS, fonts
- **Redirects** - 3xx status codes

### Step 6: Generate Report

Create structured analysis with:

**Summary Section:**
- Total requests
- API vs static breakdown
- Error count
- Slow request count

**Failed Requests:**
```
❌ POST /api/auth/login - 401 Unauthorized (250ms)
❌ GET /api/users/profile - 500 Internal Server Error (1.2s)
```

**Slow Requests (>1s):**
```
🐌 GET /api/products?limit=100 - 200 OK (2.3s)
🐌 GET /api/reports/export - 200 OK (5.1s)
```

**API Calls:**
```
✅ POST /api/auth/login - 200 OK (250ms)
✅ GET /api/dashboard - 200 OK (450ms)
```

### Step 7: Identify Potential Issues

**Common patterns to flag:**
- Same endpoint called multiple times (N+1 queries)
- Missing resources (404s for CSS/JS/images)
- CORS errors (check console messages)
- Slow endpoints (candidates for optimization)
- Unauthenticated API calls (401s suggesting auth issues)
- Server errors (500s indicating backend problems)

## Supporting Files

### scripts/analyze_network.py
Python utility for processing network request JSON and generating categorized reports. Includes:
- Request filtering by status code, URL pattern, timing
- Categorization (API vs static, success vs error)
- Markdown report generation
- CSV export for spreadsheet analysis

**Usage:**
```bash
# Basic analysis
python scripts/analyze_network.py requests.json

# With custom threshold for "slow" (2 seconds)
python scripts/analyze_network.py requests.json --threshold 2000

# Filter to specific domain
python scripts/analyze_network.py requests.json --domain api.example.com

# Export to CSV
python scripts/analyze_network.py requests.json --csv output.csv
```

### references/network_patterns.md
Common network issues and their signatures:
- N+1 query detection patterns
- CORS error identification
- Authentication flow validation
- CDN vs origin server patterns
- API versioning issues

### examples/example_analysis.md
Sample network analysis reports for:
- Login flow (authentication, session creation)
- E-commerce checkout (payment gateway integration)
- File upload workflow (multipart, progress)
- SPA navigation (lazy loading, route changes)

## Expected Outcomes

### Successful Analysis

```
✅ Network Analysis Complete

Workflow: Login to dashboard
Duration: 3.2s
Total Requests: 18

Summary:
  ✅ API Calls: 8 (7 successful, 1 failed)
  📦 Static Resources: 10 (all successful)
  🐌 Slow Requests: 2 (>1s)
  ❌ Failed Requests: 1

Failed Requests:
  ❌ POST /api/user/preferences - 500 Internal Server Error (1.1s)

Slow Requests:
  🐌 GET /api/dashboard/widgets - 200 OK (2.3s)
  🐌 GET /cdn/images/banner.png - 200 OK (1.5s)

Issues Identified:
  ⚠️ Preferences API failing (500 error)
  ⚠️ Dashboard widget endpoint slow (2.3s)
  ℹ️ Large image file from CDN (consider optimization)

Recommendations:
  1. Fix /api/user/preferences endpoint (server error)
  2. Optimize dashboard widget query (2.3s response)
  3. Compress banner.png or use responsive images
```

### Analysis with Patterns

```
✅ Network Analysis Complete

Pattern Detected: N+1 Query Problem
  GET /api/products - 200 OK (150ms)
  GET /api/products/1/details - 200 OK (80ms)
  GET /api/products/2/details - 200 OK (85ms)
  GET /api/products/3/details - 200 OK (90ms)
  ... (12 more similar requests)

Recommendation: Use batch endpoint or include details in /api/products response
```

## Integration Points

### With Browser Automation Workflows
- Invoke during existing Playwright automation
- Add network monitoring to regression tests
- Validate API contracts during E2E tests

### With Performance Monitoring
- Establish baseline request timings
- Track performance regressions over time
- Identify optimization opportunities

### With API Testing
- Verify expected endpoints are called
- Check request/response payloads
- Validate authentication flows

## Expected Benefits

| Metric | Before | After |
|--------|--------|-------|
| **Time to identify API issues** | 15-30 min (manual) | 1-2 min (automated) |
| **Network debugging accuracy** | ~60% (guessing) | ~95% (data-driven) |
| **Performance bottleneck discovery** | Ad-hoc | Systematic |
| **Failed request detection** | Reactive (user reports) | Proactive (automated) |

## Success Metrics

- **Coverage** - Network requests captured during critical user flows
- **Detection Rate** - % of API issues identified before user reports
- **Analysis Speed** - Time from workflow execution to actionable report
- **Actionability** - % of reports leading to specific fixes

## Requirements

### Tools
- Playwright MCP server enabled (browser automation tools)
- Python 3.8+ (for analysis script)
- Browser with network monitoring capability

### Environment
- Active Playwright browser session
- Network requests recording enabled (default)

### Knowledge
- Basic understanding of HTTP status codes
- Familiarity with API vs static resource distinction
- Understanding of web application architecture

## Utility Scripts

### scripts/analyze_network.py

Python utility for processing network request JSON and generating categorized reports.

**Usage:**
```bash
python scripts/analyze_network.py requests.json [--threshold 2000] [--domain api.example.com] [-o report.md] [--csv output.csv]
```

Features: JSON parsing, filtering, categorization (API/static, success/error, fast/slow), Markdown/CSV export, pattern detection (N+1 queries, CORS issues).

## Red Flags to Avoid

- [ ] Analyzing network requests without clearing previous data (baseline contamination)
- [ ] Including static resources in API analysis (skews error rates)
- [ ] Using arbitrary thresholds for "slow" without context (1s may be fast for some endpoints)
- [ ] Ignoring successful redirects (3xx can be normal flow)
- [ ] Not filtering by URL pattern when analyzing specific features
- [ ] Forgetting to wait for async requests to complete
- [ ] Analyzing network traffic without user workflow context
- [ ] Reporting all issues as critical (prioritize by impact)
- [ ] Not checking console messages for CORS/JS errors
- [ ] Assuming correlation = causation (slow request ≠ always a problem)

## Notes

- **Request timing** includes network latency + server processing + response transfer (full lifecycle)
- **CORS errors** require checking console messages (use `read_console_messages` tool)
- **Static filtering** use `includeStatic: false` in `browser_network_requests` to focus on API calls
- **Rate limiting** indicated by multiple failed requests to same endpoint (429 status)
- **Progressive enhancement** start with basic categorization, add pattern detection as needed
