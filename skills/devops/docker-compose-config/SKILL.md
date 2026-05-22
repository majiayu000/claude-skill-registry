---
name: docker-compose-config
description: Docker Compose configuration template and validation logic for MetaSaver monorepos. Includes 4 required standards (PostgreSQL service with project-prefixed env vars like RUGBYCRM_POSTGRES_USER or METASAVER_SILVER_POSTGRES_USER for multi-db, project-specific naming for containers and networks, volumes section, service health checks). Use when creating or auditing docker-compose.yml files.
---

# Docker Compose Configuration Skill

This skill provides docker-compose.yml template and validation logic for containerized service orchestration.

## Purpose

Manage docker-compose.yml configuration to:

- Configure PostgreSQL database service with project-prefixed environment variables
- Set up project-specific naming for containers, networks, volumes
- Configure service health checks

## Usage

This skill is invoked by the `docker-compose-agent` when:

- Creating new docker-compose.yml files
- Auditing existing Docker Compose configurations
- Validating Docker Compose against standards

## Templates

**Single-database template:**

```
templates/docker-compose.yml.template
```

**Multi-database template:**

```
templates/docker-compose.multi-db.yml.template
```

Use the multi-db template when a project has multiple database tiers (e.g., silver, gold).

**Placeholders to replace:**

- `{project}` - lowercase project name (e.g., `rugby-crm`)
- `{PROJECT}` - uppercase for comments (e.g., `RUGBY CRM`)
- `<PREFIX>` - uppercase env var prefix (e.g., `RUGBYCRM`)
- `<DBNAME>` - optional database tier name for multi-db projects (e.g., `SILVER`, `GOLD`)
- `{PORT}` - external port number (e.g., `5434`)

## Environment Variable Naming Pattern

**Pattern:** `{APPLICATION_NAME}_{DBNAME_OPTIONAL}_POSTGRES_{FIELD}`

| Project Type    | Example                          | Pattern                        |
| --------------- | -------------------------------- | ------------------------------ |
| Single-database | `RUGBYCRM_POSTGRES_USER`         | `PREFIX_POSTGRES_FIELD`        |
| Multi-database  | `METASAVER_SILVER_POSTGRES_USER` | `PREFIX_DBNAME_POSTGRES_FIELD` |

**Fields:** `USER`, `PASSWORD`, `DB`, `PORT`

**Multi-database examples (metasaver-com):**

- Silver tier: `METASAVER_SILVER_POSTGRES_USER`, `METASAVER_SILVER_POSTGRES_PASSWORD`, `METASAVER_SILVER_POSTGRES_DB`, `METASAVER_SILVER_POSTGRES_PORT`
- Gold tier: `METASAVER_GOLD_POSTGRES_USER`, `METASAVER_GOLD_POSTGRES_PASSWORD`, `METASAVER_GOLD_POSTGRES_DB`, `METASAVER_GOLD_POSTGRES_PORT`

## The 4 Docker Compose Standards

### Rule 1: PostgreSQL Service Configuration

Must include PostgreSQL service with project-prefixed environment variables:

```yaml
services:
  postgres:
    image: postgres:17-alpine
    container_name: rugby-crm-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${RUGBYCRM_POSTGRES_USER}
      POSTGRES_PASSWORD: ${RUGBYCRM_POSTGRES_PASSWORD}
      POSTGRES_DB: ${RUGBYCRM_POSTGRES_DB}
    ports:
      - "${RUGBYCRM_POSTGRES_PORT}:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - rugby-crm-network
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -U ${RUGBYCRM_POSTGRES_USER} -d ${RUGBYCRM_POSTGRES_DB}",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
```

Required fields:

- `image` - PostgreSQL version (recommend 17-alpine)
- `container_name` - Project-specific name (e.g., `rugby-crm-postgres`)
- `restart` - Must be `unless-stopped` or `always`
- `environment` - Project-prefixed: `{PREFIX}_POSTGRES_USER`, `{PREFIX}_POSTGRES_PASSWORD`, `{PREFIX}_POSTGRES_DB`
- `ports` - Port mapping with project-prefixed variable
- `volumes` - Named volume for data persistence
- `networks` - Project-specific network name

### Rule 2: Project-Prefixed Environment Variables

All env vars must use project prefix pattern: `${<PREFIX>_[DBNAME_]POSTGRES_*}`

- **Single-database:** `${RUGBYCRM_POSTGRES_USER}`, `${RESUMEBUILDER_POSTGRES_USER}`
- **Multi-database:** `${METASAVER_SILVER_POSTGRES_USER}`, `${METASAVER_GOLD_POSTGRES_USER}`

### Rule 3: Volumes and Networks Sections

Must include project-specific naming:

- `volumes.postgres-data`
- `networks.{project}-network` with `driver: bridge`

### Rule 4: Service Health Checks

PostgreSQL service must include healthcheck with: `test` (using prefixed vars), `interval` (10s), `timeout` (5s), `retries` (5).

## Validation

Workflow:

1. Parse YAML and verify services section exists
2. Validate postgres service has all required fields
3. Check environment variables use project-prefix pattern (e.g., `RUGBYCRM_POSTGRES_*` or `METASAVER_SILVER_POSTGRES_*`)
4. Verify volumes and networks sections exist with project-specific names
5. Validate healthcheck references correct prefixed variables
6. Report violations

## Repository Type Considerations

- **Consumer Repos**: Must follow all 4 standards unless exception declared
- **Library Repos**: May not need docker-compose.yml

## Best Practices

1. **No version field** - `version: "3.8"` is deprecated and should be omitted
2. Place docker-compose.yml at monorepo root
3. Use consistent project prefix across all env vars (e.g., `RUGBYCRM_` or `METASAVER_SILVER_`)
4. Match .env.example variables: `{PREFIX}_[DBNAME_]POSTGRES_USER`, `{PREFIX}_[DBNAME_]POSTGRES_PASSWORD`, `{PREFIX}_[DBNAME_]POSTGRES_DB`, `{PREFIX}_[DBNAME_]POSTGRES_PORT`
5. Use alpine images for smaller footprint
6. Always include health checks for databases
7. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `env-example-agent` - Environment variable management
