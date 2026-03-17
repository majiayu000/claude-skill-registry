---
description: Create a new Claude Code skill with proper structure and validation
argument-hint: <skill-name> [--location project|personal|ai] [--template minimal|full] [--resources "url1,url2"] [--skip-discovery] [--force-create]
allowed-tools: Read, Write, Bash(mkdir:*), Bash(python3:*), Bash(cat:*), Bash(ls:*), Bash(ccpm:*), Bash(command:*), Bash(cp:*), Bash(grep:*), WebFetch, WebSearch, AskUserQuestion, TodoWrite
---

# Create Claude Code Skill

Create a new skill with proper structure, SKILL.md frontmatter, and optional supporting resources. Before creating, search skill registries to determine if adoption is better than creation.

## Arguments

- `$1` - Skill name or topic (lowercase, hyphenated, max 40 chars). Example: `homebrew-formula`
- `--location` - Where to create the skill:
  - `project` (default): `.claude/skills/<skill-name>/`
  - `personal`: `~/.claude/skills/<skill-name>/`
  - `ai`: Create in aRustyDev/ai repo for distribution
- `--template` - Template type:
  - `minimal` (default): Just SKILL.md
  - `full`: SKILL.md + scripts/, references/, assets/ directories
- `--resources` - URLs to reference skills (comma-separated or from user message)
  - Parse URLs from user's message if provided inline
  - These supplement registry search results
  - Example: `--resources "url1,url2,url3"`
- `--skip-discovery` - Skip registry search, use only provided resources
- `--force-create` - Skip adopt/create assessment, proceed directly to creation

## Skill Registries

Search these registries for existing skills:

| Registry | URL Pattern | Priority |
|----------|-------------|----------|
| Claude Plugins | `https://claude-plugins.dev/skills?q=<query>` | Primary |
| Anthropic Skills | `https://github.com/anthropics/skills` | Reference |
| Awesome Claude | `https://github.com/anthropics/anthropic-cookbook` | Reference |

## Dependencies

**Recommended**: Install the `skills-search` skill for streamlined discovery:

```bash
ccpm install @daymade/claude-code-skills/skills-search
```

This provides `ccpm` CLI commands used throughout the discovery phase. If not installed, fall back to WebFetch for registry searches.

## Workflow

### Phase 0: Parse Arguments and Validate

**Use TodoWrite to track progress through phases.**

1. **Parse skill name/topic from $1**:
   - Extract skill name (everything before any flags)
   - Validate: lowercase, hyphenated, max 40 chars
   - Pattern: `^[a-z][a-z0-9-]{0,38}[a-z0-9]$`

2. **Parse optional flags**:
   - `--location`: Default to `project`
   - `--template`: Default to `minimal`
   - `--resources`: URLs provided explicitly
   - `--skip-discovery`: Boolean flag
   - `--force-create`: Boolean flag

3. **Parse resources from user message**:
   - Scan user's message for URLs matching skill registry patterns
   - Pattern: `https://claude-plugins.dev/skills/@[^/]+/[^/]+/[^/\s]+`
   - Add to resources list even if not in `--resources` flag
   - Example: If user says "Resources: url1, url2", extract those URLs

4. **Determine target directory**:
   ```bash
   case "$LOCATION" in
     project)  SKILL_DIR=".claude/skills/$SKILL_NAME" ;;
     personal) SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME" ;;
     ai)       SKILL_DIR="${AI_CONFIG_REPO:-$HOME/repos/configs/ai}/components/skills/$SKILL_NAME" ;;
   esac
   ```

5. **Check if skill already exists locally**:
   - If directory exists, ask user to confirm overwrite or choose different name

### Phase 0.5: Disambiguate Skill Purpose

**CRITICAL: Many skill topics are ambiguous. Clarify BEFORE doing any work.**

#### 0.5.1 Identify Ambiguous Topics

Check if the skill topic could have multiple interpretations:

