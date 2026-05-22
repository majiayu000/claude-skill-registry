---
name: vendure-admin-ui-reviewing
description: Review Vendure Admin UI extensions for React pattern violations, missing hooks, improper state management, and UI anti-patterns. Use when reviewing Admin UI PRs or auditing UI quality.
version: 1.0.0
---

# Vendure Admin UI Reviewing

## Purpose

Audit Vendure Admin UI extensions for violations and anti-patterns.

## Review Workflow

### Step 1: Identify UI Files

```bash
# Find UI extension files
find . -path "*/ui/*.ts" -o -path "*/ui/*.tsx"

# Find component files
find . -name "*.tsx" -path "*/components/*"

# Find hook files
find . -name "use*.ts" -path "*/hooks/*"
```

### Step 2: Run Automated Checks

```bash
# === CRITICAL VIOLATIONS ===

# Direct fetch calls (should use Vendure hooks)
grep -rn "fetch(" --include="*.tsx" --include="*.ts" | grep -v "node_modules"

# Missing useInjector for services
grep -rn "NotificationService" --include="*.tsx" | grep -v "useInjector"

# Angular patterns in React code
grep -rn "@Component\|@Injectable\|ngOnInit" --include="*.tsx"

# Missing page metadata
grep -rn "export function.*List\|export function.*Detail" --include="*.tsx" -A 20 | grep -v "usePageMetadata"

# === HIGH PRIORITY ===

# Missing loading states
grep -rn "useQuery" --include="*.tsx" -A 10 | grep -v "loading"

# Missing error states
grep -rn "useQuery" --include="*.tsx" -A 10 | grep -v "error"

# Direct state mutation
grep -rn "\.push(\|\.splice(\|\.pop(" --include="*.tsx"

# Missing useCallback/useMemo
grep -rn "onClick.*=.*async" --include="*.tsx" | grep -v "useCallback"

# === MEDIUM PRIORITY ===

# Inline styles (should use CSS variables)
grep -rn 'style={{' --include="*.tsx"

# Missing TypeScript types on GraphQL queries
grep -rn "useQuery(" --include="*.tsx" | grep -v "useQuery<"

# Console.log statements
grep -rn "console.log\|console.error" --include="*.tsx" --include="*.ts"
```

### Step 3: Manual Review Checklist

#### Extension Structure

- [ ] index.ts exports AdminUiExtension
- [ ] routes.ts uses registerReactRouteComponent
- [ ] providers.ts uses addNavMenuSection
- [ ] Translations file exists if needed
- [ ] GraphQL codegen configured

#### Components

- [ ] usePageMetadata for title/breadcrumbs
- [ ] useInjector(NotificationService) for notifications
- [ ] Loading state handled
- [ ] Error state handled
- [ ] useCallback for event handlers
- [ ] useMemo for expensive computations

#### GraphQL Integration

- [ ] Queries in separate files
- [ ] TypeScript types from codegen
- [ ] Proper refetch after mutations
- [ ] Error handling on mutations

#### Styling

- [ ] CSS variables for colors/spacing
- [ ] Responsive design considered
- [ ] No hardcoded pixel values
- [ ] Theme consistency with Vendure

---

## Severity Classification

### CRITICAL (Must Fix)

- Direct fetch calls bypassing Vendure hooks
- Angular patterns in React code
- Missing error handling
- No loading states

### HIGH (Should Fix)

- Missing usePageMetadata
- Missing useInjector for services
- Direct state mutation
- Inline styles
- Missing TypeScript types

### MEDIUM (Should Fix)

- Missing useCallback/useMemo
- Console statements
- Hardcoded strings (no translations)
- Missing accessibility attributes

---

## Common Violations

### 1. Missing Loading State

**Violation:**

```typescript
export function ItemList() {
    const { data } = useQuery(GET_ITEMS);

    return (
        <table>
            {data?.items.map(item => (
                <tr key={item.id}>{item.name}</tr>
            ))}
        </table>
    );
}
```

**Fix:**

```typescript
export function ItemList() {
    const { data, loading, error } = useQuery(GET_ITEMS);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <table>
            {data?.items.map(item => (
                <tr key={item.id}>{item.name}</tr>
            ))}
        </table>
    );
}
```

### 2. Missing useInjector

**Violation:**

```typescript
// Directly importing and using service
import { NotificationService } from "@vendure/admin-ui/core";

export function ItemForm() {
  const handleSave = async () => {
    NotificationService.success("Saved!"); // WRONG
  };
}
```

