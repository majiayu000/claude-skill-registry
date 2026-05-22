---
name: ui-ux-expert-skill
description: Technical workflow for implementing accessible React user interfaces with shadcn/ui, Tailwind CSS, and TanStack Query. Includes 6-phase process with mandatory Style Guide compliance, Context7 best practices consultation, Chrome DevTools validation, and WCAG 2.1 AA accessibility standards. Use after Test Agent, Implementer, and Supabase agents complete their work.
---

# UI/UX Expert Technical Skill

**Version**: 1.0.0
**Agent**: ui-ux-expert
**Last Updated**: 2025-01-26

---

## Purpose

This skill provides the complete technical workflow for implementing accessible, performant React user interfaces that:
- Pass 100% of E2E tests without modification
- Comply with WCAG 2.1 AA accessibility standards
- Follow the project's Style Guide exactly
- Achieve Core Web Vitals green metrics
- Integrate with implemented use cases (not data services directly)

---

## 6-PHASE WORKFLOW (MANDATORY)

### PHASE 0: Style Guide Study (MANDATORY FIRST STEP)

**Objective**: Internalize the project's visual design system before ANY implementation.

**⚠️ CRITICAL**: This is the FIRST step. All implementations must reference the Style Guide.

**Steps**:

1. **Read Style Guide completely**:
   ```
   Read('.claude/STYLE_GUIDE.md')
   ```

2. **Memorize key constraints**:
   - **Color Palette**: 5 brand colors (Brand-1 through Brand-5) + semantic tokens
     - NO arbitrary hex values (e.g., `bg-[#4A5FFF]` is PROHIBITED)
     - ONLY use semantic tokens: `bg-primary`, `text-foreground`, `border`, etc.
   - **Typography Scale**: `text-xs` through `text-4xl` ONLY
     - NO arbitrary font sizes (e.g., `text-[32px]` is PROHIBITED)
   - **Spacing Scale**: `spacing-1` (4px) through `spacing-24` (96px) ONLY
     - NO arbitrary values (e.g., `p-[17px]` is PROHIBITED)
   - **Animation Durations**: 200ms, 300ms, or 500ms ONLY
     - NO other durations
   - **Border Radius**: `--radius` variable (default 0.5rem)

3. **Note component conventions**:
   - Hover states: `hover:bg-accent`, `hover:shadow-lg`
   - Focus states: `focus:ring-2 focus:ring-ring`
   - Disabled states: `disabled:opacity-50 disabled:cursor-not-allowed`
   - Dark mode: automatic via `.dark` class

**Deliverable**: Mental model of Style Guide constraints to apply during implementation.

---

### PHASE 1: Component Research (BEFORE Design)

**Objective**: Consult Context7 and shadcn MCP for latest best practices BEFORE designing components.

**⚠️ CRITICAL**: Research first, design second. Avoid implementing outdated patterns.

**Steps**:

1. **Context7: React patterns** (MANDATORY)
   ```typescript
   mcp__context7__get_library_docs({
     context7CompatibleLibraryID: "/reactjs/react.dev",
     topic: "hooks useEffect useState useMemo useCallback custom hooks best practices",
     tokens: 2500
   })
   ```
   **Extract**: Latest Hook patterns, composition strategies, performance tips

2. **Context7: Next.js App Router** (MANDATORY)
   ```typescript
   mcp__context7__get_library_docs({
     context7CompatibleLibraryID: "/vercel/next.js",
     topic: "client components use client app router best practices",
     tokens: 2000
   })
   ```
   **Extract**: `'use client'` directive usage, routing hooks, data fetching

3. **Context7: Tailwind CSS** (MANDATORY)
   ```typescript
   mcp__context7__get_library_docs({
     context7CompatibleLibraryID: "/tailwindlabs/tailwindcss.com",
     topic: "responsive design mobile-first breakpoints animations utilities",
     tokens: 2000
   })
   ```
   **Extract**: Responsive patterns, utility combinations, animation classes

4. **Context7: TanStack Query** (MANDATORY)
   ```typescript
   mcp__context7__get_library_docs({
     context7CompatibleLibraryID: "/tanstack/query",
     topic: "useQuery useMutation optimistic updates error handling",
     tokens: 2500
   })
   ```
   **Extract**: Data fetching patterns, cache invalidation, loading states

