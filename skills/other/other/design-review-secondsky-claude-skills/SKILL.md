---
name: design-review
description: 7-phase frontend design review with accessibility (WCAG 2.1 AA), responsive testing, visual polish. Use for PR reviews, UI audits, or encountering contrast issues, broken layouts, accessibility violations, inconsistent spacing, missing focus states.

  Keywords: design review, UI audit, frontend review, accessibility audit, WCAG compliance,
  responsive design, visual QA, UX review, component review, PR design check, layout issues,
  accessibility violations, contrast problems, broken responsive, interaction bugs, keyboard
  navigation, focus states, design system compliance, visual consistency, user experience
license: MIT
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Design Review Skill

**Status**: Production Ready ✅
**Last Updated**: 2025-11-20
**Dependencies**: Playwright MCP or Chrome DevTools
**Methodology**: 7-phase systematic review (inspired by Stripe, Airbnb, Linear)

---

## Quick Start

### 1. Prerequisites Check

Before starting a design review, verify browser automation tools are available:

**Option A: Playwright MCP** (recommended for interactive testing)
- See the `playwright-testing` skill for Playwright setup
- Provides browser automation, screenshots, viewport testing, console monitoring

**Option B: Chrome DevTools CLI** (alternative for screenshots and performance)
- See the `chrome-devtools` skill for Puppeteer CLI setup
- Provides screenshot capture, performance analysis, network monitoring

For complete browser tools reference, see [references/browser-tools-reference.md](references/browser-tools-reference.md).

### 2. Understand the Review Scope

**For PR reviews:**
```bash
# Analyze git diff to understand scope
git diff --name-only origin/main...HEAD

# Read PR description for context
```

**For general UI reviews:**
Simply provide the preview URL and component/page description.

### 3. Execute 7-Phase Review

Follow the systematic checklist below. Each phase has specific objectives and testing procedures.

---

## The 7-Phase Review Methodology

### Phase 0: Preparation

**Objective:** Understand context and set up testing environment.

**Steps:**
1. **Read PR description** or review request to understand:
   - Motivation for changes
   - Scope of implementation
   - Testing notes from developer
   - Expected behavior

2. **Analyze code diff** (if PR available):
   ```bash
   git diff origin/main...HEAD
   ```
   Identify modified files (components, styles, tests)

3. **Set up live preview environment:**
   - Navigate to preview URL using browser tools
   - Set initial viewport: 1440x900 (desktop)
   - Take baseline screenshot for reference

4. **Review design principles** (if project has custom guidelines):
   - Check project CLAUDE.md for design standards
   - Review component library documentation
   - Note design system tokens and patterns

**When to skip:** For quick component reviews without git context.

---

### Phase 1: Interaction & User Flow

**Objective:** Verify the interactive experience works as expected.

**For complete interaction guide**: Load `references/interaction-patterns.md` when testing interactive states, forms, buttons, navigation flows, micro-interactions, modals, or keyboard navigation.

**Quick checklist:**
- Test 5 interactive states (default, hover, active, focus, disabled) for all elements
- Execute primary user flow (form submission, navigation, key actions)
- Verify destructive actions have confirmation dialogs
- Assess perceived performance (loading states, optimistic UI)

**Triage:** [Blocker] Critical flow broken | [High] Poor UX/missing focus states | [Medium] Missing polish | [Nitpick] Minor timing issues

---

### Phase 2: Responsiveness Testing

**Objective:** Ensure design works across all viewport sizes.

**For complete responsive guide**: Load `references/responsive-testing.md` when testing viewports, touch targets, mobile navigation, image responsiveness, or debugging horizontal scrolling.

**Test 3 viewports:**
- **Desktop (1440px)**: Optimal layout, full feature set
- **Tablet (768px)**: Graceful adaptation, 44×44px touch targets, collapsing nav
- **Mobile (375px)**: No horizontal scroll, 16px min text, mobile-friendly navigation

