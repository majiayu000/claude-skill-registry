---
name: ha-graphs-visualization
description: "Create and configure Home Assistant graphs and visualizations including history-graph, statistics-graph, mini-graph-card (HACS), and apexcharts-card (HACS) with time ranges, multiple sensors, aggregations, and annotations. Use when displaying sensor data over time, creating trend charts, comparing historical data, or building energy/climate/air quality dashboards."
---

# Home Assistant Graphs and Visualization

Create informative graphs and charts for sensor data visualization in Home Assistant dashboards.

## Quick Start

This skill covers four main graphing solutions:
- **History Graph** (native): Simple sensor history with automatic long-term statistics
- **Statistics Graph** (native): Long-term trend analysis with aggregations
- **Mini-Graph-Card** (HACS): Popular, lightweight graphs with customization
- **ApexCharts Card** (HACS): Advanced publication-quality charts with annotations

### Basic Examples

**History Graph (Native):**
```yaml
type: history-graph
entities:
  - entity: sensor.temperature
    name: Living Room
  - entity: sensor.humidity
hours_to_show: 24
```

**ApexCharts (HACS) - VALIDATED CONFIG:**

**CRITICAL:** The `span.end` field must be one of: "minute", "hour", "day", "week", "month", "year", "isoWeek"

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: 24 Hour History
  show_states: true
graph_span: 24h
span:
  end: hour  # REQUIRED: minute/hour/day/week/month/year/isoWeek
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
- ❌ WRONG: `"span": {"end": "now"}` → Causes parsing error
- ✅ CORRECT: `"span": {"end": "hour"}` → Valid value

## Graph Selection Decision Tree

```
START
│
├─ Need simple sensor history (last 24-48h)?
│  └─ YES → Use history-graph (native)
│
├─ Need long-term trends (weeks/months)?
│  └─ YES → Use statistics-graph (native)
│
├─ Need minimalist design with moderate customization?
│  └─ YES → Use mini-graph-card (HACS)
│
└─ Need advanced features (annotations, comparisons, multi-axis)?
   └─ YES → Use apexcharts-card (HACS)
```

## Comparison Matrix

| Feature | History Graph | Statistics Graph | Mini-Graph-Card | ApexCharts |
|---------|---------------|------------------|-----------------|------------|
| **Type** | Native | Native | HACS | HACS |
| **UI Editor** | ✅ Full | ✅ Full | ❌ YAML only | ❌ YAML only |
| **Performance** | ⚡ Fast | ⚡ Fast | ⚡ Fast | ⚠️ Moderate |
| **Customization** | 🔹 Basic | 🔹 Basic | 🔸 Good | 🔶 Extensive |
| **Multiple Entities** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Chart Types** | Line | Line/Bar | Line/Bar | Line/Bar/Area/Column |
| **Time Range** | Hours | Calendar periods | Hours | Flexible spans |
| **Statistics** | Auto | Built-in | Manual | Manual |
| **Best For** | Quick history | Long-term trends | Clean design | Power users |

## History Graph Card (Native)

**Best for:** Simple sensor history visualization (recent data)

### Basic Configuration

```yaml
type: history-graph
entities:
  - entity: sensor.temperature_living_room
    name: Living Room
  - entity: sensor.temperature_bedroom
    name: Bedroom
hours_to_show: 24
refresh_interval: 0  # Default: auto-refresh
```

### Key Features

- Displays sensor history from recorder database
- Automatically switches to long-term statistics for older data
- Bold line = recorder data, thin line = statistics
- If `hours_to_show` > recorder retention: uses long-term statistics

**Performance Note:** History graphs are very fast because they use HA's built-in recorder data.

## Statistics Graph Card (Native)

**Best for:** Long-term trend analysis (weeks, months, years)

### Basic Configuration

```yaml
type: statistics-graph
entities:
  - sensor.energy_daily
stat_types:
  - mean
  - min
  - max
period:
  calendar:
    period: month
chart_type: line
```

See `references/reference.md` for stat types and period options.

## Mini-Graph-Card (HACS)

**Installation:** HACS → Frontend → Search "mini-graph-card"

**Best for:** Minimalist design, lightweight, moderate customization

### Basic Temperature Graph

