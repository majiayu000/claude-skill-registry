---
name: plugin-create
description: Create new marketplace components (agents, commands, skills, bundles) with proper structure and standards compliance
user-invocable: true
allowed-tools: Read, Write, Bash, AskUserQuestion, Skill
---

# Plugin Create Skill

Interactive wizard for creating well-structured Claude Code marketplace components following architecture best practices.

## What This Skill Provides

**Component Creation**: Unified workflows for creating agents, commands, skills, and bundles with proper structure, frontmatter, and standards compliance.

**Validation**: Automated validation of component structure, frontmatter format, and architecture compliance.

**Templates**: Consistent templates for all component types with proper sections and formatting.

**Duplication Detection**: Prevents creating duplicate components by checking existing components in target bundle.

## Pattern Type

**Pattern 5 + Pattern 6**: Wizard-Style Workflow + Template-Based Generation

- Pattern 5: Interactive questionnaires with validation
- Pattern 6: Fill templates with user answers and generate files

## When to Use This Skill

Activate when creating:
- **New agents** - Focused task executors
- **New commands** - User-facing utilities and orchestrators
- **New skills** - Standards and knowledge repositories
- **New bundles** - Component collections with plugin.json

## Workflows

This skill provides 4 workflows, one for each component type. All workflows follow the same pattern:
1. Interactive questionnaire with validation
2. Duplication detection
3. Generate component from template
4. Validate generated component
5. Display summary with statistics
6. Run post-creation diagnosis

### Workflow 1: create-agent

**Parameters**:
- `scope` - Where to create (marketplace/global/project, default: marketplace)
- `bundle` - Target bundle (optional, will prompt if not provided)

**Steps**:

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:ref-development-standards
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Architecture Standards

```
Read references/agent-guide.md
```

This provides agent design principles, tool selection guidelines, and architecture rules.

#### Step 2: Interactive Questionnaire

Ask user for:

**A. Agent name** (kebab-case validation)
- Validation: Must match kebab-case pattern
- Error if invalid: "Agent name must be kebab-case (lowercase-with-hyphens)" and retry

**B. Bundle selection**
- List available bundles using Glob
- Validation: Must select valid bundle from list
- Error if invalid: "Please select a bundle from the list" and retry

**C. Description** (one sentence, <100 chars)
- Validation: Must not be empty, ≤100 chars
- Error if invalid: "Description required (max 100 chars): {current_length}/100" and retry

**D. Agent type**
1. Analysis agent (code review, diagnostics)
2. Execution agent (build, test, deploy)
3. Coordination agent (multi-step workflows)
4. Research agent (information gathering)
- Validation: Must select 1-4
- Error if invalid: "Please select agent type (1-4)" and retry

**E. Detailed capabilities** (what agent does)
- Validation: Must not be empty
- Error if empty: "Agent capabilities description required" and retry

**F. Required tools** (which tools agent needs)
- Examples: Read, Write, Edit, Glob, Grep, Bash, WebFetch
- Validation: Must list at least one tool
- Error if none: "At least one tool required" and retry
- **CRITICAL Validation - Task Tool**:
  - If user lists `Task`: ERROR
  - Message: "Agents CANNOT use Task tool (Rule 6) - unavailable at runtime. Create a COMMAND instead if delegation needed."
  - Force removal from list or abort
- **CRITICAL Validation - Maven Execution**:
  - If user lists `Bash` AND agent name ≠ "maven-builder":
  - Prompt: "Does this agent need to execute Maven commands?"
  - If yes: ERROR "Only maven-builder agent may execute Maven (Rule 7)"
  - If no: Continue

**G. When should agent be used** (trigger conditions)
- Validation: Must provide use cases
- Error if empty: "Usage conditions required" and retry

**H. Expected inputs/outputs**
- Validation: Must describe inputs and outputs
- Error if empty: "Input/output description required" and retry

Track `questions_answered` counter.

#### Step 3: Duplication Detection and Architecture Validation

