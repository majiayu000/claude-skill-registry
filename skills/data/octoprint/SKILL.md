---
name: octoprint
description: Complete OctoPrint management skill for Raspberry Pi with Creality Ender 3D printers. Control prints, monitor temperatures, manage files, configure timelapses (Octolapse), view bed leveling mesh, troubleshoot issues, and maintain OctoPi. Supports REST API and SSH access. Use when managing 3D prints, checking printer status, uploading G-code, creating timelapses, or troubleshooting print issues.
---

# OctoPrint 3D Printer Management

A comprehensive skill for managing OctoPrint on Raspberry Pi connected to Creality Ender 3D printers. Supports full print lifecycle management, monitoring, timelapse creation, bed leveling visualization, and system maintenance.

## Session Configuration

**CRITICAL: Connection Setup**

When the user first requests an OctoPrint operation, collect the necessary connection details:

```
I need OctoPrint connection details. Please provide:

**Required for API Access:**
1. **OctoPrint URL**: (e.g., http://192.168.1.100 or http://octopi.local)
2. **API Key**: (Found in OctoPrint Settings > API > Global API Key)

**Optional for SSH/Pi Maintenance:**
3. **SSH Access**: user@host (default: pi@octopi.local)
4. **SSH Auth**: SSH Key (recommended) or password

Example response:
- URL: http://192.168.1.50
- API Key: ABCDEF123456789...
- SSH: pi@192.168.1.50 (key auth)
```

After receiving details:
- Store them in working memory for the session
- Use for ALL subsequent OctoPrint operations without re-prompting
- NEVER write API keys or credentials to files or logs

---

## Printer Profiles - Creality Ender 3 Series

| Model | Build Volume (mm) | Features |
|-------|-------------------|----------|
| Ender 3 | 220 x 220 x 250 | Basic, Bowden extruder |
| Ender 3 Pro | 220 x 220 x 250 | Magnetic bed, 40x40 Y-extrusion |
| Ender 3 V2 | 220 x 220 x 250 | Silent TMC2208 drivers, new UI |
| Ender 3 V2 Neo | 220 x 220 x 250 | CR Touch auto-leveling |
| Ender 3 S1 | 220 x 220 x 270 | Direct drive, CR Touch |
| Ender 3 S1 Pro | 220 x 220 x 270 | All-metal hotend (300C) |
| Ender 3 V3 SE | 220 x 220 x 250 | Auto-leveling, direct drive |
| Ender 3 V3 KE | 220 x 220 x 240 | Klipper-based, fast printing |

**Default OctoPrint Settings for Ender 3 V2:**
- Origin: Lower Left
- Heated Bed: Yes
- Heated Chamber: No
- Default Baudrate: 115200
- Print Volume: X=220, Y=220, Z=250

---

## Quick Reference

### REST API Base

```
Base URL: http://<OCTOPRINT_HOST>/api/
Auth Header: X-Api-Key: <API_KEY>
Content-Type: application/json
```

### Common Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/version` | API and server version |
| GET | `/api/connection` | Printer connection state |
| POST | `/api/connection` | Connect/disconnect printer |
| GET | `/api/printer` | Full printer state |
| GET | `/api/printer/tool` | Tool temperatures |
| GET | `/api/printer/bed` | Bed temperature |
| GET | `/api/job` | Current job status |
| POST | `/api/job` | Start/cancel/pause job |
| GET | `/api/files` | List all files |
| POST | `/api/files/local` | Upload file |
| POST | `/api/printer/command` | Send G-code commands |

---

## Connection Management

### Check Connection Status

```bash
curl -s "http://OCTOPRINT_HOST/api/connection" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

**Response includes:**
- `current.state`: Operational, Printing, Paused, Closed, Error
- `current.port`: /dev/ttyUSB0, /dev/ttyACM0, etc.
- `current.baudrate`: 115200 (typical for Ender 3)
- `options`: Available ports, baudrates, profiles

### Connect to Printer

```bash
curl -X POST "http://OCTOPRINT_HOST/api/connection" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "connect", "port": "/dev/ttyUSB0", "baudrate": 115200}'
```

### Disconnect Printer

```bash
curl -X POST "http://OCTOPRINT_HOST/api/connection" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "disconnect"}'
```

### Auto-Connect (Use Saved Settings)

```bash
curl -X POST "http://OCTOPRINT_HOST/api/connection" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "connect"}'
```

---

## Print Job Management

### Get Current Job Status

```bash
curl -s "http://OCTOPRINT_HOST/api/job" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

