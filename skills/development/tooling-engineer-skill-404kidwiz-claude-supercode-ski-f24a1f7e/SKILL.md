---
name: tooling-engineer
description: Expert in building developer tools, CLI utilities, IDE extensions, and optimizing local development environments.
---

# Tooling Engineer

## Purpose
Provides expertise in building developer productivity tools including command-line interfaces, IDE extensions, build system optimizations, and local development environment automation. Focuses on improving developer experience and workflow efficiency.

## When to Use
- Building command-line tools and utilities
- Creating IDE/editor extensions (VS Code, JetBrains)
- Optimizing build systems and compilation times
- Automating repetitive development tasks
- Setting up local development environments
- Creating code generators and scaffolding tools
- Building linters, formatters, and static analysis tools
- Improving developer onboarding experience

## Quick Start
**Invoke this skill when:**
- Building command-line tools and utilities
- Creating IDE/editor extensions (VS Code, JetBrains)
- Optimizing build systems and compilation times
- Automating repetitive development tasks
- Setting up local development environments

**Do NOT invoke when:**
- Building CI/CD pipelines → use devops-engineer
- Creating production applications → use appropriate developer skill
- Writing shell scripts for ops → use appropriate PowerShell/Bash skill
- Building MCP servers → use mcp-developer

## Decision Framework
```
Developer Tool Need?
├── Command Line → CLI with argument parsing + subcommands
├── IDE Integration → Extension/plugin for target IDE
├── Build Optimization → Caching, parallelization, incremental builds
├── Code Generation → Templates + AST manipulation
├── Environment Setup → Container or script-based provisioning
└── Automation → Task runner or custom tooling
```

## Core Workflows

### 1. CLI Tool Development
1. Define command structure and argument schema
2. Choose CLI framework (Commander, Click, Cobra, etc.)
3. Implement core functionality with clear separation
4. Add help text and usage examples
5. Implement configuration file support
6. Add shell completion scripts
7. Package for distribution (npm, pip, brew, etc.)
8. Write documentation with common use cases

### 2. IDE Extension Development
1. Identify target IDE and extension API
2. Define extension capabilities and triggers
3. Scaffold extension project structure
4. Implement core features (commands, providers, views)
5. Add configuration options
6. Test across different editor states
7. Publish to extension marketplace
8. Gather feedback and iterate

### 3. Build System Optimization
1. Profile current build to identify bottlenecks
2. Implement caching for expensive operations
3. Enable parallel execution where possible
4. Set up incremental builds for common changes
5. Add build metrics and monitoring
6. Document build system for team
7. Measure improvement and iterate

## Best Practices
- Design CLIs with Unix philosophy (composable, focused)
- Provide sensible defaults with override options
- Include verbose/debug modes for troubleshooting
- Make tools work offline when possible
- Fail fast with clear error messages
- Version tools and maintain backwards compatibility

## Anti-Patterns
- **Feature creep** → Keep tools focused on one job
- **Silent failures** → Always report errors clearly
- **No configuration** → Allow customization for different needs
- **Manual installation** → Provide package manager distribution
- **Poor error messages** → Include context and suggested fixes
