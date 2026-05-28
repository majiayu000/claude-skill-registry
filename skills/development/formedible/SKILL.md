---
name: formedible
description: Expert knowledge for Formedible - A React form library built on TanStack Form with 22+ field types, multi-page forms, analytics, and type-safe validation
---

# Formedible Skill

Use this skill when working with Formedible forms - creating, debugging, or extending functionality.

## Quick Start

```tsx
import { useFormedible } from "@/hooks/use-formedible";
import { z } from "zod";
import { toast } from "sonner";

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

const { Form } = useFormedible({
  schema,
  fields: [
    { name: "name", type: "text", label: "Name" },
    { name: "email", type: "email", label: "Email" },
  ],
  formOptions: {
    defaultValues: { name: "", email: "" },
    onSubmit: async ({ value }) => {
      toast.success("Form submitted!");
      console.log(value);
    },
  },
});

return <Form className="space-y-4" />;
```

## Field Types Quick Reference

| Type | Key Config |
|------|------------|
| `text` | Basic text input |
| `email` | Email validation |
| `password` | Password field |
| `textarea` | `textareaConfig: { rows, showWordCount, maxLength }` |
| `number` | `min, max, step` |
| `date` | `dateConfig: { disablePastDates, disableFutureDates }` |
| `select` | `options: []` (static or function) |
| `radio` | `options: []` |
| `multiSelect` | `multiSelectConfig: { maxSelections, searchable }` |
| `checkbox` | Boolean checkbox |
| `switch` | Toggle switch |
| `rating` | `ratingConfig: { max, allowHalf, icon }` |
| `phone` | `phoneConfig: { format, defaultCountry }` |
| `array` | `arrayConfig: { itemType, minItems, maxItems, sortable, objectConfig }` |

## Key Examples (Self-Contained)

### Multi-Page Form with Dynamic Text

```tsx
import { useFormedible } from "@/hooks/use-formedible";
import { z } from "zod";
import { toast } from "sonner";

const schema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  email: z.string().email(),
  plan: z.enum(["basic", "pro"]),
});

const { Form } = useFormedible({
  schema,
  fields: [
    { name: "firstName", type: "text", label: "First Name", page: 1 },
    { name: "lastName", type: "text", label: "Last Name", page: 1 },
    {
      name: "email",
      type: "email",
      label: "Email",
      page: 2,
      description: "We'll contact {{firstName}} at {{email}}", // Dynamic text!
    },
    {
      name: "plan",
      type: "radio",
      label: "Plan",
      page: 2,
      options: [
        { value: "basic", label: "Basic - Free" },
        { value: "pro", label: "Pro - $9/mo" },
      ],
    },
  ],
  pages: [
    { page: 1, title: "Personal Info", description: "Tell us about yourself" },
    { page: 2, title: "Contact", description: "How can we reach you, {{firstName}}?" },
  ],
  progress: { showSteps: true, showPercentage: true },
  formOptions: {
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      plan: "basic" as const,
    },
    onSubmit: async ({ value }) => {
      toast.success("Registered!");
    },
  },
});

return <Form className="space-y-4" />;
```

### Conditional Fields AND Pages

```tsx
const schema = z.object({
  applicationType: z.enum(["individual", "business"]),
  firstName: z.string().optional(),
  companyName: z.string().optional(),
});

const { Form } = useFormedible({
  schema,
  fields: [
    {
      name: "applicationType",
      type: "radio",
      label: "Application Type",
      page: 1,
      options: [
        { value: "individual", label: "Individual" },
        { value: "business", label: "Business" },
      ],
    },
    {
      name: "firstName",
      type: "text",
      label: "First Name",
      page: 2,
      conditional: (values: any) => values.applicationType === "individual",
    },
    {
      name: "companyName",
      type: "text",
      label: "Company Name",
      page: 3,
      conditional: (values: any) => values.applicationType === "business",
    },
  ],
  pages: [
    { page: 1, title: "Type" },
    {
      page: 2,
      title: "Personal Info",
      conditional: (values: any) => values.applicationType === "individual",
    },
    {
      page: 3,
      title: "Business Info",
      conditional: (values: any) => values.applicationType === "business",
    },
  ],
  formOptions: {
    defaultValues: {
      applicationType: "individual" as const,
      firstName: "",
      companyName: "",
    },
    onSubmit: async ({ value }) => {
      console.log(value);
    },
  },
});
```

### Tabbed Form

