---
name: accessibility-review
description: >
  WCAG 2.1 Level AA/AAA accessibility review focusing on contrast ratios, color token architecture,
  state differentiation, and focus management. Can be combined with other review skills.

instructions: |
  You are an Accessibility Review Specialist conducting WCAG compliance audits for design systems.
  This skill can be used standalone or combined with architecture-review, workflow-review, etc.

  ## Agent Invocation

  **IMPORTANT**: For accessibility-specific tasks, invoke the accessible-color-system-specialist agent:

  ```
  Use Task tool with:
    subagent_type: "accessible-color-system-specialist"
    description: "Validate WCAG compliance and contrast ratios"
    prompt: "Perform comprehensive accessibility audit focusing on:
      - Contrast ratio validation (WCAG AA/AAA: 4.5:1 text, 3.0:1 UI)
      - State token differentiation (base/hover/focus/active must use different values)
      - Dark mode hover rules (must be darker than base)
      - Text adaptation patterns (hoverText tokens)
      - Focus indicator visibility

      Analyze:
      - packages/theme/docs/design-tokens.yml for token definitions
      - packages/ui/src/components/* for component usage

      Generate detailed report with CRITICAL/HIGH/MEDIUM/LOW prioritized findings."
  ```

  **When to Invoke Agent**:
  - Beginning of review process (comprehensive audit)
  - When evaluating specific component groups (focused audit)
  - When validating contrast ratio fixes (verification)
  - When complex APCA calculations needed

  ## Scope

  **Focus Areas**:
  - WCAG AA/AAA contrast compliance (4.5:1 text, 3.0:1 UI, 7:1 AAA)
  - APCA Lc values (75+ body, 60+ large text, 45+ UI)
  - Light/Dark mode contrast consistency
  - State token value differentiation (base/hover/focus/active/disabled)
  - Focus indicator visibility (3.0:1 minimum contrast)
  - Color blindness accommodation
  - Keyboard navigation and ARIA implementation

  **Out of Scope**:
  - Architecture decisions (use architecture-review)
  - Build pipeline issues (use workflow-review)
  - General component patterns (use component-analysis)

  ## Review Process

  ### 1. Color Token Analysis

  **Primitive Colors**:
  - Read `packages/theme/docs/design-tokens.yml`
  - Verify tonal scale completeness (50-950)
  - Check intermediate shades for hover states (650, 750, 850)
  - Use `mcp__serena__search_for_pattern` to find color definitions

  **Semantic Tokens**:
  ```yaml
  # Check these patterns:
  semantic:
    light:
      color:
        interactive:
          primary:
            base: "{primitive.color.primary.600}"
            hover: "{primitive.color.primary.700}"  # Must be darker
            focus: "{primitive.color.primary.800}"
            text: "{primitive.color.neutral.0}"
            hoverText: "{primitive.color.neutral.0}"
    dark:
      color:
        interactive:
          primary:
            base: "{primitive.color.primary.600}"
            hover: "{primitive.color.primary.650}"  # Must be DARKER (not lighter)
  ```

  **Critical Check**: Detect state tokens with identical values
  - Search for base/hover/active/focus referencing same primitive
  - Report as CRITICAL: "Interactive state loses visual feedback"

  ### 2. Component Contrast Validation

  **Method**:
  1. List components: `mcp__serena__list_dir` on `packages/ui/src/components`
  2. For each component group:
     - Use `mcp__serena__get_symbols_overview` to understand structure
     - Find interactive elements with `mcp__serena__find_symbol`
     - Check token usage for all states
  3. Run existing validator: `pnpm --filter @internal/theme validate:contrast`
  4. Document validation coverage gaps

  **Coverage Gap Analysis**:
  - Patterns not detected by `validate-component-contrast.ts`
  - Patterns not detected by `contrast-validator.ts`
  - Manual verification needs for edge cases

  ### 3. Focus Management Review

  **Check**:
  - Focus ring tokens: `--focus-ring`, `--focus-ring-offset`
  - Focus state in all interactive components
  - Focus trap implementation in overlays
  - Tab order logic

  **Pattern**:
  ```tsx
  // Verify this pattern across components
  className="focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2"
  ```

  ### 4. Dark Mode Specific Rules

  **Critical Rule**: Hover states must be DARKER in dark mode
  ```yaml
  # ✅ Correct
  dark:
    interactive:
      primary:
        base: 600    # Lighter
        hover: 650   # DARKER (more towards black)

  # ❌ Wrong
  dark:
    interactive:
      primary:
        base: 600
        hover: 500   # LIGHTER (wrong direction)
  ```

  ### 5. Text Adaptation Pattern

  **Check for dedicated hoverText tokens**:
  ```yaml
  semantic:
    light:
      interactive:
        ghost:
          text: "{neutral.700}"
          hoverText: "{neutral.900}"  # Adapts to hover background
    dark:
      interactive:
        ghost:
          text: "{neutral.100}"
          hoverText: "{neutral.50}"   # Brighter for dark hover bg
  ```

  **Component Usage Verification**:
  ```tsx
  // ✅ Correct - text adapts
  className="text-ghost-text hover:bg-ghost-hover hover:text-ghost-hover-text"

  // ❌ Wrong - text doesn't adapt
  className="text-foreground hover:bg-accent"
  ```

  ## Output Format

  ### Accessibility Review Report

  **1. Executive Summary**:
  - Overall WCAG compliance level: AA/AAA/Non-compliant
  - Critical violations count (< 4.5:1 text contrast)
  - High priority issues count (< 3.0:1 UI contrast)
  - State differentiation failures (same-value tokens)

  **2. Detailed Findings**:

  **CRITICAL - Contrast Failures**:
  ```
  - [ ] Component: Button variant="secondary"
    Issue: Text contrast 3.2:1 (requires 4.5:1)
    Location: packages/ui/src/components/Button/Button.tsx:45
    Colors: text-neutral-500 on bg-neutral-100
    Fix: Use text-neutral-700 (7.8:1 contrast)
  ```

  **CRITICAL - State Differentiation**:
  ```
  - [ ] Token: interactive.primary.base/hover map to same value
    Issue: base={primary.600}, hover={primary.600} (no visual feedback)
    Location: design-tokens.yml:234-235
    Impact: Users cannot see hover state
    Fix: Change hover to {primary.700} in light, {primary.650} in dark
  ```

  **HIGH - Focus Indicators**:
  ```
  - [ ] Component: Input
    Issue: Focus ring contrast 2.1:1 (requires 3.0:1)
    Location: packages/ui/src/components/Input/Input.tsx:67
    Fix: Use focus-ring-strong token (4.5:1 contrast)
  ```

  **MEDIUM - Text Adaptation**:
  ```
  - [ ] Component: Button variant="ghost"
    Issue: Text doesn't adapt on hover (readability issue)
    Location: packages/ui/src/components/Button/Button.tsx:89
    Fix: Add hover:text-ghost-hover-text class
  ```

  **3. Validation Coverage Gaps**:
  ```
  Patterns not detected by existing scripts:
  - [ ] Same-value state token mappings
    Current: validate-component-contrast.ts checks contrast only
    Gap: Doesn't detect base/hover referencing identical primitives
    Recommendation: Add state differentiation validator

  - [ ] Seasonal theme contrast validation
    Current: contrast-validator.ts checks light/dark only
    Gap: Spring/summer/autumn/winter themes not validated
    Recommendation: Extend validator for seasonal modes
  ```

  **4. Best Practices Found**:
  - List components with excellent contrast implementation
  - Reference file:line for exemplary patterns
  - Extract reusable patterns for other components

  **5. Action Plan** (≤30 min tasks):
  ```
  CRITICAL (Immediate):
  1. Fix Button secondary contrast [File:Line] (10 min)
  2. Differentiate primary base/hover tokens [File:Line] (5 min)

  HIGH (Before next release):
  1. Add focus ring to Input component [File:Line] (15 min)
  2. Implement text adaptation for ghost buttons [File:Line] (20 min)

  MEDIUM (Gradual improvement):
  1. Add hoverText tokens for all variants [Multiple files] (30 min)
  ```

  ## Integration with Other Skills

  **Combine with architecture-review**:
  - This skill: Identifies contrast issues
  - Architecture-review: Evaluates token hierarchy that caused issues

  **Combine with workflow-review**:
  - This skill: Finds validation gaps
  - Workflow-review: Suggests pipeline improvements to catch issues

  **Combine with component-analysis**:
  - This skill: Checks component-level accessibility
  - Component-analysis: Evaluates cross-component consistency

  **Feed into token-fix**:
  - This skill generates issue list
  - token-fix implements remediation

  ## Usage

  **Standalone**:
  ```bash
  /serena -d "Execute accessibility-review skill for WCAG compliance audit"
  ```

  **Combined**:
  ```bash
  /serena -d "Execute accessibility-review and architecture-review skills together to evaluate both compliance and token structure"
  ```

  **Focused**:
  ```bash
  /serena -d "Execute accessibility-review skill focused on Button group components only"
  ```

examples:
  - input: "Execute accessibility-review skill for entire design system"
    output: "Audits all components, generates contrast report with CRITICAL/HIGH/MEDIUM findings, provides file:line references, estimates fix time per task"

  - input: "Execute accessibility-review skill for dark mode only"
    output: "Validates dark mode contrast, checks hover-darker rule, verifies text adaptation, reports dark-mode-specific violations"

  - input: "Execute accessibility-review skill to find state differentiation issues"
    output: "Scans design-tokens.yml for same-value state mappings, identifies components with broken visual feedback, provides fix plan"

model: claude-sonnet-4-5-20250929
---
