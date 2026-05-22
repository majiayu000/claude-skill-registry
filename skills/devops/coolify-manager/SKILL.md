---
name: coolify-manager
description: >-
  Coolify Server Manager. Use this skill when you need to perform commands on
  user's server on user's behalf
---
## Overview

Use this skill when you need to:
- Report server/resource/application status
- Cnahge server/resource/application setting

## Tool Commands for [Coolify](https://coolify.io) API

### Servers

Commands can use `server` or `servers` interchangeably.

- `coolify server list` - List all servers
- `coolify server get <uuid>` - Get a server by UUID
  - `--resources` - Get the resources and their status of a server
- `coolify server add <name> <ip> <private_key_uuid>` - Add a new server
  - `-p, --port <port>` - SSH port (default: 22)
  - `-u, --user <user>` - SSH user (default: root)
  - `--validate` - Validate server immediately after adding
- `coolify server remove <uuid>` - Remove a server
- `coolify server validate <uuid>` - Validate a server connection
- `coolify server domains <uuid>` - Get server domains by UUID

### Projects
- `coolify projects list` - List all projects
- `coolify projects get <uuid>` - Get project environments

### Resources
- `coolify resources list` - List all resources

### Applications
- `coolify app list` - List all applications
- `coolify app get <uuid>` - Get application details
- `coolify app update <uuid>` - Update application configuration
  - `--name <name>` - Application name
  - `--description <description>` - Application description
  - `--git-branch <branch>` - Git branch
  - `--git-repository <url>` - Git repository URL
  - `--domains <domains>` - Domains (comma-separated)
  - `--build-command <cmd>` - Build command
  - `--start-command <cmd>` - Start command
  - `--install-command <cmd>` - Install command
  - `--base-directory <path>` - Base directory
  - `--publish-directory <path>` - Publish directory
  - `--dockerfile <content>` - Dockerfile content
  - `--docker-image <image>` - Docker image name
  - `--docker-tag <tag>` - Docker image tag
  - `--ports-exposes <ports>` - Exposed ports
  - `--ports-mappings <mappings>` - Port mappings
  - `--health-check-enabled` - Enable health check
  - `--health-check-path <path>` - Health check path
- `coolify app delete <uuid>` - Delete an application
  - `-f, --force` - Skip confirmation prompt
- `coolify app start <uuid>` - Start an application
- `coolify app stop <uuid>` - Stop an application
- `coolify app restart <uuid>` - Restart an application
- `coolify app logs <uuid>` - Get application logs

