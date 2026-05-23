---
name: safe-ingestion
description: "Ingest data from S3 into Bauplan safely using branch isolation and quality checks before publishing. Use when loading new data from S3, importing parquet/csv/jsonl files, or when the user needs to safely load data with validation before merging to main."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Safe Ingestion

Safely ingest data from S3 into the Bauplan lakehouse by isolating changes on a temporary branch, running quality checks, and only merging to `main` after validation succeeds.
This pattern is formally known as Write-Audit-Publish (WAP) in the Iceberg ecosystem.

Implement this as a Python script using the `bauplan` SDK. Do NOT use CLI commands for the ingestion itself.

**The three phases:**
1. **Import** — load data onto a temporary branch (never `main`)
2. **Validate** — run quality checks before publishing
3. **Merge** — promote to `main` only after validation passes

**Branch safety**: All operations happen on a temporary branch, NEVER on `main`. By default, branches are kept open for inspection after success or failure.

**Atomic multi-table operations**: `merge_branch` is atomic. You can create or modify multiple tables on a branch, and when you merge, either all changes apply to main or none do. This enables safe multi-table ingestion workflows.

## Required User Input

Before writing the script, you MUST gather:

1. **S3 path** (required): The S3 URI pattern for the source data (e.g., `s3://bucket/path/*.parquet`)
2. **Table name** (required): The name for the target table
3. **Validation path** (required): See "Choosing a Validation Path" below
4. **On success behavior** (optional):
   - `inspect` (default): Keep the branch open for user inspection before merging
   - `merge`: Automatically merge to main and delete the branch
5. **On failure behavior** (optional):
   - `inspect` (default): Leave the branch open for inspection/debugging
   - `delete`: Delete the failed branch

## Choosing a Validation Path

Ask the user which situation they're in. This determines what validation code goes into the script.

### Path A — "I don't know this data yet"

The user is importing data they haven't explored. They can't state expectations because they don't know the shape yet.

**Action:** Generate the script with a minimal check — table is non-empty (row count > 0). No further questions needed.

**Be honest about what this means:**
- No quality gate protects the merge. If `on_success="merge"`, bad data (wrong types, nulls in key columns, duplicates, stale records) will land on `main` with no way to catch it before downstream consumers read it.
- Quality checks can be added to the script later, but they will not retroactively gate this import or any import run before the checks are added.

**Minimal validation code:**

```python
def validate_import(client, table_name, branch, namespace="bauplan"):
    fq_table = f"{namespace}.{table_name}"
    result = client.query(f"SELECT COUNT(*) as n FROM {fq_table}", ref=branch)
    row_count = result.column("n")[0].as_py()
    assert row_count > 0, f"{fq_table} has 0 rows after import"
    print(f"  Row count: {row_count}")
```

### Path B — "I know what I want to check"

The user can state expectations directly — specific columns, properties, and severities. Examples:

- "user_id must be unique and have no nulls"
- "age must be between 0 and 120"
- "gender must be one of M, F, Non-binary"
- "engagement_score should have no nulls, warn if mean drops below 10"

**Action:** Gather the user's check specifications, then invoke the `data-quality-checks` skill to generate a `validate_import()` function. Pass it:

- Table name and branch
- Context: ingestion
- The user's specifications as-is

The `data-quality-checks` skill will translate the specifications into validation code. Embed the resulting `validate_import()` function in the script.

**Do not ask about downstream pipelines or consumers.** The user has already decided what to check. If a specification is incomplete (e.g., "check user_id" without saying what property), ask about the specific check, not the pipeline's purpose.

### Path C — "I'll add checks after I build the pipeline"

The user wants to import the data now and build the pipeline first. Once the pipeline exists, the pipeline code will tell the agent exactly what to check.

**Action:** Generate the script with minimal validation (same as Path A). After a successful import, tell the user:

> "The data is imported on branch `<branch_name>`. When your pipeline is ready, you can come back and add quality checks — the `data-quality-checks` skill can read your `models.py` and derive checks from how the pipeline actually uses this table."

This is not a failure or a shortcut. It's the right order when the user doesn't yet know what the data's consumers need.

---

## Script Template

