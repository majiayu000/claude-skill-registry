---
name: software-ui-ux-design
description: UI/UX design principles, accessibility standards, resilient state patterns, platform constraints, and design system practices for modern software interfaces.
---

# Software UI/UX Design Skill — Quick Reference

Use this skill when the primary focus is designing intuitive, accessible, and user-centered interfaces. For research planning/synthesis, use `software-ux-research`.

---

## Dec 2025 Baselines (Core)

- **Accessibility baseline**: WCAG 2.2 Level AA (W3C Recommendation, 12 Dec 2024) https://www.w3.org/TR/WCAG22/
- **EU shipping note**: European Accessibility Act applies to covered products/services after 28 Jun 2025 (Directive (EU) 2019/882) https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L0882
- **Web performance UX baseline**: Core Web Vitals stable set is `LCP` (≤2.5s), `INP` (≤200ms), `CLS` (≤0.1) https://web.dev/vitals/
- **Design system interoperability**: Prefer token-first foundations aligned to Design Tokens Community Group Technical Reports 2025.10 https://tr.designtokens.org/
- **Platform constraints**: Use Apple HIG and Material 3 as primary sources: https://developer.apple.com/design/human-interface-guidelines/ and https://m3.material.io/

## When to Use This Skill

Invoke when users ask for:

- UI/UX design patterns and best practices
- Usability evaluation and improvement recommendations
- Accessibility compliance (WCAG, ARIA)
- Design system setup and component patterns
- User-centered design methodologies
- Information architecture and navigation design
- Mobile-first and responsive design patterns
- Form design and input validation UX
- **Pattern selection based on user pain points** (from `software-ux-research` analysis)
- **UI fixes for feedback-identified issues** (navigation, onboarding, performance, forms)

---

## Operating Mode (Core)

If inputs are missing, ask for: users + top tasks, platforms (web/iOS/Android/desktop), IA depth, accessibility target, performance constraints, and any evidence (screenshots, URLs, analytics, tickets, prior research).

Default outputs (pick what the user asked for):
- UX review checklist → prioritized issues → recommendations + acceptance criteria
- Flow + state spec (happy path + edge/error/empty/loading/offline/degraded) with acceptance criteria
- Design system delta spec (tokens + components + states) with governance-ready contribution plan

## Core Interaction Design

### Interaction Checklist (Do / Avoid / Acceptance Criteria)

| Goal | Do | Avoid | Acceptance Criteria |
|------|----|-------|---------------------|
| Clarity | One primary action per view; front-load labels | Competing CTAs; ambiguous verbs | User can state next step in 5 seconds [Inference] |
| Affordances | Use native controls; strong signifiers | Clickable `<div>`; hover-only cues | All actions are discoverable without hover |
| Feedback | Immediate visual response on input | Silent taps/clicks | Every action has an observable state change |
| Error prevention | Constrain inputs; show examples | “Submit then fail” patterns | Invalid states are hard to create |
| Error recovery | Specific message + next step | “Something went wrong” only | Every error offers retry/undo/support path |
| Safe defaults | Preselect safest option; make destructive explicit | Risky defaults; hidden consequences | Destructive actions are confirmed or reversible |
| Consistency | Reuse patterns and terms | Same term used for different concepts | Pattern library covers common flows |

## Decision Tree: UI/UX Design Approach

```text
Design challenge: [Feature Type]
    ├─ Need to decide what to build? → Use software-ux-research first
    ├─ Improving an existing UI?
    │   ├─ Usability issues? → Heuristic review (resources/nielsen-heuristics.md)
    │   ├─ Accessibility gaps? → WCAG 2.2 audit (resources/wcag-accessibility.md)
    │   └─ Inconsistency? → Design system alignment (resources/design-systems.md)
    ├─ Building a new flow?
    │   ├─ Define states → loading/empty/error/offline/degraded
    │   ├─ Define recovery → retry/cancel/undo/support
    │   └─ Define telemetry → success, error, time, abandonment
    └─ Platform constraints?
        ├─ Web → semantics + focus + reflow
        ├─ iOS → system navigation + Dynamic Type
        ├─ Android → Material patterns + back/edge-to-edge
        └─ Desktop → shortcuts + selection models
```

---

## Information Architecture (Scalable Products)

