---
name: deepinit
description: 深度代码库初始化，生成分层 AGENTS.md 文档
---

# oh-my-ccg Deep Init

Generate comprehensive codebase documentation for agent context.

## Workflow

1. **Root scan**: Use explore agent to map top-level structure
2. **Module discovery**: Identify each module/package/directory
3. **Per-module analysis**: For each module:
   - Entry points and exports
   - Key classes and functions
   - Dependencies (internal and external)
   - Test coverage
4. **Generate AGENTS.md**: Hierarchical documentation:
   ```
   # Project: <name>
   ## Architecture Overview
   ## Module: <name>
   ### Entry Points
   ### Key Symbols
   ### Dependencies
   ```
5. **Generate module-level docs**: Create AGENTS.md in each major directory
6. **Update project memory**: Store structure in .oh-my-ccg/project-memory.json

## Output
- Root AGENTS.md with full project map
- Per-module AGENTS.md files
- Updated project memory
