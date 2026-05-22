---
name: supabase-automation
description: "Master Supabase CLI automation, auth configuration, edge functions, secrets management, MCP integration, and Management API for production deployments"
---

# Supabase Automation & Integration Expert

Complete automation toolkit for Supabase CLI, auth configuration, edge functions, secrets, MCP integration, and API management.

## MCP Integration

**Supabase MCP Server** provides Model Context Protocol integration for:
- **Docs** - Access Supabase documentation
- **Account** - Manage account and projects
- **Database** - Query and manage database
- **Debugging** - Debug edge functions and queries
- **Development** - Local development tools
- **Functions** - Manage edge functions
- **Branching** - Database branching (preview environments)
- **Storage** - File storage management

**MCP Connection URL:**
```
https://mcp.supabase.com/mcp?project_ref=spdtwktxdalcfigzeqrz&features=docs%2Caccount%2Cdatabase%2Cdebugging%2Cdevelopment%2Cfunctions%2Cbranching%2Cstorage
```

**Setup MCP Server:**
```bash
# Add to Claude Desktop config (~/.config/claude/claude_desktop_config.json)
{
  "mcpServers": {
    "supabase": {
      "url": "https://mcp.supabase.com/mcp",
      "params": {
        "project_ref": "spdtwktxdalcfigzeqrz",
        "features": "docs,account,database,debugging,development,functions,branching,storage"
      },
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}",
        "SUPABASE_ANON_KEY": "${SUPABASE_ANON_KEY}",
        "SUPABASE_SERVICE_ROLE_KEY": "${SUPABASE_SERVICE_ROLE_KEY}"
      }
    }
  }
}
```

## Core Capabilities

### 1. CLI Automation
- Project initialization and configuration
- Local development setup
- Database migrations and seeding
- Type generation for TypeScript
- Database schema management
- Automated deployments

### 2. Auth Configuration
- Site URL and redirect URL management
- OAuth provider setup (Google, GitHub, etc.)
- Email/password authentication
- Magic links and OTP
- JWT configuration
- Row Level Security (RLS) policies

### 3. Edge Functions
- Function creation and deployment
- Deno runtime configuration
- Secrets injection
- CORS configuration
- Function invocation and testing
- Local development server

### 4. Secrets Management
- Environment variable management
- Secret storage via Supabase CLI
- Vault integration
- Secret rotation
- Secure credential handling

### 5. Management API
- Project configuration via API
- Database connection pooling
- API key management
- Usage monitoring
- Automated backups
- SSL configuration

## Documentation References

