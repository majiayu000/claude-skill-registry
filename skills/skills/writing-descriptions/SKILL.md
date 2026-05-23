---
name: writing-descriptions
description: Examples and patterns for writing effective agent and skill descriptions. Use when crafting descriptions that serve as routing keys for Claude's invocation decisions.
---

# Writing Effective Descriptions

The `description` field is THE routing key. Claude reads descriptions to decide whether to invoke an agent or skill. Poor descriptions = artifacts that never trigger.

## The Formula

```
{Role/expertise}. Use [PROACTIVELY] when {specific trigger conditions}.
```

- **Role/expertise**: What the agent/skill does (third person for skills)
- **PROACTIVELY**: Include if Claude should invoke without being asked
- **Trigger conditions**: Specific situations that warrant invocation

## Agent Description Examples

### By Category

| Category | Description |
|----------|-------------|
| **Debugging** | "Docker troubleshooter. Use PROACTIVELY when containers fail to start, crash, or behave unexpectedly." |
| **Code Review** | "Security-focused code reviewer. Use PROACTIVELY when reviewing authentication, authorization, or data handling code." |
| **Testing** | "Test generation specialist. Use when asked to add tests or improve test coverage for existing code." |
| **Infrastructure** | "Kubernetes deployment expert. Use PROACTIVELY when working with k8s manifests, helm charts, or cluster issues." |
| **API Design** | "REST API designer. Use when creating new endpoints, designing request/response schemas, or documenting APIs." |
| **Performance** | "Performance optimization specialist. Use when profiling, optimizing queries, or reducing latency." |
| **Database** | "PostgreSQL query optimizer. Use PROACTIVELY when queries are slow or EXPLAIN shows sequential scans." |
| **Frontend** | "React component architect. Use when building complex UI components or refactoring component hierarchies." |

### Good vs Bad

| Bad | Why It Fails | Better |
|-----|--------------|--------|
| "Helps with Docker" | Too vague, no triggers | "Docker troubleshooter for container failures" |
| "General coding assistant" | No specificity | "Python async specialist for concurrent code" |
| "Does database stuff" | Unclear scope | "PostgreSQL query optimizer for slow queries" |
| "Useful for many things" | No routing signal | "Git workflow automator for branching and merging" |
| "I help you with tests" | Wrong person (first) | "Test generator for untested functions" |

## Skill Description Examples

### By Category

| Category | Example Description |
|----------|---------------------|
| **Document Processing** | "Comprehensive document creation, editing, and analysis with tracked changes support. Use when working with .docx files for creating, modifying, or extracting content." |
| **Data Analysis** | "Analyzes Excel spreadsheets, creates pivot tables, generates charts. Use when analyzing .xlsx files, spreadsheets, or tabular data." |
| **API Integration** | "Creates MCP servers for external API integration using TypeScript or Python. Use when building Model Context Protocol servers or LLM tool integrations." |
| **Creative/Design** | "Creates distinctive production-grade frontend interfaces. Use when building web components, landing pages, dashboards, or styling any web UI." |
| **Workflow Automation** | "Guides users through structured document co-authoring. Use when writing documentation, proposals, technical specs, or decision docs." |
| **Testing** | "Tests local web applications using Playwright. Use when verifying frontend functionality, debugging UI, or capturing browser screenshots." |
| **PDF Processing** | "Extracts text and tables from PDFs, fills forms, merges documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction." |
| **Presentations** | "Creates and modifies PowerPoint presentations with consistent styling. Use when building slide decks, adding charts, or formatting presentations." |

### Skills: Third Person Requirement

Skills must use third person voice:

```yaml
# Good (third person)
description: Extracts text from PDFs and fills form fields.

# Bad (first person)
description: I help you process PDFs.

# Bad (second person)
description: Helps you extract PDF text.
```

## Proactive vs On-Demand

### Use PROACTIVELY when:
- The situation is detectable from context (error messages, file types)
- Waiting for explicit request would delay the user
- The agent/skill is highly specialized

```
# Proactive - Claude should invoke without being asked
"Docker troubleshooter. Use PROACTIVELY when containers fail to start..."
"Security reviewer. Use PROACTIVELY when reviewing auth code..."
```

### On-demand (no PROACTIVELY) when:
- User should explicitly request the capability
- Multiple valid approaches exist
- The action has significant side effects

```
# On-demand - wait for user request
"Test generator. Use when asked to add tests..."
"Database migrator. Use when user requests schema changes..."
```

## Trigger Specificity

More specific triggers = more reliable invocation:

| Vague Trigger | Specific Trigger |
|---------------|------------------|
| "when needed" | "when containers fail to start or exit unexpectedly" |
| "for code review" | "when reviewing authentication, authorization, or session code" |
| "for testing" | "when test coverage is below 80% or user asks for tests" |
| "for performance" | "when queries exceed 100ms or EXPLAIN shows sequential scans" |

## Combining Multiple Triggers

Use "or" to list multiple valid triggers:

```
"PDF processor. Use when working with PDF files, filling forms,
extracting tables, or merging documents."
```

Use commas for related triggers:

```
"Kubernetes expert. Use PROACTIVELY when working with pods,
deployments, services, or ingress configurations."
```
