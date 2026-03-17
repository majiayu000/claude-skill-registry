---
name: design-doc-mermaid
description: Create Mermaid diagrams (activity, deployment, sequence, architecture) from text descriptions or source code. Use when asked to "create a diagram", "generate mermaid", "document architecture", "code to diagram", "create design doc", or "convert code to diagram". Supports hierarchical on-demand guide loading, Unicode semantic symbols, and Python utilities for diagram extraction and image conversion.
---

# Mermaid Architect - Hierarchical Diagram and Documentation Skill

Mermaid diagram and documentation system with specialized guides and code-to-diagram capabilities.

## Table of Contents

- [Decision Tree](#decision-tree)
- [Available Guides and Resources](#available-guides-and-resources)
- [Usage Patterns](#usage-patterns)
- [Resilient Workflow](#resilient-workflow)
- [Unicode Semantic Symbols](#unicode-semantic-symbols)
- [Python Utilities](#python-utilities)
- [Decision Tree Examples](#decision-tree-examples)
- [High-Contrast Styling](#high-contrast-styling)
- [File Organization](#file-organization)
- [Workflow Summary](#workflow-summary)
- [When to Use What](#when-to-use-what)
- [Best Practices](#best-practices)
- [Learning Path](#learning-path)

## Decision Tree

**How this skill works:**

1. **User makes a request** → Skill analyzes intent
2. **Skill determines diagram/document type** → Loads appropriate guide(s)
3. **AI reads specialized guide** → Generates diagram/document using templates
4. **Result delivered** → With validation and export options

**User Intent Analysis:**

```mermaid
flowchart TD
    Start([User Request]) --> Analyze{Analyze Intent}

    Analyze -->|"workflow, process, business logic"| Activity[Load Activity Diagram Guide<br/>references/guides/diagrams/activity-diagrams.md]
    Analyze -->|"infrastructure, deployment, cloud"| Deploy[Load Deployment Diagram Guide<br/>references/guides/diagrams/deployment-diagrams.md]
    Analyze -->|"system architecture, components"| Arch[Load Architecture Guide<br/>references/guides/diagrams/architecture-diagrams.md]
    Analyze -->|"API flow, interactions"| Sequence[Load Sequence Diagram Guide<br/>references/guides/diagrams/sequence-diagrams.md]
    Analyze -->|"code to diagram"| CodeToDiag[Load Code-to-Diagram Guide<br/>references/guides/code-to-diagram/ + examples/]
    Analyze -->|"design document, full docs"| DesignDoc[Load Design Document Template<br/>assets/*-design-template.md]
    Analyze -->|"unicode symbols, icons"| Unicode[Load Unicode Symbols Guide<br/>references/guides/unicode-symbols/guide.md]
    Analyze -->|"extract, validate, convert"| Scripts[Use Python Scripts<br/>scripts/extract_mermaid.py<br/>scripts/mermaid_to_image.py]

    Activity --> Generate[Generate Diagram]
    Deploy --> Generate
    Arch --> Generate
    Sequence --> Generate
    CodeToDiag --> Generate
    DesignDoc --> Generate
    Unicode --> Generate
    Scripts --> Execute[Execute Script]

    Generate --> Validate{Validate?}
    Validate -->|Yes| RunValidation[Run mmdc validation]
    Validate -->|No| Output
    RunValidation --> Output[Output Result]
    Execute --> Output

    classDef decision fill:#FFD700,stroke:#333,stroke-width:2px,color:black
    classDef guide fill:#90EE90,stroke:#333,stroke-width:2px,color:darkgreen
    classDef action fill:#87CEEB,stroke:#333,stroke-width:2px,color:darkblue

    class Analyze,Validate decision
    class Activity,Deploy,Arch,Sequence,CodeToDiag,DesignDoc,Unicode,Scripts guide
    class Generate,Execute,RunValidation,Output action
```

## Available Guides and Resources

### Diagram Type Guides (`references/guides/diagrams/`)

| Guide | Full Path | Load When User Wants | Examples |
|-------|-----------|---------------------|----------|
| Activity Diagrams | `references/guides/diagrams/activity-diagrams.md` | Workflows, processes, business logic, user flows, decision trees | "Show checkout flow", "Document ETL pipeline", "Create approval workflow" |
| Deployment Diagrams | `references/guides/diagrams/deployment-diagrams.md` | Infrastructure, cloud architecture, K8s, serverless, network topology | "Show AWS architecture", "Document GCP deployment", "Create K8s diagram" |
| Architecture Diagrams | `references/guides/diagrams/architecture-diagrams.md` | System architecture, component design, high-level structure | "Show system components", "Document microservices", "Architecture overview" |
| Sequence Diagrams | `references/guides/diagrams/sequence-diagrams.md` | API interactions, service communication, request/response flows | "Show API call sequence", "Document auth flow", "Service interactions" |

### Code-to-Diagram Guide & Examples

| Resource | Full Path | What It Provides |
|----------|-----------|------------------|
| **Master Guide** | `references/guides/code-to-diagram/README.md` | Complete workflow for analyzing any codebase and extracting diagrams |
| **Spring Boot** | `examples/spring-boot/README.md` | Controller→Service→Repository architecture, deployment config, sequence from methods, activity from business logic |
| **FastAPI** | `examples/fastapi/README.md` | Python async patterns, Pydantic models, dependency injection, cloud deployment |
| **React** | `examples/react/README.md` | Component hierarchy, state management, data flow, build pipeline |
| **Python ETL** | `examples/python-etl/README.md` | Data pipeline, transformation steps, error handling, scheduling |
| **Node/Express** | `examples/node-webapp/README.md` | Middleware chain, route handlers, async patterns, deployment |
| **Java Web App** | `examples/java-webapp/README.md` | Traditional MVC, servlet containers, WAR deployment |

### Design Document Templates

| Template | Full Path | Use For | Load When |
|----------|-----------|---------|-----------|
| Architecture Design | `assets/architecture-design-template.md` | System-wide architecture | "Create architecture doc", "Document system design" |
| API Design | `assets/api-design-template.md` | API specifications | "API design doc", "Document REST API" |
| Feature Design | `assets/feature-design-template.md` | Feature planning | "Feature design", "Plan new feature" |
| Database Design | `assets/database-design-template.md` | Database schema | "Database design", "Document schema" |
| System Design | `assets/system-design-template.md` | Complete system | "System design doc", "Full system documentation" |

### Unicode Symbols Guide

**Full Path:** `references/guides/unicode-symbols/guide.md`

**Load when user mentions:** "unicode symbols", "emoji in diagrams", "semantic icons", "add symbols"

**Quick Reference:**
- 📦 Infrastructure: ☁️ 🌐 🔌 📡 🗄️
- ⚙️ Compute: ⚙️ ⚡ 🔄 ♻️ 🚀 💨
- 💾 Data: 💾 📦 📊 📈 🗃️ 🧊
- 📨 Messaging: 📨 📬 📤 📥 🐰 📢
- 🔐 Security: 🔐 🔑 🛡️ 🚪 👤 🎫
- 📝 Monitoring: 📝 📊 🚨 ⚠️ ✅ ❌

### Python Scripts (`scripts/`)

| Script | Use For | Load When |
|--------|---------|-----------|
| `extract_mermaid.py` | Extract diagrams from Markdown, validate syntax, replace with images | "extract diagrams", "validate mermaid", "find all diagrams" |
| `mermaid_to_image.py` | Convert .mmd to PNG/SVG, batch conversion, custom themes | "convert to image", "render diagram", "create PNG" |
| `resilient_diagram.py` | Full workflow: save .mmd, generate image, validate, error recovery | "generate diagram", "create diagram with validation", "resilient diagram" |

## Usage Patterns

Common request patterns and guide selection. See [When to Use What](#when-to-use-what) for complete mapping.

| Pattern | Example Request | Guides to Load |
|---------|-----------------|----------------|
| Single Diagram | "Create activity diagram for login flow" | Diagram type guide + Unicode symbols |
| Code-to-Diagram | "Generate deployment from application.yml" | Framework example + Deployment guide |
| Design Document | "Create API design document" | Template from assets/ + Relevant diagram guides |
| Extract/Validate | "Extract diagrams from design.md" | Use `scripts/extract_mermaid.py` |
| Batch Convert | "Convert all .mmd to PNG" | Use `scripts/mermaid_to_image.py` |

## Resilient Workflow

**CRITICAL:** This is the recommended approach for ALL diagram generation. It ensures validation, error recovery, and consistent file organization.

**Full Guide:** `references/guides/resilient-workflow.md`

### Workflow Overview

```mermaid
flowchart LR
    A[1. Identify Type] --> B[2. Save .mmd + Image]
    B --> C{3. Valid?}
    C -->|Yes| D[4. Add to Markdown]
    C -->|No| E[5. Error Recovery]
    E --> F{Fix Found?}
    F -->|Yes| A
    F -->|No| G[Search External]
    G --> A

    classDef step fill:#90EE90,stroke:#333,color:darkgreen
    classDef decision fill:#FFD700,stroke:#333,color:black
    class A,B,D,E,G step
    class C,F decision
```

### Key Principle

**NEVER add a diagram to markdown until it passes validation.** This prevents broken diagrams in documentation.

### Using the Script (Recommended)

```bash
# Generate with full error recovery
python scripts/resilient_diagram.py \
    --code "flowchart TD; A-->B" \
    --markdown-file design_doc \
    --diagram-num 1 \
    --title "process_flow" \
    --format png \
    --json
```

**Output:** Both `.mmd` and `.png` files in `./diagrams/` directory.

### File Naming Convention

```
./diagrams/<markdown_file>_<num>_<type>_<title>.mmd
./diagrams/<markdown_file>_<num>_<type>_<title>.png
```

**Example:** `./diagrams/api_design_01_sequence_auth_flow.png`

### Error Recovery Priority

When validation fails, the workflow automatically:

1. **Check troubleshooting guide** - `references/guides/troubleshooting.md` (28 documented errors)
2. **Search with perplexity** - `perplexity_ask` MCP for syntax questions
3. **Search with brave** - `brave_web_search` MCP for recent solutions
4. **Ask gemini** - `gemini` skill for alternative perspective
5. **General search** - `WebSearch` tool as fallback

### Manual Fallback Steps

If the script is unavailable:

1. **Identify diagram type** from first line (flowchart, sequence, etc.)
2. **Load reference guide** from `references/guides/diagrams/`
3. **Save to** `./diagrams/<markdown_file>_<num>_<type>_<title>.mmd`
4. **Validate:** `mmdc -i file.mmd -o file.png -b transparent`
5. **On error:** Search `references/guides/troubleshooting.md` for matching error
6. **If not found:** Use search tools in priority order above
7. **Add reference:** `![Description](./diagrams/filename.png)`

### Pattern 6: Resilient Diagram Generation

**User:** "Create a sequence diagram and add it to the design doc"

**Skill Actions:**
1. Identify intent: **diagram generation** + **markdown integration**
2. Load workflow guide: `references/guides/resilient-workflow.md`
3. Identify diagram type: **sequence**
4. Load diagram guide: `references/guides/diagrams/sequence-diagrams.md`
5. Generate Mermaid code using templates
6. Execute resilient workflow:
   ```bash
   python scripts/resilient_diagram.py \
       --code "[generated code]" \
       --markdown-file design_doc \
       --diagram-num 1 \
       --title "api_sequence" \
       --json
   ```
7. If validation fails → Apply troubleshooting fix → Retry
8. On success → Add `![API Sequence](./diagrams/design_doc_01_sequence_api_sequence.png)` to markdown

## Unicode Semantic Symbols

Always use Unicode symbols to enhance diagram clarity. Common patterns:

### Infrastructure & Deployment
```mermaid
graph TB
    Client[👤 User] --> LB[🌐 Load Balancer]
    LB --> App1[⚙️ App Server 1]
    LB --> App2[⚙️ App Server 2]
    App1 --> DB[(💾 Database)]
    App1 --> Cache[(⚡ Redis)]
```

### Activity Flow with States
```mermaid
flowchart TD
    Start([🚀 Start]) --> Process[⚙️ Process Data]
    Process --> Check{✓ Valid?}
    Check -->|Yes| Save[💾 Save]
    Check -->|No| Error[❌ Error]
    Save --> Complete([✅ Complete])
```

### Microservices Architecture
```mermaid
graph TB
    API[🌐 API Gateway] --> Auth[🔐 Auth Service]
    API --> Orders[📋 Order Service]
    Orders --> Queue[📬 Message Queue]
    Queue --> Worker[⚙️ Background Worker]
    Worker --> Storage[📦 Object Storage]
```

**For complete symbol reference, load:** `references/guides/unicode-symbols/guide.md`

## Python Utilities

### Extract Mermaid Diagrams

```bash
# List all diagrams
python scripts/extract_mermaid.py document.md --list-only

# Extract to separate files
python scripts/extract_mermaid.py document.md --output-dir diagrams/

# Validate all diagrams
python scripts/extract_mermaid.py document.md --validate

# Replace with image references (for Confluence upload)
python scripts/extract_mermaid.py document.md --replace-with-images \
  --image-format png --output-markdown output.md
```

### Convert to Images

```bash
# Single conversion
python scripts/mermaid_to_image.py diagram.mmd output.png

# With custom settings
python scripts/mermaid_to_image.py diagram.mmd output.svg \
  --theme dark --background white --width 1200

# Batch convert directory
python scripts/mermaid_to_image.py diagrams/ output/ --format png --recursive

# From stdin
echo "graph TD; A-->B" | python scripts/mermaid_to_image.py - output.png
```

## Decision Tree Examples

### Example 1: User Asks for Workflow Diagram

**Input:** "Show the checkout process workflow"

**Skill Decision Path:**
```
1. Analyze: workflow, process → ACTIVITY DIAGRAM
2. Load guide: guides/diagrams/activity-diagrams.md
3. Find pattern: E-commerce checkout (template exists in guide)
4. Generate using template + Unicode symbols
5. Output activity diagram with decision points
```

**Output:** Complete activity diagram with Unicode symbols for cart, payment, order states.

### Example 2: User Provides Spring Boot Code

**Input:** "Here's my Spring Boot controller, create diagrams"

**Skill Decision Path:**
```
1. Analyze: Spring Boot, code provided → CODE-TO-DIAGRAM + SPRING BOOT
2. Load guides:
   - examples/spring-boot/README.md
   - guides/diagrams/architecture-diagrams.md (for structure)
   - guides/diagrams/sequence-diagrams.md (for method calls)
   - guides/diagrams/activity-diagrams.md (for business logic)
3. Generate multiple diagrams:
   a. Architecture diagram from @RestController/@Service/@Repository annotations
   b. Sequence diagram from method call chain
   c. Activity diagram from business logic flow
4. Output all diagrams with explanations
```

**Output:** 3-4 diagrams showing different views of the Spring Boot application.

### Example 3: User Wants Infrastructure Documentation

**Input:** "Document my GCP Cloud Run deployment with AlloyDB"

**Skill Decision Path:**
```
1. Analyze: infrastructure, GCP, Cloud Run → DEPLOYMENT DIAGRAM
2. Load guides:
   - guides/diagrams/deployment-diagrams.md
   - examples/spring-boot/ or examples/fastapi/ (if code provided)
3. Check for IaC files (Pulumi, Terraform, docker-compose)
4. Generate deployment diagram with:
   - Cloud Run services with specs
   - VPC connector
   - AlloyDB cluster
   - Security (IAM, Secret Manager)
   - Monitoring
5. Apply Unicode symbols for clarity
6. Output with resource specifications
```

**Output:** Complete GCP deployment diagram with all resources labeled.

## High-Contrast Styling

**ALL diagrams MUST use high-contrast colors:**

```mermaid
graph TB
    classDef primary fill:#90EE90,stroke:#333,stroke-width:2px,color:darkgreen
    classDef secondary fill:#87CEEB,stroke:#333,stroke-width:2px,color:darkblue
    classDef database fill:#E6E6FA,stroke:#333,stroke-width:2px,color:darkblue
    classDef error fill:#FFB6C1,stroke:#DC143C,stroke-width:2px,color:black

    %% Every classDef MUST have color: property
```

**Rules:**
- Light background → Dark text color
- Dark background → Light text color
- Always specify `color:` in every `classDef`

## File Organization

```
design-doc-mermaid/
├── SKILL.md                          # This file - Main orchestrator
├── README.md                         # User documentation
├── CLAUDE.md                         # Claude Code instructions
│
├── references/                       # Reference materials
│   ├── mermaid-diagram-guide.md     # Legacy general guide
│   └── guides/                       # Specialized guides (load on-demand)
│       ├── diagrams/
│       │   ├── activity-diagrams.md      # Workflows, processes
│       │   ├── deployment-diagrams.md    # Infrastructure, cloud
│       │   ├── architecture-diagrams.md  # System architecture
│       │   └── sequence-diagrams.md      # API interactions
│       ├── code-to-diagram/
│       │   └── README.md                 # Master guide for code analysis
│       ├── unicode-symbols/
│       │   └── guide.md                  # Complete symbol reference
│       └── troubleshooting.md        # Common syntax errors & fixes
│
├── assets/                           # Design document templates
│   ├── architecture-design-template.md
│   ├── api-design-template.md
│   ├── feature-design-template.md
│   ├── database-design-template.md
│   └── system-design-template.md
│
├── scripts/                          # Python utilities
│   ├── extract_mermaid.py           # Extract & validate diagrams
│   └── mermaid_to_image.py          # Convert to PNG/SVG
│
├── examples/                         # Language-specific patterns
│   ├── spring-boot/                 # Spring Boot patterns
│   ├── fastapi/                     # FastAPI patterns
│   ├── react/                       # React patterns
│   ├── python-etl/                  # Data pipeline patterns
│   ├── node-webapp/                 # Express.js patterns
│   └── java-webapp/                 # Traditional Java patterns
│
└── references/                       # General Mermaid reference
    └── mermaid-diagram-guide.md     # Complete Mermaid syntax guide
```

## Workflow Summary

1. **Analyze user intent** → Determine diagram type, document type, or action needed
2. **Load appropriate guide(s)** → Read only what's needed (token efficient)
3. **Apply templates and patterns** → Use examples from guides
4. **Generate output** → Create diagram or document
5. **Validate** (optional) → Use scripts to verify
6. **Convert** (optional) → Export to images if needed

## When to Use What

| User Request | Load This |
|--------------|-----------|
| "activity diagram", "workflow", "process flow" | `references/guides/diagrams/activity-diagrams.md` |
| "deployment", "infrastructure", "cloud", "k8s" | `references/guides/diagrams/deployment-diagrams.md` |
| "architecture", "system design", "components" | `references/guides/diagrams/architecture-diagrams.md` + design template |
| "API", "sequence", "interactions", "flow" | `references/mermaid-diagram-guide.md` (sequence section) |
| "Spring Boot code" | `examples/spring-boot/` + relevant diagram guides |
| "FastAPI code", "Python API" | `examples/fastapi/` + relevant diagram guides |
| "React app", "frontend" | `examples/react/` + architecture guide |
| "ETL", "data pipeline", "Python batch" | `examples/python-etl/` + activity guide |
| "symbols", "unicode", "emoji" | `references/guides/unicode-symbols/guide.md` |
| "syntax error", "diagram won't render", "troubleshoot" | `references/guides/troubleshooting.md` |
| "extract diagrams" | `scripts/extract_mermaid.py` |
| "convert to image", "PNG", "SVG" | `scripts/mermaid_to_image.py` |
| "create diagram", "generate diagram", "add diagram to markdown" | `scripts/resilient_diagram.py` + `references/guides/resilient-workflow.md` |
| "design document", "full docs" | `assets/*-design-template.md` + diagram guides |

## Best Practices

1. **Single Responsibility**: One diagram = One concept
2. **Unicode Enhancement**: Always use semantic symbols for clarity
3. **High Contrast**: Never skip the `color:` property in styles
4. **Validate Early**: Use scripts to catch syntax errors
5. **Template Reuse**: Leverage existing templates and examples
6. **Load On-Demand**: Only read guides needed for the specific request
7. **Token Efficiency**: Use hierarchical loading instead of reading everything

## Learning Path

**New to Mermaid?** Start here:
1. Read `references/guides/unicode-symbols/guide.md` for symbol meanings
2. Read `references/guides/diagrams/activity-diagrams.md` for basic patterns
3. Try examples in `examples/spring-boot/` or `examples/fastapi/`
4. Use `scripts/extract_mermaid.py --validate` to check your work

**Need to document code?** Follow this:
1. Identify your framework → Load relevant `examples/{framework}/`
2. Match code pattern to diagram type
3. Use templates from guide
4. Validate with scripts

**Creating design docs?** Follow this:
1. Choose document type → Load template from `assets/`
2. Fill in text sections
3. Load diagram guides as needed for each section
4. Use Unicode symbols throughout
5. Save to `docs/design/` with timestamp

---

**Version:** 2.0 (Hierarchical Architecture)
**Last Updated:** 2025-01-13
**Maintained by:** Claude Code Skills
