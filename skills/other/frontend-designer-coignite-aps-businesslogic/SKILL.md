---
name: frontend-designer
description: "Evidence-based frontend design: research, evaluate, and build production-grade interfaces. Audits existing UI with Chrome DevTools, documents design decisions with rationale, and applies modern design principles including AI-first patterns. Use for building, reviewing, or improving any frontend interface."
user_invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__click, mcp__chrome-devtools__fill, mcp__chrome-devtools__wait_for, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__select_page, mcp__chrome-devtools__new_page, mcp__chrome-devtools__evaluate_javascript
---

# Frontend Designer — Evidence-Based Design Skill

This skill creates, evaluates, and improves frontend interfaces using research-backed design principles. Every design decision must have a documented rationale — we never make choices without explaining WHY.

## Execution Model

**This skill MUST be run as a sub-agent** using the Agent tool. This ensures:
- It does NOT consume the main conversation's context window
- It has its own full context for research, evaluation, and iterative building
- Only the final deliverable/summary returns to the caller

**How to invoke from the main conversation:**
```
Agent tool → prompt: "You are an Evidence-Based Frontend Designer Agent. Read and
follow ALL instructions in .claude/skills/frontend-designer/SKILL.md. Project root:
[cwd]. Task: [arguments]. Execute all phases as appropriate. Save design audit reports
to docs/design-decisions/. Return a summary of your work and key design decisions."
```

## Arguments

- No args: Interactive mode — ask what the user wants (build, review, or improve)
- `review`: Audit an existing interface via Chrome DevTools
- `build <description>`: Design and build a new interface
- `improve <path>`: Improve an existing component/page
- `document`: Generate a design decisions document for the current UI

---

## PHASE 1: RESEARCH (Always do this first)

Before ANY design work, gather evidence. This phase ensures we make informed decisions, not guesses.

### 1a: Understand the Context

Ask or determine:
- **Who** is the user? (developer, business user, end customer, admin)
- **What** task are they performing? (monitoring, data entry, exploration, decision-making)
- **Where** will this be used? (desktop dashboard, mobile, embedded, kiosk)
- **How often** will they use it? (daily power user vs. occasional visitor)
- **What decisions** does the interface help them make?

### 1b: Research Comparable Interfaces

Search for evidence on how similar problems have been solved:

```
WebSearch: "[domain] dashboard UX best practices"
WebSearch: "[component type] design patterns 2025 2026"
WebSearch: "Nielsen Norman Group [relevant topic]"
```

**Key sources to prioritize:**
- Nielsen Norman Group (nngroup.com) — gold standard for usability research
- Smashing Magazine — practical design patterns, especially for AI interfaces
- Baymard Institute — e-commerce and form UX research
- Laws of UX (lawsofux.com) — psychology-backed design laws
- GOV.UK Design System — accessibility-first design patterns

### 1c: Document Research Findings

Before proceeding, write a brief research summary:

```markdown
## Design Research — [Component/Page Name]

### User Context
- Primary user: [who]
- Task: [what they're doing]
- Frequency: [how often]
- Environment: [where/device]

### Evidence Gathered
1. [Finding from source] — [URL]
2. [Finding from source] — [URL]
3. [Finding from source] — [URL]

### Design Implications
- Because [evidence], we should [decision]
- Because [evidence], we should [decision]
```

---

## PHASE 2: DESIGN PRINCIPLES (Reference Framework)

Apply these evidence-based principles to every design decision. Each principle includes its source so anyone can verify WHY we follow it.

### 2a: Nielsen's 10 Usability Heuristics

Source: Jakob Nielsen, Nielsen Norman Group, 1994 (refined 2020)
Evidence: Factor analysis of 249 usability problems across multiple studies.

