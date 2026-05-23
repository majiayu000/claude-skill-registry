---
name: kodo-supabase
description: "Architecture decision guide for multi-language applications (TypeScript, Python, Rust) using Supabase. Use when implementing backend features to decide between Supabase Edge Functions, Database Functions, Realtime, Storage, Auth, Queues, or custom backend services. Triggers on API endpoint implementation, webhook handling, background jobs, real-time features, file storage, authentication, database operations, cron jobs, AI/vector search, hybrid ORM workflows, or any architectural decisions involving Supabase services vs custom backend code."
---

# Supabase Architecture Decision Skill

Use this skill when implementing backend features with Supabase. Supports multi-language stacks:
- **TypeScript/Node.js** + Drizzle ORM
- **Python** + SQLAlchemy/Alembic
- **Rust** + SQLx

## Supabase CLI Usage

**Always use the Supabase CLI** for operations when available. The CLI is assumed to be installed and configured.

### Essential Commands

```bash
# Local development
supabase start                    # Start local Supabase
supabase stop                     # Stop local Supabase
supabase status                   # Check status and get URLs/keys

# Database
supabase db reset                 # Reset local DB and apply migrations
supabase db diff --use-migra -f name  # Generate migration from changes
supabase db push                  # Push migrations to remote
supabase migration new name       # Create empty migration
supabase migration list           # List migrations
supabase gen types typescript --local > src/types/database.ts

# Edge Functions
supabase functions new name       # Create new function
supabase functions serve          # Serve locally for dev
supabase functions deploy         # Deploy all functions
supabase functions deploy name    # Deploy specific function

# Secrets
supabase secrets set KEY=value    # Set secret for Edge Functions
supabase secrets list             # List configured secrets

# Logs
supabase logs                     # View all logs
supabase logs --service postgres  # View specific service logs
```

### Integration with kodo-planner

When working in a project with `.kodo/config.json`, check for Supabase configuration:

```json
{
  "stack": {
    "languages": ["typescript"],
    "workspaces": {
      "server": {
        "type": "web-server",
        "language": "typescript",
        "database": {
          "provider": "supabase",
          "orm": {
            "name": "drizzle",
            "schemaPath": "src/db/schema.ts"
          },
          "migrationStrategy": {
            "type": "hybrid",
            "serviceRange": { "start": "00100", "end": "00199" }
          }
        }
      }
    }
  }
}
```

For **multi-language projects**, workspaces can use different ORMs while sharing one Supabase database:

```json
{
  "stack": {
    "languages": ["typescript", "python", "rust"],
    "sharedDatabase": {
      "enabled": true,
      "provider": "supabase",
      "serviceRanges": {
        "server": "00100-00199",
        "api": "00200-00299",
        "rust-service": "00300-00399"
      }
    }
  }
}
```

### ORM Detection & Hybrid Workflow

**Check `stack.workspaces.<name>.database.orm.name` to determine workflow:**

| Language | ORM Value | Migration Tool | Schema Location | Service Range |
|----------|-----------|----------------|-----------------|---------------|
| TypeScript | `"drizzle"` | drizzle-kit | `src/db/schema.ts` | 00100-00199 |
| Python | `"sqlalchemy"` | alembic | `src/db/models/` | 00200-00299 |
| Rust | `"sqlx"` | sqlx-cli | `src/db/models/` | 00300-00399 |
| Any | `null` | supabase CLI | SQL only | 00000-00099 |

**Universal Hybrid Philosophy:** *"ORM for data modeling, Supabase for data behavior"*

