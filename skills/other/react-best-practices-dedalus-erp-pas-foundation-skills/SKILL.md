---
name: react-best-practices
description: Comprehensive React and Next.js best practices guide covering performance optimization, component architecture, shadcn/ui patterns, Motion animations, and modern React 19+ patterns. This skill should be used when writing, reviewing, or refactoring React/Next.js code. Triggers on tasks involving React components, Next.js pages, data fetching, UI components, animations, or code quality improvements.
license: MIT
---

# React Best Practices

Comprehensive guide for building modern React and Next.js applications. Covers performance optimization, component architecture, shadcn/ui patterns, Motion animations, accessibility, and React 19+ features.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Building UI with shadcn/ui components
- Adding animations and micro-interactions
- Reviewing code for quality and performance
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Architecture | CRITICAL | `arch-` |
| 2 | Eliminating Waterfalls | CRITICAL | `async-` |
| 3 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 4 | Server Components & Actions | HIGH | `server-` |
| 5 | shadcn/ui Patterns | HIGH | `shadcn-` |
| 6 | State Management | MEDIUM-HIGH | `state-` |
| 7 | Motion & Animations | MEDIUM | `motion-` |
| 8 | Re-render Optimization | MEDIUM | `rerender-` |
| 9 | Accessibility | MEDIUM | `a11y-` |
| 10 | TypeScript Patterns | MEDIUM | `ts-` |

---

## 1. Component Architecture (CRITICAL)

### Quick Reference

- `arch-functional-components` - Use functional components with hooks exclusively
- `arch-composition-over-inheritance` - Build on existing components, don't extend
- `arch-single-responsibility` - Each component should do one thing well
- `arch-presentational-container` - Separate UI from logic when beneficial
- `arch-colocation` - Keep related files together (component, styles, tests)
- `arch-avoid-prop-drilling` - Use Context or composition for deep props

### Key Principles

**Functional Components Only**
```typescript
// Correct: Functional component with hooks
function UserProfile({ userId }: { userId: string }) {
  const { data: user } = useUser(userId)
  return <div>{user?.name}</div>
}

// Incorrect: Class component
class UserProfile extends React.Component { /* ... */ }
```

**Composition Pattern**
```typescript
// Correct: Compose smaller components
function Card({ children }: { children: React.ReactNode }) {
  return <div className="rounded-lg border p-4">{children}</div>
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="font-semibold">{children}</div>
}

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <p>Content</p>
</Card>
```

**Avoid Prop Drilling**
```typescript
// Incorrect: Passing props through many levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserMenu user={user} />
    </Sidebar>
  </Layout>
</App>

// Correct: Use Context for shared state
const UserContext = createContext<User | null>(null)

function App() {
  const user = useCurrentUser()
  return (
    <UserContext.Provider value={user}>
      <Layout>
        <Sidebar>
          <UserMenu />
        </Sidebar>
      </Layout>
    </UserContext.Provider>
  )
}
```

---

## 2. Eliminating Waterfalls (CRITICAL)

### Quick Reference

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Handle partial dependencies correctly
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### Key Principles

Waterfalls are the #1 performance killer. Each sequential await adds full network latency.

**Parallel Data Fetching**
```typescript
// Incorrect: Sequential waterfalls
async function Page() {
  const user = await fetchUser()
  const posts = await fetchPosts()
  const comments = await fetchComments()
  return <div>{/* render */}</div>
}

// Correct: Parallel fetching
async function Page() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments()
  ])
  return <div>{/* render */}</div>
}
```

**Strategic Suspense Boundaries**
```typescript
// Stream content as it becomes available
function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments />
      </Suspense>
    </div>
  )
}
```

---

## 3. Bundle Size Optimization (CRITICAL)

### Quick Reference

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### Key Principles

**Avoid Barrel File Imports**
```typescript
// Incorrect: Imports entire library
import { Button } from '@/components'
import { formatDate } from '@/utils'

// Correct: Direct imports enable tree-shaking
import { Button } from '@/components/ui/button'
import { formatDate } from '@/utils/date'
```

**Dynamic Imports**
```typescript
import dynamic from 'next/dynamic'

// Load only when needed
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false
})

function Dashboard({ showChart }) {
  return showChart ? <HeavyChart /> : null
}
```

---

## 4. Server Components & Actions (HIGH)

### Quick Reference

- `server-default-server` - Components are Server Components by default
- `server-use-client-boundary` - Add 'use client' only when needed
- `server-actions` - Use Server Actions for mutations
- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-serialization` - Minimize data passed to client components

### Key Principles

**Server Components by Default**
```typescript
// Server Component (default) - can be async
async function ProductPage({ id }: { id: string }) {
  const product = await db.product.findUnique({ where: { id } })
  return <ProductDetails product={product} />
}

