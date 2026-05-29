---
name: database-migrations
description: Use when creating alembic migrations, applying migrations to remote environments, or recovering from schema drift. Triggers on changes to models.py, "run migration", "schema drift", "alembic", "database error in batch jobs".
---

## Instructions

Do not write out alembic migrations yourself. Use the alembic tool to generate and apply migrations.
You do not need to give alembic the path to alembic.ini.
Do not manually drop any tables or columns in the DB. Always use alembic migrations to make schema changes.

## Key Paths

- **Models**: `hawk/core/db/models.py`
- **Migrations**: `hawk/core/db/alembic/versions/`
- **Alembic config**: `hawk/core/db/alembic/`
- **Tests**: `tests/core/db/test_alembic_migrations.py`

## Creating Migrations

```bash
# 1. Update model in hawk/core/db/models.py
# 2. Generate migration (creates file in hawk/core/db/alembic/versions/)
alembic revision --autogenerate -m "description of changes"
# 3. Format
ruff check --fix && ruff format
# 4. Review the generated file — autogenerate isn't perfect:
#    - Reorder columns so Base fields (pk, created_at, updated_at) come first
#    - Verify index names and constraints
#    - Ensure downgrade() is reversible
```

You may need to ensure the DB is up to date before generating a new migration. Run `alembic upgrade head`.

If you need to regenerate a migration (after making model changes since the last migration):

1. Run `alembic downgrade -1` to revert the last migration.
2. Delete the migration file from the versions/ directory.
3. Run `alembic upgrade head` to ensure the DB is up to date.
4. Run the revision command again to generate a new migration file.

## Running Migrations Against Remote Environments

Alembic depends on having a valid `DATABASE_URL` set. The username should be `inspect_admin`. The password is automatically generated via RDS IAM.

The URL depends on the environment. Use `tofu output` to get the correct URL:

```bash
tofu -chdir=terraform output -var-file="terraform.tfvars" -raw warehouse_database_url_admin
```

**Note:** These commands may require AWS credentials for the target account (e.g., set `AWS_PROFILE` if needed for RDS IAM auth and tofu commands).

```bash
# Get URL and apply migrations in one command
DATABASE_URL=$(tofu -chdir=terraform output \
  -var-file="terraform.tfvars" -raw warehouse_database_url_admin) \
  alembic upgrade head
```

Other useful commands:

```bash
# Check current revision
DATABASE_URL=$(tofu -chdir=terraform output \
  -var-file="terraform.tfvars" -raw warehouse_database_url_admin) \
  alembic current

# Preview SQL without executing
DATABASE_URL=$(tofu -chdir=terraform output \
  -var-file="terraform.tfvars" -raw warehouse_database_url_admin) \
  alembic upgrade head --sql
```

**Note:** Dev environments each have their own warehouse DB, even though they share staging S3 and EventBridge. Make sure `terraform.tfvars` points to the correct environment.

## Schema Drift Recovery

Schema drift means the database schema doesn't match what the code/migrations expect. This can happen when:
- A migration was applied to the DB but later removed from the codebase
- Someone modified the DB schema directly
- A migration was partially applied

### How to Detect

- **In CI**: `test_migrations_are_up_to_date_with_models` fails
- **In production/dev**: Batch jobs fail with errors like `NotNullViolationError: null value in column "X"` (column exists in DB but code doesn't set it)
- **Manually**: Run `alembic upgrade head` and check for errors, or compare `alembic current` against expected head

### How to Fix

Create a migration that brings code in sync with DB reality:

```python
def upgrade() -> None:
    # Use IF NOT EXISTS to handle case where column already exists in DB
    op.execute("ALTER TABLE my_table ADD COLUMN IF NOT EXISTS my_column text")
    # Backfill existing rows
    op.execute("UPDATE my_table SET my_column = 'default' WHERE my_column IS NULL")
    # Then add constraint
    op.execute("ALTER TABLE my_table ALTER COLUMN my_column SET NOT NULL")
```

### Nuclear Option (Dev Environments Only)

If a dev warehouse is too drifted to migrate cleanly, tear it down and recreate:

```bash
tofu -chdir=terraform destroy \
  -var-file="terraform.tfvars" -target=module.warehouse
tofu -chdir=terraform apply \
  -var-file="terraform.tfvars" -target=module.warehouse

# Then apply all migrations to the fresh DB
DATABASE_URL=$(tofu -chdir=terraform output \
  -var-file="terraform.tfvars" -raw warehouse_database_url_admin) \
  alembic upgrade head
```

**Never do this in staging or production.** Only for dev environments where data loss is acceptable.

## When Migrations Fail

1. Check current state: `alembic current`
2. Revert: `alembic downgrade -1`
3. Fix the migration file
4. Test locally: `pytest tests/core/db/test_alembic_migrations.py -vv`
5. Retry: `alembic upgrade head`

If downgrade also fails, use the nuclear option above (dev only) or fix forward by creating a new corrective migration.

## Verification

Run before committing migration changes:

```bash
pytest tests/core/db/test_alembic_migrations.py -vv
```

This test suite:
- Applies all migrations from scratch to a fresh database
- Tests downgrade/upgrade cycle for reversibility
- Compares actual schema to SQLAlchemy models (catches drift)
- Verifies no multiple heads (branched history)

## Related Skills

- **`deploy-dev`** skill: For deploying migration changes to dev environments
- **`smoke-tests`** skill: For verifying the deployment works after migration
