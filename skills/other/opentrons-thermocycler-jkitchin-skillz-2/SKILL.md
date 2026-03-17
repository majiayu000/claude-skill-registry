---
name: opentrons-thermocycler
description: Opentrons Thermocycler Module - automated PCR thermal cycling with independent block (4-99°C) and lid (37-110°C) temperature control, profile execution, and auto-sealing lid support (GEN2) for high-throughput molecular biology workflows
allowed-tools: ["*"]
---

# Opentrons Thermocycler Module

## Overview

The **Opentrons Thermocycler Module** automates PCR thermal cycling with precise, independent control of block temperature (4-99°C) and heated lid (37-110°C). Execute complex temperature profiles with automatic cycling, integrate with liquid handling for complete PCR setup automation, and use auto-sealing lids (GEN2) for walk-away workflows.

**Core value:** Fully automate PCR setup and cycling. Load samples, dispense reagents, seal plates (GEN2), run thermal profiles, and collect products—all without manual intervention.

## When to Use

Use the Thermocycler skill when:
- Running PCR amplification protocols
- Performing qPCR or RT-PCR reactions
- Automating DNA/RNA thermal cycling workflows
- Executing multi-step temperature incubations
- Integrating thermal cycling with automated liquid handling
- Setting up high-throughput PCR screening

**Don't use when:**
- Simple temperature control needed (use Temperature Module for 4-95°C range)
- Shaking/mixing required during incubation (use Heater-Shaker Module)
- Temperature outside 4-99°C range (block) or 37-110°C (lid)

## Quick Reference

| Operation | Method | Key Parameters |
|-----------|--------|----------------|
| Load module | `protocol.load_module()` | `"thermocyclerModuleV2"` or `"thermocyclerModuleV1"` |
| Open lid | `open_lid()` | - |
| Close lid | `close_lid()` | - |
| Set lid temperature | `set_lid_temperature()` | celsius (37-110) |
| Deactivate lid | `deactivate_lid()` | - |
| Set block temperature | `set_block_temperature()` | celsius (4-99), hold_time, block_max_volume |
| Execute profile | `execute_profile()` | steps, repetitions, block_max_volume |
| Deactivate block | `deactivate_block()` | - |

## Platform Compatibility

**Both Opentrons Flex and OT-2**

### Module Generations
- **GEN1** - Original thermocycler, compatible with both platforms
- **GEN2** - Improved plate lift mechanism, auto-sealing lid support

**API compatibility:** Both generations support identical API methods

### Deck Position

**OT-2:** Spans multiple deck slots (typically slots 7, 8, 10, 11)

**Flex:** Dedicated thermocycler position

**Loading:**
```python
# No deck slot specified - thermocycler has fixed position
tc_mod = protocol.load_module("thermocyclerModuleV2")
```

## Loading the Module

```python
from opentrons import protocol_api

metadata = {'apiLevel': '2.19'}

def run(protocol: protocol_api.ProtocolContext):
    # Load Thermocycler Module (no location - fixed position)
    tc_mod = protocol.load_module("thermocyclerModuleV2")

    # Load PCR plate
    pcr_plate = tc_mod.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")
```

**Module versions:**
- `"thermocyclerModuleV1"` - GEN1
- `"thermocyclerModuleV2"` - GEN2 (recommended)

## Lid Control

### Basic Lid Operations

```python
# Open lid for pipette access
tc_mod.open_lid()

# Close lid for thermal cycling
tc_mod.close_lid()
```

**Important for gripper (Flex):**
- **Always open lid before gripper operations**
- Close lid only after plate is seated on thermocycler

### Heated Lid

The heated lid prevents condensation during thermal cycling:

```python
# Set lid temperature (blocks until reached)
tc_mod.set_lid_temperature(celsius=105)

# Run thermal profile
# ... cycling ...

# Turn off lid heater
tc_mod.deactivate_lid()
```

**Lid temperature range:** 37-110°C

**Typical settings:**
- **Standard PCR:** 105°C
- **RT-PCR:** 100-105°C
- **Custom protocols:** Match or exceed highest block temperature + 5-10°C

**Note:** Lid temperature is independent of block temperature and profiles.

