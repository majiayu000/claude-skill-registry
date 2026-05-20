---
name: uuid-generator
description: Use when asked to generate UUIDs, GUIDs, unique identifiers in various formats (UUID1, UUID4, etc.).
---

# UUID Generator

Generate universally unique identifiers (UUIDs) in various formats for distributed systems, databases, and APIs.

## Purpose

UUID generation for:
- Database primary keys
- API resource identifiers
- Distributed system coordination
- Session tokens and tracking
- File naming and versioning

## Features

- **Multiple Versions**: UUID1 (time-based), UUID4 (random), UUID5 (namespace)
- **Bulk Generation**: Generate thousands of UUIDs
- **Custom Formats**: Hyphenated, compact, URN format
- **Namespace UUIDs**: Deterministic UUIDs from names
- **Validation**: Check UUID format and version
- **Export**: CSV, JSON, plain text

## Quick Start

```python
from uuid_generator import UUIDGenerator

# Generate UUID4 (random)
gen = UUIDGenerator()
uuid = gen.generate()  # 'a1b2c3d4-e5f6-4789-g0h1-i2j3k4l5m6n7'

# Bulk generation
uuids = gen.generate_bulk(count=1000, version=4)

# Namespace UUID (deterministic)
uuid = gen.generate_namespace('example.com', namespace='dns')
```

## CLI Usage

```bash
# Generate single UUID
python uuid_generator.py

# Generate 1000 UUIDs
python uuid_generator.py --count 1000 --output uuids.txt

# Generate namespace UUID
python uuid_generator.py --namespace dns --name example.com
```
