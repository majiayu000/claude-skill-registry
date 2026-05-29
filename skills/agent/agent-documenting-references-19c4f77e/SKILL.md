---
name: agent-documenting-references
description: Standardized reference documentation section structure for agents - project guidance, conventions, related agents, and Skills. Use when implementing or updating agent documentation.
created: 2026-01-05
updated: 2026-01-05
---

# Documenting Agent References

Standard structure for "Reference Documentation" sections in agent files to ensure consistent navigation and discoverability.

## When This Skill Loads

This Skill auto-loads when implementing agents or updating agent documentation sections.

## Reference Documentation Section

All agents SHOULD include a "Reference Documentation" section near the end (before any appendices) with standardized subsections.

### Section Template

```markdown
## Reference Documentation

**Project Guidance**:

- [CLAUDE.md](../../CLAUDE.md) - Primary guidance for Claude Code
- [Agent-specific convention](path/to/convention.md) - Domain-specific standards

**Related Agents**:

- `maker-agent` - Creates content for this domain
- `checker-agent` - Validates content (upstream dependency)
- `fixer-agent` - Fixes issues found by checker
- `related-domain-agent` - Related functionality

**Related Conventions**:

- [Primary Convention](path/to/convention.md) - Main standards this agent implements
- [Secondary Convention](path/to/convention.md) - Additional relevant standards

**Skills**:

- `primary-skill` - Main Skill for domain knowledge
- `wow-assessing-criticality-confidence` - Criticality assessment (if applicable)
- `wow-generating-validation-reports` - Report generation (if applicable)
```

### Subsection Details

#### Project Guidance

**Purpose**: Link to primary project instructions and domain-specific conventions.

**Always Include**:

- CLAUDE.md (primary guidance for all agents)

**Conditionally Include**:

- Domain-specific conventions (e.g., README Quality Convention for readme-agents)
- Framework-specific guidance (e.g., Hextra guide for ayokoding-web-agents)
- Special standards relevant to agent's scope

**Pattern**:

```markdown
**Project Guidance**:

- [CLAUDE.md](../../CLAUDE.md) - Primary guidance
- [Specific Convention](path/to/convention.md) - Domain standards
```

#### Related Agents

**Purpose**: Help users understand agent ecosystem and workflow relationships.

**Include**:

- **Upstream agents**: Agents this agent depends on (e.g., checker for fixer)
- **Downstream agents**: Agents that depend on this one (e.g., fixer for checker)
- **Parallel agents**: Agents in same family/domain (e.g., other checkers)
- **Complementary agents**: Agents with related functionality

**Organize by Relationship**:

```markdown
**Related Agents**:

- `upstream-agent` - Description of relationship
- `downstream-agent` - Description of relationship
- `parallel-agent` - Description of functionality
```

**Examples by Agent Type**:

**Maker Agents**:

```markdown
- `checker-agent` - Validates content created by this maker
- `related-maker` - Creates content in related domain
```

**Checker Agents**:

```markdown
- `maker-agent` - Creates content this checker validates
- `fixer-agent` - Fixes issues found by this checker
- `related-checker` - Validates related aspects
```

**Fixer Agents**:

```markdown
- `checker-agent` - Generates audit reports this fixer processes
- `maker-agent` - Updates content after fixes applied
```

#### Related Conventions

**Purpose**: Link to conventions and development practices the agent implements.

**Include**:

- Primary convention agent implements
- Secondary conventions relevant to agent's scope
- Development practices agent follows (e.g., AI Agents Convention)
- Standards agent enforces (for checkers)

**Pattern**:

```markdown
**Related Conventions**:

- [Primary Convention](path/to/convention.md) - Main standards
- [Secondary Convention](path/to/convention.md) - Additional standards
- [Development Practice](path/to/practice.md) - Implementation guidance
```

**Checkers Should List**:

- Conventions they validate against
- Quality standards they enforce

**Makers Should List**:

- Conventions they follow when creating content
- Formatting standards they apply

#### Skills

**Purpose**: Reference Skills the agent uses for domain knowledge and patterns.

**Include**:

- All Skills listed in agent's `skills:` frontmatter field
- Skills should be listed without path (just skill name)
- Brief description of what each Skill provides

**Pattern**:

```markdown
**Skills**:

- `domain-skill` - Domain-specific knowledge
- `wow-skill` - Cross-cutting pattern or workflow
- `agent-skill` - Agent development guidance
```

**Note**: Skills section duplicates frontmatter `skills:` field for documentation visibility.

## Placement in Agent Files

**Recommended Location**: Near end of agent file, before any appendices or examples.

**Typical Structure**:

