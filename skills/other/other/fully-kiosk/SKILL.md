---
name: fully-kiosk
description: Comprehensive Fully Kiosk Browser management for Android tablets and kiosk devices. Control screen, brightness, URLs, screensavers, TTS, media playback. Manage device fleets via REST API, MQTT, Fully Cloud. Integrate with Home Assistant. Configure kiosk mode, motion detection, remote admin. Supports Fire tablets, Android tablets, wall panels. Use for dashboards, digital signage, locked kiosks.
version: 1.0.0
---

# Fully Kiosk Browser Management Skill

Complete management and configuration of Fully Kiosk Browser deployments across Android devices including Amazon Fire tablets, Samsung tablets, and wall-mounted panels.

## Overview

Fully Kiosk Browser is an Android app that transforms tablets into secure kiosk displays, digital signage, or smart home dashboards. This skill provides:

- **REST API Control**: 70+ commands for device management
- **Fleet Management**: Multi-device batch operations
- **Fully Cloud Integration**: Centralized cloud management
- **Home Assistant Integration**: Native HA integration + MQTT
- **Configuration Templates**: Pre-built configs for common use cases

## Quick Reference

### REST API Base URL
```
http://<device-ip>:2323/?cmd=<command>&password=<password>&type=json
```

### Essential Commands

| Command | Description |
|---------|-------------|
| `deviceInfo` | Get device status, battery, storage |
| `screenOn` / `screenOff` | Control display |
| `loadStartUrl` | Load configured home page |
| `loadUrl&url=<url>` | Navigate to specific URL |
| `startScreensaver` / `stopScreensaver` | Screensaver control |
| `textToSpeech&text=<text>` | Speak text aloud |
| `playSound&url=<url>` | Play audio file |
| `setStringSetting&key=<key>&value=<val>` | Change setting |
| `listSettings` | Get all current settings |

## Device Management

### Get Device Information
```bash
# Basic device info
curl "http://192.168.1.100:2323/?cmd=deviceInfo&type=json&password=YOUR_PASSWORD"

# Response includes:
# - deviceID, deviceName, deviceModel
# - batteryLevel, isPlugged
# - screenOn, screenBrightness
# - currentTabUrl, wifiSSID
# - ip4, mac, appVersion
```

### Screen Control
```bash
# Turn screen on
curl "http://192.168.1.100:2323/?cmd=screenOn&password=YOUR_PASSWORD"

# Turn screen off
curl "http://192.168.1.100:2323/?cmd=screenOff&password=YOUR_PASSWORD"

# Set brightness (0-255)
curl "http://192.168.1.100:2323/?cmd=setStringSetting&key=screenBrightness&value=128&password=YOUR_PASSWORD"

# Force device sleep
curl "http://192.168.1.100:2323/?cmd=forceSleep&password=YOUR_PASSWORD"

# Trigger motion (simulate motion detection)
curl "http://192.168.1.100:2323/?cmd=triggerMotion&password=YOUR_PASSWORD"
```

### URL Navigation
```bash
# Load home URL
curl "http://192.168.1.100:2323/?cmd=loadStartUrl&password=YOUR_PASSWORD"

# Load specific URL
curl "http://192.168.1.100:2323/?cmd=loadUrl&url=http://homeassistant.local:8123&password=YOUR_PASSWORD"

# Open in new tab
curl "http://192.168.1.100:2323/?cmd=loadUrl&url=http://example.com&newtab=true&focus=true&password=YOUR_PASSWORD"

# Switch to tab by index
curl "http://192.168.1.100:2323/?cmd=focusTab&tab=0&password=YOUR_PASSWORD"

# Refresh current tab
curl "http://192.168.1.100:2323/?cmd=refreshTab&password=YOUR_PASSWORD"

# Close tab
curl "http://192.168.1.100:2323/?cmd=closeTab&tab=1&password=YOUR_PASSWORD"
```

