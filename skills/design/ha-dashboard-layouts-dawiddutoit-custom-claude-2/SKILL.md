---
name: ha-dashboard-layouts
description: |
  Provides Home Assistant dashboard layout patterns using vertical-stack (top-to-bottom),
  horizontal-stack (side-by-side), grid (responsive multi-column), panel (full-screen), and
  nested layouts for complex designs. Use when asked to "arrange cards side by side", "create
  3 column grid", "stack cards vertically", "full-screen panel view", or "responsive layout".

---

Works with Lovelace YAML configurations, native layout cards, and mobile-first responsive patterns.
# Home Assistant Dashboard Layouts

Create responsive Home Assistant Lovelace dashboards using native layout types.

## When to Use This Skill

Use this skill when you need to:
- Arrange cards vertically (top-to-bottom stacking) for sequential information
- Place cards side-by-side horizontally for comparisons or related controls
- Create multi-column grid layouts that automatically reflow on mobile
- Build full-screen panel views for maps, cameras, or single-focus displays
- Nest layouts for complex dashboard designs with sections
- Make dashboards responsive with automatic mobile stacking

Do NOT use when:
- You need conditional card visibility (use ha-conditional-cards instead)
- Building forms or input interfaces (use entities card or custom forms)
- You need advanced CSS Grid features (consider layout-card from HACS)

## Usage

1. **Identify user intent**: Map natural language ("side by side", "3 columns") to layout type
2. **Choose layout**: vertical-stack (top to bottom), horizontal-stack (side by side), grid (multi-column), panel (full-screen)
3. **Apply configuration**: Add YAML with appropriate type and options
4. **Test responsiveness**: Verify mobile behavior (grid auto-stacks, horizontal stays side-by-side)
5. **Refine**: Adjust columns, square property, or nest layouts for complex designs

## How to Request Layouts

Map user's natural language to layout types:

**Vertical Stack** (top to bottom):
- "Stack these **vertically**"
- "Put these **one below the other**"
- "**Top to bottom**"

**Horizontal Stack** (side by side):
- "Put these **side by side**"
- "Arrange them **horizontally**"
- "**Next to each other**"
- "Layout in a **row**"

**Grid Layouts**:
- "Use a **3-column grid**" → `columns: 3`
- "Grid with **columns: 4**" → `columns: 4`
- "**Two columns** side by side" → `columns: 2`
- "Make cards **square**" → `square: true`
- "**Equal height and width**" → `square: true`

**Panel View** (full-screen single card):
- "Make this **type: panel**"
- "**Full-screen** card"
- "**Kiosk mode**"

**Nested Layouts**:
- "Vertical stack with **horizontal rows**"
- "Put separator, then **gauges horizontal**, then graph below"
- "Stack sections vertically, but put **cards side-by-side**"

## Layout Types Quick Reference

### 1. Vertical Stack

Cards stack top to bottom, full width.

```python
{
    "type": "vertical-stack",
    "cards": [
        {"type": "entity", "entity": "sensor.temperature"},
        {"type": "entity", "entity": "sensor.humidity"},
        {"type": "entity", "entity": "sensor.pressure"},
    ]
}
```

**Use when:** Cards should stack regardless of screen size.

### 2. Horizontal Stack

Cards arranged left to right, equal width distribution.

```python
{
    "type": "horizontal-stack",
    "cards": [
        {"type": "entity", "entity": "sensor.temperature"},
        {"type": "entity", "entity": "sensor.humidity"},
    ]
}
```

**Use when:** Cards should appear side-by-side on desktop and mobile. Limit to 2-3 cards (more gets cramped on mobile).

### 3. Grid Layouts

Multi-column grid with automatic mobile reflow.

```python
# 3-column grid
{
    "type": "grid",
    "columns": 3,  # Auto-stacks to 1 column on mobile
    "cards": [
        {"type": "entity", "entity": "sensor.temp1"},
        {"type": "entity", "entity": "sensor.temp2"},
        {"type": "entity", "entity": "sensor.temp3"},
        {"type": "entity", "entity": "sensor.temp4"},
        # Cards wrap to next row
    ]
}

# Square cards (equal width/height)
{
    "type": "grid",
    "columns": 3,
    "square": True,  # Forces equal aspect ratio
    "cards": [...]
}
```

