---
name: core-bluetooth
description: "Scan, connect, and communicate with Bluetooth Low Energy peripherals and publish local peripheral services using Core Bluetooth. Use when implementing BLE central or peripheral roles, discovering services and characteristics, reading and writing characteristic values, subscribing to notifications, configuring background BLE modes, restoring state after app relaunch, or working with CBCentralManager, CBPeripheral, CBPeripheralManager, CBService, CBCharacteristic, CBUUID, or Bluetooth Low Energy workflows."
---

# Core Bluetooth

Scan for, connect to, and exchange data with Bluetooth Low Energy (BLE) devices.
Covers the central role (scanning and connecting to peripherals), the peripheral
role (advertising services), background modes, and state restoration.
Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Central Role: Scanning](#central-role-scanning)
- [Central Role: Connecting](#central-role-connecting)
- [Discovering Services and Characteristics](#discovering-services-and-characteristics)
- [Reading, Writing, and Notifications](#reading-writing-and-notifications)
- [Peripheral Role: Advertising](#peripheral-role-advertising)
- [Background BLE](#background-ble)
- [State Restoration](#state-restoration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Info.plist Keys

| Key | Purpose |
|---|---|
| `NSBluetoothAlwaysUsageDescription` | Required. Explains why the app uses Bluetooth |
| `UIBackgroundModes` with `bluetooth-central` | Background scanning and connecting |
| `UIBackgroundModes` with `bluetooth-peripheral` | Background advertising |

### Bluetooth Authorization

iOS prompts for Bluetooth permission automatically when you create a
`CBCentralManager` or `CBPeripheralManager`. The usage description from
`NSBluetoothAlwaysUsageDescription` is shown in the permission dialog.

## Central Role: Scanning

### Creating the Central Manager

Always wait for the `poweredOn` state before scanning.

```swift
import CoreBluetooth

final class BluetoothManager: NSObject, CBCentralManagerDelegate {
    private var centralManager: CBCentralManager!
    private var discoveredPeripheral: CBPeripheral?

    override init() {
        super.init()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }

    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        switch central.state {
        case .poweredOn:
            startScanning()
        case .poweredOff:
            // Bluetooth is off -- prompt user to enable
            break
        case .unauthorized:
            // App not authorized for Bluetooth
            break
        case .unsupported:
            // Device does not support BLE
            break
        case .resetting, .unknown:
            break
        @unknown default:
            break
        }
    }
}
```

### Scanning for Peripherals

Scan for specific service UUIDs to save power. Pass `nil` to discover all
peripherals (not recommended in production).

```swift
let heartRateServiceUUID = CBUUID(string: "180D")

func startScanning() {
    centralManager.scanForPeripherals(
        withServices: [heartRateServiceUUID],
        options: [CBCentralManagerScanOptionAllowDuplicatesKey: false]
    )
}

func centralManager(
    _ central: CBCentralManager,
    didDiscover peripheral: CBPeripheral,
    advertisementData: [String: Any],
    rssi RSSI: NSNumber
) {
    guard RSSI.intValue > -70 else { return } // Filter weak signals

    // IMPORTANT: Retain the peripheral -- it will be deallocated otherwise
    discoveredPeripheral = peripheral
    centralManager.stopScan()
    centralManager.connect(peripheral, options: nil)
}
```

## Central Role: Connecting

```swift
func centralManager(
    _ central: CBCentralManager,
    didConnect peripheral: CBPeripheral
) {
    peripheral.delegate = self
    peripheral.discoverServices([heartRateServiceUUID])
}

func centralManager(
    _ central: CBCentralManager,
    didFailToConnect peripheral: CBPeripheral,
    error: Error?
) {
    // Handle connection failure -- retry or inform user
    discoveredPeripheral = nil
}

func centralManager(
    _ central: CBCentralManager,
    didDisconnectPeripheral peripheral: CBPeripheral,
    timestamp: CFAbsoluteTime,
    isReconnecting: Bool,
    error: Error?
) {
    if isReconnecting {
        // System is automatically reconnecting
        return
    }
    // Handle disconnection -- optionally reconnect
    discoveredPeripheral = nil
}
```

## Discovering Services and Characteristics

Implement `CBPeripheralDelegate` to walk the service/characteristic tree.

```swift
extension BluetoothManager: CBPeripheralDelegate {
    func peripheral(
        _ peripheral: CBPeripheral,
        didDiscoverServices error: Error?
    ) {
        guard let services = peripheral.services else { return }
        for service in services {
            peripheral.discoverCharacteristics(nil, for: service)
        }
    }

    func peripheral(
        _ peripheral: CBPeripheral,
        didDiscoverCharacteristicsFor service: CBService,
        error: Error?
    ) {
        guard let characteristics = service.characteristics else { return }
        for characteristic in characteristics {
            if characteristic.properties.contains(.notify) {
                peripheral.setNotifyValue(true, for: characteristic)
            }
            if characteristic.properties.contains(.read) {
                peripheral.readValue(for: characteristic)
            }
        }
    }
}
```

### Common Service and Characteristic UUIDs

| Service | UUID | Characteristics |
|---|---|---|
| Heart Rate | `180D` | Heart Rate Measurement (`2A37`), Body Sensor Location (`2A38`) |
| Battery | `180F` | Battery Level (`2A19`) |
| Device Information | `180A` | Manufacturer Name (`2A29`), Model Number (`2A24`) |
| Generic Access | `1800` | Device Name (`2A00`), Appearance (`2A01`) |

```swift
let heartRateMeasurementUUID = CBUUID(string: "2A37")
let batteryLevelUUID = CBUUID(string: "2A19")
```

## Reading, Writing, and Notifications

### Reading a Value

```swift
func peripheral(
    _ peripheral: CBPeripheral,
    didUpdateValueFor characteristic: CBCharacteristic,
    error: Error?
) {
    guard let data = characteristic.value else { return }

    switch characteristic.uuid {
    case CBUUID(string: "2A37"):
        let heartRate = parseHeartRate(data)
        print("Heart rate: \(heartRate) bpm")
    case CBUUID(string: "2A19"):
        let batteryLevel = data.first.map { Int($0) } ?? 0
        print("Battery: \(batteryLevel)%")
    default:
        break
    }
}

private func parseHeartRate(_ data: Data) -> Int {
    let flags = data[0]
    let is16Bit = (flags & 0x01) != 0
    if is16Bit {
        return Int(data[1]) | (Int(data[2]) << 8)
    } else {
        return Int(data[1])
    }
}
```

### Writing a Value

```swift
func writeValue(_ data: Data, to characteristic: CBCharacteristic,
                on peripheral: CBPeripheral) {
    if characteristic.properties.contains(.writeWithoutResponse) {
        peripheral.writeValue(data, for: characteristic, type: .withoutResponse)
    } else if characteristic.properties.contains(.write) {
        peripheral.writeValue(data, for: characteristic, type: .withResponse)
    }
}

// Confirmation callback for .withResponse writes
func peripheral(
    _ peripheral: CBPeripheral,
    didWriteValueFor characteristic: CBCharacteristic,
    error: Error?
) {
    if let error {
        print("Write failed: \(error.localizedDescription)")
    }
}
```

### Subscribing to Notifications

```swift
// Subscribe
peripheral.setNotifyValue(true, for: characteristic)

// Unsubscribe
peripheral.setNotifyValue(false, for: characteristic)

// Confirmation
func peripheral(
    _ peripheral: CBPeripheral,
    didUpdateNotificationStateFor characteristic: CBCharacteristic,
    error: Error?
) {
    if characteristic.isNotifying {
        print("Now receiving notifications for \(characteristic.uuid)")
    }
}
```

## Peripheral Role: Advertising

Publish services from the local device using `CBPeripheralManager`.

```swift
final class BLEPeripheralManager: NSObject, CBPeripheralManagerDelegate {
    private var peripheralManager: CBPeripheralManager!
    private let serviceUUID = CBUUID(string: "12345678-1234-1234-1234-123456789ABC")
    private let charUUID = CBUUID(string: "12345678-1234-1234-1234-123456789ABD")

    override init() {
        super.init()
        peripheralManager = CBPeripheralManager(delegate: self, queue: nil)
    }

    func peripheralManagerDidUpdateState(_ peripheral: CBPeripheralManager) {
        guard peripheral.state == .poweredOn else { return }
        setupService()
    }

    private func setupService() {
        let characteristic = CBMutableCharacteristic(
            type: charUUID,
            properties: [.read, .notify],
            value: nil,
            permissions: [.readable]
        )

        let service = CBMutableService(type: serviceUUID, primary: true)
        service.characteristics = [characteristic]
        peripheralManager.add(service)
    }

    func peripheralManager(
        _ peripheral: CBPeripheralManager,
        didAdd service: CBService,
        error: Error?
    ) {
        guard error == nil else { return }
        peripheralManager.startAdvertising([
            CBAdvertisementDataServiceUUIDsKey: [serviceUUID],
            CBAdvertisementDataLocalNameKey: "MyDevice"
        ])
    }
}
```

## Background BLE

### Background Central Mode

Add `bluetooth-central` to `UIBackgroundModes`. In the background:

- Scanning continues but only for specific service UUIDs
- `CBCentralManagerScanOptionAllowDuplicatesKey` is ignored (always `false`)
- Discovery callbacks are coalesced and delivered in batches

### Background Peripheral Mode

Add `bluetooth-peripheral` to `UIBackgroundModes`. In the background:

- Advertising continues but data is reduced to service UUIDs only
- The local name is not included in background advertisements

## State Restoration

State restoration allows the system to re-create your central or peripheral
manager after your app is terminated and relaunched for a BLE event.

### Central Manager State Restoration

```swift
// 1. Create with a restoration identifier
centralManager = CBCentralManager(
    delegate: self,
    queue: nil,
    options: [CBCentralManagerOptionRestoreIdentifierKey: "myCentral"]
)

// 2. Implement the restoration delegate method
func centralManager(
    _ central: CBCentralManager,
    willRestoreState dict: [String: Any]
) {
    if let peripherals = dict[CBCentralManagerRestoredStatePeripheralsKey]
        as? [CBPeripheral] {
        for peripheral in peripherals {
            // Re-assign delegate and retain
            peripheral.delegate = self
            discoveredPeripheral = peripheral
        }
    }
}
```

### Peripheral Manager State Restoration

```swift
peripheralManager = CBPeripheralManager(
    delegate: self,
    queue: nil,
    options: [CBPeripheralManagerOptionRestoreIdentifierKey: "myPeripheral"]
)

func peripheralManager(
    _ peripheral: CBPeripheralManager,
    willRestoreState dict: [String: Any]
) {
    // Restore published services, advertising state, etc.
}
```

## Common Mistakes

### DON'T: Scan or connect before poweredOn

```swift
// WRONG: Scanning immediately -- manager may not be ready
let manager = CBCentralManager(delegate: self, queue: nil)
manager.scanForPeripherals(withServices: nil) // May silently fail

// CORRECT: Wait for poweredOn in the delegate
func centralManagerDidUpdateState(_ central: CBCentralManager) {
    if central.state == .poweredOn {
        central.scanForPeripherals(withServices: [serviceUUID])
    }
}
```

### DON'T: Lose the peripheral reference

Core Bluetooth does not retain discovered peripherals. If you don't hold a
strong reference, the peripheral is deallocated and the connection fails silently.

```swift
// WRONG: No strong reference kept
func centralManager(_ central: CBCentralManager,
                    didDiscover peripheral: CBPeripheral, ...) {
    central.connect(peripheral) // peripheral may be deallocated
}

// CORRECT: Retain the peripheral
func centralManager(_ central: CBCentralManager,
                    didDiscover peripheral: CBPeripheral, ...) {
    self.discoveredPeripheral = peripheral // Strong reference
    central.connect(peripheral)
}
```

### DON'T: Scan for nil services in production

```swift
// WRONG: Discovers every BLE device in range -- drains battery
centralManager.scanForPeripherals(withServices: nil)

// CORRECT: Specify the service UUIDs you need
centralManager.scanForPeripherals(withServices: [targetServiceUUID])
```

### DON'T: Assume connection order or timing

```swift
// WRONG: Assuming immediate connection
centralManager.connect(peripheral)
discoverServicesNow() // Peripheral not connected yet

// CORRECT: Discover services in the didConnect callback
func centralManager(_ central: CBCentralManager,
                    didConnect peripheral: CBPeripheral) {
    peripheral.delegate = self
    peripheral.discoverServices([serviceUUID])
}
```

### DON'T: Write to a characteristic without checking properties

```swift
// WRONG: Crashes or silently fails if write is unsupported
peripheral.writeValue(data, for: characteristic, type: .withResponse)

// CORRECT: Check properties first
if characteristic.properties.contains(.write) {
    peripheral.writeValue(data, for: characteristic, type: .withResponse)
} else if characteristic.properties.contains(.writeWithoutResponse) {
    peripheral.writeValue(data, for: characteristic, type: .withoutResponse)
}
```

## Review Checklist

- [ ] `NSBluetoothAlwaysUsageDescription` added to Info.plist
- [ ] All BLE operations gated on `centralManagerDidUpdateState` returning `.poweredOn`
- [ ] Discovered peripherals retained with a strong reference
- [ ] Scanning uses specific service UUIDs (not `nil`) in production
- [ ] `CBPeripheralDelegate` set before calling `discoverServices`
- [ ] Characteristic properties checked before read/write/notify
- [ ] Background mode (`bluetooth-central` or `bluetooth-peripheral`) added if needed
- [ ] State restoration identifier set if app needs relaunch-on-BLE-event support
- [ ] `willRestoreState` delegate method implemented when using state restoration
- [ ] Scanning stopped after discovering the target peripheral
- [ ] Disconnection handled with optional automatic reconnect logic
- [ ] Write type matches characteristic properties (`.withResponse` vs `.withoutResponse`)

## References

- Extended patterns (reconnection strategies, data parsing, SwiftUI integration): `references/ble-patterns.md`
- [Core Bluetooth framework](https://sosumi.ai/documentation/corebluetooth)
- [CBCentralManager](https://sosumi.ai/documentation/corebluetooth/cbcentralmanager)
- [CBPeripheral](https://sosumi.ai/documentation/corebluetooth/cbperipheral)
- [CBPeripheralManager](https://sosumi.ai/documentation/corebluetooth/cbperipheralmanager)
- [CBService](https://sosumi.ai/documentation/corebluetooth/cbservice)
- [CBCharacteristic](https://sosumi.ai/documentation/corebluetooth/cbcharacteristic)
- [CBUUID](https://sosumi.ai/documentation/corebluetooth/cbuuid)
- [CBCentralManagerDelegate](https://sosumi.ai/documentation/corebluetooth/cbcentralmanagerdelegate)
- [CBPeripheralDelegate](https://sosumi.ai/documentation/corebluetooth/cbperipheraldelegate)
