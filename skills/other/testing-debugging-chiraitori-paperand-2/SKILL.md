---
name: Testing and Debugging
description: Debug tools, developer menu, and troubleshooting
---

# Testing and Debugging

## Developer Menu

Access by tapping **Version number** in More > About **7 times**.

Features:
- Clear cache
- Reset settings
- View logs
- Export debug info
- Test notifications

## Console Logging

```typescript
// Basic logging
console.log('Info:', data);
console.warn('Warning:', message);
console.error('Error:', error);

// JSON pretty print
console.log(JSON.stringify(object, null, 2));

// Group logs
console.group('Loading manga');
console.log('Source:', sourceId);
console.log('Manga:', mangaId);
console.groupEnd();
```

View logs in:
- Metro bundler terminal
- React Native Debugger
- Flipper

## Developer Service

```typescript
import { developerService } from '../services/developerService';

// Check if dev mode enabled
const isDevMode = await developerService.isDevModeEnabled();

// Enable dev mode
await developerService.enableDevMode();

// Clear all data
await developerService.clearAllData();

// Export logs
const logs = await developerService.exportLogs();
```

## Common Issues

| Issue | Debug Steps |
|-------|-------------|
| Extension not loading | Check WebView console, verify URL |
| Images not showing | Check network, verify URLs, check cache |
| Crash on startup | Clear app data, check Metro logs |
| Slow performance | Profile with React DevTools |
| Downloads failing | Check storage space, permissions |

## Metro Bundler

```bash
# Start with cache clear
npx expo start -c

# Verbose output
npx expo start --verbose

# Reset cache completely
rm -rf node_modules/.cache
npx expo start -c
```

## React DevTools

```bash
# Install globally
npm install -g react-devtools

# Run
react-devtools
```

Then shake device and select "Debug with React DevTools".

## Network Debugging

```typescript
// Log all fetch requests (dev only)
if (__DEV__) {
  const originalFetch = global.fetch;
  global.fetch = async (...args) => {
    console.log('Fetch:', args[0]);
    const response = await originalFetch(...args);
    console.log('Response:', response.status);
    return response;
  };
}
```

## Performance Profiling

```typescript
// Measure render time
const start = performance.now();
// ... render
console.log(`Render took ${performance.now() - start}ms`);

// Use React.memo for expensive components
const MemoizedComponent = React.memo(ExpensiveComponent);

// Profile with why-did-you-render
if (__DEV__) {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React);
}
```

## Build Debugging

```bash
# Android - view build logs
cd android && ./gradlew assembleRelease --info

# iOS - verbose build
npx expo run:ios --verbose

# Check native dependencies
npx expo-doctor
```

## Crash Reports

```typescript
// Global error handler
ErrorUtils.setGlobalHandler((error, isFatal) => {
  console.error('Global error:', error);
  // Log to service
});

// Unhandled promise rejections
if (__DEV__) {
  require('promise/setimmediate/rejection-tracking').enable({
    allRejections: true,
    onUnhandled: (id, error) => {
      console.warn('Unhandled promise:', error);
    },
  });
}
```

## Test Builds

```bash
# Android debug APK
cd android && ./gradlew assembleDebug

# iOS simulator build
npx expo run:ios --configuration Debug

# EAS preview build
eas build --platform android --profile preview
```
