---
name: frontend-production-quality
description: 'Use before implementing UI changes or frontend PRs. Enforces TodoWrite
  with 18+ items. Triggers: "accessibility audit", "WCAG", "Lighthouse", "screen reader",
  "a11y", "NVDA", "VoiceOver", "keyboard na'
---

---
name: frontend-production-quality
description: Use before implementing UI changes or frontend PRs. Enforces TodoWrite with 18+ items. Triggers: "accessibility audit", "WCAG", "Lighthouse", "screen reader", "a11y", "NVDA", "VoiceOver", "keyboard navigation", "focus indicator". For "Core Web Vitals" in frontend/UI context, use this skill. For pure backend/API performance optimization, use performance-optimization instead. If thinking "WIP doesn't need this" - use it anyway.
---

# Frontend Production Quality

## MANDATORY FIRST STEP

**CREATE TodoWrite** with 3 sections (18+ items total):
- **Accessibility (WCAG 2.1 AA)**: 8+ items
- **Performance (Core Web Vitals)**: 6+ items
- **Evidence Collection**: 4+ items

Do not design, implement, or review until TodoWrite is created and verified.

---

## WIP Code is NOT an Exception

🚨 **CRITICAL: If thinking "I'll commit this now and finish accessibility before code review/merge/deploy"** → STOP

- 80% of "I'll finish it later" items never get finished
- Code review often approves incomplete work under pressure
- "WIP" becomes "deployed" without completing deferred items

**If you can't complete the work now:**
1. `git stash push -m "WIP: feature - needs accessibility verification"`
2. Finish tomorrow
3. Commit only when complete

**Never commit incomplete work.**

---

## Emergency Protocol (10-minute minimum)

If production is down and rollback impossible:

```
Emergency Verification (10 min):
1. axe CLI accessibility scan (2 min)
2. Manual functional test + keyboard nav (3 min)
3. Lighthouse audit (2 min)
4. Visual inspection - contrast, focus indicators (3 min)

If ANY issues found: DO NOT DEPLOY. Fix first or rollback.
```

Post-deployment (within 24 hours): Full accessibility audit, Core Web Vitals measurement, incident ticket.

---

## Verification Checkpoint

After creating TodoWrite, verify 3 random items pass this test:

**For each item, ALL THREE must be YES:**
- Has concrete numbers/thresholds? (LCP < 2.5s, 4.5:1 contrast, tab order 1-5)
- Names specific tools/technologies? (NVDA, WebAIM, Lighthouse, `<button>`)
- States measurable outcome? (NVDA announces 'Submit button', Lighthouse A11y = 100)

**If any NO → revise items before proceeding.**

---

## TodoWrite Requirements

### Accessibility (WCAG 2.1 AA) - 8+ items

- [ ] **Semantic HTML**: `<button>`, `<a>`, `<input>` instead of `<div onClick>`
- [ ] **ARIA labels**: `aria-label`, `aria-labelledby` where semantic HTML insufficient
- [ ] **Keyboard navigation**: All interactive elements via Tab/Shift+Tab. Document tab order.
- [ ] **Focus indicators**: 2px solid border, 3:1 contrast minimum
- [ ] **Color contrast**: 4.5:1 body text, 3:1 large text (WebAIM checker)
- [ ] **Screen reader testing**: NVDA (Windows) or VoiceOver (Mac)
- [ ] **Heading hierarchy**: h1 → h2 → h3, no skips, one h1 per page
- [ ] **Form labels**: Every `<input>` has `<label>` or `aria-label`

### Performance (Core Web Vitals) - 6+ items

- [ ] **Baseline measurement**: Current LCP, FID, CLS before changes
- [ ] **LCP < 2.5s**: Largest Contentful Paint
- [ ] **FID < 100ms**: First Input Delay
- [ ] **CLS < 0.1**: Cumulative Layout Shift
- [ ] **Bundle size**: Document impact, justify if >10KB increase
- [ ] **Lazy loading**: Images `loading="lazy"`, non-critical JS on-demand

### Evidence Collection - 4+ items

- [ ] **Lighthouse A11y = 100**: Screenshot with URL, date
- [ ] **Lighthouse Perf ≥ 90**: Screenshot with Core Web Vitals
- [ ] **Keyboard tab order**: List order + focus indicator description
- [ ] **Screen reader results**: What NVDA/VoiceOver announced

---

## Specificity Test

**For EACH item, ask: "Could an engineer implement without clarifying questions?"**

| ❌ Fails Test | ✅ Passes Test |
|--------------|---------------|
| "Check accessibility" | "Semantic HTML: Replace `<div onClick>` with `<button>`, verify NVDA announces 'button'" |
| "Test performance" | "Core Web Vitals: LCP < 2.5s on 3G throttle using Lighthouse" |
| "Test keyboard navigation" | "Tab order: 1. Email input, 2. Password input, 3. Submit button. Each has 2px solid #0056b3 focus border" |

---

## Red Flags - STOP When You Think:

| Thought | Reality |
|---------|---------|
| "We'll add accessibility later" | 80% never added. Retrofit costs 3-5x more. |
| "Design is approved, just implement" | Design approval doesn't override WCAG 2.1 AA (legal requirement) |
| "Internal tooling, less critical" | ADA applies to employees |
| "It's just a commit, not deploy" | Commits become deploys. 80% of "later" never happens |
| "Code review will catch it" | YOU are the quality gate. Code review is backup. |
| "I'll finish before code review" | Finish before committing. |

---

## Response Templates

### "We'll Add Accessibility Later"

❌ **BLOCKED**: Cannot defer accessibility.

- 80% of "later" items never get added
- Retrofit costs 3-5x more
- ADA lawsuits cost $20K-100K+

**Required to override:**
1. Specific retrofit date (not "later")
2. Budget allocated (engineer-weeks)
3. Risk acceptance signed by decision maker

### Skipping Core Web Vitals

❌ **BLOCKED**: Cannot mark complete without measurement.

**Required:**
- Lighthouse audit (Perf ≥ 90, A11y = 100)
- Core Web Vitals on 3G: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Bundle size documented

Takes 5 minutes. Not optional.

---

## Final Self-Grading

Before claiming complete:

```
[ ] 18+ items across 3 sections (A11y 8+, Perf 6+, Evidence 4+)
[ ] 80%+ items have concrete numbers/thresholds
[ ] 80%+ items name specific tools
[ ] 100% items have measurable outcomes
[ ] Tested 3 random items - all passed specificity test
[ ] WCAG 2.1 AA criteria explicitly specified
[ ] Core Web Vitals targets specified

Score 7+/8: Ready to proceed
Score <7: Revise TodoWrite before implementation
```

---

## Verification Checklist (Before Complete)

**Accessibility:**
- [ ] DevTools accessibility check (0 violations)
- [ ] Keyboard navigation entire feature
- [ ] Screen reader test (NVDA/VoiceOver)
- [ ] Color contrast verified (all text 4.5:1+)

**Performance:**
- [ ] Lighthouse: Performance ≥ 90, Accessibility = 100
- [ ] Core Web Vitals on 3G: LCP < 2.5s, FID < 100ms, CLS < 0.1
- [ ] Bundle size impact documented

**Evidence:**
- [ ] Lighthouse screenshots
- [ ] Keyboard tab order documented
- [ ] Screen reader announcements documented

**Failure to provide evidence = work is not complete.**
