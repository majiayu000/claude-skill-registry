---
name: architecture-philosophy
description: Core architectural principles for StepLeague - modular design, system thinking, future-proofing, and maintenance reduction. Use when designing new features, refactoring code, considering implementation approaches, or making any architectural decisions. Keywords: architecture, design, modular, refactoring, reusable, shadcn, maintenance, future-proof, system.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# Architecture Philosophy Skill

> **THE MOST IMPORTANT SKILL:** This skill defines HOW we build everything.
> Every other skill references these principles.

---

## ⚠️ Critical: Read This First

Before implementing ANY solution:

1. **Think systems, not solutions** - Will this pattern be needed elsewhere?
2. **Check existing patterns** - Is this already solved in the codebase?
3. **Consider maintenance** - How many places need updating when requirements change?
4. **Reference other skills** - They encode project-specific implementations of these principles

---

## Core Principles

Every solution in StepLeague must follow these principles:

### 1. 🧩 Modular Over Monolithic (MOST CRITICAL)

**Build systems, not one-off solutions.**

> If you're writing code that solves just ONE specific case, you're probably doing it wrong.
> Take 5 extra minutes to think: "How can I make this reusable?"

| ❌ One-Off (BAD) | ✅ Modular System (GOOD) |
|------------------|--------------------------|
| Hardcoded notification for leagues | Generic notification system with event types |
| Custom dropdown for one form | Reusable `FormSelect` component |
| Inline error handling | Centralized `AppError` system in `src/lib/errors.ts` |
| Magic numbers (`if (count > 50)`) | Settings from `app_settings` table |
| Duplicate validation logic | Shared Zod schemas in `/lib/schemas/` |

**Questions to ask BEFORE writing code:**
- Will this pattern be needed elsewhere? → Extract it
- Can I extend an existing utility/hook/component? → Extend, don't duplicate
- Does this belong in a shared location? → Move it to `/lib/` or `/components/ui/`
- Am I hardcoding a value that might change? → Use settings

### 2. 🔮 Future-Thinking

**Design for tomorrow, implement for today.**

- **Settings over hardcoding**: Use `app_settings` table for configurable values
- **Feature flags**: Gate new features with `useFeatureFlag()`
- **Extensible schemas**: Add columns that allow future use cases

```typescript
// ❌ WRONG: Hardcoded limit
const MAX_PROXIES = 10;

// ✅ CORRECT: Configurable
const maxProxies = useAppSettings('proxy_max_per_user', 10);
```

### 3. 🛡️ Defensive Programming

**Assume things will fail. Plan for it.**

- **Use the error handling system** - Reference `error-handling` skill
- **Graceful degradation** - If a feature fails, don't crash the page
- **Fallback values** - Always have sensible defaults

```typescript
// ✅ Defensive pattern with fallback
const branding = await getCachedBranding().catch(() => DEFAULT_BRANDING);
```

### 4. 📉 Maintenance Reduction

**Less code = less bugs = less maintenance.**

| Principle | Example |
|-----------|---------|
| Use existing libraries | shadcn/ui over custom components |
| Central configuration | `badges.ts` for all badge colors |
| Registry patterns | `CacheRegistry` for cache tags |
| Convention over configuration | File-based routing |

---

## Mandatory Patterns

### A. Use shadcn/ui Components

**ALWAYS prefer shadcn over custom implementations.**

```typescript
// ✅ Use shadcn
import { Dialog } from "@/components/ui/dialog";
import { DropdownMenu } from "@/components/ui/dropdown-menu";
import { toast } from "@/hooks/use-toast";

// ❌ Don't create custom modals, dropdowns, or alerts
```

**Installed shadcn components:**
- `toast`, `dialog`, `dropdown-menu`, `input`, `label`
- `textarea`, `select`, `checkbox`, `tooltip`
- `confirm-dialog` (custom wrapper)

Reference: `src/components/ui/`

### B. Use Reusable Form Components

**Reference the `form-components` skill.**

