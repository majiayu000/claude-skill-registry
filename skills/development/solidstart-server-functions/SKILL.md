---
name: solidstart-server-functions
description: "SolidStart server functions: 'use server' directive (function/file level), use with queries/actions, single-flight mutations, secure database access."
metadata:
  globs:
    - "**/*server*"
    - "**/lib/**/*"
---

# SolidStart Server Functions

Server functions must be `async` or return a Promise. They run exclusively on the server.

## Function-Level Directive

```tsx
async function getData(id: string) {
  "use server";
  // Only runs on server
  return await db.getData(id);
}

// Can be used in client code
const data = await getData("123");
```

## File-Level Directive

```tsx
"use server";

// All functions in this file are server-only
async function getData(id: string) {
  return await db.getData(id);
}

async function updateData(id: string, data: any) {
  return await db.updateData(id, data);
}
```

## With Queries

```tsx
import { query } from "@solidjs/router";

const getUserQuery = query(async (id: string) => {
  "use server";
  const session = await useSession();
  if (!session.data.userId) {
    throw redirect("/login");
  }
  return await db.users.get({ id });
}, "user");

// In component
import { createAsync } from "@solidjs/router";

function Profile({ userId }: { userId: string }) {
  const user = createAsync(() => getUserQuery(userId));
  return <div>{user()?.name}</div>;
}
```

## With Actions

```tsx
import { action, redirect } from "@solidjs/router";

const updateUserAction = action(async (id: string, formData: FormData) => {
  "use server";
  const name = formData.get("name")?.toString();
  await db.updateUser(id, { name });
  throw redirect(`/users/${id}`);
}, "updateUser");

// In component
import { useAction } from "@solidjs/router";

function EditUser({ userId }: { userId: string }) {
  const updateUser = useAction(updateUserAction);
  
  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    await updateUser(userId, formData);
  };
  
  return <form onSubmit={handleSubmit}>...</form>;
}
```

## Single-Flight Mutations

When action updates data and redirects, SolidStart fetches redirected page data in same request:

```tsx
const updateProductAction = action(async (id: string, formData: FormData) => {
  "use server";
  await db.updateProduct(id, formData);
  throw redirect(`/products/${id}`); // Server handles efficiently
}, "updateProduct");

// Route with preload
export const route = {
  preload: ({ params }) => getProductQuery(params.id)
} satisfies RouteDefinition;
```

## Data Fetching Patterns

```tsx
import { query, createAsync } from "@solidjs/router";

const getProducts = query(async (category: string) => {
  "use server";
  return await db.getProducts({ category });
}, "products");

function ProductList({ category }: { category: string }) {
  const products = createAsync(() => getProducts(category));
  
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <For each={products()}>
        {(product) => <div>{product.name}</div>}
      </For>
    </Suspense>
  );
}
```

## Best Practices

1. Use server functions for data access - keeps API keys and database secure
2. Server functions for internal data (database access, internal operations)
3. Use with queries for read operations
4. Use with actions for mutations
5. Always mark async functions that run on server
6. Can be called from client - automatically transformed to RPC calls

