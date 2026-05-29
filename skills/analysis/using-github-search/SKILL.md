---
name: using-github-search
description: Use when researching GitHub issues, PRs, and discussions for community solutions and known gotchas - searches via WebSearch with site filters and extracts problem-solution patterns
---

# Using GitHub Search

Use this skill when researching GitHub issues, PRs, discussions for community solutions and known gotchas.

## Core Principles

- Search GitHub via WebSearch with site: filter
- Focus on closed issues (solved problems)
- Fetch promising threads for detailed analysis
- Extract problem-solution patterns

## Workflow

### 1. Issue Search

**Use WebSearch with site:github.com:**

```python
# Find closed issues with solutions
WebSearch(
    query="site:github.com React useEffect memory leak closed"
)
```

**Search patterns:**

**Closed issues (solved problems):**
```python
query="site:github.com [repo-name] [problem] closed is:issue"
```

**Pull requests (implementation examples):**
```python
query="site:github.com [repo-name] [feature] is:pr merged"
```

**Discussions (community advice):**
```python
query="site:github.com [repo-name] [topic] is:discussion"
```

**Labels for filtering:**
```python
query="site:github.com react label:bug label:performance closed"
```

### 2. Repository-Specific Search

**Known repositories:**

```python
# React issues
WebSearch(query="site:github.com/facebook/react useEffect cleanup closed")

# Next.js issues
WebSearch(query="site:github.com/vercel/next.js SSR hydration closed")

# TypeScript issues
WebSearch(query="site:github.com/microsoft/typescript type inference closed")
```

**Community repositories:**

```python
# Awesome lists
WebSearch(query="site:github.com awesome-react authentication")

# Best practice repos
WebSearch(query="site:github.com typescript best practices")
```

### 3. Fetch Issue Details

**Use WebFetch** to analyze threads:

```python
# Fetch specific issue
thread = WebFetch(
    url="https://github.com/facebook/react/issues/14326",
    prompt="Extract the problem description, root cause, and accepted solution. Include any workarounds or caveats mentioned."
)
```

**Fetch prompt patterns:**
- "Summarize the problem and official solution"
- "Extract workarounds and their trade-offs"
- "List breaking changes and migration steps"
- "Identify root cause and fix explanation"

### 4. Pattern Recognition

Look for **common patterns:**

**Problem-Solution:**
```markdown
Problem: Memory leak with event listeners in useEffect
Solution: Return cleanup function
Frequency: 50+ issues
Pattern: Missing return in useEffect
```

**Gotchas:**
```markdown
Gotcha: Array.sort() mutates in place
Impact: React state updates fail silently
Workaround: [...arr].sort()
Source: 20+ issues across projects
```

## Reporting Format

Structure findings as:

```markdown
## GitHub Research Findings

### 1. React useEffect Memory Leaks

**Source:** facebook/react#14326 (Closed, 150+ comments)
**Status:** Resolved in React 18
**URL:** https://github.com/facebook/react/issues/14326

**Problem:**
Event listeners added in useEffect not cleaned up, causing memory leaks on component unmount.

**Root Cause:**
Missing cleanup function in useEffect hook.

**Solution:**
```javascript
useEffect(() => {
  const handler = () => console.log('event')
  window.addEventListener('resize', handler)

  // Cleanup function
  return () => window.removeEventListener('resize', handler)
}, [])
```

**Caveats:**
- Cleanup runs before next effect AND on unmount
- Don't cleanup external state (e.g., API calls may complete after unmount)
- Use AbortController for fetch requests

**Community Consensus:**
- 95% of comments recommend cleanup pattern
- Official docs updated to emphasize this
- ESLint rule available: `exhaustive-deps`

---

### 2. Next.js Hydration Mismatch

**Source:** vercel/next.js#7417 (Closed, 80+ comments)
**Status:** Workarounds available, improved errors in Next 13+
**URL:** https://github.com/vercel/next.js/issues/7417

**Problem:**
Server-rendered HTML differs from client, causing hydration errors.

**Common Causes:**
1. Date.now() or random values in render
2. window object access during SSR
3. Third-party scripts modifying DOM

**Solutions:**

**Approach 1: Suppress hydration warning (temporary)**
```jsx
<div suppressHydrationWarning>{Date.now()}</div>
```

**Approach 2: Client-only rendering**
```jsx
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return null
return <div>{Date.now()}</div>
```

**Approach 3: Use next/dynamic**
```jsx
const ClientOnly = dynamic(() => import('./ClientOnly'), { ssr: false })
```

**Trade-offs:**
- Suppress: Quick but masks real issues
- Client-only: Flash of missing content
- Dynamic: Extra bundle split, best for isolated components

**Community Recommendation:**
Use dynamic imports for truly client-only components. Fix server/client differences when possible.

---

### 3. TypeScript Type Inference Limitations

**Source:** microsoft/typescript#10571 (Open, discussion ongoing)
**Status:** Design limitation, workarounds exist
**URL:** https://github.com/microsoft/typescript/issues/10571

**Problem:**
Generic type inference fails with complex nested structures.

**Workarounds:**

**Explicit type parameters:**
```typescript
// Instead of inference
const result = complexFunction<User, string>(data)
```

**Type assertions:**
```typescript
const result = complexFunction(data) as Result<User>
```

**Community Patterns:**
- 40% use explicit type parameters
- 30% restructure code to simplify inference
- 30% use type assertions with validation

**Gotcha:**
Type assertions bypass type checking. Validate at runtime or use type guards.
```

