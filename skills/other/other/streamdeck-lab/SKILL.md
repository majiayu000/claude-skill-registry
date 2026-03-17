---
name: streamdeck-lab
description: >
  Iterate, evaluate, generate dynamic pages, and push context-aware layouts to Stream Deck.
triggers:
  - streamdeck lab
  - evaluate layout
  - test streamdeck page
  - promote layout
  - generate streamdeck page
  - push streamdeck layout
  - mutate streamdeck page
provides:
  - streamdeck-evaluation
  - streamdeck-generation
  - streamdeck-push
composes: [, task-monitor]
---

# /streamdeck-lab

Iterate, evaluate, generate dynamic pages, and push context-aware layouts to Stream Deck.

## Triggers
- `streamdeck lab`
- `evaluate layout`
- `test streamdeck page`
- `promote layout`
- `generate streamdeck page`
- `push streamdeck layout`
- `mutate streamdeck page`

## Usage

### Static Evaluation
```
/streamdeck-lab evaluate --template sentinel_hud
/streamdeck-lab evaluate-all
/streamdeck-lab promote --template compliance_dashboard
```

### Dynamic Page Generation (Chaotic Environments)
```
/streamdeck-lab generate --context sentinel_hud --events missile_warning,fuel_bingo
/streamdeck-lab mutate --template sentinel_hud --event threat_popup
/streamdeck-lab push --context sentinel_hud --events mode_a2a --page 10
/streamdeck-lab events --context sentinel_hud
```

## What It Does

### Evaluate (Static)
1. Loads a page template from `config/page_templates/`
2. Evaluates against ground truth test cases in `ground_truth/contexts.json`
3. Scores on: workflow coverage (40%), icon appropriateness (20%), navigation (15%), layout density (15%), palette compliance (10%)
4. Reports command wiring and information hierarchy presence

### Generate (Dynamic)
1. Takes a context identifier and list of active events
2. Loads the base template for that context
3. Applies event mutations (inject buttons, modify text, mode switch)
4. Returns the mutated page layout with mutation log
5. Supports MIL-STD-411F alert tiers: CRITICAL (flash), WARNING, ADVISORY

### Push (Deploy)
1. Generates a dynamic page (as above)
2. Converts to ButtonDef objects
3. Pushes to Stream Deck via `build_page` socket command
4. Auto-navigates to the page (unless --no-navigate)

### Mutate (Single Event)
1. Apply one event to an existing template
2. Returns the mutated layout for inspection before pushing

## Event Catalog

### SENTINEL Events
| Event | Alert Tier | Description |
|-------|-----------|-------------|
| `missile_warning` | CRITICAL | Inbound missile — flash button, requires ACK |
| `fuel_bingo` | WARNING | Fuel below bingo level |
| `comms_degraded` | ADVISORY | Communications degraded |
| `threat_popup` | WARNING | New hostile contact detected |
| `mode_a2a` | - | Switch to air-to-air combat mode |
| `mode_a2g` | - | Switch to air-to-ground mode |
| `mode_nav` | - | Switch to navigation mode |

### Compliance Events
| Event | Alert Tier | Description |
|-------|-----------|-------------|
| `drift_detected` | WARNING | Compliance drift detected |
| `cui_violation` | CRITICAL | CUI marking violation |

### F36 Plant Events
| Event | Alert Tier | Description |
|-------|-----------|-------------|
| `test_failure` | WARNING | Multiple test failures |
| `qa_hold` | CRITICAL | QA hold — production line stop |

## MIL-STD Information Hierarchy
Templates now encode information priority per MIL-STD-1472:
- **PRIMARY** (Row 1): Critical flight/safety data, scanned first
- **SECONDARY** (Row 2): Tactical awareness, weapons, subsystems
- **TERTIARY** (Row 3): Navigation, diagnostics, support

## Dependencies
- `config/page_templates/` (page_memory)
- `config/icon_manifest.yaml` (icon manifest)
- `streamdeck.widgets.nvis_base` (NVIS palette constants)
- `streamdeck.utils.page_builder` (build_page, push_page)