### Audio & Text-to-Speech
```bash
# Text to speech
curl "http://192.168.1.100:2323/?cmd=textToSpeech&text=Doorbell%20rang&password=YOUR_PASSWORD"

# TTS with locale
curl "http://192.168.1.100:2323/?cmd=textToSpeech&text=Hello&locale=en_US&password=YOUR_PASSWORD"

# Play sound file
curl "http://192.168.1.100:2323/?cmd=playSound&url=http://server/doorbell.mp3&password=YOUR_PASSWORD"

# Play looping sound
curl "http://192.168.1.100:2323/?cmd=playSound&url=http://server/alarm.mp3&loop=true&password=YOUR_PASSWORD"

# Stop sound
curl "http://192.168.1.100:2323/?cmd=stopSound&password=YOUR_PASSWORD"

# Set volume (0-100, stream 3=Music)
curl "http://192.168.1.100:2323/?cmd=setAudioVolume&level=50&stream=3&password=YOUR_PASSWORD"
```

**Audio Stream Codes:**
- 0: Voice Call
- 1: System
- 2: Ring
- 3: Music (most common)
- 4: Alarm
- 5: Notification
- 9: TTS
- 10: Accessibility

### Video Playback
```bash
# Play video
curl "http://192.168.1.100:2323/?cmd=playVideo&url=http://server/video.mp4&loop=0&showControls=1&exitOnTouch=1&password=YOUR_PASSWORD"

# Stop video
curl "http://192.168.1.100:2323/?cmd=stopVideo&password=YOUR_PASSWORD"
```

### Screensaver Control
```bash
# Start screensaver
curl "http://192.168.1.100:2323/?cmd=startScreensaver&password=YOUR_PASSWORD"

# Stop screensaver
curl "http://192.168.1.100:2323/?cmd=stopScreensaver&password=YOUR_PASSWORD"

# Start Android Daydream
curl "http://192.168.1.100:2323/?cmd=startDaydream&password=YOUR_PASSWORD"
```

### Kiosk Mode
```bash
# Lock kiosk (enable kiosk mode)
curl "http://192.168.1.100:2323/?cmd=lockKiosk&password=YOUR_PASSWORD"

# Unlock kiosk
curl "http://192.168.1.100:2323/?cmd=unlockKiosk&password=YOUR_PASSWORD"

# Enable maintenance/locked mode
curl "http://192.168.1.100:2323/?cmd=enableLockedMode&password=YOUR_PASSWORD"

# Display overlay message
curl "http://192.168.1.100:2323/?cmd=setOverlayMessage&text=Maintenance%20Mode&password=YOUR_PASSWORD"
```

### Application Management
```bash
# Bring Fully to foreground
curl "http://192.168.1.100:2323/?cmd=toForeground&password=YOUR_PASSWORD"

# Send to background
curl "http://192.168.1.100:2323/?cmd=toBackground&password=YOUR_PASSWORD"

# Start another app
curl "http://192.168.1.100:2323/?cmd=startApplication&package=com.spotify.music&password=YOUR_PASSWORD"

# Restart Fully
curl "http://192.168.1.100:2323/?cmd=restartApp&password=YOUR_PASSWORD"

# Exit Fully
curl "http://192.168.1.100:2323/?cmd=exitApp&password=YOUR_PASSWORD"
```

### Cache & Storage
```bash
# Clear browser cache
curl "http://192.168.1.100:2323/?cmd=clearCache&password=YOUR_PASSWORD"

# Clear web storage (localStorage, sessionStorage)
curl "http://192.168.1.100:2323/?cmd=clearWebstorage&password=YOUR_PASSWORD"

# Clear cookies
curl "http://192.168.1.100:2323/?cmd=clearCookies&password=YOUR_PASSWORD"

# Reset WebView completely
curl "http://192.168.1.100:2323/?cmd=resetWebview&password=YOUR_PASSWORD"
```

### Screenshots & Camera
```bash
# Get screenshot (returns PNG)
curl "http://192.168.1.100:2323/?cmd=getScreenshot&password=YOUR_PASSWORD" > screenshot.png

# Get camera shot (requires motion detection enabled)
curl "http://192.168.1.100:2323/?cmd=getCamshot&password=YOUR_PASSWORD" > camshot.jpg
```

