---
name: ha-dashboard-cards
description: |
  Create Home Assistant Lovelace dashboard cards programmatically with static titles,
  color gradients, and section organization. Use when building HA dashboards with
  mini-graph-card showing multiple entities, adding color-coded thresholds to graphs,
  organizing dashboard sections with separators, or creating informational cards. Solves
  the dynamic title problem where mini-graph-card changes titles on hover. Triggers on
  "create HA dashboard", "mini-graph-card", "static graph titles", "color gradient graph",
  "dashboard cards", "bubble separator", "card_mod CSS". Works with Python dashboard
  builders and YAML Lovelace configurations.
---

# Home Assistant Dashboard Cards

## Quick Start

Create a mini-graph-card with multiple entities that keeps its title static:

```python
from ha_card_utils import add_static_title_to_mini_graph

card = {
    "type": "custom:mini-graph-card",
    "name": "Last 24 Hours",
    "hours_to_show": 24,
    "entities": [
        {"entity": "sensor.office_temperature", "name": "Office"},
        {"entity": "sensor.bedroom_temperature", "name": "Bedroom"},
    ],
}

add_static_title_to_mini_graph(card)
# Title now stays "Last 24 Hours" instead of changing to "Office"/"Bedroom" on hover
```

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. The Static Title Problem
4. Core Utilities
   4.1. Static Title Fix
   4.2. Color Gradients
   4.3. Section Separators
   4.4. Info Cards
5. Common Patterns
   5.1. Three-Graph Layout (1hr, 24hr, 1wk)
   5.2. Section Structure with Separators
   5.3. Sensor Sections with History
6. Color Scheme Presets
7. Supporting Files
8. Expected Outcomes
9. Requirements
10. Red Flags to Avoid

## 1. When to Use This Skill

### Explicit Triggers
- "Create HA dashboard cards"
- "Add mini-graph-card with static title"
- "Add color gradient to graph"
- "Create dashboard section with separator"
- "Fix mini-graph title changing on hover"

### Implicit Triggers
- Building Home Assistant dashboards programmatically
- Working with `custom:mini-graph-card` and multiple entities
- Creating sensor history graphs with time ranges
- Organizing dashboard sections visually
- Adding context/explanation cards to dashboards

### Problem Detection
- User reports mini-graph-card titles changing dynamically
- Dashboard needs visual thresholds (color-coded values)
- Need consistent section organization across dashboards
- Multiple graphs showing same data at different time ranges

## 2. What This Skill Does

This skill provides reusable utilities for creating Home Assistant Lovelace dashboard cards with:

1. **Static Titles** - Prevents mini-graph-card from changing titles on hover
2. **Color Gradients** - Adds threshold-based color coding to graphs
3. **Section Separators** - Creates visual section headers with icons
4. **Info Cards** - Adds informational cards with colored borders
5. **Common Patterns** - Implements standard layouts (3-graph rows, sensor sections)

All utilities are available in `ha_card_utils.py` and work with both Python dashboard builders and YAML configurations.

## 3. The Static Title Problem

### The Problem

When `custom:mini-graph-card` displays multiple entities, hovering over different sensor lines causes the card title to dynamically change to the entity name.

**Example:**
- Card title: "Last 24 Hours"
- Entities: Office (green), Bedroom (blue)
- Hover over Office line → title changes to "Office"
- Hover over Bedroom line → title changes to "Bedroom"

This is confusing because the title should indicate the time range, not which sensor is hovered.

### The Solution

Use `card_mod` with CSS to overlay static text using a `::after` pseudo-element and hide the dynamic title.

**CSS Pattern:**
```yaml
card_mod:
  style: |
    .header .name {
      visibility: visible !important;
    }
    .header .name::after {
      content: "Last 24 Hours" !important;
      visibility: visible !important;
    }
    .header .name > * {
      display: none !important;
    }
```

**How It Works:**
1. Keep header container visible
2. Inject static text via `::after` pseudo-element
3. Hide dynamic child elements with `display: none`

### Technical Deep Dive

See `references/static_title_technique.md` for complete CSS explanation, DOM structure analysis, and alternative approaches.

## 4. Core Utilities

### 4.1. Static Title Fix

**Function:** `add_static_title_to_mini_graph(card: dict) -> dict`

Forces mini-graph-card titles to remain static regardless of hover state.

**Usage:**
```python
from ha_card_utils import add_static_title_to_mini_graph

card = {
    "type": "custom:mini-graph-card",
    "name": "Last Hour",
    "hours_to_show": 1,
    "entities": [
        {"entity": "sensor.temperature", "name": "Office"},
    ],
}

add_static_title_to_mini_graph(card)
# Adds card_mod CSS to force static title
```

