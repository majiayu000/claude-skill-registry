---
name: frontend-ui
description: >
  Frontend UI-specific patterns. For generic patterns, see: typescript, react-19, nextjs-15, tailwind-4.
  Trigger: When working inside src/react-app.
license: Apache-2.0
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Related Generic Skills

- `typescript` - Const types, flat interfaces
- `react-19` - No useMemo/useCallback, compiler
- `tailwind-4` - cn() utility, styling rules
- `zod-4` - Schema validation
- `zustand-5` - State management
- `motion` - Animations

## CRITICAL: Mobile First

- **ALWAYS**: Use Mobile First approach for responsive design. then desktop styles.

## Tech Stack (Versions)

```
React 19.2.3 | Tailwind 4.1.18 | shadcn/ui
Zod 4.3.5 | React Hook Form 7.71.0 | Zustand 5.0.10" | Recharts 3.6.0 | React Router 7.12.0 | Motion 12.26.2 | TanStack Query 5.90.16 | TanStack Table 8.21.3 |
```

## DECISION TREES

### Component Placement

```
New feature UI? → components/ui + Tailwind
```

### Code Location

```
Types → types/{domain}.ts
Utils → lib/
Hooks → {feature}/hooks.ts
shadcn components  → components/ui/
pages (React Router) → pages/
```

### Styling Decision

```
Tailwind class exists? → className
Dynamic value?         → style prop
Conditional styles?    → cn()
Static only?           → className (no cn())
Recharts/library?      → CHART_COLORS constant + var()
```

## ANIMATIONS

- Use `motion` for all animations.
- Prefer simple animations (opacity, translate, scale).

## PROJECT STRUCTURE

```
react-app/
├── main.tsx/          # React app entry point
├── components/ui/   # Shared UI components (shadcn)
├── pages/          # React Router pages
├── types/               # Shared types
├── hooks/               # Shared hooks
├── lib/                 # Utilities
├── store/               # Zustand state
└── styles/              # Global CSS
```

## Form + Validation Pattern

```typescript
"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.email(),  // Zod 4 syntax
  name: z.string().min(1),
});

type FormData = z.infer<typeof schema>;

export function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await serverAction(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}
```