5. **shadcn MCP: Component discovery** (MANDATORY)
   ```typescript
   mcp__shadcn__search_items_in_registries({
     registries: ['@shadcn'],
     query: "form input button card dialog", // Adjust based on feature
     limit: 20
   })

   mcp__shadcn__view_items_in_registries({
     items: ['@shadcn/button', '@shadcn/form', '@shadcn/dialog']
   })
   ```
   **Extract**: Available components, composition patterns, accessibility features

6. **Additional Context7 queries** (as needed):
   - React Hook Form: `/react-hook-form/react-hook-form` - "zodResolver validation errors"
   - Framer Motion (if animations needed): `/grx7/framer-motion` - "variants spring animations"

**Deliverable**: Notes on latest patterns to apply in design phase.

---

### PHASE 2: Design Architecture (BEFORE Implementation)

**Objective**: Plan component hierarchy, state management, and user flows.

**Steps**:

1. **Review E2E test specifications**:
   ```typescript
   // Read E2E tests to understand required user flows
   Read('app/e2e/{feature}.spec.ts')
   ```
   **Extract**:
   - Required `data-testid` selectors
   - User interaction sequences
   - Expected UI elements (buttons, forms, lists)
   - Success/error state behaviors

2. **Design component hierarchy**:
   ```markdown
   ## Component Architecture

   ### Page Level (app/(main)/{feature}/page.tsx)
   - Route container
   - TanStack Query for data fetching
   - Layout composition

   ### Feature Components (features/{feature}/components/)
   - {Feature}List - Display collection
   - {Feature}Form - Create/Edit form
   - {Feature}Dialog - Modal interactions

   ### Presentation Components
   - {Feature}Item - Single item card
   - {Feature}Filters - Filter controls
   - {Feature}Stats - Statistics display

   ### Base Components (shadcn/ui)
   - Button, Input, Card, Dialog (composition, not modification)
   ```

3. **Plan state management**:
   ```markdown
   ## State Strategy

   **Server State** (TanStack Query):
   - useQuery for reads (list, single item)
   - useMutation for writes (create, update, delete)
   - Query key structure: ['feature', ...params]

   **Form State** (React Hook Form):
   - Zod schema for validation
   - zodResolver integration
   - Accessible error messages

   **UI State** (Zustand - if needed):
   - Dialog open/close
   - Sidebar collapsed state
   - Theme preference (handled by next-themes)
   ```

4. **Design user flows**:
   ```markdown
   ## Flow 1: Create {Entity}
   1. User clicks "Create" button
      → Opens dialog with form
   2. User fills fields (real-time validation)
   3. User submits
      → Loading state, disable form
   4. Success:
      → Close dialog, toast notification, refetch list
   5. Error:
      → Show error in form, keep dialog open, focus first error

   ## Flow 2: Edit {Entity}
   [Similar pattern...]

   ## Flow 3: Delete {Entity}
   [Similar pattern...]
   ```

5. **Plan accessibility patterns**:
   ```markdown
   ## Accessibility Design

   **Keyboard Navigation**:
   - Tab order: logical flow
   - Enter: submit forms, activate buttons
   - Escape: close dialogs
   - Arrow keys: navigate lists

   **ARIA Labels**:
   - Icon buttons: aria-label with context
   - Form fields: htmlFor + id association
   - Loading states: aria-busy
   - Error messages: aria-invalid + aria-describedby

   **Focus Management**:
   - Auto-focus first field on dialog open
   - Return focus to trigger on close
   - Focus trap in modals
   ```

6. **Plan responsive strategy**:
   ```markdown
   ## Responsive Design

   **Mobile (< 640px)**:
   - Single column layout
   - Stack cards vertically
   - Full-width buttons
   - Hide non-essential content

   **Tablet (640px - 1024px)**:
   - 2-column grid
   - Sidebar collapsible
   - Optimized spacing

   **Desktop (> 1024px)**:
   - 3-column grid
   - Fixed sidebar
   - Full feature set
   ```

**Deliverable**: Written design document covering hierarchy, state, flows, accessibility, and responsive strategy.

---

### PHASE 3: Implementation (Following Design)

**Objective**: Build React components following the design from Phase 2.

**🔐 CASL Integration (IF Authorization Required)**:

If E2E tests verify `<Can>` component visibility or the feature requires permission-based UI, implement CASL React integration FIRST before other components. See **Pattern 0: CASL React Integration** below.

**Implementation Order** (Bottom-Up):