```python
"""
Safe ingestion script for <TABLE_NAME>.
Write-Audit-Publish (WAP) pattern: import on an isolated branch, validate, then merge or inspect.
"""
import sys
import time
import bauplan


TABLE_NAME = "<table_name>"
S3_PATH = "<s3_uri>"
NAMESPACE = "bauplan"


def validate_import(client, table_name, branch, namespace="bauplan"):
    """Run quality checks on the imported data. Raises on FAIL, prints on WARN."""
    fq_table = f"{namespace}.{table_name}"

    # --- Minimal check: table must be non-empty ---
    result = client.query(f"SELECT COUNT(*) as n FROM {fq_table}", ref=branch)
    row_count = result.column("n")[0].as_py()
    assert row_count > 0, f"{fq_table} has 0 rows after import"
    print(f"  Row count: {row_count}")

    # For Path B: replace the above with checks from the data-quality-checks skill.
    # For Path A/C: the above is sufficient.


def main():
    client = bauplan.Client()
    info = client.info()
    username = info.user.username
    timestamp = int(time.time())
    branch_name = f"{username}.import_{TABLE_NAME}_{timestamp}"

    print(f"Creating branch: {branch_name}")
    client.create_branch(branch=branch_name, from_ref="main")

    try:
        # === IMPORT PHASE ===
        print(f"\nPhase 1: Creating table '{TABLE_NAME}' from S3...")
        client.create_table(
            table=TABLE_NAME,
            search_uri=S3_PATH,
            branch=branch_name,
            namespace=NAMESPACE,
            replace=True,
        )
        print(f"  Table schema created.")

        print(f"  Importing data...")
        import_state = client.import_data(
            table=TABLE_NAME,
            search_uri=S3_PATH,
            branch=branch_name,
            namespace=NAMESPACE,
        )
        if import_state.error:
            raise RuntimeError(f"import_data failed: {import_state.error}")
        print(f"  Data imported.")

        # === VALIDATION PHASE ===
        print(f"\nPhase 2: Running quality checks...")
        validate_import(client, TABLE_NAME, branch_name, NAMESPACE)

        # === MERGE PHASE ===
        # on_success="inspect" (default): keep branch open
        print(f"\nImport complete. Branch ready for inspection: '{branch_name}'")
        print(f"To query:  bauplan query \"SELECT * FROM {NAMESPACE}.{TABLE_NAME} LIMIT 10\" --ref {branch_name}")
        print(f"To merge:  bauplan branch merge {branch_name} --into main")
        print(f"To delete: bauplan branch delete {branch_name}")

        # on_success="merge": uncomment below, remove above
        # client.merge_branch(source_ref=branch_name, into_branch="main")
        # print(f"Successfully published {TABLE_NAME} to main")
        # client.delete_branch(branch_name)

    except Exception as exc:
        print(f"\nImport FAILED: {exc}")
        print(f"Branch preserved for debugging: '{branch_name}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Key SDK Methods

| Method                                         | Description                                           |
|------------------------------------------------|-------------------------------------------------------|
| `bauplan.Client()`                             | Initialize the bauplan client                         |
| `client.info()`                                | Get client info; access username via `.user.username` |
| `client.create_branch(name, from_ref="main")`  | Create a new branch from specified ref                |
| `client.has_branch(name)`                      | Check if branch exists                                |
| `client.delete_branch(name)`                   | Delete a branch                                       |
| `client.create_table(table, search_uri, ...)`  | Create table with schema inferred from S3             |
| `client.import_data(table, search_uri, ...)`   | Import data from S3 into table                        |
| `client.query(query, ref)`                     | Run SQL query, returns PyArrow Table                  |
| `client.merge_branch(source_ref, into_branch)` | Merge branch into target                              |
| `client.has_table(table, ref, namespace)`      | Check if table exists on branch                       |

> **SDK Reference**: For detailed method signatures, check https://docs.bauplanlabs.com/reference/bauplan

## Workflow Checklist

- [ ] Ask user for: S3 path, table name, on_success, on_failure
- [ ] Ask which validation path: A (don't know data), B (know what to check), or C (will add checks later)
- [ ] Path A or C: write script with minimal validation
- [ ] Path B: gather check specifications, invoke `data-quality-checks` skill, embed result in script
- [ ] Run script: `python <script_name>.py`
- [ ] Verify output shows row count > 0
- [ ] If on_success="inspect": confirm branch ready for review
- [ ] If on_success="merge": confirm merge to main succeeded

## Example Output

**Successful run (on_success="inspect")**:
```
Imported 15234 rows
Import complete. Branch ready for inspection: 'alice.import_orders_1704067200'.
To merge manually: bauplan checkout main && bauplan branch merge alice.import_orders_1704067200
```

**Successful run (on_success="merge")**:
```
Imported 15234 rows
Successfully published orders to main
Cleaned up branch: alice.import_orders_1704067200
```

**Failed run (on_failure="inspect")**:
```
Import failed: No data was imported
Branch preserved for inspection/debugging: 'alice.import_orders_1704067200'
```

## Strengthening Validation Later

If the user chose Path A or C and wants to add checks to an existing script:

1. Invoke the `data-quality-checks` skill with context: ingestion.
2. The user provides either:
   - Their own check specifications (they now know the data)
   - A path to `models.py` (they built the pipeline and want checks derived from it)
3. The `data-quality-checks` skill reads the existing script, finds the validate phase, and replaces the minimal check with proper validation logic.

Checks added after an import do not gate any previous run. If the data is already on `main`, it's there without quality validation.

## Appending to Existing Tables

To append data to a table that already exists on main, skip `create_table` and only call `import_data`:

```python
# Table already exists on main — just import new data
client.import_data(
    table=table_name,
    search_uri=s3_path,
    namespace=namespace,
    branch=branch_name,
)
```

The validate and merge phases remain the same. New rows are sandboxed on the branch until merged.

## CLI Merge After Inspection

When `on_success="inspect"` (default), the branch is left open for review. To merge after inspecting:

```bash
bauplan checkout main
bauplan branch merge <branch_name>
bauplan branch rm <branch_name>  # optional cleanup
```

The branch name is printed by the script upon completion.