---
name: awesome-copilot
description: Expert guidance for creating GitHub Copilot customizations including custom agents, prompts, instructions, and collections. Based on the awesome-copilot community toolkit with 200+ agents, 180+ prompts, and 150+ instructions. Use when customizing GitHub Copilot, creating specialized AI agents, writing coding standards, or building developer productivity tools.
---

# Awesome GitHub Copilot Customization Expert

Expert guidance for creating and managing GitHub Copilot customizations based on the community-curated awesome-copilot toolkit. Create custom agents, prompts, instructions, and collections to enhance developer productivity.

## Core Capabilities

1. **Custom Agents** - Create specialized AI personas with specific expertise
2. **Prompts** - Build reusable task templates for common workflows
3. **Instructions** - Define coding standards that auto-apply based on file patterns
4. **Collections** - Organize customizations into themed groupings
5. **Best Practices** - Community-curated standards and patterns

## Quick Reference

### Component Types

| Type | Purpose | File Extension | Access Method |
|------|---------|---------------|---------------|
| **Agents** | Specialized AI personas | `.agent.md` | Select in Copilot Chat or CCA |
| **Prompts** | Task-specific templates | `.prompt.md` | `/awesome-copilot <command>` |
| **Instructions** | Auto-applying standards | `.instructions.md` | Automatic by file pattern |
| **Collections** | Curated groupings | `.collection.md` | Browse in Copilot extensions |

---

## Instructions

### Creating Custom Agents

**File Structure:**
```
agents/
├── my-expert.agent.md
├── database-specialist.agent.md
└── security-reviewer.agent.md
```

**Agent File Template:**
```markdown
---
description: 'Clear description of what this agent does'
model: claude-3-5-sonnet-20241022
tools:
  - mcp-server-name  # Optional: MCP servers this agent uses
---

# Agent Name

## Role
You are a [specific role] specializing in [domain].

## Expertise
- Skill area 1
- Skill area 2
- Skill area 3

## Guidelines
1. Always follow [specific pattern]
2. Consider [important aspects]
3. Provide [expected outputs]

## Examples
[Concrete examples of expected interactions]
```

**Naming Conventions:**
- Lowercase only: `python-expert.agent.md`
- Hyphens for spaces: `database-migration-specialist.agent.md`
- Descriptive and clear: `azure-bicep-architect.agent.md`

---

### Creating Prompts

**File Structure:**
```
prompts/
├── create-readme.prompt.md
├── optimize-sql.prompt.md
└── generate-tests.prompt.md
```

**Prompt File Template:**
```markdown
---
title: Descriptive Prompt Title
description: What this prompt does and when to use it
---

# System Instructions

You are tasked with [specific task].

## Context
[Background information needed]

## Requirements
1. Must include [requirement 1]
2. Should follow [requirement 2]
3. Output format: [expected format]

## Process
1. Step 1
2. Step 2
3. Step 3

## Example Output
```[language]
[Example of expected output]
```
```

**Usage:**
In GitHub Copilot Chat:
```
/awesome-copilot create-readme
/awesome-copilot optimize-sql
```

---

### Creating Instructions

**File Structure:**
```
instructions/
├── csharp.instructions.md
├── react.instructions.md
└── terraform.instructions.md
```

**Instruction File Template:**
```markdown
---
description: Coding standards for [technology/framework]
patterns:
  - '**/*.cs'           # File patterns to apply to
  - '**/src/**/*.tsx'
---

# [Technology] Best Practices

## Code Style
- Follow [specific style guide]
- Use [naming conventions]
- Organize files as [structure]

## Patterns
**DO:**
```[language]
// Good example
```

**DON'T:**
```[language]
// Bad example
```

## Common Scenarios

### Scenario 1: [Common Task]
[Specific guidance]

### Scenario 2: [Another Task]
[More guidance]

## References
- [Documentation link]
- [Style guide link]
```

**Auto-Application:**
Instructions automatically apply when editing files matching the patterns.

---

### Creating Collections

**File Structure:**
```
collections/
├── devops-toolkit.collection.md
├── security-essentials.collection.md
└── azure-specialists.collection.md
```

**Collection File Template:**
```markdown
---
title: Collection Name
description: What this collection provides
---

# Collection Name

Curated collection of [theme] customizations.

## Included Items

### Agents
- [agent-name](../agents/agent-name.agent.md) - Description
- [another-agent](../agents/another-agent.agent.md) - Description

### Prompts
- [prompt-name](../prompts/prompt-name.prompt.md) - Description
- [another-prompt](../prompts/another-prompt.prompt.md) - Description

### Instructions
- [instruction-name](../instructions/instruction-name.instructions.md) - Description

## Use Cases
1. Use case 1
2. Use case 2
3. Use case 3

## Getting Started
[Quick start guide for this collection]
```

---

## Common Patterns

### Language-Specific Agent

```markdown
---
description: 'Expert in [Language] with focus on modern practices and performance'
model: claude-3-5-sonnet-20241022
---

# [Language] Expert

## Expertise
- Modern [Language] features
- Performance optimization
- Testing frameworks
- Popular libraries and frameworks

## Coding Standards
- Use [style guide]
- Follow [naming conventions]
- Prefer [patterns]

## Common Tasks
- Code review with security focus
- Performance optimization
- Refactoring legacy code
- Writing comprehensive tests
```

### DevOps Workflow Prompt

