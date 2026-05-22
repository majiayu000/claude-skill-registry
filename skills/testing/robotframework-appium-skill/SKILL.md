---
name: robotframework-appium-skill
description: Guide AI agents in creating AppiumLibrary tests for iOS and Android native apps, hybrid apps, and mobile browsers. Load when asked about mobile testing, Appium, or mobile app automation.
---

# AppiumLibrary Skill for Robot Framework

## Quick Reference

AppiumLibrary enables mobile app testing on iOS and Android using Appium automation.

## Installation

```bash
# Install the library
pip install robotframework-appiumlibrary

# Install Appium server (requires Node.js)
npm install -g appium

# Install platform drivers
appium driver install uiautomator2    # Android
appium driver install xcuitest        # iOS
```

## Appium Server

Appium server must be running before tests:

```bash
appium                    # Start with defaults
appium server             # Alternative
appium --port 4724        # Custom port
```

Default URL: `http://127.0.0.1:4723`

## Library Import

```robotframework
*** Settings ***
Library    AppiumLibrary
```

## Android Quick Start

### Open Android App

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=Android
...    platformVersion=13
...    deviceName=emulator-5554
...    automationName=UiAutomator2
...    app=${CURDIR}/app.apk
```

### Android Locators (Priority Order)

```robotframework
# 1. accessibility_id (RECOMMENDED - stable)
Click Element    accessibility_id=login_button

# 2. id (resource-id)
Click Element    id=com.example:id/login_button
Click Element    id=login_button                    # Short form if unique

# 3. xpath
Click Element    xpath=//android.widget.Button[@text='Login']

# 4. android UIAutomator2 selector
Click Element    android=new UiSelector().text("Login")

# 5. class name
Click Element    class=android.widget.Button
```

## iOS Quick Start

### Open iOS App

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=iOS
...    platformVersion=17.0
...    deviceName=iPhone 15
...    automationName=XCUITest
...    app=${CURDIR}/MyApp.app
...    udid=auto                                    # For real devices
```

### iOS Locators (Priority Order)

```robotframework
# 1. accessibility_id (RECOMMENDED - stable)
Click Element    accessibility_id=loginButton

# 2. name
Click Element    name=Login

# 3. ios predicate string
Click Element    ios=type == 'XCUIElementTypeButton' AND name == 'Login'

# 4. ios class chain (fast)
Click Element    ios=**/XCUIElementTypeButton[`name == 'Login'`]

# 5. xpath
Click Element    xpath=//XCUIElementTypeButton[@name='Login']

# 6. class name
Click Element    class=XCUIElementTypeButton
```

## Essential Keywords

### Element Interaction

```robotframework
Click Element           locator
Click Text              visible_text
Input Text              locator    text_to_enter
Clear Text              locator
Long Press              locator    duration=1000
```

### Getting Element Content

```robotframework
${text}=    Get Text              locator
${attr}=    Get Element Attribute    locator    attribute_name
${count}=   Get Matching Xpath Count    //android.widget.Button
```

### Waits

```robotframework
Wait Until Element Is Visible       locator    timeout=10s
Wait Until Page Contains            text       timeout=10s
Wait Until Page Contains Element    locator    timeout=10s
```

### Verification

```robotframework
Element Should Be Visible       locator
Element Should Be Enabled       locator
Page Should Contain Text        expected_text
Page Should Contain Element     locator
Element Text Should Be          locator    expected_text
```

### Screenshots

```robotframework
Capture Page Screenshot    filename.png
Capture Page Screenshot    ${OUTPUT_DIR}/screenshots/screen.png
```

## Get Page Source (View Hierarchy)

Useful for finding locators and debugging:

```robotframework
${source}=    Get Source
Log    ${source}
```

## Basic Gestures

```robotframework
# Scroll
Scroll Down
Scroll Up

# Swipe (start_x, start_y, end_x, end_y, duration_ms)
Swipe    500    1500    500    500    1000    # Swipe up

# Long press
Long Press    locator    duration=2000

# Tap coordinates
Click A Point    500    800
```

## Android Scroll to Element (UIAutomator2)

```robotframework
# Automatically scrolls to find element!
Click Element    android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Settings"))
```

## Context Switching (Hybrid Apps)

```robotframework
# Check current context
${context}=    Get Current Context
Log    Current: ${context}

# List all contexts
@{contexts}=    Get Contexts
Log Many    @{contexts}

# Switch to webview
Switch To Context    WEBVIEW_com.example.app

# Switch back to native
Switch To Context    NATIVE_APP
```

## Mobile Browser Testing

### Android Chrome

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=Android
...    deviceName=emulator-5554
...    automationName=UiAutomator2
...    browserName=Chrome

Go To Url    https://example.com
Input Text    id=username    admin
Click Element    css=button[type='submit']
```

### iOS Safari

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=iOS
...    deviceName=iPhone 15
...    automationName=XCUITest
...    browserName=Safari

Go To Url    https://example.com
```

## Session Management

```robotframework
# Close app but keep session
Close Application

# Close app and end session
Quit Application

# Reset app (clear data)
Reset Application

# Background/foreground
Background App    5    # Background for 5 seconds
```

## When to Load Additional References

Load additional references based on your needs:

| Need | Reference File |
|------|----------------|
| Android locator strategies | `references/locators-android.md` |
| iOS locator strategies | `references/locators-ios.md` |
| Device capabilities setup | `references/device-capabilities.md` |
| Gestures and scrolling | `references/gestures-touch.md` |
| iOS-specific features | `references/ios-specific.md` |
| Android-specific features | `references/android-specific.md` |
| Complete keyword list | `references/keywords-reference.md` |
| Common issues and solutions | `references/troubleshooting.md` |
