---
name: expo-modules
description: Building great Expo native modules for iOS and Android. Views, APIs, Marshalling, Shared Objects, Expo Documentation, Verifying Expo modules.
---

## Great module standards

- Design native APIs as if you contributing W3C specs for the browser, take inspiration from modern web modules. eg `std:kv-storage`, `clipboard`.
- Aim for 100% backwards compatibility like the web.
- Create escape hatches for single-platform functionality.
- Avoid extraneous abstractions. Directly expose native functionality.
- Avoid unnecessary async methods. Use sync methods when possible.
- Prefer string union types for API options instead of boolean flags, enums, or multiple parameters. eg instead of `capture(options: { isHighQuality: boolean })`, use `capture(options: { quality: 'high' | 'medium' | 'low' })`.
- Marshalling is awesome for platform-specific APIs.
- New Architecture only. NEVER support legacy React Native architecture.
- ALWAYS use only Expo modules API.
- Prefer Swift and Kotlin.
- Use optionality for availability checks as opposed to extraneous `isAvailable` functions or constants. eg `snapshot.capture?.()` instead of `snapshot.isAvailable && snapshot.capture()`.
- ALWAYS support the latest and greatest API features.

Example of a GREAT Expo module:

```ts
import { NativeModule } from "expo";

declare class AppClipModule extends NativeModule<{}> {
  prompt(): void;
  isAppClip?: boolean;
}

// This call loads the native module object from the JSI.
const AppClipNative =
  typeof expo !== "undefined"
    ? (expo.modules.AppClip as AppClipModule) ?? {}
    : {};

if (AppClipNative?.isAppClip) {
  navigator.appClip = {
    prompt: AppClipNative.prompt,
  };
}

// Add types for the global `navigator.appClip` object.
declare global {
  interface Navigator {
    /**
     * Only available in an App Clip context.
     * @expo
     */
    appClip?: {
      /** Open the SKOverlay */
      prompt: () => void;
    };
  }
}

export {};
```

- Simple web-style interface.
- Global type augmentation for easy access.
- Docs in the type definitions.
- Optional availability checks instead of extraneous `isAvailable` methods.

Example of a POOR Expo module:

```ts
import { NativeModulesProxy } from "expo-modules-core";
const { ExpoAppClip } = NativeModulesProxy;
export default {
  promptAppClip() {
    return ExpoAppClip.promptAppClip();
  },
  isAppClipAvailable() {
    return ExpoAppClip.isAppClipAvailable();
  },
};
```

## Great documentation

- If you have a function like `isAvailable()`, explain why it exists in the docs. Research cases where it may return false such as in a simulator or particular OS version.
- Document OS version availability for functions and constants in the type definitions.

## BAD module standards

- APIs that are hard to import, e.g. `import * as MediaLibrary from 'expo-media-library';` instead of `import { MediaLibrary } from 'expo/media';`
- Extraneous abstractions over native functionality. The native module is installing on the global, do not wrap it in another layer for no reason.
- Extraneous async methods when sync methods are possible.
- Boolean flags instead of string union types for options.
- Supporting legacy React Native architecture.

## Views

Take API inspiration from great web component libraries like BaseUI and Radix.

- https://base-ui.com/react/components/progress
- https://www.radix-ui.com/primitives/docs/components/progress

Consider if you're building a control or a display component. Controls should have more interactive APIs, while display components should be more declarative.

Prefer functions on views instead of `useImperativeHandle` + `findNodeHandle`.

```swift
AsyncFunction("capture") { (view, options: Options) -> Ref in
  return try capture(self.appContext, view)
}
```

Remember to export views in the module:

```swift
import ExpoModulesCore

public class ExpoWebViewModule: Module {
  public func definition() -> ModuleDefinition {
    Name("ExpoWebView")

    View(ExpoWebView.self) {}
  }
}
```

## Marshalling-style API

Consider this example https://github.com/EvanBacon/expo-shared-objects-haptics-example/blob/be90e92f8dba9b0807009502ab25c423c57e640d/modules/my-module/ios/MyModule.swift#L1C1-L178C2

Using `@retroactive Convertible` and `AnyArgument` to convert between Swift types and dictionaries enables passing complex data structures across the boundary without writing custom serialization code for each type.

