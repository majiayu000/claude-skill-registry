---
name: optaic-v0-migration
description: Guide for porting code from optaic-v0 to optaic-trading. Use when migrating DataAPI, pipelines, stores, accessors, operators, or expressions into the Resource/Activity architecture. Covers pattern mappings for permission checks, audit trails, and catalog lookups.
---

# OptAIC v0 Migration Patterns

Guide for adapting optaic-v0 domain logic to integrate with optaic-trading infrastructure.

## When to Use

Apply when:
- Porting DataAPI or catalog functionality
- Migrating pipeline, store, or accessor implementations
- Adapting operator/expression evaluation code
- Converting name-based lookups to Resource ID lookups

## Architecture Mapping

```
optaic-v0 (Domain)          →    optaic-trading (Infrastructure)
─────────────────────────        ──────────────────────────────
DATA_CATALOG                →    Resource table + extension tables
check_permission()          →    RBAC via authorize_or_403()
audit_operation()           →    ActivityEnvelope + tx_activity()
get_dataset_info(name)      →    get_resource_or_404(db, tenant_id, uuid)
DataAPI.preview()           →    DatasetService.preview() + RBAC
ExpressionPipeline.run()    →    ExperimentService.run() + Activity
PIPELINE_FACTORY["key"]     →    Definition.code_ref → FACTORY.build(code_ref)
```

## code_ref Linkage (CRITICAL)

The key integration pattern between DB models and libs/data/ factories:

1. **Definition resources** store `code_ref` field (e.g., "ParquetStore")
2. **Services** load Definition → get `code_ref` → call `FACTORY.build(code_ref)`
3. **Factories** (PIPELINE_FACTORY, STORE_FACTORY, ACCESSOR_FACTORY) return execution objects

```python
# Service bridges Resource model to Factory execution
store_def = await session.get(StoreDefinition, store_inst.definition_resource_id)
store = STORE_FACTORY.build(
    store_def.code_ref,  # "ParquetStore" → ParquetStore class
    config=store_inst.config_json,
)
```

See `quant-resource-patterns/references/service-patterns.md` for full pattern.

## Core Pattern Mappings

### Permission Checks

**optaic-v0:**
```python
if not check_permission(user, "read", dataset_name):
    raise PermissionError("Access denied")
```

**optaic-trading:**
```python
from apps.api.rbac_utils import authorize_or_403
await authorize_or_403(db, actor, Permission.RESOURCE_READ, resource.id)
```

### Audit Logging

**optaic-v0:**
```python
audit_operation("dataset.preview", user, dataset_name, params)
```

**optaic-trading:**
```python
envelope = ActivityEnvelope(
    tenant_id=actor.tenant_id,
    actor_principal_id=actor.id,
    resource_id=resource_id,
    resource_type="dataset",
    action="dataset.previewed",
    payload={"start_date": start, "end_date": end}
)
await record_activity_with_outbox(session, envelope)
```

### Catalog Lookups

**optaic-v0:**
```python
info = DATA_CATALOG.get(name)  # name-based
pipeline = PIPELINE_FACTORY[info.source]
```

**optaic-trading:**
```python
resource = await get_resource_or_404(db, tenant_id, resource_id)
definition = await get_resource_or_404(db, tenant_id, resource.definition_ref_id)
pipeline = await load_pipeline_from_definition(definition)
```

## File Migration Map

See [references/file-mapping.md](references/file-mapping.md) for complete source → target paths.

## Adaptation Checklist

1. [ ] Replace name-based lookups with UUID resource lookups
2. [ ] Add tenant_id to all queries
3. [ ] Replace permission checks with RBAC
4. [ ] Wrap mutations in tx_activity()
5. [ ] Add guardrails validation at lifecycle gates
6. [ ] Create Pydantic DTOs instead of returning raw dicts

## Reference Files

- [File Mapping](references/file-mapping.md) - Source file → target path mapping
- [Code Examples](references/examples.md) - Before/after code samples
