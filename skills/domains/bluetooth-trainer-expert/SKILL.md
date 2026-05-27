---
name: bluetooth-trainer-expert
description: Expert guidance on reverse-engineering, testing, and integrating Bluetooth Smart Trainers (Wahoo/FTMS) for fitness applications. Use when building or debugging cycling apps.
---

# Bluetooth Trainer Expert

This skill provides a proven workflow for developing biking fitness applications that interact with Smart Trainers (e.g., Wahoo KICKR, FTMS devices). It emphasizes a "Console First" approach to isolate connection and protocol logic before attempting UI integration.

## Core Philosophy

1.  **Console First**: Always prove the protocol logic in a simple C# Console Application (`BikeFitnessConsole`) before touching the main UI (WPF/MAUI).
2.  **Physical Verification**: Telemetry (Success/Fail responses) is insufficient for brake logic. You MUST ask the user to "Pedal and verify resistance change" to confirm the device actually engaged the magnet/motor.
3.  **Protocol Agnosticism**: Support both standard FTMS (`0x1826`) and legacy Wahoo (`0xA026...`) protocols.

## Phase 1: Diagnostic Console App

Create a lightweight console app to handle scanning, connection, and raw command testing.

**Key Features to Implement:**
-   **Scanner**: Filter for `0x1826` (FTMS), `0xA026` (Wahoo), and `0x1818` (Power).
-   **Service Explorer**: List all available Services and Characteristics to confirm UUIDs.
-   **Indication Handler**: **CRITICAL**. You must subscribe to `Indicate` on the Control Point characteristic *before* sending any write commands. Failure to do so often results in silent failures or "Attribute Not Found" errors on writes.

## Data Format (Endianness)

**Bluetooth LE GATT characteristics standardly use Little Endian byte order.**

-   **Reading**: When parsing multi-byte values (e.g., Speed, Power, Time), interpret the *least significant byte first*.
    -   Example: `0xE8 0x03` -> `0x03E8` -> `1000`.
-   **Writing**: When constructing commands (e.g., Target Watts, Grade), ensure you serialize `UInt16`/`Int16` values to Little Endian.
-   **Note**: While standard FTMS and common Wahoo OpCodes (`0x40-0x45`) follow Little Endian, always verify proprietary manufacturer-specific characteristics if behavior is unexpected.

## Phase 2: Protocol Identification & Control Points

Identify the correct Control Point (CP) for the device.

### 1. FTMS (Fitness Machine Service) - Preferred
*   **Service UUID**: `00001826-0000-1000-8000-00805f9b34fb`
*   **Control Point**: `00002ad9-0000-1000-8000-00805f9b34fb` (Fitness Machine Control Point)
*   **Init Sequence**:
    1.  Subscribe to CP Indications.
    2.  Send `0x00` (Request Control).
    3.  Send `0x07` (Start/Resume).

### 2. Wahoo Legacy (KICKR / SNAP)
*   **Service UUID**: `a026ee01-0a7d-4ab3-97fa-f1500f9feb8b`
*   **Control Point**: `a026e005-0a7d-4ab3-97fa-f1500f9feb8b` (Often hidden inside the Power Service `0x1818` on some firmware).
*   **Init Sequence**:
    1.  Subscribe to CP Indications.
    2.  Send `0x00` (Init/Unlock).

## Phase 3: OpCode Discovery Strategy

Different devices support different modes. Use the Console App to "Scan" OpCodes `0x40` through `0x45` by sending `[OpCode, 0x00]` and observing the Indication response.

*   **Response Format**: `01-OpCode-Result` (Where Result `01` = Success, `04` = Not Supported, `40` = Fail).
*   **Common OpCodes**:
    *   `0x40` **Level Mode**: 0-9 discrete levels. Basic.
    *   `0x41` **Resistance Mode**: 0-100% brake force. Most reliable.
    *   `0x42` **Sim Mode Enable**: Activates physics engine (Grade/Wind/Weight). **Warning**: Many older or lower-end devices (e.g., KICKR SNAP) return "Success" for params but FAIL (`0x40`) when trying to Enable this mode.
    *   `0x43` **Sim Parameters**: Sets Grade, Weight, Crr, Cw.

## Phase 4: "Fake" Simulation Mode (Grade Mapping)

If the device fails to support Native Sim Mode (`0x42`), you must implement **Grade-to-Resistance Mapping** in software to support "Hilly" or "Mountain" workouts.

**Recommended Mapping (User Calibrated):**
Map the visual "Grade %" to the device's "Resistance %" (OpCode `0x41`).

| Grade Input | Resistance Output | Feel |
| :--- | :--- | :--- |
| **-10%** | **0.0%** | Coasting / Free spin. |
| **0%** | **1.0%** | Flat road friction (light). |
| **20%** | **40.0%** | Steep climb. (Cap at 40% to avoid "brick wall"). |

**Logic:**
Use a piecewise linear function:
1.  **Downhill (-10 to 0)**: Interpolate 0.0 -> 0.01.
2.  **Uphill (0 to 20)**: Interpolate 0.01 -> 0.40.

## Phase 5: Telemetry

*   **Power**: Standard `0x2A63` (Cycling Power Measurement).
*   **Speed/Distance**: Often missing from FTMS on older devices. Calculate locally using **Wheel Revolutions** from the Power Measurement characteristic (Data bytes `flags & 0x10`).
    *   `Distance = WheelRevs * TireCircumference`
    *   `Speed = DeltaDistance / DeltaTime`
*   **Cadence**: Check `0x1816` (Speed & Cadence) or Crank Data in Power (`0x1818`).

## Checklist for Implementation

1.  [ ] **Console Test**: Can you connect and receive Indications?
2.  [ ] **OpCode Scan**: Which modes return `01` (Success)?
3.  [ ] **Physical Test**: Does sending `0x41 0x32` (50% res) make it hard to pedal?
4.  [ ] **Mapping**: Does -10% Grade feel like zero resistance?
5.  [ ] **UI**: Does the UI display Grade (not raw resistance) to the user?