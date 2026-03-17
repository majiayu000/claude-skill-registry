---
name: native-modules
description: Expert in React Native native modules, bridging JavaScript and native code, writing custom native modules, using Turbo Modules, Fabric, JSI, autolinking, module configuration, iOS Swift/Objective-C modules, Android Kotlin/Java modules. Activates for native module, native code, bridge, turbo module, JSI, fabric, autolinking, custom native module, ios module, android module, swift, kotlin, objective-c, java native code.
---

# Native Modules Expert

Specialized in React Native native module integration, including custom native module development, third-party native library integration, and troubleshooting native code issues.

## What I Know

### Native Module Fundamentals

**What Are Native Modules?**
- Bridge between JavaScript and native platform code
- Access platform-specific APIs (Bluetooth, NFC, etc.)
- Performance-critical operations
- Integration with existing native SDKs

**Modern Architecture**
- **Old Architecture**: Bridge-based (React Native < 0.68)
- **New Architecture** (React Native 0.68+):
  - **JSI** (JavaScript Interface): Direct JS ↔ Native communication
  - **Turbo Modules**: Lazy-loaded native modules
  - **Fabric**: New rendering engine

### Using Third-Party Native Modules

**Installation with Autolinking**
```bash
# Install module
npm install react-native-camera

# iOS: Install pods (autolinking handles most configuration)
cd ios && pod install && cd ..

# Rebuild the app
npm run ios
npm run android
```

**Manual Linking (Legacy)**
```bash
# React Native < 0.60 (rarely needed now)
react-native link react-native-camera
```

**Expo Integration**
```bash
# For Expo managed workflow, use config plugins
npx expo install react-native-camera

# Add plugin to app.json
{
  "expo": {
    "plugins": [
      [
        "react-native-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera"
        }
      ]
    ]
  }
}

# Rebuild dev client
eas build --profile development --platform all
```

### Creating Custom Native Modules

**iOS Native Module (Swift)**

```swift
// RCTCalendarModule.swift
import Foundation

@objc(CalendarModule)
class CalendarModule: NSObject {

  @objc
  static func requiresMainQueueSetup() -> Bool {
    return false
  }

  @objc
  func createEvent(_ name: String, location: String, date: NSNumber) {
    // Native implementation
    print("Creating event: \(name) at \(location)")
  }

  @objc
  func getEvents(_ callback: @escaping RCTResponseSenderBlock) {
    let events = ["Event 1", "Event 2", "Event 3"]
    callback([NSNull(), events])
  }

  @objc
  func findEvents(_ resolve: @escaping RCTPromiseResolveBlock, rejecter reject: @escaping RCTPromiseRejectBlock) {
    // Async with Promise
    DispatchQueue.global().async {
      let events = self.fetchEventsFromNativeAPI()
      resolve(events)
    }
  }
}
```

```objectivec
// RCTCalendarModule.m (Bridge file)
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(CalendarModule, NSObject)

RCT_EXTERN_METHOD(createEvent:(NSString *)name location:(NSString *)location date:(nonnull NSNumber *)date)

RCT_EXTERN_METHOD(getEvents:(RCTResponseSenderBlock)callback)

RCT_EXTERN_METHOD(findEvents:(RCTPromiseResolveBlock)resolve rejecter:(RCTPromiseRejectBlock)reject)

@end
```

**Android Native Module (Kotlin)**

```kotlin
// CalendarModule.kt
package com.myapp

import com.facebook.react.bridge.*

class CalendarModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName(): String {
        return "CalendarModule"
    }

    @ReactMethod
    fun createEvent(name: String, location: String, date: Double) {
        // Native implementation
        println("Creating event: $name at $location")
    }

    @ReactMethod
    fun getEvents(callback: Callback) {
        val events = WritableNativeArray().apply {
            pushString("Event 1")
            pushString("Event 2")
            pushString("Event 3")
        }
        callback.invoke(null, events)
    }

    @ReactMethod
    fun findEvents(promise: Promise) {
        try {
            val events = fetchEventsFromNativeAPI()
            promise.resolve(events)
        } catch (e: Exception) {
            promise.reject("ERROR", e.message, e)
        }
    }
}
```