**Essential Reading:**
- [API Reference](https://supabase.com/docs/reference/api/introduction)
- [CLI Reference](https://supabase.com/docs/reference/cli/introduction)
- [Local Development](https://supabase.com/docs/guides/local-development)
- [Deployment Guide](https://supabase.com/docs/guides/deployment)

## Quick Start Examples

### 1. Initialize Local Development
```bash
# Initialize Supabase in project
supabase init

# Start local Supabase (Docker required)
supabase start

# Generate TypeScript types
supabase gen types typescript --local > types/supabase.ts

# View local dashboard
# Studio: http://localhost:54323
# API URL: http://localhost:54321
```

### 2. Configure Auth URLs
```bash
# Set site URL (production)
supabase secrets set SITE_URL=https://app.insightpulseai.net

# Add redirect URLs via Dashboard or Management API
curl -X POST 'https://api.supabase.com/v1/projects/{project-ref}/config' \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "auth": {
      "site_url": "https://app.insightpulseai.net",
      "redirect_urls": [
        "https://app.insightpulseai.net/auth/callback",
        "https://*.insightpulseai.net/auth/callback",
        "http://localhost:3000/auth/callback"
      ]
    }
  }'
```

### 3. Deploy Edge Functions
```bash
# Create new edge function
supabase functions new my-function

# Write function code
cat > supabase/functions/my-function/index.ts << 'EOF'
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? ''
  )

  // Your function logic here
  const { data, error } = await supabase.from('table').select('*')

  return new Response(
    JSON.stringify({ data, error }),
    { headers: { "Content-Type": "application/json" } }
  )
})
EOF

# Set secrets for edge function
supabase secrets set API_KEY=your_secret_key
supabase secrets set OPENAI_API_KEY=sk-...

# Deploy edge function
supabase functions deploy my-function

# Invoke function
curl -X POST 'https://{project-ref}.supabase.co/functions/v1/my-function' \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'
```

### 4. Database Migrations
```bash
# Create new migration
supabase migration new create_users_table

# Edit migration file
cat > supabase/migrations/20250101_create_users_table.sql << 'EOF'
-- Create users table with RLS
CREATE TABLE public.users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read their own data
CREATE POLICY "Users can view own data"
  ON public.users
  FOR SELECT
  USING (auth.uid() = id);

-- Grant permissions
GRANT SELECT, INSERT, UPDATE ON public.users TO authenticated;
EOF

# Apply migrations locally
supabase db reset

# Push to production
supabase db push
```

### 5. Secrets Management
```bash
# List all secrets
supabase secrets list

# Set secret
supabase secrets set DATABASE_URL=postgresql://...
supabase secrets set STRIPE_SECRET_KEY=sk_live_...
supabase secrets set OPENAI_API_KEY=sk-...

# Unset secret
supabase secrets unset OLD_SECRET

# Use secrets in edge functions
# Automatically available as Deno.env.get('SECRET_NAME')
```

### 6. Management API - Full Configuration
```typescript
// supabase-management.ts
const SUPABASE_ACCESS_TOKEN = process.env.SUPABASE_ACCESS_TOKEN
const PROJECT_REF = 'your-project-ref'
const API_BASE = 'https://api.supabase.com/v1'

// Configure auth settings
async function configureAuth() {
  const response = await fetch(`${API_BASE}/projects/${PROJECT_REF}/config`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      auth: {
        site_url: 'https://app.insightpulseai.net',
        redirect_urls: [
          'https://app.insightpulseai.net/auth/callback',
          'https://*.insightpulseai.net/auth/callback',
          'http://localhost:3000/auth/callback'
        ],
        external_google_enabled: true,
        external_github_enabled: true,
        jwt_exp: 3600,
        refresh_token_rotation_enabled: true,
        security_refresh_token_reuse_interval: 10
      }
    })
  })
  return response.json()
}

// Configure database pooling
async function configureDatabasePooling() {
  const response = await fetch(`${API_BASE}/projects/${PROJECT_REF}/database/pooling`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      pool_mode: 'transaction',
      default_pool_size: 15,
      ignore_startup_parameters: 'extra_float_digits'
    })
  })
  return response.json()
}
```

## Common Workflows

### Workflow 1: New Project Setup
```bash
# 1. Initialize project
supabase init
supabase login

# 2. Link to remote project
supabase link --project-ref {project-ref}

# 3. Pull remote schema
supabase db pull

# 4. Generate types
supabase gen types typescript --linked > types/supabase.ts

# 5. Start local development
supabase start
```

### Workflow 2: Deploy with CI/CD
```yaml
# .github/workflows/deploy-supabase.yml
name: Deploy Supabase

on:
  push:
    branches: [main]
    paths:
      - 'supabase/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Link Supabase project
        run: supabase link --project-ref ${{ secrets.SUPABASE_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Push database migrations
        run: supabase db push

      - name: Deploy edge functions
        run: |
          supabase functions deploy --no-verify-jwt
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Set production secrets
        run: |
          supabase secrets set OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          supabase secrets set STRIPE_SECRET_KEY=${{ secrets.STRIPE_SECRET_KEY }}
```

### Workflow 3: Auth Provider Setup
```typescript
// Setup Google OAuth
// 1. Get credentials from Google Cloud Console
// 2. Configure in Supabase Dashboard or via API

const setupGoogleAuth = async () => {
  const response = await fetch(
    `https://api.supabase.com/v1/projects/${PROJECT_REF}/config`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${SUPABASE_ACCESS_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        auth: {
          external_google_enabled: true,
          external_google_client_id: 'your-google-client-id.apps.googleusercontent.com',
          external_google_secret: 'GOCSPX-...'
        }
      })
    }
  )
  return response.json()
}

// Use in your app
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://app.insightpulseai.net/auth/callback'
  }
})
```

## MCP-Powered Workflows

### MCP Workflow 1: Database Branching for Testing
```bash
# Using MCP to create database branch for feature testing
# MCP command: create_database_branch

# Create branch from production
supabase branches create feature-trial-balance --project-ref spdtwktxdalcfigzeqrz

# Get branch connection string
supabase branches get feature-trial-balance --project-ref spdtwktxdalcfigzeqrz

# Run migrations on branch
supabase db push --branch feature-trial-balance

# Test your changes
# Connect app to branch URL temporarily

# Merge branch when ready
supabase branches merge feature-trial-balance --project-ref spdtwktxdalcfigzeqrz
```

### MCP Workflow 2: Edge Function Debugging
```typescript
// Use MCP debugging features to troubleshoot edge functions

// Enable verbose logging in edge function
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  console.log('[DEBUG] Request received:', {
    method: req.method,
    url: req.url,
    headers: Object.fromEntries(req.headers)
  })

  try {
    // Your function logic
    const result = await processRequest(req)
    console.log('[DEBUG] Processing successful:', result)
    return new Response(JSON.stringify(result))
  } catch (error) {
    console.error('[ERROR] Function failed:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500
    })
  }
})

