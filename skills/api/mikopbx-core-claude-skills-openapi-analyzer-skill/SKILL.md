---
name: openapi-analyzer
description: Извлечение и анализ OpenAPI 3.1.0 спецификации из MikoPBX для валидации эндпоинтов. Использовать при проверке соответствия API, генерации тестов, проверке схем эндпоинтов или интеграции с навыками endpoint-validator и api-test-generator.
allowed-tools: Bash, Read, Grep, Glob
---

# MikoPBX OpenAPI Analyzing

Extract and analyze OpenAPI specification to validate endpoints, generate tests, and ensure API compliance.

## What This Skill Does

- **Fetches OpenAPI 3.1.0 specification** from MikoPBX (~9MB, 259 endpoints)
- **Extracts endpoint details**: parameters, request/response schemas
- **Validates compliance** with OpenAPI 3.1.0 standard
- **Compares code with spec**: finds missing parameters and discrepancies
- **Generates test data**: from schema examples and types
- **Provides Python/CLI interface**: for automation and integration

## When to Use This Skill

This is a **helper skill** used by other skills and in specific scenarios:

**Use automatically with**:
- `mikopbx-endpoint-validator` - validates against OpenAPI spec
- `mikopbx-api-test-generator` - generates tests from spec

**Use manually when**:
- Validating API compliance before releases
- Checking endpoint documentation completeness
- Generating test data from schemas
- Comparing code implementation with OpenAPI definition
- Creating API documentation

## How It Works

1. **Fetch** OpenAPI spec from MikoPBX (internal or external URL)
2. **Analyze** using Python analyzer or CLI commands
3. **Extract** endpoint details (parameters, schemas, responses)
4. **Validate** compliance with OpenAPI 3.1.0 standard
5. **Compare** with code to find discrepancies
6. **Generate** test data or documentation

---

## Quick Start

### Step 1: Fetch OpenAPI Specification

The OpenAPI spec is available at two endpoints:

- **Internal (no auth)**: `http://mikopbx-php83.localhost:8081/pbxcore/api/v3/openapi:getSpecification`
- **External (auth required)**: `https://mikopbx-php83.localhost:8445/pbxcore/api/v3/openapi:getSpecification`

**Fetch from inside container** (recommended):
```bash
# Get container ID
CONTAINER_ID=$(docker ps -q -f name=mikopbx)

# Fetch spec
docker exec $CONTAINER_ID curl -s http://mikopbx-php83.localhost:8081/pbxcore/api/v3/openapi:getSpecification > /tmp/mikopbx_openapi.json

# Verify
wc -l /tmp/mikopbx_openapi.json  # ~116K lines
ls -lh /tmp/mikopbx_openapi.json # ~9MB
```

**Fetch from outside container** (requires Bearer token):
```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://mikopbx-php83.localhost:8445/pbxcore/api/v3/openapi:getSpecification \
  -k > /tmp/mikopbx_openapi.json
```

### Step 2: Use Python Analyzer

The analyzer is located at `scripts/openapi_analyzer.py`.

**Basic usage**:
```bash
# Get API info
python3 scripts/openapi_analyzer.py info

# List all endpoints
python3 scripts/openapi_analyzer.py list

# Filter endpoints
python3 scripts/openapi_analyzer.py list extensions

# Get endpoint details
python3 scripts/openapi_analyzer.py get "/pbxcore/api/v3/extensions" POST

# Validate endpoint
python3 scripts/openapi_analyzer.py validate "/pbxcore/api/v3/extensions" POST
```

**Python API**:
```python
import sys
sys.path.insert(0, 'scripts')
from openapi_analyzer import MikoPBXOpenAPIAnalyzer

# Load analyzer
analyzer = MikoPBXOpenAPIAnalyzer('/tmp/mikopbx_openapi.json')

# Get endpoint
endpoint = analyzer.get_endpoint('/pbxcore/api/v3/extensions', 'POST')
print(endpoint['summary'])
print(endpoint['requestBody']['required'])

# Validate compliance
result = analyzer.validate_endpoint_compliance('/pbxcore/api/v3/extensions', 'POST')
print(f"Valid: {result['valid']}, Score: {result['score']}/100")

# Generate test data
test_data = analyzer.generate_test_data(endpoint)
print(test_data)
```

