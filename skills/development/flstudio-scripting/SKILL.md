---
name: flstudio-scripting
description: FL Studio Python scripting for MIDI controller development, piano roll manipulation, Edison audio editing, workflow automation, and FLP file parsing with PyFLP. Use for programmatic configuration, device customization, MIDI transport, macros, and save file manipulation. Covers all 427+ API functions across 14 MIDI scripting modules plus piano roll, Edison, and PyFLP contexts.
---

# FL Studio Python Scripting

Complete reference for FL Studio's Python API: MIDI controller scripting (14 modules, 427+ functions), piano roll note manipulation, Edison audio editing, and FLP file parsing with PyFLP.

## Quick Start

### Requirements
- FL Studio 20.8.4+, Python 3.6+

### Check API Version
```python
import general
print(f"API Version: {general.getVersion()}")
```

### Script Installation
Place scripts in `Shared\Python\User Scripts` folder.

---

## Three Scripting Contexts

### 1. MIDI Controller Scripting

**Purpose:** Control FL Studio through hardware MIDI controllers and send feedback to devices.
**Runs:** Continuously while FL Studio is open.
**Available modules:** transport, mixer, channels, arrangement, patterns, playlist, device, ui, general, plugins, screen, launchMapPages, utils, callbacks

**Entry points:**
```python
def OnInit():
    """Called when script starts."""
    pass

def OnDeInit():
    """Called when script stops."""
    pass

def OnMidiMsg(msg):
    """Called for incoming MIDI messages."""
    pass

def OnControlChange(msg):
    """Called for CC messages."""
    pass

def OnNoteOn(msg):
    """Called for note-on messages."""
    pass

def OnRefresh(flags):
    """Called when FL Studio state changes."""
    pass
```

### 2. Piano Roll Scripting

**Purpose:** Manipulate notes and markers in the piano roll editor.
**Runs:** Once when user invokes through Scripts menu.
**Available modules:** `flpianoroll`, `enveditor`

```python
import flpianoroll
score = flpianoroll.score
for note in score.notes:
    note.velocity = 0.8  # Set all velocities to 80%
```

### 3. Edison Audio Scripting

**Purpose:** Edit and process audio samples in Edison.
**Runs:** Once within Edison's context.
**Available modules:** `enveditor`

---

## API Module Reference Map

Navigate to the appropriate reference file based on what you need to control.
Read these files ONLY when you need specific API signatures.

### Core Workflow Modules

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **transport** | 20 | Play, stop, record, position, tempo, looping | [api-transport.md](references/api-transport.md) |
| **mixer** | 69 | Track volume/pan/mute/solo, EQ, routing, effects | [api-mixer.md](references/api-mixer.md) |
| **channels** | 48 | Channel rack, grid bits, step sequencer, notes | [api-channels.md](references/api-channels.md) |

### Arrangement Modules

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **arrangement** + **patterns** | 9 + 25 | Markers, time, pattern control, groups | [api-arrangement-patterns.md](references/api-arrangement-patterns.md) |
| **playlist** | 41 | Playlist tracks, live mode, performance, blocks | [api-playlist.md](references/api-playlist.md) |

### Device & Communication

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **device** | 34 | MIDI I/O, sysex, dispatch, hardware refresh | [api-device.md](references/api-device.md) |

### UI & Application Control

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **ui** + **general** | 71 + 24 | Windows, navigation, undo/redo, version, snap | [api-ui-general.md](references/api-ui-general.md) |

### Plugins

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **plugins** | 13 | Plugin parameters, presets, names, colors | [api-plugins.md](references/api-plugins.md) |

### Specialized Hardware Display

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **screen** + **launchMapPages** | 9 + 12 | AKAI Fire screen, launchpad page management | [api-screen-launchmap.md](references/api-screen-launchmap.md) |

### Utilities, Constants & MIDI Reference

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **utils** + constants | 21 | Color conversion, math, note names, MIDI tables | [api-utils-constants.md](references/api-utils-constants.md) |

### Callbacks & FlMidiMsg

| Module | Functions | What It Controls | Reference |
|--------|-----------|-----------------|-----------|
| **callbacks** | 26 | All callback functions, FlMidiMsg class, event flow | [api-callbacks.md](references/api-callbacks.md) |

