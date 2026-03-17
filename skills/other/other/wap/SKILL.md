---
name: wap-ingestion
description: "Ingest data from S3 into bauplan using the Write-Audit-Publish pattern for safe data loading. Use when loading new data from S3, performing safe data ingestion, or when the user mentions WAP, data ingestion, importing parquet/csv/jsonl files, or needs to safely load data with quality checks."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Write-Audit-Publish (WAP) Pattern

Implement WAP by writing a Python script using the `bauplan` SDK. Do NOT use CLI commands.

**The three steps**: Write (ingest to temp branch) → Audit (quality checks) → Publish (merge to main)

**Branch safety**: All operations happen on a temporary branch, NEVER on `main`. By default, branches are kept open for inspection after success or failure.

**Atomic multi-table operations**: `merge_branch` is atomic. You can create or modify multiple tables on a branch, and when you merge, either all changes apply to main or none do. This enables safe multi-table ingestion workflows.

## Required User Input

Before writing the WAP script, you MUST ask the user for the following parameters:

1. **S3 path** (required): The S3 URI pattern for the source data (e.g., `s3://bucket/path/*.parquet`)
2. **Table name** (required): The name for the target table
3. **On success behavior** (optional):
   - `inspect` (default): Keep the branch open for user inspection before merging
   - `merge`: Automatically merge to main and delete the branch
4. **On failure behavior** (optional):
   - `keep` (default): Leave the branch open for inspection/debugging
   - `delete`: Delete the failed branch

## WAP Script Template

This is the complete template for WAP:
```python
"""
WAP (Write-Audit-Publish) Template for bauplan data ingestion.

Usage:
    python wap_template.py

Or import and call wap_ingest() with your parameters.
"""
import bauplan
from datetime import datetime


def wap_ingest(
    table_name: str,
    s3_path: str,
    namespace: str = "bauplan",
    on_success: str = "inspect",  # "inspect" (default) or "merge"
    on_failure: str = "keep",  # "keep" (default) or "delete"
):
    """
    Write-Audit-Publish flow for safe data ingestion.

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

    # Generate unique branch name using username
    info = client.info()
    username = info.user.username
    branch_name = f"{username}.wap_{table_name}_{int(datetime.now().timestamp())}"

    success = False
    try:
        # === WRITE PHASE ===
        # 1. Create temporary branch from main (must not exist)
        assert not client.has_branch(branch_name), (
            f"Branch '{branch_name}' already exists - this should be an ephemeral branch"
        )
        client.create_branch(branch_name, from_ref="main")

        # 2. Verify table doesn't exist on branch before creating
        assert not client.has_table(
            table=table_name, ref=branch_name, namespace=namespace
        ), (
            f"Table '{namespace}.{table_name}' already exists on branch - refusing to overwrite"
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

        # === AUDIT PHASE ===
        # 5. Run quality check: verify data was imported
        fq_table = f"{namespace}.{table_name}"
        result = client.query(
            query=f"SELECT COUNT(*) as row_count FROM {fq_table}", ref=branch_name
        )
        row_count = result.column("row_count")[0].as_py()
        assert row_count > 0, "No data was imported"
        print(f"Imported {row_count} rows")

        success = True

        # === PUBLISH PHASE ===
        if on_success == "merge":
            # 6. Merge to main and cleanup
            client.merge_branch(source_ref=branch_name, into_branch="main")
            print(f"Successfully published {table_name} to main")
            client.delete_branch(branch_name)
            print(f"Cleaned up branch: {branch_name}")
        else:
            # Keep branch for inspection
            print(
                f"WAP completed successfully. Branch '{branch_name}' ready for inspection."
            )
            print(
                f"To merge manually: client.merge_branch(source_ref='{branch_name}', into_branch='main')"
            )

    except Exception as e:
        print(f"WAP failed: {e}")
        if on_failure == "delete":
            if client.has_branch(branch_name):
                client.delete_branch(branch_name)
                print(f"Cleaned up failed branch: {branch_name}")
        else:
            print(f"Branch '{branch_name}' preserved for inspection/debugging.")
        raise

    return branch_name, success


if __name__ == "__main__":
    # Example: customize these parameters
    branch, success = wap_ingest(
        table_name="my_table",
        s3_path="s3://my-bucket/data/*.parquet",
        namespace="bauplan",
        on_success="inspect",
        on_failure="keep",
    )
```

Minimal usage:

```python
from wap_template import wap_ingest

branch, success = wap_ingest(
    table_name="orders",
    s3_path="s3://my-bucket/data/*.parquet",
    namespace="bauplan",
    on_success="inspect",  # or "merge"
    on_failure="keep"      # or "delete"
)
```

## Key SDK Methods

| Method                                         | Description                                           |
| ---------------------------------------------- | ----------------------------------------------------- |
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

Copy and track progress:


WAP Progress:
- [ ] Ask user for: S3 path, table name, on_success, on_failure
- [ ] Write script using wap_template.py
- [ ] Run script: python wap_script.py
- [ ] Verify output shows row count > 0
- [ ] If on_success="inspect": confirm branch ready for review
- [ ] If on_success="merge": confirm merge to main succeeded


## Example Output

**Successful run (on_success="inspect")**:
```bash
$ python wap_script.py
Imported 15234 rows
WAP completed successfully. Branch 'alice.wap_orders_1704067200' ready for inspection.
To merge manually: client.merge_branch(source_ref='alice.wap_orders_1704067200', into_branch='main')
```

**Successful run (on_success="merge")**:
```bash
$ python wap_script.py
Imported 15234 rows
Successfully published orders to main
Cleaned up branch: alice.wap_orders_1704067200
```

**Failed run (on_failure="keep")**:
```bash
$ python wap_script.py
WAP failed: No data was imported
Branch 'alice.wap_orders_1704067200' preserved for inspection/debugging.
```

## WAP on Existing Tables

To append data to an existing table, skip `create_table` and only call `import_data`:

```python
# Table already exists on main - just import new data
client.import_data(
    table=table_name,
    search_uri=s3_path,
    namespace=namespace,
    branch=branch_name
)
```

This appends rows to the existing table schema. The audit and publish phases remain the same: the new rows are automatically sandboxed on the branch until merged.

## CLI Merge After Inspection

When `on_success="inspect"` (default), the branch is left open for user review. If the user asks to merge after inspecting the data, use the CLI:

```bash
# 1. Checkout to main first (required before merging)
bauplan checkout main

# 2. Merge the WAP branch into main
bauplan branch merge <username>.wap_<table_name>_<timestamp>

# 3. Optionally delete the branch after successful merge
bauplan branch rm <username>.wap_<table_name>_<timestamp>
```

> **Note**: You must be on `main` to run `bauplan branch merge`. The branch name is printed by the WAP script upon completion.
