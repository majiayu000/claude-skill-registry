---
name: template-based-generation-template
description: '[REPLACE] Generate structured content from templates. Use when [REPLACE
  with specific triggers].'
---

---
name: template-based-generation-template
description: [REPLACE] Generate structured content from templates. Use when [REPLACE with specific triggers].
allowed-tools: Write, Read, TodoWrite
---

# Template-Based Generation Template

## Purpose

This template demonstrates structured content generation from templates with placeholder filling and validation.

**Use this template when:**

- Generating configuration files
- Creating boilerplate code
- Producing structured documents
- Output follows predictable patterns

## Workflow

### Phase 1: Gather Requirements

<gather-requirements>
1. Identify required configuration values
2. Collect user inputs
3. Determine target environment
4. Check for optional features
5. Validate input completeness
</gather-requirements>

### Phase 2: Select Template

<select-template>
Based on requirements:
- Production: @references/production-config-template.md
- Development: @references/dev-config-template.md
- Testing: @references/test-config-template.md
</select-template>

### Phase 3: Fill Template

<fill-template>
1. Replace required placeholders
2. Apply conditional sections
3. Insert computed values
4. Format output appropriately
5. Add generation metadata
</fill-template>

### Phase 4: Validate Output

<validate-output>
1. Check all placeholders replaced
2. Verify syntax correctness
3. Validate security settings
4. Confirm required fields present
5. Test configuration loading
6. List scripts that should be run to validate the output of this skill
</validate-output>

## Template Selection Logic

**Production Configuration:**

- High security requirements
- Performance optimization
- Monitoring and logging
- Secrets management

**Development Configuration:**

- Debug mode enabled
- Verbose logging
- Local service URLs
- Mock credentials

**Testing Configuration:**

- Test database
- Reduced timeouts
- Isolated environment
- Deterministic behavior

## Progressive Disclosure

**Core workflow (this file):**

- Requirement gathering
- Template selection logic
- Validation rules

**Templates (references/):**

- @references/production-config-template.md - Production config example
- Domain-specific templates loaded when needed

## Example Usage

```xml
<gather-requirements>
Environment: production
Database: PostgreSQL
Features: [caching, monitoring, rate-limiting]
Region: us-east-1
</gather-requirements>

<select-template>
Selected: Production configuration template
Security level: High
Monitoring: Enabled
</select-template>

<fill-template>
Generating config/production.json:
- Database URL: [REDACTED - from environment]
- Redis URL: [REDACTED - from environment]
- Rate limit: 1000 req/min
- Monitoring: DataDog integration
- Log level: info
</fill-template>

<validate-output>
✓ No plaintext secrets
✓ All required fields present
✓ Valid JSON syntax
✓ Security headers configured
✓ CORS settings appropriate
Configuration ready!
</validate-output>
```

## See Also

- @references/production-config-template.md - Complete config generation example
