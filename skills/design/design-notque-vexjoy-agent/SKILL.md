---
name: design
description: Design workflows — UX copy, design systems, design critique, accessibility review, design handoff, user research synthesis. Use when writing UI copy, reviewing designs, building component systems, checking accessibility, or preparing developer handoffs.
routing:
  triggers:
    - "design"
    - "UX copy"
    - "design system"
    - "design critique"
    - "accessibility"
    - "WCAG"
    - "design handoff"
    - "user research"
    - "UI copy"
    - "component library"
    - "design review"
    - "typography"
    - "color system"
  category: business
  force_route: false
  pairs_with: []
user-invocable: true  # justification: design work spans multiple modes; direct invocation for targeted design tasks
---

# Design

Umbrella skill for design workflows: UX copy, design systems, critique, accessibility review, developer handoff, and user research synthesis. Each mode loads its own reference files on demand.

---

## Mode Detection

Classify into one mode before proceeding.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **UX-COPY** | write copy, button text, error message, empty state, onboarding copy, tooltip text, confirmation dialog, notification copy | `references/ux-copy.md` |
| **DESIGN-SYSTEM** | design tokens, component library, naming conventions, audit components, document component, extend system, theme architecture | `references/design-systems.md` |
| **CRITIQUE** | review design, critique mockup, design feedback, evaluate screen, visual hierarchy, usability review | `references/design-critique.md` |
| **ACCESSIBILITY** | WCAG, accessibility audit, color contrast, keyboard navigation, screen reader, a11y, focus management, ARIA | `references/accessibility-review.md` |
| **HANDOFF** | developer handoff, spec sheet, handoff doc, implementation spec, design-to-dev, responsive spec | `references/design-handoff.md` |
| **RESEARCH** | synthesize research, interview analysis, usability findings, survey results, user segments, research themes | (inline — see workflow) |

If the request spans modes, pick the primary mode and note the secondary.

---

## Workflow by Mode

### UX-COPY Mode

**Load**: `references/ux-copy.md`, `references/llm-design-failure-modes.md`

1. **Gather context** — Ask conversationally:
   - Component type (button, error, empty state, tooltip, confirmation, notification, onboarding)
   - User state and emotional context (frustrated, exploring, completing a task)
   - Brand voice (formal, friendly, playful, reassuring)
   - Constraints (character limits, platform guidelines, localization needs)
   - Existing copy patterns (what terminology the product already uses)

2. **Generate copy** using component-specific patterns from reference:
   - Primary recommendation with rationale
   - 2-3 alternatives with tone/context guidance
   - Localization notes (character expansion, idiom risks, cultural context)

3. **Validate** — Check against these gates:
   - Copy uses product's existing terminology consistently
   - Action labels match outcomes (button says what it does)
   - Error messages follow What happened + Why + How to fix
   - Character limits respected for target platform
   - No jargon without explanation

**Gate**: Copy exists for all requested components. Each piece has rationale tied to user context. Alternatives provided with differentiated use cases.

### DESIGN-SYSTEM Mode

**Load**: `references/design-systems.md`, `references/llm-design-failure-modes.md`

1. **Determine operation**:

| Operation | Inputs | Key Actions |
|-----------|--------|-------------|
| Audit | Component library or codebase | Check naming consistency, token coverage, hardcoded values, state completeness, documentation gaps |
| Document | Component name + context | Generate props/variants/states/accessibility/usage spec |
| Extend | Gap description + existing system | Propose new component using existing tokens and patterns, show relationship to existing components |

2. **Execute** using design token architecture from reference:
   - Tokens: color (brand, semantic, neutral), typography (scale, weights, line heights), spacing (scale, component padding), borders (radius, width), shadows (elevation), motion (duration, easing)
   - Components: variants, states (default, hover, active, disabled, loading, error), sizes, accessibility, composition patterns
   - Patterns: form patterns, navigation patterns, data display, feedback

3. **Validate**:

| Check | Criteria |
|-------|----------|
| Naming | Consistent convention across all components |
| Tokens | No hardcoded values — everything references a token |
| States | All interactive states defined (default, hover, active, disabled, loading, error) |
| A11y | ARIA roles, keyboard behavior, screen reader announcements documented |
| Composition | Component works standalone and composed with others |

**Gate**: Output uses consistent naming. All values reference tokens. Interactive states complete. Accessibility documented.

### CRITIQUE Mode

**Load**: `references/design-critique.md`, `references/llm-design-failure-modes.md`

