---
description: Browse and select color palettes from Coolors or curated fallbacks. Use to find the perfect color palette for a design project.
allowed-tools:
  - AskUserQuestion
  - mcp__claude-in-chrome__tabs_context_mcp
  - mcp__claude-in-chrome__tabs_create_mcp
  - mcp__claude-in-chrome__navigate
  - mcp__claude-in-chrome__computer
  - mcp__claude-in-chrome__read_page
---

# Color Curator

Browse, select, and apply color palettes for frontend designs.

## Purpose

This skill helps select the perfect color palette by:
- Browsing trending palettes on Coolors
- Presenting options to the user
- Extracting hex codes
- Mapping to Tailwind config
- Providing curated fallbacks when browser unavailable

## Browser Workflow

### Step 1: Navigate to Coolors

```javascript
tabs_context_mcp({ createIfEmpty: true })
tabs_create_mcp()
navigate({ url: "https://coolors.co/palettes/trending", tabId: tabId })
```

### Step 2: Screenshot Palettes

Take screenshots of trending palettes:

```javascript
computer({ action: "screenshot", tabId: tabId })
```

Present to user: "Here are the trending palettes. Which one catches your eye?"

### Step 3: Browse More

If user wants more options:

```javascript
computer({ action: "scroll", scroll_direction: "down", tabId: tabId })
computer({ action: "screenshot", tabId: tabId })
```

### Step 4: Select Palette

When user chooses a palette, click to view details:

```javascript
computer({ action: "left_click", coordinate: [x, y], tabId: tabId })
```

### Step 5: Extract Colors

From the palette detail view, extract:
- All 5 hex codes
- Color names if available
- Relative positions (light to dark)

### Step 6: Map to Design

Based on user's background style preference:

| Background Style | Mapping |
|-----------------|---------|
| Pure white | `bg: #ffffff`, text: darkest color |
| Off-white/warm | `bg: #faf8f5`, text: darkest |
| Light tinted | `bg: lightest from palette`, text: darkest |
| Dark/moody | `bg: darkest from palette`, text: white/#fafafa |

### Step 7: Generate Config

Create Tailwind color config:

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#[main-color]',
        secondary: '#[supporting-color]',
        accent: '#[pop-color]',
        background: '#[bg-color]',
        surface: '#[card-color]',
        text: {
          primary: '#[heading-color]',
          secondary: '#[body-color]',
          muted: '#[muted-color]'
        }
      }
    }
  }
}
```

---

## Fallback Mode

When browser tools are unavailable, use curated palettes.

### How to Use Fallbacks

1. Ask user about desired mood/aesthetic
2. Present relevant fallback palettes from `references/color-theory.md`
3. Let user choose or request adjustments
4. Provide hex codes for selected palette

### Present Options

Ask the user:

"Without browser access, I can suggest palettes based on your aesthetic. Which mood fits best?"

- **Dark & Premium**: Rich blacks with warm accents
- **Clean & Minimal**: Neutral grays with single accent
- **Bold & Energetic**: High contrast primaries
- **Warm & Inviting**: Earth tones and creams
- **Cool & Professional**: Blues and slate grays
- **Creative & Playful**: Vibrant multi-color

### Manual Input

Users can also provide:
- Hex codes directly: "Use #ff6b35 as primary"
- Color descriptions: "I want a forest green and cream palette"
- Reference: "Match these colors from my logo"

---

## Palette Best Practices

### 60-30-10 Rule

- **60%**: Dominant color (background, large areas)
- **30%**: Secondary color (containers, sections)
- **10%**: Accent color (CTAs, highlights)

### Contrast Requirements

Always verify:
- Text on background: 4.5:1 minimum
- Large text on background: 3:1 minimum
- Interactive elements: 3:1 minimum

### Color Roles

| Role | Usage | Count |
|------|-------|-------|
| Primary | Brand, CTAs, links | 1 |
| Secondary | Hover, icons, supporting | 1-2 |
| Background | Page background | 1 |
| Surface | Cards, modals, inputs | 1 |
| Border | Dividers, outlines | 1 |
| Text Primary | Headings, important text | 1 |
| Text Secondary | Body, descriptions | 1 |
| Text Muted | Captions, placeholders | 1 |

---

## Output Format

Provide the selected palette in this format:

```markdown
## Selected Color Palette

### Colors
| Role | Hex | Preview | Usage |
|------|-----|---------|-------|
| Primary | #ff6b35 | 🟧 | CTAs, links, accents |
| Background | #0a0a0a | ⬛ | Page background |
| Surface | #1a1a1a | ⬛ | Cards, modals |
| Text Primary | #ffffff | ⬜ | Headings, buttons |
| Text Secondary | #a3a3a3 | ⬜ | Body text, descriptions |
| Border | #2a2a2a | ⬛ | Dividers, outlines |

### Tailwind Config
\`\`\`javascript
colors: {
  primary: '#ff6b35',
  background: '#0a0a0a',
  surface: '#1a1a1a',
  text: {
    primary: '#ffffff',
    secondary: '#a3a3a3',
  },
  border: '#2a2a2a',
}
\`\`\`

### CSS Variables (Alternative)
\`\`\`css
:root {
  --color-primary: #ff6b35;
  --color-background: #0a0a0a;
  --color-surface: #1a1a1a;
  --color-text-primary: #ffffff;
  --color-text-secondary: #a3a3a3;
  --color-border: #2a2a2a;
}
\`\`\`
```

---

## References

See `references/color-theory.md` for:
- Curated fallback palettes by aesthetic
- Color psychology guide
- Palette creation techniques
- Accessibility considerations