## Block Temperature Control

### Basic Block Temperature

```python
# Set block temperature and wait
tc_mod.set_block_temperature(
    temperature=95,
    hold_time_seconds=180,  # Hold for 3 minutes
    block_max_volume=50     # Volume in wells (µL)
)

# Block automatically maintains temperature for hold_time
```

**Block temperature range:** 4-99°C

**Parameters:**
- `temperature` - Target temperature in °C (required)
- `hold_time_seconds` - Duration to hold at temperature
- `hold_time_minutes` - Alternative duration in minutes
- `block_max_volume` - Sample volume in µL (default: 25µL)

### Hold Time Behavior

**With hold_time:** Protocol waits at temperature for specified duration

```python
# Wait 5 minutes at 95°C
tc_mod.set_block_temperature(
    temperature=95,
    hold_time_minutes=5,
    block_max_volume=50
)
# Protocol continues after 5 minutes
```

**Without hold_time:** Set temperature and continue immediately

```python
# Set to 4°C and proceed (no hold)
tc_mod.set_block_temperature(temperature=4)

# Can perform other operations while maintaining 4°C
```

### Block Max Volume

Specify sample volume for improved temperature accuracy:

```python
# 50µL reactions
tc_mod.set_block_temperature(
    temperature=72,
    hold_time_minutes=10,
    block_max_volume=50  # Optimizes heating/cooling for 50µL
)
```

**Default:** 25µL if not specified

**Why it matters:** Algorithm adjusts for thermal mass of liquid to ensure accurate sample temperature.

## Temperature Profiles

Automate repeated temperature cycles for PCR:

### Defining a Profile

```python
# PCR profile: Denature → Anneal → Extend
pcr_profile = [
    {"temperature": 95, "hold_time_seconds": 30},  # Denaturation
    {"temperature": 57, "hold_time_seconds": 30},  # Annealing
    {"temperature": 72, "hold_time_seconds": 60}   # Extension
]
```

**Profile structure:** List of dictionaries with `temperature` and `hold_time_seconds`

### Executing a Profile

```python
# Run profile for 30 cycles
tc_mod.execute_profile(
    steps=pcr_profile,
    repetitions=30,
    block_max_volume=50
)
```

**Parameters:**
- `steps` - List of temperature steps (required)
- `repetitions` - Number of times to repeat profile (required)
- `block_max_volume` - Sample volume in µL

### Complete PCR Protocol

```python
# Setup
tc_mod = protocol.load_module("thermocyclerModuleV2")
pcr_plate = tc_mod.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")

# Open lid for loading
tc_mod.open_lid()

# Pipette PCR reagents (not shown)
# ... add template, primers, polymerase, etc. ...

# Close lid and set lid temperature
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)

# Initial denaturation
tc_mod.set_block_temperature(
    temperature=95,
    hold_time_seconds=180,  # 3 minutes
    block_max_volume=50
)

# PCR cycling
pcr_profile = [
    {"temperature": 95, "hold_time_seconds": 30},
    {"temperature": 57, "hold_time_seconds": 30},
    {"temperature": 72, "hold_time_seconds": 60}
]

tc_mod.execute_profile(steps=pcr_profile, repetitions=30, block_max_volume=50)

# Final extension
tc_mod.set_block_temperature(
    temperature=72,
    hold_time_minutes=5,
    block_max_volume=50
)

# Hold at 4°C
tc_mod.set_block_temperature(temperature=4)

# Cleanup
tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

## Auto-Sealing Lids (GEN2)

**Opentrons Flex GEN2 Thermocycler** supports auto-sealing lids for walk-away protocols:

### Auto-Sealing Lid Labware

```python
# Load auto-sealing lid and riser
auto_seal_lid = protocol.load_labware(
    "opentrons_tough_pcr_auto_sealing_lid",
    location="lid_stack_location"
)

riser = protocol.load_labware(
    "opentrons_flex_deck_riser",
    location="deck_location"
)
```

### Lid Stack Management

```python
# Stack up to 5 auto-sealing lids
lid_stack = tc_mod.load_lid_stack(
    "opentrons_tough_pcr_auto_sealing_lid",
    quantity=5
)