```
+-----------------------------------------------------------------+
|              UNIVERSAL HYBRID WORKFLOW                          |
+-----------------------------------------------------------------+
|  ORM Schema (language-specific)                                 |
|  +- TypeScript: src/db/schema.ts (Drizzle)                      |
|  +- Python: src/db/models/*.py (SQLAlchemy)                     |
|  +- Rust: src/db/models/*.rs (SQLx)                             |
|       |                                                         |
|  Native Migration Generation                                    |
|  +- drizzle-kit generate -> drizzle/migrations/                 |
|  +- alembic revision --autogenerate -> alembic/versions/        |
|  +- sqlx migrate add -> migrations/                             |
|       |                                                         |
|  Copy to supabase/migrations/XXXXX_<service>_*.sql              |
+-----------------------------------------------------------------+
|  Supabase SQL (supabase/migrations/)                            |
|  +- 00000_extensions.sql (bootstrap)                            |
|  +- 00001_core_functions.sql                                    |
|  +- 001XX_node_*.sql (TypeScript service)                       |
|  +- 002XX_python_*.sql (Python service)                         |
|  +- 003XX_rust_*.sql (Rust service)                             |
|  +- 004XX_shared_*.sql (cross-service)                          |
|       |                                                         |
|  supabase db reset (local) / supabase db push (remote)          |
+-----------------------------------------------------------------+
```

**Commands for Hybrid Workflow:**
- `/kodo supa-schema [table|column|index|relation|generate|sync]` - ORM schema management (Drizzle/SQLAlchemy/SQLx)
- `/kodo supa-migrate [new|sync|init]` - Migration management
- `/kodo supa-db [function|trigger|policy|types]` - Database behavior (language-agnostic SQL)

## Quick Decision Matrix

| Scenario | Use |
|----------|-----|
| API endpoint <2s CPU | Edge Function |
| CPU-intensive (image processing, ML) | Fly.io backend |
| Webhook from external service | Edge Function |
| Long-running job >6.5min | Fly.io worker |
| Data validation/triggers | Database Function |
| External API integration | Edge Function |
| User CRUD with auth | Direct client + RLS |
| Rate limiting, quotas | Backend API layer |
| Chat/collab <10K users | Supabase Realtime |
| Sub-10ms latency | Custom WebSocket |
| Standard auth flows | Supabase Auth |
| Pre-built auth UI, orgs/teams | Clerk |
| OIDC provider, M2M auth | Custom auth |
| <100M vectors with SQL joins | pgvector |
| Billions of vectors | Dedicated vector DB |

## Critical Constraints

### Edge Functions (Deno runtime)
- **CPU time**: 2 seconds max per request
- **Wall clock**: 150s (Free) / 400s (Paid)
- **Memory**: 256 MB
- **Bundle size**: 20 MB
- **Cold start**: ~400ms / Hot: ~125ms
- **NPM compatibility**: Limited--no native binaries, no sharp/libvips

### Database Functions
- Zero network latency (runs inside Postgres)
- Cannot call external APIs directly (use pg_net for async HTTP)
- Use `SECURITY DEFINER` with `search_path = ''` for elevated privileges

### Realtime Limits
| Plan | Connections | Messages/sec | Broadcast payload |
|------|-------------|--------------|-------------------|
| Free | 200 | 100 | 256 KB |
| Pro | 500 | 500-2,500 | 3 MB |
| Team | 10,000+ | 2,500+ | 3 MB+ |

### Storage
- Max upload: 50 MB (Free) / configurable to 500 GB (Pro+)
- Image transforms: 25 MB source, 50 MP max, $5/1,000 origins
- Use TUS resumable uploads for files >6 MB

## Decision Framework

### When to Use Edge Functions

```
- Operations complete within 2s CPU time
- Webhook handlers (Stripe, GitHub, etc.)
- External API proxy (hide API keys)
- Low-latency global API endpoints
- Background tasks via EdgeRuntime.waitUntil()
- Cron-triggered lightweight jobs
```

### When to Use Fly.io Backend

```
- CPU >2s (image processing, ML inference)
- npm packages requiring native binaries
- Long-running processes >6.5 minutes
- Complex job orchestration with BullMQ
- Worker threads, streaming responses
- Full Node.js ecosystem required
```

### When to Use Database Functions

```
- Bulk INSERT/UPDATE/DELETE (zero latency)
- Triggers (audit logs, cascading ops)
- ACID transactions across tables
- Computed columns, row validation
- Complex aggregations avoiding multiple API calls
```

### When to Use Direct Client + RLS

```
- User-driven CRUD operations
- Real-time subscriptions
- Public data without sensitive logic
- MVP/prototype development
```

### When to Add Backend API Layer

