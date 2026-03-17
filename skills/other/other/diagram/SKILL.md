---
name: diagram
context: fork
skill: diagram
model: opus
description: Generate architecture diagrams using Python diagrams library
tags: [activity/architecture, domain/tooling, type/diagram]
---

# /diagram Skill

Generate architecture diagrams in multiple formats (C4, System Landscape, Data Flow, AWS).

## When to Use This Skill

Use `/diagram` when you need to create or update architecture visualizations:
- Create new C4 context/container/component diagrams
- Generate system landscape maps
- Visualize data flow architectures
- Create AWS infrastructure diagrams
- Diagram integration patterns
- Map system dependencies

## Usage

```
/diagram <type> [options]
```

### Diagram Types

| Type | Description | Use Case |
|------|-------------|----------|
| `c4-context` | C4 Level 1 - System context | Show external actors and system boundary |
| `c4-container` | C4 Level 2 - System containers | Show major components (services, databases) |
| `c4-component` | C4 Level 3 - Component level | Show detailed component interactions |
| `system-landscape` | Enterprise system map | Show all systems and connections |
| `data-flow` | Data movement diagram | Show how data moves through systems |
| `aws-architecture` | AWS infrastructure | Show EC2, RDS, S3, networking |
| `integration-pattern` | Integration architecture | Show message flows and patterns |
| `dependency-graph` | System dependencies | Show what depends on what |

## Workflow

### Phase 1: Capture Requirements
When invoked, the skill asks:

1. **Diagram type** (required)
   - Options: c4-context, c4-container, system-landscape, data-flow, aws-architecture, integration-pattern, dependency-graph
   - Default: c4-context

2. **Scope** (required)
   - For C4: Which system/product?
   - For landscape: Which program/domain?
   - For AWS: Which account/region?
   - For data-flow: Which integration?

3. **Systems to include** (optional)
   - Comma-separated list of systems
   - Leave blank to auto-detect from context

4. **Styling preferences** (optional)
   - Color scheme: classic, muted, vibrant
   - Icon set: simple, detailed, minimalist
   - Default: classic, simple

5. **Output format** (optional)
   - `python` — PNG via Python `diagrams` library (default for AWS/landscape types)
   - `mermaid` — Inline Mermaid (default for C4 types; renders natively in Obsidian)
   - `plantuml` — C4-PlantUML with directional hints (for complex C4 layouts, >15 elements)
   - For C4 types (c4-context, c4-container, c4-component), suggest Mermaid or PlantUML and cross-reference `/c4-diagram` for data-driven generation from System note frontmatter

6. **Output location** (optional)
   - Save diagram in Canvas, Concept note, or embed in Note?
   - Default: Create standalone file

### Phase 2: Generate Diagram

The skill generates a Python script using the `diagrams` package:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark

with Diagram("System Landscape", show=False, direction="TB"):
    # Your architecture here
```

#### Layout Science (Mermaid/PlantUML formats)

When generating Mermaid or PlantUML output (not Python):

- **Declaration order matters** — declare elements in reading order (left-to-right or top-to-bottom). The Dagre/Sugiyama algorithm positions elements based on declaration sequence.
- **Tier-based ordering** — Actors → Presentation → API → Services → Data → External
- **Edge crossing targets** — <5 for complex diagrams, 0 for simple ones. Crossings are the strongest predictor of comprehension difficulty (Purchase et al.).
- **Use subgraphs/boundaries** to group related elements (Gestalt proximity principle).

For C4-specific layout guidance including iterative refinement and PlantUML directional hints, see the `/c4-diagram` skill.

### Phase 3: Render and Save

The skill:
1. Executes the Python script
2. Generates PNG image
3. Creates markdown note with embedded diagram
4. Saves to vault as Canvas or Concept note
5. Links to related System/Integration notes

### Phase 4: Validation Gate

After rendering, assess the diagram against each criterion and output a structured validation table with concrete results:

```markdown
## Diagram Validation

