---
name: nextjs-module-builder
description: Complete workflow for building new modules in Next.js 15 (App Router) with Supabase backend. Use when creating CRUD features, data management modules, or any new feature module following the 5-layer architecture (Types → Services → Hooks → Components → Pages). Covers TypeScript types, Supabase services, React hooks, Shadcn/UI components, and permission-based routing.
---

# Next.js Module Builder

Build complete feature modules following MyJKKN's standardized 5-layer architecture for Next.js 15 + Supabase applications.

## Architecture Overview

Every module follows a strict 5-layer pattern:

1. **Types Layer** (`types/`) - TypeScript interfaces and DTOs
2. **Service Layer** (`lib/services/`) - Supabase database operations and business logic
3. **Hooks Layer** (`hooks/`) - React state management and data fetching
4. **Components Layer** (`_components/`) - Reusable UI components with Shadcn/UI
5. **Pages Layer** (`app/(routes)/`) - Route handlers with Server Components

## Workflow Decision Tree

**Start here** for every new module:

1. Is database schema defined?

   - NO → Read `references/database-patterns.md` and create schema first
   - YES → Continue to step 2

2. Are TypeScript types needed?

   - YES → Follow **Step 1: Types Layer** below
   - NO → Skip to step 3

3. Need database operations?

   - YES → Follow **Step 2: Service Layer** below
   - NO → Skip to step 4

4. Need state management?

   - YES → Follow **Step 3: Hooks Layer** below
   - NO → Skip to step 5

5. Need UI components?

   - YES → Follow **Step 4: Components Layer** below
   - NO → Skip to step 6

6. Need pages/routes?

   - YES → Follow **Step 5: Pages Layer** below
   - Then proceed to step 7

7. Configure permissions
   - Follow **Step 6: Permissions & Navigation**

## Step 1: Types Layer (20-30 min)

Create `types/[module-name].ts` with these interfaces:

```typescript
// Main entity interface - include ALL database fields
export interface Entity {
  id: string;
  institution_id: string;
  name: string;
  // ... your entity fields
  is_active: boolean;
  created_at: string;
  updated_at: string;
  created_by?: string;
  updated_by?: string;
}

// Create DTO - only fields user provides
export interface CreateEntityDto {
  institution_id: string;
  name: string;
  // ... only user-provided fields
}

// Update DTO - all fields optional except id
export interface UpdateEntityDto {
  id: string;
  name?: string;
  // ... optional update fields
  is_active?: boolean;
}

// Filter interface - for search and filtering
export interface EntityFilters {
  institution_id?: string;
  search?: string;
  is_active?: boolean;
  // ... filter fields
}

// Response interface - for paginated lists
export interface EntityResponse {
  data: Entity[];
  total: number;
  page: number;
  pageSize: number;
}
```

**Detailed patterns:** See `references/typescript-patterns.md`

## Step 2: Service Layer (45-60 min)

Create `lib/services/[module]/[entity]-service.ts`:

