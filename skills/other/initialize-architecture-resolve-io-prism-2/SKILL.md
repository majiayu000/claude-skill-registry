---
name: initialize-architecture
description: Use to create complete architecture documentation structure. Creates all required architecture documents from templates.
version: 1.0.0
---

# Initialize Architecture Documentation Task

## When to Use

- **New Projects**: Initialize architecture documentation for greenfield projects
- **Missing Documentation**: Create missing architecture documents in existing projects
- **Architecture Reset**: Rebuild architecture documentation structure
- **Onboarding**: Ensure all architecture documents exist for new team members

## What This Skill Does

Creates complete architecture documentation structure from templates:

- **Configuration**: Reads locations from `.prism/core-config.yaml`
- **Status Check**: Detects existing vs missing documents
- **Generation**: Creates documents from standardized templates
- **Indexing**: Builds master README with navigation

## Prerequisites

- Project root must have `.prism/core-config.yaml`
- `architecture.architectureShardedLocation` config (default: `docs/architecture`)
- Write permissions to create files

## Quick Start

1. Run the skill
2. Review existing documentation status
3. Choose mode (create missing or recreate all)
4. Wait for document generation
5. Review generated documents and fill in project-specific details

**Output Location**: `docs/architecture/` (or as configured)

## Workflow Steps

| Step | Name | Purpose |
|------|------|---------|
| 1 | Load Configuration | Read `core-config.yaml` settings |
| 2 | Check Existing | Show status of existing docs |
| 3 | Create Directory | Ensure architecture folder exists |
| 4 | Generate Documents | Create documents from templates |
| 5 | Create Master Index | Build README.md navigation |
| 6 | Validate & Complete | Verify files and show next steps |

## Documents Generated

| Document | Purpose |
|----------|---------|
| `coding-standards.md` | Code quality and style guidelines |
| `tech-stack.md` | Technologies, frameworks, dependencies |
| `source-tree.md` | Code organization and structure |
| `deployment.md` | Infrastructure and deployment process |
| `data-model.md` | Database schemas and relationships |
| `api-contracts.md` | API endpoints and integrations |
| `README.md` | Master index and navigation |

## Modes

- **Create Missing**: Only generate documents that don't exist
- **Recreate All**: Regenerate all documents (overwrites existing)
- **Cancel**: Exit without changes

## Reference Documentation

- **[Document Templates](./reference/document-templates.md)** - Detailed templates for each document type

## Document Status Indicators

All documents start as Draft and progress through:

- 🔴 **Draft** - Initial template, needs content
- 🟡 **In Progress** - Being actively updated
- 🟢 **Complete** - Reviewed and approved

## Next Steps After Initialization

1. 📝 Review each document and fill in project-specific details
2. 🎨 Update status indicators as documents are completed
3. 👥 Assign document owners
4. 📅 Schedule quarterly reviews
5. 🔄 Keep documentation current with architecture changes

## Guardrails

- Always verify config is loaded before proceeding
- Check for existing documents to avoid accidental overwrites
- Write files immediately after generation
- Inform user of all files created
- Provide clear next steps for document completion
