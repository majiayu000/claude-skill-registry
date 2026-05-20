---
name: react-writing-plans
description: Use when you have a spec, PRD, or requirements for a React frontend feature requiring multiple components, stores, or API integrations, before writing any code. Creates concise implementation plans that reference architecture contracts.
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# React Writing Plans

## Overview

Plans are **architectural blueprints**, not copy-paste code. Each task references contracts defined in the architecture doc. Implementers use TDD skills to fill in the actual code.

**Announce at start:** "I'm using the react-writing-plans skill to create the implementation plan."

**Save plans to:** `_docs/plans/YYYY-MM-DD-<feature-name>.md`

## When to Use
- Multi-step React feature requiring new components, stores, or API integration
- PRD or spec exists but no implementation plan
- Feature touches 3+ files or requires coordinated changes
- Need to hand off implementation to another engineer or subagent

## When NOT to Use
- Single-file bug fix with obvious cause and fix
- Config/environment changes (vite.config, tsconfig, tailwind.config)
- Renaming or moving files without logic changes
- Adding an npm package with no code changes beyond the import

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** **REQUIRED SUB-SKILL:** Use `saurun:react-tdd` to implement this plan task-by-task with TDD.

**Goal:** [One sentence describing what this builds]

**Architecture:** `_docs/specs/{DATE}-{feature}-architecture.md`

**Tech Stack:** React 19, Vite, TypeScript, Tailwind CSS v4, Zustand, Vitest, React Testing Library, MSW

---
```

## Task Structure

```markdown
### Task N: [Name]

**Implements:** [Contract reference from Architecture doc, e.g., "AddItemForm (Architecture §Component Tree)"]

**Files:**
- Create: `src/components/exact/path/Component.tsx`
- Test: `src/components/exact/path/__tests__/Component.test.tsx`

**Behaviors:**
- [Happy path behavior]
- [Error case 1]
- [Error case 2]

**Dependencies:** Task X (if applicable)
```

## Frontend Task Examples

### Form Component (validation grouped by field)

```markdown
### Task 3: RegisterForm component

**Implements:** RegisterForm (Architecture §Components - Auth)

**Files:**
- Create: `src/components/auth/RegisterForm.tsx`
- Test: `src/components/auth/__tests__/RegisterForm.test.tsx`

**Behaviors:**
- Email: required, valid format
- Password: required, min 8, uppercase + lowercase + digit
- DisplayName: required, 2-50 chars
- Valid submit calls onSubmit with RegisterRequest
- Invalid submit shows field errors
```

### Complex Form (many fields)

```markdown
### Task 12: RecipeForm component

**Implements:** RecipeForm (Architecture §Components - Recipe Form)

**Files:**
- Create: `src/components/recipe-form/RecipeForm.tsx`
- Test: `src/components/recipe-form/__tests__/RecipeForm.test.tsx`

**Behaviors:**
- Title: required, 1-200 chars
- Description: required, 1-2000 chars
- Servings: required, 1-100
- PrepTime/CookTime: required, 0-1440 min
- CategoryId: required, must exist
- Ingredients: min 1 item (validated by IngredientInput)
- Steps: min 1 item (validated by StepInput)
- Populates fields from initialData when editing
- Valid submit calls onSubmit with CreateRecipeRequest

**Dependencies:** Task 9-11 (form sub-components)
```

### Display Component (concise)

```markdown
### Task 5: RecipeCard component

**Implements:** RecipeCard (Architecture §Components - Recipe)

**Files:**
- Create: `src/components/recipe/RecipeCard.tsx`
- Test: `src/components/recipe/__tests__/RecipeCard.test.tsx`

**Behaviors:**
- Displays image, title, time, and author from RecipeListItemDto
- Click navigates to /opskrift/{id}
- Save button calls onSave when authenticated
```

### Page (concise with edge cases)

```markdown
### Task 8: RecipeDetailPage

**Implements:** /opskrift/{id} → RecipeDetailPage (Architecture §Pages)

**Files:**
- Create: `src/pages/RecipeDetailPage.tsx`
- Test: `src/pages/__tests__/RecipeDetailPage.test.tsx`

**Behaviors:**
- Fetches and renders RecipeDetail component
- 404 when recipe not found
- Owner sees edit/delete buttons

**Dependencies:** Task 6 (RecipeDetail)
```

### Store (state transitions)

```markdown
### Task 2: useAuthStore

**Implements:** useAuthStore (Architecture §Stores)

**Files:**
- Create: `src/stores/authStore.ts`
- Test: `src/stores/__tests__/authStore.test.ts`

