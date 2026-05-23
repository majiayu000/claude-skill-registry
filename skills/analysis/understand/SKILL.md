---
name: understand
description: >
  Use when user asks "what does this codebase do", "explain the architecture",
  "how does this project work", "analyze this repo", "understand the code",
  or wants to learn how an unfamiliar codebase is structured.
agent: Explore
model: claude-sonnet-4-5
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git log:*, git show:*, ls:*)
  - TodoWrite
---

# Understand Codebase

Analyze application architecture, patterns, and how everything works together.

## Analysis Phases

**1. Project Discovery**
- Use Glob to map entire project structure
- Read key files (README, docs, configs)
- Use Grep to identify technology patterns
- Read entry points and main files

Discover:
- Project type and main technologies
- Architecture patterns (MVC, microservices, etc.)
- Directory structure and organization
- Dependencies and external integrations
- Build and deployment setup

**2. Architecture Analysis**
- **Entry points**: Main files, index files, app initializers
- **Core modules**: Business logic organization
- **Data layer**: Database, models, repositories
- **API layer**: Routes, controllers, endpoints
- **Frontend**: Components, views, templates
- **Configuration**: Environment setup, constants
- **Testing**: Test structure and coverage

**3. Pattern Recognition**
- Naming conventions for files and functions
- Code style and formatting rules
- Error handling approaches
- Authentication/authorization flow
- State management strategy
- Communication patterns between modules

**4. Dependency Mapping**
- Internal dependencies between modules
- External library usage patterns
- Service integrations
- API dependencies
- Database relationships
- Asset and resource management

**5. Integration Points**
- API endpoints and their consumers
- Database queries and their callers
- Event systems and listeners
- Shared utilities and helpers
- Cross-cutting concerns (logging, auth)

For large codebases, use TodoWrite to track areas needing deeper exploration.

## Output Format

Provide:
- **Architecture diagram** (in text/markdown)
- **Key components** and their responsibilities
- **Data flow** through the application
- **Important patterns** to follow
- **Tech stack summary**
- **Development workflow**

```
PROJECT OVERVIEW
├── Architecture: [Type]
├── Main Technologies: [List]
├── Key Patterns: [List]
└── Entry Point: [File]

COMPONENT MAP
├── Frontend
│   └── [Structure]
├── Backend
│   └── [Structure]
├── Database
│   └── [Schema approach]
└── Tests
    └── [Test strategy]

INTEGRATION POINTS
├── [Component] ↔ [Component]
└── [Service] → [Consumer]

DEVELOPMENT WORKFLOW
├── Build: [command]
├── Test: [command]
└── Deploy: [process]

KEY INSIGHTS
- [Important finding 1]
- [Important finding 2]
- [Unique patterns]
```

This gives you a complete mental model of how your application works.

Offer to save output to `.claude/codebase-overview.md` for future reference.
