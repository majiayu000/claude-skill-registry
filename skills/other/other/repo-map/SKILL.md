---
name: repo-map
description: Generate a ranked codebase map showing key files and relationships
argument-hint: "[--depth=2] [--focus=<module>]"
tags: [navigation, codebase, architecture, productivity]
user-invocable: true
---

# Codebase Map Generator

Generate a graph-ranked map of the codebase showing the most important files, dependencies, and call relationships.

## What To Do

1. **Analyze the repository structure**: Use Glob to find all source files, count per directory, identify entry points.

2. **Rank files by importance**:
   - Fan-in (how many files reference this file) -- higher = more important
   - Fan-out (how many files this file imports) -- moderate = hub file
   - Size and change frequency via `git log`
   - Entry points (Controllers, Program.cs, App.tsx) rank highest

3. **Generate the map** as structured summary:
   ```
   ## Core (highest rank)
   src/backend/Program.cs                    -- Entry point, DI registration
   src/backend/Services/MatchingService.cs   -- Core matching algorithm (12 refs)

   ## API Layer
   src/backend/Controllers/CandidateController.cs -- 8 endpoints

   ## Domain
   src/backend/Models/CandidateProfile.cs    -- Central model (18 refs)
   ```

4. **Focus mode**: When `--focus=<module>`, zoom into that module with full dependency graph.

## Arguments
- `--depth=<n>`: Directory tree depth (default: 2)
- `--focus=<module>`: Focus on specific module
- `--format=<md|mermaid|json>`: Output format