| # | Heuristic | What to check |
|---|-----------|---------------|
| 1 | **Visibility of system status** | Does the UI show what's happening? Loading states, progress indicators, success/error feedback? |
| 2 | **Match between system and real world** | Does it use the user's language? Are concepts familiar, not developer jargon? |
| 3 | **User control and freedom** | Can users undo, cancel, go back? Is there an emergency exit? |
| 4 | **Consistency and standards** | Do similar things look and behave the same way? Platform conventions followed? |
| 5 | **Error prevention** | Does design prevent errors before they happen? Confirmations for destructive actions? |
| 6 | **Recognition rather than recall** | Are options visible? Does user need to remember things across screens? |
| 7 | **Flexibility and efficiency** | Are there shortcuts for expert users? Can workflows be customized? |
| 8 | **Aesthetic and minimalist design** | Is every element necessary? No decorative clutter competing with content? |
| 9 | **Help users recognize, diagnose, recover from errors** | Are error messages in plain language with suggested solutions? |
| 10 | **Help and documentation** | Is contextual help available? Can users find answers without leaving the flow? |

### 2b: Gestalt Principles of Perception

Source: Wertheimer, Koffka, Kohler (1920s). Applied to web: NN/G, Interaction Design Foundation.
Evidence: Decades of cognitive psychology research on how humans perceive visual groups.

| Principle | Design Application |
|-----------|-------------------|
| **Proximity** | Related items must be close together. Unrelated items must have clear separation. Spacing IS information. |
| **Similarity** | Elements that share visual properties (color, shape, size) are perceived as a group. Use consistently for categories. |
| **Continuity** | The eye follows smooth paths. Align elements on clear axes. Use visual lines to guide attention. |
| **Closure** | The brain completes incomplete shapes. Cards, containers, and borders can be implied, not always drawn. |
| **Figure/Ground** | Make the primary content the clear "figure" against the background. Avoid ambiguity about what's foreground vs. background. |
| **Common Region** | Elements inside a shared boundary (card, box, colored area) are perceived as a group. Use containers intentionally. |

### 2c: Visual Hierarchy Rules

Source: NN/G "5 Principles of Visual Design in UX"
Evidence: Eye-tracking studies showing how users scan interfaces.

**The F-Pattern:** Users scan web pages in an F-shape — top horizontal line first, then down the left side. Place critical information top-left.

**Size = Importance:** Larger elements are noticed first. Scale conveys hierarchy.

**Contrast = Attention:** High contrast draws the eye. Use it for primary actions and critical information. Low contrast for secondary content.

**The Squint Test:** Blur your vision (or blur a screenshot). If the most important element isn't still the most prominent, your hierarchy is wrong.

### 2d: Spacing and Grid System (8pt Grid)

Source: Google Material Design, Spotify Design System, spec.fm
Evidence: Most screen resolutions are divisible by 8. Consistent spacing reduces cognitive load.

**Rules:**
- All spacing values must be multiples of 4px (minimum unit) or 8px (primary unit)
- Standard scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px
- Internal padding ≤ external margins (items inside a container have less space than between containers)
- Touch targets: minimum 44x44px (Apple HIG) or 48x48px (Material Design)

### 2e: Typography Scale

Source: Robert Bringhurst "Elements of Typographic Style", modular scale theory
Evidence: Mathematical ratios create harmonious visual rhythm.

**Recommended scale (Major Third ratio: 1.25):**

| Token | Size | Weight | Use |
|-------|------|--------|-----|
| `display-lg` | 36-48px | 700 | Page hero, dashboard KPIs |
| `display-sm` | 28-32px | 700 | Section hero values |
| `heading-lg` | 22-24px | 600 | Page titles |
| `heading-md` | 18-20px | 600 | Section headings |
| `heading-sm` | 16px | 600 | Subsection headings |
| `body-lg` | 16px | 400 | Primary body text |
| `body-md` | 14px | 400 | Default body, form labels |
| `body-sm` | 13px | 400 | Secondary text, metadata |
| `caption` | 12px | 400-500 | Labels, timestamps, help text |

**Line height:** 1.15 for large display text, 1.4-1.5 for body text, 1.6 for long-form reading.

### 2f: Color System

Source: WCAG 2.2 (W3C), Material Design 3, Radix Colors
Evidence: WCAG AA requires 4.5:1 contrast ratio for text; large text (18px+ bold or 24px+) requires 3:1.

