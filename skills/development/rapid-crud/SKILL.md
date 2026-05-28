# Rapid CRUD Skill

> **Generate Full-Stack CRUD in Minutes**: Automated workflow for creating complete Create, Read, Update, Delete features.

---

## 🎯 Purpose

This skill generates a complete vertical slice of functionality:
- **Database**: Prisma schema + migration
- **API**: Server Actions or API Routes
- **UI**: List, Create, Edit, Delete components
- **Validation**: Zod schemas
- **Types**: TypeScript interfaces

---

## 🚀 Quick Command

When user says: "Create CRUD for [resource]"

Execute this workflow:

---

## Step 1: Define Schema

```prisma
// Add to prisma/schema.prisma
model [Resource] {
  id          String   @id @default(cuid())
  name        String
  description String?
  status      String   @default("active")
  
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([userId])
}
```

Run: `npx prisma db push`

---

## Step 2: Create Validation Schema

```typescript
// lib/validations/[resource].ts
import { z } from "zod"

export const create[Resource]Schema = z.object({
  name: z.string().min(2).max(100),
  description: z.string().max(500).optional(),
  status: z.enum(["active", "inactive"]).default("active"),
})

export const update[Resource]Schema = create[Resource]Schema.partial()

export type Create[Resource]Input = z.infer<typeof create[Resource]Schema>
export type Update[Resource]Input = z.infer<typeof update[Resource]Schema>
```

---

## Step 3: Create Server Actions

```typescript
// lib/actions/[resource].ts
"use server"
import { auth } from "@/auth"
import { db } from "@/lib/db"
import { create[Resource]Schema, update[Resource]Schema } from "@/lib/validations/[resource]"
import { revalidatePath } from "next/cache"

export async function get[Resources]() {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  return db.[resource].findMany({
    where: { userId: session.user.id },
    orderBy: { createdAt: "desc" },
  })
}

export async function get[Resource](id: string) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  return db.[resource].findFirst({
    where: { id, userId: session.user.id },
  })
}

export async function create[Resource](data: FormData) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  const validated = create[Resource]Schema.parse({
    name: data.get("name"),
    description: data.get("description"),
    status: data.get("status"),
  })
  
  await db.[resource].create({
    data: { ...validated, userId: session.user.id },
  })
  
  revalidatePath("/[resources]")
  return { success: true }
}

export async function update[Resource](id: string, data: FormData) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  const existing = await db.[resource].findFirst({
    where: { id, userId: session.user.id },
  })
  if (!existing) throw new Error("Not found")
  
  const validated = update[Resource]Schema.parse({
    name: data.get("name") || undefined,
    description: data.get("description") || undefined,
    status: data.get("status") || undefined,
  })
  
  await db.[resource].update({ where: { id }, data: validated })
  
  revalidatePath("/[resources]")
  return { success: true }
}

export async function delete[Resource](id: string) {
  const session = await auth()
  if (!session?.user) throw new Error("Unauthorized")
  
  await db.[resource].deleteMany({
    where: { id, userId: session.user.id },
  })
  
  revalidatePath("/[resources]")
  return { success: true }
}
```

---

## Step 4: Create UI Components

### List Page
```tsx
// app/[resources]/page.tsx
import { get[Resources] } from "@/lib/actions/[resource]"
import { [Resource]List } from "./_components/list"

export default async function [Resources]Page() {
  const items = await get[Resources]()
  
  return (
    <div className="container py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">[Resources]</h1>
        <a href="/[resources]/new" className="btn btn-primary">
          Create New
        </a>
      </div>
      <[Resource]List items={items} />
    </div>
  )
}
```

### List Component
```tsx
// app/[resources]/_components/list.tsx
"use client"
import { delete[Resource] } from "@/lib/actions/[resource]"
import { useTransition } from "react"

export function [Resource]List({ items }: { items: [Resource][] }) {
  const [isPending, startTransition] = useTransition()
  
  const handleDelete = (id: string) => {
    if (!confirm("Are you sure?")) return
    startTransition(() => delete[Resource](id))
  }
  
  return (
    <div className="space-y-4">
      {items.map((item) => (
        <div key={item.id} className="border rounded-lg p-4 flex justify-between">
          <div>
            <h3 className="font-semibold">{item.name}</h3>
            <p className="text-gray-500">{item.description}</p>
          </div>
          <div className="flex gap-2">
            <a href={`/[resources]/${item.id}/edit`} className="btn btn-sm">
              Edit
            </a>
            <button
              onClick={() => handleDelete(item.id)}
              disabled={isPending}
              className="btn btn-sm btn-danger"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
```

### Create Form
```tsx
// app/[resources]/new/page.tsx
import { [Resource]Form } from "../_components/form"

export default function New[Resource]Page() {
  return (
    <div className="container py-8 max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Create [Resource]</h1>
      <[Resource]Form />
    </div>
  )
}
```

### Edit Form
```tsx
// app/[resources]/[id]/edit/page.tsx
import { get[Resource] } from "@/lib/actions/[resource]"
import { [Resource]Form } from "../../_components/form"
import { notFound } from "next/navigation"

export default async function Edit[Resource]Page({ params }: { params: { id: string } }) {
  const item = await get[Resource](params.id)
  if (!item) notFound()
  
  return (
    <div className="container py-8 max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Edit [Resource]</h1>
      <[Resource]Form defaultValues={item} id={params.id} />
    </div>
  )
}
```

### Form Component
```tsx
// app/[resources]/_components/form.tsx
"use client"
import { create[Resource], update[Resource] } from "@/lib/actions/[resource]"
import { useRouter } from "next/navigation"
import { useTransition } from "react"

export function [Resource]Form({
  defaultValues,
  id,
}: {
  defaultValues?: Partial<[Resource]>
  id?: string
}) {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    
    startTransition(async () => {
      if (id) {
        await update[Resource](id, formData)
      } else {
        await create[Resource](formData)
      }
      router.push("/[resources]")
    })
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block font-medium mb-1">Name</label>
        <input
          name="name"
          defaultValue={defaultValues?.name}
          required
          className="w-full border rounded-md px-3 py-2"
        />
      </div>
      
      <div>
        <label className="block font-medium mb-1">Description</label>
        <textarea
          name="description"
          defaultValue={defaultValues?.description ?? ""}
          className="w-full border rounded-md px-3 py-2"
          rows={3}
        />
      </div>
      
      <div>
        <label className="block font-medium mb-1">Status</label>
        <select
          name="status"
          defaultValue={defaultValues?.status ?? "active"}
          className="w-full border rounded-md px-3 py-2"
        >
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
      
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={isPending}
          className="btn btn-primary"
        >
          {isPending ? "Saving..." : id ? "Update" : "Create"}
        </button>
        <button
          type="button"
          onClick={() => router.back()}
          className="btn"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}
```

---

## 📋 Checklist

After generating CRUD:
- [ ] Schema added to Prisma
- [ ] `npx prisma db push` run
- [ ] Validation schema created
- [ ] Server actions created
- [ ] List page created
- [ ] Create page created
- [ ] Edit page created
- [ ] Form component created
- [ ] Delete functionality works
- [ ] Auth checks in place
- [ ] Types exported

---

## 🔄 Replace Tokens

When using this template, replace:
- `[Resource]` → `Product`, `Task`, `Project` (PascalCase)
- `[resource]` → `product`, `task`, `project` (camelCase)
- `[resources]` → `products`, `tasks`, `projects` (plural, lowercase)

---

**Time to implement**: ~5 minutes per resource with this template!
