---
name: browser-automation-debugging
description: "Use when debugging web applications or automating browser tasks. Leverage Chrome DevTools MCP for inspection, performance analysis, and automated testing."
---

# Browser Automation & Debugging

## Core Principle

**Interact with live browsers programmatically.** Use Chrome DevTools MCP to control, inspect, and debug web applications through Claude Code without manual clicking.

## Overview

Chrome DevTools MCP provides 26 tools for browser automation and debugging through Claude Code. Control real Chrome instances, capture screenshots, analyze network traffic, inspect performance, and automate testing workflows - all via natural language commands.

## When to Use This Skill

- **Debugging web applications** - Inspect live page state
- **Browser automation** - Automate repetitive browser tasks
- **End-to-end testing** - Test user flows automatically
- **Performance profiling** - Record and analyze performance traces
- **Network analysis** - Inspect API calls and responses
- **Visual regression testing** - Capture screenshots for comparison
- **Form testing** - Automate form filling and submission
- **Console debugging** - Monitor JavaScript errors and logs
- **DOM inspection** - Examine page structure and elements
- **Screenshot capture** - Document bugs or features

## Prerequisites

**Required:**
- Chrome DevTools MCP server installed (see `.mcp.json`)
- Chrome stable browser (latest version)
- Node.js v20.19+ (or v22.12+/v23+)

**Verify MCP is available:**
```
Ask Claude: "Can you open a browser and navigate to example.com?"
```

## The Iron Laws

### 1. ALWAYS WAIT FOR OPERATIONS TO COMPLETE

**Chrome DevTools MCP automatically waits for:**
- Navigation to finish loading
- Elements to appear before clicking
- Network requests to complete
- JavaScript to execute

❌ **NEVER:**
- Add arbitrary timeouts
- Assume instant completion
- Skip verification steps

✅ **ALWAYS:**
- Trust automatic waiting
- Verify results after operations
- Check for errors in console

**Authority**: Puppeteer (underlying engine) handles timing automatically.

### 2. INSPECT BEFORE AUTOMATING

**Before writing automation scripts:**
```
1. Navigate to page manually via MCP
2. Inspect element selectors
3. Test interactions step-by-step
4. Verify expected behavior
5. Then script the automation
```

### 3. CAPTURE EVIDENCE

**Always document findings:**
- Take screenshots of bugs
- Save network traces for performance issues
- Log console errors
- Record steps to reproduce

## Browser Automation Protocol

### Step 1: Announce Usage

**Template:**
```
I'm using the browser-automation-debugging skill to [debug/test/automate] [task].

Starting Chrome browser automation...
```

### Step 2: Basic Browser Control

**Navigation:**
```
Ask Claude:
"Navigate to https://example.com"
"Go to http://localhost:3000"
"Navigate back to previous page"
"Reload the current page"
```

**Element Interaction:**
```
Ask Claude:
"Click the login button"
"Fill the username field with 'user@example.com'"
"Click the submit button and wait for response"
"Upload test-file.pdf to the file input"
"Drag the slider to position 50"
```

**Screenshots:**
```
Ask Claude:
"Take a screenshot of the current page"
"Capture a full-page screenshot"
"Take a screenshot of the login form"
```

### Step 3: Debugging Workflows

#### Workflow 1: Bug Investigation

```
1. Navigate to page with bug
2. Capture screenshot (before state)
3. Open browser console
4. Perform action that triggers bug
5. Check console for errors
6. Capture screenshot (after state)
7. Inspect network requests (if API-related)
8. Document findings
```

**Example:**
```
Ask Claude:
1. "Navigate to https://myapp.com/dashboard"
2. "Take a screenshot"
3. "Show me any console errors"
4. "Click the submit button"
5. "Check console for new errors"
6. "Take another screenshot"
7. "Show me the network requests to the API"
```

#### Workflow 2: Form Testing

```
1. Navigate to form page
2. Fill all required fields
3. Submit form
4. Verify success message appears
5. Check network request was successful
6. Verify data was saved (reload page)
```

**Example:**
```
Ask Claude:
1. "Navigate to http://localhost:3000/signup"
2. "Fill email field with 'test@example.com'"
3. "Fill password field with 'SecurePass123'"
4. "Click the signup button"
5. "Wait for success message"
6. "Take a screenshot of the result"
7. "Check if API request was successful (status 200)"
```