**Quick testing:**
```bash
mcp__playwright__browser_resize(width: 1440, height: 900)  # Desktop
mcp__playwright__browser_resize(width: 768, height: 1024)  # Tablet
mcp__playwright__browser_resize(width: 375, height: 667)   # Mobile
mcp__playwright__browser_take_screenshot(fullPage: true)
```

**Triage:** [Blocker] Layout broken | [High] Horizontal scroll/overlapping | [Medium] Suboptimal spacing | [Nitpick] Minor inconsistencies

---

### Phase 3: Visual Polish

**Objective:** Assess aesthetic quality and visual consistency.

**For design principles guide**: Load `references/visual-polish.md` when evaluating typography hierarchy, spacing/layout, color palette, alignment/grid, visual hierarchy, image quality, or S-Tier design standards.

**Quick evaluation (5 criteria):**
1. **Layout & spacing**: Grid alignment, 8px scale, design tokens (no magic numbers like 17px)
2. **Typography**: Clear H1>H2>H3 hierarchy, 1.5-1.7 line height, limited font weights
3. **Color**: Design system tokens, semantic usage (red=error, green=success), consistent brand
4. **Images**: High-res (no pixelation), correct aspect ratios, optimized sizes, alt text
5. **Visual hierarchy**: Primary actions stand out, eye flows naturally, strategic whitespace

**Triage:** [Blocker] Illegible text/broken images | [High] Obvious inconsistencies | [Medium] Spacing/alignment issues | [Nitpick] Aesthetic preferences

---

### Phase 4: Accessibility (WCAG 2.1 AA)

**Objective:** Ensure inclusive design for all users.

**For complete WCAG 2.1 AA checklist**: Load `references/accessibility-wcag.md` when verifying WCAG compliance, testing keyboard navigation, checking color contrast, auditing semantic HTML, or using accessibility testing tools (Lighthouse, axe, WAVE).

**Quick WCAG tests (4 principles):**

1. **Perceivable**: Alt text on images, color contrast (4.5:1 text, 3:1 UI components), semantic HTML
2. **Operable**: Keyboard navigation (Tab order logical, visible focus on ALL interactive elements, Enter/Space activation, Escape closes modals, no keyboard traps)
3. **Understandable**: Clear labels, helpful error messages, consistent navigation/terminology
4. **Robust**: Valid HTML, proper ARIA attributes (roles, states, properties)

**Critical tests:**
- Tab through entire page (verify focus states visible, logical order, no traps)
- Test with WebAIM Contrast Checker (all text/UI ≥4.5:1 or 3:1)
- Verify form labels associated with inputs (`<label for="id">` or `aria-label`)
- Check semantic HTML (h1→h2→h3 no skipping, `<button>` not `<div onClick>`)

**Triage:** [Blocker] No keyboard access to core features | [High] WCAG AA violations | [Medium] Semantic HTML issues | [Nitpick] Enhanced accessibility

---

### Phase 5: Robustness Testing

**Objective:** Verify handling of edge cases and error conditions.

**Test scenarios:**

#### 5.1 Form Validation

- Submit form with empty required fields
- Enter invalid data (wrong email format, out-of-range numbers)
- Test field-level validation (real-time feedback)
- Verify clear error messages with guidance
- Test successful submission flow (confirmation message)

#### 5.2 Content Overflow

- **Long text strings**: Very long names, emails, titles
- **Many items**: Large lists, tables with hundreds of rows
- **Deeply nested content**: Comments with many replies
- **Empty states**: No data to display (show helpful message)

**Common overflow issues:**
- Text breaking layout (overflowing containers)
- Truncation without ellipsis or tooltip
- Performance issues with large lists
- Missing empty state designs

#### 5.3 Loading & Error States

- **Loading states**: Skeleton screens, spinners, progress indicators
- **Error messages**: Clear, actionable error descriptions
- **Retry mechanisms**: Allow user to retry failed operations
- **Timeout handling**: Graceful handling of slow/failed requests
- **Optimistic updates**: Immediate feedback, rollback on failure

