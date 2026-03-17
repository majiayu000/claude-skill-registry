---
name: webapp-testing
description: "Professional web application testing and automation using Playwright with support for multiple browsers, mobile emulation, screenshot capture, network interception, and comprehensive test assertions. Use for: (1) E2E testing across browsers, (2) UI automation, (3) Form testing and validation, (4) Visual regression testing, (5) API mocking and interception, (6) Mobile responsive testing"
---

# Web Application Testing with Playwright

## Overview

Playwright is a powerful framework for web testing and automation that supports all modern browsers (Chromium, Firefox, WebKit). It provides reliable, fast, and capable automation with auto-waiting, network control, and comprehensive testing capabilities.

Use this skill when you need to:
- Create end-to-end tests for web applications
- Automate browser interactions and workflows
- Test across multiple browsers and devices
- Verify UI/UX functionality and accessibility
- Mock APIs and intercept network requests
- Capture screenshots and videos for debugging

## Core Capabilities

### Multi-Browser Testing
- Chromium (Chrome, Edge, Brave)
- Firefox (Mozilla Firefox)
- WebKit (Safari engine)
- Cross-browser compatibility testing
- Parallel execution across browsers

### Element Interaction
- Click, double-click, right-click
- Type text with realistic keyboard simulation
- Select dropdowns and checkboxes
- Hover and focus interactions
- Drag and drop operations
- File uploads and downloads

### Assertions & Verification
- Element visibility and state checks
- Text content verification
- Attribute validation
- URL and navigation assertions
- Custom expect matchers
- Soft assertions for multiple checks

### Screenshot & Video Capture
- Full page screenshots
- Element-specific captures
- Video recording of test sessions
- Visual comparison testing
- Trace files for debugging

### Network Interception
- Mock API responses
- Intercept and modify requests
- Monitor network traffic
- Test offline scenarios
- Performance monitoring

### Mobile Device Emulation
- 100+ device presets (iPhone, Pixel, iPad, etc.)
- Custom viewport configurations
- Touch event simulation
- Geolocation testing
- Orientation changes

## Core Testing Workflow

### 1. Basic Test Setup

Create a simple test with Playwright's auto-waiting:

```python
import pytest
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    """Test that homepage loads successfully."""
    page.goto("https://example.com")
    expect(page).to_have_title("Example Domain")
    expect(page.locator("h1")).to_contain_text("Example Domain")

def test_navigation(page: Page):
    """Test navigation between pages."""
    page.goto("https://example.com")
    page.click("text=More information")
    expect(page).to_have_url("https://www.iana.org/domains/reserved")
```

### 2. Form Interactions

Test form filling, validation, and submission:

```python
def test_login_form(page: Page):
    """Test login form submission."""
    page.goto("https://example.com/login")

    # Fill form fields
    page.fill("#username", "testuser@example.com")
    page.fill("#password", "SecurePassword123")
    page.check("#remember-me")

    # Submit and verify
    page.click("button[type='submit']")
    expect(page).to_have_url("https://example.com/dashboard")
    expect(page.locator(".welcome-message")).to_be_visible()
```

### 3. API Mocking

Mock API responses for controlled testing:

```python
def test_with_mocked_api(page: Page):
    """Test with mocked API response."""
    # Mock API response
    page.route("**/api/user", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"name": "Test User", "premium": true}'
    ))

    page.goto("https://example.com/profile")
    expect(page.locator(".user-name")).to_contain_text("Test User")
```

### 4. Mobile Emulation

Test responsive designs on mobile devices:

```python
@pytest.fixture
def mobile_page(playwright):
    """Create mobile browser context."""
    iphone = playwright.devices['iPhone 12']
    browser = playwright.chromium.launch()
    context = browser.new_context(**iphone)
    page = context.new_page()
    yield page
    context.close()
    browser.close()

def test_mobile_menu(mobile_page: Page):
    """Test mobile navigation."""
    mobile_page.goto("https://example.com")
    expect(mobile_page.locator(".hamburger-menu")).to_be_visible()
    mobile_page.click(".hamburger-menu")
    expect(mobile_page.locator(".mobile-menu")).to_be_visible()
```

### 5. Visual Regression

Capture screenshots for visual comparison:

```python
def test_homepage_screenshot(page: Page):
    """Capture homepage screenshot."""
    page.goto("https://example.com")

    # Full page screenshot
    page.screenshot(path="screenshots/homepage.png", full_page=True)

    # Element screenshot
    page.locator("header").screenshot(path="screenshots/header.png")

    # Screenshot with masks for dynamic content
    page.screenshot(
        path="screenshots/dashboard.png",
        mask=[page.locator(".timestamp"), page.locator(".session-id")]
    )
```

## Key Testing Principles

### Use Reliable Selectors

```python
# ✅ GOOD: Test IDs and semantic selectors
page.click("[data-testid='submit-button']")
page.click("button:text('Submit')")
page.click("role=button[name='Submit']")

# ❌ BAD: Fragile structural selectors
page.click("div > div > button:nth-child(3)")
```

### Leverage Auto-Waiting

