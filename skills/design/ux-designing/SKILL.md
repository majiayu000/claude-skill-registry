---
name: ux-designing
description: Design user interfaces, user flows, and interactions for web applications. Use when designing new features, improving existing interfaces, creating user flows, designing forms, or planning page layouts. Triggers on requests like "design a UI for", "improve this interface", "create a user flow", "design this form", "plan the layout", or "make this more user-friendly".
---

# UX Designing

Design effective user experiences for this Next.js CMS application.

## Process

1. **Understand the user goal** - What are they trying to accomplish?
2. **Map the current flow** - How do users achieve this today?
3. **Identify friction points** - Where do users struggle?
4. **Design improvements** - Propose interface changes
5. **Consider edge cases** - Error states, empty states, loading

## User Flow Mapping

Document flows with states and transitions:

```
[Start] → [Action] → [Decision] → [Outcome]
                  ↓
              [Alt Path]
```

Example - Article Publishing:
```
[Dashboard] → [New Article] → [Edit Form] → [Preview] → [Publish]
                    ↓              ↓
              [Save Draft]   [Schedule]
```

## Interface Patterns

### Forms

**Progressive Disclosure**
- Show only relevant fields initially
- Reveal advanced options on demand
- Group related fields visually

**Validation**
- Inline validation as user types
- Clear error messages near fields
- Success confirmation on submit

```tsx
// Good: Inline validation with clear feedback
<input
  className={error ? 'border-red-500' : 'border-gray-300'}
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && <p id="email-error" className="text-red-500 text-sm">{error}</p>}
```

### Tables (Admin)

**Essential Features**
- Sortable columns
- Pagination with count
- Bulk actions
- Quick filters
- Row actions (edit, delete, view)

**Empty States**
- Explain why empty
- Provide action to add first item
- Use illustration/icon for visual interest

### Modals

**When to Use**
- Confirmations (delete, publish)
- Quick edits without navigation
- Media selection

**Best Practices**
- Clear title and purpose
- Obvious close mechanism
- Focus trap for accessibility
- Escape key to close

### Loading States

```tsx
// Skeleton loading for content
<div className="animate-pulse">
  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>

// Spinner for actions
<button disabled={loading}>
  {loading ? <Spinner /> : 'Save'}
</button>
```

## Page Layout Patterns

### Admin Pages
```
┌─────────────────────────────────────────┐
│ Header (logo, user menu)                │
├──────────┬──────────────────────────────┤
│          │ Page Title + Actions         │
│ Sidebar  ├──────────────────────────────┤
│ (nav)    │                              │
│          │ Content Area                 │
│          │                              │
│          │                              │
└──────────┴──────────────────────────────┘
```

### Public Pages
```
┌─────────────────────────────────────────┐
│ Header (nav, auth menu)                 │
├─────────────────────────────────────────┤
│                                         │
│ Main Content                            │
│                                         │
├─────────────────────────────────────────┤
│ Footer (links, copyright)               │
└─────────────────────────────────────────┘
```

## Tailwind Patterns for This Project

Use existing theme CSS variables:

```tsx
// Primary actions
className="bg-primary text-primary-foreground hover:bg-primary/90"

// Secondary actions
className="bg-secondary text-secondary-foreground hover:bg-secondary/80"

// Destructive actions
className="bg-red-600 text-white hover:bg-red-700"

// Cards/containers
className="bg-card text-card-foreground border border-border rounded-lg"
```

## Output

Provide UX design deliverables:
1. User flow diagram (text-based)
2. Component specifications
3. State descriptions (loading, empty, error)
4. Tailwind class suggestions
5. Accessibility considerations
