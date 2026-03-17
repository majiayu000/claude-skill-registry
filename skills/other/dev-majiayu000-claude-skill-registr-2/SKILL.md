---
name: css-development:validate
description: Review existing CSS against established Tailwind + semantic component patterns, checking naming, dark mode, tests, and documentation
---

# CSS Development: Validate

## Overview

Reviews existing CSS code against established patterns and provides specific, actionable feedback:
- Semantic naming conventions
- Tailwind `@apply` composition
- Dark mode variant coverage
- Test coverage (static + rendering)
- Documentation quality
- Composition opportunities

**This is a sub-skill of `css-development`** - typically invoked automatically via the main skill.

## When This Skill Applies

Use when:
- Reviewing existing CSS code
- Auditing component styles for consistency
- Checking if patterns are being followed
- Before merging CSS changes
- Refactoring prep (identify issues first)

## Pattern Reference

This skill validates against patterns documented in the main `css-development` skill:

**Semantic naming:** `.button-primary` not `.btn-blue`
**Tailwind composition:** Use `@apply` to compose utilities
**Dark mode:** Include `dark:` variants
**Test coverage:** Static CSS + component rendering tests
**Documentation:** Usage comments above classes

## Workflow

When this skill is invoked, create a TodoWrite checklist and work through validation systematically.

### Announce Usage

"I'm using the css-development:validate skill to review this CSS against established patterns."

### Create TodoWrite Checklist

Use the TodoWrite tool:

```
Validating CSS:
- [ ] Read CSS files (load components.css and related styles)
- [ ] Check semantic naming (verify descriptive class names)
- [ ] Verify @apply usage (ensure Tailwind composition)
- [ ] Check dark mode coverage (confirm dark: variants present)
- [ ] Look for composition opportunities (identify reusable patterns)
- [ ] Verify test coverage (check static and rendering tests exist)
- [ ] Check documentation (ensure usage comments present)
- [ ] Report findings (provide file:line references and suggestions)
```

### Validation Checklist Details

#### Step 1: Read CSS Files

**Action:** Use Read tool to load CSS files for review

**Files to check:**
- `styles/components.css` (main semantic components)
- Any component-specific CSS files mentioned
- Inline styles in component files (if applicable)

**What to capture:**
- All class definitions
- Usage of `@apply` vs. inline utilities
- Presence of dark mode variants
- Documentation comments

**Mark as completed** when files are loaded and understood.

---

#### Step 2: Check Semantic Naming

**Action:** Review all class names for semantic, descriptive naming

**Good patterns:**
- `.button-primary`, `.card-header`, `.form-field`, `.empty-state`
- Context + component: `.session-card`, `.marketing-hero`
- Base + variant: `.badge-success`, `.button-danger`

**Bad patterns (report these):**
- Utility names: `.btn-blue`, `.card-sm`, `.text-big`
- Abbreviations: `.btn`, `.hdr`, `.desc`
- Generic: `.component`, `.item`, `.thing`
- Random: `.style1`, `.custom`, `.special`

**For each issue:**
- Note file and line number
- Show the problematic class name
- Suggest semantic alternative based on usage context

**Mark as completed** when all class names reviewed.

---

#### Step 3: Verify @apply Usage

**Action:** Check that Tailwind utilities are composed via `@apply`, not scattered in markup

**Good patterns:**
```css
.button-primary {
  @apply bg-indigo-500 hover:bg-indigo-700 px-6 py-3 rounded-lg;
}
```

**Bad patterns (report these):**
```html
<!-- Utilities in markup instead of semantic class -->
<button class="bg-indigo-500 hover:bg-indigo-700 px-6 py-3 rounded-lg">
  Click me
</button>
```

**Check:**
- Are utilities composed into semantic classes via `@apply`?
- Are there repeated utility combinations in markup that should be extracted?
- Are semantic classes actually being used in components?

**For each issue:**
- Show the problematic markup or CSS
- Explain why it should use `@apply`
- Suggest extraction to semantic class

**Mark as completed** when @apply usage is reviewed.

---

#### Step 4: Check Dark Mode Coverage

**Action:** Verify colored and interactive elements have `dark:` variants

**What needs dark mode:**
- Background colors (bg-*)
- Text colors (text-*)
- Border colors (border-*)
- Interactive states (hover, focus)
- Shadows that affect visibility

**What typically doesn't need dark mode:**
- Spacing utilities (p-*, m-*, gap-*)
- Layout utilities (flex, grid, etc.)
- Pure structural styles

**Pattern to check:**
```css
/* Good - has dark mode */
.card {
  @apply bg-white dark:bg-gray-800 text-gray-900 dark:text-white;
}

/* Bad - missing dark mode */
.card {
  @apply bg-white text-gray-900;
}
```