```typescript
import { createClientSupabaseClient } from '@/lib/supabase/client';
import type { CreateEntityDto, UpdateEntityDto, EntityFilters } from '@/types/[module]';

export class EntityService {
  private static supabase = createClientSupabaseClient();

  // GET with pagination and filters
  static async getEntities(filters: EntityFilters = {}, page = 1, pageSize = 10) {
    try {
      let query = this.supabase.from('entities').select('*', { count: 'exact' });

      // Apply filters
      if (filters.institution_id) {
        query = query.eq('institution_id', filters.institution_id);
      }
      if (filters.search) {
        query = query.ilike('name', `%${filters.search}%`);
      }
      if (filters.is_active !== undefined) {
        query = query.eq('is_active', filters.is_active);
      }

      // Pagination
      const from = (page - 1) * pageSize;
      const to = from + pageSize - 1;
      query = query.range(from, to);

      const { data, error, count } = await query;
      if (error) throw error;

      return { data: data || [], total: count || 0, page, pageSize };
    } catch (error) {
      console.error('[module/entity] Error fetching:', error);
      throw error;
    }
  }

  // GET by ID
  static async getEntityById(id: string) {
    try {
      const { data, error } = await this.supabase
        .from('entities')
        .select('*')
        .eq('id', id)
        .single();

      if (error) throw error;
      return data;
    } catch (error) {
      console.error('[module/entity] Error fetching by ID:', error);
      throw error;
    }
  }

  // CREATE
  static async createEntity(dto: CreateEntityDto) {
    try {
      const { data, error } = await this.supabase
        .from('entities')
        .insert([dto])
        .select()
        .single();

      if (error) throw error;
      console.log('[module/entity] Created:', data.id);
      return data;
    } catch (error) {
      console.error('[module/entity] Error creating:', error);
      throw error;
    }
  }

  // UPDATE
  static async updateEntity(dto: UpdateEntityDto) {
    try {
      const { id, ...updates } = dto;
      const { data, error } = await this.supabase
        .from('entities')
        .update(updates)
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      console.log('[module/entity] Updated:', id);
      return data;
    } catch (error) {
      console.error('[module/entity] Error updating:', error);
      throw error;
    }
  }

  // DELETE (soft delete recommended)
  static async deleteEntity(id: string) {
    try {
      // Soft delete: set is_active = false
      const { error } = await this.supabase
        .from('entities')
        .update({ is_active: false })
        .eq('id', id);

      if (error) throw error;
      console.log('[module/entity] Deleted:', id);
      return true;
    } catch (error) {
      console.error('[module/entity] Error deleting:', error);
      throw error;
    }
  }
}
```

**Detailed patterns:** See `references/service-patterns.md`

## Step 3: Hooks Layer (30-45 min)

Create `hooks/[module]/use-[entity].ts`:

```typescript
'use client';

import { useState, useEffect, useCallback } from 'react';
import { EntityService } from '@/lib/services/[module]/[entity]-service';
import type { Entity, EntityFilters } from '@/types/[module]';
import { usePermissions } from '@/hooks/use-permissions';

export function useEntities(filters: EntityFilters = {}) {
  const [entities, setEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const { userProfile } = usePermissions();

  const fetchEntities = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Auto-apply institution filter
      const effectiveFilters = {
        ...filters,
        institution_id: filters.institution_id || userProfile?.institution_id
      };

      const response = await EntityService.getEntities(
        effectiveFilters,
        page,
        pageSize
      );

      setEntities(response.data);
      setTotal(response.total);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch';
      setError(message);
      console.error('[hooks/entity] Fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [filters, page, userProfile?.institution_id]);

  useEffect(() => {
    fetchEntities();
  }, [fetchEntities]);

  return {
    entities,
    loading,
    error,
    total,
    page,
    setPage,
    pageSize,
    refetch: fetchEntities
  };
}
```

**Detailed patterns:** See `references/hooks-patterns.md`

## Step 4: Components Layer (90-120 min)

**Required components** in `app/(routes)/[module]/_components/`:

1. `data-table-schema.ts` - Zod validation schema
2. `columns.tsx` - TanStack Table column definitions
3. `[entity]-data-table.tsx` - Data table wrapper component
4. `[entity]-form.tsx` - Create/Edit form with React Hook Form
5. `[entity]-filters.tsx` - Search and filter controls
6. `row-actions.tsx` - Edit/Delete action menu

**Complete component code examples:** See `references/component-patterns.md`

## Step 5: Pages Layer (45-60 min)

**Required pages:**

1. `page.tsx` - List view with filters and data table
2. `new/page.tsx` - Create form page
3. `[id]/edit/page.tsx` - Edit form page
4. `[id]/page.tsx` - Detail view page (optional)

Each page must include:

- `ContentLayout` wrapper
- `Breadcrumb` navigation
- `PermissionGuard` for access control
- Proper error handling and loading states

**Complete page code examples:** See `references/page-patterns.md`

## Step 6: Permissions & Navigation (20-30 min)

### 1. Define Permissions

Add to `lib/sidebarMenuLink.ts`:

```typescript
export const MENU_PERMISSIONS = {
  '[module].[entity].view': ['super_admin', 'admin', 'faculty'],
  '[module].[entity].create': ['super_admin', 'admin'],
  '[module].[entity].edit': ['super_admin', 'admin'],
  '[module].[entity].delete': ['super_admin'],
};
```

### 2. Add Menu Item

```typescript
{
  groupLabel: 'Module',
  menus: [
    {
      label: 'Entities',
      href: '/[module]/entities',
      permission: '[module].[entity].view'
    }
  ]
}
```

### 3. Apply Guards

```typescript
<PermissionGuard module="[module].[entity]" action="create">
  <Button>Create</Button>
</PermissionGuard>

// Or use shorthand components
<CanCreate module="[module].[entity]">
  <Button>Create</Button>
</CanCreate>
```

**Complete permission setup:** See `references/permission-patterns.md`

## File Structure

```
app/(routes)/[module]/
├── page.tsx                    # List view
├── new/page.tsx               # Create form
├── [id]/
│   ├── page.tsx              # Detail view (optional)
│   └── edit/page.tsx         # Edit form
└── _components/
    ├── data-table-schema.ts
    ├── columns.tsx
    ├── [entity]-data-table.tsx
    ├── [entity]-form.tsx
    ├── [entity]-filters.tsx
    └── row-actions.tsx

lib/services/[module]/
└── [entity]-service.ts

hooks/[module]/
└── use-[entity].ts

types/
└── [module].ts
```

## Development Standards

### Naming Conventions

- **Files**: `kebab-case` (entity-name.tsx)
- **Components**: `PascalCase` (EntityForm)
- **Functions**: `camelCase` (fetchEntities)
- **Types**: `PascalCase` (CreateEntityDto)
- **Hooks**: `use` prefix (useEntities)
- **Services**: `Service` suffix (EntityService)

### Logging Format

Always use module prefix:

```typescript
console.log('[module/entity] Action completed:', details);
console.warn('[module/entity] Validation warning:', data);
console.error('[module/entity] Error occurred:', error);
```

### TypeScript Rules

- Use strict mode (no implicit any)
- No `any` types - use `unknown` with type guards
- Explicit return types on service methods
- Use DTOs for all API boundaries
- Interfaces over types for extensibility

### Error Handling

- Try-catch in all service methods
- User-friendly messages in UI (toast notifications)
- Console errors with module prefix for debugging
- Graceful degradation for failed operations

## Quality Checklist

Before marking module as complete:

- [ ] All TypeScript types are strict (no `any`)
- [ ] Service methods have proper error handling
- [ ] RLS policies tested in Supabase dashboard
- [ ] All CRUD operations tested manually
- [ ] Permissions applied to all pages and actions
- [ ] Loading states display correctly
- [ ] Error messages are user-friendly
- [ ] Console logs use correct module prefix
- [ ] Navigation flows logically between pages
- [ ] Mobile responsive (test on small screens)
- [ ] Forms validate inputs correctly
- [ ] Data table pagination works
- [ ] Search and filters function properly

## Time Estimates

- **Database Setup**: 30-45 minutes
- **Types Layer**: 20-30 minutes
- **Service Layer**: 45-60 minutes
- **Hooks Layer**: 30-45 minutes
- **Components Layer**: 90-120 minutes
- **Pages Layer**: 45-60 minutes
- **Permissions**: 20-30 minutes
- **Testing**: 30-45 minutes

**Total**: 5-7 hours for a complete module

## Reference Files

For detailed implementation patterns and complete code examples:

- `references/architecture-patterns.md` - Overall architecture and design patterns
- `references/database-patterns.md` - Database schema, indexes, and RLS policies
- `references/typescript-patterns.md` - Type definitions and DTO patterns
- `references/service-patterns.md` - Service layer with complex queries
- `references/hooks-patterns.md` - Custom hooks with advanced patterns
- `references/component-patterns.md` - Complete UI component examples
- `references/page-patterns.md` - Page structure with all routing patterns
- `references/permission-patterns.md` - Permission system integration
