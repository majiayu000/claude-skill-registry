---
name: api-client
description: Универсальный REST API клиент для MikoPBX с автоматической аутентификацией и выполнением запросов внутри Docker контейнеров. Использовать когда нужно тестировать API эндпоинты, выполнять CRUD операции (GET, POST, PATCH, DELETE) или отлаживать API ответы с конкретными параметрами.
allowed-tools: Bash, Read, Skill
---

# MikoPBX REST API Client

## Overview

Universal skill for executing REST API requests to MikoPBX with automatic authentication, container detection, and response formatting. Eliminates manual token management and curl command construction.

## Key Features

- ✅ **Automatic Authentication** - Gets JWT tokens automatically using auth-token-manager skill
- ✅ **Container Auto-detection** - Finds and uses running mikopbx-php83/mikopbx_php74 containers
- ✅ **All HTTP Methods** - Supports GET, POST, PATCH, DELETE, PUT
- ✅ **Smart Response Formatting** - JSON pretty-print with configurable line limits
- ✅ **Parameter Handling** - Query strings, form data, JSON payloads
- ✅ **Error Handling** - Clear error messages with troubleshooting hints
- ✅ **Internal Container Execution** - Runs requests inside container for network isolation testing

## When to Use This Skill

Use this skill when you need to:
- Test any REST API endpoint with specific parameters
- Execute CRUD operations (create, read, update, delete)
- Debug API responses and behavior
- Verify data after code changes
- Test search and filtering functionality
- Check CDR records or extension lists
- Validate API endpoint compliance

## Quick Start Examples

### Example 1: Simple GET Request
```bash
# Get list of extensions
./.claude/skills/api-client/scripts/api-request.sh GET extensions

# Get extensions with search
./.claude/skills/api-client/scripts/api-request.sh GET "extensions?search=201&limit=5"
```

### Example 2: GET with Date Range (CDR)
```bash
# Get call records for specific date range
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?dateFrom=2025-10-17&dateTo=2025-10-18%2023:59:59&limit=10"

# Search CDR by phone number
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?search=79643442732&limit=5"

# Search CDR by name
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?search=Ivan&dateFrom=2025-10-17&dateTo=2025-10-18%2023:59:59&limit=3"
```

### Example 3: POST Request (Create)
```bash
# Create new extension
./.claude/skills/api-client/scripts/api-request.sh POST extensions \
  --data "number=202&username=test_user&mobile=1234567890"

# Create with JSON payload
./.claude/skills/api-client/scripts/api-request.sh POST extensions \
  --json '{"number":"203","username":"john","mobile":"9876543210"}'
```

### Example 4: PATCH Request (Update)
```bash
# Update extension
./.claude/skills/api-client/scripts/api-request.sh PATCH "extensions/202" \
  --data "mobile=5555555555&username=updated_user"
```

### Example 5: DELETE Request
```bash
# Delete extension
./.claude/skills/api-client/scripts/api-request.sh DELETE "extensions/202"

# Delete CDR record
./.claude/skills/api-client/scripts/api-request.sh DELETE "cdr/12345"
```

### Example 6: Custom Container and Line Limit
```bash
# Use specific container
./.claude/skills/api-client/scripts/api-request.sh GET extensions --container mikopbx_php74

# Limit output to 50 lines
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?limit=100" --lines 50

# Full output (no limit)
./.claude/skills/api-client/scripts/api-request.sh GET extensions --lines 0
```

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Request                                             │
│    api-request.sh GET "cdr?search=Ivan&limit=5"             │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Container Detection                                      │
│    - Find running mikopbx-php83 or mikopbx_php74           │
│    - Get container ID                                       │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Authentication (via auth-token-manager skill)            │
│    - Execute get-auth-token.sh inside container            │
│    - Obtain JWT Bearer token                               │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. API Request Execution (inside container)                 │
│    curl -H "Authorization: Bearer $TOKEN"                   │
│         "http://127.0.0.1:8081/pbxcore/api/v3/cdr?..."      │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Response Formatting                                      │
│    - Parse JSON                                             │
│    - Pretty-print with python3 -m json.tool                 │
│    - Apply line limit (default: 80)                         │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Output to User                                           │
│    - Formatted JSON response                                │
│    - Error messages if failed                               │
└─────────────────────────────────────────────────────────────┘
```

## Script Usage

**IMPORTANT**: Always use absolute path to the script from project root:

```bash
/Users/nb/PhpstormProjects/mikopbx/Core/.claude/skills/api-client/scripts/api-request.sh <METHOD> <ENDPOINT> [OPTIONS]
```

Or when working in project directory, use:

```bash
./.claude/skills/api-client/scripts/api-request.sh <METHOD> <ENDPOINT> [OPTIONS]
```

### Required Arguments

- **METHOD** - HTTP method: GET, POST, PATCH, DELETE, PUT
- **ENDPOINT** - API endpoint path (without `/pbxcore/api/v3` prefix)

### Optional Arguments

- `--data "key=value&key2=value2"` - Form data for POST/PATCH
- `--json '{"key":"value"}'` - JSON payload for POST/PATCH
- `--container NAME` - Specific container name (default: auto-detect)
- `--lines N` - Limit output to N lines (default: 80, 0 = no limit)
- `--debug` - Show debug information

### Examples

```bash
# GET request
./.claude/skills/api-client/scripts/api-request.sh GET extensions