| Criterion | Target | Result | Status |
|-----------|--------|--------|--------|
| Edge crossings | <5 complex, 0 simple | {count} | {PASS/FAIL} |
| Visual hierarchy | Boundary most prominent | {assessment} | {PASS/FAIL} |
| Grouping | Related elements proximate | {assessment} | {PASS/FAIL} |
| Flow direction | Consistent L-to-R or T-to-B | {direction} | {PASS/FAIL} |
| Traceability | Can follow each line | {assessment} | {PASS/FAIL} |
| Abstraction | One level per diagram | {level} | {PASS/FAIL} |
```

Replace `{count}`, `{assessment}`, `{direction}`, and `{level}` with the actual findings for the generated diagram. Every `/diagram` invocation must include this table in its output.

#### How to Assess Each Criterion

**CRITICAL: You must read the rendered PNG back using the Read tool and visually inspect it.** Do not assess criteria from the Python/Mermaid source alone — valid code frequently produces poor layouts.

| Criterion                     | How to Check (from the rendered PNG)                                         |
| ----------------------------- | ---------------------------------------------------------------------------- |
| **Edge crossings**            | Trace each relationship path visually — do any lines cross confusingly?      |
| **Visual hierarchy**          | Is the `Cluster` boundary immediately identifiable as the primary element?   |
| **Grouping**                  | Do elements within the same `Cluster` appear as distinct tiers/layers?       |
| **Flow direction**            | Does data flow follow the declared `direction` parameter (TB or LR)?         |
| **Relationship traceability** | Can each `Edge` be followed from source to destination without confusion?    |
| **Abstraction level**         | Does the diagram mix levels (e.g., database tables on a container diagram)?  |
| **Edge label readability**    | Are all edge labels readable at normal zoom? Max ~30 characters per line.    |
| **Path distinguishability**   | If multiple data flow paths exist, can you tell them apart at a glance?      |
| **Node placement**            | Are related nodes close together? Are any nodes orphaned or visually adrift? |

#### Iterative Refinement (Visual Review Loop)

After rendering, **read the PNG back** using the Read tool and assess against every criterion above. If any criterion fails, revise and re-render. Repeat until all pass. Do not present to the user until the loop completes with all-PASS.

Apply one or more of the following techniques for the Python `diagrams` library:

- **Edge crossings / Traceability** — Reorder node declarations to match the tier hierarchy (Actors → Presentation → Services → Data → External). The Graphviz engine positions nodes based on declaration order, so aligning code order with visual order reduces crossings.
- **Visual hierarchy / Grouping** — Add or restructure `Cluster` blocks to group related elements by tier or domain. Nested clusters create visual nesting that reinforces boundaries.
- **Flow direction** — Change the `direction` parameter (`"TB"`, `"LR"`) or restructure `Edge` connections so the primary data flow follows a single consistent direction.
- **Abstraction** — If mixed levels are detected, split the diagram into separate scripts at different abstraction levels (e.g., one context-level diagram and one container-level diagram).
- **Edge label readability** — Shorten labels to ~30 chars per line max. Use 2-3 short lines rather than one long line. Increase `fontsize` on Edge styles if labels look small in the rendered PNG.
- **Orphaned nodes** — If a node looks visually adrift, move it into a nearby Cluster or reposition it closer to its connected nodes.
- **Path distinguishability** — When a diagram has 2+ distinct data flow paths, assign each a different `Edge` colour and `penwidth`. Use a legend or consistent naming (Path 1, Path 2) so the reader can follow each flow independently.

### Design Rules

These rules prevent common layout mistakes. Apply them **before** generating the first render:

#### Box vs Label: What Deserves a Node?

At **C4 context level**, only these should be boxes (nodes):
- **Systems** (software systems, external services, SaaS platforms)
- **Actors** (people, roles, user groups)
- **Devices** (laptops, endpoints, physical hardware)

These should be **edge labels or annotations**, NOT boxes:
- Authentication mechanisms (IAM roles, OAuth flows, MFA)
- Network paths (VPC endpoints, NAT gateways at context level, load balancers)
- Protocols (HTTPS, SMB, SFTP)
- Policies (firewall rules, SCPs, bucket policies)

**Rule of thumb:** If you can't send it a request or log into it, it's probably a label.

At **C4 container level**, network components (VPC endpoints, load balancers) and IAM roles may become boxes — the abstraction level determines what's a node.

#### Choosing TB vs LR Direction

| Layout pattern | Use `TB` (top-to-bottom) | Use `LR` (left-to-right) |
|---------------|--------------------------|--------------------------|
| Single linear flow | Yes | — |
| Hierarchical (org chart, decision tree) | Yes | — |
| Two+ parallel output paths | — | Yes — paths branch vertically |
| Wide system landscape (many peers) | — | Yes |
| Timeline or sequence | — | Yes |

**Default remains TB**, but switch to LR when the diagram has branching paths — a tall narrow diagram with 10+ vertical nodes is hard to read.

#### Cluster Nesting

- **C4 context level:** Maximum 1 level of clusters (cloud boundaries). No nested sub-clusters — they add visual noise.
- **C4 container level:** Up to 2 levels (cloud boundary → service group).
- **C4 component level:** Up to 3 levels if needed.

**Anti-pattern:** Don't create clusters for logical groupings that aren't real boundaries (e.g., "Path 1: Vendor Upload" is a data flow, not a deployment boundary).

For Mermaid/PlantUML formats: reorder declarations to match data flow, add directional hints (`Rel_Down`, `Lay_Right`). See `/c4-diagram` skill for detailed refinement guidance.

## Format Selection Guide

| Scenario                               | Format         | Reason                                              |
| -------------------------------------- | -------------- | --------------------------------------------------- |
| AWS infrastructure, cloud icons        | `python`       | Rich icon library, professional PNG output           |
| System landscape, presentations        | `python`       | Best for standalone images and Confluence            |
| Quick C4 diagram in Obsidian           | `mermaid`      | Native rendering, Git-friendly, fast iteration       |
| C4 from System note frontmatter        | `mermaid`      | Use `/c4-diagram` for data-driven generation         |
| Complex C4 with persistent crossings   | `plantuml`     | Directional hints fix crossings Mermaid cannot       |
| >15 elements in a C4 diagram           | `plantuml`     | Layout control prevents chaos at scale               |
| Formal documentation, PDF export       | `plantuml`     | Automatic legends, consistent server-side rendering  |

## Examples

### Example 1: C4 Context Diagram for Data Platform

```
/diagram c4-context

