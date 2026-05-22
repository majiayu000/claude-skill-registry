---
name: database-isolation
description: Use when implementing tenant data isolation in databases. Covers Row-Level Security (RLS), schema-per-tenant, database-per-tenant patterns with EF Core, SQL Server, PostgreSQL, and Cosmos DB implementations.
allowed-tools: Read, Glob, Grep, Task
---

# Database Isolation Patterns

Implementation patterns for isolating tenant data at the database level, from logical to physical isolation.

## When to Use This Skill

- Implementing tenant data isolation in a new SaaS application
- Choosing between RLS, schema-per-tenant, or database-per-tenant
- Configuring EF Core for multi-tenant scenarios
- Preventing cross-tenant data access
- Optimizing database performance in multi-tenant systems

## Isolation Spectrum

```text
Isolation Level vs Cost/Complexity:

Logical (Shared)                                    Physical (Isolated)
     ◄──────────────────────────────────────────────────────►

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  Row-Level   │   Schema     │   Database   │    Server    │
│  Security    │   per Tenant │   per Tenant │   per Tenant │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Lowest Cost  │              │              │ Highest Cost │
│ Shared DB    │ Shared DB    │ Dedicated DB │ Dedicated    │
│ Shared Schema│ Dedicated    │              │ Server       │
│              │ Schema       │              │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Scale: 1M+   │ Scale: 10K   │ Scale: 1K    │ Scale: 100s  │
│ tenants      │ tenants      │ tenants      │ tenants      │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

## Pattern 1: Row-Level Security (RLS)

### Concept

```text
Single Database, Shared Schema, Logical Isolation:

┌─────────────────────────────────────────────────────────────┐
│                      Shared Database                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Orders Table                                             │ │
│  │ ┌─────┬──────────┬─────────────┬────────┬─────────────┐ │ │
│  │ │ id  │ tenant_id│ customer    │ amount │ created_at  │ │ │
│  │ ├─────┼──────────┼─────────────┼────────┼─────────────┤ │ │
│  │ │ 1   │ acme     │ John Doe    │ 99.00  │ 2025-01-15  │ │ │
│  │ │ 2   │ contoso  │ Jane Smith  │ 149.00 │ 2025-01-15  │ │ │
│  │ │ 3   │ acme     │ Bob Wilson  │ 49.00  │ 2025-01-16  │ │ │
│  │ │ 4   │ startup  │ Alice Brown │ 199.00 │ 2025-01-16  │ │ │
│  │ └─────┴──────────┴─────────────┴────────┴─────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  RLS Policy: Only show rows where tenant_id = current_tenant │
└─────────────────────────────────────────────────────────────┘

Tenant "acme" sees only rows 1 and 3
Tenant "contoso" sees only row 2
Tenant "startup" sees only row 4
```

### SQL Server Implementation (PascalCase Convention)

```text
Step 1: Add TenantId to all tables
┌────────────────────────────────────────────────────────────┐
│ ALTER TABLE Orders ADD TenantId NVARCHAR(50) NOT NULL;     │
│ CREATE INDEX IX_Orders_TenantId ON Orders(TenantId);       │
└────────────────────────────────────────────────────────────┘

Step 2: Create security predicate function
┌────────────────────────────────────────────────────────────┐
│ CREATE FUNCTION dbo.fn_TenantAccessPredicate               │
│   (@TenantId NVARCHAR(50))                                 │
│ RETURNS TABLE                                              │
│ WITH SCHEMABINDING                                         │
│ AS RETURN                                                  │
│   SELECT 1 AS AccessGranted                                │
│   WHERE @TenantId = CAST(SESSION_CONTEXT(N'TenantId')      │
│                          AS NVARCHAR(50))                  │
│         OR SESSION_CONTEXT(N'TenantId') IS NULL;           │
└────────────────────────────────────────────────────────────┘

Step 3: Create security policy
┌────────────────────────────────────────────────────────────┐
│ CREATE SECURITY POLICY dbo.TenantSecurityPolicy            │
│   ADD FILTER PREDICATE                                     │
│     dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Orders,  │
│   ADD BLOCK PREDICATE                                      │
│     dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Orders   │
│     AFTER INSERT, AFTER UPDATE;                            │
└────────────────────────────────────────────────────────────┘

