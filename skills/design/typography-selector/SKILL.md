---
description: Browse and select fonts from Google Fonts or curated pairings. Use to find the perfect typography for a design project.
allowed-tools:
  - AskUserQuestion
  - mcp__claude-in-chrome__tabs_context_mcp
  - mcp__claude-in-chrome__tabs_create_mcp
  - mcp__claude-in-chrome__navigate
  - mcp__claude-in-chrome__computer
  - mcp__claude-in-chrome__read_page
  - mcp__claude-in-chrome__find
---

# Typography Selector

Browse, select, and apply typography for frontend designs.

## Purpose

This skill helps select the perfect fonts by:
- Browsing trending fonts on Google Fonts
- Suggesting pairings based on aesthetic
- Generating Google Fonts imports
- Mapping to Tailwind config
- Providing curated fallbacks when browser unavailable

## Browser Workflow

### Step 1: Navigate to Google Fonts

```javascript
tabs_context_mcp({ createIfEmpty: true })
tabs_create_mcp()
navigate({ url: "https://fonts.google.com/?sort=trending", tabId: tabId })
```

### Step 2: Browse Fonts

Take screenshots of trending fonts:

```javascript
computer({ action: "screenshot", tabId: tabId })
```

Present to user: "Here are trending fonts. What style catches your eye?"

### Step 3: Search Specific Fonts

If user has a preference:

```javascript
navigate({ url: "https://fonts.google.com/?query=Outfit", tabId: tabId })
computer({ action: "screenshot", tabId: tabId })
```

### Step 4: View Font Details

Click on a font to see all weights and styles:

```javascript
computer({ action: "left_click", coordinate: [x, y], tabId: tabId })
computer({ action: "screenshot", tabId: tabId })
```

### Step 5: Select Fonts

Get user's choice for:
- **Display/Heading font**: For headlines, hero text
- **Body font**: For paragraphs, readable text
- **Mono font** (optional): For code, technical content

### Step 6: Generate Import

Create Google Fonts import:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,700&display=swap" rel="stylesheet">
```

### Step 7: Generate Config

Create Tailwind font config:

```javascript
tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        display: ['Fraunces', 'serif'],
        body: ['Outfit', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    }
  }
}
```

---

## Fallback Mode

When browser tools are unavailable, use curated pairings.

### How to Use Fallbacks

1. Ask user about desired aesthetic
2. Present relevant pairings from `references/font-pairing.md`
3. Let user choose or request adjustments
4. Provide import code for selected fonts

### Quick Aesthetic Match

| Aesthetic | Recommended Pairing |
|-----------|---------------------|
| Dark & Premium | Fraunces + Outfit |
| Minimal | Satoshi + Satoshi |
| Neobrutalism | Space Grotesk + Space Mono |
| Editorial | Instrument Serif + Inter |
| Y2K/Cyber | Orbitron + JetBrains Mono |
| Scandinavian | Plus Jakarta Sans + Plus Jakarta Sans |
| Corporate | Work Sans + Inter |

---

## Typography Best Practices

### Font Pairing Rules

**Contrast, not conflict:**
- Pair serif with sans-serif
- Pair display with readable body
- Match x-height for harmony
- Limit to 2 fonts (3 max with mono)

**Weight distribution:**
- Headlines: Bold (600-900)
- Subheads: Medium (500-600)
- Body: Regular (400)
- Captions: Light to Regular (300-400)

### Sizing Scale

Use a consistent type scale:

```css
/* Minor Third (1.2) */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
--text-7xl: 4.5rem;    /* 72px */
```

### Line Height

| Content Type | Line Height | Tailwind Class |
|--------------|-------------|----------------|
| Headlines | 1.1 - 1.2 | leading-tight |
| Subheads | 1.25 - 1.35 | leading-snug |
| Body text | 1.5 - 1.75 | leading-relaxed |
| Small text | 1.4 - 1.5 | leading-normal |

### Letter Spacing

| Usage | Tracking | Tailwind Class |
|-------|----------|----------------|
| All caps | Wide | tracking-widest |
| Headlines | Tight to normal | tracking-tight |
| Body | Normal | tracking-normal |
| Small caps | Wide | tracking-wide |

---

## Fonts to Avoid

**Overused (instant "template" feeling):**
- Inter (the default AI font)
- Roboto (Android default)
- Open Sans (early 2010s web)
- Arial / Helvetica (unless intentional Swiss)
- Lato (overexposed)
- Poppins (overused in 2020s)

**Why these feel generic:**
- Used in every Figma template
- Default in many tools
- No distinctive character
- Signal "no design decision made"

---

## Output Format

Provide selected typography in this format:

```markdown
## Selected Typography

### Font Stack
| Role | Font | Weights | Fallback |
|------|------|---------|----------|
| Display | Fraunces | 400, 700 | serif |
| Body | Outfit | 400, 500, 600 | sans-serif |
| Mono | JetBrains Mono | 400 | monospace |

### Google Fonts Import
\`\`\`html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Outfit:wght@400;500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
\`\`\`

### Tailwind Config
\`\`\`javascript
fontFamily: {
  display: ['Fraunces', 'serif'],
  body: ['Outfit', 'sans-serif'],
  mono: ['JetBrains Mono', 'monospace'],
}
\`\`\`

### Usage Examples
\`\`\`html
<h1 class="font-display text-6xl font-bold leading-tight">
  Headline
</h1>
<p class="font-body text-lg leading-relaxed">
  Body text goes here.
</p>
<code class="font-mono text-sm">
  code example
</code>
\`\`\`
```

---

## References

See `references/font-pairing.md` for:
- Curated font pairings by aesthetic
- Font classification guide
- Advanced pairing techniques
- Performance considerations
