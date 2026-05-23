---
name: performance-security
description: Performance optimization, accessibility, and security best practices for React apps. Covers code-splitting, React Compiler patterns, asset optimization, a11y testing, and security hardening. Use when optimizing performance or reviewing security.
---

# Performance, Accessibility & Security

Production-ready patterns for building fast, accessible, and secure React applications.

## Performance Optimization

### Code-Splitting

**Automatic with TanStack Router:**
- File-based routing automatically code-splits by route
- Each route is its own chunk
- Vite handles dynamic imports efficiently

**Manual code-splitting:**
```typescript
import { lazy, Suspense } from 'react'

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'))

function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart data={data} />
    </Suspense>
  )
}
```

**Route-level lazy loading:**
```typescript
// src/routes/dashboard.lazy.tsx
export const Route = createLazyFileRoute('/dashboard')({
  component: DashboardComponent,
})
```

### React Compiler First

The React Compiler automatically optimizes performance when you write compiler-friendly code:

**✅ Do:**
- Keep components pure (no side effects in render)
- Derive values during render (don't stash in refs)
- Keep props serializable
- Inline event handlers (unless they close over large objects)

**❌ Avoid:**
- Mutating props or state
- Side effects in render phase
- Over-using useCallback/useMemo (compiler handles this)
- Non-serializable props (functions, symbols)

**Verify optimization:**
- Check React DevTools for "Memo ✨" badge
- Components without badge weren't optimized (check for violations)

### Images & Assets

**Use Vite asset pipeline:**
```typescript
// Imports are optimized and hashed
import logo from './logo.png'

<img src={logo} alt="Logo" />
```

**Prefer modern formats:**
```typescript
// WebP for photos
<img src="/hero.webp" alt="Hero" />

// SVG for icons
import { ReactComponent as Icon } from './icon.svg'
<Icon />
```

**Lazy load images:**
```typescript
<img src={imageSrc} loading="lazy" alt="Description" />
```

**Responsive images:**
```typescript
<img
  srcSet="
    /image-320w.webp 320w,
    /image-640w.webp 640w,
    /image-1280w.webp 1280w
  "
  sizes="(max-width: 640px) 100vw, 640px"
  src="/image-640w.webp"
  alt="Description"
/>
```

### Bundle Analysis

```bash
# Build with analysis
npx vite build --mode production

# Visualize bundle
pnpm add -D rollup-plugin-visualizer
```

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true }),
  ],
})
```

### Performance Checklist

- [ ] Code-split routes and heavy components
- [ ] Verify React Compiler optimizations (✨ badges)
- [ ] Optimize images (WebP, lazy loading, responsive)
- [ ] Prefetch critical data in route loaders
- [ ] Use TanStack Query for automatic deduplication
- [ ] Set appropriate `staleTime` per query
- [ ] Minimize bundle size (check with visualizer)
- [ ] Enable compression (gzip/brotli on server)

## Accessibility (a11y)

### Semantic HTML

**✅ Use semantic elements:**
```typescript
// Good
<nav><a href="/about">About</a></nav>
<button onClick={handleClick}>Submit</button>
<main><article>Content</article></main>

// Bad
<div onClick={handleNav}>About</div>
<div onClick={handleClick}>Submit</div>
<div><div>Content</div></div>
```

### ARIA When Needed

**Only add ARIA when semantic HTML isn't enough:**
```typescript
// Custom select component
<div
  role="listbox"
  aria-label="Select country"
  aria-activedescendant={activeId}
>
  <div role="option" id="us">United States</div>
  <div role="option" id="uk">United Kingdom</div>
</div>

// Loading state
<button aria-busy={isLoading} disabled={isLoading}>
  {isLoading ? 'Loading...' : 'Submit'}
</button>
```

### Keyboard Navigation

**Ensure all interactive elements are keyboard accessible:**
```typescript
function Dialog({ isOpen, onClose }: DialogProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      return () => document.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen, onClose])

  return isOpen ? (
    <div role="dialog" aria-modal="true">
      {/* Focus trap implementation */}
      <button onClick={onClose} aria-label="Close dialog">×</button>
      {/* Dialog content */}
    </div>
  ) : null
}
```

### Testing with React Testing Library

**Use accessible queries (by role/label):**
```typescript
import { render, screen } from '@testing-library/react'

