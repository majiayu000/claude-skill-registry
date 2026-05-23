---
name: opencode-skill-creation
description: Generate OpenCode skills following official documentation best practices
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: skill-development
---

## What I do

I guide you through creating a new OpenCode skill from scratch by:

1. **Collect Requirements**: Prompt for skill name, description, purpose, audience, and workflow type
2. **Generate Frontmatter**: Create proper YAML frontmatter with all required fields
3. **Structure Content**: Build complete skill documentation following official standards
4. **Validate**: Ensure skill meets naming rules and documentation guidelines
5. **Create Files**: Write SKILL.md to appropriate directory structure
6. **Update Agents**: **CRITICAL FINAL STEP** - Always run opencode-skills-maintainer to update Build-With-Skills and Plan-With-Skills agents

## When to use me

Use this when:
- You want to create a new OpenCode skill without manually formatting SKILL.md
- You need to ensure your skill follows official documentation standards
- You want to avoid repetitive setup when creating multiple skills
- You want to ensure agents are automatically updated with new skills

Ask clarifying questions about:
- Skill's primary purpose and capabilities
- Target audience (developers, DevOps, QA, etc.)
- Workflow type (testing, linting, deployment, etc.)
- Prerequisites and dependencies
- Expected inputs and outputs

## Prerequisites

- Write access to the skills/ directory
- Understanding of OpenCode skill structure
- Knowledge of the skill's purpose and requirements
- Python 3+ for YAML validation (optional but recommended)

## Steps

### Step 1: Gather Skill Requirements

Prompt the user for the following information:

**Required Fields**:
- **Name**: Unique skill identifier (1-64 chars, lowercase alphanumeric with single hyphens)
- **Description**: Brief description (1-1024 chars) specific enough for agents to choose correctly
- **License**: Usually "Apache-2.0" but can be specified

**Optional Fields**:
- **Compatibility**: Usually "opencode" but can specify framework compatibility
- **Audience**: Target users (developers, DevOps, QA, etc.)
- **Workflow**: Workflow type (testing, linting, deployment, etc.)

**Prompt Template**:
```
Please provide the following information for your new skill:

1. **Skill Name**: (lowercase, alphanumeric, single hyphens, 1-64 chars)
2. **Description**: (1-1024 characters, specific for skill selection)
3. **License**: (default: Apache-2.0)
4. **Compatibility**: (default: opencode)
5. **Target Audience**: (e.g., developers, DevOps, QA)
6. **Workflow Type**: (e.g., testing, linting, deployment)

Example:
  - Name: python-pytest-creator
  - Description: Generate comprehensive pytest test files for Python using test-generator-framework
  - Audience: developers
  - Workflow: testing
```

### Step 2: Validate Skill Name

Ensure the skill name follows naming rules:

```bash
# Check name length (1-64 characters)
if [ ${#skill_name} -lt 1 ] || [ ${#skill_name} -gt 64 ]; then
  echo "Error: Skill name must be 1-64 characters"
  exit 1
fi

# Check for valid characters (lowercase alphanumeric and single hyphens)
if [[ ! $skill_name =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: Skill name must be lowercase alphanumeric with single hyphens"
  exit 1
fi

# Check for double hyphens
if [[ $skill_name =~ -- ]]; then
  echo "Error: Skill name cannot contain double hyphens"
  exit 1
fi

# Check for leading/trailing hyphens
if [[ $skill_name =~ ^- || $skill_name =~ -$ ]]; then
  echo "Error: Skill name cannot start or end with hyphens"
  exit 1
fi
```

### Step 3: Generate YAML Frontmatter

Create the frontmatter section with all provided fields:

```yaml
---
name: <skill-name>
description: <skill-description>
license: <license-type>
compatibility: <compatibility>
metadata:
  audience: <target-audience>
  workflow: <workflow-type>
---
```

**Example**:
```yaml
---
name: python-pytest-creator
description: Generate comprehensive pytest test files for Python using test-generator-framework
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---
```

### Step 4: Build Skill Content

