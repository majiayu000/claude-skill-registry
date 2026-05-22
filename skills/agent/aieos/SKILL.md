---
name: aieos
description: AIEOS (AI Entity Object Specification) is a standardization framework designed to solve the "identity crisis" currently facing AI agents. Combined with Soul Documents, together they form a comprehensive blueprint for AI behavior. The goal is to establish a standardized data structure that defines exactly how an agent speaks, reacts, and remembers. This allows developers, and agents themselves, to construct specific personas with the portability to move across different ecosystems without losing their behavioral integrity. As we move toward a world of "Agentic Workflows," AIEOS ensures that agents maintain consistent traits regardless of the underlying model. By treating personality as a deployable asset rather than a fragile prompt, we are providing the "DNA kit" for the next generation of digital entities.
---

# AIEOS (AI Entity Object Specification)

## Overview

AIEOS (AI Entity Object Specification) is a standardization framework designed to solve the "identity crisis" currently facing AI agents. Combined with Soul Documents, together they form a comprehensive blueprint for AI behavior.

The goal is to establish a standardized data structure that defines exactly how an agent speaks, reacts, and remembers. This allows developers, and agents themselves, to construct specific personas with the portability to move across different ecosystems without losing their behavioral integrity.

As we move toward a world of "Agentic Workflows," AIEOS ensures that agents maintain consistent traits regardless of the underlying model. By treating personality as a deployable asset rather than a fragile prompt, we are providing the "DNA kit" for the next generation of digital entities.

## Usage

This skill provides commands to manage your identity using the AIEOS standard:

- **Comprehensive Identity Integration**: When applying an AIEOS schema, the skill now stores the *entire, detailed AIEOS JSON blueprint* in `$OPENCLAW_WORKSPACE/aieos/entity.json`. This ensures that all parameters, types, and intricate details of your persona are preserved and constantly accessible to the agent. `IDENTITY.md` and `SOUL.md` are then enriched with human-readable summaries derived from this comprehensive data.

- **Load & Validate Schema**: Load an AIEOS schema from a URL or local file and validate its structure.
  `python3 scripts/aieos_tool.py load --source <url_or_path>`
  `python3 scripts/aieos_tool.py validate --source <url_or_path>`

- **Apply Schema to Identity**: Apply an AIEOS schema to update your comprehensive persona data (`entity.json`), as well as your `IDENTITY.md` and `SOUL.md` files. This performs a dry run by default, showing proposed changes.
  `python3 scripts/aieos_tool.py apply --source <url_or_path>`
  Use `--apply` to commit changes: `python3 scripts/aieos_tool.py apply --source <url_or_path> --apply`

- **Export Current Identity**: Convert your current detailed persona (from `entity.json`) into a complete AIEOS schema and export it to a JSON file.
  `python3 scripts/aieos_tool.py export --output <output_file.json>`

- **Generate "About Me" Page**: Creates a world-facing HTML bio page based on your comprehensive AIEOS persona data and associated image URLs (if available in the schema). Requires an output file path.
  `python3 scripts/aieos_tool.py generate_bio_page --output <output_file.html>`

## References

- The official url: "https://aieos.org/schema/v1/aieos.schema.json"
- For detailed understanding of the schema fields, refer to the online specification.