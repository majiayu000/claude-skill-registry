---
name: sphero-mini
description: Control Sphero Mini robot ball via Bluetooth Low Energy. Roll, change colors, read sensors, draw shapes, and play with cats. Uses bleak for cross-platform BLE support (macOS/Windows/Linux).
homepage: https://github.com/trflorian/sphero_mini_win
metadata:
  {
    "openclaw":
      {
        "emoji": "⚽",
        "requires": { "bins": ["python3"], "packages": ["bleak"] },
        "install":
          [
            {
              "id": "sphero-bleak",
              "kind": "pip",
              "package": "bleak",
              "label": "Install bleak (Bluetooth Low Energy library for macOS/Windows/Linux)",
            },
          ],
      },
  }
---

# Sphero Mini Control

Control your Sphero Mini robot ball via Bluetooth Low Energy using Python and bleak.

## Features

- 🎨 **LED Control** - Change main LED color and back LED intensity
- 🎯 **Movement** - Roll in any direction at variable speeds
- 🎲 **Random Mode** - Cat play mode with unpredictable movements
- 📐 **Draw Shapes** - Squares, stars, circles with programmable patterns
- 🔋 **Power Management** - Wake, sleep, and check battery status
- 🧭 **Heading Control** - Reset and control orientation
- 🖥️ **Cross-platform** - Works on macOS, Windows, and Linux (uses bleak, not bluepy)

## Setup

### 1. Install Dependencies

**All platforms:**
```bash
pip3 install bleak
```

### 2. Find Your Sphero Mini's MAC/UUID

**macOS/Windows:**
Use the included scan script:
```bash
python3 scripts/scan_sphero.py
```

Look for a device named like "SM-XXXX" (Sphero Mini).

### 3. Update MAC Address

Edit the scripts and replace `SPHERO_MAC` with your device's address.

## Quick Start

### Scan for Sphero Mini

```bash
python3 scripts/scan_sphero.py
```

### Change Color

```python
import asyncio
from sphero_mini_bleak import SpheroMini

async def change_color():
    sphero = SpheroMini("YOUR-MAC-ADDRESS")
    await sphero.connect()
    await sphero.wake()
    
    # Set to red
    await sphero.setLEDColor(255, 0, 0)
    await asyncio.sleep(2)
    
    await sphero.disconnect()

asyncio.run(change_color())
```

### Roll Forward

```python
import asyncio
from sphero_mini_bleak import SpheroMini

async def roll_forward():
    sphero = SpheroMini("YOUR-MAC-ADDRESS")
    await sphero.connect()
    await sphero.wake()
    
    # Roll forward at speed 100
    await sphero.roll(100, 0)
    await asyncio.sleep(3)
    
    # Stop
    await sphero.roll(0, 0)
    await sphero.disconnect()

asyncio.run(roll_forward())
```

## Pre-built Scripts

### 🐱 Cat Play Mode (Random Movement)

```bash
python3 scripts/cat_play.py
```

Makes Sphero move randomly for 1 minute with color changes - perfect for playing with cats!

### 📐 Draw Shapes

```bash
# Draw a square
python3 scripts/draw_square.py

# Draw a star
python3 scripts/draw_star.py
```

### 🎨 Color Control

```bash
# Set specific color
python3 scripts/set_color.py red
python3 scripts/set_color.py 255 0 128  # Custom RGB
```

## Common Commands

### Movement
```python
# Roll (speed: 0-255, heading: 0-359 degrees)
await sphero.roll(speed=100, heading=0)    # Forward
await sphero.roll(100, 90)                  # Right
await sphero.roll(100, 180)                 # Backward
await sphero.roll(100, 270)                 # Left
await sphero.roll(0, 0)                     # Stop
```

### LED Control
```python
# Main LED color (RGB values 0-255)
await sphero.setLEDColor(red=255, green=0, blue=0)      # Red
await sphero.setLEDColor(0, 255, 0)                     # Green
await sphero.setLEDColor(0, 0, 255)                     # Blue
await sphero.setLEDColor(128, 0, 128)                   # Purple

# Back LED brightness (0-255)
await sphero.setBackLED(255)  # Full brightness
await sphero.setBackLED(0)    # Off
```

### Power Management
```python
# Wake from sleep
await sphero.wake()

# Go to sleep (low power, BLE still on)
await sphero.sleep()

# Check battery voltage
voltage = await sphero.getBatteryVoltage()
print(f"Battery: {voltage}V")
```

## Tips

- **Wake Sphero**: Shake it to wake from deep sleep before connecting
- **Connection timeout**: If connection fails, shake Sphero and try again
- **Finding Sphero**: After scripts finish, Sphero is set to white for easy visibility
- **Cat safety**: Use soft surfaces when playing with cats to avoid damage

## Example: Cat Play Mode

The cat play mode script makes Sphero:
- Move in random directions (40-120 speed)
- Change colors randomly (6 vibrant colors)
- Stop unpredictably (30% chance for brief pauses)
- Run for exactly 1 minute
- End with white color so you can find it

Perfect for entertaining cats! 🐱

## Troubleshooting

### Cannot Connect

1. Shake Sphero to wake it up
2. Ensure it's not connected to the Sphero Edu app
3. Check MAC/UUID address is correct
4. Try increasing timeout in `sphero_mini_bleak.py`

### Sphero Doesn't Move

1. Call `await sphero.wake()` first
2. Wait 1-2 seconds after waking
3. Check battery level

### Colors Don't Change

1. Add `await asyncio.sleep(0.5)` between color changes
2. Ensure you called `await sphero.wake()`

## Library Credits

This skill uses:
- [sphero_mini_win](https://github.com/trflorian/sphero_mini_win) by trflorian - Sphero Mini control library using bleak
- [bleak](https://github.com/hbldh/bleak) - Cross-platform Bluetooth Low Energy library

**Note**: This library is for **Sphero Mini only**. For other Sphero models (BB8, SPRK+, Bolt), use [pysphero](https://github.com/EnotYoyo/pysphero) instead.

## Advanced Usage

### Custom Patterns

Create your own movement patterns:

```python
async def figure_eight():
    # Draw a figure-8 pattern
    for i in range(2):  # Two loops
        for heading in range(0, 360, 10):
            await sphero.roll(80, heading)
            await asyncio.sleep(0.1)
```

### Color Cycling

```python
async def rainbow():
    colors = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0),
        (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
    ]
    for r, g, b in colors:
        await sphero.setLEDColor(r, g, b)
        await asyncio.sleep(1)
```

## Documentation

- **SKILL.md** — This file
- **references/api.md** — Complete API reference
- **references/troubleshooting.md** — Common issues and solutions
- **scripts/** — Ready-to-use example scripts

## License

MIT