0. **CASL Integration** (IF authorization required - implement FIRST)
   - AbilityContext provider
   - useAppAbility hook
   - Load ability in layout/page

1. **Form Components** (Highest Priority)
   - Complex, reusable
   - React Hook Form + Zod validation
   - Example: `CreateTaskForm.tsx`

2. **List/Display Components**
   - TanStack Query integration
   - Loading and error states
   - Example: `TaskList.tsx`

3. **Action Components**
   - Buttons, dialogs
   - Wire up mutations
   - Example: `CreateTaskDialog.tsx`

4. **Page Integration**
   - Compose all components
   - Test user flows
   - Example: `app/(main)/tasks/page.tsx`

**Code Patterns**:

#### Pattern 0: CASL React Integration (IF Authorization Required)

**When to implement**: If E2E tests verify `<Can>` component visibility or PRD specifies permission-based UI.

**Step 0.1: Create Ability Context**

**File**: `features/{feature}/context/AbilityContext.tsx`

```typescript
'use client';

import { createContext, useContext, type ReactNode } from 'react';
import type { AppAbility } from '../entities';

const AbilityContext = createContext<AppAbility | null>(null);

export function AbilityProvider({
  ability,
  children,
}: {
  ability: AppAbility;
  children: ReactNode;
}) {
  return (
    <AbilityContext.Provider value={ability}>
      {children}
    </AbilityContext.Provider>
  );
}

export function useAppAbility() {
  const ability = useContext(AbilityContext);
  if (!ability) {
    throw new Error('useAppAbility must be used within AbilityProvider');
  }
  return ability;
}
```

**Step 0.2: Load Ability in Layout/Page**

**File**: `app/(main)/{feature}/layout.tsx` or `app/(main)/{feature}/page.tsx`

```typescript
import { loadUserAbility } from '@/features/{feature}/use-cases/loadUserAbility';
import { AbilityProvider } from '@/features/{feature}/context/AbilityContext';
import { createClient } from '@/lib/supabase-server';
import { redirect } from 'next/navigation';

export default async function FeatureLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // 1. Get authenticated user
  const supabase = createClient();
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (authError || !user) {
    redirect('/login');
  }

  // 2. Get current workspace (from cookies or URL)
  const workspaceId = 'workspace-id'; // TODO: Get from context

  // 3. Load user's ability for this workspace
  const ability = await loadUserAbility(user.id, workspaceId);

  // 4. Provide ability to all child components
  return (
    <AbilityProvider ability={ability}>
      {children}
    </AbilityProvider>
  );
}
```

**Step 0.3: Use in Components**

**Declarative visibility with `<Can>` component**:

```typescript
'use client';

import { Can } from '@casl/react';
import { useAppAbility } from '../context/AbilityContext';
import { Button } from '@/components/ui/button';
import { Trash2, Edit, Plus } from 'lucide-react';

export function BoardActions({ board }: { board: Board }) {
  const ability = useAppAbility();

  return (
    <div className="flex gap-2">
      {/* Show button ONLY if user can create boards */}
      <Can I="create" a="Board" ability={ability}>
        <Button variant="default">
          <Plus className="mr-2 h-4 w-4" />
          Create
        </Button>
      </Can>

      {/* Show button ONLY if user can update boards */}
      <Can I="update" a="Board" ability={ability}>
        <Button variant="secondary">
          <Edit className="mr-2 h-4 w-4" />
          Edit
        </Button>
      </Can>

      {/* Show button ONLY if user can delete boards */}
      <Can I="delete" a="Board" ability={ability}>
        <Button variant="destructive">
          <Trash2 className="mr-2 h-4 w-4" />
          Delete
        </Button>
      </Can>
    </div>
  );
}
```

**Programmatic checks with `ability.can()`**:

```typescript
'use client';

import { useAppAbility } from '../context/AbilityContext';
import { Button } from '@/components/ui/button';
import { Settings } from 'lucide-react';

export function BoardHeader({ board }: { board: Board }) {
  const ability = useAppAbility();

  // Complex conditional rendering
  const canManage = ability.can('update', 'Board') && ability.can('delete', 'Board');

  return (
    <div className="flex items-center justify-between">
      <h1>{board.name}</h1>

      {/* Conditional rendering based on multiple abilities */}
      {canManage && (
        <Button variant="outline">
          <Settings className="mr-2 h-4 w-4" />
          Manage Board
        </Button>
      )}

      {/* Disable button if user cannot perform action */}
      <Button
        disabled={!ability.can('archive', 'Board')}
        onClick={() => archiveBoard(board.id)}
      >
        Archive
      </Button>
    </div>
  );
}
```

