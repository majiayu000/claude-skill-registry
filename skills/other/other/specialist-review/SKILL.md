---
name: specialist-review
description: Conducts a focused review from ONE specific specialist's perspective (e.g., Security Specialist, Performance Expert). Use when the user requests "Ask [specialist role] to review [target]", "Get [specialist]'s opinion on [topic]", "Have [role] review [code/component]", or when they want deep expertise in ONE specific domain. Do NOT use for comprehensive multi-perspective reviews (use architecture-review instead) or for listing available specialists (use list-members instead).
allowed-tools: Read,Write,Glob,Grep
---

# Specialist Review

Conducts focused reviews from a specific specialist's perspective.

## Overview

This skill performs a deep-dive review from one specialist's expertise:
1. Parses which specialist and what target to review
2. Loads or creates the specialist in the team
3. Analyzes the target from that specialist's unique lens
4. Conducts expert-level review with specific findings
5. Generates detailed review document
6. Reports key findings and recommendations

**Specialist guidance**: [references/specialist-perspectives.md](references/specialist-perspectives.md)
**Review template**: [assets/specialist-review-template.md](assets/specialist-review-template.md)

## High-Level Workflow

### 1. Parse Request

Extract from user request:
- **Specialist role**: Which expert? (e.g., "Security Specialist", "Performance Expert")
- **Target**: What to review? (e.g., "API authentication", "database queries")

**Input validation**: Apply sanitization from `_patterns.md`:
- Specialist role: Alphanumeric + spaces/hyphens only, convert to kebab-case for filename
- Target: Remove dangerous characters, convert to kebab-case
- Combined filename length: max 100 characters

**Examples**:
- "Security Specialist" + "API authentication" → `security-specialist-api-authentication.md`
- "Ruby Expert" + "ActiveRecord models" → `ruby-expert-activerecord-models.md`

### 2. Load or Create Specialist

Check `.architecture/members.yml` for the requested specialist.

**If exists**: Load their profile (specialties, disciplines, domains, perspective)

**If doesn't exist**: Create new member and add to `members.yml`:
```yaml
- id: [specialist_id]
  name: "[Person Name]"
  title: "[Specialist Title]"
  specialties: ["[Specialty 1]", "[Specialty 2]", "[Specialty 3]"]
  disciplines: ["[Discipline 1]", "[Discipline 2]"]
  skillsets: ["[Skill 1]", "[Skill 2]"]
  domains: ["[Domain 1]", "[Domain 2]"]
  perspective: "[Their unique viewpoint]"
```

Inform user: "I've added [Name] ([Title]) to your architecture team."

**Specialist guidance**: See [references/specialist-perspectives.md § Creating New Specialists](references/specialist-perspectives.md#creating-new-specialists)

### 3. Analyze Target

Use available tools to examine the target:
- `Glob` to find relevant files
- `Grep` to search for patterns
- `Read` to examine code, configs, documentation

**Understand**:
- Current implementation
- Dependencies and context
- Related ADRs or documentation
- Patterns being used

### 4. Conduct Expert Review

Adopt the specialist's persona and expertise. Apply their unique lens.

**Review from specialist's perspective**:
- Focus on their domain of expertise (security, performance, maintainability, etc.)
- Provide expert-level insights, not surface-level comments
- Reference specific files, line numbers, and code
- Explain impact and provide actionable fixes

**Review structure** (for each specialist):
- Specialist perspective and focus
- Executive summary with assessment
- Current implementation description
- Strengths identified
- Concerns with severity and specific fixes
- Recommendations (immediate, short-term, long-term)
- Best practices and industry standards
- Code examples showing issues and improvements
- Risks if not addressed
- Success metrics

**Detailed guidance by specialist**: [references/specialist-perspectives.md § Core Specialists](references/specialist-perspectives.md#core-specialists)

**Review template**: Load and fill [assets/specialist-review-template.md](assets/specialist-review-template.md)

### 5. Create Review Document

Load the template:
```bash
cat .claude/skills/specialist-review/assets/specialist-review-template.md
```

Fill in all sections with detailed, specific findings.

**Save to**: `.architecture/reviews/[specialist-role]-[target].md`

**Format**: `[role-kebab-case]-[target-kebab-case].md`

### 6. Report to User

Provide concise summary:

```
[Specialist Title] Review Complete: [Target]

Reviewer: [Specialist Name]
Location: .architecture/reviews/[filename].md
Assessment: [Overall assessment]

Key Findings:
1. [Most important finding]
2. [Second finding]
3. [Third finding]

Priority Actions:
1. [Critical action 1]
2. [Critical action 2]

Critical Issues: [Count]
High Priority: [Count]
Total Recommendations: [Count]

Next Steps:
- Address critical issues immediately
- Review detailed findings in document
- [Specific next action based on findings]
```

## Specialist Quick Reference

**Core Specialists** (see [references/specialist-perspectives.md](references/specialist-perspectives.md)):
- **Security Specialist**: Authentication, authorization, vulnerabilities, OWASP
- **Performance Specialist**: Query optimization, caching, bottlenecks, scalability
- **Domain Expert**: Business logic, domain models, ubiquitous language
- **Maintainability Expert**: Code quality, technical debt, testability
- **Systems Architect**: Architecture patterns, component interaction, coherence
- **AI Engineer**: LLM integration, agent orchestration, evaluation

**Technology Specialists**:
- **JavaScript/Python/Ruby/Go/Rust Expert**: Language-specific best practices
- **Framework Specialists**: React, Rails, Django, Spring, etc.

**Creating new specialists**: Automatically added to team when requested

## Related Skills

**Before Specialist Review**:
- `list-members` - See available specialists
- `architecture-status` - Check if area previously reviewed

**After Specialist Review**:
- `create-adr` - Document decisions from findings
- `architecture-review` - Include in comprehensive review
- Request another specialist for different domain perspective

**Workflow Examples**:
1. Security review → Finds auth issue → Create ADR → Performance review
2. Ruby Expert review → Rails-specific guidance → Implement → Follow-up review
3. Full architecture review → Deep-dive with specialists on concerns

## Quality Guidelines

**Excellent specialist reviews**:
- Stay laser-focused within domain
- Provide expert-level, not generic, insights
- Reference exact files and line numbers
- Include code examples (current vs recommended)
- Explain "why", not just "what"
- Consider context and constraints
- Provide actionable, implementable advice
- Estimate effort for each recommendation

**Avoid**:
- Straying outside specialist's domain
- Vague or surface-level comments
- Missing specific locations
- Recommendations without implementation guidance

## Documentation

- **Specialist guidance**: [references/specialist-perspectives.md](references/specialist-perspectives.md)
- **Review template**: [assets/specialist-review-template.md](assets/specialist-review-template.md)
- **Common patterns**: [../_patterns.md](../_patterns.md)
