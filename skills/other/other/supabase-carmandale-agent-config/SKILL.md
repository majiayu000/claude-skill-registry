---
name: supabase
description: "Manage Supabase projects, databases, migrations, Edge Functions, and storage using the `supabase` CLI."
---

# Supabase Skill

Use the `supabase` CLI to manage Supabase projects and local development.

## Projects

List all projects:
```bash
supabase projects list
```

Link to a remote project:
```bash
supabase link --project-ref <project-id>
```

## Local Development

Start local Supabase stack (Postgres, Auth, Storage, etc.):
```bash
supabase start
```

Stop local stack:
```bash
supabase stop
```

Check status of local services:
```bash
supabase status
```

## Database

Run SQL query:
```bash
supabase db execute --sql "SELECT * FROM users LIMIT 10"
```

Pull remote schema to local:
```bash
supabase db pull
```

Push local migrations to remote:
```bash
supabase db push
```

Reset local database:
```bash
supabase db reset
```

Diff local vs remote schema:
```bash
supabase db diff
```

## Migrations

Create a new migration:
```bash
supabase migration new <migration-name>
```

List migrations:
```bash
supabase migration list
```

Apply migrations locally:
```bash
supabase migration up
```

Squash migrations:
```bash
supabase migration squash
```

## Edge Functions

List functions:
```bash
supabase functions list
```

Create a new function:
```bash
supabase functions new <function-name>
```

Deploy a function:
```bash
supabase functions deploy <function-name>
```

Deploy all functions:
```bash
supabase functions deploy
```

Serve functions locally:
```bash
supabase functions serve
```

View function logs:
```bash
supabase functions logs <function-name>
```

## Storage

List buckets:
```bash
supabase storage ls
```

List objects in a bucket:
```bash
supabase storage ls <bucket-name>
```

Copy file to storage:
```bash
supabase storage cp <local-path> ss:///<bucket>/<path>
```

Download from storage:
```bash
supabase storage cp ss:///<bucket>/<path> <local-path>
```

## Secrets

Set a secret for Edge Functions:
```bash
supabase secrets set <NAME>=<value>
```

List secrets:
```bash
supabase secrets list
```

Unset a secret:
```bash
supabase secrets unset <NAME>
```

## Type Generation

Generate TypeScript types from database schema:
```bash
supabase gen types typescript --local > types/supabase.ts
```

Generate types from remote:
```bash
supabase gen types typescript --project-id <project-id> > types/supabase.ts
```

## Authentication

Login to Supabase:
```bash
supabase login
```

Check current status:
```bash
supabase projects list
```
