---
name: configuring-acquisition-system
description: >-
  Guides users through configuring data acquisition systems on local machines using MCP tools for hardware discovery
  and direct YAML file editing for system parameters. Covers working directory setup, hardware discovery, system
  configuration, and credential management. Use when setting up a new acquisition PC, reconfiguring hardware, or
  troubleshooting system configuration issues.
---

# Configuring Acquisition System

Guides users through configuring data acquisition systems using MCP tools for hardware discovery and direct YAML file
editing for system parameters. Supports complete system setup, targeted configuration changes, and verification
workflows.

---

## MCP Server Requirements

This skill uses MCP tools from multiple libraries. Which servers are needed depends on the system's hardware.

| Server                  | CLI Command        | Purpose                                        | Required For           |
|-------------------------|--------------------|------------------------------------------------|------------------------|
| sl-shared-assets        | `sl-configure mcp` | Working directory, credentials, task templates | All systems            |
| sl-experiment           | `sl-get mcp`       | Zaber motor discovery, project listing         | Systems with Zaber     |
| ataraxis-video-system   | `axvs mcp`         | Camera discovery, video requirements check     | Systems with cameras   |
| ataraxis-comm-interface | `axci-mcp`         | Microcontroller discovery, MQTT broker check   | Systems with AMC/MQTT  |

If a required MCP server is unavailable, inform the user which server is needed and the command to start it.

---

## Supported Acquisition Systems

| System      | Description                                 | Reference                                        |
|-------------|---------------------------------------------|--------------------------------------------------|
| `mesoscope` | Two-photon mesoscope with VR behavioral rig | [MESOSCOPE_REFERENCE.md](MESOSCOPE_REFERENCE.md) |

Each system has a reference file documenting all configurable parameters, their purposes, valid ranges, and default
values. When working with a specific system, you MUST read that system's reference file for detailed parameter
documentation.

---

## Network Storage Prerequisites

All acquisition systems require network storage locations to be mounted via SMB before configuration. These mounts
must be configured at the operating system level and are not managed by this skill or MCP tools.

### Required SMB Mounts (All Systems)

| Mount Purpose      | Configuration Field    | Description                                    |
|--------------------|------------------------|------------------------------------------------|
| Compute server     | `server_directory`     | Long-term hot storage for processed data       |
| NAS backup         | `nas_directory`        | Archival/cold storage backup                   |

### System-Specific Mounts

Each system may require additional mounts for its specific hardware. For mesoscope systems:

| Mount Purpose      | Configuration Field    | Description                                    |
|--------------------|------------------------|------------------------------------------------|
| ScanImagePC share  | `mesoscope_directory`  | Shared directory where ScanImagePC saves TIFFs |

The ScanImagePC (MATLAB workstation) must expose a shared directory that the acquisition PC can access. This enables
the acquisition system to aggregate mesoscope frame data with behavioral data during preprocessing.

### Mount Configuration

Before running this skill, ensure:
1. All network shares are mounted and accessible from the acquisition PC
2. The mount points have appropriate read/write permissions
3. Mounts persist across reboots (add to `/etc/fstab` or use systemd mount units)

Example mount verification:
```bash
# Check if mounts are accessible
ls /mnt/server/data
ls /mnt/nas/backup
ls /mnt/mesoscope/data  # Mesoscope systems only
```

If mounts are not configured, coordinate with system administrators to set up SMB shares before proceeding with
acquisition system configuration.

---

## Skill Modes

### Discovery Mode

Use when the user wants to identify connected hardware without modifying configuration.

**When to use:**
- User asks "What cameras are connected?"
- User asks "Which serial ports have microcontrollers?"
- User wants to verify hardware is accessible before configuration
- Troubleshooting hardware connectivity issues

