---
name: attack-flow
description: Generate SITF-compliant attack flow JSON files from attack descriptions or incident reports. Use when analyzing supply chain attacks, breaches, or security incidents.
argument-hint: <attack-name> [websearch|url]
tools: Read, Grep, Glob, WebSearch, WebFetch, Write, Bash
---

# Attack Flow Generator

Generate SITF-compliant attack flow JSON files from attack descriptions or incident reports.

## Usage

```
/attack-flow <attack-name> [source]
```

- `attack-name`: Identifier for the attack (e.g., "s1ngularity", "solarwinds")
- `source`: URL, "websearch" for auto-research, or omit to use conversation context

Arguments: $ARGUMENTS

## Instructions

When this skill is invoked:

### Phase 1: Research

1. If source is "websearch" or a URL, gather attack details:
   - Attack timeline and phases
   - Entry point and initial access method
   - Lateral movement and persistence techniques
   - Data exfiltration or impact
   - Affected components (CI/CD, VCS, Registry, Endpoint, Production)

2. If source is omitted, use context from the current conversation.

### Phase 2: Technique Mapping

1. Read `techniques.json` to get the full technique library.

2. For each attack step, find the best matching technique:
   - Match by **action semantics**, not surface keywords
   - Example: Uploading stolen data to repos → T-V003 (Secret Exfiltration), NOT T-V008 (Malicious Hosting)
   - Example: Accessing VCS with stolen creds → T-V001 must come BEFORE any VCS actions

3. If no matching technique exists:
   - Create a placeholder node with `"type": "technique-gap"`
   - Include suggested technique metadata in the data field
   - Note in output that `/technique-proposal` should be run for gaps

### Phase 3: Layout Calculation

Apply these layout rules:

#### Rule 1: Component Layout (Left-to-Right by Attack Flow)
- Order components by their **sequence in the attack chain**, not by standard SITF order
- If attack flows CI/CD → Registry → Endpoint → VCS, layout left-to-right accordingly
- Minimum horizontal gap between components: 80-100px
- Component x-positions: Use increments of ~300px starting from x=0

#### Rule 2: Technique Ordering (Top-to-Bottom)
- **Primary**: Order techniques by their **sequence in the attack flow**
- **Secondary**: Within same attack step, order by stage (Initial Access → Discovery → Post-Compromise)
- Vertical gap between techniques: ~130-150px
- First technique starts at y = component.y + 80

#### Rule 3: Technique-Component Alignment
- Every technique node MUST be visually positioned within its parent component
- Calculate x-position: `component.x + 30`
- Validate technique.data.component matches parent component.data.componentId

#### Rule 4: Component Sizing
- Height = (technique_count × 150) + 120 (padding)
- Width = 230-250px

#### Rule 5: Edge Connections
- Connect source.bottom → target.top for vertical flows within component
- Connect source.right → target.left for cross-component flows
- Add labels for significant transitions ("Second wave", etc.)
- Use `"type": "smoothstep"` for all edges

### Phase 4: JSON Generation

Generate the attack flow JSON with this structure:

```json
{
  "metadata": {
    "name": "Attack Name",
    "created": "ISO-8601 timestamp",
    "version": "1.0",
    "framework": "SITF",
    "description": "Brief attack description"
  },
  "nodes": [
    // Entry points, components, techniques, exit points
  ],
  "edges": [
    // Connections between nodes
  ]
}
```

Node types:
- `entryPoint`: Attack entry (Phishing, Vulnerability Exploit, Stolen Credentials, etc.)
- `component`: SITF component container (endpoint, vcs, cicd, registry, production)
- `technique`: Attack technique from techniques.json
- `technique-gap`: Placeholder for missing technique (flag for /technique-proposal)
- `exitPoint`: Attack outcome (Future Breach, Persistence, Secondary Supply Chain Attack, etc.)

### Phase 5: Validation

Run this checklist before outputting:

```
[ ] Valid JSON structure (parse test passes)
[ ] Required fields present: metadata.{name,created,version,framework}, nodes[], edges[]
[ ] All node IDs are unique
[ ] All edge source/target reference valid node IDs
[ ] All techniques positioned within their component boundaries (x/y validation)
[ ] Techniques ordered by attack flow sequence
[ ] Initial Access techniques appear first when order is ambiguous
[ ] All technique IDs exist in techniques.json OR flagged as technique-gap
[ ] Exit points connected to terminal techniques
[ ] No orphaned nodes (every non-entry node has incoming edge)
```

### Phase 6: Output

1. Write the JSON file to `sample-flows/<attack-name>.json`
2. Validate the JSON with Python: `python3 -c "import json; json.load(open('file'))"`
3. Provide a summary table of the attack flow
4. If any technique-gaps exist, list them and recommend running `/technique-proposal`

## Example

```
/attack-flow s1ngularity websearch
```

This will:
1. Search for s1ngularity attack details
2. Map attack steps to SITF techniques
3. Generate `sample-flows/s1ngularity.json`
4. Output attack flow summary
