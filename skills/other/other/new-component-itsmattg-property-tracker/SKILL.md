---
name: new-component
description: Create a React component following project conventions — imports, types, cn(), tRPC patterns
disable-model-invocation: true
---

# New Component Runbook

## Conventions

See `src/components/CLAUDE.md` for full patterns. Key points:

### Import Order
```tsx
"use client";                                    // 1. Directive (only if needed)
import { useState } from "react";                // 2. React
import Link from "next/link";                    // 3. Next.js
import { Plus } from "lucide-react";             // 4. Third-party
import { Button } from "@/components/ui/button"; // 5. Internal UI
import { MyCard } from "@/components/my/MyCard";  // 6. Internal app
import { trpc } from "@/lib/trpc/client";        // 7. Internal lib
import { MyHelper } from "./MyHelper";            // 8. Relative
```

### Type Patterns
- UI components: inline types `React.ComponentProps<"div">`
- App components: file-local `interface` (NOT exported)
- Never export prop interfaces
- Use `z.infer<typeof schema>` for form types

### Styling
- Use `cn()` for conditional classes: `cn("base", conditional && "extra", className)`
- Tailwind v4 — CSS variables for colors: `var(--color-primary)`
- No hardcoded hex colors

### Icons
- `import { Plus } from "lucide-react"` (named imports only)
- `<Plus className="w-4 h-4" />` (Tailwind classes, not `size` prop)

### tRPC Data Fetching
```tsx
const { data, isLoading } = trpc.<domain>.<method>.useQuery({ ... });
const utils = trpc.useUtils();
const mutation = trpc.<domain>.<method>.useMutation({
  onSuccess: () => utils.<domain>.list.invalidate(),
});
```

### "use client" Directive
Only add when the component needs hooks or interactivity. Server components by default.

## Checklist

- [ ] Import order follows convention
- [ ] Types are file-local (not exported)
- [ ] `cn()` used for class merging
- [ ] Icons use named imports + Tailwind sizing
- [ ] `"use client"` only if hooks/interactivity needed
- [ ] No anti-patterns from `.claude/rules/anti-patterns.md`