| Topic Pattern | Possible Interpretations |
|---------------|-------------------------|
| `<tool>` (e.g., "docker", "terraform") | Develop tools vs Use tools vs Configure tools |
| `<framework>` (e.g., "react", "django") | Build apps vs Create components vs Test apps |
| `<platform>-<feature>` (e.g., "github-actions") | **Develop** actions vs **Write** workflows vs Manage settings |
| `<api/service>` (e.g., "stripe", "aws") | Build integrations vs Use SDK vs Deploy to |

#### 0.5.2 Common Ambiguous Topics

These topics ALWAYS require disambiguation:

```
github-actions    → Develop custom actions vs Write workflow YAML
terraform         → Write modules vs Use modules vs Manage state
docker            → Build images vs Run containers vs Compose services
kubernetes        → Develop operators vs Deploy apps vs Manage clusters
api               → Build APIs vs Consume APIs
cli               → Build CLI tools vs Use CLI tools
```

#### 0.5.3 Ask for Clarification

If topic is ambiguous, use AskUserQuestion:

```
The topic "<skill-name>" could mean different things:

1. **Developing <X>** - Building/creating new <X> (e.g., custom actions, modules, images)
2. **Using <X>** - Consuming/configuring existing <X> (e.g., workflows, providers, containers)
3. **Other** - Please specify

Which is your intent?
```

**Example for "github-actions":**
```
"GitHub Actions" could mean:

1. **Developing custom actions** - Building JS/TS, Docker, or Composite actions
   that others call with `uses:`
2. **Writing workflows** - Authoring .github/workflows/*.yml files that
   orchestrate jobs and call actions
3. **Other** - Please specify

Which is your intent?
```

#### 0.5.4 Record the Clarified Purpose

Store the clarified purpose for use in later phases:

```
SKILL_PURPOSE="Developing custom GitHub Actions (JS/TS, Docker, Composite)"
SKILL_NOT_ABOUT="Writing workflow YAML files, managing Actions settings"
```

**Do NOT proceed to Phase 1 without a clear, unambiguous purpose.**

### Phase 1: Discover Existing Skills

Search skill registries to find existing skills that match the requested topic.

**Skip this phase if `--skip-discovery` is set and resources were provided.**

#### 1.0 Check for ccpm availability

```bash
# Check if ccpm is available
command -v ccpm &> /dev/null && echo "ccpm available" || echo "ccpm not found"
```

If `ccpm` is available, use it for discovery. Otherwise, fall back to WebFetch.

#### 1.0.1 Merge user-provided resources

If user provided resources (via `--resources` or inline in message):
- Add them to the candidate list
- These take priority over registry search results
- Still search registry to find additional candidates

#### 1.1 Search Claude Plugins Registry

**With ccpm (preferred)**:
```bash
# Search for skills matching the topic
ccpm search "<skill-name-or-topic>" --limit 10 --json

# Search related terms
ccpm search "<related-term>" --limit 5 --json
```

**Fallback (WebFetch)**:
```
https://claude-plugins.dev/skills?q=<skill-name-or-topic>
```

Extract from results:
- Skill name and description
- Author/maintainer
- Download count or popularity indicators
- Tags

#### 1.2 Search Related Terms

Generate related search terms based on the skill name:
- Synonyms (e.g., `typescript` → `ts`, `javascript`)
- Related concepts (e.g., `react` → `frontend`, `components`)
- Broader categories (e.g., `eslint` → `linting`, `code-quality`)

Search for each related term to find skills the user might not have considered.

#### 1.3 Fetch Top Candidates

For the top 3-5 matching skills (plus all user-provided resources), get detailed information.

**IMPORTANT: Fetch all candidates in parallel using multiple WebFetch calls in a single message.**

**With ccpm (preferred)**:
```bash
# Get detailed skill info
ccpm info "@<author>/<repo>/<skill-name>"
```

**Fallback (WebFetch) - fetch in parallel**:
```
# Make multiple WebFetch calls simultaneously:
WebFetch(url1, "Extract SKILL.md content and patterns")
WebFetch(url2, "Extract SKILL.md content and patterns")
WebFetch(url3, "Extract SKILL.md content and patterns")
# ... all in same message for parallel execution
```

#### 1.3.1 Handle Fetch Failures