```
- Per-IP or per-user rate limiting
- Custom API key validation
- Payment status checks
- Quota enforcement
- Operations bypassing RLS with service_role
```

### When to Use Clerk vs Supabase Auth

**Use Supabase Auth when:**
```
- Building with Supabase from scratch
- Need deep RLS integration (auth.uid() in policies)
- Cost-sensitive at scale ($0.00325/MAU vs $0.02)
- Simple user authentication without orgs
- Want single vendor for auth + database
```

**Use Clerk when:**
```
- Need polished pre-built auth UI fast
- Complex organization/team management
- Multi-tenant SaaS with role-based access
- Already using Clerk in existing projects
- Want dedicated auth infrastructure
- Need advanced features (MFA, SSO) with minimal setup
```

## Fly.io + Supabase Integration

### Connection Pooling

```env
# For Prisma/Drizzle on Fly.io
DATABASE_URL="postgres://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?pgbouncer=true"
DIRECT_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres"
```

- Use port 6543 (transaction pooler) for serverless/Fly.io
- Use port 5432 (direct) only for migrations
- Disable prepared statements in transaction mode

### Regional Co-location

| Supabase Region | Fly.io Region |
|-----------------|---------------|
| us-east-1 | iad |
| eu-west-2 | lhr |
| ap-southeast-1 | sin |

**Always co-locate**--cross-region adds 150-350ms+ latency.

### JWT Verification on Fly.io

**TypeScript/Node.js:**
```javascript
import jwt from 'jsonwebtoken';
import jwksClient from 'jwks-rsa';

const client = jwksClient({
  jwksUri: `https://${PROJECT_REF}.supabase.co/auth/v1/.well-known/jwks.json`,
  cache: true,
  cacheMaxAge: 600000
});

async function verifySupabaseToken(token) {
  const decoded = jwt.decode(token, { complete: true });
  const key = await client.getSigningKey(decoded.header.kid);
  return jwt.verify(token, key.getPublicKey(), {
    audience: 'authenticated',
    issuer: `https://${PROJECT_REF}.supabase.co/auth/v1`
  });
}
```

**Python (FastAPI):**
```python
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
import httpx

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")

async def get_current_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = auth_header[7:]
    try:
        payload = jwt.decode(
            token, SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401)
```

**Rust (Axum):**
```rust
use axum::{extract::State, http::{Request, StatusCode}, middleware::Next, response::Response};
use jsonwebtoken::{decode, DecodingKey, Validation, Algorithm};

