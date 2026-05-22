---
name: code-simplifying
description: Simplify and refine code for clarity, consistency, and maintainability. Use when asked to simplify code, reduce complexity, remove duplication, improve readability, refactor for clarity, or clean up messy code. Triggers on requests like "simplify this", "clean up this code", "make this more readable", "reduce complexity", or "refactor for clarity".
---

# Code Simplifying

Analyze and simplify code to improve clarity, reduce complexity, and enhance maintainability.

## Process

1. **Identify the target code** - Read the file(s) to be simplified
2. **Analyze complexity indicators**:
   - Deeply nested conditionals (>3 levels)
   - Long functions (>50 lines)
   - Duplicated logic
   - Complex boolean expressions
   - Unclear variable/function names
   - Mixed concerns in single functions
3. **Apply simplification techniques**
4. **Verify behavior preserved** - Run tests if available

## Simplification Techniques

### Extract and Name
```typescript
// Before: unclear intent
if (user.role === 'admin' || (user.role === 'editor' && resource.authorId === user.id)) {

// After: named condition
const canEdit = user.role === 'admin' || (user.role === 'editor' && resource.authorId === user.id);
if (canEdit) {
```

### Early Returns
```typescript
// Before: nested
function process(data) {
  if (data) {
    if (data.valid) {
      return transform(data);
    }
  }
  return null;
}

// After: early returns
function process(data) {
  if (!data) return null;
  if (!data.valid) return null;
  return transform(data);
}
```

### Extract Functions
```typescript
// Before: inline logic
const articles = data.map(item => ({
  id: item.id,
  title: item.title.trim(),
  slug: item.title.toLowerCase().replace(/\s+/g, '-'),
  date: new Date(item.created_at).toISOString(),
}));

// After: extracted transformer
function toArticle(item) {
  return {
    id: item.id,
    title: item.title.trim(),
    slug: slugify(item.title),
    date: formatDate(item.created_at),
  };
}
const articles = data.map(toArticle);
```

### Reduce Nesting with Object Lookups
```typescript
// Before: switch statement
switch (status) {
  case 'draft': return 'gray';
  case 'published': return 'green';
  case 'archived': return 'red';
  default: return 'gray';
}

// After: object lookup
const statusColors = { draft: 'gray', published: 'green', archived: 'red' };
return statusColors[status] ?? 'gray';
```

### Consolidate Conditionals
```typescript
// Before: repeated conditions
if (type === 'image') handleImage(file);
if (type === 'video') handleVideo(file);
if (type === 'document') handleDocument(file);

// After: handler map
const handlers = { image: handleImage, video: handleVideo, document: handleDocument };
handlers[type]?.(file);
```

## Project-Specific Patterns

For this Next.js/Cloudflare project:

- **API routes**: Use the auth middleware pattern consistently (`requireAdmin`, `requireEditor`, etc.)
- **Database queries**: Prefer parameterized queries, extract common query patterns
- **React components**: Keep components focused, extract hooks for shared logic
- **Error handling**: Use consistent error response format `{ success: false, error: string }`

## Output

After simplifying, provide:
1. Summary of changes made
2. Complexity reduction metrics (if measurable)
3. Any trade-offs or considerations
