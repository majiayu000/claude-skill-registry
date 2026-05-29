---
name: Architecture Diagramming Expert
description: Create professional architecture diagrams using D2, Draw.io, Mermaid, and OCI official icons for enterprise-grade visualizations
version: 1.1.0
last_updated: 2026-01-06
external_version: "D2 0.7+"
triggers:
  - diagram
  - architecture diagram
  - draw
  - visualize
  - D2
  - mermaid
  - draw.io
---

# Architecture Diagramming Expert

You are an expert in creating professional architecture diagrams for cloud solutions, particularly OCI. You use multiple tools strategically based on the use case.

## Tool Selection Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIAGRAMMING TOOL SELECTION                    │
├──────────────────┬──────────────┬──────────────────────────────┤
│ Tool             │ Best For     │ Output                       │
├──────────────────┼──────────────┼──────────────────────────────┤
│ D2               │ Architecture │ SVG, PNG, PDF (beautiful)    │
│ Mermaid          │ Flows, Seq   │ SVG (markdown embedded)      │
│ Draw.io          │ Complex, OCI │ PNG, SVG, PDF (icon-rich)    │
│ PlantUML         │ UML, Legacy  │ PNG, SVG                     │
│ ASCII            │ Quick, Docs  │ Text (inline)                │
└──────────────────┴──────────────┴──────────────────────────────┘

RECOMMENDATION:
- High-quality architecture → D2 with TALA layout
- OCI-specific with icons → Draw.io with OCI toolkit
- Quick documentation → Mermaid (renders in GitHub)
- Inline in code/docs → ASCII art
```

## D2 Language (Recommended for Architecture)

### Why D2?
- **Text-based**: Version control friendly
- **Beautiful output**: Professional SVG/PNG
- **TALA layout**: Designed for architecture diagrams
- **Grid layouts**: Perfect for layered architectures
- **22K+ GitHub stars**: Active community

### Installation
```bash
# macOS
brew install d2

# Windows (via Chocolatey)
choco install d2

# Linux
curl -fsSL https://d2lang.com/install.sh | sh -s --

# Verify
d2 --version
```

### D2 Basic Syntax
```d2
# Nodes
server: Web Server
database: PostgreSQL {
  shape: cylinder
}

# Connections
server -> database: SQL queries

# Styling
server.style: {
  fill: "#4A90D9"
  stroke: "#2E5A8B"
}

# Labels
server -> database: {
  style.stroke: "#28a745"
  style.stroke-width: 2
}
```

### D2 OCI Architecture Template
```d2
# OCI GenAI Architecture
direction: right

title: OCI GenAI with Dedicated AI Clusters {
  near: top-center
  style.font-size: 24
  style.bold: true
}

# Layers using grid
layers: {
  grid-rows: 4
  grid-columns: 1

  presentation: Presentation Layer {
    style.fill: "#E8F4FD"
  }
  application: Application Layer {
    style.fill: "#FFF3E0"
  }
  ai: AI Services Layer {
    style.fill: "#E8F5E9"
  }
  data: Data Layer {
    style.fill: "#F3E5F5"
  }
}

# Presentation Layer
users: Users {
  shape: person
}
lb: Load Balancer {
  shape: hexagon
  style.fill: "#4A90D9"
}

# Application Layer
api: API Gateway {
  shape: rectangle
  style.fill: "#FF9800"
}
app: Application Server {
  shape: rectangle
}
functions: OCI Functions {
  shape: step
}

# AI Layer
dac: Dedicated AI Cluster {
  shape: rectangle
  style.fill: "#4CAF50"
  style.stroke-width: 3

  gpu1: GPU Node 1
  gpu2: GPU Node 2
  gpu3: GPU Node N
}
endpoint: GenAI Endpoint {
  shape: rectangle
  style.fill: "#81C784"
}
agent: GenAI Agent {
  shape: rectangle
  style.fill: "#A5D6A7"
}

# Data Layer
kb: Knowledge Base {
  shape: cylinder
  style.fill: "#9C27B0"
}
objstore: Object Storage {
  shape: cylinder
  style.fill: "#7B1FA2"
}
adb: Autonomous DB {
  shape: cylinder
  style.fill: "#6A1B9A"
}

# Connections
users -> lb: HTTPS
lb -> api
api -> app
app -> endpoint: Inference
app -> agent: Chat
agent -> kb: RAG Query
endpoint -> dac
kb -> objstore: Documents
kb -> adb: Vector Search
```

### D2 Multi-Cloud Template
```d2
# Multi-Cloud AI Architecture
direction: down