After parallel fetch, report results:

```
Fetched 3 resources:
✓ @author/skill-a - Full content retrieved
✗ @author/skill-b - 404 Not Found (description only)
✓ @author/skill-c - Full content retrieved
```

**If some resources fail**:
1. Report which failed and why
2. Use available content (descriptions still useful for context)
3. If ALL fail, ask user:
   - Provide alternative URLs?
   - Search registry for similar skills?
   - Proceed with default templates?

Extract and analyze from each successful fetch:
- SKILL.md content and structure
- Trigger phrases in description
- Skill type (workflow/reference/integration/automation)
- Supporting files (scripts/, references/, assets/)
- Quality indicators:
  - Clear documentation
  - Concrete examples
  - Active maintenance
  - Download count

#### 1.3.2 Synthesis Step

**Present extracted patterns to user before proceeding:**

```
## Patterns Extracted from Reference Skills

**Structure**:
- Overview → Prerequisites → Core Patterns → Examples → Troubleshooting

**Trigger phrases**:
- "Use when developing Workers..."
- "Use when configuring bindings..."

**Common sections**:
- Configuration reference
- Code patterns with TypeScript
- CLI commands

**Proceed with these patterns?** [Yes / Modify / Add more references]
```

#### 1.3.3 Validate Resource-Purpose Alignment

**CRITICAL: Verify fetched resources match the clarified purpose from Phase 0.5.**

After synthesis, check if the resources align with the stated skill purpose:

1. **Compare resource content to SKILL_PURPOSE**:
   - Do the patterns/topics match the user's intended purpose?
   - Are resources about "developing X" when user wants "developing X"?
   - Are resources about "using X" when user wants "using X"?

2. **Flag misalignment if detected**:

```
⚠ Resource-Purpose Mismatch Detected

Your stated purpose: "Developing custom GitHub Actions"
Resources appear to be about: "Writing GitHub Actions workflows"

The fetched resources discuss:
- Workflow YAML syntax
- Job configuration
- Reusable workflows (workflow_call)

But your stated purpose is about:
- Building custom actions (action.yml)
- @actions/core toolkit
- Publishing to Marketplace

Options:
1. Search for resources matching your actual purpose
2. Proceed anyway (resources provide context but not templates)
3. Clarify your intent (maybe you want both?)
```

3. **If mismatch confirmed**:
   - Search registry with refined terms (e.g., "action development", "custom action", "action toolkit")
   - Ask user for alternative resource URLs
   - Note that existing resources may still inform structure but not content

**Do NOT proceed to Phase 2 if resources fundamentally mismatch the purpose.**

#### 1.4 Check Local Skills

**With ccpm (preferred)**:
```bash
# List installed skills
ccpm list
```

**Fallback (manual check)**:
```bash
# Project skills
ls -la .claude/skills/

# Personal skills
ls -la ~/.claude/skills/

# AI config library
ls -la "${AI_CONFIG_REPO:-$HOME/repos/configs/ai}/components/skills/"
```

### Phase 2: Assess Adopt vs Create

Present findings and recommend an approach.

**Skip this phase if `--force-create` is set. Proceed directly to Phase 3 using discovered skills as references.**

#### 2.1 Scoring Criteria

Score each discovered skill (0-10 for each criterion):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Relevance** | 3x | How closely does it match the requested functionality? |
| **Quality** | 2x | Is it well-documented with examples? |
| **Completeness** | 2x | Does it cover the full use case? |
| **Maintenance** | 1x | Is it actively maintained? |
| **Extensibility** | 1x | Can it be extended if needed? |

**Adopt threshold**: Total weighted score >= 70/100

#### 2.2 Present Options to User

Use AskUserQuestion to present findings:

**If strong match found (score >= 70)**:
```
Found existing skill that matches your needs:

📦 @author/skill-name (score: 85/100)
   "Description of the skill..."
   ✓ Covers: feature1, feature2, feature3
   ✗ Missing: feature4 (minor)

Recommendation: Adopt this skill

Options:
1. Adopt existing skill (install it)
2. Adopt + Extend (install and customize locally)
3. Create new skill (use existing as reference)
4. Create from scratch (ignore existing)
```