**Test procedure:**
```bash
# Simulate slow network
# Check browser DevTools Network tab → throttling

# Force error states
# Test with invalid API responses or network failures
```

**Common problems:**
- No loading indicators (appears frozen)
- Vague error messages ("Error occurred")
- No retry mechanism after failures
- Layout jumps when content loads

**Triage priorities:**
- **[Blocker]** Crashes or complete failures under edge cases
- **[High]** Poor error handling or confusing states
- **[Medium]** Missing edge case handling or minor issues
- **[Nitpick]** Loading state aesthetics or minor polish

---

### Phase 6: Code Health

**Objective:** Ensure maintainable, consistent implementation.

**For code patterns guide**: Load `references/code-health-patterns.md` when evaluating component reuse (DRY principle), design token usage (colors, spacing, typography), pattern consistency (naming, file structure, API patterns), or identifying red flags (duplication, magic numbers, broken abstractions).

**Quick review (3 criteria):**
1. **Component reuse**: No copy-paste, shared components extracted, composition over duplication
2. **Design tokens**: CSS variables for colors/spacing/typography (no magic numbers like `margin: 17px`), border radii consistent
3. **Pattern consistency**: Follows codebase patterns, naming conventions match, file structure organized

**Triage:** [High] Introduces tech debt/breaks patterns | [Medium] Missed reuse opportunities | [Nitpick] Code style preferences

---

### Phase 7: Content & Console

**Objective:** Verify polished details and technical correctness.

#### 7.1 Content Review

**Check for:**
- **Grammar and spelling**: No typos or grammatical errors
- **Clarity**: Labels and instructions are unambiguous
- **Tone consistency**: Matches brand voice (formal/casual)
- **Placeholder text**: Replaced with real content (no "Lorem ipsum")
- **Microcopy quality**: Helpful error messages, button labels, tooltips

**Common content issues:**
- Typos in UI text
- Placeholder text left in production
- Vague labels ("Submit" vs "Save Changes")
- Inconsistent terminology
- Unhelpful error messages ("Error" vs "Email format invalid")

#### 7.2 Console Check

**Test procedure:**
```bash
# Using Playwright MCP
mcp__playwright__browser_console_messages()

# Using Chrome DevTools
# Open DevTools → Console tab
```

**Look for:**
- **JavaScript errors**: Uncaught exceptions, null references
- **React warnings**: Key prop warnings, lifecycle issues
- **Network failures**: Failed API requests, 404s
- **Deprecation warnings**: Old API usage warnings
- **Performance warnings**: Slow renders, memory leaks

**Triage priorities:**
- **[Blocker]** Console errors breaking functionality
- **[High]** Grammar errors or confusing content in user-facing text
- **[Medium]** Console warnings or minor content issues
- **[Nitpick]** Content polish, minor console noise

---

## Communication Principles

### 1. Problems Over Prescriptions

Describe the **problem and its impact**, not the solution. Let the developer decide implementation.

**❌ Prescriptive (avoid):**
"Change the margin to 16px"

**✅ Problem-focused (preferred):**
"The spacing feels inconsistent with adjacent elements, creating visual clutter that distracts from the primary CTA. The current spacing breaks the established rhythm of the design system."

### 2. Triage Matrix

Categorize **every issue** with clear priority:

| Priority | Criteria | Action Required |
|----------|----------|----------------|
| **[Blocker]** | Critical failures, core functionality broken, critical accessibility violations | Must fix before merge |
| **[High-Priority]** | Significant UX issues, obvious design inconsistencies, WCAG violations | Should fix before merge |
| **[Medium-Priority]** | Improvements, minor inconsistencies, edge case handling | Consider for follow-up PR |
| **[Nitpick]** | Aesthetic preferences, minor polish, subjective opinions | Optional refinements |