Step 4: Set context per request
┌────────────────────────────────────────────────────────────┐
│ EXEC sp_set_session_context @key=N'TenantId',              │
│                             @value=@CurrentTenantId;       │
└────────────────────────────────────────────────────────────┘
```

### PostgreSQL Implementation

```text
Step 1: Enable RLS on table
┌────────────────────────────────────────────────────────────┐
│ ALTER TABLE orders ENABLE ROW LEVEL SECURITY;              │
│ ALTER TABLE orders FORCE ROW LEVEL SECURITY;               │
└────────────────────────────────────────────────────────────┘

Step 2: Create policy
┌────────────────────────────────────────────────────────────┐
│ CREATE POLICY tenant_isolation_policy ON orders            │
│   USING (tenant_id = current_setting('app.current_tenant'))│
│   WITH CHECK (tenant_id =                                  │
│               current_setting('app.current_tenant'));      │
└────────────────────────────────────────────────────────────┘

Step 3: Set context per connection
┌────────────────────────────────────────────────────────────┐
│ SET app.current_tenant = 'acme';                           │
└────────────────────────────────────────────────────────────┘
```

### EF Core Global Query Filters

```text
Application-Level RLS (Defense in Depth):

DbContext Configuration:
┌────────────────────────────────────────────────────────────┐
│ public class AppDbContext : DbContext                      │
│ {                                                          │
│   private readonly ITenantContext _tenantContext;          │
│                                                            │
│   protected override void OnModelCreating(ModelBuilder mb) │
│   {                                                        │
│     // Apply filter to all tenant entities                 │
│     mb.Entity<Order>()                                     │
│       .HasQueryFilter(o =>                                 │
│         o.TenantId == _tenantContext.TenantId);            │
│                                                            │
│     mb.Entity<Customer>()                                  │
│       .HasQueryFilter(c =>                                 │
│         c.TenantId == _tenantContext.TenantId);            │
│   }                                                        │
│ }                                                          │
└────────────────────────────────────────────────────────────┘

Key Points:
- EF Core filters applied BEFORE SQL generation
- Cannot be bypassed by LINQ queries
- Use IgnoreQueryFilters() only for admin scenarios
- Combine with database RLS for defense in depth
```

### When to Use RLS

```text
✅ Ideal For:
- B2C SaaS with many tenants (10,000+)
- Homogeneous tenant requirements
- Cost-sensitive deployments
- Simple compliance requirements
- Minimal schema customization needs

❌ Avoid When:
- Strict compliance (HIPAA, PCI with audit requirements)
- Tenants need schema customization
- Performance isolation critical
- Data sovereignty requirements
```

## Pattern 2: Schema-Per-Tenant

### Concept

```text
Single Database, Separate Schemas:

┌─────────────────────────────────────────────────────────────┐
│                      Shared Database                         │
│                                                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │ Schema: acme    │ │ Schema: contoso │ │ Schema: startup │ │
│  │                 │ │                 │ │                 │ │
│  │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │
│  │ │ Orders      │ │ │ │ Orders      │ │ │ │ Orders      │ │ │
│  │ │ Customers   │ │ │ │ Customers   │ │ │ │ Customers   │ │ │
│  │ │ Products    │ │ │ │ Products    │ │ │ │ Products    │ │ │
│  │ │ (Custom tbl)│ │ │ └─────────────┘ │ │ │ (Custom tbl)│ │ │
│  │ └─────────────┘ │ │                 │ │ └─────────────┘ │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│                                                              │
│  Each schema is isolated, can have custom tables/columns     │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Pattern

```text
Connection/Schema Selection:
┌────────────────────────────────────────────────────────────┐
│ Option A: Schema in Connection String                      │
│ - Set default schema per connection                        │
│ - Works with connection pooling                            │
│                                                            │
│ Option B: Schema per Query                                 │
│ - Prefix table names: [acme].Orders                        │
│ - More flexible, slightly more complex                     │
│                                                            │
│ Option C: EF Core Schema Configuration                     │
│ - Set HasDefaultSchema() in OnModelCreating               │
│ - Dynamic based on tenant context                          │
└────────────────────────────────────────────────────────────┘
```