**Semantic palette structure:**
- **Surface colors**: background, surface, surface-elevated (layer system for depth)
- **Content colors**: on-surface (primary text), on-surface-variant (secondary), on-surface-disabled
- **Interactive colors**: primary, primary-container, on-primary
- **Feedback colors**: success/green, warning/amber, error/red, info/blue
- **Never** use color as the ONLY indicator — always pair with icons, text, or patterns (color-blind accessibility)

### 2g: AI-First Interface Patterns (2025-2026)

Source: Smashing Magazine "Design Patterns for AI Interfaces" (Vitaly Friedman, 2025), Groovy Web "UI/UX Trends for AI-First Apps 2026", AufaitUX "AI Design Patterns Enterprise Dashboards"
Evidence: Chat interfaces are fading as the default. Task-oriented UIs with AI augmentation outperform pure conversational interfaces.

| Pattern | Description | When to use |
|---------|-------------|-------------|
| **Insight Cards** | Compact cards showing ML predictions, anomalies, or suggestions with confidence scores | Dashboards, monitoring |
| **Temperature Controls** | Sliders/knobs that let users control AI behavior (creativity, precision, scope) | AI generation tools |
| **Structured Presets** | Pre-built templates and starting points instead of blank canvas | Content creation, config |
| **Progressive Disclosure of AI** | Show AI capabilities gradually as user demonstrates readiness | Onboarding, complex tools |
| **Ambient Intelligence** | UI adapts layout/content based on user behavior — with "Personalised for you" labels and one-click reset | Dashboards, feeds |
| **Confidence Indicators** | Visual representation of how certain the AI is (bars, percentages, traffic lights) | Search results, predictions |
| **Streaming Output** | Typewriter-effect for AI responses with skeleton loading for structure | Chat, generation |
| **Explanation Layers** | Expandable "why" sections that explain AI reasoning | Recommendations, scores |
| **Human-in-the-Loop Controls** | Approve/reject/edit AI suggestions before they take effect | Automation, workflows |
| **Multimodal Feedback** | Accept input via text, voice, image, drag-drop — not just chat | Search, creation |

### 2h: Information Architecture

Source: Rosenfeld & Morville "Information Architecture for the World Wide Web", NN/G, Figma
Evidence: Poor IA is the #1 cause of user frustration in complex applications.

**Key rules:**
- **Breadth vs. Depth**: Prefer broad, shallow navigation (5-7 top items) over deep nesting. Users should reach any page in ≤3 clicks.
- **Labels matter**: Use the user's vocabulary, not internal/developer terminology
- **Progressive disclosure**: Show only what's needed now. Reveal complexity on demand.
- **Consistent navigation**: Primary nav stays fixed. Users must always know where they are.
- **Search is not a substitute for navigation**: If users must search to find things, your IA is broken.

---

## PHASE 3: EVALUATE (Chrome DevTools Audit)

Use Chrome DevTools to evaluate existing interfaces. Run this phase when reviewing or improving UI.

### 3a: Visual Inspection

```
1. Open the page: mcp__chrome-devtools__navigate_page
2. Take a screenshot: mcp__chrome-devtools__take_snapshot
3. Analyze the screenshot against:
   - Visual hierarchy (squint test)
   - Spacing consistency (8pt grid alignment)
   - Typography scale (are sizes from the defined scale?)
   - Color contrast (sufficient for accessibility?)
   - Gestalt grouping (are related items visually grouped?)
```

### 3b: Responsive Check

```javascript
// Run in Chrome DevTools console via evaluate_javascript
// Test at key breakpoints
const breakpoints = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'widescreen', width: 1920, height: 1080 }
];
// Resize viewport and screenshot at each breakpoint
```

### 3c: Accessibility Audit

```javascript
// Check color contrast ratios
const elements = document.querySelectorAll('*');
const issues = [];
elements.forEach(el => {
  const style = window.getComputedStyle(el);
  const bg = style.backgroundColor;
  const fg = style.color;
  const fontSize = parseFloat(style.fontSize);
  // Flag elements with potential contrast issues
  if (fg === bg) issues.push({ el: el.tagName, issue: 'invisible text' });
});
console.log('Potential issues:', issues.length);
```

