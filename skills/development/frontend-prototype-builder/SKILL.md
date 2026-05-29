---
name: frontend-prototype-builder
description: |
  Build deployable frontend prototypes from Figma designs and test cases.
  Complete workflow: ensure services → validate data → generate pages → test with browser.

  Use when:
  (1) "构建前端原型" or "build frontend prototype"
  (2) "从 Figma 生成页面" or "generate pages from Figma"
  (3) "修复前端 404 问题" or "debug frontend 404"
  (4) "端到端测试前端" or "E2E test frontend"
  (5) Need to create testable UI for PM/designers

  Inputs: specs/design/pages.yaml, specs/design/figma/, specs/testcases/*.md
  Outputs: Working frontend pages in frontend/app/ and frontend/components/pages/
---

# Frontend Prototype Builder SOP

Build 70-80% deployable prototypes from Figma designs + test cases that PMs and designers can test with real data.

## Prerequisites

Before starting, ensure:
- [ ] `specs/design/pages.yaml` exists (run `ux-spec-generator` if missing)
- [ ] `specs/design/figma/` has design docs (run `figma-resource-extractor` if missing)
- [ ] `.synnovator/generated/openapi.yaml` exists (run `schema-to-openapi` if missing)
- [ ] `frontend/lib/api-client.ts` exists (run `openapi-to-components` if missing)

## Workflow Overview

```
Phase 0: Health Check
    ↓
Phase 1: Start Services
    ↓
Phase 2: Validate Database
    ↓
Phase 3: Generate/Update Pages
    ↓
Phase 4: Visual Validation (screenshots)
    ↓
Phase 5: E2E Browser Testing
    ↓
Phase 6: Fix Issues & Iterate
```

---

## Phase 0: Health Check

### 0.1 Check Required Files

```bash
# Check if critical files exist
ls -la specs/design/pages.yaml
ls -la .synnovator/generated/openapi.yaml
ls -la frontend/lib/api-client.ts
ls -la frontend/lib/types.ts
```

If any missing, run the corresponding skill:
- Missing `pages.yaml` → `/ui-spec-generator`
- Missing `openapi.yaml` → `/schema-to-openapi`
- Missing `api-client.ts` or `types.ts` → `/openapi-to-components`

### 0.2 Check Service Status

```bash
# Check if ports are in use
lsof -i :8000  # Backend (FastAPI)
lsof -i :3000  # Frontend (Next.js)
```

---

## Phase 1: Start Services

### 1.1 Start Backend (if not running)

```bash
# Terminal 1: Start backend
make backend
# Or manually:
# cd /path/to/project && uv run uvicorn app.main:app --reload --port 8000
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### 1.2 Verify Backend Health

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### 1.3 Start Frontend (if not running)

```bash
# Terminal 2: Start frontend
make frontend
# Or manually:
# cd frontend && npm run dev
```

Wait for: `Ready in X.Xs`

### 1.4 Verify Frontend Access

```bash
curl -I http://localhost:3000
# Expected: HTTP/1.1 200 OK
```

---

## Phase 2: Validate Database

### 2.1 Check Database Has Data

```bash
# Quick check via API
curl http://localhost:8000/api/users | jq '.total'
curl http://localhost:8000/api/posts | jq '.total'
curl http://localhost:8000/api/categories | jq '.total'
```

If totals are 0, import test data:

### 2.2 Import Test Data (if needed)

Use the `data-importer` skill:
```
/data-importer
```

Or manually:
```bash
uv run python -m scripts.import_data
```

### 2.3 Verify Data Import

```bash
# Verify specific entities exist
curl http://localhost:8000/api/posts | jq '.items[0]'
curl http://localhost:8000/api/users | jq '.items[0]'
```

---

## Phase 3: Generate/Update Pages

### 3.1 Identify Pages to Generate

Read `specs/design/pages.yaml` and check which pages exist:

```yaml
# pages.yaml structure
pages:
  - id: home
    route: /
    pen_file: components/home.pen
    ...
```

### 3.2 Page Generation Checklist

For each page in `pages.yaml`:

| Step | Check | Action if Missing |
|------|-------|-------------------|
| 1 | `frontend/app/{route}/page.tsx` exists | Create route file |
| 2 | `frontend/components/pages/{id}.tsx` exists | Create component |
| 3 | Component imports from `@/lib/api-client` | Add API imports |
| 4 | Component uses correct data fetching | Add useEffect/Server Component |
| 5 | Navigation uses `router.push()` or `<Link>` | Add navigation |
| 6 | Actions call API functions | Wire up handlers |

### 3.3 Page Component Template

```tsx
// frontend/app/{route}/page.tsx
import { PageComponent } from "@/components/pages/{page-id}"

export default function Page({ params }: { params: { id?: string } }) {
  return <PageComponent {...(params.id ? { id: Number(params.id) } : {})} />
}
```

```tsx
// frontend/components/pages/{page-id}.tsx
"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { listPosts, getPost, likePost } from "@/lib/api-client"
import type { Post } from "@/lib/types"

export function PageComponent({ id }: { id?: number }) {
  const router = useRouter()
  const [data, setData] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await listPosts()
        setData(result.items)
      } catch (err) {
        console.error("Failed to fetch:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  // Handler example
  async function handleLike(postId: number) {
    try {
      await likePost(postId, 1) // userId=1 for prototype
      // Refetch or optimistic update
    } catch (err) {
      console.error("Like failed:", err)
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div>
      {data.map(item => (
        <div
          key={item.id}
          onClick={() => router.push(`/posts/${item.id}`)}
          className="cursor-pointer"
        >
          {item.title}
          <button onClick={(e) => { e.stopPropagation(); handleLike(item.id) }}>
            Like
          </button>
        </div>
      ))}
    </div>
  )
}
```

### 3.4 Implement UX Interaction Specs (CRITICAL)

> **This step is mandatory.** Skipping it produces visual-only prototypes with no interactivity.

For each page, read the corresponding `specs/ux/pages/{page-id}.yaml` and implement all defined interactions.

**Interaction Translation Table:**

| UX Spec Definition | React Implementation |
|-------------------|----------------------|
| `trigger: click, action: navigate, target: "/path"` | `onClick={() => router.push("/path")}` |
| `trigger: tab_change` with `filter` | `onClick={() => updateSearchParams(key, value)}` or `router.push(newUrl)` |
| `trigger: select, action: update_url_param` | `onChange` handler + `useSearchParams` + `router.push` |
| `trigger: click, action: toggle_like` | `onClick={handleLike}` with API call |
| `trigger: submit` | `onSubmit` or `onClick={handleSubmit}` with API call |
| `trigger: click, action: open_modal` | `onClick={() => setModalOpen(true)}` |
| `trigger: click, action: show_dropdown` | Use shadcn `DropdownMenu` component |

**Implementation Pattern for Tabs with URL Filtering:**

```tsx
// 1. Define route mapping
const tabRoutes: Record<string, string> = {
  "热门": "/",
  "提案广场": "/proposals",
  "找队友": "/posts?tag=find-teammate",
  "找点子": "/posts?tag=find-idea",
}

// 2. Add onClick to each tab
<Badge onClick={() => router.push(tabRoutes[tab] ?? "/")}>
  {tab}
</Badge>
```

**Implementation Pattern for Filter Dropdowns:**

```tsx
// 1. Use useSearchParams
const searchParams = useSearchParams()

// 2. Create update helper
function updateSearchParam(key: string, value: string | null) {
  const next = new URLSearchParams(searchParams.toString())
  if (value === null) next.delete(key)
  else next.set(key, value)
  router.push(`${pathname}?${next.toString()}`)
}

// 3. Wire to component
<DropdownMenuItem onClick={() => updateSearchParam("status", "published")}>
  已发布
</DropdownMenuItem>
```

**Checklist for Each Page:**

| Step | Check | Source |
|------|-------|--------|
| 1 | List all `interactions` from `specs/ux/pages/{page}.yaml` | UX spec |
| 2 | For each `trigger: click` → verify `onClick` exists | Code audit |
| 3 | For each `trigger: tab_change` → verify URL update logic | Code audit |
| 4 | For each `trigger: submit` → verify API call wired | Code audit |
| 5 | Shared components from `uses_shared` have interactions | `specs/ux/global/shared-components.yaml` |

### 3.5 Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| 404 on API | Console: "API 404" | Check backend running, route prefix is `/api` |
| Buttons don't work | No response | Add onClick handlers, check console for errors |
| Navigation fails | Page not found | Check dynamic route `[id]` folder exists |
| Data not loading | Empty page | Check useEffect runs, API returns data |
| CORS error | Console: blocked | Backend CORS includes localhost:3000 |
| **Tabs don't filter** | Click has no effect | Missing `onClick` → add `router.push(tabRoutes[tab])` |
| **Dropdowns don't filter** | Selection ignored | Missing `onChange` → use `updateSearchParam()` helper |
| **Like button static** | No count update | Missing API call → implement `handleLike()` with `likePost()` |

---

## Phase 4: Visual Validation

### 4.1 Take Screenshots

Use agent-browser to capture current state:

```
/agent-browser screenshot http://localhost:3000 --output screenshots/home.png
/agent-browser screenshot http://localhost:3000/posts/1 --output screenshots/post-detail.png
```

### 4.2 Compare with Figma

Check screenshots against:
- `specs/design/figma/pages/*.md` for expected layout
- `specs/design/pages.yaml` for component structure

---

## Phase 5: E2E Browser Testing

### 5.1 Run Test Cases

Use agent-browser to execute test scenarios from `specs/testcases/`:

```
/agent-browser test http://localhost:3000 --scenario "Navigate to post detail"
```

Test checklist:
- [ ] Home page loads with data
- [ ] Can click on post card → navigates to detail
- [ ] Can click like button → count updates
- [ ] Can submit comment → appears in list
- [ ] Navigation links work

### 5.2 Automated E2E Script

```typescript
// tests/e2e/prototype.spec.ts
import { test, expect } from '@playwright/test'

test('home page loads posts', async ({ page }) => {
  await page.goto('http://localhost:3000')
  await expect(page.locator('[data-testid="post-card"]')).toHaveCount(3)
})

test('navigate to post detail', async ({ page }) => {
  await page.goto('http://localhost:3000')
  await page.click('[data-testid="post-card"]:first-child')
  await expect(page).toHaveURL(/\/posts\/\d+/)
  await expect(page.locator('h1')).toBeVisible()
})

test('like button works', async ({ page }) => {
  await page.goto('http://localhost:3000/posts/1')
  const likeBtn = page.locator('[data-testid="like-btn"]')
  const countBefore = await likeBtn.textContent()
  await likeBtn.click()
  await expect(likeBtn).not.toHaveText(countBefore!)
})
```

---

## Phase 6: Fix Issues & Iterate

### 6.1 Common Fix Patterns

**Issue: "API 404: Post not found"**
```typescript
// Check: Is the post ID valid?
// Fix: Ensure database has data with that ID
curl http://localhost:8000/api/posts
```

**Issue: "TypeError: Cannot read property 'items' of undefined"**
```typescript
// Check: API response structure
// Fix: Add null checks
const result = await listPosts()
setData(result?.items ?? [])
```

**Issue: "Click does nothing"**
```tsx
// Check: Event handler attached?
// Fix: Add onClick and verify function exists
<Button onClick={() => console.log('clicked')}>Test</Button>
```

**Issue: "Hydration mismatch"**
```tsx
// Check: Server/client rendering difference
// Fix: Use "use client" directive, or dynamic import
"use client"  // Add at top of file
```

### 6.2 Iteration Cycle

```
1. Run E2E tests
    ↓
2. Identify failures
    ↓
3. Check console/network for errors
    ↓
4. Apply fix from patterns above
    ↓
5. Re-run tests
    ↓
6. Repeat until all tests pass
```

---

## Quick Reference: Skill Chain

| Phase | Skill to Use | Purpose |
|-------|--------------|---------|
| Pre-0 | `figma-resource-extractor` | Extract Figma designs |
| Pre-0 | `schema-to-openapi` | Generate OpenAPI spec |
| Pre-0 | `openapi-to-components` | Generate API client + types |
| Pre-0 | `ux-spec-generator` | Generate pages.yaml |
| 2 | `data-importer` | Import test data |
| 3 | (this skill) | Generate page components |
| 4-5 | `agent-browser` | E2E testing |

---

## Troubleshooting Checklist

Before reporting "it doesn't work", verify:

- [ ] Backend server running on :8000 (`curl localhost:8000/health`)
- [ ] Frontend server running on :3000 (`curl -I localhost:3000`)
- [ ] Database has test data (`curl localhost:8000/api/posts | jq .total`)
- [ ] No console errors in browser DevTools
- [ ] Network tab shows successful API responses
- [ ] Dynamic route folders exist (`app/posts/[id]/page.tsx`)
- [ ] Components import from `@/lib/api-client`
- [ ] Event handlers are wired (check onClick props)

---

## Output Checklist

A successful prototype build produces:

- [ ] All pages from `pages.yaml` have route files
- [ ] All pages fetch and display real data
- [ ] Navigation between pages works
- [ ] Interactive elements (like, comment, follow) call APIs
- [ ] **All interactions from `specs/ux/pages/*.yaml` are implemented** (tabs, filters, buttons)
- [ ] **Tabs/filters update URL params and trigger data refetch**
- [ ] E2E tests pass for core user journeys
- [ ] PM/designer can click through the prototype

## Interaction Verification Checklist

Before marking a page complete, verify these interactions work:

### Global (all pages)
- [ ] Logo click → navigates to `/`
- [ ] Search bar → expands on focus (or navigates on submit)
- [ ] "发布新内容" button → opens publish menu or navigates
- [ ] Sidebar nav items → navigate to correct routes
- [ ] User avatar dropdown → shows menu options

### Tabs & Filters
- [ ] Each tab click → updates URL or navigates
- [ ] Filter dropdowns → update URL params
- [ ] Active state → visually indicates current selection

### Content Cards
- [ ] Card click → navigates to detail page
- [ ] Like button → calls API, updates count
- [ ] Share button → opens share modal or copies link

### Forms
- [ ] Submit button → calls API
- [ ] Input validation → shows errors
- [ ] Success → shows toast or redirects