**Behaviors:**
- login stores user/token and persists to localStorage
- logout clears state and localStorage
- isAuthenticated derived from token presence
```

## Conciseness Rules

**Plans are for autonomous agents, not humans. Every word costs tokens.**

### The Core Rule

**If it needs a test case, it needs a behavior line.**

This distinguishes testable behaviors (KEEP) from implementation details (DELETE).

### What to KEEP (Testable Behaviors)

These become test cases — always include them:

| Category | Examples |
|----------|----------|
| **Validation rules** | "Email must be valid format", "Password min 8 chars with uppercase + lowercase + digit" |
| **Error states** | "API error shows toast", "404 shows not found message" |
| **User interactions with outcomes** | "Submit calls onSave with form data", "Delete removes item from list" |
| **Edge cases** | "Empty list shows EmptyState", "Unauthorized redirects to login" |
| **Business logic** | "Servings adjustment scales ingredient amounts", "Owner sees edit button" |

### What to DELETE (Implementation Details)

These are NOT test cases — never include them:

| Category | Examples |
|----------|----------|
| **CSS/styling** | "Applies centered flex layout", "Uses red accent for errors" |
| **Animation** | "Animates open/close smoothly", "Fades in on mount" |
| **Standard React patterns** | "Accepts className prop", "Forwards ref" |
| **Accessibility (unless custom)** | "Button has proper role", "Input has aria-label" |
| **Generic UX** | "Disables button when loading", "Shows spinner while pending" |

### Form Validation: Group by Field

**List each field's validation constraints on ONE line.** Don't split min/max into separate behaviors.

```markdown
# ❌ TOO VERBOSE (splits constraints into separate lines)
**Behaviors:**
- Title field: required, shows error when empty
- Title field: max 200 chars, shows error when exceeded
- Description field: required, shows error when empty
- Description field: max 2000 chars, shows error when exceeded

# ❌ TOO CONCISE (agent won't know what to test)
**Behaviors:**
- Shows validation errors per field requirements

# ✓ CORRECT (one line per field, all constraints grouped)
**Behaviors:**
- Title: required, 1-200 chars
- Description: required, 1-2000 chars
- Password: required, min 8, uppercase + lowercase + digit
- Valid submit calls onSubmit with request DTO
- Invalid submit shows field errors
```

**Note:** "Shows error when X" is implied — just list the constraint.

### Combining Non-Validation Behaviors

For non-form components, combine related states:

```markdown
# ❌ VERBOSE
- Shows loading spinner while fetching
- Displays data when loaded
- Shows error message on failure

# ✓ COMBINED
- Handles loading/error/success states
- Renders data per architecture DTO
```

### Hard Limits
- **Forms:** 1 behavior per field + 2-3 for submit/populate = roughly (field count + 3)
- **Other components:** Max 4 behaviors
- If over limit → split task or combine related behaviors

## What Plans Include

| Element | Required |
|---------|----------|
| Exact file paths (Create/Modify/Test) | ✓ |
| Contract reference (`Implements:`) | ✓ |
| Behaviors (1 per field for forms, max 4 for others) | ✓ |
| Task dependencies | When applicable |

## What Plans Do NOT Include

| Element | Reason |
|---------|--------|
| Full test code | TDD skill generates tests from behaviors |
| Full implementation code | Implementer writes from contract + behaviors |
| Step-by-step TDD instructions | TDD skill handles workflow |
| CSS/styling details | Not testable — implementer decides |
| Animation/transition details | Not testable — implementer decides |
| Standard React patterns | "Accepts className", "Accessible button" implied |
| Generic UX behaviors | "Disables button when loading" implied |
| Summary tables | Unnecessary for agent execution |

## Test Infrastructure Task

**Task 1 of every plan MUST set up test infrastructure:**

```markdown
### Task 1: Test infrastructure setup

**Implements:** Shared test helpers (N/A - infrastructure)

**Files:**
- Create: `src/test-utils.tsx`
- Create: `src/mocks/server.ts`
- Create: `src/mocks/handlers.ts`
- Modify: `vitest.setup.ts`

**Behaviors:**
- renderWithProviders wraps components with necessary providers
- MSW server configured with onUnhandledRequest: 'error'
- Zustand store reset in beforeEach
```

## Tailwind v4 Compliance

**Implementers MUST follow these rules (remind in plan if UI-heavy):**

- CSS variables use **parentheses**: `bg-(--brand-color)` NOT `bg-[--brand-color]`
- Use renamed utilities: `shadow-xs`, `rounded-xs` (not `shadow-sm`, `rounded-sm` for smallest)
- Class merging: always `cn()`, never template literals
- No `theme()` in arbitrary values — use `var(--color-*)` instead

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing full test/implementation code | Just list behaviors — TDD skill writes code |
| Forgetting `Implements:` reference | Every task MUST reference architecture contract |
| Vague behaviors like "handles errors" | Be specific: "API error shows toast message" |
| Missing file paths | Every task MUST list exact Create/Modify/Test paths |
| Tasks too large (>3 files) | Split into smaller tasks |
| No test infrastructure in Task 1 | `renderWithProviders` + MSW setup MUST be Task 1 |
| Square bracket CSS vars | Use `bg-(--var)` NOT `bg-[--var]` |
| **Splitting field constraints** | Group all constraints for a field on ONE line: "Title: required, 1-200 chars" |
| **Collapsing ALL validation** | Each field needs its own behavior line |
| **Implementation details as behaviors** | "Applies flex layout" → delete (not testable) |
| **Stating obvious patterns** | Delete "accepts className", "disables when loading" |
| **Summary tables at end** | Delete — unnecessary for agent execution |

## Completion

After saving the plan, report:

**"Plan saved to `_docs/plans/<filename>.md`. Ready for execution."**