**When to Use:**
- Any mini-graph-card with multiple entities
- Time-range graphs (Last Hour, Last 24 Hours, Last Week)
- Comparison graphs showing multiple sensors

### 4.2. Color Gradients

**Function:** `add_color_gradient_to_mini_graph(card: dict, thresholds: list[dict]) -> dict`

Adds threshold-based color gradients to graphs for visual feedback.

**Usage:**
```python
from ha_card_utils import add_color_gradient_to_mini_graph

thresholds = [
    {"value": 0, "color": "#3498db"},    # Blue: Cold
    {"value": 20, "color": "#2ecc71"},   # Green: Comfortable
    {"value": 30, "color": "#e74c3c"},   # Red: Hot
]

add_color_gradient_to_mini_graph(card, thresholds)
```

**When to Use:**
- Temperature graphs (cold/comfortable/hot zones)
- Air quality sensors (good/moderate/poor ranges)
- Battery levels (full/medium/low/critical)
- Any sensor with meaningful value thresholds

**Note:** This removes fixed entity colors so the gradient can take effect.

### 4.3. Section Separators

**Function:** `create_bubble_separator(name: str, icon: str, enhanced: bool = False) -> dict`

Creates bubble-card separators for organizing dashboard sections.

**Usage:**
```python
from ha_card_utils import create_bubble_separator

# Standard separator
separator = create_bubble_separator("Temperature", "mdi:thermometer")

# Enhanced separator with gradient background
separator = create_bubble_separator(
    "Temperature",
    "mdi:thermometer",
    enhanced=True
)
```

**Enhanced Features:**
- Gradient background with spacing
- Larger font and bold text
- Thicker separator line

**When to Use:**
- Major section headers (enhanced=True)
- Sub-section labels (enhanced=False)
- Organizing related cards into groups

### 4.4. Info Cards

**Function:** `create_info_card(content: str, border_color: str, background_color: str | None = None) -> dict`

Creates markdown cards with colored borders for explanations and context.

**Usage:**
```python
from ha_card_utils import create_info_card

info = create_info_card(
    "**Lower resistance = more pollution.** Good air quality: >100 kΩ",
    "#e74c3c"  # Red border
)
```

**When to Use:**
- Explaining sensor readings
- Providing context for air quality/gas sensors
- Warning messages or alerts
- Instructions for manual controls

**Color Suggestions:**
- `#e74c3c` (Red) - Warnings, critical info
- `#f1c40f` (Yellow) - Cautions, tips
- `#3498db` (Blue) - Informational notes
- `#2ecc71` (Green) - Success, good status

## 5. Common Patterns

### 5.1. Three-Graph Layout (1hr, 24hr, 1wk)

Display the same sensor data at three time ranges in a horizontal row:

```python
from ha_card_utils import add_static_title_to_mini_graph

def create_three_graph_row(entity_id: str, entity_name: str):
    """Create 3 graphs showing 1 hour, 24 hours, and 1 week."""
    return {
        "type": "horizontal-stack",
        "cards": [
            add_static_title_to_mini_graph({
                "type": "custom:mini-graph-card",
                "name": "Last Hour",
                "hours_to_show": 1,
                "entities": [{"entity": entity_id, "name": entity_name}],
            }),
            add_static_title_to_mini_graph({
                "type": "custom:mini-graph-card",
                "name": "Last 24 Hours",
                "hours_to_show": 24,
                "entities": [{"entity": entity_id, "name": entity_name}],
            }),
            add_static_title_to_mini_graph({
                "type": "custom:mini-graph-card",
                "name": "Last Week",
                "hours_to_show": 168,  # 7 days × 24 hours
                "entities": [{"entity": entity_id, "name": entity_name}],
            }),
        ],
    }
```

**When to Use:**
- Comparing short-term vs long-term trends
- Temperature, humidity, air quality history
- Any sensor where time-range comparison is valuable

### 5.2. Section Structure with Separators

Organize dashboard sections with enhanced separators and sub-sections:

```python
from ha_card_utils import create_bubble_separator

section = {
    "type": "vertical-stack",
    "cards": [
        # Major section header
        create_bubble_separator("Temperature", "mdi:thermometer", enhanced=True),

        # Sub-section label
        {
            "type": "custom:bubble-card",
            "card_type": "separator",
            "name": "Current Readings",
            "icon": "mdi:home-thermometer",
        },

        # Sensor cards here...

        # Sub-section label
        {
            "type": "custom:bubble-card",
            "card_type": "separator",
            "name": "Temperature History",
            "icon": "mdi:chart-line",
        },

        # Graph row here...
    ],
}
```

**Structure Pattern:**
1. Enhanced separator (major section)
2. Sub-section separator (current readings)
3. Sensor cards (Mushroom template cards showing current values)
4. Sub-section separator (history)
5. Three-graph row (time-range comparison)