---

## Top 5 Use Cases

### Use Case 1: Validate Endpoint Compliance

Check if endpoint meets OpenAPI 3.1.0 standards.

```bash
# Validate single endpoint
python3 scripts/openapi_analyzer.py validate "/pbxcore/api/v3/extensions" POST
```

**Output**:
```json
{
  "valid": true,
  "issues": [],
  "warnings": [],
  "score": 100
}
```

**What it checks**:
- ✓ Has `summary` and `operationId`
- ✓ POST/PUT/PATCH has `requestBody`
- ✓ Has `responses` defined
- ✓ Has expected response codes (200, 400, 404, etc.)

---

### Use Case 2: Compare OpenAPI with Code

Find discrepancies between spec and DataStructure implementation.

```python
import sys
sys.path.insert(0, 'scripts')
from openapi_analyzer import MikoPBXOpenAPIAnalyzer

analyzer = MikoPBXOpenAPIAnalyzer()
endpoint = analyzer.get_endpoint('/pbxcore/api/v3/extensions', 'POST')

# Parameters from your DataStructure.php
code_params = ['number', 'type', 'callerid', 'userid', 'internal_id']

# Compare
comparison = analyzer.compare_with_code(endpoint, code_params)

print(f"Compliance: {comparison['compliance'] * 100:.1f}%")
print(f"In spec only: {comparison['in_spec_only']}")
print(f"In code only: {comparison['in_code_only']}")
print(f"In both: {comparison['in_both']}")
```

**Output**:
```
Compliance: 92.3%
In spec only: {'mobile_number', 'email'}
In code only: {'internal_id'}
In both: {'number', 'type', 'callerid', 'userid'}
```

**Action**: Add missing parameters to code or update OpenAPI spec.

---

### Use Case 3: Generate Test Data

Create test data from OpenAPI examples.

```python
analyzer = MikoPBXOpenAPIAnalyzer()
endpoint = analyzer.get_endpoint('/pbxcore/api/v3/extensions', 'POST')

# Generate test data
test_data = analyzer.generate_test_data(endpoint)
print(test_data)
```

**Output**:
```python
{
  "number": "201",      # from example
  "type": "SIP",        # from enum
  "callerid": "Test User",  # from example
  "userid": "1"         # from example
}
```

**Use in tests**:
```python
response = requests.post(
    f"{BASE_URL}/pbxcore/api/v3/extensions",
    json=test_data,
    headers=headers
)
assert response.status_code == 201
```

---

### Use Case 4: Find Endpoints by Pattern

Discover all endpoints related to a resource.

```bash
# Find all extension endpoints
python3 scripts/openapi_analyzer.py list extensions
```

**Output**:
```
/pbxcore/api/v3/extensions
/pbxcore/api/v3/extensions/{id}
/pbxcore/api/v3/extensions/{id}:copy
/pbxcore/api/v3/extensions:getDefault
/pbxcore/api/v3/extensions:getForSelect
```

**Use to**:
- Explore API structure
- Find custom actions (with `:`)
- Plan test coverage
- Generate documentation

---

### Use Case 5: Extract Schema Details

Get component schema for data modeling.

```bash
# Get Extension schema
python3 scripts/openapi_analyzer.py schema Extension
```

