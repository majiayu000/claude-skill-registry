---
name: readme-improvement
description: Use when the user asks to create or improve a README file, project documentation, getting started guide, or installation instructions. Triggers on keywords like "README", "getting started", "installation guide", "project overview", "setup instructions".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# README Improvement

You are to operate as an expert technical writer and project documentation specialist to create a comprehensive, accurate README.md file.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

---

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT
Before every major operation:
1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION
Before claiming any relationship:
- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples

### TOOL_EFFICIENCY_PROTOCOL
- Batch multiple Grep searches into single calls with OR patterns
- Use parallel Read operations for related files

### CONTEXT_ANCHOR_SYSTEM
Every 10 operations:
1. Re-read the original task description
2. Verify the current operation aligns with original goals
3. Update the `Current Focus` in `## Progress` section

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN README ANALYSIS

Build a structured knowledge model in `.ai/workspace/analysis/[project-name].md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with standard headings
2. **Discovery searches** for all project files

### README-SPECIFIC DISCOVERY

**PROJECT_OVERVIEW_DISCOVERY**: Focus on README-relevant patterns:

1. **Project Structure Analysis**: Find entry points, map key directories, identify technologies. Document under `## Project Structure`.

2. **Feature Discovery**: Find user-facing features and map API endpoints. Document under `## Feature Mapping`.

3. **Setup Requirements Analysis**: Find package files, map dependencies, identify configuration needs. Document under `## Setup Requirements`.

### PHASE 1B: SYSTEMATIC FILE ANALYSIS FOR README

**IMPORTANT: MUST DO WITH TODO LIST**

For each file, document in `## Knowledge Graph`:
- Standard fields plus README-specific:
- `readmeRelevance`: How component should be represented (1-10)
- `userImpact`: How component affects end users
- `setupRequirements`: Prerequisites for this component
- `configurationNeeds`: Configuration required
- `featureDescription`: User-facing features provided
- `troubleshootingAreas`: Common issues users might encounter
- `exampleUsage`: Usage examples for README
- `projectContext`: How it fits into overall project

### PHASE 1C: OVERALL ANALYSIS

Write comprehensive summary showing:
- Complete end-to-end workflows discovered
- Key features and capabilities
- Setup and configuration requirements

---

## PHASE 2: README PLAN GENERATION

Generate detailed README outline under `## README Plan`:
- Project Overview
- Installation
- Usage
- Configuration
- Development guidelines

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present README plan for explicit approval. **DO NOT** proceed without it.

---

## PHASE 4: README EXECUTION

Once approved, create the comprehensive README using all README_SAFEGUARDS.

### README Structure Template

```markdown
# Project Name

Brief description of the project.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- Feature 1
- Feature 2

## Prerequisites
- Node.js >= 18
- .NET 9 SDK

## Installation
```bash
# Clone the repository
git clone [url]

# Install dependencies
npm install
dotnet restore
```

## Configuration
[Configuration details]

## Usage
[Usage examples]

## Development
[Development setup]

## Testing
[Testing instructions]

## Troubleshooting
[Common issues and solutions]
```

---

## SUCCESS VALIDATION

Verify README is:
- Accurate (all instructions work)
- Comprehensive (covers all setup needs)
- Helpful (new users can get started)

Document under `## README Validation`.

---

## README Guidelines

- **User-first approach**: Organize for new users
- **Verified instructions**: Test all setup and installation instructions
- **Clear project purpose**: Explain what the project does and why
- **Practical examples**: Include working examples users can follow
- **No assumptions**: Don't assume user knowledge