### IA Checklist

- [ ] Identify primary user roles and their top tasks (by frequency and criticality).
- [ ] Define content types (nouns) and actions (verbs); avoid mixing.
- [ ] Choose navigation model: global (app-level) vs local (within a section).
- [ ] Ensure findability at scale: search, filters, sort, saved views.
- [ ] Label in user language; include short helper text where needed.
- [ ] Plan permissions/visibility states: “no access”, “request access”, “limited view”.

### Common IA Anti-Patterns

| Anti-pattern | Why it fails | Better |
|-------------|--------------|--------|
| Deep nesting (“6 clicks deep”) | Recall burden, lost context | Flatter IA + search + saved views |
| Hamburger-only desktop nav | Hidden affordance for frequent tasks | Visible primary nav + overflow |
| Filters without “clear/reset” | Traps users in empty results | Clear-all + applied-filter chips |

## Platform Constraints & Anti-Patterns

### Web (Browser-Based)

| Do | Avoid | Rationale |
|----|-------|-----------|
| Use semantic HTML first | “div soup” interaction | A11y and reliability (WAI-ARIA APG) https://www.w3.org/WAI/ARIA/apg/ |
| ARIA only when needed | ARIA overrides for native controls | “No ARIA is better than bad ARIA” (WAI-ARIA APG) https://www.w3.org/WAI/ARIA/apg/ |
| Manage focus on SPA navigation | Focus resets to `<body>` | Preserves context (WCAG 2.4.3/2.4.7) https://www.w3.org/TR/WCAG22/ |
| Visible focus + non-obscured focus | Focus hidden by sticky UI | WCAG 2.4.7 + 2.4.11 https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum |
| Reflow at 320 CSS px | Fixed-width layouts | WCAG 1.4.10 Reflow https://www.w3.org/TR/WCAG22/#reflow |
| Provide non-drag alternatives | Drag-only interactions | WCAG 2.5.7 https://www.w3.org/TR/WCAG22/#dragging-movements |
| Minimum target size | Tiny hit targets | WCAG 2.5.8 https://www.w3.org/TR/WCAG22/#target-size-minimum |

**Browser-Specific Gotchas:**

- Safari: `datetime-local` input limited; custom date picker needed
- Firefox: `:focus-visible` support differs; test across browsers
- Chrome: `autocomplete` behavior inconsistent with custom forms

### iOS / iPadOS (Apple HIG)

| Do | Avoid | Rationale |
|----|-------|-----------|
| Use system navigation patterns (tab bar, navigation bar) | Custom navigation paradigms | User muscle memory |
| Support Dynamic Type (accessibility text scaling) | Fixed font sizes | iOS accessibility requirement |
| Implement pull-to-refresh for list views | Custom refresh gestures | iOS convention since 2011 |
| Use SF Symbols for icons | Custom icon sets for standard actions | System consistency |
| Support dark mode and system materials | Light-only designs | Platform coherence |
| Handle Safe Areas (notch, Dynamic Island) | Assume full-screen content | Content occlusion |
| Prefer system controls for text entry, pickers, permissions | Custom re-implementations | Better a11y and IME behavior |

### Android (Material Design 3)

| Do | Avoid | Rationale |
|----|-------|-----------|
| Use Material 3 components (FAB, bottom sheets, chips) | iOS-style patterns (tab bar at bottom for primary nav) | Platform identity |
| Support Dynamic Color (Material You) | Hardcoded brand colors only | Android 12+ personalization |
| Implement edge-to-edge content | System bar padding hacks | Modern Android aesthetic |
| Use navigation rail on tablets | Phone UI stretched to tablet | Large screen guidance https://developer.android.com/large-screens |
| Handle back gesture (predictive back) | Block system back navigation | Predictive back gesture https://developer.android.com/guide/navigation/predictive-back-gesture |
| Support split-screen/foldables | Assume single-window only | Samsung Fold, Pixel Fold |

**Android-Specific:**

- Test on Samsung One UI (modified Material)
- Handle varying display densities (mdpi to xxxhdpi)
- Support both gesture and 3-button navigation

### Desktop (Windows/macOS/Linux)

