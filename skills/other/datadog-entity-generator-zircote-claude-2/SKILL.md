---
name: datadog-entity-generator
description: >-
  Generate exhaustively complete and accurate Datadog Software Catalog entity YAML files (v3 schema) by examining project source code and interviewing engineers.
  Use when engineers need to create or update entity.datadog.yaml files for services, datastores, queues, APIs, or systems.
  Triggers include: "create entity yaml", "generate service catalog entry", "document this project in datadog", "create service definition", "add to software catalog", or any request involving Datadog entity/service documentation.
  Supports all v3 entity kinds: service, datastore, queue, api, system. Fetches existing Datadog data via API. Validates against official JSON schema. Merges with existing definitions. Outputs to .datadog/ directory.
---

# Datadog Entity Generator

Generate comprehensive, validated Datadog Software Catalog entity YAML files (v3 schema) through project analysis and engineer interviews.

## Workflow Overview

1. **Analyze project** - Scan source code for metadata signals
2. **Fetch existing Datadog data** - Query API for existing entities, teams, related services
3. **Interview engineer** - Fill gaps with targeted questions
4. **Generate YAML** - Create complete entity definition(s)
5. **Validate** - Check against official JSON schema
6. **Merge/Output** - Handle existing files, write to `.datadog/`

## Step 1: Project Analysis

Run the project analyzer to extract metadata signals:

```bash
uv run scripts/project_analyzer.py /path/to/project
```

**Detected signals:**
- `pyproject.toml`, `package.json`, `pom.xml`, `build.gradle` → name, description, language, dependencies
- `Dockerfile`, `docker-compose.yml` → service type, dependencies
- `kubernetes/`, `helm/`, `terraform/` → infrastructure, dependencies
- `.github/workflows/`, `.gitlab-ci.yml` → CI/CD pipelines
- `README.md`, `CODEOWNERS` → description, owners
- Existing `.datadog/entity.datadog.yaml` → merge base
- `openapi.yaml`, `swagger.json` → API definitions

**Output:** JSON with detected values and confidence levels.

## Step 2: Fetch Existing Datadog Data

Query Datadog API for context (requires `DD_API_KEY` and `DD_APP_KEY` in environment):

```bash
uv run scripts/datadog_fetcher.py --service-name <name>
```

**Fetches:**
- Existing entity definitions for the service
- Teams (for owner validation)
- Related services with dependencies
- Monitors, SLOs associated with service
- APM service topology (dependencies)

## Step 3: Engineer Interview

Conduct structured interview to fill gaps. See `references/interview-guide.md` for complete question bank.

**Interview strategy:**
1. Start with auto-detected values for confirmation
2. Ask only for missing required fields
3. Negotiate optional fields based on engineer preference
4. Validate URLs and integration patterns

**Core questions by entity kind:**

### Service
- Service name (confirm auto-detected or provide)
- Display name (human-readable)
- Owner team (validate against Datadog teams or accept new)
- Tier: `critical`, `high`, `medium`, `low`
- Lifecycle: `production`, `experimental`, `deprecated`
- Type: `web`, `grpc`, `rest`, `graphql`, `worker`, `custom`
- Languages (confirm from detection)
- Dependencies (services, datastores, queues)
- System membership (componentOf)
- PagerDuty service URL
- JIRA project
- Confluence space
- MS Teams channel
- Runbook URL
- Dashboard URL

### Datastore
- Type: `postgres`, `mysql`, `redis`, `mongodb`, `elasticsearch`, `cassandra`, `dynamodb`, etc.
- What services depend on this datastore?

### Queue
- Type: `kafka`, `rabbitmq`, `sqs`, `kinesis`, `pubsub`, etc.
- Producer and consumer services?

### API
- Type: `openapi`, `graphql`, `rest`, `grpc`
- OpenAPI spec file reference?
- Implementing service?

### System
- Component services, datastores, queues
- Domain/product area

**Required tags (HMH standards):**
- `env:` (production, staging, development)
- `service:` (service name)
- `tier:` (critical, high, medium, low)

## Step 4: Generate YAML

Use the entity generator with collected data:

```bash
uv run scripts/entity_generator.py --input collected_data.json --output .datadog/
```

**Multi-entity support:** For monorepos, generate multiple entities separated by `---` in single file or separate files.

## Step 5: Validate

Validate against official Datadog JSON schema:

