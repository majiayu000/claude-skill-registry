---
name: shadcn-components
description: |
  shadcn/ui component patterns for this Next.js application.
  Covers available components, compound patterns, variants, form integration, and accessibility.
  Use this skill when building UI with shadcn/ui components.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# shadcn/ui Components Skill

Patterns and best practices for using shadcn/ui components in this Next.js application.

## Architecture Overview

```
core/components/ui/              # Base shadcn/ui components (62 total)
├── button.tsx                   # With variants (cva)
├── card.tsx                     # Compound component
├── form.tsx                     # React Hook Form integration
├── input.tsx                    # forwardRef pattern
└── ...

contents/themes/{theme}/components/  # Theme-specific extensions
└── custom-components/
```

## When to Use This Skill

- Building UI with shadcn/ui components
- Creating custom components that extend shadcn/ui
- Implementing forms with validation
- Understanding variant and compound patterns
- Ensuring accessibility compliance

## Available Components (62 total)

### Primitives

| Component | Description | Pattern |
|-----------|-------------|---------|
| `alert` | Feedback messages | Compound |
| `accordion` | Collapsible sections | Compound |
| `alert-dialog` | Confirmation dialogs | Compound |
| `avatar` | User avatars | Compound |
| `badge` | Status indicators | Variant |
| `breadcrumb` | Navigation path | Compound |
| `button` | Interactive buttons | Variant |
| `button-group` | Grouped buttons | - |
| `calendar` | Date picker | - |
| `card` | Content container | Compound |
| `checkbox` | Boolean input | forwardRef |
| `collapsible` | Toggle content | Compound |
| `command` | Command palette | Compound |
| `context-menu` | Right-click menu | Compound |
| `dialog` | Modal dialogs | Compound |
| `dropdown-menu` | Action menus | Compound |
| `input` | Text input | forwardRef |
| `label` | Form labels | forwardRef |
| `menubar` | Application menu | Compound |
| `pagination` | Page navigation | Compound |
| `popover` | Floating content | Compound |
| `progress` | Progress indicator | forwardRef |
| `radio-group` | Single selection | Compound |
| `scroll-area` | Custom scrollbar | Compound |
| `select` | Dropdown select | Compound |
| `separator` | Visual divider | forwardRef |
| `sheet` | Side panel | Compound + Variant |
| `slider` | Range input | forwardRef |
| `switch` | Toggle switch | forwardRef |
| `tabs` | Tab navigation | Compound |
| `toggle` | Toggle button | Variant |
| `tooltip` | Hover hints | Compound |
| `table` | Data tables | Compound |
| `textarea` | Multi-line input | forwardRef |

### Custom/Extended Components

| Component | Description |
|-----------|-------------|
| `address-input` | Address form fields |
| `combobox` | Searchable select |
| `currency-select` | Currency picker |
| `country-select` | Country picker |
| `timezone-select` | Timezone picker |
| `double-range` | Two-handle slider |
| `rating` | Star rating |
| `file-upload` | File upload with validation |
| `image-upload` | Image upload with preview |
| `audio-upload` | Audio file upload |
| `video-upload` | Video file upload |
| `form` | React Hook Form wrapper |
| `google-icon` | Google Material icons |
| `last-used-badge` | Recently used indicator |
| `multi-select` | Multiple selection |
| `password-input` | Password with toggle |
| `phone-input` | Phone number input |
| `relation-display` | Related entity display |
| `simple-relation-select` | Entity relation picker |
| `user-select` | User picker |
| `user-display` | User avatar + name |
| `rich-text-editor` | WYSIWYG editor |
| `skeleton` | Loading placeholders |
| `sonner` | Toast notifications |
| `tags-input` | Tag entry |

## Key Patterns

### 1. Compound Component Pattern

All compound components follow the Card pattern:

