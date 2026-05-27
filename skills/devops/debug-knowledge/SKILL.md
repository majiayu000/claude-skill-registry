---
name: debug-knowledge
description: Debug the Copilot Knowledge service - investigate sync failures, schema mismatches, and data issues between tenants.
model: inherit
---

# Debug Knowledge Service

You are debugging the **Copilot Knowledge** service, which exports models from one tenant's WrenAI instance and syncs them to other tenants.

## Architecture Overview

```
┌─────────────────┐    Export     ┌──────────────────┐     Sync      ┌─────────────────┐
│  Source Tenant  │ ───────────► │  KnowledgeItem   │ ────────────► │  Target Tenant  │
│  (WrenAI + DB)  │              │  (hub-backend)   │               │  (WrenAI + DB)  │
└─────────────────┘              └──────────────────┘               └─────────────────┘
```

**Key services location:** `hub-backend/app/services/hub/chord_ai/knowledge/`

## Debugging Setup

Always start by setting up your test environment. Use `mise` for correct Ruby version:

```ruby
# Run with: eval "$(mise activate bash)" && bin/rails runner "<code>"

tenant_1 = Hub::Tenant.first
store_1 = tenant_1.stores.first

tenant_2 = Hub::Tenant.second
store_2 = tenant_2.stores.first

user = Hub::User.last
environment = 'staging'  # or 'production'
```

## Key Services Reference

### 1. List Models in WrenAI

See what models exist in a tenant's WrenAI instance:

```ruby
result = Hub::ChordAI::Knowledge::Models::List.call(
  tenant: tenant, store: store, user: user, environment: 'staging'
)
models = result.success? ? result.data : []
models.each { |m| puts "#{m['referenceName']} (#{m['fields']&.count} fields)" }
```

### 2. Get Single Model Details

Get full details including fields, calculated fields:

```ruby
result = Hub::ChordAI::Knowledge::Models::Get.call(
  tenant: tenant, store: store, user: user, id: model_id, environment: 'staging'
)
model = result.data
model['fields'].each { |f| puts "#{f['sourceColumnName']} -> #{f['type']}" }
```

### 3. List Data Source Tables (Snowflake)

See what tables/columns exist in the actual database:

```ruby
result = Hub::ChordAI::Knowledge::DataSourceTables.call(
  tenant: tenant, store: store, user: user, environment: 'staging'
)
tables = result.data
table = tables.find { |t| t['name'].include?('TABLE_NAME') }
table['columns'].each { |c| puts c['name'] }
```

### 4. Check Knowledge Items (Exported Models)

```ruby
Hub::ChordAI::KnowledgeItem.all.each do |item|
  puts "#{item.reference_name} - #{item.item_type} (#{item.assignments.count} assignments)"
end
```

### 5. Check Assignments and Sync Status

```ruby
item = Hub::ChordAI::KnowledgeItem.find(id)
item.assignments.each do |a|
  puts "Tenant: #{a.hub_tenant.name}, Status: #{a.sync_status}, Error: #{a.last_error}"
end
```

## Common Debugging Scenarios

### Scenario 1: GraphQL Schema Mismatch

**Symptom:** Error like `String cannot represent a non string value` or `Field "X" is not defined`

**Investigation:**

1. Identify which service is failing from the error path (e.g., `data.fields[0]`)
2. Find the GraphQL mutation in the service file
3. Use the **wrenai agent** to check the actual schema:

```
Use Task tool with subagent_type=wrenai to find the GraphQL input type definition
in wren-ui/src/apollo/server/schema.ts
```

4. Compare what hub-backend sends vs what schema expects

**Common fixes:**

- Array of objects → Array of strings (fields: [String!]!)
- Missing required field (id: Int!)
- Extra field not in schema

### Scenario 2: Column Not Found in Data Source

**Symptom:** Error like `Column "X" not found in table "Y" in the data Source`

**Investigation:**

1. Check if column exists in source tenant's data source:

```ruby
# Get data source tables
result = Hub::ChordAI::Knowledge::DataSourceTables.call(...)
table = result.data.find { |t| t['name'] == 'TABLE_NAME' }
cols = table['columns'].map { |c| c['name'] }
puts cols.include?('COLUMN_NAME')  # Should be true
```

2. Check if model has phantom columns (model fields > data source columns):

```ruby
# Compare model fields vs data source columns
model_fields = model['fields'].map { |f| f['sourceColumnName'] }
db_columns = table['columns'].map { |c| c['name'] }

phantom = model_fields - db_columns
puts "Phantom columns: #{phantom}"  # These exist in model but not DB
```

3. If phantom columns exist, the source model is corrupted/stale

### Scenario 3: Model Exists in One Tenant But Not Another

**Symptom:** Sync fails because model doesn't exist in target

**Investigation:**

```ruby
# Compare models between tenants
result_1 = Hub::ChordAI::Knowledge::Models::List.call(tenant: tenant_1, ...)
result_2 = Hub::ChordAI::Knowledge::Models::List.call(tenant: tenant_2, ...)

names_1 = result_1.data.map { |m| m['referenceName'] }
names_2 = result_2.data.map { |m| m['referenceName'] }

only_in_1 = names_1 - names_2
only_in_2 = names_2 - names_1

puts "Only in tenant 1: #{only_in_1}"
puts "Only in tenant 2: #{only_in_2}"
```

### Scenario 4: Field Count Mismatch Between Tenants

**Symptom:** Same model name but different field counts

**Investigation:**

```ruby
model_1 = result_1.data.find { |m| m['referenceName'] == 'MODEL_NAME' }
model_2 = result_2.data.find { |m| m['referenceName'] == 'MODEL_NAME' }

fields_1 = model_1['fields'].map { |f| f['sourceColumnName'] }.sort
fields_2 = model_2['fields'].map { |f| f['sourceColumnName'] }.sort

only_in_1 = fields_1 - fields_2
only_in_2 = fields_2 - fields_1

puts "Fields only in tenant 1: #{only_in_1}"
puts "Fields only in tenant 2: #{only_in_2}"
```

## When to Use WrenAI Agent

Spawn the **wrenai agent** (via Task tool with `subagent_type=wrenai`) when you need to:

1. **Validate GraphQL schema** - Find input type definitions in `wren-ui/src/apollo/server/schema.ts`
2. **Understand WrenAI internals** - How models, fields, relations are stored
3. **Check GraphQL resolvers** - What mutations actually do on the WrenAI side
4. **Investigate WrenAI-specific errors** - Errors originating from WrenAI's validation

Example prompt for wrenai agent:

```
Find the GraphQL schema definition for UpdateModelMetadataInput and
UpdateColumnMetadataInput in wren-ui/src/apollo/server/schema.ts.
List all fields and their types.
```

## Quick Diagnostic Checklist

When investigating a Knowledge sync failure:

- [ ] What's the exact error message?
- [ ] Which service is failing? (check stack trace)
- [ ] Is it a GraphQL schema issue or data issue?
- [ ] Does the model exist in source tenant's WrenAI?
- [ ] Does the table exist in target's data source?
- [ ] Do all model fields exist in the data source?
- [ ] Are there phantom columns in the source model?
- [ ] Is this a new model creation or update to existing?

## File Locations

| Component | Location |
|-----------|----------|
| Knowledge services | `hub-backend/app/services/hub/chord_ai/knowledge/` |
| Models services | `hub-backend/app/services/hub/chord_ai/knowledge/models/` |
| Sync logic | `hub-backend/app/services/hub/chord_ai/knowledge/sync_model.rb` |
| Export logic | `hub-backend/app/services/hub/chord_ai/knowledge/export.rb` |
| WrenAI GraphQL schema | `wrenai/wren-ui/src/apollo/server/schema.ts` |
| Project documentation | `projects/copilot-knowledge/` |
| Learning notes | `learn/hub-backend/wrenai-graphql-integration.md` |