**Check for duplicates:**
1. Use Glob to find all agents in target bundle
2. Use Grep to search for similar names/descriptions
3. If duplicates found:
   - Display: "⚠️ Similar agents found: {list with descriptions}"
   - Prompt: "[C]ontinue anyway/[R]ename agent/[A]bort creation?"
   - If rename: Return to Step 2A
   - If abort: Exit workflow
   - Track in `duplication_checks` counter

**Validate architecture compliance:**
- Self-contained (no cross-agent dependencies)
- Proper tool fit (agent needs listed tools)
- No prohibited tools (Task, Maven for non-maven-builder)

Track `validations_performed` counter.

#### Step 4: Generate Agent File

**Generate frontmatter:**
```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component generate --type "agent" --config "{answers_json}"
```

Where answers_json contains:
```json
{
  "name": "agent-name",
  "description": "One sentence description",
  "model": "optional_model_name",
  "tools": ["Tool1", "Tool2", "Tool3"]
}
```

**Load template:**
```
Read assets/templates/agent-template.md
```

**Fill template** with:
- Generated frontmatter
- Agent name (title case for heading)
- Purpose statement from capabilities
- Workflow steps (numbered, based on agent type)
- Tool usage guidance
- Critical rules (based on selected tools)
- CONTINUOUS IMPROVEMENT RULE with 3-5 improvement areas specific to agent type

**CRITICAL - CONTINUOUS IMPROVEMENT RULE Pattern**:
Agent template MUST use pattern:
```markdown
## CONTINUOUS IMPROVEMENT RULE

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with:
   - Component: `{type: "agent", name: "{agent-name}", bundle: "{bundle}"}`
   - Category: bug | improvement | pattern | anti-pattern
   - Summary and detail of the finding
```

**Write file:**
```
Write: {bundle}/agents/{agent-name}.md
```

Track `files_created` counter.

#### Step 5: Validate Generated Component

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component validate --file "{file_path}" --type "agent"
```

Validation checks:
- Frontmatter format correct (comma-separated tools)
- No Task tool present
- CONTINUOUS IMPROVEMENT RULE uses manage-lessons skill pattern
- All required sections present

If validation fails: Display errors and prompt "[R]etry generation/[A]bort"

Track `validations_performed` counter.

#### Step 6: Display Summary

```
╔════════════════════════════════════════════════════════════╗
║          Agent Created Successfully                        ║
╚════════════════════════════════════════════════════════════╝

Agent: {agent-name}
Location: {file-path}
Bundle: {bundle-name}
Type: {agent-type}

Statistics:
- Questions answered: {questions_answered}
- Validations performed: {validations_performed}
- Duplication checks: {duplication_checks}
- Files created: {files_created}

