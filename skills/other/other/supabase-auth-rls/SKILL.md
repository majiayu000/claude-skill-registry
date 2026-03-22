---
name: supabase-auth-rls
description: "Scaffold a Supabase project with database schema, Row Level Security policies, and auth integration. Use for: setting up RLS policies, debugging 'RLS not working', multi-tenant access control, auth.uid() patterns, team/org membership, profile triggers. Triggers: supabase, supabase rls, row level security, supabase auth, rls policy, supabase setup, supabase permissions, multi-tenant supabase, supabase project, rls not working."
---

# Supabase Auth + RLS Setup

Scaffold a Supabase project with properly designed database schema, Row Level Security (RLS) policies, and auth integration. This skill addresses the #1 developer pain point with Supabase — getting RLS right.

This skill is **reference-guided**. The agent uses bundled templates, patterns, and troubleshooting guides to configure the user's project — not to generate boilerplate from scratch.

## When to Use

- User wants to set up a new Supabase project with proper auth and RLS
- User is struggling with RLS policies ("RLS doesn't work", "can see all rows", "can't see any rows")
- User needs multi-tenant access control (team/org membership patterns)
- User wants to add RLS to existing tables
- User asks about `auth.uid()`, `auth.jwt()`, or auth helper functions
- User needs to debug permission issues in Supabase
- User wants to test RLS policies

## Tools Used

- `bash` — Run Supabase CLI commands (`supabase init`, `supabase start`, `supabase db reset`, `supabase gen types`)
- `ask_user_question` — Gather app requirements, confirm schema, approve policies
- `read` / `write` / `edit` — Create and modify migration files, config files
- `web_fetch` — Check Supabase docs if needed for version-specific details

## Bundled Files

```
supabase-auth-rls/
├── SKILL.md                          # This file (agent instructions)
├── README.md                         # Human-facing docs
├── references/
│   ├── rls-patterns.md               # 7 common RLS policy patterns with SQL
│   ├── auth-helpers.md               # auth.uid(), auth.jwt(), auth.role() reference
│   └── troubleshooting.md            # "RLS doesn't work" debugging checklist
└── templates/
    ├── migration-schema.sql          # Starter schema (profiles, orgs, members, projects, tasks)
    └── migration-rls.sql             # RLS policies matching the schema template
```

## Stopping Points

- ✋ Phase 0: User approves the workflow before any action
- ✋ Step 1: User confirms app type and access patterns
- ✋ Step 3: User reviews schema before applying migration
- ✋ Step 4: User reviews RLS policies before enabling
- ✋ Step 6: User confirms policies pass verification

---

## Phase 0: Briefing & Consent

**Goal:** Explain what this skill does and get explicit user approval before executing anything.

**⚠️ STOP:** This phase MUST be completed before ANY other action. Do not run any commands, read any files, or execute any tools until the user approves.

Present the following briefing to the user:

> ### Supabase Auth + RLS — What This Skill Does
>
> Row Level Security (RLS) is Supabase's authorization layer. When enabled, every database query is filtered by policies you define — users only see and modify data they're allowed to. Getting this wrong means either data leaks (too permissive) or broken apps (too restrictive).
>
> This skill walks you through setting up a Supabase project with:
>
> 1. **Database schema** with proper `auth.users` foreign keys and relationships
> 2. **RLS policies** tailored to your app's access patterns
> 3. **Auth integration** (profile triggers, JWT claims, helper functions)
> 4. **Verification** that policies work correctly
>
> **What will happen (7 steps):**
>
> 1. **Gather requirements** — what kind of app? who can see/edit what?
> 2. **Set up project** — initialize Supabase (CLI + local dev)
> 3. **Design schema** — tables, relationships, indexes
> 4. **Write RLS policies** — based on your access patterns
> 5. **Add auth integration** — profile trigger, custom claims if needed
> 6. **Verify policies** — test with simulated users
> 7. **Generate typed client** — TypeScript types from your schema
>
> **Prerequisites:** Node.js 18+, Docker (for Supabase local dev)
>
> Ready to proceed?

Wait for explicit user approval. If the user says no or wants to modify the plan, adjust accordingly.

---

## Workflow

### Step 1: Gather Requirements

**Goal:** Understand the app's access patterns to select the right RLS strategy.

Ask the user these questions (use `ask_user_question`):

1. **What kind of app is this?**
   - Personal data (users own their stuff — todos, notes, bookmarks)
   - Team/org SaaS (users belong to organizations/workspaces)
   - Public + private mix (some content public, some restricted)
   - Role-based (admin/editor/viewer access levels)

