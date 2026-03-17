---
name: ha-custom-cards
description: |
  Configures HACS custom cards (ApexCharts, modern-circular-gauge, bubble-card, mini-graph-card,
  mushroom) for Home Assistant dashboards with validated configurations, color schemes, and error
  patterns. Use when asked to "add custom card", "install HACS card", "create gauge/graph",
  "ApexCharts dashboard", "mushroom cards", or "bubble separator".

---

Works with HACS installation (UI and API), Lovelace YAML dashboards, and custom card configurations.
# Home Assistant Custom Cards

Configure HACS (Home Assistant Community Store) custom cards for enhanced dashboard visualizations.

## Installed Cards

| Card | Purpose | Repository ID |
|------|---------|---------------|
| `mini-graph-card` | Compact sparkline graphs | 151280062 |
| `bubble-card` | Section separators with icons | 680112919 |
| `modern-circular-gauge` | Beautiful circular gauges | 871730343 |
| `lovelace-mushroom` | Modern entity cards | 444350375 |
| `apexcharts-card` | Advanced graphs with time axis | 331701152 |

## When to Use This Skill

Use this skill when you need to:
- Create circular gauge visualizations with color segments for temperature, humidity, or other metrics
- Build advanced time-series graphs with ApexCharts for multi-sensor comparisons
- Add section separators with icons using bubble-card for dashboard organization
- Install HACS custom cards programmatically via WebSocket API
- Troubleshoot ApexCharts span.end errors with validated configurations
- Build modern Mushroom-style entity cards

Do NOT use when:
- Native Home Assistant cards meet your needs (prefer built-in cards for simplicity)
- You haven't verified entity IDs exist before using them in custom cards
- Building dashboards without checking browser console for errors

## Quick Start

All configurations in this skill are validated and tested. Critical errors (like ApexCharts `span.end`) are documented with solutions.

## Usage

1. **Install via HACS**: Use UI (HACS → Frontend → Search) or API (WebSocket `hacs/repository/download`)
2. **Choose card type**: Gauge (circular), graph (ApexCharts/mini-graph), separator (bubble-card), entity (mushroom)
3. **Apply configuration**: Copy validated YAML from examples below
4. **Verify**: Check browser console (F12) for errors, restart HA if card doesn't load
5. **Customize**: Adjust colors, min/max values, time spans based on sensor type

### Modern Circular Gauge (VALIDATED)

```yaml
type: custom:modern-circular-gauge
entity: sensor.temperature
name: Temperature
min: 10
max: 40
needle: true
segments:
  - from: 10
    color: "#3498db"    # Cold - blue
  - from: 18
    color: "#2ecc71"    # Comfortable - green
  - from: 26
    color: "#f1c40f"    # Warm - yellow
  - from: 32
    color: "#e74c3c"    # Hot - red
```

### ApexCharts with Time Axis (VALIDATED)

**CRITICAL:** The `span.end` field must be one of: "minute", "hour", "day", "week", "month", "year", "isoWeek"

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: 24 Hour History
  show_states: true
graph_span: 24h
span:
  end: hour  # REQUIRED: must be minute/hour/day/week/month/year/isoWeek
yaxis:
  - min: 0
    max: 50
    decimals: 1
apex_config:
  chart:
    height: 200
  xaxis:
    type: datetime
    labels:
      datetimeFormatter:
        hour: "HH:mm"
  legend:
    show: true
series:
  - entity: sensor.temperature
    name: Temperature
    color: "#e74c3c"
    stroke_width: 2
```

**Common ApexCharts Errors:**
- WRONG: `"span": {"end": "now"}` → ❌ Causes parsing error
- CORRECT: `"span": {"end": "hour"}` → ✅ Valid value

### Bubble Card Separator

```yaml
type: custom:bubble-card
card_type: separator
name: Section Name
icon: mdi:thermometer
```

### Mushroom Climate Card (VALIDATED)

```yaml
type: custom:mushroom-climate-card
entity: climate.ac_unit
name: AC Name
hvac_modes:
  - "off"
  - cool
  - heat
  - auto