---

## Non-MIDI Scripting APIs

### Piano Roll & Edison
Note, Marker, ScriptDialog, score classes for piano roll manipulation plus Edison enveditor utilities.
See [piano-roll-edison.md](references/piano-roll-edison.md)

### FLP File Parsing (PyFLP)
External library for reading/writing .flp project files without FL Studio running. Batch processing, analysis, automated generation.
See [pyflp.md](references/pyflp.md)

---

## Common Patterns

### Minimal MIDI Controller Skeleton

```python
# name=My Controller
# url=https://example.com

import device
import mixer
import transport

def OnInit():
    if device.isAssigned():
        print(f"Connected: {device.getName()}")

def OnDeInit():
    print("Script shut down")

def OnControlChange(msg):
    if msg.data1 == 7:  # Volume CC
        mixer.setTrackVolume(mixer.trackNumber(), msg.data2 / 127.0)
        msg.handled = True

def OnNoteOn(msg):
    track = msg.data1 % 8
    mixer.setActiveTrack(track)
    msg.handled = True

def OnRefresh(flags):
    pass  # Update hardware display here
```

### Key Pattern: Always Check Device Assignment

```python
def OnInit():
    if not device.isAssigned():
        print("No output device linked!")
        return
    # Safe to use device.midiOutMsg() etc.
```

### Key Pattern: Mark Events as Handled

```python
def OnControlChange(msg):
    if msg.data1 == 7:
        mixer.setTrackVolume(0, msg.data2 / 127.0)
        msg.handled = True  # Prevent FL Studio from also processing this
```

### Key Pattern: Send Feedback to Hardware

```python
def OnRefresh(flags):
    if device.isAssigned():
        # Update volume fader LED
        vol = int(mixer.getTrackVolume(0) * 127)
        device.midiOutMsg(0xB0, 0, 7, vol)
```

For complete examples (MIDI learn, scale enforcer, LED feedback, batch quantization, sysex handling, performance monitoring, automation engine, debugging):
See [examples-patterns.md](references/examples-patterns.md)

---

## Best Practices

### Performance
1. Cache module references at top level (import once)
2. Avoid tight loops in MIDI callbacks (keep under 10ms)
3. Batch UI updates; use `device.directFeedback()` for controller echo

### Hardware Integration
1. Always check `device.isAssigned()` before device functions
2. Implement two-way sync for all controls (send feedback on state change)
3. Test on real hardware (virtual ports behave differently)

### Code Organization
1. Separate MIDI mapping from business logic (use a controller class)
2. Keep callbacks responsive; offload complex work
3. Handle edge cases: invalid indices, missing devices, out-of-range values

---

## Troubleshooting

### Script Not Receiving MIDI
1. Check `device.isAssigned()` returns `True`
2. Verify MIDI input port in FL Studio MIDI Settings
3. Ensure callback functions are defined at module level (not nested)
4. Check MIDI message status bytes match expected values

### Piano Roll Script Not Working
1. Verify script is in `Shared\Python\User Scripts` folder
2. Ensure a pattern is open in piano roll before running
3. Access notes via `flpianoroll.score.notes`

### Performance Issues
1. Avoid complex calculations inside `OnIdle()` (called every ~20ms)
2. Don't repeatedly query values that haven't changed
3. Use `device.setHasMeters()` only if peak meters are needed

---

## FAQ

- **Double-click detection:** Use `device.isDoubleClick(index)`
- **Inter-script communication:** Use `device.dispatch(ctrlIndex, message)`
- **LED control:** `device.midiOutMsg(0x90, 0, note, velocity)` for note-on LEDs
- **processMIDICC vs OnControlChange:** Use `On*` callbacks for modern code
- **GUI access:** Limited through `ui` module; full UI automation not available
- **Multiple devices:** Check `device.getName()` to identify, handle per-port

---

## Resources

- **Official FL Studio API:** https://www.image-line.com/fl-studio/modules/python-scripting/
- **PyFLP GitHub:** https://github.com/demberto/PyFLP
- **API Functions:** 427+ across 14 modules | **Last Updated:** 2025
