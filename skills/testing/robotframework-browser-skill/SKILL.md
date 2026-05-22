---
name: robotframework-browser-skill
description: Guide AI agents in creating Browser Library tests using Playwright-powered automation with auto-waiting, assertion engine, and modern web features. Use when asked to create web tests with Browser Library, handle locators, assertions, iframes, Shadow DOM, or multi-tab scenarios.
---

# Browser Library Skill

## Quick Reference

Browser Library uses Playwright for fast, reliable browser automation with built-in auto-waiting and powerful assertion capabilities.

## Installation

```bash
pip install robotframework-browser
rfbrowser init
```

## Library Import

```robotframework
*** Settings ***
Library    Browser    auto_closing_level=KEEP
```

Import options:
- `auto_closing_level=KEEP` - Keep browser open between tests (faster)
- `auto_closing_level=TEST` - Close after each test (clean state)
- `timeout=30s` - Default timeout for operations
- `enable_presenter_mode=true` - Slow down for demos

## Essential Concepts

### Browser -> Context -> Page Hierarchy

```
Browser (chromium/firefox/webkit)
  └── Context (isolated session: cookies, storage)
        └── Page (single tab/window)
```

- **Browser**: The browser process (Chrome, Firefox, or WebKit)
- **Context**: Isolated browser session with its own cookies, localStorage, and cache
- **Page**: A single tab or popup window within a context

```robotframework
New Browser    chromium    headless=false
New Context    viewport={'width': 1920, 'height': 1080}
New Page       https://example.com
```

### Auto-Waiting

Browser Library automatically waits for elements to be actionable before interacting. No explicit waits needed in most cases.

- Waits for element to be visible
- Waits for element to be stable (not animating)
- Waits for element to be enabled
- Waits for element to receive events

## Core Keywords Quick Reference

### Navigation

```robotframework
New Browser    chromium    headless=false
New Context    viewport={'width': 1920, 'height': 1080}
New Page       https://example.com
Go To          https://example.com/login
Reload
Go Back
Go Forward
```

### Locators (Selector Syntax)

```robotframework
# CSS (default)
Click    button.submit
Click    #login-btn
Click    [data-testid="submit"]

# Text
Click    text=Login
Click    "Login"              # Exact text match

# XPath
Click    xpath=//button[@type='submit']

# Chained selectors (powerful!)
Click    .form >> button.submit
Click    #container >> text=Save

# nth-match
Click    button >> nth=0      # First button
Click    button >> nth=-1     # Last button

# Role selectors (accessibility)
Click    role=button[name="Submit"]
```

### Input

```robotframework
Fill             input#username    myuser
Type Text        input#password    secret123    delay=50ms
Check Checkbox   #remember-me
Uncheck Checkbox    #newsletter
Select Options By    select#country    value    US
Select Options By    select#country    label    United States
Clear Text       input#search
```

### Getting Content

```robotframework
${text}=     Get Text           h1.title
${value}=    Get Property       input#email    value
${attr}=     Get Attribute      a.link    href
${count}=    Get Element Count  li.item
${states}=   Get Element States button#submit
```

### Assertions (built-in!)

```robotframework
Get Text           h1              ==           Welcome
Get Text           .message        contains     Success
Get Text           .message        *=           Success     # Alternative
Get Element Count  li.item         >            5
Get Url                            contains     /dashboard
Get Title                          ==           Home Page
```

### Screenshots

```robotframework
Take Screenshot                              # Current viewport
Take Screenshot    fullPage=true             # Full page
Take Screenshot    selector=#main            # Specific element
Take Screenshot    filename=test.png         # Named file
```

### Waiting (when auto-wait isn't enough)

```robotframework
Wait For Elements State    .results    visible    timeout=10s
Wait For Elements State    .spinner    hidden
Wait For Response          **/api/data    timeout=30s
Wait For Navigation        url=**/success
Wait For Load State        networkidle
```

## Locator Strategy Priority

1. `data-testid`, `data-test`, `data-cy` attributes - Most stable
2. Accessible roles and labels - `role=button[name="Submit"]`
3. CSS selectors - `button.submit`, `#login-btn`
4. Text content - `text=Login`, `"Exact Text"`
5. XPath - Last resort: `xpath=//button[@type='submit']`

## Common Patterns

### Login Flow

```robotframework
*** Keywords ***
Login As User
    [Arguments]    ${username}    ${password}
    New Page       ${LOGIN_URL}
    Fill           input[name="username"]    ${username}
    Fill           input[name="password"]    ${password}
    Click          button[type="submit"]
    Get Url        contains    /dashboard
```

### Wait for Network

```robotframework
Click    button#load-data
Wait For Response    **/api/data    timeout=10s
Get Text    .data-container    !=    ${EMPTY}
```

### Handle Loading States

```robotframework
Click    button#submit
Wait For Elements State    .loading-spinner    hidden    timeout=30s
Get Text    .result    contains    Success
```

### Form Validation

```robotframework
Fill     input#email    invalid-email
Click    button[type="submit"]
Get Text    .error-message    contains    valid email

Clear Text    input#email
Fill          input#email    valid@example.com
Click         button[type="submit"]
Get Url       contains    /success
```

### Screenshot on Failure

```robotframework
*** Settings ***
Library    Browser    auto_closing_level=TEST
Test Teardown    Run Keyword If Test Failed    Take Screenshot
```

## When to Load Additional References

Load these reference files when you need deeper knowledge:

| Need | Reference File |
|------|----------------|
| Complex locators, chaining, nth-match | `references/locators.md` |
| Assertion operators, retry logic | `references/assertion-engine.md` |
| Browser/Context/Page management | `references/browser-context-page.md` |
| Complete keyword reference | `references/keywords-reference.md` |
| iframes and Shadow DOM | `references/iframes-shadow-dom.md` |
| Multiple tabs/windows | `references/tabs-windows.md` |
| Session persistence, cookies | `references/authentication-storage.md` |
| File download/upload | `references/downloads-uploads.md` |
| Debugging test failures | `references/troubleshooting.md` |