Next steps:
1. Review agent file: {file-path}
2. Run diagnosis: /plugin-doctor agents agent-name={agent-name}
3. Test agent functionality
```

#### Step 7: Run Agent Diagnosis

```
SlashCommand: /pm-plugin-development:plugin-doctor agents agent-name={agent-name}
```

If diagnosis fails: Display warning but don't abort (agent already created).

### Workflow 2: create-command

**Parameters**:
- `scope` - Where to create (marketplace/global/project, default: marketplace)
- `bundle` - Target bundle (optional, will prompt if not provided)

**Steps**:

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:ref-development-standards
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Command Standards

```
Read references/command-guide.md
```

This provides command design principles, quality standards, and orchestration patterns.

#### Step 2: Interactive Questionnaire

Ask user for:

**A. Command name** (kebab-case with verb)
- Validation: Must match kebab-case pattern, should start with verb
- Error if invalid: "Command name must be kebab-case starting with verb (e.g., create-agent)" and retry

**B. Bundle selection** (same as agent workflow)

**C. Description** (one sentence, <100 chars)

**D. Command type**
1. Orchestration (coordinates agents/commands)
2. Diagnostic (analyzes and reports)
3. Interactive (user questionnaire)
4. Automation (executes workflow)
- Validation: Must select 1-4

**E. Parameters** (what parameters command accepts)
- Can be empty for commands with no parameters
- Prompt: "List parameters (comma-separated) or press Enter if none"

**F. Workflow steps** (main steps command performs)
- Validation: Must provide at least 2 steps
- Error if <2: "Command requires at least 2 workflow steps" and retry

**G. Tool requirements** (which tools needed)
- Validation: Must list at least one tool OR "none" for orchestration-only
- Error if empty: "Specify tools needed or 'none' for orchestration-only" and retry

Track `questions_answered` counter.

#### Step 3: Duplication Detection

Same pattern as agent workflow, using Glob/Grep to find similar commands.

#### Step 4: Generate Command File

**Generate frontmatter:**
```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component generate --type "command" --config "{answers_json}"
```

**Load template:**
```
Read assets/templates/command-template.md
```

**Fill template** with:
- Generated frontmatter (name, description only - no tools)
- Command overview
- CONTINUOUS IMPROVEMENT RULE with command-specific improvements
- PARAMETERS section (if applicable)
- WORKFLOW section (numbered steps)
- CRITICAL RULES section
- USAGE EXAMPLES section
- RELATED section

**CONTINUOUS IMPROVEMENT RULE for commands:**
```markdown
## CONTINUOUS IMPROVEMENT RULE

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with:
   - Component: `{type: "command", name: "{command-name}", bundle: "{bundle}"}`
   - Category: bug | improvement | pattern | anti-pattern
   - Summary and detail of the finding
```

**Write file:**
```
Write: {bundle}/commands/{command-name}.md
```

Track `files_created` counter.

#### Step 5: Validate Generated Component

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component validate --file "{file_path}" --type "command"
```

Validation checks:
- Frontmatter format correct
- All required sections present (WORKFLOW, USAGE EXAMPLES)
- CONTINUOUS IMPROVEMENT RULE uses manage-lessons skill pattern

#### Step 6: Display Summary

Same format as agent workflow.

#### Step 7: Run Command Diagnosis

```
SlashCommand: /pm-plugin-development:plugin-doctor commands command-name={command-name}
```

### Workflow 3: create-skill

**Parameters**:
- `scope` - Where to create (marketplace/global/project, default: marketplace)
- `bundle` - Target bundle (optional, will prompt if not provided)

**Steps**:

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:ref-development-standards
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Skill Standards

```
Read references/skill-guide.md
```

This provides skill patterns, resource organization, and progressive disclosure guidance.

#### Step 2: Interactive Questionnaire

Ask user for:

**A. Skill name** (kebab-case, descriptive)
- Example: `java-unit-testing-patterns`
- Validation: Must match kebab-case pattern

**B. Bundle selection** (same as agent workflow)

**C. Short description** (1 sentence, <100 chars)

**D. Detailed description** (2-3 sentences, what standards/knowledge skill provides)
- Validation: Must be at least 100 chars
- Error if too short: "Detailed description must be at least 100 characters: {current_length}/100" and retry

**E. Skill type**
1. Standards skill (provides coding/process standards)
2. Reference skill (provides reference material)
3. Diagnostic skill (provides diagnostic patterns/tools)
- Validation: Must select 1-3

**F. Standards categories** (if standards skill)
- What domains does this cover? (e.g., Java, Testing, Documentation)

**G. Target audience**
- Who uses these standards? (developers, documentation writers, etc.)

**H. Standards files** (what standards files will be included)
- Prompt user to list main standards documents
- Suggest organization structure based on categories

Track `questions_answered` counter.

#### Step 3: Duplication Detection

Same pattern, using Glob/Grep to find similar skills.

#### Step 4: Create Skill Structure

**Create directories:**
```
bash mkdir -p {bundle}/skills/{skill-name}/standards
```

**Generate SKILL.md:**

Generate frontmatter:
```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component generate --type "skill" --config "{answers_json}"
```

Load template:
```
Read assets/templates/skill-template.md
```

Fill template with:
- Generated frontmatter
- Overview
- What This Skill Provides
- When to Activate
- Workflow (how to use standards)
- Standards Organization (list of standards files)
- Tool Access requirements

