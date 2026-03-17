---
name: skill-creator
description: Interactive skill creation wizard that guides you through building properly formatted Claude Skills with YAML frontmatter, progressive disclosure, and best practices
---

# Skill Creator

## Purpose

Interactive wizard that helps create new Claude Skills with proper structure, YAML frontmatter, progressive disclosure, and validation. Asks clarifying questions to generate well-formatted skills automatically.

## When to Use

- Creating new Claude Skills from workflow patterns
- Converting repetitive agent code into reusable skills
- Standardizing skill format across team
- Teaching skill creation best practices
- Bootstrapping skill structure quickly

## Instructions

### Step 1: Gather Requirements

Ask the user about the workflow they want to automate:

```
🎯 Skill Creator - Interactive Wizard

I'll help you create a new Claude Skill. Let me ask a few questions:

1. What workflow or task do you want to automate?
   (Describe in 1-2 sentences)

2. When should this skill be triggered?
   Example: "When tests fail", "Before creating PR", "During implementation"

3. What tools/commands does this workflow use?
   Example: "git, gh CLI, npm test", "curl, jq, bash"

4. What inputs does this workflow need?
   Example: "issue number, branch name", "file path, test pattern"

5. What should the output be?
   Example: "JSON with results", "Success/failure message", "Generated files"
```

### Step 2: Validate Skill Name

```bash
# Skill naming rules:
# - Lowercase with hyphens (kebab-case)
# - Descriptive and concise
# - No more than 64 characters
# - Examples: fetch-issue-analysis, validate-typescript, root-cause-tracing

SKILL_NAME="<user-provided-name>"

# Validate length
if [ ${#SKILL_NAME} -gt 64 ]; then
  echo "❌ Skill name too long (max 64 chars)"
  echo "Suggested: $(echo "$SKILL_NAME" | cut -c1-64)"
fi

# Validate format
if ! echo "$SKILL_NAME" | grep -Eq '^[a-z][a-z0-9-]*$'; then
  echo "❌ Invalid format. Use lowercase letters, numbers, hyphens only"
  echo "Example: fetch-github-issue"
fi
```

### Step 3: Create Description (Max 1024 chars)

```
Description Guidelines:
- Start with action verb (Fetch, Validate, Create, Run, etc.)
- Explain WHAT it does, not HOW
- Include primary use case
- Keep under 1024 characters (will be loaded at startup)
- Mention integration points if relevant

Example:
"Fetch GitHub issue details with AI analysis comment from github-actions bot, extracting structured data for architecture planning in workflow automation"
```

### Step 4: Determine Skill Category

```
Select category (creates directory structure):

1. state-management/     - Workflow state, checkpoints, recovery
2. github-integration/   - GitHub API, issues, PRs, reviews
3. git-workflows/        - Git operations, branching, commits
4. quality/              - Testing, validation, gates
5. testing/              - Test execution, coverage
6. gemini-api/           - Gemini API patterns, rate limiting
7. debugging/            - Error diagnosis, root cause tracing
8. meta/                 - Skills about skills, creation, templates
9. custom/               - Project-specific patterns

Enter number or custom category name:
```

### Step 5: Estimate Complexity

```
Complexity estimation (determines progressive disclosure):

Simple (< 200 lines):
  - Single script/command
  - Few parameters
  - No conditionals
  → Single SKILL.md file

Medium (200-500 lines):
  - Multiple steps
  - Decision logic
  - Several examples
  → SKILL.md only

Complex (> 500 lines):
  - Extensive workflows
  - Many examples
  - Detailed reference
  → SKILL.md + REFERENCE.md (progressive disclosure)
  → Consider validation scripts in scripts/

Estimated complexity for your skill: [Simple/Medium/Complex]
```

### Step 6: Generate Directory Structure

```bash
CATEGORY="<selected-category>"
SKILL_NAME="<validated-name>"
COMPLEXITY="<simple|medium|complex>"

# Create base structure
mkdir -p ".claude/skills/$CATEGORY/$SKILL_NAME"

# Simple/Medium: SKILL.md only
if [ "$COMPLEXITY" != "complex" ]; then
  touch ".claude/skills/$CATEGORY/$SKILL_NAME/SKILL.md"
fi

# Complex: Add progressive disclosure
if [ "$COMPLEXITY" = "complex" ]; then
  touch ".claude/skills/$CATEGORY/$SKILL_NAME/SKILL.md"
  touch ".claude/skills/$CATEGORY/$SKILL_NAME/REFERENCE.md"
  mkdir -p ".claude/skills/$CATEGORY/$SKILL_NAME/scripts"
fi

echo "✅ Created structure at .claude/skills/$CATEGORY/$SKILL_NAME/"
```

### Step 7: Generate SKILL.md Template

