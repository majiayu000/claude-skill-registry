---
name: shadcn-components
description: Add or customize shadcn/ui components in the shared UI package. Use when adding new components from shadcn registry or updating existing component variants.
allowed-tools: Read, Edit, Write, Bash, mcp__shadcn__search_items_in_registries, mcp__shadcn__view_items_in_registries, mcp__shadcn__get_add_command_for_items
---

# shadcn/ui Components Skill

This skill helps you work with shadcn/ui components in `packages/ui/`.

## When to Use This Skill

- Adding new shadcn/ui components to the shared UI library
- Customizing existing shadcn/ui component variants
- Updating component styling with Tailwind
- Finding and implementing component examples
- Debugging shadcn/ui component issues
- Managing component dependencies

## shadcn/ui Overview

shadcn/ui is a collection of re-usable components built with Radix UI and Tailwind CSS. Components are copied into your codebase, giving you full control.

```
packages/ui/
├── src/
│   ├── components/     # shadcn/ui components
│   │   ├── badge.tsx
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── lib/
│   │   └── utils.ts    # cn() utility for class merging
│   └── styles/
│       └── globals.css # Global styles
├── components.json     # shadcn/ui configuration
└── package.json
```

## Discovery and Research

### Search for Components

```typescript
// Use MCP tool to search for components
mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "button"
})

mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "form input"
})
```

### View Component Details

```typescript
// Get component implementation details
mcp__shadcn__view_items_in_registries({
  items: ["@shadcn/button", "@shadcn/card"]
})
```

### Get Component Examples

```typescript
// Find usage examples
mcp__shadcn__get_item_examples_from_registries({
  registries: ["@shadcn"],
  query: "button demo"
})

mcp__shadcn__get_item_examples_from_registries({
  registries: ["@shadcn"],
  query: "form example"
})
```

### Get Add Command

```typescript
// Get CLI command to add components
mcp__shadcn__get_add_command_for_items({
  items: ["@shadcn/button", "@shadcn/dialog"]
})
```

## Adding New Components

### Step 1: Search and Research

```bash
# Use MCP tools to find the component
# Example: Adding a dropdown menu component
```

```typescript
mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "dropdown menu"
})
```

### Step 2: Get Add Command

```typescript
mcp__shadcn__get_add_command_for_items({
  items: ["@shadcn/dropdown-menu"]
})

// Returns: npx shadcn@latest add dropdown-menu
```

### Step 3: Add Component

```bash
# Navigate to packages/ui
cd packages/ui

# Add component using CLI
npx shadcn@latest add dropdown-menu

# Or add multiple components at once
npx shadcn@latest add dropdown-menu select tabs
```

### Step 4: Export Component

Update `packages/ui/src/index.ts`:

```typescript
export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuRadioGroup,
} from "./components/dropdown-menu";
```

### Step 5: Use in App

```typescript
// In apps/web or apps/api
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@sgcarstrends/ui";

export function UserMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger>Open</DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem>Profile</DropdownMenuItem>
        <DropdownMenuItem>Settings</DropdownMenuItem>
        <DropdownMenuItem>Logout</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

## Core Components

### Button Component

```typescript
// packages/ui/src/components/button.tsx
import { Button } from "@sgcarstrends/ui";

// Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon">Icon</Button>
```

### Card Component

```typescript
import {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
} from "@sgcarstrends/ui";

export function InfoCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card description goes here</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Card content</p>
      </CardContent>
      <CardFooter>
        <p>Card footer</p>
      </CardFooter>
    </Card>
  );
}
```

### Dialog Component

```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@sgcarstrends/ui";

export function ConfirmDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <div className="flex justify-end gap-2">
          <Button variant="outline">Cancel</Button>
          <Button>Confirm</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

### Form Components

```typescript
import { Label } from "@sgcarstrends/ui";
import { Input } from "@sgcarstrends/ui";
import { Textarea } from "@sgcarstrends/ui";

export function ContactForm() {
  return (
    <form className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input id="name" placeholder="Enter your name" />
      </div>

      <div className="space-y-2">
        <Label htmlFor="message">Message</Label>
        <Textarea id="message" placeholder="Enter your message" />
      </div>

      <Button type="submit">Submit</Button>
    </form>
  );
}
```

### Badge Component

```typescript
import { Badge } from "@sgcarstrends/ui";

export function StatusBadge({ status }: { status: string }) {
  return (
    <>
      <Badge variant="default">Default</Badge>
      <Badge variant="secondary">Secondary</Badge>
      <Badge variant="destructive">Destructive</Badge>
      <Badge variant="outline">Outline</Badge>
    </>
  );
}
```

## Customization

### Customizing Component Variants

Edit component file directly:

```typescript
// packages/ui/src/components/button.tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // Add custom variant
        success: "bg-green-500 text-white hover:bg-green-600",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
        // Add custom size
        xl: "h-14 rounded-md px-10 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);
```