Write SKILL.md:
```
Write: {bundle}/skills/{skill-name}/SKILL.md
```

**Generate README.md:**

Create skill overview README with:
- Skill overview
- Standards list
- Usage examples
- Integration notes

Write README:
```
Write: {bundle}/skills/{skill-name}/README.md
```

**Create placeholder standards files:**

For each standards file user specified:
```
Write: {bundle}/skills/{skill-name}/standards/{file-name}.md
```

With placeholder content:
```markdown
# {Title}

[Content to be added]

## Overview

## Standards

## References
```

Track `files_created` and `standards_files_created` counters.

#### Step 5: Validate Generated Component

```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component validate --file "{skill_path}/SKILL.md" --type "skill"
```

Validation checks:
- Frontmatter format correct
- SKILL.md structure valid
- No CONTINUOUS IMPROVEMENT RULE (skills don't have this)

#### Step 6: Display Summary

```
╔════════════════════════════════════════════════════════════╗
║          Skill Created Successfully                        ║
╚════════════════════════════════════════════════════════════╝

Skill: {skill-name}
Location: {file-path}
Bundle: {bundle-name}
Type: {skill-type}

Statistics:
- Questions answered: {questions_answered}
- Validations performed: {validations_performed}
- Duplication checks: {duplication_checks}
- Files created: {files_created}
- Standards files created: {standards_files_created}

Next steps:
1. Review skill file: {file-path}
2. Populate standards files in standards/ directory
3. Run diagnosis: /plugin-doctor skills skill-name={skill-name}
4. Test skill activation
```

#### Step 7: Run Skill Diagnosis

```
SlashCommand: /pm-plugin-development:plugin-doctor skills skill-name={skill-name}
```

### Workflow 4: create-bundle

**Parameters**:
- `scope` - Where to create (marketplace/global/project, default: marketplace)

**Steps**:

#### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:ref-development-standards
```

These provide architecture principles and non-prompting tool usage patterns.

#### Step 1: Load Bundle Standards

```
Read references/bundle-guide.md
```

This provides bundle structure requirements, plugin.json configuration, naming conventions, and validation guidelines.

#### Step 2: Interactive Questionnaire

Ask user for:

**A. Bundle name** (kebab-case)
- Example: `java-development-standards`
- Validation: Must match kebab-case pattern

**B. Display name** (human-readable)
- Example: "Java Development Standards"

**C. Description** (one sentence)

**D. Version** (semantic version, default: 1.0.0)

**E. Author** (bundle author name)

**F. Bundle type**
1. Standards bundle (provides development standards)
2. Tool bundle (provides commands/agents)
3. Mixed bundle (standards + tools)
- Validation: Must select 1-3

**G. Initial components**
- Skills? (y/n) - If yes, how many initially?
- Commands? (y/n) - If yes, how many initially?
- Agents? (y/n) - If yes, how many initially?

Track `questions_answered` counter.

#### Step 3: Create Bundle Structure

**Load bundle structure template:**
```
Read assets/templates/bundle-structure.json
```

Use this template for directories and plugin.json structure.

**Create directories:**
```
bash mkdir -p {scope}/bundles/{bundle-name}/{skills,commands,agents}
```

**Generate plugin.json:**

Create plugin.json using template from bundle-structure.json:
```json
{
  "name": "bundle-name",
  "display_name": "Display Name",
  "description": "Bundle description",
  "version": "1.0.0",
  "author": "Author Name",
  "components": []
}
```

Write:
```
Write: {scope}/bundles/{bundle-name}/plugin.json
```

**Generate README.md:**

Create bundle README with:
- Bundle overview and purpose
- What this bundle provides
- Components list (initially empty)
- Installation instructions
- Usage examples
- Integration notes

Write:
```
Write: {scope}/bundles/{bundle-name}/README.md
```

**Create component READMEs** (if requested):
```
Write: {scope}/bundles/{bundle-name}/skills/README.md
Write: {scope}/bundles/{bundle-name}/commands/README.md
Write: {scope}/bundles/{bundle-name}/agents/README.md
```

Track `files_created` counter.

#### Step 4: Create Initial Components

For each component type user requested:

**Skills**: For each skill count:
```
# Recursively invoke workflow 3 (create-skill)
# Pass scope and bundle-name parameters
```

**Commands**: For each command count:
```
# Recursively invoke workflow 2 (create-command)
# Pass scope and bundle-name parameters
```

**Agents**: For each agent count:
```
# Recursively invoke workflow 1 (create-agent)
# Pass scope and bundle-name parameters
```

#### Step 5: Update plugin.json

After components created, read plugin.json and update components array with created items.

Track `components_created` counter.

#### Step 6: Display Summary

```
╔════════════════════════════════════════════════════════════╗
║          Bundle Created Successfully                       ║
╚════════════════════════════════════════════════════════════╝

Bundle: {bundle-name}
Location: {bundle-path}
Type: {bundle-type}

Components created:
- Skills: {skills_count}
- Commands: {commands_count}
- Agents: {agents_count}

Statistics:
- Questions answered: {questions_answered}
- Files created: {files_created}

Next steps:
1. Review bundle: {bundle-path}
2. Add more components: Use /plugin-create
3. Test bundle
4. Run diagnosis: /plugin-doctor metadata
```

#### Step 7: Run Metadata Validation

```
SlashCommand: /pm-plugin-development:plugin-doctor metadata
```

Review results and offer to fix any metadata issues found.

## References

This skill uses the following reference files (load on-demand):

### Agent Creation
- **agent-guide.md** - Agent design principles, tool selection, architecture rules

### Command Creation
- **command-guide.md** - Command design principles, quality standards, orchestration patterns

### Skill Creation
- **skill-guide.md** - Skill patterns, resource organization, progressive disclosure

### Bundle Creation
- **bundle-guide.md** - Bundle structure, plugin.json configuration, naming conventions

## Scripts

Script: `pm-plugin-development:plugin-create` → `component.py`

| Subcommand | Purpose |
|------------|---------|
| `validate` | Validates marketplace component structure |
| `generate` | Generates YAML frontmatter for components |

### component.py validate
**Purpose**: Validates marketplace component structure

**Usage**:
```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component validate --file <file_path> --type <component_type>
```

**Output**: JSON with validation results

### component.py generate
**Purpose**: Generates YAML frontmatter for components

**Usage**:
```bash
python3 .plan/execute-script.py pm-plugin-development:plugin-create:component generate --type <component_type> --config '<answers_json>'
```

**Output**: Formatted YAML frontmatter string

## Templates

This skill uses the following templates in assets/templates/:

- **agent-template.md** - Template for new agents
- **command-template.md** - Template for new commands
- **skill-template.md** - Template for new skills (SKILL.md)
- **bundle-structure.json** - Bundle directory structure template

## Critical Rules

**Frontmatter Format**:
- ALWAYS use comma-separated format for tools: `tools: Read, Write, Edit`
- NEVER use array syntax: `tools: [Read, Write, Edit]`

**Tool Prohibitions**:
- Agents CANNOT use Task tool (Rule 6) - unavailable at runtime
- Only maven-builder agent can execute Maven (Rule 7)

**CONTINUOUS IMPROVEMENT RULE**:
- Agents: Use manage-lessons skill to record lessons (report to caller)
- Commands: Use manage-lessons skill to record lessons
- Skills: No CONTINUOUS IMPROVEMENT RULE

**Validation**:
- ALL questionnaire responses must be validated
- Clear error messages with retry prompts
- Check for duplicates before creating

**Progressive Disclosure**:
- Load reference guides on-demand (never load all at once)
- Use relative paths for all resources

## Quality Standards

Following these ensures:
- Consistent component structure across marketplace
- Proper frontmatter formatting
- Architecture compliance
- No duplicate components
- Validated creation with post-diagnosis
- Statistics tracking for transparency