```yaml
type: custom:mini-graph-card
entities:
  - sensor.temperature_bedroom
  - sensor.temperature_living_room
name: Temperature Comparison
hours_to_show: 24
points_per_hour: 2
line_width: 2
font_size: 75
```

### Multiple Entities with Colors

```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.temperature
    name: Temp
    color: '#e74c3c'
  - entity: sensor.humidity
    name: Humidity
    color: '#3498db'
    y_axis: secondary
show:
  labels: true
  legend: true
  name: true
  state: true
```

See `references/reference.md` for complete configuration options and `examples/examples.md` for more patterns.

## ApexCharts Card (HACS) - VALIDATED CONFIGURATIONS

**Installation:** HACS → Frontend → Search "apexcharts-card"

**Best for:** Advanced visualizations, publication-quality charts, complex comparisons

### CRITICAL: Valid Span Configuration

**Always use one of these valid values for `span.end`:**

```yaml
span:
  end: minute   # Start of current minute
  end: hour     # Start of current hour (RECOMMENDED)
  end: day      # Start of current day
  end: week     # Start of current week
  end: month    # Start of current month
  end: year     # Start of current year
  end: isoWeek  # Start of ISO week (Monday)
```

**Never use:** `"now"` or other string values - these cause errors.

### Basic Time Series (VALIDATED)

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Temperature History
  show_states: true
graph_span: 24h
span:
  end: hour  # REQUIRED
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
  - entity: sensor.temperature_living_room
    name: Living Room
    color: "#e74c3c"
    stroke_width: 2
  - entity: sensor.temperature_bedroom
    name: Bedroom
    color: "#3498db"
    stroke_width: 2
```

### Multi-Sensor with Dual Y-Axis (VALIDATED)

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Temperature & Humidity
  show_states: true
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
apex_config:
  chart:
    height: 250
  xaxis:
    type: datetime
    labels:
      datetimeFormatter:
        hour: "HH:mm"
series:
  - entity: sensor.temperature
    name: Temperature
    yaxis_id: temp
    color: '#e74c3c'
    stroke_width: 2
  - entity: sensor.humidity
    name: Humidity
    yaxis_id: humidity
    color: '#3498db'
    stroke_width: 2
```

## Supporting Files

- **examples/examples.md** - Comprehensive real-world examples (climate dashboards, air quality, energy usage, multi-room comparisons, annotations, area charts)
- **references/reference.md** - Technical depth (performance optimization, advanced ApexCharts configuration, troubleshooting, best practices, official documentation)

## Best Practices

1. **Choose the Right Graph Type**
   - Line: Continuous data (temperature, humidity)
   - Bar/Column: Discrete data (daily energy, events)
   - Area: Cumulative data (solar production, rainfall)

2. **Use Meaningful Colors**
   - Red: High temperatures, alerts, energy consumption
   - Blue: Low temperatures, water, humidity
   - Green: Normal values, success, efficiency
   - Orange: Warnings, moderate values

3. **Show Current State**
   ```yaml
   header:
     show_states: true  # Shows current value in header
   ```

4. **Use Appropriate Time Ranges**
   - Real-time monitoring: 1-6 hours
   - Daily patterns: 24 hours
   - Weekly trends: 7 days
   - Monthly analysis: 30 days
   - Long-term: statistics-graph

## Common Issues

### ApexCharts Span Error

**Error:** `"Invalid value for span.end"`

**Solution:** Change `span.end` to one of: minute, hour, day, week, month, year, isoWeek

```yaml
# WRONG
span:
  end: now  # ❌ Causes error

# CORRECT
span:
  end: hour  # ✅ Valid value
```

### No Data Showing

- Verify entity exists (Developer Tools → States)
- Check recorder retention period
- Ensure sensor has `state_class: measurement`
- Check long-term statistics (Developer Tools → Statistics)

See `references/reference.md` for complete troubleshooting guide.

## Notes

- History graphs automatically switch to long-term statistics for older data
- ApexCharts `span.end` MUST use valid enum values (hour/day/week/month/year)
- Mini-graph-card `points_per_hour` controls performance (lower = faster)
- Statistics graphs are best for long-term trends (weeks/months)
- Custom cards require HACS installation and HA restart
