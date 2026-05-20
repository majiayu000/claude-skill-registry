---
name: ui-review
description: Comprehensive UI review for WCAG compliance, design system adherence, and legaltech patterns
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, mcp__claude-in-chrome__*, mcp__hallucination-detector__*, mcp__memory__*
context: full
agent: general-purpose
model: claude-opus-4-5-20250514
---

# ui-review

Comprehensive UI review for 45Black legaltech products. Reviews live UIs against WCAG standards, design system compliance, and legaltech-specific patterns.

## When To Use

- Before shipping a new UI feature
- After design system updates
- Accessibility audit needed
- Compliance review required
- User mentions: "review UI", "check accessibility", "WCAG audit", "design review"

## Workflow

### 1. Capture Current State

If URL provided, use browser automation:
```
1. Navigate to the URL using mcp__claude-in-chrome__navigate
2. Take screenshot using mcp__claude-in-chrome__computer (action: screenshot)
3. Get accessibility tree using mcp__claude-in-chrome__read_page
4. If multiple pages, repeat for each
```

If codebase review, read component files:
```
1. Find UI components using Glob
2. Read component code
3. Identify design token usage
```

### 2. WCAG 2.1 Compliance Check

Run through this checklist:

#### Level AA (Mandatory for 45Black)

| Criterion | Check | Pass/Fail |
|-----------|-------|-----------|
| **1.1.1 Non-text Content** | All images have alt text | |
| **1.3.1 Info and Relationships** | Semantic HTML, proper headings | |
| **1.4.3 Contrast (Minimum)** | 4.5:1 for text, 3:1 for large text | |
| **1.4.4 Resize Text** | Works at 200% zoom | |
| **1.4.11 Non-text Contrast** | 3:1 for UI components | |
| **2.1.1 Keyboard** | All functions keyboard accessible | |
| **2.4.3 Focus Order** | Logical focus sequence | |
| **2.4.4 Link Purpose** | Links describe destination | |
| **2.4.6 Headings and Labels** | Descriptive headings | |
| **2.4.7 Focus Visible** | Clear focus indicators | |
| **3.1.1 Language** | `lang` attribute set | |
| **3.2.1 On Focus** | No unexpected changes | |
| **3.3.1 Error Identification** | Errors clearly identified | |
| **3.3.2 Labels or Instructions** | Form fields have labels | |

#### Level AAA (Target for Trustee Edition)

| Criterion | Check | Pass/Fail |
|-----------|-------|-----------|
| **1.4.6 Contrast (Enhanced)** | 7:1 for text | |
| **2.4.9 Link Purpose (Link Only)** | Link text alone is clear | |
| **3.2.5 Change on Request** | User-initiated changes only | |

### 3. Design System Compliance

#### Detect Which System Should Apply

```
Is this client-facing (trustees, advisers)?
└── YES → Check against TRUSTEE EDITION v1.0
    └── Reference: ~/.45black/brand/TRUSTEE.md

Is this internal (developers, admins)?
└── YES → Check against SAVILLE v5.0
    └── Reference: ~/.45black/brand/SAVILLE-v5.md
    └── Sub-check: Core or Clarity variant?
```

#### Trustee Edition Checklist

| Element | Expected | Actual | Status |
|---------|----------|--------|--------|
| Primary colour | `#1A4F7A` (Governance Blue) | | |
| Background | `#FFFFFF` (Paper White) | | |
| Typography | Inter | | |
| Touch targets | ≥44px | | |
| Border radius | ≤8px | | |
| Focus indicator | 3px outline, 2px offset | | |
| Status colours | Compliance palette | | |
| Print stylesheet | Present | | |

#### Saville v5.0 Checklist

| Element | Expected | Actual | Status |
|---------|----------|--------|--------|
| Primary colour | `#2E8B8B` (Deep Teal) | | |
| Code Bar | 6px height, correct order | | |
| Warm carbon | `#121210` (not #0F0F0F) | | |
| Typography | IBM Plex Sans | | |
| Touch targets | ≥44px | | |
| Border radius | ≤12px | | |
| Focus indicator | 2px ring | | |
| Orange usage | 19pt+ only | | |
| Animation | ≤300ms | | |
| Matte texture | ON (Core) / OFF (Clarity) | | |

### 4. Legaltech-Specific Patterns

#### EU AI Act Compliance (Mandatory)

| Requirement | Check | Status |
|-------------|-------|--------|
| **AI Transparency** | All AI outputs marked "AI-Generated" | |
| **Verification Prompt** | "Always verify AI suggestions" footer | |
| **Human-in-Loop** | No auto-approval of AI suggestions | |
| **Audit Trail** | AI interactions logged | |
| **Confidence Display** | AI confidence scores shown | |

#### Legal Citation Standards

| Requirement | Check | Status |
|-------------|-------|--------|
| **Legislation References** | Clickable, linked to source | |
| **Case Citations** | Proper format ([YYYY] court ref) | |
| **Definition Tooltips** | Legal terms have hover definitions | |
| **Provenance** | Source and date visible | |

#### Compliance UI Patterns

| Requirement | Check | Status |
|-------------|-------|--------|
| **Status Badges** | Using design system colours | |
| **Obligation Cards** | Clear hierarchy (title, source, stakeholder) | |
| **Due Date Visibility** | Overdue items prominently marked | |
| **Audit Evidence** | Upload/attachment clearly labelled | |

### 5. Generate Report

Create a structured report:

```markdown
# UI Review Report: [Product Name]
**Date:** [Current Date]
**Reviewer:** Claude UI Expert
**Design System:** [Trustee/Saville Core/Saville Clarity]

## Summary
- **Overall Score:** [Pass/Pass with Issues/Fail]
- **WCAG AA:** [X/14 checks passed]
- **Design System:** [X/Y tokens correct]
- **Legaltech Patterns:** [X/Y implemented]

## Critical Issues (Must Fix)
1. [Issue]: [Location] - [Fix instruction]
2. ...

## Warnings (Should Fix)
1. [Issue]: [Location] - [Fix instruction]
2. ...

## Recommendations (Nice to Have)
1. [Suggestion]
2. ...

## Evidence
- [Screenshot references]
- [Accessibility tree excerpts]

## Next Steps
1. Use `/ui-fix` to generate implementation patches
```

### 6. Store Learnings

If patterns discovered, save to memory:
```
mcp__memory__create_entities with:
- Entity: UIPattern
- Observations: What was found, why it matters
```

## Quick Checks (Single Command)

For rapid reviews, use these focused checks:

```
/ui-review contrast    → Only check colour contrast ratios
/ui-review focus       → Only check focus indicators
/ui-review ai-markers  → Only check AI transparency labels
/ui-review status      → Only check status badge usage
```

## Integration with Other Skills

```
/ui-architect → Design the structure
/ui-review    → Check compliance (THIS SKILL)
/ui-fix       → Generate fixes
```

## Model Preference

**opus** - Compliance checking requires careful reasoning about edge cases

---
*Part of 45Black UI Expert Devstack*
*For non-coders: This skill audits your UI and tells you what needs fixing*