```typescript
// Exports multiple related components
export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }

// Usage
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description text</CardDescription>
  </CardHeader>
  <CardContent>
    Main content here
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**Components using this pattern:**
- Card, Dialog, Alert, Sheet, Popover
- Select, Accordion, Tabs, Command
- ContextMenu, DropdownMenu, Menubar
- Breadcrumb, Table, RadioGroup

### 2. Variant Pattern with cva()

```typescript
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  // Base classes
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// Component definition
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  )
)
```

**Components using variants:**
- Button (variant + size)
- Badge (variant)
- Alert (variant)
- Toggle (variant + size)
- Sheet (side)

### 3. forwardRef Pattern

```typescript
const Input = React.forwardRef<
  HTMLInputElement,
  React.ComponentProps<"input">
>(({ className, type, ...props }, ref) => (
  <input
    type={type}
    className={cn(
      "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1",
      "text-base shadow-sm transition-colors file:border-0",
      "placeholder:text-muted-foreground focus-visible:outline-none",
      "focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed",
      className
    )}
    ref={ref}
    {...props}
  />
))
Input.displayName = "Input"
```

### 4. cn() Utility

All components use `cn()` from `@/core/lib/utils` for class merging:

```typescript
import { cn } from '@/core/lib/utils'

// Merges classes with Tailwind conflict resolution
className={cn(
  "base-tailwind-classes",
  isActive && "active-classes",
  className  // Props override
)}
```

## Form Integration

### Form Components

```typescript
export {
  Form,           // = FormProvider from react-hook-form
  FormField,      // Controller wrapper with context
  FormItem,       // Layout wrapper with useId
  FormLabel,      // Accessible label with error styling
  FormControl,    // Slot-based control that adds ARIA attributes
  FormDescription,// Helper text
  FormMessage,    // Error message display
  useFormField    // Custom hook for field state
}
```

### Complete Form Example

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/core/components/ui/form'
import { Input } from '@/core/components/ui/input'
import { Button } from '@/core/components/ui/button'

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
})

type FormData = z.infer<typeof formSchema>

export function MyForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
    },
  })

  function onSubmit(data: FormData) {
    console.log(data)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input
                  placeholder="Enter your name"
                  data-cy="name-input"
                  {...field}
                />
              </FormControl>
              <FormDescription>
                Your display name
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
                <Input
                  type="email"
                  placeholder="you@example.com"
                  data-cy="email-input"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" data-cy="submit-btn">
          Submit
        </Button>
      </form>
    </Form>
  )
}
```

## data-cy Attributes

**IMPORTANT:** Core shadcn/ui components do NOT include `data-cy` attributes. They must be added at the usage layer.

```typescript
// CORRECT - Add data-cy when using components
<Button
  data-cy="create-task-btn"
  onClick={handleCreate}
>
  Create Task
</Button>

<Input
  data-cy="task-title-input"
  placeholder="Task title"
  {...field}
/>

<Dialog>
  <DialogTrigger data-cy="open-dialog-btn">
    Open
  </DialogTrigger>
  <DialogContent data-cy="task-dialog">
    {/* ... */}
  </DialogContent>
</Dialog>
```

## Accessibility

### Built-in ARIA Support

```typescript
// FormControl automatically adds:
<FormControl>
  {/* aria-invalid, aria-describedby */}
</FormControl>

// Dialog adds focus trap and escape handling
<Dialog>
  {/* role="dialog", aria-modal="true" */}
</Dialog>

// Select adds:
<Select>
  {/* role="combobox", aria-expanded */}
</Select>
```

### Keyboard Navigation

All interactive components support:
- **Tab** - Navigate between elements
- **Enter/Space** - Activate buttons, toggles
- **Escape** - Close dialogs, popovers
- **Arrow keys** - Navigate lists, menus

### Labels and Descriptions

```typescript
<FormItem>
  <FormLabel htmlFor="email">Email</FormLabel>
  <FormControl>
    <Input id="email" aria-describedby="email-description" />
  </FormControl>
  <FormDescription id="email-description">
    We'll never share your email
  </FormDescription>
</FormItem>
```

## Theming

### CSS Variables

All components use CSS variables instead of hardcoded colors:

```typescript
// CORRECT - Use semantic colors
className="bg-background text-foreground"
className="bg-primary text-primary-foreground"
className="bg-destructive text-destructive-foreground"
className="border-input"
className="ring-ring"

// WRONG - Hardcoded colors
className="bg-white text-black"
className="bg-blue-500 text-white"
```

### Available Color Tokens

| Token | Usage |
|-------|-------|
| `background` / `foreground` | Page background, main text |
| `card` / `card-foreground` | Card backgrounds |
| `primary` / `primary-foreground` | Primary actions |
| `secondary` / `secondary-foreground` | Secondary actions |
| `destructive` / `destructive-foreground` | Destructive actions |
| `accent` / `accent-foreground` | Highlights, hover states |
| `muted` / `muted-foreground` | Subdued elements |
| `success` / `success-foreground` | Success states |
| `input` | Input borders |
| `ring` | Focus rings |

## Common Patterns

### Dialog with Form

```typescript
<Dialog>
  <DialogTrigger asChild>
    <Button data-cy="open-create-dialog">Create New</Button>
  </DialogTrigger>
  <DialogContent data-cy="create-dialog">
    <DialogHeader>
      <DialogTitle>Create Item</DialogTitle>
      <DialogDescription>
        Fill in the details below
      </DialogDescription>
    </DialogHeader>
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Form fields */}
        <DialogFooter>
          <Button type="submit" data-cy="submit-create">
            Create
          </Button>
        </DialogFooter>
      </form>
    </Form>
  </DialogContent>
</Dialog>
```

### Dropdown Menu

```typescript
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" data-cy="actions-menu-btn">
      Actions
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent data-cy="actions-menu">
    <DropdownMenuLabel>Actions</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem data-cy="edit-action">
      Edit
    </DropdownMenuItem>
    <DropdownMenuItem
      className="text-destructive"
      data-cy="delete-action"
    >
      Delete
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### Toast Notifications

```typescript
import { toast } from 'sonner'

// Success
toast.success('Task created successfully')

// Error
toast.error('Failed to create task')

// With action
toast('Task created', {
  action: {
    label: 'Undo',
    onClick: () => handleUndo(),
  },
})
```

## Anti-Patterns

```typescript
// NEVER: Modify core/components/ui/ directly
// Files in this directory are auto-generated by shadcn/ui

// CORRECT: Create extensions in theme
// contents/themes/{theme}/components/custom-button.tsx

// NEVER: Hardcode colors
className="bg-green-500 text-white border-gray-300"

// CORRECT: Use CSS variables
className="bg-success text-success-foreground border-input"

// NEVER: Skip forwardRef for inputs
function MyInput(props) {
  return <input {...props} />  // Can't attach refs!
}

// CORRECT: Use forwardRef
const MyInput = React.forwardRef((props, ref) => (
  <input ref={ref} {...props} />
))

// NEVER: Missing accessibility attributes
<button onClick={toggle}>
  {isOpen ? 'Close' : 'Open'}
</button>

// CORRECT: Include ARIA attributes
<button
  onClick={toggle}
  aria-expanded={isOpen}
  aria-controls="panel-id"
>
  {isOpen ? 'Close' : 'Open'}
</button>

// NEVER: Skip data-cy on interactive elements
<Button onClick={handleSubmit}>Submit</Button>

// CORRECT: Always include data-cy
<Button data-cy="submit-form-btn" onClick={handleSubmit}>Submit</Button>
```

## Checklist

Before finalizing UI with shadcn/ui:

- [ ] Uses CSS variable colors (not hardcoded)
- [ ] Includes `data-cy` on all interactive elements
- [ ] Uses `cn()` for class merging
- [ ] Implements proper form validation with Zod
- [ ] Includes ARIA attributes where needed
- [ ] Uses forwardRef for custom inputs
- [ ] Follows compound component patterns
- [ ] Extensions are in theme directory, not core
- [ ] Keyboard navigation works correctly
- [ ] Loading states use Skeleton components

## Related Skills

- `tailwind-theming` - CSS variables and theming
- `react-patterns` - React best practices
- `cypress-selectors` - data-cy naming conventions
- `accessibility` - WCAG compliance
