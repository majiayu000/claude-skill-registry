---
name: agent-skill-creator
description: Creates new agent skills following modern best practices with proper structure and documentation. Use when asked to build a new skill, organize skill resources, design skill descriptions, or validate skill structure for portability across Copilot platforms.
---

# Agent Skill Creator

Foundational skill for designing and creating composable, portable agent skills that follow modern best practices.

## When to Use This Skill

Use this skill when you need to:
- Create a new agent skill for specialized workflows
- Design a skill description that properly activates in Copilot
- Organize resources (scripts, documentation, templates) for a skill
- Understand skill design principles (consolidation, composability, evaluability)
- Create tech-specific skills (.NET, TypeScript, Python, etc.)
- Validate skill structure for cross-platform compatibility

## Important: Foundational Reference

This skill establishes universal principles applicable to **all** agent skills. For the authoritative standards and validation checklist, see [Agent Skills File Guidelines](../../../instructions/agent-skills.instructions.md).

---

## Core Skill Design Principles

Before creating a skill, understand these foundational concepts:

1. **Consolidation**: Group related capabilities into one skill (not fragmented across many)
2. **Progressive Disclosure**: Keep SKILL.md focused (~500 lines); move detailed content to references/
3. **Composability**: Each skill works independently AND integrates with other skills
4. **Evaluability**: Clear triggers and measurable outcomes enable validation

See [Skill Design Principles](./references/skill-design-principles.md) for detailed explanation and design checklist.

---

## Step-by-Step Skill Creation

### Step 1: Define Scope

**Input needed**: Skill name and high-level purpose

Ask:
- What specialized workflow or capability does this skill teach?
- What problem does it solve?
- Is this skill focused enough (not trying to do too much)?

**Consolidation check**: Does your skill consolidate related capabilities, or does it fragment into multiple skills?