**Response includes:**
- `state`: Printing, Paused, Operational, etc.
- `job.file.name`: Current file name
- `progress.completion`: Percentage (0-100)
- `progress.printTime`: Elapsed seconds
- `progress.printTimeLeft`: Remaining seconds

### Start Print

```bash
# Select and start a file
curl -X POST "http://OCTOPRINT_HOST/api/files/local/myfile.gcode" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "select", "print": true}'
```

### Pause Print

```bash
curl -X POST "http://OCTOPRINT_HOST/api/job" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "pause", "action": "pause"}'
```

### Resume Print

```bash
curl -X POST "http://OCTOPRINT_HOST/api/job" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "pause", "action": "resume"}'
```

### Cancel Print

```bash
curl -X POST "http://OCTOPRINT_HOST/api/job" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "cancel"}'
```

---

## Temperature Control

### Get Current Temperatures

```bash
# All temperatures
curl -s "http://OCTOPRINT_HOST/api/printer" \
  -H "X-Api-Key: API_KEY" | jq '.temperature'

# Tool (hotend) only
curl -s "http://OCTOPRINT_HOST/api/printer/tool" \
  -H "X-Api-Key: API_KEY" | jq '.'

# Bed only
curl -s "http://OCTOPRINT_HOST/api/printer/bed" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

### Set Hotend Temperature

```bash
# Heat to 200°C (PLA)
curl -X POST "http://OCTOPRINT_HOST/api/printer/tool" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "target", "targets": {"tool0": 200}}'

# Cool down (set to 0)
curl -X POST "http://OCTOPRINT_HOST/api/printer/tool" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "target", "targets": {"tool0": 0}}'
```

### Set Bed Temperature

```bash
# Heat bed to 60°C (PLA)
curl -X POST "http://OCTOPRINT_HOST/api/printer/bed" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "target", "target": 60}'

# Cool down bed
curl -X POST "http://OCTOPRINT_HOST/api/printer/bed" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "target", "target": 0}'
```

### Common Temperature Presets

| Material | Hotend (°C) | Bed (°C) |
|----------|-------------|----------|
| PLA | 190-210 | 50-60 |
| PETG | 230-250 | 70-80 |
| ABS | 230-250 | 90-110 |
| TPU | 220-240 | 40-60 |
| ASA | 240-260 | 90-110 |

---

## File Management

### List Files

```bash
# All files
curl -s "http://OCTOPRINT_HOST/api/files" \
  -H "X-Api-Key: API_KEY" | jq '.files[].name'

# With details
curl -s "http://OCTOPRINT_HOST/api/files?recursive=true" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

### Upload File

```bash
# Upload G-code file
curl -X POST "http://OCTOPRINT_HOST/api/files/local" \
  -H "X-Api-Key: API_KEY" \
  -F "file=@/path/to/file.gcode"

# Upload and start printing immediately
curl -X POST "http://OCTOPRINT_HOST/api/files/local" \
  -H "X-Api-Key: API_KEY" \
  -F "file=@/path/to/file.gcode" \
  -F "print=true"

# Upload to specific folder
curl -X POST "http://OCTOPRINT_HOST/api/files/local" \
  -H "X-Api-Key: API_KEY" \
  -F "file=@/path/to/file.gcode" \
  -F "path=myfolder"
```

### Delete File

```bash
curl -X DELETE "http://OCTOPRINT_HOST/api/files/local/filename.gcode" \
  -H "X-Api-Key: API_KEY"
```

### Get File Info

