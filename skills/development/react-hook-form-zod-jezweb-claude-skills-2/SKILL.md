---
name: react-hook-form-zod
description: |
  Build type-safe validated forms using React Hook Form v7 and Zod v4. Single schema works on client and server with full TypeScript inference via z.infer.

  Use when building forms, multi-step wizards, or fixing uncontrolled warnings, resolver errors, useFieldArray issues, performance problems with large forms.
user-invocable: true
---

# React Hook Form + Zod Validation

**Status**: Production Ready ✅
**Last Verified**: 2026-01-20
**Latest Versions**: react-hook-form@7.71.1, zod@4.3.5, @hookform/resolvers@5.2.2

---

## Quick Start

```bash
npm install react-hook-form@7.70.0 zod@4.3.5 @hookform/resolvers@5.2.2
```

**Basic Form Pattern**:
```typescript
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormData = z.infer<typeof schema>

const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { email: '', password: '' }, // REQUIRED to prevent uncontrolled warnings
})

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register('email')} />
  {errors.email && <span role="alert">{errors.email.message}</span>}
</form>
```

**Server Validation** (CRITICAL - never skip):
```typescript
// SAME schema on server
const data = schema.parse(await req.json())
```

---

## Key Patterns

**useForm Options** (validation modes):
- `mode: 'onSubmit'` (default) - Best performance
- `mode: 'onBlur'` - Good balance
- `mode: 'onChange'` - Live feedback, more re-renders
- `shouldUnregister: true` - Remove field data when unmounted (use for multi-step forms)

**Zod Refinements** (cross-field validation):
```typescript
z.object({ password: z.string(), confirm: z.string() })
  .refine((data) => data.password === data.confirm, {
    message: "Passwords don't match",
    path: ['confirm'], // CRITICAL: Error appears on this field
  })
```

**Zod Transforms**:
```typescript
z.string().transform((val) => val.toLowerCase()) // Data manipulation
z.string().transform(parseInt).refine((v) => v > 0) // Chain with refine
```

**Zod v4.3.0+ Features**:
```typescript
// Exact optional (can omit field, but NOT undefined)
z.string().exactOptional()

// Exclusive union (exactly one must match)
z.xor([z.string(), z.number()])

// Import from JSON Schema
z.fromJSONSchema({ type: "object", properties: { name: { type: "string" } } })
```

**zodResolver** connects Zod to React Hook Form, preserving type safety

---

## Registration

**register** (for standard HTML inputs):
```typescript
<input {...register('email')} /> // Uncontrolled, best performance
```

**Controller** (for third-party components):
```typescript
<Controller
  name="category"
  control={control}
  render={({ field }) => <CustomSelect {...field} />} // MUST spread {...field}
/>
```

**When to use Controller**: React Select, date pickers, custom components without ref. Otherwise use `register`.

---

## Error Handling

**Display errors**:
```typescript
{errors.email && <span role="alert">{errors.email.message}</span>}
{errors.address?.street?.message} // Nested errors (use optional chaining)
```

**Server errors**:
```typescript
const onSubmit = async (data) => {
  const res = await fetch('/api/submit', { method: 'POST', body: JSON.stringify(data) })
  if (!res.ok) {
    const { errors: serverErrors } = await res.json()
    Object.entries(serverErrors).forEach(([field, msg]) => setError(field, { message: msg }))
  }
}
```

---

## Advanced Patterns

**useFieldArray** (dynamic lists):
```typescript
const { fields, append, remove } = useFieldArray({ control, name: 'contacts' })

{fields.map((field, index) => (
  <div key={field.id}> {/* CRITICAL: Use field.id, NOT index */}
    <input {...register(`contacts.${index}.name` as const)} />
    {errors.contacts?.[index]?.name && <span>{errors.contacts[index].name.message}</span>}
    <button onClick={() => remove(index)}>Remove</button>
  </div>
))}
<button onClick={() => append({ name: '', email: '' })}>Add</button>
```

**Async Validation** (debounce):
```typescript
const debouncedValidation = useDebouncedCallback(() => trigger('username'), 500)
```

**Multi-Step Forms**:
```typescript
const step1 = z.object({ name: z.string(), email: z.string().email() })
const step2 = z.object({ address: z.string() })
const fullSchema = step1.merge(step2)

const nextStep = async () => {
  const isValid = await trigger(['name', 'email']) // Validate specific fields
  if (isValid) setStep(2)
}
```

**Conditional Validation**:
```typescript
z.discriminatedUnion('accountType', [
  z.object({ accountType: z.literal('personal'), name: z.string() }),
  z.object({ accountType: z.literal('business'), companyName: z.string() }),
])
```

**Conditional Fields with shouldUnregister**:
```typescript
const form = useForm({
  resolver: zodResolver(schema),
  shouldUnregister: false, // Keep values when fields unmount (default)
})

// Or use conditional schema validation:
z.object({
  showAddress: z.boolean(),
  address: z.string(),
}).refine((data) => {
  if (data.showAddress) {
    return data.address.length > 0;
  }
  return true;
}, {
  message: "Address is required",
  path: ["address"],
})
```