Also check:
- All images have alt text
- Interactive elements are keyboard-focusable (Tab through the page)
- Focus indicators are visible
- ARIA labels on icon-only buttons
- Form labels associated with inputs
- Heading hierarchy (h1 → h2 → h3, no skips)

### 3d: Performance Check

```javascript
// Get Core Web Vitals
const entries = performance.getEntriesByType('navigation');
const paint = performance.getEntriesByType('paint');
console.log('DOM Content Loaded:', entries[0]?.domContentLoadedEventEnd);
console.log('Load:', entries[0]?.loadEventEnd);
paint.forEach(p => console.log(p.name + ':', p.startTime));

// Check for layout shifts
new PerformanceObserver(list => {
  list.getEntries().forEach(entry => {
    console.log('Layout shift:', entry.value);
  });
}).observe({ type: 'layout-shift', buffered: true });
```

### 3e: Design Token Compliance

Check if the interface follows the design system tokens:

```javascript
// Audit for hardcoded colors
const allElements = document.querySelectorAll('*');
const hardcodedColors = [];
allElements.forEach(el => {
  const style = el.getAttribute('style') || '';
  if (style.match(/#[0-9a-fA-F]{3,8}|rgb\(|rgba\(/)) {
    hardcodedColors.push({
      element: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
      style: style.substring(0, 100)
    });
  }
});
console.log('Hardcoded colors found:', hardcodedColors.length);
hardcodedColors.slice(0, 20).forEach(c => console.log(' ', c.element, c.style));
```

### 3f: Generate Audit Report

Compile all findings into a structured evaluation:

```markdown
## Design Audit — [Page/Component Name]
Date: [DATE]
URL: [URL]

### Heuristic Evaluation (Nielsen's 10)
| # | Heuristic | Score (1-5) | Issues | Recommendations |
|---|-----------|-------------|--------|-----------------|
| 1 | Visibility of system status | X | ... | ... |
... (all 10)

### Visual Design Assessment
- Grid compliance: X% of spacing follows 8pt grid
- Typography: X of Y text sizes match the type scale
- Color tokens: X hardcoded colors found
- Contrast: X elements below AA ratio

### Accessibility
- Keyboard navigation: PASS/FAIL
- Focus indicators: PASS/FAIL
- Alt text coverage: X%
- Heading hierarchy: PASS/FAIL
- ARIA compliance: X issues

### Performance
- First Paint: Xms
- DOM Content Loaded: Xms
- Layout shifts: X

### Top 5 Improvements (Priority Order)
1. [Most impactful change] — Rationale: [evidence]
2. ...
```

---

## PHASE 4: BUILD (Implementation)

When creating new interfaces, follow this process:

### 4a: Design Before Code

1. Define the information architecture (what content, how organized)
2. Sketch the layout with ASCII or describe the wireframe
3. Map every element to design tokens (colors, spacing, typography)
4. Identify interactive states (hover, focus, active, disabled, loading, error, empty)
5. Plan responsive behavior at each breakpoint

### 4b: Implementation Rules