```bash
curl -s "http://OCTOPRINT_HOST/api/files/local/filename.gcode" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

---

## Print Head & Axis Control

### Home Axes

```bash
# Home all axes
curl -X POST "http://OCTOPRINT_HOST/api/printer/printhead" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "home", "axes": ["x", "y", "z"]}'

# Home X and Y only
curl -X POST "http://OCTOPRINT_HOST/api/printer/printhead" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "home", "axes": ["x", "y"]}'
```

### Jog Print Head

```bash
# Move X +10mm
curl -X POST "http://OCTOPRINT_HOST/api/printer/printhead" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "jog", "x": 10}'

# Move Y -20mm, Z +5mm
curl -X POST "http://OCTOPRINT_HOST/api/printer/printhead" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "jog", "y": -20, "z": 5}'

# Move with specific feedrate (mm/min)
curl -X POST "http://OCTOPRINT_HOST/api/printer/printhead" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "jog", "x": 10, "speed": 3000}'
```

### Extrude/Retract Filament

```bash
# Extrude 10mm
curl -X POST "http://OCTOPRINT_HOST/api/printer/tool" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "extrude", "amount": 10}'

# Retract 5mm (negative value)
curl -X POST "http://OCTOPRINT_HOST/api/printer/tool" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "extrude", "amount": -5}'
```

---

## G-code Commands

### Send Single Command

```bash
curl -X POST "http://OCTOPRINT_HOST/api/printer/command" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "G28"}'
```

### Send Multiple Commands

```bash
curl -X POST "http://OCTOPRINT_HOST/api/printer/command" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"commands": ["G28", "G1 Z10 F300", "M104 S200"]}'
```

### Common G-code Commands for Ender 3

| Command | Description |
|---------|-------------|
| `G28` | Home all axes |
| `G28 X Y` | Home X and Y only |
| `G28 Z` | Home Z only |
| `G29` | Auto bed leveling (if equipped) |
| `G1 X100 Y100 F3000` | Move to X100 Y100 at 50mm/s |
| `G1 Z10 F300` | Move Z to 10mm at 5mm/s |
| `M104 S200` | Set hotend to 200°C (no wait) |
| `M109 S200` | Wait for hotend to reach 200°C |
| `M140 S60` | Set bed to 60°C (no wait) |
| `M190 S60` | Wait for bed to reach 60°C |
| `M106 S255` | Fan 100% |
| `M106 S127` | Fan 50% |
| `M107` | Fan off |
| `M84` | Disable steppers |
| `M500` | Save settings to EEPROM |
| `M501` | Load settings from EEPROM |
| `M503` | Report current settings |
| `M420 S1` | Enable saved mesh leveling |
| `M420 V` | View current mesh |

---

## Bed Leveling (with Bed Level Visualizer Plugin)

### Trigger Bed Mesh Probe

```bash
# Run auto bed level probe (G29)
curl -X POST "http://OCTOPRINT_HOST/api/printer/command" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "G29"}'
```

### View Current Mesh (via G-code)

```bash
# Report mesh values
curl -X POST "http://OCTOPRINT_HOST/api/printer/command" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "M420 V"}'
```

### Plugin API (Bed Level Visualizer)

```bash
# Trigger mesh update (plugin-specific)
curl -X POST "http://OCTOPRINT_HOST/api/plugin/bedlevelvisualizer" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "mesh"}'
```

### Manual Bed Leveling Procedure

For printers without auto bed leveling:

1. **Preheat bed** to printing temperature (60°C for PLA)
2. **Home all axes**: `G28`
3. **Move to corners** and adjust:
   - Front Left: `G1 X30 Y30 F3000`
   - Front Right: `G1 X190 Y30 F3000`
   - Back Right: `G1 X190 Y190 F3000`
   - Back Left: `G1 X30 Y190 F3000`
   - Center: `G1 X110 Y110 F3000`
4. **Paper test**: Adjust knobs for slight friction
5. **Repeat** until consistent

---

## Timelapse (Octolapse Plugin)

### Octolapse API Endpoints

```bash
# Get Octolapse status
curl -s "http://OCTOPRINT_HOST/plugin/octolapse/status" \
  -H "X-Api-Key: API_KEY" | jq '.'

