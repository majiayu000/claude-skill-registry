---
name: setup-container-config
description: Creates and validates YAML configuration files with schema validation following ModuleImplementationGuide.md Section 4. Generates config/default.yaml with proper structure, creates config/schema.json for validation, sets up environment variable overrides, configures service URLs from registry, and sets up RabbitMQ event bindings. Use when setting up new services, adding configuration options, or updating service configs.
---

# Setup Container Config

Creates and validates YAML configuration files with schema validation following ModuleImplementationGuide.md Section 4.

## Configuration Structure

### config/default.yaml

Reference: ModuleImplementationGuide.md Section 4.2

```yaml
# Module metadata
module:
  name: [module-name]
  version: 1.0.0

# Server settings (use env vars for deployment)
server:
  port: ${PORT:-3XXX}
  host: ${HOST:-0.0.0.0}

# Cosmos DB Configuration (shared database, prefixed containers)
cosmos_db:
  endpoint: ${COSMOS_DB_ENDPOINT}
  key: ${COSMOS_DB_KEY}
  database_id: ${COSMOS_DB_DATABASE_ID:-castiel}
  containers:
    main: [module-name]_data

# External service URLs (from config, not hardcoded)
services:
  auth:
    url: ${AUTH_URL:-http://localhost:3021}
  logging:
    url: ${LOGGING_URL:-http://localhost:3014}
  user_management:
    url: ${USER_MANAGEMENT_URL:-http://localhost:3022}

# RabbitMQ Configuration (RabbitMQ only; no Azure Service Bus)
rabbitmq:
  url: ${RABBITMQ_URL}
  exchange: coder_events
  queue: [module-name]_service
  bindings:
    - "event.name"  # Events to consume
  # Optional: for batch job workers (ModuleImplementationGuide §9.6)
  queue_batch_jobs: ${RABBITMQ_QUEUE_BATCH_JOBS:-bi_batch_jobs}

# Optional: Data Lake (for event→Data Lake consumers, e.g. DataLakeCollector)
data_lake:
  connection_string: ${DATA_LAKE_CONNECTION_STRING:-}
  container: ${DATA_LAKE_CONTAINER:-risk}
  path_prefix: ${DATA_LAKE_PATH_PREFIX:-/risk_evaluations}
  # ml_outcomes_prefix: ${DATA_LAKE_ML_OUTCOMES_PREFIX:-/ml_outcomes}  # for outcome consumer (BI Sales Risk)

# Feature flags
features:
  feature_flag: ${FEATURE_FLAG:-true}
```

**For BI Sales Risk containers (plan §8.5.4, §8.1–8.3):** add `application_insights` and `metrics`; for ml-service add `azure_ml`; for risk-analytics add `data_lake` (backfill), `feature_flags`, `thresholds`. See BI_SALES_RISK_IMPLEMENTATION_PLAN §8.

## Environment Variable Syntax

Use `${VAR:-default}` pattern:

```yaml
server:
  port: ${PORT:-3000}  # Uses PORT env var, defaults to 3000
  host: ${HOST:-0.0.0.0}

cosmos_db:
  endpoint: ${COSMOS_DB_ENDPOINT}  # Required, no default
  key: ${COSMOS_DB_KEY}  # Required, no default
```

Reference: ModuleImplementationGuide.md Section 4.1 (Configuration Hierarchy)

## config/schema.json

Create JSON Schema for validation:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["server", "cosmos_db"],
  "properties": {
    "module": {
      "type": "object",
      "required": ["name", "version"],
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string" }
      }
    },
    "server": {
      "type": "object",
      "required": ["port"],
      "properties": {
        "port": { "type": ["number", "string"] },
        "host": { "type": "string" }
      }
    },
    "cosmos_db": {
      "type": "object",
      "required": ["endpoint", "key", "database_id"],
      "properties": {
        "endpoint": { "type": "string" },
        "key": { "type": "string" },
        "database_id": { "type": "string" },
        "containers": {
          "type": "object",
          "additionalProperties": { "type": "string" }
        }
      }
    },
    "services": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "url": { "type": "string" }
        }
      }
    },
    "rabbitmq": {
      "type": "object",
      "properties": {
        "url": { "type": "string" },
        "exchange": { "type": "string" },
        "queue": { "type": "string" },
        "bindings": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  }
}
```

## Config Loader (src/config/index.ts)

Reference: ModuleImplementationGuide.md Section 4.4, containers/auth/src/config/index.ts

```typescript
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { parse as parseYaml } from 'yaml';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { ModuleConfig } from './types';