test('button is accessible', () => {
  render(<button>Submit</button>)

  // ✅ Good - query by role
  const button = screen.getByRole('button', { name: /submit/i })
  expect(button).toBeInTheDocument()

  // ❌ Avoid - query by test ID
  const button = screen.getByTestId('submit-button')
})
```

**Common accessible queries:**
```typescript
// By role (preferred)
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { level: 1 })

// By label
screen.getByLabelText(/email address/i)

// By text
screen.getByText(/welcome/i)
```

### Color Contrast

- Ensure 4.5:1 contrast ratio for normal text
- Ensure 3:1 contrast ratio for large text (18pt+)
- Don't rely on color alone for meaning
- Test with browser DevTools accessibility panel

### Accessibility Checklist

- [ ] Use semantic HTML elements
- [ ] Add alt text to all images
- [ ] Ensure keyboard navigation works
- [ ] Provide focus indicators
- [ ] Test with screen reader (NVDA/JAWS/VoiceOver)
- [ ] Verify color contrast meets WCAG AA
- [ ] Use React Testing Library accessible queries
- [ ] Add skip links for main content
- [ ] Ensure form inputs have labels

## Security

### Never Ship Secrets

**❌ Wrong - secrets in code:**
```typescript
const API_KEY = 'sk_live_abc123' // Exposed in bundle!
```

**✅ Correct - environment variables:**
```typescript
// Only VITE_* variables are exposed to client
const API_KEY = import.meta.env.VITE_PUBLIC_KEY
```

**In `.env.local` (not committed):**
```bash
VITE_PUBLIC_KEY=pk_live_abc123  # Public key only!
```

**Backend handles secrets:**
```typescript
// Frontend calls backend, backend uses secret API key
await apiClient.post('/process-payment', { amount, token })
// Backend has access to SECRET_KEY via server env
```

### Validate All Untrusted Data

**At boundaries (API responses):**
```typescript
import { z } from 'zod'

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
})

async function fetchUser(id: string) {
  const response = await apiClient.get(`/users/${id}`)

  // Validate response
  return UserSchema.parse(response.data)
}
```

**User input:**
```typescript
const formSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be 8+ characters'),
})

type FormData = z.infer<typeof formSchema>

function LoginForm() {
  const handleSubmit = (data: unknown) => {
    const result = formSchema.safeParse(data)

    if (!result.success) {
      setErrors(result.error.errors)
      return
    }

    // result.data is typed and validated
    login(result.data)
  }
}
```

### XSS Prevention

React automatically escapes content in JSX:
```typescript
// ✅ Safe - React escapes
<div>{userInput}</div>

// ❌ Dangerous - bypasses escaping
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

**If you must use HTML:**
```typescript
import DOMPurify from 'dompurify'

<div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(trustedHTML)
}} />
```

### Content Security Policy

Add CSP headers on server:
```nginx
# nginx example
add_header Content-Security-Policy "
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self' data:;
  connect-src 'self' https://api.example.com;
";
```

### Dependency Security

**Pin versions in package.json:**
```json
{
  "dependencies": {
    "react": "19.0.0",  // Exact version
    "@tanstack/react-query": "^5.59.0"  // Allow patches
  }
}
```

**Audit regularly:**
```bash
pnpm audit
pnpm audit --fix
```

**Use Renovate or Dependabot:**
```json
// .github/renovate.json
{
  "extends": ["config:base"],
  "automerge": true,
  "major": { "automerge": false }
}
```

### CI Security

**Run with `--ignore-scripts`:**
```bash
# Prevents malicious post-install scripts
pnpm install --ignore-scripts
```

**Scan for secrets:**
```bash
# Add to CI
git-secrets --scan
```

### Security Checklist

- [ ] Never commit secrets or API keys
- [ ] Only expose `VITE_*` env vars to client
- [ ] Validate all API responses with Zod
- [ ] Sanitize user-generated HTML (if needed)
- [ ] Set Content Security Policy headers
- [ ] Pin dependency versions
- [ ] Run `pnpm audit` regularly
- [ ] Enable Renovate/Dependabot
- [ ] Use `--ignore-scripts` in CI
- [ ] Implement proper authentication flow

## Related Skills

- **core-principles** - Project structure and standards
- **react-patterns** - Compiler-friendly code
- **tanstack-query** - Performance via caching and deduplication
- **tooling-setup** - TypeScript strict mode for type safety
