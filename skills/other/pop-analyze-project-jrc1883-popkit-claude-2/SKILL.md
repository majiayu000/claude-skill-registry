---
name: analyze-project
description: "Use when starting work on an unfamiliar project or needing to understand a codebase - performs comprehensive analysis discovering architecture, patterns, dependencies, testing coverage, and improvement opportunities. Do NOT use on projects you already know well or for targeted questions about specific files - use direct exploration instead for focused queries."
inputs:
  - from: any
    field: focus
    required: false
outputs:
  - field: analysis_report
    type: file_path
  - field: analysis_json
    type: file_path
next_skills:
  - pop-project-setup
  - pop-writing-plans
workflow:
  id: analyze-project
  name: Project Analysis Workflow
  version: 1
  description: Comprehensive codebase analysis with progressive disclosure
  steps:
    - id: detect_project
      description: Detect project type and basic structure
      type: agent
      agent: code-explorer
      next: depth_decision
    - id: depth_decision
      description: Choose analysis depth
      type: user_decision
      question: "What level of analysis do you need?"
      header: "Depth"
      options:
        - id: quick
          label: "Quick"
          description: "5-10 line summary, ~30 seconds"
          next: quick_analysis
        - id: standard
          label: "Standard"
          description: "Full analysis with recommendations"
          next: focus_decision
        - id: deep
          label: "Deep dive"
          description: "Exhaustive analysis with metrics"
          next: focus_decision
      next_map:
        quick: quick_analysis
        standard: focus_decision
        deep: focus_decision
    - id: quick_analysis
      description: Generate quick summary
      type: skill
      skill: pop-auto-docs
      next: complete
    - id: focus_decision
      description: Choose analysis focus area
      type: user_decision
      question: "Which area should we focus on?"
      header: "Focus"
      options:
        - id: architecture
          label: "Architecture"
          description: "Structure, patterns, entry points"
          next: run_analysis
        - id: quality
          label: "Quality"
          description: "Tests, linting, TypeScript"
          next: run_analysis
        - id: dependencies
          label: "Dependencies"
          description: "Packages, vulnerabilities"
          next: run_analysis
        - id: all
          label: "All areas"
          description: "Complete analysis"
          next: run_analysis
      next_map:
        architecture: run_analysis
        quality: run_analysis
        dependencies: run_analysis
        all: run_analysis
    - id: run_analysis
      description: Execute analysis based on selections
      type: spawn_agents
      agents:
        - type: code-explorer
          task: "Map project structure and architecture patterns"
        - type: performance-optimizer
          task: "Identify performance issues and bottlenecks"
      wait_for: all
      next: output_decision
    - id: output_decision
      description: Choose output format
      type: user_decision
      question: "How should we present the analysis?"
      header: "Output"
      options:
        - id: markdown
          label: "Markdown"
          description: "Human-readable report"
          next: generate_report
        - id: json
          label: "JSON"
          description: "Machine-readable for tooling"
          next: generate_json
        - id: both
          label: "Both"
          description: "Markdown + JSON files"
          next: generate_both
      next_map:
        markdown: generate_report
        json: generate_json
        both: generate_both
    - id: generate_report
      description: Generate markdown analysis report
      type: skill
      skill: pop-auto-docs
      next: next_step_decision
    - id: generate_json
      description: Generate JSON analysis output
      type: skill
      skill: pop-auto-docs
      next: next_step_decision
    - id: generate_both
      description: Generate both output formats
      type: skill
      skill: pop-auto-docs
      next: next_step_decision
    - id: next_step_decision
      description: Decide what to do after analysis
      type: user_decision
      question: "Analysis complete. What's next?"
      header: "Next Step"
      options:
        - id: generate
          label: "Generate MCP"
          description: "Create project-specific tools"
          next: generate_mcp
        - id: plan
          label: "Create plan"
          description: "Plan improvements"
          next: create_plan
        - id: done
          label: "Done"
          description: "Stop here"
          next: complete
      next_map:
        generate: generate_mcp
        plan: create_plan
        done: complete
    - id: generate_mcp
      description: Generate project-specific MCP server
      type: skill
      skill: pop-generate-mcp
      next: complete
    - id: create_plan
      description: Create implementation plan for improvements
      type: skill
      skill: pop-writing-plans
      next: complete
    - id: complete
      description: Analysis workflow finished
      type: terminal
---

# Analyze Project

## Overview

Perform deep analysis of a codebase to understand its architecture, patterns, dependencies, and opportunities for improvement.

**Core principle:** Understand before changing. Map before navigating.

**Trigger:** `/popkit:project analyze` command or when starting work on unfamiliar project

