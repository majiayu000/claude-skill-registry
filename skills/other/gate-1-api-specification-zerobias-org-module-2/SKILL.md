---
name: gate-1-api-specification
description: Gate 1 validation: API specification quality checks
---

### Gate 1: API Specification

**STOP AND CHECK:**
```bash
# No 'describe' operations
grep -E "describe[A-Z]" api.yml
# Must return nothing

# No error responses
grep -E "'40[0-9]'|'50[0-9]'" api.yml
# Must return nothing

# No snake_case in properties
grep "_" api.yml | grep -v "x-" | grep -v "#"
# Must return nothing

# No envelope/wrapper objects in responses
# Response should be direct $ref or array, not wrapped in {status, data, meta, response, result, caller, token, etc.}
yq eval '.paths.*.*.responses.*.content.*.schema | select(has("properties"))' api.yml
# Should only return schemas with business object properties, NOT envelope properties

# No connection context parameters in operations
grep -E "name: (apiKey|token|baseUrl|organizationId)" api.yml
# Must return nothing - these come from ConnectionProfile/State

# No nullable in API specification
grep "nullable:" api.yml
# Must return nothing - NEVER use nullable in api.yml

# Schema context separation check
# Find schemas referenced by other schemas (nested usage)
nested_schemas=$(yq eval '.components.schemas[] | .. | select(type == "string" and test("#/components/schemas/")) | capture("#/components/schemas/(?<schema>.+)").schema' api.yml | sort -u)

# Find schemas with their own endpoints (direct response usage)
endpoint_schemas=$(yq eval '.paths.*.*.responses.*.content.*.schema["$ref"]' api.yml | grep -o '[^/]*$' | sort -u)

# Schemas in BOTH lists need review
for schema in $nested_schemas; do
  if echo "$endpoint_schemas" | grep -q "^${schema}$"; then
    # Count properties in schema
    prop_count=$(yq eval ".components.schemas.${schema}.properties | length" api.yml)
    if [ "$prop_count" -gt 10 ]; then
      echo "⚠️  WARNING: Schema '${schema}' used in BOTH nested and direct contexts with ${prop_count} properties"
      echo "   Consider creating '${schema}Summary' for nested usage"
    fi
  fi
done
```

**PROCEED ONLY IF:**
- ✅ Operation name uses get/list/search/create/update/delete
- ✅ Summary uses "Retrieve" for get/list operations
- ✅ Descriptions from vendor documentation included
- ✅ ONLY 200/201 responses (NO 4xx/5xx)
- ✅ All properties camelCase
- ✅ Nested objects use $ref
- ✅ Response schemas map directly to main business object (NO envelope: status/data/meta/response/result/caller/token)
- ✅ NO connection context parameters (apiKey, token, baseUrl, organizationId) in operation parameters
- ✅ NO `nullable: true` in any schema properties
- ✅ Schemas used in BOTH nested and direct contexts have been reviewed for separation (if >10 properties, consider Summary version)

**IF FAILED:** Fix API spec before proceeding to generation.
