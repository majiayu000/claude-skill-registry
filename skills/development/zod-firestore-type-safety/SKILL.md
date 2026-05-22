---
name: zod-firestore-type-safety
description: |
  End-to-end type safety for Firestore using Zod schemas with withConverter API. Includes runtime validation,
  type inference, schema evolution, and error handling patterns for both client and server SDKs.
  Keywords: "zod", "type safety", "validation", "converter", "schema", "runtime", "firestore"
---

# Zod Firestore Type Safety

## Overview

Firestore is schemaless, creating a mismatch with TypeScript's compile-time types. Zod bridges this gap by providing runtime validation at the application boundary, ensuring data integrity.

## Core Pattern: Zod + withConverter

### The Atomic Unit

Every Firestore collection requires three components:

1. **Zod Schema**: Runtime validation definition
2. **TypeScript Type**: Inferred from Zod schema
3. **Converters**: Client and server withConverter objects

**Template**:
```typescript
import { z } from 'zod';
import { Timestamp } from 'firebase/firestore';

// 1. Zod Schema
export const UserSchema = z.object({
  id: z.string(),
  name: z.string().min(1, 'Name required').max(100),
  email: z.string().email('Invalid email'),
  role: z.enum(['admin', 'user', 'moderator']),
  age: z.number().int().positive().optional(),
  createdAt: z.instanceof(Timestamp),
  updatedAt: z.instanceof(Timestamp),
});

// 2. Inferred TypeScript Type
export type User = z.infer<typeof UserSchema>;

// 3. Converters (import from shared utility)
import { zodConverter, zodAdminConverter } from '@/lib/firebase/zodConverter';

export const userConverter = zodConverter(UserSchema);
export const userAdminConverter = zodAdminConverter(UserSchema);
```

### Generic Zod Converter Implementation

```typescript
// lib/firebase/zodConverter.ts
import type {
  DocumentData,
  FirestoreDataConverter,
  QueryDocumentSnapshot,
  SnapshotOptions,
  WithFieldValue,
} from 'firebase/firestore';
import type { ZodSchema } from 'zod';

/**
 * Client-side converter with validation on read and write
 * Automatically injects document ID and ref
 */
export function zodConverter<T extends DocumentData>(
  schema: ZodSchema<T>
): FirestoreDataConverter<T> {
  return {
    toFirestore(data: WithFieldValue<T>): DocumentData {
      // Validate before writing to Firestore
      const validated = schema.parse(data);
      return validated;
    },
    fromFirestore(
      snapshot: QueryDocumentSnapshot<DocumentData>,
      options?: SnapshotOptions
    ): T {
      const data = snapshot.data(options);

      // Inject document metadata for convenience
      const dataWithMeta = {
        ...data,
        id: snapshot.id,
        ref: snapshot.ref,
      };

      // Validate after reading from Firestore
      return schema.parse(dataWithMeta) as T;
    },
  };
}

/**
 * Server-side converter (Admin SDK)
 * Validates on read, optional validation on write
 */
export function zodAdminConverter<T extends DocumentData>(
  schema: ZodSchema<T>,
  validateWrites = false // Server code is trusted, skip write validation by default
): FirestoreDataConverter<T> {
  return {
    toFirestore(data: WithFieldValue<T>): DocumentData {
      if (validateWrites) {
        return schema.parse(data);
      }
      return data as DocumentData;
    },
    fromFirestore(snapshot: QueryDocumentSnapshot<DocumentData>): T {
      const data = snapshot.data();
      const dataWithMeta = {
        ...data,
        id: snapshot.id,
        ref: snapshot.ref,
      };
      return schema.parse(dataWithMeta) as T;
    },
  };
}
```

## Usage Examples

### Client-Side (React Component)

```typescript
'use client';

import { collection, doc, getDoc, getDocs, query, where } from 'firebase/firestore';
import { db } from '@/lib/firebase/client';
import { userConverter, type User } from '@/lib/firebase/schemas/user.schema';

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    async function fetchUser() {
      // Use withConverter for type-safe, validated read
      const userRef = doc(db, 'users', userId).withConverter(userConverter);
      const userDoc = await getDoc(userRef);

      if (userDoc.exists()) {
        const userData = userDoc.data(); // Type: User (validated!)
        setUser(userData);
      }
    }
    fetchUser();
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

### Server-Side (Next.js Server Component)

```typescript
// app/users/page.tsx
import { adminDb } from '@/lib/firebase/admin';
import { userAdminConverter, type User } from '@/lib/firebase/schemas/user.schema';

