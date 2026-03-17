---
name: idempiere-setup
description: Orchestrates the setup of an iDempiere development environment using the setup.sh script. Use when the user wants to install Eclipse, clone iDempiere source code, run Maven builds, or configure the database for iDempiere development.
---

# iDempiere Setup

This skill automates the setup of an iDempiere development environment using the local `setup.sh` script.

## Core Tasks

### Full Environment Setup
To perform a complete setup including Eclipse, source code, and database configuration:
```bash
./setup.sh [options]
```

### Workspace Only Setup
To install Eclipse and clone/update source code without database configuration:
```bash
./setup.sh --skip-setup-db [options]
```

### Database Only Setup
To configure the database and server environment without setting up the Eclipse workspace:
```bash
./setup.sh --skip-setup-ws [options]
```

## Configuration Options

### Database Configuration
- `--db-type <postgresql|oracle>`: Default is `postgresql`.
- `--db-host <host>`: Default is `localhost`.
- `--db-port <port>`: Default is `5432` for PostgreSQL, `1521` for Oracle.
- `--db-name <name>`: Default is `idempiere`.
- `--db-user <user>`: Default is `adempiere`.
- `--db-pass <pass>`: Default is `adempiere`.
- `--db-admin-pass <pass>`: Password for `postgres` (PostgreSQL) or `system` (Oracle).

### Docker Integration
- `--docker-postgres-create`: Create and run a PostgreSQL Docker container.
- `--docker-postgres-name <name>`: Set the container name (default: `postgres`).
- `--oracle-docker-container <name>`: Specify an existing Oracle Docker container.
- `--oracle-docker-home <path>`: Oracle home inside the container (default: `/opt/oracle`).

### Source Code Configuration
- `--branch <branch_name>`: Checkout a specific branch (e.g., `release-11`).
- `--repository-url <url>`: Use a custom git repository.
- `--source <folder>`: Set the source folder name (default: `idempiere`).

### HTTP/HTTPS Configuration
- `--http-host <ip>`: Listen address (default: `0.0.0.0`).
- `--http-port <port>`: HTTP port (default: `8080`).
- `--https-port <port>`: HTTPS port (default: `8443`).

### Other Options
- `--load-idempiere-env`: Load environment variables from `idempiereEnv.properties`.
- `--eclipse <folder>`: Path to the Eclipse IDE folder (default: `eclipse`).
- `--skip-migration-script`: Do not run database migration scripts.
- `--install-copilot`: Automatically install the Copilot plugin.

## Common Scenarios

- **New Developer Setup (PostgreSQL):**
  `./setup.sh --docker-postgres-create --db-admin-pass mypassword`
- **Updating Existing Workspace:**
  `./setup.sh --skip-setup-db`
- **Re-configuring Database:**
  `./setup.sh --skip-setup-ws --db-pass newpassword`

## Instructions
- Before running any setup scripts, check the operating system. If on Windows, use git-bash.exe to execute the .sh files. If Git Bash is not found, ask the user to switch to a WSL terminal.
- Perform setup in current folder, not from the skill folder. Please get user confirmation for current working folder before start running of the setup workflow.
- If on Linux, copy eclipse.sh from the skill folder to the user confirm destination folder. Please only copy eclipse.sh, not other files.
