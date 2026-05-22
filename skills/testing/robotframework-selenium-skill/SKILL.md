---
name: robotframework-selenium-skill
description: Generate Robot Framework tests using SeleniumLibrary for browser automation with Selenium WebDriver. Use when asked to create web UI tests, automate browsers, interact with forms, handle multiple windows/frames, or execute JavaScript.
---

# SeleniumLibrary Skill

Create browser automation tests using SeleniumLibrary with Selenium WebDriver.

## Quick Reference

SeleniumLibrary provides browser automation using Selenium WebDriver. Unlike Browser Library, explicit waits are often required for reliable test execution.

## Installation

```bash
pip install robotframework-seleniumlibrary
```

WebDriver binaries (chromedriver, geckodriver, etc.) must be in PATH or use webdriver-manager:

```bash
pip install webdriver-manager
```

## Library Import

```robotframework
*** Settings ***
Library    SeleniumLibrary    timeout=10s    implicit_wait=0s
```

### Import Options

| Option | Default | Description |
|--------|---------|-------------|
| timeout | 5s | Default timeout for wait keywords |
| implicit_wait | 0s | Implicit wait (not recommended) |
| run_on_failure | Capture Page Screenshot | Keyword to run on failure |
| screenshot_root_directory | None | Directory for screenshots |
| plugins | None | Plugin modules to load |

## WebDriver Setup Options

### Chrome

```robotframework
# Basic
Open Browser    ${URL}    chrome

# Headless
Open Browser    ${URL}    headless_chrome

# With Options
Open Browser    ${URL}    chrome    options=add_argument("--headless");add_argument("--no-sandbox")

# With WebDriver Manager
Open Browser    ${URL}    chrome    executable_path=${DRIVER_PATH}
```

### Firefox

```robotframework
Open Browser    ${URL}    firefox
Open Browser    ${URL}    headless_firefox
Open Browser    ${URL}    firefox    options=add_argument("--headless")
```

### Edge

```robotframework
Open Browser    ${URL}    edge
Open Browser    ${URL}    headless_edge
```

## Locator Strategies

SeleniumLibrary requires strategy prefixes except for id and name attributes.

| Strategy | Syntax | Example |
|----------|--------|---------|
| id | `id=value` or `value` | `id=username` or `username` |
| name | `name=value` or `value` | `name=email` |
| xpath | `xpath=expression` | `xpath=//button[@type='submit']` |
| css | `css=selector` | `css=button.primary` |
| class | `class=name` | `class=submit-btn` |
| tag | `tag=name` | `tag=button` |
| link | `link=text` | `link=Click here` |
| partial link | `partial link=text` | `partial link=Click` |
| dom | `dom=expression` | `dom=document.forms[0]` |
| jquery | `jquery=selector` | `jquery=button:visible` |
| data | `data=attr:value` | `data=testid:submit` |
| default | (no prefix) | `username` (tries id, then name) |

### Locator Priority (recommended)

1. id - Unique, fastest
2. data-testid - Stable, test-specific
3. name - Often stable
4. css - Flexible, readable
5. xpath - Powerful but fragile
6. link - For anchor text

## Core Keywords Quick Reference

### Browser Control

```robotframework
Open Browser         ${URL}    chrome
Close Browser
Close All Browsers
Maximize Browser Window
Set Window Size      1920    1080
```

### Navigation

```robotframework
Go To                ${URL}
Go Back
Go Forward
Reload Page
${url}=    Get Location
${title}=  Get Title
```

### Element Interaction

```robotframework
Click Element        css=button.submit
Click Button         id=submit
Click Link           link=Home
Input Text           id=username    myuser
Input Password       id=password    secret
Clear Element Text   id=search
Press Keys           id=search    RETURN
Press Keys           None    CTRL+a
```

### Dropdowns

```robotframework
Select From List By Value    id=country    US
Select From List By Label    id=country    United States
Select From List By Index    id=country    0
Unselect From List By Value  id=items      item1
```

### Checkboxes and Radio Buttons

```robotframework
Select Checkbox      id=agree
Unselect Checkbox    id=newsletter
Select Radio Button  gender    male
```

### Getting Content

```robotframework
${text}=     Get Text              css=h1.title
${value}=    Get Value             id=email
${attr}=     Get Element Attribute    css=a.link    href
${count}=    Get Element Count     css=.item
@{elements}= Get WebElements       css=.item
```

## Waiting Keywords (Critical)

SeleniumLibrary does NOT auto-wait. Always use explicit waits.