**If partial matches found (score 40-69)**:
```
Found related skills that partially match:

📦 @author/skill-a (score: 55/100)
   Good for: X, Y
   Missing: Z

📦 @author/skill-b (score: 48/100)
   Good for: Y, Z
   Missing: X

Recommendation: Create new skill using these as reference

Options:
1. Adopt skill-a and extend it
2. Adopt skill-b and extend it
3. Create new skill (use both as reference) [Recommended]
4. Create from scratch
```

**If no matches found (score < 40)**:
```
No existing skills found for "<skill-name>".

Proceeding to create new skill from scratch.
```

#### 2.3 Handle User Choice

Based on user selection:

| Choice | Action |
|--------|--------|
| **Adopt** | Install skill via ccpm, skip to Phase 8 |
| **Adopt + Extend** | Install skill, copy to local for modifications |
| **Create with reference** | Continue to Phase 3, use discovered skills as templates |
| **Create from scratch** | Continue to Phase 3, use default templates |

**Adopt workflow (with ccpm)**:
```bash
# Install the skill
ccpm install "@<author>/<repo>/<skill-name>"

# Verify installation
ccpm list | grep "<skill-name>"
```

**Adopt + Extend workflow**:
```bash
# Install first
ccpm install "@<author>/<repo>/<skill-name>"

# Copy to local location for customization
cp -r ~/.claude/skills/<skill-name> "$SKILL_DIR"

# User can now modify the local copy
```

### Phase 3: Confirm Skill Purpose and Scope

**THIS PHASE IS MANDATORY. NEVER SKIP IT.**

Even when:
- Continuing from previous context
- Resources seem clear
- User seems impatient
- `--force-create` is set (still confirm purpose, just skip adopt/create assessment)

#### 3.1 Present Inferred Information

Use the clarified purpose from Phase 0.5 and patterns from Phase 1:

```
## Confirm Skill Purpose

Based on our discussion and reference analysis:

| Field | Value |
|-------|-------|
| **Skill Name** | `<skill-name>` |
| **Purpose** | <SKILL_PURPOSE from Phase 0.5> |
| **This skill IS about** | <specific focus areas> |
| **This skill is NOT about** | <SKILL_NOT_ABOUT from Phase 0.5> |
| **Type** | reference + integration |
| **Trigger Phrases** | "create X", "configure Y", "deploy Z" |

Is this correct? [Yes / Modify]
```

**Example for github-actions:**
```
## Confirm Skill Purpose

| Field | Value |
|-------|-------|
| **Skill Name** | `github-actions` |
| **Purpose** | Developing custom GitHub Actions |
| **This skill IS about** | Building JS/TS actions, Docker actions, Composite actions, action.yml, @actions toolkit, Marketplace publishing |
| **This skill is NOT about** | Writing workflow YAML files, configuring workflow triggers, job matrices |
| **Type** | reference + workflow |
| **Trigger Phrases** | "create a GitHub Action", "build custom action", "publish to Marketplace" |

Is this correct? [Yes / Modify]
```

#### 3.2 Handle Modifications

If user wants to modify:
1. Ask which field(s) to change
2. Update the values
3. Re-present for confirmation
4. Loop until confirmed

#### 3.3 Skill Type Selection

If not already clear, ask via AskUserQuestion:

1. **Skill Type**:
   - `workflow` - Step-by-step procedures
   - `reference` - Documentation/lookup capability
   - `integration` - Tool/API integration
   - `automation` - Script-based automation

**Only proceed to Phase 4 after explicit confirmation.**

### Phase 4: Create Directory Structure

1. **Create skill directory**:
   ```bash
   mkdir -p "$SKILL_DIR"
   ```

2. **For full template, create subdirectories**:
   ```bash
   mkdir -p "$SKILL_DIR/scripts"
   mkdir -p "$SKILL_DIR/references"
   mkdir -p "$SKILL_DIR/assets"
   ```

### Phase 5: Generate SKILL.md

