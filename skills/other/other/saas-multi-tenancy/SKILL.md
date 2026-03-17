---
name: saas-multi-tenancy
description: Design tenant isolation models from shared database to dedicated infrastructure
---

# SaaS Multi-Tenancy

## Tenancy Model Selection

| Model | Isolation | Cost/Tenant | Ops Complexity | Compliance | Best For |
|-------|-----------|-------------|----------------|------------|----------|
| **Shared DB, row-level** | Low | Lowest | Low | Basic | Early-stage SaaS, <1000 tenants |
| **Schema-per-tenant** | Medium | Low-Medium | Medium | Moderate | Mid-market, moderate compliance |
| **DB-per-tenant** | High | Medium-High | High | Strong | Enterprise, regulated industries |
| **Infra-per-tenant** | Complete | Highest | Very High | Maximum | Healthcare, finance, gov contracts |

**Default:** Start with shared DB + row-level isolation. Migrate to schema/DB-per-tenant when compliance or noisy-neighbor issues demand it.

### Scale Thresholds

- **<100 tenants**: Shared DB handles everything
- **100-1000 tenants**: Schema-per-tenant if data size varies widely
- **1000+ tenants**: Shared DB with partitioning, or tiered (shared for free, dedicated for enterprise)
- **Regulated tenants**: DB-per-tenant minimum; infra-per-tenant for SOC2/HIPAA

## PostgreSQL Row-Level Security

```sql
-- Enable RLS on tenant tables
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;  -- Applies to table owners too

-- Tenant isolation: rows visible only to matching tenant
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Insert policy: prevent writing to other tenants
CREATE POLICY tenant_insert ON orders
    FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Admin bypass: superadmin role sees all
CREATE POLICY admin_bypass ON orders
    USING (current_setting('app.is_admin', true)::boolean = true);

-- Set tenant context per request (transaction-scoped, done in middleware)
SET LOCAL app.current_tenant_id = 'tenant-uuid-here';

-- Shared lookup tables (plans, features) -- disable RLS
ALTER TABLE plans DISABLE ROW LEVEL SECURITY;
```

## Tenant-Aware Middleware (FastAPI)

```python
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextvars import ContextVar

_current_tenant: ContextVar[str] = ContextVar("current_tenant")  # Async-safe

app = FastAPI()

def get_current_tenant() -> str:
    try:
        return _current_tenant.get()
    except LookupError:
        raise HTTPException(status_code=500, detail="Tenant context not set")

@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    """Extract tenant from subdomain, header, or JWT."""
    host = request.headers.get("host", "")
    subdomain = host.split(".")[0] if "." in host else None
    header_tenant = request.headers.get("X-Tenant-ID")
    jwt_tenant = getattr(request.state, "tenant_id", None)

    tenant_id = jwt_tenant or header_tenant or subdomain
    if not tenant_id:
        return JSONResponse(status_code=400, content={"error": "Tenant required"})

    tenant = await get_tenant(tenant_id)
    if not tenant or not tenant.is_active:
        return JSONResponse(status_code=403, content={"error": "Invalid tenant"})

    _current_tenant.set(tenant_id)
    return await call_next(request)

@app.get("/api/orders")
async def list_orders(
    tenant_id: str = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """RLS handles filtering -- query is tenant-unaware."""
    await db.execute(text("SET LOCAL app.current_tenant_id = :tid"),
                     {"tid": tenant_id})
    result = await db.execute(select(Order))  # RLS filters automatically
    return result.scalars().all()
```

## SQLAlchemy Session Routing

```python
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# --- Schema-per-tenant ---
engine = create_async_engine("postgresql+asyncpg://localhost/saas_db")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@event.listens_for(engine.sync_engine, "before_cursor_execute")
def set_search_path(conn, cursor, statement, parameters, context, executemany):
    tenant_id = _current_tenant.get(None)
    if tenant_id:
        cursor.execute(f"SET search_path TO tenant_{tenant_id}, public")

# --- DB-per-tenant ---
_engine_cache: dict[str, AsyncEngine] = {}

def get_tenant_engine(tenant_id: str) -> AsyncEngine:
    """Lazy-create engine per tenant DB."""
    if tenant_id not in _engine_cache:
        _engine_cache[tenant_id] = create_async_engine(
            f"postgresql+asyncpg://localhost/tenant_{tenant_id}",
            pool_size=5, max_overflow=2, pool_recycle=3600,
        )
    return _engine_cache[tenant_id]

async def get_db_per_tenant(tenant_id: str) -> AsyncSession:
    return AsyncSession(get_tenant_engine(tenant_id), expire_on_commit=False)
```

