---
name: tailwind-design-system
description: Build scalable design systems with Tailwind CSS, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns.
---

# Tailwind Design System

## Design Token Hierarchy

```
Brand Tokens (abstract) → Semantic Tokens (purpose) → Component Tokens (specific)
Example: blue-500 → primary → button-bg

Component Architecture: Base styles → Variants → Sizes → States → Overrides
```

## Tailwind Config with CSS Variables

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: 'hsl(var(--primary))', foreground: 'hsl(var(--primary-foreground))' },
        secondary: { DEFAULT: 'hsl(var(--secondary))', foreground: 'hsl(var(--secondary-foreground))' },
        destructive: { DEFAULT: 'hsl(var(--destructive))', foreground: 'hsl(var(--destructive-foreground))' },
        muted: { DEFAULT: 'hsl(var(--muted))', foreground: 'hsl(var(--muted-foreground))' },
        accent: { DEFAULT: 'hsl(var(--accent))', foreground: 'hsl(var(--accent-foreground))' },
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        border: 'hsl(var(--border))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        lg: 'var(--radius)', md: 'calc(var(--radius) - 2px)', sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}
export default config
```

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%; --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%; --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%; --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%; --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%; --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%; --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%; --ring: 222.2 84% 4.9%; --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%; --foreground: 210 40% 98%;
    --primary: 210 40% 98%; --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%; --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%; --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%; --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%; --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%; --ring: 212.7 26.8% 83.9%;
  }
}
```

## Pattern 1: CVA Components

```typescript
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2', sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8', icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
  }
)

// Usage
<Button variant="destructive" size="lg">Delete</Button>
<Button asChild><Link href="/home">Home</Link></Button>
```

## Pattern 2: Compound Components

```typescript
const Card = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('rounded-lg border bg-card text-card-foreground shadow-sm', className)} {...props} />
  )
)
const CardHeader = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
  )
)
const CardTitle = forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props} />
  )
)
const CardContent = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
  )
)
const CardFooter = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex items-center p-6 pt-0', className)} {...props} />
  )
)
```

## Pattern 3: Form Components with Validation

```typescript
const Input = forwardRef<HTMLInputElement, InputProps & { error?: string }>(
  ({ className, type, error, ...props }, ref) => (
    <div className="relative">
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
          error && 'border-destructive focus-visible:ring-destructive', className
        )}
        ref={ref} aria-invalid={!!error} {...props}
      />
      {error && <p className="mt-1 text-sm text-destructive" role="alert">{error}</p>}
    </div>
  )
)

// Usage with React Hook Form + Zod
const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({ resolver: zodResolver(schema) })
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" {...register('email')} error={errors.email?.message} />
      </div>
      <Button type="submit" className="w-full">Sign In</Button>
    </form>
  )
}
```

## Pattern 4: Responsive Grid System

```typescript
const gridVariants = cva('grid', {
  variants: {
    cols: {
      1: 'grid-cols-1', 2: 'grid-cols-1 sm:grid-cols-2',
      3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3', 4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
    },
    gap: { none: 'gap-0', sm: 'gap-2', md: 'gap-4', lg: 'gap-6', xl: 'gap-8' },
  },
  defaultVariants: { cols: 3, gap: 'md' },
})

const containerVariants = cva('mx-auto w-full px-4 sm:px-6 lg:px-8', {
  variants: {
    size: { sm: 'max-w-screen-sm', md: 'max-w-screen-md', lg: 'max-w-screen-lg', xl: 'max-w-screen-xl', full: 'max-w-full' },
  },
  defaultVariants: { size: 'xl' },
})
```

## Pattern 5: Dark Mode ThemeProvider

```typescript
'use client'
type Theme = 'dark' | 'light' | 'system'

export function ThemeProvider({ children, defaultTheme = 'system', storageKey = 'theme' }: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)
  const [resolvedTheme, setResolvedTheme] = useState<'dark' | 'light'>('light')

  useEffect(() => {
    const stored = localStorage.getItem(storageKey) as Theme | null
    if (stored) setTheme(stored)
  }, [storageKey])

  useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')
    const resolved = theme === 'system'
      ? window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      : theme
    root.classList.add(resolved)
    setResolvedTheme(resolved)
  }, [theme])

  return (
    <ThemeContext.Provider value={{
      theme, resolvedTheme,
      setTheme: (t: Theme) => { localStorage.setItem(storageKey, t); setTheme(t) },
    }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

## Utility Functions

```typescript
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
export const focusRing = cn('focus-visible:outline-none focus-visible:ring-2', 'focus-visible:ring-ring focus-visible:ring-offset-2')
export const disabled = 'disabled:pointer-events-none disabled:opacity-50'
```

## Cross-References

- **frontend:design-system-patterns** -- headless component libraries, variant systems (CVA), design tokens
- **frontend:responsive-web-design** -- container queries, fluid typography, responsive images
- **frontend:accessibility-testing** -- WCAG compliance, focus management, screen reader testing
