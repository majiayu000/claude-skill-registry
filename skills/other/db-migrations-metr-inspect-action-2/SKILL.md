---
name: database-migrations
description: How to create and use our alembic database migration tool. Use when making changes to models.py.
---

## Instructions

Do not write out alembic migrations yourself. Use the alembic tool to generate and apply migrations.
You do not need to give alembic the path to alembic.ini.
Do not manually drop any tables or columns in the DB. Always use alembic migrations to make schema changes.

Alembic depends on having a valid DATABASE_URL set. The username should be inspect_admin. The password will be automatically generated via RDS IAM.

The URL depends on the environment you are working in. E.g. it should follow a pattern like DATABASE_URL='postgresql://inspect_admin@{environment}-inspect-ai-warehouse.cluster-{cluster-id}.{region}.rds.amazonaws.com/inspect'
`tofu output -var-file="${ENVIRONMENT}.tfvars" -raw warehouse_database_url_admin` will return the correct URL for the given environment.

Make sure to have AWS_PROFILE=staging set for RDS IAM auth and tofu commands.

To create a new migration, run:

`alembic revision --autogenerate -m "description of changes"`

Run `ruff check --fix && ruff format` to silence any formatting issues in the generated migration file.

You may need to ensure the DB is up to date before generating a new migration. Run:
`alembic upgrade head`

If we want to regenerate a migration file (in a branch we're working on after making schema changes since the last migration), we can delete the previous migration file and run the revision command again.

1. Run `alembic downgrade -1` to revert the last migration.
2. Delete the migration file from the versions/ directory.
3. Run `alembic upgrade head` to ensure the DB is up to date.
4. Run the revision command again to generate a new migration file.

## Verification

Run the tests in `tests/core/db/test_alembic_migrations.py`