**Field-level permissions**:

```typescript
'use client';

import { Can } from '@casl/react';
import { useAppAbility } from '../context/AbilityContext';

export function BoardDetails({ board }: { board: Board }) {
  const ability = useAppAbility();

  return (
    <div>
      <p>Name: {board.name}</p>
      <p>Description: {board.description}</p>

      {/* Show sensitive field ONLY if user can read it */}
      <Can I="read" a="Board" field="settings" ability={ability}>
        <p>Settings: {JSON.stringify(board.settings)}</p>
      </Can>
    </div>
  );
}
```

**CASL Implementation Checklist**:

- [ ] ✅ AbilityContext.tsx created with provider and hook
- [ ] ✅ AbilityProvider wraps feature in layout/page
- [ ] ✅ loadUserAbility() called server-side
- [ ] ✅ `<Can>` component used for show/hide logic
- [ ] ✅ `ability.can()` used for complex conditional rendering
- [ ] ✅ Buttons disabled (not just hidden) when user lacks permission
- [ ] ✅ Field-level permissions implemented (if applicable)
- [ ] ✅ E2E tests pass (verify visibility matches permissions)
- [ ] ✅ No console errors about missing AbilityContext

**Critical Rules**:
- ✅ ALWAYS use `<Can>` for simple show/hide (cleaner, declarative)
- ✅ Use `ability.can()` for complex logic (multiple checks, computed values)
- ✅ Disable buttons when user can't act (better UX than hiding)
- ✅ Wrap pages/layouts with AbilityProvider (not individual components)
- ❌ NEVER implement authorization logic in components (use ability)
- ❌ NEVER bypass CASL checks to "improve UX" (security first)
- ❌ NEVER call useAppAbility() outside AbilityProvider (will throw error)

---

#### Pattern 1: Page Component
```typescript
'use client'

import { useQuery } from '@tanstack/react-query'
import { taskUseCases } from '@/features/tasks/use-cases'
import { TaskList } from '@/features/tasks/components/TaskList'
import { CreateTaskDialog } from '@/features/tasks/components/CreateTaskDialog'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'
import { useState } from 'react'

export default function TasksPage() {
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ['tasks'],
    queryFn: taskUseCases.getTasks,
  })

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Tasks</h1>
          <p className="text-sm text-muted-foreground">
            Manage your tasks and track progress
          </p>
        </div>
        <Button
          onClick={() => setCreateDialogOpen(true)}
          data-testid="create-task-button"
        >
          <Plus className="mr-2 h-4 w-4" />
          Create Task
        </Button>
      </div>

      {/* Content */}
      {isLoading && <TaskListSkeleton />}
      {error && <ErrorDisplay error={error} />}
      {tasks && <TaskList tasks={tasks} />}

      {/* Dialogs */}
      <CreateTaskDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
      />
    </div>
  )
}
```

#### Pattern 2: Form Component
```typescript
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { TaskCreateSchema, type TaskCreate } from '../entities'
import { taskUseCases } from '../use-cases'
import { useTranslations } from 'next-intl'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'

interface TaskFormProps {
  onSuccess?: () => void
}

export function TaskForm({ onSuccess }: TaskFormProps) {
  const t = useTranslations('tasks')
  const queryClient = useQueryClient()

  // Create Zod schema inside component for translation access
  const form = useForm<TaskCreate>({
    resolver: zodResolver(TaskCreateSchema),
    defaultValues: {
      title: '',
      description: '',
      status: 'pending',
    },
  })

  const createMutation = useMutation({
    mutationFn: taskUseCases.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success(t('create.success'))
      form.reset()
      onSuccess?.()
    },
    onError: (error) => {
      toast.error(t('create.error'), {
        description: error.message,
      })
    },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((data) => createMutation.mutate(data))}>
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel htmlFor="title">{t('form.title.label')}</FormLabel>
              <FormControl>
                <Input
                  id="title"
                  data-testid="task-title-input"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={createMutation.isPending}
          data-testid="submit-button"
        >
          {createMutation.isPending ? t('form.submitting') : t('form.submit')}
        </Button>
      </form>
    </Form>
  )
}
```