// Check logs via MCP or CLI
// supabase functions logs my-function --project-ref spdtwktxdalcfigzeqrz
```

### MCP Workflow 3: Storage Management
```typescript
// Using MCP storage features for BIR document management

import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

// Create storage bucket for BIR forms
const { data: bucket, error: bucketError } = await supabase
  .storage
  .createBucket('bir-forms', {
    public: false,
    fileSizeLimit: 52428800, // 50MB
    allowedMimeTypes: ['application/pdf', 'image/png', 'image/jpeg']
  })

// Upload BIR form with RLS
const { data, error } = await supabase
  .storage
  .from('bir-forms')
  .upload(
    `company_${companyId}/1601C_${period}.pdf`,
    fileBuffer,
    {
      contentType: 'application/pdf',
      upsert: true,
      metadata: {
        company_id: companyId,
        form_type: '1601C',
        period: period
      }
    }
  )

// Create RLS policy for storage
/*
CREATE POLICY "Company users can access their BIR forms"
ON storage.objects FOR ALL
USING (
  bucket_id = 'bir-forms'
  AND (storage.foldername(name))[1] = 'company_' || auth.jwt() ->> 'company_id'
);
*/
```

## InsightPulse Integration Patterns

### Pattern 1: Odoo + Supabase Auth
```typescript
// Edge function for Odoo SSO
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  // Verify Supabase JWT
  const token = req.headers.get('Authorization')?.replace('Bearer ', '')
  const { data: { user }, error } = await supabase.auth.getUser(token)

  if (error || !user) {
    return new Response('Unauthorized', { status: 401 })
  }

  // Connect to Odoo
  const odooResponse = await fetch(`${Deno.env.get('ODOO_URL')}/web/session/authenticate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      params: {
        db: Deno.env.get('ODOO_DB'),
        login: user.email,
        password: Deno.env.get('ODOO_SSO_PASSWORD')
      }
    })
  })

  return new Response(JSON.stringify(await odooResponse.json()), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

### Pattern 2: Real-time Finance Updates
```typescript
// Subscribe to trial balance changes
const subscription = supabase
  .channel('trial-balance-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'account_move_line',
      filter: 'company_id=eq.1'
    },
    (payload) => {
      console.log('Change detected:', payload)
      // Update Superset dashboard
      // Trigger recalculation
    }
  )
  .subscribe()
```

### Pattern 3: Vector Search for BIR Forms
```sql
-- Create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add vector column for OCR embeddings
ALTER TABLE bir_forms
ADD COLUMN embedding vector(1536);

-- Create vector index
CREATE INDEX ON bir_forms
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Search similar forms
SELECT
  form_number,
  form_type,
  1 - (embedding <=> $1::vector) AS similarity
FROM bir_forms
ORDER BY embedding <=> $1::vector
LIMIT 10;
```

## Environment Configuration

### Local Development (.env.local)
```bash
# Supabase Local
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Local Postgres
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
```

### Production (.env.production)
```bash
# Supabase Production
NEXT_PUBLIC_SUPABASE_URL=https://spdtwktxdalcfigzeqrz.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Production Postgres (Pooler)
DATABASE_URL=postgresql://postgres.spdtwktxdalcfigzeqrz:password@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require

# Management API
SUPABASE_ACCESS_TOKEN=sbp_...
SUPABASE_PROJECT_REF=spdtwktxdalcfigzeqrz
```

## Security Best Practices

### 1. Row Level Security (RLS)
```sql
-- Enable RLS on all tables
ALTER TABLE account_move_line ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their company's data
CREATE POLICY "company_isolation"
  ON account_move_line
  FOR ALL
  USING (
    company_id IN (
      SELECT company_id
      FROM user_companies
      WHERE user_id = auth.uid()
    )
  );
```

### 2. Service Role Key Protection
- Never expose service role key in client code
- Use edge functions for privileged operations
- Rotate keys regularly via Dashboard

### 3. OAuth Configuration
```bash
# Set redirect URLs to prevent open redirects
# Use wildcards carefully: https://*.insightpulseai.net is safer than https://*
```

## Troubleshooting

### Issue: Edge function deployment fails
```bash
# Check function logs
supabase functions logs my-function

# Test locally first
supabase functions serve my-function

# Verify Deno permissions
deno run --allow-net --allow-env index.ts
```

### Issue: Auth redirect not working
```bash
# Verify redirect URLs in dashboard
# Check site URL matches your domain
# Ensure CORS is configured

# Test auth flow
curl -X POST 'https://{project-ref}.supabase.co/auth/v1/token?grant_type=password' \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'
```

### Issue: Database migration conflict
```bash
# Reset local database
supabase db reset

# Force push (DANGER: production)
supabase db push --force

# Create repair migration
supabase migration new repair_conflict
```

## CLI Command Reference

```bash
# Project Management
supabase init                          # Initialize new project
supabase login                         # Login to Supabase
supabase projects list                 # List all projects
supabase link --project-ref {ref}      # Link to remote project