---

## shadcn/ui Integration

**Note**: shadcn/ui deprecated the Form component. Use the Field component for new implementations (check latest docs).

**Common Import Mistake**: IDEs/AI may auto-import `Form` from "react-hook-form" instead of from shadcn. Always import:
```typescript
// ✅ Correct:
import { useForm } from "react-hook-form";
import { Form, FormField, FormItem } from "@/components/ui/form"; // shadcn

// ❌ Wrong (auto-import mistake):
import { useForm, Form } from "react-hook-form";
```

**Legacy Form component**:
```typescript
<FormField control={form.control} name="username" render={({ field }) => (
  <FormItem>
    <FormControl><Input {...field} /></FormControl>
    <FormMessage />
  </FormItem>
)} />
```

---

## Performance

- Use `register` (uncontrolled) over `Controller` (controlled) for standard inputs
- Use `watch('email')` not `watch()` (isolates re-renders to specific fields)
- `shouldUnregister: true` for multi-step forms (clears data on unmount)

### Large Forms (300+ Fields)

**Warning**: Forms with 300+ fields using a resolver (Zod/Yup) AND reading `formState` properties can freeze for 10-15 seconds during registration. ([Issue #13129](https://github.com/react-hook-form/react-hook-form/issues/13129))

**Performance Characteristics**:
- Clean (no resolver, no formState read): Almost immediate
- With resolver only: Almost immediate
- With formState read only: Almost immediate
- With BOTH resolver + formState read: ~9.5 seconds for 300 fields

**Workarounds**:

1. **Avoid destructuring formState** - Read properties inline only when needed:
```typescript
// ❌ Slow with 300+ fields:
const { isDirty, isValid } = form.formState;

// ✅ Fast:
const handleSubmit = () => {
  if (!form.formState.isValid) return; // Read inline only when needed
};
```

2. **Use mode: "onSubmit"** - Don't validate on every change:
```typescript
const form = useForm({
  resolver: zodResolver(largeSchema),
  mode: "onSubmit", // Validate only on submit, not onChange
});
```

3. **Split into sub-forms** - Multiple smaller forms with separate schemas:
```typescript
// Instead of one 300-field form, use 5-6 forms with 50-60 fields each
const form1 = useForm({ resolver: zodResolver(schema1) }); // Fields 1-50
const form2 = useForm({ resolver: zodResolver(schema2) }); // Fields 51-100
```

4. **Lazy render fields** - Use tabs/accordion to mount only visible fields:
```typescript
// Only mount fields for active tab, reduces initial registration time
{activeTab === 'personal' && <PersonalInfoFields />}
{activeTab === 'address' && <AddressFields />}
```

---

## Critical Rules

✅ **Always set defaultValues** (prevents uncontrolled→controlled warnings)

✅ **Validate on BOTH client and server** (client can be bypassed - security!)

✅ **Use `field.id` as key** in useFieldArray (not index)

✅ **Spread `{...field}`** in Controller render

✅ **Use `z.infer<typeof schema>`** for type inference

❌ **Never skip server validation** (security vulnerability)

❌ **Never mutate values directly** (use `setValue()`)

❌ **Never mix controlled + uncontrolled** patterns

❌ **Never use index as key** in useFieldArray

---

## Known Issues (20 Prevented)

1. **Zod v4 Type Inference** - [#13109](https://github.com/react-hook-form/react-hook-form/issues/13109): Use `z.infer<typeof schema>` explicitly. Resolved in v7.66.x+. **Note**: @hookform/resolvers has TypeScript compatibility issues with Zod v4 ([#813](https://github.com/react-hook-form/resolvers/issues/813)). Workaround: Use `import { z } from 'zod/v3'` or wait for resolver update.

2. **Uncontrolled→Controlled Warning** - Always set `defaultValues` for all fields

3. **Nested Object Errors** - Use optional chaining: `errors.address?.street?.message`

4. **Array Field Re-renders** - Use `key={field.id}` in useFieldArray (not index)

5. **Async Validation Race Conditions** - Debounce validation, cancel pending requests

6. **Server Error Mapping** - Use `setError()` to map server errors to fields

7. **Default Values Not Applied** - Set `defaultValues` in useForm options (not useState)

8. **Controller Field Not Updating** - Always spread `{...field}` in render function

9. **useFieldArray Key Warnings** - Use `field.id` as key (not index)

10. **Schema Refinement Error Paths** - Specify `path` in refinement: `refine(..., { path: ['fieldName'] })`

11. **Transform vs Preprocess** - Use `transform` for output, `preprocess` for input

12. **Multiple Resolver Conflicts** - Use single resolver (zodResolver), combine schemas if needed

13. **Zod v4 Optional Fields Bug** - [#13102](https://github.com/react-hook-form/react-hook-form/issues/13102): Setting optional fields (`.optional()`) to empty string `""` incorrectly triggers validation errors. Workarounds: Use `.nullish()`, `.or(z.literal(""))`, or `z.preprocess((val) => val === "" ? undefined : val, z.email().optional())`

14. **useFieldArray Primitive Arrays Not Supported** - [#12570](https://github.com/react-hook-form/react-hook-form/issues/12570): Design limitation. `useFieldArray` only works with arrays of objects, not primitives like `string[]`. Workaround: Wrap primitives in objects: `[{ value: "string" }]` instead of `["string"]`

15. **useFieldArray SSR ID Mismatch** - [#12782](https://github.com/react-hook-form/react-hook-form/issues/12782): Hydration mismatch warnings with SSR (Remix, Next.js). Field IDs generated on server don't match client. Workaround: Use client-only rendering for field arrays or wait for V8 (uses deterministic `key`)

16. **Next.js 16 reset() Validation Bug** - [#13110](https://github.com/react-hook-form/react-hook-form/issues/13110): Calling `form.reset()` after Server Actions submission causes validation errors on next submit. Fixed in v7.65.0+. Before fix: Use `setValue()` instead of `reset()`

17. **Validation Race Condition** - [#13156](https://github.com/react-hook-form/react-hook-form/issues/13156): During resolver validation, intermediate render where `isValidating=false` but `errors` not populated yet. Don't derive validity from errors alone. Use: `!errors.field && !isValidating`

18. **ZodError Thrown in Beta Versions** - [#12816](https://github.com/react-hook-form/react-hook-form/issues/12816): Zod v4 beta versions throw `ZodError` directly instead of capturing in `formState.errors`. Fixed in stable Zod v4.1.x+. Avoid beta versions

19. **Large Form Performance** - [#13129](https://github.com/react-hook-form/react-hook-form/issues/13129): 300+ fields with resolver + formState read freezes for 10-15 seconds. See Performance section for 4 workarounds

20. **shadcn Form Import Confusion** - IDEs/AI may auto-import `Form` from "react-hook-form" instead of shadcn. Always import `Form` components from `@/components/ui/form`

---

## Upcoming Changes in V8 (Beta)

React Hook Form v8 (currently in beta as of v8.0.0-beta.1, released 2026-01-11) introduces breaking changes. [RFC Discussion #7433](https://github.com/orgs/react-hook-form/discussions/7433)

**Breaking Changes**:

1. **useFieldArray: `id` → `key`**:
```typescript
// V7:
const { fields } = useFieldArray({ control, name: "items" });
fields.map(field => <div key={field.id}>...</div>)

// V8:
const { fields } = useFieldArray({ control, name: "items" });
fields.map(field => <div key={field.key}>...</div>)
// keyName prop removed
```

2. **Watch component: `names` → `name`**:
```typescript
// V7:
<Watch names={["email", "password"]} />

// V8:
<Watch name={["email", "password"]} />
```

3. **watch() callback API removed**:
```typescript
// V7:
watch((data, { name, type }) => {
  console.log(data, name, type);
});

// V8: Use useWatch or manual subscription
const data = useWatch({ control });
useEffect(() => {
  console.log(data);
}, [data]);
```

4. **setValue() no longer updates useFieldArray**:
```typescript
// V7:
setValue("items", newArray); // Updates field array

// V8: Must use replace() API
const { replace } = useFieldArray({ control, name: "items" });
replace(newArray);
```

**V8 Benefits**:
- Fixes SSR hydration mismatch (deterministic `key` instead of random `id`)
- Improved performance
- Better TypeScript inference

**Migration Timeline**: V8 is in beta. Stable release date TBD. Monitor [releases](https://github.com/react-hook-form/react-hook-form/releases) for stable version.

---

## Bundled Resources

**Templates**: basic-form.tsx, advanced-form.tsx, shadcn-form.tsx, server-validation.ts, async-validation.tsx, dynamic-fields.tsx, multi-step-form.tsx, package.json

**References**: zod-schemas-guide.md, rhf-api-reference.md, error-handling.md, performance-optimization.md, shadcn-integration.md, top-errors.md

**Docs**: https://react-hook-form.com/ | https://zod.dev/ | https://ui.shadcn.com/docs/components/form

---

**License**: MIT | **Last Verified**: 2026-01-20 | **Skill Version**: 2.1.0 | **Changes**: Added 8 new known issues (Zod v4 optional fields bug, useFieldArray primitives limitation, SSR hydration mismatch, performance guidance for large forms, Next.js 16 reset() bug, validation race condition, ZodError thrown in beta, shadcn import confusion), added Zod v4.3.0 features (.exactOptional(), .xor(), z.fromJSONSchema()), added conditional field patterns with shouldUnregister, added V8 beta breaking changes section, expanded Zod v4 resolver compatibility notes, updated to react-hook-form@7.71.1
