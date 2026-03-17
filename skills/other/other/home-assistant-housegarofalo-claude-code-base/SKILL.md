---
name: home-assistant
description: Ultimate Home Assistant skill - complete administration, wireless protocols (Zigbee/ZHA/Z2M, Z-Wave JS, Thread, Matter), ESPHome device building, advanced troubleshooting, performance optimization, security hardening, custom integration development, and professional dashboard design. Covers configuration, REST API, automation debugging, database optimization, SSL/TLS, Jinja2 templating, and HACS custom cards. Use for any HA task.
---

# Home Assistant Complete Management & Development

The ultimate comprehensive skill for Home Assistant covering:
- **Administration**: Configuration analysis, REST API, automation management, entity monitoring
- **Wireless Protocols**: Zigbee (ZHA + Zigbee2MQTT), Z-Wave JS, Thread, Matter
- **ESPHome**: Full device building with YAML, sensors, GPIO, I2C, SPI, custom components
- **Troubleshooting**: Log analysis, automation traces, debug logging, performance tuning
- **Database**: Recorder optimization, MariaDB/PostgreSQL, entity filtering, long-term statistics
- **Security**: SSL/TLS, authentication, IP banning, secrets management
- **Development**: Custom integrations, advanced Jinja2 templating, config flows
- **Dashboards**: HACS cards, themes, animations, responsive layouts, floor plans

## Session Configuration

**CRITICAL: Connection Setup**

When the user first requests a Home Assistant operation, collect the necessary connection details:

```
I need Home Assistant connection details. Please provide what applies:

**For Configuration File Access:**
1. **Config Path**: Local path OR SSH details to HA config directory
   - Local: /config, /homeassistant, or custom path
   - SSH: user@host:/path/to/config

**For REST API Access (optional but recommended):**
2. **HA URL**: (e.g., http://192.168.1.100:8123 or https://ha.example.com)
3. **Long-Lived Access Token**: (Create at Profile > Security > Long-Lived Access Tokens)

Example response:
- Config Path: /home/user/homeassistant
- HA URL: http://192.168.1.100:8123
- Token: eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp...
```

After receiving details:
- Store them in working memory for the session
- Use for ALL subsequent HA operations without re-prompting
- NEVER write tokens/credentials to files or logs

---

## Cross-Platform SSH Support

**CRITICAL: SSH authentication handling differs by platform.**

When accessing Home Assistant configuration via SSH, the method depends on your operating system.

### Authentication Priority

1. **SSH Keys (RECOMMENDED)** - Works on all platforms without additional tools
2. **REST API** - Works everywhere, preferred for most operations
3. **Python SSH Helper** - Works on all platforms with `paramiko` library
4. **sshpass** - Linux/macOS only (not available on Windows)

### Platform-Specific SSH Commands

**With SSH Keys (All Platforms):**
```bash
# Direct SSH command - keys are used automatically if configured
ssh -o StrictHostKeyChecking=accept-new user@<HA-HOST> "cat /config/configuration.yaml"
```

**With Password - Windows:**
```powershell
# Use Python helper (paramiko-based)
python scripts/ssh_helper.py --host <HA-HOST> --user homeassistant --password "<password>" --command "cat /config/configuration.yaml"

# Download config file
python scripts/ssh_helper.py --host <HA-HOST> --user homeassistant --password "<password>" --download /config/configuration.yaml --local-path ./configuration.yaml
```

**With Password - macOS/Linux:**
```bash
# Using sshpass (if installed)
sshpass -p '<password>' ssh -o StrictHostKeyChecking=accept-new user@<HA-HOST> "cat /config/configuration.yaml"

# Or use Python helper (cross-platform)
python3 scripts/ssh_helper.py --host <HA-HOST> --user homeassistant --password "<password>" --command "cat /config/configuration.yaml"
```

### Setting Up SSH Keys for Home Assistant

```bash
# Generate key if you don't have one
ssh-keygen -t ed25519 -C "ha-admin"

# For Home Assistant OS (via Terminal add-on or SSH add-on)
# Add your public key to the authorized_keys in the SSH add-on configuration
```

### SSH Access by Installation Type

| Installation | SSH Available | Username | Config Path |
|--------------|---------------|----------|-------------|
| Home Assistant OS | Via SSH Add-on | `root` | `/config/` |
| Home Assistant Container | Via Docker host | Host user | Mounted path |
| Home Assistant Core | Via host SSH | User running HA | `~/.homeassistant/` |

**Recommendation:** Use the REST API for most operations - it's cross-platform and doesn't require SSH setup.

---

## Quick Reference

### File Structure (Home Assistant OS)

```
/config/                          # Main configuration directory
├── configuration.yaml            # Primary configuration file
├── automations.yaml              # UI-created automations
├── scripts.yaml                  # UI-created scripts
├── scenes.yaml                   # UI-created scenes
├── secrets.yaml                  # Sensitive credentials (NEVER share)
├── known_devices.yaml            # Device tracker known devices
├── customize.yaml                # Entity customizations
├── home-assistant.log            # Current session log
├── home-assistant.log.1          # Previous session log
├── .storage/                     # Internal state storage (DO NOT EDIT)
│   ├── auth                      # Authentication data
│   ├── core.config_entries       # Integration configs
│   ├── core.entity_registry      # Entity registry
│   ├── core.device_registry      # Device registry
│   └── lovelace                  # Dashboard configs
├── custom_components/            # HACS and manual integrations
├── www/                          # Static web assets
├── blueprints/                   # Automation blueprints
│   ├── automation/
│   └── script/
├── packages/                     # Package configurations
└── tts/                          # Text-to-speech cache
```

### REST API Base

```
Base URL: http://<HA_HOST>:8123/api/
Auth Header: Authorization: Bearer <LONG_LIVED_TOKEN>
Content-Type: application/json
```

---

## Configuration Analysis

### Reading Configuration Files

```bash
# Read main configuration
cat /config/configuration.yaml

# Check for syntax errors (via API)
curl -X POST "http://HA_HOST:8123/api/config/core/check_config" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json"

# List all YAML files
find /config -name "*.yaml" -type f

# Search for specific configuration
grep -r "sensor:" /config/*.yaml
grep -r "automation:" /config/*.yaml
```

### Configuration Best Practices Check

When analyzing configuration, look for:

1. **Secrets Usage**: Ensure sensitive data uses `!secret` references
2. **Split Configuration**: Large configs should use `!include` directives
3. **Deprecated Syntax**: Check for legacy platform syntax vs modern format
4. **Proper Indentation**: YAML requires consistent spacing (2 spaces recommended)
5. **Entity Naming**: Consistent, descriptive entity_id patterns
6. **Automation Organization**: Group related automations logically

### Modern vs Legacy Configuration

**Modern Format (Preferred):**
```yaml
template:
  - sensor:
      - name: "My Sensor"
        state: "{{ states('sensor.source') }}"
```

**Legacy Format (Deprecated):**
```yaml
sensor:
  - platform: template
    sensors:
      my_sensor:
        value_template: "{{ states('sensor.source') }}"
```

---

## REST API Reference

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | API status check |
| GET | `/api/config` | Current configuration |
| GET | `/api/states` | All entity states |
| GET | `/api/states/<entity_id>` | Specific entity state |
| POST | `/api/states/<entity_id>` | Set entity state |
| GET | `/api/services` | Available services by domain |
| POST | `/api/services/<domain>/<service>` | Call a service |
| GET | `/api/events` | Event types and listeners |
| POST | `/api/events/<event_type>` | Fire an event |
| GET | `/api/history/period/<timestamp>` | Historical states |
| GET | `/api/logbook/<timestamp>` | Logbook entries |
| GET | `/api/error_log` | Error log (plain text) |
| POST | `/api/template` | Render a template |
| POST | `/api/config/core/check_config` | Validate configuration |
| GET | `/api/components` | Loaded components |
| GET | `/api/calendars` | Calendar entities |

### Common API Operations

**Get All Entity States:**
```bash
curl -s "http://HA_HOST:8123/api/states" \
  -H "Authorization: Bearer TOKEN" | jq '.'
```

**Get Specific Entity:**
```bash
curl -s "http://HA_HOST:8123/api/states/light.living_room" \
  -H "Authorization: Bearer TOKEN" | jq '.'
```

**Call a Service (Turn On Light):**
```bash
curl -X POST "http://HA_HOST:8123/api/services/light/turn_on" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness": 255}'
```

**Call a Service (Run Script):**
```bash
curl -X POST "http://HA_HOST:8123/api/services/script/turn_on" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "script.my_script"}'
```

**Trigger Automation:**
```bash
curl -X POST "http://HA_HOST:8123/api/services/automation/trigger" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.my_automation"}'
```

**Render Template:**
```bash
curl -X POST "http://HA_HOST:8123/api/template" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states(\"sensor.temperature\") }}"}'
```

**Check Configuration:**
```bash
curl -X POST "http://HA_HOST:8123/api/config/core/check_config" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json"
```

**Get History:**
```bash
curl -s "http://HA_HOST:8123/api/history/period/2024-01-01T00:00:00?filter_entity_id=sensor.temperature&end_time=2024-01-02T00:00:00" \
  -H "Authorization: Bearer TOKEN" | jq '.'
```

---

## Automation Management

### Automation YAML Structure

```yaml
automation:
  - id: 'unique_automation_id'
    alias: "Descriptive Automation Name"
    description: "What this automation does"
    mode: single  # single, restart, queued, parallel

    trigger:
      - platform: state
        entity_id: binary_sensor.motion
        to: 'on'
      - platform: time
        at: '07:00:00'
      - platform: sun
        event: sunset
        offset: '-00:30:00'

    condition:
      - condition: state
        entity_id: input_boolean.automation_enabled
        state: 'on'
      - condition: time
        after: '06:00:00'
        before: '23:00:00'

    action:
      - service: light.turn_on
        target:
          entity_id: light.living_room
        data:
          brightness_pct: 100
      - delay:
          seconds: 5
      - service: notify.mobile_app
        data:
          message: "Motion detected!"
```

### Common Trigger Platforms

