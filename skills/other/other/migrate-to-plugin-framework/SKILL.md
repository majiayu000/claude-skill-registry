---
name: migrate-to-plugin-framework
description: >-
  This skill should be used when migrating Terraform provider data sources or
  resources from hashicorp/terraform-plugin-sdk/v2 to
  hashicorp/terraform-plugin-framework. Trigger phrases include "migrate to
  plugin framework", "SDK v2 to plugin framework", "convert to plugin framework",
  "migrate data source", "migrate resource", "plugin framework migration",
  "move to framework", or "upgrade from SDK v2". Provides step-by-step migration
  workflow, code patterns, schema mapping, and common gotchas.
---

# Terraform SDK v2 to Plugin Framework Migration

Migrate Terraform provider data sources and resources from `terraform-plugin-sdk/v2` to
`terraform-plugin-framework`, following patterns established by completed migrations in the
target codebase.

## Migration Workflow

### Phase 0: Codebase Discovery

Before writing any code, understand how the target provider is structured. This determines whether you follow existing conventions or fall back to the templates in `references/`.

1. **Find existing framework code** — search for imports of `terraform-plugin-framework` to locate already-migrated data sources and resources. Note their file structure, naming conventions, and patterns.
2. **Identify the provider registration files** — find where `DataSources()` and `Resources()` are returned from the framework provider, and where `DataSourcesMap`/`ResourcesMap` are defined in the SDK provider.
3. **Check for codegen or shared tooling** — some providers use code generation (e.g. `tfplugindocs`, custom generators). Look for `go:generate` directives, `Makefile` targets, or `tools/` directories.
4. **Locate test infrastructure** — find how existing tests set up `protoV5ProviderFactories` or equivalent. Note the test package conventions and any shared test helpers.
5. **Check for a muxed server** — look for `tf5muxserver` or `tf6muxserver` usage. This determines whether the protocol v5 block constraint applies (see `references/gotchas.md` #1).

### Phase 1: Analyse the SDK v2 Source

1. Read the existing SDK v2 file to understand:
   - Schema fields: types, Optional/Required/Computed, validation, defaults
   - CRUD operations: which API calls are made
   - Helper functions: filter logic, flatten functions, state waiting
   - CustomizeDiff: any custom validation logic
2. Identify the API client methods and response types used
3. Check for nested blocks (`TypeSet`/`TypeList` with `Elem: &schema.Resource{}`)
4. Note any `ForceNew`, `DiffSuppressFunc`, or `DefaultFunc` usage

### Phase 2: Create Package Structure

**If Phase 0 found existing framework code:** match those conventions exactly (directory layout, file naming, import organisation).

**Otherwise**, use the 3-file pattern as a fallback:

**Data sources:**
```
internal/<package>/
├── datasource_<name>.go         # Schema, interfaces, Metadata, Configure
├── datasource_<name>_model.go   # Model struct with tfsdk tags
├── datasource_<name>_read.go    # Read implementation + helpers
└── helpers.go                   # Shared utilities (if needed)
```

**Resources:**
```
internal/<package>/
├── resource_<name>.go           # Schema, interfaces, Metadata, Configure
├── resource_<name>_model.go     # Model struct(s) with tfsdk tags
├── resource_<name>_crud.go      # Create, Read, Update, Delete implementations
└── helpers.go                   # Shared utilities (if needed)
```

### Phase 3: Write the Model

Create the model struct:

- **`id` is always `types.String`** — even if SDK v2 used `TypeInt` (see `references/gotchas.md` #5)
- Use `types.String`, `types.Bool`, `types.Int64`, `types.Float64` for scalars
- Use `types.Set`, `types.List`, `types.Map` for collections
- Every field needs a `tfsdk:"field_name"` tag matching the schema attribute name

Consult `references/schema-mapping.md` for the full type mapping table.

### Phase 4: Write the Schema

Create the schema definition with: interface checks, struct, constructor, Metadata, Configure, and Schema methods.

Key rules:
- **Protocol v5 nested blocks** — if the provider uses `tf5muxserver`, SDK v2 `TypeSet`/`TypeList` with `Elem: &schema.Resource{}` MUST become blocks, not attributes. See `references/gotchas.md` #1.
- **`MaxItems: 1` nested objects** become `SingleNestedBlock`. See `references/gotchas.md` #6.
- **Explicit `id`** — declare as `schema.StringAttribute{Computed: true}`. See `references/gotchas.md` #5.
- **`ForceNew`** becomes `planmodifier.RequiresReplace()`.
- **`DefaultFunc`** becomes `Default` (e.g., `stringdefault.StaticString("value")`).
- **`DiffSuppressFunc`** becomes a custom `planmodifier`.
- **`CustomizeDiff`** becomes `ModifyPlan` (implement `ResourceWithModifyPlan`).

For code templates, see `references/data-source-template.md` or `references/resource-template.md`.

### Phase 5: Write the Read/CRUD Implementation

Implement the operations following these patterns:

1. **Nil safety** — defensive client check at the start of every operation. See `references/gotchas.md` #4.
2. **Read config/state** via `req.Config.Get(ctx, &state)` (data sources) or `req.Plan.Get(ctx, &plan)` (resources).
3. **API pointer dereference** — dereference safely. See `references/gotchas.md` #2.
4. **Filter pattern** for data sources: list all items, apply filters, expect exactly 1 result.
5. **Flatten pattern** for nested sets: use `types.ObjectValueFrom` with model structs. See `references/gotchas.md` #3.
6. **Set state** via `resp.State.Set(ctx, &state)`.
7. **Concurrency control** — replicate any mutex patterns from the SDK v2 implementation.
8. **State waiting** for resources: wait for stable state after mutations if the API is asynchronous.

### Phase 6: Register and Remove

Three changes required:

1. **Add to the framework provider**: import the new package, add to `DataSources()` or `Resources()` return slice.
2. **Remove from the SDK provider**: delete the entry from `DataSourcesMap` or `ResourcesMap`.
3. **Delete the old SDK v2 file**.

> Use the registration files identified in Phase 0. Look for how existing framework data sources/resources are registered.

### Phase 7: Verify Build Iteratively

Run the build and fix errors in a loop:

1. Run `go build ./...`
2. If compilation errors occur:
   - Fix the reported errors
   - Run `go build ./...` again
3. Run `go vet ./...` to catch additional issues
4. Repeat until clean

Common build errors during migration:
- Missing imports (framework packages have different import paths than SDK v2)
- Type mismatches between model fields and API types (pointer vs value)
- Interface compliance failures (missing methods on the struct)

### Phase 8: Tests

Leverage the test infrastructure discovered in Phase 0:

1. **Check if existing tests still pass** — if tests were in a separate package using the muxed provider factories, they may work without changes after registration is updated.
2. **If tests need migration**, follow the same test patterns found in Phase 0:
   - Use the same `protoV5ProviderFactories` setup
   - Match the existing test naming and structure conventions
   - Use the same `testAccPreCheck` pattern
3. **Provide the test command** for the user to run (do not run tests yourself):
   ```
   go test ./internal/<package>/... -v 2>&1 | tee test-output.log
   ```

### Phase 9: Documentation

Update the corresponding `docs/data-sources/` or `docs/resources/` markdown file if the schema changed (e.g., `id` type change from int to string).

## Quick Reference

| Need | File |
|------|------|
| Type mapping (SDK v2 → Framework) | `references/schema-mapping.md` |
| Common failure modes | `references/gotchas.md` |
| Data source code template | `references/data-source-template.md` |
| Resource code template | `references/resource-template.md` |
