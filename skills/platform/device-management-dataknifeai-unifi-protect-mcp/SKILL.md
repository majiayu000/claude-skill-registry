---
name: device-management
description: Manage device adoption and onboarding, maintain device inventory, and monitor device configurations across your UniFi Protect infrastructure.
---

# Device Management Skill

Manage device adoption, maintain inventory, and monitor device configurations.

## What this skill does

This skill enables you to:
- Manage device adoption and onboarding process
- Maintain comprehensive device inventory (cameras, sensors, lights)
- Monitor device configurations and status
- Track pending devices awaiting adoption
- Plan device upgrades and replacements
- Monitor Protect system status and versions

## When to use this skill

Use this skill when you need to:
- Adopt new devices into the Protect system
- Create and maintain device inventory
- Check device adoption status
- Monitor system versions and updates
- Plan hardware refreshes
- Track device models and specifications
- Verify device configuration compliance

## Available Tools

- `get_protect_devices` - List cameras and monitoring devices
- `get_protect_sensors` - List sensors
- `get_protect_info` - Get system info and status

## Typical Workflows

### New Device Adoption
1. Use `get_protect_devices` to find new devices
2. Review device details (MAC address, IP, model)
3. Plan adoption and placement
4. Document adoption process completion

### Device Inventory Management
1. Use `get_protect_devices` to get camera inventory
2. Use `get_protect_sensors` for sensor inventory
3. Organize devices by type and location
4. Create inventory reports
5. Plan upgrade cycles based on age and performance

### System Monitoring
1. Use `get_protect_info` to check system status
2. Monitor system version and uptime
3. Track system health metrics
4. Plan maintenance windows
5. Verify backup status

## Example Questions

- "List all cameras in the system"
- "Show all sensors and their status"
- "What's the system version and status?"
- "Get specifications for all devices"
- "Create a device inventory report"
- "Plan a device upgrade strategy"

## Response Format

When using this skill, I provide:
- Device listings with MAC addresses and IP information
- Device specifications (model, firmware version)
- System status and version information
- Inventory organization by type/location
- Upgrade recommendations based on age/performance
- Hardware planning suggestions

## Best Practices

- Adopt devices in logical groups by location
- Maintain up-to-date device inventory
- Document device purpose and location
