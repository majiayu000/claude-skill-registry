# shadcn/ui - Component Library

---
progressive_disclosure:
  entry_point: summary, when_to_use, quick_start
  estimated_tokens:
    entry: 85
    full: 4800
---

## Summary

shadcn/ui is a collection of re-usable React components built with Radix UI primitives and styled with Tailwind CSS. Unlike traditional component libraries, shadcn/ui components are **copied directly into your project**, giving you full ownership and customization control. Components are accessible, customizable, and open source.

**Core Philosophy**: Copy-paste components, not npm packages. You own the code.

## When to Use

**Use shadcn/ui when**:
- Building React applications with Tailwind CSS
- Need accessible, production-ready UI components
- Want full control over component code and styling
- Prefer composition over configuration
- Building with Next.js, Vite, Remix, or Astro
- Need dark mode support out of the box
- Want TypeScript-first components

**Don't use when**:
- Not using Tailwind CSS (core styling dependency)
- Need legacy browser support (uses modern CSS features)
- Prefer packaged npm libraries over code ownership
- Building non-React frameworks (Vue, Svelte, Angular)

## Quick Start

### Installation

```bash
# Initialize shadcn/ui in your project
npx shadcn-ui@latest init

# Follow interactive prompts:
# - TypeScript? (yes/no)
# - Style: Default/New York
# - Base color: Slate/Gray/Zinc/Neutral/Stone
# - CSS variables: (yes/no)
# - React Server Components: (yes/no)
# - components.json location
# - Tailwind config location
# - CSS file location
# - Import alias (@/components)
```

### Add Your First Component

```bash
# Add individual components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog

# Add multiple components at once
npx shadcn-ui@latest add button card dialog form input
```

### Basic Usage

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function Example() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  )
}
```

---

## Architecture

### Copy-Paste Philosophy

**Key Difference from Traditional Libraries**:
- **Traditional**: `npm install component-library` → locked to package versions
- **shadcn/ui**: Components copied to `components/ui/` → you own the code

**Benefits**:
- Full customization control
- No breaking changes from package updates
- Easy to modify for specific needs
- Transparent implementation
- Tree-shakeable by default

### Component Structure

```
src/
├── components/
│   └── ui/
│       ├── button.tsx      # Component implementation
│       ├── card.tsx        # Owns its code
│       ├── dialog.tsx      # Modifiable
│       └── ...
├── lib/
│   └── utils.ts            # cn() helper for class merging
└── app/
    └── globals.css         # Tailwind directives + CSS variables
```

### Technology Stack

**Core Dependencies**:
- **Radix UI**: Accessible component primitives (headless UI)
- **Tailwind CSS**: Utility-first styling
- **TypeScript**: Type safety
- **class-variance-authority (CVA)**: Variant management
- **clsx**: Class name concatenation
- **tailwind-merge**: Conflict-free class merging

**Radix UI Integration**:
```tsx
// shadcn/ui components wrap Radix primitives
import * as DialogPrimitive from "@radix-ui/react-dialog"

// Add styling and variants
const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogContent = React.forwardRef<...>(
  ({ className, children, ...props }, ref) => (
    <DialogPrimitive.Content
      ref={ref}
      className={cn("fixed ...", className)}
      {...props}
    />
  )
)
```

## Configuration

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

**Key Options**:
- `style`: "default" or "new-york" (design variants)
- `rsc`: React Server Components support
- `cssVariables`: Use CSS variables for theming
- `prefix`: Tailwind class prefix (optional)

### Tailwind Configuration

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss"

const config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config
```

### CSS Variables (globals.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

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

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

## Component Catalog

### Button

```tsx
import { Button } from "@/components/ui/button"

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
<Button size="icon"><Icon /></Button>

// States
<Button disabled>Disabled</Button>
<Button asChild>
  <Link href="/about">As Link</Link>
</Button>
```

