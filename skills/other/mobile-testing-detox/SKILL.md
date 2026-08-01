---
name: mobile-testing-detox
description: Detox E2E gray-box testing for React Native - matchers, actions, expectations, waitFor, device API, synchronization, mocking, artifacts, CI integration
---

# Detox E2E Testing Patterns

> **Quick Guide:** Detox is a gray-box E2E testing framework for React Native. It synchronizes with the app's JS thread, native UI, and network automatically -- eliminating flaky `sleep()` calls. Match elements with `by.id()` (preferred), act with `.tap()` / `.typeText()`, assert with `expect().toBeVisible()`. Use `waitFor().withTimeout()` only when automatic sync fails. Always add `testID` to interactive elements and forward it to native components. Mocking happens via Metro source extensions, not Jest mocks.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST add `testID` props to every interactive element and forward them to native components -- Detox cannot find custom components without forwarded testID)**

**(You MUST use `by.id()` as the primary matcher -- it is locale-agnostic, stable across UI changes, and decoupled from display text)**

**(You MUST call `waitFor().withTimeout()` only as a last resort -- Detox auto-synchronizes with JS, UI, and network by default)**

**(You MUST use Metro source extensions (`.mock.js` / `.e2e.js`) for mocking -- Jest mocks do not work in Detox E2E tests)**

**(You MUST set a `withTimeout()` on every `waitFor` call -- calling `waitFor` without a timeout does nothing)**

</critical_requirements>

---

**Auto-detection:** Detox, detox, .detoxrc.js, detox.config.js, by.id, by.text, by.label, element(), expect(), waitFor, device.launchApp, device.reloadReactNative, device.terminateApp, device.disableSynchronization, testID, E2E test React Native, gray-box testing, detox test, detox build

**When to use:**

- Writing end-to-end tests for React Native apps on iOS and Android
- Configuring Detox device, app, and artifact settings in `.detoxrc.js`
- Matching elements, performing actions, and asserting expectations
- Handling synchronization issues with animations or long-polling
- Mocking network responses or app configuration for E2E tests
- Setting up CI pipelines for automated Detox test runs
- Debugging flaky tests caused by synchronization problems

**Key patterns covered:**

- `.detoxrc.js` configuration (devices, apps, configurations, artifacts)
- Element matchers (`by.id`, `by.text`, `by.label`, compound matchers)
- Actions (`tap`, `typeText`, `scroll`, `swipe`, `longPress`)
- Expectations (`toBeVisible`, `toExist`, `toHaveText`, `not`)
- `waitFor` with polling and `withTimeout` for manual synchronization
- Device API (`launchApp`, `reloadReactNative`, `terminateApp`, biometrics)
- Mocking via Metro bundler source extensions
- Artifacts (screenshots, videos, logs) and CI integration
- testID strategy and naming conventions

**When NOT to use:**