| Do | Avoid | Rationale |
|----|-------|-----------|
| Support keyboard shortcuts with discoverability | Mouse-only interactions | Power user efficiency |
| Implement proper window resize behavior | Fixed-size windows | Desktop user expectation |
| Support multi-window/multi-monitor | Assume single viewport | Desktop workflow |
| Provide hover states for all interactive elements | Touch-first design without hover | Desktop has hover capability |
| Support right-click context menus | Hamburger menus for all actions | Desktop convention |
| Handle high-DPI displays (Retina, 4K) | 1x assets only | Blurry icons/images |
| Implement selection models (click, shift-click, cmd/ctrl-click) | Single-select only in lists | Desktop productivity patterns |

---

## State-Heavy UI Patterns

### State Matrix: Required States for All Interactive Views

| State | Visual Treatment | When to Show | Duration |
|-------|------------------|--------------|----------|
| **Loading** | Placeholder matching layout; label if blocking | Data fetching | Until data arrives or times out |
| **Empty** | Message + next step + CTA | Zero items, no data | Until content exists |
| **Partial Data** | Show available content + placeholders | Incremental loads | Until complete |
| **Error** | Alert with specific message + retry action | Request fails, validation fails | Until user dismisses or retries |
| **Success** | Inline confirmation or toast | Action completes | Context-dependent |
| **Offline** | Banner with status + cached data indicator | Network unavailable | Until reconnection |
| **Degraded** | Warning badge + limited functionality notice | Partial system failure | Until service restored |
| **No Access** | Explain + request path | Missing permissions | Until access granted |

### Loading State Decision Tree

```text
Data fetch initiated
    ├─ Fast → pressed/disabled state only
    ├─ Noticeable → inline placeholder
    └─ Long-running → progress + cancel + background option
```

### Empty State Checklist

- [ ] Illustration/icon relevant to context (not generic)
- [ ] Clear headline explaining the state
- [ ] Supporting text with next steps
- [ ] Primary CTA to resolve empty state
- [ ] Avoid "No data found" without guidance

### Error State Severity Levels

| Level | Example | Treatment | User Action |
|-------|---------|-----------|-------------|
| **Recoverable** | Network timeout | Inline warning + retry | Retry button |
| **Correctable** | Invalid email format | Field-level error | Fix input |
| **Blocking** | 500 server error | Full-page error | Contact support / retry later |
| **Partial** | Some items failed to load | Inline notice per item | Retry individual items |

---

## Long-Running Operations

### Pattern: Operations >10 Seconds

For uploads, exports, batch processing, and migrations:

| Element | Implementation | Example |
|---------|----------------|---------|
| **Progress** | Determinate if known, indeterminate if unknown | "Uploading 3 of 10 files (30%)" |
| **Cancel** | Always provide cancel option | "Cancel upload" button |
| **Background** | Allow user to navigate away | "Processing in background—we'll notify you" |
| **Resumability** | Support pause/resume for large operations | "Resume upload" after interruption |
| **Notification** | Notify on completion | Toast, badge, or push notification |
| **History** | Show operation history/status | "Recent exports" list |

### Implementation Checklist

- [ ] Show progress percentage or step count if determinable
- [ ] Allow cancel at any point without data loss
- [ ] Support backgrounding (user can navigate away)
- [ ] Provide completion notification (in-app and/or push)
- [ ] Handle interruptions gracefully (network drop, browser close)
- [ ] Show operation history with status and retry option
- [ ] For uploads: show per-file progress, allow skip/retry individual

---

## Performance UX & Latency Budgets

### Perceived Speed Thresholds

Use human response-time thresholds to decide when to show feedback and when to switch to progress indicators (NN/g) https://www.nngroup.com/articles/response-times-3-important-limits/

| Duration | User Perception | UI Response |
|----------|-----------------|-------------|
| ~0.1s | Feels instant | No extra UI beyond direct manipulation feedback |
| ~1s | Flow stays intact | Keep context; show subtle “working” feedback |
| ≥10s | Attention breaks | Show percent-done + cancel + resumability |

### Core Web Vitals (User-Centric Performance)

Core Web Vitals stable set and thresholds (including INP replacing FID as the interaction metric) https://web.dev/vitals/