## Settings Management

### Reading Settings
```bash
# List ALL settings (300+ keys)
curl "http://192.168.1.100:2323/?cmd=listSettings&type=json&password=YOUR_PASSWORD"
```

### Writing Settings
```bash
# Set string setting
curl "http://192.168.1.100:2323/?cmd=setStringSetting&key=startURL&value=http://homeassistant.local:8123&password=YOUR_PASSWORD"

# Set boolean setting
curl "http://192.168.1.100:2323/?cmd=setBooleanSetting&key=kioskMode&value=true&password=YOUR_PASSWORD"

# Import settings from JSON URL
curl "http://192.168.1.100:2323/?cmd=importSettingsFile&url=http://server/config.json&password=YOUR_PASSWORD"
```

### Common Setting Keys

**Display Settings:**
- `startURL` - Home page URL
- `screenBrightness` - Brightness (0-255)
- `screenOffTimer` - Minutes until screen off
- `screensaverTimer` - Minutes until screensaver
- `screenOrientation` - 0=auto, 1=portrait, 2=landscape, 3=reverse-landscape

**Kiosk Settings:**
- `kioskMode` - Enable kiosk mode (boolean)
- `kioskModePin` - PIN to exit kiosk
- `kioskExitGesture` - Exit gesture type
- `lockSafeMode` - Prevent safe mode boot

**Motion Detection:**
- `motionDetection` - Enable motion detection
- `motionSensitivity` - Sensitivity 0-100
- `screenOnOnMotion` - Turn screen on when motion detected
- `stopScreensaverOnMotion` - Stop screensaver on motion

**Remote Admin:**
- `remoteAdmin` - Enable remote admin
- `remoteAdminPassword` - Admin password
- `remoteAdminFromLocalNetwork` - Allow local network only

**Web Settings:**
- `enableZoom` - Allow pinch zoom
- `desktopMode` - Request desktop site
- `userAgent` - Custom user agent string

## Fleet Management

### Python Multi-Device Manager

Use the included `fully_manager.py` script for fleet operations:

```bash
# Screen on all devices
python fully_manager.py --action screen_on --all

# Set brightness on specific devices
python fully_manager.py --action set_brightness --value 150 --devices kitchen,bedroom

# Push URL to all devices
python fully_manager.py --action load_url --url "http://ha.local:8123/dashboard" --all

# Get fleet status
python fully_manager.py --action status --all --output json

# TTS announcement to all devices
python fully_manager.py --action tts --text "Dinner is ready" --all
```

### Device Inventory Configuration

Create `devices.yaml` for your fleet:

```yaml
# ~/.fully-kiosk/devices.yaml
devices:
  kitchen-tablet:
    host: 192.168.1.100
    password: "your_password"
    location: Kitchen
    type: fire-hd-10
    use_case: dashboard

  living-room-panel:
    host: 192.168.1.101
    password: "your_password"
    location: Living Room
    type: android-tablet
    use_case: dashboard

  garage-signage:
    host: 192.168.1.102
    password: "your_password"
    location: Garage
    type: fire-hd-8
    use_case: signage

  guest-kiosk:
    host: 192.168.1.103
    password: "your_password"
    location: Guest Room
    type: samsung-tab
    use_case: kiosk

groups:
  dashboards: [kitchen-tablet, living-room-panel]
  all-fire: [kitchen-tablet, garage-signage]
  public: [guest-kiosk, garage-signage]
```

## Fully Cloud Integration

### Setup
1. Create account at https://cloud.fully-kiosk.com
2. In device: Settings > Other Settings > Fully Cloud
3. Enable "Use Fully Cloud" and authenticate

### Cloud Features
- **Remote Admin**: Access any device from anywhere
- **Push Configuration**: Deploy settings to multiple devices
- **Device Groups**: Organize devices into manageable groups
- **Alerts**: Email/Pushbullet notifications for offline, low battery, unplugged
- **Scheduled Actions**: Time-based command execution
- **App Management**: Silent APK installation (with Enterprise enrollment)

