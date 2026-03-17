---
name: taxonomy
description: >
  Extract Federated Taxonomy tags from text. LLM extracts candidates,
  deterministic validation filters to known vocabulary. Returns bridge tags
  for multi-hop graph traversal.
allowed-tools: ["Bash", "Read"]
triggers:
  - taxonomy
  - tag this
  - classify
  - what tags
  - bridge tags
metadata:
  short-description: Extract taxonomy tags for graph traversal
---

# Taxonomy

Extract Federated Taxonomy tags from text for memory storage and multi-hop graph traversal.

## Quick Start

```bash
# Extract tags from text
./run.sh --text "Error handling in the authentication module" --collection operational

# Extract from file
./run.sh --file document.txt --collection lore

# Just get bridge tags (for graph traversal)
./run.sh --text "..." --bridges-only
```

## Output

```json
{
  "bridge_tags": ["Resilience", "Loyalty"],
  "collection_tags": {"function": "Fix", "domain": "Middleware"},
  "confidence": 0.8,
  "worth_remembering": true
}
```

## Bridge Tags (Tier 0)

Shared across all collections - enable cross-collection queries:

| Tag | Indicates |
|-----|-----------|
| Precision | Methodical, optimized, algorithmic |
| Resilience | Fault tolerance, error handling, robustness |
| Fragility | Technical debt, brittleness, single point of failure |
| Corruption | Bugs, data corruption, silent failures |
| Loyalty | Security, compliance, auth, encryption |
| Stealth | Hidden, evasion, infiltration |

## Collection Types

- **lore** - Narrative/story content (HLT vocabulary)
- **operational** - Code/technical lessons (Operational vocabulary)
- **sparta** - Security content (ATT&CK/D3FEND vocabulary)

## Use Cases

1. **Before storing to memory**: Get tags to enable graph traversal
2. **Filtering what to remember**: Check `worth_remembering` field
3. **Cross-collection queries**: Use bridge_tags for multi-hop search

## Composing with /learn

```bash
# /learn can call /taxonomy for tag extraction
tags=$(./run.sh --text "$content" --collection operational --json)
bridge_tags=$(echo "$tags" | jq -r '.bridge_tags | join(",")')
```