```bash
uv run scripts/schema_validator.py .datadog/entity.datadog.yaml
```

Validation checks:
- Required fields present (apiVersion, kind, metadata.name)
- Valid enum values (lifecycle, tier, kind)
- URL formats for links and integrations
- Contact email format
- Tag format (`key:value`)

## Step 6: Merge & Output

If `.datadog/entity.datadog.yaml` exists:
- Parse existing definitions
- Deep merge with new data (new values override, arrays extend)
- Preserve custom extensions
- Show diff for engineer approval

**Output location:** `.datadog/entity.datadog.yaml`

## Entity Schema Quick Reference

See `references/v3-schema.md` for complete schema documentation.

### Common Structure (all kinds)

```yaml
apiVersion: v3
kind: service  # service | datastore | queue | api | system
metadata:
  name: my-service              # Required, unique identifier
  displayName: My Service       # Human-readable name
  namespace: default            # Optional, defaults to 'default'
  owner: team-name              # Primary owner team
  additionalOwners:             # Multi-ownership
    - name: sre-team
      type: operator
  description: Short description
  tags:
    - env:production
    - service:my-service
    - tier:critical
  contacts:
    - name: On-Call
      type: email
      contact: oncall@company.com
    - name: Team Channel
      type: microsoft-teams
      contact: https://teams.microsoft.com/l/channel/...
  links:
    - name: Runbook
      type: runbook
      url: https://confluence.company.com/runbook
    - name: Dashboard
      type: dashboard
      url: https://app.datadoghq.com/dashboard/xxx
    - name: Source Code
      type: repo
      provider: github
      url: https://github.com/org/repo
spec:
  lifecycle: production         # production | experimental | deprecated
  tier: critical                # critical | high | medium | low
  # ... kind-specific fields
integrations:
  pagerduty:
    serviceURL: https://company.pagerduty.com/service-directory/PXXXXXX
datadog:
  codeLocations:
    - repositoryURL: https://github.com/org/repo
      paths:
        - "src/**"
  logs:
    - name: Error Logs
      query: "service:my-service status:error"
  events:
    - name: Deployments
      query: "source:kubernetes service:my-service"
extensions:
  company.com/jira-project: PROJ
  company.com/confluence-space: https://confluence.company.com/space
```

### Service-specific spec

```yaml
spec:
  type: web                     # web | grpc | rest | graphql | worker
  languages:
    - python
    - go
  dependsOn:
    - service:auth-service
    - datastore:postgres-main
    - queue:events-kafka
  componentOf:
    - system:platform
```

### Datastore-specific spec

```yaml
spec:
  type: postgres                # postgres | mysql | redis | mongodb | etc.
  dependencyOf:                 # Services that depend on this
    - service:api-service
```

### Queue-specific spec

```yaml
spec:
  type: kafka                   # kafka | rabbitmq | sqs | kinesis
  componentOf:
    - system:messaging
```

### System-specific spec

```yaml
spec:
  components:
    - service:web-frontend
    - service:api-backend
    - datastore:main-db
    - queue:events
```

## Integration URL Patterns

See `references/integration-patterns.md` for complete patterns.

**PagerDuty:** `https://<subdomain>.pagerduty.com/service-directory/P<alphanumeric>`

**JIRA:** Extension field `company.com/jira-project: <PROJECT_KEY>`

**Confluence:** Link with `type: doc`, `provider: confluence`

**MS Teams:** Contact with `type: microsoft-teams`, URL format: `https://teams.microsoft.com/l/channel/...`

**Snyk/SonarQube/BrowserStack/Orca:** Custom extensions field

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/project_analyzer.py` | Analyze project for metadata signals |
| `scripts/datadog_fetcher.py` | Fetch existing Datadog entities and context |
| `scripts/entity_generator.py` | Generate entity YAML from collected data |
| `scripts/schema_validator.py` | Validate YAML against JSON schema |

## Confidence Thresholds

- **Auto-apply (≥90%):** Directly include in YAML without confirmation
- **Confirm (70-89%):** Present to engineer for confirmation
- **Ask (< 70%):** Ask engineer to provide value

## Interview Best Practices

1. Present all auto-detected values first for batch confirmation
2. Group related questions (e.g., all contacts together)
3. Provide examples for complex fields (URLs, queries)
4. Validate URLs and patterns in real-time
5. Explain why each field matters for adoption
6. Offer to skip optional fields with explicit acknowledgment
