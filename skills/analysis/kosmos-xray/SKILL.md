---
name: kosmos-xray
description: Context-efficient codebase exploration using AST analysis. Use when exploring Kosmos architecture, understanding code structure, or preparing documentation for AI programmers. Triggers: xray, map structure, skeleton, interface, architecture, explore kosmos, warm start, token budget, context compression.
---

# Kosmos X-Ray Skill

Specialized tools for analyzing the Kosmos codebase efficiently within limited context windows. Uses AST parsing to extract structural information (classes, methods, signatures) without loading implementation details, achieving ~95% token reduction.

## Enhanced Features (v2)

The skeleton extractor now captures:
- **Pydantic/dataclass fields** - `name: str = Field(...)` visible in output
- **Decorators** - `@dataclass`, `@property`, `@tool` shown above definitions
- **Global constants** - `CONFIG_VAR = "value"` at module level
- **Line numbers** - Every definition includes `# L{line}` for navigation

**IMPORTANT**: Always use these features when exploring - they reveal data structures that would otherwise appear as empty `pass` statements.

## When to Use This Skill

- **Exploring the codebase** - Map directory structure before diving into files
- **Understanding architecture** - Extract class hierarchies and dependencies
- **Understanding data models** - Skeleton shows Pydantic fields that define the data
- **Onboarding** - Generate documentation for new AI programmers
- **Context management** - Identify large files that should use skeleton view instead of full read

## Core Tools

### 1. mapper.py - Directory Structure Map

Shows file tree with token estimates. Identifies context hazards (large files).

```bash
# Map entire project
python .claude/skills/kosmos-xray/scripts/mapper.py

# Map specific directory
python .claude/skills/kosmos-xray/scripts/mapper.py kosmos/workflow/

# Get summary only (no tree) - RECOMMENDED FIRST STEP
python .claude/skills/kosmos-xray/scripts/mapper.py --summary

# JSON output for parsing
python .claude/skills/kosmos-xray/scripts/mapper.py --json
```

### 2. skeleton.py - Interface Extraction (Enhanced)

Extracts Python file skeletons via AST. **Now shows Pydantic fields, decorators, constants, and line numbers.**

```bash
# Single file skeleton (includes line numbers by default)
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/workflow/research_loop.py

# Directory with pattern filter
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/ --pattern "**/base*.py"

# Filter by priority (critical, high, medium, low) - USE THIS FOR ONBOARDING
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/ --priority critical

# Include private methods (_method) for internal understanding
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/agents/ --private

# Omit line numbers if not needed
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/config.py --no-line-numbers

# JSON output for programmatic use
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/models/ --json
```

**What skeleton.py reveals:**
```python
# Before (old behavior): Data models appeared empty
class Hypothesis(BaseModel):
    pass

# After (enhanced): Full data structure visible
@dataclass
class PaperAnalysis:  # L34
    paper_id: str  # L36
    executive_summary: str  # L37
    confidence_score: float  # L42
```

### 3. dependency_graph.py - Import Analysis

Maps import relationships between modules. Identifies architectural layers and circular dependencies.

```bash
# Analyze dependencies (text output)
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/

# With root package name (recommended)
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --root kosmos

# Focus on specific area
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --focus workflow

# Generate Mermaid diagram for documentation - USE FOR WARM_START.md
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --root kosmos --mermaid

# Combined: Mermaid focused on workflow
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --root kosmos --mermaid --focus workflow

# JSON output
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --json
```

## Recommended Workflow (Use ALL Features)

1. **Survey first** - `mapper.py --summary` to see codebase size and large files
2. **X-ray critical classes** - `skeleton.py --priority critical` to see core interfaces WITH FIELDS
3. **Generate architecture diagram** - `dependency_graph.py --mermaid` for visual map
4. **Verify imports** - Run import checks before documenting entry points
5. **Read selectively** - Only read full implementation when skeleton isn't enough

## Best Practices

### DO:
- Always use `--priority critical` first to understand core architecture
- Use `--mermaid` output for documentation diagrams
- Check line numbers when you need to reference specific code
- Use `--private` when understanding internal agent behavior
- Verify imports before documenting them as entry points

### DON'T:
- Read full files when skeleton would suffice (wastes context)
- Ignore large file warnings from mapper.py
- Skip the Pydantic fields - they define the data contracts
- Forget to include line numbers in documentation references

## Integration with kosmos_architect Agent

This skill is automatically loaded by the `kosmos_architect` agent. You can also use it directly for targeted analysis.

```
# Use the agent for full onboarding documentation (uses ALL features)
@kosmos_architect generate

# Or use individual tools directly
@kosmos-xray Map the workflow directory
```

## Configuration Files

- `configs/ignore_patterns.json` - Directories and files to skip
- `configs/priority_modules.json` - Module priority levels and patterns

## Context Budget Guidelines

| Operation | Typical Tokens | Use When |
|-----------|---------------|----------|
| mapper.py --summary | ~500 | First exploration |
| mapper.py full | ~2-5K | Understanding structure |
| skeleton.py (1 file) | ~200-500 | Understanding interface |
| skeleton.py --priority critical | ~5K | Core architecture |
| dependency_graph.py text | ~2-3K | Architecture analysis |
| dependency_graph.py --mermaid | ~500 | Documentation diagrams |
| Full file read | Varies | Need implementation details |

For detailed API documentation, see [reference.md](reference.md).
For quick command reference, see [CHEATSHEET.md](CHEATSHEET.md).
