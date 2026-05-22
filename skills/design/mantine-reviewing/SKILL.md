---
name: mantine-reviewing
description: Review React components using Mantine UI library for accessibility, Styles API correctness, component patterns, and common pitfalls. Use when reviewing Mantine code or before merging Mantine-based PRs.
version: 1.0.0
---

# Mantine Code Review

## Purpose

Review React components using Mantine UI library for accessibility compliance, Styles API correctness, component pattern adherence, and common pitfall detection.

## When NOT to Use

- Non-Mantine React components (use general React review)
- Backend code review
- Mantine v6 or earlier (patterns differ)
- Initial development (use `mantine-developing` skill instead)

## Review Workflow

### Step 1: Identify Mantine Files

```bash
# Find files using Mantine
grep -r "from '@mantine" --include="*.tsx" --include="*.ts" -l
```

### Step 2: Run Automated Checks

```bash
# TypeScript errors
npm run typecheck

# Lint issues
npm run lint

# Check for common issues
grep -rn "disabled.*Tooltip\|Tooltip.*disabled" --include="*.tsx"
grep -rn "Accordion\.Control.*Button\|Button.*Accordion\.Control" --include="*.tsx"
grep -rn "ActionIcon[^>]*>" --include="*.tsx" | grep -v "aria-label"
```

### Step 3: Manual Review

Use CHECKLIST.md for comprehensive review criteria.

### Step 4: Report Findings

Format findings by severity:
- **CRITICAL**: Accessibility violations, invalid HTML
- **HIGH**: Performance issues, incorrect patterns
- **MEDIUM**: Style issues, suboptimal approaches
- **LOW**: Minor improvements, suggestions

## Critical Review Areas

### 1. Accessibility (CRITICAL)

**Must check:**
```tsx
// ❌ FAIL: Missing aria-label on icon button
<ActionIcon onClick={handleSearch}>
  <IconSearch />
</ActionIcon>

// ✅ PASS: Has aria-label
<ActionIcon aria-label="Search" onClick={handleSearch}>
  <IconSearch />
</ActionIcon>
```

**Review for:**
- All `ActionIcon` components have `aria-label`
- All `CloseButton` have `aria-label` or parent has `closeButtonLabel`
- Heading hierarchy correct (`order` prop on Accordion)
- Focus states visible (not removed by custom CSS)
- Keyboard navigation works

### 2. Nested Interactive Elements (CRITICAL)

**Invalid HTML - browsers will break layout:**
```tsx
// ❌ FAIL: Button inside button (Accordion.Control is a button)
<Accordion.Control>
  Click here <Button>Delete</Button>
</Accordion.Control>

// ✅ PASS: Button outside Control
<Group>
  <Accordion.Control style={{ flex: 1 }}>Click here</Accordion.Control>
  <Button>Delete</Button>
</Group>
```

**Check all:**
- `Accordion.Control` has no Button, ActionIcon, or Link children
- `Button` has no interactive children
- `UnstyledButton` has no interactive children

### 3. Styles API Usage (HIGH)

**Check for anti-patterns:**
```tsx
// ❌ FAIL: Inline style only affects root
<Button style={{ color: 'red' }}>Text won't be red</Button>

// ❌ FAIL: !important hack
<Button className="my-button">...</Button>
.my-button span { color: red !important; }

// ✅ PASS: Correct Styles API usage
<Button styles={{ label: { color: 'red' } }}>Red text</Button>
<Button classNames={{ label: classes.redLabel }}>Red text</Button>
```

