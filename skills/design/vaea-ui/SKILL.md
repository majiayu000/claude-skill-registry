---
name: vaea-ui
description: >
  VAEA ACM-AI design system enforcer. Auto-triggers on frontend/**/*.tsx, frontend/**/*.css,
  .impeccable.md. Loads VAEA design context, enforces government-grade standards, gates UI story
  completion with mandatory checklist. Use for: frontend components, UI stories, design review
  (/vaea-ui critique|audit), quality pass (/vaea-ui polish), layout/typography (/vaea-ui arrange|typeset),
  responsive adaptation (/vaea-ui adapt), accessibility (/vaea-ui harden), AG Grid theming, risk badges,
  dark mode. Orchestrates: frontend-design, critique, audit, polish, normalize, adapt, clarify, arrange,
  typeset, harden, optimize, ui-ux-pro-max. Triggers on: React, Tailwind, AG Grid, Radix UI, shadcn/ui,
  design tokens, WCAG, ARIA, responsive, dark mode, building grid, ACM grid, job card, mobile card view.
---

# VAEA UI — Design System Enforcer

Single entry point for all design quality on ACM-AI. Orchestrates existing design skills
through VAEA brand constraints.

## Activation Modes

### Mode 1: Auto Context Injection (on file touch)

When ANY agent modifies `frontend/**/*.tsx`, `frontend/**/*.ts`, or `frontend/**/*.css`:

1. Load `.impeccable.md` from project root — this is the design authority
2. Load hard rules from `references/acm-patterns.md` (read that file now)
3. Apply VAEA constraints to all design decisions
4. No review, no checklist — just ensure the agent HAS the knowledge

### Mode 2: Explicit Sub-Command (on invocation)

Invoke with `/vaea-ui <command>` or `/vaea-ui <command> <file-or-scope>`.

### Mode 3: Story Completion Gate (on story-complete)

When a UI story is marked complete, run the mandatory checklist from
`references/design-checklist.md` (read that file now). **BLOCK completion if any
critical item fails.**

---

## Context Gathering Protocol

Before ANY design work, execute these steps in order:

### Step 1: Load Design Context

Read `.impeccable.md` at the project root. This file contains:
- Users and personas (compliance officers, facility managers, assessors)
- Brand personality: Professional, Transparent, Calm
- Emotional tone: Confidence & Trust
- References: Salesforce + Xero
- Anti-references: generic SaaS, legacy .gov.au, over-designed, dense ERP
- 5 design principles
- Full color system with coral expansion rules
- Typography and font loading requirements
- Responsive strategy (true responsive, card view on mobile for grids)
- Motion direction (invest in framer-motion)
- Accessibility target (WCAG 2.2 AAA aspirational)

If `.impeccable.md` does not exist, run `/teach-impeccable` first. STOP and do not
proceed without design context.

### Step 2: Load ACM Component Patterns

Read `references/acm-patterns.md` in THIS skill directory. Contains hard rules with
code examples for:
- AG Grid theming (must use `.ag-theme-custom` from globals.css)
- Risk badge dual encoding (icon + color, never color alone)
- Mobile card fallback (card view below md breakpoint)
- Font loading (next/font, not Google Fonts link tags)
- ARIA patterns (specific to ACM components)
- Coral usage (CTAs, badges, notifications — expanded role)
- Government design patterns (12px radius, teal shadows, acknowledgment footer)

### Step 3: Load Dependency Skills

Load these skills for their specialized knowledge, filtered through VAEA constraints:

| Skill | Load When | VAEA Override |
|-------|-----------|---------------|
| `ui-ux-pro-max` | Creating new components or pages | Filter palettes to VAEA teal/coral/gold only. Filter fonts to Inter + JetBrains Mono only. Use Next.js 15 + React 19 stack. |
| `frontend-design` | Any visual design work | Skip its Context Gathering (we already loaded .impeccable.md). Apply its AI Slop Test. |
| `baseline-ui` | CSS/Tailwind validation | Merge its constraints with ACM-specific rules. |
| `taste-skill` | Creative component work | Use its anti-AI-slop rules. Override its font bans (Inter IS our font). Set DESIGN_VARIANCE=5, MOTION_INTENSITY=6, VISUAL_DENSITY=7 (data-dense). |

---

## Curated Command Sheet

10 commands tuned for ACM-AI's "Professional, Transparent, Calm" personality.

### Evaluation

#### `/vaea-ui critique [file|scope]`
Evaluate design effectiveness. Loads `critique` skill internally.
- Assesses: visual hierarchy, information architecture, emotional resonance, design quality
- ACM lens: Does it inspire confidence? Is data scannable? Does it feel like Salesforce/Xero?
- Leads to: `/vaea-ui polish`, `/vaea-ui arrange`, `/vaea-ui typeset`

#### `/vaea-ui audit [file|scope]`
Comprehensive quality audit. Loads `audit` skill internally.
- Checks: accessibility (WCAG 2.2 AAA), performance, theming, responsive, anti-patterns
- ACM lens: Dual-encoded risk indicators? AG Grid theme from globals.css? Mobile card fallback?
- Leads to: `/vaea-ui normalize`, `/vaea-ui harden`, `/vaea-ui optimize`, `/vaea-ui adapt`

### Quality

#### `/vaea-ui polish [file|scope]`
Final quality pass before shipping.
- Fixes: alignment, spacing, consistency, detail issues
- ACM lens: Design token usage (no raw hex/px), VAEA shadow system, consistent border-radius

