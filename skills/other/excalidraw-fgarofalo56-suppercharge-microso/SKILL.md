---
name: excalidraw
description: Create and design Excalidraw diagrams, especially architecture diagrams for software, cloud (AWS, Azure, GCP), databases, AI/ML, analytics, and infrastructure. Generates valid .excalidraw JSON files. Works with VS Code, VS Code Insiders, Obsidian. Triggers on excalidraw, architecture diagram, system design, cloud diagram, infrastructure diagram, flowchart, whiteboard, software architecture, database diagram, network diagram, data flow, microservices diagram, C4 model.
---

# Excalidraw Diagram Designer

Expert skill for creating professional Excalidraw diagrams with focus on technical architecture. Generates valid `.excalidraw` JSON files that work seamlessly with VS Code, VS Code Insiders, and Obsidian.

## Quick Start

### Create a Diagram
1. Ask what type of diagram is needed
2. Generate the `.excalidraw` JSON file
3. User opens it in their preferred editor

### File Extensions
- `.excalidraw` - Standard JSON format
- `.excalidraw.json` - Explicit JSON format
- `.excalidraw.svg` - Embedded in SVG (editable)
- `.excalidraw.png` - Embedded in PNG (editable)

## Core Element Types

### Basic Shapes
```json
{
  "type": "rectangle|ellipse|diamond",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid|hachure|cross-hatch",
  "strokeWidth": 2,
  "strokeStyle": "solid|dashed|dotted",
  "roughness": 1,
  "opacity": 100
}
```

### Text Elements
```json
{
  "type": "text",
  "x": 100,
  "y": 100,
  "text": "Your text here",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "left|center|right",
  "verticalAlign": "top|middle|bottom",
  "strokeColor": "#1e1e1e"
}
```

### Lines & Arrows
```json
{
  "type": "arrow|line",
  "x": 100,
  "y": 100,
  "points": [[0, 0], [200, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow|triangle|dot|bar",
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2
}
```

### Shapes with Labels (Text Containers)
```json
{
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "backgroundColor": "#a5d8ff",
  "boundElements": [{"type": "text", "id": "text-id"}]
}
```

## Complete File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Architecture Diagram Libraries

**Always recommend users install these libraries from https://libraries.excalidraw.com:**

### Cloud Providers
| Library | Contents |
|---------|----------|
| **AWS Architecture Icons** | Lambda, EC2, S3, RDS, ELB, API Gateway |
| **AWS Serverless Icons** | Lambda, DynamoDB, EventBridge, Cognito, SNS, SQS |
| **Azure Cloud Services** | Key Vault, App Insights, DevOps, VMs, SQL Database |
| **Azure Network** | VPN Gateway, Firewall, Load Balancer, DNS Zones |
| **Azure Containers** | AKS, Container Registry, App Services |
| **GCP Icons** | Cloud Run, BigQuery, Dataflow, Pub/Sub, Vertex AI |
| **Google Architecture Icons** | Complete GCP service portfolio |

### Infrastructure & Architecture
| Library | Contents |
|---------|----------|
| **Software Architecture** | Microservice, database, cache, event bus, browser, mobile |
| **C4 Architecture** | Simon Brown's C4 model elements |
| **Cloud Design Patterns** | Cloud architecture concepts |
| **Technology Logos** | Kubernetes, Docker, Terraform, Kafka, Redis |
| **Network Topology** | VPN, Firewall, Server, Switch, Router, Client |

### Data & DevOps
| Library | Contents |
|---------|----------|
| **Data Science Logos** | Airflow, Jupyter, Pandas, TensorFlow, Scikit-learn |
| **Dev Ops Icons** | Ansible, Jenkins, Vault, Consul, Elasticsearch |
| **Database Icons** | Oracle, PostgreSQL, MongoDB, Redis components |
| **Snowflake Icons** | Snowflake data warehouse components |

## Architecture Diagram Patterns

### 1. Microservices Architecture
```
[API Gateway] --> [Service A] --> [Database A]
              --> [Service B] --> [Database B]
              --> [Service C] --> [Message Queue] --> [Worker]
```

### 2. Cloud Infrastructure (3-Tier)
```
[Users] --> [CDN/Load Balancer]
        --> [Web Tier (Auto-scaling)]
        --> [App Tier (Containers/Functions)]
        --> [Data Tier (Database + Cache)]
```