#### Workflow 3: Performance Analysis

```
1. Start performance recording
2. Navigate to page or trigger action
3. Stop recording
4. Analyze trace for bottlenecks
5. Identify slow operations
6. Document findings with metrics
```

**Example:**
```
Ask Claude:
1. "Start recording performance trace"
2. "Navigate to https://myapp.com/slow-page"
3. "Stop recording"
4. "Show me the performance bottlenecks"
5. "Which operations took longest?"
6. "Show me network timing for all requests"
```

#### Workflow 4: Network Debugging

```
1. Navigate to page
2. Monitor network requests
3. Trigger action (form submit, API call)
4. Inspect request/response
5. Check status codes
6. Verify response data
7. Identify failed requests
```

**Example:**
```
Ask Claude:
1. "Navigate to https://myapp.com/api-test"
2. "Monitor network requests"
3. "Click the load data button"
4. "Show me all API requests made"
5. "Which requests failed?"
6. "Show me the response for the /api/users request"
```

### Step 4: Advanced Automation

#### Multi-Step User Flows

```
Test complete user journey:
1. Navigate to homepage
2. Click login link
3. Fill credentials
4. Submit form
5. Verify dashboard loads
6. Navigate to profile
7. Update settings
8. Save changes
9. Verify success message
10. Logout
```

#### Visual Regression Testing

```
1. Navigate to page (baseline version)
2. Take screenshot → save as baseline.png
3. Deploy changes
4. Navigate to page (new version)
5. Take screenshot → save as current.png
6. Compare screenshots visually
7. Document differences
```

#### Automated Smoke Tests

```
Critical paths to test:
- Homepage loads
- Login works
- Main navigation functional
- Search returns results
- Checkout process completes
- Account settings save
```

## Common Automation Patterns

### Pattern 1: Login Automation

```
Ask Claude:
"Navigate to https://myapp.com/login,
fill email with 'user@example.com',
fill password with 'password123',
click login button,
wait for dashboard to load,
take a screenshot"
```

### Pattern 2: E2E Shopping Cart Test

```
Ask Claude:
"Navigate to https://shop.example.com,
search for 'laptop',
click the first product,
click add to cart,
go to cart page,
verify item is in cart,
take screenshot,
proceed to checkout"
```

### Pattern 3: Form Validation Testing

```
Ask Claude:
"Navigate to https://myapp.com/signup,
leave all fields empty,
click submit,
capture error messages,
take screenshot,
now fill valid data,
submit again,
verify success"
```

### Pattern 4: Responsive Design Testing

```
Ask Claude:
"Navigate to https://myapp.com,
take screenshot in desktop mode,
switch to mobile viewport (375x667),
take screenshot in mobile mode,
compare layouts"
```

### Pattern 5: Console Error Monitoring

```
Ask Claude:
"Navigate to https://myapp.com,
monitor console messages,
perform user actions [specify actions],
show me any errors or warnings logged,
categorize by severity"
```

## Debugging Workflows by Issue Type

### JavaScript Errors

```
1. Navigate to page with error
2. Open console
3. Reproduce error
4. Capture error message and stack trace
5. Identify file and line number
6. Check network for failed resource loads
7. Take screenshot for documentation
```

### Network/API Issues

```
1. Navigate to page
2. Monitor network requests
3. Trigger API call
4. Check response status code
5. Inspect response body
6. Verify request headers
7. Check timing (slow requests)
8. Document failed endpoints
```

### Performance Problems

```
1. Start performance recording
2. Load page or trigger slow operation
3. Stop recording
4. Analyze timeline:
   - Long tasks (>50ms)
   - Layout thrashing
   - Forced reflows
   - Excessive JavaScript execution
5. Identify bottleneck
6. Document with metrics
```

### UI/UX Issues

```
1. Navigate to page
2. Take baseline screenshot
3. Perform user action
4. Take result screenshot
5. Check for layout shifts (CLS)
6. Verify responsive behavior
7. Test keyboard navigation
8. Check focus indicators
```

## Best Practices

### 1. Use Descriptive Selectors

❌ **BAD:**
```
"Click the button"  (too ambiguous)
```

✅ **GOOD:**
```
"Click the submit button"
"Click the button with text 'Sign Up'"
"Click the button with id 'submit-form'"
```