```markdown
---
name: ${SKILL_NAME}
description: ${DESCRIPTION}
---

# ${TITLE}

## Purpose

[1-2 paragraph explanation of what this skill does and why it exists]

## When to Use

- [Use case 1]
- [Use case 2]
- [Integration point - e.g., "Conductor Phase 2"]

## Instructions

### Step 1: [First Action]

\`\`\`bash
# Example commands or code
PARAM1=\${1:-"default"}

# Validate inputs
if [ -z "$PARAM1" ]; then
  echo "❌ Error: Parameter required"
  exit 1
fi
\`\`\`

### Step 2: [Second Action]

\`\`\`bash
# Implementation
\`\`\`

### Step 3: [Output/Return]

Output format:

\`\`\`json
{
  "status": "success",
  "result": "..."
}
\`\`\`

## Integration with [Agent/Workflow]

Used in [agent name] [phase]:

\`\`\`markdown
**Step X: [Task Name]**

Use \`${SKILL_NAME}\` skill:
- Input: [parameters]
- Output: [result]
\`\`\`

## Error Handling

### [Error Case 1]

\`\`\`json
{
  "status": "error",
  "error": "Description",
  "code": "ERROR_CODE"
}
\`\`\`

## Related Skills

- \`related-skill-1\` - Brief description
- \`related-skill-2\` - Brief description

## Examples

### Example 1: [Common Case]

\`\`\`bash
# Input
${SKILL_NAME} param1 param2

# Output
{
  "status": "success"
}
\`\`\`

## Best Practices

1. **Practice 1** - Explanation
2. **Practice 2** - Explanation

## Notes

- Important consideration 1
- Important consideration 2
```

### Step 8: Generate REFERENCE.md (if complex)

Only for complex skills (> 500 lines estimated):

```markdown
# ${SKILL_NAME} - Reference Documentation

## Detailed API Reference

[Comprehensive technical details that don't fit in SKILL.md]

## Advanced Use Cases

### Use Case 1: [Advanced Scenario]

[Detailed explanation with code]

### Use Case 2: [Edge Case]

[Detailed explanation with code]

## Decision Matrices

[Complex decision trees, lookup tables, extensive examples]

## Schema Reference

[JSON schemas, data structures, type definitions]

## Troubleshooting Guide

[Common errors and resolutions]
```

### Step 9: Add Validation Scripts (if complex)

For complex skills, offer to create validation scripts:

```bash
# Example: scripts/validate-input.sh

#!/usr/bin/env bash
set -e

INPUT=$1

# Validation logic
if [ -z "$INPUT" ]; then
  echo "ERROR: Input required"
  exit 1
fi

echo "VALID"
exit 0
```

Advantages:
- Scripts consume 0 context tokens (only output counted)
- Deterministic, repeatable
- Faster execution
- Version controlled

### Step 10: Update Skills Catalog

Add new skill to `.claude/skills/README.md`:

```markdown
### ${CATEGORY}

- **${SKILL_NAME}** - ${DESCRIPTION}
  - Files: SKILL.md [+ REFERENCE.md] [+ scripts/]
  - Complexity: [Simple/Medium/Complex]
  - Integration: [Where used]
```

### Step 11: Validation Checklist

```
✅ Validation Checklist:

[ ] YAML frontmatter present with name + description
[ ] Name is kebab-case, ≤ 64 chars
[ ] Description ≤ 1024 chars
[ ] SKILL.md has clear structure:
    - Purpose
    - When to Use
    - Instructions (step by step)
    - Integration points
    - Error handling
    - Related skills
    - Examples
[ ] If > 500 lines: Content split to REFERENCE.md
[ ] If validation needed: Scripts in scripts/ directory
[ ] Related skills cross-referenced
[ ] Added to README.md catalog
[ ] Examples include both input and output
[ ] Error cases documented with JSON format
```

## Output Format

### Success

```
🎉 Skill Created Successfully!

Location: .claude/skills/${CATEGORY}/${SKILL_NAME}/

Files created:
  ✅ SKILL.md (${LINE_COUNT} lines)
  ${REFERENCE_MD_STATUS}
  ${SCRIPTS_STATUS}

Next steps:
1. Review generated content in SKILL.md
2. Customize examples for your use case
3. Test skill with: /skill ${SKILL_NAME}
4. Add to agent workflows as needed
5. Commit to git for team sharing

Integration suggestions:
- Add to ${SUGGESTED_AGENT} agent
- Use in ${SUGGESTED_PHASE} phase
- Related to: ${RELATED_SKILLS}
```

### With Warnings

```
⚠️ Skill Created with Warnings:

Location: .claude/skills/${CATEGORY}/${SKILL_NAME}/

Warnings:
  ⚠️ Description is ${CHAR_COUNT}/1024 chars (close to limit)
  ⚠️ Skill seems complex (${ESTIMATED_LINES} lines) - consider REFERENCE.md
  ⚠️ No validation scripts - consider adding for deterministic checks

Review and address warnings before use.
```

## Integration with Development Workflow

### Used by Developers

When creating new workflow automation:

```markdown
**Developer**: "I keep running the same git commands for feature branches"

**Claude**: "Let me use the skill-creator skill to automate that"

[Runs skill-creator, asks questions, generates create-feature-branch skill]

**Result**: Reusable skill saved to .claude/skills/git-workflows/
```

### Used by Conductor