### 5.3. Sensor Sections with History

Complete sensor section combining current values, context, and history:

```python
from ha_card_utils import (
    create_bubble_separator,
    create_info_card,
    add_static_title_to_mini_graph,
    add_color_gradient_to_mini_graph,
    COLOR_SCHEMES,
)

def create_temperature_section(entities: list[dict]):
    """
    Create complete temperature section.

    Args:
        entities: List of dicts with keys:
            - entity_id: Entity ID (e.g., "sensor.office_temperature")
            - name: Display name (e.g., "Office")
            - color: Graph line color (e.g., "#2ecc71")
    """
    # Build temperature thresholds
    temp_thresholds = [
        COLOR_SCHEMES["temperature"]["cold"],
        COLOR_SCHEMES["temperature"]["comfortable"],
        COLOR_SCHEMES["temperature"]["warm"],
        COLOR_SCHEMES["temperature"]["hot"],
    ]

    # Build graph entities
    graph_entities = [
        {"entity": e["entity_id"], "name": e["name"], "color": e["color"]}
        for e in entities
    ]

    return {
        "type": "vertical-stack",
        "cards": [
            # Section header
            create_bubble_separator("Temperature", "mdi:thermometer", enhanced=True),

            # Current readings sub-section
            {
                "type": "custom:bubble-card",
                "card_type": "separator",
                "name": "Current Temperatures",
                "icon": "mdi:home-thermometer",
            },

            # Sensor cards (Mushroom template cards)
            # ... add current value cards here ...

            # History sub-section
            {
                "type": "custom:bubble-card",
                "card_type": "separator",
                "name": "Temperature History",
                "icon": "mdi:chart-line",
            },

            # Three-graph row with color gradients
            {
                "type": "horizontal-stack",
                "cards": [
                    add_color_gradient_to_mini_graph(
                        add_static_title_to_mini_graph({
                            "type": "custom:mini-graph-card",
                            "name": "Last Hour",
                            "hours_to_show": 1,
                            "entities": graph_entities,
                        }),
                        temp_thresholds
                    ),
                    add_color_gradient_to_mini_graph(
                        add_static_title_to_mini_graph({
                            "type": "custom:mini-graph-card",
                            "name": "Last 24 Hours",
                            "hours_to_show": 24,
                            "entities": graph_entities,
                        }),
                        temp_thresholds
                    ),
                    add_color_gradient_to_mini_graph(
                        add_static_title_to_mini_graph({
                            "type": "custom:mini-graph-card",
                            "name": "Last Week",
                            "hours_to_show": 168,
                            "entities": graph_entities,
                        }),
                        temp_thresholds
                    ),
                ],
            },
        ],
    }
```

## 6. Color Scheme Presets

The `COLOR_SCHEMES` dict provides preset thresholds for common sensor types:

### Temperature

```python
from ha_card_utils import COLOR_SCHEMES

temp_thresholds = [
    COLOR_SCHEMES["temperature"]["cold"],         # 10°C → Blue
    COLOR_SCHEMES["temperature"]["comfortable"],  # 18°C → Green
    COLOR_SCHEMES["temperature"]["warm"],         # 26°C → Yellow
    COLOR_SCHEMES["temperature"]["hot"],          # 32°C → Red
]
```

### Humidity

```python
humidity_thresholds = [
    COLOR_SCHEMES["humidity"]["dry"],          # 0% → Red
    COLOR_SCHEMES["humidity"]["low"],          # 30% → Green
    COLOR_SCHEMES["humidity"]["comfortable"],  # 60% → Yellow
    COLOR_SCHEMES["humidity"]["high"],         # 80% → Red
]
```

### Air Quality (Oxidising/Reducing Gas)

```python
# Oxidising gas (lower resistance = more pollution)
oxidising_thresholds = [
    COLOR_SCHEMES["air_quality"]["oxidising"]["poor"],       # 0 kΩ → Red
    COLOR_SCHEMES["air_quality"]["oxidising"]["moderate"],   # 10 kΩ → Orange
    COLOR_SCHEMES["air_quality"]["oxidising"]["good"],       # 30 kΩ → Green
    COLOR_SCHEMES["air_quality"]["oxidising"]["excellent"],  # 100 kΩ → Blue
]

# Reducing gas
reducing_thresholds = [
    COLOR_SCHEMES["air_quality"]["reducing"]["poor"],       # 0 kΩ → Red
    COLOR_SCHEMES["air_quality"]["reducing"]["moderate"],   # 100 kΩ → Orange
    COLOR_SCHEMES["air_quality"]["reducing"]["good"],       # 200 kΩ → Green
    COLOR_SCHEMES["air_quality"]["reducing"]["excellent"],  # 500 kΩ → Blue
]
```

**Customizing Thresholds:**

