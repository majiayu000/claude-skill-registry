---
name: detox-mobile-test
description: Эксперт Detox тестирования. Используй для React Native E2E tests и mobile automation.
---

# Detox Mobile Testing Expert

Эксперт по E2E тестированию React Native приложений с Detox.

## Core Testing Principles

### Synchronization
- Автоматическая синхронизация с React Native bridge
- Синхронизация с анимациями и сетевыми запросами
- `waitFor()` для явных ожиданий
- `toBeVisible()` вместо `toExist()` для стабильности

### Test Organization
- AAA pattern (Arrange, Act, Assert)
- Изоляция через `beforeEach()` и `afterEach()`
- `describe()` для группировки
- Page Object pattern для сложного UI

## Configuration

### .detoxrc.json

```json
{
  "testRunner": {
    "args": {
      "$0": "jest",
      "config": "e2e/jest.config.js"
    },
    "jest": {
      "setupTimeout": 120000
    }
  },
  "apps": {
    "ios.debug": {
      "type": "ios.app",
      "binaryPath": "ios/build/Build/Products/Debug-iphonesimulator/MyApp.app",
      "build": "xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build"
    },
    "ios.release": {
      "type": "ios.app",
      "binaryPath": "ios/build/Build/Products/Release-iphonesimulator/MyApp.app",
      "build": "xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Release -sdk iphonesimulator -derivedDataPath ios/build"
    },
    "android.debug": {
      "type": "android.apk",
      "binaryPath": "android/app/build/outputs/apk/debug/app-debug.apk",
      "build": "cd android && ./gradlew assembleDebug assembleAndroidTest -DtestBuildType=debug"
    },
    "android.release": {
      "type": "android.apk",
      "binaryPath": "android/app/build/outputs/apk/release/app-release.apk",
      "build": "cd android && ./gradlew assembleRelease assembleAndroidTest -DtestBuildType=release"
    }
  },
  "devices": {
    "simulator": {
      "type": "ios.simulator",
      "device": { "type": "iPhone 14" }
    },
    "emulator": {
      "type": "android.emulator",
      "device": { "avdName": "Pixel_4_API_30" }
    }
  },
  "configurations": {
    "ios.sim.debug": {
      "device": "simulator",
      "app": "ios.debug"
    },
    "ios.sim.release": {
      "device": "simulator",
      "app": "ios.release"
    },
    "android.emu.debug": {
      "device": "emulator",
      "app": "android.debug"
    },
    "android.emu.release": {
      "device": "emulator",
      "app": "android.release"
    }
  }
}
```

### Jest Config

```javascript
// e2e/jest.config.js
module.exports = {
  rootDir: '..',
  testMatch: ['<rootDir>/e2e/**/*.test.js'],
  testTimeout: 120000,
  maxWorkers: 1,
  globalSetup: 'detox/runners/jest/globalSetup',
  globalTeardown: 'detox/runners/jest/globalTeardown',
  reporters: ['detox/runners/jest/reporter'],
  testEnvironment: 'detox/runners/jest/testEnvironment',
  verbose: true
};
```

## Basic Test Structure

```javascript
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  afterAll(async () => {
    await device.terminateApp();
  });

  it('should login with valid credentials', async () => {
    // Arrange
    const email = 'test@example.com';
    const password = 'password123';

    // Act
    await element(by.id('email-input')).typeText(email);
    await element(by.id('password-input')).typeText(password);
    await element(by.id('login-button')).tap();

    // Assert
    await expect(element(by.id('home-screen'))).toBeVisible();
  });

  it('should show error for invalid credentials', async () => {
    // Arrange
    const email = 'wrong@example.com';
    const password = 'wrongpassword';

    // Act
    await element(by.id('email-input')).typeText(email);
    await element(by.id('password-input')).typeText(password);
    await element(by.id('login-button')).tap();

    // Assert
    await expect(element(by.id('error-message'))).toBeVisible();
    await expect(element(by.text('Invalid credentials'))).toBeVisible();
  });
});
```

## Element Matchers

```javascript
// By testID
element(by.id('submit-button'))

// By text
element(by.text('Submit'))

// By label (accessibility)
element(by.label('Submit form'))

// By type
element(by.type('RCTTextInput'))

// By traits (iOS)
element(by.traits(['button']))

// Combining matchers
element(by.id('item').withAncestor(by.id('list')))
element(by.id('item').withDescendant(by.text('Title')))

// Index for multiple matches
element(by.id('list-item')).atIndex(0)
```

## Actions

```javascript
// Tap
await element(by.id('button')).tap();
await element(by.id('button')).multiTap(2);
await element(by.id('button')).longPress();
await element(by.id('button')).longPress(2000); // 2 seconds

// Text input
await element(by.id('input')).typeText('Hello');
await element(by.id('input')).replaceText('New text');
await element(by.id('input')).clearText();

// Scroll
await element(by.id('scrollView')).scroll(200, 'down');
await element(by.id('scrollView')).scroll(200, 'up');
await element(by.id('scrollView')).scrollTo('bottom');
await element(by.id('scrollView')).scrollTo('top');

// Scroll until visible
await waitFor(element(by.id('item')))
  .toBeVisible()
  .whileElement(by.id('scrollView'))
  .scroll(200, 'down');

// Swipe
await element(by.id('card')).swipe('left');
await element(by.id('card')).swipe('right', 'fast', 0.9);

// Pinch
await element(by.id('map')).pinch(1.5); // zoom in
await element(by.id('map')).pinch(0.5); // zoom out
```

