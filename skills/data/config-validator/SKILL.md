---
name: dapr-config-validator
description: Automatically validate DAPR configuration files (dapr.yaml, component YAML files) when they are created or modified. Checks for schema compliance, missing required fields, invalid values, and common misconfigurations. Use when validating DAPR configs, reviewing component setup, or before deployment.
allowed-tools: Read, Grep, Glob
---

# DAPR Configuration Validator

This skill automatically validates DAPR configuration files to catch errors before runtime.

## When to Use

Claude automatically uses this skill when:
- A YAML file in `components/` directory is created or modified
- A `dapr.yaml` file is created or modified
- User asks to validate DAPR configuration
- Before deployment to catch issues early

## Validation Rules

### dapr.yaml Validation

```yaml
# Required structure
version: 1
common:
  resourcesPath: ./components
apps:
  - appId: my-service      # Required: unique identifier
    appDirPath: ./src      # Required: path to app
    appPort: 8000          # Required: application port
    command: ["python", "main.py"]
```

**Checks performed:**
- [ ] `version` field present and valid
- [ ] `apps` array is not empty
- [ ] Each app has required fields: `appId`, `appDirPath`, `appPort`
- [ ] `appPort` values don't conflict
- [ ] Referenced paths exist
- [ ] Commands are valid

### Component YAML Validation

```yaml
# Required structure
apiVersion: dapr.io/v1alpha1   # Must be exact
kind: Component                 # Must be exact
metadata:
  name: component-name         # Required: valid name
spec:
  type: state.redis            # Required: valid type
  version: v1                  # Required: valid version
  metadata:                    # Component-specific fields
  - name: redisHost
    value: localhost:6379
```

**Checks performed:**
- [ ] `apiVersion` is `dapr.io/v1alpha1`
- [ ] `kind` is `Component`
- [ ] `metadata.name` is valid (lowercase, alphanumeric, hyphens)
- [ ] `spec.type` is a valid DAPR component type
- [ ] `spec.version` is specified
- [ ] Required metadata fields for component type are present
- [ ] No secrets in plain text (warn if found)
- [ ] Secret references are properly formatted

### Valid Component Types

**State Stores:**
- `state.redis`
- `state.azure.cosmosdb`
- `state.postgresql`
- `state.mongodb`
- `state.azure.tablestorage`

**Pub/Sub:**
- `pubsub.redis`
- `pubsub.azure.servicebus.topics`
- `pubsub.kafka`
- `pubsub.rabbitmq`

**Secret Stores:**
- `secretstores.azure.keyvault`
- `secretstores.local.file`
- `secretstores.kubernetes`

**Bindings:**
- `bindings.azure.blobstorage`
- `bindings.azure.eventgrid`
- `bindings.cron`
- `bindings.http`

## Validation Process

1. **Find Configuration Files**
   ```
   Scan for:
   - dapr.yaml in project root
   - components/*.yaml
   - components/**/*.yaml
   ```

2. **Parse YAML**
   - Validate YAML syntax
   - Check for duplicate keys
   - Verify proper indentation

3. **Schema Validation**
   - Check required fields
   - Validate field types
   - Verify enum values

4. **Cross-Reference Checks**
   - Components referenced in dapr.yaml exist
   - Secret stores exist if secrets are referenced
   - No conflicting ports or app-ids

5. **Security Checks**
   - No hardcoded secrets
   - Secret references properly formatted
   - Scopes defined for sensitive components

## Output Format

```
DAPR Configuration Validation Report
=====================================

✓ dapr.yaml - Valid
  - 2 applications defined
  - Resources path: ./components

✓ components/statestore.yaml - Valid
  - Type: state.redis
  - Name: statestore

⚠ components/pubsub.yaml - Warnings
  - Type: pubsub.azure.servicebus.topics
  - Warning: connectionString appears to contain a secret value
  - Recommendation: Use secretKeyRef instead

✗ components/secrets.yaml - Invalid
  - Error: Missing required field 'spec.type'
  - Error: 'metadata.name' contains invalid characters

Summary: 2 valid, 1 warning, 1 error
```

## Common Issues and Fixes

### Missing Required Field
```yaml
# Bad
spec:
  metadata:
  - name: host
    value: localhost

# Good
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
```

### Secret in Plain Text
```yaml
# Bad (security risk)
- name: password
  value: mysecretpassword

# Good (use secret reference)
- name: password
  secretKeyRef:
    name: redis-secrets
    key: password
```

### Invalid Component Name
```yaml
# Bad
metadata:
  name: My State Store   # No spaces, uppercase

# Good
metadata:
  name: my-state-store   # Lowercase, hyphens only
```

### Wrong apiVersion
```yaml
# Bad
apiVersion: v1

# Good
apiVersion: dapr.io/v1alpha1
```

## Integration Points

This skill integrates with:
- `config-specialist` agent for deeper configuration help
- `dapr-debugger` agent when validation errors cause runtime issues
- `/dapr:component` command to generate valid configs