**Output**:
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "number": {"type": "string", "example": "201"},
    "type": {"type": "string", "enum": ["SIP", "IAX", "QUEUE"]},
    "callerid": {"type": "string"}
  },
  "required": ["number", "type"]
}
```

**Extract required fields**:
```bash
python3 scripts/openapi_analyzer.py schema Extension | jq -r '.required[]'
```

**Use to**:
- Validate data models
- Generate TypeScript/PHP interfaces
- Create mock data
- Document data structures

---

## OpenAPI Specification Details

### Metadata
- **OpenAPI Version**: 3.1.0
- **API Version**: 3.0.0
- **Total Endpoints**: 259
- **Total Schemas**: 96
- **File Size**: ~9MB, 116K lines JSON

### Structure
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "MikoPBX REST API",
    "version": "3.0.0"
  },
  "paths": {
    "/pbxcore/api/v3/extensions": {
      "get": {...},
      "post": {...}
    }
  },
  "components": {
    "schemas": {
      "Extension": {...},
      "ExtensionListItem": {...}
    }
  }
}
```

---

## Integration Patterns

### With mikopbx-endpoint-validator

```bash
# 1. Fetch OpenAPI spec
docker exec $CONTAINER_ID curl -s http://mikopbx-php83.localhost:8081/pbxcore/api/v3/openapi:getSpecification > /tmp/openapi.json

# 2. Get endpoint from OpenAPI
python3 scripts/openapi_analyzer.py get "/pbxcore/api/v3/extensions" POST > /tmp/endpoint.json

# 3. Compare with DataStructure.php
# (Extract params from code, then compare)

# 4. Validate compliance
python3 scripts/openapi_analyzer.py validate "/pbxcore/api/v3/extensions" POST
```

See [integration-examples.md](examples/integration-examples.md) for complete workflows.

### With mikopbx-api-test-generator

```python
# Generate pytest test from OpenAPI
analyzer = MikoPBXOpenAPIAnalyzer()
endpoint = analyzer.get_endpoint('/pbxcore/api/v3/extensions', 'POST')
test_data = analyzer.generate_test_data(endpoint)

# Use test_data in generated pytest...
```

See [integration-examples.md](examples/integration-examples.md) for test generation.

---

## Cache Strategy

OpenAPI spec is large (9MB), so **cache it**:

```bash
SPEC_FILE="/tmp/mikopbx_openapi.json"
CACHE_TTL=3600  # 1 hour

# Check cache age
if [ ! -f "$SPEC_FILE" ] || [ $(($(date +%s) - $(stat -f %m "$SPEC_FILE"))) -gt $CACHE_TTL ]; then
    echo "Fetching fresh spec..."
    docker exec $CONTAINER_ID curl -s http://mikopbx-php83.localhost:8081/pbxcore/api/v3/openapi:getSpecification > "$SPEC_FILE"
else
    echo "Using cached spec"
fi
```

**Python caching**:
```python
# Good: Create once, reuse
analyzer = MikoPBXOpenAPIAnalyzer()
for path in paths:
    endpoint = analyzer.get_endpoint(path, 'GET')

# Bad: Recreates analyzer each time
for path in paths:
    analyzer = MikoPBXOpenAPIAnalyzer()  # Reloads 9MB file!
```

---

## Common Patterns

### Pattern 1: Batch Validation

Validate all endpoints and find issues:

```bash
python3 scripts/openapi_analyzer.py list | while read path; do
    for method in GET POST PUT DELETE; do
        python3 scripts/openapi_analyzer.py validate "$path" "$method" 2>/dev/null
    done
done | jq -s 'map(select(.valid == false))'
```

### Pattern 2: Generate Compliance Report

```bash
#!/bin/bash
total=0
valid=0
total_score=0

while read path; do
    result=$(python3 scripts/openapi_analyzer.py validate "$path" "POST" 2>/dev/null)
    if [ $? -eq 0 ]; then
        total=$((total + 1))
        [ "$(echo "$result" | jq -r '.valid')" == "true" ] && valid=$((valid + 1))
        total_score=$((total_score + $(echo "$result" | jq -r '.score')))
    fi
done < <(python3 scripts/openapi_analyzer.py list)

echo "Valid: $valid/$total ($((valid * 100 / total))%)"
echo "Average score: $((total_score / total))/100"
```