### 2. Verify Results

❌ **BAD:**
```
"Fill form and submit" (no verification)
```

✅ **GOOD:**
```
"Fill form, submit, and verify success message appears"
"Fill form, submit, and check if redirected to dashboard"
```

### 3. Handle Errors Gracefully

```
"Navigate to page,
if login required then login first,
then perform action"

"Click button,
check console for errors,
if errors exist document them"
```

### 4. Document Automation Steps

```
Test: User Registration Flow
Steps:
1. Navigate to /signup
2. Fill email: test@example.com
3. Fill password: SecurePass123
4. Submit form
5. Verify success message
6. Check email confirmation sent
Results: ✅ PASS / ❌ FAIL
Screenshots: [link]
```

## Troubleshooting

### Chrome Not Found

**Error**: Chrome executable not found

**Solution:**
```
1. Install Chrome stable (latest)
2. Update Chrome to latest version
3. Restart Claude Code
4. Verify: chrome --version
```

### Element Not Found

**Error**: Cannot find element

**Solution:**
```
1. Take screenshot to verify page loaded
2. Check element actually exists on page
3. Use more specific selector
4. Wait for dynamic content to load
5. Check for iframe (may need to switch context)
```

### Timeout Errors

**Error**: Navigation timeout

**Solution:**
```
1. Check network connection
2. Verify URL is accessible
3. Check if page is very slow
4. Look for console errors blocking load
5. Disable problematic scripts temporarily
```

### Node Version Error

**Error**: Unsupported Node.js version

**Solution:**
```
1. Update Node.js to v20.19+ or v22.12+/v23+
2. Verify: node --version
3. Restart Claude Code
```

## Integration with Other Skills

**Before automation:**
- `brainstorming` - Plan automation strategy
- `writing-plans` - Break automation into steps

**During automation:**
- `systematic-debugging` - Debug issues found
- `test-driven-development` - Write permanent tests

**After automation:**
- `verification-before-completion` - Verify automation works
- `playwright-frontend-testing` - Convert to permanent tests

## Chrome DevTools MCP Capabilities

**26 Tools Available:**

**Browser Control (8 tools):**
- Navigate pages
- Click elements
- Fill forms
- Upload files
- Drag objects
- Press keys
- Scroll page
- Execute JavaScript

**Performance (3 tools):**
- Start/stop trace recording
- Analyze performance
- Get metrics

**Network (2 tools):**
- Monitor requests
- Analyze responses

**Debugging (5 tools):**
- Capture screenshots
- Read console
- Inspect DOM
- Get page info
- Evaluate JavaScript

**Emulation (2 tools):**
- Device emulation
- Viewport control

**Navigation (6 tools):**
- Go forward/back
- Reload page
- Wait for conditions
- Handle dialogs
- Manage cookies
- Get page source

## Advanced Techniques

### JavaScript Execution

```
Ask Claude:
"Execute JavaScript on the page:
document.querySelector('.username').textContent"

"Run this script to get all links:
Array.from(document.querySelectorAll('a')).map(a => a.href)"
```

### Custom Wait Conditions

```
Ask Claude:
"Wait until the element with class 'loading' disappears"
"Wait until the API response appears in network tab"
"Wait for 3 seconds then take screenshot"
```

### Cookie Management

```
Ask Claude:
"Set cookie: session_id=abc123"
"Clear all cookies"
"Get all cookies from current domain"
```

### Viewport Testing

```
Ask Claude:
"Set viewport to 1920x1080 (desktop)"
"Set viewport to 375x667 (iPhone SE)"
"Set viewport to 768x1024 (iPad)"
"Test responsive breakpoints: mobile, tablet, desktop"
```

## Remember

**Browser automation is powerful but not a replacement for human testing.**

Use it for:
- ✅ Repetitive tasks
- ✅ Quick smoke tests
- ✅ Debugging assistance
- ✅ Performance analysis
- ✅ Screenshot capture

But still do:
- 👤 Manual exploratory testing
- 👤 UX validation
- 👤 Accessibility testing with assistive tech
- 👤 Cross-browser compatibility checks

**Authority**: Automation finds regressions, humans find usability issues.

---

**Resources:**
- [Puppeteer Documentation](https://pptr.dev/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Chrome DevTools MCP GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp/)
