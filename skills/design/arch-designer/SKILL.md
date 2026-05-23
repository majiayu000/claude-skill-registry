---
name: arch-designer
description: Use when the user wants to generate architecture diagrams, visualize their codebase structure, create pitch decks with system diagrams, or understand their infrastructure layout from code
---

# Architecture Designer

Generate professional, ByteByteGo-quality architecture diagrams from your codebase.

## When to Use

Use this plugin when:
- User asks about architecture visualization or diagrams
- User wants to document their system architecture
- User is preparing a pitch deck or presentation
- User asks "what does my architecture look like?"
- User wants to understand infrastructure from Terraform/Docker files
- User needs diagrams for documentation or README

## Available Commands

| Command | Purpose |
|---------|---------|
| `/arch:generate` | Scan codebase and generate full architecture diagram suite |
| `/arch:view $SCOPE` | Generate a focused diagram for a specific component or flow |
| `/arch:deck --investor` | Create investor pitch deck with auto-generated diagrams |
| `/arch:deck --client` | Create client-facing presentation deck |
| `/arch:export` | Export diagrams in multiple formats (SVG, PNG, PDF) |
| `/arch:refresh` | Regenerate diagrams after code changes |

## Supported Sources

The plugin can analyze:
- **Terraform** - AWS resources (Lambda, DynamoDB, S3, SQS, API Gateway, etc.)
- **Docker Compose** - Services, dependencies, networking

Future analyzers will add support for:
- Kubernetes manifests
- AWS CDK
- CloudFormation
- Application code (Express routes, database connections)

## How It Works

1. **Analyzers** scan IaC files and extract components
2. **GraphBuilder** merges results into a unified architecture graph
3. **Dagre layout** positions nodes using hierarchical algorithm
4. **SVG renderer** creates animated, styled diagrams

## Output Location

Diagrams are saved to `docs/architecture/latest/`:
- `overview.svg` - Animated SVG with flow indicators
- `overview.png` - Static image for embedding
- `embed.html` - Copy-paste snippet for README

## Interactive Refinement

After generation, you can refine diagrams conversationally:
- "Zoom into the auth flow"
- "Add a callout explaining the cache layer"
- "Move the database to the right"
- "Highlight the payment processing path"
