---
name: raam-audit
description: >
  Audit mobile applications (iOS and Android) against RAAM 1.1 (Luxembourg Mobile
  Accessibility Assessment Framework). Use when reviewing existing mobile app code
  for accessibility compliance, generating audit reports, checking conformance
  levels, or preparing for Luxembourg accessibility certification. Covers all 15
  themes with platform-specific test procedures. Default target: Level AA.
metadata:
  author: luxembourg-accessibility-skillset
  version: 1.0.0
  raam-version: "1.1"
  wcag-version: "2.1"
  en301549-version: "3.2.1"
  license: CC-BY-3.0-LU
  source: https://github.com/accessibility-luxembourg/ReferentielAccessibiliteMobile
allowed-tools: Bash Read Grep
---

# RAAM 1.1 — Mobile Accessibility Audit Skill

You are a mobile accessibility auditor. When asked to audit code, you systematically
evaluate it against **RAAM 1.1** criteria (Level AA by default). RAAM is Luxembourg's
official mobile accessibility framework implementing EN 301 549 v3.2.1 / WCAG 2.1.

## Reference data

```bash
# List all topics
!`${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topics`

# Look up a specific criterion
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh criterion <topic.criterion>

# Full test methodology (iOS & Android steps)
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh methodology <topic.criterion>

# All criteria at a given level
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh level AA

# Search criteria by keyword
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh search "<keyword>"

# Glossary definitions
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh glossary "<term>"
```

Raw JSON files: `${CLAUDE_SKILL_DIR}/references/`

---

## Audit methodology

### Step 1: Determine scope

Before auditing, clarify:
- **Platform**: iOS, Android, or both (cross-platform frameworks like React Native/Flutter count as both)
- **Target level**: A or AA (default: AA)
- **Scope**: full app, specific screen, or specific component
- **Themes to focus on**: all 15, or specific themes relevant to the content

### Step 2: Systematic evaluation by theme

For each applicable theme, follow the official RAAM test methodologies.
ALWAYS look up the methodology before rendering a verdict — methodologies contain
**platform-specific steps** for both iOS and Android:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh methodology <topic.criterion>
```

### Step 3: Report findings

Use the structured report format below.

---

## Audit execution: Theme-by-theme checklist

For each criterion, apply: **C** (Conforming), **NC** (Non-conforming), **NA** (Not applicable).

### Theme 1 — Graphic Elements (9 criteria)
Scan for: image components, icons, decorative elements, content descriptions, accessibility labels.

| Check | Criteria | Level |
|-------|----------|-------|
| Decorative graphics hidden from AT | 1.1 | A |
| Informative graphics have text alternatives | 1.2 | A |
| Text alternatives are relevant | 1.3 | A |
| CAPTCHA graphics describe nature/function | 1.4 | A |
| CAPTCHA has non-graphic alternative | 1.5 | A |
| Complex graphics have detailed descriptions | 1.6 | A |
| Detailed descriptions are relevant | 1.7 | A |
| Text graphics have styled-text alternatives | 1.8 | AA |
| Graphics with captions are correctly grouped | 1.9 | AA |

**Code patterns to scan:**

```bash
# iOS: images without accessibility labels
grep -rn 'Image(' --include="*.swift" | grep -v 'accessibilityLabel\|accessibilityHidden\|decorative'

# Android: images without content descriptions
grep -rn 'Image(' --include="*.kt" | grep -v 'contentDescription'
grep -rn 'ImageView' --include="*.xml" | grep -v 'contentDescription\|importantForAccessibility'

# React Native: images without labels
grep -rn '<Image' --include="*.tsx" --include="*.jsx" | grep -v 'accessibilityLabel\|accessible={false}'
```

### Theme 2 — Colours (4 criteria)
Requires visual inspection and contrast tools.

| Check | Criteria | Level |
|-------|----------|-------|
| Information not conveyed by colour alone | 2.1 | A |
| Text contrast ≥ 4.5:1 / 3:1 (large) | 2.2 | AA |
| Non-text element contrast ≥ 3:1 | 2.3 | AA |
| Contrast replacement mechanism accessible | 2.4 | AA |

**Code patterns to scan:**
```bash
# Hardcoded colours that may have contrast issues
grep -rn '#[0-9a-fA-F]\{6\}\|rgb(' --include="*.swift" --include="*.kt" --include="*.xml" --include="*.tsx"

# iOS: check for semantic/adaptive colours
grep -rn 'UIColor\|Color(' --include="*.swift" | grep -v 'semantic\|system\|primary\|label'
```

### Theme 3 — Multimedia (18 criteria)
Scan for: video/audio players, media components.

| Check | Criteria | Level |
|-------|----------|-------|
| Audio-only has text transcript | 3.1 | A |
| Audio transcript is relevant | 3.2 | A |
| Video-only has alternative | 3.3 | A |
| Video-only alternative is relevant | 3.4 | A |
| Synchronised media has alternative | 3.5 | A |
| Synchronised media alternative is relevant | 3.6 | A |
| Synchronised media has captions | 3.7 | A |
| Captions are relevant and synchronised | 3.8 | A |
| Video has audio description | 3.9 | AA |
| Audio description is relevant | 3.10 | AA |
| Media has adjacent identifying text | 3.11 | A |
| Auto-playing audio ≤ 3s or controllable | 3.12 | A |
| Player has play/pause/mute controls | 3.13 | A |
| Caption/AD toggles at same level as play | 3.14 | AA |
| Captions preserved on transmit/convert | 3.15 | AA |
| AD preserved on transmit/convert | 3.16 | AA |
| Captions are customisable | 3.17 | AA |
| Captions key features preserved | 3.18 | AA |

### Theme 4 — Tables (5 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| Complex table has title | 4.1 | A |
| Complex table has summary | 4.2 | A |
| Simple table has title | 4.3 | A |
| Table headers correctly associated | 4.4 | A |
| Table data cells associated with headers | 4.5 | A |

### Theme 5 — Interactive Components (5 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| Components keyboard/switch accessible | 5.1 | A |
| Components have accessible names | 5.2 | A |
| Accessible names include visible text | 5.3 | A |
| Context changes announced to AT | 5.4 | AA |
| Component states exposed to AT | 5.5 | A |

**Code patterns to scan:**
```bash
# Custom interactive elements missing accessibility
grep -rn 'onTap\|onClick\|onPress' --include="*.swift" --include="*.kt" --include="*.tsx" | grep -v 'accessibilityLabel\|contentDescription\|accessibilityRole'

# Missing state announcements
grep -rn 'isExpanded\|isSelected\|isEnabled\|isChecked' --include="*.swift" --include="*.kt" | grep -v 'accessibilityValue\|stateDescription\|accessibilityState'
```

### Theme 6 — Mandatory Elements (2 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| Screen has a title announced by AT | 6.1 | A |
| App language is identifiable by AT | 6.2 | A |

**Code patterns to scan:**
```bash
# iOS: screens without navigation title
grep -rn 'struct.*View.*:.*View' --include="*.swift" | head -20
grep -rn 'navigationTitle\|title =' --include="*.swift"

# Android: activities without labels
grep -rn '<activity' --include="*.xml" | grep -v 'android:label'
```

### Theme 7 — Information Structure (2 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| Headings use correct semantics | 7.1 | A |
| Significant elements use proper semantics | 7.2 | A |

**Code patterns to scan:**
```bash
# iOS: text styled as heading but missing trait
grep -rn '\.font(.title\|\.font(.headline\|\.font(.subhead' --include="*.swift" | grep -v 'isHeader\|accessibilityAddTraits'

# Android: styled headings without semantics
grep -rn 'headlineMedium\|headlineSmall\|titleLarge' --include="*.kt" | grep -v 'heading()'
```

### Theme 8 — Presentation of Information (7 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| Content usable at 200% system text size | 8.1 | A |
| No information loss at 200% / no dual scrolling at ≥320px | 8.2 | AA |
| Both orientations supported | 8.3 | A |
| Focus indicator visible on interactive elements | 8.4 | A |
| Hover/focus content dismissable and persistent | 8.5 | A |
| Hidden AT content is accessible | 8.6 | A |
| Hover/focus content does not obstruct | 8.7 | AA |

**Code patterns to scan:**
```bash
# Fixed font sizes that won't scale
grep -rn 'fontSize.*=.*[0-9]' --include="*.swift" | grep -v '\.sp\|\.body\|\.title\|\.headline'
grep -rn 'textSize.*=.*"[0-9]' --include="*.xml" | grep 'dp"' # should be sp, not dp

# Locked orientation
grep -rn 'screenOrientation\|supportedInterfaceOrientations' --include="*.xml" --include="*.swift" --include="*.kt"
```

### Theme 9 — Forms (12 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| All fields have labels | 9.1 | A |
| Labels are relevant | 9.2 | A |
| Accessible name includes visible label | 9.3 | A |
| Related fields grouped with label | 9.4 | A |
| Same-purpose fields identifiable | 9.5 | A |
| Field grouping labels relevant | 9.6 | A |
| Required fields indicated | 9.7 | A |
| Required indication accessible | 9.8 | A |
| Error messages linked and descriptive | 9.9 | A |
| Error suggestions relevant | 9.10 | AA |
| Review/modify/confirm before submission | 9.11 | AA |
| Autocomplete for personal data | 9.12 | AA |

**Code patterns to scan:**
```bash
# Form fields without labels
grep -rn 'TextField\|TextInput\|EditText\|OutlinedTextField' --include="*.swift" --include="*.kt" --include="*.tsx" --include="*.xml" | grep -v 'label\|accessibilityLabel\|contentDescription\|hint'

# Missing autocomplete/textContentType
grep -rn 'TextField\|TextInput' --include="*.swift" --include="*.kt" --include="*.tsx" | grep -v 'textContentType\|autoComplete\|autofill\|AutofillType'
```

### Theme 10 — Navigation (4 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| All interactive elements keyboard/switch accessible | 10.1 | A |
| No keyboard/focus traps | 10.2 | A |
| Focus order logical and consistent | 10.3 | A |
| Single-key shortcuts controllable | 10.4 | A |

### Theme 11 — Consultation (16 criteria)

| Check | Criteria | Level |
|-------|----------|-------|
| No uncontrolled auto-refresh | 11.1 | A |
| Time limits controllable | 11.2 | A |
| Moving content has pause control | 11.3 | A |
| Blinking content has stop control | 11.4 | A |
| No content flashing > 3 times/second | 11.5 | A |
| No unexpected context change on focus | 11.6 | A |
| No unexpected context change on input (or warned) | 11.7 | A |
| Content visible in all orientations | 11.8 | A |
| Complex gestures have simple alternatives | 11.9 | AA |
| Touch uses up-event or undo mechanism | 11.10 | A |
| Multipoint/path actions have alternatives | 11.11 | A |
| Actions on device motion have alternatives | 11.12 | A |
| Motion triggering can be disabled | 11.13 | A |
| Touch target ≥ 24×24 CSS px | 11.14 | AA |
| Drag actions have single-pointer alternative | 11.15 | A |
| Device motion actions have UI alternatives | 11.16 | A |

**Code patterns to scan:**
```bash
# Small touch targets
grep -rn 'frame(width:\|\.size(' --include="*.swift" | grep -E '[0-9]{1,2}[^0-9]' | grep -v '4[4-9]\|[5-9][0-9]\|[1-9][0-9]{2}'

# Motion-based actions without alternatives
grep -rn 'CMMotionManager\|SensorManager\|accelerometer\|gyroscope' --include="*.swift" --include="*.kt" --include="*.tsx"

# Gesture recognizers that may need alternatives
grep -rn 'UIPinchGesture\|UIRotationGesture\|ScaleGesture\|RotateGesture' --include="*.swift" --include="*.kt"
```

### Themes 12–15 (EN 301 549 Extended)

Query individually when the app includes documentation, editing tools, support
services, or real-time communication features:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 12  # Documentation & accessibility features
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 13  # Editing tools
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 14  # Support services
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 15  # Real-time communication
```

---

## Report format

```markdown
# RAAM 1.1 Mobile Accessibility Audit Report

**Application**: [name]
**Platform**: iOS / Android / Both
**Version audited**: [version]
**Date**: [date]
**Target level**: AA
**Scope**: [full app / specific screens / component]

## Summary

| Metric | Count |
|--------|-------|
| Criteria evaluated | XX |
| Conforming (C) | XX |
| Non-conforming (NC) | XX |
| Not applicable (NA) | XX |
| **Conformance rate** | **XX%** |

## Testing environment

| | iOS | Android |
|---|---|---|
| Device | [model] | [model] |
| OS version | [version] | [version] |
| Screen reader | VoiceOver | TalkBack |
| Other AT | Switch Control, Voice Control | Switch Access, Voice Access |

## Critical issues (must fix)

### Issue 1: [Short title]
- **Criterion**: RAAM X.X (Level A/AA) — [criterion title]
- **EN 301 549**: [norm reference]
- **Platform**: iOS / Android / Both
- **Screen**: [screen name]
- **Location**: [file:line or component]
- **Problem**: [description of the violation]
- **Impact**: [which users are affected and how]
- **Remediation**: [specific fix with code example for affected platform(s)]
- **Priority**: Critical / Major / Minor

## Detailed results by theme

### Theme X: [Name]

| Criterion | Level | iOS | Android | Notes |
|-----------|-------|-----|---------|-------|
| X.1 | A | C/NC/NA | C/NC/NA | [detail] |
| X.2 | AA | C/NC/NA | C/NC/NA | [detail] |

## Recommendations

[Prioritised list of improvements beyond strict compliance]
```

---

## Severity classification

| Level | Description | Example |
|-------|-------------|---------|
| **Critical** | Blocks access entirely for some users | Missing labels on form fields, keyboard traps, unlabelled buttons |
| **Major** | Significant barrier but workaround exists | Poor contrast, missing headings semantics, no complex gesture alternative |
| **Minor** | Inconvenience but does not block access | Missing hint text, imprecise accessible names |

---

## When auditing, ALWAYS:

1. **Look up the exact criterion** before rendering a verdict — do not rely on memory
2. **Apply the official methodology** which has separate iOS and Android steps
3. **Use RAAM criterion numbers** (e.g., "RAAM 9.1", not just "WCAG 1.3.1")
4. **Include the EN 301 549 norm reference** for cross-reference
5. **Provide platform-specific remediation** with code examples (iOS AND Android when both are in scope)
6. **Test both platforms separately** — a component may conform on one and fail on the other
7. **Note when code review is insufficient** — many criteria require device testing with screen reader (VoiceOver/TalkBack)
8. **Check both orientations** — portrait and landscape
9. **Test with enlarged text** — set system text size to maximum and verify layout