### Export/Import Configuration

From Fully Cloud Remote Admin:
1. Open device's Remote Admin
2. Go to Export/Import menu
3. Export current settings as JSON
4. Import JSON to other devices or save as template

## Home Assistant Integration

### Native Integration Setup

1. **Enable Remote Admin** on device:
   - Settings > Remote Administration (PLUS)
   - Enable Remote Admin
   - Set password
   - Enable "Local Network Access"

2. **Add Integration in HA**:
   - Settings > Devices & Services > Add Integration
   - Search "Fully Kiosk Browser"
   - Enter device IP and password

### Available HA Entities

**Sensors:**
- `sensor.<device>_battery` - Battery level
- `sensor.<device>_storage` - Free storage
- `sensor.<device>_memory` - Free RAM
- `sensor.<device>_page` - Current URL

**Binary Sensors:**
- `binary_sensor.<device>_plugged_in` - Charging status
- `binary_sensor.<device>_kiosk_mode` - Kiosk enabled

**Switches:**
- `switch.<device>_screensaver` - Toggle screensaver
- `switch.<device>_maintenance_mode` - Maintenance mode
- `switch.<device>_kiosk_lock` - Lock/unlock kiosk
- `switch.<device>_motion_detection` - Motion detection

**Buttons:**
- `button.<device>_restart` - Restart app
- `button.<device>_reload` - Reload page
- `button.<device>_to_foreground` - Bring to front

**Numbers:**
- `number.<device>_brightness` - Screen brightness
- `number.<device>_volume` - Media volume

**Camera:**
- `camera.<device>_screenshot` - Live screenshot

### HA Services

```yaml
# Load URL
service: fully_kiosk.load_url
target:
  device_id: <device_id>
data:
  url: "http://homeassistant.local:8123/dashboard"

# Set configuration
service: fully_kiosk.set_config
target:
  device_id: <device_id>
data:
  key: "screenBrightness"
  value: "128"

# Start application
service: fully_kiosk.start_application
target:
  device_id: <device_id>
data:
  application: "com.spotify.music"
```

### HA Automation Examples

**Motion-Activated Screen:**
```yaml
automation:
  - alias: "Kitchen Tablet - Motion Screen On"
    trigger:
      - platform: state
        entity_id: binary_sensor.kitchen_motion
        to: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.kitchen_tablet_screensaver
      - service: light.turn_on
        target:
          entity_id: light.kitchen_tablet_screen
        data:
          brightness: 200

  - alias: "Kitchen Tablet - Screen Off After Idle"
    trigger:
      - platform: state
        entity_id: binary_sensor.kitchen_motion
        to: "off"
        for:
          minutes: 5
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.kitchen_tablet_screensaver
```

**Doorbell TTS Announcement:**
```yaml
automation:
  - alias: "Doorbell - Announce on All Tablets"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_doorbell
        to: "on"
    action:
      - service: rest_command.fully_tts
        data:
          text: "Someone is at the front door"
          device: kitchen_tablet
      - service: rest_command.fully_tts
        data:
          text: "Someone is at the front door"
          device: living_room_tablet
```

**REST Commands in HA:**
```yaml
# configuration.yaml
rest_command:
  fully_tts:
    url: "http://{{ device }}.local:2323/?cmd=textToSpeech&text={{ text | urlencode }}&password=YOUR_PASSWORD"
    method: GET

  fully_load_url:
    url: "http://{{ device }}.local:2323/?cmd=loadUrl&url={{ url | urlencode }}&password=YOUR_PASSWORD"
    method: GET

  fully_screen_on:
    url: "http://{{ device }}.local:2323/?cmd=screenOn&password=YOUR_PASSWORD"
    method: GET

  fully_screen_off:
    url: "http://{{ device }}.local:2323/?cmd=screenOff&password=YOUR_PASSWORD"
    method: GET

  fully_play_sound:
    url: "http://{{ device }}.local:2323/?cmd=playSound&url={{ sound_url | urlencode }}&password=YOUR_PASSWORD"
    method: GET
```

