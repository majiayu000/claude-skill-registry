---
name: json-validator
description: 根据JSON Schema验证JSON文件，提供详细错误报告和自动修复建议。
metadata:
  short-description: 验证JSON/Schema
source:
  repository: https://github.com/python-jsonschema/jsonschema
  license: MIT
---

# JSON Validator Tool

## Description
Validate JSON files against JSON Schema with detailed error reporting and formatting.

## Trigger
- `/json-validate` command
- User needs to validate JSON
- User wants schema validation

## Usage

```bash
# Validate JSON syntax
python scripts/json_validator.py data.json

# Validate against schema
python scripts/json_validator.py data.json --schema schema.json

# Format JSON
python scripts/json_validator.py data.json --format --output formatted.json

# Minify JSON
python scripts/json_validator.py data.json --minify
```

## Tags
`json`, `validate`, `schema`, `format`, `lint`

## Compatibility
- Codex: ✅
- Claude Code: ✅
