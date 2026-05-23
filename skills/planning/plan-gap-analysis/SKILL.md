---
name: plan-gap-analysis
description: Analyze gaps between implementation plans and actual codebase implementation for the Rust self-learning memory project
---

# Plan Gap Analysis

Analyze gaps between documented plans in `plans/` and actual implementation.

## Workflow

### Phase 1: Plan Inventory

Read all plan files:
- `00-overview.md` - Project summary and metrics
- `01-understand.md` - Requirements and components
- `02-plan.md` - Architecture decisions and roadmap
- `03-execute.md` - Implementation details
- `04-review.md` - Quality requirements
- `05-secure.md` - Security requirements
- `06-feedback-loop.md` - Refinements

### Phase 2: Codebase Inventory

```bash
# List all crates
find . -name "Cargo.toml" -not -path "*/target/*"

# List source files
find . -name "*.rs" -not -path "*/target/*"
```

**Crates to analyze**:
- `memory-core` - Core data structures and orchestration
- `memory-storage-turso` - Turso/libSQL backend
- `memory-storage-redb` - redb cache layer
- `memory-mcp` - MCP server and sandbox
- `test-utils` - Test utilities
- `benches` - Performance benchmarks

### Phase 3: Gap Identification

Check each phase:

| Phase | Focus Areas |
|-------|-------------|
| UNDERSTAND | Data structures, type definitions |
| PLAN | Architectural decisions, success metrics |
| EXECUTE | Storage, learning, MCP features |
| REVIEW | FR1-FR7, NFR1-NFR6 tests |
| SECURE | Attack surfaces, mitigations |
| FEEDBACK | Edge cases, optimizations |

### Phase 4: Prioritization

**Critical** (Blocks production):
- Security vulnerabilities
- Data corruption risks
- Missing core functionality

**High** (Affects quality):
- Performance targets not met
- Test coverage below target
- Missing error handling

**Medium** (Technical debt):
- Code quality issues
- Documentation gaps

### Phase 5: TODO Generation

```markdown
## Phase [N]: [NAME]

### Critical Priority
- [ ] [Component] - [Missing item]
  - File: path/to/file.rs
  - Plan: plans/0X-phase.md:LineNumber
  - Impact: [Description]
  - Effort: [Estimate]
```

## Output Format

```markdown
# Plan Gap Analysis Report
**Total Requirements**: X
**Implemented**: Y (Z%)
**Gaps Identified**: N

## By Phase
- Phase 1: X/Y complete
- Phase 2: X/Y complete
- ...

## Critical Gaps
1. [Gap] - Priority, Effort
```

## Best Practices

✓ Be systematic: Check every requirement
✓ Be specific: Reference exact file locations
✓ Be accurate: Verify, don't assume
✓ Be prioritized: Critical > High > Medium > Low
✓ Be actionable: Include file paths and estimates