// Client Component - only when needed for interactivity
'use client'
function AddToCartButton({ productId }: { productId: string }) {
  const [isPending, startTransition] = useTransition()

  return (
    <Button
      onClick={() => startTransition(() => addToCart(productId))}
      disabled={isPending}
    >
      Add to Cart
    </Button>
  )
}
```

**Server Actions**
```typescript
// actions.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({ data: { title, content } })
  revalidatePath('/posts')
}

// Component usage
function CreatePostForm() {
  return (
    <form action={createPost}>
      <Input name="title" placeholder="Title" />
      <Textarea name="content" placeholder="Content" />
      <Button type="submit">Create Post</Button>
    </form>
  )
}
```

---

## 5. shadcn/ui Patterns (HIGH)

### Quick Reference

- `shadcn-composition` - Build on existing shadcn/ui primitives
- `shadcn-variants` - Use class-variance-authority for component variants
- `shadcn-theme-integration` - Use CSS custom properties for theming
- `shadcn-accessibility` - Leverage built-in accessibility from Radix
- `shadcn-customization` - Modify copied components, don't wrap excessively

### Core Principles

shadcn/ui is built around:
- **Open Code**: Components are copied into your project, fully customizable
- **Composition**: Every component uses a common, composable interface
- **Beautiful Defaults**: Carefully chosen default styles
- **Accessibility by Default**: Built on Radix UI primitives

### Component Installation

```bash
# Add components as needed
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add form
```

### Building Custom Components

**Composition Over Creation**
```typescript
// Correct: Build on existing primitives
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface ProductCardProps {
  product: Product
  onSelect?: () => void
}

function ProductCard({ product, onSelect }: ProductCardProps) {
  return (
    <Card
      className="cursor-pointer hover:shadow-md transition-shadow"
      onClick={onSelect}
    >
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>{product.name}</CardTitle>
          {product.isNew && <Badge>New</Badge>}
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{product.description}</p>
        <p className="text-lg font-bold mt-2">${product.price}</p>
      </CardContent>
    </Card>
  )
}
```

**Using Variants with CVA**
```typescript
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const statusBadgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold',
  {
    variants: {
      status: {
        pending: 'bg-yellow-100 text-yellow-800',
        active: 'bg-green-100 text-green-800',
        inactive: 'bg-gray-100 text-gray-800',
        error: 'bg-red-100 text-red-800',
      },
    },
    defaultVariants: {
      status: 'pending',
    },
  }
)

interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof statusBadgeVariants> {
  label: string
}

function StatusBadge({ status, label, className, ...props }: StatusBadgeProps) {
  return (
    <span className={cn(statusBadgeVariants({ status }), className)} {...props}>
      {label}
    </span>
  )
}
```

### Common shadcn/ui Components

**Forms with React Hook Form + Zod**
```typescript
'use client'

import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const formSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">Sign In</Button>
      </form>
    </Form>
  )
}
```

**Dialog/Modal Pattern**
```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

function ConfirmDialog({
  onConfirm,
  title,
  description
}: {
  onConfirm: () => void
  title: string
  description: string
}) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline">Cancel</Button>
          <Button variant="destructive" onClick={onConfirm}>
            Confirm
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

**Data Table with Tanstack Table**
```typescript
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table'

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
}

function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <TableHead key={header.id}>
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.map((row) => (
            <TableRow key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <TableCell key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

---

## 6. State Management (MEDIUM-HIGH)

### Quick Reference

- `state-local-first` - Use useState/useReducer for local state
- `state-context-static` - Use Context for infrequently changing data
- `state-derived-compute` - Compute derived values, don't store them
- `state-url-state` - Use URL for shareable/bookmarkable state
- `state-server-state` - Use SWR/TanStack Query for server state

### Key Principles

**Avoid Derived State**
```typescript
// Incorrect: Storing derived state
function ProductList({ products }) {
  const [items, setItems] = useState(products)
  const [count, setCount] = useState(products.length) // Derived!

  // Bug: count can get out of sync with items
}

// Correct: Compute derived values
function ProductList({ products }) {
  const [items, setItems] = useState(products)
  const count = items.length // Always in sync
}
```

**URL State for Filters/Pagination**
```typescript
'use client'

import { useSearchParams, useRouter } from 'next/navigation'