**Implementation Pattern** (CVA):
```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### Card

```tsx
import {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description goes here</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Dialog (Modal)

```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Form (with react-hook-form + zod)

```tsx
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const formSchema = z.object({
  username: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
  email: z.string().email({
    message: "Please enter a valid email address.",
  }),
})

function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>
                This is your public display name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="user@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### Table

```tsx
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

<Table>
  <TableCaption>A list of your recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Method</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>INV001</TableCell>
      <TableCell>Paid</TableCell>
      <TableCell>Credit Card</TableCell>
      <TableCell className="text-right">$250.00</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Additional Components

**Available via CLI**:
- `accordion` - Collapsible content sections
- `alert` - Contextual feedback messages
- `alert-dialog` - Interrupting modal dialogs
- `avatar` - User profile images
- `badge` - Status indicators
- `calendar` - Date picker
- `checkbox` - Binary input
- `command` - Command palette (⌘K menu)
- `context-menu` - Right-click menus
- `dropdown-menu` - Dropdown menus
- `hover-card` - Hover tooltips
- `input` - Text input
- `label` - Form labels
- `menubar` - Application menu bar
- `navigation-menu` - Site navigation
- `popover` - Floating panels
- `progress` - Progress indicators
- `radio-group` - Radio button groups
- `scroll-area` - Custom scrollbars
- `select` - Dropdown selects
- `separator` - Visual dividers
- `sheet` - Side panels
- `skeleton` - Loading placeholders
- `slider` - Range input
- `switch` - Toggle switch
- `tabs` - Tab navigation
- `textarea` - Multi-line input
- `toast` - Notification toasts
- `toggle` - Toggle button
- `tooltip` - Hover tooltips

## Theming

### Color Customization

**Change base color scheme**:
```bash
# Regenerate components with new base color
npx shadcn-ui@latest init

# Choose new base: Slate, Gray, Zinc, Neutral, Stone
```

**Manual color override** (globals.css):
```css
:root {
  --primary: 210 100% 50%;  /* HSL: Blue */
  --primary-foreground: 0 0% 100%;
}

.dark {
  --primary: 210 100% 60%;  /* Lighter blue for dark mode */
}
```

### Custom Variants

```tsx
// Extend button variants
const buttonVariants = cva(
  "...",
  {
    variants: {
      variant: {
        // ...existing variants
        gradient: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
      },
    },
  }
)

// Usage
<Button variant="gradient">Gradient Button</Button>
```

### Theme Switching

```tsx
// Using next-themes
import { ThemeProvider } from "next-themes"

// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}

// Theme toggle component
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { setTheme, theme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
    >
      <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

## Dark Mode

### Setup with Next.js

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
"use client"

import { ThemeProvider } from "next-themes"

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
}

// app/layout.tsx
import { Providers } from "./providers"

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

### Dark Mode Utilities

```tsx
// Force dark mode for specific section
<div className="dark">
  <Card>Always dark, regardless of theme</Card>
</div>

// Conditional styling
<div className="bg-white dark:bg-slate-950">
  <p className="text-slate-900 dark:text-slate-50">
    Adapts to theme
  </p>
</div>
```

## Next.js Integration

### App Router Setup

```bash
# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest my-app --typescript --tailwind --app

# Initialize shadcn/ui
cd my-app
npx shadcn-ui@latest init

# Add components
npx shadcn-ui@latest add button card form
```

### Server Components

```tsx
// app/page.tsx (Server Component by default)
import { Button } from "@/components/ui/button"

export default function HomePage() {
  return (
    <main>
      <h1>Welcome</h1>
      {/* Static components work in Server Components */}
      <Button asChild>
        <a href="/about">Learn More</a>
      </Button>
    </main>
  )
}
```

### Client Components

```tsx
// app/interactive.tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"

export function InteractiveSection() {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <p>Client-side interactivity</p>
      </DialogContent>
    </Dialog>
  )
}
```

### Route Handlers

```tsx
// app/api/submit/route.ts
import { NextResponse } from "next/server"
import { z } from "zod"

const formSchema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
})

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validatedData = formSchema.parse(body)

    // Process form data
    return NextResponse.json({ success: true })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ errors: error.errors }, { status: 400 })
    }
    return NextResponse.json({ error: "Internal error" }, { status: 500 })
  }
}
```

## Accessibility

### ARIA Support

All shadcn/ui components include proper ARIA attributes via Radix UI:

```tsx
// Dialog automatically includes:
// - role="dialog"
// - aria-describedby
// - aria-labelledby
// - Focus trap
// - Escape key handler
<Dialog>
  <DialogContent>
    {/* Automatically accessible */}
  </DialogContent>
</Dialog>

// Button includes:
// - role="button"
// - tabindex="0"
// - Keyboard activation (Space/Enter)
<Button>Accessible by default</Button>
```

### Keyboard Navigation

**Built-in keyboard support**:
- `Tab` / `Shift+Tab` - Navigate between interactive elements
- `Enter` / `Space` - Activate buttons
- `Escape` - Close dialogs, dropdowns, popovers
- `Arrow keys` - Navigate menus, select options, radio groups
- `Home` / `End` - Jump to first/last in lists

**Example: Command Palette**:
```tsx
import {
  Command,
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "@/components/ui/command"

// ⌘K to open
<CommandDialog open={open} onOpenChange={setOpen}>
  <CommandInput placeholder="Type a command..." />
  <CommandList>
    <CommandEmpty>No results found.</CommandEmpty>
    <CommandGroup heading="Suggestions">
      <CommandItem>Calendar</CommandItem>
      <CommandItem>Search Emoji</CommandItem>
      <CommandItem>Calculator</CommandItem>
    </CommandGroup>
  </CommandList>
</CommandDialog>
```

### Screen Reader Support

```tsx
// Visually hidden but accessible to screen readers
<span className="sr-only">Close dialog</span>

// Skip navigation links
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

// Descriptive labels
<FormLabel htmlFor="email">Email address</FormLabel>
<Input
  id="email"
  type="email"
  aria-describedby="email-description"
  aria-invalid={!!errors.email}
/>
<FormDescription id="email-description">
  We'll never share your email.
</FormDescription>
```

### Focus Management

```tsx
// Focus trap in Dialog (automatic)
<Dialog>
  <DialogContent>
    {/* Focus stays within dialog until closed */}
  </DialogContent>
</Dialog>

// Custom focus management
import { useRef, useEffect } from "react"

function CustomComponent() {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  return <Input ref={inputRef} />
}
```

## Composition Patterns

### Compound Components

```tsx
// Card composition
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>

// Form composition
<Form {...form}>
  <FormField
    control={form.control}
    name="field"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Label</FormLabel>
        <FormControl>
          <Input {...field} />
        </FormControl>
        <FormDescription>Help text</FormDescription>
        <FormMessage />
      </FormItem>
    )}
  />
</Form>
```

### Polymorphic Components (asChild)

```tsx
// Render Button as Link
import { Button } from "@/components/ui/button"
import Link from "next/link"

<Button asChild>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>

// Render as custom component
<Button asChild>
  <motion.button
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
  >
    Animated Button
  </motion.button>
</Button>
```

**How it works** (Radix Slot):
```tsx
import { Slot } from "@radix-ui/react-slot"

interface ButtonProps {
  asChild?: boolean
}

const Button = ({ asChild, ...props }: ButtonProps) => {
  const Comp = asChild ? Slot : "button"
  return <Comp {...props} />
}
```

### Custom Compositions

```tsx
// Create custom card variant
export function PricingCard({
  title,
  price,
  features,
  highlighted
}: PricingCardProps) {
  return (
    <Card className={cn(highlighted && "border-primary")}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription className="text-3xl font-bold">
          ${price}/mo
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {features.map((feature) => (
            <li key={feature} className="flex items-center">
              <Check className="mr-2 h-4 w-4 text-primary" />
              {feature}
            </li>
          ))}
        </ul>
      </CardContent>
      <CardFooter>
        <Button className="w-full" variant={highlighted ? "default" : "outline"}>
          Get Started
        </Button>
      </CardFooter>
    </Card>
  )
}
```

## CLI Commands

### Initialize

```bash
# Interactive init
npx shadcn-ui@latest init

# Non-interactive with defaults
npx shadcn-ui@latest init -y

# Specify options
npx shadcn-ui@latest init --typescript --tailwind
```

### Add Components

```bash
# Single component
npx shadcn-ui@latest add button

# Multiple components
npx shadcn-ui@latest add button card dialog form

# All components (not recommended - adds everything)
npx shadcn-ui@latest add --all

# Specific version
npx shadcn-ui@latest add button@1.0.0

# Overwrite existing
npx shadcn-ui@latest add button --overwrite

# Different path
npx shadcn-ui@latest add button --path src/components/ui
```

### Diff Components

```bash
# Check for component updates
npx shadcn-ui@latest diff

# Diff specific component
npx shadcn-ui@latest diff button

# Show what would change
npx shadcn-ui@latest diff --check
```

### Update Components

```bash
# Update all components
npx shadcn-ui@latest update

# Update specific components
npx shadcn-ui@latest update button card

# Preview changes before applying
npx shadcn-ui@latest update --dry-run
```

## Advanced Patterns

### Custom Hooks

```tsx
// useToast hook (built-in with toast component)
import { useToast } from "@/components/ui/use-toast"

function MyComponent() {
  const { toast } = useToast()

  return (
    <Button
      onClick={() => {
        toast({
          title: "Scheduled: Catch up",
          description: "Friday, February 10, 2023 at 5:57 PM",
        })
      }}
    >
      Show Toast
    </Button>
  )
}

// Custom form hook
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"

function useFormWithToast<T extends z.ZodType>(schema: T) {
  const { toast } = useToast()
  const form = useForm({
    resolver: zodResolver(schema),
  })

  const handleSubmit = form.handleSubmit(async (data) => {
    try {
      // Submit logic
      toast({ title: "Success!" })
    } catch (error) {
      toast({ title: "Error", variant: "destructive" })
    }
  })

  return { form, handleSubmit }
}
```

### Responsive Design

```tsx
// Mobile-first responsive components
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card>Mobile: 1 col, Tablet: 2 col, Desktop: 3 col</Card>
</div>

// Responsive dialog (sheet on mobile, dialog on desktop)
import { useMediaQuery } from "@/hooks/use-media-query"
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { Sheet, SheetContent } from "@/components/ui/sheet"

function ResponsiveModal({ children, ...props }) {
  const isDesktop = useMediaQuery("(min-width: 768px)")

  if (isDesktop) {
    return (
      <Dialog {...props}>
        <DialogContent>{children}</DialogContent>
      </Dialog>
    )
  }

  return (
    <Sheet {...props}>
      <SheetContent>{children}</SheetContent>
    </Sheet>
  )
}
```

### Animation Variants

```tsx
// Using Framer Motion with shadcn/ui
import { motion } from "framer-motion"
import { Card } from "@/components/ui/card"

const MotionCard = motion(Card)

<MotionCard
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Animated Card
</MotionCard>

// Staggered list animation
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map((item) => (
    <motion.li key={item.id} variants={item}>
      <Card>{item.content}</Card>
    </motion.li>
  ))}
</motion.ul>
```

## Best Practices

**Code Organization**:
- Keep shadcn/ui components in `components/ui/` (don't mix with app components)
- Create custom compositions in `components/` (outside ui/)
- Use `lib/utils.ts` for shared utilities

**Customization**:
- Modify components directly in your project (you own the code)
- Use CSS variables for theme-wide changes
- Extend variants with CVA for new styles
- Don't edit `components.json` manually (use CLI)

**Performance**:
- Tree-shaking automatic (only imports what you use)
- Use `asChild` to avoid unnecessary wrapper elements
- Lazy load heavy components (Calendar, Command)
- Prefer Server Components when possible (Next.js)

**Accessibility**:
- Don't remove ARIA attributes from components
- Test keyboard navigation for custom compositions
- Maintain focus management in dialogs/modals
- Use semantic HTML with `asChild` when applicable

**TypeScript**:
- Leverage exported types (ButtonProps, CardProps, etc.)
- Use VariantProps for variant type safety
- Add strict null checks for form validation

## Troubleshooting

**Import errors**:
```bash
# Check path aliases in tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Tailwind classes not applying**:
```ts
// Ensure content paths include your components
// tailwind.config.ts
content: [
  './src/components/**/*.{ts,tsx}',  // Add this
  './src/app/**/*.{ts,tsx}',
]
```

**Dark mode not working**:
```tsx
// Add suppressHydrationWarning to <html>
<html lang="en" suppressHydrationWarning>
```

**Form validation not triggering**:
```tsx
// Ensure FormMessage is included in FormField
<FormField>
  <FormItem>
    <FormControl>...</FormControl>
    <FormMessage />  {/* Required for errors */}
  </FormItem>
</FormField>
```

## Resources

- **Official Docs**: https://ui.shadcn.com
- **Component Source**: https://github.com/shadcn-ui/ui
- **Radix UI Docs**: https://www.radix-ui.com
- **Tailwind CSS**: https://tailwindcss.com
- **CVA Docs**: https://cva.style/docs
- **Examples**: https://ui.shadcn.com/examples
- **Community**: https://discord.gg/shadcn-ui