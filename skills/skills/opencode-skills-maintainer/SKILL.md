---
name: opencode-skills-maintainer
description: Automatically update Build-With-Skills and Plan-With-Skills agents with new skills from skills/ folder, keeping their system prompts synchronized with available skills
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: maintenance
---

## What I do

I maintain the Build-With-Skills and Plan-With-Skills agents by:

1. **Discover All Skills**: Scan the `skills/` folder to discover all available skills
2. **Extract Skill Metadata**: Read frontmatter from each SKILL.md file (name, description, category)
3. **Categorize Skills**: Organize skills into logical categories (Framework, Test Generators, Linters, etc.)
4. **Update Agent Prompts**: Update both Build-With-Skills and Plan-With-Skills system prompts with the complete, current skill list
5. **Validate Changes**: Ensure config.json is valid after updates
6. **Generate Report**: Provide a summary of changes made

## When to use me

Use this skill when:
- You've added new skills to the skills/ folder
- You've removed skills from the skills/ folder
- You've updated skill descriptions or metadata
- You want to ensure agents have the latest skill list
- Agents are unable to find skills that should be available

## Prerequisites

- Access to the repository root directory
- `jq` tool installed for JSON validation
- Python 3+ installed for JSON manipulation
- Write permissions for config.json

## Steps

### Step 1: Discover All Skills

Scan the `skills/` folder to find all skill directories:

```bash
# Find all skill directories
find skills/ -name "SKILL.md" -type f | sort
```

### Step 2: Extract Skill Metadata

For each skill, read the frontmatter to extract:

```bash
# Extract name and description from frontmatter
for skill_dir in skills/*/; do
  echo "=== $(basename "$skill_dir") ==="
  head -10 "$skill_dir/SKILL.md" | grep -E "(name:|description:)" | head -2
  echo
done
```

**Required Fields**:
- `name`: The skill identifier (used in agent prompts)
- `description`: Brief description of what the skill does
- Optional: `category`, `workflow`, `audience` (from metadata section)

### Step 3: Categorize Skills

Organize skills into logical categories:

```bash
# Framework Skills (Foundational Workflows)
- linting-workflow
- test-generator-framework
- ticket-branch-workflow
- pr-creation-workflow

# Language-Specific Test Generators
- python-pytest-creator
- nextjs-unit-test-creator

# Language-Specific Linters
- python-ruff-linter
- javascript-eslint-linter

# Project Setup
- nextjs-standard-setup

# Git/Workflow
- git-issue-creator
- git-pr-creator
- jira-git-integration
- jira-git-workflow
- nextjs-pr-workflow

# OpenCode Meta
- opencode-agent-creation
- opencode-skill-creation
- opencode-skill-auditor

# OpenTofu/Infrastructure
- opentofu-provider-setup
- opentofu-provisioning-workflow
- opentofu-aws-explorer
- opentofu-kubernetes-explorer
- opentofu-neon-explorer
- opentofu-keycloak-explorer

# Code Quality/Documentation
- docstring-generator
- typescript-dry-principle
- coverage-readme-workflow

# Utilities
- ascii-diagram-creator
```

### Step 4: Update Build-With-Skills Agent Prompt

Generate the "Available Skills" section for Build-With-Skills:

```python
# Python script to update Build-With-Skills prompt
import json

# Build the skills section
skills_section = """## Available Skills (Hardcoded in System Prompt)

### Framework Skills (Foundational Workflows)
- **linting-workflow**: {description}
- **test-generator-framework**: {description}
- **ticket-branch-workflow**: {description}
- **pr-creation-workflow**: {description}

### Language-Specific Test Generators
- **python-pytest-creator**: {description}
- **nextjs-unit-test-creator**: {description}

# ... (continue for all categories)

"""
```

**Update Process**:
1. Read current config.json
2. Replace the skill discovery section with hardcoded skill list
3. Remove references to SKILL_INDEX.json
4. Update skill execution paths from `[skill-path]` to `[skill-name]`
5. Preserve all other prompt content (workflow, guidelines, QA)
6. Write back to config.json

### Step 5: Update Plan-With-Skills Agent Prompt

Generate the same "Available Skills" section for Plan-With-Skills:

**The skills section should be identical** between both agents to ensure consistency.

**Update Process**:
1. Read current config.json
2. Replace the skill discovery section with hardcoded skill list
3. Remove references to SKILL_INDEX.json
4. Update skill selection guidelines to match hardcoded list
5. Preserve all other prompt content (workflow, guidelines, QA)
6. Write back to config.json

### Step 6: Validate Changes

Validate the updated config.json:

```bash
# Validate JSON syntax
jq . config.json

# Check if JSON is valid
echo "Exit code: $?"
# Exit code 0 = valid JSON
```

### Step 7: Generate Report

Create a summary of changes:

```markdown
# Skills Maintenance Report

## Skills Found: {total_count}

### Categories
- Framework Skills: {count}
- Language-Specific Test Generators: {count}
- Language-Specific Linters: {count}
- Project Setup: {count}
- Git/Workflow: {count}
- OpenCode Meta: {count}
- OpenTofu/Infrastructure: {count}
- Code Quality/Documentation: {count}
- Utilities: {count}

## Changes Made
- Updated Build-With-Skills agent prompt with {count} skills
- Updated Plan-With-Skills agent prompt with {count} skills
- Removed SKILL_INDEX.json references
- Updated skill discovery workflow to use hardcoded list

## New Skills Added (if any)
- [skill-name]: description

## Removed Skills (if any)
- [skill-name]: previously in list

## Validation
✓ JSON validation passed
✓ Both agents updated successfully
✓ Skill lists synchronized
```

## Best Practices

### Categorization Logic