| Metric | UX Meaning | Design/System Impact |
|--------|------------|----------------------|
| LCP ≤ 2.5s | “Content loads fast” | Reduce hero weight; reserve layout; avoid late-loading fonts |
| INP ≤ 200ms | “UI responds” | Avoid main-thread long tasks; prioritize input responsiveness |
| CLS ≤ 0.1 | “UI doesn’t jump” | Set media dimensions; avoid late injections; stable skeletons |

### Perceived Performance Techniques

| Technique | When to Use | Implementation |
|-----------|-------------|----------------|
| **Optimistic UI** | High-confidence operations | Show success immediately, rollback on failure |
| **Skeleton Screens** | Content loading | Match layout shape of final content |
| **Progressive Loading** | Large datasets | Load critical content first, then enhance |
| **Streaming/Chunked** | Incremental content, long lists | Show content as it arrives |
| **Prefetching** | Predictable navigation | Preload likely next pages on hover/idle |
| **Placeholder Content** | Images, media | Low-res blur-up, dominant color |

### Anti-Patterns

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Spinner for everything | No layout context, feels slower | Skeleton matching content shape |
| Blocking UI during async | User can't interact | Background processing + toast |
| Full-page reload on action | Loses context, slow | Client-side state update |
| No feedback <3 seconds | User thinks action failed | Immediate button state change |

---

## Accessibility & Motion Safety (WCAG 2.2 AA)

### WCAG 2.2 Changes That Impact Product UI

| Requirement | What to Build | Link |
|-------------|---------------|------|
| Focus not obscured (AA) | Keep focus visible with sticky headers/footers | https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum |
| Focus appearance (AA) | Provide a clearly visible focus indicator | https://www.w3.org/TR/WCAG22/#focus-appearance |
| Dragging movements | Provide non-drag alternatives | https://www.w3.org/TR/WCAG22/#dragging-movements |
| Target size (minimum) | Make targets at least 24×24 CSS px (exceptions apply) | https://www.w3.org/TR/WCAG22/#target-size-minimum |
| Consistent help | Keep help mechanisms consistent across pages | https://www.w3.org/TR/WCAG22/#consistent-help |
| Redundant entry | Don’t require re-entering known information | https://www.w3.org/TR/WCAG22/#redundant-entry |
| Accessible authentication | Avoid cognitive-function tests without alternatives | https://www.w3.org/TR/WCAG22/#accessible-authentication-minimum |

### Reduced Motion Support

`prefers-reduced-motion` is defined in Media Queries Level 5 https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion

```css
/* Always provide reduced motion path */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Motion Safety Checklist

- [ ] All animations respect `prefers-reduced-motion`
- [ ] No content flashes >3 times per second (WCAG 2.3.1)
- [ ] Parallax effects have static alternative
- [ ] Auto-playing carousels can be paused
- [ ] No pure-motion conveyed information (add text labels)
- [ ] Avoid large-area color transitions (can trigger vestibular issues)

### Focus Management Requirements

| Scenario | Focus Behavior | Implementation |
|----------|----------------|----------------|
| Modal opens | Focus moves to modal | `trapFocus()` + `aria-modal="true"` |
| Modal closes | Focus returns to trigger | Store and restore `document.activeElement` |
| Route change (SPA) | Focus to main content | `main.focus()` or skip link |
| Toast appears | Announce, don't steal focus | `aria-live="polite"` |
| Error on submit | Focus to first error field | `firstError.focus()` |
| Dynamic content loads | Announce update | `aria-live` region |

### Keyboard Navigation Patterns

| Pattern | Keys | Implementation |
|---------|------|----------------|
| **Roving tabindex** | Arrow keys within composite | Tab to enter widget, arrows to move, Tab to exit |
| **Focus trap** | Tab cycles within region | Modal, dropdown (until dismissed) |
| **Skip links** | Tab → Enter | "Skip to main content" as first focusable |
| **Escape to close** | Esc | Modals, dropdowns, tooltips |
| **Enter/Space to activate** | Enter or Space | Buttons, links, toggles |

---

## Design Tokens (Dec 2025)

### Design Tokens Community Group Format

Standardized token format for design system interoperability (Design Tokens Technical Reports 2025.10) https://tr.designtokens.org/

```json
{
  "color": {
    "primary": {
      "$value": "#0066cc",
      "$type": "color",
      "$description": "Primary brand color"
    },
    "primary-hover": {
      "$value": "{color.primary}",
      "$type": "color",
      "$extensions": {
        "mode": {
          "dark": "#3399ff"
        }
      }
    }
  },
  "spacing": {
    "sm": {
      "$value": "8px",
      "$type": "dimension"
    }
  }
}
```

### Token Architecture

| Layer | Examples | Purpose |
|-------|----------|---------|
| Primitive | `blue-500`, `16px` | Raw values |
| Semantic | `color-primary`, `spacing-sm` | Intent-based |
| Component | `button-bg`, `card-padding` | Component-specific |

### Governance & Contribution Model

| Topic | Policy (Default) | Notes |
|------|-------------------|-------|
| Ownership | Design + Eng co-owners | Shared accountability |
| Versioning | SemVer + changelog | Breaking changes require migration notes |
| Deprecation | “Warn → ship both → remove” | Provide codemods where possible [Inference] |
| Contributions | RFC → design review → implementation → release | Include a11y + QA gates |
| Documentation | Token tables, component API, examples, dos/don’ts | “How to use” beats “what it is” |

---

## Hybrid Input Handling

Modern users switch between mouse, touch, keyboard, trackpad, and stylus—often within a single session.

### Input Detection & Adaptation

Pointer and hover capabilities are defined in Media Queries Level 4 https://www.w3.org/TR/mediaqueries-4/#mf-interaction

```typescript
// Detect primary input modality
const supportsHover = window.matchMedia('(hover: hover)').matches;
const supportsTouch = 'ontouchstart' in window;
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Respond to input changes
window.matchMedia('(pointer: coarse)').addEventListener('change', (e) => {
  // User switched to touch device or changed mode
  updateInteractionStyle(e.matches ? 'touch' : 'pointer');
});
```

### Input-Aware Design Matrix

| Feature | Mouse/Trackpad | Touch | Keyboard | Stylus |
|---------|----------------|-------|----------|--------|
| **Hover states** | Show on hover | N/A (use long-press or tap) | Show on focus | Show on hover |
| **Target size** | ≥24px (WCAG minimum) | ≥44px (recommended) | N/A | ≥44px |
| **Tooltips** | On hover | On long-press or tap icon | On focus | On hover |
| **Context menu** | Right-click | Long-press | Shift+F10 | Right-click equivalent |
| **Drag-and-drop** | Native | Touch-and-hold + drag | Provide keyboard alternative | Native |
| **Selection** | Click + shift/ctrl | Tap + selection mode | Space to select | Tap |

### Hybrid Input Checklist

- [ ] All interactions work with keyboard alone
- [ ] Touch targets meet WCAG 2.5.8 minimum and aim larger where feasible
- [ ] Hover states have touch-accessible alternative
- [ ] Drag-and-drop has non-drag alternative (WCAG 2.5.7) https://www.w3.org/TR/WCAG22/#dragging-movements
- [ ] No hover-only information (provide tap/focus alternative)
- [ ] Stylus/pen input treated as pointer (supports hover)
- [ ] Test with actual touch devices, not just emulation

---

## Optional: AI/Automation UX

> **Scope Note**: This section applies ONLY to products with AI/ML features (chatbots, recommendations, generative AI, automation). Skip if building traditional software.

### Transparency Principles

| Principle | Implementation | Anti-Pattern |
|-----------|----------------|--------------|
| **System status** | Show when AI is processing, queuing, or generating | Hidden inference without feedback |
| **Source attribution** | Cite sources for AI-generated content | Presenting AI output as absolute truth |
| **Confidence cues** | Visual distinction for uncertain/confident outputs | Equal styling for all confidence levels |
| **Model limitations** | Disclose known limitations | Implying omniscience |

### User Control Patterns

| Control | Implementation |
|---------|----------------|
| **Stop/Cancel** | Interrupt generation mid-stream |
| **Regenerate** | Request alternative output |
| **Edit** | Modify AI output before accepting |
| **Undo** | Reverse AI-applied changes |
| **Override** | Human decision supersedes AI suggestion |
| **Disable** | Turn off AI features entirely |

### Trust Calibration

- Show confidence scores where meaningful (not arbitrary percentages)
- Use appropriate hedging language ("likely", "suggests", "might")
- Distinguish facts from inferences
- Provide "Why this recommendation?" explanations
- Allow feedback on AI quality (thumbs up/down, ratings)

### Anti-Patterns to Avoid

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Anthropomorphizing | False expectations of understanding | Describe capabilities accurately |
| "AI says so" | Removes human accountability | Human reviews AI recommendations |
| False certainty | Overconfidence in uncertain outputs | Communicate uncertainty appropriately |
| Hidden AI | User unaware AI is involved | Disclose AI involvement |

---

## Navigation

### Resources (Best Practices & Guides)

- [resources/frontend-aesthetics-2025.md](resources/frontend-aesthetics-2025.md) — Distinctive visual systems (typography, color, spacing, motion) with implementation notes
- [resources/design-systems.md](resources/design-systems.md) — Comprehensive design system implementation guide (foundations, components, patterns)
- [resources/component-library-comparison.md](resources/component-library-comparison.md) — 2025 UI library comparison (MUI, shadcn/ui, Ant Design, Chakra UI, Radix UI, React Aria, Mantine, Headless UI)
- [resources/modern-ux-patterns-2024.md](resources/modern-ux-patterns-2024.md) — Modern UX patterns (skeleton screens, optimistic UI, progressive disclosure, micro-interactions)
- [resources/nielsen-heuristics.md](resources/nielsen-heuristics.md) — Heuristic evaluation guide with practical examples
- [resources/wcag-accessibility.md](resources/wcag-accessibility.md) — WCAG 2.2 success criteria and implementation guide
- [data/sources.json](data/sources.json) — Curated external references (accessibility, platform guidelines, tokens, performance, design systems)

### UI Pattern Inspiration (External)

For real-world UI patterns and competitive research:

- **[Mobbin](https://mobbin.com/)** — 300k+ mobile/web screenshots, searchable by flow type, screen type, UI element (recommended for pattern research)
- **[Page Flows](https://pageflows.com/)** — User flow recordings from top apps
- **[Refero Design](https://refero.design/)** — Web design references by page type

### Templates by Category

**Component Libraries (Implementation Guides):**

- [templates/component-libraries/template-shadcn-ui.md](templates/component-libraries/template-shadcn-ui.md) — shadcn/ui with Radix UI + Tailwind CSS (copy-paste components, full ownership)
- [templates/component-libraries/template-mui-material-ui.md](templates/component-libraries/template-mui-material-ui.md) — Material-UI (Google Material Design, enterprise-grade, 95k+ stars)

**Interaction Patterns (Micro-interactions & Animations):**

- [templates/interaction-patterns/template-micro-interactions.md](templates/interaction-patterns/template-micro-interactions.md) — 2024 micro-interaction patterns (buttons, forms, loading states, toasts, drag-and-drop)

**Design & Planning:**

- [templates/design-brief.md](templates/design-brief.md) — Single-source design brief (goals, IA, accessibility, experimentation)
- [templates/ux-review-checklist.md](templates/ux-review-checklist.md) — Heuristic + accessibility review checklist
- Shared checklist: [../software-clean-code-standard/templates/checklists/ux-design-review-checklist.md](../software-clean-code-standard/templates/checklists/ux-design-review-checklist.md) — Product-agnostic UX design review checklist (core + optional AI)

### Related Skills (Cross-Functional)

- [../software-ux-research/SKILL.md](../software-ux-research/SKILL.md) — **Research sibling**: Use FIRST for feedback analysis, pain point extraction, competitive analysis → feeds pattern selection here
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Frontend implementation (Next.js 16, React, TypeScript, Tailwind CSS, shadcn/ui)
- [../software-mobile/SKILL.md](../software-mobile/SKILL.md) — Mobile UX patterns (iOS Swift, Android Kotlin, platform conventions)
- [../product-management/SKILL.md](../product-management/SKILL.md) — Product strategy, user research, positioning
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — UI/E2E testing, visual regression, accessibility automation
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System design patterns and architecture principles
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — API design for optimal UX (REST, GraphQL, real-time)

---

## Operational Playbooks
- [resources/operational-playbook.md](resources/operational-playbook.md) — Design themes, accessibility heuristics, mobile-first guidance, and decision frameworks