#### Pattern 3: Responsive Component
```typescript
<div className="
  grid
  grid-cols-1        /* Mobile: 1 column */
  md:grid-cols-2     /* Tablet: 2 columns */
  lg:grid-cols-3     /* Desktop: 3 columns */
  gap-4 md:gap-6     /* Responsive gap */
  p-4 md:p-6 lg:p-8  /* Responsive padding */
">
  {items.map(item => <ItemCard key={item.id} item={item} />)}
</div>
```

**Critical Rules**:
- ✅ Use `data-testid` from E2E tests
- ✅ Use `useTranslations()` for ALL text (NO hardcoded strings)
- ✅ Use semantic tokens from Style Guide (NO arbitrary values)
- ✅ Integrate with use cases via TanStack Query (NOT data services)
- ✅ Add ARIA labels for icon buttons
- ✅ Ensure keyboard navigation works

**Deliverable**: Implemented React components following all patterns.

---

### PHASE 4: Validation (Chrome DevTools + Accessibility)

**Objective**: Verify implementation meets all quality standards.

**Steps**:

1. **Run E2E tests** (MANDATORY - must pass 100%)
   ```bash
   cd app
   npm run test:e2e -- --grep "{feature}"
   ```
   **Expected**: ALL tests GREEN ✅
   **If RED**: Fix implementation (DO NOT modify tests)

2. **Visual verification with Chrome DevTools MCP** (MANDATORY)
   ```typescript
   // Start browser session
   mcp__chrome_devtools__new_page()

   // Navigate to feature
   mcp__chrome_devtools__navigate_page({
     url: "http://localhost:3000/{feature-page}"
   })

   // Capture screenshots at all breakpoints
   const breakpoints = [
     { name: 'mobile', width: 375, height: 667 },
     { name: 'tablet', width: 768, height: 1024 },
     { name: 'desktop', width: 1440, height: 900 }
   ]

   for (const bp of breakpoints) {
     // Light mode
     await mcp__chrome_devtools__take_screenshot({
       filePath: `./screenshots/${bp.name}-light.png`,
       fullPage: true
     })

     // Dark mode
     await mcp__chrome_devtools__evaluate_script({
       script: "document.documentElement.classList.add('dark')"
     })
     await mcp__chrome_devtools__take_screenshot({
       filePath: `./screenshots/${bp.name}-dark.png`,
       fullPage: true
     })
     await mcp__chrome_devtools__evaluate_script({
       script: "document.documentElement.classList.remove('dark')"
     })
   }
   ```

3. **Accessibility audit** (MANDATORY - WCAG 2.1 AA)
   ```bash
   cd app
   npm run test:e2e -- --grep "accessibility"
   ```
   **Manual checks**:
   - [ ] Color contrast ≥4.5:1 for text (use Chrome DevTools "Inspect")
   - [ ] All interactive elements keyboard accessible (Tab, Enter, Escape)
   - [ ] Icon buttons have aria-label
   - [ ] Form fields have labels (htmlFor + id)
   - [ ] Focus indicators visible
   - [ ] Screen reader compatible (test with VoiceOver/NVDA)

4. **Style Guide compliance verification** (MANDATORY)
   ```bash
   # Search for Style Guide violations
   grep -r "bg-\[#" features/{feature}/  # Arbitrary colors
   grep -r "text-\[[0-9]" features/{feature}/  # Arbitrary font sizes
   grep -r "p-\[[0-9]" features/{feature}/  # Arbitrary padding
   ```
   **Expected**: NO matches (all values from Style Guide)

5. **Performance check** (TARGET)
   ```bash
   npm run build
   npm run start
   # Open Lighthouse in Chrome DevTools
   # Run audit for Performance + Accessibility
   ```
   **Targets**:
   - Lighthouse Accessibility: >90
   - LCP (Largest Contentful Paint): <2.5s
   - FID (First Input Delay): <100ms
   - CLS (Cumulative Layout Shift): <0.1

**Deliverable**: All tests passing, screenshots captured, accessibility verified, Style Guide compliant.

---

### PHASE 5: Documentation (Iteration File)

**Objective**: Document implementation with evidence for Architect + User review.

**Template**: Use `PRDs/_templates/agent-iteration-template.md`