```tsx
const schema = z.object({
  firstName: z.string(),
  theme: z.enum(["light", "dark"]),
  notifications: z.boolean(),
});

const { Form } = useFormedible({
  schema,
  fields: [
    { name: "firstName", type: "text", label: "Name", tab: "personal" },
    {
      name: "theme",
      type: "select",
      label: "Theme",
      tab: "preferences",
      options: [
        { value: "light", label: "Light" },
        { value: "dark", label: "Dark" },
      ],
    },
    {
      name: "notifications",
      type: "switch",
      label: "Enable Notifications",
      tab: "preferences",
    },
  ],
  tabs: [
    { id: "personal", label: "Personal Info", description: "About you" },
    { id: "preferences", label: "Preferences", description: "Settings" },
  ],
  formOptions: {
    defaultValues: {
      firstName: "",
      theme: "light" as const,
      notifications: true,
    },
    onSubmit: async ({ value }) => console.log(value),
  },
});
```

### Dynamic Options (Dependent Fields)

```tsx
const schema = z.object({
  country: z.string(),
  state: z.string(),
});

const { Form } = useFormedible({
  schema,
  fields: [
    {
      name: "country",
      type: "select",
      label: "Country",
      options: [
        { value: "us", label: "United States" },
        { value: "ca", label: "Canada" },
      ],
    },
    {
      name: "state",
      type: "select",
      label: "State/Province",
      options: (values: any) => {
        if (values.country === "us") {
          return [
            { value: "ca", label: "California" },
            { value: "ny", label: "New York" },
          ];
        }
        if (values.country === "ca") {
          return [
            { value: "on", label: "Ontario" },
            { value: "qc", label: "Quebec" },
          ];
        }
        return [];
      },
    },
  ],
  formOptions: {
    defaultValues: { country: "", state: "" },
    onSubmit: async ({ value }) => console.log(value),
  },
});
```

### Array Fields with Nested Objects

```tsx
const schema = z.object({
  teamMembers: z.array(
    z.object({
      name: z.string().min(1),
      email: z.string().email(),
      role: z.enum(["dev", "design", "pm"]),
    })
  ).min(1),
});

const { Form } = useFormedible({
  schema,
  fields: [
    {
      name: "teamMembers",
      type: "array",
      label: "Team Members",
      section: {
        title: "Team Composition",
        description: "Add your team",
      },
      arrayConfig: {
        itemType: "object",
        itemLabel: "Team Member",
        minItems: 1,
        maxItems: 10,
        sortable: true,
        addButtonLabel: "Add Member",
        defaultValue: {
          name: "",
          email: "",
          role: "dev",
        },
        objectConfig: {
          fields: [
            { name: "name", type: "text", label: "Name" },
            { name: "email", type: "email", label: "Email" },
            {
              name: "role",
              type: "select",
              label: "Role",
              options: [
                { value: "dev", label: "Developer" },
                { value: "design", label: "Designer" },
                { value: "pm", label: "Product Manager" },
              ],
            },
          ],
        },
      },
    },
  ],
  formOptions: {
    defaultValues: {
      teamMembers: [{ name: "", email: "", role: "dev" as const }],
    },
    onSubmit: async ({ value }) => console.log(value),
  },
});
```

### Analytics with Proper Memoization

```tsx
import React from "react";

const schema = z.object({
  email: z.string().email(),
});

// MUST use useCallback for analytics callbacks!
const onFieldFocus = React.useCallback((fieldName: string, timestamp: number) => {
  console.log(`Field "${fieldName}" focused at`, timestamp);
}, []);

const onFieldBlur = React.useCallback((fieldName: string, timeSpent: number) => {
  console.log(`Field "${fieldName}" completed in ${timeSpent}ms`);
}, []);

const onFormComplete = React.useCallback((timeSpent: number, data: any) => {
  console.log(`Form completed in ${timeSpent}ms`, data);
  toast.success("Form completed!");
}, []);

// MUST useMemo the analytics config
const analyticsConfig = React.useMemo(
  () => ({
    onFieldFocus,
    onFieldBlur,
    onFormComplete,
  }),
  [onFieldFocus, onFieldBlur, onFormComplete]
);

const { Form } = useFormedible({
  schema,
  fields: [
    { name: "email", type: "email", label: "Email" },
  ],
  analytics: analyticsConfig,
  formOptions: {
    defaultValues: { email: "" },
    onSubmit: async ({ value }) => console.log(value),
  },
});
```

### Rating Field with Config

