---
name: frontend-flow
description: Ensures frontend code quality by enforcing Design System (9 ESLint rules), Storybook coverage, and 5-step verification pipeline. Use when creating/modifying React components in frontend/src/, especially shared/ where quality gates are mandatory. Triggers on "create component", "verify frontend", "storybook coverage", "перевір фронтенд", "frontend flow". Goal - all verification passes before task completion, knowledge captured in vault.
---

# Frontend Flow

Quality-first frontend development workflow for Pulse Radar.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│  QUALITY-FOCUSED FRONTEND WORKFLOW                          │
│                                                              │
│  1. SESSION    2. DISCOVERY   3. IMPLEMENT   4. STORYBOOK   │
│  ────────────  ────────────   ────────────   ────────────   │
│  Journal       Storybook MCP  Tokens         Stories        │
│  Beads         Vault Search   Patterns       Screenshots    │
│  Context       AGENTS.md      Design System  Interaction    │
│                                                              │
│  5. VERIFICATION (CRITICAL)   6. KNOWLEDGE                  │
│  ────────────────────────────  ────────────                 │
│  TypeScript → ESLint → Tests   Journal done                 │
│  Story check → Accessibility   Capture                      │
│  ALL MUST PASS                 Beads update                 │
└─────────────────────────────────────────────────────────────┘
```

**Principle:** Quality over speed. Verification must pass before task completion.

## Phase 1: Session & Context

**Trigger:** Starting frontend work

**Actions:**
1. Start journal session: `/obsidian:journal session "Task title"`
2. Get issue context: `bd show {issue}`
3. Read previous handoff if exists

**Goal:** Establish context and enable progress tracking.

## Phase 2: Discovery (CRITICAL!)

**Trigger:** BEFORE creating or modifying any component

**Required checks:**

```bash
# 1. Check existing components in Storybook
storybook_list_components

# 2. Get props API for similar components
storybook_get_component_props componentId="..."

# 3. Search knowledge vault
/obsidian:search "relevant pattern"