```typescript
// ✅ Use form fields
import { FormInput, FormSelect, FormCheckbox } from "@/components/ui/form-fields";

// ❌ Don't use raw <input>, <select> elements
```

### C. Use the API Handler Pattern

**Reference the `api-handler` skill.**

```typescript
// ✅ Use withApiHandler
export const POST = withApiHandler({
  auth: 'required',
  schema: mySchema,
}, async ({ user, body, adminClient }) => {
  return { success: true };
});

// ❌ Don't write boilerplate auth checks in every route
```

### D. Use the Error System

**Reference the `error-handling` skill.**

```typescript
// ✅ Use AppError
throw new AppError({
  code: ErrorCode.VALIDATION_FAILED,
  message: 'Invalid input',
  context: { field: 'email' },
  recoverable: true,
});

// ❌ Don't throw generic Error objects
```

### E. Use CSS Variables for Theming

**Reference the `design-system` skill.**

```tsx
// ✅ Semantic variables
<div className="bg-card text-foreground border-border">

// ❌ Hardcoded Tailwind colors
<div className="bg-slate-900 text-slate-300 border-slate-700">
```

---

## Decision Framework

When implementing any feature, follow this checklist:

### Before Writing Code

1. **Check existing patterns** in AGENTS.md
2. **Search for similar implementations** in the codebase
3. **Review relevant skills** in `.agent/skills/`
4. **Consider: Is this a one-off or a pattern?**

### While Writing Code

1. **Extract reusable pieces** into utilities/components
2. **Use centralized configuration** (settings, registries)
3. **Add proper error handling** with AppError
4. **Follow the design system** for all UI

### After Writing Code

1. **Update documentation** if adding new patterns
2. **Add to design system page** if creating UI components
3. **Reference in AGENTS.md** if it's a key pattern
4. **Create a skill** if it's complex enough

---

## Cross-Skill References

| When Working On | Reference Skill |
|-----------------|-----------------|
| New features | `prd-creation` |
| API routes | `api-handler` |
| Database queries | `supabase-patterns` |
| Error handling | `error-handling` |
| UI/Styling | `design-system` |
| Forms | `form-components` |
| After completion | `project-updates` |

---

## Anti-Patterns to Avoid

### 1. The "Quick Fix"

> "I'll just add this inline, it's faster"

**Why it's bad:** Creates tech debt, makes code harder to maintain.

**Instead:** Take 5 extra minutes to do it properly.

### 2. The "Special Case"

> "This component is unique, it needs custom styling"

**Why it's bad:** Breaks consistency, harder to theme.

**Instead:** Use existing components, extend if needed.

### 3. The "Magic Number"

> `if (count > 50) { ... }`

**Why it's bad:** Unexplained, not configurable.

**Instead:** Use settings or named constants.

### 4. The "Silenced Error"

> `try { ... } catch { /* ignore */ }`

**Why it's bad:** Hides bugs, makes debugging impossible.

**Instead:** Use `normalizeError()` and `reportErrorClient()`.

### 5. The "Copy-Paste Component"

> Creating a new component that's 90% the same as existing one.

**Why it's bad:** Duplicated code, inconsistent behavior.

**Instead:** Extract shared logic, use props for variations.

---

## The 3-Time Rule

**If you do something 3 times, extract it.**

| Count | Action |
|-------|--------|
| 1st time | Implement inline |
| 2nd time | Note the pattern |
| 3rd time | Extract to utility/component/skill |

---

## Key Reference Files

| Area | File |
|------|------|
| Error handling | `src/lib/errors.ts` |
| API handler | `src/lib/api/handler.ts` |
| Form components | `src/components/ui/form-fields.tsx` |
| Badge config | `src/lib/badges.ts` |
| Cache registry | `src/lib/cache/serverCache.ts` |
| Menu config | `src/lib/menuConfig.ts` |
| Theme variables | `src/app/globals.css` |
| Settings hook | `src/hooks/useAppSettings.ts` |

---

## Summary

> **Build systems, not solutions.**
> 
> Every feature you implement should make the next feature easier to build.