2. **What are the main data entities?** (e.g., "projects, tasks, comments")

3. **Who can see what?** Try to get the user to describe in plain English:
   - "Users can only see their own tasks"
   - "Team members can see all projects in their org, but only admins can create them"
   - "Published posts are public, drafts are only visible to the author"

4. **Is this a new project or adding RLS to existing tables?**

Based on answers, map to patterns from `references/rls-patterns.md`:
- Personal data → **Pattern 1** (user owns data)
- Team/org → **Pattern 2** (membership table)
- Public + private → **Pattern 3** (public read) + **Pattern 4** (published/draft)
- Role-based → **Pattern 5** (admin bypass) or **Pattern 7** (JWT claims)

**✋ STOP:** Confirm the selected patterns and access rules with the user before proceeding.

### Step 2: Set Up Supabase Project

**Goal:** Get a working Supabase project with local development running.

**If new project:**

```bash
# Check prerequisites
node --version    # Need 18+
docker --version  # Need Docker running
npx supabase --version  # Check CLI installed

# Initialize
mkdir <project-name> && cd <project-name>
npx supabase init

# Start local dev
npx supabase start
```

The `supabase start` output gives you local credentials:
- `API URL` — local Supabase URL
- `anon key` — client-side key (respects RLS)
- `service_role key` — server-side key (bypasses RLS)
- `DB URL` — direct Postgres connection

**If existing project:**

```bash
cd <project-directory>
npx supabase start   # Make sure local dev is running
npx supabase db reset # Reset to clean state if needed
```

Verify the project is running:
```bash
npx supabase status
```

### Step 3: Design and Apply Schema

**Goal:** Create tables with proper relationships, timestamps, and auth integration.

Read `templates/migration-schema.sql` as a starting point. Adapt it based on Step 1 requirements:

- Replace example tables (projects, tasks) with the user's actual entities
- Keep the patterns: UUID PKs, `auth.users` FKs, timestamps, `set_updated_at` trigger
- Keep the `profiles` table and `handle_new_user` trigger — almost every app needs this
- Keep the org membership pattern if the app is multi-tenant

Create the migration:
```bash
npx supabase migration new initial_schema
```

Write the adapted schema SQL to the generated migration file (in `supabase/migrations/`).

**✋ STOP:** Show the user the schema and get approval before applying.

Apply the migration:
```bash
npx supabase db reset
```

### Step 4: Write RLS Policies

**Goal:** Create policies that enforce the access rules from Step 1.

Read `references/rls-patterns.md` for the patterns identified in Step 1. Read `references/auth-helpers.md` for auth function usage.

Read `templates/migration-rls.sql` as a starting point. Adapt the policies to match the user's entities and access rules.

Create the RLS migration:
```bash
npx supabase migration new add_rls_policies
```

Write adapted RLS policies to the migration file.

**Key rules when writing policies:**

1. **Always enable RLS first:** `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`
2. **Every table needs a SELECT policy** — without one, no rows are visible
3. **UPDATE needs both USING and WITH CHECK** — USING selects rows, WITH CHECK validates the new values
4. **INSERT only uses WITH CHECK** — there's no existing row to filter
5. **DELETE only uses USING** — there's no new row to validate
6. **Avoid querying the same table in its own policy** — causes recursion. Use `SECURITY DEFINER` functions instead.
7. **Index columns used in policies** — `user_id`, `org_id`, membership lookups

**✋ STOP:** Show the user the policies and explain each one. Get approval before applying.

Apply:
```bash
npx supabase db reset
```

### Step 5: Add Auth Integration

**Goal:** Set up auth-related features beyond basic RLS.

This step covers:

1. **Profile trigger** (if not already in schema): Auto-create a profile row when a user signs up. See `references/auth-helpers.md` for the `handle_new_user` pattern.

2. **Custom claims** (if using JWT-based access): Set `app_metadata` for roles, subscription tiers, etc. This requires a server-side function:

```sql
-- Edge Function or server-side code sets this
-- Example: assign user to org during onboarding
CREATE OR REPLACE FUNCTION public.set_user_org_claim(user_uuid UUID, org_uuid UUID)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  UPDATE auth.users
  SET raw_app_meta_data = raw_app_meta_data || jsonb_build_object('org_id', org_uuid)
  WHERE id = user_uuid;
END;
$$;
```

3. **Auto-add org membership on org creation**: The creator should automatically become the owner.

