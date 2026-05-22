---
name: mobile-debugging
description: React Native debugging with Flipper, React DevTools, and crash analysis. Use for mobile app debugging or network request issues.
---

# Mobile Debugging Expert

Specialized in debugging React Native and Expo applications across iOS and Android platforms. Expert in using debugging tools, analyzing crashes, network debugging, and troubleshooting common React Native issues.

## What I Know

### Debugging Tools

**React DevTools**
- Component tree inspection
- Props and state inspection
- Profiler for performance analysis
- Component re-render tracking
- Installation: `npm install -g react-devtools`
- Usage: `react-devtools` before starting app

**Chrome DevTools (Remote Debugging)**
- JavaScript debugger access
- Breakpoints and step-through debugging
- Console for logging and evaluation
- Network tab for API inspection
- Source maps for original code navigation

**Flipper (Meta's Debugging Platform)**
- Layout inspector for UI debugging
- Network inspector with request/response details
- Logs viewer with filtering
- React DevTools plugin integration
- Database inspector
- Crash reporter integration
- Performance metrics monitoring

**React Native Debugger (Standalone)**
- All-in-one debugging solution
- Redux DevTools integration
- React DevTools integration
- Network inspection
- AsyncStorage inspection

### Debugging Techniques

**Console Logging Strategies**
```javascript
// Basic logging
console.log('Debug:', value);

// Structured logging
console.log({
  component: 'UserProfile',
  action: 'loadData',
  userId: user.id,
  timestamp: new Date().toISOString()
});

// Conditional logging
if (__DEV__) {
  console.log('Development only:', debugData);
}

// Performance logging
console.time('DataLoad');
await fetchData();
console.timeEnd('DataLoad');

// Table logging for arrays
console.table(users);
```

**Breakpoint Debugging**
```javascript
// Debugger statement
function processData(data) {
  debugger; // Execution pauses here when debugger attached
  return data.map(item => transform(item));
}

// Conditional breakpoints in DevTools
// Right-click on line number → Add conditional breakpoint
// Condition: userId === '12345'
```

**Error Boundaries**
```javascript
import React from 'react';
import { View, Text } from 'react-native';

class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log to error tracking service
    console.error('Error caught:', error, errorInfo);
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <View>
          <Text>Something went wrong.</Text>
          <Text>{this.state.error?.message}</Text>
        </View>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### Network Debugging

**Intercepting Network Requests**
```javascript
// Using Flipper (recommended)
// Automatically intercepts fetch() and XMLHttpRequest

// Manual interception for custom debugging
const originalFetch = global.fetch;
global.fetch = async (...args) => {
  console.log('Fetch Request:', args[0], args[1]);
  const response = await originalFetch(...args);
  console.log('Fetch Response:', response.status);
  return response;
};

// Using React Native Debugger Network tab
// Automatically works with fetch() and axios
```

**API Response Debugging**
```javascript
// Wrapper for API calls with detailed logging
async function apiCall(endpoint, options = {}) {
  const startTime = Date.now();

  try {
    const response = await fetch(endpoint, options);
    const duration = Date.now() - startTime;

    console.log({
      endpoint,
      method: options.method || 'GET',
      status: response.status,
      duration: `${duration}ms`,
      success: response.ok
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('API Error Response:', error);
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Call Failed:', {
      endpoint,
      error: error.message,
      duration: `${Date.now() - startTime}ms`
    });
    throw error;
  }
}
```

### Platform-Specific Debugging

**iOS Debugging**
- Safari Web Inspector for JSContext debugging
- Xcode Console for native logs
- Instruments for performance profiling
- Crash logs: `~/Library/Logs/DiagnosticReports/`
- System logs: `log stream --predicate 'processImagePath contains "MyApp"'`

**Android Debugging**
- Chrome DevTools for JavaScript debugging
- Android Studio Logcat for system logs
- ADB logcat filtering: `adb logcat *:E` (errors only)
- Native crash logs: `adb logcat AndroidRuntime:E`
- Monitoring device: `adb shell top`

### Common Debugging Scenarios

**App Crashes on Startup**
```bash
# iOS: Check Xcode console
# Open Xcode → Window → Devices and Simulators → Select device → View logs

# Android: Check logcat
adb logcat *:E

# Look for:
# - Missing native modules
# - JavaScript bundle errors
# - Permission issues
# - Initialization errors
```

**White Screen / Blank Screen**
```javascript
// Add error boundary to root
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error }) {
  return (
    <View>
      <Text>App crashed: {error.message}</Text>
    </View>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <App />
</ErrorBoundary>
```

**Red Screen Errors**
```javascript
// Globally catch errors in development
if (__DEV__) {
  ErrorUtils.setGlobalHandler((error, isFatal) => {
    console.log('Global Error:', { error, isFatal });
    // Log to crash reporting service in production
  });
}
```

**Network Request Failures**
```bash
# Check if Metro bundler is accessible
curl http://localhost:8081/status

# Check if API is accessible from device
# iOS Simulator: localhost works
# Android Emulator: use 10.0.2.2 instead of localhost
# Real device: use computer's IP address

# Test network connectivity
adb shell ping 8.8.8.8  # Android
```

**Performance Issues**
```javascript
// Use React DevTools Profiler
import { Profiler } from 'react';

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log({
    component: id,
    phase,
    actualDuration,
    baseDuration
  });
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

## When to Use This Skill

Ask me when you need help with:
- Setting up debugging tools (Flipper, React DevTools)
- Debugging crashes or error screens
- Inspecting network requests and responses
- Finding performance bottlenecks
- Analyzing component re-renders
- Debugging native module issues
- Reading crash logs and stack traces
- Setting up error boundaries
- Remote debugging on physical devices
- Debugging platform-specific issues
- Troubleshooting "white screen" errors
- Inspecting AsyncStorage or databases

## Essential Debugging Commands

### Start Debugging
```bash
# Open React DevTools
react-devtools

# Start app with remote debugging
npm start

# In app: Shake device → Debug Remote JS
# Or: Press "d" in Metro bundler terminal
```

### Platform Logs
```bash
# iOS System Logs (real device)
idevicesyslog

# iOS Simulator Logs
xcrun simctl spawn booted log stream --level=debug

# Android Logs (all)
adb logcat

# Android Logs (app only, errors)
adb logcat *:E | grep com.myapp

# Android Logs (React Native only)
adb logcat ReactNative:V ReactNativeJS:V *:S

# Clear Android logs
adb logcat -c
```

### Performance Analysis
```bash
# iOS: Use Instruments
# Xcode → Open Developer Tool → Instruments → Time Profiler

# Android: Use Systrace
react-native log-android

# React Native performance monitor
# Shake device → Show Perf Monitor
```

### Flipper Setup
```bash
# Install Flipper Desktop
brew install --cask flipper

# For Expo dev clients, add to app.json:
{
  "expo": {
    "plugins": ["react-native-flipper"]
  }
}

# Rebuild dev client
eas build --profile development --platform all
```

## Pro Tips & Tricks

### 1. Custom Dev Menu

Add custom debugging tools to dev menu:

```javascript
import { DevSettings } from 'react-native';

if (__DEV__) {
  DevSettings.addMenuItem('Clear AsyncStorage', async () => {
    await AsyncStorage.clear();
    console.log('AsyncStorage cleared');
  });

  DevSettings.addMenuItem('Log Redux State', () => {
    console.log('Redux State:', store.getState());
  });

  DevSettings.addMenuItem('Toggle Debug Mode', () => {
    global.DEBUG = !global.DEBUG;
    console.log('Debug mode:', global.DEBUG);
  });
}
```

### 2. Network Request Logger

Comprehensive network debugging:

```javascript
// Create a network logger file
import axios from 'axios';

if (__DEV__) {
  axios.interceptors.request.use(
    (config) => {
      console.log('→ API Request', {
        method: config.method?.toUpperCase(),
        url: config.url,
        data: config.data,
        headers: config.headers
      });
      return config;
    },
    (error) => {
      console.error('→ Request Error', error);
      return Promise.reject(error);
    }
  );

  axios.interceptors.response.use(
    (response) => {
      console.log('← API Response', {
        status: response.status,
        url: response.config.url,
        data: response.data
      });
      return response;
    },
    (error) => {
      console.error('← Response Error', {
        status: error.response?.status,
        url: error.config?.url,
        data: error.response?.data
      });
      return Promise.reject(error);
    }
  );
}
```

### 3. React Query DevTools (for data fetching)

```javascript
import { useReactQueryDevTools } from '@tanstack/react-query-devtools';

function App() {
  // Development only
  if (__DEV__) {
    useReactQueryDevTools();
  }

  return <YourApp />;
}
```

### 4. Debugging State Updates

Track state changes with custom hook:

```javascript
import { useEffect, useRef } from 'react';

function useTraceUpdate(props, componentName) {
  const prev = useRef(props);

  useEffect(() => {
    const changedProps = Object.entries(props).reduce((acc, [key, value]) => {
      if (prev.current[key] !== value) {
        acc[key] = {
          from: prev.current[key],
          to: value
        };
      }
      return acc;
    }, {});

    if (Object.keys(changedProps).length > 0) {
      console.log(`[${componentName}] Changed props:`, changedProps);
    }

    prev.current = props;
  });
}

// Usage
function MyComponent(props) {
  useTraceUpdate(props, 'MyComponent');
  return <View>...</View>;
}
```

### 5. Debugging Offline/Online State

```javascript
import NetInfo from '@react-native-community/netinfo';

// Monitor network state
NetInfo.addEventListener(state => {
  console.log('Network State:', {
    isConnected: state.isConnected,
    type: state.type,
    isInternetReachable: state.isInternetReachable
  });
});
```

### 6. Production Error Tracking

Integrate with error tracking services:

```javascript
// Using Sentry (example)
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'YOUR_SENTRY_DSN',
  enableInExpoDevelopment: true,
  debug: __DEV__
});

// Capture custom errors
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: { feature: 'user-profile' },
    extra: { userId: user.id }
  });
}
```

## Integration with SpecWeave

**During Development**
- Document debugging approaches in increment `reports/`
- Track known issues and workarounds in `spec.md`
- Include debugging steps in `tasks.md` test plans

**Production Monitoring**
- Set up error boundaries for all features
- Integrate crash reporting (Sentry, Bugsnag)
- Document debugging procedures in runbooks
- Track common errors in living documentation