**For each issue:**
- Note which class is missing dark mode variants
- Show the current CSS
- Suggest specific `dark:` utilities to add

**Mark as completed** when dark mode coverage is checked.

---

#### Step 5: Look for Composition Opportunities

**Action:** Identify repeated patterns that could use existing classes or be extracted

**Look for:**
- Same utility combinations repeated in multiple classes
- Similar patterns that could share a base class
- Inline utilities that could reference semantic classes

**Example issue:**
```css
/* Repeated pattern */
.card-primary {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
}

.card-secondary {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
  @apply border-2 border-gray-200;
}

/* Suggestion: Extract base .card class, add variants */
.card {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
}

.card-secondary {
  @apply border-2 border-gray-200;
}
```

**For each opportunity:**
- Show the repeated pattern
- Suggest base class + composition
- Estimate impact (how many places benefit)

**Mark as completed** when composition opportunities are identified.

---

#### Step 6: Verify Test Coverage

**Action:** Check that CSS classes have test coverage

**Static CSS tests** - Check `styles/__tests__/components.test.ts`:
```typescript
it('should have button-primary class', () => {
  expect(content).toContain('.button-primary');
});
```

**Component rendering tests** - Check component test files:
```typescript
it('applies button-primary class', () => {
  render(<Button variant="primary">Click</Button>);
  expect(screen.getByRole('button')).toHaveClass('button-primary');
});
```

**For classes without tests:**
- List the class name
- Note which test is missing (static, rendering, or both)
- Provide test template to add

**Mark as completed** when test coverage is checked.

---

#### Step 7: Check Documentation

**Action:** Verify components have usage documentation

**Required documentation:**
- Comment above CSS class explaining purpose
- Usage example in comment

**Example:**
```css
/* Button component - Primary action button with hover lift effect
   Usage: <button className="button-primary">Click me</button> */
.button-primary {
  ...
}
```

**For classes without documentation:**
- List the class name and location
- Suggest documentation to add based on class purpose

**Mark as completed** when documentation is checked.

---

#### Step 8: Report Findings

**Action:** Compile all findings into structured report

**Report format:**

```markdown
## CSS Validation Report

### ✅ Good Patterns Found

- `.button-primary` follows semantic naming (components.css:15)
- Dark mode variants present on interactive elements (components.css:17-19)
- Tests cover className application (Button.test.tsx:23)
- Documentation comments present (components.css:14)

### ⚠️ Issues Found

#### Semantic Naming Issues

**components.css:45** - `.btn-blue` uses utility naming
- Current: `.btn-blue`
- Suggestion: Rename to `.button-secondary` for consistency with `.button-primary`
- Impact: Update 3 component files

**components.css:67** - `.card-sm` uses size in name
- Current: `.card-sm`
- Suggestion: Extract size to utility or rename to `.card-compact` for semantic meaning
- Impact: Update 5 usages

#### Missing Dark Mode Variants

**components.css:78** - `.card-header` missing dark mode
- Current: `@apply bg-gray-100 text-gray-900`
- Suggestion: Add `dark:bg-gray-800 dark:text-white`
- Impact: Visual bug in dark mode

**components.css:92** - `.badge` missing dark mode
- Current: `@apply bg-indigo-100 text-indigo-800`
- Suggestion: Add `dark:bg-indigo-900 dark:text-indigo-200`
- Impact: Low contrast in dark mode

#### Missing Test Coverage

**components.css:102** - `.empty-state` has no tests
- Missing: Both static CSS test and component rendering test
- Suggestion: Add tests to verify class exists and renders correctly

#### Missing Documentation

**components.css:115** - `.session-card` lacks usage comment
- Suggestion: Add comment explaining purpose and usage example

### 📊 Summary

- **Total classes reviewed:** 12
- **Issues found:** 7
- **Priority:** 2 high (dark mode bugs), 3 medium (naming), 2 low (docs)

### 🎯 Recommended Actions

1. **High priority:** Add dark mode variants to `.card-header` and `.badge` (visual bugs)
2. **Medium priority:** Rename `.btn-blue` → `.button-secondary` for consistency
3. **Medium priority:** Add test coverage for `.empty-state`
4. **Low priority:** Add documentation comments to undocumented classes

Would you like me to fix these issues, or would you prefer to address them manually?
```

**Mark as completed** when report is generated and presented.

---

### Completion

After generating the validation report:

1. **Ask user what they want to do next:**
   - Fix issues automatically?
   - Fix specific issues only?
   - Just wanted the report?

2. **Offer to invoke refactor skill** if there are structural issues that need refactoring

3. **Suggest committing** any fixes made
