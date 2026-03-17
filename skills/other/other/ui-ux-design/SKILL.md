---
name: ui-ux-design
description: "Create production-grade frontend interfaces with strong UX and visual craft. Use when building web components, pages, dashboards, forms, landing pages, or any UI. Use when user says 'build a form', 'create a dashboard', 'design a component', 'make a landing page', or asks for UI/UX work."
allowed-tools: Read, Write, Edit
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Check if UI/UX task is complete based on what was asked. If task was advice/consultation only - no code checklist applies. If code was written: verify interactive states, semantic HTML, focus states, labels (for forms), and contrast were considered for what was built. Only flag missing items that apply to the specific output. Respond {\"ok\": true} if done, or {\"ok\": false, \"reason\": \"specific missing item\"} if not."
---

# UI/UX Design

Create functional, accessible, visually distinctive interfaces. Output is working code.

## When to Use

**Activate automatically when:**

- User requests UI components, pages, or applications
- User mentions forms, dashboards, landing pages, modals
- User asks to "design", "build", or "create" any interface
- User wants to improve existing UI/UX

## Workflow

### Step 1: Assess Context

Before coding, identify (internal reasoning):

- Problem being solved
- Target users
- Aesthetic direction (see [REFERENCES.md](REFERENCES.md#aesthetic-directions))
- Constraints (framework, brand, accessibility level)

### Step 2: Consult References

Fetch implementation values from [REFERENCES.md](REFERENCES.md):

- Color palette (with WCAG-compliant values)
- Font pairing
- Component patterns (button, input, card, etc.)
- Spacing and typography tokens

### Step 3: Generate Code

Produce working implementation with:

- All interactive states (hover, focus, active, disabled, loading, error)
- Semantic HTML (button, nav, main—not div soup)
- Mobile-first responsive design
- CSS variables for maintainability

### Step 4: Verify

Run through checklist before delivering.

## Output Requirements

| Requirement | Standard |
|-------------|----------|
| Contrast | 4.5:1 text, 3:1 UI components |
| Focus states | Visible outline on all interactive elements |
| Touch targets | Minimum 44×44px |
| Reduced motion | Respect `prefers-reduced-motion` |
| Labels | All inputs have associated labels |
| Empty states | Helpful message + clear action |
| Error states | Explain what happened + how to fix |

## Aesthetic Directions

Match to context. See [REFERENCES.md](REFERENCES.md#aesthetic-directions) for characteristics.

| Style | Best For |
|-------|----------|
| Minimalism | Productivity, professional, portfolios |
| Glassmorphism | Dashboards, tech products |
| Neubrutalism | Creative, startups, distinctive brands |
| Editorial | Content sites, publications |
| Organic | Consumer apps, wellness, community |
| Dark Mode | User preference, low-light contexts |

## Anti-Patterns

Avoid these markers of generic AI output:

- Purple/blue gradients on white
- Inter/Roboto/system fonts everywhere
- Cookie-cutter card layouts
- Rounded rectangles with soft shadows on everything
- Color-only meaning (no icons/text backup)
- Removed focus outlines
- Error messages without solutions

## Checklist

Copy and track:

```
- [ ] Context assessed (problem, users, aesthetic direction)
- [ ] REFERENCES.md consulted for palette + fonts
- [ ] All interactive states implemented
- [ ] Loading and error states included
- [ ] Contrast meets WCAG AA
- [ ] Semantic HTML used
- [ ] Focus states visible
- [ ] Form inputs labeled
- [ ] prefers-reduced-motion respected
- [ ] Responsive breakpoints tested
- [ ] Empty states handled
```

## Recovery

| Issue | Action |
|-------|--------|
| User dislikes direction | Propose 2-3 alternatives from Aesthetic Directions |
| Looks too generic | Check Anti-Patterns, apply distinctive typography |
| Accessibility concerns | Verify contrast, focus states, semantic HTML |
| States incomplete | Walk through checklist systematically |

---

> **License:** MIT - See LICENSE for complete terms
> **Author:** Arvind Menon