**Structure**:
```markdown
# UI/UX Expert - Iteration 01

**Agent**: UI/UX Expert
**Date**: YYYY-MM-DD HH:MM
**Status**: Ready for Review

---

## Context
Creating user interface for [Feature Name]

## Work Completed

### Pages Created
1. **{Feature}Page** (`app/(main)/{feature}/page.tsx`)
   - Description of functionality
   - Data fetching setup
   - Layout composition

### Components Created
1. **{Feature}Form** (`features/{feature}/components/{Feature}Form.tsx`)
   - React Hook Form + Zod validation
   - Loading states
   - Error handling
   - Accessibility: WCAG 2.1 AA compliant

2. **{Feature}List** (`features/{feature}/components/{Feature}List.tsx`)
   - TanStack Query integration
   - Empty states
   - Responsive grid

[List all components...]

## Technical Decisions
1. **Component Library**: shadcn/ui (Button, Dialog, Form, Card)
2. **State Management**: TanStack Query for server state
3. **Validation**: Zod schemas with zodResolver
4. **Internationalization**: next-intl (no hardcoded strings)

## Evidence

### E2E Tests
\```bash
npm run test:e2e -- --grep "{feature}"
# PASS: 12/12 tests ✅
# All user flows working
\```

### Screenshots
**Mobile (375px)**:
![Mobile Light](./ screenshots/mobile-light.png)
![Mobile Dark](./screenshots/mobile-dark.png)

**Tablet (768px)**:
![Tablet Light](./screenshots/tablet-light.png)
![Tablet Dark](./screenshots/tablet-dark.png)

**Desktop (1440px)**:
![Desktop Light](./screenshots/desktop-light.png)
![Desktop Dark](./screenshots/desktop-dark.png)

### Accessibility Audit
- [x] Keyboard navigation works (Tab, Enter, Escape, Arrow keys)
- [x] Screen reader compatible (tested with VoiceOver)
- [x] Focus indicators visible
- [x] ARIA labels present on icon buttons
- [x] Color contrast ratios meet WCAG AA (≥4.5:1 text, ≥3:1 UI)
- [x] Form labels properly associated (htmlFor + id)

### Style Guide Compliance
- [x] All colors from semantic tokens (no arbitrary hex values)
- [x] Typography from scale (text-xs through text-4xl)
- [x] Spacing from scale (spacing-1 through spacing-24)
- [x] Animation durations: 200ms, 300ms, or 500ms only
- [x] NO traditional CSS (Tailwind utilities only)

### Performance Metrics
- **Lighthouse Score**: 95+ (Performance + Accessibility)
- **LCP**: 1.8s ✅ (<2.5s target)
- **FID**: 50ms ✅ (<100ms target)
- **CLS**: 0.05 ✅ (<0.1 target)

## Coverage Against Requirements
| Requirement | Status | Evidence |
|------------|--------|----------|
| Create {entity} flow | ✅ | E2E test passing |
| List view | ✅ | E2E test passing |
| Accessibility WCAG AA | ✅ | Audit passed |
| Responsive design | ✅ | Screenshots at all breakpoints |
| Style Guide compliant | ✅ | No violations found |

## Quality Checklist
- [x] All E2E tests passing (100%)
- [x] Style Guide followed exactly
- [x] WCAG 2.1 AA compliance verified
- [x] No hardcoded strings (i18n complete)
- [x] shadcn/ui components used (no custom UI library)
- [x] Chrome DevTools validated
- [x] Screenshots provided (all breakpoints, both modes)
- [x] Cross-browser compatible (Chromium, Firefox, Safari)

---

## Review Status
**Submitted**: YYYY-MM-DD HH:MM

### Architect Review
**Status**: Pending

### User Review
**Status**: Pending
```

**Deliverable**: Complete iteration document with screenshots and evidence.

---

## MCP INTEGRATIONS

### Context7 (MANDATORY in Phase 1)
**Purpose**: Get latest React/Next.js/Tailwind/TanStack Query best practices

**Critical queries**:
- `/reactjs/react.dev` - React Hooks, component patterns
- `/vercel/next.js` - App Router, client components
- `/tailwindlabs/tailwindcss.com` - Responsive design, utilities
- `/tanstack/query` - Data fetching patterns

### shadcn MCP (MANDATORY in Phase 1)
**Purpose**: Discover shadcn/ui components and composition patterns

**Functions**:
- `search_items_in_registries` - Find components
- `view_items_in_registries` - Get component details
- `get_item_examples_from_registries` - Usage examples