```python
# ✅ GOOD: Playwright auto-waits
page.click("button")
expect(page.locator(".result")).to_be_visible()

# ⚠️ Avoid: Manual waits
time.sleep(2)  # Only when absolutely necessary
```

### Ensure Test Isolation

```python
# ✅ GOOD: Clean state between tests
@pytest.fixture(autouse=True)
def clear_state(page: Page):
    yield
    page.context.clear_cookies()
    page.evaluate("localStorage.clear()")
```

### Handle Flaky Tests

```python
# ✅ GOOD: Wait for specific conditions
page.click("button")
page.wait_for_selector(".result")
result = page.locator(".result").text_content()

# ✅ GOOD: Use soft assertions
expect.soft(page.locator(".title")).to_be_visible()
expect.soft(page.locator(".price")).to_contain_text("$")
```

## Page Object Model

Organize tests using the Page Object pattern for maintainability:

```python
class LoginPage:
    """Login page object."""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator("button[type='submit']")

    def login(self, username: str, password: str):
        """Perform login."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()

# Use in tests
def test_login(page: Page):
    login_page = LoginPage(page)
    login_page.login("test@example.com", "password123")
    expect(page).to_have_url("/dashboard")
```

## Common Test Patterns

### Authentication

```python
@pytest.fixture
def authenticated_page(page: Page):
    """Provide authenticated session."""
    page.goto("https://example.com/login")
    page.fill("#username", "test@example.com")
    page.fill("#password", "password")
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard")
    yield page
```

### File Operations

```python
# Upload
page.set_input_files("#file-input", "path/to/file.pdf")

# Download
with page.expect_download() as download_info:
    page.click("a:text('Download')")
download = download_info.value
download.save_as("downloads/file.pdf")
```

### Network Monitoring

```python
requests = []
page.on("request", lambda req: requests.append(req))
page.goto("https://example.com")

# Verify API calls were made
api_requests = [r for r in requests if "/api/" in r.url]
assert len(api_requests) > 0
```

## Running Tests

### Basic Commands

```bash
# Install Playwright
pip install playwright pytest-playwright
playwright install

# Run all tests
pytest tests/

# Run specific browser
pytest --browser chromium --browser firefox

# Run in headed mode (see browser)
pytest --headed

# Debug mode
PWDEBUG=1 pytest tests/test_login.py

# Parallel execution
pytest -n auto

# Generate test code
playwright codegen https://example.com
```

### Configuration

See `references/setup-configuration.md` for:
- Complete installation instructions
- Project structure setup
- pytest.ini configuration
- playwright.config.ts for TypeScript
- CI/CD integration examples

## Quality Standards

Ensure tests meet these criteria:
- Tests are independent and can run in any order
- Selectors are reliable (test IDs, semantic selectors)
- Proper error handling and assertions
- Screenshots/videos captured on failure
- No hardcoded waits (use auto-waiting)
- Clean state management between tests

## Additional Resources

### Detailed Documentation
- [Setup & Configuration](./references/setup-configuration.md) - Installation, project structure, and configuration
- [Best Practices](./references/best-practices.md) - Selector strategies, wait patterns, flaky test prevention
- [Common Pitfalls](./references/common-pitfalls.md) - Race conditions, selector brittleness, cleanup issues
- [CI/CD Integration](./references/ci-cd-integration.md) - GitHub Actions, Docker, deployment pipelines

### Code Examples
- [Login Testing](./examples/login-testing.md) - Authentication flows and session management
- [Form Testing](./examples/form-testing.md) - Form validation, file uploads, dropdowns
- [E-commerce Testing](./examples/ecommerce-testing.md) - Shopping cart, checkout flows, coupons
- [API Mocking](./examples/api-mocking.md) - Network interception, mocking, monitoring
- [Mobile Testing](./examples/mobile-testing.md) - Device emulation, touch events, responsive design
- [Page Object Model](./examples/page-object-model.md) - POM pattern implementation

### Helper Scripts
- [Playwright Helper](./scripts/playwright_helper.py) - Utility functions for common Playwright operations
- [Test Examples](./scripts/test_examples.py) - Complete test suite examples

### External Resources
- Official Documentation: https://playwright.dev
- Python API: https://playwright.dev/python/docs/intro
- TypeScript API: https://playwright.dev/docs/intro
- Best Practices: https://playwright.dev/docs/best-practices
- Community Discord: https://aka.ms/playwright/discord

## Troubleshooting

**Tests are flaky:**
- Use Playwright's auto-waiting instead of manual sleeps
- Ensure proper wait conditions (`wait_for_selector`, `wait_for_url`)
- Use `expect()` assertions which auto-retry

**Selectors not finding elements:**
- Verify element exists with browser DevTools
- Use Playwright Inspector: `PWDEBUG=1 pytest test.py`
- Try multiple selector strategies (text, role, test-id)

**Tests slow in CI:**
- Enable parallel execution: `pytest -n auto`
- Use headed mode only for debugging
- Consider browser context reuse for related tests

For more troubleshooting tips, see [Common Pitfalls](./references/common-pitfalls.md).