# Move lid with gripper
protocol.move_lid(
    lid=lid_stack,
    new_location=pcr_plate,
    use_gripper=True
)
```

**Important:** Do not affix rubber seal to internal Thermocycler lid when using auto-sealing lids.

### Complete Workflow with Auto-Sealing

```python
# Load module and labware
tc_mod = protocol.load_module("thermocyclerModuleV2")
pcr_plate = tc_mod.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")

# Load auto-sealing lids
lid_stack = tc_mod.load_lid_stack(
    "opentrons_tough_pcr_auto_sealing_lid",
    quantity=3
)

# Setup samples
tc_mod.open_lid()
# ... pipette reagents ...

# Apply auto-sealing lid with gripper
protocol.move_lid(lid_stack, pcr_plate, use_gripper=True)

# Close thermocycler lid
tc_mod.close_lid()

# Run PCR
# ... thermal cycling ...

# Open for retrieval
tc_mod.open_lid()
```

## Common Patterns

### Standard PCR

```python
# Standard Taq PCR protocol
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)

# Initial denaturation
tc_mod.set_block_temperature(95, hold_time_minutes=3, block_max_volume=50)

# Cycling
standard_pcr = [
    {"temperature": 95, "hold_time_seconds": 30},
    {"temperature": 55, "hold_time_seconds": 30},
    {"temperature": 72, "hold_time_seconds": 60}
]
tc_mod.execute_profile(steps=standard_pcr, repetitions=35, block_max_volume=50)

# Final extension
tc_mod.set_block_temperature(72, hold_time_minutes=10, block_max_volume=50)

# Hold at 4°C
tc_mod.set_block_temperature(4)

tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

### Gradient PCR (Multiple Annealing Temperatures)

```python
# Test multiple annealing temperatures in columns
annealing_temps = [52, 54, 56, 58, 60, 62, 64, 66]  # 8 temperatures

for i, temp in enumerate(annealing_temps):
    protocol.comment(f"Column {i+1}: {temp}°C annealing")

    # Pipette samples into column (example)
    # pipette.transfer(50, master_mix, pcr_plate.columns()[i])

    # Run gradient PCR for this column
    gradient_profile = [
        {"temperature": 95, "hold_time_seconds": 30},
        {"temperature": temp, "hold_time_seconds": 30},  # Variable annealing
        {"temperature": 72, "hold_time_seconds": 60}
    ]

    tc_mod.execute_profile(steps=gradient_profile, repetitions=30, block_max_volume=50)
```

**Note:** This example is simplified. True gradient PCR requires hardware that supports simultaneous temperature gradients across the block.

### Two-Step PCR (No Extension)

```python
# Two-step PCR (denature + anneal/extend combined)
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)

tc_mod.set_block_temperature(95, hold_time_minutes=3, block_max_volume=25)

two_step = [
    {"temperature": 95, "hold_time_seconds": 15},
    {"temperature": 60, "hold_time_seconds": 60}  # Combined anneal/extend
]

tc_mod.execute_profile(steps=two_step, repetitions=40, block_max_volume=25)

tc_mod.set_block_temperature(4)
tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

### RT-PCR (Reverse Transcription + PCR)

```python
# Reverse transcription + PCR
tc_mod.close_lid()
tc_mod.set_lid_temperature(100)

# Reverse transcription
tc_mod.set_block_temperature(42, hold_time_minutes=30, block_max_volume=20)

# RT inactivation
tc_mod.set_block_temperature(85, hold_time_minutes=5, block_max_volume=20)

# Cool for PCR enzyme addition (if needed)
tc_mod.set_block_temperature(4)
tc_mod.open_lid()

# Add PCR enzymes
# pipette.transfer(...)

tc_mod.close_lid()
tc_mod.set_lid_temperature(105)

# PCR cycling
tc_mod.set_block_temperature(95, hold_time_minutes=2, block_max_volume=25)

rt_pcr_profile = [
    {"temperature": 95, "hold_time_seconds": 15},
    {"temperature": 60, "hold_time_seconds": 30},
    {"temperature": 72, "hold_time_seconds": 30}
]

