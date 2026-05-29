---
name: configuring-acquisition-system
description: >-
  Guides users through configuring a data acquisition system on the local machine. Covers working directory setup,
  acquisition system selection and parameter configuration, and Google credentials setup. Use when setting up a new
  acquisition PC, changing acquisition system type, or when the user asks about system configuration.
---

# Acquisition System Setup

Guides users through configuring data acquisition systems on local machines. Supports both complete system setup and
flexible ad-hoc configuration changes for any supported acquisition system.

---

## Prerequisites

The MCP server must be running. Start it with: `sl-configure mcp`

---

## Supported Acquisition Systems

| System      | Description                         | Reference                         |
|-------------|-------------------------------------|-----------------------------------|
| `mesoscope` | Two-photon mesoscope imaging system | [MESOSCOPE_REFERENCE.md](MESOSCOPE_REFERENCE.md) |

Each system has its own reference file documenting all configurable parameters, their purposes, valid ranges, and
default values based on actual usage in sl-experiment.

---

## Usage Modes

This skill supports two modes of operation:

### Flexible Mode (Default)

For users who want to check or modify specific configuration parameters without following a structured workflow.
Use this mode when the user:

- Asks about a specific configuration section (e.g., "What are my camera settings?")
- Wants to update specific parameters (e.g., "Change the lick threshold to 500")
- Needs to reconfigure one aspect of an existing system
- Asks general questions about system configuration

In flexible mode, respond directly to the user's request using the appropriate query or update tools. Refer to the
system-specific reference file for parameter details.

### Complete Setup Mode

For users setting up a new machine or performing a full system reconfiguration. Use this mode when the user:

- Explicitly asks to "set up" or "configure" the acquisition system from scratch
- Is working with a machine that has no existing configuration
- Asks for a "complete setup" or "full configuration"

In complete setup mode, follow the structured workflow in the [Complete Setup Workflow](#complete-setup-workflow)
section.

---

## Quick Reference

### Check Current Configuration

| What to Check            | Tool                                       |
|--------------------------|--------------------------------------------|
| Working directory        | `get_working_directory_tool()`             |
| System overview          | `get_system_configuration_tool()`          |
| Available sections       | `list_system_configuration_sections_tool()`|
| Directory paths          | `get_filesystem_configuration_tool()`      |
| Google Sheet IDs         | `get_sheets_configuration_tool()`          |
| Camera settings          | `get_cameras_configuration_tool()`         |
| Microcontroller settings | `get_microcontrollers_configuration_tool()`|
| External assets          | `get_external_assets_configuration_tool()` |
| Google credentials       | `get_google_credentials_tool()`            |

### Update Configuration

| What to Update           | Tool                                          |
|--------------------------|-----------------------------------------------|
| Working directory        | `set_working_directory_tool()`                |
| Create/replace system    | `create_system_configuration_tool()`          |
| Directory paths          | `update_filesystem_configuration_tool()`      |
| Google Sheet IDs         | `update_sheets_configuration_tool()`          |
| Camera settings          | `update_cameras_configuration_tool()`         |
| Microcontroller ports    | `update_microcontroller_ports_tool()`         |
| Wheel/encoder settings   | `update_wheel_configuration_tool()`           |
| Brake calibration        | `update_brake_configuration_tool()`           |
| Lick sensor calibration  | `update_lick_sensor_configuration_tool()`     |
| Torque sensor calibration| `update_torque_sensor_configuration_tool()`   |
| Valve calibration        | `update_valve_calibration_tool()`             |
| Timing parameters        | `update_timing_configuration_tool()`          |
| Zaber/MQTT settings      | `update_external_assets_configuration_tool()` |
| Google credentials       | `set_google_credentials_tool()`               |

---

## Flexible Mode Guidelines

When operating in flexible mode, follow these guidelines:

### Responding to Queries

When the user asks about configuration, query the relevant section and present the information clearly. Refer to the
system-specific reference file to explain what each parameter controls.

### Responding to Update Requests

When the user wants to change a parameter:

1. Confirm you understand what they want to change
2. Check the reference file for valid ranges and constraints
3. Call the appropriate update tool with the new value(s)
4. Confirm the change was successful

### Handling Ambiguous Requests

If the user's request is ambiguous, ask for clarification. Reference the system-specific documentation to help guide
them to the correct parameter.

### Proactive Assistance

When the user modifies one parameter, you may suggest related parameters they might also want to check or update based
on the reference documentation, but do not make changes without explicit confirmation.

---

## Complete Setup Workflow

Use this workflow when the user requests a complete system setup.

### Workflow Checklist

```
Acquisition System Setup Progress:
- [ ] Step 1: Check/set working directory
- [ ] Step 2: Check/create acquisition system configuration
- [ ] Step 3: Configure system parameters
- [ ] Step 4: Configure Google credentials
- [ ] Step 5: Verify complete setup
```

### Step 1: Working Directory

Check if configured:
```python
get_working_directory_tool()
```

If not configured, ask the user for their preferred location and set it:
```python
set_working_directory_tool(directory="/path/to/sun_lab_data")
```

### Step 2: Acquisition System

Check if configured:
```python
get_system_configuration_tool()
```

If not configured, ask which system type to create:
```python
create_system_configuration_tool(system="mesoscope")
```

If already configured, ask the user if they want to:
1. Keep the current system and proceed to parameter configuration
2. Replace with a new configuration
3. Skip to Google credentials

### Step 3: System Parameters

Show available configuration sections:
```python
list_system_configuration_sections_tool()
```

For each section the user wants to configure:
1. Query current values with the appropriate `get_*` tool
2. Reference the system-specific documentation file to explain parameters
3. Ask which parameters they want to change
4. Apply changes with the appropriate `update_*` tool

### Step 4: Google Credentials

Check current status:
```python
get_google_credentials_tool()
```

If not configured or user wants to replace, ask for the credentials path:
```python
set_google_credentials_tool(credentials_path="/path/to/credentials.json")
```

### Step 5: Verification

Verify all configurations are working:
```python
get_working_directory_tool()
get_system_configuration_tool()
get_google_credentials_tool()  # If configured
```

---

## Configuration Sections Overview

Each acquisition system has these configurable sections:

| Section           | Purpose                                           |
|-------------------|---------------------------------------------------|
| Filesystem        | Directory paths for data storage and network mounts|
| Google Sheets     | Sheet identifiers for lab records                 |
| Cameras           | Video camera indices and encoding parameters      |
| Microcontrollers  | USB ports and hardware calibration parameters     |
| External Assets   | Motor controllers and communication settings      |

See the system-specific reference file for detailed parameter documentation including:
- What each parameter controls in practice
- Which sl-experiment component uses it
- Valid ranges and constraints
- Default values and why they matter

---

## Troubleshooting

| Error                                    | Cause                              | Solution                                  |
|------------------------------------------|------------------------------------|-------------------------------------------|
| `Unable to resolve the path`             | Working directory not configured   | Call `set_working_directory_tool()`       |
| `found 0 files`                          | No system configuration exists     | Call `create_system_configuration_tool()` |
| `found N files` (N > 1)                  | Multiple configuration files exist | Delete extra files, keep only one         |
| `Unable to resolve...credentials file`   | Google credentials not set         | Call `set_google_credentials_tool()`      |