1. **Gather context**:
   - Design stage (exploration, refinement, final polish)
   - Target users and their goals
   - Focus area (optional — "just the navigation" vs full review)
   - Platform (web desktop, web mobile, native iOS, native Android)

2. **Apply structured critique** — Four-step method:
   - **Describe**: What is present? Elements, layout, visual relationships. No judgment yet.
   - **Analyze**: How are design principles applied? Hierarchy, contrast, alignment, proximity, repetition.
   - **Interpret**: What does the design communicate? Emotional tone, brand alignment, user expectations.
   - **Evaluate**: What works, what could improve, and specific recommendations.

3. **Evaluate against heuristics** — Apply Nielsen's 10 to the specific design:

| Heuristic | Key Question |
|-----------|-------------|
| Visibility of system status | Does the user know what's happening? |
| Match with real world | Does it use the user's language and mental models? |
| User control and freedom | Can the user undo, go back, escape? |
| Consistency and standards | Does it follow platform conventions and its own patterns? |
| Error prevention | Does the design prevent errors before they happen? |
| Recognition over recall | Are options visible, not memorized? |
| Flexibility and efficiency | Does it serve both novices and experts? |
| Aesthetic and minimalist design | Does every element earn its space? |
| Error recovery | Are errors explained with clear recovery paths? |
| Help and documentation | Is contextual help available where needed? |

4. **Match feedback to stage**:

| Stage | Focus | Avoid |
|-------|-------|-------|
| Exploration | Concept direction, user flow logic, information architecture | Pixel-level visual polish |
| Refinement | Visual hierarchy, interaction patterns, consistency, edge cases | Questioning the fundamental approach |
| Final | Color contrast, spacing precision, copy accuracy, accessibility | Structural redesign suggestions |

**Gate**: Critique covers usability, visual hierarchy, consistency, and accessibility. Feedback is specific (element + issue + recommendation). Positive observations included. Stage-appropriate depth.

### ACCESSIBILITY Mode

**Load**: `references/accessibility-review.md`, `references/llm-design-failure-modes.md`

1. **Determine scope**: Full WCAG 2.1 AA audit vs targeted check (contrast, keyboard, screen reader).

2. **Audit by WCAG principle**:

| Principle | Key Criteria |
|-----------|-------------|
| Perceivable | Alt text (1.1.1), semantic structure (1.3.1), text contrast 4.5:1 (1.4.3), UI contrast 3:1 (1.4.11) |
| Operable | Keyboard access (2.1.1), focus order (2.4.3), visible focus (2.4.7), touch targets 44x44px (2.5.5) |
| Understandable | Predictable behavior (3.2.1), error identification (3.3.1), input labels (3.3.2) |
| Robust | Name/role/value for all UI components (4.1.2) |

3. **Check component-specific patterns** from reference (buttons, forms, modals, navigation, data tables, carousels).

4. **Generate audit report** with:
   - Issue count by severity (Critical, Major, Minor)
   - Each finding: WCAG criterion, location, issue, severity, remediation
   - Color contrast check table (foreground, background, ratio, required, pass/fail)
   - Keyboard navigation map
   - Screen reader announcement check
   - Priority fixes ranked by user impact

**Gate**: Audit covers all four WCAG principles. Each finding cites a specific WCAG criterion. Remediation provided for every issue. Severity reflects real user impact.

### HANDOFF Mode

**Load**: `references/design-handoff.md`, `references/llm-design-failure-modes.md`

1. **Gather inputs**:
   - Design (Figma URL, screenshot, description)
   - Tech stack (framework, CSS approach, component library)
   - Design system tokens (if available)
   - Target breakpoints

2. **Generate spec** covering all artifact categories:

| Category | Contents |
|----------|----------|
| Layout | Grid system, breakpoints, responsive behavior rules |
| Design tokens | Color, typography, spacing, elevation — token names mapped to values |
| Components | Name, variant, props, special behavior notes |
| States | Every interactive element: default, hover, active, disabled, loading, error |
| Interactions | Click/tap, hover, transitions (duration + easing), gestures |
| Content | Character limits, truncation rules, empty states, loading states |
| Edge cases | Min/max content, i18n text expansion, slow connections, missing data |
| Accessibility | Focus order, ARIA labels/roles, keyboard interactions, screen reader announcements |
| Animation | Element, trigger, description, duration (ms), easing function |

