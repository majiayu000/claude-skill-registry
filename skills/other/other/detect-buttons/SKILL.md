---
name: detect-buttons
description: Guide user through button detection for an unknown mouse using Slicer Python console
allowed-tools:
  - Read
context: manual
---

# Detect Buttons Skill

Guide user through button detection for an unknown mouse.

## When to Use

Use this skill when:
- User has a mouse not in the built-in profiles
- User needs to determine Qt button codes
- User wants to verify button codes on their system

## Steps

1. **Explain the Process**
   Tell the user:
   - They'll need to run code in Slicer's Python console
   - Each button press will print its Qt code
   - They should note which physical button maps to which code

2. **Provide Detection Code**
   Give the user this code to paste in Slicer Python console:

   ```python
   import qt

   class ButtonDetector(qt.QObject):
       def __init__(self):
           super().__init__()
           self.detected = []
           slicer.app.installEventFilter(self)
           print("Button detection active. Press mouse buttons...")
           print("Press Ctrl+C in console when done.")

       def eventFilter(self, obj, event):
           if event.type() == qt.QEvent.MouseButtonPress:
               btn = int(event.button())
               mods = int(event.modifiers())
               if btn not in [b[0] for b in self.detected]:
                   self.detected.append((btn, mods))
                   print(f"Detected button: {btn} (modifiers: {hex(mods)})")
           return False

       def stop(self):
           slicer.app.removeEventFilter(self)
           print("\nDetection stopped. Results:")
           for btn, mods in self.detected:
               print(f"  Button {btn}")
           return self.detected

   detector = ButtonDetector()
   # When done: detector.stop()
   ```

3. **Collect Results**
   After user runs detection, ask them to share:
   - Which button code corresponds to which physical button
   - Any buttons that weren't detected

4. **Map to Profile**
   Help user create mapping:
   ```
   Code 1  -> Left Click (not remappable)
   Code 2  -> Right Click (not remappable)
   Code 4  -> Middle Click
   Code 8  -> Back / Thumb Back
   Code 16 -> Forward / Thumb Forward
   Code 32 -> Extra button (side, thumb, etc.)
   ```

5. **Create Profile**
   Use the add-mouse-profile skill to create the profile JSON.

## Platform Notes

- **Windows**: Standard Qt codes usually work
- **macOS**: Some buttons may not generate Qt events if intercepted by system
- **Linux**: Standard codes work; evdev can detect more buttons

## Troubleshooting

**Button not detected:**
- Check if system/driver software is intercepting
- On Linux, check if user is in `input` group
- Try running Slicer as administrator (Windows)

**Wrong button detected:**
- Driver software may be remapping buttons
- Disable vendor software (Logitech Options, etc.)
- Reset mouse to default configuration

## Example Output

```
Button detection active. Press mouse buttons...
Detected button: 1 (modifiers: 0x0)      # Left click
Detected button: 2 (modifiers: 0x0)      # Right click
Detected button: 4 (modifiers: 0x0)      # Middle click
Detected button: 8 (modifiers: 0x0)      # Back
Detected button: 16 (modifiers: 0x0)     # Forward
Detected button: 32 (modifiers: 0x0)     # Thumb button
```