| Platform | Use Case | Example |
|----------|----------|---------|
| `state` | Entity state changes | `to: 'on'`, `from: 'off'` |
| `numeric_state` | Numeric thresholds | `above: 25`, `below: 10` |
| `time` | Specific time | `at: '07:00:00'` |
| `time_pattern` | Recurring pattern | `minutes: '/5'` (every 5 min) |
| `sun` | Sunrise/sunset | `event: sunset`, `offset: '-00:30:00'` |
| `zone` | Location zones | `entity_id: person.john`, `zone: zone.home`, `event: enter` |
| `device` | Device triggers | Device-specific events |
| `webhook` | External webhooks | `webhook_id: 'my_webhook'` |
| `event` | HA events | `event_type: 'my_event'` |
| `mqtt` | MQTT messages | `topic: 'home/sensor'` |
| `template` | Template evaluation | `value_template: "{{ condition }}"` |

### Automation Debugging

**Via API - Get automation trace:**
```bash
curl -s "http://HA_HOST:8123/api/states/automation.my_automation" \
  -H "Authorization: Bearer TOKEN" | jq '.attributes'
```

**Enable debug logging:**
```yaml
# In configuration.yaml
logger:
  default: info
  logs:
    homeassistant.components.automation: debug
```

**Automation Trace (UI):**
- Navigate to Settings > Automations & Scenes
- Click the automation > Click "Traces" (top right)
- View step-by-step execution history

---

## Entity Management

### Entity Domains

| Domain | Description | Example |
|--------|-------------|---------|
| `light` | Lighting control | `light.living_room` |
| `switch` | On/off switches | `switch.garage_door` |
| `sensor` | Sensor readings | `sensor.temperature` |
| `binary_sensor` | Boolean sensors | `binary_sensor.motion` |
| `climate` | HVAC/thermostats | `climate.nest` |
| `cover` | Blinds/doors/gates | `cover.garage` |
| `fan` | Fan control | `fan.bedroom` |
| `media_player` | Media devices | `media_player.tv` |
| `camera` | Camera feeds | `camera.front_door` |
| `person` | Person tracking | `person.john` |
| `device_tracker` | Device location | `device_tracker.phone` |
| `input_boolean` | Virtual toggles | `input_boolean.guest_mode` |
| `input_number` | Virtual numbers | `input_number.brightness` |
| `input_select` | Dropdown options | `input_select.mode` |
| `input_text` | Text inputs | `input_text.message` |
| `input_datetime` | Date/time inputs | `input_datetime.alarm` |
| `group` | Entity groups | `group.all_lights` |
| `scene` | Preset states | `scene.movie_time` |
| `script` | Executable scripts | `script.morning_routine` |
| `automation` | Automations | `automation.sunrise_lights` |

### Template Sensors

```yaml
template:
  - sensor:
      - name: "Average Temperature"
        unit_of_measurement: "°F"
        state: >
          {{ ((states('sensor.living_room_temp') | float) +
              (states('sensor.bedroom_temp') | float)) / 2 | round(1) }}
        availability: >
          {{ states('sensor.living_room_temp') not in ['unknown', 'unavailable'] and
             states('sensor.bedroom_temp') not in ['unknown', 'unavailable'] }}

  - binary_sensor:
      - name: "Anyone Home"
        state: >
          {{ is_state('person.john', 'home') or
             is_state('person.jane', 'home') }}
        device_class: presence
```

### Helper Entities (Input Helpers)

```yaml
# input_boolean for manual toggles
input_boolean:
  vacation_mode:
    name: Vacation Mode
    icon: mdi:airplane

# input_number for adjustable values
input_number:
  notification_volume:
    name: Notification Volume
    min: 0
    max: 100
    step: 5
    unit_of_measurement: "%"

# input_select for mode selection
input_select:
  home_mode:
    name: Home Mode
    options:
      - Home
      - Away
      - Night
      - Guest
```

---

## Security Auditing

### Security Checklist

Run these checks when auditing a Home Assistant installation:

1. **Secrets File Usage:**
```bash
# Find hardcoded credentials (should use !secret)
grep -rE "(password|api_key|token|secret):" /config/*.yaml | grep -v "!secret"
```

2. **secrets.yaml Protection:**
```bash
# Verify secrets.yaml exists and has restricted permissions
ls -la /config/secrets.yaml
# Should be: -rw------- (600) or -rw-r----- (640)
```

3. **Exposed Ports:**
```bash
# Check what ports HA is listening on
netstat -tulpn | grep -E "(8123|8124)"
```

4. **Authentication Review:**
```bash
# Check auth configuration
grep -A 10 "homeassistant:" /config/configuration.yaml
# Look for: auth_providers, trusted_networks, ip_ban_enabled
```

5. **Add-on Security:**
```yaml
# Review add-on configurations for:
# - Unnecessary privileged access
# - Exposed ports
# - Disabled SSL
```

### Security Best Practices

```yaml
# configuration.yaml security settings
homeassistant:
  auth_providers:
    - type: homeassistant
  # Uncomment for trusted networks (use carefully)
  # auth_providers:
  #   - type: trusted_networks
  #     trusted_networks:
  #       - 192.168.1.0/24

http:
  # Enable SSL (recommended)
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem

  # IP banning for failed logins
  ip_ban_enabled: true
  login_attempts_threshold: 5

  # Restrict to local only (if not using remote access)
  # server_host: 127.0.0.1

# Enable recorder purging to manage database size
recorder:
  purge_keep_days: 10
  commit_interval: 1
```

### secrets.yaml Structure

```yaml
# secrets.yaml - NEVER commit this file to git
# Add to .gitignore: secrets.yaml

# API Keys
openweathermap_api_key: "your-api-key-here"
google_api_key: "your-google-key"

# Passwords
mqtt_password: "secure-password"
influxdb_password: "another-password"

# Tokens
telegram_bot_token: "bot123456:ABC-DEF..."
pushover_api_token: "your-token"

# URLs with credentials
database_url: "mysql://user:pass@localhost/hass"

# GPS coordinates (privacy)
home_latitude: 40.7128
home_longitude: -74.0060
```

---

## Troubleshooting

### Log Analysis

**View Current Logs:**
```bash
# Via filesystem
tail -f /config/home-assistant.log

# Via API
curl -s "http://HA_HOST:8123/api/error_log" \
  -H "Authorization: Bearer TOKEN"
```

**Enable Debug Logging:**
```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    homeassistant.core: debug
    homeassistant.components.automation: debug
    homeassistant.components.script: debug
    custom_components.my_integration: debug
```

**Filter Logs for Specific Component:**
```bash
grep "homeassistant.components.sensor" /config/home-assistant.log
```

### Common Issues & Solutions

| Issue | Diagnostic | Solution |
|-------|-----------|----------|
| Entity unavailable | Check integration status | Restart integration, check device connectivity |
| Automation not triggering | Check automation trace | Verify trigger conditions, check if enabled |
| YAML syntax error | Run config check | Fix indentation, quote strings properly |
| Integration not loading | Check logs for errors | Verify credentials, check network |
| Database errors | Check disk space | Purge old data, increase disk |
| Slow dashboard | Check entity count | Reduce entities per view, optimize templates |
| Service call fails | Check service parameters | Use Developer Tools > Services to test |

### Configuration Validation

```bash
# Check configuration via CLI (HA OS)
ha core check

# Check configuration via API
curl -X POST "http://HA_HOST:8123/api/config/core/check_config" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json"

# Response on success:
# {"result": "valid", "errors": null}

# Response on error:
# {"result": "invalid", "errors": "Error details..."}
```

### Developer Tools

Access via HA UI: Developer Tools section

| Tool | Purpose |
|------|---------|
| States | View/modify entity states |
| Services | Test service calls |
| Template | Test Jinja2 templates |
| Events | Fire/listen to events |
| Statistics | View long-term statistics |
| Actions | Test action sequences |

---

## Zigbee Integration (ZHA & Zigbee2MQTT)

### Coordinator Hardware Selection

| Coordinator | Chip | Protocol | Recommendation |
|-------------|------|----------|----------------|
| Home Assistant Connect ZBT-2 | EFR32MG21 | EZSP | **Best** - Native HA support |
| Home Assistant Yellow | EFR32MG21 | EZSP | **Excellent** - Built-in |
| SONOFF ZBDongle-E | EFR32MG21 | EZSP | **Great** - Affordable |
| SONOFF ZBDongle-P | CC2652P | Z-Stack | **Great** - Popular |
| SMLIGHT SLZB-07 | EFR32MG21 | EZSP | **Great** - Ethernet option |
| ConBee III | deCONZ | deCONZ | Good - Requires deCONZ |
| CC2531 | CC2531 | Z-Stack | **Not recommended** - Legacy |

**USB Placement Critical:**
- Use USB 2.0 ports only (USB 3.x causes RF interference)
- Use USB extension cable (1-2m) to distance from computer
- Keep away from WiFi routers, power supplies, SSDs

### ZHA (Zigbee Home Automation) Setup

**Initial Configuration:**
1. Settings > Devices & Services > Add Integration > ZHA
2. Select serial port (use `/dev/serial/by-id/` path for stability)
3. Allow network formation (creates PAN ID, channel)

**YAML Configuration Options:**
```yaml
# configuration.yaml
zha:
  zigpy_config:
    network:
      channel: 15  # Default, don't change unless necessary
      channels: [15, 20, 25]  # Scan channels
    ota:
      otau_directory: /config/zigpy_ota
      ikea_provider: true
      ledvance_provider: true
      inovelli_provider: true
  device_config:
    # Override device type if misdetected
    "aa:bb:cc:dd:ee:ff:00:11-1":
      type: "switch"
  custom_quirks_path: /config/custom_zha_quirks/
```

**Device Pairing:**
```bash
# Via UI: Settings > Devices & Services > ZHA > Add Device
# Put device in pairing mode (usually hold button 5-10 sec)

# Via service call (API):
curl -X POST "http://HA_HOST:8123/api/services/zha/permit" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"duration": 60}'
```

**Network Visualization:**
- Settings > Devices & Services > ZHA > Configure > Visualization
- Shows coordinator, routers, and end devices
- Color coding: Green (good), Yellow (weak), Red (poor)

**ZHA Toolkit (Advanced Operations):**
```yaml
# Install via HACS: zha-toolkit
# Available services:
service: zha_toolkit.execute
data:
  command: scan_device
  ieee: "aa:bb:cc:dd:ee:ff:00:11"

# Bind devices directly (bypasses HA for faster response)
service: zha_toolkit.bind_ieee
data:
  source_ieee: "aa:bb:cc:dd:ee:ff:00:11"
  target_ieee: "11:22:33:44:55:66:77:88"
  cluster: 6  # On/Off cluster
```

### Zigbee2MQTT Setup

**Prerequisites:**
- MQTT broker (Mosquitto addon)
- Zigbee coordinator