**Available discovery tools (use those applicable to your system's hardware):**

| Hardware Type      | MCP Tool                        | Server                  |
|--------------------|---------------------------------|-------------------------|
| Cameras            | `list_cameras()`                | ataraxis-video-system   |
| Microcontrollers   | `list_microcontrollers()`       | ataraxis-comm-interface |
| Zaber motors       | `get_zaber_devices_tool()`      | sl-experiment           |
| MQTT broker        | `check_mqtt_broker(host, port)` | ataraxis-comm-interface |
| Video requirements | `check_runtime_requirements()`  | ataraxis-video-system   |
| CTI file status    | `get_cti_status()`              | ataraxis-video-system   |

### Configuration Mode

Use when the user wants to modify system configuration.

**When to use:**
- User asks to "set up" or "configure" the acquisition system
- User wants to change specific parameters (e.g., "change the lick threshold")
- User needs to update hardware port assignments after reconnecting devices

**Configuration approach:**
1. Use MCP tools for paths and credentials (working directory, Google credentials, task templates)
2. Use sl-shared-assets CLI tools for creating and managing configuration files
3. Use discovery tools to identify correct hardware values
4. Edit existing configuration files directly only for hardware parameter updates

**Important:** Always prefer existing CLIs and MCP tools over manual file operations. Use the `sl-configure` CLI from
sl-shared-assets for creating and managing system configuration files. Manual YAML editing should only be used to
update hardware parameters (camera indices, serial ports, sensor calibration) in an existing configuration file.

**MCP tools for configuration:**

| Setting            | Get Tool                              | Set Tool                              |
|--------------------|---------------------------------------|---------------------------------------|
| Working directory  | `get_working_directory_tool()`        | `set_working_directory_tool(dir)`     |
| Google credentials | `get_google_credentials_tool()`       | `set_google_credentials_tool(path)`   |
| Task templates dir | `get_task_templates_directory_tool()` | `set_task_templates_directory_tool()` |
| CTI file           | `get_cti_status()`                    | `set_cti_file(path)`                  |

**Direct file editing (hardware parameters only):**
For hardware parameters (cameras, microcontrollers, sensors, motors), edit the existing YAML configuration file.
See [Configuration File Reference](#configuration-file-reference) for file location and structure.

### Verification Mode

Use when the user wants to confirm the system is properly configured.

**When to use:**
- After completing setup
- Before running an experiment
- Troubleshooting runtime errors

**Verification checklist:**
1. Working directory is set and accessible
2. Configuration file exists and is valid YAML
3. All hardware is discoverable (cameras, microcontrollers, Zaber motors)
4. MQTT broker is reachable
5. Google credentials are configured (if using Google Sheets)
6. Task templates directory is set (if using Unity tasks)

---

## Complete Setup Workflow

Use this workflow when setting up a new machine or performing full system reconfiguration. The examples below use the
mesoscope system. For other systems, adapt the hardware discovery steps based on the system's reference file.

### Phase 1: Prerequisites

**Check video system requirements:**
```
check_runtime_requirements()
```

Expected output shows FFMPEG, Nvidia GPU, and CTI file status. If CTI is not configured and using Harvesters cameras:
```
set_cti_file("/path/to/gentl_producer.cti")
```

**Check MQTT broker:**
```
check_mqtt_broker(host="127.0.0.1", port=1883)
```

If MQTT broker is not running, inform the user to start Mosquitto or their MQTT broker service.

### Phase 2: Hardware Discovery

**Discover cameras:**
```
list_cameras()
```

Note the camera indices from the output. For mesoscope systems, identify which index corresponds to the face camera
and which to the body camera based on resolution/model information.

**Discover microcontrollers:**
```
list_microcontrollers()
```

Note the port assignments. The output shows microcontroller IDs that indicate their function:
- Actor microcontroller: Controls outputs (valve, brake, screens)
- Sensor microcontroller: Monitors inputs (lick, torque, TTL)
- Encoder microcontroller: High-precision wheel encoder

**Discover Zaber motors:**
```
get_zaber_devices_tool()
```

Note the port assignments for each motor group:
- Headbar motors: Z, Pitch, Roll axes
- Lickport motors: Z, Y, X axes
- Wheel motor: X-axis horizontal position

**Device path convention:**
- Microcontrollers use `/dev/ttyACM*` ports (USB CDC ACM devices)
- Zaber motors use `/dev/ttyUSB*` ports (USB serial adapters)

Do not confuse these device types when mapping discovered hardware to configuration fields.

### Phase 3: Working Directory and Paths

**Check current working directory:**
```
get_working_directory_tool()
```

**Set working directory if not configured:**
```
set_working_directory_tool(directory="/path/to/sun_lab_data")
```

**Create configuration directory if needed:**
Use the Bash tool to create the directory structure:
```bash
mkdir -p /path/to/sun_lab_data/configuration
```

### Phase 4: System Configuration File

**Configuration file location:**
```
{working_directory}/configuration/mesoscope_system_configuration.yaml
```

**If the file does not exist**, create it using the template in
[Configuration File Template](#configuration-file-template).

**If the file exists**, read it and update the following based on discovered hardware:

| Configuration Field | Discovery Source                  | YAML Path                       |
|---------------------|-----------------------------------|---------------------------------|
| `face_camera_index` | `list_cameras()` output           | `cameras.face_camera_index`     |
| `body_camera_index` | `list_cameras()` output           | `cameras.body_camera_index`     |
| `actor_port`        | `list_microcontrollers()` output  | `microcontrollers.actor_port`   |
| `sensor_port`       | `list_microcontrollers()` output  | `microcontrollers.sensor_port`  |
| `encoder_port`      | `list_microcontrollers()` output  | `microcontrollers.encoder_port` |
| `headbar_port`      | `get_zaber_devices_tool()` output | `assets.headbar_port`           |
| `lickport_port`     | `get_zaber_devices_tool()` output | `assets.lickport_port`          |
| `wheel_port`        | `get_zaber_devices_tool()` output | `assets.wheel_port`             |

**Ask the user for values that cannot be discovered:**
- Filesystem paths (`root_directory`, `server_directory`, `nas_directory`, `mesoscope_directory`)
- Google Sheet IDs (`surgery_sheet_id`, `water_log_sheet_id`)
- MQTT broker settings (`unity_ip`, `unity_port`) if not using defaults

### Phase 5: Credentials and Templates

**Set Google credentials:**
```
get_google_credentials_tool()
set_google_credentials_tool(credentials_path="/path/to/credentials.json")
```

**Set task templates directory:**
```
get_task_templates_directory_tool()
set_task_templates_directory_tool(directory="/path/to/sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations")
```

### Phase 6: Verification

**Re-run discovery to confirm hardware:**
```
list_cameras()
list_microcontrollers()
get_zaber_devices_tool()
check_mqtt_broker(host="127.0.0.1", port=1883)
```

**Verify configuration file is valid:**
Read the configuration file and check for YAML syntax errors.

**Check projects exist:**
```
get_projects_tool()
```

If no projects exist and the user wants to create them, use the `/experiment-design` skill which provides MCP tools
for creating projects and experiment configurations. Do not create project directories manually.

---

## Next Steps

After completing system configuration, the acquisition system is ready for experiment design and execution.

**Creating experiments:**
Use the `/experiment-design` skill to create projects and experiment configurations. This skill provides MCP tools
for selecting task templates, configuring experiment states, and customizing trial parameters.

**Typical workflow sequence:**
1. `/acquisition-system-setup` - Configure hardware and system (this skill)
2. `/experiment-design` - Create experiment configurations
3. `sl-run` CLI - Execute experiments

---

## sl-configure CLI Reference

The `sl-configure` CLI from sl-shared-assets manages configuration files. Use these commands instead of manual file
operations.

| Command                   | Purpose                                            |
|---------------------------|----------------------------------------------------|
| `sl-configure directory`  | Set working directory for configuration storage    |
| `sl-configure system`     | Create system configuration file (clears existing) |
| `sl-configure google`     | Set Google credentials file path                   |
| `sl-configure templates`  | Set task templates directory path                  |
| `sl-configure project`    | Create project directory structure                 |
| `sl-configure experiment` | Create experiment from task template               |
| `sl-configure server`     | Configure remote compute server connection         |
| `sl-configure mcp`        | Start MCP server for agentic access                |

**Creating a new system configuration:**
```bash
sl-configure system -s mesoscope
```

This command creates a new `mesoscope_system_configuration.yaml` file with default values and removes any existing
system configuration files. After running, edit the file to set hardware-specific parameters.

---

## Configuration File Reference

### File Location

The system configuration file is located at:
```
{working_directory}/configuration/<system_name>_system_configuration.yaml
```

For mesoscope: `mesoscope_system_configuration.yaml`

To find the working directory, use `get_working_directory_tool()`.

### YAML Formatting Rules

When editing the configuration file, follow these formatting rules to maintain compatibility with sl-shared-assets:

| Rule                  | Example                                        |
|-----------------------|------------------------------------------------|
| Indent nested fields  | 10 spaces                                      |
| Document start marker | `---` on first line                            |
| Document end marker   | `...` on last line                             |
| Integers              | `500` (no decimal point)                       |
| Floats                | `15.0333` (include decimal point)              |
| Strings               | No quotes unless containing special characters |
| Booleans              | `true` or `false` (lowercase)                  |

### Section Overview

| Section            | Purpose                                            | Discovery Tool             |
|--------------------|----------------------------------------------------|----------------------------|
| `filesystem`       | Data storage paths (local, server, NAS, mesoscope) | None (user-provided)       |
| `sheets`           | Google Sheet IDs for lab records                   | None (user-provided)       |
| `cameras`          | Camera indices and encoding parameters             | `list_cameras()`           |
| `microcontrollers` | USB ports and sensor calibration                   | `list_microcontrollers()`  |
| `assets`           | Zaber motor ports and MQTT settings                | `get_zaber_devices_tool()` |

For detailed parameter documentation, see [MESOSCOPE_REFERENCE.md](MESOSCOPE_REFERENCE.md).

---

## Configuration File Template (Mesoscope)

Use this template when creating a new mesoscope configuration file. Replace placeholder values with actual paths and
discovered hardware values. For other systems, refer to their reference files for the appropriate template structure.

```yaml
---
name: mesoscope
filesystem:
          root_directory: /path/to/local/data
          server_directory: /mnt/server/data
          nas_directory: /mnt/nas/backup
          mesoscope_directory: /mnt/mesoscope/data
sheets:
          surgery_sheet_id: ""
          water_log_sheet_id: ""
cameras:
          face_camera_index: 0
          body_camera_index: 1
          face_camera_quantization: 20
          face_camera_preset: 7
          body_camera_quantization: 20
          body_camera_preset: 7
microcontrollers:
          actor_port: /dev/ttyACM0
          sensor_port: /dev/ttyACM1
          encoder_port: /dev/ttyACM2
          keepalive_interval_ms: 500
          minimum_brake_strength_g_cm: 43.2047
          maximum_brake_strength_g_cm: 1152.1246
          wheel_diameter_cm: 15.0333
          wheel_encoder_ppr: 8192
          wheel_encoder_report_cw: false
          wheel_encoder_report_ccw: true
          wheel_encoder_delta_threshold_pulse: 15
          wheel_encoder_polling_delay_us: 500
          lick_threshold_adc: 600
          lick_signal_threshold_adc: 300
          lick_delta_threshold_adc: 300
          lick_averaging_pool_size: 2
          torque_baseline_voltage_adc: 2048
          torque_maximum_voltage_adc: 3443
          torque_sensor_capacity_g_cm: 720.0779
          torque_report_cw: true
          torque_report_ccw: true
          torque_signal_threshold_adc: 150
          torque_delta_threshold_adc: 100
          torque_averaging_pool_size: 4
          valve_calibration_data:
                    15000: 1.1
                    30000: 3.0
                    45000: 6.25
                    60000: 10.9
          sensor_polling_delay_ms: 1
          screen_trigger_pulse_duration_ms: 500
          cm_per_unity_unit: 10.0
assets:
          headbar_port: /dev/ttyUSB0
          lickport_port: /dev/ttyUSB1
          wheel_port: /dev/ttyUSB2
          unity_ip: 127.0.0.1
          unity_port: 1883
...
```

---

## Quick Reference

### Hardware Discovery Commands

| Hardware           | MCP Tool                               | What to Look For                   |
|--------------------|----------------------------------------|------------------------------------|
| Cameras            | `list_cameras()`                       | Index, resolution, model name      |
| Microcontrollers   | `list_microcontrollers()`              | Port path, microcontroller ID      |
| Zaber motors       | `get_zaber_devices_tool()`             | Port path, device name, axis count |
| MQTT broker        | `check_mqtt_broker("127.0.0.1", 1883)` | Connection success/failure         |
| Video requirements | `check_runtime_requirements()`         | FFMPEG, GPU, CTI status            |

### Path and Credential Commands

| Setting            | Get Command                           | Set Command                           |
|--------------------|---------------------------------------|---------------------------------------|
| Working directory  | `get_working_directory_tool()`        | `set_working_directory_tool(dir)`     |
| Google credentials | `get_google_credentials_tool()`       | `set_google_credentials_tool(path)`   |
| Task templates     | `get_task_templates_directory_tool()` | `set_task_templates_directory_tool()` |
| CTI file           | `get_cti_status()`                    | `set_cti_file(path)`                  |

---

## Troubleshooting

| Error                             | Cause                        | Solution                            |
|-----------------------------------|------------------------------|-------------------------------------|
| `Unable to resolve the path`      | Working directory not set    | Use `set_working_directory_tool()`  |
| `found 0 files`                   | No config file exists        | Use `sl-configure` CLI to create    |
| `found N files` (N > 1)           | Multiple config files exist  | Use `sl-configure` CLI to clear     |
| `Unable to resolve...credentials` | Google credentials not set   | Use `set_google_credentials_tool()` |
| Camera not found at index         | Wrong camera index in config | Run `list_cameras()` and update     |
| Microcontroller connection failed | Wrong port or disconnected   | Run `list_microcontrollers()`       |
| Zaber motor not responding        | Wrong port or powered off    | Run `get_zaber_devices_tool()`      |
| MQTT broker unreachable           | Broker not running           | Start Mosquitto or MQTT broker      |
| YAML parse error                  | Malformed config file        | Check indentation (10 spaces)       |
