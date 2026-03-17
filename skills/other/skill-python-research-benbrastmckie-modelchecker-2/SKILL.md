---
name: skill-python-research
description: Research Python/Z3 patterns and APIs for semantic theory development. Invoke for Python-language research tasks.
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Bash(python *)
context: fork
---

# Python Research Skill

Specialized research agent for Python/Z3 semantic theory development tasks.

## Trigger Conditions

This skill activates when:
- Task language is "python"
- Research involves Z3, semantic theories, or model checking
- Codebase exploration is needed

## Research Strategies

### 1. Local Codebase First

Always check existing code first:
```
1. Grep for relevant patterns
2. Glob for similar files
3. Read existing implementations
4. Understand existing patterns before proposing new ones
```

### 2. Z3 API Research

For Z3-specific patterns:
```
1. WebSearch "z3 python {concept}"
2. WebFetch Z3 documentation
3. Check existing z3_helpers.py
4. Test patterns with Bash(python -c "...")
```

### 3. Theory Pattern Research

For semantic theory patterns:
```
1. Read existing theories (logos, exclusion, imposition, bimodal)
2. Identify common patterns
3. Check theory_lib/__init__.py for registration
4. Review theory-specific tests
```

## Research Areas

### Z3 Patterns
- Solver configuration and optimization
- Constraint generation patterns
- Model extraction and interpretation
- Incremental solving
- Timeout handling

### Theory Development
- SemanticDefaults extension patterns
- Operator definition and registration
- Example creation patterns
- Iteration support

### Testing Patterns
- pytest fixtures for Z3
- Theory validation testing
- Model iteration testing
- Performance benchmarking

### Codebase Conventions
- Import patterns (relative vs absolute)
- Type hinting standards
- Documentation requirements
- Error handling patterns

## Execution Flow

```
1. Receive task context (description, focus)
2. Extract key concepts (Z3 features, theory patterns, testing)
3. Search local codebase for related code
4. Search web for Z3/Python documentation if needed
5. Validate patterns with quick Python tests
6. Analyze implementation approaches
7. Create research report
8. Return results
```

## Research Report Format

```markdown
# Python Research Report: Task #{N}

**Task**: {title}
**Date**: {date}
**Focus**: {focus}

## Summary

{Overview of findings}

## Codebase Findings

### Related Files
- `path/to/file.py` - {description}

### Existing Patterns
```python
# Pattern name
def example():
    ...
```

### Similar Implementations
- {Description of similar code}

## Z3 API Findings

### Relevant APIs
| API | Purpose | Example |
|-----|---------|---------|
| `z3.Solver()` | {purpose} | {code} |

### Best Practices
- {Practice and rationale}

## Recommended Approach

1. {Step 1 with specific patterns to use}
2. {Step 2}

## Code Sketch

```python
# Proposed implementation approach
class NewFeature:
    ...
```

## Testing Strategy

- Unit tests: {approach}
- Integration tests: {approach}

## Potential Challenges

- {Challenge and mitigation}

## References

- {Documentation links}
- {Related codebase files}
```

## Return Format

```json
{
  "status": "completed",
  "summary": "Found N relevant patterns for implementation",
  "artifacts": [
    {
      "path": ".claude/specs/{N}_{SLUG}/reports/research-001.md",
      "type": "research",
      "description": "Python/Z3 research report"
    }
  ],
  "patterns_found": [
    {"name": "Pattern.name", "location": "file.py", "relevance": "high"}
  ],
  "z3_apis_needed": [
    "z3.Solver", "z3.Bool"
  ],
  "recommended_approach": "Description of recommended approach"
}
```

## Quick Validation Commands

```bash
# Test Z3 pattern
PYTHONPATH=Code/src python -c "
import z3
s = z3.Solver()
x = z3.Bool('x')
s.add(x)
print(s.check())
"

# Test import
PYTHONPATH=Code/src python -c "from model_checker import ..."

# Check theory structure
ls Code/src/model_checker/theory_lib/logos/
```

## Key Codebase Locations

- **Theory base**: `Code/src/model_checker/theory_lib/`
- **Model structure**: `Code/src/model_checker/models/`
- **Z3 helpers**: `Code/src/model_checker/utils/z3_helpers.py`
- **Testing utils**: `Code/src/model_checker/utils/testing.py`
- **Standards docs**: `Code/docs/core/`