Create SKILL.md informed by reference skills (if any).

#### 5.1 Analyze Reference Skills

If reference skills were selected, extract patterns:

- **Structure**: How do they organize sections?
- **Trigger phrases**: What description patterns work well?
- **Code examples**: What formats do they use?
- **Best practices**: What conventions do they follow?

#### 5.2 Generate Frontmatter

```yaml
---
name: <skill-name>
description: <purpose>. This skill should be used when the user asks to '<trigger-phrase-1>', '<trigger-phrase-2>', or '<trigger-phrase-3>'.
---
```

#### 5.3 Generate Body

Use the appropriate template based on skill type, enhanced with patterns from reference skills.

**IMPORTANT: For ambiguous topics, include a "Not About" section in the Overview.**

**Workflow Type**:
```markdown
# <Skill Name>

## Overview
<Brief description informed by reference skills>

**This skill covers:**
- <Focus area 1>
- <Focus area 2>

**This skill does NOT cover:**
- <SKILL_NOT_ABOUT item 1>
- <SKILL_NOT_ABOUT item 2>
- See `<other-skill>` for that

## Prerequisites
<Required tools/setup>

## Workflow

### Step 1: <First Step>
<Instructions in imperative form>

### Step 2: <Second Step>
<Instructions in imperative form>

## Examples
<Concrete examples, modeled after reference skills>

## Troubleshooting
<Common issues and solutions>
```

**Reference Type**:
```markdown
# <Skill Name>

## Overview
<Brief description>

## Quick Reference
<Most commonly needed information>

## Detailed Reference
<Comprehensive documentation>

## See Also
- Reference: [topic.md](references/topic.md)
```

**Integration Type**:
```markdown
# <Skill Name>

## Overview
<Brief description>

## Configuration
<Setup instructions>

## API/Tool Usage
<Interaction patterns>

## Examples
<Usage examples>
```

**Automation Type**:
```markdown
# <Skill Name>

## Overview
<Brief description>

## Scripts

### <script-name>.py
<Script description and usage>

## Workflow
<How to use the automation>
```

### Phase 6: Create Supporting Files (Full Template Only)

If `--template full`, create files informed by reference skills:

1. **Scripts**: Based on patterns from reference skills or placeholders
2. **References**: Detailed documentation extracted/adapted from references
3. **Assets**: Templates, config files, etc.

### Phase 7: Validate Skill Structure

1. **Check SKILL.md exists and has valid frontmatter**

2. **Validate fields**:
   - `name` matches directory name
   - `description` includes trigger phrases
   - Description under 1024 characters

3. **Check line count**:
   ```bash
   LINES=$(wc -l < "$SKILL_DIR/SKILL.md")
   if [ "$LINES" -gt 500 ]; then
     echo "Warning: SKILL.md is $LINES lines (recommended: <500)"
     echo "Consider moving detailed content to references/"
   fi
   ```

   **If over 500 lines**: Identify sections to extract to references/ and refactor

4. **Check quality**:
   - Uses imperative form
   - No placeholder text remaining (ignore TypeScript generics like `<T>`)
   - Examples are concrete
   - File references in "See Also" are valid

5. **Report validation results**:
   ```
   Validation Results:
   ✓ Frontmatter valid
   ✓ Description: 281 chars
   ⚠ Lines: 526 (consider refactoring)
   ✓ No placeholders
   ✓ References exist
   ```

### Phase 8: Report Results

**If adopted**:
```
## Skill Adopted

| Item | Value |
|------|-------|
| Skill | `@author/skill-name` |
| Source | claude-plugins.dev |
| Action | Installed to <location> |

To customize: Edit `<path>/SKILL.md`
```

**If created**:
```
## Skill Created

| Item | Value |
|------|-------|
| Skill Name | `<skill-name>` |
| Location | `<skill-directory>` |
| Template | `<minimal|full>` |
| Reference Skills | `@author/skill-a`, `@author/skill-b` |
| Files Created | `<list>` |

**Next Steps:**
1. Review and customize SKILL.md
2. Test with trigger phrases
3. Optionally promote: `/promote-skill <path>`
```

