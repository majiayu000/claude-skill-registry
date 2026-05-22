---
name: design-token-orchestrator
description: Unified design token automation for Northcote Curio. Build, validate, and sync design tokens across CSS, Tailwind, and theme systems. Ensures compliance with Northcote palette and Victorian aesthetic principles.
---

# Design Token Orchestrator Skill

## Overview

One-stop automation for the complete design token lifecycle: generation → validation → synchronization. Eliminates manual script execution and ensures Northcote Curio color palette compliance.

This skill integrates three previously standalone scripts into a cohesive workflow that maintains design system integrity.

## When to Use This Skill

Use this skill when you need to:

- **Build design tokens** from a source JSON into CSS variables and Tailwind config
- **Validate token compliance** against Northcote Curio palette rules
- **Sync theme files** to keep tokens aligned across systems
- **Audit color usage** to detect forbidden colors (blues, purples, neons)
- **Generate token reports** showing coverage and compliance scores

## How It Works

The orchestrator provides three core operations:

### 1. Build Tokens (`build`)

**Input**: `design-system/tokens.json`
**Output**:

- `frontend/src/styles/design-tokens.css` (CSS variables)
- `design-system/tailwind-token-patch.js` (Tailwind config)

**What it does**:

- Parses token JSON
- Generates CSS custom properties (`--sys-color-*`, `--sys-shape-*`, etc.)
- Creates Tailwind theme extensions
- Validates structure

**Usage**:

```bash
python .claude/skills/design-token-orchestrator/scripts/build_tokens.py
```

---

### 2. Validate Tokens (`validate`)

**Input**: `design-system/tokens.json`
**Output**: Compliance report (JSON)

**What it does**:

- Checks required token categories (color, typography, spacing, elevation, shape)
- Validates WCAG AA contrast ratios
- Detects forbidden colors (blues, purples, neons)
- Compares against Northcote reference palette
- Scores compliance 0-100

**Usage**:

```bash
python .claude/skills/design-token-orchestrator/scripts/validate_tokens.py
```

**Validation Rules**:

1. ✅ **Palette Compliance**: Colors must be from Northcote botanical palette
2. ❌ **Forbidden Colors**: Electric blue (#0080FF), neon purple (#9D4EDD), cyan
3. ✅ **Contrast Requirements**: Text/background pairs must meet WCAG AA (4.5:1)
4. ✅ **Token Structure**: Must include color, typography, spacing, elevation, shape

---

### 3. Sync Tokens (`sync`)

**Input**: Current theme files
**Output**: Synchronized token definitions

**What it does**:

- Reads theme configuration
- Extracts design values
- Writes to canonical token JSON
- Ensures single source of truth

**Usage**:

```bash
python .claude/skills/design-token-orchestrator/scripts/sync_tokens.py
```

---

## Skill Workflow Examples

### Example 1: Fresh Token Build

**Scenario**: You've updated `design-system/tokens.json` with new colors.

**Steps**:

1. "Build tokens from the updated JSON"
2. "Validate the new tokens against Northcote compliance"
3. If validation passes → tokens are ready to use
4. If validation fails → review flagged colors and fix

**Expected Output**:

```
✅ Generated 78 color tokens
✅ Generated 7 shape tokens
✅ Tailwind config patched
✅ Validation: 94/100 (1 contrast warning)
```

---

### Example 2: Audit Existing Tokens

**Scenario**: You want to verify current tokens are Northcote-compliant.

**Steps**:

1. "Validate existing design tokens"
2. Review compliance report
3. Identify violations (e.g., forbidden blue detected)
4. Fix violations in source JSON
5. Rebuild tokens

**Expected Output**:

```json
{
  "compliance_score": 87,
  "violations": [
    {
      "category": "forbidden_color",
      "token": "color.accent.blue",
      "value": "#0080FF",
      "rule": "Electric blue forbidden in Northcote palette"
    }
  ]
}
```

---

### Example 3: Full Token Lifecycle

**Scenario**: Complete token system update.

**Workflow**:

```
1. Sync theme → tokens.json
2. Validate compliance
3. Fix violations
4. Build CSS + Tailwind
5. Verify output
```

**Commands**:

```bash
# Step 1: Sync
python scripts/sync_tokens.py

# Step 2: Validate
python scripts/validate_tokens.py

# Step 3: Build (if validation passes)
python scripts/build_tokens.py
```

---

## Integration with Other Skills

### With `northcote-visual-audit`

Visual audit validates rendered components. Token orchestrator validates source tokens. Together, they ensure design → implementation fidelity.

### With `northcote-typography-strategy`

Typography strategy defines font choices. Token orchestrator ensures those fonts are correctly defined as CSS variables.

### With `brand-brief-optimizer`

Brief optimizer establishes design direction. Token orchestrator implements that direction as executable tokens.

---

## Technical Specifications

### Required Token Structure

```json
{
  "color": {
    "primary": "#C45C4B",
    "secondary": "#D4A84B",
    "tertiary": "#8A9A7A"
  },
  "typography": {
    "fontFamilyBase": "'Crimson Text', serif",
    "fontFamilyHeading": "'Lora', serif"
  },
  "spacing": {
    "scale": {
      "space1": "4px",
      "space2": "8px"
    }
  },
  "shape": {
    "corner_small": "8px",
    "corner_medium": "12px"
  },
  "elevation": {
    "level_0": "none",
    "level_1": "0 1px 2px rgba(0,0,0,0.05)"
  }
}
```

### Generated CSS Variables

```css
:root {
  --sys-color-primary: #c45c4b;
  --sys-color-secondary: #d4a84b;
  --sys-font-base: "Crimson Text", serif;
  --sys-shape-corner-small: 8px;
  --sys-elevation-level-1: 0 1px 2px rgba(0, 0, 0, 0.05);
}
```

---

## Northcote Palette Reference

The skill includes a reference palette at `resources/northcote-palette.json`:

```json
{
  "waratahCrimson": "#C45C4B",
  "wattleGold": "#D4A84B",
  "eucalyptusSage": "#8A9A7A",
  "ochreEarth": "#CC8B4A",
  "coralRed": "#D05D5D",
  "specimenNight": "#1A1714",
  "parchmentCream": "#F5F1E8"
}
```

**Forbidden Colors**:

- Electric blue (#0080FF)
- Neon purple (#9D4EDD)
- Cyan (#00FFFF)

---

## Dependencies

```bash
# Python dependencies
pip install wcag-contrast-ratio

# All scripts are Python 3.8+ compatible
```

---

## Error Handling

All scripts return:

- **Exit code 0**: Success
- **Exit code 1**: Validation failure or build error
- **Logs**: Written to console (redirect to file if needed)

---

## Limitations

This skill:

✅ Automates token generation and validation
✅ Ensures Northcote palette compliance
✅ Detects forbidden colors
✅ Validates WCAG contrast ratios

❌ Does not modify component code (use other skills for that)
❌ Does not generate tokens from scratch (requires source JSON)
❌ Does not handle runtime theme switching

---

## Key Principle

**Design tokens are the single source of truth.** Everything else—CSS, Tailwind, component styles—derives from tokens. This skill ensures that source of truth remains pure, compliant, and synchronized.

---

_Unified token automation. Northcote compliance guaranteed. Victorian precision in every variable._
