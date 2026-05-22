---
name: using-ux-designer
description: Route to the right UX skill based on your task and platform context
---

# Using UX Designer

## Overview

This meta-skill routes you to the right UX design skills based on your situation. Load this skill when you need UX expertise but aren't sure which specific skill to use.

**Core Principle**: Different UX tasks require different skills. Match your situation to the appropriate skill, load only what you need.

## When to Use

Load this skill when:
- Starting any UX/UI design task
- User mentions: "design", "UX", "UI", "interface", "user experience", "layout", "navigation"
- You need to critique or review a design
- You need to create a new interface or feature
- User asks about UX principles or concepts

**Don't use for**: Backend logic, database design, pure technical implementation without UX implications

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-ux-designer/SKILL.md`

Reference sheets like `ux-fundamentals.md` are at:
  `skills/using-ux-designer/ux-fundamentals.md`

NOT at:
  `skills/ux-fundamentals.md` ← WRONG PATH

When you see a link like `[ux-fundamentals.md](ux-fundamentals.md)`, read the file from the same directory as this SKILL.md.

---

## Routing by Situation

### Learning & Explanation

**Symptoms**: "What is...", "Explain...", "Teach me about...", "How does X work in UX?"

**Route to**: [ux-fundamentals.md](ux-fundamentals.md)

**Examples**:
- "What is information architecture?" → [ux-fundamentals.md](ux-fundamentals.md)
- "Explain visual hierarchy" → [ux-fundamentals.md](ux-fundamentals.md)
- "How do I think about accessibility?" → [ux-fundamentals.md](ux-fundamentals.md)

---

### Design Critique & Review

**Symptoms**: "Review this design", "Critique this interface", "Is this usable?", "Does this follow best practices?"

**Route to**: Relevant competency skills based on critique focus

**General Review** (no specific focus):
- [visual-design-foundations.md](visual-design-foundations.md) (visual hierarchy, color, typography)
- [information-architecture.md](information-architecture.md) (content organization, navigation)
- [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) (WCAG, inclusive design)

**Specific Focus**:
- Visual issues (color, contrast, hierarchy) → [visual-design-foundations.md](visual-design-foundations.md)
- Navigation/findability issues → [information-architecture.md](information-architecture.md)
- Interaction feedback, touch targets → [interaction-design-patterns.md](interaction-design-patterns.md)
- Accessibility concerns → [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md)

**Add platform extension** if design is platform-specific:
- Mobile app → Add [mobile-design-patterns.md](mobile-design-patterns.md)
- Web dashboard → Add [web-application-design.md](web-application-design.md)
- Desktop software → Add [desktop-software-design.md](desktop-software-design.md)
- Game interface → Add [game-ui-design.md](game-ui-design.md)

---

### New Interface Design

**Symptoms**: "Design a...", "Create interface for...", "Build a [feature] screen"

**Route to**: Competency skills + platform extension

**Standard Web/Mobile Feature**:
1. [visual-design-foundations.md](visual-design-foundations.md) (layout, hierarchy, color)
2. [interaction-design-patterns.md](interaction-design-patterns.md) (buttons, feedback, states)
3. Platform-specific:
   - Mobile → [mobile-design-patterns.md](mobile-design-patterns.md)
   - Web app → [web-application-design.md](web-application-design.md)

**Complex Navigation/IA**:
1. [information-architecture.md](information-architecture.md) (content structure, nav systems)
2. [visual-design-foundations.md](visual-design-foundations.md) (visual hierarchy)
3. Platform extension as needed

**Research Phase** (early discovery):
1. [user-research-and-validation.md](user-research-and-validation.md) (understand users first)
2. Then return to design skills once research complete

---

### Specific UX Domains

#### Visual Design Issues

**Symptoms**: "Colors don't work", "Typography feels off", "Hierarchy unclear", "Layout cramped"

**Route to**: [visual-design-foundations.md](visual-design-foundations.md)

**Add**: [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) if contrast/readability concerns

---

#### Navigation & Findability

**Symptoms**: "Users can't find features", "Navigation confusing", "Menu structure", "Content organization"

**Route to**: [information-architecture.md](information-architecture.md)

**Add**: Platform extension for platform-specific nav patterns

---

#### Interaction & Feedback

**Symptoms**: "Button states unclear", "No loading feedback", "Micro-interactions", "Touch targets too small"

**Route to**: [interaction-design-patterns.md](interaction-design-patterns.md)

**Add**: Platform extension for platform-specific interaction conventions

---

#### Accessibility & Inclusion

**Symptoms**: "WCAG compliance", "Accessibility audit", "Colorblind-safe", "Keyboard navigation", "Screen reader"

**Route to**: [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md)

**Note**: This skill should be referenced by all other design decisions (accessibility is universal)

---

#### User Research & Validation

**Symptoms**: "Understand users", "User interviews", "Usability testing", "Mental models", "Journey mapping"

**Route to**: [user-research-and-validation.md](user-research-and-validation.md)

**Add**: Other skills once research informs design direction

---

## Platform-Specific Routing

### Mobile (iOS/Android)

**Symptoms**: "Mobile app", "iOS", "Android", "Touch interface", "Phone", "Tablet"

**Route to**:
- Core competency skills (visual, IA, interaction) as needed
- **Always add**: [mobile-design-patterns.md](mobile-design-patterns.md)

**Mobile-Specific Concerns**:
- Touch targets (44x44pt iOS, 48x48dp Android)
- Gestures (swipe, pinch, long-press)
- Platform conventions (iOS HIG vs Material Design)
- One-handed use, thumb zones

---

### Web Applications

**Symptoms**: "Web app", "Dashboard", "SaaS", "Data visualization", "Admin panel", "Responsive design"

**Route to**:
- Core competency skills as needed
- **Always add**: [web-application-design.md](web-application-design.md)

**Web-Specific Concerns**:
- Responsive breakpoints
- Complex data display (tables, charts)
- Keyboard shortcuts, power-user workflows
- Multi-tasking (tabs, split views)

---

### Desktop Software

**Symptoms**: "Desktop app", "Electron", "Native application", "Multi-window", "Keyboard shortcuts"

**Route to**:
- Core competency skills as needed
- **Always add**: [desktop-software-design.md](desktop-software-design.md)

**Desktop-Specific Concerns**:
- Window management (multi-window, panels)
- Keyboard-first workflows
- Workspace customization
- Power-user features (preferences, scripting)

---

### Game UI

**Symptoms**: "Game", "HUD", "Menu system", "Game interface", "In-game UI", "Player experience"

**Route to**:
- Core competency skills as needed
- **Always add**: [game-ui-design.md](game-ui-design.md)

**Game-Specific Concerns**:
- Visibility vs immersion (diegetic UI)
- Controller/gamepad navigation
- Readability during action
- Performance impact (frame rate)

---

## Multi-Skill Scenarios

### Complete Feature Design (Mobile Login)

**Load in order**:
1. [visual-design-foundations.md](visual-design-foundations.md) (layout, button hierarchy)
2. [interaction-design-patterns.md](interaction-design-patterns.md) (form feedback, button states)
3. [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) (form labels, contrast)
4. [mobile-design-patterns.md](mobile-design-patterns.md) (touch targets, platform conventions)

---

### Dashboard Redesign (Web)

**Load in order**:
1. [information-architecture.md](information-architecture.md) (organize data, navigation)
2. [visual-design-foundations.md](visual-design-foundations.md) (hierarchy, chart design)
3. [web-application-design.md](web-application-design.md) (responsive, data display patterns)
4. [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) (data table accessibility)

---

### Game HUD Evaluation

**Load in order**:
1. [visual-design-foundations.md](visual-design-foundations.md) (readability, contrast)
2. [game-ui-design.md](game-ui-design.md) (immersion, performance, input method)
3. [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) (colorblind-safe indicators)

---

## Cross-Faction Integration

### Lyra + Muna (Technical Writer)

**When designing documentation UX**:
- `lyra/ux-designer/information-architecture` (organize docs)
- `muna/technical-writer/documentation-structure` (content structure)
- `muna/technical-writer/clarity-and-style` (microcopy, UI text)

**Example**: "Design documentation site navigation" → Load IA + documentation-structure

---

### Lyra + Ordis (Security Architect)

**When designing secure interfaces**:
- `lyra/ux-designer/visual-design-foundations` (secure feedback, error states)
- `ordis/security-architect/threat-modeling` (authentication UX threats)

**Example**: "Design login with MFA" → Load interaction-patterns + threat-modeling

---

## Decision Tree

```
User Request
    |
    ├─ "What is...?" / "Explain..." → ux-fundamentals
    |
    ├─ "Review this design"
    |   ├─ General → visual-design + IA + accessibility
    |   └─ Specific concern → Relevant competency skill
    |       └─ Add platform extension if platform-specific
    |
    ├─ "Design a [feature]"
    |   ├─ Research phase? → user-research-and-validation first
    |   └─ Design phase
    |       ├─ Identify competencies needed (visual, IA, interaction)
    |       ├─ Detect platform (mobile, web, desktop, game)
    |       └─ Load competency + platform extension
    |
    └─ Specific domain
        ├─ Visual → visual-design-foundations
        ├─ Navigation → information-architecture
        ├─ Interaction → interaction-design-patterns
        ├─ Accessibility → accessibility-and-inclusive-design
        └─ Research → user-research-and-validation