pub async fn auth_middleware<B>(
    State(state): State<AppState>,
    mut request: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    let token = request.headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "))
        .ok_or(StatusCode::UNAUTHORIZED)?;

    let mut validation = Validation::new(Algorithm::HS256);
    validation.set_audience(&["authenticated"]);

    let token_data = decode::<Claims>(
        token,
        &DecodingKey::from_secret(state.jwt_secret.as_bytes()),
        &validation
    ).map_err(|_| StatusCode::UNAUTHORIZED)?;

    request.extensions_mut().insert(token_data.claims);
    Ok(next.run(request).await)
}
```

### Edge Function Regional Pinning

For database-heavy operations, pin to database region:

```typescript
const { data } = await supabase.functions.invoke('my-function', {
  headers: { 'x-region': 'us-east-1' }
});
```

## Reference Documentation

For detailed information on specific features, see:

### ORM & Schema Management (Hybrid Workflow)
- **Hybrid ORM Architecture**: See [references/hybrid-orm-architecture.md](references/hybrid-orm-architecture.md) for the universal hybrid pattern, multi-service file structure, migration conventions, deployment workflow
- **Drizzle Integration** (TypeScript): See [references/drizzle-integration.md](references/drizzle-integration.md) for schema patterns, query examples, calling DB functions, transactions, type generation
- **SQLAlchemy Integration** (Python): See [references/python-sqlalchemy-integration.md](references/python-sqlalchemy-integration.md) for async patterns, Alembic migrations, Pydantic models, FastAPI integration
- **SQLx Integration** (Rust): See [references/rust-sqlx-integration.md](references/rust-sqlx-integration.md) for compile-time verification, sqlx-cli migrations, Axum middleware, FromRow patterns

### Database & Functions
- **Database Functions**: See [references/database-functions.md](references/database-functions.md) for PL/pgSQL patterns, triggers, security modes
- **Queues & Cron**: See [references/queues-cron.md](references/queues-cron.md) for pgmq patterns, pg_cron scheduling
- **AI/Vector**: See [references/ai-vector.md](references/ai-vector.md) for pgvector indexing, embedding generation

### Serverless & Edge
- **Edge Functions**: See [references/edge-functions.md](references/edge-functions.md) for WebSocket support, background tasks, npm compatibility, deployment patterns
- **Fly.io Integration**: See [references/flyio-integration.md](references/flyio-integration.md) for hybrid architecture patterns

### Auth & Storage
- **Auth (Supabase)**: See [references/auth.md](references/auth.md) for providers, hooks, custom claims, session management
- **Auth (Clerk)**: See [references/clerk.md](references/clerk.md) for SDK usage, webhooks, DB sync, organization management, Supabase RLS integration
- **Storage**: See [references/storage.md](references/storage.md) for CDN, transforms, signed URLs, RLS policies
- **Realtime**: See [references/realtime.md](references/realtime.md) for channels, presence, broadcast, postgres changes

### Operations
- **Pricing**: See [references/pricing.md](references/pricing.md) for cost analysis, tier limits, when to scale

## Common Patterns

### Webhook Handler (Edge Function)

```typescript
// supabase/functions/stripe-webhook/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Stripe from 'https://esm.sh/stripe@14.0.0'

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')!
  const body = await req.text()

  const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!)
  const event = stripe.webhooks.constructEvent(
    body, signature, Deno.env.get('STRIPE_WEBHOOK_SECRET')!
  )

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // Process event and write to DB
  await supabase.from('payments').insert({
    stripe_event_id: event.id,
    type: event.type,
    data: event.data.object
  })

  return new Response(JSON.stringify({ received: true }), {
    headers: { "Content-Type": "application/json" }
  })
})
```

### Background Task with waitUntil

```typescript
serve(async (req) => {
  const { userId } = await req.json()

  // Return immediately
  const response = new Response(JSON.stringify({ accepted: true }))

  // Continue processing after response
  EdgeRuntime.waitUntil((async () => {
    await generateEmbeddings(userId)
    await sendNotification(userId)
  })())

  return response
})
```

### Database Trigger Function

```sql
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = ''
AS $$
BEGIN
  INSERT INTO public.profiles (id, email, created_at)
  VALUES (NEW.id, NEW.email, NOW());

  -- Async webhook via pg_net
  PERFORM net.http_post(
    url := 'https://project.supabase.co/functions/v1/new-user-webhook',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || current_setting('app.service_role_key'),
      'Content-Type', 'application/json'
    ),
    body := jsonb_build_object('user_id', NEW.id)
  );

  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
```

### RLS Policy with JWT Claims

```sql
-- Efficient: uses cached JWT claim
CREATE POLICY "Users can view own org data"
ON documents FOR SELECT
USING (
  org_id = (SELECT auth.jwt() ->> 'org_id')::uuid
);

-- Add index for policy column
CREATE INDEX idx_documents_org_id ON documents(org_id);
```

### Fly.io Worker with Queue Processing

```typescript
// Fly.io Node.js worker
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

async function processQueue() {
  while (true) {
    const { data: messages } = await supabase.rpc('pop_queue', {
      queue_name: 'heavy_jobs',
      batch_size: 10,
      visibility_timeout: 300
    })

    for (const msg of messages || []) {
      try {
        await processHeavyJob(msg.payload)
        await supabase.rpc('ack_message', { message_id: msg.id })
      } catch (error) {
        console.error('Job failed:', error)
        // Message returns to queue after visibility timeout
      }
    }

    await new Promise(r => setTimeout(r, 1000))
  }
}

processQueue()
```

## Integration

Before implementing:
```bash
kodo query "supabase patterns"
kodo query "database schema"
```

After implementation:
```bash
kodo reflect  # Capture decisions
```
