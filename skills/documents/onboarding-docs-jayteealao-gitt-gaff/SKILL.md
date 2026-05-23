---
name: onboarding-docs
description: This skill should be used when generating developer onboarding documentation including architecture overviews, setup guides, code tours, and decision records.
---

# Onboarding Documentation Skill

Generate comprehensive onboarding documentation for new developers.

## When to Use

- Creating documentation for new team members
- Generating architecture overviews
- Building local development setup guides
- Creating guided code walkthroughs
- Documenting architecture decisions (ADRs)

## Reference Documents

- [Architecture Overview](./references/architecture-overview.md) - High-level system documentation
- [Setup Guide](./references/setup-guide.md) - Local development setup patterns
- [Code Tour](./references/code-tour.md) - Guided codebase walkthrough patterns
- [Decision Log](./references/decision-log.md) - Architecture decision records (ADR)

## Documentation Structure

### Recommended Layout

```
docs/
├── onboarding/
│   ├── README.md              # Welcome and navigation
│   ├── architecture.md        # System architecture
│   ├── setup.md               # Local development setup
│   ├── code-tour.md           # Guided codebase tour
│   └── decisions/             # Architecture Decision Records
│       ├── 001-database.md
│       ├── 002-api-design.md
│       └── template.md
├── api/                       # API documentation
├── deployment/                # Deployment guides
└── troubleshooting/           # Common issues
```

## Core Principles

### 1. Progressive Disclosure

Start with high-level concepts, then dive deeper:

```markdown
Level 1: What does this system do? (1 paragraph)
Level 2: What are the main components? (architecture diagram)
Level 3: How do they interact? (sequence diagrams)
Level 4: Implementation details (code references)
```

### 2. Task-Oriented Structure

Organize around what developers need to DO:

```markdown
✓ "How to set up the development environment"
✓ "How to add a new API endpoint"
✓ "How to debug authentication issues"

✗ "The Authentication Module"
✗ "Database Schema"
✗ "Configuration Options"
```

### 3. Working Examples

Every concept should have a working example:

```markdown
✓ Code snippets that can be copy-pasted
✓ Complete working examples in a separate repo/directory
✓ Links to relevant test files as examples

✗ Pseudo-code that doesn't compile
✗ Incomplete snippets
✗ "Exercise for the reader" scenarios
```

### 4. Keep It Current

Documentation should be treated as code:

```markdown
- Version control all documentation
- Review docs in PRs that change behavior
- Automate doc validation where possible
- Include "last verified" dates
```

## Content Templates

### Welcome Document

```markdown
# Welcome to [Project Name]

## Quick Links
- 🚀 [Setup Guide](./setup.md) - Get your local environment running
- 🏗️ [Architecture](./architecture.md) - Understand the system
- 🗺️ [Code Tour](./code-tour.md) - Navigate the codebase
- 📚 [API Docs](../api/README.md) - API reference

## First Day Checklist
- [ ] Read the architecture overview
- [ ] Complete local setup
- [ ] Run the test suite
- [ ] Make a small change and deploy to staging

## Getting Help
- Slack: #team-channel
- On-call: @oncall-rotation
- Documentation issues: File a PR
```

### Architecture Document

```markdown
# System Architecture

## Overview
[1-2 paragraph system description]

## System Diagram
[ASCII diagram or link to diagram]

## Components
### [Component 1]
- **Purpose:** [What it does]
- **Technology:** [Tech stack]
- **Location:** `src/components/...`
- **Depends on:** [Other components]

## Data Flow
[Sequence diagram or description]

## Key Decisions
- [Why we chose X over Y](./decisions/001-xxx.md)
```

## Verification Checklist

Before finalizing onboarding docs:

- [ ] New developer can complete setup in < 30 minutes
- [ ] All code examples compile/run
- [ ] All links are valid
- [ ] Diagrams are up-to-date
- [ ] No references to removed/renamed components
- [ ] Contact information is current