let cachedConfig: ModuleConfig | null = null;

function deepMerge<T extends Record<string, any>>(target: T, source: Partial<T>): T {
  const result = { ...target };
  for (const key in source) {
    const sourceValue = source[key];
    const targetValue = result[key];
    if (sourceValue !== undefined) {
      if (
        typeof sourceValue === 'object' &&
        sourceValue !== null &&
        !Array.isArray(sourceValue) &&
        typeof targetValue === 'object' &&
        targetValue !== null &&
        !Array.isArray(targetValue)
      ) {
        result[key] = deepMerge(targetValue, sourceValue);
      } else {
        result[key] = sourceValue as any;
      }
    }
  }
  return result;
}

function resolveEnvVars(obj: any): any {
  if (typeof obj === 'string') {
    return obj.replace(/\$\{([^}]+)\}/g, (match, expression) => {
      const [varName, defaultValue] = expression.split(':-');
      const envValue = process.env[varName];
      if (envValue !== undefined) return envValue;
      if (defaultValue !== undefined) return defaultValue;
      return match;
    });
  }
  if (Array.isArray(obj)) {
    return obj.map(resolveEnvVars);
  }
  if (typeof obj === 'object' && obj !== null) {
    const result: Record<string, any> = {};
    for (const key in obj) {
      result[key] = resolveEnvVars(obj[key]);
    }
    return result;
  }
  return obj;
}

export function loadConfig(): ModuleConfig {
  if (cachedConfig) return cachedConfig;
  
  const env = process.env.NODE_ENV || 'development';
  const configDir = join(__dirname, '../../config');
  
  // Load default config
  const defaultPath = join(configDir, 'default.yaml');
  if (!existsSync(defaultPath)) {
    throw new Error(`Default config not found: ${defaultPath}`);
  }
  const defaultConfig = parseYaml(readFileSync(defaultPath, 'utf8')) as ModuleConfig;
  
  // Load environment-specific overrides
  let envConfig: Partial<ModuleConfig> = {};
  const envPath = join(configDir, `${env}.yaml`);
  if (existsSync(envPath)) {
    envConfig = parseYaml(readFileSync(envPath, 'utf8')) as Partial<ModuleConfig>;
  }
  
  // Load schema
  const schemaPath = join(configDir, 'schema.json');
  const schema = JSON.parse(readFileSync(schemaPath, 'utf8'));
  
  // Merge and resolve
  const config = deepMerge(defaultConfig, envConfig);
  const resolved = resolveEnvVars(config) as ModuleConfig;
  
  // Convert port to number if string
  if (typeof resolved.server.port === 'string') {
    resolved.server.port = parseInt(resolved.server.port, 10);
  }
  
  // Validate against schema
  const ajv = new Ajv({ allErrors: true, useDefaults: true });
  addFormats(ajv);
  const validate = ajv.compile(schema);
  
  if (!validate(resolved)) {
    const errors = validate.errors?.map(e => `${e.instancePath} ${e.message}`).join(', ');
    throw new Error(`Invalid configuration: ${errors}`);
  }
  
  cachedConfig = resolved;
  return resolved;
}
```

## Config Types (src/config/types.ts)

```typescript
export interface ModuleConfig {
  module: {
    name: string;
    version: string;
  };
  server: {
    port: number;
    host: string;
  };
  cosmos_db: {
    endpoint: string;
    key: string;
    database_id: string;
    containers: Record<string, string>;
  };
  services?: Record<string, { url: string }>;
  rabbitmq?: {
    url: string;
    exchange: string;
    queue: string;
    bindings: string[];
    queue_batch_jobs?: string;
  };
  data_lake?: {
    connection_string: string;
    container: string;
    path_prefix: string;
  };
  features?: Record<string, boolean | string>;
}
```

## Configuration Rules

Reference: ModuleImplementationGuide.md Section 4.3

- ✅ All config in YAML files
- ✅ Schema validation for config
- ✅ Environment variable support for secrets
- ✅ Default values for non-secrets
- ✅ No hardcoded URLs, ports, or paths
- ✅ Config typed with TypeScript interfaces

## Checklist

- [ ] config/default.yaml created with proper structure
- [ ] config/schema.json created for validation
- [ ] Environment variables use ${VAR:-default} syntax
- [ ] Service URLs from config, never hardcoded
- [ ] Config loader implements Section 4.4 pattern
- [ ] Config types defined in TypeScript
- [ ] Schema validates all required fields