See [Skill Design Principles - Consolidation](./references/skill-design-principles.md#consolidation-principle) for guidance.

### Step 2: Design Skill Description

**Output**: YAML frontmatter with `name` and `description`

The description is **critical**—it's how Copilot discovers and activates your skill.

**Formula**: [CAPABILITY] for [DOMAIN]. Use when [TRIGGER 1], [TRIGGER 2], [TRIGGER 3]. [OPTIONAL: Supported details].

**Example** (webapp-testing skill):
```yaml
description: Toolkit for testing local web applications using Playwright. Use when asked to verify frontend functionality, debug UI behavior, capture browser screenshots, check for visual regressions, or view browser console logs. Supports Chrome, Firefox, and WebKit browsers.
```

See [Description Keywords & Activation Triggers](./references/description-keywords.md) for:
- How to write descriptions that activate properly
- Trigger phrase examples by category
- Testing your description before finalizing
- Common anti-patterns to avoid

### Step 3: Create Directory Structure

**Output**: Directory tree with SKILL.md and optional subdirectories

```
.github/skills/[skill-name]/
├── SKILL.md                    # Required: Main skill instructions
├── LICENSE.txt                 # Recommended: Apache 2.0 license
├── references/                 # Optional: Deep documentation
│   └── [topic-guide].md
├── scripts/                    # Optional: Executable automation
│   └── [helper-script].py
└── templates/                  # Optional: Starter code (modified by agent)
    └── [scaffold].py
```

See [Resource Bundling Strategy](./references/resource-bundling-strategy.md) for:
- When to create scripts/ (complex, reusable code)
- When to create references/ (>500 lines of docs)
- When to create templates/ (boilerplate code)
- When to create assets/ (static files used as-is)

### Step 4: Write SKILL.md Body

**Structure** (see [Agent Skills File Guidelines](../../../instructions/agent-skills.instructions.md#body-content) for sections):

- `## When to Use This Skill` - Reinforce description triggers
- `## Prerequisites` - Required tools, setup, dependencies
- `## Step-by-Step Workflows` - Numbered procedures for common tasks
- `## Troubleshooting` - Common issues and solutions
- `## References` - Links to bundled docs and external resources

**Length guideline**: Keep main body 400-500 lines. Move detailed content to `references/` folder.

**Content principles**:
- Use imperative mood ("Run", "Create", "Configure")
- Be specific and actionable
- Include exact commands with parameters
- Show expected outputs

**Link to references** instead of embedding everything:
```markdown
## Configure Environment
See [setup guide](./references/environment-setup.md) for detailed instructions.
```

### Step 5: Bundle Resources

**Decide** which resources to include using the decision framework:

- **Scripts**: Reusable code that would be regenerated repeatedly? → `scripts/`
- **References**: Documentation >500 lines? → `references/`
- **Templates**: Boilerplate code the agent modifies? → `templates/`
- **Assets**: Static files used unchanged in output? → `assets/`

See [Resource Bundling Strategy](./references/resource-bundling-strategy.md#decision-framework) for decision trees and examples.

### Step 6: Validate Skill Structure

**Checklist** (from [Agent Skills File Guidelines](../../../instructions/agent-skills.instructions.md#validation-checklist)):

- [ ] Frontmatter has valid `name` and `description`
- [ ] `name` is lowercase with hyphens, ≤64 characters
- [ ] `description` clearly states **WHAT** (capability), **WHEN** (triggers), **KEYWORDS**
- [ ] Body includes when-to-use, prerequisites, workflows
- [ ] SKILL.md body is 400-500 lines max (detailed content in references/)
- [ ] All resource links use relative paths
- [ ] Scripts include help docs and error handling
- [ ] No hardcoded credentials or secrets

### Step 7: Test Activation

**Verify** the skill activates when expected:

1. Save the skill directory to `.github/skills/[skill-name]/`
2. Test activation by mentioning the trigger phrases from your description
3. Verify Copilot loads the full SKILL.md body
4. Check that referenced resources (scripts, docs) load on-demand

---

## Tech-Specific Skills (.NET, TypeScript, Python)

Planning to create tech-specific agent skills?

See [Tech-Stack Extension Pattern](./references/tech-stack-pattern.md) for:
- Naming convention: `{tech}-agent-skill` (e.g., `dotnet-agent-skill`)
- How to reference agent-skill-creator as foundational
- Structure for adding tech-specific principles on top
- Implementation timeline and examples

Future tech-specific skills will build on this foundational skill, allowing modular reuse across different technology contexts.

---

## Best Practices Summary

| Principle | Implementation |
|-----------|---|
| **Progressive Disclosure** | Keep SKILL.md ~500 lines; link to references/ for deep dives |
| **Composability** | Each skill works standalone; document integration points with other skills |
| **Evaluability** | Include clear triggers, measurable outcomes, validation steps |
| **Consolidation** | Group related capabilities; don't fragment into multiple skills |
| **Description Quality** | Include WHAT, WHEN, and KEYWORDS; avoid vague language |
| **Resource Organization** | Use scripts/, references/, templates/, assets/ appropriately |
| **Documentation Standards** | Follow [Agent Skills File Guidelines](../../../instructions/agent-skills.instructions.md) |

---

## Related Skills & References

- **[Agent Skills File Guidelines](../../../instructions/agent-skills.instructions.md)** - Authoritative standards and validation checklist
- **[Skill Design Principles](./references/skill-design-principles.md)** - Core concepts (consolidation, progressive disclosure, etc.)
- **[Description Keywords Guide](./references/description-keywords.md)** - Writing descriptions that activate properly
- **[Resource Bundling Strategy](./references/resource-bundling-strategy.md)** - When/how to use scripts/, references/, templates/
- **[Tech-Stack Pattern](./references/tech-stack-pattern.md)** - Creating tech-specific skills (.NET, TypeScript, etc.)

## Example Skills in This Library

These skills follow the principles above:

- [context-fundamentals](../../context-fundamentals/SKILL.md) - Progressive disclosure, context engineering
- [tool-design](../../tool-design/SKILL.md) - Consolidation principle, architectural reduction
- [evaluation](../../evaluation/SKILL.md) - Evaluability framework, quality measurement
- [webapp-testing](../../webapp-testing/SKILL.md) - Resource bundling with Playwright helper