## Search Strategies

### Find Solved Problems
```python
WebSearch(query="site:github.com react hooks stale closure closed is:issue")
```

### Implementation Examples
```python
WebSearch(query="site:github.com authentication JWT refresh is:pr merged")
```

### Breaking Changes
```python
WebSearch(query="site:github.com next.js migration breaking changes v14")
```

### Community Discussions
```python
WebSearch(query="site:github.com typescript best practices is:discussion")
```

### Security Issues
```python
WebSearch(query="site:github.com express security vulnerability closed CVE")
```

## Anti-Patterns

❌ **Don't:** Only search open issues (may not have solutions)
✅ **Do:** Focus on closed issues with accepted solutions

❌ **Don't:** Trust first comment without reading thread
✅ **Do:** Read accepted solution and top comments

❌ **Don't:** Apply workarounds without understanding trade-offs
✅ **Do:** Document caveats and alternatives

❌ **Don't:** Assume issue applies to current version
✅ **Do:** Check version context and current status

## Quality Indicators

**High-value issues have:**
- ✅ Closed with accepted solution
- ✅ 20+ comments (community vetted)
- ✅ Official maintainer response
- ✅ Code examples in solution
- ✅ Referenced in docs or other issues

**Skip if:**
- ❌ Open with no recent activity
- ❌ No clear solution or consensus
- ❌ Very old (>2 years) without recent confirmation
- ❌ Off-topic discussion
- ❌ No code examples

## Example Session

```python
# 1. Search for known React issues
results = WebSearch(
    query="site:github.com/facebook/react useEffect infinite loop closed"
)
# → Found 10 closed issues

# 2. Fetch most relevant
issue1 = WebFetch(
    url="https://github.com/facebook/react/issues/12345",
    prompt="Extract the root cause of infinite loops in useEffect and the recommended solution"
)
# → Got dependency array explanation and fix

# 3. Search for migration issues
migration = WebSearch(
    query="site:github.com/vercel/next.js migrate v13 to v14 breaking changes"
)
# → Found migration guide and common issues

# 4. Fetch migration PR
pr = WebFetch(
    url="https://github.com/vercel/next.js/pull/56789",
    prompt="List all breaking changes and required code updates"
)
# → Got comprehensive migration checklist

# 5. Search for community patterns
patterns = WebSearch(
    query="site:github.com awesome-typescript patterns is:repo"
)
# → Found curated best practices repo

# 6. Synthesize findings
# Combine issue solutions, migration steps, community patterns
# Note frequency of issues, consensus solutions
```

## Citation Format

```markdown
**Issue:** Memory leak in React hooks
**Source:** facebook/react#14326 (Closed)
**URL:** https://github.com/facebook/react/issues/14326
**Status:** Resolved in React 18
**Comments:** 150+ (High community engagement)

**Official Response:**
> "The cleanup function must be returned from useEffect. This is critical for preventing memory leaks." - Dan Abramov (React team)

**Community Consensus:**
95% of solutions recommend cleanup pattern. ESLint rule added to enforce.
```

## Useful Repositories

**Best Practices:**
- awesome-[tech] lists (curated resources)
- [framework]-best-practices repos
- [company]-engineering-blogs

**Security:**
- OWASP repos for security patterns
- CVE databases for vulnerabilities
- Security advisories in popular frameworks

**Migration Guides:**
- Official framework upgrade guides
- Community migration experience issues
- Breaking change tracking issues
