---
name: project-docs
description: Generate comprehensive, professional project documentation structures including README, ARCHITECTURE, USER_GUIDE, DEVELOPER_GUIDE, and CONTRIBUTING files. Use when the user requests project documentation creation, asks to "document a project", needs standard documentation files, or wants to set up docs for a new repository. Adapts to Python/Go projects and OpenSource/internal contexts.
license: MIT
compatibility: opencode
---

# Project Documentation Generator

Generate complete, professional documentation structures for software projects. Automatically adapts content and structure based on project language (Python/Go), context (OpenSource/internal), and existing files.

## Core Documentation Files

Always generate these five core files:

1. **README.md** - Project overview, quick start, badges
2. **ARCHITECTURE.md** - System design, components, data flow
3. **USER_GUIDE.md** - Usage examples, configuration, troubleshooting
4. **DEVELOPER_GUIDE.md** - Development setup, testing, contribution workflow
5. **CONTRIBUTING.md** - Contribution guidelines, code standards, PR process

## Workflow

### 1. Context Detection

Before generating docs, detect:

- **Language**: Scan for `go.mod`, `pyproject.toml`, `requirements.txt`, `setup.py`
- **Project type**: Check for `Dockerfile`, `terraform/`, `k8s/`, AI/ML indicators
- **Existing docs**: Identify what already exists to avoid duplication
- **License**: Detect from LICENSE file or ask user
- **Context**: Determine if OpenSource or internal based on repo structure

### 2. Ask Clarifying Questions

Ask user ONE question at a time to fill gaps:

- "What's the primary purpose of this project in one sentence?"
- "Who's the main audience? (developers, ops, end-users, all)"
- "Is this OpenSource or internal? (affects badges, contact info)"
- "Any company-specific tooling to mention? (Jira, Slack channels, etc.)"

### 3. Content Adaptation

Read `references/templates.md` to select appropriate template variants based on detected context.

**Language-specific elements:**

- Python: Package managers (`uv`, `pip`, `poetry`), testing (`pytest`), linting (`ruff`, `mypy`)
- Go: Build commands, testing, `golangci-lint`, module structure

**Context-specific elements:**

- OpenSource: Badges, CODE_OF_CONDUCT, security policy, community guidelines
- Internal: Slack channels, internal tools, compliance requirements, team contacts

**Project type adjustments:**

- AI Agents: MCP architecture, prompt patterns, example interactions
- Infrastructure: Terraform/K8s setup, deployment procedures, DR plans
- Microservices: API schemas, service mesh, health checks
- CLI Tools: Installation methods, command examples, flags

### 4. File Generation

Generate files in this order:

1. **README.md** first (most visible, sets tone)
2. **ARCHITECTURE.md** (technical foundation)
3. **DEVELOPER_GUIDE.md** (setup and contribution)
4. **USER_GUIDE.md** (end-user focused)
5. **CONTRIBUTING.md** (community guidelines)

Each file must:

- Use clear headers and structure from templates
- Include concrete, runnable examples
- Reference other docs when needed (avoid duplication)
- Match project's actual structure and commands

### 5. Template Application

For each file:

1. Select template variant from `references/templates.md`
2. Fill in project-specific details
3. Add context-appropriate sections
4. Ensure consistency across all files

### 6. Quality Checks

Before finalizing, verify:

- All code examples are runnable and accurate
- Commands match detected language/tooling
- Cross-references between docs are correct
- No placeholder text remains
- Tone is consistent (technical/friendly/formal based on context)

### 7. Output

Place all files in `docs/` and use `present_files` to share with user.

## Resources

### references/templates.md

Contains complete documentation templates for all five core files with variants for:

- Python vs Go projects
- OpenSource vs internal contexts
- Different project types (agent, service, CLI, infra)
- Different complexity levels

Claude should read this file to select appropriate templates before generating docs.

## Special Considerations

**For AI Agent projects:**

- Explain MCP server architecture
- Document tool integrations
- Show example prompts and interactions
- Include LLM configuration details

**For Infrastructure/DevOps:**

- Environment requirements (cloud providers, versions)
- Deployment runbooks
- Monitoring setup
- Disaster recovery procedures

**For Microservices:**

- API endpoint documentation
- Service dependency diagrams
- Inter-service communication patterns
- Health check and metrics endpoints

## Quality Standards

Every documentation file must:

- Have table of contents for files >200 lines
- Use proper code fences with language tags
- Include "Quick Start" section at top
- Show real, tested examples
- Explain "why" decisions were made
- Use consistent terminology throughout

## Avoid

- Generic placeholder text like "TODO" or "Coming soon"
- Outdated technology references
- Overly complex explanations without examples
- Duplicating content across multiple files
- Missing concrete code examples
