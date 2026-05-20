---
name: tanstack-integration
description: "Find opportunities to improve web application code using TanStack libraries (Query, Table, Form, Router, etc.). Avoid man-with-hammer syndrome by applying TanStack after vanilla implementation works."
---

# TanStack Integration — Strategic Library Adoption

> **Philosophy:** Avoid "man with a hammer syndrome" (to whom everything appears as a nail). Start vanilla, then strategically adopt TanStack where it provides clear benefits.
>
> **Timing:** Use this AFTER your app is already working pretty well in vanilla Next.js/React/Tailwind.

---

## What is TanStack?

TanStack is a set of high-quality libraries for web applications:

| Library | Purpose |
|---------|---------|
| **TanStack Query** | Server state management, caching, synchronization |
| **TanStack Table** | Headless table/grid logic |
| **TanStack Form** | Form state management and validation |
| **TanStack Router** | Type-safe routing |
| **TanStack Virtual** | Virtualization for large lists |
| **TanStack Ranger** | Range/slider components |

---

## The Anti-Pattern: Premature Adoption

**Don't do this:**
1. Start new project
2. Immediately install all TanStack libraries
3. Force everything through TanStack patterns
4. End up with over-engineered code

**Why it's bad:**
- Not every feature needs TanStack
- Adds complexity where simple solutions work
- Makes code harder to understand for no benefit
- "Man with a hammer" sees every problem as a nail

---

## The Correct Pattern: Strategic Adoption

**Do this instead:**
1. Build with vanilla Next.js 16, React 19, Tailwind
2. Get the app working well
3. Run the TanStack analysis prompt
4. Adopt TanStack only where it clearly improves things
5. Repeat several rounds

---

## THE EXACT PROMPT — TanStack Analysis

```
Ok, I want you to look through the ENTIRE project and look for areas where, if we leveraged one of the many TanStack libraries (e.g., query, table, forms, etc), we could make part of the code much better, simpler, more performant, more maintainable, elegant, shorter, more reliable, etc. Use ultrathink
```

---

## When to Use Each TanStack Library

### TanStack Query

**Good candidates:**
- API calls that need caching
- Data that's fetched frequently
- Optimistic updates
- Background refetching
- Pagination with caching
- Infinite scroll

**Skip if:**
- Simple one-time fetches
- Static data
- Data that doesn't need synchronization

### TanStack Table

**Good candidates:**
- Complex data tables with sorting/filtering
- Tables with pagination
- Column resizing/reordering
- Row selection
- Expandable rows
- Server-side data tables

**Skip if:**
- Simple static tables
- Tables with < 20 rows
- No interactivity needed

### TanStack Form

**Good candidates:**
- Complex multi-step forms
- Forms with complex validation
- Forms with dynamic fields
- Forms with async validation
- Wizard-style workflows

**Skip if:**
- Simple contact forms
- Forms with 3-4 fields
- Basic validation needs

### TanStack Router

**Good candidates:**
- Large apps needing type-safe routing
- Complex nested routes
- Route-based code splitting
- Search params management

**Skip if:**
- Using Next.js App Router (already good)
- Simple navigation needs
- Few routes

### TanStack Virtual

**Good candidates:**
- Lists with 1000+ items
- Infinite scroll views
- Large data grids
- Chat message lists

**Skip if:**
- Lists with < 100 items
- Already using windowing elsewhere
- Performance is fine without it

---

## Integration Workflow

### Step 1: Get App Working

Build your app with vanilla patterns first:
- `fetch` or axios for API calls
- Native form handling
- Simple HTML tables
- Next.js routing

### Step 2: Run Analysis

Use the TanStack analysis prompt with Claude Code + Opus 4.5 or Codex + GPT 5.2 (High reasoning effort).

### Step 3: Evaluate Suggestions

The model will identify opportunities. For each:
- Does the complexity justify the benefit?
- Is the current solution actually problematic?
- Will this improve maintainability?

### Step 4: Selective Adoption

Only adopt where there's clear benefit. It's fine to:
- Use TanStack Query but not Table
- Use Table for one complex table, not all tables
- Mix vanilla and TanStack approaches

### Step 5: Repeat

Run the analysis again after changes. New opportunities may emerge.

---

## Best Models for This Task

| Model | Configuration |
|-------|---------------|
| **Claude Code + Opus 4.5** | Use ultrathink |
| **Codex + GPT 5.2** | High or Extra-High reasoning effort |

---

## Example Improvements

### Before: Manual Data Fetching

```typescript
// Vanilla approach
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  fetch('/api/users')
    .then(res => res.json())
    .then(setData)
    .catch(setError)
    .finally(() => setLoading(false));
}, []);
```

### After: TanStack Query

```typescript
// TanStack Query approach
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: () => fetch('/api/users').then(res => res.json()),
});
```

**Benefits:**
- Built-in caching
- Automatic refetching
- Request deduplication
- DevTools support

### Before: Complex Table Logic

```typescript
// Vanilla approach with manual sorting, filtering, pagination
// ... 200+ lines of state management
```

### After: TanStack Table

```typescript
// TanStack Table handles sorting, filtering, pagination
const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
});
```

**Benefits:**
- Headless (you control the UI)
- All table logic handled
- Consistent behavior
- Much less code

---

## Creating Beads for TanStack Work

```bash
bd create "Evaluate TanStack Query opportunities" -t enhancement -p 3
bd create "Migrate user data fetching to TanStack Query" -t enhancement -p 2
bd create "Implement data table with TanStack Table" -t feature -p 2
bd create "Add TanStack Virtual to chat message list" -t performance -p 2
```

---

## Complete Prompt Reference

### TanStack Analysis
```
Ok, I want you to look through the ENTIRE project and look for areas where, if we leveraged one of the many TanStack libraries (e.g., query, table, forms, etc), we could make part of the code much better, simpler, more performant, more maintainable, elegant, shorter, more reliable, etc. Use ultrathink
```

### Focused Query Analysis
```
Look through the project for data fetching patterns that would benefit from TanStack Query. Consider caching needs, refetching patterns, and optimistic updates. Identify the top 3 opportunities. Use ultrathink.
```

### Focused Table Analysis
```
Look through the project for table/grid components that would benefit from TanStack Table. Consider sorting, filtering, pagination, and column management needs. Identify candidates. Use ultrathink.
```

---

## Tips

1. **Don't over-adopt** — Some vanilla patterns are fine
2. **Measure the benefit** — Does it actually improve the code?
3. **Consider team familiarity** — TanStack has a learning curve
4. **Check bundle size** — Only import what you need
5. **Read the docs** — TanStack documentation is excellent