**Important:** Prefix all nitpicks with "Nit:" to signal low priority.

### 3. Evidence-Based Feedback

Always provide **screenshots** for visual issues. Screenshots should:
- Show the problem clearly
- Include relevant context (surrounding elements)
- Indicate what to look at (arrows, highlights if needed)

**Example:**
```markdown
### [High-Priority] Poor contrast on disabled button

**Problem:** Disabled button text has insufficient contrast (2.1:1), failing WCAG AA
standard (requires 4.5:1). Users with low vision may not recognize the button as disabled.

**Screenshot:** [Attach screenshot showing disabled button]

**Impact:** Accessibility violation, potential confusion for users with visual impairments.
```

### 4. Start with Positives

Always acknowledge what works well before listing issues. This:
- Shows you recognize good work
- Provides balanced feedback
- Maintains positive collaboration

**Example:**
```markdown
### Design Review Summary

The new checkout flow shows excellent attention to user experience. The step indicator
is clear and well-designed, error messages are helpful and actionable, and the overall
layout feels spacious and uncluttered. The loading states with skeleton screens are
particularly well-executed. Great work on the form validation feedback!

However, there are a few accessibility and responsiveness issues to address before merge...
```

---

## Report Structure Template

**For complete template**: Load `assets/review-report-template.md` for the full markdown template with all sections and examples.

**Essential structure:**

```markdown
## Design Review Summary
[2-3 sentences: positive acknowledgment + overall assessment]
**Review scope:** [PR #, pages, components]
**Viewports tested:** Desktop (1440px), Tablet (768px), Mobile (375px)
**Methodology:** 7-phase comprehensive review

---

### Findings

#### 🚨 Blockers
[Critical issues requiring immediate fix before merge]
- **[Blocker] [Title]**: Problem + Screenshot + Phase

#### ⚠️ High-Priority Issues
[Significant issues to fix before merge]
- **[High] [Title]**: Problem + Screenshot + Phase

#### 📋 Medium-Priority / Suggestions
[Improvements for follow-up PR]
- **[Medium] [Title]**: Problem + Phase

#### ✨ Nitpicks
[Minor aesthetic details - optional]
- **Nit:** [Issue] - [Brief description]

---

### Testing Evidence
**Screenshots:** Desktop (1440px) + Tablet (768px) + Mobile (375px)
**Console output:** [Errors/warnings or "Console clean"]
**Accessibility:** Keyboard nav + Focus states + Color contrast

---

### Next Steps
1. Fix Blockers
2. Address High-Priority issues
3. Consider Medium-Priority items

**Overall assessment:** [Ready to merge after blockers fixed / Needs revisions / Ready to merge!]
```

---

## When to Load References

Load reference files when working on specific aspects of design review:

### accessibility-wcag.md
Load when:
- **Standards-based**: Verifying WCAG 2.1 AA compliance for production deployment
- **Issue-based**: Encountering accessibility violations (color contrast, keyboard navigation, semantic HTML, focus states, ARIA attributes)
- **Testing-based**: Conducting comprehensive accessibility audit with systematic checklist
- **Tools-based**: Using accessibility testing tools (Lighthouse, axe, WAVE, Pa11y) for automated testing
- **Triage-based**: Determining severity of accessibility issues (Blocker/High/Medium for WCAG violations)

### browser-tools-reference.md
Load when:
- **Setup-based**: Installing or configuring Playwright MCP or Chrome DevTools CLI for testing
- **Command-based**: Need specific Playwright commands (navigate, resize viewport, screenshot, click, type, hover, get console output)
- **Workflow-based**: Implementing common testing workflows (responsive review across 3 viewports, form interaction testing, keyboard navigation testing)
- **Selector-based**: Struggling with CSS selectors, text selectors, or accessibility selectors for element targeting
- **Troubleshooting-based**: Playwright MCP not finding elements, Chrome dependencies missing, screenshot capture issues