## Expectations

```javascript
// Visibility
await expect(element(by.id('view'))).toBeVisible();
await expect(element(by.id('view'))).not.toBeVisible();
await expect(element(by.id('view'))).toExist();
await expect(element(by.id('view'))).not.toExist();

// Focus
await expect(element(by.id('input'))).toBeFocused();

// Text
await expect(element(by.id('label'))).toHaveText('Hello');
await expect(element(by.id('input'))).toHaveValue('input value');

// Toggle state
await expect(element(by.id('switch'))).toHaveToggleValue(true);

// Slider
await expect(element(by.id('slider'))).toHaveSliderPosition(0.5);

// ID
await expect(element(by.id('view'))).toHaveId('view');

// Label
await expect(element(by.id('button'))).toHaveLabel('Submit');
```

## waitFor API

```javascript
// Wait for element to be visible
await waitFor(element(by.id('loading')))
  .not.toBeVisible()
  .withTimeout(10000);

// Wait for element to exist
await waitFor(element(by.id('data')))
  .toExist()
  .withTimeout(5000);

// Wait while scrolling
await waitFor(element(by.id('item-50')))
  .toBeVisible()
  .whileElement(by.id('list'))
  .scroll(100, 'down');

// Custom polling
await waitFor(element(by.id('result')))
  .toHaveText('Success')
  .withTimeout(30000);
```

## Page Object Pattern

```javascript
// e2e/pages/LoginPage.js
class LoginPage {
  get emailInput() {
    return element(by.id('email-input'));
  }

  get passwordInput() {
    return element(by.id('password-input'));
  }

  get loginButton() {
    return element(by.id('login-button'));
  }

  get errorMessage() {
    return element(by.id('error-message'));
  }

  async login(email, password) {
    await this.emailInput.typeText(email);
    await this.passwordInput.typeText(password);
    await this.loginButton.tap();
  }

  async assertErrorVisible(message) {
    await expect(this.errorMessage).toBeVisible();
    if (message) {
      await expect(element(by.text(message))).toBeVisible();
    }
  }
}

module.exports = new LoginPage();

// e2e/tests/login.test.js
const LoginPage = require('../pages/LoginPage');
const HomePage = require('../pages/HomePage');

describe('Login', () => {
  it('should login successfully', async () => {
    await LoginPage.login('user@test.com', 'password123');
    await expect(HomePage.welcomeMessage).toBeVisible();
  });
});
```

## Debugging

### Verbose Logging

```javascript
// In test
await device.launchApp({
  launchArgs: {
    detoxPrintBusyIdleResources: 'YES'
  }
});
```

### Screenshots

```javascript
// Take screenshot
await device.takeScreenshot('login-screen');

// On failure (in jest setup)
afterEach(async () => {
  if (jasmine.currentTest.failedExpectations.length > 0) {
    await device.takeScreenshot(`failed-${jasmine.currentTest.fullName}`);
  }
});
```

### Element Debugging

```javascript
// Get element attributes
const attributes = await element(by.id('button')).getAttributes();
console.log(attributes);
// { text: 'Submit', visible: true, enabled: true, ... }
```

## Handling Common Issues

### Disable Synchronization

```javascript
// For non-React Native screens (WebViews, etc.)
await device.disableSynchronization();
await element(by.id('webview-button')).tap();
await device.enableSynchronization();
```

### Permission Dialogs

```javascript
// iOS
await device.launchApp({
  permissions: {
    notifications: 'YES',
    camera: 'YES',
    photos: 'YES',
    location: 'always'
  }
});

// Android - handle at runtime
await element(by.text('Allow')).tap();
```

### Keyboard Issues

```javascript
// Dismiss keyboard
await element(by.id('input')).typeText('text\n');
// or
await device.pressBack(); // Android

// Avoid keyboard overlap
await element(by.id('input')).tap();
await element(by.id('input')).typeText('text');
await element(by.id('submit')).tap();
```

## CI/CD Integration

### GitHub Actions

```yaml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ios-e2e:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install pods
        run: cd ios && pod install

      - name: Build app
        run: npx detox build --configuration ios.sim.release

      - name: Run tests
        run: npx detox test --configuration ios.sim.release --cleanup

      - name: Upload artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: detox-artifacts
          path: artifacts/

  android-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '11'

      - name: Install dependencies
        run: npm ci

      - name: Build app
        run: npx detox build --configuration android.emu.release

      - name: Start emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 30
          target: google_apis
          script: npx detox test --configuration android.emu.release --cleanup
```

## Performance Tips

```javascript
// Use reloadReactNative instead of launchApp
beforeEach(async () => {
  await device.reloadReactNative(); // Fast
  // await device.launchApp({ newInstance: true }); // Slow
});

// Record videos only on failure
// In detoxrc.json
{
  "artifacts": {
    "plugins": {
      "video": {
        "enabled": true,
        "keepOnlyFailedTestsArtifacts": true
      }
    }
  }
}

// Test sharding for parallel execution
// jest.config.js
module.exports = {
  maxWorkers: process.env.CI ? 2 : 1,
  // ...
};
```

## Лучшие практики

1. **Stable selectors** — используйте testID, не text
2. **Proper waits** — waitFor вместо sleep
3. **Page Objects** — переиспользуемые абстракции
4. **Isolated tests** — каждый тест независим
5. **CI/CD first** — тесты должны работать в CI
6. **Record on failure** — видео/скриншоты при падении