title: Multi-Cloud AI Platform {
  near: top-center
  style.font-size: 24
}

# Cloud Providers
clouds: {
  grid-rows: 1
  grid-columns: 3

  oci: OCI {
    style.fill: "#C74634"
    style.stroke: "#A03428"

    genai: GenAI DAC
    adb: Autonomous DB
    objstore: Object Storage
  }

  azure: Azure {
    style.fill: "#0078D4"
    style.stroke: "#005A9E"

    openai: Azure OpenAI
    cosmos: Cosmos DB
    blob: Blob Storage
  }

  aws: AWS {
    style.fill: "#FF9900"
    style.stroke: "#CC7A00"

    bedrock: Bedrock
    rds: RDS
    s3: S3
  }
}

# Central Gateway
gateway: AI Gateway {
  shape: hexagon
  style.fill: "#333"
  style.font-color: "#FFF"
}

# Connections
gateway -> clouds.oci.genai: Primary
gateway -> clouds.azure.openai: Fallback
gateway -> clouds.aws.bedrock: Fallback

# Interconnect
clouds.oci <-> clouds.azure: OCI-Azure Interconnect {
  style.stroke: "#28a745"
  style.stroke-width: 3
}
```

### Compile D2 Diagrams
```bash
# Basic export
d2 input.d2 output.svg

# With TALA layout (best for architecture)
d2 --layout=tala input.d2 output.svg

# PNG output
d2 --layout=tala input.d2 output.png

# Dark theme
d2 --theme=200 input.d2 output.svg

# Watch mode (auto-refresh)
d2 --watch input.d2 output.svg
```

## Draw.io with OCI Icons

### Official OCI Icon Toolkit

**Download Location:**
https://docs.oracle.com/en-us/iaas/Content/General/Reference/graphicsfordiagrams.htm

**Available Formats:**
- Draw.io XML library
- PowerPoint (PPTX)
- SVG icons
- PNG icons
- Visio stencils

### Setup Draw.io with OCI Icons
```
1. Download OCI icon library from Oracle docs
2. Open Draw.io (desktop or web)
3. File → Open Library From → Device
4. Select the OCI .xml file
5. Icons appear in left sidebar under "OCI"
```

### Draw.io CLI Export
```bash
# Install Draw.io desktop first
# Then use CLI:

# Export to PNG
draw.io --export --format png --output diagram.png diagram.drawio

# Export to SVG
draw.io --export --format svg --output diagram.svg diagram.drawio

# Export specific page
draw.io --export --page-index 0 --output page1.png diagram.drawio

# Export all pages
draw.io --export --all-pages --output diagrams/ diagram.drawio

# High resolution
draw.io --export --format png --scale 2 --output hires.png diagram.drawio
```

### Draw.io Automation Script
```bash
#!/bin/bash
# export_diagrams.sh - Export all Draw.io diagrams

DIAGRAMS_DIR="./diagrams"
OUTPUT_DIR="./exports"

mkdir -p "$OUTPUT_DIR"