### Pattern 3: Extract Test Data

```bash
python3 scripts/openapi_analyzer.py get "/pbxcore/api/v3/extensions" POST | \
  jq '.requestBody.properties | to_entries | map({
    key: .key,
    value: (.value.example // .value.enum[0] // "test")
  }) | from_entries'
```

---

## Output Format

Always provide **structured reports**:

```
📋 OpenAPI Analysis Report
==========================

🔍 Endpoint: POST /pbxcore/api/v3/extensions
📖 Operation ID: createExtension
📝 Summary: Создать новый добавочный

✅ OpenAPI Compliance:
   Score: 95/100
   Status: Valid
   Issues: None
   Warnings: Missing description for parameter 'callerid'

📊 Parameter Comparison:
   ✅ In both (5): number, type, callerid, userid, show_in_phonebook
   ⚠️  In OpenAPI only (2): mobile_number, email
   ⚠️  In Code only (1): internal_extension_id

📝 Required Parameters:
   • number (string, example: "201")
   • type (enum: SIP, IAX, QUEUE, IVR, CONFERENCE, EXTERNAL)

💡 Recommendations:
   1. Add 'mobile_number' and 'email' to DataStructure
   2. Add description for 'callerid' parameter in OpenAPI
   3. Consider if 'internal_extension_id' should be in OpenAPI spec
```

---

## Troubleshooting

### Spec fetch fails

```bash
# Check container is running
docker ps | grep mikopbx

# Try internal URL
docker exec $CONTAINER_ID curl -s http://mikopbx-php83.localhost:8081/pbxcore/api/v3/openapi:getSpecification

# Check curl works in container
docker exec $CONTAINER_ID curl --version
```

### Python import error

```bash
# Ensure script path is correct
python3 scripts/openapi_analyzer.py info

# Or use full path
python3 /full/path/to/scripts/openapi_analyzer.py info
```

### Endpoint not found

```bash
# List available endpoints
python3 scripts/openapi_analyzer.py list

# Check exact path format (include /pbxcore/api/v3 prefix)
python3 scripts/openapi_analyzer.py get "/pbxcore/api/v3/extensions" POST
```

### Large output

```bash
# Pipe to less
python3 scripts/openapi_analyzer.py get "/path" POST | less

# Save to file
python3 scripts/openapi_analyzer.py get "/path" POST > /tmp/endpoint.json

# Extract specific fields
python3 scripts/openapi_analyzer.py get "/path" POST | jq '.summary'
```

---

## Additional Resources

### Complete Documentation

- **[Python API Reference](reference/api-reference.md)** - Full API documentation for `MikoPBXOpenAPIAnalyzer` class
- **[CLI Usage Guide](reference/cli-usage.md)** - Complete command-line interface reference with examples
- **[Integration Examples](examples/integration-examples.md)** - Integration with mikopbx-endpoint-validator and mikopbx-api-test-generator

### Quick Links

- OpenAPI 3.1.0 Specification: https://spec.openapis.org/oas/v3.1.0
- Python analyzer: `scripts/openapi_analyzer.py`
- MikoPBX OpenAPI endpoint: `/pbxcore/api/v3/openapi:getSpecification`

---

## Success Criteria

Analysis is successful when:
- ✅ OpenAPI spec fetched successfully
- ✅ Endpoint found in specification
- ✅ All parameters extracted correctly
- ✅ Schemas resolved (including $ref)
- ✅ Comparison with code completed
- ✅ Validation results clear and actionable
- ✅ Test data generated successfully

## Best Practices

1. **Cache the spec** - It's 9MB, fetch once per session or hour
2. **Use Python for complex analysis** - CLI for simple queries
3. **Validate both ways** - Code→OpenAPI and OpenAPI→Code
4. **Check examples** - Use for test data generation
5. **Monitor compliance** - Aim for 90+ score
6. **Track required fields** - Critical for validation
7. **Document discrepancies** - Note mismatches for later fixes
