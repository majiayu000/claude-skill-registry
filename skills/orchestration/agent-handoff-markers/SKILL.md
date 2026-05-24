---
model: opus
created: 2025-12-16
modified: 2025-12-26
reviewed: 2025-12-26
name: agent-handoff-markers
description: Standardized inline markers for inter-agent communication. Use when creating handoff annotations for other agents, scanning for pending work from upstream agents, or when the user mentions handoff markers, agent coordination, or cross-agent communication.
allowed-tools: Glob, Grep, Read, Edit, Write, TodoWrite
---

# Agent Handoff Markers

Structured inline markers for asynchronous agent-to-agent communication.

## Benefits

### Asynchronous Agent Coordination
- Agents can request work from other agents without blocking
- Work can be discovered and processed in future sessions
- Enables non-linear development workflows

### Traceability
- Clear audit trail of inter-agent requests
- Completion markers show what was delivered
- Referenced files provide full context

### Reduced Context Switching
- Agents can complete their current work before handling handoffs
- Markers persist until addressed
- No need for immediate handoff processing

### Improved Code Documentation
- Markers serve as inline documentation of intent
- Requirements are captured at the point of need
- Context is preserved alongside the code

### Workflow Flexibility
- Any agent can create markers for any other agent
- Priority levels allow triage
- Type categorization enables filtering

### CI/CD Integration Potential
- Markers can be scanned in pre-commit hooks
- Blocking markers could fail builds if unaddressed
- Automated reports of pending work

## Core Concept

Handoff markers are structured comments in code that:
1. Request work from a specific agent
2. Provide context for the receiving agent
3. Define requirements and constraints
4. Track completion status

## Marker Format

### Basic Structure

```typescript
// @AGENT-HANDOFF-MARKER(target-agent) {
//   type: "category",
//   context: "what this code does",
//   needs: ["requirement 1", "requirement 2"],
//   priority: "blocking|enhancement",
//   refs: ["path/to/related/file"]
// }
```

### Full Example

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "form-validation",
//   context: "User registration form with email/password",
//   needs: [
//     "error message placement strategy",
//     "focus management on validation failure",
//     "ARIA live region for error announcements",
//     "inline vs summary validation decision"
//   ],
//   priority: "blocking",
//   refs: [
//     "src/components/FormField.tsx",
//     "docs/design/registration-flow.md"
//   ],
//   constraints: [
//     "must work with React Hook Form",
//     "mobile-first responsive"
//   ]
// }
async function handleRegistration(data: FormData) {
  try {
    await api.register(data);
  } catch (errors) {
    // @AGENT-PLACEHOLDER: implement error display
    console.error(errors);
  }
}
```

## Target Agents

### UX-Related Targets

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation)
// For: Accessibility, component UX, responsive patterns, design tokens

// @AGENT-HANDOFF-MARKER(service-design)
// For: User journey decisions, information architecture, high-level UX strategy
```

### Development Targets

```typescript
// @AGENT-HANDOFF-MARKER(typescript-development)
// For: Framework-specific implementation, type system, state management

// @AGENT-HANDOFF-MARKER(code-review)
// For: Quality review, security assessment, performance evaluation

// @AGENT-HANDOFF-MARKER(test-architecture)
// For: Test strategy, coverage requirements, test patterns
```

## Marker Types

### Component Implementation

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "component-implementation",
//   context: "Modal dialog for confirmation actions",
//   needs: [
//     "focus trap implementation",
//     "keyboard handling (Escape to close)",
//     "ARIA dialog pattern",
//     "animation on open/close"
//   ]
// }
```

### Accessibility

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "accessibility",
//   context: "Data table with sortable columns",
//   needs: [
//     "ARIA sort attributes",
//     "keyboard navigation for column headers",
//     "screen reader announcements for sort changes",
//     "focus management after sort"
//   ]
// }
```

### Form Validation

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "form-validation",
//   context: "Multi-step checkout form",
//   needs: [
//     "validation timing (blur vs submit)",
//     "error message positioning",
//     "progress indicator accessibility",
//     "step navigation keyboard support"
//   ]
// }
```

### Loading States

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "loading-states",
//   context: "Dashboard data fetching",
//   needs: [
//     "skeleton screen design",
//     "loading announcement for screen readers",
//     "error recovery UI",
//     "empty state handling"
//   ]
// }
```

### Design Tokens

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "design-tokens",
//   context: "Component library theming",
//   needs: [
//     "color token architecture",
//     "dark mode support",
//     "component-level token scoping",
//     "responsive token overrides"
//   ]
// }
```

### Responsive Behavior

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "responsive",
//   context: "Navigation menu",
//   needs: [
//     "mobile menu pattern (drawer/bottom sheet)",
//     "breakpoint strategy",
//     "touch target sizing",
//     "focus management across breakpoints"
//   ]
// }
```

## Priority Levels

### Blocking

Work cannot proceed without this. Use for:
- Critical accessibility barriers
- Core interaction patterns
- Required user flows

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "accessibility",
//   priority: "blocking",
//   context: "Form submit button",
//   needs: ["keyboard activation", "disabled state handling"]
// }
```

### Enhancement

Improves quality but not blocking. Use for:
- Performance optimizations
- Polish and refinement
- Non-critical improvements

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   type: "loading-states",
//   priority: "enhancement",
//   context: "Profile image upload",
//   needs: ["optimistic UI", "progress indicator animation"]
// }
```

## Scanning for Markers

### Finding All Handoffs

