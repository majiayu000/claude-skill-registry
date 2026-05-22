---
name: nextjs-shadcn
description: shadcn/ui for Next.js App Router - Field components, TanStack Form integration, Server/Client Components. Use when building UI with shadcn in Next.js.
user-invocable: false
---

# shadcn/ui for Next.js

Beautiful, accessible components with TanStack Form integration.

## Installation

```bash
bunx --bun shadcn@latest init
```

### Configuration (Tailwind CSS v4)

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "gray",
    "cssVariables": true,
    "prefix": ""
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/modules/cores/shadcn/components",
    "utils": "@/modules/cores/lib/utils",
    "ui": "@/modules/cores/shadcn/components/ui",
    "lib": "@/modules/cores/lib",
    "hooks": "@/modules/cores/hooks"
  }
}
```

**Note:** For Tailwind CSS v4, the `config` field must be empty.

---

## Adding Components

```bash
bunx --bun shadcn@latest add button card field input
```

---

## Form with TanStack Form

```typescript
// components/ProfileForm.tsx
'use client'

import { useForm } from '@tanstack/react-form'
import { toast } from 'sonner'
import { z } from 'zod'
import { Button } from '@/modules/cores/shadcn/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/modules/cores/shadcn/components/ui/card'
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from '@/modules/cores/shadcn/components/ui/field'
import { Input } from '@/modules/cores/shadcn/components/ui/input'

const formSchema = z.object({
  username: z
    .string()
    .min(3, 'Username must be at least 3 characters.')
    .max(10, 'Username must be at most 10 characters.')
    .regex(/^[a-zA-Z0-9_]+$/, 'Letters, numbers, underscores only.'),
})

export function ProfileForm() {
  const form = useForm({
    defaultValues: { username: '' },
    validators: { onSubmit: formSchema },
    onSubmit: async ({ value }) => {
      toast('Saved!', { description: JSON.stringify(value) })
    },
  })

  return (
    <Card className="w-full sm:max-w-md">
      <CardHeader>
        <CardTitle>Profile Settings</CardTitle>
        <CardDescription>Update your profile information.</CardDescription>
      </CardHeader>
      <CardContent>
        <form
          id="profile-form"
          onSubmit={(e) => {
            e.preventDefault()
            form.handleSubmit()
          }}
        >
          <FieldGroup>
            <form.Field
              name="username"
              children={(field) => {
                const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
                return (
                  <Field data-invalid={isInvalid}>
                    <FieldLabel htmlFor="username">Username</FieldLabel>
                    <Input
                      id="username"
                      name={field.name}
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      onChange={(e) => field.handleChange(e.target.value)}
                      aria-invalid={isInvalid}
                      placeholder="shadcn"
                    />
                    <FieldDescription>
                      Your public display name. 3-10 characters.
                    </FieldDescription>
                    {isInvalid && <FieldError errors={field.state.meta.errors} />}
                  </Field>
                )
              }}
            />
          </FieldGroup>
        </form>
      </CardContent>
      <CardFooter>
        <Field orientation="horizontal">
          <Button type="button" variant="outline" onClick={() => form.reset()}>
            Reset
          </Button>
          <Button type="submit" form="profile-form">
            Save
          </Button>
        </Field>
      </CardFooter>
    </Card>
  )
}
```

---

## Field Component Pattern

```typescript
// New shadcn Field components for forms
import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
  FieldTitle,
} from '@/modules/cores/shadcn/components/ui/field'

// Basic field
<Field data-invalid={hasError}>
  <FieldLabel htmlFor="email">Email</FieldLabel>
  <Input id="email" />
  <FieldDescription>Your email address.</FieldDescription>
  {hasError && <FieldError errors={errors} />}
</Field>

// Horizontal field (for switches, checkboxes)
<Field orientation="horizontal">
  <FieldContent>
    <FieldTitle>Notifications</FieldTitle>
    <FieldDescription>Receive email notifications.</FieldDescription>
  </FieldContent>
  <Switch />
</Field>
```

---

## Server Components (Default)

```typescript
// app/users/page.tsx (Server Component)
import { Card, CardContent, CardHeader, CardTitle } from '@/modules/cores/shadcn/components/ui/card'
import { Badge } from '@/modules/cores/shadcn/components/ui/badge'

export default async function UsersPage() {
  const users = await getUsers()

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {users.map((user) => (
        <Card key={user.id}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {user.name}
              <Badge variant={user.role === 'admin' ? 'default' : 'secondary'}>
                {user.role}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{user.email}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

---

## Toast Notifications

```typescript
// app/layout.tsx
import { Toaster } from '@/modules/cores/shadcn/components/ui/sonner'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}

// Usage in components
import { toast } from 'sonner'

toast('Success!', { description: 'Your changes have been saved.' })
toast.error('Error', { description: 'Something went wrong.' })
```

---

## Component Categories

| Category | Components |
|----------|------------|
| Layout | Card, Separator, Tabs, Accordion |
| Forms | Button, Input, Field, Select, Checkbox, Switch |
| Feedback | Alert, Toast (Sonner), Dialog, Sheet |
| Data | Table, Badge, Avatar, Calendar |
| Navigation | Breadcrumb, DropdownMenu, Command |

---

## Best Practices

1. **Use Field components** - New pattern for form fields
2. **TanStack Form** - Preferred over React Hook Form
3. **Server Components** - Default, no `'use client'`
4. **Sonner for toasts** - Modern toast notifications
5. **MCP tools** - Use `mcp__shadcn__*` to explore components
