---
name: supabase-ship
description: Supabase shipping gate for Postgres migrations, RLS, auth config, Edge Functions, storage policies, secrets, and rollout safety. Use when releasing on Supabase and you want a provider-specific read on schema drift, policy mistakes, auth surprises, function config risk, or rollback realism.
user-invocable: true
argument-hint: "[migration, Edge Function, policy change, or Supabase release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- A migration without rollback reality is just a schema bet with production stakes.
- Missing or wrong RLS is not a tiny config issue.
- If auth settings drift, your happy-path test results are fiction.
- Edge Functions fail at the seam between code, secrets, and policy.

## What to interrogate

### 1. Release surface

State what is shipping:
- Postgres migration
- RLS or database policy change
- auth config or provider change
- Edge Function change
- storage bucket or storage policy change
- secrets, env config, or client/server boundary change

### 2. Data and policy realism

Check:
- forward and backward migration safety
- destructive DDL assumptions
- RLS coverage and unintended public access
- service-role versus anon/authenticated boundary mistakes
- storage policy and signed URL assumptions

### 3. Runtime and integration risk

Review:
- Edge Function secret/config completeness
- function auth expectations
- local versus hosted environment drift
- queue/background behavior if functions trigger follow-on work
- client assumptions about schema, auth, or storage shape

### 4. Rollout and rollback

Ask:
- can this schema or policy change be rolled back honestly?
- do old clients keep working during rollout?
- does auth or policy state make rollback fake?
- what breaks first if the migration or function deploy is wrong?

## Output format

### Supabase release surface

What actually changes in the platform.

### Platform blockers

Migration, policy, auth, storage, or function blockers.

### Rollout risk

What fails during deploy, mixed-version operation, or rollback.

### Mitigation and rollback plan

Concrete safer rollout steps.

### Verdict

- **Safe to release**
- **Fix before release**
- **Supabase release red flag**
