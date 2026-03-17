---
name: Config Backup
description: Backup network device configurations with group/role/site filtering. Use when user asks to "backup config", "save configuration", "export configs", or needs to persist device configurations.
version: 1.0.0

# OLAV Extended Fields
intent: backup
complexity: simple

# Output Configuration
output:
  format: markdown
  language: auto
  sections:
    - summary
    - details
---

# Config Backup Skill

Backup network device configurations to local storage with flexible filtering options.

## Workflow

1. **List Available Devices**: Call `list_devices()` to view all devices and their group/role/site attributes
2. **Filter Target Devices**: Select devices by group, role, or site (e.g., "core role" → R3, R4)
3. **Execute Backup Commands**: Run `nornir_execute(device, "show running-config")` on each device
4. **Save Configurations**: Call `save_device_config(device, "running", content)` to persist backups

## Device Classification

View device attributes with `list_devices()`:

| Device | Groups | Role | Site |
|--------|--------|------|------|
| R1 | test | border | lab |
| R2 | test | border | lab |
| R3 | test | core | lab |
| R4 | test | core | lab |
| SW1 | test | access | lab |
| SW2 | test | access | lab |

## Usage Examples

### Backup by Group
```
User: backup group:test running config
Process:
  1. list_devices() → Find devices in "test" group
  2. Execute show running-config on R1, R2, R3, R4, SW1, SW2
  3. save_device_config saves each config to data/exports/
```

### Backup by Role
```
User: backup role:core all configs
Process:
  1. list_devices() → Find devices with role="core" (R3, R4)
  2. nornir_execute fetches running + startup configs
  3. save_device_config persists both configs
```

### Backup by Site
```
User: backup site:lab running config
Process:
  1. list_devices() → Find all devices at site="lab"
  2. Batch backup all 6 devices
```

### Single Device Backup
```
User: backup R1 running config
Process:
  1. nornir_execute("R1", "show running-config")
  2. save_device_config("R1", "running", content)
```

## Backup Types

- `running` - Current running configuration (show running-config)
- `startup` - Startup configuration (show startup-config)
- `all` - Both running and startup configs

## Backup Storage

All backups are saved to `agent_dir/data/configs/`:
```
agent_dir/data/configs/
├── R1-running-config-20260108-120000.txt
├── R2-running-config-20260108-120000.txt
├── R1-startup-config-20260108-120000.txt
└── ...
```

## Version Control with Git

```bash
# Initialize repository (one-time)
cd agent_dir/data
git init
git config user.name "OLAV Backup"

# After backup
git add -A
git commit -m "Backup $(date +%Y%m%d-%H%M%S)"

# View backup history
git log --oneline | head -10
```

## Supported Filters

| Filter | Example | Matches |
|--------|---------|---------|
| Group | `group:test` | All devices in "test" group |
| Role | `role:core` | All devices with role="core" |
| Site | `site:lab` | All devices at site="lab" |
| Comma-list | `R1,R2,R3` | Specific devices |
| All | `all` | All available devices |
