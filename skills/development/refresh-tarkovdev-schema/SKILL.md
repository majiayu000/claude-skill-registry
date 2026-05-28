---
name: refresh-tarkovdev-schema
description: Update the tarkov.dev GraphQL schema and regenerate the Go client code
---

# Refresh Tarkov.dev Schema Skill

Use this skill when updating the tarkov.dev GraphQL schema or regenerating the Go client.

---

## When to Use

- Tarkov.dev API has added new fields or types you need
- GraphQL queries are failing with "unknown field" errors
- You want to use new data that's available in the API
- After a major tarkov.dev API update
- Setting up the project for the first time (if schema is missing)

## Quick Update

```bash
# Fetch latest schema and regenerate client
task tarkovdev
```

This runs two steps:
1. `tarkovdev:get-schema` - Downloads the latest schema from tarkov.dev
2. `tarkovdev:regenerate` - Regenerates Go code from your queries

## Step-by-Step Process

### Step 1: Fetch Latest Schema

```bash
task tarkovdev:get-schema
```

**What it does:**
- Introspects the tarkov.dev GraphQL API at `https://api.tarkov.dev/graphql`
- Writes the schema to `internal/tarkovdev/schemas/schema.graphql`

**Requirements:**
- `graphql-inspector` CLI tool (installed via `task deps:install:node`)
- Internet connection to reach api.tarkov.dev

### Step 2: Update Your Queries (if needed)

If you want to use new fields, update your queries in:

```
internal/tarkovdev/schemas/queries.graphql
```

**Example:** Adding a new field to an existing query

```graphql
query GetWeapons {
  items(type: weapon) {
    id
    name
    # Add new fields here
    weight
    basePrice
  }
}
```

### Step 3: Regenerate Go Client

```bash
task tarkovdev:regenerate
```

**What it does:**
- Runs `genqlient` code generator
- Reads `genqlient.yaml` configuration
- Generates Go types and functions in `internal/tarkovdev/generated-queries.go`

**Configuration file:** `genqlient.yaml`

```yaml
schema: internal/tarkovdev/schemas/schema.graphql
operations:
  - internal/tarkovdev/schemas/queries.graphql
generated: internal/tarkovdev/generated-queries.go
```

### Step 4: Verify the Changes

```bash
# Check what changed
git diff internal/tarkovdev/

# Ensure it compiles
go build ./...

# Run relevant tests
go test ./internal/tarkovdev/...
go test ./internal/importers/...
```

## What Gets Generated

After regeneration, `internal/tarkovdev/generated-queries.go` contains:

- **Go structs** for all GraphQL types used in your queries
- **Query functions** like `GetWeapons(ctx, client)`, `GetMods(ctx, client)`, etc.
- **Response types** with proper JSON unmarshaling

**Example generated code:**

```go
type GetWeaponsResponse struct {
    Items []GetWeaponsItem `json:"items"`
}

type GetWeaponsItem struct {
    Id   string `json:"id"`
    Name string `json:"name"`
    // New fields appear here automatically
}

func GetWeapons(ctx context.Context, client graphql.Client) (*GetWeaponsResponse, error) {
    // Generated query execution
}
```

## Making Query Changes

### Add a New Query

1. Open `internal/tarkovdev/schemas/queries.graphql`
2. Add your query:

```graphql
query GetTraderOffers {
  traders {
    id
    name
    cashOffers {
      item {
        id
        name
      }
      price
    }
  }
}
```

3. Regenerate:

```bash
task tarkovdev:regenerate
```

4. Use the generated function:

```go
import "tarkov-build-optimiser/internal/tarkovdev"

resp, err := tarkovdev.GetTraderOffers(ctx, graphqlClient)
```

### Modify an Existing Query

1. Edit the query in `queries.graphql`
2. Regenerate: `task tarkovdev:regenerate`
3. Update any code using the old structure (compiler will help find it)

### Remove a Query

1. Delete or comment out the query in `queries.graphql`
2. Regenerate: `task tarkovdev:regenerate`
3. Remove any code calling the deleted query function

## Understanding the Schema

### View the Schema

```bash
# Open in your editor
code internal/tarkovdev/schemas/schema.graphql
```

The schema shows:
- Available types (Item, Weapon, Mod, Trader, etc.)
- Fields on each type
- Query operations you can use
- Enums and their values

### Explore Available Fields

```graphql
# Look for the type you're interested in
type Item {
  id: ID!
  name: String
  weight: Float
  types: [ItemType!]!
  # ... many more fields
}
```

### Check Query Operations

```graphql
type Query {
  items(type: ItemType): [Item]
  item(id: ID!): Item
  traders: [Trader]
  # ... etc
}
```

## Troubleshooting

### Schema fetch fails

**Error:** Can't connect to api.tarkov.dev

**Solutions:**
- Check internet connection
- Verify API is online: `curl https://api.tarkov.dev/graphql`
- Check if API endpoint changed (update in Taskfile)
- Try again later (API might be down)

### Code generation fails

**Error:** genqlient errors during regeneration

**Check:**
- Query syntax is valid GraphQL
- Field names match the schema exactly (case-sensitive)
- Types used in queries exist in the schema
- Required fields are included in queries

**Debug:**
```bash
# Validate your queries manually
cat internal/tarkovdev/schemas/queries.graphql

# Check genqlient version
go list -m github.com/Khan/genqlient
```

### Generated code has compilation errors

**After regeneration, Go build fails**

**Solutions:**
- Update code using the changed types
- Check if field names or types changed in the API
- Verify your queries match the new schema
- Look for breaking changes in tarkov.dev API

### New fields not appearing

**You fetched the schema but new fields aren't available**

**Check:**
- Did you run `task tarkovdev:get-schema`?
- Is the field added to your query in `queries.graphql`?
- Did you run `task tarkovdev:regenerate` after updating queries?
- Is the field actually in the schema? (Check `schema.graphql`)

## Best Practices

### When to Update

- ✅ Before starting work that needs new API fields
- ✅ When GraphQL errors mention unknown fields
- ✅ Periodically to stay current with API changes
- ❌ Not during active development unless needed
- ❌ Not if your queries are working fine

### After Updating

1. Check the diff to understand what changed
2. Update your queries if needed
3. Rebuild and test
4. Update importers if data structures changed
5. Commit schema and generated code together

### Query Design

- Request only fields you actually use (performance)
- Use fragments for reusable field sets
- Keep queries focused and named clearly
- Document complex queries with comments

## Files Involved

- **Schema source:** `https://api.tarkov.dev/graphql`
- **Schema file:** `internal/tarkovdev/schemas/schema.graphql`
- **Your queries:** `internal/tarkovdev/schemas/queries.graphql`
- **Generated code:** `internal/tarkovdev/generated-queries.go`
- **Config:** `genqlient.yaml`
- **Client wrapper:** `internal/tarkovdev/tarkov-dev.go`

## Dependencies

Installed via `task deps:install:node`:
- `graphql-inspector` - For schema introspection

Installed via `task deps:install:go`:
- `github.com/Khan/genqlient` - For code generation