```python
# Override preset values
custom_temp_thresholds = [
    {"value": 15, "color": "#3498db"},   # Cold
    {"value": 22, "color": "#2ecc71"},   # Comfortable
    {"value": 28, "color": "#e74c3c"},   # Hot
]
```

## 7. Supporting Files

- **`references/static_title_technique.md`** - Complete technical reference for card_mod CSS technique, DOM structure analysis, and alternative approaches
- **`references/color_gradients.md`** - Color threshold guide with visual examples and color palette recommendations
- **`examples/complete_sections.py`** - Full examples of temperature, humidity, and air quality sections
- **`examples/yaml_examples.yaml`** - YAML equivalents for manual dashboard editing
- **`scripts/apply_static_titles.py`** - Batch script to apply static titles to existing dashboards

## 8. Expected Outcomes

### Successful Card Creation

```
✓ Static Title Applied
  Card: "Last 24 Hours"
  Has card_mod: True
  CSS injected: .header .name::after

✓ Color Gradient Applied
  Thresholds: 4 levels (Cold/Comfortable/Warm/Hot)
  Entity colors removed: True
  Gradient active: True

✓ Section Created
  Cards: 8 (separator, sub-headers, sensors, graphs)
  Three-graph row: 1hr, 24hr, 1wk
  All titles static: True
```

### Common Issues

**Issue: Title still changes on hover**
- Cause: card-mod not installed or card_mod syntax error
- Fix: Install card-mod via HACS, check CSS quotes/braces

**Issue: Color gradient not visible**
- Cause: Entity colors override gradient
- Fix: `add_color_gradient_to_mini_graph()` removes entity colors automatically

**Issue: Separator not showing gradient**
- Cause: Using `enhanced=False` or card-mod not applied
- Fix: Use `create_bubble_separator(name, icon, enhanced=True)`

## 9. Requirements

### HACS Custom Cards

- **card-mod** - Required for CSS styling and static titles
- **mini-graph-card** - Compact graph visualization
- **bubble-card** - Section separators and buttons
- **mushroom** - Modern entity cards (optional, for current readings)

### Python Dependencies

- `websocket-client` - For WebSocket API communication
- Python 3.10+ - For type hints and dict syntax

### Home Assistant

- Version 2023.5+ recommended
- Lovelace dashboards enabled
- Long-lived access token configured

### Project Files

- `ha_card_utils.py` - Core utilities module
  - **Skill copy:** Available in this skill directory (`~/.claude/skills/ha-dashboard-cards/ha_card_utils.py`)
  - **Project copy:** Original in HA project (`~/projects/play/ha/ha_card_utils.py`)
  - Can be imported directly if working in the HA project, or copy to your project directory
- `CLAUDE.md` - Project configuration with HA instance details (in HA project)

## 10. Red Flags to Avoid

1. **Not using static titles on multi-entity graphs** - Always apply `add_static_title_to_mini_graph()` when showing multiple entities
2. **Hardcoding card_mod CSS** - Use utility functions instead of copy-pasting CSS
3. **Missing card-mod installation** - Verify card-mod is installed before using utilities
4. **Entity colors override gradients** - Remove entity colors when using color_thresholds
5. **Inconsistent section structure** - Follow the pattern: enhanced separator → sub-section → cards → sub-section → graphs
6. **Wrong time ranges** - Use 1/24/168 hours for consistent time-range comparisons
7. **Missing info cards** - Add context for air quality sensors and complex readings
8. **No color gradients on sensor graphs** - Use thresholds for visual feedback on temperature/humidity/air quality
9. **Not using preset color schemes** - Use `COLOR_SCHEMES` for consistency across dashboards
10. **Forgetting to import utilities** - Always `from ha_card_utils import ...` at top of file

## Notes

- **CSS Escaping:** When using card_mod in Python, use `{{` and `}}` to escape braces in f-strings
- **Title Synchronization:** The `content` value in card_mod must match the `name` value for consistency
- **Performance:** CSS overlays have negligible performance impact
- **YAML Compatibility:** All utilities work with YAML by copying the generated card_mod structure
- **Dashboard Builder Pattern:** Use `dashboard_builder.py` as the single source of truth for programmatically managed dashboards
- **Standalone Dashboards:** Complex multi-view dashboards (Irrigation, Solar) can be managed directly in HA UI
- **Testing:** Test card changes in a separate dashboard before applying to production dashboards
- **Version Control:** Commit `ha_card_utils.py` and dashboard builders to git for reproducibility

**Applied Successfully:**
- Enviro+ dashboard (15 mini-graph cards with static titles)
- Temperature/Humidity/Air Quality sections with color gradients
- Enhanced separators for major sections
- Info cards explaining gas sensor readings

**Dashboard URL:** `http://192.168.68.123:8123/enviro-plus/new-panel`