3. **Validate completeness**:
   - Every interactive element has all states specified
   - Token references used (not raw values)
   - Edge cases documented (empty, loading, error, overflow, missing data)
   - Responsive behavior explicit at each breakpoint
   - Accessibility requirements stated

**Gate**: Spec covers all categories in the table. Uses token references. All states documented. Edge cases present. A developer can build from this spec without guessing.

### RESEARCH Mode

**Load**: `references/llm-design-failure-modes.md`

1. **Accept inputs** — Interview transcripts, survey data, usability test notes, support tickets, app reviews, NPS responses.

2. **Process each source**:
   - Extract observations (what happened), verbatim quotes, behaviors (vs stated preferences), pain points, positive signals, context
   - Behavioral data outweighs stated preferences. What users do > what users say.

3. **Synthesize**:
   - Affinity mapping: one observation per note, let clusters emerge, split large clusters
   - Theme development: initial codes -> theme candidates -> review against evidence -> refined themes
   - Triangulation: findings supported by multiple sources are stronger. Flag single-source findings.

4. **Priority matrix**:

| | High Impact | Low Impact |
|---|---|---|
| **High Frequency** | Top priority | Quality-of-life |
| **Low Frequency** | Segment-specific | Note and deprioritize |

5. **Generate synthesis**:
   - Executive summary (3-4 sentences)
   - Key themes: name, prevalence (X of Y participants), summary, supporting evidence with quotes, implication
   - Insights-to-opportunities table: insight, opportunity, impact, effort
   - User segments identified: name, characteristics, needs, rough size
   - Prioritized recommendations with evidence basis
   - Questions for further research
   - Methodology notes and limitations

**Gate**: Themes supported by evidence with quotes. Behaviors distinguished from stated preferences. Quote attribution uses participant type ("Enterprise admin, 200-person team"), not names. Recommendations tied to specific findings.

---

## LLM Failure Modes in Design Work

**Load `references/llm-design-failure-modes.md` for all modes.** These are specific ways LLMs fail at design tasks:

| Failure Mode | What Happens | Defense |
|-------------|-------------|---------|
| Generic copy | Copy sounds professional but lacks product personality and context | Ground every piece in the product's existing voice, user's emotional state, and specific feature context |
| Inaccessible suggestions | Recommends color combinations or patterns that fail WCAG | Check every color pairing against 4.5:1 (text) and 3:1 (UI) ratios. Verify keyboard paths. |
| Platform-blind critique | Applies desktop heuristics to mobile or iOS patterns to Android | Identify target platform first. Apply platform-specific conventions. |
| Missing edge cases | Specs cover happy path but omit empty, loading, error, overflow, i18n states | Use the edge case checklist from handoff reference for every spec. |
| Surface-level critique | "Looks clean" or "good hierarchy" without specificity | Every critique finding names the element, the issue, and a concrete recommendation. |
| Fabricated research | Invents plausible user quotes, statistics, or persona details | Every finding cites user-provided source material. Flag confidence levels. Mark assumptions explicitly. |
| Token-value confusion | Specs use raw px/hex values instead of design tokens | Reference token names. Flag any raw value as "needs token mapping." |
| Framework dumping | Lists heuristics or WCAG criteria as a checklist without applying to the specific design | Apply each criterion to the actual design. Skip criteria that do not apply. Explain how each applies. |

---

## Output Conventions

- Markdown with clear headers. Scannable by busy designers and developers.
- Tables for comparisons, audit findings, component specs, token mappings.
- Severity labels: **Critical** (blocks users), **Major** (degrades experience), **Minor** (polish).
- Every recommendation is specific enough to act on. "Improve contrast" is not actionable. "Change body text from #999 to #595959 on #fff background to meet 4.5:1 ratio" is.
- Include what works well alongside what needs improvement.

---

## Reference Loading Table

| Mode | Primary Reference | Secondary Reference |
|------|------------------|-------------------|
| UX-COPY | `references/ux-copy.md` | `references/llm-design-failure-modes.md` |
| DESIGN-SYSTEM | `references/design-systems.md` | `references/llm-design-failure-modes.md` |
| CRITIQUE | `references/design-critique.md` | `references/llm-design-failure-modes.md` |
| ACCESSIBILITY | `references/accessibility-review.md` | `references/llm-design-failure-modes.md` |
| HANDOFF | `references/design-handoff.md` | `references/llm-design-failure-modes.md` |
| RESEARCH | (inline) | `references/llm-design-failure-modes.md` |
