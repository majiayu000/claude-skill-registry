---
name: skill-researcher
description: Conduct general research using web search, documentation, and codebase exploration. Invoke for non-Lean research tasks.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
context:
  - core/formats/report-format.md
  - core/standards/documentation.md
  - core/workflows/status-transitions.md
---

# Researcher Skill

General-purpose research agent for non-Lean tasks.

## Trigger Conditions

This skill activates when:
- Task language is "general", "meta", or "markdown"
- Research is needed for implementation planning
- Documentation or external resources need to be gathered

## Research Strategy

### 1. Codebase Research

Search the local codebase for:
- Similar implementations
- Related patterns
- Existing utilities to leverage
- Integration points

Tools: `Glob`, `Grep`, `Read`

### 2. Web Research

Search for external resources:
- Official documentation
- Best practices
- Tutorials and examples
- Stack Overflow solutions

Tools: `WebSearch`, `WebFetch`

### 3. Documentation Research

Find relevant project documentation:
- README files
- Architecture docs
- API specifications
- Change logs

Tools: `Glob`, `Read`

## Execution Flow

```
1. Receive task context (description, focus_prompt)
2. Identify key concepts and search terms
3. Search codebase for related code
4. Search web for documentation/examples
5. Analyze findings and identify patterns
6. Synthesize recommendations
7. Create research report
8. Return results
```

## Research Report Format

Create report at `.claude/specs/{N}_{SLUG}/reports/research-{NNN}.md`:

```markdown
# Research Report: Task #{N}

**Task**: {title}
**Date**: {date}
**Focus**: {focus_prompt}

## Summary

{2-3 sentence overview}

## Codebase Findings

### Related Files
- `path/to/file.ext` - {relevance}

### Existing Patterns
{Description of patterns found}

## External Resources

### Documentation
- {Link} - {summary}

### Examples
- {Link} - {summary}

## Recommendations

1. {Approach recommendation}
2. {Key consideration}

## Next Steps

{Suggested actions}
```

## Return Format

```json
{
  "status": "completed",
  "summary": "Research completed with N findings",
  "artifacts": [
    {
      "path": ".claude/specs/{N}_{SLUG}/reports/research-001.md",
      "type": "research",
      "description": "Research report"
    }
  ],
  "key_findings": [
    "Finding 1",
    "Finding 2"
  ],
  "recommendations": [
    "Recommendation 1"
  ]
}
```