# 4. Read Design System rules
frontend/AGENTS.md
```

**Checkpoint:** "Existing component found? → USE IT instead of creating new!"

**Anti-pattern:** Creating new component without Storybook check = quality violation.

→ See @references/discovery.md for detailed checklist.

## Phase 3: Implementation (Design System)

**Trigger:** During code writing

**Required rules:**

| Rule | Use | Don't Use |
|------|-----|-----------|
| Colors | `@shared/tokens/*` | `bg-red-500`, `text-green-600` |
| Patterns | `@shared/patterns/*` | Manual composition |
| Icons | `lucide-react` | heroicons, Radix icons |
| Touch | `h-11 w-11` (44px) | `h-9 w-9` (36px) |
| Spacing | `gap-2`, `gap-4`, `p-4` | `gap-3`, `p-5` (off-grid) |
| Icon buttons | `aria-label="..."` | No label |
| Status | Icon + Text | Color only |

**Related skills:** `/frontend`, `/design-tokens`

## Phase 3.5: Component Portability (NEW!)

**Trigger:** When creating/modifying components in `shared/`

**Principle:** Components in shared/ must be PORTABLE — work without API, store, router.

```
┌─────────────────────────────────────────────────────────────┐
│  PORTABLE COMPONENT = Pure Function                         │
│                                                             │
│  Props → Component → UI                                     │
│                                                             │
│  ✅ No useQuery/useMutation inside                          │
│  ✅ No apiClient/fetch calls inside                         │
│  ✅ No useNavigate/useParams/useLocation                    │
│  ✅ No useStore (Zustand) directly                          │
│  ✅ All data via props                                      │
│  ✅ Works in Storybook WITHOUT providers                    │
└─────────────────────────────────────────────────────────────┘
```

**Anti-pattern (FORBIDDEN):**
```tsx
// ❌ NON-PORTABLE — violates CDD principles
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/lib/api'

export function ActivityHeatmap() {
  const { data } = useQuery({ queryFn: () => apiClient.get('/activity') })
  return <Heatmap data={data} />
}
```

**Correct pattern (Presenter + Hook):**
```tsx
// ✅ PORTABLE PRESENTER — shared/components/
interface ActivityHeatmapProps {
  data: ActivityDataPoint[]
  isLoading?: boolean
  className?: string
}

export function ActivityHeatmap({ data, isLoading, className }: ActivityHeatmapProps) {
  if (isLoading) return <ActivityHeatmapSkeleton />
  return <HeatmapRenderer data={data} className={className} />
}

// Data hook — features/activity/hooks/ or page level
export function useActivityData(timeRange: TimeRange) {
  return useQuery({
    queryKey: ['activity', timeRange],
    queryFn: () => activityService.getActivity(timeRange)
  })
}

// Page usage — composition
function DashboardPage() {
  const { data, isLoading } = useActivityData('week')
  return <ActivityHeatmap data={data ?? []} isLoading={isLoading} />
}
```

**Portability Checklist:**
- [ ] No useQuery/useMutation in shared/components
- [ ] No apiClient/fetch imports in shared/components
- [ ] No useNavigate/useParams in shared/components
- [ ] All data passed via typed props interface
- [ ] Optional className prop for customization
- [ ] Works in Storybook without QueryClient/Router mocks

**Verification command:**
```bash
# Should return 0 violations
grep -rE "useQuery|apiClient" src/shared/components --include="*.tsx" | grep -v test
```

## Phase 3.6: Component Integration Decision (NEW!)

**Trigger:** When needing a new UI element

**Decision Tree:**
```
NEED NEW UI ELEMENT?
         │
         ▼
┌─────────────────────────────┐
│ 1. Check shared/ui/         │ → EXISTS → USE IT
└─────────────────────────────┘
         │ NOT FOUND
         ▼
┌─────────────────────────────┐
│ 2. Check shared/components/ │ → EXISTS → USE IT
└─────────────────────────────┘
         │ NOT FOUND
         ▼
┌─────────────────────────────┐
│ 3. Check shared/patterns/   │ → EXISTS → USE IT
└─────────────────────────────┘
         │ NOT FOUND
         ▼
┌─────────────────────────────┐
│ 4. Check shadcn registry    │
│    ui.shadcn.com/docs       │
└─────────────────────────────┘
         │
    FOUND ┴ NOT FOUND
      │        │
      ▼        ▼
  EVALUATE   BUILD in shared/components
      │
 Fits 80%? ┬ YES → npx shadcn add → shared/ui
           │
           └ NO → WRAP in shared/components
```

**Where to put new component:**

| Type | Location | Example |
|------|----------|---------|
| shadcn primitive | `shared/ui/` | Button, Dialog, Select |
| shadcn + customize | `shared/ui/` (modify) | Badge with new variant |
| Composition | `shared/patterns/` | CardWithStatus, FormField |
| Business reusable | `shared/components/` | SearchBar, TopicSelector |
| Feature-specific | `features/X/components/` | AtomCard, ProviderList |
| Page-specific | `pages/X/components/` | DashboardStats |

**Adding shadcn component example:**
```bash
# 1. Check if exists
grep -r "DatePicker\|Calendar" src/shared/

# 2. Add from shadcn
npx shadcn@latest add calendar

# 3. Create composition wrapper if needed
# src/shared/components/DatePicker/index.tsx
```

**Checkpoint:** "Component location decided? Portability requirements clear?"

## Phase 4: Storybook (Component Library)

**Trigger:** After creating/modifying component

**Mandatory coverage:**

| Location | Story Required? | Min Stories |
|----------|-----------------|-------------|
| `shared/ui/` | Always | 4-6 |
| `shared/patterns/` | Always | 5-8 |
| `shared/components/` | Always | 4-6 |
| `features/*/` | If >50 LOC or reused | 2-4 |

**Actions:**
1. Create `.stories.tsx` with `tags: ['autodocs']`
2. Cover all variants, states, sizes
3. Add interaction tests for clickable elements
4. Capture screenshot: `storybook_capture_screenshot storyId="..."`

**Checkpoint:** "Story created with full coverage?"

**Related skill:** `/storybook`

## Phase 5: Verification Pipeline (MOST IMPORTANT!)

**Trigger:** After code written, BEFORE considering task complete

**Required pipeline (ALL steps!):**

```bash
cd frontend

# 1. TypeScript — type safety
npx tsc --noEmit

