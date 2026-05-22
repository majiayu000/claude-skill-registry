---
name: ux-toolkit
description: Comprehensive UX evaluation meta-skill. Use when conducting UI/UX audits, accessibility reviews, user flow analysis, responsive testing, or interaction design evaluation.
version: 2.0.0
---

# UX Toolkit

Professional-grade meta-skill for systematic UX evaluation across 9 domains. Framework-agnostic design works for web, mobile, and desktop applications.

## When to Use

Invoke for:
- UI/UX heuristic evaluations (Nielsen + modern methodologies)
- Accessibility (WCAG 2.2) compliance audits
- User flow & friction analysis
- Responsive/cross-device testing
- Interaction & micro-interaction review
- Design system consistency audits
- Content & UX writing review
- AI/ML interface patterns
- Privacy & ethical design review

## Audit Type Selection

```
What do you need to evaluate?
    │
    ├─► Full UX Audit ─────────► Load ALL references
    │
    ├─► Accessibility Only ────► Load accessibility-inspector.md
    │
    ├─► Usability Review ──────► Load heuristic-audit.md + user-flow-analysis.md
    │
    ├─► Visual/Responsive ─────► Load responsive-behavior.md + interaction-review.md
    │
    ├─► Design System ─────────► Load design-system-audit.md
    │
    ├─► Content Audit ─────────► Load content-ux-audit.md
    │
    ├─► AI Interface ──────────► Load ai-ux-patterns.md
    │
    └─► Privacy/Ethics ────────► Load privacy-ethics-audit.md
```

## Sub-Workflows

| Domain | Reference | Purpose |
|--------|-----------|---------|
| Heuristic Audit | `references/heuristic-audit.md` | Nielsen's 10 + modern methodologies (OOUX, JTBD, Cognitive Walkthrough) |
| A11Y Inspector | `references/accessibility-inspector.md` | WCAG 2.2 AA/AAA, keyboard nav, screen readers |
| Flow Analysis | `references/user-flow-analysis.md` | Task paths, friction points, cognitive load |
| Responsive | `references/responsive-behavior.md` | Breakpoints, touch targets, RTL/LTR, PWA |
| Interactions | `references/interaction-review.md` | Micro-interactions, animations, feedback |
| Design System | `references/design-system-audit.md` | Token consistency, component audit |
| Content UX | `references/content-ux-audit.md` | UX writing, readability, voice & tone |
| AI/ML Patterns | `references/ai-ux-patterns.md` | Explainability, trust, ML error handling |
| Privacy & Ethics | `references/privacy-ethics-audit.md` | Dark patterns, consent, GDPR/DSA compliance |

## Quick Start

### 1. Define Scope

```
Audit Scope:
├── Screens/Pages: [List target screens]
├── User Flows: [Primary conversion, core tasks]
├── Platform: [Web/Mobile/Desktop/All]
├── WCAG Target: [A/AA/AAA]
└── Priority Focus: [Accessibility/Usability/Performance]
```

### 2. Select Audit Type

| Type | References | Time | Coverage |
|------|------------|------|----------|
| Quick A11Y | accessibility-inspector.md | 1-2h | Automated + keyboard nav |
| Heuristic Review | heuristic-audit.md | 2-4h | Nielsen's 10 + severity |
| Full UX Audit | All 9 references | 1-2d | Complete evaluation |
| Focused Audit | 2-3 specific refs | 3-6h | Targeted domain review |

### 3. Execute Workflow

Each reference contains:
- Checklist items w/ pass/fail criteria
- Severity + effort classification
- Remediation guidance
- Tool recommendations

### 4. Generate Report

```bash
python3 scripts/generate_report.py --type [full|heuristic|a11y|flow|responsive|interaction] --output report.md --format [md|json|csv]
```

## Severity Classification

| Level | Impact | Frequency | Priority | Action |
|-------|--------|-----------|----------|--------|
| Critical | Blocks task | Any | P0 | Fix immediately |
| Major | Significant friction | >50% users | P1 | Fix before release |
| Minor | Reduced efficiency | <50% users | P2 | Fix in next sprint |
| Cosmetic | Polish issue | Any | P3 | Backlog |

### Priority Matrix

```
                    HIGH FREQUENCY
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         │   MAJOR       │   CRITICAL    │
         │   (P1)        │   (P0)        │
         │               │               │
LOW      ├───────────────┼───────────────┤      HIGH
IMPACT   │               │               │      IMPACT
         │   COSMETIC    │   MINOR       │
         │   (P3)        │   (P2)        │
         │               │               │
         └───────────────┼───────────────┘
                         │
                    LOW FREQUENCY
```