#### `/vaea-ui harden [file|scope]`
Improve interface resilience.
- Fixes: error handling, text overflow, edge cases, loading/empty/error states
- ACM lens: ConnectionGuard patterns, ErrorBoundary on every page, Skeleton matching final layout

#### `/vaea-ui normalize [file|scope]`
Normalize to match VAEA design system.
- Fixes: inconsistent token usage, off-brand colors, wrong component variants
- ACM lens: oklch tokens only, VAEA teal palette, branded teal-tinted dark mode

#### `/vaea-ui optimize [file|scope]`
Improve interface performance.
- Fixes: loading speed, rendering, animations, images, bundle size
- ACM lens: AG Grid lazy loading, React Query staleTime tuning, next/font migration, route prefetching

### Adaptation

#### `/vaea-ui adapt [file|scope]`
Adapt for different screen sizes and devices.
- Fixes: responsive behavior, touch targets, grid-to-card transitions
- ACM lens: AG Grid to card view below md, Sheet for mobile chat, collapsible sidebar, pinned columns

#### `/vaea-ui clarify [file|scope]`
Improve UX copy and microcopy.
- Fixes: labels, error messages, instructions, tooltips, empty states
- ACM lens: Government tone (direct, factual, no jargon), status messages state facts, errors explain next step

### Layout & Typography

#### `/vaea-ui arrange [file|scope]`
Improve layout, spacing, and visual rhythm.
- Fixes: monotonous grids, inconsistent spacing, weak visual hierarchy
- ACM lens: 4px spacing grid, BentoGrid for dashboards, data density over whitespace in grids

#### `/vaea-ui typeset [file|scope]`
Improve typography.
- Fixes: font choices, hierarchy, sizing, weight consistency, readability
- ACM lens: Inter for body, JetBrains Mono for data, Text component variants, tabular-nums for numbers

---

## Hard Rules (Non-Negotiable)

These rules MUST be followed. Violations block story completion.

### 1. Design Tokens Only
```
NEVER: className="text-[#53A69D]" or style={{ color: '#53A69D' }}
ALWAYS: className="text-primary" or className="text-vaea-teal-300"
```

### 2. AG Grid Theme from globals.css
```
NEVER: <style jsx global>{`.ag-theme-alpine { ... }`}</style>
ALWAYS: className="ag-theme-custom" (defined once in globals.css)
```

### 3. Risk Indicators Dual Encoded
```
NEVER: <Badge className="bg-risk-high">High</Badge>
ALWAYS: <Badge className="bg-risk-high"><XCircle className="h-3 w-3 mr-1" />High</Badge>
```

### 4. Mobile Card Fallback for Grids
```tsx
// Below md: card stack. Above md: AG Grid.
{isMobile ? <RecordCardList records={records} /> : <DataGrid ... />}
```

### 5. Font Loading via next/font
```
NEVER: <link href="https://fonts.googleapis.com/css2?family=Inter..." />
ALWAYS: import { Inter } from 'next/font/google'
```

### 6. Coral for CTAs and Important Actions
```
NEVER: Primary CTA using only teal
ALWAYS: Important actions, notification dots, critical badges use vaea-coral
```

### 7. ARIA on All Interactive Elements
```
NEVER: <button onClick={...}><Search /></button>
ALWAYS: <button onClick={...} aria-label="Search records"><Search /></button>
```

### 8. Text Component for Typography
```
NEVER: <h2 className="text-2xl font-bold">Title</h2>
ALWAYS: <Text variant="h2">Title</Text>
```

### 9. Teal-Tinted Dark Mode
```
NEVER: Dark mode backgrounds using neutral grey (oklch(0.15 0 0))
ALWAYS: Dark mode backgrounds with teal tint (oklch(0.175 0.025 170))
```

### 10. Aboriginal Acknowledgment in Footer
Victorian government requirement. Always present via `branding.ts` config.

---

## Story Completion Gate

When a UI story is marked complete, the agent MUST run the mandatory design checklist.
Read `references/design-checklist.md` for the full checklist.

**Quick summary — ALL must pass:**

- [ ] Design tokens used (no raw hex/px values)
- [ ] Responsive: tested at mobile (< 640px), tablet (768px), desktop (1280px+)
- [ ] Dark mode: verified in both light and dark themes
- [ ] ARIA: all interactive elements have labels, roles, states
- [ ] Risk indicators: dual encoded (icon + color) if applicable
- [ ] AG Grid: uses `.ag-theme-custom` from globals.css, no inline styles
- [ ] Typography: uses `<Text>` component variants, not raw heading tags
- [ ] Loading states: Skeleton components matching final layout structure
- [ ] Error states: ErrorBoundary + meaningful fallback on every page/section
- [ ] Mobile grids: card view fallback below md breakpoint if AG Grid is used

If ANY critical item fails, the story is **INCOMPLETE**. Fix before marking done.

---

## AI Slop Test

Before submitting any UI work, ask yourself:

> "If someone saw this and said 'AI made this,' would they believe it immediately?"

If yes, that's the problem. Check for:
- Generic card-in-card nesting
- Uniform card grids with no visual hierarchy
- Purple/blue gradient text
- Glassmorphism everywhere
- Centered hero metric layout
- Sparklines as decoration
- Bounce/elastic animations
- Dark mode with glowing neon accents

ACM-AI should feel like it was designed by a government UX team that cares deeply about
data quality — not generated by an AI coding assistant.

---

## File Reference

| File | When to Load |
|------|-------------|
| `.impeccable.md` (project root) | Always — design authority |
| `references/acm-patterns.md` | When implementing components |
| `references/design-checklist.md` | At story completion |