## MQTT Integration

### Enable MQTT in Fully Kiosk
Settings > Other Settings > MQTT Integration (experimental):
- **MQTT Broker URL**: `tcp://192.168.1.50:1883`
- **MQTT Broker Username/Password**: Your broker credentials
- **Device Info Topic**: `fully/kitchen-tablet/deviceInfo`
- **Event Topic**: `fully/kitchen-tablet/event`

### MQTT Topics Published

**Device Info (JSON):**
```
fully/<device>/deviceInfo
```
Contains: batteryLevel, isPlugged, screenOn, currentTabUrl, etc.

**Events:**
```
fully/<device>/event
```
Events: screenOn, screenOff, onMotion, pluggedIn, unplugged, etc.

### Home Assistant MQTT Sensors

```yaml
# configuration.yaml
mqtt:
  sensor:
    - name: "Kitchen Tablet Battery"
      state_topic: "fully/kitchen-tablet/deviceInfo"
      value_template: "{{ value_json.batteryLevel }}"
      unit_of_measurement: "%"
      device_class: battery

    - name: "Kitchen Tablet Screen"
      state_topic: "fully/kitchen-tablet/deviceInfo"
      value_template: "{{ value_json.screenOn }}"

  binary_sensor:
    - name: "Kitchen Tablet Plugged"
      state_topic: "fully/kitchen-tablet/deviceInfo"
      value_template: "{{ value_json.isPlugged }}"
      payload_on: "true"
      payload_off: "false"
      device_class: plug
```

## Configuration Templates

### Home Assistant Dashboard Preset
Optimized settings for wall-mounted HA dashboards:

```json
{
  "startURL": "http://homeassistant.local:8123",
  "kioskMode": true,
  "kioskModePin": "1234",
  "showNavigationBar": false,
  "showStatusBar": false,
  "enableFullscreen": true,
  "keepScreenOn": true,
  "screenBrightness": 150,
  "screensaverTimer": 5,
  "screensaverBrightness": 0,
  "motionDetection": true,
  "motionSensitivity": 80,
  "screenOnOnMotion": true,
  "stopScreensaverOnMotion": true,
  "remoteAdmin": true,
  "enablePullToRefresh": true,
  "autoplayVideos": true,
  "enableZoom": false,
  "clearCacheOnReload": true
}
```

### Digital Signage Preset
For information displays and signage:

```json
{
  "startURL": "http://signage-server/display",
  "kioskMode": true,
  "showNavigationBar": false,
  "showStatusBar": false,
  "enableFullscreen": true,
  "keepScreenOn": true,
  "screenBrightness": 200,
  "autoReloadOnIdle": true,
  "idleTimeout": 60,
  "errorReload": true,
  "enableZoom": false,
  "desktopMode": false,
  "screensaverTimer": 0,
  "motionDetection": false
}
```

### Locked Guest Kiosk Preset
Maximum lockdown for public/guest access:

```json
{
  "startURL": "http://guest-portal.local",
  "kioskMode": true,
  "kioskModePin": "5678",
  "kioskExitGesture": 4,
  "showNavigationBar": false,
  "showStatusBar": false,
  "lockStatusBar": true,
  "disableHomeButton": true,
  "disablePowerButton": true,
  "disableVolumeButtons": true,
  "disableNotifications": true,
  "enableScreenshots": false,
  "enableZoom": false,
  "blockOtherApps": true,
  "whitelistUrls": "guest-portal.local,cdn.example.com",
  "remoteAdmin": true,
  "remoteAdminFromLocalNetwork": true
}
```

## Troubleshooting

### Common Issues

**Cannot connect to device:**
1. Verify device IP: `ping <device-ip>`
2. Check Remote Admin enabled: Settings > Remote Administration
3. Verify port 2323 is accessible: `curl http://<ip>:2323`
4. Check password is correct

