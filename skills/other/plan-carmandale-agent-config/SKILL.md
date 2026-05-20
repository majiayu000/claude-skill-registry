---
name: plan
description: Transform feature descriptions, bug reports, or improvement ideas into well-structured project plans. Use when starting new work, creating issues, or needing to research a codebase before implementation. Includes repository research, pattern analysis, and structured plan generation.
---

# Plan Skill

Transform feature descriptions into actionable, well-researched project plans.

## When to Use

- Starting a new feature or bug fix
- Need to understand a codebase before implementing
- Creating structured issues or specs
- Research existing patterns before adding new code

## Workflow Overview

```
Feature Description
        │
        ▼
┌───────────────────┐
│  1. RESEARCH      │  ← Analyze repo, patterns, docs
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  2. STRUCTURE     │  ← Choose detail level, outline plan
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  3. WRITE         │  ← Generate plan file
└─────────┬─────────┘
          │
          ▼
    plans/<title>.md
```

---

## Phase 1: Research

Before planning, understand the codebase thoroughly.

### 1.1 Repository Structure Analysis

```bash
# Find key documentation
find . -maxdepth 2 -name "*.md" -type f 2>/dev/null | head -20

# Check for architecture docs
cat ARCHITECTURE.md README.md CONTRIBUTING.md CLAUDE.md AGENTS.md 2>/dev/null | head -100

# Understand directory structure
ls -la
find . -type d -maxdepth 2 | grep -v node_modules | grep -v .git | head -30
```

### 1.2 Pattern Discovery

Search for similar implementations:

```bash
# Find similar features (adjust pattern to match feature type)
rg -l "similar_keyword" --type-add 'code:*.{rb,py,ts,js,swift}' -t code

# Check for service objects, controllers, models (Rails)
ls app/services/ app/controllers/ app/models/ 2>/dev/null

# Check for existing patterns
rg "class.*Service" --type ruby -l 2>/dev/null
rg "interface.*Props" --type ts -l 2>/dev/null
```

### 1.3 Framework Documentation Research

**For Rails projects:**
```bash
# Check Gemfile for key dependencies
cat Gemfile | rg "gem ['\"]" | head -20

# Find configuration patterns
ls config/initializers/ 2>/dev/null
```

**For TypeScript/Node projects:**
```bash
# Check package.json dependencies
cat package.json | jq '.dependencies, .devDependencies' 2>/dev/null

# Find config files
ls *.config.* tsconfig.json 2>/dev/null
```

### 1.4 Git History Analysis

```bash
# Recent changes in relevant areas
git log --oneline -20 -- "path/to/relevant/dir"

# Who knows this code best?
git shortlog -sn -- "path/to/relevant/dir" | head -5

# Related PRs/issues
git log --oneline --grep="keyword" -10
```

### 1.5 Best Practices Check

Look for project conventions:

```bash
# Check for linting/formatting config
ls .eslintrc* .prettierrc* .rubocop* .editorconfig 2>/dev/null

# Check for testing patterns
ls -la test/ spec/ __tests__/ 2>/dev/null
find . -name "*_test.*" -o -name "*.test.*" -o -name "*_spec.*" | head -10
```

---

## Phase 2: Structure the Plan

### Choose Detail Level

**MINIMAL** - Simple bugs, small improvements, clear features
- Problem statement
- Acceptance criteria
- Essential context only

**STANDARD** - Most features, complex bugs
- Overview + motivation
- Technical considerations
- Detailed acceptance criteria
- Success metrics
- Dependencies & risks

**COMPREHENSIVE** - Major features, architectural changes
- Everything above plus:
- Implementation phases
- Alternative approaches considered
- Resource requirements
- Risk mitigation strategies

### Plan Template (STANDARD)

```markdown
# [Feature Title]

## Overview
[1-2 paragraph description of what this feature does and why it matters]

## Problem Statement
[What problem does this solve? Who is affected?]

## Research Findings

### Existing Patterns
- [Pattern 1]: `path/to/file.ext:line` - [description]
- [Pattern 2]: `path/to/file.ext:line` - [description]

### Dependencies
- [Dependency 1]: [how it's relevant]
- [Dependency 2]: [how it's relevant]

### Constraints
- [Constraint 1]
- [Constraint 2]

## Proposed Solution

### Approach
[High-level technical approach]

### Files to Create/Modify
- [ ] `path/to/new/file.ext` - [purpose]
- [ ] `path/to/existing/file.ext` - [changes needed]

### Implementation Steps
1. [ ] [First step]
2. [ ] [Second step]
3. [ ] [Third step]

## Technical Considerations

### Architecture Impact
[How does this fit into existing architecture?]

### Performance
[Any performance considerations?]

### Security
[Any security considerations?]

## Acceptance Criteria
- [ ] [Criterion 1 - specific, testable]
- [ ] [Criterion 2 - specific, testable]
- [ ] [Criterion 3 - specific, testable]

## Testing Strategy
- [ ] Unit tests for [component]
- [ ] Integration tests for [flow]
- [ ] Manual testing: [what to verify]

## Success Metrics
[How do we know this is successful?]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## References
- Similar implementation: `path/to/file.ext`
- Documentation: [URL]
- Related issue: #[number]
```

---

## Phase 3: Write the Plan

### Output Location

Write plans to `plans/` directory:

```bash
mkdir -p plans
```

Filename format: `plans/YYYY-MM-DD-<kebab-case-title>.md`

Example: `plans/2025-01-15-user-authentication-flow.md`

### Quality Checklist

Before finalizing the plan:

- [ ] Problem is clearly stated
- [ ] Research findings include specific file paths
- [ ] Implementation steps are actionable
- [ ] Acceptance criteria are testable
- [ ] All file references exist and are accurate
- [ ] Dependencies are identified
- [ ] Open questions are captured

---

## Research Perspectives

When researching, adopt these analytical lenses:

### Repository Analyst Perspective
- What's the project structure and organization?
- What patterns does this codebase use?
- What are the naming conventions?
- Where do similar features live?

### Best Practices Perspective
- What does the framework recommend?
- What do the project's linting rules enforce?
- What testing patterns are established?
- What documentation standards exist?

### Framework Documentation Perspective
- What APIs are available for this feature?
- What's the recommended approach in the official docs?
- Are there any deprecation warnings to consider?
- What version-specific considerations exist?

### Git History Perspective
- How have similar features been implemented?
- Who are the domain experts for this area?
- What problems have occurred in this area before?
- Are there related PRs or issues?

---

## Integration with Beads

If using beads for issue tracking:

```bash
# Create a bead for this plan
bd create --title="feat: <title>" --type=feature --priority=2

# Link plan to bead
# Add bead ID to plan header
```

---

## After Planning

Once the plan is written, options:

1. **Review the plan**: `/review plans/<filename>.md`
2. **Start work**: `/work plans/<filename>.md`
3. **Create issue**: Copy plan to GitHub/Linear issue
4. **Refine**: Edit the plan based on feedback

---

## Tips

- **Be specific**: Include file paths with line numbers when referencing code
- **Be honest**: Note what you don't know in "Open Questions"
- **Be practical**: Plans should be implementable, not theoretical
- **Be concise**: More detail ≠ better plan
- **Reference existing code**: The best patterns are already in the codebase