```swift
extension CHHapticEventParameter: @retroactive Convertible, AnyArgument {
    public static func convert(from value: Any?, appContext: AppContext) throws -> Self {
        guard let dict = value as? [String: Any],
              let parameterIDRaw = dict["parameterID"] as? String,
              let value = dict["value"] as? Double else {
            throw NotADictionaryException()
        }
        return Self(parameterID: CHHapticEvent.ParameterID(rawValue: parameterIDRaw), value: Float(value))
    }
}

extension CHHapticEvent: @retroactive Convertible, AnyArgument {
    public static func convert(from value: Any?, appContext: AppContext) throws -> Self {
        guard let dict = value as? [String: Any],
              let eventTypeRaw = dict["eventType"] as? String,
              let relativeTime = dict["relativeTime"] as? Double else {
            throw NotADictionaryException()
        }
        let eventType = CHHapticEvent.EventType(rawValue: eventTypeRaw)
        let parameters = (dict["parameters"] as? [[String: Any]])?.compactMap { paramDict -> CHHapticEventParameter? in
            try? CHHapticEventParameter.convert(from: paramDict, appContext: appContext)
        } ?? []
        return Self(eventType: eventType, parameters: parameters, relativeTime: relativeTime)
    }
}

extension CHHapticDynamicParameter: @retroactive Convertible, AnyArgument {
    public static func convert(from value: Any?, appContext: AppContext) throws -> Self {
        guard let dict = value as? [String: Any],
              let parameterIDRaw = dict["parameterID"] as? String,
              let value = dict["value"] as? Double,
              let relativeTime = dict["relativeTime"] as? Double else {
            throw NotADictionaryException()
        }

        return Self(parameterID: CHHapticDynamicParameter.ID(rawValue: parameterIDRaw), value: Float(value), relativeTime: relativeTime)
    }
}

extension CHHapticPattern: @retroactive Convertible, AnyArgument {
    public static func convert(from value: Any?, appContext: AppContext) throws -> Self {
        guard let dict = value as? [String: Any],
              let eventsArray = dict["events"] as? [[String: Any]] else {
            throw NotADictionaryException()
        }
        let events = try eventsArray.map { eventDict -> CHHapticEvent in
            try CHHapticEvent.convert(from: eventDict, appContext: appContext)
        }
        let parameters = (dict["parameters"] as? [[String: Any]])?.compactMap { paramDict -> CHHapticDynamicParameter? in
            return try? CHHapticDynamicParameter.convert(from: paramDict, appContext: appContext)
        } ?? []
        return try Self(events: events, parameters: parameters)
    }
}

internal final class NotAnArrayException: Exception {
    override var reason: String {
        "Given value is not an array"
    }
}

internal final class IncorrectArraySizeException: GenericException<(expected: Int, actual: Int)> {
    override var reason: String {
        "Given array has unexpected number of elements: \(param.actual), expected: \(param.expected)"
    }
}

internal final class NotADictionaryException: Exception {
    override var reason: String {
        "Given value is not a dictionary"
    }
}

```

Later this can be used to implement methods that accept complex data structures as arguments.

```swift
Function("playPattern") { (pattern: CHHapticPattern) in
    let player = try hapticEngine.makePlayer(with: pattern)
    try player.start(atTime: 0)
}
```

Use shorthand where possible, especially when the JS value matches the Swift value:

```swift
Property("__typename") { $0.__typename }
```

## Shared objects

Shared objects are long-lived native instances that are shared to JS. They can be used to keep heavy state objects, such as a decoded bitmap, alive across React components, rather than spinning up a new native instance every time a component mounts.

- https://docs.expo.dev/modules/shared-objects/
- https://expo.dev/blog/the-real-world-impact-of-shared-objects

## Interacting with AppDelegate

To interact with HealthKit, the module may need to respond to app lifecycle events. This can be done by implementing the `ExpoAppDelegateSubscriber` protocol.

```swift
import ExpoModulesCore

public class ExpoHeadAppDelegateSubscriber: ExpoAppDelegateSubscriber {

// Any AppDelegate methods you want to implement
  public func application(
    _ application: UIApplication,
    continue userActivity: NSUserActivity,
    restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void
  ) -> Bool {
    launchedActivity = userActivity

   // ...

    return false
  }
}
```

Then add the subscriber to the `expo-module.config.json`:

```json
{
  "platforms": ["apple", "android", "web"],
  "apple": {
    "modules": ["ExpoHeadModule", ...],
    "appDelegateSubscribers": ["ExpoHeadAppDelegateSubscriber"]
  }
}
```

## Expo ecosystem integration

- Create a Config Plugin for setting up all permissions and entitlements.
- Permissions APIs should follow Expo's permission model and implement hooks.
  - Ref: https://github.com/expo/expo/blob/843d5e108ff70539ac353721d3a7765a5d08d502/packages/expo-media-library/src/MediaLibrary.ts#L502-L519
- Document when things don't work in Expo Go and link to dev client instructions.
- Consider creating Expo devtools plugins for interacting with native APIs. Optimize for Claude Code usage, e.g. a Bun CLI before a UI.
  - Ref: https://docs.expo.dev/debugging/devtools-plugins
- If any feature launches the app or could benefit from deep linking, add an Expo Router integration. A good example is `expo-quick-actions` which has a `expo-quick-actions/router` import for automatic deep linking. Other good examples are Expo notifications (open settings, redirect notifications), widgets, siri shortcuts.
  - Ref: https://github.com/EvanBacon/expo-quick-actions

## Verification

- Run `yarn expo run:ios --no-bundler` in an Expo app to headlessly compile the module and verify there are no compilation errors.
