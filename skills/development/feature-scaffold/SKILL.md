# Feature Scaffold Skill

> **Generate Complete Features**: Create entire feature folders with all files in the correct structure.

---

## 🎯 Purpose

When user says: "Create a [feature] feature"

This skill generates:
- Page components
- API routes/Server Actions
- Validation schemas
- Types
- Tests (optional)

All following consistent project structure.

---

## 📁 Feature Structure

```
src/
├── app/
│   └── [feature]/
│       ├── page.tsx           # List page
│       ├── loading.tsx        # Loading state
│       ├── error.tsx          # Error boundary
│       ├── new/
│       │   └── page.tsx       # Create page
│       ├── [id]/
│       │   ├── page.tsx       # Detail page
│       │   └── edit/
│       │       └── page.tsx   # Edit page
│       └── _components/
│           ├── list.tsx       # List component
│           ├── form.tsx       # Create/Edit form
│           ├── card.tsx       # Card component
│           └── delete-button.tsx
├── lib/
│   ├── actions/
│   │   └── [feature].ts       # Server Actions
│   └── validations/
│       └── [feature].ts       # Zod schemas
└── types/
    └── [feature].ts           # TypeScript types
```

---

## 🚀 Step 1: Types

```typescript
// types/[feature].ts
export interface [Feature] {
  id: string
  // Add fields
  createdAt: Date
  updatedAt: Date
}

export type Create[Feature]Input = Omit<[Feature], 'id' | 'createdAt' | 'updatedAt'>
export type Update[Feature]Input = Partial<Create[Feature]Input>
```

---

## 🚀 Step 2: Validation

```typescript
// lib/validations/[feature].ts
import { z } from "zod"

export const create[Feature]Schema = z.object({
  name: z.string().min(2).max(100),
  // Add fields
})

export const update[Feature]Schema = create[Feature]Schema.partial()

export type Create[Feature]Input = z.infer<typeof create[Feature]Schema>
```

---

## 🚀 Step 3: Server Actions

```typescript
// lib/actions/[feature].ts
"use server"
import { auth } from "@/auth"
import { db } from "@/lib/db"
import { create[Feature]Schema } from "@/lib/validations/[feature]"
import { revalidatePath } from "next/cache"

export async function get[Features]() {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  return db.[feature].findMany({
    where: { userId: session.user.id },
    orderBy: { createdAt: "desc" },
  })
}

export async function get[Feature](id: string) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  return db.[feature].findFirst({
    where: { id, userId: session.user.id },
  })
}

export async function create[Feature](formData: FormData) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  const data = create[Feature]Schema.parse({
    name: formData.get("name"),
  })
  
  await db.[feature].create({
    data: { ...data, userId: session.user.id },
  })
  
  revalidatePath("/[features]")
  return { success: true }
}

export async function update[Feature](id: string, formData: FormData) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  const existing = await db.[feature].findFirst({
    where: { id, userId: session.user.id },
  })
  if (!existing) throw new Error("Not found")
  
  const data = create[Feature]Schema.partial().parse({
    name: formData.get("name") || undefined,
  })
  
  await db.[feature].update({ where: { id }, data })
  
  revalidatePath("/[features]")
  return { success: true }
}

export async function delete[Feature](id: string) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  await db.[feature].deleteMany({
    where: { id, userId: session.user.id },
  })
  
  revalidatePath("/[features]")
  return { success: true }
}
```

---

## 🚀 Step 4: List Page

```tsx
// app/[features]/page.tsx
import { get[Features] } from "@/lib/actions/[feature]"
import { [Feature]List } from "./_components/list"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default async function [Features]Page() {
  const items = await get[Features]()
  
  return (
    <div className="container py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">[Features]</h1>
        <Button asChild>
          <Link href="/[features]/new">Create New</Link>
        </Button>
      </div>
      <[Feature]List items={items} />
    </div>
  )
}
```

---

## 🚀 Step 5: Loading & Error

```tsx
// app/[features]/loading.tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="container py-8">
      <Skeleton className="h-8 w-48 mb-6" />
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <Skeleton key={i} className="h-24 w-full" />
        ))}
      </div>
    </div>
  )
}

// app/[features]/error.tsx
"use client"

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div className="container py-8 text-center">
      <h2 className="text-xl font-bold mb-4">Something went wrong</h2>
      <p className="text-muted-foreground mb-4">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}
```

---

## 🚀 Step 6: Components

```tsx
// app/[features]/_components/list.tsx
"use client"
import { [Feature] } from "@/types/[feature]"
import { [Feature]Card } from "./card"

export function [Feature]List({ items }: { items: [Feature][] }) {
  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        No items yet. Create your first one!
      </div>
    )
  }
  
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {items.map((item) => (
        <[Feature]Card key={item.id} item={item} />
      ))}
    </div>
  )
}

// app/[features]/_components/card.tsx
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { DeleteButton } from "./delete-button"

export function [Feature]Card({ item }: { item: [Feature] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{item.name}</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Content */}
      </CardContent>
      <CardFooter className="flex gap-2">
        <Button variant="outline" size="sm" asChild>
          <Link href={`/[features]/${item.id}/edit`}>Edit</Link>
        </Button>
        <DeleteButton id={item.id} />
      </CardFooter>
    </Card>
  )
}

// app/[features]/_components/delete-button.tsx
"use client"
import { delete[Feature] } from "@/lib/actions/[feature]"
import { Button } from "@/components/ui/button"
import { useTransition } from "react"

export function DeleteButton({ id }: { id: string }) {
  const [isPending, startTransition] = useTransition()
  
  const handleDelete = () => {
    if (!confirm("Delete this item?")) return
    startTransition(() => delete[Feature](id))
  }
  
  return (
    <Button
      variant="destructive"
      size="sm"
      onClick={handleDelete}
      disabled={isPending}
    >
      {isPending ? "..." : "Delete"}
    </Button>
  )
}
```

---

## 📋 Scaffold Checklist

After generating:
- [ ] Types created
- [ ] Validation schema created
- [ ] Server actions created
- [ ] List page created
- [ ] Create page created
- [ ] Edit page created
- [ ] Detail page (if needed)
- [ ] Loading state
- [ ] Error boundary
- [ ] All components created
- [ ] Prisma schema updated
- [ ] Migration run

---

## 🔄 Token Replacements

Replace these when using:
- `[Feature]` → `Project`, `Task` (PascalCase singular)
- `[feature]` → `project`, `task` (camelCase singular)
- `[Features]` → `Projects`, `Tasks` (PascalCase plural)
- `[features]` → `projects`, `tasks` (lowercase plural)

---

**Scaffold. Customize. Ship!**