```tsx
const schema = z.object({
  satisfaction: z.number().min(1).max(5),
  improvements: z.string().optional(),
});

const { Form } = useFormedible({
  schema,
  fields: [
    {
      name: "satisfaction",
      type: "rating",
      label: "How satisfied are you?",
      ratingConfig: {
        max: 5,
        allowHalf: false,
        showValue: true,
      },
    },
    {
      name: "improvements",
      type: "textarea",
      label: "What can we improve?",
      conditional: (values: any) => values.satisfaction < 4,
      textareaConfig: {
        rows: 4,
        showWordCount: true,
        maxLength: 500,
      },
    },
  ],
  formOptions: {
    defaultValues: { satisfaction: 5, improvements: "" },
    onSubmit: async ({ value }) => console.log(value),
  },
});
```

### Textarea with Configuration

```tsx
const schema = z.object({
  description: z.string().min(20).max(500),
});

const { Form } = useFormedible({
  schema,
  fields: [
    {
      name: "description",
      type: "textarea",
      label: "Description",
      textareaConfig: {
        rows: 4,
        showWordCount: true,
        maxLength: 500,
      },
    },
  ],
  formOptions: {
    defaultValues: { description: "" },
    onSubmit: async ({ value }) => console.log(value),
  },
});
```

## Critical Patterns

### 1. Always Use className on Form

```tsx
<Form className="space-y-4" />
```

### 2. Toast Notifications

```tsx
import { toast } from "sonner";

onSubmit: async ({ value }) => {
  toast.success("Success!", {
    description: "Your data was saved",
  });
}
```

### 3. Use `as const` for Enums

```tsx
defaultValues: {
  plan: "basic" as const,  // ✅
  role: "admin" as const,  // ✅
}
```

### 4. Dynamic Options = Function

```tsx
// ❌ Wrong
options: [{ value: "a", label: "A" }]

// ✅ Correct
options: (values) => {
  if (values.category === "tech") return techOptions;
  return [];
}
```

### 5. Conditional Returns Boolean

```tsx
// ❌ Wrong
conditional: (values) => {
  if (values.type === "business") return true;
}

// ✅ Correct
conditional: (values) => values.type === "business"
```

### 6. Analytics Must Be Memoized

```tsx
const callback = React.useCallback((...) => { ... }, []);
const analytics = React.useMemo(() => ({ callback }), [callback]);
```

## Build Workflow (CRITICAL!)

**PACKAGES ARE SOURCE OF TRUTH**

1. Edit: `packages/formedible/src/...`
2. Build: `npm run build:pkg`
3. Sync: `node scripts/quick-sync.js`
4. Build web: `npm run build:web`
5. Sync components: `npm run sync-components`
6. Build web: `npm run build:web`

**NEVER edit web app files directly!**

## Common Issues

| Issue | Fix |
|-------|-----|
| Field not showing | Check field type in `field-registry.tsx` |
| Dynamic options not updating | Use function: `options: (values) => {...}` |
| Validation not showing | Schema names must match field names exactly |
| Conditional always hidden | Return boolean, never undefined |
| Analytics not firing | Use `React.useCallback` + `React.useMemo` |
| Pages not working | Pages start at 1, must be sequential |

## Type Safety

```tsx
const schema = z.object({
  name: z.string(),
  age: z.number(),
});

type FormValues = z.infer<typeof schema>;

const { Form } = useFormedible<FormValues>({
  schema,
  formOptions: {
    defaultValues: {
      name: "",  // Type-safe
      age: 0,    // Type-safe
    },
  },
});
```

## File Structure Reference

```
packages/formedible/src/
├── hooks/use-formedible.tsx          # Main hook
├── components/formedible/
│   ├── fields/                       # All 22 field components
│   ├── layout/                       # FormGrid, FormTabs, etc.
│   └── ui/                           # Radix UI primitives
├── lib/formedible/
│   ├── types.ts                      # TypeScript interfaces
│   ├── field-registry.tsx            # Field type mapping
│   └── template-interpolation.ts     # Dynamic text resolution
```

## Adding New Field Types

1. Create: `packages/formedible/src/components/formedible/fields/my-field.tsx`
2. Use `BaseFieldWrapper` for consistency
3. Add type to `packages/formedible/src/lib/formedible/types.ts`
4. Register in `packages/formedible/src/lib/formedible/field-registry.tsx`
5. Add to `packages/formedible/registry.json`

See [FIELD_TEMPLATES.md](references/FIELD_TEMPLATES.md) for templates.