# 2. ESLint — Design System compliance (9 rules)
npm run lint

# 3. Unit tests — logic correctness
npm run test:run

# 4. Story coverage — documentation
npm run story:check

# 5. Accessibility (for shared/ components)
npm run test:a11y
```

**ESLint Design System Rules (all 9 — ERROR level):**

| # | Rule | Ensures |
|---|------|---------|
| 1 | `no-raw-tailwind-colors` | Semantic tokens only |
| 2 | `no-odd-spacing` | 4px grid system |
| 3 | `no-heroicons` | lucide-react only |
| 4 | `no-raw-zindex` | Named z-index tokens |
| 5 | `no-direct-fonts` | Font tokens only |
| 6 | `no-raw-page-wrapper` | PageWrapper required |
| 7 | `no-direct-api-imports` | Service classes |
| 8 | `no-hardcoded-api-paths` | API_ENDPOINTS config |
| 9 | `stories-require-autodocs` | Autodocs tag |

**If any step fails:** Fix → Re-run pipeline → Don't proceed until ALL pass.

→ See @references/verification.md for troubleshooting.

## Phase 6: Knowledge Capture

**Trigger:** After successful verification

**Actions:**
1. Close journal session: `/obsidian:journal done`
2. Add findings as wikilinks: `[[знання/паттерни/pattern-name]]`
3. Capture learnings: `/obsidian:capture auto`
4. Update Beads: `bd comments add {issue} "Progress: ..."`
5. Generate handoff for next session

**Learning categories:**
- `знання/паттерни/` — reusable approaches
- `знання/рішення/` — architectural decisions
- `знання/помилки/` — mistakes to avoid

→ See @references/documentation.md for templates.

## Quality Gates

| Gate | Criterion | Blocking? |
|------|-----------|-----------|
| Discovery | Storybook checked BEFORE coding | Yes |
| Design System | Tokens instead of raw colors | Yes (ESLint blocks) |
| Storybook | Story for shared/ components | Yes |
| TypeScript | `tsc --noEmit` passes | Yes |
| ESLint | 9 Design System rules pass | Yes |
| Tests | Unit tests pass | Yes |
| Story Coverage | `story:check` passes | Yes |
| Accessibility | `test:a11y` for shared/ | Recommended |
| Knowledge | Learnings captured in vault | Recommended |

**Principle:** If verification fails → task NOT complete.

## Quick Reference

**Commands:**

| Action | Command |
|--------|---------|
| Start Storybook | `just storybook` |
| TypeScript check | `npx tsc --noEmit` |
| ESLint | `npm run lint` |
| ESLint fix | `npm run lint:fix` |
| Unit tests | `npm run test:run` |
| Story coverage | `npm run story:check` |
| A11y tests | `npm run test:a11y` |

**Related skills:**

| Skill | When to use |
|-------|-------------|
| `/frontend` | Architecture, state management |
| `/storybook` | Story templates, interaction tests |
| `/design-tokens` | Token API reference |
| `/testing` | Vitest, Playwright patterns |

## Example

```
User: "Create TopicCard component"

Claude follows frontend-flow:

1. [Session] /obsidian:journal session "TopicCard component"

2. [Discovery] BEFORE coding!
   → storybook_list_components → check existing cards
   → Found CardWithStatus — base structure exists!
   → /obsidian:search "card pattern" → found prior decisions

3. [Implementation]
   → Using @shared/tokens for colors
   → Using @shared/patterns/CardWithStatus as base
   → All icon buttons with aria-label
   → 44px touch targets

4. [Storybook]
   → TopicCard.stories.tsx with tags: ['autodocs']
   → 5 stories: Default, Empty, Loading, Error, WithBadge
   → storybook_capture_screenshot

5. [Verification] ALL must pass!
   → npx tsc --noEmit ✅
   → npm run lint ✅ (9 ESLint rules pass)
   → npm run test:run ✅
   → npm run story:check ✅
   → npm run test:a11y ✅

6. [Knowledge]
   → /obsidian:journal done
   → Findings: [[знання/паттерни/topic-card-composition]]
   → /obsidian:capture auto
```

**Key:** Verification runs COMPLETELY before task is considered done.
