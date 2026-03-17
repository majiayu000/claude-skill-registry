---
name: skill-contract-generator
description: Generates evolution contracts for skills, defining what can be updated, what must remain stable, and how to extract knowledge. Use when creating new skills or formalizing update rules for existing skills. Adds a "Skill Contract" section to SKILL.md that guides skill-updater during project work.
---

# Skill Contract Generator

## Overview

This skill adds a structured "Skill Contract" section to any skill's SKILL.md file. The contract declares what parts of the skill are stable (general knowledge) versus mutable (can evolve during projects), and defines rules for updates and knowledge extraction.

## When to Use This Skill

Use this skill when:
- Creating a new skill and want to define its evolution rules
- Formalizing update boundaries for an existing skill
- Preparing a skill to be used with `skill-updater`
- Clarifying what knowledge should be extracted after projects

## Workflow

### Step 1: Select Target Skill

Identify which skill needs a contract:
- **For new skills**: Use immediately after creating with `skill-creator`
- **For existing skills**: Add contracts retroactively

Ask the user:
- "Which skill do you want to create a contract for?"
- "Where is the skill's SKILL.md file?"

Default assumption: `.claude/skills/<skill-name>/SKILL.md`

### Step 2: Analyze Skill Structure

Read the skill's SKILL.md to understand:
- **Skill type**: Meta-skill vs. general skill
- **Content structure**: What sections exist
- **Resources**: scripts/, references/, assets/ directories
- **Complexity**: Simple reference vs. complex workflow

This analysis informs contract generation.

### Step 3: Define Stable Elements

Identify what should remain constant across projects:

**Core Workflow Steps:**
- Fundamental process that defines the skill
- Essential decision logic
- Standard operating procedures

**Domain Knowledge:**
- Best practices that apply universally
- Technical specifications
- API/library patterns that rarely change

**Examples:**
- For `git-workflow`: All Git commands are stable
- For `project-context-generator`: The 4-step workflow is stable
- For `skill-analyzer`: Matching heuristics are stable

### Step 4: Define Mutable Elements

Identify what can evolve during projects:

**New References:**
- Project-specific patterns discovered
- Examples from real usage
- Edge cases encountered

**Improved Explanations:**
- Clarified instructions based on confusion
- Better examples
- Refined decision trees

**Additional Scripts:**
- Helper utilities that prove useful
- Validation tools
- Automation scripts

**Examples:**
- For `git-workflow`: Can add project-specific workflows to references/
- For `project-logger`: Can add new entry types based on project needs
- For `skill-analyzer`: Can refine matching criteria

### Step 5: Define Update Rules

Specify how updates should happen:

**Allowed Operations:**
- Add files to references/ (always allowed)
- Modify specific sections of SKILL.md (list which ones)
- Add scripts to scripts/ (with constraints)
- Optimize phrasing (without changing meaning)

**Prohibited Operations:**
- Changing core workflow structure
- Removing established best practices
- Breaking backward compatibility

**Review Requirements:**
- What changes need human approval
- What can be automated
- When to create a new skill vs. updating existing

### Step 6: Define Knowledge Extraction Needs

Specify what to look for when extracting knowledge:

**Patterns to Extract:**
- Common use cases that emerge
- Frequently asked questions
- Reusable code snippets

**Abstraction Triggers:**
- When to generalize project-specific patterns
- What threshold indicates general applicability
- How to separate general vs. project-specific

**Examples:**
- For `frontend-design`: Extract common component patterns
- For `project-logger`: Extract common log entry patterns
- For domain skills: Extract reusable business logic

### Step 7: Generate Contract Section and File

Create both a concise contract summary in SKILL.md and a detailed contract file in references/.

**A. Create references/contract.md** (detailed specification):