**Review for:**
- Using `classNames` or `styles` prop for inner elements
- No `!important` in CSS targeting Mantine components
- Correct selector names (check component's Styles API docs)
- CSS variables used appropriately

### 4. Tooltip on Disabled (HIGH)

**Tooltip won't show on truly disabled elements:**
```tsx
// ❌ FAIL: Tooltip invisible
<Tooltip label="Cannot submit">
  <Button disabled>Submit</Button>
</Tooltip>

// ✅ PASS: Use data-disabled
<Tooltip label="Cannot submit">
  <Button data-disabled onClick={(e) => e.preventDefault()}>
    Submit
  </Button>
</Tooltip>
```

### 5. ActionIcon.Group Structure (HIGH)

**Direct children only:**
```tsx
// ❌ FAIL: Wrapped children break styling
<ActionIcon.Group>
  <div><ActionIcon><IconEdit /></ActionIcon></div>
</ActionIcon.Group>

// ✅ PASS: Direct ActionIcon children
<ActionIcon.Group>
  <ActionIcon aria-label="Edit"><IconEdit /></ActionIcon>
  <ActionIcon aria-label="Delete"><IconTrash /></ActionIcon>
</ActionIcon.Group>
```

### 6. Select vs Autocomplete (MEDIUM)

```tsx
// When value MUST be from list → Select
<Select data={countries} />

// When free text is acceptable → Autocomplete
<Autocomplete data={suggestions} />
```

**Review for correct component choice based on requirements.**

### 7. Form Handling (MEDIUM)

**Prefer @mantine/form over manual state:**
```tsx
// ❌ Suboptimal: Manual state for each field
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');

// ✅ Better: useForm hook
const form = useForm({
  initialValues: { email: '', password: '' },
  validate: { email: (v) => ... }
});
<TextInput {...form.getInputProps('email')} />
```

**Review for:**
- Using `useForm` for forms with validation
- Using `getInputProps` for input binding
- Correct `type: 'checkbox'` for checkbox/switch inputs
- Validation configured appropriately

### 8. Dark Mode Compatibility (MEDIUM)

```tsx
// ❌ FAIL: Hardcoded colors break dark mode
<Box style={{ background: 'white', color: 'black' }}>

// ✅ PASS: Theme-aware colors
<Box style={{
  background: 'light-dark(white, var(--mantine-color-dark-7))',
  color: 'light-dark(black, white)'
}}>

// ✅ PASS: Theme color references
<Box bg="gray.0" c="dark.9">
```

### 9. Performance (MEDIUM)

**Check for:**
- Unnecessary re-renders from inline objects/functions
- Missing `useMemo`/`useCallback` for expensive operations
- Large lists without virtualization
- Heavy components not code-split

```tsx
// ❌ FAIL: New object every render
<Button styles={{ root: { padding: 10 } }}>

// ✅ PASS: Stable reference
const buttonStyles = { root: { padding: 10 } };
<Button styles={buttonStyles}>

// ✅ PASS: Or use CSS modules
<Button classNames={{ root: classes.button }}>
```

### 10. Polymorphic Component Types (LOW)

```tsx
// When using component prop, ref type changes
const buttonRef = useRef<HTMLButtonElement>(null); // Default
const linkRef = useRef<HTMLAnchorElement>(null);   // With component="a"

<Button ref={buttonRef}>Button</Button>
<Button component="a" ref={linkRef} href="/">Link</Button>
```

**Review for TypeScript errors related to ref types.**

## Review Output Template

```markdown
## Mantine Code Review: [Component/File]

### Summary
[1-2 sentence overview]

### Critical Issues
- [ ] [Issue description] - [file:line]

### High Priority
- [ ] [Issue description] - [file:line]

### Medium Priority
- [ ] [Issue description] - [file:line]

### Low Priority / Suggestions
- [ ] [Suggestion]

### Accessibility Audit
- [ ] All icon buttons have aria-label
- [ ] No nested interactive elements
- [ ] Keyboard navigation works
- [ ] Focus states visible

### Styles API Audit
- [ ] No !important hacks
- [ ] Correct selector usage
- [ ] Theme-aware colors

### Passed Checks
- [x] [What's good about the code]
```

## Quick Commands

```bash
# Find missing aria-labels on ActionIcon
grep -rn "ActionIcon" --include="*.tsx" | grep -v "aria-label"

# Find potential nested interactives
grep -rn "Accordion\.Control" -A5 --include="*.tsx" | grep -E "Button|ActionIcon|Link"

# Find disabled buttons in tooltips
grep -rn "Tooltip" -A3 --include="*.tsx" | grep "disabled"

# Find hardcoded colors
grep -rn "style={{" --include="*.tsx" | grep -E "color:|background:|bg:"

# Find inline style objects (potential perf issue)
grep -rn "styles={{" --include="*.tsx"
```

## Integration

**Related skills:**
- `mantine-developing` - Development patterns and guidance
- `hermes-code-reviewer` - General TypeScript review

**For detailed checklist:** See CHECKLIST.md


---

## Related Agent

For comprehensive React + Mantine UI guidance that coordinates this and other Mantine skills, use the **`mantine-ui-expert`** agent.

**Cost Optimization:** Use `model="haiku"` when invoking this agent for routine code reviews. Haiku is sufficient for pattern matching and Styles API validation.
