---
name: quality-gated-updates
description: "Ingest data from S3 into Bauplan safely using branch isolation and quality checks before publishing. Use when loading new data from S3, importing parquet/csv/jsonl files, or when the user needs to safely load data with validation before merging to main."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Quality-Gated Updates

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

Before writing the script, you MUST ask the user for:

1. **S3 path** (required): The S3 URI pattern for the source data (e.g., `s3://bucket/path/*.parquet`)
2. **Table name** (required): The name for the target table
3. **On success behavior** (optional):
   - `inspect` (default): Keep the branch open for user inspection before merging
   - `merge`: Automatically merge to main and delete the branch
4. **On failure behavior** (optional):
   - `inspect` (default): Leave the branch open for inspection/debugging
   - `delete`: Delete the failed branch

## Script Template

```python
"""
Quality-gated update for Bauplan data ingestion.

Safely imports data from S3 using branch isolation and validation
before merging to main (Write-Audit-Publish pattern).

Usage:
    python quality_gated_update.py

Or import and call quality_gated_update() with your parameters.
"""
import bauplan
from datetime import datetime


def quality_gated_update(
    table_name: str,
    s3_path: str,
    namespace: str = "bauplan",
    on_success: str = "inspect",  # "inspect" (default) or "merge"
    on_failure: str = "inspect",  # "inspect" (default) or "delete"
):
    """
    Import → Validate → Merge flow for safe data ingestion.

    Args:
        table_name: Target table name
        s3_path: S3 URI pattern (e.g., 's3://bucket/path/*.parquet')
        namespace: Target namespace (default: 'bauplan')
        on_success: "inspect" to keep branch for review, "merge" to auto-merge
        on_failure: "keep" to preserve branch for debugging, "delete" to cleanup

    Returns:
        tuple: (branch_name, success)
    """
    client = bauplan.Client()

    # Generate unique branch name
    info = client.info()
    username = info.user.username
    branch_name = f"{username}.import_{table_name}_{int(datetime.now().timestamp())}"

    success = False
    try:
        # === IMPORT PHASE ===
        # 1. Create temporary branch from main
        assert not client.has_branch(branch_name), (
            f"Branch '{branch_name}' already exists"
        )
        client.create_branch(branch_name, from_ref="main")

        # 2. Verify table doesn't already exist on branch
        assert not client.has_table(
            table=table_name, ref=branch_name, namespace=namespace
        ), (
            f"Table '{namespace}.{table_name}' already exists on branch"
        )

        # 3. Create table (schema inferred from S3 files)
        client.create_table(
            table=table_name,
            search_uri=s3_path,
            namespace=namespace,
            branch=branch_name,
        )

        # 4. Import data into table
        client.import_data(
            table=table_name,
            search_uri=s3_path,
            namespace=namespace,
            branch=branch_name,
        )

        # === VALIDATE PHASE ===
        # 5. Quality check: verify data was imported
        fq_table = f"{namespace}.{table_name}"
        result = client.query(
            query=f"SELECT COUNT(*) as row_count FROM {fq_table}", ref=branch_name
        )
        row_count = result.column("row_count")[0].as_py()
        assert row_count > 0, "No data was imported"
        print(f"Imported {row_count} rows")

        success = True

        # === MERGE PHASE ===
        if on_success == "merge":
            client.merge_branch(source_ref=branch_name, into_branch="main")
            print(f"Successfully published {table_name} to main")
            client.delete_branch(branch_name)
            print(f"Cleaned up branch: {branch_name}")
        else:
            print(
                f"Import complete. Branch '{branch_name}' ready for inspection."
            )
            print(
                f"To merge manually: client.merge_branch(source_ref='{branch_name}', into_branch='main')"
            )

    except Exception as e:
        print(f"Import failed: {e}")
        if on_failure == "delete":
            if client.has_branch(branch_name):
                client.delete_branch(branch_name)
                print(f"Cleaned up failed branch: {branch_name}")
        else:
            print(f"Branch '{branch_name}' preserved for inspection/debugging.")
        raise

    return branch_name, success


if __name__ == "__main__":
    branch, success = quality_gated_update(
        table_name="my_table",
        s3_path="s3://my-bucket/data/*.parquet",
        namespace="bauplan",
        on_success="inspect",
        on_failure="keep",
    )
```

Minimal usage:

```python
from quality_gated_update import quality_gated_update

branch, success = quality_gated_update(
    table_name="orders",
    s3_path="s3://my-bucket/data/*.parquet",
    on_success="inspect",  # or "merge"
    on_failure="inspect",  # or "delete"
)
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
- [ ] Write script using the template above
- [ ] Run script: `python quality_gated_update.py`
- [ ] Verify output shows row count > 0
- [ ] If on_success="inspect": confirm branch ready for review
- [ ] If on_success="merge": confirm merge to main succeeded

## Example Output

**Successful run (on_success="inspect")**:
```
Imported 15234 rows
Import complete. Branch ready for inspection: 'alice.import_orders_1704067200'.
To merge manually: client.merge_branch(source_ref='alice.import_orders_1704067200', into_branch='main')
```

**Successful run (on_success="merge")**:
```
Imported 15234 rows
Successfully published orders to main
Cleaned up branch: alice.import_orders_1704067200
```

**Failed run (on_failure="keep")**:
```
**Failed run (on_failure="inspect")**:
```
Import failed: No data was imported
Branch preserved for inspection/debugging: 'alice.import_orders_1704067200' 
```

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
