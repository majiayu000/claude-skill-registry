---
name: appium-mobile
description: "Automate mobile app testing with Appium for iOS and Android platforms. Use when writing or maintaining Appium test suites for native, hybrid, or mobile web applications across simulators, emulators, and cloud device farms."
allowed-tools: "Bash, Read, Write, Edit, Glob, Grep"
---

# Appium Mobile Testing

Automate iOS and Android testing using the Appium framework with WebDriverIO.

## When to Use

- Writing Appium test suites for native, hybrid, or mobile web apps
- Configuring Appium server capabilities for iOS (XCUITest) or Android (UiAutomator2)
- Integrating with cloud device farms (BrowserStack, Sauce Labs, AWS Device Farm)
- Implementing mobile-specific gestures (swipe, pinch, long-press)

## Server Configuration

Set up desired capabilities for your target platform:

```javascript
// iOS
const iosCaps = {
  platformName: 'iOS',
  'appium:automationName': 'XCUITest',
  'appium:deviceName': 'iPhone 14',
  'appium:app': './app/MyApp.ipa'
};

// Android
const androidCaps = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': 'Pixel 6',
  'appium:app': './app/MyApp.apk'
};
```

## Element Locator Strategies

Prefer resource/accessibility IDs over XPath for reliability:

| Strategy | iOS | Android |
|----------|-----|---------|
| **Accessibility ID** (preferred) | `accessibility id` | `accessibility id` |
| **Class chain** | `-ios class chain` | N/A |
| **Predicate** | `-ios predicate string` | N/A |
| **UI Automator** | N/A | `-android uiautomator` |
| **XPath** (last resort) | `xpath` | `xpath` |

## Gesture Handling

```javascript
// Swipe up
await driver.execute('mobile: swipe', { direction: 'up' });

// Long press
await driver.execute('mobile: longClickGesture', {
  elementId: element.elementId,
  duration: 2000
});
```

## Validation Steps

1. Verify app state after each action (`driver.queryAppState('com.app.id')`)
2. Assert screen orientation when relevant (`driver.getOrientation()`)
3. Wait for elements explicitly — avoid hard-coded sleeps

## Dependencies

- `appium` — Appium server (v2+)
- `webdriverio` — WebDriver client
- Xcode (iOS) or Android SDK (Android)