```

---

## Common Patterns

### Pattern 1: "I need general UX advice"
**Load**: [ux-fundamentals.md](ux-fundamentals.md) (teaches principles)

### Pattern 2: "Critique my [platform] design"
**Load**: visual-design + IA + accessibility + [platform-extension]

### Pattern 3: "Design [feature] for [platform]"
**Load**: Relevant competencies + [platform-extension]

### Pattern 4: "Is this accessible?"
**Load**: [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) (primary)
**Reference**: visual-design (contrast), interaction-design (keyboard nav)

### Pattern 5: "How do users navigate this?"
**Load**: [information-architecture.md](information-architecture.md) (primary)
**Add**: user-research-and-validation (if testing/validation needed)

---

## Benefits of Routing

**Focused expertise**: Load only what's needed for the task
**Clear boundaries**: Each skill has distinct responsibility
**Composable**: Combine skills for complex scenarios
**Efficient**: Avoid loading all 11 skills at once
**Explicit**: User sees which skills are active

---

## UX Designer Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [ux-fundamentals.md](ux-fundamentals.md) - Core UX principles, teaching foundational concepts, design thinking
2. [visual-design-foundations.md](visual-design-foundations.md) - Color theory, typography, visual hierarchy, layout, contrast
3. [information-architecture.md](information-architecture.md) - Navigation systems, content organization, findability, menu structure
4. [interaction-design-patterns.md](interaction-design-patterns.md) - Button states, feedback patterns, micro-interactions, touch targets
5. [accessibility-and-inclusive-design.md](accessibility-and-inclusive-design.md) - WCAG compliance, inclusive design, colorblind-safe, screen readers, keyboard navigation
6. [user-research-and-validation.md](user-research-and-validation.md) - User interviews, usability testing, mental models, journey mapping, research methods
7. [mobile-design-patterns.md](mobile-design-patterns.md) - iOS/Android patterns, touch gestures, platform conventions, thumb zones
8. [web-application-design.md](web-application-design.md) - Responsive design, dashboards, data visualization, SaaS patterns, keyboard shortcuts
9. [desktop-software-design.md](desktop-software-design.md) - Multi-window management, keyboard-first workflows, power-user features, workspace customization
10. [game-ui-design.md](game-ui-design.md) - HUD design, diegetic UI, controller navigation, immersion vs visibility

**Cross-faction**:
- `muna/technical-writer/*` - Documentation UX and microcopy
- `ordis/security-architect/*` - Security-aware interface design