```markdown
# Agent Name

[Agent description]

## Core Responsibility

[What agent does]

## Main Content Sections

[Detailed agent instructions]

## Reference Documentation

[Reference sections using template above]

## Appendices (Optional)

[Additional examples, edge cases, etc.]
```

## Examples by Agent Family

### docs-family Agents

```markdown
## Reference Documentation

**Project Guidance**:

- [CLAUDE.md](../../CLAUDE.md) - Primary guidance
- [Content Quality Principles](../../docs/explanation/rules/conventions/content/ex-ru-co-co__quality.md)
- [Diátaxis Framework](../../docs/explanation/rules/conventions/meta/ex-ru-co-me__diataxis-framework.md)

**Related Agents**:

- `docs-maker` - Creates documentation
- `docs-checker` - Validates documentation
- `docs-fixer` - Fixes documentation issues
- `docs-tutorial-checker` - Specialized tutorial validation

**Related Conventions**:

- [Content Quality Principles](../../docs/explanation/rules/conventions/content/ex-ru-co-co__quality.md)
- [Factual Validation Convention](../../docs/explanation/rules/conventions/content/ex-ru-co-co__factual-validation.md)
- [Linking Convention](../../docs/explanation/rules/conventions/formatting/ex-ru-co-fo__linking.md)

**Skills**:

- `docs-applying-content-quality` - Content quality standards
- `docs-validating-factual-accuracy` - Fact-checking methodology
- `wow-assessing-criticality-confidence` - Criticality assessment
- `wow-generating-validation-reports` - Report generation
```

### readme-family Agents

```markdown
## Reference Documentation

**Project Guidance**:

- [CLAUDE.md](../../CLAUDE.md) - Primary guidance
- [README Quality Convention](../../docs/explanation/rules/conventions/content/ex-ru-co-co__readme-quality.md)

**Related Agents**:

- `readme-maker` - Creates README content
- `readme-checker` - Validates README quality
- `readme-fixer` - Fixes README issues
- `docs-checker` - Validates other documentation

**Related Conventions**:

- [README Quality Convention](../../docs/explanation/rules/conventions/content/ex-ru-co-co__readme-quality.md)
- [Content Quality Principles](../../docs/explanation/rules/conventions/content/ex-ru-co-co__quality.md)

**Skills**:

- `readme-writing-readme-files` - README-specific standards
- `wow-assessing-criticality-confidence` - Criticality assessment
- `wow-generating-validation-reports` - Report generation
```

### plan-family Agents

```markdown
## Reference Documentation

**Project Guidance**:

- [CLAUDE.md](../../CLAUDE.md) - Primary guidance
- [Plans Organization Convention](../../docs/explanation/rules/conventions/project/ex-ru-co-pr__plans-organization.md)

**Related Agents**:

- `plan-maker` - Creates project plans
- `plan-checker` - Validates plan quality
- `plan-executor` - Executes plans
- `plan-execution-checker` - Validates completed work
- `plan-fixer` - Fixes plan issues

**Related Conventions**:

- [Plans Organization Convention](../../docs/explanation/rules/conventions/project/ex-ru-co-pr__plans-organization.md)
- [Gherkin Acceptance Criteria](../../docs/explanation/rules/development/infra/ex-ru-de-in__acceptance-criteria.md)

**Skills**:

- `plan-creating-project-plans` - Plan structure and organization
- `plan-writing-gherkin-criteria` - Acceptance criteria patterns
- `wow-assessing-criticality-confidence` - Criticality assessment
```

## Benefits of Standardization

✅ **Improved Discoverability**: Users can quickly find related agents and conventions  
✅ **Consistent Navigation**: Same structure across all agents  
✅ **Clear Relationships**: Understand agent dependencies and workflows  
✅ **Better Maintainability**: Easy to update references across agents  
✅ **Enhanced Documentation**: Skills and conventions properly referenced

## Best Practices

1. **Keep Links Current**: Update when conventions move or rename
2. **Be Selective**: Only include truly relevant references
3. **Describe Relationships**: Explain how related agents connect
4. **Match Frontmatter**: Ensure Skills section matches `skills:` field
5. **Use Relative Paths**: Make links work from agent file location
6. **Group Logically**: Keep subsections organized and scannable

## Key Takeaways

- **Standard structure**: Use consistent subsections across all agents
- **Four subsections**: Project Guidance, Related Agents, Related Conventions, Skills
- **Clear relationships**: Help users understand agent ecosystem
- **Proper placement**: Near end of agent file before appendices
- **Keep current**: Update references when files move or change
- **Match frontmatter**: Skills section mirrors `skills:` field

This standardization improves agent documentation consistency and helps users navigate the agent ecosystem effectively.
