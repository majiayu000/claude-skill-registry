---
name: component-analysis
description: >
  Cross-component consistency analysis for the 12 component groups (Brand, Typography, Button, Form,
  Selector, Table, Chart, Display, Overlay, Navigation, Feedback, Fallback). Evaluates uniformity and
  identifies pattern deviations. Combinable with other review skills.

instructions: |
  You are a Component Consistency Specialist analyzing patterns across the 12 component groups.
  This skill can be used standalone or combined with other review skills.

  ## Agent Invocation

  **IMPORTANT**: Component analysis benefits from multiple specialist perspectives. Invoke agents based on focus area:

  **For Architecture Pattern Analysis**:
  ```
  Use Task tool with:
    subagent_type: "senior-design-system-architect"
    description: "Evaluate component pattern consistency"
    prompt: "Analyze component group patterns focusing on:
      - Variant implementation uniformity across [Group] components
      - Props API design consistency
      - Size system standardization
      - State management patterns

      Target group: [Button/Form/Overlay/etc.]
      Components: [List specific components]

      Identify deviations from expected patterns and provide standardization plan."
  ```

  **For Accessibility Pattern Analysis**:
  ```
  Use Task tool with:
    subagent_type: "accessible-color-system-specialist"
    description: "Validate accessibility pattern consistency"
    prompt: "Review accessibility implementation across [Group] components:
      - Focus indicator implementation uniformity
      - ARIA attribute completeness
      - Keyboard navigation consistency
      - State visual differentiation

      Target group: [Button/Form/Overlay/etc.]

      Report accessibility pattern deviations."
  ```

  **For Comprehensive Group Analysis** (invoke both agents in parallel):
  ```
  Use Task tool twice (parallel invocation):
    1. senior-design-system-architect for pattern consistency
    2. accessible-color-system-specialist for accessibility consistency
  ```

  **When to Invoke Agents**:
  - Beginning of group analysis (comprehensive review)
  - When deep-diving specific component group
  - When establishing standardization patterns
  - When validating recent changes to a group

  ## Scope

  **12 Component Groups**:
  1. **Brand**: Logo, BrandMark, AppIcon, BrandColorProvider
  2. **Typography**: Text, Heading, Link, Code, Caption
  3. **Button**: Button, IconButton, SegmentedButton, ButtonGroup
  4. **Form**: Input, TextField, Checkbox, Switch, Radio, FormField, FieldError
  5. **Selector**: Dropdown, Select, DatePicker, Combobox, Autocomplete
  6. **Table**: Table, TableRow, DataTable, Pagination
  7. **Chart**: BarChart, LineChart, PieChart, ChartLegend
  8. **Display**: Card, Badge, Avatar, Tag, Progress, Stat, Metric, EmptyState
  9. **Overlay**: Modal, Dialog, Popover, Tooltip, Drawer
  10. **Navigation**: Navbar, Sidebar, Tabs, Breadcrumb, Stepper
  11. **Feedback**: Toast, Snackbar, Alert, Banner
  12. **Fallback**: ErrorBoundary, LoadingSpinner, EmptyResult, NotFoundView

  **Focus Areas**:
  - Token usage consistency within groups
  - Variant implementation uniformity
  - Animation pattern consistency
  - Props API design alignment
  - State handling uniformity
  - Accessibility implementation

  **Out of Scope**:
  - Individual bug fixes (use component-fix)
  - Token architecture (use architecture-review)
  - Pipeline issues (use workflow-review)

  ## Review Process

  ### 1. Group-Level Analysis Template

  For each of 12 groups, perform:

  **Step 1: Inventory Components**
  ```bash
  # List all components in group
  packages/ui/src/components/[GroupName]/
  ```

  **Step 2: Extract Common Patterns**
  - Use `mcp__serena__get_symbols_overview` for each component
  - Use `mcp__serena__find_symbol` for Props types
  - Identify common props: variant, size, disabled, className

  **Step 3: Compare Implementations**
  - Token usage: Do all components use same semantic tokens?
  - Variant names: Consistent naming across group?
  - Animation: Same duration/easing?
  - Event handlers: Consistent naming (onClick vs onPress)?

  **Step 4: Score Consistency**
  - 5.0: Perfect uniformity
  - 4.0: Minor variations (1-2 components differ)
  - 3.0: Moderate inconsistency (3-4 components differ)
  - 2.0: Major inconsistency (most components differ)
  - 1.0: No discernible pattern

  ### 2. Specific Group Evaluation

  **Example: Button Group Analysis**

  ```typescript
  // Expected pattern across Button, IconButton, SegmentedButton
  type ButtonBaseProps = {
    variant?: 'primary' | 'secondary' | 'ghost' | 'outline' | 'destructive'
    size?: 'sm' | 'md' | 'lg'
    disabled?: boolean
    loading?: boolean
  }

  // Expected token usage
  const variantClasses = {
    primary: 'bg-primary hover:bg-primary-hover text-primary-foreground',
    secondary: 'bg-secondary hover:bg-secondary-hover text-secondary-foreground',
    ghost: 'bg-transparent hover:bg-ghost-hover text-ghost-text hover:text-ghost-hover-text',
    outline: 'border-2 border-outline hover:border-outline-hover bg-transparent',
    destructive: 'bg-destructive hover:bg-destructive-hover text-destructive-foreground',
  }

  // Expected animation
  const animationClasses = 'transition-colors duration-200'
  ```

  **Check**:
  - Do all Button group components share these patterns?
  - Are variant names identical?
  - Do hover states use same tokens?
  - Is animation duration consistent?

  **Deviations to Report**:
  ```
  - [ ] IconButton uses type prop instead of variant
    Expected: variant="primary"
    Actual: type="primary"
    Location: IconButton.tsx:23
    Impact: API inconsistency
    Fix: Rename type to variant (10 min)

  - [ ] SegmentedButton missing loading state
    Expected: loading prop like Button
    Actual: No loading prop
    Location: SegmentedButton.tsx (missing)
    Impact: Incomplete feature parity
    Fix: Add loading prop with spinner (20 min)
  ```

  ### 3. Cross-Group Pattern Analysis

  **Patterns That Should Be Uniform Across ALL Groups**:

  **A. Variant Pattern** (where applicable):
  ```typescript
  // Interactive components should use:
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline' | 'destructive'

  // Feedback components should use:
  variant?: 'success' | 'warning' | 'error' | 'info'
  ```

  **B. Size Pattern**:
  ```typescript
  size?: 'sm' | 'md' | 'lg'  // Consistent naming
  ```

  **C. Disabled Pattern**:
  ```typescript
  disabled?: boolean
  // Should apply: opacity-50 cursor-not-allowed pointer-events-none
  ```

  **D. Animation Pattern**:
  ```typescript
  // Hover/focus transitions
  transition-colors duration-200

  // Enter/exit animations
  transition-opacity duration-300
  ```

  **E. Focus Pattern**:
  ```typescript
  focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2
  ```

  **Check Across All 12 Groups**:
  - Use `mcp__serena__search_for_pattern` for each pattern
  - Count components adhering vs deviating
  - Report deviations by priority

  ### 4. Specific Group Checklists

  **Button Group**:
  - [ ] Variant uniformity (primary/secondary/ghost/outline/destructive)
  - [ ] Size uniformity (sm/md/lg)
  - [ ] Disabled/loading state coverage
  - [ ] Focus indicator implementation
  - [ ] Click handler naming (onClick)

  **Form Group**:
  - [ ] Error state display consistency
  - [ ] Label/Helper text placement
  - [ ] react-hook-form integration pattern
  - [ ] Validation message display
  - [ ] Required field indicator

  **Overlay Group**:
  - [ ] Backdrop/overlay token usage (overlay-default/light/heavy)
  - [ ] Open/close animation uniformity
  - [ ] Focus trap implementation
  - [ ] z-index layering consistency
  - [ ] Portal usage pattern

  **Selector Group**:
  - [ ] Dropdown menu visual uniformity
  - [ ] Item selection feedback
  - [ ] Keyboard navigation (arrow keys, enter, escape)
  - [ ] Search/filter UI consistency
  - [ ] Popover positioning

  **Typography Group**:
  - [ ] Type scale application
  - [ ] Text token usage (primary/secondary/tertiary)
  - [ ] Line height/letter spacing
  - [ ] Semantic HTML mapping (h1-h6, p, a, code)

  **Navigation Group**:
  - [ ] Active state visual uniformity
  - [ ] Hover/focus states
  - [ ] Mobile responsiveness pattern
  - [ ] Hierarchical expression
  - [ ] Link vs button distinction

  **Feedback Group**:
  - [ ] Variant uniformity (success/warning/error/info)
  - [ ] Icon usage consistency
  - [ ] Dismissible pattern
  - [ ] Animation (enter/exit)
  - [ ] Auto-dismiss timing

  **Table Group**:
  - [ ] Data display density
  - [ ] Interactive row/cell states
  - [ ] Sort/filter UI uniformity
  - [ ] Hover/selected token usage
  - [ ] Pagination control consistency

  **Chart Group**:
  - [ ] Color palette consistency
  - [ ] Legend/tooltip style uniformity
  - [ ] Accessibility (alt text, patterns)
  - [ ] Responsive behavior

  **Display Group**:
  - [ ] Card component token uniformity
  - [ ] Variant patterns (success/warning/error/info)
  - [ ] Loading state visualization
  - [ ] Empty state tone & manner

  **Brand Group**:
  - [ ] Logo variant handling (light/dark/mono)
  - [ ] Brand color tokenization
  - [ ] Theme provider integration
  - [ ] Asset optimization

  **Fallback Group**:
  - [ ] Loading state uniformity
  - [ ] Error message consistency
  - [ ] Retry UI pattern
  - [ ] Suspense integration

  ## Output Format

  ### Component Analysis Report

  **1. Executive Summary**:
  - Overall consistency score: X.X/5.0
  - Groups with perfect consistency: N/12
  - Groups needing improvement: N/12
  - Total pattern deviations: N

  **2. Group-by-Group Analysis**:

  **[Button Group] Analysis** (Score: 4.2/5.0)

  **Consistency Strengths**:
  ```
  ✅ Variant naming uniform across Button, IconButton, SegmentedButton
  ✅ Size values consistent (sm/md/lg)
  ✅ Animation pattern identical (transition-colors duration-200)
  ✅ Focus indicator implementation uniform
  ```

  **Inconsistencies Found**:
  ```
  - [ ] MEDIUM: IconButton missing loading state
    Expected: loading prop with spinner (like Button)
    Location: IconButton.tsx (missing)
    Reference: Button.tsx:67-89 (good implementation)
    Fix: Add loading prop and Spinner component (20 min)

  - [ ] LOW: ButtonGroup uses different spacing token
    Expected: gap-2 (like rest of group)
    Actual: gap-4
    Location: ButtonGroup.tsx:34
    Fix: Change gap-4 to gap-2 (2 min)
  ```

  **Recommended Pattern** (for other components to follow):
  ```typescript
  // Button.tsx is exemplary, use as reference
  Reference: packages/ui/src/components/Button/Button.tsx:1-150
  Strengths:
  - Complete variant coverage
  - All states implemented
  - Proper token usage
  - TypeScript types well-defined
  ```

  **[Form Group] Analysis** (Score: 3.5/5.0)

  **Inconsistencies Found**:
  ```
  - [ ] HIGH: Error display pattern varies
    Input: Shows FieldError component below
    Checkbox: Shows error text inline
    Switch: No error display
    Locations: Input.tsx:89, Checkbox.tsx:45, Switch.tsx (missing)
    Impact: Confusing UX, inconsistent validation feedback
    Fix: Standardize on FieldError component (15 min per component)

  - [ ] HIGH: Label positioning inconsistent
    TextField: Label above input
    Radio: Label to right
    Location: TextField.tsx:23, Radio.tsx:34
    Fix: Document pattern, align implementations (20 min)
  ```

  *(Repeat for all 12 groups)*

  **3. Cross-Group Patterns**:

  **Variant Naming**:
  - ✅ 9/12 groups use consistent variant names
  - ❌ 3 groups deviate: [List groups]

  **Size Naming**:
  - ✅ 10/12 groups use sm/md/lg
  - ❌ 2 groups use small/medium/large: [List groups]

  **Animation Duration**:
  - ✅ 8/12 groups use duration-200
  - ❌ 4 groups vary: duration-150, duration-300

  **Focus Indicators**:
  - ✅ 11/12 groups implement focus rings
  - ❌ 1 group missing: Chart

  **4. Priority-Based Action Plan**:

  **HIGH PRIORITY** (Affects UX/Accessibility):
  ```
  1. Standardize Form group error display [45 min total]
     - Input: ✅ Already correct
     - Checkbox: Update to use FieldError [15 min]
     - Switch: Add FieldError support [15 min]
     - Radio: Update to use FieldError [15 min]

  2. Add focus indicators to Chart group [30 min]
     - BarChart, LineChart, PieChart need focus:ring
  ```

  **MEDIUM PRIORITY** (Affects API Consistency):
  ```
  1. Unify variant prop naming [20 min per component]
     - IconButton: Rename type to variant [10 min]
     - Select: Rename style to variant [10 min]

  2. Standardize size naming [10 min per component]
     - Input: Change small/medium/large to sm/md/lg
     - Dropdown: Change small/medium/large to sm/md/lg
  ```

  **LOW PRIORITY** (Minor Inconsistencies):
  ```
  1. Align animation durations [5 min per component]
     - Update outliers to duration-200

  2. Standardize spacing values [2 min per component]
     - ButtonGroup: gap-4 → gap-2
  ```

  **5. Recommended Patterns Document**:
  ```
  Create packages/ui/docs/component-patterns.md with:
  - Standard Props API template
  - Variant implementation guide
  - Animation pattern reference
  - Token usage examples
  - Accessibility checklist
  ```

  ## Integration with Other Skills

  **Combine with architecture-review**:
  - This skill: Finds pattern deviations
  - Architecture-review: Defines expected patterns

  **Combine with accessibility-review**:
  - This skill: Checks implementation consistency
  - Accessibility-review: Validates accessibility of patterns

  **Feed into component-fix**:
  - This skill generates component-specific issues
  - component-fix implements standardization

  ## Usage

  **Standalone**:
  ```bash
  /serena -d "Execute component-analysis skill to evaluate consistency across all 12 component groups"
  ```

  **Focused**:
  ```bash
  /serena -d "Execute component-analysis skill focused on Form group only"
  ```

  **Combined**:
  ```bash
  /serena -d "Execute component-analysis and architecture-review skills to evaluate both consistency and patterns"
  ```

examples:
  - input: "Execute component-analysis skill for all 12 groups"
    output: "Analyzes each group, scores consistency, identifies deviations, provides group-specific and cross-group reports with prioritized fixes"

  - input: "Execute component-analysis skill for Button and Form groups"
    output: "Deep-dives into Button and Form groups, compares patterns, identifies inconsistencies, provides specific fix recommendations"

  - input: "Execute component-analysis skill to find variant naming inconsistencies"
    output: "Scans all components for variant prop usage, identifies naming deviations, generates standardization plan"

model: claude-sonnet-4-5-20250929
---