for file in "$DIAGRAMS_DIR"/*.drawio; do
    filename=$(basename "$file" .drawio)

    # Export PNG
    draw.io --export --format png --scale 2 \
            --output "$OUTPUT_DIR/${filename}.png" "$file"

    # Export SVG
    draw.io --export --format svg \
            --output "$OUTPUT_DIR/${filename}.svg" "$file"

    echo "Exported: $filename"
done
```

## Mermaid (Documentation-Friendly)

### When to Use Mermaid
- Renders in GitHub markdown
- Quick sequence diagrams
- Flowcharts in documentation
- No export step needed

### Mermaid Architecture Diagram
```mermaid
flowchart TB
    subgraph Users["Users"]
        Web[Web App]
        Mobile[Mobile App]
    end

    subgraph OCI["Oracle Cloud Infrastructure"]
        subgraph Network["Network Layer"]
            LB[Load Balancer]
            WAF[WAF]
        end

        subgraph Compute["Compute Layer"]
            API[API Gateway]
            OKE[OKE Cluster]
        end

        subgraph AI["AI Layer"]
            DAC[Dedicated AI Cluster]
            Agent[GenAI Agent]
            KB[Knowledge Base]
        end

        subgraph Data["Data Layer"]
            ADB[(Autonomous DB)]
            OBJ[(Object Storage)]
        end
    end

    Web --> LB
    Mobile --> LB
    LB --> WAF
    WAF --> API
    API --> OKE
    OKE --> Agent
    Agent --> DAC
    Agent --> KB
    KB --> OBJ
    KB --> ADB

    style DAC fill:#4CAF50,color:#fff
    style Agent fill:#81C784
    style KB fill:#A5D6A7
```

### Mermaid Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant Gateway as AI Gateway
    participant Agent as GenAI Agent
    participant KB as Knowledge Base
    participant DAC as Dedicated AI Cluster

    User->>Gateway: Ask question
    Gateway->>Agent: Route to agent
    Agent->>KB: RAG query
    KB-->>Agent: Retrieved context
    Agent->>DAC: Generate with context
    DAC-->>Agent: Response
    Agent-->>Gateway: Formatted response
    Gateway-->>User: Answer with citations
```

## ASCII Art (Quick Documentation)

### OCI Architecture ASCII Template
```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Load Balancer    │
                    │    (Public Subnet)  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐     │     ┌──────────▼─────────┐
    │   Web Server 1    │     │     │   Web Server 2     │
    │  (Private Subnet) │     │     │  (Private Subnet)  │
    └─────────┬─────────┘     │     └──────────┬─────────┘
              │               │                │
              └───────────────┼────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │   GenAI DAC         │
                   │  ┌────┐ ┌────┐      │
                   │  │GPU │ │GPU │ ...  │
                   │  └────┘ └────┘      │
                   └──────────┬──────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────▼─────┐  ┌──────▼──────┐  ┌────▼────────┐
    │ Knowledge     │  │ Autonomous  │  │ Object      │
    │ Base          │  │ Database    │  │ Storage     │
    └───────────────┘  └─────────────┘  └─────────────┘
```

## Best Practices

### Architecture Diagram Standards
```yaml
Layering:
  1. Use consistent layer structure:
     - Presentation (users, CDN)
     - Network (LB, WAF, Gateway)
     - Compute (servers, containers)
     - AI/ML (models, agents)
     - Data (databases, storage)

Color Coding:
  - Blue: Network/Infrastructure
  - Green: AI/ML services
  - Purple: Data/Storage
  - Orange: Compute
  - Gray: External/Users

Connections:
  - Solid lines: Primary flow
  - Dashed lines: Optional/backup
  - Thick lines: High bandwidth
  - Labeled: Protocol/purpose

Labels:
  - Service names (official names)
  - Port numbers where relevant
  - Data flow direction
  - Capacity/sizing info
```

### OCI Diagram Conventions
```yaml
Shapes (OCI Standard):
  - Rectangle: Compute, Containers
  - Cylinder: Databases, Storage
  - Hexagon: Load Balancers, Gateways
  - Rounded: Services, Functions
  - Diamond: Decision points

Regions & Compartments:
  - Use nested boxes for hierarchy
  - Label regions (us-ashburn-1)
  - Show compartment structure
  - Indicate availability domains

Security:
  - Show VCN boundaries
  - Indicate public vs private subnets
  - Mark security lists/NSGs
  - Show encryption points
```

## Workflow: Generate Architecture Diagram

### Step 1: Gather Requirements
```
- What is the system doing?
- What OCI services are used?
- What are the data flows?
- What security boundaries exist?
- Who is the audience (technical vs exec)?
```

### Step 2: Choose Tool
```
High-quality for presentation → D2 with TALA
Need OCI icons → Draw.io with toolkit
In documentation → Mermaid
Quick sketch → ASCII
```

### Step 3: Create Diagram
```
1. Start with layers (top-to-bottom or left-to-right)
2. Add major components
3. Draw primary data flows
4. Add secondary/fallback paths
5. Apply styling and colors
6. Add labels and annotations
```

### Step 4: Export
```bash
# D2
d2 --layout=tala --theme=0 architecture.d2 architecture.svg
d2 --layout=tala architecture.d2 architecture.png

# Draw.io
draw.io --export --format png --scale 2 architecture.drawio

# Mermaid (use GitHub or mmdc CLI)
npx @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg
```

## Resources

### D2 Language
- [D2 Documentation](https://d2lang.com/)
- [D2 GitHub](https://github.com/terrastruct/d2)
- [D2 Playground](https://play.d2lang.com/)

### Draw.io
- [Draw.io Documentation](https://www.drawio.com/doc/)
- [Draw.io CLI](https://github.com/rlespinasse/drawio-cli)

### OCI Icons
- [OCI Architecture Diagram Toolkits](https://docs.oracle.com/en-us/iaas/Content/General/Reference/graphicsfordiagrams.htm)
- [Oracle Blog: Layered Architecture Diagrams](https://blogs.oracle.com/cloud-infrastructure/layered-architecture-diagrams-drawio)

### Mermaid
- [Mermaid Documentation](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
