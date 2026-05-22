---
name: brand-architect
description: Generate brand identity options from brief - marks, colors, typography
---

# Brand Architect Skill

Creates brand identity options based on your brand brief.

## Capabilities

- Generate mark/logo options (SVG)
- Propose color palettes (dark/light modes)
- Suggest typography stacks
- Create mark + text compositions
- Update preview files with options
- Guide through selection process
- Record decisions

## Input Requirements

Requires `knowledge/BRAND_BRIEF.md` with:
- Brand name and tagline
- Values and voice
- Visual direction preferences

## Commands

```
/brand-architect              # Full workflow
/brand-architect marks        # Generate mark options only
/brand-architect colors       # Generate color palette options
/brand-architect typography   # Suggest typography
/brand-architect compositions # Mark + text lockups
/brand-architect review       # Review current options
/brand-architect decide       # Record selections
```

## Workflow

### Step 1: Read Brief
```
Reading knowledge/BRAND_BRIEF.md...

Brand: {name}
Tagline: "{tagline}"
Aesthetic: {aesthetic}
Mark preference: {type}

Ready to generate options.
```

### Step 2: Generate Marks

Create 3-5 mark options based on brief:

```
Generating mark options...

OPTION 1: {description}
├─ Type: {symbol/lettermark/wordmark/icon}
├─ Concept: {what it represents}
└─ File: outputs/svg/mark/mark-v1-transparent.svg

OPTION 2: {description}
...
```

For each mark:
1. Create transparent SVG (base)
2. Create dark mode variant
3. Create light mode variant
4. Test at multiple sizes (16px, 80px, 400px)

### Step 3: Generate Colors

Propose color palette:

```
Color Palette Proposal:

DARK MODE (default):
├─ Background: #000000
├─ Foreground: #FFFFFF
├─ Accent: {based on brand}
└─ Preview: [color swatches]

LIGHT MODE:
├─ Background: #FFFFFF
├─ Foreground: #000000
├─ Accent: {darker version}
└─ Preview: [color swatches]
```

### Step 4: Suggest Typography

```
Typography Recommendation:

Based on your {aesthetic} aesthetic:

FONT STACK:
{stack}

RATIONALE:
- {why this fits the brand}
- {where it works well}

ALTERNATIVES:
1. {alternative stack} - {when to use}
2. {alternative stack} - {when to use}
```

### Step 5: Update Previews

Update preview HTML files with generated options:

```
Updating previews...

✓ previews/brand/twitter-profile.html
✓ previews/brand/og-preview.html
✓ previews/brand/favicon-preview.html
✓ previews/brand/mobile-preview.html

Open these in your browser to see options in context.
```

### Step 6: Guide Selection

```
Let's review each option in context.

MARK SELECTION:
Open previews/brand/twitter-profile.html

Which mark works best as a PFP?
1. mark-v1 - {description}
2. mark-v2 - {description}
3. mark-v3 - {description}
```

Wait for user input at each decision point.

### Step 7: Record Decisions

Save selections to `knowledge/BRAND_DECISIONS.md`:

```
Recording your selections...

✓ Primary mark: mark-v3
✓ Colors: dark-first, accent #00ff88
✓ Typography: ui-monospace stack

Saved to knowledge/BRAND_DECISIONS.md

Next: Run /web-architect to generate final assets.
```

## Mark Generation Guidelines

### SVG Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <!-- Use paths, not text elements -->
  <path d="..." fill="currentColor"/>
</svg>
```

### Size Variants
| Size | Use |
|------|-----|
| 16px | Favicon |
| 32px | Favicon @2x |
| 80px | Small icon |
| 160px | Medium icon |
| 400px | PFP, large icon |

### Naming Convention
```
mark-{version}-{size}-{theme}.svg
mark-v1-transparent.svg     # Base
mark-v1-80-dark.svg         # Dark mode
mark-v1-80-light.svg        # Light mode
```

## Color Generation Guidelines

### Required Tokens
- Background (bg)
- Foreground (fg)
- Accent (primary action color)
- Success, Error, Warning
- Muted (secondary text)

### Contrast Requirements
- Text on bg: 4.5:1 minimum
- Large text: 3:1 minimum

## Output Files

```
outputs/
├── svg/
│   └── mark/
│       ├── mark-v1-transparent.svg
│       ├── mark-v1-80-dark.svg
│       ├── mark-v1-80-light.svg
│       ├── mark-v2-transparent.svg
│       └── ...
└── (other outputs created by web-architect)

knowledge/
└── BRAND_DECISIONS.md  # Updated with selections
```

## Error Handling

### No Brief Found
```
Brand brief not found.

Please create knowledge/BRAND_BRIEF.md using the template:
cp templates/BRAND_BRIEF.md knowledge/BRAND_BRIEF.md

Then fill it out and run /brand-architect again.
```

### Incomplete Brief
```
Brand brief is incomplete.

Missing required fields:
- {field 1}
- {field 2}

Please update knowledge/BRAND_BRIEF.md and try again.
```