### Creating Compound Components

```typescript
// packages/ui/src/components/stat-card.tsx
import { Card, CardHeader, CardTitle, CardContent } from "./card";
import { cn } from "../lib/utils";

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  trend?: "up" | "down";
  className?: string;
}

export function StatCard({
  title,
  value,
  description,
  trend,
  className,
}: StatCardProps) {
  return (
    <Card className={cn("", className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {trend && (
          <span
            className={cn(
              "text-xs",
              trend === "up" ? "text-green-500" : "text-red-500"
            )}
          >
            {trend === "up" ? "↑" : "↓"}
          </span>
        )}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
      </CardContent>
    </Card>
  );
}
```

Export in `packages/ui/src/index.ts`:

```typescript
export { StatCard } from "./components/stat-card";
```

## Theming

### Customizing Colors

Edit `packages/ui/src/styles/globals.css`:

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

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;

    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}
```

## Component Configuration

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/styles/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

## Utility Functions

### cn() Utility

```typescript
// packages/ui/src/lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Usage:

```typescript
import { cn } from "@sgcarstrends/ui/lib/utils";

export function MyComponent({ className }: { className?: string }) {
  return (
    <div className={cn("base-classes", "conditional-classes", className)}>
      Content
    </div>
  );
}
```

## Testing Components

```typescript
// packages/ui/src/components/__tests__/button.test.tsx
import { render, screen } from "@testing-library/react";
import { Button } from "../button";

describe("Button", () => {
  it("renders correctly", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  it("applies variant styles", () => {
    render(<Button variant="destructive">Delete</Button>);
    const button = screen.getByText("Delete");
    expect(button).toHaveClass("bg-destructive");
  });

  it("handles click events", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    screen.getByText("Click me").click();
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

Run tests:

```bash
pnpm -F @sgcarstrends/ui test
```

## Common Patterns

### Responsive Components

```typescript
import { Button } from "@sgcarstrends/ui";

export function ResponsiveButton() {
  return (
    <Button className="w-full md:w-auto">
      Responsive Button
    </Button>
  );
}
```

### Composition

```typescript
import { Card, CardHeader, CardTitle, CardContent } from "@sgcarstrends/ui";
import { Button } from "@sgcarstrends/ui";

export function ActionCard({ title, children, onAction }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {children}
        <Button onClick={onAction} className="w-full">
          Take Action
        </Button>
      </CardContent>
    </Card>
  );
}
```

## Troubleshooting

### Component Not Found

**Problem:** Import error when using component
**Solution:**
1. Check component is exported in `packages/ui/src/index.ts`
2. Verify component file exists in `packages/ui/src/components/`
3. Run `pnpm install` to update dependencies

### Styling Issues

**Problem:** Tailwind classes not applying
**Solution:**
1. Check `packages/ui/tailwind.config.ts` includes correct content paths
2. Verify CSS variables are defined in `globals.css`
3. Ensure parent app imports UI package's global CSS

### TypeScript Errors

**Problem:** Type errors when using components
**Solution:**
1. Check component props are properly typed
2. Run `pnpm build` in packages/ui
3. Restart TypeScript server in IDE

## Updating Components

When shadcn/ui updates:

```bash
cd packages/ui

# Update specific component
npx shadcn@latest add button --overwrite

# Update multiple components
npx shadcn@latest add button card dialog --overwrite
```

## References

- shadcn/ui Documentation: https://ui.shadcn.com
- Radix UI: https://www.radix-ui.com
- Related files:
  - `packages/ui/src/components/` - All UI components
  - `packages/ui/components.json` - shadcn/ui config
  - `packages/ui/CLAUDE.md` - UI package documentation

## Best Practices

1. **Use MCP Tools**: Search before adding to avoid duplicates
2. **Export Components**: Always export in index.ts
3. **Naming**: Follow shadcn/ui naming conventions
4. **Testing**: Write tests for custom variants
5. **Documentation**: Document custom components
6. **Versioning**: Keep shadcn/ui components updated
7. **Customization**: Extend, don't modify core components
8. **Type Safety**: Leverage TypeScript for props
9. **Size Utility**: Use `size-*` instead of `h-* w-*` for equal dimensions (Tailwind v3.4+)

### Size Utility Convention

When styling shadcn/ui components with equal height and width, use the `size-*` utility:

```tsx
// ✅ Good - Use size-* for equal dimensions
<Button size="icon" className="size-10">
  <Icon className="size-4" />
</Button>

<Avatar className="size-8">
  <AvatarImage src={imageUrl} />
</Avatar>

// ❌ Avoid - Redundant h-* and w-*
<Button size="icon" className="h-10 w-10">
  <Icon className="h-4 w-4" />
</Button>

<Avatar className="h-8 w-8">
  <AvatarImage src={imageUrl} />
</Avatar>
```
