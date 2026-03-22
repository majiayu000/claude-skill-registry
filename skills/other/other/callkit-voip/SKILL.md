---
name: callkit-voip
description: "Implement VoIP calling with CallKit and PushKit. Use when building incoming/outgoing call flows, registering for VoIP push notifications, configuring CXProvider and CXCallController, handling call actions, coordinating audio sessions, or creating Call Directory extensions for caller ID and call blocking."
---

# CallKit + PushKit VoIP

Build VoIP calling features that integrate with the native iOS call UI using
CallKit and PushKit. Covers incoming/outgoing call flows, VoIP push
registration, audio session coordination, and call directory extensions.
Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Provider Configuration](#provider-configuration)
- [Incoming Call Flow](#incoming-call-flow)
- [Outgoing Call Flow](#outgoing-call-flow)
- [PushKit VoIP Registration](#pushkit-voip-registration)
- [Audio Session Coordination](#audio-session-coordination)
- [Call Directory Extension](#call-directory-extension)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Project Configuration

1. Enable the **Voice over IP** background mode in Signing & Capabilities
2. Add the **Push Notifications** capability
3. For call directory extensions, add a **Call Directory Extension** target

### Key Types

| Type | Role |
|---|---|
| `CXProvider` | Reports calls to the system, receives call actions |
| `CXCallController` | Requests call actions (start, end, hold, mute) |
| `CXCallUpdate` | Describes call metadata (caller name, video, handle) |
| `CXProviderDelegate` | Handles system call actions and audio session events |
| `PKPushRegistry` | Registers for and receives VoIP push notifications |

## Provider Configuration

Create a single `CXProvider` at app launch and keep it alive for the app
lifetime. Configure it with a `CXProviderConfiguration` that describes your
calling capabilities.

```swift
import CallKit

/// CXProvider dispatches all delegate calls to the queue passed to `setDelegate(_:queue:)`.
/// The `let` properties are initialized once and never mutated, making this type
/// safe to share across concurrency domains despite @unchecked Sendable.
final class CallManager: NSObject, @unchecked Sendable {
    static let shared = CallManager()

    let provider: CXProvider
    let callController = CXCallController()

    private override init() {
        let config = CXProviderConfiguration()
        config.localizedName = "My VoIP App"
        config.supportsVideo = true
        config.maximumCallsPerCallGroup = 1
        config.maximumCallGroups = 2
        config.supportedHandleTypes = [.phoneNumber, .emailAddress]
        config.includesCallsInRecents = true

        provider = CXProvider(configuration: config)
        super.init()
        provider.setDelegate(self, queue: nil)
    }
}
```

## Incoming Call Flow

When a VoIP push arrives, report the incoming call to CallKit immediately.
The system displays the native call UI. You must report the call before the
PushKit completion handler returns -- failure to do so causes the system to
terminate your app.

```swift
func reportIncomingCall(
    uuid: UUID,
    handle: String,
    hasVideo: Bool
) async throws {
    let update = CXCallUpdate()
    update.remoteHandle = CXHandle(type: .phoneNumber, value: handle)
    update.hasVideo = hasVideo
    update.localizedCallerName = "Jane Doe"

    try await withCheckedThrowingContinuation {
        (continuation: CheckedContinuation<Void, Error>) in
        provider.reportNewIncomingCall(
            with: uuid,
            update: update
        ) { error in
            if let error {
                continuation.resume(throwing: error)
            } else {
                continuation.resume()
            }
        }
    }
}
```

### Handling the Answer Action

Implement `CXProviderDelegate` to respond when the user answers:

```swift
extension CallManager: CXProviderDelegate {
    func providerDidReset(_ provider: CXProvider) {
        // End all calls, reset audio
    }

    func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
        // Configure audio, connect to call server
        configureAudioSession()
        connectToCallServer(callUUID: action.callUUID)
        action.fulfill()
    }

    func provider(_ provider: CXProvider, perform action: CXEndCallAction) {
        disconnectFromCallServer(callUUID: action.callUUID)
        action.fulfill()
    }
}
```

## Outgoing Call Flow

Use `CXCallController` to request an outgoing call. The system routes the
request through your `CXProviderDelegate`.

```swift
func startOutgoingCall(handle: String, hasVideo: Bool) {
    let uuid = UUID()
    let handle = CXHandle(type: .phoneNumber, value: handle)
    let startAction = CXStartCallAction(call: uuid, handle: handle)
    startAction.isVideo = hasVideo

    let transaction = CXTransaction(action: startAction)
    callController.request(transaction) { error in
        if let error {
            print("Failed to start call: \(error)")
        }
    }
}
```

### Delegate Methods for Outgoing Calls

```swift
extension CallManager {
    func provider(_ provider: CXProvider, perform action: CXStartCallAction) {
        configureAudioSession()
        // Begin connecting to server
        provider.reportOutgoingCall(
            with: action.callUUID,
            startedConnectingAt: Date()
        )

        connectToServer(callUUID: action.callUUID) {
            provider.reportOutgoingCall(
                with: action.callUUID,
                connectedAt: Date()
            )
        }
        action.fulfill()
    }
}
```

## PushKit VoIP Registration

Register for VoIP pushes at every app launch. Send the token to your server
whenever it changes.

```swift
import PushKit

final class PushManager: NSObject, PKPushRegistryDelegate {
    let registry: PKPushRegistry

    override init() {
        registry = PKPushRegistry(queue: .main)
        super.init()
        registry.delegate = self
        registry.desiredPushTypes = [.voIP]
    }

    func pushRegistry(
        _ registry: PKPushRegistry,
        didUpdate pushCredentials: PKPushCredentials,
        for type: PKPushType
    ) {
        let token = pushCredentials.token
            .map { String(format: "%02x", $0) }
            .joined()
        // Send token to your server
        sendTokenToServer(token)
    }

    func pushRegistry(
        _ registry: PKPushRegistry,
        didReceiveIncomingPushWith payload: PKPushPayload,
        for type: PKPushType,
        completion: @escaping () -> Void
    ) {
        guard type == .voIP else {
            completion()
            return
        }

        let callUUID = UUID()
        let handle = payload.dictionaryPayload["handle"] as? String ?? "Unknown"

        Task {
            do {
                try await CallManager.shared.reportIncomingCall(
                    uuid: callUUID,
                    handle: handle,
                    hasVideo: false
                )
            } catch {
                // Call was filtered by DND or block list
            }
            completion()
        }
    }
}
```

## Audio Session Coordination

CallKit manages audio session activation/deactivation. Configure your audio
session when CallKit tells you to, not before.

```swift
extension CallManager {
    func provider(_ provider: CXProvider, didActivate audioSession: AVAudioSession) {
        // Audio session is now active -- start audio engine / WebRTC
        startAudioEngine()
    }

    func provider(_ provider: CXProvider, didDeactivate audioSession: AVAudioSession) {
        // Audio session deactivated -- stop audio engine
        stopAudioEngine()
    }

    func configureAudioSession() {
        let session = AVAudioSession.sharedInstance()
        do {
            try session.setCategory(
                .playAndRecord,
                mode: .voiceChat,
                options: [.allowBluetooth, .allowBluetoothA2DP]
            )
        } catch {
            print("Audio session configuration failed: \(error)")
        }
    }
}
```

## Call Directory Extension

Create a Call Directory extension to provide caller ID and call blocking.

```swift
import CallKit

final class CallDirectoryHandler: CXCallDirectoryProvider {
    override func beginRequest(
        with context: CXCallDirectoryExtensionContext
    ) {
        if context.isIncremental {
            addOrRemoveIncrementalEntries(to: context)
        } else {
            addAllEntries(to: context)
        }
        context.completeRequest()
    }

    private func addAllEntries(
        to context: CXCallDirectoryExtensionContext
    ) {
        // Phone numbers must be in ascending order (E.164 format as Int64)
        let blockedNumbers: [CXCallDirectoryPhoneNumber] = [
            18005551234, 18005555678
        ]
        for number in blockedNumbers {
            context.addBlockingEntry(
                withNextSequentialPhoneNumber: number
            )
        }

        let identifiedNumbers: [(CXCallDirectoryPhoneNumber, String)] = [
            (18005551111, "Local Pizza"),
            (18005552222, "Dentist Office")
        ]
        for (number, label) in identifiedNumbers {
            context.addIdentificationEntry(
                withNextSequentialPhoneNumber: number,
                label: label
            )
        }
    }
}
```

Reload the extension from the main app after data changes:

```swift
CXCallDirectoryManager.sharedInstance.reloadExtension(
    withIdentifier: "com.example.app.CallDirectory"
) { error in
    if let error { print("Reload failed: \(error)") }
}
```

## Common Mistakes

### DON'T: Fail to report a call on VoIP push receipt

If your PushKit delegate receives a VoIP push but does not call
`reportNewIncomingCall(with:update:completion:)`, iOS terminates your app and
may stop delivering pushes entirely.

```swift
// WRONG -- no call reported
func pushRegistry(
    _ registry: PKPushRegistry,
    didReceiveIncomingPushWith payload: PKPushPayload,
    for type: PKPushType,
    completion: @escaping () -> Void
) {
    // Just process data, no call reported
    processPayload(payload)
    completion()
}

// CORRECT -- always report a call
func pushRegistry(
    _ registry: PKPushRegistry,
    didReceiveIncomingPushWith payload: PKPushPayload,
    for type: PKPushType,
    completion: @escaping () -> Void
) {
    let uuid = UUID()
    provider.reportNewIncomingCall(
        with: uuid, update: makeUpdate(from: payload)
    ) { _ in completion() }
}
```

### DON'T: Start audio before CallKit activates the session

Starting your audio engine before `provider(_:didActivate:)` causes silence
or immediate deactivation. CallKit manages session priority with the system.

```swift
// WRONG
func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
    startAudioEngine()  // Too early -- session not active yet
    action.fulfill()
}

// CORRECT
func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
    prepareAudioEngine()  // Prepare, but do not start
    action.fulfill()
}

func provider(_ provider: CXProvider, didActivate audioSession: AVAudioSession) {
    startAudioEngine()  // Now it's safe
}
```

### DON'T: Forget to call action.fulfill() or action.fail()

Failing to fulfill or fail an action leaves the call in a limbo state and
triggers the timeout handler.

```swift
// WRONG
func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
    connectToServer()
    // Forgot action.fulfill()
}

// CORRECT
func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
    connectToServer()
    action.fulfill()
}
```

### DON'T: Ignore push token refresh

The VoIP push token can change at any time. If your server has a stale token,
pushes silently fail and incoming calls never arrive.

```swift
// WRONG -- only send token once at first registration
func pushRegistry(
    _ registry: PKPushRegistry,
    didUpdate pushCredentials: PKPushCredentials,
    for type: PKPushType
) {
    // Token saved locally but never updated on server
}

// CORRECT -- always update server
func pushRegistry(
    _ registry: PKPushRegistry,
    didUpdate pushCredentials: PKPushCredentials,
    for type: PKPushType
) {
    let token = pushCredentials.token.map { String(format: "%02x", $0) }.joined()
    sendTokenToServer(token)  // Always send to server
}
```

## Review Checklist

- [ ] VoIP background mode enabled in capabilities
- [ ] Single `CXProvider` instance created at app launch and retained
- [ ] `CXProviderDelegate` set before reporting any calls
- [ ] Every VoIP push results in a `reportNewIncomingCall` call
- [ ] `action.fulfill()` or `action.fail()` called for every provider delegate action
- [ ] Audio engine started only after `provider(_:didActivate:)` callback
- [ ] Audio engine stopped in `provider(_:didDeactivate:)` callback
- [ ] Audio session category set to `.playAndRecord` with `.voiceChat` mode
- [ ] VoIP push token sent to server on every `didUpdate pushCredentials` callback
- [ ] `PKPushRegistry` created at every app launch (not lazily)
- [ ] Call Directory phone numbers added in ascending E.164 order
- [ ] `CXCallUpdate` populated with `localizedCallerName` and `remoteHandle`
- [ ] Outgoing calls report `startedConnectingAt` and `connectedAt` timestamps

## References

- Extended patterns (hold, mute, group calls, delegate lifecycle): `references/callkit-patterns.md`
- [CallKit framework](https://sosumi.ai/documentation/callkit)
- [CXProvider](https://sosumi.ai/documentation/callkit/cxprovider)
- [CXCallController](https://sosumi.ai/documentation/callkit/cxcallcontroller)
- [CXCallAction](https://sosumi.ai/documentation/callkit/cxcallaction)
- [CXCallUpdate](https://sosumi.ai/documentation/callkit/cxcallupdate)
- [CXProviderConfiguration](https://sosumi.ai/documentation/callkit/cxproviderconfiguration)
- [CXProviderDelegate](https://sosumi.ai/documentation/callkit/cxproviderdelegate)
- [PKPushRegistry](https://sosumi.ai/documentation/pushkit/pkpushregistry)
- [PKPushRegistryDelegate](https://sosumi.ai/documentation/pushkit/pkpushregistrydelegate)
- [CXCallDirectoryProvider](https://sosumi.ai/documentation/callkit/cxcalldirectoryprovider)
- [Making and receiving VoIP calls](https://sosumi.ai/documentation/callkit/making-and-receiving-voip-calls)
- [Responding to VoIP Notifications from PushKit](https://sosumi.ai/documentation/pushkit/responding-to-voip-notifications-from-pushkit)