**Installation:**
1. Settings > Add-ons > Add-on Store
2. Add repository: `https://github.com/zigbee2mqtt/hassio-zigbee2mqtt`
3. Install Zigbee2MQTT addon
4. Configure serial port and MQTT

**Configuration (addon config):**
```yaml
serial:
  port: /dev/serial/by-id/usb-Silicon_Labs_...
  adapter: ezsp  # or zstack for CC2652
mqtt:
  server: mqtt://core-mosquitto:1883
  user: mqtt_user
  password: mqtt_pass
homeassistant: true
permit_join: false
frontend:
  port: 8080
advanced:
  channel: 15
  network_key: GENERATE
  pan_id: GENERATE
  log_level: info
  last_seen: ISO_8601
```

**Device Pairing in Z2M:**
1. Open Zigbee2MQTT dashboard (sidebar)
2. Click "Permit Join (All)" or specific device
3. Put device in pairing mode
4. Device appears automatically

**Z2M vs ZHA Comparison:**

| Feature | ZHA | Zigbee2MQTT |
|---------|-----|-------------|
| Setup | Easier (built-in) | More steps |
| Device Support | Good | Excellent (more quirks) |
| Configuration | Limited YAML | Full YAML control |
| Frontend | Basic | Rich dashboard |
| MQTT Required | No | Yes |
| Updates | With HA | Independent |

### Zigbee Network Optimization

**Best Practices:**
1. **Router Devices**: Add mains-powered devices first (they extend mesh)
2. **Channel Selection**: Stay on channel 15 (default), avoid WiFi overlap
3. **Coordinator Placement**: Central location, elevated
4. **Max Direct Children**: ~32 per coordinator, but hundreds via routers

**Interference Mitigation:**
```yaml
# Check WiFi channel overlap
# Zigbee 11 = WiFi 1
# Zigbee 15 = WiFi 1-6 (some overlap)
# Zigbee 20 = WiFi 6-8
# Zigbee 25 = WiFi 11-13
# Zigbee 26 = WiFi 12-14
```

**OTA Firmware Updates:**
```yaml
# ZHA OTA - automatic for supported devices
# Wake battery devices to receive updates
# IKEA, Inovelli, Ledvance supported

# Check update status in device info
# Updates take ~10 minutes per device
```

### Zigbee Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Device won't pair | Too far from coordinator | Pair near coordinator, move after |
| Device drops offline | Weak signal/no router nearby | Add router device in between |
| Commands delayed | Network congestion | Add more routers, check interference |
| NCP failed state | Serial communication lost | Check USB connection, restart addon |
| Entity unavailable | Device interview incomplete | Remove and re-pair device |

**Debug Logging:**
```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    homeassistant.components.zha: debug
    zigpy: debug
    bellows: debug
    zhaquirks: debug
```

---

## Z-Wave Integration (Z-Wave JS)

### Z-Wave Controller Hardware

| Controller | Chip | Generation | Notes |
|------------|------|------------|-------|
| Zooz ZST39 | 800LR | Gen 8 | **Best** - Long Range support |
| Aeotec Z-Stick 7 | 700 | Gen 7 | Excellent |
| Zooz ZST10 | 700 | Gen 7 | Great value |
| HUSBZB-1 | 500 | Gen 5 | Combined Zigbee (legacy) |

**USB Placement:**
- Same as Zigbee: USB 2.0, extension cable, away from interference

### Z-Wave JS Setup

**Installation:**
1. Settings > Add-ons > Z-Wave JS (official addon)
2. Configure serial port
3. Start addon
4. Settings > Devices & Services > Add Integration > Z-Wave

**Security Keys (Auto-generated):**
```yaml
# Keys stored in addon configuration
# S0 Legacy - older secure devices (locks, garage doors)
# S2 Unauthenticated - devices that don't verify user
# S2 Authenticated - devices requiring PIN entry
# S2 Access Control - door locks, secure access

# View keys: Settings > Add-ons > Z-Wave JS > Configuration
```

**Device Inclusion:**
```bash
# SmartStart (Preferred for S2 devices):
# 1. Scan QR code from device
# 2. Device auto-joins when powered

# Classic Inclusion:
# 1. Settings > Devices & Services > Z-Wave > Add Device
# 2. Put device in inclusion mode
# 3. Enter PIN if prompted (for S2)

# Exclusion (remove from old network):
# 1. Click "Remove Device" in Z-Wave panel
# 2. Put device in exclusion mode
```

### Z-Wave JS UI (Advanced)

**Install Z-Wave JS UI addon for:**
- Full network visualization
- Device parameter configuration
- Firmware updates
- Advanced diagnostics

**Configuration:**
```yaml
# Z-Wave JS UI addon config
serial:
  port: /dev/serial/by-id/usb-...
network_key: # Auto-generated or from old network
s0_legacy: # S0 key
s2_unauthenticated: # S2 key
s2_authenticated: # S2 key
s2_access_control: # S2 key
```

### Z-Wave Network Management

**Network Healing:**
```bash
# Rebuild routes after moving devices
# Settings > Devices & Services > Z-Wave > Heal Network

# Or via service:
curl -X POST "http://HA_HOST:8123/api/services/zwave_js/heal_network" \
  -H "Authorization: Bearer TOKEN"
```

**Device Interview:**
```yaml
# Re-interview device to refresh capabilities
service: zwave_js.refresh_value
data:
  entity_id: switch.device_name

# Or refresh entire device
service: zwave_js.refresh_node_info
data:
  device_id: device_id_here
```

### Z-Wave Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Device shows "Dead" | Communication lost | Check range, heal network |
| No entities | Interview incomplete | Wait or re-interview |
| S2 pairing fails | Wrong PIN | Check device documentation |
| Intermittent control | Weak mesh | Add more nodes, heal network |
| USB not detected | Driver issue | Check system logs, try USB 2.0 hub |

**Debug Logging:**
```yaml
logger:
  logs:
    homeassistant.components.zwave_js: debug
    zwave_js_server: debug
```

---

## Thread & Matter Integration

### Thread Network Setup

**Thread Border Router Options:**
1. **Home Assistant Yellow** - Built-in Thread radio
2. **Home Assistant Connect ZBT-1/ZBT-2** - USB Thread adapter
3. **Apple HomePod Mini** - Apple ecosystem
4. **Google Nest Hub (2nd gen)** - Google ecosystem

**OpenThread Border Router Addon:**
```yaml
# Install addon: OpenThread Border Router
# Configure for Thread radio

# Settings > Devices & Services > Thread
# View network credentials, preferred network
```

**Thread Credential Sharing:**
```bash
# Share HA Thread network to phone:
# Settings > Devices & Services > Thread > Configure
# "Send credentials to phone"

# Import existing Thread network:
# Use Companion App > Settings > Troubleshooting
# "Sync Thread credentials"
```

### Matter Integration

**Prerequisites:**
- Home Assistant 2023.1+
- Matter Server addon (auto-installed with integration)
- Companion App (for commissioning)
- Thread border router (for Thread devices)

**Setup:**
1. Settings > Devices & Services > Add Integration > Matter
2. Matter Server addon starts automatically

**Device Commissioning:**
```bash
# iOS:
# 1. HA App > Settings > Devices & Services
# 2. Add Matter device > "No, it's new"
# 3. Scan QR code or enter setup code

# Android:
# 1. Same steps as iOS
# 2. May need to add device to Google Developer Console for test devices

# Commissioning can take several minutes
```

**Multi-Admin (Multi-Fabric):**
```yaml
# Matter devices support up to 5 controllers
# Share from Apple Home or Google Home to HA:
# 1. In Apple/Google app, get sharing QR code
# 2. In HA, add Matter device using that code
# No factory reset needed!
```

**Matter Device Types Supported:**
- Lights (on/off, dimming, color)
- Switches and plugs
- Sensors (temperature, humidity, motion, contact)
- Locks
- Thermostats
- Window coverings
- Bridges (Philips Hue, etc.)

### Thread/Matter Troubleshooting

| Issue | Solution |
|-------|----------|
| "Matter is unavailable" | Wait 24h for Google Play Services update, update Companion App |
| Commissioning fails | Ensure phone on same WiFi network as HA |
| Thread device won't join | Verify border router active and nearby |
| Device shows offline | Check Thread network in Thread integration |
| Can't share to phone | Sync Thread credentials via Companion App |

**Debug Logging:**
```yaml
logger:
  logs:
    homeassistant.components.matter: debug
    homeassistant.components.thread: debug
    matter_server: debug
```

---

## ESPHome Device Builder

### ESPHome Fundamentals

**Installation:**
1. Settings > Add-ons > ESPHome (official addon)
2. Open ESPHome dashboard from sidebar

**Supported Hardware:**
- ESP8266 (NodeMCU, Wemos D1, Sonoff)
- ESP32 (DevKit, WROOM, various modules)
- ESP32-S2, ESP32-S3, ESP32-C3
- RP2040 (Raspberry Pi Pico W)

### YAML Configuration Structure

**Basic Device Template:**
```yaml
esphome:
  name: living-room-sensor
  friendly_name: Living Room Sensor

esp32:
  board: esp32dev
  framework:
    type: arduino  # or esp-idf

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Fallback hotspot
  ap:
    ssid: "Sensor Fallback"
    password: "fallback123"

captive_portal:

# Enable logging
logger:
  level: DEBUG

# Enable Home Assistant API
api:
  encryption:
    key: !secret api_encryption_key

ota:
  - platform: esphome
    password: !secret ota_password

# Optional web server
web_server:
  port: 80
```

### Common Sensor Configurations

**DHT Temperature/Humidity:**
```yaml
sensor:
  - platform: dht
    pin: GPIO4
    model: DHT22  # or DHT11, AM2302
    temperature:
      name: "Temperature"
      filters:
        - offset: -2.0  # Calibration offset
    humidity:
      name: "Humidity"
    update_interval: 60s
```

**BME280 (I2C Temperature/Humidity/Pressure):**
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true

sensor:
  - platform: bme280_i2c
    address: 0x76  # or 0x77
    temperature:
      name: "Temperature"
      oversampling: 16x
    humidity:
      name: "Humidity"
    pressure:
      name: "Pressure"
    update_interval: 60s
```

**PIR Motion Sensor:**
```yaml
binary_sensor:
  - platform: gpio
    pin: GPIO14
    name: "Motion"
    device_class: motion
    filters:
      - delayed_off: 30s  # Stay on for 30s after motion stops