**Fix:**

```typescript
import { NotificationService } from "@vendure/admin-ui/core";
import { useInjector } from "@vendure/admin-ui/react";

export function ItemForm() {
  const notificationService = useInjector(NotificationService);

  const handleSave = async () => {
    notificationService.success("Saved!"); // CORRECT
  };
}
```

### 3. Missing Page Metadata

**Violation:**

```typescript
export function ItemDetail() {
    // No page metadata!
    return (
        <div>
            <h1>Item Details</h1>
            {/* content */}
        </div>
    );
}
```

**Fix:**

```typescript
export function ItemDetail() {
    const { setTitle, setBreadcrumb } = usePageMetadata();

    React.useEffect(() => {
        setTitle('Item Details');
        setBreadcrumb([
            { label: 'Items', link: ['/extensions/my-plugin/items'] },
            { label: 'Details', link: [] }
        ]);
    }, [setTitle, setBreadcrumb]);

    return (
        <PageBlock>
            {/* content */}
        </PageBlock>
    );
}
```

### 4. Direct State Mutation

**Violation:**

```typescript
const [items, setItems] = React.useState<Item[]>([]);

const addItem = (item: Item) => {
  items.push(item); // WRONG - mutating state
  setItems(items);
};
```

**Fix:**

```typescript
const [items, setItems] = React.useState<Item[]>([]);

const addItem = React.useCallback((item: Item) => {
  setItems((prev) => [...prev, item]); // CORRECT - new array
}, []);
```

### 5. Missing TypeScript Types on Query

**Violation:**

```typescript
const { data } = useQuery(GET_ITEMS); // No type!
// data is 'any'
```

**Fix:**

```typescript
const { data } = useQuery<GetItemsQuery>(GET_ITEMS);
// data is properly typed
```

### 6. Missing useCallback on Event Handlers

**Violation:**

```typescript
export function ItemList() {
    const handleDelete = async (id: string) => {
        // Creates new function on every render
    };

    return items.map(item => (
        <button onClick={() => handleDelete(item.id)}>Delete</button>
    ));
}
```

**Fix:**

```typescript
export function ItemList() {
    const handleDelete = React.useCallback(async (id: string) => {
        // Memoized function
    }, [/* dependencies */]);

    return items.map(item => (
        <button onClick={() => handleDelete(item.id)}>Delete</button>
    ));
}
```

---

## Quick Detection Commands

```bash
# All-in-one UI audit
echo "=== CRITICAL: Direct fetch calls ===" && \
grep -rn "fetch(" --include="*.tsx" | grep -v "node_modules" | head -10 && \
echo "" && \
echo "=== HIGH: Missing loading states ===" && \
grep -rn "useQuery" --include="*.tsx" -l | xargs -I{} sh -c 'grep -L "loading" {} 2>/dev/null' | head -10 && \
echo "" && \
echo "=== MEDIUM: Missing TypeScript types ===" && \
grep -rn "useQuery(" --include="*.tsx" | grep -v "useQuery<" | head -10
```

---

## Review Output Template

```markdown
## Admin UI Review: [Component/Feature Name]

### Summary

[Overview of UI quality]

### Critical Issues (Must Fix)

- [ ] [Issue] - `file:line`

### High Priority

- [ ] [Issue] - `file:line`

### Passed Checks

- [x] Extension structure correct
- [x] Routes properly registered
- [x] Navigation items configured
- [x] Loading states handled

### Recommendations

- [Suggestions]
```

---

## Extension Structure Checklist

```markdown
## Extension Structure Review

### Required Files

- [ ] ui/index.ts - AdminUiExtension export
- [ ] ui/routes.ts - registerReactRouteComponent
- [ ] ui/providers.ts - addNavMenuSection

### GraphQL Setup

- [ ] ui/graphql/queries.ts - Query definitions
- [ ] ui/graphql/mutations.ts - Mutation definitions
- [ ] ui/gql/graphql.ts - Generated types
- [ ] ui/codegen.yml - Codegen configuration

### Component Organization

- [ ] components/ - React components
- [ ] hooks/ - Custom hooks
- [ ] styles/ - CSS files
- [ ] translations/ - i18n files
```

---

## Cross-Reference

All rules match patterns in **vendure-admin-ui-writing** skill.

---

## Related Skills

- **vendure-admin-ui-writing** - UI patterns
- **vendure-plugin-reviewing** - Plugin-level review
- **vendure-graphql-reviewing** - GraphQL review
