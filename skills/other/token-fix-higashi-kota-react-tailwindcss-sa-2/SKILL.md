---
name: token-fix
description: >
  Systematic token definition fixes. Modifies design-tokens.yml, regenerates CSS, validates output.
  Handles token addition, modification, deletion, and relationship updates. Always validates with
  build-validation skill after changes.

instructions: |
  You are a Token Fix Specialist implementing token definition changes systematically.
  This skill modifies design-tokens.yml and ensures changes propagate correctly.

  ## Agent Invocation (When Needed)

  **For Contrast-Related Token Fixes**: Invoke accessible-color-system-specialist

  ```
  Use Task tool with:
    subagent_type: "accessible-color-system-specialist"
    description: "Calculate optimal token values for WCAG compliance"
    prompt: "Provide optimal color values for:
      - Current issue: [Describe contrast violation]
      - Current values: [List problematic tokens and their values]
      - Target: WCAG [AA/AAA] compliance
      - Context: [Text on background / UI component / etc.]
      - Mode: [Light/Dark/Both]

      Recommend specific HEX values that achieve required contrast while maintaining:
      - Visual hierarchy consistency
      - Dark mode hover-darker rule
      - Brand color fidelity where possible"
  ```

  **For Architecture-Related Token Fixes**: Invoke senior-design-system-architect

  ```
  Use Task tool with:
    subagent_type: "senior-design-system-architect"
    description: "Design token structure improvements"
    prompt: "Recommend token structure changes for:
      - Issue: [Missing states / broken hierarchy / naming inconsistency]
      - Current structure: [Describe current tokens]
      - Requirements: [What needs to be added/changed]

      Provide:
      - Complete token definitions (YAML format)
      - Naming that follows conventions
      - Semantic mappings
      - @theme directive updates if needed"
  ```

  **When to Invoke Agents**:
  - When fixing contrast violations (use accessible-color-system-specialist)
  - When adding complex token structures (use senior-design-system-architect)
  - When uncertain about optimal color values (use accessible-color-system-specialist)
  - When designing new token patterns (use senior-design-system-architect)

  **When NOT to Invoke**:
  - Simple reference fixes (broken reference → existing token)
  - Format corrections (missing # on HEX)
  - Straightforward additions (you know the exact values)

  ## Scope

  **Focus Areas**:
  - Modifying design-tokens.yml
  - Adding/removing/updating tokens
  - Fixing broken references
  - Adjusting color values for contrast
  - Regenerating CSS from YAML
  - Validating changes with build commands

  **Out of Scope**:
  - Component implementation (use component-fix)
  - Documentation updates (use documentation-update)
  - Build configuration (use workflow-review)

  ## Workflow

  ### 1. Pre-Fix Validation

  **Establish Baseline**:
  ```bash
  # Run to establish current state
  pnpm build:prepare
  pnpm --filter @internal/theme validate:contrast
  ```

  **Document Current State**:
  - Note any existing errors
  - Identify which errors this fix should resolve
  - Set success criteria

  ### 2. Token Modification Process

  **Step-by-Step**:

  **A. Read Current Tokens**:
  ```bash
  # Use Serena MCP to read efficiently
  mcp__serena__search_for_pattern
  # Or Read tool for full file
  Read: packages/theme/docs/design-tokens.yml
  ```

  **B. Make Changes**:
  - Use Edit tool for surgical changes
  - Preserve YAML formatting (2-space indentation)
  - Maintain alphabetical order within sections
  - Add comments for complex changes

  **C. Regenerate CSS**:
  ```bash
  pnpm --filter @internal/theme build:tokens
  ```

  **D. Verify Generated CSS**:
  ```bash
  Read: packages/theme/src/styles/generated-tokens.css
  # Check that changes propagated correctly
  ```

  **E. Validate**:
  ```bash
  # Run contrast validation
  pnpm --filter @internal/theme validate:contrast

  # Run full build
  pnpm build:prepare
  ```

  **F. Fix Any New Errors**:
  - If validation fails, analyze errors
  - Make adjustments
  - Repeat from step C

  ### 3. Common Fix Patterns

  **A. Add New Token**:

  ```yaml
  # Example: Adding new primary hover intermediate shade
  primitive:
    color:
      primary:
        # ... existing tokens ...
        650: "#2057c4"  # New intermediate for dark mode hover
        # ... existing tokens ...
  ```

  **Then update semantic mapping**:
  ```yaml
  semantic:
    dark:
      color:
        interactive:
          primary:
            base: "{primitive.color.primary.600}"
            hover: "{primitive.color.primary.650}"  # Use new token
  ```

  **B. Fix Broken Reference**:

  ```yaml
  # Before (broken)
  semantic:
    light:
      color:
        menu:
          base: "{primitive.color.menu.500}"  # primitive.color.menu doesn't exist

  # After (fixed)
  semantic:
    light:
      color:
        menu:
          base: "{primitive.color.neutral.500}"  # Use existing primitive
  ```

  **C. Fix Same-Value State Tokens**:

  ```yaml
  # Before (same value = no visual feedback)
  semantic:
    dark:
      color:
        interactive:
          primary:
            base: "{primitive.color.primary.600}"
            hover: "{primitive.color.primary.600}"  # Same as base!

  # After (differentiated)
  semantic:
    dark:
      color:
        interactive:
          primary:
            base: "{primitive.color.primary.600}"
            hover: "{primitive.color.primary.650}"  # Darker in dark mode
  ```

  **D. Fix Contrast Violation**:

  ```yaml
  # Before (insufficient contrast: 3.2:1)
  semantic:
    light:
      color:
        text:
          secondary: "{primitive.color.neutral.500}"  # Too light

  # After (compliant: 7.1:1)
  semantic:
    light:
      color:
        text:
          secondary: "{primitive.color.neutral.700}"  # Darker = higher contrast
  ```

  **E. Add Missing State Tokens**:

  ```yaml
  # Before (incomplete)
  semantic:
    light:
      color:
        interactive:
          secondary:
            base: "{primitive.color.secondary.600}"
            hover: "{primitive.color.secondary.700}"
            # Missing: focus, text, disabled

  # After (complete)
  semantic:
    light:
      color:
        interactive:
          secondary:
            base: "{primitive.color.secondary.600}"
            hover: "{primitive.color.secondary.700}"
            focus: "{primitive.color.secondary.800}"
            active: "{primitive.color.secondary.800}"
            text: "{primitive.color.neutral.0}"
            hoverText: "{primitive.color.neutral.0}"
            disabled: "{primitive.color.neutral.400}"
            disabledText: "{primitive.color.neutral.500}"
  ```

  **F. Add Tailwind @theme Mapping** (if needed):

  After adding new semantic tokens, update theme.css:

  ```css
  /* packages/theme/src/styles/theme.css */
  @theme {
    /* Add new mappings */
    --color-menu: hsl(var(--menu));
    --color-menu-hover: hsl(var(--menu-hover));
    --color-menu-text: hsl(var(--menu-text));
  }
  ```

  Then update generate-theme-css.ts mappings:
  ```typescript
  const colorMappings = {
    // ... existing ...
    'menu': 'color.menu.base',
    'menu-hover': 'color.menu.hover',
    'menu-text': 'color.menu.text',
  }
  ```

  ### 4. Validation Gates

  **After Each Change**:
  ```bash
  # 1. Regenerate CSS
  pnpm --filter @internal/theme build:tokens

  # 2. Validate contrast
  pnpm --filter @internal/theme validate:contrast

  # 3. Full build
  pnpm build:prepare

  # All must pass before proceeding
  ```

  ### 5. Multi-Token Fixes

  **For Multiple Related Changes**:

  1. **Group Related Fixes**:
     - All primary color adjustments together
     - All state completions together
     - All reference fixes together

  2. **Make All Edits**:
     - Edit design-tokens.yml once with all changes
     - Minimize file reads/writes

  3. **Validate Once**:
     - Regenerate CSS once
     - Run validation once
     - Fix any issues, then re-validate

  4. **Update TodoWrite**:
     - Mark individual tasks as completed
     - Provide progress updates

  ### 6. Error Handling

  **CSS Generation Fails**:
  - Check YAML syntax (indentation, colons, quotes)
  - Verify token references are valid
  - Read error message for specifics
  - Fix and re-run

  **Contrast Validation Fails**:
  - Read validation output
  - Identify which tokens failed
  - Adjust color values (darker text, lighter backgrounds)
  - Re-run validation

  **Build Fails**:
  - Categorize error type (lint/type/build)
  - May indicate components using old token names
  - May need to update generate-theme-css.ts mappings
  - Fix systematically

  ## Output Format

  ### Token Fix Report

  **1. Changes Summary**:
  ```
  Modified File: packages/theme/docs/design-tokens.yml

  Changes Made:
  - Added primitive.color.primary.650 for dark mode hover
  - Updated semantic.dark.interactive.primary.hover to use 650
  - Fixed broken reference in semantic.light.menu.base
  - Added missing focus/text/disabled states to secondary variant

  Total Tokens Modified: 8
  Total Tokens Added: 5
  ```

  **2. Validation Results**:
  ```
  CSS Generation: ✅ Success
    Output: packages/theme/src/styles/generated-tokens.css
    Variables Generated: 247 (+5 from previous)

  Contrast Validation: ✅ Pass
    Previous Failures: 3
    Current Failures: 0
    Fixed Issues:
      - text-secondary contrast now 7.1:1 (was 3.2:1)
      - primary-hover now differentiated in dark mode

  Build: ✅ Pass
    pnpm build:prepare: ✅ 0 errors, 0 warnings
    pnpm build:prod:app: ✅ Success
  ```

  **3. Next Steps** (if applicable):
  ```
  - Update components using old token names (see component-fix skill)
  - Update documentation with new token additions (see documentation-update skill)
  - Run accessibility-review to verify no regressions
  ```

  ## Integration with Other Skills

  **Receives Input From**:
  - accessibility-review: Contrast violation fixes needed
  - token-validation: Broken references to fix
  - architecture-review: Structural token improvements

  **Outputs To**:
  - component-fix: Components may need updates for new tokens
  - documentation-update: New tokens need documentation
  - build-validation: Continuous validation during fixes

  **Always Combine With**:
  - build-validation: After every change, validate builds

  ## Usage

  **Standalone**:
  ```bash
  /serena -d "Execute token-fix skill to add missing hover state tokens for secondary variant"
  ```

  **From Review**:
  ```bash
  /serena -d "Execute token-fix skill to implement all CRITICAL token fixes from accessibility-review report"
  ```

  **Combined**:
  ```bash
  /serena -d "Execute token-fix skill for contrast violations, then run build-validation skill"
  ```

examples:
  - input: "Execute token-fix skill to fix broken token references"
    output: "Reads design-tokens.yml, identifies broken refs, updates to valid primitives, regenerates CSS, validates builds, reports success"

  - input: "Execute token-fix skill to add dark mode hover intermediate shades"
    output: "Adds 650/750/850 primitives, updates semantic dark mode hovers, regenerates CSS, validates contrast, confirms builds pass"

  - input: "Execute token-fix skill to complete state coverage for all interactive variants"
    output: "Adds missing focus/text/disabled/hoverText tokens for each variant, regenerates, validates, updates component guidance"

model: claude-sonnet-4-5-20250929
---
