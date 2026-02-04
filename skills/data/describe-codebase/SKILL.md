---
name: describe-codebase
description: Generate an onboarding-level summary of a codebase for new developers, including architecture, patterns, and key entry points
category: documentation
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Describe Codebase

Generate an onboarding-level summary designed for a new developer joining the team.

## Procedure

### Phase 1 - Gather Information

1. Map the overall architecture and core modules, explaining their purposes
2. Identify and highlight code patterns, design paradigms (e.g., functional, event-driven, modular, object-oriented) and practices across the codebase
3. Identify main dependencies relevant to further development
4. Identify and explain commands that can be run to interact with the codebase
5. Identify the main data flows, state management patterns, and functional dependencies
6. Describe how security, configuration, and environment management are handled
7. Outline major entry points (APIs, CLI, smart contracts, services) and their responsibilities
8. Identify key abstractions, reusable utilities, and integration boundaries
9. Point out any complex or critical paths that require extra caution
10. Recommend areas of the code that a new developer should study first to become productive

### Phase 2 - Generate Summary

Produce a comprehensive yet readable summary covering:

- **Architecture Overview**: High-level structure and module relationships
- **Design Patterns**: Patterns used throughout the codebase
- **Key Dependencies**: External libraries and their purposes
- **Development Commands**: How to build, test, and run the project
- **Data Flow**: How data moves through the system
- **Configuration**: Environment and configuration management
- **Entry Points**: Main APIs, CLI commands, or services
- **Critical Paths**: Areas requiring extra attention
- **Getting Started**: Recommended study path for new developers

## Constraints
- Only describe what can be inferred from the provided code
- Do not invent undocumented behavior
- Describe in clear, easy to understand format
- Use full sentences with appropriate level of detail depending on complexity