**Framework Skills**: Skills that provide foundational workflows used by other skills
- Test framework, linting framework, PR workflow, ticket workflow

**Language-Specific**: Skills for specific programming languages or frameworks
- Test generators, linters, project setup

**Meta Skills**: Skills that create/audit other skills or agents
- opencode-agent-creation, opencode-skill-creation, opencode-skill-auditor

**Domain-Specific**: Skills for specific domains
- OpenTofu infrastructure, Git/DevOps, documentation

### Prompt Structure

Both agent prompts should follow this structure:
1. Available Skills (hardcoded, categorized)
2. Core Workflow (updated to remove SKILL_INDEX.json)
3. Skill Selection Guidelines (match hardcoded list)
4. Skill Execution Process (path updated to `[skill-name]`)
5. Error Handling (no fallback to SKILL_INDEX.json)
6. Quality Assurance (unchanged)
7. Output Format (no first step to read SKILL_INDEX.json)

### Consistency

- Both agents should have **identical** skill lists and categories
- Skill names and descriptions should match SKILL.md exactly
- Maintain alphabetical ordering within categories
- Use consistent formatting (bold names, descriptions after colon)

## Common Issues

### SKILL.md Not Found

**Issue**: Cannot find SKILL.md in a skill directory

**Solution**:
```bash
# Verify SKILL.md exists for all skills
for dir in skills/*/; do
  if [ ! -f "$dir/SKILL.md" ]; then
    echo "Missing SKILL.md in: $dir"
  fi
done
```

### Invalid Frontmatter

**Issue**: SKILL.md has missing or malformed frontmatter

**Solution**:
```bash
# Check for required frontmatter fields
for dir in skills/*/; do
  if ! grep -q "^name:" "$dir/SKILL.md"; then
    echo "Missing 'name:' field in: $dir/SKILL.md"
  fi
  if ! grep -q "^description:" "$dir/SKILL.md"; then
    echo "Missing 'description:' field in: $dir/SKILL.md"
  fi
done
```

### JSON Validation Fails

**Issue**: `jq . config.json` returns errors

**Solution**:
- Check for unclosed brackets or quotes
- Ensure strings are properly escaped
- Verify no trailing commas in JSON arrays
- Use Python JSON validation as backup:
  ```bash
  python3 -m json.tool config.json > /dev/null
  ```

### Agent Prompts Not Updated

**Issue**: config.json changes don't reflect in agent prompts

**Solution**:
- Verify config.json was saved correctly
- Check that Python script wrote the file successfully
- Re-run this skill to regenerate prompts
- Manually verify prompt sections with `jq`

## Verification Commands

After running this skill, verify with these commands:

```bash
# Verify JSON syntax
jq . config.json && echo "✓ JSON valid"

# Check Build-With-Skills has skill list
jq '.agent["build-with-skills"].prompt' config.json | grep "Available Skills" && echo "✓ Build-With-Skills updated"

# Check Plan-With-Skills has skill list
jq '.agent["plan-with-skills"].prompt' config.json | grep "Available Skills" && echo "✓ Plan-With-Skills updated"

# Verify no SKILL_INDEX.json references
! jq '.agent["build-with-skills"].prompt' config.json | grep -q "SKILL_INDEX.json" && echo "✓ SKILL_INDEX.json references removed"

# Verify both agents have identical skill sections
BWS_SKILLS=$(jq '.agent["build-with-skills"].prompt' config.json | sed -n '/## Available Skills/,/## Core Workflow/p')
PWS_SKILLS=$(jq '.agent["plan-with-skills"].prompt' config.json | sed -n '/## Available Skills/,/## Core Workflow/p')
[ "$BWS_SKILLS" = "$PWS_SKILLS" ] && echo "✓ Skill lists synchronized"
```

**Verification Checklist**:
- [ ] JSON validation passes
- [ ] Build-With-Skills has "Available Skills" section
- [ ] Plan-With-Skills has "Available Skills" section
- [ ] Both skill lists are identical
- [ ] No SKILL_INDEX.json references remain
- [ ] Skill names match SKILL.md files
- [ ] All skills are categorized correctly
- [ ] Descriptions match SKILL.md frontmatter

## Automation

This skill can be automated with a cron job or git hook:

**Git Pre-Commit Hook**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if skills changed
if git diff --name-only --cached | grep -q "^skills/"; then
  echo "Skills changed, updating agent prompts..."
  opencode --agent build-with-skills "Use opencode-skills-maintainer to update agent prompts"
fi
```

**Cron Job** (run daily):
```bash
# Run at 2 AM daily
0 2 * * * cd /path/to/repo && opencode --agent build-with-skills "Use opencode-skills-maintainer to update agent prompts"
```

## Example Output

**Skills Found: 27**

### Categories
- Framework Skills: 4
- Language-Specific Test Generators: 2
- Language-Specific Linters: 2
- Project Setup: 1
- Git/Workflow: 5
- OpenCode Meta: 3
- OpenTofu/Infrastructure: 6
- Code Quality/Documentation: 3
- Utilities: 1

## Changes Made
- Updated Build-With-Skills agent prompt with 27 skills
- Updated Plan-With-Skills agent prompt with 27 skills
- Removed SKILL_INDEX.json references
- Updated skill discovery workflow to use hardcoded list

## New Skills Added
- nextjs-standard-setup: Create standardized Next.js 16 demo applications with shadcn, Tailwind v4, and specific folder structure using Tekk-prefixed components

## Validation
✓ JSON validation passed
✓ Both agents updated successfully
✓ Skill lists synchronized

## Related Skills

- `opencode-agent-creation`: For creating new agents
- `opencode-skill-creation`: For creating new skills
- `opencode-skill-auditor`: For auditing skill redundancy