function ProductFilters() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const category = searchParams.get('category') || 'all'

  function setCategory(newCategory: string) {
    const params = new URLSearchParams(searchParams)
    params.set('category', newCategory)
    router.push(`?${params.toString()}`)
  }

  return (
    <Select value={category} onValueChange={setCategory}>
      {/* options */}
    </Select>
  )
}
```

---

## 7. Motion & Animations (MEDIUM)

### Quick Reference

- `motion-purposeful` - Animations should enhance UX, not distract
- `motion-performance` - Use transform/opacity, avoid layout triggers
- `motion-reduced-motion` - Respect prefers-reduced-motion
- `motion-layout-id` - Use layoutId for shared element transitions
- `motion-exit-animations` - Use AnimatePresence for exit animations
- `motion-variants` - Define reusable animation states

### Installation

```bash
npm install motion
```

### Core Principles

Motion (formerly Framer Motion) provides declarative animations that enhance user experience.

**Basic Animations**
```typescript
'use client'

import { motion } from 'motion/react'

function FadeInCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="rounded-lg border p-4"
    >
      {children}
    </motion.div>
  )
}
```

**Interaction States**
```typescript
function InteractiveButton({ children }: { children: React.ReactNode }) {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
    >
      {children}
    </motion.button>
  )
}
```

**Exit Animations with AnimatePresence**
```typescript
import { motion, AnimatePresence } from 'motion/react'