Structure the skill documentation with the following sections:

#### Required Sections

**"## What I do"** (What the skill achieves):
- List primary capabilities (3-7 items)
- Use bullet points with action verbs
- Be specific about what the skill does
- Include any frameworks or tools used

**"## When to use me"** (Usage scenarios):
- List scenarios when to use this skill
- Use bullet points with specific conditions
- Include examples of tasks
- Mention alternatives (if any)

#### Optional Sections (Recommended)

**"## Prerequisites"**: Requirements to run the skill
**"## Steps"**: Detailed workflow steps
**"## Best Practices"**: Recommended approaches
**"## Common Issues"**: Troubleshooting guide
**"## Verification Commands"**: Commands to validate results
**"## Related Skills"**: Other skills that work well together

### Step 5: Create Directory and File

Create the skill directory structure:

```bash
# Create skill directory
mkdir -p "skills/<skill-name>"

# Create SKILL.md file
touch "skills/<skill-name>/SKILL.md"
```

**Example**:
```bash
mkdir -p skills/python-pytest-creator
touch skills/python-pytest-creator/SKILL.md
```

### Step 6: Write Skill Documentation

**IMPORTANT: Always use `read` tool before using `write` or `edit` on existing files.**

This is especially critical when updating:
- **PLAN.md** - Always read first to preserve existing task status
- **README.md** - Always read first to preserve documentation structure
- **Existing SKILL.md files** - Always read first to avoid overwriting content

**Why Read First?**
- The `write` tool completely overwrites existing files
- Prevents accidental data loss of existing content
- Ensures you have full context before making changes
- Required for proper file safety in OpenCode workflows

Write the complete SKILL.md file:

```bash
# For NEW files (created in Step 5), you can write directly:
cat > "skills/<skill-name>/SKILL.md" << 'EOF'
---
name: <skill-name>
description: <skill-description>
license: <license-type>
compatibility: <compatibility>
metadata:
  audience: <target-audience>
  workflow: <workflow-type>
---

## What I do

- [Capability 1]
- [Capability 2]
- [Capability 3]

## When to use me

Use this when:
- [Scenario 1]
- [Scenario 2]

## [Optional sections...]

EOF

# For EXISTING files, ALWAYS read first:
# 1. Read the file
read filePath="PLAN.md"

# 2. Now use edit to make targeted changes
edit filePath="PLAN.md" oldString="old content" newString="new content"

# OR use write with full content (only if you have the full context)
write filePath="PLAN.md" content="full updated content after reading"
```

### Step 7: Validate Created Skill

Verify the skill was created correctly:

```bash
# Check file exists
if [ ! -f "skills/<skill-name>/SKILL.md" ]; then
  echo "Error: SKILL.md was not created"
  exit 1
fi

# Validate YAML syntax (requires python3 and pyyaml)
python3 -c "import yaml; yaml.safe_load(open('skills/<skill-name>/SKILL.md'))" 2>&1

# Check frontmatter fields
grep -q "^name:" "skills/<skill-name>/SKILL.md" || echo "Warning: Missing 'name' field"
grep -q "^description:" "skills/<skill-name>/SKILL.md" || echo "Warning: Missing 'description' field"
```

### Step 8: Update Agents (CRITICAL FINAL STEP)

**ALWAYS execute this final step** to ensure agents know about the new skill:

```bash
# Use Build-With-Skills agent with opencode-skills-maintainer
opencode --agent build-with-skills "Use opencode-skills-maintainer skill to update Build-With-Skills and Plan-With-Skills agents with the new skill I just created"

# Or manually invoke the skill if already in an agent session
echo "Running opencode-skills-maintainer to update agents with new skill..."
# [Agent will execute opencode-skills-maintainer workflow]
```

**Why This Step is Critical**:
- Build-With-Skills and Plan-With-Skills use hardcoded skill lists
- Without this step, agents won't know the new skill exists
- The skill will be created but unavailable to agents
- This ensures consistency between skills/ folder and agent prompts