Scope: Data Platform (Data Integration Platform)
Systems: ERP System, Kafka, Data Warehouse, API Gateway
Color scheme: classic
Output: Canvas - Data Platform C4 Context.md
```

**Result:** Creates `Canvas - Data Platform C4 Context.md` with C4 Level 1 diagram showing:
- External actors (users, partners)
- Data Platform as central system
- ERP System (source)
- Data Warehouse (destination)
- API Gateway (API access)
- Data flows between components

### Example 2: Data Flow Diagram for Real-time Integration

```
/diagram data-flow

Scope: ERP to Data Warehouse Real-time Integration
Systems: ERP System, Kafka, Data Platform, Data Warehouse
Styling: vibrant
Output: Concept - ERP to Data Warehouse Real-time Flow.md
```

**Result:** Creates `Concept - ERP to Data Warehouse Real-time Flow.md` showing:
- ERP transaction generation
- Kafka event publishing
- Data Platform stream processing
- Data Warehouse real-time table updates
- Data quality checks at each stage
- Error handling paths

### Example 3: AWS Architecture Diagram for Production

```
/diagram aws-architecture

Scope: Production Account (eu-west-1)
Systems: EKS, RDS, S3, ALB, Kafka
Color scheme: muted
Output: Canvas - Production AWS Architecture.md
```

**Result:** Creates `Canvas - Production AWS Architecture.md` showing:
- VPC with 3 AZs
- EKS cluster nodes
- RDS (Multi-AZ)
- S3 buckets
- Network components (ALB, NLB)
- Security groups
- Cost annotations

## Smart Defaults

The skill automatically:

1. **Detects systems from context**
   - Reads active System notes
   - Includes systems marked as "active"
   - Respects system criticality (red for critical, orange for high)

2. **Extracts data flows**
   - Reads Integration notes
   - Shows real-time vs batch
   - Includes latency SLAs
   - Shows volume metrics

3. **Applies styling**
   - Critical systems: Red background
   - High priority: Orange background
   - Medium: Blue background
   - Data flows: Green (real-time), Blue (batch)

4. **Generates captions**
   - Includes latency/throughput labels
   - Shows SLA compliance status
   - Indicates criticality level

5. **Creates cross-references**
   - Links nodes to System documentation
   - References Integration notes
   - Links to Architecture decisions

## Options

### Styling Options

```
/diagram <type> --style vibrant
```

- `classic` - Traditional blues, grays, blacks
- `muted` - Soft pastels, professional
- `vibrant` - Bright colors, high contrast
- `dark` - Dark background, light text

### Icon Sets

```
/diagram <type> --icons detailed
```

- `simple` - Minimal icons, text-based
- `minimalist` - Very simple, clean
- `detailed` - Rich icons, realistic

### Layout Direction

```
/diagram <type> --direction LR
```

- `TB` - Top to Bottom (default)
- `LR` - Left to Right
- `RL` - Right to Left
- `BT` - Bottom to Top

### Include Metrics

```
/diagram <type> --metrics yes
```

- Show latency SLAs
- Show throughput/capacity
- Show cost annotations
- Show availability targets

### Filter by Criticality

```
/diagram system-landscape --criticality critical
```

- `critical` - Critical systems only
- `high` - High + Critical
- `medium` - Medium and above
- `all` - All systems

## Output Formats

The skill generates:

1. **PNG image** - High-resolution diagram
2. **Markdown note** - With embedded image and metadata
3. **Canvas file** - Interactive Obsidian Canvas view (for diagram types: system-landscape, c4-*, aws-architecture)
4. **YAML frontmatter** - Includes diagram metadata for queryability:
   ```yaml
   type: Canvas
   title: "System Landscape"
   diagramType: system-landscape
   scope: Enterprise
   systems: [ERP, DataPlatform, DataWarehouse, APIGateway, AWS]
   latencyTarget: null
   refreshedDate: 2026-01-14
   ```

## Quality Indicators

Each generated diagram includes:

```yaml
# Quality Indicators
confidence: high               # Auto-generated from current data
freshness: current           # Just generated
source: synthetic            # Generated from note metadata
verified: false              # Needs manual review
reviewed: null
```

## Refresh Strategy

Diagrams are regenerated:

1. **On demand** - User runs `/diagram` command
2. **On note update** - When linked System/Integration notes change (manual trigger: `/diagram --refresh`)
3. **Weekly** - Automated task to refresh all Canvas diagrams (optional)

To refresh existing diagram:

```
/diagram refresh Canvas - System Landscape.md
```

## Integration with Other Skills

The `/diagram` skill works with:

- **`/system`** - Links diagrams to system notes
- **`/integration`** - Shows data flows from integration specs
- **`/architecture`** - Includes in HLD documentation
- **`/scenario-compare`** - Generates before/after diagrams
- **`/impact-analysis`** - Shows affected systems

## Error Handling

If diagram generation fails:

1. User is shown error message with diagnostics
2. Suggests checking:
   - System names match note titles
   - Integration directions are valid
   - AWS account/region exists
3. Offers to generate with fewer systems
4. Falls back to Mermaid text diagram (if Python fails)

## Examples from This Vault

These Canvas files were generated using the `/diagram` skill:

- `Canvas - System Landscape` - All enterprise systems
- `Canvas - C4 Context Diagram` - Data Platform context
- `Canvas - Data Flow Diagram` - ERP to Data Warehouse flow
- `Canvas - AWS Architecture` - Production infrastructure
- `Canvas - Scenario Comparison` - Scenario alternatives

## Next Steps

After creating a diagram:

1. Review the PNG for accuracy
2. Adjust colors/layout if needed via `--style`, `--icons`, `--direction`
3. Add annotations via `/canvas-annotate` skill
4. Create scenario-specific variants via `/scenario-compare`
5. Include in architecture reviews and documentation

## Related Skills

- `/c4-diagram` - Data-driven C4 diagram generation from System note frontmatter (Mermaid, flowchart, or PlantUML)
- `/diagram-review` - Analyse existing diagrams for readability and architecture quality
- `/scenario-compare` - Compare diagrams for different scenarios
- `/impact-analysis` - Analyse impacts of changes shown in diagram
- `/architecture-report` - Generate report with diagrams
- `/system-landscape` - Alternative skill specifically for system maps
- `/dependency-graph` - Focus on dependencies and risks

## Further Reading

- **`.claude/prompts/c4-mermaid-diagrams.md`** — Graph drawing theory, C4 templates, and Mermaid best practices
- **`Reference - C4 Diagrams with AI`** — Research-backed guide to readable C4 diagrams

---

**Invoke with:** `/diagram <type>`

**Example:** `/diagram c4-context` → Prompts for scope and options → Generates diagram
