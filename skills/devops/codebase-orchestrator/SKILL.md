---
description: Multi-MCP deployment tool for Claude Desktop that coordinates filesystem,
  git, and testing servers to assess deployment readiness across build status, test
  coverage, code quality, and component migration progress. Integrates with Compliance-Dashboard
  skill for design system validation.
name: codebase-orchestrator
---

# Codebase Orchestrator Skill

## Overview

Coordinates multiple Model Context Protocol (MCP) servers to provide comprehensive codebase status assessment. Enables deterministic evaluation of deployment readiness by orchestrating:

- **Filesystem MCP**: Directory structure analysis and file navigation
- **Git MCP**: Version control status and commit history
- **Testing MCP**: Test coverage metrics and execution status

Used in conjunction with the Compliance-Dashboard skill to track design system maturity across CareerCopilot's Northcote Curio component ecosystem.

## When to Use This Skill

Use Codebase-Orchestrator when you need to:

- **Assess deployment readiness** across build, test, quality, and migration metrics
- **Coordinate multi-server orchestration** to avoid token bloat from redundant queries
- **Evaluate component migration progress** from Material 3 to Northcote metaphors
- **Track design system health** (what percentage of components follow Northcote standards?)
- **Delegate next-step planning** to IDE agents (Claude Code, Codex CLI) with comprehensive context

## How It Works

The skill operates as an orchestrator that:

1. **Scans codebase** using filesystem MCP to understand structure
2. **Evaluates git status** using git MCP to track changes and history
3. **Runs test suite** using testing MCP to assess code quality
4. **Synthesizes results** into deployment readiness assessment
5. **Identifies gaps** and recommends next steps for improvement

## Usage Examples

### Example 1: Pre-Deployment Assessment
"Run codebase orchestrator to assess if CareerCopilot is ready for production deployment"

Claude will:
1. Check build status
2. Verify test coverage
3. Assess code quality metrics
4. Identify blocking issues
5. Report readiness score

### Example 2: Component Migration Tracking
"How far along are we with Material 3 → Northcote component migration?"

Claude will:
1. Scan components directory
2. Identify legacy Material 3 components (M3Button, M3Card, etc.)
3. Count migrated Northcote components (Pebble, Stone, Sediment, etc.)
4. Calculate migration percentage
5. Identify remaining work

### Example 3: Design System Compliance Integration
"Use codebase orchestrator to feed metrics into the compliance dashboard"

Claude will:
1. Assess current component compliance with Northcote standards
2. Track trend (improving or diverging?)
3. Identify high-priority refinement targets
4. Report progress toward design system maturity

## Key Capabilities

### Deployment Readiness Matrix

Evaluates across four dimensions:

| Dimension | What It Checks | Status Indicators |
|---|---|---|
| **Build Status** | Codebase compilation, dependency resolution | Green/Yellow/Red |
| **Test Coverage** | Unit test execution, coverage percentage | % Covered |
| **Code Quality** | Linting, type safety, common issues | Pass/Fail per metric |
| **Migration Progress** | Material 3 → Northcote component transformation | % Complete |

### MCP Coordination Strategy

Rather than making redundant queries to each MCP independently:

1. **Identifies what information is needed** across all servers
2. **Batches requests** to minimize token consumption
3. **Synthesizes results** into coherent picture
4. **Delegates detailed work** to specialized agents when needed

This prevents token bloat and keeps focus on high-level orchestration.

## Integration with Compliance-Dashboard

This skill feeds metrics directly to the Compliance-Dashboard skill:

- **Component migration data** → Tracks design system evolution
- **Quality metrics** → Informs code health scores
- **Test coverage** → Validates implementation reliability
- **Build status** → Assesses deployment stability

The result: comprehensive visibility into CareerCopilot's design system maturity.

## Configuration

No additional configuration required beyond standard Claude Desktop setup. The skill automatically discovers available MCP servers and coordinates across them.

## Output Format

Results are delivered as:

```json
{
  "orchestration_summary": {
    "timestamp": "2026-01-28T...",
    "overall_status": "green|yellow|red",
    "deployment_readiness": 0-100,
    "key_findings": [...]
  },
  "dimension_assessment": {
    "build_status": {...},
    "test_coverage": {...},
    "code_quality": {...},
    "migration_progress": {...}
  },
  "recommendations": [...]
}
```