**What opencode-skills-maintainer Does**:
1. Scans skills/ folder for all SKILL.md files
2. Extracts skill metadata from frontmatter
3. Updates both Build-With-Skills and Plan-With-Skills agent prompts
4. Validates config.json with jq
5. Generates a maintenance report

## Best Practices

### Naming Conventions

- **Use descriptive names**: `python-pytest-creator` (good), `skill-1` (bad)
- **Include workflow type**: `-test`, `-lint`, `-setup`, `-workflow`
- **Follow lowercase**: `nextjs-standard-setup` (good), `NextJS-Standard-Setup` (bad)
- **Single hyphens only**: `git-pr-creator` (good), `git--pr-creator` (bad)
- **No underscores**: `python_pytest` (bad), `python-pytest` (good)

### Description Guidelines

- **Be specific**: "Generate pytest tests" (good), "Create tests" (vague)
- **Include framework**: "using test-generator-framework" (good)
- **Mention capabilities**: "for Next.js 16 with App Router" (good)
- **Length**: 1-1024 characters (optimal: 50-150 chars)

### Content Structure

- **Start with capabilities**: "## What I do" section first
- **Follow with scenarios**: "## When to use me" section
- **Add details**: Optional sections based on complexity
- **Use code blocks**: Include examples with triple backticks
- **Be thorough**: More detail is better than less

### File Safety

- **ALWAYS read before writing**: Use `read` tool before using `write` or `edit` on any existing file
- **Never assume content**: Always check current file content before modifying
- **Preserve existing data**: Read the file first to avoid overwriting content
- **Check file existence**: Use `glob` or `read` to verify file exists before operations

**Why This is Critical**:
- The `write` tool completely overwrites existing files
- Using `read` first prevents accidental data loss
- Ensures you have the full context before making changes
- Required when updating PLAN.md, README.md, or any existing documentation

**Example Workflow**:
```bash
# WRONG - Direct write without reading
write filePath="PLAN.md" content="new content"

# CORRECT - Read first, then write/edit
read filePath="PLAN.md"
# Now you have the full context
edit filePath="PLAN.md" oldString="..." newString="..."
# OR
write filePath="PLAN.md" content="full updated content"
```

### Validation

- **Always validate YAML**: Check frontmatter syntax
- **Test the skill**: Try using it after creation
- **Review documentation**: Ensure clarity and completeness
- **Check naming**: Verify skill follows naming conventions
- **Update agents**: Never skip Step 8!
- **Always read before write**: Verify file content before modifying existing files

## Common Issues

### Invalid Skill Name

**Issue**: Skill name doesn't follow naming rules

**Solution**:
```bash
# Valid examples
python-pytest-creator ✓
nextjs-standard-setup ✓
linting-workflow ✓

# Invalid examples
PythonPytestCreator ✗ (uppercase)
python--pytest ✗ (double hyphens)
-python ✗ (leading hyphen)
python_ ✗ (underscore)
```

### YAML Validation Errors

**Issue**: Frontmatter has invalid YAML syntax

**Solution**:
- Check for proper indentation (2 spaces for lists)
- Ensure quotes around special characters
- Verify no trailing spaces after colons
- Use Python YAML validator:
  ```bash
  python3 -c "import yaml; yaml.safe_load(open('SKILL.md'))"
  ```

### Description Too Vague

**Issue**: Agents can't determine when to use the skill

**Solution**:
- Include specific frameworks or tools
- Mention target languages or domains
- Specify workflow type (testing, linting, etc.)
- Keep description between 50-150 characters

**Bad**: "Create tests for code"
**Good**: "Generate comprehensive pytest test files for Python using test-generator-framework"

### Agents Can't Find New Skill

**Issue**: New skill created but agents don't recognize it

**Solution**:
- **Did you run Step 8?** Always run opencode-skills-maintainer as final step
- Check if config.json was updated: `jq .agent["build-with-skills"].prompt config.json | grep "<skill-name>"`
- Manually invoke opencode-skills-maintainer if automated step failed
- Verify skill name matches frontmatter exactly

