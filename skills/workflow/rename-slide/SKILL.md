# Rename Slide Skill

Rename a slide's identifier, title, and/or file.

## Auto-invoke triggers
- "rename slide"
- "change slide name"
- "update slide title"

## Workflow

### Step 1: Identify Slide
Ask which slide to rename (by number or current name).

### Step 2: Gather New Names
Ask what to rename:
- **File name** (kebab-case, e.g., "client-success")
- **Title** (full title for sidebar, e.g., "Client Success Story")
- **Short title** (abbreviated for nav, e.g., "Success")
- **ID** (unique identifier, usually same as file name)

User can update any combination of these.

### Step 3: Preview Changes
Show:
```
Current:
  File: 05-stats.tsx
  Export: Slide05Stats
  ID: stats
  Title: Impact Metrics
  Short: Stats

After rename:
  File: 05-results.tsx
  Export: Slide05Results
  ID: results
  Title: Key Results
  Short: Results
```

Ask for confirmation.

### Step 4: Execute Rename

1. **Rename the file**:
   - `git mv src/deck/slides/05-stats.tsx src/deck/slides/05-results.tsx`
   - Or rename directly if not using git

2. **Update export in slide file**:
   - Change `export function Slide05Stats()` to `export function Slide05Results()`

3. **Update config.ts**:
   - Update import path: `from "./slides/05-results"`
   - Update import name: `{ Slide05Results }`
   - Update config entry:
     ```typescript
     {
       id: "results",
       title: "Key Results",
       shortTitle: "Results",
       component: Slide05Results,
     }
     ```

### Step 5: Verify
Run `pnpm build` to ensure no errors.

## Naming Conventions

| Field | Format | Example |
|-------|--------|---------|
| File | `NN-kebab-case.tsx` | `05-client-success.tsx` |
| Export | `SlideNNCamelCase` | `Slide05ClientSuccess` |
| ID | `kebab-case` | `client-success` |
| Title | Title Case | `Client Success Story` |
| Short Title | 1-2 words | `Success` |

## Example

User: "Rename slide 8 from 'quote' to 'testimonial'"

Changes:
```
File:   08-quote.tsx      -> 08-testimonial.tsx
Export: Slide08Quote      -> Slide08Testimonial
ID:     quote             -> testimonial
Title:  Testimonial       -> Customer Testimonial
Short:  Quote             -> Testimonial
```

## Partial Rename

User can rename just the title without changing the file:

"Change slide 5 title to 'Performance Metrics'"

Only updates `config.ts`:
```typescript
{
  id: "stats",           // unchanged
  title: "Performance Metrics",  // updated
  shortTitle: "Metrics",         // optionally updated
  component: Slide05Stats,       // unchanged
}
```