```bash
# Find all handoff markers
rg "@AGENT-HANDOFF-MARKER\(" --type ts --type tsx

# Find markers for specific agent
rg "@AGENT-HANDOFF-MARKER\(ux-implementation\)" --type ts

# Find blocking markers only
rg "@AGENT-HANDOFF-MARKER.*priority.*blocking" --type ts

# Count markers by agent
rg -o "@AGENT-HANDOFF-MARKER\([^)]+\)" | sort | uniq -c
```

### Agent Workflow

When starting work, agents should:

1. **Scan for incoming markers**
   ```bash
   rg "@AGENT-HANDOFF-MARKER\(ux-implementation\)" --type ts --type tsx -A 10
   ```

2. **Process each marker**
   - Read context and requirements
   - Check referenced files
   - Implement or specify solution

3. **Mark completion**
   ```typescript
   // @AGENT-HANDOFF-MARKER-COMPLETE(ux-implementation) {
   //   implemented: ["focus trap", "ARIA dialog", "Escape key"],
   //   notes: "Uses FocusTrap from @headlessui/react"
   // }
   ```

4. **Create downstream markers if needed**
   ```typescript
   // @AGENT-HANDOFF-MARKER(typescript-development) {
   //   type: "component-implementation",
   //   context: "Modal with UX specs defined above",
   //   needs: ["React component implementation", "state management"]
   // }
   ```

## Placeholder Patterns

### Simple Placeholder

```typescript
// @AGENT-PLACEHOLDER: error display implementation
console.error(errors);
```

### Detailed Placeholder

```typescript
// @AGENT-PLACEHOLDER {
//   waiting-for: "ux-implementation",
//   requirement: "accessible error announcements",
//   current-behavior: "logs to console"
// }
setErrors(validationErrors);
```

### Implementation Stub

```typescript
function showValidationErrors(errors: ValidationError[]) {
  // @AGENT-PLACEHOLDER: implement accessible error display
  // Requirements from @AGENT-HANDOFF-MARKER above:
  // - Focus first error field
  // - Announce via ARIA live region
  // - Display inline error messages

  // Temporary implementation
  errors.forEach(e => console.error(e.message));
}
```

## Completion Markers

### Simple Completion

```typescript
// @AGENT-HANDOFF-MARKER-COMPLETE(ux-implementation)
// Implemented: focus trap, ARIA attributes, keyboard handling
```

### Detailed Completion

```typescript
// @AGENT-HANDOFF-MARKER-COMPLETE(ux-implementation) {
//   resolved: "2024-01-15",
//   implemented: [
//     "WCAG 2.1 AA compliant",
//     "Focus trap using @headlessui/react",
//     "Escape key closes modal",
//     "Focus returns to trigger on close"
//   ],
//   tests: "src/__tests__/Modal.a11y.test.tsx",
//   notes: "Added to component library as BaseModal"
// }
```

## Integration with File-Based Coordination

Handoff markers complement the existing file-based system:

### Agent Output Files

When completing markers, update the agent output:

```markdown
<!-- ~/.claude/docs/ux-implementation-output.md -->

## Completed Handoffs

### Modal Dialog (src/components/Modal.tsx)
- Implemented focus trap
- Added ARIA attributes
- Keyboard navigation complete
- Tests added

### Registration Form (src/pages/Register.tsx)
- Error display pattern implemented
- Focus management on validation
- ARIA live regions for announcements

## Pending Downstream Work

- @AGENT-HANDOFF-MARKER(typescript-development) for Modal component wrapper
- @AGENT-HANDOFF-MARKER(test-architecture) for E2E accessibility tests
```

### Inter-Agent Context

Update shared context with marker status:

```json
{
  "workflow": "ux-implementation",
  "completed_handoffs": [
    "src/components/Modal.tsx:42",
    "src/pages/Register.tsx:156"
  ],
  "pending_handoffs": [
    {
      "file": "src/components/DataTable.tsx",
      "line": 89,
      "type": "accessibility",
      "priority": "blocking"
    }
  ]
}
```

## Best Practices

### Be Specific

```typescript
// Bad: Vague requirement
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   needs: ["make it accessible"]
// }

// Good: Specific requirements
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   needs: [
//     "ARIA combobox pattern for autocomplete",
//     "keyboard navigation (arrow keys, Enter, Escape)",
//     "screen reader announcement on selection"
//   ]
// }
```

### Provide Context

```typescript
// Bad: No context
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   needs: ["error handling"]
// }

// Good: Full context
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   context: "Payment form in checkout flow, high-stakes interaction",
//   needs: ["error recovery UX", "clear error messaging"],
//   constraints: ["PCI compliance", "real-time validation"]
// }
```

### Include References

```typescript
// @AGENT-HANDOFF-MARKER(ux-implementation) {
//   context: "Notification system",
//   refs: [
//     "docs/design/notifications.md",      // Design spec
//     "src/hooks/useNotifications.ts",     // Existing hook
//     "src/components/Toast/Toast.tsx"     // Related component
//   ]
// }
```

### Clean Up Completed Markers

After implementation, either:
1. Convert to `@AGENT-HANDOFF-MARKER-COMPLETE` marker
2. Remove marker and document in commit message
3. Move to documentation if pattern is reusable

## Command Integration

Use the `/handoffs` command to manage markers:

```bash
# List all pending handoffs
/handoffs

# Filter by agent
/handoffs --agent ux-implementation

# Show stale markers (>7 days)
/handoffs --stale

# Output as JSON for scripting
/handoffs --json
```

## References

- Agent Coordination Patterns: See agent-coordination-patterns skill
- File-Based Coordination: See agent-file-coordination skill
- Multi-Agent Workflows: See multi-agent-workflows skill