tc_mod.execute_profile(steps=rt_pcr_profile, repetitions=40, block_max_volume=25)

tc_mod.set_block_temperature(4)
tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

### Touchdown PCR

```python
# Touchdown PCR - decreasing annealing temperature
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)
tc_mod.set_block_temperature(95, hold_time_minutes=3, block_max_volume=50)

# High stringency cycles (65°C → 55°C, -1°C per cycle)
for temp in range(65, 54, -1):
    touchdown_profile = [
        {"temperature": 95, "hold_time_seconds": 30},
        {"temperature": temp, "hold_time_seconds": 30},
        {"temperature": 72, "hold_time_seconds": 60}
    ]
    tc_mod.execute_profile(steps=touchdown_profile, repetitions=1, block_max_volume=50)

# Lower stringency cycles (55°C for remaining)
standard_profile = [
    {"temperature": 95, "hold_time_seconds": 30},
    {"temperature": 55, "hold_time_seconds": 30},
    {"temperature": 72, "hold_time_seconds": 60}
]
tc_mod.execute_profile(steps=standard_profile, repetitions=25, block_max_volume=50)

tc_mod.set_block_temperature(72, hold_time_minutes=10, block_max_volume=50)
tc_mod.set_block_temperature(4)
tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

## Integration with Liquid Handling

### Automated PCR Setup

```python
# Complete automated PCR setup
tc_mod = protocol.load_module("thermocyclerModuleV2")
pcr_plate = tc_mod.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt")
pipette = protocol.load_instrument("flex_1channel_1000", "left")

# Reagents
master_mix = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "C1")
template_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "C2")

# Open thermocycler
tc_mod.open_lid()

# Distribute master mix
pipette.distribute(
    volume=45,
    source=master_mix["A1"],
    dest=pcr_plate.wells(),
    new_tip="once"
)

# Add template DNA
pipette.transfer(
    volume=5,
    source=template_plate.wells(),
    dest=pcr_plate.wells(),
    mix_after=(3, 25),
    new_tip="always"
)

# Run PCR
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)
tc_mod.set_block_temperature(95, hold_time_minutes=3, block_max_volume=50)

pcr_profile = [
    {"temperature": 95, "hold_time_seconds": 30},
    {"temperature": 58, "hold_time_seconds": 30},
    {"temperature": 72, "hold_time_seconds": 60}
]

tc_mod.execute_profile(steps=pcr_profile, repetitions=30, block_max_volume=50)
tc_mod.set_block_temperature(72, hold_time_minutes=5, block_max_volume=50)
tc_mod.set_block_temperature(4)

tc_mod.deactivate_lid()
tc_mod.deactivate_block()
tc_mod.open_lid()
```

### Integration with Gripper (Flex)

```python
# Prepare samples off-deck, move to thermocycler
sample_plate = protocol.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt", "C2")

# Setup samples
# ... pipetting ...

# Move to thermocycler with gripper
tc_mod.open_lid()
protocol.move_labware(sample_plate, tc_mod, use_gripper=True)

# Run PCR
tc_mod.close_lid()
# ... thermal cycling ...

