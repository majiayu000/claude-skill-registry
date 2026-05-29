---
name: recipe-builder
description: Create and manage WaveCap-SDR recipe templates for common capture scenarios. Use when setting up new band plans, creating presets for trunking systems, or building reusable multi-channel configurations for marine/aviation/broadcast monitoring.
---

# Recipe Builder for WaveCap-SDR

This skill helps create recipe templates in `backend/config/wavecapsdr.yaml` for common SDR monitoring scenarios.

## When to Use This Skill

Use this skill when:
- Setting up multi-channel monitoring (VHF marine, aviation, etc.)
- Creating band plans for specific services
- Building reusable configurations
- Documenting common frequency setups
- Sharing configurations with team

## Recipe Structure

Recipes define capture + channels in YAML:

```yaml
recipes:
  my_recipe:
    name: "My Recipe"
    description: "Description of what this monitors"
    capture:
      center_hz: 156800000  # 156.8 MHz
      sample_rate: 250000    # 250 kHz
      bandwidth: 250000
      gain_db: 30
    channels:
      - name: "Channel 16"
        offset_hz: 0
        mode: "fm"
      - name: "Channel 9"
        offset_hz: -250000
        mode: "fm"
```

## Common Recipe Templates

### VHF Marine

```yaml
recipes:
  marine_vhf:
    name: "VHF Marine"
    description: "VHF marine channels 16, 9, 6"
    capture:
      center_hz: 156800000  # Ch 16
      sample_rate: 250000
      gain_db: 35
    channels:
      - {name: "Ch 16 - Distress", offset_hz: 0, mode: "fm"}
      - {name: "Ch 9 - Calling", offset_hz: -250000, mode: "fm"}
      - {name: "Ch 6 - Safety", offset_hz: -500000, mode: "fm"}
```

### FM Broadcast

```yaml
recipes:
  fm_broadcast:
    name: "FM Broadcast"
    description: "Local FM radio stations"
    capture:
      center_hz: 98000000
      sample_rate: 2000000
      gain_db: 30
    channels:
      - {name: "KEXP 90.3", offset_hz: -7700000, mode: "wbfm"}
      - {name: "KUOW 94.9", offset_hz: -3100000, mode: "wbfm"}
      - {name: "KNHC 89.5", offset_hz: -8500000, mode: "wbfm"}
```

## Usage

Run the recipe builder script:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/recipe-builder/create_recipe.py \
  --name my_recipe \
  --center 156.8e6 \
  --sample-rate 250000 \
  --channels "Ch 16:0" "Ch 9:-250000"
```

This generates YAML to add to config.