**Screen won't stay on:**
- Enable "Keep Screen On" in Device Management
- Check "Prevent Sleep While Plugged" setting
- Disable Android battery optimization for Fully Kiosk

**Motion detection not working:**
- Grant camera permission to Fully Kiosk
- Increase motion sensitivity (0-100)
- Check camera isn't blocked by other apps
- Verify "Screen On On Motion" is enabled

**Fire Tablet specific issues:**
- Remove Amazon launcher: Use ADB to disable
- Disable OTA updates: Block Amazon URLs in router
- Battery drain: Enable "Keep WiFi On During Sleep"

**MQTT not connecting:**
- Verify broker URL format: `tcp://host:port`
- Check broker allows anonymous or credentials are correct
- Enable experimental MQTT in Other Settings

### Device Reset

If device is unresponsive:
```bash
# Force restart app
curl "http://<ip>:2323/?cmd=killMyProcess&password=PASSWORD"

# Reboot device (requires root)
curl "http://<ip>:2323/?cmd=rebootDevice&password=PASSWORD"
```

### Log Access

```bash
# Get Fully Kiosk log
curl "http://<ip>:2323/?cmd=showLog&password=PASSWORD"

# Get Android logcat
curl "http://<ip>:2323/?cmd=logcat&password=PASSWORD"
```

## Best Practices

### Security
1. Use strong Remote Admin passwords
2. Enable "Local Network Only" for Remote Admin
3. Use HTTPS if exposing to internet (via reverse proxy)
4. Regularly rotate passwords across fleet
5. Enable Fully Cloud for secure remote access

### Performance
1. Clear cache periodically (weekly)
2. Use motion detection to reduce screen-on time
3. Set appropriate screensaver/screen-off timers
4. Disable unused features (camera if not using motion detection)

### Fleet Management
1. Use consistent naming convention (location-type format)
2. Create device groups for batch operations
3. Export/save configuration templates
4. Monitor battery health across fleet
5. Schedule maintenance windows for updates

### Home Assistant Integration
1. Use native integration for simple setups
2. Add REST commands for advanced operations
3. Consider MQTT for real-time status updates
4. Create input_booleans for dashboard states
5. Use scripts to coordinate multiple devices

## Included Scripts & Templates

This skill includes ready-to-use scripts and templates in the `scripts/` and `templates/` directories.

### Scripts

#### fully_manager.py - Fleet Management CLI
Primary tool for managing multiple Fully Kiosk devices from the command line.

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# List all devices
python scripts/fully_manager.py --devices templates/devices-example.yaml list

# Turn on all screens
python scripts/fully_manager.py --devices devices.yaml screen-on

# Set brightness on specific group
python scripts/fully_manager.py --devices devices.yaml --group kitchen brightness 180

# Send TTS announcement to all devices
python scripts/fully_manager.py --devices devices.yaml tts "Dinner is ready"

# Get device info as JSON
python scripts/fully_manager.py --devices devices.yaml info --json
```

#### fleet_status.py - Real-Time Fleet Monitor
Continuous monitoring dashboard with alerts and notifications.

```bash
# Basic monitoring (30 second refresh)
python scripts/fleet_status.py --devices devices.yaml

# Custom interval with logging
python scripts/fleet_status.py --devices devices.yaml --interval 60 --log fleet.log

# With Slack/Discord webhook alerts
python scripts/fleet_status.py --devices devices.yaml --webhook https://hooks.slack.com/...

# Single status check (no continuous monitoring)
python scripts/fleet_status.py --devices devices.yaml --once

# Configure alert thresholds
python scripts/fleet_status.py --devices devices.yaml --alert-battery 15 --alert-offline 10
```

Features:
- Rich terminal UI with live updates
- Battery, WiFi signal, memory monitoring
- Offline/online transition alerts
- Low battery warnings
- Webhook notifications (Slack, Discord, etc.)
- Log file output for historical tracking

#### fully_cloud.py - Fully Cloud API Manager
Manage devices through Fully Cloud centralized management.

```bash
# List all cloud-registered devices
python scripts/fully_cloud.py --token YOUR_API_TOKEN list

