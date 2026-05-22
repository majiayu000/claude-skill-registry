---
name: architecture-review
description: Conducts a comprehensive multi-perspective architecture review using ALL architecture team members. Use when the user requests "Start architecture review", "Full architecture review", "Review architecture for version X.Y.Z", "Conduct comprehensive review", or when they want assessment from multiple perspectives. Do NOT use for single-specialist reviews (use specialist-review instead) or for status checks (use architecture-status instead).
allowed-tools: Read,Write,Glob,Grep,Bash(git:*)
---

# Architecture Review

Conducts comprehensive multi-perspective architecture reviews with all team members.

## Process Overview

1. **Determine Scope** - Identify what to review (version, feature, or component)
2. **Load Team** - Read members from `.architecture/members.yml` and check pragmatic mode
3. **Analyze System** - Examine architecture using Read, Glob, Grep, and git tools
4. **Individual Reviews** - Each member reviews from their specialized perspective
5. **Collaborative Discussion** - Synthesize findings and establish priorities
6. **Create Document** - Generate comprehensive review using template
7. **Report Results** - Summarize findings and next steps for user

**Detailed guidance**: [references/review-process.md](references/review-process.md)

## Workflow Steps

### 1. Determine Scope

Identify review target and create filename:
- **Version**: "version X.Y.Z" → `X-Y-Z.md`
- **Feature**: "feature name" → `feature-kebab-case.md`
- **Component**: "component name" → `component-kebab-case.md`

Apply input validation (see `_patterns.md` § Filename Sanitization).

### 2. Load Configuration and Team

```bash
cat .architecture/config.yml     # Check pragmatic_mode.enabled
cat .architecture/members.yml    # Load all members
```

Include Pragmatic Enforcer if pragmatic mode enabled for reviews.

### 3. Analyze the Target

Use available tools to examine the system:
- `Read` - Code, configs, documentation
- `Glob` - Find files by pattern
- `Grep` - Search for specific patterns
- `Bash(git:*)` - Git history and status

Focus based on review type:
- **Version**: Overall architecture, components, patterns, technical debt
- **Feature**: Implementation, integration, security, performance
- **Component**: Structure, dependencies, boundaries, interfaces

### 4. Conduct Individual Member Reviews

For each member in `members.yml`, write a review including:
- Perspective statement
- Key observations (3-5)
- Strengths (3-5)
- Concerns with impact and recommendations (3-7)
- Prioritized recommendations with effort estimates (3-7)

**Format details**: [references/review-process.md § Individual Member Review Format](references/review-process.md#individual-member-review-format)

**Pragmatic integration**: If enabled, add pragmatic analysis after each member. See [references/pragmatic-integration.md](references/pragmatic-integration.md)

### 5. Facilitate Collaborative Discussion

Synthesize findings:
- Identify common concerns
- Discuss disagreements
- Establish consensus
- Prioritize: Critical (0-2 weeks) | Important (2-8 weeks) | Nice-to-Have (2-6 months)

**Discussion format**: [references/review-process.md § Collaborative Discussion](references/review-process.md#collaborative-discussion-process)

### 6. Create Review Document

Load template and fill in all sections:
```bash
cat .claude/skills/architecture-review/assets/review-template.md
```

Include:
- Executive summary and overall assessment
- Individual member reviews
- Collaborative discussion
- Consolidated findings (strengths, improvements, debt, risks)
- Recommendations (immediate, short-term, long-term)
- Success metrics and follow-up plan

Save to `.architecture/reviews/[filename].md`

**Template**: [assets/review-template.md](assets/review-template.md)

### 7. Report to User

```
Architecture Review Complete: [Target]

Location: .architecture/reviews/[filename].md
Overall Assessment: [Strong | Adequate | Needs Improvement]

Top 3 Priorities:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

Immediate Actions:
- [Action 1]
- [Action 2]

Next Steps:
- Review with team
- "Start architecture recalibration for [target]"
- Create ADRs for key decisions
```

## Related Skills

**Before**: `architecture-status`, `list-members`
**During**: `specialist-review`, `create-adr`
**After**: `architecture-recalibration`, `create-adr`

## Documentation

- **Process guide**: [references/review-process.md](references/review-process.md)
- **Pragmatic mode**: [references/pragmatic-integration.md](references/pragmatic-integration.md)
- **Template**: [assets/review-template.md](assets/review-template.md)
- **Patterns**: [../_patterns.md](../_patterns.md)