When discovering repetitive patterns:

```markdown
**Conductor Phase 6**: Generate final report

If repetitive patterns detected during workflow:
  "I noticed you ran [command sequence] 3 times"
  "Would you like me to create a skill for this?"

  If yes: Use skill-creator to generate skill
```

## Best Practices

### 1. Start with "Why"

Always explain WHY the skill exists before HOW it works:

```markdown
## Purpose

**Why**: Developers waste 10 minutes per feature branch creating standardized branch names manually. This skill automates the process, ensuring consistent naming (feature/issue-123-description) and proper base branch setup.

**What**: Creates feature branch with validation, issue linking, and automatic tracking.
```

### 2. Progressive Disclosure

Keep frequently-accessed content in SKILL.md, move details to REFERENCE.md:

```markdown
## SKILL.md (Common workflows)

For advanced configuration, see REFERENCE.md Section 3.2

## REFERENCE.md (Details)

### Section 3.2: Advanced Configuration

[Extensive details here]
```

### 3. Validation Scripts for Determinism

If logic is deterministic, extract to scripts:

```bash
# ❌ Don't: Inline logic consuming tokens
```bash
if grep -q "test" file.txt; then
  if [ $(wc -l < file.txt) -gt 10 ]; then
    # complex validation logic
  fi
fi
```

# ✅ Do: Script consuming 0 tokens
bash scripts/validate-file.sh file.txt
```

### 4. Cross-Reference Related Skills

Help users discover complementary skills:

```markdown
## Related Skills

- `create-feature-branch` - Creates branch (run before this skill)
- `commit-with-validation` - Commits changes (run after this skill)
- `create-pull-request` - Creates PR (final step in workflow)

**Typical workflow**: create-feature-branch → [implementation] → THIS SKILL → create-pull-request
```

### 5. Include Integration Examples

Show how skills integrate with agents:

```markdown
## Integration with Conductor

Used in Phase 2 (Implementation), Step 4:

**Before implementation**:
Use `validate-architecture` to ensure design alignment

**After implementation**:
Proceed to Phase 3 (Quality Assurance)
```

## Examples

### Example 1: Simple Skill (< 200 lines)

```bash
User: "I want to check if tests exist before editing code"

Output:
.claude/skills/quality/check-tests-exist/
  SKILL.md

Content:
- 150 lines
- Single workflow
- No REFERENCE.md needed
```

### Example 2: Medium Skill (200-500 lines)

```bash
User: "I want to validate TypeScript compilation"

Output:
.claude/skills/quality/validate-typescript/
  SKILL.md

Content:
- 400 lines
- Multiple validation modes
- Examples and error handling
- No REFERENCE.md yet (under 500 line threshold)
```

### Example 3: Complex Skill (> 500 lines)

```bash
User: "I want to save complete workflow state for resumption"

Output:
.claude/skills/state-management/save-workflow-state/
  SKILL.md          # 250 lines - common workflows
  REFERENCE.md      # 200 lines - state schema, decision matrix
  scripts/
    validate-state.sh

Progressive disclosure:
- SKILL.md: How to save state (always loaded)
- REFERENCE.md: State schema details (loaded on-demand)
- scripts/: Validation logic (0 tokens, output only)
```

## Error Handling

### Invalid Skill Name

```
❌ Error: Invalid skill name "Fetch_Issue"

Skill names must:
- Use lowercase letters only
- Use hyphens for word separation (kebab-case)
- Be ≤ 64 characters
- Start with letter

Suggested: "fetch-issue"
```

### Description Too Long

```
⚠️ Warning: Description is 1,150 characters (limit: 1,024)

Description loaded at startup - keep concise!

Current:
"Fetch GitHub issue details with AI analysis comment from github-actions bot, extracting structured data including architectural alignment, technical feasibility, implementation suggestions, files affected, testing strategy, dependencies, and estimated complexity for use in architecture planning and workflow automation across conductor and orchestrator agents..."

Suggested:
"Fetch GitHub issue with AI analysis for workflow planning, extracting architecture insights and implementation guidance"

(Removed: 1,050 chars, Kept: 100 chars)
```

### Skill Already Exists

```
❌ Error: Skill "fetch-issue-analysis" already exists

Location: .claude/skills/github-integration/fetch-issue-analysis/

Options:
1. Choose different name
2. Edit existing skill
3. Create variant with suffix (e.g., fetch-issue-analysis-v2)

Would you like to:
- View existing skill
- Edit existing skill
- Choose new name
```

## Related Skills

- `agent-creator` - Creates agent definitions (orchestration layer)
- `validate-skill-format` - Validates skill YAML and structure
- `skill-catalog-generator` - Auto-generates skill documentation

## Notes

- Skills created with this tool follow official Claude Skills specification
- Progressive disclosure (REFERENCE.md) recommended for skills > 500 lines
- Validation scripts reduce token consumption by 30-40%
- All skills are git-committed for team sharing
- YAML frontmatter is mandatory (name + description)
- Description limit: 1,024 characters (enforced at startup)
- Name limit: 64 characters (enforced at startup)