```

**Door/Window Contact:**
```yaml
binary_sensor:
  - platform: gpio
    pin:
      number: GPIO5
      mode:
        input: true
        pullup: true
      inverted: true
    name: "Door"
    device_class: door
```

**Analog Sensor (Moisture/Light):**
```yaml
sensor:
  - platform: adc
    pin: GPIO34
    name: "Soil Moisture"
    update_interval: 60s
    unit_of_measurement: "%"
    filters:
      - calibrate_linear:
          - 3.3 -> 0.0   # Dry
          - 1.5 -> 100.0 # Wet
    attenuation: 11db
```

**Ultrasonic Distance:**
```yaml
sensor:
  - platform: ultrasonic
    trigger_pin: GPIO12
    echo_pin: GPIO14
    name: "Tank Level"
    update_interval: 60s
    filters:
      - lambda: return (1.0 - x) * 100;  # Convert to percentage
    unit_of_measurement: "%"
```

### Output Configurations

**GPIO Switch (Relay):**
```yaml
switch:
  - platform: gpio
    pin: GPIO5
    name: "Relay"
    id: relay1
    restore_mode: RESTORE_DEFAULT_OFF
```

**PWM LED/Dimmer:**
```yaml
output:
  - platform: ledc
    pin: GPIO16
    id: pwm_output
    frequency: 1000Hz

light:
  - platform: monochromatic
    name: "LED"
    output: pwm_output
    gamma_correct: 2.8
```

**RGB LED Strip (Addressable):**
```yaml
light:
  - platform: neopixelbus
    type: GRB
    variant: WS2812
    pin: GPIO5
    num_leds: 60
    name: "LED Strip"
    effects:
      - random:
      - rainbow:
      - color_wipe:
      - scan:
```

**Servo Motor:**
```yaml
servo:
  - id: my_servo
    output: pwm_servo

output:
  - platform: ledc
    id: pwm_servo
    pin: GPIO18
    frequency: 50Hz

# Control via number component
number:
  - platform: template
    name: "Servo Position"
    min_value: -100
    max_value: 100
    step: 1
    set_action:
      - servo.write:
          id: my_servo
          level: !lambda 'return x / 100.0;'
```

### Communication Protocols

**I2C Bus:**
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true
  id: bus_a
  frequency: 400kHz
```

**SPI Bus:**
```yaml
spi:
  clk_pin: GPIO18
  mosi_pin: GPIO23
  miso_pin: GPIO19
```

**UART (Serial):**
```yaml
uart:
  tx_pin: GPIO1
  rx_pin: GPIO3
  baud_rate: 9600
  id: uart_bus
```

**Dallas 1-Wire (DS18B20):**
```yaml
dallas:
  - pin: GPIO4

sensor:
  - platform: dallas
    address: 0x1234567890ABCDEF
    name: "Temperature"
    resolution: 12
```

### Advanced ESPHome Features

**Lambda Expressions:**
```yaml
sensor:
  - platform: template
    name: "Calculated Value"
    lambda: |-
      float temp = id(temperature_sensor).state;
      float hum = id(humidity_sensor).state;
      // Calculate heat index
      return temp + (0.5 * (temp + 61.0 + ((temp-68.0)*1.2) + (hum*0.094)));
    update_interval: 60s
    unit_of_measurement: "°F"
```

**Automation (On-Device):**
```yaml
binary_sensor:
  - platform: gpio
    pin: GPIO14
    name: "Motion"
    on_press:
      - light.turn_on:
          id: led_light
          brightness: 100%
      - delay: 5min
      - light.turn_off: led_light
```

**Time-Based Actions:**
```yaml
time:
  - platform: homeassistant
    id: ha_time
    on_time:
      - seconds: 0
        minutes: 0
        hours: 7
        then:
          - switch.turn_on: morning_light
```

**Substitutions (Variables):**
```yaml
substitutions:
  device_name: living-room
  friendly_name: "Living Room"
  update_interval: 60s

esphome:
  name: ${device_name}
  friendly_name: ${friendly_name}

sensor:
  - platform: dht
    update_interval: ${update_interval}
```

**Packages (Reusable Configs):**
```yaml
# common.yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
  encryption:
    key: !secret api_key

# device.yaml
packages:
  common: !include common.yaml

esphome:
  name: my-device
```

### ESPHome Flashing & Updates

**Initial Flash (USB):**
1. Connect device via USB
2. In ESPHome dashboard, click "Install"
3. Select "Plug into this computer"
4. Choose serial port

**OTA Updates (Wireless):**
```yaml
ota:
  - platform: esphome
    password: "secure_ota_password"
    safe_mode: true

# Updates happen automatically when config changes
# Or manually: Install > Wirelessly
```

**Secrets Management:**
```yaml
# secrets.yaml (in ESPHome config directory)
wifi_ssid: "MyNetwork"
wifi_password: "MyPassword"
api_encryption_key: "base64_encoded_32_byte_key"
ota_password: "ota_secure_pass"

# Usage in device config
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
```

### ESPHome Troubleshooting

| Issue | Solution |
|-------|----------|
| Won't connect to WiFi | Check credentials, signal strength, 2.4GHz only |
| API connection fails | Check encryption key, firewall |
| Sensor reads incorrectly | Add calibration filters |
| Device reboots randomly | Check power supply (3.3V devices need stable power) |
| OTA update fails | Ensure enough flash space, try safe mode |
| Compile error | Check YAML syntax, pin conflicts |

**Debug Output:**
```yaml
logger:
  level: DEBUG  # VERBOSE for even more
  logs:
    sensor: DEBUG
    wifi: INFO
    api: DEBUG
```

---

## Advanced Troubleshooting

### Log Analysis Deep Dive

**Log Locations:**
```bash
# Home Assistant OS
/config/home-assistant.log      # Current log
/config/home-assistant.log.1    # Previous log

# Docker
docker logs homeassistant

# Core (venv)
~/.homeassistant/home-assistant.log
```

**Log Levels:**
```yaml
# configuration.yaml
logger:
  default: warning  # critical, fatal, error, warning, info, debug
  logs:
    # Per-component logging
    homeassistant.core: warning
    homeassistant.components.automation: debug
    homeassistant.components.script: debug
    homeassistant.components.zha: info
    homeassistant.components.zwave_js: info

    # Third-party libraries
    zigpy: debug
    zwave_js_server: debug
    aiohttp: warning

    # Custom components
    custom_components.my_integration: debug
```

**Real-time Log Monitoring:**
```bash
# Via API
curl -s "http://HA_HOST:8123/api/error_log" \
  -H "Authorization: Bearer TOKEN"

# Via SSH (HA OS)
tail -f /config/home-assistant.log | grep -i error

# Via Docker
docker logs -f homeassistant 2>&1 | grep -i error
```

**Log Filtering Patterns:**
```bash
# Find all errors
grep -i "error\|exception\|traceback" home-assistant.log

# Find specific integration issues
grep "homeassistant.components.zha" home-assistant.log

# Find startup issues
grep -A 5 "Setup of" home-assistant.log | grep -i "fail\|error"

# Find automation execution
grep "automation" home-assistant.log | grep -i "triggered\|executed"
```

### Automation Debugging

**Automation Traces:**
1. Settings > Automations & Scenes
2. Click automation > Three-dot menu > Traces
3. View step-by-step execution path
4. Check variable values at each step

**Increase Trace Storage:**
```yaml
# In automation definition
automation:
  - id: my_automation
    alias: "My Automation"
    trace:
      stored_traces: 25  # Default is 5
```

**Template Testing:**
```bash
# Developer Tools > Template
# Test Jinja2 expressions before using in automations

# Example test:
{{ states('sensor.temperature') | float > 75 }}
{{ trigger.to_state.state }}  # Only works in automation context
```

**Manual Automation Trigger:**
```bash
# Via API (with conditions)
curl -X POST "http://HA_HOST:8123/api/services/automation/trigger" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.my_auto", "skip_condition": false}'

# Via API (skip conditions)
curl -X POST "http://HA_HOST:8123/api/services/automation/trigger" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.my_auto", "skip_condition": true}'
```

**Common Automation Issues:**

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Never triggers | Check trigger conditions in trace | Verify entity_id, states match |
| Triggers too often | Review trigger type | Add conditions or throttle |
| Actions don't execute | Check condition block in trace | Fix condition logic |
| Template error | Test in Developer Tools | Fix Jinja2 syntax |
| Wrong entity controlled | entity_id mismatch | Check entity registry |
| Variables not available | Scope issue | Use trigger variables correctly |

### Performance Diagnostics

**System Metrics:**
```yaml
# Add system monitoring
sensor:
  - platform: systemmonitor
    resources:
      - type: processor_use
      - type: memory_use_percent
      - type: disk_use_percent
        arg: /
      - type: load_1m
      - type: load_5m
      - type: network_in
        arg: eth0
      - type: network_out
        arg: eth0
```

**Entity Count Impact:**
```bash
# Check entity count via API
curl -s "http://HA_HOST:8123/api/states" \
  -H "Authorization: Bearer TOKEN" | jq 'length'

# Target: < 1000 entities for smooth performance
# > 2000 entities: Consider recorder optimization
```

**Startup Time Analysis:**
```yaml
# Enable startup timing
homeassistant:
  debug: true

# Check logs for:
# "Setup of integration X took X.XX seconds"
```

---

## Database & Recorder Optimization

### Recorder Configuration

**Basic Optimization:**
```yaml
# configuration.yaml
recorder:
  purge_keep_days: 7  # Reduce from default 10
  commit_interval: 5  # Seconds between writes (default 1)

  # Exclude high-frequency entities
  exclude:
    domains:
      - automation
      - updater
      - camera
    entity_globs:
      - sensor.date_*
      - sensor.time_*
      - sensor.uptime_*
    entities:
      - sensor.last_boot
      - sun.sun
```

**Aggressive Filtering:**
```yaml
recorder:
  purge_keep_days: 5
  commit_interval: 10

  # Include only what you need
  include:
    domains:
      - sensor
      - binary_sensor
      - switch
      - light
      - climate
    entities:
      - person.john
      - person.jane

  # Still exclude noisy entities
  exclude:
    entity_globs:
      - sensor.*_linkquality
      - sensor.*_battery_*
      - sensor.*_signal_*
```

### MariaDB Migration (Recommended)

**Install MariaDB Addon:**
1. Settings > Add-ons > MariaDB
2. Configure with strong password
3. Start addon