### code-health-patterns.md
Load when:
- **Pattern-based**: Evaluating component reuse patterns, DRY principle compliance, extracting shared components
- **Token-based**: Checking design token usage (colors, spacing scale, typography scale, border radii consistency)
- **Consistency-based**: Reviewing pattern consistency (naming conventions, file structure organization, API patterns, state management)
- **Example-based**: Need code examples comparing good vs bad patterns (inline styles vs tokens, duplication vs composition)
- **Red-flag-based**: Identifying code health issues (copy-paste duplication, magic numbers like `17px`, inconsistent state management, broken abstractions)

### design-principles-s-tier.md
Load when:
- **Standards-based**: Ensuring S-Tier SaaS dashboard quality (Stripe, Airbnb, Linear, Vercel level polish)
- **System-based**: Evaluating design system foundation (color palette structure, typography scale, spacing scale, core UI components)
- **Module-based**: Reviewing specific modules (multimedia moderation interfaces, data tables, configuration panels, dashboards)
- **Philosophy-based**: Applying core design philosophy (users first, meticulous craft over speed, simplicity over complexity, consistency)
- **Architecture-based**: Evaluating CSS & styling architecture (design tokens, component patterns, responsive strategies)

### interaction-patterns.md
Load when:
- **States-based**: Testing interactive states (default, hover, active, focus, disabled) for buttons, inputs, links
- **Form-based**: Testing form interactions, validation patterns, error states, success states, loading states
- **Button-based**: Evaluating button loading states, destructive action confirmation patterns, primary vs secondary actions
- **Flow-based**: Testing navigation flows, user journeys, multi-step processes, modal interactions
- **Animation-based**: Reviewing micro-interactions, animation timing (200-300ms), perceived performance (optimistic UI, skeleton screens)
- **Modal-based**: Testing modal interactions, keyboard traps, focus management, Escape key behavior

### responsive-testing.md
Load when:
- **Viewport-based**: Testing at specific viewports (desktop 1440px, tablet 768px, mobile 375px) with Playwright MCP
- **Touch-based**: Verifying touch target sizes meet minimum 44×44px requirement for mobile usability
- **Overflow-based**: Debugging horizontal scrolling issues or layout overflow problems on mobile
- **Mobile-based**: Ensuring text readability (16px minimum font size), mobile navigation patterns, responsive images
- **Breakpoint-based**: Implementing or testing breakpoint strategy (common breakpoints: 640px, 768px, 1024px, 1280px)
- **Navigation-based**: Testing responsive navigation patterns (hamburger menus, collapsing navigation, mobile drawer menus)

### visual-polish.md
Load when:
- **Typography-based**: Evaluating font hierarchy (H1>H2>H3), font scale standards (16/18/24/32/48/64px), line height (1.5-1.7), readability
- **Spacing-based**: Checking 8-point grid compliance (8/16/24/32/40/48/64px), consistent spacing scale, component padding/margin
- **Color-based**: Verifying color palette consistency, semantic color usage (red=error, green=success), design token usage (no hardcoded hex values)
- **Alignment-based**: Checking grid-based layout, precise alignment (0.5px precision), vertical rhythm, visual balance
- **Hierarchy-based**: Evaluating visual hierarchy techniques (size contrast, weight contrast, color contrast, position, strategic whitespace)
- **Quality-based**: Assessing image quality (no pixelation), correct aspect ratios, proper image optimization for web
- **Component-based**: Reviewing design system components (button styles, form input styles, card components, consistent border radii)

---

## Known Issues Prevention

This skill prevents **8** documented design review issues:

