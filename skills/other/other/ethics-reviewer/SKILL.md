---
name: ethics-reviewer
description: This skill should be used when the user mentions "dark patterns", "accessibility", "a11y", "privacy", "tracking", "analytics", "notifications", "user data", "GDPR", "consent", "manipulation", "sustainability", "performance budget", or when building user-facing features that collect data, send notifications, display urgency, or gate access. Addresses ethical constraints in software design — manipulation, accessibility, privacy, and sustainability.
version: 1.0.0
---

# Ethics Reviewer

Passive ethical review skill. Activates when user-facing features touch the four ethical concerns: manipulation, accessibility, privacy, and sustainability. Checks designs and implementations against principled constraints without requiring explicit invocation.

---

## When This Skill Applies

Use this skill when:
- Building forms that collect personal data
- Implementing notifications, emails, or alerts
- Designing pricing pages, upgrade flows, or paywalls
- Adding analytics, tracking, or telemetry
- Creating urgency mechanisms (countdowns, scarcity indicators)
- Implementing accessibility-sensitive UI (navigation, forms, modals)
- Making performance decisions that affect device/network inclusivity
- The conversation involves user-facing features of any kind

**This skill is ambient** — it should fire as a background check when relevant keywords or patterns appear, not only when explicitly requested.

---

## The Four Ethical Constraints

### 1. No Manipulation

Software should amplify the user, not exploit them.

**Red flags**:
- Confirmshaming ("No thanks, I don't want to save money")
- Hidden opt-outs (pre-checked boxes, buried unsubscribe)
- Artificial urgency ("Only 2 left!" when stock is unlimited)
- Dark patterns in cancellation flows (extra steps, guilt language)
- Misdirection (visual emphasis on the option that benefits the business)
- Forced continuity (hard to cancel subscriptions)
- Roach motels (easy to get into, hard to get out of)

**Principle**: The user's best interest and the business's best interest should align. If they diverge, side with the user.

**Check**:
- Would the user feel tricked if they understood the full mechanism?
- Is the easiest path also the one that serves the user?
- Can the user reverse this action as easily as they took it?

### 2. Accessibility as Default

If someone can't use it, it doesn't work.

**Requirements** (not aspirations):
- Semantic HTML (headings, landmarks, labels, roles)
- Keyboard navigable (all interactive elements reachable via Tab/Enter/Escape)
- Screen reader compatible (meaningful alt text, aria-labels where semantic HTML isn't enough)
- Colour contrast ratios meet WCAG 2.1 AA minimum (4.5:1 for normal text, 3:1 for large text)
- Focus indicators visible
- Error messages associated with inputs (aria-describedby or aria-errormessage)
- No information conveyed by colour alone
- Reduced motion support (`prefers-reduced-motion`)

**Check**:
- Can a keyboard-only user complete this flow?
- Does every image/icon have appropriate alt text or aria-label?
- Does the colour scheme pass contrast checks?
- Are form errors announced to screen readers?

### 3. Privacy by Default

Collect the minimum. Store it carefully. Be transparent about it.

**Principles**:
- **Data minimisation**: Only collect what's needed for the feature to work
- **Purpose limitation**: Don't repurpose data without consent
- **Transparent collection**: Tell users what's collected and why
- **Secure storage**: Encrypt sensitive data, use environment variables for secrets
- **Right to delete**: Users can remove their data
- **No silent tracking**: Analytics require disclosure; no hidden telemetry

**Red flags**:
- Collecting email "for later" without a clear purpose
- Tracking user behaviour without disclosure
- Storing data you don't actively need
- Third-party scripts that phone home with user data
- Cookies set before consent given

**Check**:
- What data does this feature collect?
- Is all of it necessary for the feature to work?
- Is the user informed about the collection?
- Can the user opt out without losing core functionality?
- Is sensitive data encrypted at rest and in transit?

### 4. Sustainability

Software that wastes resources wastes everyone's time and energy.

**Principles**:
- **Performance budgets**: Set limits on page weight, load time, bundle size
- **Device inclusivity**: Don't require flagship hardware; test on constrained devices
- **Network inclusivity**: Work on slow connections; progressive enhancement
- **Efficient queries**: Avoid N+1, over-fetching, unnecessary computation
- **Lazy loading**: Don't load what's not visible
- **Caching strategy**: Don't re-fetch what hasn't changed

**Check**:
- Does this feature degrade gracefully on slow connections?
- Is the bundle size impact proportional to the feature's value?
- Are images/assets appropriately sized and lazy-loaded?
- Are database queries efficient? (No N+1, appropriate indexes)

---

## How to Apply

This skill doesn't produce a standalone output. It **annotates** other work:

### During Design
When discussing a feature, flag ethical concerns inline:
```
⚠️ Ethics: This notification flow sends emails on a schedule the user didn't choose.
Consider: opt-in frequency selection, easy one-click unsubscribe.
```

### During Implementation
When reviewing or writing code, flag issues:
```
⚠️ Ethics (accessibility): This modal traps focus but doesn't return focus
to the trigger element on close.
```

### During Review
When assessing completed work:
```
⚠️ Ethics (privacy): This analytics call sends the user's full name to a
third-party service. Consider sending an anonymised ID instead.
```

---

## Severity Levels

Not all ethical concerns are equal. Use these to calibrate:

**Must fix** (blocks shipping):
- Keyboard traps (user literally cannot proceed)
- Data collection without disclosure
- Dark patterns that exploit vulnerable users
- Missing alt text on functional images
- WCAG AA contrast failures on primary UI

**Should fix** (fix before v1):
- Missing reduced-motion support
- Overly broad data collection (works but collects more than needed)
- Cancellation flows with unnecessary friction
- Images without descriptive alt text (decorative is fine)
- Large bundle sizes on critical paths

**Consider** (improve over time):
- Enhanced screen reader experience beyond minimum
- Performance optimisation for constrained devices
- Additional privacy controls beyond legal requirements
- WCAG AAA contrast compliance

---

## Integration Points

### With domain-modeller
When the domain model includes personal data entities (User, Profile, Preferences), ethics-reviewer flags data minimisation and privacy concerns.

### With frontend-styler
Accessibility checks integrate directly into styling work — contrast, focus indicators, semantic structure.

### With api-designer
Privacy-by-default patterns in API design — no excessive data in responses, secure defaults, proper auth scoping.

### With testing-obsessive
Accessibility testing is part of the testing strategy — automated a11y checks, keyboard navigation tests, screen reader verification.

---

## Quick Reference Checklist

Before shipping any user-facing feature:

- [ ] **Manipulation**: Would the user feel tricked? Is the easiest path the honest one?
- [ ] **Accessibility**: Can a keyboard/screen-reader user complete this flow?
- [ ] **Privacy**: Is data collection minimal, disclosed, and deletable?
- [ ] **Sustainability**: Does this work on slow connections and modest hardware?

---

## Success Criteria

Ethics review is effective when:
- Concerns are caught during design, not after launch
- The team treats accessibility as a requirement, not a nice-to-have
- Users can understand, control, and delete their data
- No dark patterns exist in the product
- The software works for people with different abilities, devices, and connections