**Configuration:**
```yaml
# configuration.yaml
recorder:
  db_url: mysql://homeassistant:PASSWORD@core-mariadb/homeassistant?charset=utf8mb4
  purge_keep_days: 14
  commit_interval: 1
```

**MariaDB Tuning (Advanced):**
```ini
# Custom mariadb options (in addon config)
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
```

### PostgreSQL Migration

**Docker Setup:**
```yaml
# docker-compose.yml addition
postgres:
  image: postgres:15
  environment:
    POSTGRES_DB: homeassistant
    POSTGRES_USER: homeassistant
    POSTGRES_PASSWORD: secure_password
  volumes:
    - ./postgres_data:/var/lib/postgresql/data
```

**Configuration:**
```yaml
recorder:
  db_url: postgresql://homeassistant:secure_password@postgres/homeassistant
```

### Long-Term Statistics (InfluxDB)

**Use Case:** Keep detailed history for years without database bloat

**InfluxDB Addon Setup:**
1. Install InfluxDB addon
2. Create database and user
3. Configure integration

**Configuration:**
```yaml
# configuration.yaml
influxdb:
  host: a0d7b954-influxdb
  port: 8086
  database: homeassistant
  username: homeassistant
  password: !secret influxdb_password
  max_retries: 3

  # Only send important sensors
  include:
    domains:
      - sensor
    entities:
      - climate.thermostat

  # Exclude noisy data
  exclude:
    entity_globs:
      - sensor.*_battery
```

### Database Maintenance

**Manual Purge:**
```bash
# Via service call
curl -X POST "http://HA_HOST:8123/api/services/recorder/purge" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keep_days": 5, "repack": true}'
```

**Statistics Cleanup:**
```yaml
# Remove old statistics
service: recorder.purge_entities
data:
  entity_id:
    - sensor.old_entity
  keep_days: 0
```

**Database Size Check (SQLite):**
```bash
# Via SSH
ls -lh /config/home-assistant_v2.db

# Should be < 1GB for smooth operation
# If larger, increase filtering or migrate to MariaDB
```

---

## Security Hardening

### SSL/TLS Configuration

**Let's Encrypt with DuckDNS:**
```yaml
# Install DuckDNS addon
# Configure with your subdomain and token

# configuration.yaml
http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
  server_port: 443
```

**Self-Signed Certificate:**
```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 \
  -keyout /ssl/privkey.pem \
  -out /ssl/fullchain.pem \
  -days 365 -nodes \
  -subj "/CN=homeassistant.local"

# configuration.yaml
http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

**Nginx Proxy Manager:**
```yaml
# Use NPM addon for SSL termination
# Supports Let's Encrypt auto-renewal
# Reverse proxy to HA on port 8123
```

### Authentication Hardening

**IP Banning:**
```yaml
http:
  ip_ban_enabled: true
  login_attempts_threshold: 5
  # Banned IPs stored in /config/ip_bans.yaml
```

**Trusted Networks:**
```yaml
homeassistant:
  auth_providers:
    - type: homeassistant
    - type: trusted_networks
      trusted_networks:
        - 192.168.1.0/24
        - 10.0.0.0/8
      trusted_users:
        192.168.1.100:
          - user_id_here
      allow_bypass_login: true  # Skip login from trusted networks
```

**Multi-Factor Authentication:**
1. Profile > Security > Multi-factor auth modules
2. Enable TOTP (Time-based One-Time Password)
3. Scan QR code with authenticator app

### Network Security

**Firewall Rules (Linux):**
```bash
# Allow only local network to HA
sudo ufw allow from 192.168.1.0/24 to any port 8123

# Block external access
sudo ufw deny 8123
```

**Reverse Proxy Headers:**
```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 192.168.1.1  # Your proxy IP
    - 172.30.33.0/24  # Docker network
```

### Secrets Management Best Practices

**secrets.yaml Structure:**
```yaml
# /config/secrets.yaml
# CRITICAL: Add to .gitignore

# API Keys
openweathermap_api: "abc123..."
google_api_key: "xyz789..."

# Passwords
mqtt_password: "secure_mqtt_pass"
mariadb_password: "secure_db_pass"
influxdb_password: "secure_influx_pass"

# Tokens
telegram_bot_token: "bot123:ABC..."
pushover_api_key: "po_key..."

# Sensitive URLs
database_url: "mysql://user:pass@host/db"

# Coordinates (privacy)
home_latitude: 40.7128
home_longitude: -74.0060
home_elevation: 10

# Encryption keys
api_encryption_key: "base64_32_byte_key..."
```

**Environment Variables (Docker):**
```yaml
# docker-compose.yml
environment:
  - HASS_HTTP_SSL_CERTIFICATE=/ssl/fullchain.pem
  - HASS_HTTP_SSL_KEY=/ssl/privkey.pem