# Get available profiles
curl -s "http://OCTOPRINT_HOST/plugin/octolapse/settings" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

### Octolapse Configuration Tips

**Recommended settings for Ender 3 V2:**

1. **Printer Profile**: Select "Creality Ender 3" or create custom
2. **Stabilization**:
   - Type: "Smart - Layer Change Only"
   - Position: Back-left corner (X=0, Y=220)
3. **Snapshot Trigger**:
   - Layer change (smoothest results)
   - Timer-based for quick prints
4. **Camera Settings**:
   - USB webcam: Use mjpg-streamer
   - Pi Camera: Use raspistill or libcamera

### Octolapse Start/Stop via API

```bash
# Check if Octolapse is active
curl -s "http://OCTOPRINT_HOST/plugin/octolapse/status" \
  -H "X-Api-Key: API_KEY" | jq '.is_timelapse_active'
```

### Download Timelapses

```bash
# List completed timelapses
curl -s "http://OCTOPRINT_HOST/api/timelapse" \
  -H "X-Api-Key: API_KEY" | jq '.files[].name'

# Download specific timelapse
curl -O "http://OCTOPRINT_HOST/downloads/timelapse/filename.mp4" \
  -H "X-Api-Key: API_KEY"
```

---

## Webcam & Monitoring

### Webcam Stream URLs

```
# MJPG Stream (default)
http://OCTOPRINT_HOST/webcam/?action=stream

# Snapshot
http://OCTOPRINT_HOST/webcam/?action=snapshot
```

### Get Webcam Settings

```bash
curl -s "http://OCTOPRINT_HOST/api/settings" \
  -H "X-Api-Key: API_KEY" | jq '.webcam'
```

### Raspberry Pi Camera Setup

```bash
# SSH to Pi, then check camera
ssh pi@octopi.local

# Test camera (legacy raspistill)
raspistill -o test.jpg

# Test camera (libcamera - newer)
libcamera-still -o test.jpg

# Restart webcam service
sudo systemctl restart webcamd
```

---

## OctoEverywhere / Obico Integration

### Remote Access Setup

If you have OctoEverywhere or Obico installed:

```bash
# Check plugin status
curl -s "http://OCTOPRINT_HOST/api/plugin/octoeverywhere" \
  -H "X-Api-Key: API_KEY" | jq '.'

# Or for Obico
curl -s "http://OCTOPRINT_HOST/api/plugin/obico" \
  -H "X-Api-Key: API_KEY" | jq '.'
```

### Features Available
- Remote access from anywhere (no port forwarding)
- AI-powered print failure detection
- Mobile notifications
- Gadget integration (smart speakers, etc.)

---

## System Management (SSH)

### OctoPi Service Control

```bash
# SSH to OctoPi
ssh pi@octopi.local

# Restart OctoPrint
sudo systemctl restart octoprint

# Check OctoPrint status
sudo systemctl status octoprint

# View OctoPrint logs
sudo journalctl -u octoprint -f

# View webcam logs
sudo journalctl -u webcamd -f
```

### System Health

```bash
# Check disk space
ssh pi@octopi.local "df -h"

# Check memory
ssh pi@octopi.local "free -h"

# Check CPU temperature (important for Pi!)
ssh pi@octopi.local "vcgencmd measure_temp"

# Check if throttled (power issues)
ssh pi@octopi.local "vcgencmd get_throttled"
# 0x0 = OK, anything else = issues
```

### Update OctoPrint

```bash
# Via SSH
ssh pi@octopi.local
~/oprint/bin/pip install --upgrade octoprint

# Or via OctoPrint UI: Settings > Software Update
```

### Backup OctoPrint

```bash
# Create backup
ssh pi@octopi.local "tar -czvf ~/octoprint-backup-$(date +%Y%m%d).tar.gz ~/.octoprint"

# Download backup
scp pi@octopi.local:~/octoprint-backup-*.tar.gz ./
```

---

## Troubleshooting

### Common Issues