# GET with query parameters
./.claude/skills/api-client/scripts/api-request.sh GET "extensions?search=201"

# POST with form data
./.claude/skills/api-client/scripts/api-request.sh POST extensions --data "number=204&username=test"

# POST with JSON
./.claude/skills/api-client/scripts/api-request.sh POST extensions --json '{"number":"205","username":"jane"}'

# PATCH request
./.claude/skills/api-client/scripts/api-request.sh PATCH "extensions/204" --data "mobile=1111111111"

# DELETE request
./.claude/skills/api-client/scripts/api-request.sh DELETE "extensions/204"

# Custom container
./.claude/skills/api-client/scripts/api-request.sh GET extensions --container mikopbx_php74

# More output lines
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?limit=100" --lines 200

# Debug mode
./.claude/skills/api-client/scripts/api-request.sh GET extensions --debug
```

## Endpoint Examples by Category

### Extensions API
```bash
# List all extensions
./.claude/skills/api-client/scripts/api-request.sh GET extensions

# Get specific extension
./.claude/skills/api-client/scripts/api-request.sh GET "extensions/201"

# Search extensions
./.claude/skills/api-client/scripts/api-request.sh GET "extensions?search=admin&limit=5"

# Create extension
./.claude/skills/api-client/scripts/api-request.sh POST extensions \
  --data "number=206&username=newuser&mobile=1234567890"

# Update extension
./.claude/skills/api-client/scripts/api-request.sh PATCH "extensions/206" --data "mobile=9999999999"

# Delete extension
./.claude/skills/api-client/scripts/api-request.sh DELETE "extensions/206"
```

### CDR (Call Detail Records) API
```bash
# Get recent CDR
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?limit=10"

# CDR by date range
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?dateFrom=2025-10-17&dateTo=2025-10-18%2023:59:59"

# Search by phone number
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?search=79643442732&limit=5"

# Search by caller name
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?search=Ivan&limit=3"

# Get CDR metadata
./.claude/skills/api-client/scripts/api-request.sh GET "cdr/metadata"

# Get playback URL (requires token or view parameter)
./.claude/skills/api-client/scripts/api-request.sh GET "cdr/12345:playback?view=inline"

# Delete CDR record
./.claude/skills/api-client/scripts/api-request.sh DELETE "cdr/12345"
```

### Providers API
```bash
# List providers
./.claude/skills/api-client/scripts/api-request.sh GET providers

# Get provider by ID
./.claude/skills/api-client/scripts/api-request.sh GET "providers/1"

# Create SIP provider
./.claude/skills/api-client/scripts/api-request.sh POST providers \
  --json '{"type":"sip","description":"Test Provider","host":"sip.example.com"}'

# Update provider
./.claude/skills/api-client/scripts/api-request.sh PATCH "providers/1" --data "disabled=0"

# Delete provider
./.claude/skills/api-client/scripts/api-request.sh DELETE "providers/1"
```

### Incoming Routes API
```bash
# List incoming routes
./.claude/skills/api-client/scripts/api-request.sh GET incoming-routes

# Create route
./.claude/skills/api-client/scripts/api-request.sh POST incoming-routes \
  --data "provider=1&number=201&priority=1"

# Update route
./.claude/skills/api-client/scripts/api-request.sh PATCH "incoming-routes/1" --data "priority=5"

# Delete route
./.claude/skills/api-client/scripts/api-request.sh DELETE "incoming-routes/1"
```

### System API
```bash
# System info
./.claude/skills/api-client/scripts/api-request.sh GET "system/info"

# Check for updates
./.claude/skills/api-client/scripts/api-request.sh GET "system:check-for-updates"

# Get system status
./.claude/skills/api-client/scripts/api-request.sh GET "system/status"
```

### Search API
```bash
# Global search
./.claude/skills/api-client/scripts/api-request.sh GET "search?query=admin&limit=20"

# Search by category
./.claude/skills/api-client/scripts/api-request.sh GET "search?query=201&category=extensions"
```

## Environment Variables

The script respects these environment variables:

```bash
# API credentials (passed to auth-token-manager)
MIKOPBX_LOGIN="admin"                    # Default username
MIKOPBX_PASSWORD="123456789MikoPBX#1"   # Default password