show_temperature_control: true
collapsible_controls: true
```

## Common Patterns

### Grid Layout with Gauges

```yaml
type: grid
columns: 3
square: false
cards:
  - type: custom:modern-circular-gauge
    entity: sensor.officeht_temperature
    name: Temperature
    min: 10
    max: 40
    needle: true
    segments:
      - from: 10
        color: "#3498db"
      - from: 18
        color: "#2ecc71"
      - from: 26
        color: "#f1c40f"
      - from: 32
        color: "#e74c3c"
  - type: custom:modern-circular-gauge
    entity: sensor.officeht_humidity
    name: Humidity
    min: 0
    max: 100
    needle: true
    segments:
      - from: 0
        color: "#e74c3c"
      - from: 30
        color: "#f1c40f"
      - from: 40
        color: "#2ecc71"
      - from: 60
        color: "#f1c40f"
      - from: 70
        color: "#e74c3c"
```

See `examples/examples.md` for complete environmental dashboard section with separators and graphs.

## ApexCharts Advanced Features

### Valid Span Configuration (VALIDATED)

**CRITICAL:** Always use one of these valid values for `span.end`:

```yaml
span:
  end: minute   # Start of current minute
  end: hour     # Start of current hour
  end: day      # Start of current day
  end: week     # Start of current week
  end: month    # Start of current month
  end: year     # Start of current year
  end: isoWeek  # Start of ISO week (Monday)
```

**Never use:** `"now"` or other string values - these cause errors.

### Dual Y-Axis

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Temperature & Humidity
graph_span: 24h
span:
  end: hour
yaxis:
  - id: temp
    min: 0
    max: 50
    decimals: 1
  - id: humidity
    opposite: true
    min: 0
    max: 100
series:
  - entity: sensor.temperature
    name: Temperature
    yaxis_id: temp
    color: "#e74c3c"
    stroke_width: 2
  - entity: sensor.humidity
    name: Humidity
    yaxis_id: humidity
    color: "#3498db"
    stroke_width: 2
```

### Annotations (Sunrise/Sunset)

**WARNING:** JavaScript template annotations may cause errors. Use with caution.

```yaml
apex_config:
  annotations:
    xaxis:
      - x: "${ new Date(states['sun.sun'].attributes.next_rising).getTime() }"
        borderColor: "#FFA500"
        label:
          text: Sunrise
          style:
            background: "#FFA500"
```

**Note:** If annotations cause configuration errors, remove them or use static timestamps instead.

See `references/reference.md` for complete ApexCharts advanced features and time formatting options.

## Supporting Files

- **examples/examples.md** - Comprehensive examples (environmental dashboard section, grid layouts, mushroom cards, ApexCharts patterns)
- **references/reference.md** - Color schemes, HACS installation (UI and API), troubleshooting, best practices, official documentation

## HACS Installation

### Via UI

1. Open HACS → Frontend
2. Search for card name
3. Click Download
4. Restart Home Assistant

### Via API (Programmatic)

```python
import json
import websocket

ws_url = "ws://192.168.68.123:8123/api/websocket"
ws = websocket.create_connection(ws_url)

# Auth
ws.recv()
ws.send(json.dumps({
    "type": "auth",
    "access_token": os.environ["HA_LONG_LIVED_TOKEN"]
}))
ws.recv()

# Install card by repository ID
ws.send(json.dumps({
    "id": 1,
    "type": "hacs/repository/download",
    "repository": 151280062,  # mini-graph-card
}))
response = json.loads(ws.recv())
ws.close()
```

## Common Error Patterns

### 1. ApexCharts span error

Check `span.end` uses valid value (hour/day/week/month/year)

```yaml
# WRONG
span:
  end: now  # ❌

# CORRECT
span:
  end: hour  # ✅
```

### 2. Entity not found

Verify entity exists in Developer Tools → States

### 3. Card not loading

Check HACS installation and browser console (F12)

### 4. JavaScript template error

Remove or simplify template annotations

See `references/reference.md` for complete troubleshooting guide.

## Best Practices

1. **Use meaningful colors**: Red for warnings/hot, blue for cold/water, green for normal
2. **Test incrementally**: Add cards one at a time and validate
3. **Check browser console**: View errors in browser console (F12)
4. **Validate entities**: Ensure entity IDs exist before using in cards
5. **Restart HA after HACS install**: Custom cards require restart to activate

## Notes

- ApexCharts `span.end` MUST use valid enum values (minute/hour/day/week/month/year/isoWeek)
- All HACS cards require Home Assistant restart after installation
- Repository IDs: mini-graph-card (151280062), apexcharts-card (331701152), bubble-card (680112919)
- JavaScript template annotations may cause errors - test before deploying
- Use Developer Tools → States to verify entity IDs exist