#### Application Environment Variables
- `coolify app env list <app_uuid>` - List all environment variables
- `coolify app env get <app_uuid> <env_uuid_or_key>` - Get a specific environment variable
- `coolify app env create <app_uuid>` - Create a new environment variable
  - `--key <key>` - Variable key (required)
  - `--value <value>` - Variable value (required)
  - `--preview` - Available in preview deployments
  - `--build-time` - Available at build time
  - `--is-literal` - Treat value as literal (don't interpolate variables)
  - `--is-multiline` - Value is multiline
- `coolify app env update <app_uuid> <env_uuid>` - Update an environment variable
- `coolify app env delete <app_uuid> <env_uuid>` - Delete an environment variable
- `coolify app env sync <app_uuid>` - Sync environment variables from a .env file
  - `--file <path>` - Path to .env file (required)
  - `--build-time` - Make all variables available at build time
  - `--preview` - Make all variables available in preview deployments
  - `--is-literal` - Treat all values as literal (don't interpolate variables)
  - **Behavior**: Updates existing variables, creates missing ones. Does NOT delete variables not in the file.

#### Application Deployments
- `coolify app deployments list <app-uuid>` - List all deployments for an application
- `coolify app deployments logs <app-uuid> [deployment-uuid]` - Get deployment logs (formatted as human-readable text)
  - If only `app-uuid` is provided: retrieves logs from the **latest/most recent deployment only**
  - If `deployment-uuid` is also provided: retrieves logs for that **specific deployment**
  - `-n, --lines <n>` - Number of log lines to display (default: 0 = all lines)
  - `-f, --follow` - Follow log output in real-time (like tail -f)
  - `--debuglogs` - Show debug logs (includes hidden commands and internal operations)

### Databases
- `coolify database list` - List all databases
- `coolify database get <uuid>` - Get database details
- `coolify database create <type>` - Create a new database
  - Supported types: `postgresql`, `mysql`, `mariadb`, `mongodb`, `redis`, `keydb`, `clickhouse`, `dragonfly`
  - `--server-uuid <uuid>` - Server UUID (required)
  - `--project-uuid <uuid>` - Project UUID (required)
  - `--environment-name <name>` - Environment name (required unless using --environment-uuid)
  - `--environment-uuid <uuid>` - Environment UUID (required unless using --environment-name)
  - `--destination-uuid <uuid>` - Destination UUID if server has multiple destinations
  - `--name <name>` - Database name
  - `--description <description>` - Database description
  - `--image <image>` - Docker image
  - `--instant-deploy` - Deploy immediately after creation
  - `--is-public` - Make database publicly accessible
  - `--public-port <port>` - Public port number
  - `--limits-memory <size>` - Memory limit (e.g., '512m', '2g')
  - `--limits-cpus <cpus>` - CPU limit (e.g., '0.5', '2')
  - Database-specific flags (postgres-user, mysql-root-password, etc.)
- `coolify database update <uuid>` - Update database configuration
- `coolify database delete <uuid>` - Delete a database
  - `--delete-configurations` - Delete configurations (default: true)
  - `--delete-volumes` - Delete volumes (default: true)
  - `--docker-cleanup` - Run docker cleanup (default: true)
  - `--delete-connected-networks` - Delete connected networks (default: true)
- `coolify database start <uuid>` - Start a database
- `coolify database stop <uuid>` - Stop a database
- `coolify database restart <uuid>` - Restart a database

#### Database Backups
- `coolify database backup list <database_uuid>` - List all backup configurations
- `coolify database backup create <database_uuid>` - Create a new backup configuration
  - `--frequency <cron>` - Backup frequency (cron expression)
  - `--enabled` - Enable backup schedule
  - `--save-s3` - Save backups to S3
  - `--s3-storage-uuid <uuid>` - S3 storage UUID
  - `--databases-to-backup <list>` - Comma-separated list of databases to backup
  - `--dump-all` - Dump all databases
  - `--retention-amount-local <n>` - Number of backups to retain locally
  - `--retention-days-local <n>` - Days to retain backups locally
  - `--retention-storage-local <size>` - Max storage for local backups (e.g., '1GB', '500MB')
  - `--retention-amount-s3 <n>` - Number of backups to retain in S3
  - `--retention-days-s3 <n>` - Days to retain backups in S3
  - `--retention-storage-s3 <size>` - Max storage for S3 backups (e.g., '1GB', '500MB')
  - `--timeout <seconds>` - Backup timeout in seconds
  - `--disable-local` - Disable local backup storage
- `coolify database backup update <database_uuid> <backup_uuid>` - Update a backup configuration
- `coolify database backup delete <database_uuid> <backup_uuid>` - Delete a backup configuration
- `coolify database backup trigger <database_uuid> <backup_uuid>` - Trigger an immediate backup
- `coolify database backup executions <database_uuid> <backup_uuid>` - List backup executions
- `coolify database backup delete-execution <database_uuid> <backup_uuid> <execution_uuid>` - Delete a backup execution

### Services
- `coolify service list` - List all services
- `coolify service get <uuid>` - Get service details
- `coolify service start <uuid>` - Start a service
- `coolify service stop <uuid>` - Stop a service
- `coolify service restart <uuid>` - Restart a service
- `coolify service delete <uuid>` - Delete a service

#### Service Environment Variables
- `coolify service env list <service_uuid>` - List all environment variables
- `coolify service env get <service_uuid> <env_uuid_or_key>` - Get a specific environment variable
- `coolify service env create <service_uuid>` - Create a new environment variable
  - Same flags as application environment variables
- `coolify service env update <service_uuid> <env_uuid>` - Update an environment variable
- `coolify service env delete <service_uuid> <env_uuid>` - Delete an environment variable
- `coolify service env sync <service_uuid>` - Sync environment variables from a .env file
  - `--file <path>` - Path to .env file (required)
  - `--build-time` - Make all variables available at build time
  - `--preview` - Make all variables available in preview deployments
  - `--is-literal` - Treat all values as literal (don't interpolate variables)
  - **Behavior**: Updates existing variables, creates missing ones. Does NOT delete variables not in the file.

### Deployments
- `coolify deploy uuid <uuid>` - Deploy a resource by UUID
  - `-f, --force` - Force deployment
- `coolify deploy name <name>` - Deploy a resource by name
  - `-f, --force` - Force deployment
- `coolify deploy batch <name1,name2,...>` - Deploy multiple resources at once
  - `-f, --force` - Force all deployments
- `coolify deploy list` - List all deployments
- `coolify deploy get <uuid>` - Get deployment details
- `coolify deploy cancel <uuid>` - Cancel a deployment
  - `-f, --force` - Skip confirmation prompt

### GitHub Apps
- `coolify github list` - List all GitHub App integrations
- `coolify github get <app_uuid>` - Get GitHub App details
- `coolify github create` - Create a new GitHub App integration
  - `--name <name>` - GitHub App name (required)
  - `--api-url <url>` - GitHub API URL (required, e.g., https://api.github.com)
  - `--html-url <url>` - GitHub HTML URL (required, e.g., https://github.com)
  - `--app-id <id>` - GitHub App ID (required)
  - `--installation-id <id>` - GitHub Installation ID (required)
  - `--client-id <id>` - GitHub OAuth Client ID (required)
  - `--client-secret <secret>` - GitHub OAuth Client Secret (required)
  - `--private-key-uuid <uuid>` - UUID of existing private key (required)
  - `--organization <org>` - GitHub organization
  - `--custom-user <user>` - Custom user for SSH (default: git)
  - `--custom-port <port>` - Custom port for SSH (default: 22)
  - `--webhook-secret <secret>` - GitHub Webhook Secret
  - `--system-wide` - Is this app system-wide (cloud only)
- `coolify github update <app_uuid>` - Update a GitHub App
- `coolify github delete <app_uuid>` - Delete a GitHub App
  - `-f, --force` - Skip confirmation prompt
- `coolify github repos <app_uuid>` - List repositories accessible by a GitHub App
- `coolify github branches <app_uuid> <owner/repo>` - List branches for a repository

### Teams
- `coolify team list` - List all teams
- `coolify team get <team_id>` - Get team details
- `coolify team current` - Get current team
- `coolify team members list [team_id]` - List team members

### Private Keys

Commands can use `private-key`, `private-keys`, `key`, or `keys` interchangeably.

- `coolify private-key list` - List all private keys
- `coolify private-key add <key_name> <private-key>` - Add a new private key
  - Use `@filename` to read from file: `coolify private-key add mykey @~/.ssh/id_rsa`
- `coolify private-key remove <uuid>` - Remove a private key

## Global Flags

All commands support these global flags:

- `--context <name>` - Use a specific context instead of default
- `--host <fqdn>` - Override the Coolify instance hostname
- `--token <token>` - Override the authentication token
- `--format <format>` - Output format: `table` (default), `json`, or `pretty`
- `-s, --show-sensitive` - Show sensitive information (tokens, IPs, etc.)
- `-f, --force` - Force operation (skip confirmations)
- `--debug` - Enable debug mode

## Examples

### Multi-Environment Workflows

```bash
# Add multiple contexts
coolify context add prod https://prod.coolify.io <prod-token>
coolify context add staging https://staging.coolify.io <staging-token>
coolify context add dev https://dev.coolify.io <dev-token>

# Set default
coolify context use prod

# Use different contexts
coolify --context=staging servers list
coolify --context=prod deploy name api
coolify --context=dev resources list

# Default context (prod in this case)
coolify servers list
```

### Application Management

```bash
# List all applications
coolify app list

# Get application details
coolify app get <uuid>

# Manage application lifecycle
coolify app start <uuid>
coolify app stop <uuid>
coolify app restart <uuid>

# View application logs
coolify app logs <uuid>

# Environment variables
coolify app env list <uuid>
coolify app env create <uuid> --key API_KEY --value secret123

# Sync from .env file (updates existing, creates new, keeps others unchanged)
coolify app env sync <uuid> --file .env
coolify app env sync <uuid> --file .env.production --build-time --preview
```

### Database Management

```bash
# List databases
coolify database list

# Create a PostgreSQL database
coolify database create postgresql \
  --server-uuid <server-uuid> \
  --project-uuid <project-uuid> \
  --name mydb \
  --instant-deploy

# Manage database lifecycle
coolify database start <uuid>
coolify database stop <uuid>
coolify database restart <uuid>

# Backup management
coolify database backup list <database-uuid>
coolify database backup create <database-uuid> \
  --frequency "0 2 * * *" \
  --enabled \
  --save-s3 \
  --retention-days-locally 7
coolify database backup trigger <database-uuid> <backup-uuid>
```

### Service Management

```bash
# List services
coolify service list

# Get service details
coolify service get <uuid>

# Manage services
coolify service start <uuid>
coolify service restart <uuid>

# Environment variables (same as applications)
coolify service env sync <uuid> --file .env
```

### Deploy Workflows

```bash
# Deploy single app by name (easier than UUID)
coolify deploy name my-application

# Deploy multiple apps at once
coolify deploy batch api,worker,frontend

# Force deploy with specific context
coolify --context=prod deploy batch api,worker --force

# Traditional UUID deployment still works
coolify deploy uuid abc123-def456-...

# Monitor deployments
coolify deploy list
coolify deploy get <deployment-uuid>

# Cancel a deployment
coolify deploy cancel <deployment-uuid>
```

### GitHub Apps Integration

```bash
# List GitHub Apps
coolify github list

# Create a GitHub App integration
coolify github create \
  --name "My GitHub App" \
  --api-url "https://api.github.com" \
  --html-url "https://github.com" \
  --app-id 123456 \
  --installation-id 789012 \
  --client-id "Iv1.abc123" \
  --client-secret "secret" \
  --private-key-uuid <key-uuid>

# List repositories accessible by the app
coolify github repos <app-uuid>

# List branches for a repository
coolify github branches <app-uuid> owner/repo

# Delete a GitHub App
coolify github delete <app-uuid>
```

### Team Management

```bash
# List teams
coolify team list

# Get current team
coolify team current

# List team members
coolify team members list
```

### Server Management

```bash
# List servers in production
coolify --context=prod server list

# Add a server with validation
coolify server add myserver 192.168.1.100 <key-uuid> --validate

# Get server details with resources
coolify server get <uuid> --resources
```

## Output Formats

The CLI supports three output formats:

```bash
# Table format (default, human-readable)
coolify server list

# JSON format (for scripts)
coolify server list --format=json

# Pretty JSON (for debugging)
coolify server list --format=pretty
```