```markdown
# Skill Contract: [skill-name]

> Complete specification of what can evolve and what must remain stable.

## Stable (General Knowledge)

**Core Elements:**
- [List workflow steps, domain knowledge, or essential patterns]
- [What defines this skill's identity]

**Do not modify:**
- [Specific sections or content that must remain unchanged]

## Mutable (Can Evolve)

**Can be updated during projects:**
- [What can be added/refined in SKILL.md]
- [New files that can be added to references/]
- [Scripts that can be added to scripts/]

**Update guidelines:**
- [How to add new content]
- [What format to use]
- [When to update vs. create new skill]

## Update Rules

**Allowed without review:**
- Add new examples to existing sections
- Add reference files documenting project patterns
- Fix typos or clarify confusing wording

**Requires review:**
- Modify core workflow steps
- Change established best practices
- Add new sections to SKILL.md

**Prohibited:**
- Remove existing best practices
- Change fundamental skill purpose
- Break compatibility with existing usage

## Knowledge Extraction

**What to extract after projects:**
- [Patterns that emerged multiple times]
- [Common questions or confusion points]
- [Reusable code or templates]

**When to extract:**
- [Trigger: e.g., "After 3 projects using this skill"]
- [Indicator: e.g., "When same pattern appears in 2+ projects"]

**How to extract:**
- Add generalizable patterns to references/
- Update examples in SKILL.md with real cases
- Create new skills for project-specific domains
```

**B. Add concise summary to SKILL.md** (progressive disclosure):

```markdown
## Skill Contract

**Stable:** [One-line summary of what cannot change]
**Mutable:** [One-line summary of what can evolve]
**Update rules:** [One-line summary or "See references/contract.md"]

> Full contract specification in `references/contract.md`
```

**Example:**
```markdown
## Skill Contract

**Stable:** Core workflow steps, domain knowledge, essential patterns
**Mutable:** References, examples, clarifications, project-specific workflows
**Update rules:** See `references/contract.md` for detailed rules

> Full contract specification in `references/contract.md`
```

### Step 8: Insert Contract and Create File

Execute both operations:

**A. Create references/contract.md:**
1. Create `references/` directory if it doesn't exist
2. Write detailed contract to `references/contract.md`
3. Use the full template from Step 7A

**B. Insert contract summary into SKILL.md:**

**Placement:**
- After the main content
- Before the "Resources" section (if any)
- As the second-to-last section

**Insertion process:**
1. Read current SKILL.md
2. Find insertion point (before Resources or at end)
3. Insert concise "## Skill Contract" section
4. Write updated SKILL.md

**Result:** Skill now has both:
- Concise contract in SKILL.md (respects context window)
- Detailed contract in references/contract.md (for deep dives)

### Step 9: Confirm and Document

Present the contract to the user:
- Show the generated contract
- Explain the stable/mutable boundaries
- Confirm update rules make sense

Ask:
- "Does this contract accurately reflect the skill's evolution rules?"
- "Are there additional constraints or freedoms needed?"

Update if necessary, then confirm completion.

## Contract Templates by Skill Type

### Template: Reference/Guidelines Skills

For skills like `git-workflow` that provide reference information:

**Stable:**
- Core reference content (commands, APIs, patterns)
- Organizational structure

**Mutable:**
- Additional examples
- Project-specific workflows in references/
- Clarifications and tips

### Template: Workflow Skills

For skills like `project-context-generator` with step-by-step processes:

**Stable:**
- Workflow steps and their order
- Core questions to ask
- Template structure

**Mutable:**
- Example questions
- Template sections (can add, not remove)
- Additional guidance for edge cases

### Template: Meta-Skills

For skills like `skill-analyzer` that operate on other skills:

**Stable:**
- Core algorithm or heuristics
- Input/output format
- Integration points

**Mutable:**
- Heuristic weights or criteria
- Edge case handling
- Additional validation rules

## Best Practices

### Be Specific About Boundaries

**Good:**
```
Can add new examples to "Best Practices" section
Can add files to references/ documenting project patterns
Cannot modify the 4-step workflow structure
```

**Avoid vague:**
```
Can update as needed
Don't change important parts
```

### Consider Skill Maturity

**New skills**: More permissive contracts (still learning what works)
**Mature skills**: Stricter contracts (proven patterns to preserve)

### Balance Flexibility and Stability

- Too rigid: Skill can't improve
- Too flexible: Skill loses coherence
- Right balance: Core identity preserved, details evolve

## Resources

### references/contract_template.md

Template for the Skill Contract section with:
- Standard structure
- Examples for different skill types
- Placeholder text for customization

See this file for the complete contract template that can be customized for any skill.