## Automated Handover Mode

When invoked for autonomous task handoff to Gemini 3 Pro, orchestrator embeds compact, machine-readable handover data directly in output:

**Usage Pattern:**
```
use codebase-orchestrator to assess component migration and prepare handover for gemini-3-pro
```

**Embedded Handover Output:**
Adds `handover` key to standard JSON containing:
- Executable task array (prioritized, with dependencies)
- Token system references (paths only, no duplication)
- MCP transport hints (which servers needed)
- Recovery procedures (error handling, auto-revert rules)
- Progress checkpoints (reporting gates)

**Compact Format Example:**
```json
{
  "handover": {
    "v": "1.0",
    "target": "gemini-3-pro:mcp",
    "transport": {"fs": true, "git": true, "test": true},
    "budget_tokens": 2000,
    "tasks": [
      {
        "id": "cleanup_dupes",
        "type": "delete",
        "files": ["Pebble 2.tsx", "Stone 2.tsx", "Jar 2.tsx", ...],
        "cmd": "git rm {files}",
        "commit_msg": "chore: remove duplicate component files"
      },
      {
        "id": "migrate_lens",
        "type": "component_migration",
        "priority": 1,
        "component": "Lens",
        "file": "frontend/src/components/inputs/Lens.tsx",
        "blocking": "Core form input",
        "deps": ["token-system"],
        "transforms": {
          "M3Color": "ncColor.botanical",
          "fontFamily:Roboto": "ncFont.body",
          "elevation": "ncShadow.organic"
        },
        "test": "npm test -- --testPathPattern=Lens",
        "commit_msg": "refactor(components): migrate Lens to Northcote"
      }
    ],
    "refs": {
      "tokens": "frontend/src/design-tokens/northcote-tokens.ts",
      "examples": ["frontend/src/components/core/Pebble.tsx"]
    },
    "recovery": {
      "test_fail": "auto_revert",
      "token_missing": "halt_report",
      "import_error": "revert_check_deps"
    },
    "checkpoints": ["after_cleanup", "per_component", "final_audit"]
  }
}
```

**Token Efficiency:**
- Standard orchestrator output: ~1K tokens
- With embedded handover: ~3K tokens (+2K overhead)
- vs. separate handover documents: ~15K tokens
- **Total savings: 87% reduction**

**Workflow:**
1. Orchestrator generates assessment + embedded handover
2. Gemini 3 Pro receives output via MCP (Filesystem)
3. Parses `handover.tasks` array (machine-readable)
4. Executes tasks sequentially with embedded error recovery
5. Reports status at checkpoints (progress tracking)
6. No manual copy-paste, no separate documents needed

**Integration:**
Seamlessly coordinates with Compliance-Dashboard which prioritizes components by compliance impact, feeding results into handover task ordering.

## Examples of What This Skill Reveals

- "85% of components have migrated to Northcote naming conventions"
- "Test coverage is 92% but 3 critical paths uncovered"
- "Build passes but 2 peer dependencies need updating"
- "Component audit ready; 12 components awaiting visual validation"

## Limitations

- Requires git, filesystem, and testing MCPs to be configured
- Cannot execute changes; identifies work that needs doing
- Assessment is point-in-time; trends require multiple samples over time
- Delegates implementation details to IDE agents for execution

## Related Skills

- **Compliance-Dashboard**: Visual tracking of design system health metrics
- **Northcote-Visual-Audit**: Component visual validation (feeds into compliance tracking)
- **Component-Transformer**: Executes migrations identified by this skill

---

## Technical Notes

The skill is language-agnostic and works across:
- Python-based codebases
- TypeScript/JavaScript projects
- Mixed-language monorepos
- Multi-package structures

Token efficiency is achieved through:
- Single consolidated query to orchestrate multiple MCPs
- Batch processing to minimize round-trips
- Early termination when blocking issues identified
- Progressive detail only when needed for decision-making

---

*This skill is the foundation for understanding your codebase's state at scale. Use it before major decisions about deployment, migration, or design system evolution.*