```

### Security Audit Checklist

```bash
# 1. Check for hardcoded secrets
grep -rE "(password|api_key|token):" /config/*.yaml | grep -v "!secret"

# 2. Verify secrets.yaml permissions
ls -la /config/secrets.yaml  # Should be 600 or 640

# 3. Check exposed ports
netstat -tlnp | grep -E "8123|1883|8080"

# 4. Review auth providers
grep -A 10 "auth_providers" /config/configuration.yaml

# 5. Check for default passwords
grep -r "password: admin\|password: homeassistant" /config/

# 6. Verify SSL is enabled
grep -A 5 "http:" /config/configuration.yaml | grep ssl

# 7. Check IP ban status
cat /config/ip_bans.yaml 2>/dev/null || echo "No bans"
```

---

## Custom Integration Development

### Project Structure

```
custom_components/
└── my_integration/
    ├── __init__.py       # Integration setup
    ├── manifest.json     # Integration metadata
    ├── config_flow.py    # UI configuration
    ├── const.py          # Constants
    ├── sensor.py         # Sensor platform
    ├── switch.py         # Switch platform
    ├── strings.json      # English strings
    └── translations/
        └── en.json       # Translations
```

### manifest.json

```json
{
  "domain": "my_integration",
  "name": "My Integration",
  "version": "1.0.0",
  "documentation": "https://github.com/user/my_integration",
  "issue_tracker": "https://github.com/user/my_integration/issues",
  "dependencies": [],
  "codeowners": ["@username"],
  "requirements": ["some_library==1.0.0"],
  "config_flow": true,
  "iot_class": "local_polling"
}
```

**IoT Classes:**
- `local_push` - Device pushes updates
- `local_polling` - HA polls device locally
- `cloud_push` - Cloud pushes updates
- `cloud_polling` - HA polls cloud API
- `calculated` - Derived from other entities

### Basic Integration (__init__.py)

```python
"""My Integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "my_integration"
PLATFORMS = ["sensor", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
```

### Config Flow (UI Setup)

```python
"""Config flow for My Integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from .const import DOMAIN

class MyIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate input
            try:
                # Test connection
                await self._test_connection(user_input[CONF_HOST])
            except ConnectionError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PASSWORD): str,
            }),
            errors=errors,
        )

    async def _test_connection(self, host):
        """Test connection to device."""
        # Implement connection test
        pass
```

### Sensor Platform

```python
"""Sensor platform for My Integration."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor platform."""
    async_add_entities([MySensor(entry)])

class MySensor(SensorEntity):
    """My sensor entity."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, entry):
        """Initialize sensor."""
        self._attr_name = "My Temperature"
        self._attr_unique_id = f"{entry.entry_id}_temperature"
        self._attr_native_value = None

    async def async_update(self):
        """Update sensor state."""
        # Fetch data from device/API
        self._attr_native_value = 21.5
```

### Async Patterns

```python
"""Async data coordinator pattern."""
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class MyCoordinator(DataUpdateCoordinator):
    """Data coordinator for My Integration."""

    def __init__(self, hass, client):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="My Integration",
            update_interval=timedelta(seconds=30),
        )
        self.client = client

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            return await self.client.async_get_data()
        except ApiError as err:
            raise UpdateFailed(f"Error fetching data: {err}")
```

---

## Advanced Jinja2 Templating

### Template Fundamentals

**Testing Templates:**
- Developer Tools > Template
- Live preview as you type
- Access to all entities and states

**Basic Syntax:**
```jinja2
{# Comment - not rendered #}
{{ expression }}           {# Output expression result #}
{% statement %}           {# Control flow #}
```

### State Access

```jinja2
{# Get entity state #}
{{ states('sensor.temperature') }}

{# Get attribute #}
{{ state_attr('sensor.temperature', 'unit_of_measurement') }}

{# Check state #}
{{ is_state('light.living_room', 'on') }}

{# Get all attributes #}
{{ states.sensor.temperature.attributes }}

{# Last changed timestamp #}
{{ states.sensor.temperature.last_changed }}
```

### Filters & Functions

```jinja2
{# Type conversion #}
{{ states('sensor.temp') | float }}
{{ states('sensor.count') | int }}
{{ 'true' | bool }}

{# Math operations #}
{{ (states('sensor.temp') | float) * 1.8 + 32 }}
{{ states('sensor.value') | float | round(2) }}
{{ [1, 2, 3] | sum }}
{{ [1, 2, 3] | average }}

{# String operations #}
{{ 'hello world' | upper }}
{{ 'HELLO' | lower }}
{{ 'hello' | capitalize }}
{{ 'hello world' | title }}
{{ 'text' | replace('e', 'a') }}
{{ 'a,b,c' | split(',') }}

{# Date/time #}
{{ now() }}
{{ now().strftime('%Y-%m-%d %H:%M') }}
{{ as_timestamp(now()) }}
{{ as_datetime(states('sensor.timestamp')) }}
{{ relative_time(states.sensor.motion.last_changed) }}

{# Default values #}
{{ states('sensor.maybe_missing') | default('N/A') }}
{{ states('sensor.temp') | float(0) }}  {# Default if conversion fails #}
```

### Control Structures

```jinja2
{# Conditionals #}
{% if is_state('light.living_room', 'on') %}
  Light is on
{% elif is_state('light.living_room', 'unavailable') %}
  Light is unavailable
{% else %}
  Light is off
{% endif %}

{# Ternary operator #}
{{ 'Occupied' if is_state('binary_sensor.motion', 'on') else 'Empty' }}

{# Loops #}
{% for light in states.light %}
  {{ light.entity_id }}: {{ light.state }}
{% endfor %}

{# Loop with filter #}
{% for light in states.light | selectattr('state', 'eq', 'on') %}
  {{ light.name }} is on
{% endfor %}

{# Loop with index #}
{% for item in ['a', 'b', 'c'] %}
  {{ loop.index }}: {{ item }}
{% endfor %}
```

### Advanced Templates

**Count Entities by State:**
```jinja2
{{ states.light | selectattr('state', 'eq', 'on') | list | count }}

{# With area filter #}
{{ states.light
   | selectattr('state', 'eq', 'on')
   | selectattr('attributes.area_id', 'eq', 'living_room')
   | list | count }}
```

**List All Entities in State:**
```jinja2
{% set on_lights = states.light | selectattr('state', 'eq', 'on') | map(attribute='name') | list %}
{{ on_lights | join(', ') if on_lights else 'No lights on' }}
```

**Time-Based Logic:**
```jinja2
{% set hour = now().hour %}
{% if hour < 6 %}Night
{% elif hour < 12 %}Morning
{% elif hour < 18 %}Afternoon
{% else %}Evening{% endif %}

{# Is it daytime? #}
{{ is_state('sun.sun', 'above_horizon') }}

{# Minutes until sunset #}
{{ ((as_timestamp(state_attr('sun.sun', 'next_setting')) - as_timestamp(now())) / 60) | round }}
```

**Sensor Aggregation:**
```jinja2
{% set temps = [
  states('sensor.living_room_temp') | float,
  states('sensor.bedroom_temp') | float,
  states('sensor.kitchen_temp') | float
] %}
Average: {{ (temps | sum / temps | length) | round(1) }}°
Max: {{ temps | max }}°
Min: {{ temps | min }}°
```

### Custom Template Sensors

```yaml
# configuration.yaml
template:
  - sensor:
      - name: "Lights On Count"
        unique_id: lights_on_count
        state: >
          {{ states.light | selectattr('state', 'eq', 'on') | list | count }}
        icon: mdi:lightbulb-group

      - name: "Average Indoor Temperature"
        unique_id: avg_indoor_temp
        state: >
          {% set temps = [
            states('sensor.living_room_temp'),
            states('sensor.bedroom_temp'),
            states('sensor.office_temp')
          ] | map('float', 0) | select('>', 0) | list %}
          {{ (temps | sum / temps | count) | round(1) if temps else 'unknown' }}
        unit_of_measurement: "°F"
        device_class: temperature
        state_class: measurement
        availability: >
          {{ states('sensor.living_room_temp') not in ['unavailable', 'unknown'] }}

  - binary_sensor:
      - name: "Anyone Home"
        unique_id: anyone_home
        state: >
          {{ states.person | selectattr('state', 'eq', 'home') | list | count > 0 }}
        device_class: presence

      - name: "Windows Open"
        unique_id: windows_open
        state: >
          {{ states.binary_sensor
             | selectattr('attributes.device_class', 'eq', 'window')
             | selectattr('state', 'eq', 'on')
             | list | count > 0 }}
        device_class: window
```

### Macros (Reusable Functions)

```yaml
# Create in custom_templates/macros.jinja
{% macro light_status(entity) %}
  {% if is_state(entity, 'on') %}
    {{ state_attr(entity, 'brightness') | int(0) / 255 * 100 | round }}%
  {% else %}
    Off
  {% endif %}
{% endmacro %}

{% macro format_duration(seconds) %}
  {% set hours = (seconds // 3600) | int %}
  {% set minutes = ((seconds % 3600) // 60) | int %}
  {{ hours }}h {{ minutes }}m
{% endmacro %}
```

**Using Macros:**
```yaml
# configuration.yaml
homeassistant:
  packages: !include_dir_named packages

# In templates, import with:
# {% from 'macros.jinja' import light_status, format_duration %}
```

### JavaScript in Button-Card

```yaml
type: custom:button-card
entity: sensor.temperature
name: |
  [[[
    return `Temperature: ${entity.state}°F`;
  ]]]
icon: |
  [[[
    const temp = parseFloat(entity.state);
    if (temp > 80) return 'mdi:thermometer-alert';
    if (temp > 70) return 'mdi:thermometer';
    return 'mdi:thermometer-low';
  ]]]
styles:
  icon:
    - color: |
        [[[
          const temp = parseFloat(entity.state);
          if (temp > 80) return '#ff5722';
          if (temp > 70) return '#ff9800';
          if (temp > 60) return '#4caf50';
          return '#2196f3';
        ]]]
  card:
    - background: |
        [[[
          const temp = parseFloat(entity.state);
          const hue = Math.max(0, Math.min(240, 240 - (temp - 50) * 4));
          return `hsl(${hue}, 70%, 20%)`;
        ]]]
```

---

## Dashboard Pro - Design & Customization

### Dashboard Design Workflow

**CRITICAL: When building a new dashboard, first ask the user:**

```
What type of dashboard are you creating?

1. **Wall-mounted tablet** (10-15" fixed display)
   - Larger touch targets, always-visible info
   - Optimized for landscape orientation
   - Pop-ups for detailed controls

2. **Mobile phone** (handheld, responsive)
   - Compact cards, vertical scrolling
   - Bottom navigation for easy thumb access
   - Quick glance information

3. **Desktop/laptop browser** (large screen)
   - Multi-column layouts, more data density
   - Side-by-side comparisons
   - Advanced graphs and charts

4. **All devices** (fully responsive)
   - Uses layout-card with media queries
   - Adapts to screen size automatically
```

---

### HACS Setup (Required for Custom Cards)

**Install HACS:**
```bash
# Via SSH to Home Assistant
wget -O - https://get.hacs.xyz | bash -

# Or manually download to /config/custom_components/hacs/
```

**Enable in configuration.yaml:**
```yaml
# Not required for newer HACS versions, but ensure custom resources work
frontend:
  extra_module_url:
    - /hacsfiles/lovelace-card-mod/card-mod.js
```

**Essential HACS Frontend Resources:**

| Card | Purpose | Install Priority |
|------|---------|------------------|
| `card-mod` | CSS styling for ANY card | **Required** |
| `mushroom` | Clean, modern card collection | **Required** |
| `bubble-card` | Pop-ups, buttons, separators | **Required** |
| `button-card` | Ultimate customizable buttons | **Required** |
| `layout-card` | Responsive grid layouts | **Required** |
| `apexcharts-card` | Advanced data visualization | High |
| `mini-graph-card` | Simple, clean graphs | High |
| `stack-in-card` | Remove card borders in stacks | High |
| `auto-entities` | Dynamic entity lists | Medium |
| `browser-mod` | Browser control, pop-ups | Medium |

---

### Theme Setup (Dark/Modern Style)

**Enable themes in configuration.yaml:**
```yaml
frontend:
  themes: !include_dir_merge_named themes
  extra_module_url:
    - /hacsfiles/lovelace-card-mod/card-mod.js
```

**Recommended Dark Themes (via HACS):**

| Theme | Style | Best For |
|-------|-------|----------|
| Noctis | Dark blue, clean | Wall tablets, general use |
| Waves | Noctis + Caule blend | Modern dark aesthetic |
| Bubble | Minimalist dark | Mobile-first dashboards |
| Mushroom | Soft dark | Mushroom card pairing |
| Caule Black | True black AMOLED | Battery saving on OLED |
| iOS Dark | Apple-style | iOS users |

**Install Noctis Theme:**
1. HACS > Frontend > Search "Noctis"
2. Install and restart HA
3. Profile > Theme > Select "Noctis"

**Theme with card-mod enhancements:**
```yaml
# themes/noctis.yaml (add card-mod styling)
noctis:
  # Base colors
  primary-color: "#5294E2"
  accent-color: "#5294E2"

  # Card styling via card-mod
  card-mod-theme: noctis
  card-mod-card-yaml: |
    .: |
      ha-card {
        border-radius: 12px;
        box-shadow: none;
        border: 1px solid rgba(255,255,255,0.1);
      }

  # Blur effect on more-info dialogs
  card-mod-more-info-yaml: |
    $: |
      .mdc-dialog .mdc-dialog__scrim {
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        background: rgba(0,0,0,.6);
      }
```

---

### Mushroom Cards (Foundation for Clean UIs)

**Available Card Types:**

| Card | Use Case |
|------|----------|
| `mushroom-entity-card` | General entity display |
| `mushroom-light-card` | Light with brightness slider |
| `mushroom-switch-card` | Simple toggle |
| `mushroom-fan-card` | Fan with speed control |
| `mushroom-cover-card` | Blinds/covers with position |
| `mushroom-climate-card` | Thermostat control |
| `mushroom-media-player-card` | Media controls |
| `mushroom-person-card` | Person with location |
| `mushroom-alarm-control-panel-card` | Security panel |
| `mushroom-template-card` | Fully customizable |
| `mushroom-chips-card` | Status chips row |
| `mushroom-title-card` | Section headers |

**Basic Mushroom Light Card:**
```yaml
type: custom:mushroom-light-card
entity: light.living_room
name: Living Room
icon: mdi:ceiling-light
use_light_color: true
show_brightness_control: true
show_color_control: true
collapsible_controls: true
```

**Mushroom Chips Card (Status Row):**
```yaml
type: custom:mushroom-chips-card
chips:
  - type: menu
  - type: weather
    entity: weather.home
    show_conditions: true
    show_temperature: true
  - type: entity
    entity: person.john
    icon: mdi:face-man
  - type: entity
    entity: alarm_control_panel.home
  - type: conditional
    conditions:
      - entity: binary_sensor.front_door
        state: "on"
    chip:
      type: template
      icon: mdi:door-open
      icon_color: red
      content: Door Open!
```

**Mushroom Template Card (Advanced):**
```yaml
type: custom:mushroom-template-card
entity: sensor.living_room_temperature
primary: Living Room
secondary: "{{ states(entity) }}°F"
icon: mdi:thermometer
icon_color: |-
  {% set temp = states(entity) | float %}
  {% if temp > 75 %}red
  {% elif temp > 70 %}orange
  {% elif temp < 65 %}blue
  {% else %}green{% endif %}
tap_action:
  action: more-info
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, rgba(82,148,226,0.2), transparent);
    }
```

---

### Bubble Card (Pop-ups & Modern Buttons)

**Card Types:**
- `pop-up` - Full-screen overlay for detailed controls
- `button` - Versatile button with sub-buttons
- `separator` - Visual dividers
- `horizontal-buttons-stack` - Row of buttons
- `cover` - Cover/blind controls
- `media-player` - Media controls
- `empty-column` - Spacing

**Pop-up Setup:**
```yaml
# Step 1: Create pop-up card (place at TOP of view)
type: custom:bubble-card
card_type: pop-up
hash: '#living-room'
name: Living Room
icon: mdi:sofa
bg_color: var(--primary-color)
bg_opacity: 0.8
# Optional: blur background
styles: |
  .bubble-pop-up-container {
    backdrop-filter: blur(10px);
  }

# Step 2: Add content cards inside the pop-up
cards:
  - type: custom:mushroom-light-card
    entity: light.living_room
  - type: custom:mushroom-climate-card
    entity: climate.living_room
```

**Button with Sub-buttons:**
```yaml
type: custom:bubble-card
card_type: button
button_type: state
entity: light.living_room
name: Living Room
icon: mdi:sofa
show_state: true
card_layout: large
sub_button:
  - name: Ceiling
    icon: mdi:ceiling-light
    entity: light.ceiling
    show_state: true
    tap_action:
      action: toggle
  - name: Lamp
    icon: mdi:lamp
    entity: light.lamp
    show_state: true
    tap_action:
      action: toggle
  - name: LED Strip
    icon: mdi:led-strip
    entity: light.led_strip
    show_background: false
    tap_action:
      action: toggle
```

**Navigation Button to Pop-up:**
```yaml
type: custom:bubble-card
card_type: button
button_type: name
name: Living Room
icon: mdi:sofa
tap_action:
  action: navigate
  navigation_path: '#living-room'
styles: |
  .bubble-icon-container {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
  }
```

**Horizontal Button Stack:**
```yaml
type: custom:bubble-card
card_type: horizontal-buttons-stack
buttons:
  - name: Living
    icon: mdi:sofa
    tap_action:
      action: navigate
      navigation_path: '#living-room'
  - name: Kitchen
    icon: mdi:silverware-fork-knife
    tap_action:
      action: navigate
      navigation_path: '#kitchen'
  - name: Bedroom
    icon: mdi:bed
    tap_action:
      action: navigate
      navigation_path: '#bedroom'
```

---

### Button-Card (Ultimate Customization)

**Basic Button:**
```yaml
type: custom:button-card
entity: light.living_room
name: Living Room
icon: mdi:ceiling-light
show_state: true
tap_action:
  action: toggle
styles:
  card:
    - border-radius: 12px
    - background-color: var(--card-background-color)
  icon:
    - color: var(--primary-color)
```

**Button with State-based Styling:**
```yaml
type: custom:button-card
entity: light.living_room
name: Living Room
icon: mdi:ceiling-light
show_state: true
color_type: icon
state:
  - value: "on"
    color: gold
    styles:
      card:
        - background: linear-gradient(to bottom, rgba(255,215,0,0.3), transparent)
      icon:
        - animation: pulse 2s ease-in-out infinite
  - value: "off"
    color: gray
    styles:
      card:
        - background: var(--card-background-color)
```

**Button-Card Templates (Reusable Styles):**

Create in `ui-lovelace.yaml` or `button_card_templates.yaml`:
```yaml
button_card_templates:
  # Base template for all room cards
  room_card:
    show_state: true
    show_name: true
    show_icon: true
    color_type: icon
    tap_action:
      action: navigate
    styles:
      card:
        - border-radius: 16px
        - padding: 16px
        - background: var(--card-background-color)
      grid:
        - grid-template-areas: '"i n" "i s"'
        - grid-template-columns: 40% 1fr
        - grid-template-rows: min-content min-content
      icon:
        - width: 50px
        - color: var(--primary-color)
      name:
        - font-size: 16px
        - font-weight: bold
        - justify-self: start
      state:
        - font-size: 12px
        - justify-self: start
        - color: var(--secondary-text-color)

  # Light button with animated icon when on
  light_button:
    template: room_card
    state:
      - value: "on"
        styles:
          icon:
            - color: gold
            - filter: drop-shadow(0 0 10px gold)
          card:
            - background: linear-gradient(135deg, rgba(255,215,0,0.2), transparent)

  # Temperature sensor with color coding
  temp_sensor:
    show_state: true
    show_name: true
    show_icon: true
    state_display: '[[[ return `${entity.state}°F` ]]]'
    styles:
      icon:
        - color: |
            [[[
              var temp = parseFloat(entity.state);
              if (temp > 80) return '#ff5722';
              if (temp > 75) return '#ff9800';
              if (temp > 70) return '#4caf50';
              if (temp > 65) return '#03a9f4';
              return '#2196f3';
            ]]]
```

**Using Templates:**
```yaml
type: custom:button-card
template: light_button
entity: light.living_room
name: Living Room
tap_action:
  action: navigate
  navigation_path: '#living-room'
```

---

### Card-Mod (CSS Styling for ANY Card)

**Basic Styling:**
```yaml
type: entities
entities:
  - entity: light.living_room
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #1a1a2e, #16213e);
      border-radius: 16px;
      border: 1px solid rgba(255,255,255,0.1);
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
```

**Animate Icons Based on State:**
```yaml
type: custom:mushroom-entity-card
entity: fan.bedroom
card_mod:
  style:
    mushroom-shape-icon$: |
      .shape {
        {% if is_state('fan.bedroom', 'on') %}
        --shape-animation: spin 1s linear infinite;
        {% endif %}
      }
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
```

**Glassmorphism Effect:**
```yaml
card_mod:
  style: |
    ha-card {
      background: rgba(255, 255, 255, 0.05) !important;
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
    }
```

**Conditional Styling with Jinja2:**
```yaml
card_mod:
  style: |
    ha-card {
      {% if is_state('binary_sensor.motion', 'on') %}
      border: 2px solid #ff9800;
      animation: pulse 1s ease-in-out infinite;
      {% else %}
      border: 1px solid rgba(255,255,255,0.1);
      {% endif %}
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }
```

**Card-Mod in Themes (Apply Globally):**
```yaml
# themes/my-theme.yaml
my-theme:
  card-mod-theme: my-theme

  # Style all cards
  card-mod-card-yaml: |
    .: |
      ha-card {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
      }

  # Style the sidebar
  card-mod-root-yaml: |
    ha-sidebar {
      background: #1a1a2e !important;
    }
```

---

### Layout-Card (Responsive Grids)

**Basic Grid Layout:**
```yaml
type: custom:layout-card
layout_type: grid
layout:
  grid-template-columns: repeat(3, 1fr)
  grid-gap: 16px
cards:
  - type: custom:mushroom-light-card
    entity: light.living_room
  - type: custom:mushroom-light-card
    entity: light.kitchen
  - type: custom:mushroom-light-card
    entity: light.bedroom
```

**Responsive Layout with Media Queries:**
```yaml
type: custom:layout-card
layout_type: grid
layout:
  grid-template-columns: repeat(4, 1fr)
  grid-gap: 16px
  mediaquery:
    # Tablet (768px - 1024px)
    "(max-width: 1024px)":
      grid-template-columns: repeat(3, 1fr)
    # Large phone (480px - 768px)
    "(max-width: 768px)":
      grid-template-columns: repeat(2, 1fr)
    # Small phone (< 480px)
    "(max-width: 480px)":
      grid-template-columns: 1fr
cards:
  - type: custom:mushroom-light-card
    entity: light.living_room
  # ... more cards
```

**Grid with Spanning Cards:**
```yaml
type: custom:layout-card
layout_type: grid
layout:
  grid-template-columns: repeat(4, 1fr)
  grid-template-rows: auto
  grid-gap: 16px
cards:
  # Weather spans 2 columns
  - type: weather-forecast
    entity: weather.home
    view_layout:
      grid-column: span 2

  # Graph spans full width
  - type: custom:mini-graph-card
    entities:
      - sensor.temperature
    view_layout:
      grid-column: span 4

  # Regular cards
  - type: custom:mushroom-light-card
    entity: light.living_room
```

---

### ApexCharts Card (Advanced Data Visualization)

**Basic Line Chart:**
```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Temperature History
  show_states: true
  colorize_states: true
graph_span: 24h
series:
  - entity: sensor.living_room_temperature
    name: Living Room
    stroke_width: 2
    color: '#5294E2'
  - entity: sensor.outdoor_temperature
    name: Outside
    stroke_width: 2
    color: '#ff9800'
```

**Radial Bar (Gauge Style):**
```yaml
type: custom:apexcharts-card
chart_type: radialBar
header:
  show: false
series:
  - entity: sensor.cpu_usage
    name: CPU
    color: '#5294E2'
apex_config:
  plotOptions:
    radialBar:
      hollow:
        size: '60%'
      dataLabels:
        name:
          show: true
          fontSize: '14px'
        value:
          show: true
          fontSize: '24px'
```

**Energy Usage (Area Chart with Gradient):**
```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Energy Today
  show_states: true
graph_span: 24h
span:
  start: day
series:
  - entity: sensor.energy_usage
    type: area
    stroke_width: 2
    color: '#4CAF50'
    opacity: 0.3
    curve: smooth
    statistics:
      type: state
      period: hour
apex_config:
  chart:
    height: 200
  fill:
    type: gradient
    gradient:
      shadeIntensity: 0.8
      opacityFrom: 0.7
      opacityTo: 0.2
```

**Multi-Series with Comparison:**
```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Temperature Comparison
graph_span: 7d
span:
  start: week
series:
  - entity: sensor.indoor_temp
    name: Indoor
    group_by:
      func: avg
      duration: 1d
  - entity: sensor.outdoor_temp
    name: Outdoor
    group_by:
      func: avg
      duration: 1d
apex_config:
  chart:
    type: bar
  plotOptions:
    bar:
      horizontal: false
      columnWidth: '60%'
```

---

### Mini-Graph-Card (Simple Clean Graphs)

**Basic Graph:**
```yaml
type: custom:mini-graph-card
entities:
  - sensor.living_room_temperature
name: Living Room Temp
hours_to_show: 24
points_per_hour: 2
line_width: 2
```

**Multiple Entities with Styling:**
```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.living_room_temp
    name: Living Room
    color: '#5294E2'
  - entity: sensor.bedroom_temp
    name: Bedroom
    color: '#ff9800'
    show_state: true
    state_adaptive_color: true
name: Home Temperatures
hours_to_show: 24
line_width: 2
font_size: 75
show:
  labels: true
  labels_secondary: true
  extrema: true
  average: true
  fill: fade
```

**Bar Graph for Daily Stats:**
```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.daily_energy
    name: Energy
hours_to_show: 168
aggregate_func: max
group_by: date
show:
  graph: bar
  state: true
  name: true
```

---

### Floor Plan Dashboard (Picture Elements)

**Basic Floor Plan Setup:**
```yaml
type: picture-elements
image: /local/floorplan/home.png
elements:
  # Light icons
  - type: state-icon
    entity: light.living_room
    tap_action:
      action: toggle
    style:
      top: 45%
      left: 30%
      "--paper-item-icon-active-color": gold

  # Temperature label
  - type: state-label
    entity: sensor.living_room_temp
    style:
      top: 50%
      left: 30%
      color: white
      font-size: 12px

  # Room navigation
  - type: icon
    icon: mdi:sofa
    tap_action:
      action: navigate
      navigation_path: '#living-room'
    style:
      top: 55%
      left: 30%
      color: var(--primary-color)
```

**Interactive Floor Plan with Overlays:**
```yaml
type: picture-elements
image: /local/floorplan/home_dark.png
elements:
  # Light overlay (shows when on)
  - type: image
    entity: light.living_room
    tap_action:
      action: toggle
    state_image:
      "on": /local/floorplan/overlays/living_room_light.png
      "off": /local/floorplan/transparent.png
    style:
      top: 50%
      left: 50%
      width: 100%
      opacity: 0.6

  # Motion indicator
  - type: conditional
    conditions:
      - entity: binary_sensor.living_room_motion
        state: "on"
    elements:
      - type: icon
        icon: mdi:motion-sensor
        style:
          top: 40%
          left: 35%
          color: '#ff9800'
          "--mdc-icon-size": 24px
```

**3D Floor Plan Tips:**

1. Create in SweetHome3D (free software)
2. Export as PNG with transparent background
3. Create "light on" overlays for each room
4. Use conditional elements for dynamic states
5. Layer images for lighting effects

---

### Animations & Effects

**Spinning Icon (Fan, Loading):**
```yaml
card_mod:
  style:
    mushroom-shape-icon$: |
      .shape {
        --shape-animation: spin 1s linear infinite;
      }
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
```

**Pulsing Glow (Alerts):**
```yaml
card_mod:
  style: |
    ha-card {
      animation: glow 2s ease-in-out infinite;
    }
    @keyframes glow {
      0%, 100% { box-shadow: 0 0 5px rgba(255,152,0,0.5); }
      50% { box-shadow: 0 0 20px rgba(255,152,0,0.8); }
    }
```

**Color Transition:**
```yaml
card_mod:
  style: |
    ha-card {
      transition: background-color 0.3s ease, transform 0.2s ease;
    }
    ha-card:hover {
      transform: translateY(-2px);
      background-color: rgba(255,255,255,0.1);
    }
```

**Breathing Effect:**
```yaml
card_mod:
  style: |
    ha-card {
      animation: breathe 3s ease-in-out infinite;
    }
    @keyframes breathe {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.85; }
    }
```

**Gradient Animation:**
```yaml
card_mod:
  style: |
    ha-card {
      background: linear-gradient(270deg, #667eea, #764ba2, #f093fb);
      background-size: 600% 600%;
      animation: gradientShift 10s ease infinite;
    }
    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
```

---

### Complete Dashboard Examples

**Mobile-First Home View:**
```yaml
title: Home
views:
  - title: Home
    path: home
    type: custom:layout-card
    layout_type: grid
    layout:
      grid-template-columns: 1fr
      grid-gap: 8px
      mediaquery:
        "(min-width: 768px)":
          grid-template-columns: repeat(2, 1fr)
        "(min-width: 1200px)":
          grid-template-columns: repeat(3, 1fr)
    cards:
      # Status chips at top
      - type: custom:mushroom-chips-card
        chips:
          - type: weather
            entity: weather.home
          - type: entity
            entity: person.john
          - type: entity
            entity: alarm_control_panel.home
        view_layout:
          grid-column: 1 / -1

      # Room cards
      - type: custom:mushroom-template-card
        entity: light.living_room
        primary: Living Room
        secondary: "{{ states('sensor.living_room_temp') }}°F"
        icon: mdi:sofa
        tap_action:
          action: navigate
          navigation_path: '#living-room'

      # More room cards...
```

**Tablet Wall Dashboard:**
```yaml
title: Wall Panel
views:
  - title: Main
    path: main
    panel: true
    cards:
      - type: custom:layout-card
        layout_type: grid
        layout:
          grid-template-columns: 2fr 1fr
          grid-template-rows: auto 1fr
          grid-gap: 16px
          height: 100vh
        cards:
          # Left side - Floor plan
          - type: picture-elements
            image: /local/floorplan.png
            view_layout:
              grid-row: span 2
            elements:
              # ... floor plan elements

          # Right side - Quick controls
          - type: vertical-stack
            cards:
              - type: custom:mushroom-chips-card
                # ... chips
              - type: horizontal-stack
                cards:
                  # ... room buttons

          # Right side bottom - Weather & info
          - type: vertical-stack
            cards:
              - type: weather-forecast
                entity: weather.home
              - type: custom:mini-graph-card
                entities:
                  - sensor.outdoor_temp
```

---

### Dashboard YAML Mode Setup

**Enable YAML Mode:**
```yaml
# configuration.yaml
lovelace:
  mode: yaml
  resources:
    - url: /hacsfiles/button-card/button-card.js
      type: module
    - url: /hacsfiles/lovelace-card-mod/card-mod.js
      type: module
    - url: /hacsfiles/lovelace-mushroom/mushroom.js
      type: module
    - url: /hacsfiles/bubble-card/bubble-card.js
      type: module
    - url: /hacsfiles/lovelace-layout-card/layout-card.js
      type: module
    - url: /hacsfiles/apexcharts-card/apexcharts-card.js
      type: module
    - url: /hacsfiles/mini-graph-card/mini-graph-card-bundle.js
      type: module
```

**Dashboard Structure:**
```yaml
# ui-lovelace.yaml
title: My Home
button_card_templates: !include button_card_templates.yaml
views:
  - !include views/home.yaml
  - !include views/lights.yaml
  - !include views/climate.yaml
  - !include views/security.yaml
```

---

### Dashboard Troubleshooting

| Issue | Solution |
|-------|----------|
| Custom card not showing | Clear browser cache, check Resources in dashboard settings |
| card-mod styles not working | Ensure card-mod is loaded as module, check Shadow DOM paths |
| Pop-up not opening | Verify hash matches exactly (case-sensitive) |
| Layout not responsive | Check mediaquery syntax, use browser dev tools to test |
| Animations choppy | Reduce animation complexity, check device performance |
| Theme not applying | Restart HA after theme changes, check YAML syntax |
| Icons not spinning | Use correct Shadow DOM selector for card type |
| Graphs not loading | Check entity exists, verify time range has data |

---

## Backup & Restore

### Backup Locations

```bash
# HA OS - Full backup
/backup/

# Manual backup targets
/config/                    # All configuration
/config/.storage/           # Entity/device registries
/config/custom_components/  # Custom integrations
```

### Backup Commands

**Cross-Platform (Python - Recommended for Windows):**
```bash
# Use the Python backup script (works on Windows, macOS, Linux)
python scripts/backup.py /path/to/config

# Specify custom backup destination
python scripts/backup.py /path/to/config /path/to/backups

# Windows example
python scripts/backup.py C:\Users\user\homeassistant C:\backups

# The script automatically:
# - Excludes logs, databases, cache files
# - Creates timestamped .tar.gz archives
# - Cleans up old backups (keeps last 10)
# - Shows compression statistics
```

**macOS/Linux (Bash):**
```bash
# Create config backup
tar -czvf ha-config-backup-$(date +%Y%m%d).tar.gz \
  --exclude='home-assistant.log*' \
  --exclude='.storage' \
  --exclude='tts' \
  /config/

# Backup with storage (includes registries)
tar -czvf ha-full-backup-$(date +%Y%m%d).tar.gz /config/

# Or use the bash script (macOS/Linux only)
bash scripts/backup.sh /path/to/config
```

### Restore Process

1. Stop Home Assistant
2. Backup current config (safety)
3. Extract backup to /config/
4. Restart Home Assistant
5. Verify all integrations load

---

## Installation-Specific Notes

### Home Assistant OS (Recommended)
- Full Supervisor support
- Add-ons available
- Config at `/config/` or `/homeassistant/`
- SSH via Terminal add-on or SSH add-on

### Home Assistant Container (Docker)
- No Supervisor/Add-ons
- Config mounted from host
- Example: `-v /path/to/config:/config`

### Home Assistant Core (Python venv)
- Manual Python installation
- No Supervisor/Add-ons
- Config typically at `~/.homeassistant/`

---

## When to Use This Skill

**Configuration & Administration:**
- "Check my Home Assistant configuration"
- "Find YAML errors in my config"
- "What's the state of my living room lights?"
- "Turn on the bedroom fan"
- "Create an automation for motion lights"
- "Debug why my automation isn't working"
- "Review my HA security settings"
- "Help me set up a template sensor"
- "What's in my Home Assistant logs?"
- "Backup my Home Assistant configuration"
- "List all my entities"
- "Call a service via the API"

**Dashboard Design & Customization:**
- "Create a beautiful dashboard for my tablet"
- "Help me design a mobile-friendly dashboard"
- "Set up Mushroom cards for my lights"
- "Create pop-ups using Bubble Card"
- "Make my cards have animations"
- "Set up a dark theme with Noctis"
- "Create a floor plan dashboard"
- "Add graphs for my temperature sensors"
- "Make my dashboard responsive for all devices"
- "Style my cards with custom CSS"
- "Create reusable button-card templates"
- "Set up ApexCharts for energy monitoring"
- "Add spinning icons when my fan is on"
- "Create a glassmorphism effect on my cards"

## When NOT to Use This Skill

- ESPHome device configuration (use ESPHome skill)
- Zigbee/Z-Wave device pairing (use HA UI)
- Network/router configuration (use network tools)
- Creating 3D floor plan images (use SweetHome3D or similar)

---

## Additional Resources

- [REST API Reference](./reference.md) - Complete API endpoint documentation
- [Helper Scripts](./scripts/) - Cross-platform Python scripts:
  - `ha_client.py` - REST API client library
  - `config_audit.py` - Configuration security auditor
  - `backup.py` - Cross-platform backup (Windows/macOS/Linux)
  - `backup.sh` - Bash backup script (macOS/Linux only)
  - `ssh_helper.py` - Cross-platform SSH with password auth
- [Official HA Docs](https://www.home-assistant.io/docs/)
- [HA Developer Docs](https://developers.home-assistant.io/)
- [HA Community](https://community.home-assistant.io/)
