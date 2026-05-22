---
name: api-documentation
description: Use when API code changes (routes, endpoints, schemas). Enforces Swagger/OpenAPI sync. Pauses work if documentation has drifted, triggering documentation-audit skill.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - mcp__github__*
model: opus
---

# API Documentation Enforcement

## Overview

Ensures all API changes are reflected in Swagger/OpenAPI documentation. When documentation drift is detected, work pauses until documentation is synchronized.

**Core principle:** API documentation is a first-class artifact, not an afterthought. No API change ships without documentation.

**Announce at start:** "I'm using api-documentation to verify Swagger/OpenAPI sync."

## When This Skill Triggers

This skill is triggered when ANY of these file patterns are modified:

| Pattern | Framework | Trigger Reason |
|---------|-----------|----------------|
| `**/routes/**/*.ts` | Express/Fastify | Route definitions |
| `**/controllers/**/*.ts` | NestJS/Express | Controller endpoints |
| `**/*.controller.ts` | NestJS | Controller class |
| `**/api/**/*.py` | FastAPI/Flask | API endpoints |
| `**/*_router.py` | FastAPI | Router definitions |
| `**/handlers/**/*.go` | Go | HTTP handlers |
| `**/schema*.ts` | TypeScript | Schema definitions |
| `**/dto/**/*.ts` | NestJS | Data transfer objects |
| `**/models/**/*.ts` | Various | API models |

## Documentation Locations

Check these locations for existing API documentation:

| File | Format | Standard |
|------|--------|----------|
| `openapi.yaml` | YAML | OpenAPI 3.x |
| `openapi.json` | JSON | OpenAPI 3.x |
| `swagger.yaml` | YAML | Swagger 2.0 |
| `swagger.json` | JSON | Swagger 2.0 |
| `docs/api.yaml` | YAML | OpenAPI 3.x |
| `api/openapi.yaml` | YAML | OpenAPI 3.x |

## The Protocol

### Step 1: Detect API Changes

```bash
# Check if current changes affect API
API_CHANGED=false

# Check common API file patterns
for pattern in "routes/" "controllers/" "api/" "handlers/" "*.controller.ts" "*_router.py"; do
  if git diff --name-only HEAD~1 | grep -q "$pattern"; then
    API_CHANGED=true
    break
  fi
done

# Check for schema/DTO changes
if git diff --name-only HEAD~1 | grep -qE "(schema|dto|model)"; then
  API_CHANGED=true
fi

echo "API Changed: $API_CHANGED"
```

### Step 2: Find Documentation File

```bash
find_api_docs() {
  for file in openapi.yaml openapi.json swagger.yaml swagger.json \
              docs/api.yaml docs/openapi.yaml api/openapi.yaml; do
    if [ -f "$file" ]; then
      echo "$file"
      return 0
    fi
  done
  return 1
}

DOC_FILE=$(find_api_docs)
if [ -z "$DOC_FILE" ]; then
  echo "ERROR: No API documentation file found"
  echo "PAUSE: Trigger documentation-audit skill"
fi
```

### Step 3: Verify Sync

Compare API code with documentation:

```bash
verify_api_sync() {
  local doc_file=$1

  # Extract endpoints from code
  CODE_ENDPOINTS=$(find . -name "*.ts" -path "*/routes/*" -exec grep -h "@(Get|Post|Put|Delete|Patch)" {} \; | \
    sed 's/.*@\(Get\|Post\|Put\|Delete\|Patch\)(\([^)]*\)).*/\1 \2/' | sort -u)

  # Extract endpoints from OpenAPI
  DOC_ENDPOINTS=$(yq '.paths | keys[]' "$doc_file" 2>/dev/null | sort -u)

  # Compare
  MISSING=$(comm -23 <(echo "$CODE_ENDPOINTS" | sort) <(echo "$DOC_ENDPOINTS" | sort))

  if [ -n "$MISSING" ]; then
    echo "DRIFT DETECTED: Endpoints in code but not in docs:"
    echo "$MISSING"
    return 1
  fi

  return 0
}
```

### Step 4: Handle Drift

If documentation drift is detected:

```markdown
## API Documentation Drift Detected

**Status:** PAUSED
**Reason:** API documentation is out of sync with code

### Missing from Documentation
- `POST /api/users` (found in `routes/users.ts:45`)
- `GET /api/users/:id/profile` (found in `routes/users.ts:67`)

### Action Required
1. Invoke `documentation-audit` skill
2. Update Swagger/OpenAPI documentation
3. Resume current work after sync complete

---
*api-documentation skill paused work*
```

Then invoke documentation-audit:

```
Use Skill tool: documentation-audit
```

## Documentation Requirements

When updating API documentation, include:

### Required Fields

| Field | Description |
|-------|-------------|
| `summary` | Short description of endpoint |
| `description` | Detailed explanation |
| `parameters` | All path/query/header params |
| `requestBody` | Request schema with examples |
| `responses` | All response codes with schemas |
| `tags` | Grouping for organization |
| `security` | Auth requirements |

### Required Examples

Every endpoint must have:
- Request example (for POST/PUT/PATCH)
- Success response example
- Error response example

### Example OpenAPI Entry

```yaml
/api/users:
  post:
    summary: Create a new user
    description: |
      Creates a new user account with the provided details.
      Requires admin authentication.
    tags:
      - Users
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateUserRequest'
          example:
            email: user@example.com
            name: John Doe
            role: member
    responses:
      '201':
        description: User created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            example:
              id: usr_123abc
              email: user@example.com
              name: John Doe
              role: member
              createdAt: '2025-01-02T10:30:00Z'
      '400':
        description: Invalid request body
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
            example:
              code: VALIDATION_ERROR
              message: Email is required
      '401':
        description: Authentication required
      '403':
        description: Insufficient permissions
```

## Validation

After updating documentation, validate:

```bash
# Validate OpenAPI spec
npx @apidevtools/swagger-cli validate openapi.yaml

# Or with yq for basic structure check
yq 'has("openapi") and has("paths") and has("info")' openapi.yaml
```

## Checklist

Before resuming work:

- [ ] API documentation file exists
- [ ] All endpoints are documented
- [ ] Request/response schemas defined
- [ ] Examples provided for all operations
- [ ] Security requirements documented
- [ ] Documentation validates successfully
- [ ] Changes committed to branch

## Integration

This skill coordinates with:

| Skill | Purpose |
|-------|---------|
| `documentation-audit` | Full documentation sync |
| `issue-driven-development` | Triggered during implementation |
| `comprehensive-review` | Validates documentation complete |

## When to Skip

This skill can be skipped when:
- Changes are purely internal (no API surface change)
- Changes are to test files only
- Changes are to documentation itself
- Project has no API (CLI tool, library, etc.)