### Migrations Considerations

```text
Migration Strategy:
┌────────────────────────────────────────────────────────────┐
│ Approach 1: Apply to All Schemas (Homogeneous)             │
│ - Loop through all tenant schemas                          │
│ - Apply same migration to each                             │
│ - Must be backward compatible                              │
│                                                            │
│ Approach 2: Per-Tenant Migrations (Heterogeneous)          │
│ - Track migration state per tenant                         │
│ - Allows tenant-specific schema variations                 │
│ - More complex to manage                                   │
│                                                            │
│ Recommendation: Start homogeneous, allow customization     │
│ only for enterprise tier                                   │
└────────────────────────────────────────────────────────────┘
```

### When to Use Schema-Per-Tenant

```text
✅ Ideal For:
- Medium number of tenants (100-10,000)
- Some schema customization needed
- Better isolation than RLS, lower cost than DB-per-tenant
- Easier backup/restore per tenant than RLS

❌ Avoid When:
- Very large number of tenants (schema count limits)
- Strict performance isolation needed
- Complete infrastructure isolation required
- Per-tenant backup/restore at database level needed
```

## Pattern 3: Database-Per-Tenant

### Concept

```text
Dedicated Database per Tenant:

┌──────────────────────────────────────────────────────────────────┐
│                     SQL Server Instance                          │
│                                                                  │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐       │
│  │ DB: db_acme    │ │ DB: db_contoso │ │ DB: db_startup │ ...   │
│  │                │ │                │ │                │       │
│  │ Full schema    │ │ Full schema    │ │ Full schema    │       │
│  │ Own backups    │ │ Own backups    │ │ Own backups    │       │
│  │ Own security   │ │ Own security   │ │ Own security   │       │
│  │ Custom config  │ │ Custom config  │ │ Custom config  │       │
│  └────────────────┘ └────────────────┘ └────────────────┘       │
│                                                                  │
│  Elastic Pool for cost optimization (optional)                   │
└──────────────────────────────────────────────────────────────────┘
```

### Connection String Resolution

```text
Tenant Catalog → Connection String (SQL Server - PascalCase):
┌────────────────────────────────────────────────────────────┐
│ TenantCatalog Table:                                       │
│ ┌──────────┬───────────────────────────────────────────┐  │
│ │ TenantId │ ConnectionString                          │  │
│ ├──────────┼───────────────────────────────────────────┤  │
│ │ acme     │ Server=sql1;Database=db_acme;...          │  │
│ │ contoso  │ Server=sql1;Database=db_contoso;...       │  │
│ │ startup  │ Server=sql2;Database=db_startup;...       │  │
│ └──────────┴───────────────────────────────────────────┘  │
│                                                            │
│ Resolution Flow:                                           │
│ 1. Request arrives with TenantId                          │
│ 2. Lookup connection string in catalog (cached)           │
│ 3. Create/reuse connection from tenant-specific pool      │
│ 4. Execute query on tenant's database                     │
└────────────────────────────────────────────────────────────┘
```

### Elastic Pools (Azure SQL)

```text
Cost Optimization with Elastic Pools:
┌────────────────────────────────────────────────────────────┐
│ Without Elastic Pool:                                      │
│ - 10 tenants × S2 ($75/month) = $750/month                │
│ - Each DB has dedicated 50 DTU                            │
│ - Underutilized during off-peak                           │
│                                                            │
│ With Elastic Pool:                                         │
│ - 1 pool with 200 eDTU = $300/month                       │
│ - 10 databases share the pool                             │
│ - Burst to 50 eDTU per DB when needed                     │
│ - Average utilization across tenants                      │
│                                                            │
│ Savings: 60% ($450/month)                                  │
│                                                            │
│ Best For: Variable, unpredictable workloads                │
└────────────────────────────────────────────────────────────┘
```

### When to Use Database-Per-Tenant

```text
✅ Ideal For:
- Enterprise customers with strict compliance
- Tenants needing complete data isolation
- Per-tenant backup/restore requirements
- Custom schema per tenant
- Data sovereignty requirements
- Tenants with significantly different workloads

❌ Avoid When:
- Many small tenants (cost prohibitive)
- Fast provisioning needed (<1 minute)
- Minimal compliance requirements
- Cost-sensitive market
```