- Unit or component testing (use your project's unit test runner)
- Web-only React applications (Detox is mobile-only)
- Apps built with Flutter, Swift, or Kotlin (Detox is React Native focused)
- Simple snapshot or render tests (use component testing tools)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Matchers, actions, expectations, waitFor, testID strategy
- [examples/synchronization.md](examples/synchronization.md) - Animation handling, manual sync, debug synchronization
- [examples/ci-artifacts.md](examples/ci-artifacts.md) - Artifacts configuration, CI workflows, mocking with Metro
- [reference.md](reference.md) - Decision frameworks, matcher/action/expectation tables, checklists

---

<philosophy>

## Philosophy

Detox is a **gray-box** E2E testing framework -- it has internal knowledge of your app's state (JS thread idle, animations complete, network requests finished) and automatically synchronizes with it. This is what makes Detox tests dramatically less flaky than black-box alternatives that rely on arbitrary `sleep()` calls.

**Core principles:**

1. **Automatic synchronization first** - Detox waits for the app to be idle before each interaction. Only use `waitFor` when auto-sync genuinely fails (looping animations, long-polling).
2. **testID is the primary matcher** - `by.id()` is stable across locale changes, text updates, and layout shifts. `by.text()` and `by.label()` are fragile fallbacks.
3. **Gray-box over black-box** - Detox can access app internals via launch arguments and Metro mocking. Use this advantage instead of fighting the framework.
4. **Mock at the boundary** - Mocking in Detox happens through Metro source extensions (`.mock.js`), not Jest mocks. The app runs for real; only external dependencies are swapped.
5. **Fail fast, debug visually** - Use artifacts (screenshots on failure, video recordings) to diagnose issues. Enable `--debug-synchronization` to find what blocks the idle loop.

**Mental model:**

Detox tests should read like a user script: navigate, interact, verify. The framework handles timing. If you find yourself adding manual waits, something is wrong -- either an animation loop, a long-polling connection, or a synchronization issue that should be fixed at the source.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: .detoxrc.js Configuration

The config file defines devices, apps, and test configurations. Keep configs in three dictionaries: `devices`, `apps`, and `configurations`.

```javascript
// .detoxrc.js -- three key dictionaries: devices, apps, configurations
/** @type {import('detox').DetoxConfig} */
module.exports = {
  testRunner: { args: { $0: "jest", config: "e2e/jest.config.js" } },
  apps: {
    "ios.debug": {
      type: "ios.app",
      binaryPath: "ios/build/.../MyApp.app",
      build: "xcodebuild ...",
    },
    "android.debug": {
      type: "android.apk",
      binaryPath: "android/.../app-debug.apk",
      build: "cd android && ./gradlew ...",
      reversePorts: [8081],
    },
  },
  devices: {
    simulator: { type: "ios.simulator", device: { type: "iPhone 16" } },
    emulator: {
      type: "android.emulator",
      device: { avdName: "Pixel_7_API_34" },
    },
  },
  configurations: {
    "ios.sim.debug": { device: "simulator", app: "ios.debug" },
    "android.emu.debug": { device: "emulator", app: "android.debug" },
  },
};
```

**Why good:** JSDoc for autocomplete, separate device/app/config concerns, `reversePorts` for Android Metro, both platforms configured

See [examples/ci-artifacts.md](examples/ci-artifacts.md) for artifacts and CI-specific configuration.

---

### Pattern 2: Element Matchers

Match elements using `by.id()` (preferred), `by.text()`, `by.label()`, or compound matchers. Always prefer `by.id()` -- it is locale-agnostic and decoupled from display text.

```typescript
// Preferred: by.id matches testID prop
element(by.id("login-button"));

// Text matching (fragile -- breaks on locale change)
element(by.text("Submit"));

// Accessibility label
element(by.label("Close dialog"));

// Compound: element with id AND text
element(by.id("greeting").and(by.text("Hello")));

// Hierarchy: child within parent
element(by.id("item-title").withAncestor(by.id("product-list")));

// Multiple matches: select by index (0-based)
element(by.text("Add to cart")).atIndex(1);
```

**Why good:** `by.id()` is decoupled from UI text, survives refactors, works across locales

See [examples/core.md](examples/core.md) for full matcher examples including regex support.

---

### Pattern 3: Actions

Simulate user interactions: tap, type, scroll, swipe. Actions auto-wait for the element to exist and the app to be idle.

```typescript
// Tap
await element(by.id("submit-btn")).tap();

// Type text (uses keyboard simulation)
await element(by.id("email-input")).typeText("user@example.com");

// Replace text (no keyboard, faster)
await element(by.id("search-input")).replaceText("new query");

// Clear and retype
await element(by.id("name-input")).clearText();
await element(by.id("name-input")).typeText("New Name");

// Scroll down 300 points
await element(by.id("scroll-view")).scroll(300, "down");

// Swipe left
await element(by.id("card")).swipe("left", "fast");
```

**Why good:** actions auto-synchronize, typeText simulates real keyboard (triggers onChangeText), replaceText is faster for pre-filling

See [examples/core.md](examples/core.md) for long press, multi-tap, scroll-to-edge, and date picker actions.

---

### Pattern 4: Expectations

Verify element state after interactions. Expectations also auto-synchronize.

```typescript
// Visibility (default: 75% visible threshold)
await expect(element(by.id("welcome-banner"))).toBeVisible();

// Existence in hierarchy (may not be visible)
await expect(element(by.id("hidden-data"))).toExist();

// Text content
await expect(element(by.id("greeting"))).toHaveText("Hello, World");

// Negation
await expect(element(by.id("error-message"))).not.toBeVisible();
await expect(element(by.id("deleted-item"))).not.toExist();

// Toggle/switch state
await expect(element(by.id("notifications-toggle"))).toHaveToggleValue(true);
```

**Why good:** auto-synchronization before assertion, `.not` for negative checks, `toBeVisible` checks actual screen visibility (not just hierarchy existence)

See [examples/core.md](examples/core.md) for slider position, custom visibility threshold, and `toHaveValue`.

---

### Pattern 5: waitFor with Polling

`waitFor` polls an expectation repeatedly until it passes or times out. **Every `waitFor` must have a `withTimeout()`** -- without it, the call does nothing.

```typescript
const LOGIN_TIMEOUT_MS = 5000;
const SCROLL_AMOUNT = 100;

// Wait for element to appear (e.g., after network request)
await waitFor(element(by.id("dashboard")))
  .toBeVisible()
  .withTimeout(LOGIN_TIMEOUT_MS);

// Scroll until element is visible
await waitFor(element(by.id("item-42")))
  .toBeVisible()
  .whileElement(by.id("item-list"))
  .scroll(SCROLL_AMOUNT, "down");
```

**Why good:** named timeout constant, `whileElement` scrolls automatically until found, no manual sleep loops

See [examples/synchronization.md](examples/synchronization.md) for when to use waitFor vs fixing synchronization.

---

### Pattern 6: Device API

Control the device and app lifecycle between tests.

```typescript
// Reset app state between tests
beforeEach(async () => {
  await device.reloadReactNative();
});

// Full relaunch (slower but more thorough)
beforeEach(async () => {
  await device.launchApp({ newInstance: true });
});

// Launch with deep link
await device.launchApp({ url: "myapp://profile/123", newInstance: true });

// Launch with custom arguments (accessible via launch args in app)
await device.launchApp({
  launchArgs: { mockServerPort: "9090" },
});

// Background and foreground
await device.sendToHome();
await device.launchApp({ newInstance: false });

// Take screenshot
await device.takeScreenshot("after-login");
```

**Why good:** `reloadReactNative` is faster than full relaunch, `newInstance: true` ensures clean state, `launchArgs` enables runtime configuration for mocking

See [examples/core.md](examples/core.md) for biometrics, permissions, and `terminateApp`.

---

### Pattern 7: testID Strategy

Add `testID` to every interactive element. Forward it through custom components to native components.

```tsx
// Native component: testID works directly
<Pressable testID="settings-btn" onPress={openSettings}>
  <Text>Settings</Text>
</Pressable>;

// Custom component: MUST forward testID to a native component
interface CardProps {
  testID?: string;
  title: string;
  onPress: () => void;
}

function Card({ testID, title, onPress }: CardProps) {
  return (
    <Pressable testID={testID} onPress={onPress}>
      <Text testID={testID ? `${testID}.title` : undefined}>{title}</Text>
    </Pressable>
  );
}

// Usage: derived child IDs with dot notation
<Card testID="product-card" title="Widget" onPress={handlePress} />;
// Matches: by.id("product-card"), by.id("product-card.title")
```

**Why good:** dot-notation hierarchy, custom components forward testID, child elements get derived IDs for granular matching

See [examples/core.md](examples/core.md) for naming conventions and list item testID patterns.

---

### Pattern 8: Mocking with Metro Source Extensions

Detox mocking uses Metro bundler to swap module implementations. Jest mocks do not work in E2E tests.

```javascript
// src/api/client.js - production
export const API_URL = "https://api.production.com";

// src/api/client.mock.js - test override
export * from "./client.js";
export const API_URL = "http://localhost:9090";
```

Start Metro with mock extensions:

```bash
npx react-native start --sourceExts mock.js,js,json,ts,tsx
```

**Why good:** production code unchanged, Metro resolves `.mock.js` first, test-specific behavior without conditionals in production code

See [examples/ci-artifacts.md](examples/ci-artifacts.md) for environment-based Metro config and mock server patterns.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Matcher to Use

```
Need to find an element?
|
+-> Has a testID?
|   +-> YES -> by.id("testID")  (always preferred)
|   +-> NO  -> Can you add one?
|       +-> YES -> Add testID, use by.id()
|       +-> NO  -> Continue...
|
+-> Has unique visible text?
|   +-> YES -> by.text("exact text")
|   +-> NO  -> by.label("accessibility label")
|
+-> Multiple matches?
    +-> Use .atIndex(n) or compound matchers:
        by.id("x").withAncestor(by.id("parent"))
```

### When to Use waitFor vs Fix Synchronization

```
Test is flaky / element not found?
|
+-> Is there a looping animation?
|   +-> YES -> Mock the animation in tests (Metro extension)
|              or disable via launch arg
|
+-> Is there a long-polling / WebSocket connection?
|   +-> YES -> device.setURLBlacklist([".*long-poll.*"])
|
+-> Is there a setTimeout loop?
|   +-> YES -> Convert to setInterval (Detox ignores setInterval)
|
+-> None of the above?
    +-> Use waitFor().toBeVisible().withTimeout(ms)
    +-> Enable --debug-synchronization to find the blocker
```

### Test Lifecycle Strategy

```
How to reset between tests?
|
+-> Need clean JS state only?
|   +-> device.reloadReactNative()  (fast, reloads JS bundle)
|
+-> Need clean app data + permissions?
|   +-> device.launchApp({ delete: true })  (reinstalls app)
|
+-> Need clean device state?
    +-> device.resetContentAndSettings()  (full simulator reset, iOS)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `sleep()` or manual delays instead of Detox auto-synchronization -- Detox waits for idle automatically; sleep masks real issues
- Calling `waitFor()` without `.withTimeout()` -- does nothing, silently passes without waiting
- Using `by.text()` as the primary matcher -- breaks on locale changes and text updates; use `by.id()`
- Adding `testID` to a custom component without forwarding to a native component -- Detox cannot find it
- Using Jest mocks (`jest.mock()`) in Detox tests -- E2E tests run in the app process, not Jest; use Metro source extensions

**Medium Priority Issues:**

- Using `device.launchApp({ delete: true })` in every `beforeEach` -- extremely slow; use `reloadReactNative()` unless you need clean storage
- Not using `--record-videos failing` and `--take-screenshots failing` in CI -- makes debugging failed CI tests impossible
- Hardcoded timeout values -- use named constants (`LOGIN_TIMEOUT_MS`, not `5000`)
- Using `by.type()` for matching -- platform-specific class names differ between iOS and Android

**Gotchas & Edge Cases:**

- `toBeVisible()` checks 75% screen visibility by default -- an element can `toExist()` but not `toBeVisible()` if it is offscreen or obscured
- `typeText()` requires the element to be focused first on some platforms -- tap the input before typing if `typeText` fails
- `by.traits()` is iOS only -- no Android equivalent exists
- `reloadReactNative()` does not clear AsyncStorage, MMKV, or other persistent storage -- use `launchApp({ delete: true })` for that
- Looping animations (spinners, pulse effects) block Detox synchronization indefinitely -- mock them or use `disableSynchronization()` + `waitFor`
- `setURLBlacklist` accepts an array of regex strings, not plain URLs -- escape dots and slashes properly
- Android emulator tests need `reversePorts: [8081]` in the app config or Metro bundler is unreachable
- `device.disableSynchronization()` is global -- always re-enable with `device.enableSynchronization()` in an `afterEach` or `finally` block
- `getAttributes()` returns different shapes on iOS vs Android -- check platform before accessing specific fields
- FlashList/FlatList items may not have `testID` accessible until scrolled into view -- use `waitFor().whileElement().scroll()` pattern

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST add `testID` props to every interactive element and forward them to native components -- Detox cannot find custom components without forwarded testID)**

**(You MUST use `by.id()` as the primary matcher -- it is locale-agnostic, stable across UI changes, and decoupled from display text)**

**(You MUST call `waitFor().withTimeout()` only as a last resort -- Detox auto-synchronizes with JS, UI, and network by default)**

**(You MUST use Metro source extensions (`.mock.js` / `.e2e.js`) for mocking -- Jest mocks do not work in Detox E2E tests)**

**(You MUST set a `withTimeout()` on every `waitFor` call -- calling `waitFor` without a timeout does nothing)**

**Failure to follow these rules will produce flaky tests, unmatchable elements, and silent test passes that verify nothing.**

</critical_reminders>
