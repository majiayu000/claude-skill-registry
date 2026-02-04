---
name: treido-supabase
description: Manage Treido's Supabase database including schema design, migrations, Row Level Security (RLS) policies, storage buckets, and auth configuration. Use when working on database tables, columns, indexes, RLS policies, storage rules, or auth providers. Triggers include schema changes, security policy updates, migration creation, or Supabase-related debugging.
deprecated: true
---

# Treido Supabase

> Deprecated (2026-01-29). Use `treido-audit-supabase` (audit) + `treido-impl-backend` (implementation), coordinated by `treido-orchestrator`.

## Quick Start

1. Identify what needs to change (schema, RLS, storage, auth)
2. Create a migration file in `supabase/migrations/`
3. Test locally: `supabase db reset`
4. Verify RLS policies work as expected

## Decision Tree

```
What are you modifying?
├─ Table schema → Create migration in supabase/migrations/
├─ RLS policies → Add to same migration or separate policy migration
├─ Storage bucket → supabase/config.toml or migration
├─ Auth settings → supabase/config.toml
├─ Edge functions → supabase/functions/
└─ App code using Supabase → Wrong skill. Use treido-backend
```

## File Structure

```
supabase/
├── config.toml           # Local Supabase config
├── migrations/           # SQL migrations (timestamped)
│   ├── 20240101000000_initial_schema.sql
│   ├── 20240102000000_add_products.sql
│   └── 20240103000000_add_rls_policies.sql
├── functions/            # Edge functions (Deno)
└── seed.sql              # Development seed data
```

## Migration Naming

Use timestamp prefix: `YYYYMMDDHHMMSS_description.sql`

```bash
# Generate timestamp
date +%Y%m%d%H%M%S
# Output: 20260130123456

# Migration filename
20260130123456_add_seller_profiles.sql
```

## Schema Patterns

### Basic Table
```sql
-- supabase/migrations/20260130000000_add_products.sql

create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null,
  seller_id uuid references auth.users(id) on delete cascade not null,
  title text not null,
  description text,
  price numeric(10,2) not null check (price >= 0),
  status text default 'draft' check (status in ('draft', 'active', 'sold', 'archived'))
);

-- Index for common queries
create index products_seller_id_idx on public.products(seller_id);
create index products_status_idx on public.products(status) where status = 'active';

-- Updated at trigger
create trigger set_updated_at
  before update on public.products
  for each row
  execute function public.set_updated_at();
```

### Junction Table (Many-to-Many)
```sql
create table if not exists public.product_categories (
  product_id uuid references public.products(id) on delete cascade,
  category_id uuid references public.categories(id) on delete cascade,
  primary key (product_id, category_id)
);
```

## Row Level Security (RLS)

### Enable RLS (Required)
```sql
alter table public.products enable row level security;
```

### Common Policy Patterns

**Public Read**
```sql
create policy "Anyone can view active products"
  on public.products for select
  using (status = 'active');
```

**Owner Read/Write**
```sql
create policy "Users can view own products"
  on public.products for select
  using (auth.uid() = seller_id);

create policy "Users can insert own products"
  on public.products for insert
  with check (auth.uid() = seller_id);

create policy "Users can update own products"
  on public.products for update
  using (auth.uid() = seller_id)
  with check (auth.uid() = seller_id);

create policy "Users can delete own products"
  on public.products for delete
  using (auth.uid() = seller_id);
```

**Admin Access**
```sql
create policy "Admins can do anything"
  on public.products for all
  using (
    exists (
      select 1 from public.user_roles
      where user_id = auth.uid() and role = 'admin'
    )
  );
```

## Storage Bucket Policies

```sql
-- Create bucket (if not in config.toml)
insert into storage.buckets (id, name, public)
values ('product-images', 'product-images', true);

-- Allow authenticated users to upload
create policy "Users can upload product images"
  on storage.objects for insert
  with check (
    bucket_id = 'product-images' and
    auth.role() = 'authenticated'
  );

-- Allow public read
create policy "Anyone can view product images"
  on storage.objects for select
  using (bucket_id = 'product-images');
```

## Query Optimization

### Field Projection (Always)
```tsx
// ❌ FORBIDDEN in hot paths
const { data } = await supabase.from('products').select('*');

// ✅ CORRECT - explicit fields
const { data } = await supabase
  .from('products')
  .select('id, title, price, images');
```

### Use Indexes
```sql
-- For frequently filtered columns
create index products_category_idx on public.products(category_id);

-- For text search
create index products_title_trgm_idx on public.products 
  using gin (title gin_trgm_ops);

-- Partial index for common filters
create index products_active_idx on public.products(created_at desc) 
  where status = 'active';
```

### Pagination
```tsx
// ✅ Use range-based pagination
const { data } = await supabase
  .from('products')
  .select('id, title, price')
  .eq('status', 'active')
  .order('created_at', { ascending: false })
  .range(0, 19); // First 20 items
```

## Local Development

```bash
# Start local Supabase
supabase start

# Reset database (runs all migrations)
supabase db reset

# Create new migration
supabase migration new add_feature_name

# Generate types
supabase gen types typescript --local > lib/database.types.ts
```

## Verification

After schema changes:

```bash
# Reset and verify migrations run cleanly
supabase db reset

# Generate types
supabase gen types typescript --local > lib/database.types.ts

# Run type check
pnpm -s typecheck
```

## References

**For RLS patterns:** See [references/rls.md](references/rls.md)
**For schema conventions:** See [references/schema.md](references/schema.md)