## Cosmos DB Multi-Tenancy

### Partition Key Strategy

```text
Cosmos DB Isolation Levels:

Level 1: Partition Key per Tenant (Logical)
┌────────────────────────────────────────────────────────────┐
│ Container: orders                                          │
│ Partition Key: /tenantId                                   │
│                                                            │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│ │ Partition:   │ │ Partition:   │ │ Partition:   │        │
│ │ acme         │ │ contoso      │ │ startup      │        │
│ └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                            │
│ Pros: Lowest cost, automatic scaling                       │
│ Cons: Shared RU/s, noisy neighbor possible                 │
└────────────────────────────────────────────────────────────┘

Level 2: Container per Tenant
┌────────────────────────────────────────────────────────────┐
│ Database: myapp                                            │
│                                                            │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│ │ Container:   │ │ Container:   │ │ Container:   │        │
│ │ acme-orders  │ │contoso-orders│ │startup-orders│        │
│ └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                            │
│ Pros: Per-tenant RU/s limits, RBAC per container          │
│ Cons: Container limits (500K), higher management          │
└────────────────────────────────────────────────────────────┘

Level 3: Database per Tenant
┌────────────────────────────────────────────────────────────┐
│ Cosmos Account: myapp                                      │
│                                                            │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│ │ Database:    │ │ Database:    │ │ Database:    │        │
│ │ acme         │ │ contoso      │ │ startup      │        │
│ │ └─containers │ │ └─containers │ │ └─containers │        │
│ └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                            │
│ Pros: Full isolation, RBAC per database                   │
│ Cons: Higher cost, more management overhead               │
└────────────────────────────────────────────────────────────┘
```

## Defense in Depth

### Layered Security

```text
Multi-Layer Isolation:
┌────────────────────────────────────────────────────────────┐
│ Layer 1: Network (outer)                                   │
│ - VNet isolation for Silo tenants                         │
│ - Private endpoints                                       │
│ - Firewall rules                                          │
├────────────────────────────────────────────────────────────┤
│ Layer 2: Database                                          │
│ - RLS policies (SQL Server/PostgreSQL)                    │
│ - Partition isolation (Cosmos DB)                         │
│ - Connection-level authentication                         │
├────────────────────────────────────────────────────────────┤
│ Layer 3: Application                                       │
│ - EF Core global query filters                            │
│ - Tenant context validation middleware                    │
│ - Business logic checks                                   │
├────────────────────────────────────────────────────────────┤
│ Layer 4: API (inner)                                       │
│ - Request-level tenant validation                         │
│ - Authorization checks                                    │
│ - Audit logging                                           │
└────────────────────────────────────────────────────────────┘

Principle: No single layer failure should expose data
```

## Decision Framework

### Quick Selection

```text
Tenant Count and Requirements → Pattern:

< 100 tenants + Compliance needed → Database-per-tenant
< 100 tenants + Cost-sensitive   → Schema-per-tenant
100-10,000 tenants              → Schema-per-tenant or RLS
> 10,000 tenants                → RLS (mandatory)

Customization needed?
- None: RLS
- Some: Schema-per-tenant
- Full: Database-per-tenant

Compliance level?
- SOC 2/GDPR basic: RLS with audit logging
- HIPAA/PCI: Database-per-tenant minimum
- Government/Financial: Database-per-tenant + network isolation
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| No TenantId index | Slow queries, table scans | Add composite indexes |
| Trusting client TenantId | Data leakage | Server-side validation |
| Missing RLS on some tables | Partial isolation | Apply to ALL tenant tables |
| Hard-coded connection strings | No per-tenant isolation | Dynamic resolution |
| Ignoring query filters in admin | Admin bypass leaks data | Audit admin operations |

## Related Skills

- `tenancy-models` - Pool/Silo/Bridge architecture patterns
- `tenant-context-propagation` - Passing context across services
- `noisy-neighbor-prevention` - Resource isolation techniques

## References

- Load `references/row-level-security.md` for detailed RLS implementations
- Load `references/schema-per-tenant.md` for schema isolation patterns
- Load `references/database-per-tenant.md` for dedicated database patterns

---

**Last Updated:** 2025-12-26