### Element Waits

```robotframework
Wait Until Element Is Visible         css=.results    timeout=10s
Wait Until Element Is Not Visible     css=.loader
Wait Until Element Is Enabled         id=submit
Wait Until Page Contains Element      css=.loaded
Wait Until Page Does Not Contain Element    css=.spinner
```

### Text Waits

```robotframework
Wait Until Page Contains              Success
Wait Until Page Does Not Contain      Loading
Wait Until Element Contains           css=h1    Welcome
Wait Until Element Does Not Contain   css=.status    Pending
```

### Element Count Waits

```robotframework
Wait Until Element Count Is                   css=.item    5
Wait Until Element Count Is Greater Than      css=.item    0
Wait Until Element Count Is Less Than         css=.item    10
```

## Verification Keywords

```robotframework
Element Should Be Visible     css=.success
Element Should Not Be Visible css=.error
Element Should Be Enabled     id=submit
Element Should Be Disabled    id=submit
Element Should Contain        css=h1    Welcome
Element Text Should Be        css=.title    Exact Title
Page Should Contain           Login successful
Page Should Not Contain       Error
Checkbox Should Be Selected   id=agree
```

## Common Patterns

### Login with Explicit Waits

```robotframework
*** Keywords ***
Login
    [Arguments]    ${username}    ${password}
    Open Browser    ${LOGIN_URL}    chrome
    Wait Until Element Is Visible    id=username
    Input Text      id=username    ${username}
    Input Password  id=password    ${password}
    Click Button    id=submit
    Wait Until Page Contains    Welcome
```

### Form Submission with Validation

```robotframework
*** Keywords ***
Submit Form And Verify Error
    Input Text    id=email    invalid-email
    Click Button    id=submit
    Wait Until Element Is Visible    css=.error-message
    Element Should Contain    css=.error-message    valid email
```

### Wait for AJAX Content

```robotframework
*** Keywords ***
Load And Verify Data
    Click Element    id=load-data
    Wait Until Element Is Not Visible    css=.spinner    timeout=30s
    Wait Until Element Is Visible    css=.data-table
    Wait Until Element Count Is Greater Than    css=.data-row    0
```

### Table Cell Interaction

```robotframework
*** Keywords ***
Click Table Cell
    [Arguments]    ${table_id}    ${row}    ${col}
    Click Element    xpath=//table[@id='${table_id}']//tr[${row}]//td[${col}]

Get Table Cell Value
    [Arguments]    ${table_id}    ${row}    ${col}
    ${text}=    Get Text    xpath=//table[@id='${table_id}']//tr[${row}]//td[${col}]
    RETURN    ${text}
```

## Screenshot Capture

```robotframework
Capture Page Screenshot
Capture Page Screenshot    ${OUTPUT_DIR}/screenshot.png
Capture Element Screenshot    css=.error-panel    error.png
```

## JavaScript Execution

```robotframework
Execute JavaScript    window.scrollTo(0, document.body.scrollHeight)
${result}=    Execute JavaScript    return document.title
Execute JavaScript    arguments[0].click()    ARGUMENTS    ${element}
```

## When to Load Additional References

Load specific reference files based on task requirements:

| Task | Reference File |
|------|----------------|
| Complex locator strategies | `references/locators.md` |
| Timing and wait patterns | `references/waiting-strategies.md` |
| Complete keyword list | `references/keywords-reference.md` |
| WebDriver configuration | `references/webdriver-setup.md` |
| Multiple windows/tabs | `references/frames-windows.md` |
| JavaScript interactions | `references/javascript-execution.md` |
| Screenshot/logging | `references/screenshots-logs.md` |
| Debugging test failures | `references/troubleshooting.md` |

## Example Test Structure

```robotframework
*** Settings ***
Library           SeleniumLibrary    timeout=10s
Suite Setup       Open Browser    ${URL}    chrome
Suite Teardown    Close All Browsers
Test Setup        Go To    ${URL}

*** Variables ***
${URL}            https://example.com
${BROWSER}        chrome

*** Test Cases ***
User Can Login With Valid Credentials
    [Documentation]    Verify successful login flow
    Wait Until Element Is Visible    id=username
    Input Text        id=username    testuser
    Input Password    id=password    testpass
    Click Button      id=login
    Wait Until Page Contains    Welcome
    Element Should Be Visible    css=.dashboard

*** Keywords ***
Open Login Page
    Go To    ${URL}/login
    Wait Until Element Is Visible    id=username
```