# Container selection
MIKOPBX_CONTAINER="mikopbx-php83"       # Default container name
```

## Response Format

Successful responses are formatted as JSON:

```json
{
  "result": true,
  "data": {
    "items": [...],
    "totalCount": 42
  },
  "messages": {}
}
```

Error responses:

```json
{
  "result": false,
  "data": {},
  "messages": {
    "error": ["Validation failed: number is required"]
  }
}
```

## Common Use Cases

### 1. Testing After Code Changes
```bash
# After modifying Extensions API
./.claude/skills/api-client/scripts/api-request.sh GET extensions
./.claude/skills/api-client/scripts/api-request.sh POST extensions --data "number=999&username=test"
./.claude/skills/api-client/scripts/api-request.sh DELETE "extensions/999"
```

### 2. Debugging Search Functionality
```bash
# Test search with various parameters
./.claude/skills/api-client/scripts/api-request.sh GET "extensions?search=admin"
./.claude/skills/api-client/scripts/api-request.sh GET "extensions?search=201&limit=1"
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?search=Ivan&dateFrom=2025-10-17"
```

### 3. CDR Verification
```bash
# Check if CDR records exist
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?limit=5" --lines 100

# Verify specific call
./.claude/skills/api-client/scripts/api-request.sh GET "cdr?search=79643442732"
```

### 4. Data Validation
```bash
# Create extension and verify in database
./.claude/skills/api-client/scripts/api-request.sh POST extensions --data "number=777&username=validation_test"

# Then check with sqlite-inspector skill
# docker exec <container> sqlite3 /cf/conf/mikopbx.db "SELECT * FROM Extensions WHERE number='777'"
```

## Integration with Other Skills

### Works with auth-token-manager
- Automatically invokes auth-token-manager to get JWT tokens
- No manual token management needed

### Works with container-inspector
- Uses container-inspector logic to find containers
- Supports both mikopbx-php83 and mikopbx_php74

### Works with sqlite-inspector
- API client modifies data via REST API
- sqlite-inspector verifies changes in database

### Works with openapi-analyzer
- openapi-analyzer provides endpoint documentation
- api-client executes actual requests to those endpoints

## Error Handling

### Container Not Found
```
❌ ERROR: No running MikoPBX containers found
Available containers:
  docker ps --filter "name=mikopbx"
```

**Solution**: Start container or specify correct name

### Authentication Failed
```
❌ ERROR: Failed to obtain authentication token
```

**Solution**: Check credentials in environment variables

### Invalid Endpoint
```
{
  "result": false,
  "messages": {
    "error": ["Endpoint not found"]
  }
}
```

**Solution**: Verify endpoint path, check openapi-analyzer skill for valid endpoints

### Network Error
```
curl: (7) Failed to connect to 127.0.0.1 port 8081
```

**Solution**: Verify container is running and web service is started

## Performance Tips

1. **Use container IP** - Faster than localhost (avoids loopback)
2. **Limit response lines** - Use `--lines` for large datasets
3. **Run inside container** - No network latency (127.0.0.1)
4. **Reuse tokens** - Token valid for 15 minutes (future enhancement)

## Advanced Usage

### Batch Requests
```bash
# Create multiple extensions
for i in {301..305}; do
  ./.claude/skills/api-client/scripts/api-request.sh POST extensions \
    --data "number=$i&username=user_$i&mobile=555000$i"
done

# Verify all created
./.claude/skills/api-client/scripts/api-request.sh GET "extensions?search=user_" --lines 200
```

### JSON Response Processing
```bash
# Extract specific field from response
RESPONSE=$(./.claude/skills/api-client/scripts/api-request.sh GET extensions --lines 0)
TOTAL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['totalCount'])")
echo "Total extensions: $TOTAL"
```

### Debug Full Request/Response
```bash
# Enable debug mode
./.claude/skills/api-client/scripts/api-request.sh GET extensions --debug

# Shows:
# - Container ID
# - Token (first 50 chars)
# - Full curl command
# - Raw response
```

## Troubleshooting

### Issue: "No containers found"
**Cause**: Container not running
**Solution**: `docker ps --filter "name=mikopbx"` and start if needed

### Issue: "Authentication failed"
**Cause**: Wrong credentials
**Solution**: Check MIKOPBX_LOGIN and MIKOPBX_PASSWORD env vars

### Issue: "Command not found: python3"
**Cause**: Python not in container (unlikely)
**Solution**: Container should have python3, check with `docker exec <container> which python3`

### Issue: "Broken JSON response"
**Cause**: API returned non-JSON (HTML error page)
**Solution**: Check endpoint path, use `--debug` to see raw response

## Files

- `scripts/api-request.sh` - Main API request execution script
- `SKILL.md` - This documentation
- `reference/http-methods.md` - HTTP methods reference
- `reference/common-endpoints.md` - Common endpoint patterns
- `examples/crud-examples.md` - CRUD operation examples
- `README.md` - Quick reference

## See Also

- [auth-token-manager skill](../auth-token-manager/SKILL.md) - JWT token management
- [container-inspector skill](../container-inspector/SKILL.md) - Container management
- [openapi-analyzer skill](../openapi-analyzer/SKILL.md) - API documentation
- [REST API Development Guide](/src/PBXCoreREST/CLAUDE.md) - API implementation guide
