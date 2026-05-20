---
name: repomix
description: (ePost) Use when you need a full codebase overview, repo summary, or are unfamiliar with a repository structure

metadata:
  agent-affinity: [epost-researcher, epost-planner]
  keywords: [repomix, codebase, summary, analysis, repo, overview]
  platforms: [all]
  triggers: ["repomix", "codebase summary", "repo overview"]
---

# Repomix Skill

## Purpose
Generate comprehensive codebase summaries for analysis and understanding.

## When Active
User needs codebase overview, unfamiliar with repo structure, preparing for full analysis.

## Expertise

### Usage

#### Local Project
```bash
repomix
# Output: repomix-output.xml
```

#### Remote Repository
```bash
repomix --remote https://github.com/owner/repo
```

#### With Configuration
Create `.repomixignore` to exclude files (same syntax as .gitignore).

### Common Patterns
- Generate summary before full codebase review
- Create `docs/codebase-summary.md` from repomix output
- Check freshness: if summary >2 days old, regenerate
- Use for unfamiliar codebases or onboarding

### Output Analysis
- Extract file structure and size metrics
- Identify key entry points
- Understand module organization
- Find documentation files
- Note configuration files

## Patterns

### Integration with Other Skills
- **With Code Review**: Use summary to understand scope
- **With Debugging**: Use for context before deep dive
- **With Documentation**: Extract codebase structure for docs
- **With Planning**: Use to assess complexity

## Best Practices
- Generate fresh summary at project start
- Include summary in onboarding docs
- Update when major restructuring happens
- Use with .repomixignore for large monorepos
- Reference summary in documentation
- Cross-check with actual repo structure

### Related Skills
- `knowledge-retrieval` — Internal-first knowledge search protocol
- `docs-seeker` — External documentation lookup (Context7, WebSearch)