## Effort Estimation

| Effort | Description | Examples |
|--------|-------------|----------|
| Low | < 1 hour, single file | CSS fix, label addition, alt text |
| Medium | 1-4 hours, few files | Component refactor, form validation |
| High | > 4 hours, architectural | Navigation restructure, focus management |

## Modern Methodologies

Beyond Nielsen's 10 heuristics, this toolkit incorporates:

| Methodology | Focus | When to Use |
|-------------|-------|-------------|
| **Cognitive Walkthrough** | Task completion probability | Complex flows, onboarding |
| **OOUX** | Object-noun consistency | Information architecture |
| **JTBD** | Job stories validation | Feature validation |
| **Six Minds Framework** | Cognitive architecture | Complex interfaces |
| **Baymard Heuristics** | E-commerce specifics | Shopping flows |

## WCAG Compliance Levels

| Level | Requirement | Target |
|-------|-------------|--------|
| A | Minimum accessibility | Baseline |
| AA | Acceptable accessibility | **Standard target** |
| AAA | Enhanced accessibility | Specific audiences |

**WCAG 2.2 Status**: This toolkit covers all 9 new WCAG 2.2 criteria (October 2023).

## Platform Adapters

| Platform | Automated Testing | Manual Testing |
|----------|------------------|----------------|
| Web | axe-core, Lighthouse | Browser DevTools |
| iOS | Xcode Accessibility Inspector | VoiceOver |
| Android | Accessibility Scanner (ADB) | TalkBack |
| Desktop | Platform-specific tools | Keyboard + screen reader |
| Design Files | Figma plugins (Stark, A11y) | Manual review |

## Integration Points

| Tool | Purpose | Usage |
|------|---------|-------|
| axe-core | Automated a11y | `scripts/run_axe.js` |
| Lighthouse | Performance + a11y | Chrome DevTools |
| Contrast Checker | Color ratios | `scripts/check_contrast.py` |
| Readability | Content grade level | Flesch-Kincaid analysis |
| Visual Regression | Layout stability | BackstopJS/Playwright |

## Process Overview

```
1. Scope Definition     → Define screens/flows to audit
2. Reference Loading    → Load relevant sub-workflow(s)
3. Automated Scans      → Run axe-core, Lighthouse
4. Manual Review        → Execute checklists
5. Finding Capture      → Document w/ severity + effort
6. Prioritization       → Apply Impact × Frequency matrix
7. Report Generation    → Compile actionable report
```

## Anti-Patterns to Detect

| Anti-Pattern | Category | Severity |
|--------------|----------|----------|
| Confirm-shaming | Dark Pattern | Critical |
| Hidden costs | Dark Pattern | Critical |
| Forced continuity | Dark Pattern | Major |
| No loading feedback | Visibility | Major |
| Keyboard traps | Accessibility | Critical |
| Color-only indicators | Accessibility | Major |
| Infinite scroll w/o footer | Navigation | Minor |
| Auto-playing video w/ sound | Attention | Major |

## Competitive Benchmarking

For comprehensive audits, compare key flows against 1-2 competitors:

```markdown
| Metric | Your Product | Competitor A | Competitor B |
|--------|--------------|--------------|--------------|
| Task completion time | Xs | Xs | Xs |
| Click count | X | X | X |
| Error rate | X% | X% | X% |
| A11y score (Lighthouse) | X | X | X |
```

## Report Formats

| Format | Use Case | Command |
|--------|----------|---------|
| Markdown | Documentation, PRs | `--format md` |
| JSON | Jira/Linear import | `--format json` |
| CSV | Spreadsheet analysis | `--format csv` |

## Files Structure

```
ux-toolkit/
├── SKILL.md                          # This file
├── references/
│   ├── heuristic-audit.md            # Nielsen + modern heuristics
│   ├── accessibility-inspector.md    # WCAG 2.2 compliance
│   ├── user-flow-analysis.md         # Flow & friction analysis
│   ├── responsive-behavior.md        # Cross-device behavior
│   ├── interaction-review.md         # Micro-interactions
│   ├── design-system-audit.md        # Token & component audit
│   ├── content-ux-audit.md           # UX writing & readability
│   ├── ai-ux-patterns.md             # AI/ML interface patterns
│   └── privacy-ethics-audit.md       # Dark patterns & consent
├── scripts/
│   ├── check_contrast.py             # Color contrast checker
│   ├── generate_report.py            # Report generator
│   └── run_axe.js                    # Automated a11y testing
└── data/
    └── issues-database.json          # Common issues + remediation
```

---

Ref: Load specific `references/*.md` for detailed checklists & workflows.