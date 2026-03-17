---
name: react-forms
description: TanStack Form v1 - type-safe forms with Zod/Yup/Valibot validation, async validation, arrays, nested fields, React 19 Server Actions
version: 1.0.0
user-invocable: true
references: references/tanstack-form-basics.md, references/zod-validation.md, references/async-validation.md, references/server-actions.md, references/arrays-nested.md, references/typescript.md, references/yup-valibot.md, references/shadcn-integration.md, references/listeners.md, references/linked-fields.md, references/reactivity.md, references/reset-api.md, references/ssr-hydration.md, references/devtools.md, references/react-native.md, references/standard-schema.md, references/templates/basic-form.md, references/templates/multi-step-form.md, references/templates/dynamic-fields.md, references/templates/file-upload-form.md, references/templates/server-action-form.md, references/templates/optimistic-form.md, references/templates/nested-form.md, references/templates/search-form.md, references/templates/conditional-fields.md, references/templates/form-composition.md, references/templates/listeners-form.md, references/templates/linked-fields-form.md, references/templates/reactivity-form.md, references/templates/reset-form.md, references/templates/ssr-form.md, references/templates/devtools-form.md, references/templates/react-native-form.md
---

# TanStack Form v1 Core Features

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing form components and validation patterns
2. **fuse-ai-pilot:research-expert** - Verify latest TanStack Form v1 docs via Context7/Exa
3. **mcp__context7__query-docs** - Check Zod validation and React 19 Server Actions patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## MANDATORY: SOLID Principles

**ALWAYS apply SOLID principles from `solid-react` skill.**

→ See `../solid-react/SKILL.md` for complete rules

**Key Rules:**
- Files < 100 lines (split at 90)
- Interfaces in `modules/[feature]/src/interfaces/`
- JSDoc mandatory on all exports
- No business logic in components

---

## Core Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `useForm()` | Initialize form with validation | `references/tanstack-form-basics.md` |
| `useField()` | Subscribe to individual field | `references/tanstack-form-basics.md` |
| `form.Field` | Render prop component for fields | `references/tanstack-form-basics.md` |
| `form.Subscribe` | Watch form state changes | `references/tanstack-form-basics.md` |

→ See `references/tanstack-form-basics.md` for detailed usage

---

## Validation Adapters

| Library | Adapter | Bundle Size |
|---------|---------|-------------|
| **Zod** | `zodValidator()` | ~12KB |
| **Yup** | `yupValidator()` | ~40KB |
| **Valibot** | `valibotValidator()` | ~6KB |

→ See `references/zod-validation.md` for Zod patterns
→ See `references/yup-valibot.md` for alternatives

---

## Key Features

### Async Validation
Server-side checks with debouncing and loading states.
→ See `references/async-validation.md`

### Server Actions (React 19)
Integration with useActionState and progressive enhancement.
→ See `references/server-actions.md`

### Arrays & Nested Fields
Dynamic field arrays and dot notation for nested objects.
→ See `references/arrays-nested.md`

### TypeScript Integration
Full type inference from Zod schemas and defaultValues.
→ See `references/typescript.md`

### shadcn/ui Integration
Field wrapper components with shadcn styling.
→ See `references/shadcn-integration.md`

### Listeners (Side Effects)
onMount, onChange, onBlur, onSubmit with debouncing.
→ See `references/listeners.md`

### Linked Fields
Cross-field validation and dependent dropdowns.
→ See `references/linked-fields.md`

### Reactivity & Performance
useStore selectors and granular subscriptions.
→ See `references/reactivity.md`

### Reset API
Form and field reset with custom values.
→ See `references/reset-api.md`

### SSR & Hydration
TanStack Start integration and server state merge.
→ See `references/ssr-hydration.md`

### Devtools
Debug form state with @tanstack/react-form-devtools.
→ See `references/devtools.md`

### React Native
Mobile-specific patterns with TextInput.
→ See `references/react-native.md`

### Standard Schema
ArkType and Effect Schema support.
→ See `references/standard-schema.md`

---

## Templates

| Template | Use Case |
|----------|----------|
| `templates/basic-form.md` | Login/signup with Zod |
| `templates/multi-step-form.md` | Wizard with step validation |
| `templates/dynamic-fields.md` | Add/remove field arrays |
| `templates/file-upload-form.md` | File input with preview |
| `templates/server-action-form.md` | React 19 Server Actions |
| `templates/optimistic-form.md` | useOptimistic integration |
| `templates/nested-form.md` | Dot notation nested fields |
| `templates/search-form.md` | Debounced search |
| `templates/conditional-fields.md` | Show/hide based on values |
| `templates/form-composition.md` | Reusable field components |
| `templates/listeners-form.md` | Side effects & auto-save |
| `templates/linked-fields-form.md` | Cross-field validation |
| `templates/reactivity-form.md` | Performance optimization |
| `templates/reset-form.md` | Form/field reset patterns |
| `templates/ssr-form.md` | SSR & hydration |
| `templates/devtools-form.md` | Devtools integration |
| `templates/react-native-form.md` | React Native forms |

---

## Best Practices

1. **Validation**: Use Zod/Yup/Valibot, NOT custom regex
2. **Async**: Debounce server validation (300-500ms)
3. **Errors**: Display `field.state.meta.errors`
4. **Nested**: Use dot notation (`address.street`)
5. **Arrays**: Use `mode="array"` with pushValue/removeValue
6. **TypeScript**: Infer types with `z.infer<typeof schema>`

---

## Forbidden (Anti-Patterns)

- ❌ `useState` for form state → use `useForm()`
- ❌ Regex validation → use Zod/Yup/Valibot
- ❌ No debounce on async → use `onChangeAsyncDebounceMs`
- ❌ Validation in components → move to schema
- ❌ Direct `onChange` → use `field.handleChange`
- ❌ No TypeScript types → use `z.infer<typeof schema>`