# Database
supabase db reset                      # Reset local database
supabase db push                       # Push migrations to remote
supabase db pull                       # Pull remote schema
supabase db diff                       # Show schema differences
supabase migration new {name}          # Create new migration
supabase migration up                  # Apply migrations

# Edge Functions
supabase functions new {name}          # Create new function
supabase functions deploy {name}       # Deploy function
supabase functions serve {name}        # Run function locally
supabase functions delete {name}       # Delete function

# Secrets
supabase secrets list                  # List all secrets
supabase secrets set {KEY}={VALUE}     # Set secret
supabase secrets unset {KEY}           # Remove secret

# Type Generation
supabase gen types typescript --local              # Generate from local
supabase gen types typescript --linked             # Generate from remote
supabase gen types typescript --db-url {URL}       # Generate from URL

# Local Development
supabase start                         # Start local Supabase
supabase stop                          # Stop local Supabase
supabase status                        # Show local status
```

## Supabase UI Components (shadcn/ui)

Supabase provides official UI components built on shadcn/ui for Next.js and React apps.

### Installation

```bash
# Install shadcn/ui first
npx shadcn@latest init

# Add Supabase UI components
npx shadcn@latest add https://ui.supabase.com/registry/supabase-auth-block.json
npx shadcn@latest add https://ui.supabase.com/registry/supabase-storage-upload.json
npx shadcn@latest add https://ui.supabase.com/registry/supabase-realtime-chat.json
```

### Available Components

#### 1. SupabaseAuthBlock
Complete authentication UI with sign-up, sign-in, password reset, and OAuth.

```typescript
import { SupabaseAuthBlock } from '@/components/supabase-ui/auth-block'

export default function LoginPage() {
  return (
    <SupabaseAuthBlock
      providers={['google', 'github']}
      redirectTo="/dashboard"
      appearance={{
        theme: 'default',
        variables: {
          default: {
            colors: {
              brand: '#3b82f6',
              brandAccent: '#2563eb'
            }
          }
        }
      }}
    />
  )
}
```

#### 2. SupabaseStorageUpload
File upload component with progress tracking and thumbnail previews.

```typescript
import { SupabaseStorageUpload } from '@/components/supabase-ui/storage-upload'

export function FileUploader() {
  return (
    <SupabaseStorageUpload
      bucket="avatars"
      path={`${userId}/`}
      accept="image/*"
      maxSize={5242880} // 5MB
      onUpload={(url) => console.log('Uploaded:', url)}
    />
  )
}
```

#### 3. SupabaseRealtimeChat
Real-time chat component with presence and typing indicators.

```typescript
import { SupabaseRealtimeChat } from '@/components/supabase-ui/realtime-chat'

export function ChatRoom({ roomId }: { roomId: string }) {
  return (
    <SupabaseRealtimeChat
      channel={`room:${roomId}`}
      onMessage={(message) => console.log(message)}
    />
  )
}
```

### Hybrid Stack: Next.js + OWL

For InsightPulse, we use **both** Supabase UI (Next.js) and Odoo OWL:

**Use Next.js + Supabase UI for:**
- Public portals and customer-facing apps
- Analytics dashboards (read-heavy)
- Real-time features (chat, notifications)
- File uploads and storage
- Authentication and user management

**Use Odoo OWL for:**
- ERP workflows (accounting, inventory, HR)
- Complex business logic
- BIR tax forms and compliance
- Multi-company/multi-currency
- Backend admin interfaces

See: `/docs/HYBRID_STACK_ARCHITECTURE.md` for complete integration guide.

## When to Use This Skill

Use this skill when you need to:
- ✅ Set up local Supabase development environment
- ✅ Configure authentication providers and redirect URLs
- ✅ Deploy and manage edge functions
- ✅ Manage secrets and environment variables
- ✅ Automate database migrations
- ✅ Integrate Supabase with Odoo/Superset
- ✅ Configure RLS policies
- ✅ Use Management API for infrastructure automation
- ✅ Set up CI/CD for Supabase deployments
- ✅ Implement vector search with pgvector
- ✅ Configure production database pooling
- ✅ Build Next.js apps with Supabase UI components
- ✅ Create hybrid Next.js + OWL architectures

## Related Skills
- `supabase-rpc-manager` - For RPC calls and real-time subscriptions
- `odoo` - For Odoo ERP integration
- `superset-dashboard-automation` - For analytics integration

## Related Documentation
- `/docs/HYBRID_STACK_ARCHITECTURE.md` - Next.js + OWL integration guide

## Support Resources
- [Supabase Discord](https://discord.supabase.com)
- [GitHub Discussions](https://github.com/supabase/supabase/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/supabase)
- [Supabase UI Library](https://ui.supabase.com)