# Retrieve plate
tc_mod.open_lid()
protocol.move_labware(sample_plate, "C2", use_gripper=True)
```

## GEN2 Improvements

**Plate lift mechanism:**
- Press button for 3 seconds with lid open to activate
- Raises plate for easier manual or gripper removal
- Improves plate access and prevents damage

**Auto-sealing lid support:**
- Use Opentrons Tough PCR Auto-sealing Lids
- Stack up to 5 lids
- Automated lid placement with gripper

## Best Practices

1. **Set lid temperature before cycling** - Prevents condensation
2. **Use block_max_volume parameter** - Improves temperature accuracy
3. **Deactivate block and lid at protocol end** - Prevents equipment running indefinitely
4. **Open lid before gripper operations** - Required for plate movement
5. **Use profiles for repeated cycles** - More efficient than individual set_block_temperature calls
6. **Cool to 4°C at end** - Preserves samples until retrieval
7. **Plan for thermal equilibration** - Allow extra time for large temperature changes
8. **Test profiles with simulation** - Verify timing before running on hardware
9. **Document profile parameters** - Include reasoning in protocol comments
10. **Consider enzyme specifications** - Match temperatures to polymerase requirements

## Common Mistakes

**❌ Not setting lid temperature:**
```python
tc_mod.close_lid()
tc_mod.execute_profile(...)  # Condensation risk - no lid heating
```

**✅ Correct:**
```python
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)
tc_mod.execute_profile(...)
```

**❌ Gripper movement with closed lid:**
```python
protocol.move_labware(plate, tc_mod, use_gripper=True)  # Error: lid closed
```

**✅ Correct:**
```python
tc_mod.open_lid()
protocol.move_labware(plate, tc_mod, use_gripper=True)
```

**❌ Not deactivating modules:**
```python
tc_mod.execute_profile(...)
# Protocol ends - thermocycler still heating!
```

**✅ Correct:**
```python
tc_mod.execute_profile(...)
tc_mod.deactivate_lid()
tc_mod.deactivate_block()
```

**❌ Wrong profile structure:**
```python
# Missing hold_time_seconds
bad_profile = [
    {"temperature": 95},
    {"temperature": 55}
]
tc_mod.execute_profile(steps=bad_profile, repetitions=30)  # Error
```

**✅ Correct:**
```python
good_profile = [
    {"temperature": 95, "hold_time_seconds": 30},
    {"temperature": 55, "hold_time_seconds": 30}
]
tc_mod.execute_profile(steps=good_profile, repetitions=30)
```

## Troubleshooting

**Module not reaching temperature:**
- Verify temperature is within range (4-99°C block, 37-110°C lid)
- Check ambient temperature for low-temp targets
- Allow sufficient time for thermal equilibration

**Condensation in wells:**
- Ensure lid temperature is set and reached before cycling
- Set lid temperature ≥ highest block temperature + 5-10°C
- Verify lid is properly closed

**Profile not executing:**
- Check profile structure (list of dicts with temperature and hold_time_seconds)
- Verify repetitions parameter is provided
- Ensure block_max_volume matches sample volume

**Plate removal difficulty (GEN1):**
- Wait for block to cool below 60°C
- Use plate lift mechanism (GEN2)
- Ensure lid is fully open

**Gripper errors:**
- Verify lid is open before movement
- Check plate is compatible PCR labware
- Ensure thermocycler position is clear

## Integration with Other Modules

### With Temperature Module (Pre-cooling)

```python
temp_mod = protocol.load_module("temperature module gen2", "D1")
tc_mod = protocol.load_module("thermocyclerModuleV2")

# Pre-cool samples on temperature module
temp_mod.set_temperature(4)
protocol.move_labware(sample_plate, temp_mod, use_gripper=True)
protocol.delay(minutes=5)

# Transfer to thermocycler
tc_mod.open_lid()
protocol.move_labware(sample_plate, tc_mod, use_gripper=True)

# Run PCR
tc_mod.close_lid()
# ... thermal cycling ...
```

### With Magnetic Module (PCR Cleanup)

```python
# After PCR, perform magnetic bead cleanup
tc_mod.set_block_temperature(4)
tc_mod.open_lid()

mag_block = protocol.load_module("magneticBlockV1", "D2")

# Move PCR product to magnetic block
protocol.move_labware(pcr_plate, mag_block, use_gripper=True)

# Cleanup workflow
# ... magnetic bead purification ...
```

## API Version Requirements

- **Minimum API version:** 2.0 (thermocycler support)
- **GEN2 features:** API 2.13+
- **Auto-sealing lids:** API 2.15+
- **Recommended:** 2.19+ for full feature support

## Additional Resources

- **Thermocycler Documentation:** https://docs.opentrons.com/v2/modules/thermocycler.html
- **PCR Protocol Library:** https://protocols.opentrons.com/
- **Opentrons Support:** https://support.opentrons.com/

## Related Skills

- `opentrons` - Main Opentrons Python API skill
- `opentrons-temperature-module` - Simple temperature control (4-95°C)
- `opentrons-gripper` - Automated labware movement (Flex)
- `opentrons-magnetic-block` - Magnetic bead separation for PCR cleanup
