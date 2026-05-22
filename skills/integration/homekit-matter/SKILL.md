---
name: homekit-matter
description: "Control smart-home accessories and commission Matter devices using HomeKit and MatterSupport. Use when managing homes/rooms/accessories, creating action sets or triggers, reading accessory characteristics, onboarding Matter devices, or building a third-party smart-home ecosystem app."
---

# HomeKit + MatterSupport

Control home automation accessories and commission Matter devices. HomeKit manages
the home/room/accessory model, action sets, and triggers. MatterSupport handles
device commissioning into your ecosystem. Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [HomeKit Data Model](#homekit-data-model)
- [Managing Accessories](#managing-accessories)
- [Reading and Writing Characteristics](#reading-and-writing-characteristics)
- [Action Sets and Triggers](#action-sets-and-triggers)
- [Matter Commissioning](#matter-commissioning)
- [MatterAddDeviceExtensionRequestHandler](#matteradddeviceextensionrequesthandler)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### HomeKit Configuration

1. Enable the **HomeKit** capability in Xcode (Signing & Capabilities)
2. Add `NSHomeKitUsageDescription` to Info.plist:

```xml
<key>NSHomeKitUsageDescription</key>
<string>This app controls your smart home accessories.</string>
```

### MatterSupport Configuration

For Matter commissioning into your own ecosystem:

1. Enable the **MatterSupport** capability
2. Add a **MatterSupport Extension** target to your project
3. Add the `com.apple.developer.matter.allow-setup-payload` entitlement if
   your app provides the setup code directly

### Availability Check

```swift
import HomeKit

let homeManager = HMHomeManager()

// HomeKit is available on iPhone, iPad, Apple TV, Apple Watch, Mac, and Vision Pro.
// Authorization is handled through the delegate:
homeManager.delegate = self
```

## HomeKit Data Model

HomeKit organizes home automation in a hierarchy:

```text
HMHomeManager
  -> HMHome (one or more)
       -> HMRoom (rooms in the home)
            -> HMAccessory (devices in a room)
                 -> HMService (functions: light, thermostat, etc.)
                      -> HMCharacteristic (readable/writable values)
       -> HMZone (groups of rooms)
       -> HMActionSet (grouped actions)
       -> HMTrigger (time or event-based triggers)
```

### Initializing the Home Manager

Create a single `HMHomeManager` and implement the delegate to know when
data is loaded. HomeKit loads asynchronously -- do not access `homes` until
the delegate fires.

```swift
import HomeKit

final class HomeStore: NSObject, HMHomeManagerDelegate {
    let homeManager = HMHomeManager()

    override init() {
        super.init()
        homeManager.delegate = self
    }

    func homeManagerDidUpdateHomes(_ manager: HMHomeManager) {
        // Safe to access manager.homes now
        let homes = manager.homes
        let primaryHome = manager.primaryHome
        print("Loaded \(homes.count) homes")
    }

    func homeManager(
        _ manager: HMHomeManager,
        didUpdate status: HMHomeManagerAuthorizationStatus
    ) {
        if status.contains(.authorized) {
            print("HomeKit access granted")
        }
    }
}
```

### Accessing Rooms

```swift
guard let home = homeManager.primaryHome else { return }

let rooms = home.rooms
let kitchen = rooms.first { $0.name == "Kitchen" }

// Room for accessories not assigned to a specific room
let defaultRoom = home.roomForEntireHome()
```

## Managing Accessories

### Discovering and Adding Accessories

```swift
// System UI for accessory discovery
home.addAndSetupAccessories { error in
    if let error {
        print("Setup failed: \(error)")
    }
}
```

### Listing Accessories and Services

```swift
for accessory in home.accessories {
    print("\(accessory.name) in \(accessory.room?.name ?? "unassigned")")

    for service in accessory.services {
        print("  Service: \(service.serviceType)")

        for characteristic in service.characteristics {
            print("    \(characteristic.characteristicType): \(characteristic.value ?? "nil")")
        }
    }
}
```

### Moving an Accessory to a Room

```swift
guard let accessory = home.accessories.first,
      let bedroom = home.rooms.first(where: { $0.name == "Bedroom" }) else { return }

home.assignAccessory(accessory, to: bedroom) { error in
    if let error {
        print("Failed to move accessory: \(error)")
    }
}
```

## Reading and Writing Characteristics

### Reading a Value

```swift
let characteristic: HMCharacteristic = // obtained from a service

characteristic.readValue { error in
    guard error == nil else { return }
    if let value = characteristic.value as? Bool {
        print("Power state: \(value)")
    }
}
```

### Writing a Value

```swift
// Turn on a light
characteristic.writeValue(true) { error in
    if let error {
        print("Write failed: \(error)")
    }
}
```

### Observing Changes

Enable notifications for real-time updates:

```swift
characteristic.enableNotification(true) { error in
    guard error == nil else { return }
}

// In HMAccessoryDelegate:
func accessory(
    _ accessory: HMAccessory,
    service: HMService,
    didUpdateValueFor characteristic: HMCharacteristic
) {
    print("Updated: \(characteristic.value ?? "nil")")
}
```

## Action Sets and Triggers

### Creating an Action Set

An `HMActionSet` groups characteristic writes that execute together:

```swift
home.addActionSet(withName: "Good Night") { actionSet, error in
    guard let actionSet, error == nil else { return }

    // Turn off living room light
    let lightChar = livingRoomLight.powerCharacteristic
    let action = HMCharacteristicWriteAction(
        characteristic: lightChar,
        targetValue: false as NSCopying
    )
    actionSet.addAction(action) { error in
        guard error == nil else { return }
        print("Action added to Good Night scene")
    }
}
```

### Executing an Action Set

```swift
home.executeActionSet(actionSet) { error in
    if let error {
        print("Execution failed: \(error)")
    }
}
```

### Creating a Timer Trigger

```swift
var dateComponents = DateComponents()
dateComponents.hour = 22
dateComponents.minute = 30

let trigger = HMTimerTrigger(
    name: "Nightly",
    fireDate: Calendar.current.nextDate(
        after: Date(),
        matching: dateComponents,
        matchingPolicy: .nextTime
    )!,
    timeZone: .current,
    recurrence: dateComponents,  // Repeats daily at 22:30
    recurrenceCalendar: .current
)

home.addTrigger(trigger) { error in
    guard error == nil else { return }

    // Attach the action set to the trigger
    trigger.addActionSet(goodNightActionSet) { error in
        guard error == nil else { return }

        trigger.enable(true) { error in
            print("Trigger enabled: \(error == nil)")
        }
    }
}
```

### Creating an Event Trigger

```swift
let motionDetected = HMCharacteristicEvent(
    characteristic: motionSensorCharacteristic,
    triggerValue: true as NSCopying
)

let eventTrigger = HMEventTrigger(
    name: "Motion Lights",
    events: [motionDetected],
    predicate: nil
)

home.addTrigger(eventTrigger) { error in
    // Add action sets as above
}
```

## Matter Commissioning

Use `MatterAddDeviceRequest` to commission a Matter device into your ecosystem.
This is separate from HomeKit -- it handles the pairing flow.

### Basic Commissioning

```swift
import MatterSupport

func addMatterDevice() async throws {
    guard MatterAddDeviceRequest.isSupported else {
        print("Matter not supported on this device")
        return
    }

    let topology = MatterAddDeviceRequest.Topology(
        ecosystemName: "My Smart Home",
        homes: [
            MatterAddDeviceRequest.Home(displayName: "Main House")
        ]
    )

    let request = MatterAddDeviceRequest(
        topology: topology,
        setupPayload: nil,
        showing: .allDevices
    )

    // Presents system UI for device pairing
    try await request.perform()
}
```

### Filtering Devices

```swift
// Only show devices from a specific vendor
let criteria = MatterAddDeviceRequest.DeviceCriteria.vendorID(0x1234)

let request = MatterAddDeviceRequest(
    topology: topology,
    setupPayload: nil,
    showing: criteria
)
```

### Combining Device Criteria

```swift
let criteria = MatterAddDeviceRequest.DeviceCriteria.all([
    .vendorID(0x1234),
    .not(.productID(0x0001))  // Exclude a specific product
])
```

## MatterAddDeviceExtensionRequestHandler

For full ecosystem support, create a MatterSupport Extension. The extension
handles commissioning callbacks:

```swift
import MatterSupport

final class MatterHandler: MatterAddDeviceExtensionRequestHandler {

    override func validateDeviceCredential(
        _ deviceCredential: DeviceCredential
    ) async throws {
        // Validate the device attestation certificate
        // Throw to reject the device
    }

    override func rooms(
        in home: MatterAddDeviceRequest.Home?
    ) async -> [MatterAddDeviceRequest.Room] {
        // Return rooms in the selected home
        return [
            MatterAddDeviceRequest.Room(displayName: "Living Room"),
            MatterAddDeviceRequest.Room(displayName: "Kitchen")
        ]
    }

    override func configureDevice(
        named name: String,
        in room: MatterAddDeviceRequest.Room?
    ) async {
        // Save the device configuration to your backend
        print("Configuring \(name) in \(room?.displayName ?? "no room")")
    }

    override func commissionDevice(
        in home: MatterAddDeviceRequest.Home?,
        onboardingPayload: String,
        commissioningID: UUID
    ) async throws {
        // Use the onboarding payload to commission the device
        // into your fabric using the Matter framework
    }
}
```

## Common Mistakes

### DON'T: Access homes before the delegate fires

```swift
// WRONG -- homes array is empty until delegate is called
let manager = HMHomeManager()
let homes = manager.homes  // Always empty here

// CORRECT -- wait for delegate
func homeManagerDidUpdateHomes(_ manager: HMHomeManager) {
    let homes = manager.homes  // Now populated
}
```

### DON'T: Confuse HomeKit setup with Matter commissioning

```swift
// WRONG -- using HomeKit accessory setup for a Matter ecosystem app
home.addAndSetupAccessories { error in }

// CORRECT -- use MatterAddDeviceRequest for Matter ecosystem commissioning
let request = MatterAddDeviceRequest(
    topology: topology,
    setupPayload: nil,
    showing: .allDevices
)
try await request.perform()
```

### DON'T: Forget required entitlements

```swift
// WRONG -- calling Matter APIs without the MatterSupport entitlement
// Results in runtime error

// CORRECT -- ensure these are set up:
// 1. HomeKit capability for HMHomeManager access
// 2. MatterSupport Extension target for ecosystem commissioning
// 3. com.apple.developer.matter.allow-setup-payload if providing setup codes
```

### DON'T: Create multiple HMHomeManager instances

```swift
// WRONG -- each instance loads the full database independently
class ScreenA { let manager = HMHomeManager() }
class ScreenB { let manager = HMHomeManager() }

// CORRECT -- single shared instance
@Observable
final class HomeStore {
    static let shared = HomeStore()
    let homeManager = HMHomeManager()
}
```

### DON'T: Write characteristics without checking metadata

```swift
// WRONG -- writing a value outside the valid range
characteristic.writeValue(500) { _ in }

// CORRECT -- check metadata first
if let metadata = characteristic.metadata,
   let maxValue = metadata.maximumValue?.intValue {
    let safeValue = min(brightness, maxValue)
    characteristic.writeValue(safeValue) { _ in }
}
```

## Review Checklist

- [ ] HomeKit capability enabled in Xcode
- [ ] `NSHomeKitUsageDescription` present in Info.plist
- [ ] Single `HMHomeManager` instance shared across the app
- [ ] `HMHomeManagerDelegate` implemented; homes not accessed before `homeManagerDidUpdateHomes`
- [ ] `HMHomeDelegate` set on homes to receive accessory and room changes
- [ ] `HMAccessoryDelegate` set on accessories to receive characteristic updates
- [ ] Characteristic metadata checked before writing values
- [ ] Error handling in all completion handlers
- [ ] MatterSupport capability and extension target added for Matter commissioning
- [ ] `MatterAddDeviceRequest.isSupported` checked before performing requests
- [ ] Matter extension handler implements `commissionDevice(in:onboardingPayload:commissioningID:)`
- [ ] Action sets tested with the HomeKit Accessory Simulator before shipping
- [ ] Triggers enabled after creation (`trigger.enable(true)`)

## References

- Extended patterns (Matter extension, delegate wiring, SwiftUI): `references/matter-commissioning.md`
- [HomeKit framework](https://sosumi.ai/documentation/homekit)
- [HMHomeManager](https://sosumi.ai/documentation/homekit/hmhomemanager)
- [HMHome](https://sosumi.ai/documentation/homekit/hmhome)
- [HMAccessory](https://sosumi.ai/documentation/homekit/hmaccessory)
- [HMRoom](https://sosumi.ai/documentation/homekit/hmroom)
- [HMActionSet](https://sosumi.ai/documentation/homekit/hmactionset)
- [HMTrigger](https://sosumi.ai/documentation/homekit/hmtrigger)
- [MatterSupport framework](https://sosumi.ai/documentation/mattersupport)
- [MatterAddDeviceRequest](https://sosumi.ai/documentation/mattersupport/matteradddevicerequest)
- [MatterAddDeviceExtensionRequestHandler](https://sosumi.ai/documentation/mattersupport/matteradddeviceextensionrequesthandler)
- [Enabling HomeKit in your app](https://sosumi.ai/documentation/homekit/enabling-homekit-in-your-app)
- [Adding Matter support to your ecosystem](https://sosumi.ai/documentation/mattersupport/adding-matter-support-to-your-ecosystem)
