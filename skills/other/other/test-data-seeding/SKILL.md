---
name: test-data-seeding
description: >
  A skill for generating and seeding realistic test data into a database.
  Use this skill for tasks related to database seeding, test data generation,
  and populating a database for development, testing, or demo purposes.
  It supports idempotent seeding, relationship data generation (e.g., users and their tasks),
  and environment-specific data sets (dev, test, demo).
  Triggers: "seed database", "generate test data", "populate db", "database seeding".
---

# Test Data Seeding Skill

This skill provides a complete framework for seeding your database with realistic test data using Python and the Faker library. It is designed to be customizable for your specific data models and ORM.

## Core Features

- **Realistic Data Generation**: Uses the **Faker** library.
- **Idempotent Seeding**: Scripts are designed to be run multiple times without creating duplicate data.
- **Relationship-Aware**: Handles generation of data with parent-child relationships (e.g., users and their tasks).
- **Environment-Specific**: Configure different data volumes for `dev`, `test`, and `demo` environments.
- **Performance Optimized**: Uses bulk inserts where possible.
- **Data Cleanup**: Includes a script to reset the database.
- **Versioning**: Seed data generation is deterministic and can be versioned by committing the scripts.

## How to Use This Skill

The workflow is as follows:

1.  **Configure Your Models**: Update `references/data_models.md` and the model import sections in the Python scripts.
2.  **Customize the Scripts**: Modify `scripts/reset_db.py` and `scripts/seed.py` to work with your specific ORM and database connection.
3.  **Run the Seeding Command**: Use the `scripts/invoke_seeding.sh` command to reset and/or seed your database.

## Bundled Resources

### Scripts (`scripts/`)

-   **`invoke_seeding.sh`**: The main CLI for this skill. Use it to run the seeding process.
    ```bash
    # Seed the 'dev' environment
    bash scripts/invoke_seeding.sh dev

    # Reset the database and then seed the 'demo' environment
    bash scripts/invoke_seeding.sh demo --reset
    ```
    *Make sure the script is executable: `chmod +x scripts/invoke_seeding.sh`*

-   **`seed.py`**: The core data generation and seeding script.
    -   **TODO**: You must configure your database connection and ORM logic in the `TODO` sections at the top of the file.
    -   You can customize the number of records for each environment in the `SEED_COUNTS` dictionary.

-   **`reset_db.py`**: A script to wipe all data from your tables.
    -   **TODO**: You must configure this script with your database connection and provide your models in the correct order for deletion to respect foreign key constraints.

### References (`references/`)

-   **`data_models.md`**: A template document to define your database schema. You should replace the example content with your actual models. This helps in understanding the data structure when customizing the seeding script.

-   **`faker_examples.md`**: A handy reference guide with examples of how to use the Faker library to generate different kinds of data. Refer to this when you want to customize the data being generated in `scripts/seed.py`.