```sql
-- Trigger to add creator as owner when org is created
CREATE OR REPLACE FUNCTION public.handle_new_org()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.org_members (org_id, user_id, role)
  VALUES (NEW.id, auth.uid(), 'owner');
  RETURN NEW;
END;
$$;

CREATE TRIGGER on_org_created
  AFTER INSERT ON public.organizations
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_org();
```

Only add what the user's app needs. Skip custom claims if using membership table lookups.

### Step 6: Verify Policies

**Goal:** Confirm RLS policies work correctly.

**Quick verification via SQL:**

```sql
-- Check RLS is enabled on all tables
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- List all policies
SELECT tablename, policyname, permissive, cmd FROM pg_policies WHERE schemaname = 'public';
```

**Test with simulated users:**

```sql
-- Create test data
INSERT INTO auth.users (id, email, encrypted_password, email_confirmed_at, raw_user_meta_data)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'alice@test.com', crypt('password', gen_salt('bf')), now(), '{"full_name": "Alice"}'),
  ('22222222-2222-2222-2222-222222222222', 'bob@test.com', crypt('password', gen_salt('bf')), now(), '{"full_name": "Bob"}');

-- Test as Alice
BEGIN;
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub": "11111111-1111-1111-1111-111111111111", "role": "authenticated", "email": "alice@test.com"}';

-- Should only see Alice's data
SELECT * FROM public.profiles;
SELECT * FROM public.organizations;  -- Only orgs Alice is a member of

ROLLBACK;

-- Test as Bob
BEGIN;
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub": "22222222-2222-2222-2222-222222222222", "role": "authenticated", "email": "bob@test.com"}';

-- Should only see Bob's data
SELECT * FROM public.profiles;

ROLLBACK;

-- Test as anonymous
BEGIN;
SET LOCAL ROLE anon;

-- Should see whatever your anon policies allow (maybe public profiles, maybe nothing)
SELECT * FROM public.profiles;

ROLLBACK;
```

For automated testing, use pgTAP — see `references/troubleshooting.md` for a pgTAP example.

**✋ STOP:** Confirm with the user that the verification results match expectations.

### Step 7: Generate Typed Client

**Goal:** Generate TypeScript types from the schema for type-safe client code.

```bash
npx supabase gen types typescript --local > src/database.types.ts
```

Show the user an example of using the types:

```typescript
import { createClient } from '@supabase/supabase-js';
import type { Database } from './database.types';

const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Fully typed — autocomplete on columns, type checking on inserts
const { data: tasks } = await supabase
  .from('tasks')
  .select('id, title, status, assigned_to')
  .eq('status', 'todo');
```

## Troubleshooting

If the user hits issues at any point, read `references/troubleshooting.md` for diagnostic steps.

| Symptom | Likely Cause | Reference |
|---------|-------------|-----------|
| Can see all rows | RLS not enabled, or using service_role key | troubleshooting.md — "I can see all rows" |
| Can't see any rows | Missing SELECT policy, or auth.uid() is NULL | troubleshooting.md — "I can't see any rows" |
| INSERT works but row disappears | SELECT policy filters out the inserted row | troubleshooting.md — "INSERT works but disappears" |
| Infinite recursion | Circular policy references between tables | troubleshooting.md — "Infinite recursion" |
| Slow queries | Missing indexes on policy columns | troubleshooting.md — "Performance Issues" |
| Works in SQL editor but not client | SQL editor uses postgres role (bypasses RLS) | troubleshooting.md — "Works in SQL editor" |

## Architecture Notes

- **RLS evaluates per-row.** Every SELECT, INSERT, UPDATE, DELETE checks the policy for each row. Keep policies simple and indexed.
- **`SECURITY DEFINER` functions** run as the function owner (postgres), bypassing RLS. Use them to break circular policy references or encapsulate complex access checks.
- **The `service_role` key bypasses ALL RLS.** Never expose it client-side. Use it only in Edge Functions and server routes.
- **JWT claims vs database lookups:** JWT claims are faster (no query) but stale until token refresh. Database lookups are always current but add query overhead. Use JWT claims for stable attributes (subscription tier), database lookups for dynamic attributes (team membership).
- **`auth.users` is in the `auth` schema.** Don't modify it directly except through Supabase's Admin API or `SECURITY DEFINER` functions. Reference it with foreign keys from the `public` schema.

## Output

When this skill completes successfully, the user will have:

- A Supabase project running locally with `supabase start`
- Database schema with proper auth integration (profiles trigger, org membership)
- RLS policies tailored to their app's access patterns
- Verified policies with simulated user tests
- TypeScript types generated for type-safe client code
- Migration files committed to `supabase/migrations/` for reproducibility