| Issue | Diagnostic | Solution |
|-------|-----------|----------|
| Printer not connecting | Check USB cable, port | Try different cable, check `/dev/ttyUSB*` |
| API 403 Forbidden | Invalid API key | Regenerate key in Settings > API |
| Prints failing mid-way | Power/temperature | Check PSU, enable thermal runaway |
| Layer shifts | Belt tension, speed | Tighten belts, reduce print speed |
| Stringing | Temperature, retraction | Lower temp, increase retraction |
| First layer not sticking | Bed level, Z-offset | Re-level bed, adjust Z-offset |
| Webcam not working | Service status | `sudo systemctl restart webcamd` |
| Pi overheating | Cooling | Add heatsink/fan, check `vcgencmd measure_temp` |

### Check OctoPrint Logs

```bash
# Via API
curl -s "http://OCTOPRINT_HOST/api/logs" \
  -H "X-Api-Key: API_KEY" | jq '.logs'

# Via SSH
ssh pi@octopi.local "tail -100 ~/.octoprint/logs/octoprint.log"
```

### Serial Connection Debug

```bash
# Check available ports
ssh pi@octopi.local "ls -la /dev/ttyUSB* /dev/ttyACM* 2>/dev/null"

# Check permissions
ssh pi@octopi.local "groups pi"  # Should include 'dialout'

# Test serial manually
ssh pi@octopi.local "screen /dev/ttyUSB0 115200"  # Ctrl-A, K to exit
```

### Power Issues (Raspberry Pi)

```bash
# Check for undervoltage
ssh pi@octopi.local "dmesg | grep -i voltage"

# Check throttling status
ssh pi@octopi.local "vcgencmd get_throttled"
# Decode: https://github.com/raspberrypi/documentation/blob/master/hardware/raspberrypi/frequency-management.md
```

---

## Safety & Best Practices

### Before Printing
1. Ensure bed is clean (IPA wipe)
2. Check filament path is clear
3. Verify temperatures match material
4. Confirm first layer adhesion

### During Printing
1. Monitor first few layers
2. Watch for thermal runaway
3. Keep camera running for remote monitoring
4. Set up failure detection (Obico AI)

### Emergency Commands

```bash
# Emergency stop (via G-code)
curl -X POST "http://OCTOPRINT_HOST/api/printer/command" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "M112"}'

# Cancel current print
curl -X POST "http://OCTOPRINT_HOST/api/job" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "cancel"}'

# Disable heaters immediately
curl -X POST "http://OCTOPRINT_HOST/api/printer/command" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"commands": ["M104 S0", "M140 S0"]}'
```

---

## When to Use This Skill

- "Check my 3D printer status"
- "What's the temperature of my printer?"
- "Upload this G-code file to OctoPrint"
- "Start/pause/cancel the print"
- "Heat the bed to 60 degrees"
- "Home the printer"
- "Create a timelapse of my print"
- "Check my bed level mesh"
- "Troubleshoot why my print failed"
- "Connect to my Ender 3"
- "Extrude some filament"
- "Move the print head"
- "Check OctoPrint logs"
- "Restart OctoPrint service"

## When NOT to Use This Skill

- Slicing STL files (use slicer software: Cura, PrusaSlicer)
- CAD design (use Fusion 360, TinkerCAD, etc.)
- Klipper-based printers (different API)
- Printers not connected to OctoPrint

---

## Cross-Platform SSH Notes

For SSH access to the Raspberry Pi, follow the same platform-specific approaches as the SSH Server Admin skill:

**With SSH Keys (All Platforms):**
```bash
ssh -o StrictHostKeyChecking=accept-new pi@octopi.local "command"
```

**With Password - Windows:**
```powershell
# Use Python helper
python scripts/ssh_helper.py --host octopi.local --user pi --password "raspberry" --command "vcgencmd measure_temp"
```

**With Password - macOS/Linux:**
```bash
sshpass -p 'raspberry' ssh pi@octopi.local "vcgencmd measure_temp"
```

---

## Version History

- v1.0.0 (2025-12-20): Initial release with full API support, Ender 3 profiles, Octolapse, Bed Level Visualizer, and OctoEverywhere integration