```kotlin
// CalendarPackage.kt
package com.myapp

import com.facebook.react.ReactPackage
import com.facebook.react.bridge.NativeModule
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.uimanager.ViewManager

class CalendarPackage : ReactPackage {
    override fun createNativeModules(reactContext: ReactApplicationContext): List<NativeModule> {
        return listOf(CalendarModule(reactContext))
    }

    override fun createViewManagers(reactContext: ReactApplicationContext): List<ViewManager<*, *>> {
        return emptyList()
    }
}
```

**JavaScript Usage**

```javascript
// CalendarModule.js
import { NativeModules } from 'react-native';

const { CalendarModule } = NativeModules;

export default {
  createEvent: (name, location, date) => {
    CalendarModule.createEvent(name, location, date);
  },

  getEvents: (callback) => {
    CalendarModule.getEvents((error, events) => {
      if (error) {
        console.error(error);
      } else {
        callback(events);
      }
    });
  },

  findEvents: async () => {
    try {
      const events = await CalendarModule.findEvents();
      return events;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
};

// Usage in components
import CalendarModule from './CalendarModule';

function MyComponent() {
  const handleCreateEvent = () => {
    CalendarModule.createEvent('Meeting', 'Office', Date.now());
  };

  const handleGetEvents = async () => {
    const events = await CalendarModule.findEvents();
    console.log('Events:', events);
  };

  return (
    <View>
      <Button title="Create Event" onPress={handleCreateEvent} />
      <Button title="Get Events" onPress={handleGetEvents} />
    </View>
  );
}
```

### Turbo Modules (New Architecture)

**Creating a Turbo Module**

```typescript
// NativeCalendarModule.ts (Codegen spec)
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  createEvent(name: string, location: string, date: number): void;
  findEvents(): Promise<string[]>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('CalendarModule');
```

**Benefits of Turbo Modules**
- Lazy loading: Loaded only when used
- Type safety with TypeScript
- Faster initialization
- Better performance via JSI

### Native UI Components

**Custom Native View (iOS - Swift)**

```swift
// RCTCustomViewManager.swift
import UIKit

@objc(CustomViewManager)
class CustomViewManager: RCTViewManager {

  override static func requiresMainQueueSetup() -> Bool {
    return true
  }

  override func view() -> UIView! {
    return CustomView()
  }

  @objc func setColor(_ view: CustomView, color: NSNumber) {
    view.backgroundColor = RCTConvert.uiColor(color)
  }
}

class CustomView: UIView {
  override init(frame: CGRect) {
    super.init(frame: frame)
    self.backgroundColor = .blue
  }

  required init?(coder: NSCoder) {
    fatalError("init(coder:) has not been implemented")
  }
}
```

**Custom Native View (Android - Kotlin)**

```kotlin
// CustomViewManager.kt
class CustomViewManager : SimpleViewManager<View>() {

    override fun getName(): String {
        return "CustomView"
    }

    override fun createViewInstance(reactContext: ThemedReactContext): View {
        return View(reactContext).apply {
            setBackgroundColor(Color.BLUE)
        }
    }

    @ReactProp(name = "color")
    fun setColor(view: View, color: Int) {
        view.setBackgroundColor(color)
    }
}
```

**JavaScript Usage**

```javascript
import { requireNativeComponent } from 'react-native';

const CustomView = requireNativeComponent('CustomView');

function MyComponent() {
  return (
    <CustomView
      style={{ width: 200, height: 200 }}
      color="red"
    />
  );
}
```

### Common Native Module Issues

**Module Not Found**
```bash
# iOS: Clear build and reinstall pods
cd ios && rm -rf build Pods && pod install && cd ..
npm run ios

# Android: Clean and rebuild
cd android && ./gradlew clean && cd ..
npm run android

# Clear Metro cache
npx react-native start --reset-cache
```

**Autolinking Not Working**
```bash
# Verify module in package.json
npm list react-native-camera

# Re-run pod install
cd ios && pod install && cd ..

# Check react-native.config.js for custom linking config
```

**Native Crashes**
```bash
# iOS: Check Xcode console for crash logs
# Look for:
# - Unrecognized selector sent to instance
# - Null pointer exceptions
# - Memory issues

# Android: Check logcat
adb logcat *:E
# Look for:
# - Java exceptions
# - JNI errors
# - Null pointer exceptions
```

