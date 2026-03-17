---
name: shadcn
description: Comprehensive shadcn/ui component library with theming, customization patterns, and accessibility. Use when building modern React UIs with Tailwind CSS. IMPORTANT - Always use MCP server tools first when available.
---

# shadcn/ui Skill

Beautiful, accessible components built with Radix UI and Tailwind CSS. Copy and paste into your apps.

## MCP Server Integration (PRIORITY)

**ALWAYS check and use MCP server tools first:**

```
# 1. Check availability
mcp__shadcn__get_project_registries

# 2. Search components
mcp__shadcn__search_items_in_registries
  registries: ["@shadcn"]
  query: "button"

# 3. Get examples
mcp__shadcn__get_item_examples_from_registries
  registries: ["@shadcn"]
  query: "button-demo"

# 4. Get install command
mcp__shadcn__get_add_command_for_items
  items: ["@shadcn/button"]

# 5. Verify implementation
mcp__shadcn__get_audit_checklist
```

## Quick Start

### Installation

```bash
# Initialize shadcn in your project
npx shadcn@latest init

# Add components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
```

### Project Structure

```
src/
├── components/
│   └── ui/           # shadcn components
│       ├── button.tsx
│       ├── card.tsx
│       └── input.tsx
├── lib/
│   └── utils.ts      # cn() utility
└── app/
    └── globals.css   # CSS variables
```

## Key Concepts

| Concept | Guide |
|---------|-------|
| **Theming** | [reference/theming.md](reference/theming.md) |
| **Accessibility** | [reference/accessibility.md](reference/accessibility.md) |
| **Animations** | [reference/animations.md](reference/animations.md) |
| **Components** | [reference/components.md](reference/components.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **Form Patterns** | [examples/form-patterns.md](examples/form-patterns.md) |
| **Data Display** | [examples/data-display.md](examples/data-display.md) |
| **Navigation** | [examples/navigation.md](examples/navigation.md) |
| **Feedback** | [examples/feedback.md](examples/feedback.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/theme-config.ts](templates/theme-config.ts) | Tailwind theme extension |
| [templates/component-scaffold.tsx](templates/component-scaffold.tsx) | Base component with variants |
| [templates/form-template.tsx](templates/form-template.tsx) | Form with validation |

## Component Categories

### Inputs
- Button, Input, Textarea, Select, Checkbox, Radio, Switch, Slider

### Data Display
- Card, Table, Avatar, Badge, Calendar

### Feedback
- Alert, Toast, Dialog, Sheet, Tooltip, Popover

### Navigation
- Tabs, Navigation Menu, Breadcrumb, Pagination

### Layout
- Accordion, Collapsible, Separator, Scroll Area

## Theming System

### CSS Variables

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... */
  }
}
```

### Dark Mode Toggle

```tsx
"use client";

import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { Moon, Sun } from "lucide-react";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

## Utility Function

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Common Patterns

### Form with Validation

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
```

### Toast Notifications

```tsx
import { toast } from "sonner";

// Success
toast.success("Task created successfully");

// Error
toast.error("Something went wrong");

// With action
toast("Event created", {
  action: {
    label: "Undo",
    onClick: () => console.log("Undo"),
  },
});
```

## Accessibility Checklist

- [ ] All interactive elements are keyboard accessible
- [ ] Focus states are visible
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] ARIA labels on icon-only buttons
- [ ] Form inputs have associated labels
- [ ] Error messages are announced to screen readers
- [ ] Dialogs trap focus and return focus on close
- [ ] Reduced motion preferences respected