### 3. Data Pipeline
```
[Sources] --> [Ingestion] --> [Processing] --> [Storage] --> [Analytics]
   |              |              |              |              |
 APIs         Kafka/        Spark/          Data Lake      BI Tools
 Files        Kinesis       Databricks      Warehouse      ML Models
```

### 4. Event-Driven Architecture
```
[Producers] --> [Event Bus/Broker] --> [Consumers]
                      |
              [Event Store/Log]
```

## Color Palettes for Architecture Diagrams

### Professional Tech Palette
| Component | Color | Hex |
|-----------|-------|-----|
| Compute/Services | Blue | `#a5d8ff` |
| Storage/Database | Green | `#b2f2bb` |
| Networking | Orange | `#ffd8a8` |
| Security | Red | `#ffc9c9` |
| Integration | Purple | `#d0bfff` |
| Users/External | Gray | `#dee2e6` |

### Cloud Provider Colors
| Provider | Primary | Secondary |
|----------|---------|-----------|
| AWS | `#ff9900` | `#232f3e` |
| Azure | `#0078d4` | `#50e6ff` |
| GCP | `#4285f4` | `#34a853` |
| Kubernetes | `#326ce5` | `#ffffff` |

## VS Code Integration

### Setup
1. Install extension: `pomdtr.excalidraw-editor`
2. Create file with `.excalidraw` extension
3. Open file to launch Excalidraw editor

### Workspace Library
Add to `.vscode/settings.json`:
```json
{
  "excalidraw.workspaceLibraryPath": ".excalidraw/library.excalidrawlib"
}
```

### Keyboard Shortcuts
- `R` - Rectangle
- `D` - Diamond
- `E` - Ellipse
- `A` - Arrow
- `L` - Line
- `T` - Text
- `Shift` - Lock aspect ratio (1:1)

## Obsidian Integration

### Setup
1. Install "Excalidraw" plugin from Community Plugins
2. Create new drawing: `Ctrl/Cmd + P` > "Create new drawing"

### ExcalidrawAutomate API
```javascript
const ea = ExcalidrawAutomate;
ea.reset();

// Add elements
ea.addRect(100, 100, 200, 100);
ea.addText(150, 140, "Service A");
ea.addArrow([[300, 150], [400, 150]]);

// Create drawing
await ea.create();
```

### Templater Integration
Create templates that generate architecture diagrams:
```javascript
<%*
const ea = ExcalidrawAutomate;
ea.reset();
ea.style.strokeColor = "#1e1e1e";
ea.style.backgroundColor = "#a5d8ff";
// Build diagram...
await ea.create({filename: "architecture"});
%>
```

## Best Practices

### Layout Guidelines
1. **Flow direction**: Left-to-right or top-to-bottom
2. **Alignment**: Use grid (20px default)
3. **Spacing**: Minimum 40px between elements
4. **Grouping**: Related components close together
5. **Labels**: Clear, concise text on all elements

### Architecture Diagram Checklist
- [ ] Clear title and legend
- [ ] Consistent colors per component type
- [ ] Directional arrows showing data/control flow
- [ ] Labeled connections
- [ ] Grouped related services
- [ ] External vs internal systems distinguished

### Icon Usage
- Use official cloud provider icons for vendor services
- Use generic shapes for abstract concepts
- Maintain consistent icon sizes (60x60 or 80x80 recommended)
- Add labels below or inside icons

## Example: Generate Complete Architecture Diagram

When user requests "Create an AWS serverless architecture diagram":

1. **Identify components**: API Gateway, Lambda, DynamoDB, S3, CloudWatch
2. **Define layout**: Left-to-right flow
3. **Apply colors**: AWS orange/gray palette
4. **Generate JSON** with proper element positioning
5. **Save as** `aws-serverless-architecture.excalidraw`

## Troubleshooting

### File Won't Open
- Verify JSON syntax is valid
- Check file extension is correct
- Ensure `"type": "excalidraw"` is present

### Elements Not Visible
- Check `x`, `y` coordinates are reasonable (0-2000 range)
- Verify `opacity` is not 0
- Ensure `isDeleted` is not true

### Arrows Not Connecting
- Use `boundElements` array on shapes
- Set `startBinding` and `endBinding` on arrows
- Match element IDs correctly

## Reference Files

For detailed documentation, see:
- `reference.md` - Complete element property reference
- `scripts/excalidraw_generator.py` - Python diagram generator
- `templates/` - Ready-to-use architecture templates