| Issue | Problem | Impact | Prevention |
|-------|---------|--------|------------|
| **#1: Missing Accessibility** | Reviews focus only on visual appearance, ignoring keyboard navigation and screen readers | WCAG violations shipped to production, excluding users with disabilities | Phase 4 enforces complete WCAG 2.1 AA checklist with keyboard testing |
| **#2: Incomplete Responsive Testing** | Reviewing only at desktop viewport, missing mobile breakage | Broken mobile layouts, frustrated mobile users | Phase 2 requires testing at 1440px, 768px, and 375px viewports |
| **#3: Vague Feedback** | Comments like "looks off" without screenshots or specifics | Wasted time, unclear action items, frustrated developers | Evidence-based feedback principle requires screenshots |
| **#4: Prescriptive Solutions** | Dictating implementation ("change margin to 16px") instead of describing UX impact | Design-dev friction, missed better solutions | "Problems Over Prescriptions" principle enforced |
| **#5: No Triage Priority** | All feedback treated equally, blocking merges on nitpicks | Slowed delivery, unclear priorities | Triage matrix (Blocker/High/Medium/Nitpick) required |
| **#6: Skipped Edge Cases** | Happy path works, but error states and overflow break layout | Production bugs with edge cases | Phase 5 mandates robustness testing |
| **#7: Console Errors Ignored** | Visual design passes, but JavaScript errors exist in console | Runtime failures, poor user experience | Phase 7 requires console check |
| **#8: Inconsistent Methodology** | Ad-hoc reviews miss critical areas depending on reviewer mood | Incomplete reviews, missed issues | 7-phase checklist ensures comprehensive, repeatable reviews |

---

## Dependencies

### Required

**Browser automation tools** (one of the following):

1. **Playwright MCP** (recommended)
   - See `playwright-testing` skill for installation
   - Provides: Browser automation, screenshots, viewport testing, console monitoring
   - Best for: Interactive testing, keyboard navigation, form testing

2. **Chrome DevTools CLI**
   - See `chrome-devtools` skill for installation
   - Provides: Screenshot capture, performance analysis, network monitoring
   - Best for: Visual testing, performance audits

**Live preview environment:**
- URL accessible for testing
- Represents actual implementation (not mockups)

### Optional

- **Git/GitHub**: For PR context and diff analysis
- **Design system docs**: For consistency checks against established patterns
- **Project CLAUDE.md**: For project-specific design guidelines

### Installation Guidance

If browser tools are not available, this skill will:
1. Detect missing tools
2. Link to appropriate skill for installation (`playwright-testing` or `chrome-devtools`)
3. Provide fallback guidance for manual testing

---

## Related Skills

- **playwright-testing**: E2E testing with Playwright, browser automation setup
- **chrome-devtools**: Browser automation via Puppeteer CLI scripts
- **frontend-design**: Create new frontend interfaces with design quality (complementary skill)
- **tailwind-v4-shadcn**: UI framework implementation (designs being reviewed may use this)
- **ai-sdk-ui**: AI-powered UI components (may be part of reviewed interfaces)

---

## Official Documentation

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Playwright Documentation**: https://playwright.dev/
- **Inclusive Design Principles**: https://inclusivedesignprinciples.org/
- **A11y Project Checklist**: https://www.a11yproject.com/checklist/

---

## Production Validation

**This skill is based on real design review workflows** used at:
- **Methodology inspiration**: Stripe, Airbnb, Linear (7-phase systematic approach)
- **Testing approach**: Automated browser testing with Playwright/Puppeteer
- **Accessibility standards**: WCAG 2.1 AA compliance (industry standard)

**Estimated token efficiency:**
- Without skill: ~25k tokens (trial-and-error, repeated corrections)
- With skill: ~8k tokens (guided methodology, systematic approach)
- **Savings: ~68%** with 100% checklist coverage

---

**Questions or issues?**

1. Check [references/accessibility-wcag.md](references/accessibility-wcag.md) for complete WCAG checklist
2. See [references/browser-tools-reference.md](references/browser-tools-reference.md) for Playwright/Chrome DevTools commands
3. Review [references/visual-polish.md](references/visual-polish.md) for design principles
4. Verify browser tools are installed (see `playwright-testing` or `chrome-devtools` skills)
5. Ensure preview URL is live and accessible
