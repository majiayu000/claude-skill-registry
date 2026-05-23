---
name: uuid-generator
description: 生成UUID（v1、v4、v5）和其他唯一标识符，如ULID、nanoid。
metadata:
  short-description: 生成唯一ID
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# UUID Generator Tool

## Description
Generate various types of unique identifiers including UUID v1, v4, v5, ULID, and nanoid.

## Trigger
- `/uuid` command
- User needs unique identifiers
- User wants to generate IDs

## Usage

```bash
# Generate UUID v4
python scripts/uuid_generator.py

# Generate multiple UUIDs
python scripts/uuid_generator.py --count 10

# Generate UUID v5 with namespace
python scripts/uuid_generator.py --v5 --namespace dns --name example.com

# Generate short ID
python scripts/uuid_generator.py --short --length 12
```

## Tags
`uuid`, `id`, `generator`, `unique`, `identifier`

## Compatibility
- Codex: ✅
- Claude Code: ✅
