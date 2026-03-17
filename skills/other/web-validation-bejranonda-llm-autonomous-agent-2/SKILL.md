---
name: web-validation
description: Comprehensive web page validation with authentication, screenshot capture, mobile testing, and enhanced error detection
version: 2.0.0
category: validation
tags: [web, javascript, testing, validation, browser, console, debugging, screenshots, mobile, authentication]
---

# Web Validation Skill

## Overview

This skill provides comprehensive methodology for validating web applications, detecting JavaScript errors, monitoring browser console output, capturing screenshots, and testing across mobile and desktop viewports with authentication support.

**Key Capabilities:**
- Automated JavaScript error detection with categorization
- Browser console log capture (errors, warnings, info)
- Network request monitoring and failure detection
- Performance metrics collection
- **Authentication support for protected pages** (NEW)
- **Screenshot capture for mobile and desktop** (NEW)
- **React hydration error detection (#185)** (NEW)
- **Multi-viewport testing (14 device presets)** (NEW)
- HTML/CSS validation
- Automated testing with headless browsers

## When to Apply This Skill

Use this skill when:
- Validating web-based dashboards (e.g., dashboard.py)
- Detecting JavaScript syntax errors automatically
- Monitoring console output without manual browser inspection
- Testing web applications before deployment
- Debugging web page issues
- Ensuring cross-browser compatibility
- Validating after code changes to web components
- **Testing authenticated/protected pages**
- **Capturing visual evidence for debugging**
- **Testing responsive design across devices**
- **Detecting React hydration mismatches**

## Authentication Support (NEW)

### Form-Based Authentication

Validate protected pages by automatically logging in:

```python
from lib.web_page_validator import WebPageValidator, AuthConfig

auth = AuthConfig(
    login_url="http://localhost:3000/auth/signin",
    email="test@example.com",
    password="TestPass123!",
    email_selector='input[type="email"]',
    password_selector='input[type="password"]',
    submit_selector='button[type="submit"]',
    post_login_wait=2.0
)

with WebPageValidator(auth_config=auth) as validator:
    validator.authenticate()
    result = validator.validate_url('http://localhost:3000/dashboard')
```

### Environment Variables

Credentials can be set via environment variables for CI/CD:
```bash
export TEST_EMAIL="test@example.com"
export TEST_PASSWORD="TestPass123!"
```

### Multi-Page Authentication Flow

```python
# Validate public and protected pages in one session
results = validator.validate_pages_with_auth(
    public_pages=[
        ("http://localhost:3000/", "Home"),
        ("http://localhost:3000/auth/signin", "Sign In"),
    ],
    protected_pages=[
        ("http://localhost:3000/dashboard", "Dashboard"),
        ("http://localhost:3000/settings", "Settings"),
    ]
)
```

## Screenshot Capture (NEW)

### Automatic Screenshots

Capture screenshots on validation for visual evidence:

```python
from lib.web_page_validator import WebPageValidator, ScreenshotConfig, ViewportConfig

screenshot_config = ScreenshotConfig(
    enabled=True,
    output_directory=".claude/screenshots",
    capture_on_error=True,
    capture_on_success=False,
    full_page=False
)

with WebPageValidator(screenshot_config=screenshot_config) as validator:
    result = validator.validate_url('http://localhost:3000')
    for ss in result.screenshots:
        print(f"Screenshot: {ss.file_path}")
```

### Multi-Viewport Screenshots

Capture screenshots across multiple devices:

```bash
python lib/web_page_validator.py http://localhost:3000 --viewport all --screenshot
```

### Screenshot Naming Convention

Files are named: `{page_name}_{viewport}_{timestamp}.png`
- `home_desktop_20251204_143022.png`
- `dashboard_mobile_20251204_143025.png`

## Mobile and Responsive Testing (NEW)

### Available Device Presets

| Viewport | Width | Height | Type | Device |
|----------|-------|--------|------|--------|
| desktop | 1920 | 1080 | Desktop | Full HD |
| desktop_small | 1280 | 720 | Desktop | HD |
| mobile | 375 | 812 | Mobile | iPhone X/12/13 |
| mobile_small | 320 | 568 | Mobile | iPhone SE |
| tablet | 768 | 1024 | Tablet | iPad |
| ipad_pro | 1024 | 1366 | Tablet | iPad Pro 12.9 |
| android_pixel | 393 | 851 | Mobile | Pixel 5 |
| android_samsung | 360 | 800 | Mobile | Galaxy S21 |
| android_tablet | 800 | 1280 | Tablet | Android Tablet |

### Mobile-First Testing

```python
from lib.web_page_validator import WebPageValidator, ViewportConfig

# Test on mobile viewport
validator = WebPageValidator(default_viewport=ViewportConfig.mobile())
result = validator.validate_url('http://localhost:3000')

# Test all viewports
results = validator.validate_all_viewports('http://localhost:3000')
```

### CLI Mobile Testing

```bash
# Mobile viewport
python lib/web_page_validator.py http://localhost:3000 --viewport mobile

# Tablet viewport
python lib/web_page_validator.py http://localhost:3000 --viewport tablet

# All viewports
python lib/web_page_validator.py http://localhost:3000 --viewport all

# Custom dimensions
python lib/web_page_validator.py http://localhost:3000 --viewport-width 414 --viewport-height 896
```

## React Hydration Error Detection (NEW)

### What is Hydration Error #185?

React hydration errors occur when server-rendered HTML doesn't match client-rendered content. This causes:
- Minified React error #185
- "Something went wrong" error boundary
- Content flickering or missing UI elements

### Automatic Detection

The validator automatically detects:
1. Console messages containing "#185" or "hydration"
2. Error boundary UI ("Something went wrong")
3. React Error Overlay presence
4. Next.js hydration warnings

```python
result = validator.validate_url('http://localhost:3000')

if result.has_react_hydration_error:
    print("[CRITICAL] React hydration mismatch detected!")

if result.error_boundary_visible:
    print("[WARN] Error boundary is visible to users!")
```

### Error Categories

Errors are automatically categorized:
- `REACT_HYDRATION` - React #185 and hydration mismatches
- `JAVASCRIPT_SYNTAX` - SyntaxError
- `JAVASCRIPT_RUNTIME` - TypeError, ReferenceError
- `NETWORK_FAILURE` - Failed HTTP requests
- `UNCAUGHT_EXCEPTION` - Unhandled exceptions
- `CONSOLE_ERROR` - Generic console.error

## Validation Methodology

### 1. Automated Browser Testing

**Approach**: Use headless browser automation to capture real browser behavior

**Tools**:
- **Selenium WebDriver**: Industry standard for browser automation
- **Playwright**: Modern alternative with better API
- **Chrome DevTools Protocol**: Direct browser control

**Implementation**:
```python
from lib.web_page_validator import WebPageValidator

with WebPageValidator(headless=True) as validator:
    result = validator.validate_url('http://127.0.0.1:5000')

    if not result.success:
        print(f"Found {len(result.console_errors)} errors")
        for error in result.console_errors:
            print(f"  - {error.message}")
```

### 2. Console Log Monitoring

**Types of Console Logs**:
- **Errors**: Critical issues that break functionality
- **Warnings**: Potential problems that should be addressed
- **Info**: Informational messages for debugging
- **Logs**: General debug output

**Capture Strategy**:
```javascript
// Enable console capture in browser
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

// Retrieve logs after page load
logs = driver.get_log('browser')
for log in logs:
    if log['level'] == 'SEVERE':
        # Critical error detected
        handle_error(log['message'])
```

### 3. JavaScript Error Detection

**Common JavaScript Error Patterns**:
- **SyntaxError**: Invalid JavaScript syntax
- **ReferenceError**: Undefined variables or functions
- **TypeError**: Invalid type operations
- **Uncaught exceptions**: Unhandled runtime errors

**Detection Methods**:
1. Browser console logs (level: SEVERE)
2. window.onerror event handler
3. Promise rejection tracking
4. Resource loading failures

**Example Detection**:
```python
# Check for SyntaxError in console logs
for log in console_logs:
    if 'SyntaxError' in log.message:
        # Extract line number and source
        # Parse error message
        # Generate fix suggestions
```

### 4. Network Request Monitoring

**What to Monitor**:
- Failed HTTP requests (404, 500, etc.)
- Timeout errors
- CORS issues
- Missing resources (CSS, JS, images)
- Slow-loading resources

**Performance Metrics**:
```javascript
// Collect Resource Timing data
const resources = performance.getEntriesByType('resource');
resources.forEach(r => {
    if (r.transferSize === 0 && r.duration > 0) {
        // Resource failed to load
        console.error(`Failed to load: ${r.name}`);
    }
});
```

### 5. Performance Validation

**Key Metrics**:
- **Load Time**: Total page load duration
- **DOM Ready**: Time until DOM is interactive
- **First Contentful Paint**: Time until first content renders
- **Resource Count**: Number of loaded resources
- **Page Size**: Total transfer size

**Thresholds**:
- Load time < 3 seconds (good)
- Load time 3-5 seconds (acceptable)
- Load time > 5 seconds (needs optimization)

## Validation Workflow

### Pre-Deployment Validation

**Step 1: Start Web Server**
```bash
python lib/dashboard.py --no-browser --port 5000 &
```

**Step 2: Wait for Server Ready**
```python
import time
import urllib.request

def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except:
            time.sleep(0.5)
    return False

wait_for_server('http://127.0.0.1:5000')
```

**Step 3: Run Validation**
```bash
python lib/web_page_validator.py http://127.0.0.1:5000 --verbose
```

**Step 4: Analyze Results**
```python
if result.success:
    print("[OK] No errors detected")
else:
    print(f"[ERROR] Found {len(result.console_errors)} errors")
    # Auto-fix or report to user
```

### Continuous Validation

**Integration Points**:
1. **On dashboard startup**: Automatically validate after server starts
2. **After code changes**: Run validation in git pre-commit hook
3. **Scheduled monitoring**: Periodic validation of running dashboards
4. **CI/CD pipeline**: Automated testing before deployment

### Error Analysis and Auto-Fix

**Common Issues and Fixes**:

**1. Literal Newlines in JavaScript Strings**
```python
# Problem: csvContent = 'Header\n'  # Python processes \n
# Fix: csvContent = r'Header\n'     # Raw string preserves \n
```

**2. Template Literal Interpolation**
```javascript
// Problem: `Value: $0`  # Tries to interpolate $0
// Fix: `Value: \$0`     # Escape the dollar sign
```

**3. Missing Resource Files**
```python
# Problem: 404 errors for CSS/JS files
# Fix: Check file paths and ensure resources exist
```

**4. CORS Issues**
```python
# Problem: Cross-origin request blocked
# Fix: Add CORS headers to Flask app
from flask_cors import CORS
CORS(app)
```

## Best Practices

### 1. Validation Coverage

**Essential Checks**:
- [ ] Page loads successfully (HTTP 200)
- [ ] No JavaScript syntax errors
- [ ] No console errors
- [ ] All resources load (CSS, JS, images)
- [ ] Page title is correct
- [ ] Load time is acceptable (< 5s)

**Recommended Checks**:
- [ ] No console warnings
- [ ] Performance metrics within thresholds
- [ ] Mobile responsiveness
- [ ] Accessibility compliance
- [ ] Cross-browser compatibility

### 2. Error Reporting

**Report Structure**:
```
=== WEB PAGE VALIDATION REPORT ===
URL: http://127.0.0.1:5000
Status: FAILED
Load Time: 2.34s

CONSOLE ERRORS (3):
1. [SEVERE] Uncaught SyntaxError: Invalid or unexpected token
   Source: http://127.0.0.1:5000/:1827
   Time: 2025-11-06T09:00:00

JAVASCRIPT ERRORS (1):
1. Uncaught SyntaxError: Invalid or unexpected token at line 1827

RECOMMENDATIONS:
1. Fix JavaScript syntax errors in source files
2. Use Python raw strings (r'...') for JavaScript escape sequences
3. Validate JavaScript code before deployment
```

### 3. Automated Remediation

**When Auto-Fix is Safe**:
- String escaping issues (add raw strings)
- Missing CORS headers (add to Flask config)
- Outdated dependencies (update requirements.txt)
- Simple syntax errors (apply known patterns)

**When Manual Review Required**:
- Logic errors in JavaScript
- Complex refactoring needed
- Security-related issues
- Breaking changes to API

### 4. Integration with Quality Control

**Quality Score Impact**:
- **0 errors**: Full credit (20/20 points)
- **1-2 warnings**: Minor deduction (18/20 points)
- **1-2 errors**: Moderate deduction (12/20 points)
- **3+ errors**: Significant deduction (5/20 points)
- **Critical errors**: Automatic failure (0/20 points)

## Tool Usage

### Command-Line Usage

**Basic Validation**:
```bash
python lib/web_page_validator.py http://127.0.0.1:5000
```

**Verbose Output**:
```bash
python lib/web_page_validator.py http://127.0.0.1:5000 --verbose
```

**Save Report to File**:
```bash
python lib/web_page_validator.py http://127.0.0.1:5000 --output report.txt
```

**JSON Output**:
```bash
python lib/web_page_validator.py http://127.0.0.1:5000 --json > result.json
```

**Show Browser (Debugging)**:
```bash
python lib/web_page_validator.py http://127.0.0.1:5000 --no-headless
```

### Programmatic Usage

**Python Integration**:
```python
from lib.web_page_validator import WebPageValidator, format_validation_report

# Validate URL
with WebPageValidator(headless=True, timeout=30) as validator:
    result = validator.validate_url('http://127.0.0.1:5000', wait_for_load=3)

# Check success
if result.success:
    print("[OK] Page validated successfully")
else:
    print(f"[ERROR] Validation failed: {result.error_summary}")

    # Get detailed report
    report = format_validation_report(result, verbose=True)
    print(report)

    # Access specific errors
    for error in result.console_errors:
        print(f"Error: {error.message}")
```

### Slash Command Usage

```bash
# Validate dashboard at default URL
/validate:web http://127.0.0.1:5000

# Validate with auto-fix enabled
/validate:web http://127.0.0.1:5000 --auto-fix

# Validate and save report
/validate:web http://127.0.0.1:5000 --report
```

## Installation Requirements

### Required Dependencies

**Selenium (Recommended)**:
```bash
pip install selenium
```

**ChromeDriver** (for Selenium):
- Download from: https://chromedriver.chromium.org/
- Or use: `pip install webdriver-manager`

**Playwright (Alternative)**:
```bash
pip install playwright
playwright install chromium
```

### Minimal Installation

If browser automation is not available, the tool falls back to basic HTTP validation:
- No additional dependencies required
- Limited error detection
- No console log capture
- Basic connectivity and HTTP status checking only

## Integration Examples

### Dashboard Startup Validation

**Modify dashboard command to auto-validate**:
```python
# In commands/monitor/dashboard.md
# After starting server, run validation
subprocess.Popen(['python', 'lib/dashboard.py', '--no-browser', '--port', '5000'])
time.sleep(3)  # Wait for server to start

# Validate
result = subprocess.run(
    ['python', 'lib/web_page_validator.py', 'http://127.0.0.1:5000'],
    capture_output=True
)

if result.returncode != 0:
    print("[WARN] Dashboard validation failed, see report for details")
```

### Git Pre-Commit Hook

**Validate before committing dashboard changes**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if dashboard.py was modified
if git diff --cached --name-only | grep -q "dashboard.py"; then
    echo "Running dashboard validation..."

    # Start server
    python lib/dashboard.py --no-browser --port 5555 &
    PID=$!
    sleep 3

    # Validate
    python lib/web_page_validator.py http://127.0.0.1:5555
    RESULT=$?

    # Cleanup
    kill $PID

    if [ $RESULT -ne 0 ]; then
        echo "ERROR: Dashboard validation failed"
        exit 1
    fi
fi
```

### Continuous Monitoring

**Periodic validation of running dashboard**:
```python
import schedule
import time
from lib.web_page_validator import WebPageValidator

def validate_dashboard():
    with WebPageValidator() as validator:
        result = validator.validate_url('http://127.0.0.1:5000')

        if not result.success:
            # Alert or log errors
            print(f"[ALERT] Dashboard errors detected: {result.error_summary}")
            # Send notification, log to file, etc.

# Run validation every 5 minutes
schedule.every(5).minutes.do(validate_dashboard)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## Troubleshooting

### Common Issues

**1. Selenium WebDriver not found**
```
Solution: Install ChromeDriver
- Download from: https://chromedriver.chromium.org/
- Or: pip install webdriver-manager
- Add to PATH
```

**2. Chrome not installed**
```
Solution: Install Google Chrome browser
- Download from: https://www.google.com/chrome/
- Or use Playwright as alternative
```

**3. Timeout errors**
```
Solution: Increase timeout
python lib/web_page_validator.py URL --timeout 60
```

**4. No errors detected but page broken**
```
Solution: Increase wait time after page load
python lib/web_page_validator.py URL --wait 10
```

**5. Permission denied on Windows**
```
Solution: Run as administrator or disable antivirus temporarily
```

## Advanced Features

### Custom Validation Rules

**Add custom checks**:
```python
class CustomWebPageValidator(WebPageValidator):
    def validate_custom_rules(self, page):
        issues = []

        # Check for specific elements
        if not page.find_element(By.ID, 'dashboard-content'):
            issues.append("Missing dashboard-content element")

        # Check for required JavaScript globals
        has_required_js = page.execute_script("""
            return typeof Chart !== 'undefined' &&
                   typeof dashboardData !== 'undefined';
        """)

        if not has_required_js:
            issues.append("Missing required JavaScript libraries")

        return issues
```

### Performance Budgets

**Enforce performance thresholds**:
```python
def validate_performance(result):
    budget = {
        'loadTime': 3000,  # 3 seconds
        'domReady': 1000,  # 1 second
        'resourceCount': 50
    }

    violations = []

    if result.load_time > budget['loadTime'] / 1000:
        violations.append(f"Load time exceeds budget: {result.load_time:.2f}s > 3s")

    return violations
```

### Accessibility Validation

**Check for accessibility issues**:
```python
# Install axe-core for accessibility testing
page.execute_script("""
    // Inject axe-core library
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.2/axe.min.js';
    document.head.appendChild(script);
""")

# Run accessibility scan
results = page.execute_script("return axe.run();")
violations = results.get('violations', [])
```

## Success Metrics

**Validation Quality Indicators**:
- **100% error-free**: All pages load without console errors
- **< 1 second validation time**: Fast feedback loop
- **Zero false positives**: Accurate error detection
- **Automated remediation**: 80%+ of issues fixed automatically
- **Continuous monitoring**: 24/7 health checking

## Summary

The web validation skill provides:
- **Automated error detection** without manual browser inspection
- **Real-time console monitoring** for JavaScript issues
- **Comprehensive validation** of web applications
- **Performance measurement** and optimization guidance
- **Integration-ready** for CI/CD pipelines and quality control

Use this skill whenever working with web-based components to ensure quality and catch errors early in the development cycle.
