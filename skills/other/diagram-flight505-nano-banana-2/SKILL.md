---
name: diagram
description: "Generate publication-quality technical diagrams using Nano Banana Pro (Gemini 3 Pro Image) with AI-powered quality review. Smart iteration only regenerates when quality is below threshold."
allowed-tools: [Read, Write, Edit, Bash]
---

# Nano Banana - Diagram Generation

## Overview

Generate any technical diagram by describing it in natural language. Nano Banana Pro automatically creates publication-quality diagrams with intelligent quality review.

**Key Features:**
- 🍌 **Smart Iteration**: Only regenerates if quality is below threshold (saves API calls)
- 🎯 **Document-Type Aware**: Different quality standards for different document types
- 🔍 **AI Quality Review**: Gemini 3 Pro reviews each generation for professional standards
- 📊 **Publication-Ready**: High contrast, readable fonts, colorblind-friendly

## When to Use This Skill

Use this skill when you need:

- **Architecture Diagrams**: System designs, microservices, C4 models
- **Flowcharts**: Process flows, decision trees, user journeys
- **Data Models**: ERD diagrams, schema visualizations
- **Sequence Diagrams**: API interactions, message flows
- **Infrastructure Diagrams**: Cloud architecture, deployment topologies
- **Pipeline Diagrams**: CI/CD, data pipelines, ML workflows
- **Any Technical Visualization**: Describe it, Nano Banana creates it

## Quick Start

```bash
# Generate an architecture diagram
python skills/diagram/scripts/generate_diagram.py "Microservices architecture with API gateway, auth service, and database" -o architecture.png --doc-type architecture

# Generate a flowchart for a presentation
python skills/diagram/scripts/generate_diagram.py "User authentication flow with OAuth2" -o auth_flow.png --doc-type presentation

# Generate with verbose output
python skills/diagram/scripts/generate_diagram.py "Database schema for e-commerce" -o schema.png -v
```

## Document Types & Quality Thresholds

Different documents have different quality requirements. Nano Banana automatically adjusts:

| Document Type | Threshold | Best For |
|--------------|-----------|----------|
| `specification` | 8.5/10 | Technical specs, PRDs |
| `architecture` | 8.0/10 | Architecture documents |
| `proposal` | 8.0/10 | Business proposals |
| `journal` | 8.5/10 | Academic publications |
| `conference` | 8.0/10 | Conference papers |
| `thesis` | 8.0/10 | Dissertations |
| `grant` | 8.0/10 | Grant proposals |
| `sprint` | 7.5/10 | Sprint planning |
| `report` | 7.5/10 | Technical reports |
| `preprint` | 7.5/10 | arXiv, bioRxiv |
| `readme` | 7.0/10 | README files |
| `poster` | 7.0/10 | Academic posters |
| `presentation` | 6.5/10 | Slides, talks |
| `default` | 7.5/10 | General purpose |

**Smart Iteration**: If the first generation scores above the threshold, no second iteration is performed. This saves time and API costs.

## Diagram Examples

### System Architecture
```bash
python generate_diagram.py "Three-tier web application architecture with:
- React frontend
- Node.js API layer with load balancer
- PostgreSQL database with read replicas
- Redis cache layer
- CDN for static assets" -o three_tier.png --doc-type architecture
```

### Sequence Diagram
```bash
python generate_diagram.py "Sequence diagram showing OAuth2 authorization code flow:
1. User clicks login
2. App redirects to auth server
3. User authenticates
4. Auth server returns code
5. App exchanges code for token
6. App accesses protected resource" -o oauth_flow.png --doc-type specification
```

### Data Flow
```bash
python generate_diagram.py "Data pipeline showing:
- Data ingestion from multiple sources (API, files, streaming)
- ETL processing with Apache Spark
- Data warehouse (Snowflake)
- BI dashboards and ML model training" -o pipeline.png --doc-type report
```

### C4 Model - Container Diagram
```bash
python generate_diagram.py "C4 Container diagram for e-commerce platform:
- Web App (React SPA)
- Mobile App (React Native)
- API Gateway (Kong)
- Order Service (Python)
- Payment Service (Go)
- Inventory Service (Java)
- PostgreSQL Database
- Redis Cache
- RabbitMQ Message Queue" -o c4_container.png --doc-type architecture
```

## How It Works

1. **Initial Generation**: Nano Banana Pro (Gemini 3 Pro Image) generates the diagram
2. **Quality Review**: Gemini 3 Pro evaluates on 5 criteria:
   - Technical Accuracy (0-2 pts)
   - Clarity and Readability (0-2 pts)
   - Label Quality (0-2 pts)
   - Layout and Composition (0-2 pts)
   - Professional Appearance (0-2 pts)
3. **Decision**: If score ≥ threshold → Done! If score < threshold → Iterate
4. **Improvement**: Feedback is incorporated into an improved prompt
5. **Regeneration**: New diagram generated with improvements (max 2 iterations)

## Output Files

For an output path of `diagram.png`, you'll get:
- `diagram_v1.png` - First iteration
- `diagram_v2.png` - Second iteration (if needed)
- `diagram.png` - Final version (copy of best iteration)
- `diagram_review_log.json` - Quality scores and review details

## Configuration

### Environment Variable (Recommended)
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

### .env File
Create a `.env` file in your project:
```
OPENROUTER_API_KEY=your_api_key_here
```

### Get Your API Key
1. Go to https://openrouter.ai/keys
2. Create a new API key
3. Add credits to your account

## Tips for Better Diagrams

### Be Specific
```bash
# ❌ Too vague
"System diagram"

# ✅ Specific and detailed
"Microservices architecture diagram showing user service, order service, and payment service communicating via REST APIs, with a shared PostgreSQL database and Redis cache"
```

### Include Relationships
```bash
# ✅ Good - describes connections
"Data flow diagram showing:
- User uploads file to S3
- Lambda triggered on upload
- Lambda processes and stores metadata in DynamoDB
- SNS notifies downstream services"
```

### Specify Style When Needed
```bash
# ✅ Style hints
"Flowchart with decision diamonds for the loan approval process, using green for approved paths and red for rejected paths"
```

## Python API

```python
from skills.diagram.scripts.generate_diagram_ai import NanoBananaGenerator

generator = NanoBananaGenerator(verbose=True)
results = generator.generate_iterative(
    user_prompt="Kubernetes cluster architecture with ingress, services, and pods",
    output_path="k8s_arch.png",
    iterations=2,
    doc_type="architecture"
)

print(f"Final Score: {results['final_score']}/10")
print(f"Early Stop: {results['early_stop']}")
```

## Integration with Other Skills

- Use with **sprint planning** to visualize user story workflows
- Use with **architecture research** to diagram ADR decisions
- Use with **building blocks** to visualize component relationships
- Use with **competitive analysis** to create comparison diagrams

## Troubleshooting

### "OPENROUTER_API_KEY not found"
Set the environment variable or create a `.env` file. See Configuration section.

### Low Quality Scores
- Add more detail to your prompt
- Specify relationships between components
- Use a higher threshold document type to force more iterations

### Generation Timeout
Complex diagrams may take up to 2 minutes. The timeout is set to 120 seconds per API call.

## Cost Considerations

- Gemini 3 Pro Image: ~$2/M input, ~$12/M output tokens
- Simple diagram (1 iteration): ~$0.05-0.15
- Complex diagram (2 iterations): ~$0.10-0.30
- Smart iteration saves costs by stopping early when quality is sufficient
