---
name: supabase-project-creator
description: Create a new Supabase project with full auth setup (Email, Google, Apple SIWA)
model: sonnet
---

# Supabase Project Creator

Automate the creation of a new Supabase project with complete authentication setup.

## What This Skill Does

1. Creates a new Supabase project
2. Applies auth schema migration (profiles table, triggers)
3. Outputs callback URLs for Google/Apple console
4. Provides Supabase dashboard links for auth provider configuration

## Prerequisites (Already Configured)

Credentials are stored in MCP memory:
- **Google OAuth**: `GoogleOAuthCredentials` entity
- **Apple SIWA**: `AppleSIWACredentials` entity
- **Supabase Org**: `SupabaseOrgInfo` entity

## Workflow

### Step 1: Get Project Details

Ask the user for:
- Project name (e.g., "MyNewApp")
- Region preference (default: us-east-1)

### Step 2: Confirm Cost

```
Use mcp__supabase__get_cost with:
- type: "project"
- organization_id: "cqwwexcenmknepxltuea"

Then use mcp__supabase__confirm_cost with:
- type: "project"
- recurrence: "monthly"
- amount: (from get_cost result)
```

### Step 3: Create Project

```
Use mcp__supabase__create_project with:
- name: <project_name>
- organization_id: "cqwwexcenmknepxltuea"
- region: <chosen_region>
- confirm_cost_id: <from step 2>
```

Wait for project to be ACTIVE_HEALTHY (poll with get_project).

### Step 4: Apply Auth Schema Migration

```sql
-- Enable extensions
create extension if not exists "uuid-ossp";

-- Profiles table
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text,
  full_name text,
  avatar_url text,
  provider text,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- Enable RLS
alter table public.profiles enable row level security;

-- Policies
create policy "Users can view own profile"
  on public.profiles for select using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update using (auth.uid() = id);

create policy "Users can insert own profile"
  on public.profiles for insert with check (auth.uid() = id);

-- Auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, email, full_name, avatar_url, provider)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'),
    coalesce(new.raw_user_meta_data->>'avatar_url', new.raw_user_meta_data->>'picture'),
    coalesce(new.raw_app_meta_data->>'provider', 'email')
  );
  return new;
end;
$$;

create or replace trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Updated_at trigger
create or replace function public.update_updated_at()
returns trigger language plpgsql security invoker set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_updated_at
  before update on public.profiles
  for each row execute procedure public.update_updated_at();
```

### Step 5: Get API Keys

```
Use mcp__supabase__get_project_url
Use mcp__supabase__get_publishable_keys
```

### Step 6: Output Results

Provide the user with:

```
## Project Created: <name>

**Supabase URL:** https://<project_ref>.supabase.co
**Anon Key:** <key>
**Dashboard:** https://supabase.com/dashboard/project/<project_ref>

### Callback URL (add to Google & Apple):
https://<project_ref>.supabase.co/auth/v1/callback

### Manual Steps Required:

1. **Add callback URL to Google OAuth:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Edit "Supabase Auth" OAuth client
   - Add redirect URI: https://<project_ref>.supabase.co/auth/v1/callback

2. **Add callback URL to Apple SIWA:**
   - Go to: https://developer.apple.com/account/resources/identifiers/list/serviceId
   - Edit "Leavn Web Auth" (com.leavn.web)
   - Add domain: <project_ref>.supabase.co
   - Add return URL: https://<project_ref>.supabase.co/auth/v1/callback

3. **Configure Auth Providers in Supabase:**
   - Go to: https://supabase.com/dashboard/project/<project_ref>/auth/providers

   **Google:**
   - Client ID: 266992035640-0oegr8f1q49ub97si4s3c73al036mbvg.apps.googleusercontent.com
   - Client Secret: (retrieve from MCP memory: GoogleOAuthCredentials)

   **Apple:**
   - Service ID: com.leavn.web
   - Team ID: 49HAGQE8FB
   - Key ID: M652AAWJXF
   - Private Key: (retrieve from MCP memory: ApplePrivateKey)
```

### Step 7: Run Security Advisor

```
Use mcp__supabase__get_advisors with:
- project_id: <new_project_id>
- type: "security"
```

Fix any warnings found.

## Stored Credentials Reference

### Google OAuth
- Client ID: `266992035640-0oegr8f1q49ub97si4s3c73al036mbvg.apps.googleusercontent.com`
- Client Secret: Retrieve from `mcp__memory__open_nodes` with name `GoogleOAuthCredentials`

### Apple SIWA
- Services ID: `com.leavn.web`
- Team ID: `49HAGQE8FB`
- Key ID: `M652AAWJXF`
- Private Key: Retrieve from `mcp__memory__open_nodes` with name `ApplePrivateKey`

### Supabase Org
- Organization ID: `cqwwexcenmknepxltuea`
- Default Region: `us-east-1`
