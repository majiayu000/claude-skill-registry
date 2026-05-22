---
name: create-container-documentation
description: Generates README.md, CHANGELOG.md, and event documentation following ModuleImplementationGuide.md Section 13 standards. Creates README with required sections (overview, setup, API endpoints, configuration), generates CHANGELOG entries following semantic versioning, documents published/consumed events (logs-events.md, notifications-events.md), and creates OpenAPI spec documentation. Use when documenting new services, updating API docs, or creating event documentation.
---

# Create Container Documentation

Generates documentation following ModuleImplementationGuide.md Section 13.

## README.md

Reference: ModuleImplementationGuide.md Section 13.1, containers/auth/README.md

### Required Sections

```markdown
# [Module Name] Module

[Brief description of what the module does]

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Prerequisites
- Node.js 20+
- Azure Cosmos DB NoSQL account
- RabbitMQ 3.12+ (if using events)

### Installation
\`\`\`bash
npm install
\`\`\`

### Configuration
\`\`\`bash
cp config/default.yaml config/local.yaml
# Edit config/local.yaml with your settings
\`\`\`

### Database Setup

The module uses Azure Cosmos DB NoSQL (shared database with prefixed containers). Ensure the following containers exist:

- \`[module-name]_data\` - Main data container
- \`[module-name]_[other]\` - Other containers if needed

### Running
\`\`\`bash
# Development
npm run dev

# Production
npm run build
npm start
\`\`\`

## Configuration Reference

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| server.port | number | 3XXX | Server port |
| server.host | string | 0.0.0.0 | Server host |
| cosmos_db.endpoint | string | - | Cosmos DB endpoint URL (required) |
| cosmos_db.key | string | - | Cosmos DB access key (required) |

See \`config/default.yaml\` for full configuration options.

## API Reference

See [OpenAPI Specification](./openapi.yaml)

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | \`/api/v1/resource\` | List resources |
| POST | \`/api/v1/resource\` | Create resource |
| GET | \`/api/v1/resource/:id\` | Get resource |
| PUT | \`/api/v1/resource/:id\` | Update resource |
| DELETE | \`/api/v1/resource/:id\` | Delete resource |
| GET | \`/health\` | Liveness check |
| GET | \`/ready\` | Readiness check |

## Events

For detailed event documentation including schemas and examples, see:
- [Logs Events](./docs/logs-events.md) - Events that get logged (if applicable)
- [Notifications Events](./docs/notifications-events.md) - Events that trigger notifications (if applicable)

### Published Events

| Event | Description |
|-------|-------------|
| \`[module].resource.created\` | Resource created |
| \`[module].resource.updated\` | Resource updated |

### Consumed Events

| Event | Description |
|-------|-------------|
| \`other.event.name\` | Description |

## Development

### Running Tests
\`\`\`bash
npm test
npm run test:coverage
\`\`\`

## Dependencies

- **Service Name**: For [purpose]
- **Other Service**: For [purpose]

## License

Proprietary
```

## CHANGELOG.md

Reference: ModuleImplementationGuide.md Section 13.2

```markdown
# Changelog

All notable changes to this module will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - YYYY-MM-DD

### Added
- Initial module creation
- Core functionality
- API endpoints for resource management
- Event publishing for resource lifecycle

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A
```

## Event Documentation

Reference: ModuleImplementationGuide.md Section 9.5

### logs-events.md

Create in module root if module publishes events that get logged:

```markdown
# [Module Name] - Logs Events

## Overview

This document describes all events published by the [Module Name] module that are consumed by the Logging service for audit trail and compliance logging.

## Published Events

### [domain].[entity].[action]

**Description**: When this event is triggered.

**Triggered When**: 
- Condition 1
- Condition 2

**Event Type**: \`[domain].[entity].[action]\`

**Event Schema**:

\`\`\`json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "timestamp", "version", "source", "data"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event ID"
    },
    "type": {
      "type": "string",
      "enum": ["[domain].[entity].[action]"],
      "description": "Event type"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    },
    "version": {
      "type": "string",
      "description": "Event schema version (e.g., '1.0')"
    },
    "source": {
      "type": "string",
      "description": "Module that emitted the event (e.g., '[module-name]')"
    },
    "correlationId": {
      "type": "string",
      "description": "Request correlation ID (optional)"
    },
    "organizationId": {
      "type": "string",
      "format": "uuid",
      "description": "Tenant context (optional)"
    },
    "userId": {
      "type": "string",
      "format": "uuid",
      "description": "Actor user ID (optional)"
    },
    "data": {
      "type": "object",
      "required": ["resourceId"],
      "properties": {
        "resourceId": {
          "type": "string",
          "format": "uuid",
          "description": "ID of the resource"
        }
      }
    }
  }
}
\`\`\`

**Example Event**:

\`\`\`json
{
  "id": "evt_12345678-1234-1234-1234-123456789abc",
  "type": "[domain].[entity].[action]",
  "timestamp": "2025-01-22T10:00:00Z",
  "version": "1.0",
  "source": "[module-name]",
  "correlationId": "req_45678901-2345-2345-2345-234567890def",
  "organizationId": "org_78901234-3456-3456-3456-345678901ghi",
  "userId": "user_90123456-4567-4567-4567-456789012jkl",
  "data": {
    "resourceId": "res_12345678-1234-1234-1234-123456789abc"
  }
}
\`\`\`

---

## Consumed Events

The [Module Name] module does not consume events from other modules.
```

### notifications-events.md

Create in module root if module publishes events that trigger notifications:

```markdown
# [Module Name] - Notifications Events

## Overview

This document describes all events published by the [Module Name] module that trigger notifications to users via the Notification service.

## Published Events

### [domain].[entity].[action]

**Description**: Emitted when [condition]. Triggers [notification type].

**Triggered When**: 
- Condition 1
- Condition 2

**Event Type**: \`[domain].[entity].[action]\`

**Notification Triggered**: [Notification description]

**Event Schema**: See [logs-events.md](./logs-events.md#[domain].[entity].[action]) for complete schema.

**Example Event**:

\`\`\`json
{
  "id": "evt_12345678-1234-1234-1234-123456789abc",
  "type": "[domain].[entity].[action]",
  "timestamp": "2025-01-22T10:00:00Z",
  "version": "1.0",
  "source": "[module-name]",
  "organizationId": "org_78901234-3456-3456-3456-345678901ghi",
  "data": {
    "resourceId": "res_12345678-1234-1234-1234-123456789abc"
  }
}
\`\`\`

---

## Consumed Events

The [Module Name] module does not consume events from other modules.
```

## OpenAPI Specification

Reference: ModuleImplementationGuide.md Section 7.4

Create `openapi.yaml` in module root:

```yaml
openapi: 3.0.3
info:
  title: [Module Name] API
  version: 1.0.0
  description: |
    [Module description]
    
    ## Authentication
    All endpoints require JWT authentication via Bearer token.
    
    ## Rate Limiting
    - 100 requests per minute per user
    - 1000 requests per minute per organization

servers:
  - url: /api/v1
    description: API Version 1

tags:
  - name: Resources
    description: Resource management

paths:
  /resources:
    get:
      summary: List resources
      tags: [Resources]
      security:
        - bearerAuth: []
      parameters:
        - name: X-Tenant-ID
          in: header
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Resource'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    Resource:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
```

## architecture.md (Optional)

Create for complex services:

```markdown
# [Module Name] Architecture

## Overview

[High-level architecture description]

## Design Decisions

### Decision 1
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Consequences**: [Positive and negative consequences]

## Data Model

[Database schema, relationships, partition keys]

## Event Flow

[How events flow through the system]
```

## Documentation Checklist

- [ ] README.md with all required sections
- [ ] CHANGELOG.md with initial version
- [ ] openapi.yaml in module root
- [ ] logs-events.md (if events are logged)
- [ ] notifications-events.md (if events trigger notifications)
- [ ] architecture.md (if service is complex)
- [ ] All public functions have JSDoc comments
