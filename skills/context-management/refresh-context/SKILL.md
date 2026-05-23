---
name: refresh-context
description: Reads and loads architectural context files (architecture.md and architecture.puml) to understand the PSX Memory Card Manager project structure, components, and design patterns. Use when starting a new session or when architectural context is needed for code changes.
metadata:
  author: psx-memcard-project
  version: "1.0"
allowed-tools: read_file
---

# Refresh Context Skill

This skill loads the architectural context for the PSX Memory Card Manager project by reading key documentation files.

## When to use this skill

- At the start of a new session to understand project architecture
- When making changes that affect multiple components
- When architectural context is needed for implementing new features
- When debugging issues that span multiple layers (UI, ViewModel, Domain)

## What this skill does

Reads and provides context from:
1. `architecture.md` - Detailed component structure, MVVM patterns, and responsibilities
2. `architecture.puml` - Visual C4 model diagrams showing system boundaries and data flow

## Instructions

### Step 1: Read architecture documentation
Load the main architecture documentation to understand:
- MVVM pattern implementation
- Component responsibilities and boundaries
- Dependency injection structure
- Layer separation (UI, ViewModel, Domain)

```bash
# Read the architecture documentation
read_file('architecture.md', 1, 300)
```

### Step 2: Load visual architecture model
Read the PlantUML C4 model to understand:
- System container boundaries  
- Component relationships and data flow
- Dependency directions between layers

```bash
# Read the PlantUML C4 model
read_file('architecture.puml', 1, 100)  
```

## Key architectural concepts to remember

After reading the files, keep these principles in mind:

- **MVVM Pattern**: Views render UI, ViewModels manage state, Domain handles business logic
- **Dependency Injection**: Use uber/dig container in `internal/dig/container.go`
- **Layer Separation**: UI (`internal/ui/`) ↔ ViewModel ↔ Domain (`internal/memcard/`)
- **Data Binding**: ViewModels use bindings/events, never manipulate widgets directly

## Expected outcome

After running this skill, you should have context about:
- Main application components (ManagerWindowView, BlocksContainer, etc.)
- Memory card domain concepts (MemoryCard, Block, Icon)
- How data flows between UI and business logic
- Project structure and file organization