function NotificationList({ notifications }: { notifications: Notification[] }) {
  return (
    <AnimatePresence>
      {notifications.map((notification) => (
        <motion.div
          key={notification.id}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.2 }}
        >
          <Notification data={notification} />
        </motion.div>
      ))}
    </AnimatePresence>
  )
}
```

**Shared Element Transitions**
```typescript
function ProductGrid({ products }: { products: Product[] }) {
  const [selected, setSelected] = useState<Product | null>(null)

  return (
    <>
      <div className="grid grid-cols-3 gap-4">
        {products.map((product) => (
          <motion.div
            key={product.id}
            layoutId={`product-${product.id}`}
            onClick={() => setSelected(product)}
            className="cursor-pointer"
          >
            <img src={product.image} alt={product.name} />
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selected && (
          <motion.div
            layoutId={`product-${selected.id}`}
            className="fixed inset-0 flex items-center justify-center"
          >
            <ProductDetail product={selected} onClose={() => setSelected(null)} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
```

**Reusable Variants**
```typescript
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
}

function StaggeredList({ items }: { items: string[] }) {
  return (
    <motion.ul variants={staggerContainer} initial="initial" animate="animate">
      {items.map((item, i) => (
        <motion.li key={i} variants={fadeInUp}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

**Scroll-Triggered Animations**
```typescript
import { motion, useInView } from 'motion/react'
import { useRef } from 'react'

function ScrollReveal({ children }: { children: React.ReactNode }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-100px' })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.5 }}
    >
      {children}
    </motion.div>
  )
}
```

**Respecting Reduced Motion**
```typescript
import { motion, useReducedMotion } from 'motion/react'

function AccessibleAnimation({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

### Performance Tips

- Use `transform` and `opacity` for smooth 60fps animations
- Set `willChange` prop for complex animations
- Keep exit animations short (under 300ms)
- Use `useInView` to lazy-load animations
- Avoid animating `width`, `height`, `top`, `left` directly

---

## 8. Re-render Optimization (MEDIUM)

### Quick Reference

- `rerender-memo` - Extract expensive work into memoized components
- `rerender-usememo` - Memoize expensive calculations
- `rerender-usecallback` - Stabilize callback references
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-transitions` - Use startTransition for non-urgent updates

### Key Principles

**Memoization for Expensive Components**
```typescript
import { memo } from 'react'

const ExpensiveList = memo(function ExpensiveList({
  items
}: {
  items: Item[]
}) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{/* expensive render */}</li>
      ))}
    </ul>
  )
})
```

**Stable Callbacks**
```typescript
function Parent() {
  const [count, setCount] = useState(0)

  // Stable reference - won't cause child re-renders
  const handleClick = useCallback(() => {
    setCount(c => c + 1)
  }, [])

  return <MemoizedChild onClick={handleClick} />
}
```

**Non-Urgent Updates with Transitions**
```typescript
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setQuery(e.target.value) // Urgent: update input immediately

    startTransition(() => {
      setResults(filterResults(e.target.value)) // Non-urgent: can be interrupted
    })
  }

  return (
    <>
      <Input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

---

## 9. Accessibility (MEDIUM)

### Quick Reference

- `a11y-semantic-html` - Use correct HTML elements
- `a11y-keyboard-nav` - Ensure keyboard navigability
- `a11y-aria-labels` - Add descriptive labels for screen readers
- `a11y-focus-management` - Manage focus in modals and dynamic content
- `a11y-color-contrast` - Ensure sufficient color contrast

### Key Principles

**Semantic HTML**
```typescript
// Incorrect: div soup
<div onClick={handleClick}>Click me</div>

// Correct: semantic button
<button onClick={handleClick}>Click me</button>
```

**Focus Management in Modals**
```typescript
function Modal({ isOpen, onClose, children }) {
  const closeButtonRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (isOpen) {
      closeButtonRef.current?.focus()
    }
  }, [isOpen])

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        {children}
        <Button ref={closeButtonRef} onClick={onClose}>
          Close
        </Button>
      </DialogContent>
    </Dialog>
  )
}
```

**Skip Links**
```typescript
function Layout({ children }) {
  return (
    <>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4"
      >
        Skip to main content
      </a>
      <Header />
      <main id="main-content">{children}</main>
    </>
  )
}
```

---

## 10. TypeScript Patterns (MEDIUM)

### Quick Reference

- `ts-strict-mode` - Enable strict TypeScript configuration
- `ts-component-props` - Define explicit prop interfaces
- `ts-generics` - Use generics for reusable components
- `ts-discriminated-unions` - Use for state machines
- `ts-infer-when-possible` - Let TypeScript infer when obvious

### Key Principles

**Component Props**
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

function Button({
  variant = 'default',
  size = 'md',
  isLoading,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  )
}
```

**Discriminated Unions for State**
```typescript
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }

function useAsync<T>(asyncFn: () => Promise<T>) {
  const [state, setState] = useState<AsyncState<T>>({ status: 'idle' })

  // TypeScript knows exact shape based on status
  if (state.status === 'success') {
    return state.data // TypeScript knows data exists
  }
}
```

**Generic Components**
```typescript
interface SelectProps<T> {
  options: T[]
  value: T
  onChange: (value: T) => void
  getLabel: (option: T) => string
  getValue: (option: T) => string
}

function Select<T>({ options, value, onChange, getLabel, getValue }: SelectProps<T>) {
  return (
    <select
      value={getValue(value)}
      onChange={(e) => {
        const selected = options.find(o => getValue(o) === e.target.value)
        if (selected) onChange(selected)
      }}
    >
      {options.map((option) => (
        <option key={getValue(option)} value={getValue(option)}>
          {getLabel(option)}
        </option>
      ))}
    </select>
  )
}
```

---

## React 19+ Features

### New Hooks

**useActionState** - Form state management
```typescript
'use client'

import { useActionState } from 'react'

function SubscribeForm() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData) => {
      const email = formData.get('email')
      const result = await subscribe(email)
      return result
    },
    null
  )

  return (
    <form action={formAction}>
      <Input name="email" type="email" />
      <Button type="submit" disabled={isPending}>
        {isPending ? 'Subscribing...' : 'Subscribe'}
      </Button>
      {state?.error && <p className="text-red-500">{state.error}</p>}
    </form>
  )
}
```

**useOptimistic** - Optimistic UI updates
```typescript
'use client'

import { useOptimistic } from 'react'

function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  )

  async function addTodo(formData: FormData) {
    const title = formData.get('title') as string
    const newTodo = { id: crypto.randomUUID(), title, completed: false }

    addOptimisticTodo(newTodo) // Immediately show in UI
    await createTodo(title)    // Then persist to server
  }

  return (
    <>
      <form action={addTodo}>
        <Input name="title" />
        <Button type="submit">Add</Button>
      </form>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </>
  )
}
```

**use** - Async resource reading
```typescript
import { use, Suspense } from 'react'

async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise) // Suspends until resolved
  return <div>{user.name}</div>
}

function Page({ userId }: { userId: string }) {
  const userPromise = fetchUser(userId)

  return (
    <Suspense fallback={<UserSkeleton />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  )
}
```

---

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx
│   ├── page.tsx
│   └── (routes)/
├── components/
│   ├── ui/                 # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   └── features/           # Feature-specific components
│       ├── auth/
│       └── dashboard/
├── hooks/                  # Custom hooks
├── lib/                    # Utilities
│   ├── utils.ts           # cn() helper, etc.
│   └── validations.ts     # Zod schemas
├── actions/               # Server Actions
└── types/                 # TypeScript types
```

---

## References

- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Motion Documentation](https://motion.dev)
- [Radix UI Primitives](https://radix-ui.com)
- [TanStack Query](https://tanstack.com/query)
- [Tailwind CSS](https://tailwindcss.com)
