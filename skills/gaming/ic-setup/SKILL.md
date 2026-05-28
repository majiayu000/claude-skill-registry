---
name: ic-setup
description: Generate hardware setup and wiring instructions for IC10 code. Use when user wants to know how to physically connect devices to use their IC10 scripts.
---

# IC10 Hardware Setup

Generate complete hardware setup instructions including device connections, wiring diagrams, power requirements, and installation steps.

## Workflow

### 1. Analysis Phase
Use Task tool to spawn:
- `code-analyzer` - Extract device information from code

### 2. Hardware Guide Generation Phase
Use Task tool to spawn:
- `hardware-guide` - Create complete setup instructions with diagrams

## What You Get

A complete hardware guide including:

### Device Connection Table
- IC port mappings (d0-d5)
- Device types and purposes
- Required connections (logic cables, power, pipes, etc.)

### Wiring Diagrams
- ASCII art showing physical layout
- Logic cable connections
- Power network topology
- Atmosphere/hydraulic routing (if applicable)

### Power Requirements
- Total power calculation
- Peak vs average consumption
- Recommended power source (battery/generator/APC)

### Installation Steps
- Device placement recommendations
- Connection procedures
- Testing checklist
- Troubleshooting tips

### Safety Notes
- Pressure system warnings
- Power handling precautions
- Rocket launch safety

## Instructions

When user asks for hardware setup:

1. **Review the IC10 code**
   - Identify all devices used (d0-d5, db)
   - Check for device comments
   - Note any special requirements

2. **Launch code-analyzer** to extract device info
3. **Launch hardware-guide** to create setup instructions
4. **Present the complete guide** including:
   - Visual diagrams
   - Connection table
   - Power requirements
   - Installation steps

## Example Triggers

- "How do I wire this up?"
- "What devices do I need?"
- "Show me the setup"
- "Installation instructions"
- "Hardware guide for this code"
- "Physical connections"
- "How do I connect..."

## Output Format

After setup guide is generated, present:

```markdown
## Hardware Setup: [Script Name]

### Quick Summary

**Devices Needed**: X devices (list)
**Total Power**: XW (peak)
**Difficulty**: Beginner/Intermediate/Advanced

---

### Device Connections

| IC Port | Device | Connections Required |
|-----------|--------|-------------------|
| d0 | Gas Sensor | Logic cable + Power |
| d1 | Active Vent | Logic cable + Power + Atmos pipe |
...

### Wiring Diagram

```
[ASCII diagram showing physical setup]
```

### Power Analysis

| Device | Power Draw | Notes |
|---------|------------|--------|
| IC Housing | 10W | Always on |
| Gas Sensor | 5W | ... |
... | ... | ... |
| **Total** | **XXW** | Peak: XXW, Avg: XXW |

**Power Source**: Battery ≥ XXXW or Generator

### Installation Steps

#### Step 1: Device Placement
[ ] Place IC Housing...
[ ] Place Gas Sensor...
...

#### Step 2: Logic Connections
[ ] Connect Gas Sensor to IC d0...
...

#### Step 3: Power Connections
[ ] Power IC Housing...
...

#### Step 4: Test
[ ] Load script...
[ ] Test operation...
```

## Notes

- Setup guide is based on code analysis
- In-game testing recommended to verify all connections work
- Power calculations are estimates (actual may vary)
- Some scripts may require additional devices not in code (e.g., APC for power distribution)