## When to Use This Skill

Ask me when you need help with:
- Integrating third-party native modules
- Creating custom native modules
- Troubleshooting native module installation
- Writing iOS native code (Swift/Objective-C)
- Writing Android native code (Kotlin/Java)
- Debugging native crashes
- Understanding Turbo Modules and JSI
- Migrating to New Architecture
- Creating custom native UI components
- Handling platform-specific APIs
- Resolving autolinking issues

## Essential Commands

### Module Development
```bash
# Create module template
npx create-react-native-module my-module

# Build iOS module
cd ios && xcodebuild

# Build Android module
cd android && ./gradlew assembleRelease

# Test module locally
npm link
cd ../MyApp && npm link my-module
```

### Debugging Native Code
```bash
# iOS: Run with Xcode debugger
open ios/MyApp.xcworkspace

# Android: Run with Android Studio debugger
# Open android/ folder in Android Studio

# Print native logs
# iOS
tail -f ~/Library/Logs/DiagnosticReports/*.crash

# Android
adb logcat | grep "CalendarModule"
```

## Pro Tips & Tricks

### 1. Type-Safe Native Modules with Codegen

Use Codegen (New Architecture) for type safety:

```typescript
// NativeMyModule.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  getString(key: string): Promise<string>;
  setString(key: string, value: string): void;
}

export default TurboModuleRegistry.getEnforcing<Spec>('MyModule');
```

### 2. Event Emitters for Native → JS Communication

```swift
// iOS - Emit events to JavaScript
import Foundation

@objc(DeviceOrientationModule)
class DeviceOrientationModule: RCTEventEmitter {

  override func supportedEvents() -> [String]! {
    return ["OrientationChanged"]
  }

  @objc
  override static func requiresMainQueueSetup() -> Bool {
    return true
  }

  @objc
  func startObserving() {
    NotificationCenter.default.addObserver(
      self,
      selector: #selector(orientationChanged),
      name: UIDevice.orientationDidChangeNotification,
      object: nil
    )
  }

  @objc
  func stopObserving() {
    NotificationCenter.default.removeObserver(self)
  }

  @objc
  func orientationChanged() {
    let orientation = UIDevice.current.orientation
    sendEvent(withName: "OrientationChanged", body: ["orientation": orientation.rawValue])
  }
}
```

```javascript
// JavaScript - Listen to native events
import { NativeEventEmitter, NativeModules } from 'react-native';

const { DeviceOrientationModule } = NativeModules;
const eventEmitter = new NativeEventEmitter(DeviceOrientationModule);

function MyComponent() {
  useEffect(() => {
    const subscription = eventEmitter.addListener('OrientationChanged', (data) => {
      console.log('Orientation:', data.orientation);
    });

    return () => subscription.remove();
  }, []);

  return <View />;
}
```

### 3. Native Module with Callbacks

```kotlin
// Android - Pass callbacks
@ReactMethod
fun processData(data: String, successCallback: Callback, errorCallback: Callback) {
    try {
        val result = heavyProcessing(data)
        successCallback.invoke(result)
    } catch (e: Exception) {
        errorCallback.invoke(e.message)
    }
}
```

```javascript
// JavaScript
CalendarModule.processData(
  'input data',
  (result) => console.log('Success:', result),
  (error) => console.error('Error:', error)
);
```

### 4. Synchronous Native Methods (Use Sparingly)

```swift
// iOS - Synchronous method (blocks JS thread!)
@objc
func getDeviceId() -> String {
    return UIDevice.current.identifierForVendor?.uuidString ?? "unknown"
}
```

```javascript
// JavaScript - Synchronous call
const deviceId = CalendarModule.getDeviceId();
console.log(deviceId);  // Returns immediately
```

**Warning**: Synchronous methods block the JS thread. Use only for very fast operations (<5ms).

## Integration with SpecWeave

**Native Module Planning**
- Document native dependencies in `spec.md`
- Include native module setup in `plan.md`
- Add native code compilation to `tasks.md`

**Testing Strategy**
- Unit test native code separately
- Integration test JS ↔ Native bridge
- Test on both iOS and Android
- Document platform-specific behaviors

**Documentation**
- Maintain native module API documentation
- Document platform-specific quirks
- Keep runbooks for common native issues
