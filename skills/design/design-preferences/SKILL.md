---
name: design-preferences
description: |
  Gather user design preferences before building UI.
  Use when: starting a project with visual interface (Web App, Mobile, Browser Extension).
  Triggers: "design preferences", "visual style", "choose theme", "design step".
---

# Design Preferences

Gather user preferences for visual design before building. Creates `docs/DESIGN.md` with selected choices.

## When to Use

**Applies to project types with UI:**
- Web App (SaaS)
- Mobile App
- Browser Extension
- Telegram Bot (if inline keyboards / web app)

**Skip for:**
- REST API (no UI)
- GraphQL API (no UI)
- CLI Tool (terminal only)
- Data Pipeline
- Library/SDK

---

## Question Flow

### Step 1: Design Priority

```
question: "Насколько важен дизайн для этого проекта?"
header: "Design"
options:
  - label: "Профессиональный"
    description: "Уникальный стиль, впечатляет пользователей"
  - label: "Функциональный"
    description: "Чистый и понятный, без лишнего"
  - label: "Минимальный MVP"
    description: "Работает -> достаточно, стиль потом"
```

**If "Минимальный MVP"** -> Skip remaining questions, use defaults.

### Step 2: Aesthetic Direction

```
question: "Какой визуальный стиль ближе?"
header: "Style"
options:
  - label: "Minimalist"
    description: "Много пространства, чистые линии"
  - label: "Bold & Modern"
    description: "Яркие акценты, современный"
  - label: "Soft & Friendly"
    description: "Округлые формы, мягкие тона"
  - label: "Dark & Professional"
    description: "Тёмная тема, серьёзный"
  - label: "Colorful & Playful"
    description: "Яркие цвета, игривый"
```

### Step 3: Theme Selection

Based on aesthetic direction, offer matching themes from theme-factory:

| Direction | Matching Themes |
|-----------|-----------------|
| Minimalist | Modern Minimalist, Arctic Frost |
| Bold & Modern | Tech Innovation, Sunset Boulevard |
| Soft & Friendly | Desert Rose, Botanical Garden |
| Dark & Professional | Ocean Depths, Midnight Galaxy |
| Colorful & Playful | Golden Hour, Sunset Boulevard |

```
question: "Какая цветовая схема?"
header: "Theme"
options:
  - label: "{Theme 1}"
    description: "{Primary colors}"
  - label: "{Theme 2}"
    description: "{Primary colors}"
  - label: "Custom"
    description: "Опишу свои цвета"
```

**If "Custom"** -> Ask follow-up: "Опиши желаемые цвета или бренд"

### Step 4: Typography Style

```
question: "Какой стиль текста?"
header: "Fonts"
options:
  - label: "Sans-Serif (современный)"
    description: "Чистый, технологичный"
  - label: "Serif (классический)"
    description: "Традиционный, солидный"
  - label: "Mixed (заголовки/текст)"
    description: "Display + body fonts"
```

### Step 5: Animation Level

```
question: "Сколько анимации?"
header: "Motion"
options:
  - label: "Subtle"
    description: "Только hover эффекты"
  - label: "Moderate"
    description: "Переходы, hover, scroll"
  - label: "Rich"
    description: "Page transitions, stagger, parallax"
  - label: "None"
    description: "Без анимации"
```

---

## Output: docs/DESIGN.md

```markdown
# Design Specification

## Priority
{Professional / Functional / MVP}

## Aesthetic Direction
{Selected style}

## Theme
**Name:** {theme name}
**Colors:**
- Primary: {hex}
- Secondary: {hex}
- Accent: {hex}
- Background: {hex}
- Text: {hex}

**Fonts:**
- Headers: {font name}
- Body: {font name}

## Motion
**Level:** {Subtle / Moderate / Rich / None}
**Patterns:**
- Hover: {yes/no}
- Page transitions: {yes/no}
- Scroll animations: {yes/no}
- Loading states: {yes/no}

## Implementation Notes
- Use CSS variables for theme colors
- Follow frontend-design skill principles
- Avoid generic fonts (Inter, Roboto, Arial)
- {Additional notes based on choices}
```

---

## Default Values (MVP mode)

If user chooses "Минимальный MVP":
- Theme: Modern Minimalist
- Fonts: System sans-serif
- Motion: None
- Priority: Ship fast, style later

---

## Integration with /ship

Place this step between Phase 1 (Idea Validation) and Phase 2 (Project Setup):

```
Phase 1: Idea Validation
  -> Step 1.6: Create PRD

Phase 1.5: Design Preferences   <-- NEW
  -> Ask design questions
  -> Create DESIGN.md

Phase 2: Project Setup
  -> Read PRD.md + DESIGN.md
  -> Apply theme to templates
```

---

## Theme Details Reference

### Ocean Depths
- Primary: #1a2332 (Deep Navy)
- Secondary: #2d8b8b (Teal)
- Accent: #a8dadc (Seafoam)
- Background: #f1faee (Cream)
- Use: Corporate, finance, trust

### Sunset Boulevard
- Primary: #e76f51 (Burnt Orange)
- Secondary: #f4a261 (Coral)
- Accent: #e9c46a (Warm Sand)
- Background: #264653 (Deep Purple)
- Use: Creative, marketing, lifestyle

### Forest Canopy
- Primary: #2d4a2b (Forest Green)
- Secondary: #7d8471 (Sage)
- Accent: #a4ac86 (Olive)
- Background: #faf9f6 (Ivory)
- Use: Eco, wellness, organic

### Modern Minimalist
- Primary: #36454f (Charcoal)
- Secondary: #708090 (Slate Gray)
- Accent: #d3d3d3 (Light Gray)
- Background: #ffffff (White)
- Use: Tech, architecture, data

### Golden Hour
- Primary: #f4a900 (Mustard)
- Secondary: #c1666b (Terracotta)
- Accent: #d4b896 (Warm Beige)
- Background: #4a403a (Chocolate)
- Use: Food, hospitality, artisan

### Arctic Frost
- Primary: #d4e4f7 (Ice Blue)
- Secondary: #4a6fa5 (Steel Blue)
- Accent: #c0c0c0 (Silver)
- Background: #fafafa (Crisp White)
- Use: Healthcare, tech, clean

### Desert Rose
- Primary: #d4a5a5 (Dusty Rose)
- Secondary: #b87d6d (Clay)
- Accent: #e8d5c4 (Sand)
- Background: #5d2e46 (Burgundy)
- Use: Fashion, beauty, boutique

### Tech Innovation
- Primary: #0066ff (Electric Blue)
- Secondary: #00ffff (Neon Cyan)
- Accent: #ffffff (White)
- Background: #1e1e1e (Dark Gray)
- Use: Startups, AI/ML, digital

### Botanical Garden
- Primary: #4a7c59 (Fern Green)
- Secondary: #f9a620 (Marigold)
- Accent: #b7472a (Terracotta)
- Background: #f5f3ed (Cream)
- Use: Garden, food, natural

### Midnight Galaxy
- Primary: #2b1e3e (Deep Purple)
- Secondary: #4a4e8f (Cosmic Blue)
- Accent: #a490c2 (Lavender)
- Background: #e6e6fa (Silver)
- Use: Entertainment, gaming, creative