## Data Partitioning Strategies

```sql
-- PostgreSQL native partitioning by tenant_id
CREATE TABLE orders (
    id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    total DECIMAL(10,2),
    PRIMARY KEY (tenant_id, id)
) PARTITION BY HASH (tenant_id);

-- Create 16 hash partitions (scale with tenant count)
CREATE TABLE orders_p0 PARTITION OF orders FOR VALUES WITH (MODULUS 16, REMAINDER 0);
CREATE TABLE orders_p1 PARTITION OF orders FOR VALUES WITH (MODULUS 16, REMAINDER 1);
-- ... repeat for p2 through p15

CREATE INDEX idx_orders_tenant ON orders (tenant_id);
CREATE INDEX idx_orders_created ON orders (tenant_id, created_at DESC);
-- Partition pruning: WHERE tenant_id = X scans only 1 of 16 partitions
```

## Tenant Migration Tooling

```python
import asyncio
from alembic import command
from alembic.config import Config

async def create_tenant_schema(tenant_id: str):
    """Provision new tenant: create schema + run migrations."""
    schema_name = f"tenant_{tenant_id}"
    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
        alembic_cfg.set_section_option("alembic", "schema", schema_name)
        command.upgrade(alembic_cfg, "head")

async def migrate_all_tenants():
    """Run pending migrations across all tenant schemas."""
    tenants = await get_all_active_tenants()
    sem = asyncio.Semaphore(5)            # Limit concurrent migrations
    async def migrate_one(t):
        async with sem:
            await create_tenant_schema(t.id)
    await asyncio.gather(*[migrate_one(t) for t in tenants])
```

## Billing and Metering Per Tenant

```python
from datetime import datetime, timedelta
import redis

r = redis.Redis(decode_responses=True)

class TenantMeter:
    def record_api_call(self, tenant_id: str):
        date_key = datetime.utcnow().strftime("%Y-%m-%d")
        key = f"meter:{tenant_id}:api_calls:{date_key}"
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, 86400 * 35)     # Keep 35 days for billing cycles
        pipe.execute()

    def record_storage_bytes(self, tenant_id: str, bytes_delta: int):
        r.incrby(f"meter:{tenant_id}:storage_bytes", bytes_delta)

    def get_usage_summary(self, tenant_id: str, days: int = 30) -> dict:
        pipe = r.pipeline()
        today = datetime.utcnow()
        for i in range(days):
            date_key = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            pipe.get(f"meter:{tenant_id}:api_calls:{date_key}")
        daily_counts = pipe.execute()
        return {
            "total_api_calls": sum(int(c or 0) for c in daily_counts),
            "storage_bytes": int(r.get(f"meter:{tenant_id}:storage_bytes") or 0),
        }

    def check_quota(self, tenant_id: str, plan_limits: dict) -> bool:
        usage = self.get_usage_summary(tenant_id)
        return (usage["total_api_calls"] < plan_limits["max_api_calls"]
                and usage["storage_bytes"] < plan_limits["max_storage_bytes"])
```

## Gotchas

- **RLS is not a silver bullet**: Always test with `SET ROLE` to verify policies; a missing policy = full access
- **Schema migration drift**: All tenant schemas must stay in sync; one failed migration breaks consistency
- **Connection pool exhaustion**: DB-per-tenant with 1000 tenants and `pool_size=5` = 5000 connections
- **Cross-tenant queries**: Reporting needs a separate path (ETL to warehouse, not cross-schema JOINs)
- **Tenant deletion is hard**: Soft-delete first, then async cleanup; cascading deletes are slow
- **Noisy neighbor in shared DB**: One tenant's bulk import degrades everyone; use per-tenant rate limiting
- **Search path injection**: Never interpolate tenant_id into SQL without validation; use allowlist
- **Backup/restore granularity**: Shared DB = all-or-nothing; DB-per-tenant = per-tenant restore possible
- **Testing gap**: Most bugs are cross-tenant data leaks; integration tests must verify isolation