```markdown
---
title: Generate CI/CD Pipeline
description: Creates GitHub Actions or Azure Pipelines workflow
---

# CI/CD Pipeline Generator

Generate a complete CI/CD pipeline with:

## Requirements
1. Build stage with dependency caching
2. Test stage with coverage reporting
3. Security scanning
4. Deployment stages (dev, staging, prod)
5. Approval gates for production

## Platform-Specific
- **GitHub Actions**: Use reusable workflows
- **Azure Pipelines**: Use YAML templates
- **Jenkins**: Use declarative pipeline

## Best Practices
- Fail fast on critical errors
- Parallel execution where possible
- Secrets management via key vault
- Artifact storage and versioning
```

### Framework Instruction Set

```markdown
---
description: Best practices for [Framework] development
patterns:
  - '**/*.jsx'
  - '**/*.tsx'
  - '**/components/**'
---

# [Framework] Development Standards

## Component Structure
```
components/
├── ComponentName/
│   ├── index.ts        # Barrel export
│   ├── ComponentName.tsx
│   ├── ComponentName.test.tsx
│   ├── ComponentName.styles.ts
│   └── types.ts
```

## Coding Rules
1. Use functional components with hooks
2. Extract business logic into custom hooks
3. Implement proper TypeScript types
4. Write unit tests for all components
5. Use CSS-in-JS or CSS modules

## Anti-Patterns
- Avoid prop drilling (use context)
- Don't mutate state directly
- Keep components single-responsibility
```

---

## Best Practices

### Agent Design
1. **Single Responsibility** - Each agent should have one clear expertise
2. **Specific Context** - Provide concrete guidelines, not generic advice
3. **Include Examples** - Show expected interactions and outputs
4. **Reference Standards** - Link to official docs and style guides
5. **Test Thoroughly** - Validate agent responses before deployment

### Prompt Engineering
1. **Clear Instructions** - Be explicit about requirements
2. **Structured Output** - Define expected format precisely
3. **Error Handling** - Include guidance for edge cases
4. **Context Limits** - Keep prompts focused and concise
5. **Reusable** - Design for multiple similar use cases

### Instruction Quality
1. **Pattern Matching** - Use specific glob patterns for file targeting
2. **Comprehensive Coverage** - Address common scenarios thoroughly
3. **Prioritize DO's** - Show correct patterns prominently
4. **Explain Why** - Include rationale for standards
5. **Keep Updated** - Review as frameworks evolve

### Collection Curation
1. **Themed Grouping** - Organize by workflow or domain
2. **Complete Coverage** - Include all needed components
3. **Cross-Reference** - Link related items clearly
4. **Onboarding Guide** - Help users get started quickly
5. **Maintain Quality** - Review and update regularly

---

## Validation & Testing

### Before Submitting

1. **Validate Front Matter:**
   ```bash
   # Check YAML syntax
   npm run validate
   ```

2. **Test File Naming:**
   - All lowercase: ✓
   - Hyphens only: ✓
   - No spaces/underscores: ✓
   - Correct extension: ✓

3. **Build Check:**
   ```bash
   npm run build
   ```

4. **Line Endings:**
   ```bash
   bash scripts/fix-line-endings.sh
   ```

5. **Test in Copilot:**
   - Load agent/prompt/instruction
   - Verify it activates correctly
   - Test with sample scenarios
   - Validate output quality

---

## Repository Structure

```
awesome-copilot/
├── agents/                # 200+ specialized agents
│   ├── python-expert.agent.md
│   ├── azure-architect.agent.md
│   └── security-reviewer.agent.md
├── prompts/              # 180+ task templates
│   ├── create-readme.prompt.md
│   ├── optimize-code.prompt.md
│   └── generate-tests.prompt.md
├── instructions/         # 150+ coding standards
│   ├── csharp.instructions.md
│   ├── react.instructions.md
│   └── terraform.instructions.md
├── collections/          # Curated groupings
│   ├── azure-devops.collection.md
│   └── security-toolkit.collection.md
├── .schemas/            # JSON schemas for validation
└── scripts/             # Build and validation tools
```

---

## Available Categories

### Agents (200+)
- **Languages**: Python, Java, C#, Go, Rust, TypeScript, PHP, Kotlin
- **Frameworks**: React, Next.js, Angular, .NET, Laravel, Spring Boot
- **Cloud**: Azure, AWS, GCP specialists and architects
- **DevOps**: CI/CD, IaC (Terraform, Bicep), Kubernetes
- **Databases**: PostgreSQL, MongoDB, SQL Server, CosmosDB
- **Specialized**: Security, Accessibility, Performance, AI/ML

### Prompts (180+)
- Code generation and refactoring
- Testing (Jest, Pytest, JUnit, xUnit)
- Documentation (README, API docs)
- Architecture and planning
- Cloud optimization
- Data modeling
- MCP server generation

### Instructions (150+)
- Language-specific standards
- Framework best practices
- DevOps patterns
- Database optimization
- Security guidelines
- Accessibility requirements
- Performance tuning

---

## When to Use This Skill

- Creating custom GitHub Copilot agents
- Writing reusable code generation prompts
- Defining project coding standards
- Building developer productivity tools
- Customizing AI assistance for specific domains
- Organizing team development guidelines
- Contributing to awesome-copilot repository

## Keywords

github copilot, custom agents, prompts, instructions, collections, ai customization, code generation, developer productivity, coding standards, best practices, mcp integration, copilot extensions, ai agents, prompt engineering, code templates, development workflows