export default async function UsersPage() {
  // Use Admin SDK with converter in Server Component
  const usersSnapshot = await adminDb
    .collection('users')
    .withConverter(userAdminConverter)
    .where('role', '==', 'admin')
    .get();

  const users: User[] = usersSnapshot.docs.map(doc => doc.data()); // Type: User[]

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### Server Action (Mutation)

```typescript
// app/actions/updateUser.ts
'use server';

import { adminDb } from '@/lib/firebase/admin';
import { UserSchema, userAdminConverter } from '@/lib/firebase/schemas/user.schema';
import { z } from 'zod';

// Validation schema for update input
const UpdateUserInput = UserSchema.pick({
  name: true,
  email: true,
}).partial(); // All fields optional

export async function updateUser(
  userId: string,
  updates: z.infer<typeof UpdateUserInput>
) {
  // Validate input
  const validated = UpdateUserInput.parse(updates);

  // Write with converter (validation optional for server-side)
  const userRef = adminDb
    .collection('users')
    .doc(userId)
    .withConverter(userAdminConverter);

  await userRef.update({
    ...validated,
    updatedAt: new Date(),
  });

  return { success: true };
}
```

## Schema Evolution Best Practices

### Adding Optional Fields

When evolving schemas, mark new fields as optional or provide defaults:

```typescript
// Initial schema
export const PostSchema = z.object({
  title: z.string(),
  content: z.string(),
  createdAt: z.instanceof(Timestamp),
});

// Evolution: Add optional viewCount field
export const PostSchema = z.object({
  title: z.string(),
  content: z.string(),
  createdAt: z.instanceof(Timestamp),
  viewCount: z.number().int().nonnegative().default(0), // Default prevents validation errors on old docs
});
```

**Why**: Old documents without `viewCount` will validate successfully with the default value.

### Handling Breaking Changes

If you must make a breaking change (e.g., rename field), migrate data first:

```typescript
// Before: { email: "alice@example.com" }
// After:  { emailAddress: "alice@example.com" }

// Step 1: Make both fields optional during migration
export const UserSchema = z.object({
  email: z.string().email().optional(),
  emailAddress: z.string().email().optional(),
}).refine(
  data => data.email || data.emailAddress,
  'Either email or emailAddress required'
);

// Step 2: Run migration script to copy email → emailAddress
// Step 3: Remove old field from schema
```

## Zod Validation Patterns

### String Validation

```typescript
z.string().min(1, 'Required') // Non-empty
z.string().max(200, 'Too long')
z.string().email('Invalid email')
z.string().url('Invalid URL')
z.string().regex(/^[A-Z]{3}$/, 'Must be 3 uppercase letters')
z.string().uuid()
z.string().trim() // Remove whitespace
z.string().toLowerCase() // Normalize case
```

### Number Validation

```typescript
z.number().int() // Integer only
z.number().positive() // > 0
z.number().nonnegative() // >= 0
z.number().min(0).max(100) // Range
z.number().multipleOf(5) // Divisible by 5
```

### Enum Validation

```typescript
z.enum(['draft', 'published', 'archived']) // Must be one of these
z.nativeEnum(MyEnum) // TypeScript enum
```

### Array Validation

```typescript
z.array(z.string()) // Array of strings
z.array(z.string()).min(1, 'At least one item') // Non-empty
z.array(z.string()).max(10, 'Max 10 items')
z.array(z.string()).nonempty() // Alias for min(1)
```

### Object Validation

```typescript
// Required fields
z.object({
  name: z.string(),
  age: z.number(),
})

// Optional fields
z.object({
  name: z.string(),
  age: z.number().optional(),
})

// Partial (all fields optional)
UserSchema.partial()

// Pick specific fields
UserSchema.pick({ name: true, email: true })

// Omit fields
UserSchema.omit({ password: true })
```

### Timestamps

```typescript
import { Timestamp } from 'firebase/firestore';

// Firestore Timestamp
z.instanceof(Timestamp)

// JavaScript Date (convert to Timestamp on write)
z.date().transform(date => Timestamp.fromDate(date))
```

### References

```typescript
import { DocumentReference } from 'firebase/firestore';

// Firestore reference
z.instanceof(DocumentReference)

// Or just store the path as string
z.string().regex(/^[^/]+\/[^/]+$/, 'Invalid ref path')
```

## Error Handling

### Validation Errors

```typescript
import { z } from 'zod';

try {
  const user = UserSchema.parse(data);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error('Validation errors:', error.errors);

    // Format for UI display
    const formattedErrors = error.flatten().fieldErrors;
    // { name: ["Name required"], email: ["Invalid email"] }
  }
}
```

### Safe Parse (No Throw)

```typescript
const result = UserSchema.safeParse(data);

if (result.success) {
  const user = result.data; // Type: User
} else {
  const errors = result.error.flatten().fieldErrors;
}
```

## Anti-Patterns

❌ **Skipping Converter**:
```typescript
// BAD: No runtime validation
const userDoc = await getDoc(doc(db, 'users', userId));
const user = userDoc.data(); // Type: any
```

✅ **Using Converter**:
```typescript
// GOOD: Type-safe + validated
const userDoc = await getDoc(doc(db, 'users', userId).withConverter(userConverter));
const user = userDoc.data(); // Type: User (validated)
```

❌ **Using `any` Type**:
```typescript
// BAD
const data: any = snapshot.data();
```

✅ **Using `unknown` with Validation**:
```typescript
// GOOD
const data: unknown = snapshot.data();
const validated = UserSchema.parse(data);
```

❌ **Hardcoding Enum Values**:
```typescript
// BAD: Out of sync with schema
if (user.role === 'admin') { }
```

✅ **Using Zod Enum**:
```typescript
// GOOD: Single source of truth
export const RoleSchema = z.enum(['admin', 'user', 'moderator']);
export type Role = z.infer<typeof RoleSchema>;

if (user.role === 'admin') { } // Type-safe
```

## Best Practices Summary

✅ **Do**:
- Always use `z.infer<typeof Schema>` for types
- Mark new fields as optional when evolving schemas
- Use `.default()` for fields that should have fallback values
- Validate on both read and write for client SDK
- Use `.safeParse()` for user input validation
- Define enums in Zod schema (single source of truth)

❌ **Don't**:
- Skip runtime validation with converters
- Use `any` type (use `unknown` with validation)
- Make breaking schema changes without migration
- Hardcode validation logic outside Zod schema
- Forget to handle validation errors gracefully

---

**Related Skills**: `firestore-data-modeling-patterns`, `firebase-nextjs-integration-strategies`
**Token Estimate**: ~1,400 tokens
