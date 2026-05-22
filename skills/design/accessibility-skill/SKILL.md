---
document_name: "accessibility.skill.md"
location: ".claude/skills/accessibility.skill.md"
codebook_id: "CB-SKILL-A11Y-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for accessibility compliance"
skill_metadata:
  category: "design"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "WCAG guidelines knowledge"
    - "Assistive technology awareness"
category: "skills"
status: "active"
tags:
  - "skill"
  - "design"
  - "ux"
  - "accessibility"
  - "wcag"
ai_parser_instructions: |
  This skill defines procedures for accessibility.
  Used by UX Designer agent.
---

# Accessibility Skill

=== PURPOSE ===

Procedures for ensuring WCAG 2.1 AA compliance.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(ux-designer) @ref(CB-AGENT-UXDESIGN-001) | Primary skill for accessibility |

=== WCAG 2.1 PRINCIPLES ===

**POUR Framework:**
- **Perceivable** - Information must be presentable
- **Operable** - Interface must be operable
- **Understandable** - Information must be understandable
- **Robust** - Content must work with assistive tech

=== PROCEDURE: Perceivable Checklist ===

### 1.1 Text Alternatives
- [ ] All images have alt text
- [ ] Decorative images have empty alt=""
- [ ] Complex images have long descriptions
- [ ] Icons have accessible names

### 1.2 Time-based Media
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] Live events have captions

### 1.3 Adaptable
- [ ] Content structure uses semantic HTML
- [ ] Reading order is logical
- [ ] Instructions don't rely on sensory characteristics
- [ ] Orientation not restricted

### 1.4 Distinguishable
- [ ] Color is not sole indicator
- [ ] Audio can be controlled
- [ ] Text contrast ≥4.5:1
- [ ] Large text contrast ≥3:1
- [ ] Text can resize to 200%
- [ ] No images of text
- [ ] Content reflows at 320px
- [ ] Non-text contrast ≥3:1
- [ ] Text spacing adjustable
- [ ] Content on hover/focus dismissible

=== PROCEDURE: Operable Checklist ===

### 2.1 Keyboard Accessible
- [ ] All functionality via keyboard
- [ ] No keyboard traps
- [ ] Character key shortcuts can be disabled

### 2.2 Enough Time
- [ ] Time limits adjustable
- [ ] Moving content can be paused
- [ ] No auto-update without warning
- [ ] Re-authentication preserves data

### 2.3 Seizures and Physical
- [ ] No flashing >3 times/second
- [ ] Motion can be disabled

### 2.4 Navigable
- [ ] Skip links present
- [ ] Pages have titles
- [ ] Focus order logical
- [ ] Link purpose clear
- [ ] Multiple ways to find pages
- [ ] Headings describe content
- [ ] Focus indicator visible
- [ ] Location indicated

### 2.5 Input Modalities
- [ ] Touch targets ≥44x44px
- [ ] No drag-only actions
- [ ] Label in name for speech users
- [ ] Motion activation has alternatives

=== PROCEDURE: Understandable Checklist ===

### 3.1 Readable
- [ ] Language of page declared
- [ ] Language of parts declared

### 3.2 Predictable
- [ ] Focus doesn't cause context change
- [ ] Input doesn't cause unexpected change
- [ ] Navigation is consistent
- [ ] Components identified consistently

### 3.3 Input Assistance
- [ ] Errors identified clearly
- [ ] Labels/instructions provided
- [ ] Error suggestions given
- [ ] Error prevention for legal/financial

=== PROCEDURE: Robust Checklist ===

### 4.1 Compatible
- [ ] HTML is valid
- [ ] Name, role, value available
- [ ] Status messages announced

=== PROCEDURE: Testing Tools ===

**Automated Testing:**
```bash
# axe-core (browser extension or CLI)
npx @axe-core/cli https://example.com

# Pa11y
npx pa11y https://example.com

# Lighthouse
npx lighthouse https://example.com --only-categories=accessibility
```

**Manual Testing:**
1. **Keyboard navigation** - Tab through entire page
2. **Screen reader** - Test with NVDA/VoiceOver/JAWS
3. **Zoom** - Test at 200% and 400%
4. **Color blindness** - Use simulator tools
5. **Motion** - Test with reduced motion enabled

=== PROCEDURE: Audit Report ===

```markdown
# Accessibility Audit Report

**URL/Feature:** [What was audited]
**Standard:** WCAG 2.1 AA
**Auditor:** @ux-designer
**Date:** YYYY-MM-DD

## Summary
- Total issues: X
- Critical: X
- Serious: X
- Moderate: X
- Minor: X

## Tool Results
- axe-core: X issues
- Pa11y: X issues
- Lighthouse score: XX/100

## Manual Testing
- Keyboard: [PASS/FAIL]
- Screen reader: [PASS/FAIL]
- Zoom: [PASS/FAIL]

## Issues

### [Critical] Missing alt text on product images
**WCAG:** 1.1.1 Non-text Content
**Location:** /products page
**Impact:** Screen reader users cannot identify products
**Remediation:** Add descriptive alt text to all product images
**Code example:**
```html
<!-- Before -->
<img src="product.jpg">
<!-- After -->
<img src="product.jpg" alt="Blue cotton t-shirt, front view">
```

### [Serious] Insufficient color contrast
**WCAG:** 1.4.3 Contrast (Minimum)
**Location:** Footer links
**Current ratio:** 2.8:1
**Required ratio:** 4.5:1
**Remediation:** Change text color from #999 to #767676

## Compliance Summary
| Criterion | Status |
|-----------|--------|
| 1.1.1 Non-text Content | FAIL |
| 1.4.3 Contrast | FAIL |
| 2.1.1 Keyboard | PASS |
| ... | ... |
```

=== PROCEDURE: Common Fixes ===

**Images:**
```html
<!-- Informative -->
<img src="chart.png" alt="Sales increased 25% in Q4">

<!-- Decorative -->
<img src="decoration.png" alt="" role="presentation">

<!-- Complex -->
<figure>
  <img src="diagram.png" alt="System architecture">
  <figcaption>Detailed description...</figcaption>
</figure>
```

**Forms:**
```html
<label for="email">Email address</label>
<input id="email" type="email" aria-describedby="email-hint">
<span id="email-hint">We'll never share your email</span>

<!-- Error state -->
<input id="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error" role="alert">Please enter a valid email</span>
```

**Focus:**
```css
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none; /* Remove for mouse users */
}

:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(user-flows) | Accessible flows |
| @skill(usability-review) | Overlapping audit |
| @skill(component-development) | Implementation |