# Get device status
python scripts/fully_cloud.py --token YOUR_API_TOKEN status DEVICE_ID

# Send command to device
python scripts/fully_cloud.py --token YOUR_API_TOKEN command DEVICE_ID screenOn

# Send command with parameters
python scripts/fully_cloud.py --token YOUR_API_TOKEN command DEVICE_ID loadUrl \
  --params '{"url":"http://example.com"}'

# Sync settings from local file
python scripts/fully_cloud.py --token YOUR_API_TOKEN sync DEVICE_ID settings.json

# View device logs
python scripts/fully_cloud.py --token YOUR_API_TOKEN logs DEVICE_ID --limit 100

# List device groups
python scripts/fully_cloud.py --token YOUR_API_TOKEN groups
```

#### backup_restore.py - Configuration Backup & Restore
Export and restore device configurations for disaster recovery and fleet provisioning.

```bash
# Backup single device
python scripts/backup_restore.py --devices devices.yaml backup kitchen-tablet

# Backup all devices
python scripts/backup_restore.py --devices devices.yaml backup-all --output backups/

# Restore to a device
python scripts/backup_restore.py --devices devices.yaml restore kitchen-tablet backup.json

# Clone config from one device to another
python scripts/backup_restore.py --devices devices.yaml clone kitchen-tablet bedroom-tablet

# Compare two device configurations
python scripts/backup_restore.py --devices devices.yaml diff kitchen-tablet bedroom-tablet
```

### Templates

#### Configuration Templates
Pre-built JSON configurations in `templates/`:

| Template | Use Case |
|----------|----------|
| `config-ha-dashboard.json` | Home Assistant dashboard display |
| `config-digital-signage.json` | Unattended information displays |
| `config-locked-kiosk.json` | Maximum security guest/public kiosks |
| `config-fire-tablet.json` | Amazon Fire tablet optimizations |

#### ha-automations.yaml - Home Assistant Automation Package
Complete automation package with 12+ pre-built automations:

```yaml
# Installation:
# 1. Copy to /config/packages/fully_kiosk.yaml
# 2. Add to configuration.yaml:
#    homeassistant:
#      packages:
#        fully_kiosk: !include packages/fully_kiosk.yaml
# 3. Update entity IDs to match your devices
# 4. Restart Home Assistant
```

Included automations:
- Motion-based screen on/off
- Night mode with dimming schedule
- Doorbell camera display
- Weather alert TTS announcements
- Low battery notifications
- Presence-based dashboard switching
- Morning routine with gradual brightness
- Auto-restart on low memory
- Daily scheduled page reload

Included scripts:
- `fully_kiosk_all_screens_on` / `off`
- `fully_kiosk_reload_all`
- `fully_kiosk_announce` (multi-device TTS)
- `fully_kiosk_display_camera`

#### lovelace-cards.yaml - Dashboard Cards
Pre-built Lovelace cards for tablet status display. See `templates/lovelace-cards.yaml`.

#### devices-example.yaml - Fleet Configuration
Example device inventory file:

```yaml
devices:
  kitchen-tablet:
    ip: 192.168.1.100
    password: your_password
    groups: [kitchen, main-floor]

  bedroom-tablet:
    ip: 192.168.1.101
    password: your_password
    groups: [bedroom, upstairs]
```

## Related Skills

- **home-assistant**: HA configuration and automation
- **mqtt-iot**: MQTT broker setup and management
- **node-red-automation**: Visual automation flows
- **tailscale-vpn**: Secure remote access to devices

## Resources

- [Fully Kiosk Browser Official Site](https://www.fully-kiosk.com)
- [Fully Cloud EMM](https://cloud.fully-kiosk.com)
- [Home Assistant Integration Docs](https://www.home-assistant.io/integrations/fully_kiosk/)
- [Fully Kiosk REST API Reference](https://www.fully-kiosk.com/en/#rest)