## Arguments

| Flag             | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `--json`         | Output structured JSON instead of markdown, save to `.claude/analysis.json` |
| `--quick`        | Quick summary only (5-10 lines)                                             |
| `--focus <area>` | Focus analysis: `arch`, `deps`, `quality`, `patterns`                       |

## Analysis Areas

### 1. Project Structure

Directory structure, entry points, file counts by type.

### 2. Technology Stack

Package managers, frameworks (Next.js, React, Vue, Express, FastAPI, Rust), databases (Supabase, Prisma, MongoDB, PostgreSQL).

### 3. Architecture Patterns

Frontend (component structure, state management, routing), Backend (API design, service layer, database access), Common (error handling, logging, configuration).

### 4. Code Quality

Linting config, TypeScript strictness, TODO/FIXME comments.

### 5. Testing Coverage

Test files, test frameworks, coverage reports.

### 6. Dependencies

Count, outdated packages, security vulnerabilities.

### 7. CI/CD and DevOps

CI config, Docker, deployment configuration.

## Output Format

### Markdown Report

```markdown
# [Project Name] Analysis Report

## Summary

- **Type**: [Web App / API / CLI / Library]
- **Stack**: [Primary technologies]
- **Size**: [Files, Lines of code]
- **Health**: [Good / Needs attention / Critical issues]

## Technology Stack

### Frontend

- Framework: [Next.js 14 / React / Vue / etc.]
- Styling: [Tailwind / styled-components / etc.]
- State: [Redux / Zustand / Context]

### Backend

- Runtime: [Node.js / Python / Rust / Go]
- Framework: [Express / FastAPI / Actix]
- Database: [PostgreSQL / MongoDB / etc.]

### DevOps

- CI/CD: [GitHub Actions / GitLab CI / etc.]
- Deployment: [Vercel / AWS / etc.]
- Container: [Docker / etc.]

## Architecture

### Key Patterns

- [Pattern 1]: [Where used]
- [Pattern 2]: [Where used]

### Entry Points

- Main: `[path]`
- API: `[path]`
- Tests: `[path]`

## Code Quality

| Metric            | Value                | Status       |
| ----------------- | -------------------- | ------------ |
| Linting           | [Configured/Missing] | [OK/Warning] |
| TypeScript Strict | [Yes/No]             | [OK/Warning] |
| Test Coverage     | [X%]                 | [OK/Warning] |
| TODO Comments     | [N]                  | [OK/Warning] |

## Recommendations

### Critical

1. [Issue requiring immediate attention]

### High Priority

1. [Important improvement]

### Nice to Have

1. [Enhancement suggestion]

## Next Steps

1. Run `/generate-mcp` to create project-specific tools
2. Run `/generate-skills` to capture discovered patterns
3. Run `/setup-precommit` to configure quality gates
```

### JSON Output

When `--json` flag is provided, saves to `.claude/analysis.json`:

```json
{
  "project_name": "project-name",
  "project_type": "nextjs",
  "analyzed_at": "2026-01-30T00:00:00Z",
  "frameworks": [{ "name": "nextjs", "confidence": 0.95, "version": "14.0.0" }],
  "patterns": [
    {
      "name": "pattern-name",
      "category": "architecture",
      "confidence": 0.85,
      "examples": ["path1", "path2"],
      "description": "Description"
    }
  ],
  "recommended_skills": ["skill1", "skill2"],
  "recommended_agents": ["agent1", "agent2"],
  "commands": {},
  "quality_metrics": {}
}
```

## Skill/Agent Recommendations

Based on detected patterns:

| Pattern                | Recommended Skill        | Priority |
| ---------------------- | ------------------------ | -------- |
| nextjs + vercel-config | `project:deploy`         | high     |
| prisma OR drizzle      | `project:db-migrate`     | high     |
| supabase               | `project:supabase-sync`  | medium   |
| docker-compose         | `project:docker-dev`     | medium   |
| feature-flags          | `project:feature-toggle` | low      |

| Pattern                     | Recommended Agent        |
| --------------------------- | ------------------------ |
| Large codebase (>100 files) | `performance-optimizer`  |
| React/Vue components        | `accessibility-guardian` |
| API routes                  | `api-designer`           |
| Security-sensitive          | `security-auditor`       |
| Low test coverage           | `test-writer-fixer`      |

## Integration

**Called by:**

- Manual `/analyze-project` command
- After `/init-project`

**Informs:**

- **/generate-mcp** - What tools to create
- **/generate-skills** - What patterns to capture
- **/setup-precommit** - What checks to configure
