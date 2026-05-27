---
name: deno-monorepo-template
description: Deno monorepo with Hono, tRPC, Drizzle, and Supabase.
---

# Deno Monorepo

A Deno monorepo with Hono, tRPC, Drizzle, and Supabase.

## Tech Stack

- **Runtime**: Deno
- **Framework**: Hono
- **RPC**: tRPC
- **ORM**: Drizzle
- **Database**: Supabase

## Prerequisites

- Deno installed
- Supabase project

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/runreal/deno-monorepo-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/runreal/deno-monorepo-template.git _temp_template
mv _temp_template/* _temp_template/.* . 2>/dev/null || true
rm -rf _temp_template
```

### 2. Remove Git History (Optional)

```bash
rm -rf .git
git init
```

### 3. Install Dependencies

```bash
deno install
```

### 4. Setup Environment

Configure Supabase credentials.

## Development

```bash
deno task dev
```