## Example Usage

### Search and Create
```
/create-skill typescript-dev
```

1. Searches registries for TypeScript-related skills
2. Finds `@wshobson/agents/typescript-advanced-types`, `@blencorp/claude-code-kit/react`
3. User chooses "Create with reference"
4. Creates new skill using patterns from discovered skills

### Create with User-Provided Resources
```
User: Create a skill for TypeScript development
Resources:
    - https://claude-plugins.dev/skills/@diet103/claude-code-infrastructure-showcase/frontend-dev-guidelines
    - https://claude-plugins.dev/skills/@wshobson/agents/typescript-advanced-types

/create-skill typescript-dev --template full
```

1. Parses URLs from user's message automatically
2. Fetches all provided resources in parallel
3. Skips or supplements registry search with these
4. Uses all resources as references for creation

### Skip Discovery, Use Only Provided Resources
```
/create-skill my-skill --resources "url1,url2" --skip-discovery --force-create
```

1. Skips registry search entirely
2. Fetches only the provided URLs
3. Skips adopt/create assessment
4. Proceeds directly to creation using provided skills as templates

### Force Create from Scratch
```
/create-skill my-custom-workflow --template full --force-create
```

1. Searches registry (unless --skip-discovery)
2. Skips adopt/create assessment
3. Uses any found skills as references
4. Proceeds directly to creation

### Adopt Existing
```
/create-skill docker
```

1. Finds `@author/docker-compose` (score: 92/100)
2. User chooses "Adopt"
3. Installs via `ccpm install`

## Best Practices Checklist

- [ ] Disambiguated skill purpose if topic was ambiguous (Phase 0.5)
- [ ] Searched registries before creating
- [ ] Validated resources match intended purpose (Phase 1.3.3)
- [ ] Evaluated adopt vs create tradeoffs
- [ ] Confirmed skill purpose and scope with user (Phase 3 - mandatory)
- [ ] Used reference skills to inform structure
- [ ] Description includes specific trigger phrases
- [ ] Included "Not About" section for ambiguous topics
- [ ] Instructions use imperative form
- [ ] SKILL.md under 500 lines
- [ ] No placeholder content remains
- [ ] Examples are concrete and runnable

## Related Commands

- `/promote-skill` - Promote a project skill to the ai config library
- `/validate-skill` - Validate an existing skill structure

## Notes

- Always search before creating to avoid reinventing the wheel
- High-quality existing skills are often better than new mediocre ones
- Adopt + Extend is a good middle ground for customization needs
- Reference skills help ensure consistent quality and patterns

## Interrupt Recovery

When the user corrects the skill purpose or scope during generation:

### 1. Acknowledge the Correction

```
I understand - you want a skill about <corrected purpose>, not <what I was building>.
Let me adjust.
```

### 2. Assess What to Preserve

| Component | Preserve? | Notes |
|-----------|-----------|-------|
| Directory structure | ✓ Yes | Unchanged |
| SKILL.md | ✗ Regenerate | Content was wrong |
| references/ | ? Partial | Keep if still relevant |
| scripts/ | ? Partial | Keep if still relevant |
| assets/ | ? Partial | Keep if still relevant |

### 3. Regenerate Affected Content

1. Update SKILL_PURPOSE and SKILL_NOT_ABOUT
2. Do NOT restart from Phase 0 (arguments are still valid)
3. Optionally search for new resources matching corrected purpose
4. Regenerate SKILL.md with correct focus
5. Update or remove irrelevant supporting files
6. Re-validate

### 4. Confirm Before Proceeding

After regeneration, re-confirm with user:

```
I've regenerated the skill with the corrected focus:

| Field | New Value |
|-------|-----------|
| Purpose | <corrected purpose> |
| Focus | <what it now covers> |
| Not About | <what it excludes> |

Does this look correct now?
```

### 5. Learn from the Correction

Note what caused the misunderstanding:
- Was the topic inherently ambiguous?
- Did resources mislead the interpretation?
- Was Phase 0.5 skipped or insufficient?

Consider whether the command itself needs updating to prevent similar issues.
