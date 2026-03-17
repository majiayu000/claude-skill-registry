---
name: effect-frontend-patterns
description: Effect TypeScript patterns for frontend development including Schema validation, TanStack Query integration, forms, and WebSocket streams.
agents: [blaze]
triggers: [effect typescript, schema validation, tanstack query, websocket stream, form validation, type-safe error]
---

# Effect TypeScript for Frontend

**Effect** is the missing standard library for TypeScript. Use it for type-safe error handling, validation, and data fetching in frontend applications.

## Documentation

Before implementing, consult:
- **AI Documentation**: `https://effect.website/llms.txt`
- **Main Docs**: `https://effect.website/docs`

Use Context7:
```
resolve_library_id({ libraryName: "effect typescript" })
get_library_docs({ context7CompatibleLibraryID: "/effect-ts/effect", topic: "schema validation" })
```

## Effect Schema (Replaces Zod)

```typescript
import { Schema } from "effect"

// Define schemas
const UserSchema = Schema.Struct({
  id: Schema.String,
  name: Schema.String.pipe(Schema.minLength(1), Schema.maxLength(100)),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  role: Schema.Literal("admin", "user", "guest"),
  createdAt: Schema.Date,
})
type User = Schema.Schema.Type<typeof UserSchema>

// Form validation schema
const CreateUserSchema = Schema.Struct({
  name: Schema.String.pipe(Schema.minLength(1), Schema.maxLength(100)),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  password: Schema.String.pipe(Schema.minLength(8)),
})

// Validate unknown data
const parseUser = Schema.decodeUnknown(UserSchema)
```

## Effect + TanStack Query

```typescript
import { Effect, Schema } from "effect"
import { useQuery, useMutation } from "@tanstack/react-query"

// Type-safe API error
class ApiError extends Schema.TaggedError<ApiError>("ApiError")({
  message: Schema.String,
  statusCode: Schema.Number,
}) {}

// Effect-powered fetch with validation
const fetchUsers = Effect.tryPromise({
  try: () => fetch("/api/users").then((r) => r.json()),
  catch: () => new ApiError({ message: "Network error", statusCode: 500 }),
}).pipe(
  Effect.flatMap(Schema.decodeUnknown(Schema.Array(UserSchema))),
  Effect.catchTag("ParseError", (e) => 
    Effect.fail(new ApiError({ message: "Invalid response", statusCode: 422 }))
  )
)

// React hook
function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: () => Effect.runPromise(fetchUsers),
  })
}

// Mutation with Effect
function useCreateUser() {
  return useMutation({
    mutationFn: (data: typeof CreateUserSchema.Type) =>
      Effect.runPromise(
        Effect.tryPromise({
          try: () => fetch("/api/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          }).then((r) => r.json()),
          catch: () => new ApiError({ message: "Failed to create user", statusCode: 500 }),
        }).pipe(Effect.flatMap(Schema.decodeUnknown(UserSchema)))
      ),
  })
}
```

## React Hook Form + Effect Schema

```typescript
import { useForm } from "react-hook-form"
import { effectTsResolver } from "@hookform/resolvers/effect-ts"
import { Schema } from "effect"

function CreateUserForm() {
  const form = useForm({
    resolver: effectTsResolver(CreateUserSchema),
    defaultValues: { name: "", email: "", password: "" },
  })

  return (
    <Form {...form}>
      <FormField
        control={form.control}
        name="name"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Name</FormLabel>
            <FormControl>
              <Input {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      {/* ... other fields */}
    </Form>
  )
}
```

## WebSocket with Effect Stream

```typescript
import { Effect, Stream, Schema, Fiber } from "effect"

// Define message schema
const NotificationSchema = Schema.Struct({
  id: Schema.String,
  type: Schema.Literal("info", "warning", "error"),
  message: Schema.String,
  timestamp: Schema.Date,
})

// Create WebSocket stream
const notificationStream = Stream.async<typeof NotificationSchema.Type, Error>((emit) => {
  const ws = new WebSocket("/api/ws/notifications")
  
  ws.onmessage = (event) => {
    const result = Schema.decodeUnknownSync(NotificationSchema)(JSON.parse(event.data))
    emit.single(result)
  }
  
  ws.onerror = () => emit.fail(new Error("WebSocket connection failed"))
  ws.onclose = () => emit.end()
  
  return Effect.sync(() => ws.close())
})

// React hook
function useNotificationStream(onNotification: (n: Notification) => void) {
  useEffect(() => {
    const fiber = Effect.runFork(
      Stream.runForEach(notificationStream, (notification) =>
        Effect.sync(() => onNotification(notification))
      )
    )
    return () => Effect.runSync(Fiber.interrupt(fiber))
  }, [onNotification])
}
```

## Context7 Topics to Query

```
get_library_docs({ context7CompatibleLibraryID: "/effect-ts/effect", topic: "schema validation" })
get_library_docs({ context7CompatibleLibraryID: "/effect-ts/effect", topic: "error handling tagged errors" })
get_library_docs({ context7CompatibleLibraryID: "/effect-ts/effect", topic: "stream async" })
```

## PRD → Component Mapping

| Requirement | Components | Effect Pattern |
|-------------|------------|----------------|
| "Login/signup" | `Form` + `Input` + **Better Auth** | Effect Schema validation |
| "Dashboard" | `Card` grid + `Chart` | Effect data fetching |
| "User list" | `Table` or `DataTable` | Effect + TanStack Query |
| "Settings" | `Tabs` with `Form` sections | Effect Schema forms |
| "Real-time updates" | WebSocket feed | Effect.Stream |
| "Search" | `Command` palette | Effect debounced search |
| "File upload" | Drag-drop zone | Effect error handling |