**Common column counts:**
- `columns: 2` → Mobile-friendly, compact
- `columns: 3` → Balanced tablet/desktop
- `columns: 4` → Wide desktop screens

**Use `square: true` when:** Uniform appearance needed (gauges, icons, visual consistency).

### 4. Panel View

Full-screen single card (view-level property, not card type).

```python
{
    "views": [
        {
            "title": "Map",
            "type": "panel",  # ← VIEW property
            "cards": [
                {"type": "map", "entities": ["person.john"]}
                # Only ONE card allowed
            ]
        }
    ]
}
```

**Use when:** Full-screen dashboards, kiosk mode, maps, cameras, single-focus displays.

### 5. Nested Layouts

Combine layouts for complex designs.

```python
# Pattern: Vertical stack containing sections
{
    "type": "vertical-stack",
    "cards": [
        # Section 1: Horizontal cards
        {
            "type": "custom:bubble-card",
            "card_type": "separator",
            "name": "Quick Controls",
        },
        {
            "type": "horizontal-stack",
            "cards": [
                {"type": "entity", "entity": "sensor.temp"},
                {"type": "entity", "entity": "sensor.humidity"},
            ]
        },
        # Section 2: Grid layout
        {
            "type": "custom:bubble-card",
            "card_type": "separator",
            "name": "Sensors",
        },
        {
            "type": "grid",
            "columns": 3,
            "cards": [
                {"type": "entity", "entity": "sensor.pm25"},
                {"type": "entity", "entity": "sensor.co2"},
                {"type": "entity", "entity": "sensor.voc"},
            ]
        },
    ]
}
```

**Common nesting patterns:**
- `vertical-stack` → `horizontal-stack` (sections with side-by-side cards)
- `vertical-stack` → `grid` (sections with multi-column cards)
- `horizontal-stack` → `vertical-stack` (two-column responsive layout)

## Mobile Responsiveness

**Grid cards automatically reflow:**
- Desktop: Respects `columns` value
- Mobile: Stacks to 1 column
- No media queries needed

**Horizontal stacks:**
- Remain side-by-side on mobile
- Use sparingly (2-3 cards max)

**Best practices:**
- Test on actual mobile device (browser resize ≠ mobile behavior)
- Place frequently-used controls at top
- Use `columns: 2` or `columns: 3` for mobile-friendly grids

## Advanced Layouts

For more complex requirements, see reference files:

- **[references/sections-view.md](references/sections-view.md)** - Modern drag-and-drop Sections View (HA 2024+)
- **[references/layout-card.md](references/layout-card.md)** - HACS layout-card with CSS Grid and media queries
- **[references/view-types.md](references/view-types.md)** - Masonry, Sidebar, and other view types
- **[references/responsive-patterns.md](references/responsive-patterns.md)** - Advanced mobile-first patterns

## Common Dashboard Patterns

### Temperature Gauges in Grid

```python
{
    "type": "grid",
    "columns": 4,
    "cards": [
        {
            "type": "custom:modern-circular-gauge",
            "entity": "sensor.office_temperature",
            "name": "Office",
            "min": 10,
            "max": 40,
        },
        {
            "type": "custom:modern-circular-gauge",
            "entity": "sensor.living_room_temperature",
            "name": "Living Room",
            "min": 10,
            "max": 40,
        },
        # ... more gauges
    ]
}
```

### Gauge + Graph Side-by-Side

```python
{
    "type": "horizontal-stack",
    "cards": [
        {
            "type": "custom:modern-circular-gauge",
            "entity": "sensor.temperature",
            "name": "Current",
        },
        {
            "type": "custom:mini-graph-card",
            "entity": "sensor.temperature",
            "name": "24h Trend",
            "hours_to_show": 24,
        },
    ]
}
```

### Section with Separator

```python
{
    "type": "vertical-stack",
    "cards": [
        {
            "type": "custom:bubble-card",
            "card_type": "separator",
            "name": "Climate",
            "icon": "mdi:thermometer",
        },
        {
            "type": "grid",
            "columns": 3,
            "cards": [
                # Climate cards here
            ],
        },
    ]
}
```

## Official Documentation

- [Views - Home Assistant](https://www.home-assistant.io/dashboards/views/)
- [Grid card - Home Assistant](https://www.home-assistant.io/dashboards/grid/)