**Structure:**
- Semantic HTML first (`<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`)
- Component hierarchy matches information hierarchy
- Every container has a purpose (don't nest divs without reason)

**Styling:**
- CSS custom properties (design tokens) for all visual values
- 8pt grid for all spacing
- CSS Grid for page layouts, Flexbox for component layouts
- Mobile-first media queries
- Transitions on interactive elements (150-300ms, ease-out)
- No `!important` unless overriding third-party styles

**Interactivity:**
- Every action has feedback (visual state change within 100ms)
- Loading states for any operation >300ms
- Error states with plain-language messages and recovery actions
- Empty states with helpful guidance (not just "No data")
- Confirmation for destructive actions

### 4c: For Directus Extensions (Project-Specific)

When building within the BusinessLogic CMS (Directus), also read:
- `legacy-implementation/businesslogic-cms/.claude/skills/frontend-design/SKILL.md` for Directus-specific components and theme variables
- Use `v-*` Directus components over custom HTML
- Use `var(--theme--*)` CSS variables exclusively
- `<style scoped>` on all components

### 4d: For Standalone Services (ai-api, gateway, public API)

When building public-facing or standalone UIs:
- Choose a component library (Radix, shadcn/ui, Headless UI) or build from design tokens
- Implement a token file (CSS custom properties or JS object)
- Ensure the token system supports dark/light theme switching
- Build accessible-first (WCAG 2.2 AA minimum)

---

## PHASE 5: DOCUMENT DESIGN DECISIONS

Every non-trivial design choice must be recorded. This creates institutional knowledge and prevents "why does it look like this?" questions later.

### Design Decision Record (DDR) Format

Save to `docs/design-decisions/` or inline as comments:

```markdown
## DDR-[number]: [Decision Title]

**Date:** [DATE]
**Component:** [path/to/component]
**Author:** [who decided]

### Context
[What problem or question prompted this decision?]

### Research
[What evidence did we gather?]
- [Source 1] — [Finding]
- [Source 2] — [Finding]

### Decision
[What we chose to do]

### Rationale
[WHY this choice, backed by evidence]

### Alternatives Considered
1. [Alternative A] — rejected because [reason]
2. [Alternative B] — rejected because [reason]

### Consequences
- Positive: [what improves]
- Negative: [trade-offs we accept]
- Risks: [what could go wrong]
```

---

## QUALITY CHECKLIST

Before considering any design work complete:

### Usability
- [ ] Passes all 10 Nielsen heuristics (no score below 3)
- [ ] Visual hierarchy guides user to primary action within 3 seconds
- [ ] All interactive elements have visible hover/focus/active states
- [ ] Error states provide recovery guidance
- [ ] Loading states prevent user confusion
- [ ] Empty states guide users on what to do

### Visual Design
- [ ] All spacing follows 8pt grid (multiples of 4px minimum)
- [ ] Typography uses defined scale (no arbitrary sizes)
- [ ] Colors come from design tokens (zero hardcoded hex values)
- [ ] Visual hierarchy passes the squint test
- [ ] Gestalt grouping is intentional (proximity, similarity, common region)
- [ ] Consistent use of elevation/shadow for depth

### Accessibility (WCAG 2.2 AA)
- [ ] Color contrast ≥ 4.5:1 for text, ≥ 3:1 for large text and UI components
- [ ] Color is never the only indicator (always paired with icon/text/pattern)
- [ ] All images have alt text
- [ ] Full keyboard navigation works (Tab, Enter, Escape, Arrow keys)
- [ ] Focus indicators are visible
- [ ] Screen reader compatible (ARIA labels, semantic HTML, heading hierarchy)
- [ ] Touch targets ≥ 44x44px

### Performance
- [ ] No unnecessary re-renders or DOM manipulation
- [ ] Images are optimized (WebP, lazy loading)
- [ ] CSS animations use transform/opacity (GPU-accelerated)
- [ ] No layout shifts after initial paint

### Documentation
- [ ] Design decisions documented with rationale
- [ ] Component has clear props/API documentation
- [ ] States documented (default, hover, active, disabled, loading, error, empty)

---

## REFERENCE SOURCES

These are the authoritative sources backing this skill. When in doubt, consult these:

| Source | URL | What for |
|--------|-----|----------|
| Nielsen Norman Group | nngroup.com | Usability heuristics, UX research, evidence-based design |
| Smashing Magazine — AI Patterns | smashingmagazine.com | AI interface design patterns, agentic AI UX |
| WCAG 2.2 | w3.org/WAI/WCAG22/quickref | Accessibility requirements |
| Laws of UX | lawsofux.com | Psychology-backed design principles |
| Material Design 3 | m3.material.io | Component patterns, color system, spacing |
| Radix Colors | radix-ui.com/colors | Accessible color scales with contrast guarantees |
| Interaction Design Foundation — Gestalt | ixdf.org | Gestalt principles applied to digital |
| 8pt Grid Guide | spec.fm/specifics/8-pt-grid | Spacing system rationale |
| W3C Design Tokens | design-tokens.github.io/community-group | Design token specification |
| Figma — Information Architecture | figma.com/resource-library | IA patterns and best practices |

When researching for a specific design decision, ALWAYS search these sources first, then branch out to domain-specific resources.
