---
name: types-gen
description: "Generate TypeScript types from Supabase database schema"
---

# Generate Supabase Types

Generate TypeScript types from the Supabase database schema.

## Command

Run the following command to generate types:

```bash
npx supabase gen types typescript --project-id YOUR_PROJECT_ID > lib/database.types.ts
```

Or if using local Supabase:

```bash
npx supabase gen types typescript --local > lib/database.types.ts
```

## Setup for Auto-Generation

### 1. **Add to package.json**

```json
{
  "scripts": {
    "gen-types": "npx supabase gen types typescript --project-id $SUPABASE_PROJECT_ID > lib/database.types.ts",
    "gen-types:local": "npx supabase gen types typescript --local > lib/database.types.ts"
  }
}
```

### 2. **Usage in Code**

```typescript
import type { Database } from '@/lib/database.types'

// Get table type
type User = Database['public']['Tables']['users']['Row']
type UserInsert = Database['public']['Tables']['users']['Insert']
type UserUpdate = Database['public']['Tables']['users']['Update']

// Use with Supabase client
const supabase = createClient<Database>(url, key)

// Type-safe queries
const { data } = await supabase
  .from('users')
  .select('*')
  .single()  // data is typed as User

// Type-safe inserts
const { data } = await supabase
  .from('users')
  .insert({
    email: 'user@example.com',
    name: 'John Doe'
  })  // TypeScript validates the shape
```

### 3. **Create Utility Types**

```typescript
// lib/database.helpers.ts
import type { Database } from './database.types'

// Extract table types
export type Tables<T extends keyof Database['public']['Tables']> =
  Database['public']['Tables'][T]['Row']

export type Enums<T extends keyof Database['public']['Enums']> =
  Database['public']['Enums'][T]

// Usage
import type { Tables } from '@/lib/database.helpers'
type User = Tables<'users'>
type Post = Tables<'posts'>
```

### 4. **When to Regenerate**

Run `npm run gen-types` after:
- Creating new tables
- Adding/removing columns
- Changing column types
- Modifying RLS policies
- Adding enums

### 5. **Best Practices**

- Commit generated types to git
- Run after schema changes
- Use in all Supabase queries
- Create helper types for common patterns
- Keep types file in `lib/` or `types/`
- Don't manually edit generated file
- Don't use `any` instead of generated types

### 6. **Integration with Pre-commit Hook**

```bash
# .husky/pre-commit
#!/bin/sh
npm run gen-types
git add lib/database.types.ts
```

## Troubleshooting

**Issue**: `supabase` command not found
```bash
npm install -g supabase
```

**Issue**: Missing project ID
```bash
# Find your project ID in Supabase dashboard
# Or set in .env
SUPABASE_PROJECT_ID=your-project-id
```

**Issue**: Types not updating
```bash
# Clear cache and regenerate
rm lib/database.types.ts
npm run gen-types
```

Generate and use TypeScript types to catch database-related bugs at compile time instead of runtime.