### Accidental Data Loss

**Issue**: File content overwritten when using `write` tool without reading first

**Solution**:
- **ALWAYS use `read` before `write` or `edit` on existing files**
- The `write` tool completely overwrites files without warning
- Always read the file first to see existing content
- Use `edit` for targeted changes when possible
- Only use `write` when you have the complete file content

**Example of What NOT To Do**:
```bash
# BAD - This overwrites everything!
write filePath="PLAN.md" content="just the new tasks"
```

**Correct Approach**:
```bash
# GOOD - Read first to preserve existing content
read filePath="PLAN.md"
# Now you have the full context
edit filePath="PLAN.md" oldString="old text" newString="new text"
```

**Common Files Requiring Read First**:
- **PLAN.md** - Contains task statuses that must be preserved
- **README.md** - Contains documentation structure
- **Existing SKILL.md** - Contains complete skill documentation
- **config.json** - Contains agent and MCP server configurations

## Verification Commands

After creating a skill, verify with these commands:

```bash
# 1. Check skill directory exists
ls -la skills/<skill-name>/

# 2. Verify SKILL.md exists
test -f skills/<skill-name>/SKILL.md && echo "✓ SKILL.md exists"

# 3. Validate YAML frontmatter
python3 -c "import yaml; yaml.safe_load(open('skills/<skill-name>/SKILL.md'))" && echo "✓ YAML valid"

# 4. Check required fields
grep "^name:" skills/<skill-name>/SKILL.md && echo "✓ Name field present"
grep "^description:" skills/<skill-name>/SKILL.md && echo "✓ Description field present"

# 5. Verify agents updated (CRITICAL!)
jq '.agent["build-with-skills"].prompt' config.json | grep -q "<skill-name>" && echo "✓ Build-With-Skills updated" || echo "❌ Build-With-Skills NOT updated"
jq '.agent["plan-with-skills"].prompt' config.json | grep -q "<skill-name>" && echo "✓ Plan-With-Skills updated" || echo "❌ Plan-With-Skills NOT updated"

# 6. If agents not updated, run maintainer
opencode --agent build-with-skills "Use opencode-skills-maintainer skill"
```

**Verification Checklist**:
- [ ] Skill name follows naming rules (1-64 chars, lowercase, single hyphens)
- [ ] SKILL.md file created in skills/<skill-name>/ directory
- [ ] YAML frontmatter is valid and complete
- [ ] "## What I do" section is present and descriptive
- [ ] "## When to use me" section is present and specific
- [ ] Optional sections added based on complexity
- [ ] **opencode-skills-maintainer was executed as final step**
- [ ] Build-With-Skills agent prompt includes new skill
- [ ] Plan-With-Skills agent prompt includes new skill
- [ ] Skill can be invoked and executes correctly
- [ ] **Read tool was used before modifying any existing files** (PLAN.md, README.md, etc.)

## Example Output

### Created Skill: python-pytest-creator

**Location**: `skills/python-pytest-creator/SKILL.md`

**Frontmatter**:
```yaml
---
name: python-pytest-creator
description: Generate comprehensive pytest test files for Python using test-generator-framework
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---
```

**Content Sections**:
- ✓ What I do (5 capabilities listed)
- ✓ When to use me (4 scenarios described)
- ✓ Prerequisites (3 requirements)
- ✓ Steps (8 detailed steps)
- ✓ Best Practices (5 guidelines)
- ✓ Verification Commands (6 commands)

**Agent Updates**:
- ✓ Build-With-Skills updated with python-pytest-creator
- ✓ Plan-With-Skills updated with python-pytest-creator
- ✓ Both agents have identical skill entries

**Validation**:
- ✓ YAML valid
- ✓ Required fields present
- ✓ Naming conventions followed
- ✓ Description is specific (78 characters)

## Related Skills

- **opencode-skills-maintainer**: Used as final step to update agents with new skills
- **opencode-agent-creation**: For creating new agents with similar best practices
- **opencode-skill-auditor**: For auditing and modularizing existing skills
