---
name: postman-collection-manager
description: Import, export, and manage Postman collections. Use when working with Postman collections, importing OpenAPI specs, exporting collections, or when user mentions Postman import, collection management, API collections.
allowed-tools: Bash, Read, Write
---

# Postman Collection Manager

This skill manages Postman collections including import, export, and conversion operations.

## Instructions

### Importing Collections

1. **Import from OpenAPI**
   - Use script: `scripts/openapi-to-postman.sh <openapi.json> <output-collection.json>`
   - Converts OpenAPI spec to Postman collection format

2. **Import from URL**
   - Use script: `scripts/import-from-url.sh <collection-url> <output.json>`
   - Downloads and saves Postman collection

### Exporting Collections

1. **Export Collection**
   - Use script: `scripts/export-collection.sh <collection.json> <format>`
   - Formats: json, yaml, newman-ready

2. **Extract Endpoints**
   - Use script: `scripts/extract-endpoints.sh <collection.json>`
   - Lists all endpoints in collection

### Managing Collections

1. **Merge Collections**
   - Use script: `scripts/merge-collections.sh <collection1.json> <collection2.json> <output.json>`
   - Combines multiple collections

2. **Filter Collection**
   - Use script: `scripts/filter-collection.sh <collection.json> <pattern> <output.json>`
   - Filters requests by name or folder

## Available Scripts

- **`scripts/openapi-to-postman.sh`** - Convert OpenAPI to Postman
- **`scripts/import-from-url.sh`** - Download collection from URL
- **`scripts/export-collection.sh`** - Export in various formats
- **`scripts/extract-endpoints.sh`** - List all endpoints
- **`scripts/merge-collections.sh`** - Merge multiple collections
- **`scripts/filter-collection.sh`** - Filter collection requests

## Examples

**Example 1: Import OpenAPI**
```bash
# Convert OpenAPI spec to Postman collection
./scripts/openapi-to-postman.sh api-spec.json my-api-collection.json
```

**Example 2: Manage Collections**
```bash
# Extract all endpoints
./scripts/extract-endpoints.sh my-collection.json

# Filter to only GET requests
./scripts/filter-collection.sh my-collection.json "GET" filtered.json
```

## Requirements

- jq for JSON processing
- curl for URL imports
- openapi-to-postmanv2 npm package (for OpenAPI conversion)

## Success Criteria

- ✅ Collections imported successfully
- ✅ OpenAPI conversions accurate
- ✅ Exports valid and usable
- ✅ Merged collections maintain structure