### Chrome DevTools (MANDATORY in Phase 4)
**Purpose**: Visual validation and accessibility audits

**Functions**:
- `new_page` - Start browser session
- `navigate_page` - Go to URL
- `take_screenshot` - Capture visuals
- `evaluate_script` - Run JavaScript (e.g., toggle dark mode)

---

## REFERENCES (Load on Demand)

Reference files in `references/` provide detailed guidance. Load only when needed:

1. **react-patterns.md** - React Hook patterns, composition strategies
2. **shadcn-composition.md** - shadcn/ui component catalog and usage
3. **tailwind-responsive.md** - Responsive design patterns, breakpoints
4. **accessibility-wcag.md** - WCAG 2.1 AA compliance checklist
5. **performance-web-vitals.md** - Core Web Vitals optimization
6. **tanstack-query-patterns.md** - Data fetching best practices
7. **form-validation-patterns.md** - React Hook Form + Zod integration
8. **animation-best-practices.md** - Framer Motion & Tailwind animations

**Example**:
```
User: "How do I implement optimistic updates?"
↓
Read('references/tanstack-query-patterns.md')
↓
Apply optimistic update pattern from reference
```

---

## SCRIPTS (Automation Helpers)

Scripts in `scripts/` automate repetitive tasks. Run when needed:

1. **take-baseline-screenshots.sh** - Capture before-implementation screenshots
2. **validate-accessibility.sh** - Run Lighthouse accessibility audit
3. **check-style-guide-compliance.sh** - Scan for Style Guide violations
4. **run-e2e-tests.sh** - Execute E2E tests for feature
5. **capture-final-screenshots.sh** - Capture after-implementation screenshots
6. **generate-component-manifest.sh** - List all components created

**Example**:
```bash
./scripts/check-style-guide-compliance.sh features/tasks/
# Scans for arbitrary colors, spacing, font sizes
```

---

## ASSETS (Component Templates)

Templates in `assets/` provide starting points. Customize as needed:

1. **component-templates/page-template.tsx** - Page component structure
2. **component-templates/form-template.tsx** - Form with validation
3. **component-templates/list-template.tsx** - Data list pattern
4. **component-templates/modal-template.tsx** - Dialog pattern
5. **form-examples/simple-form.tsx** - Basic form
6. **form-examples/multi-step-form.tsx** - Wizard pattern
7. **layout-patterns/dashboard-layout.tsx** - Dashboard structure

**Example**:
```
User: "Create a task creation form"
↓
Read('assets/component-templates/form-template.tsx')
↓
Customize for task-specific fields
↓
Integrate with taskUseCases.createTask
```

---

## CRITICAL REMINDERS

### DO (MANDATORY)
✅ Read Style Guide FIRST (Phase 0)
✅ Consult Context7 + shadcn MCP BEFORE design (Phase 1)
✅ Make E2E tests pass WITHOUT modifying them
✅ Use Chrome DevTools for visual validation
✅ Achieve WCAG 2.1 AA compliance
✅ Use semantic tokens (NO arbitrary values)
✅ Capture screenshots at ALL breakpoints
✅ Document with evidence in iteration file
✅ Wait for Architect + User approval

### DO NOT (PROHIBITED)
❌ Implement business logic (use cases handle this)
❌ Modify E2E tests to make them pass
❌ Access data services directly (go through use cases)
❌ Use non-approved libraries (shadcn/ui + Tailwind ONLY)
❌ Write traditional CSS (Tailwind utilities ONLY)
❌ Create inaccessible components (WCAG AA mandatory)
❌ Use arbitrary values outside Style Guide
❌ Skip Context7 consultation
❌ Advance without approval

---

## SUCCESS CRITERIA

Implementation is complete when:
- ✅ 100% E2E tests passing
- ✅ Lighthouse accessibility score >90
- ✅ WCAG 2.1 AA compliant (verified)
- ✅ Core Web Vitals green (LCP <2.5s, FID <100ms, CLS <0.1)
- ✅ Style Guide compliance 100%
- ✅ Cross-browser compatible
- ✅ Screenshots at all breakpoints (mobile, tablet, desktop)
- ✅ Both light and dark modes verified
- ✅ Documented in iteration file
- ✅ Architect + User approval received

---

**This skill ensures UI implementations are accessible, performant, beautiful, and exactly match the project's visual design system.**
