# TanStack Router - Common Errors & Solutions

## Error 1: Devtools Dependency Not Found

**Symptom:** Build error: Cannot find module '@tanstack/router-devtools-core'

**Solution:**
```bash
npm install @tanstack/router-devtools
```

## Error 2: Routes Not Auto-Generated

**Symptom:** `routeTree.gen.ts` not created, type errors

**Solution:** Vite plugin MUST come before react():
```typescript
// vite.config.ts
plugins: [
  TanStackRouterVite(), // First!
  react(),
]
```

## Error 3: Link `to` Not Typed

**Symptom:** No autocomplete for routes

**Solution:** Import and use the generated routeTree:
```typescript
import { routeTree } from './routeTree.gen'
const router = createRouter({ routeTree })
```

## Error 4: Loader Not Running

**Symptom:** Data not loaded on navigation

**Solution:** Ensure route exports `Route`:
```typescript
export const Route = createFileRoute('/path')({
  loader: async () => { /* ... */ }
})
```

## Error 5: Memory Leak with TanStack Form

**Symptom:** Production crashes every 30min when using forms

**Issue:** GitHub #5734 (open)

**Workaround:** Use React Hook Form instead, or avoid TanStack Form until fixed

## Error 6: Middleware Undefined in Vite Build

**Symptom:** Build works in dev, fails in production

**Solution:** Check Vite plugin configuration and bundling settings

## Error 7: API Route Loaders Fail After Restart

**Symptom:** Loaders return stale data or error after dev server restart

**Solution:** Clear browser cache, or add cache-busting to loader queries

## Prevention Tips

1. Always use TanStackRouterVite plugin
2. Keep devtools as dev dependency
3. Include all route state in query keys
4. Test production builds locally
5. Use TypeScript strict mode

## Further Reading

- [TanStack Router Docs](https://tanstack.com/router/latest)
- [GitHub Issues](https://github.com/TanStack/router/issues)
