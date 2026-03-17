---
name: letta
description: Letta framework for building stateful AI agents with long-term memory. Use for AI agent development, memory management, tool integration, and multi-agent systems.
---

# Letta Skill

Comprehensive assistance with letta development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with letta
- Asking about letta features or APIs
- Implementing letta solutions
- Debugging letta code
- Learning letta best practices

## Quick Reference

### Common Patterns

*Quick reference patterns will be added as you use the skill.*

### Example Code Patterns

**Example 1** (bash):
```bash
pip install letta-evals
```

**Example 2** (bash):
```bash
uv pip install letta-evals
```

**Example 3** (python):
```python
import requests

url = "https://api.letta.com/v1/mcp-servers/mcp_server_id"

headers = {"Authorization": "Bearer <token>"}

response = requests.delete(url, headers=headers)

print(response.json())
```

**Example 4** (python):
```python
from letta_client import Letta

client = Letta(
    project="YOUR_PROJECT",
    token="YOUR_TOKEN",
)
client.groups.delete(
    group_id="group-123e4567-e89b-42d3-8456-426614174000",
)
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **agents.md** - Agents documentation
- **api_sdk.md** - Api Sdk documentation
- **blocks.md** - Blocks documentation
- **deployment.md** - Deployment documentation
- **getting_started.md** - Getting Started documentation
- **messages.md** - Messages documentation
- **multiprocessing.md** - Multiprocessing documentation
- **other.md** - Other documentation
- **tools.md** - Tools documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
