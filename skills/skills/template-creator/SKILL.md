---
name: template-creator
description: Creates and manages templates for agents, skills, workflows, hooks, and code patterns. Ensures consistency across the framework. Use when creating new template types or standardizing patterns.
version: 2.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
# Phase 1 Integration: Template tools validated against .claude/config/tool-manifest.json
# Templates should reference tools from the manifest for consistency
# Single source of truth: .claude/config/tool-manifest.json
assigned_agents: []
best_practices:
  - Include all required fields with placeholders
  - Add documentation comments in templates
  - Version templates for tracking changes
  - Include validation examples
  - Use consistent placeholder format
error_handling: graceful
streaming: supported
output_location: .claude/templates/
---

# Template Creator Skill

Creates and manages templates for agents, skills, workflows, hooks, and code patterns. Ensures consistency across the multi-agent framework through standardized structures.

## ROUTER UPDATE REQUIRED (CRITICAL - DO NOT SKIP)

**After creating ANY template, you MUST update the appropriate documentation:**

```
1. Update .claude/templates/README.md with new template type
2. Update CLAUDE.md Section 8.5 if user-invocable
3. Update learnings.md with creation summary
```

**Verification:**

```bash
grep "<template-name>" .claude/templates/README.md || echo "ERROR: README NOT UPDATED!"
```

**WHY**: Templates not documented are invisible to other creators and will never be used.

---

## Overview

Templates ensure consistency across the multi-agent framework. This skill creates templates for:

- **Agent definitions** - Standardized agent structures
- **Skill definitions** - Reusable capability patterns
- **Workflow definitions** - Multi-agent orchestration patterns
- **Hook implementations** - Pre/post execution hooks
- **Code patterns** - Language-specific scaffolding

**Core principle:** Templates are the DNA of the system. Consistent templates produce consistent, predictable agents and skills.

## When to Use

**Always:**

- Creating a new type of artifact that will be replicated
- Standardizing an existing pattern across the codebase
- Adding a new template category (hooks, schemas, etc.)
- Improving existing templates with better patterns

**Exceptions:**

- One-off files that will never be replicated
- Temporary/throwaway code

## Template Types

| Type     | Location                       | Purpose                          | Key Fields                              |
| -------- | ------------------------------ | -------------------------------- | --------------------------------------- |
| Agent    | `.claude/templates/agents/`    | Agent definition templates       | name, description, tools, skills, model |
| Skill    | `.claude/templates/skills/`    | Skill definition templates       | name, version, tools, invoked_by        |
| Workflow | `.claude/templates/workflows/` | Workflow orchestration templates | phases, agents, dependencies            |
| Hook     | `.claude/templates/hooks/`     | Hook implementation templates    | trigger, action, validation             |
| Code     | `.claude/templates/code/`      | Language-specific code patterns  | language, pattern_type                  |
| Schema   | `.claude/templates/schemas/`   | JSON/YAML schema templates       | properties, required, validation        |

## The Iron Law

```
NO TEMPLATE WITHOUT PLACEHOLDER DOCUMENTATION
```

Every `{{PLACEHOLDER}}` must have a corresponding comment explaining:

1. What value should replace it
2. Valid options/formats
3. Example value

**No exceptions:**

- Every placeholder is documented
- Every required field is marked
- Every optional field has a default

## Workflow

### Step -1: Existence Check and Updater Delegation (MANDATORY - FIRST STEP)

**BEFORE creating any template file, check if it already exists:**

1. **Check if template already exists:**

   ```bash
   test -f .claude/templates/<template-name> && echo "EXISTS" || echo "NEW"
   ```

2. **If template EXISTS:**
   - **DO NOT proceed with creation**
   - **Invoke template-updater workflow instead:**

     ```javascript
     Skill({
       skill: 'template-updater',
       args: {
         name: '<template-name>',
         changes: '<description of requested changes>',
         justification: 'Update requested via template-creator',
       },
     });
     ```

   - **Return updater result and STOP**

3. **If template is NEW:**
   - Continue with Step 0 below

---

### Step 0: Load Related Skills (FIRST)

Invoke related creator skills for context:

```javascript
Skill({ skill: 'agent-creator' }); // For agent template patterns
Skill({ skill: 'skill-creator' }); // For skill template patterns
```

### Step 1: Gather Template Requirements

**Analyze the request:**

1. **Template Type**: Which category (agent, skill, workflow, hook, code)?
2. **Purpose**: What will this template be used for?
3. **Required Fields**: What fields are mandatory?
4. **Optional Fields**: What fields are optional with defaults?
5. **Validation Rules**: What constraints apply?

**Example analysis:**

```
Template Request: "Create a hook template for pre-execution validation"
- Type: Hook
- Purpose: Validate inputs before skill execution
- Required: trigger, action, validation_schema
- Optional: error_message, continue_on_failure
- Rules: trigger must be "pre" or "post"
```

### Step 2: Analyze Existing Templates for Patterns

Search for existing patterns to ensure consistency:

```bash
# Find existing templates
Glob: .claude/templates/**/*.md

# Check agent template patterns
Read: .claude/templates/agents/agent-template.md

# Check skill template patterns
Read: .claude/templates/skills/skill-template.md

# Check workflow template patterns
Read: .claude/templates/workflows/workflow-template.md
```

**Pattern extraction checklist:**

- [ ] YAML frontmatter format
- [ ] Section headings style
- [ ] Placeholder format (`{{UPPER_CASE}}`)
- [ ] Comment style (`<!-- OPTIONAL: -->`)
- [ ] Memory Protocol section
- [ ] Verification commands

### Step 3: Generate Template with Placeholders

**Placeholder Format Standard:**

| Placeholder Type | Format                   | Example                    |
| ---------------- | ------------------------ | -------------------------- |
| Required field   | `{{FIELD_NAME}}`         | `{{AGENT_NAME}}`           |
| Optional field   | `{{FIELD_NAME:default}}` | `{{MODEL:sonnet}}`         |
| Multi-line       | `{{FIELD_NAME_BLOCK}}`   | `{{DESCRIPTION_BLOCK}}`    |
| List item        | `{{ITEM_N}}`             | `{{TOOL_1}}`, `{{TOOL_2}}` |

**Template Structure:**

```markdown
---
# YAML Frontmatter with all required fields
name: { { NAME } }
description: { { DESCRIPTION } }
# ... other fields
---

# {{DISPLAY_NAME}}

## POST-CREATION CHECKLIST (BLOCKING - DO NOT SKIP)

<!-- Always include blocking checklist -->

## Overview

{{OVERVIEW_DESCRIPTION}}

## Sections

<!-- Domain-specific sections -->

## Memory Protocol (MANDATORY)

<!-- Always include memory protocol -->
```

### Step 4: Add Documentation Comments

Add inline documentation for each placeholder:

```markdown
---
# [REQUIRED] Unique identifier, lowercase-with-hyphens
name: { { AGENT_NAME } }

# [REQUIRED] Single line, describes what it does AND when to use it
# Example: "Reviews mobile app UX against Apple HIG. Use for iOS UX audits."
description: { { DESCRIPTION } }

# [OPTIONAL] Default: sonnet. Options: haiku, sonnet, opus
model: { { MODEL:sonnet } }
---

<!-- SECTION: Core Persona -->
<!-- Define the agent's identity and working style -->

## Core Persona

**Identity**: {{IDENTITY}}

<!-- Example: "Senior Python Developer", "Security Analyst" -->
```

### Step 5: Validate Template Structure (BLOCKING)

Before writing the template file, verify ALL requirements:

**Validation Checklist:**

```
[ ] YAML frontmatter is valid syntax
[ ] All required fields have placeholders
[ ] All placeholders follow naming convention
[ ] All placeholders have documentation comments
[ ] POST-CREATION CHECKLIST section present
[ ] Memory Protocol section present
[ ] Verification commands included
[ ] Example values provided where helpful
```

**Verification Commands in Template:**

```bash
# Include these in the template's POST-CREATION CHECKLIST
grep "{{" <created-file> && echo "ERROR: Unresolved placeholders!"
```

### Step 6: Write Template File

Write to appropriate location:

```bash
# Agent template
Write: .claude/templates/agents/<template-name>.md

# Skill template
Write: .claude/templates/skills/<template-name>.md

# Workflow template
Write: .claude/templates/workflows/<template-name>.md

# Hook template (create directory if needed)
mkdir -p .claude/templates/hooks/
Write: .claude/templates/hooks/<template-name>.md

# Code template (create directory if needed)
mkdir -p .claude/templates/code/
Write: .claude/templates/code/<template-name>.md
```

### Step 7: Update Templates README (MANDATORY - BLOCKING)

After writing the template, update `.claude/templates/README.md`:

1. **Add to appropriate section** (or create new section)
2. **Document usage instructions**
3. **Add to Quick Reference table**

**Entry format:**

```markdown
### {{Template Type}} Templates (`{{directory}}/`)

Use when {{use case}}.

**File:** `{{directory}}/{{template-name}}.md`

**Usage:**

1. Copy template to `{{target-path}}`
2. Replace all `{{PLACEHOLDER}}` values
3. {{Additional steps}}
```

**Verification:**

```bash
grep "<template-name>" .claude/templates/README.md || echo "ERROR: README NOT UPDATED - BLOCKING!"
```

### Step 8: Post-Creation Template Registration (Phase 1 Integration)

**This step is CRITICAL.** After creating the template artifact, you MUST register it in the template discovery system.

**Phase 1 Context:** Phase 1 is responsible for discovering and cataloging templates for reuse. Templates created without registration are invisible to other creators and will never be used to standardize new artifacts.

After template file is written and validated:

1. **Create/Update Template Registry Entry** in appropriate location:

   If registry doesn't exist, create `.claude/context/artifacts/template-registry.json`:

   ```json
   {
     "templates": [
       {
         "name": "{template-name}",
         "id": "{template-name}",
         "type": "{agent|skill|workflow|hook|code|schema}",
         "category": "{subcategory if applicable}",
         "description": "{What this template is for}",
         "version": "1.0.0",
         "location": ".claude/templates/{category}/{template-name}.md",
         "placeholders": ["{PLACEHOLDER_1}", "{PLACEHOLDER_2}"],
         "usageScenarios": ["{Scenario 1}", "{Scenario 2}"]
       }
     ]
   }
   ```

2. **Document Placeholders with Usage Guide:**

   For each placeholder in the template, ensure documentation exists:

   ```markdown
   ## Template Placeholders

   | Placeholder       | Description  | Format   | Example   |
   | ----------------- | ------------ | -------- | --------- |
   | {{PLACEHOLDER_1}} | What this is | {format} | {example} |
   | {{PLACEHOLDER_2}} | What this is | {format} | {example} |
   ```

3. **Register in `.claude/templates/README.md`:**

   Add comprehensive entry to the templates catalog:

   ```markdown
   ### {Template Type} Templates (`{directory}/`)

   Use when {describe use case}.

   **File:** `.claude/templates/{directory}/{template-name}.md`

   **Placeholders:**

   - {{PLACEHOLDER_1}}: {Description}
   - {{PLACEHOLDER_2}}: {Description}

   **Usage:**

   1. Copy template to `{target-path}`
   2. Replace all `{{PLACEHOLDER_*}}` values with actual values
   3. Validate with: `grep "{{" {file} && echo "ERROR: Unresolved placeholders!"`

   **Related Templates:**

   - {Related template 1}
   - {Related template 2}

   **Assigned for use by:**

   - {Creator skill 1}
   - {Creator skill 2}
   ```

4. **Update Consumer Skills/Creators:**

   If this template is meant to be used by specific creators, add reference:
   - In agent-creator.md: Add to Step 2 (Agent Definition)
   - In skill-creator.md: Add to Step 2 (Skill Definition)
   - In hook-creator.md: Add to Step 3 (Hook Template)
   - In workflow-creator.md: Add to Step 4 (Workflow Definition)

   Example:

   ```markdown
   **Available Templates:**

   - See `.claude/templates/{category}/{template-name}.md` for standardized {type} template
   ```

5. **Update Memory:**

   Append to `.claude/context/memory/learnings.md`:

   ```markdown
   ## Template: {template-name}

   - **Type:** {agent|skill|workflow|hook|code|schema}
   - **Purpose:** {What this template standardizes}
   - **Placeholders:** {List key placeholders}
   - **Discovery Path:** {How users find it}
   - **Related Templates:** {Any related templates}
   ```

**Why this matters:** Without template registration:

- Other creators cannot discover available templates
- Artifacts are created inconsistently instead of using standards
- System loses visibility into template network
- "Invisible artifact" pattern emerges

**Phase 1 Integration:** Template registry is the discovery mechanism for Phase 1, enabling creators and agents to discover standardized patterns and ensure consistent artifact creation.

### Step 9: System Impact Analysis (MANDATORY)

After creating a template:

1. **README Update (BLOCKING)**
   - Add to .claude/templates/README.md (Step 8 covers this)
   - Document template purpose and placeholders

2. **Related Templates**
   - Check if new template supersedes existing one
   - Add cross-references if related

3. **Consumer Documentation**
   - Document which skills/agents should use this template
   - Update relevant creator skill with template reference
   - Update CLAUDE.md Section 8.5 if template is user-invocable

**BLOCKING**: Template without README entry may not be discovered.

**Analysis Format:**

```
[TEMPLATE-CREATOR] System Impact Analysis for: <template-name>

1. README UPDATE (MANDATORY - Step 8)
   - Added to .claude/templates/README.md
   - Usage instructions documented
   - Quick Reference table updated
   - Template registry entry created

2. RELATED TEMPLATES CHECK
   - Does this template supersede an existing one?
   - Are there related templates that need cross-references?
   - Update related creators if needed

3. CONSUMER DOCUMENTATION
   - Which skills/agents should use this template?
   - Is template reference added to relevant creator skill?
   - Is CLAUDE.md Section 8.5 update needed?

4. MEMORY UPDATE
   - Record creation in learnings.md
   - Document any decisions in decisions.md
```

## Completion Checklist (BLOCKING)

**All items MUST pass before template creation is complete:**

```
[ ] Template file created at .claude/templates/<name>.md
[ ] All placeholders use {{PLACEHOLDER_NAME}} format
[ ] README.md in .claude/templates/ updated
[ ] No hardcoded values (all configurable via placeholders)
[ ] Template tested with at least one real usage
[ ] Memory files updated with learnings
```

**BLOCKING**: If ANY item fails, template creation is INCOMPLETE. Fix all issues before proceeding.

### Reference Template

**Use `.claude/templates/agent-skill-invocation-section.md` as the canonical reference template.**

Before finalizing any template, compare:

- [ ] Has clear placeholder documentation
- [ ] Placeholders are UPPERCASE with underscores
- [ ] Has usage examples section
- [ ] Has integration notes

## Template Best Practices

### Placeholder Standards

| Practice        | Good                | Bad                        |
| --------------- | ------------------- | -------------------------- |
| Naming          | `{{AGENT_NAME}}`    | `{{name}}`, `{AGENT_NAME}` |
| Required fields | Always present      | Sometimes omitted          |
| Optional fields | `{{FIELD:default}}` | No default indicator       |
| Documentation   | Inline comments     | Separate docs file         |
| Examples        | In comments         | None provided              |

### Structure Standards

1. **YAML Frontmatter First**
   - All machine-readable metadata
   - Comments explaining each field

2. **POST-CREATION CHECKLIST Second**
   - Blocking steps after using template
   - Verification commands

3. **Content Sections**
   - Follow existing pattern for type
   - Include all required sections

4. **Memory Protocol Last**
   - Standard format across all templates
   - Always present

### Validation Examples

Include validation examples in templates:

````markdown
## Validation

After replacing placeholders, validate:

```bash
# Check YAML is valid
head -50 <file> | grep -E "^---$" | wc -l  # Should be 2

# Check no unresolved placeholders
grep "{{" <file> && echo "ERROR: Unresolved placeholders!"

# Check required sections present
grep -E "^## Memory Protocol" <file> || echo "ERROR: Missing Memory Protocol!"
```
````

````

## Workflow Integration

This skill is part of the unified artifact lifecycle. For complete multi-agent orchestration:

**Router Decision:** `.claude/workflows/core/router-decision.md`
- How the Router discovers and invokes this skill's artifacts

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`
- Discovery, creation, update, deprecation phases
- Version management and registry updates
- CLAUDE.md integration requirements

**External Integration:** `.claude/workflows/core/external-integration.md`
- Safe integration of external artifacts
- Security review and validation phases

---

## Cross-Reference: Creator Ecosystem

This skill is part of the **Creator Ecosystem**. Use companion creators when needed:

| Creator | When to Use | Invocation |
|---------|-------------|------------|
| **agent-creator** | Template needs agent integration | `Skill({ skill: 'agent-creator' })` |
| **skill-creator** | Template needs skill integration | `Skill({ skill: 'skill-creator' })` |
| **workflow-creator** | Template needs workflow patterns | Create in `.claude/workflows/` |
| **schema-creator** | Template needs JSON schemas | Create in `.claude/schemas/` |
| **hook-creator** | Template needs hooks | Create in `.claude/hooks/` |

### Integration Workflow

After creating a template that needs additional artifacts:

```javascript
// 1. Template created for new hook type
// 2. Need to create example hook using template
Skill({ skill: 'hook-creator' });

// 3. Template created for new agent category
// 4. Need to update agent-creator to recognize new category
// Edit .claude/skills/agent-creator/SKILL.md to add category
````

## Examples

### Example 1: Creating a Hook Template

**Request:** "Create a template for pre-execution validation hooks"

**Process:**

1. **Analyze**: Hook type, validation focus, pre-execution trigger
2. **Research**: Check existing hooks in `.claude/hooks/`
3. **Design**: Structure for validation hooks
4. **Create**: `.claude/templates/hooks/validation-hook-template.md`

````markdown
---
# [REQUIRED] Hook identifier, lowercase-with-hyphens
name: { { HOOK_NAME } }

# [REQUIRED] What this hook validates
description: { { VALIDATION_DESCRIPTION } }

# [REQUIRED] Options: pre, post
trigger: pre

# [REQUIRED] Options: block, warn, log
on_failure: { { ON_FAILURE:block } }
---

# {{HOOK_DISPLAY_NAME}} Hook

## POST-CREATION CHECKLIST (BLOCKING)

After creating this hook:

- [ ] Register in `.claude/settings.json`
- [ ] Test with sample input
- [ ] Document in hook README

## Validation Logic

```javascript
// {{VALIDATION_DESCRIPTION}}
function validate(input) {
  {
    {
      VALIDATION_LOGIC;
    }
  }
}
```
````

## Memory Protocol (MANDATORY)

**Before starting:** Read `.claude/context/memory/learnings.md`
**After completing:** Record patterns to learnings.md

````

5. **Update README**: Add hooks section to templates README
6. **Update Memory**: Record in learnings.md

### Example 2: Creating a Code Pattern Template

**Request:** "Create a template for TypeScript API endpoint patterns"

**Process:**

1. **Analyze**: TypeScript, API endpoint, code scaffolding
2. **Research**: Check `.claude/templates/code-styles/typescript.md`
3. **Design**: Structure for endpoint patterns
4. **Create**: `.claude/templates/code/typescript-api-endpoint.md`

```markdown
---
# [REQUIRED] Pattern identifier
name: {{PATTERN_NAME}}

# [REQUIRED] Language for this pattern
language: typescript

# [REQUIRED] Type: endpoint, service, model, utility
pattern_type: endpoint

# [OPTIONAL] Framework: express, fastify, nestjs
framework: {{FRAMEWORK:express}}
---

# {{PATTERN_DISPLAY_NAME}} Pattern

## Usage

Copy this pattern when creating new API endpoints.

## Template

```typescript
// {{ENDPOINT_DESCRIPTION}}
// Route: {{HTTP_METHOD}} {{ROUTE_PATH}}

import { Request, Response } from '{{FRAMEWORK}}';
import { {{SERVICE_NAME}} } from '../services/{{SERVICE_FILE}}';

export async function {{HANDLER_NAME}}(req: Request, res: Response) {
  try {
    {{HANDLER_LOGIC}}

    res.json({ success: true, data: result });
  } catch (error) {
    {{ERROR_HANDLING}}
  }
}
````

## Validation

After using this pattern:

- [ ] Route registered in router
- [ ] Input validation added
- [ ] Error handling implemented
- [ ] Tests written

```

## Troubleshooting

### Issue: Placeholders Not Rendering

**Symptoms:** `{{PLACEHOLDER}}` appears in final file

**Solution:**
- Check placeholder format (double braces, UPPER_CASE)
- Ensure user replaced all placeholders
- Add validation command to catch unreplaced

### Issue: Template Not Discoverable

**Symptoms:** Template exists but not found by creators

**Solution:**
- Verify README.md is updated
- Check file is in correct directory
- Run grep verification command

### Issue: Inconsistent Template Structure

**Symptoms:** Different templates have different formats

**Solution:**
- Review existing templates before creating
- Use this skill's patterns
- Run consistency check across templates

## Verification Checklist

Before completing template creation:

- [ ] Template file exists at correct path
- [ ] YAML frontmatter is valid
- [ ] All placeholders use `{{UPPER_CASE}}` format
- [ ] All placeholders have documentation comments
- [ ] POST-CREATION CHECKLIST section present
- [ ] Memory Protocol section present
- [ ] README.md updated
- [ ] Verification with grep passed
- [ ] learnings.md updated

## File Placement & Standards

### Output Location Rules
This skill outputs to: `.claude/templates/`

Subdirectories by type:
- `agents/` - Agent definition templates
- `skills/` - Skill definition templates
- `workflows/` - Workflow orchestration templates
- `hooks/` - Hook implementation templates
- `code/` - Language-specific code patterns
- `schemas/` - JSON/YAML schema templates

### Mandatory References
- **File Placement**: See `.claude/docs/FILE_PLACEMENT_RULES.md`
- **Developer Workflow**: See `.claude/docs/DEVELOPER_WORKFLOW.md`
- **Artifact Naming**: See `.claude/docs/ARTIFACT_NAMING.md`

### Enforcement
File placement is enforced by `file-placement-guard.cjs` hook.
Invalid placements will be blocked in production mode.

---

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**
- New template pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

---

## Iron Laws of Template Creation

These rules are INVIOLABLE. Breaking them causes inconsistency across the framework.

```

1. NO TEMPLATE WITHOUT PLACEHOLDER DOCUMENTATION
   - Every {{PLACEHOLDER}} must have an inline comment
   - Comments explain valid values and examples

2. NO TEMPLATE WITHOUT POST-CREATION CHECKLIST
   - Users must know what to do after using template
   - Blocking steps prevent incomplete artifacts

3. NO TEMPLATE WITHOUT MEMORY PROTOCOL
   - All templates must include Memory Protocol section
   - Ensures artifacts created from template follow memory rules

4. NO TEMPLATE WITHOUT README UPDATE
   - Templates README must document new template
   - Undocumented templates are invisible

5. NO PLACEHOLDER WITHOUT NAMING CONVENTION
   - Use {{UPPER_CASE_WITH_UNDERSCORES}}
   - Never use lowercase or mixed case

6. NO OPTIONAL FIELD WITHOUT DEFAULT
   - Format: {{FIELD:default_value}}
   - Makes templates usable without full customization

7. NO TEMPLATE WITHOUT VERIFICATION COMMANDS
   - Include commands to validate created artifacts
   - Users can verify their work is correct

````

## Assigned Agents

This skill is typically invoked by:

| Agent | Role | Assignment Reason |
|-------|------|-------------------|
| planner | Planning standardization | Creates templates for new patterns |
| architect | Architecture patterns | Creates templates for architectural artifacts |
| developer | Code patterns | Creates code scaffolding templates |

**To invoke this skill:**

```javascript
Skill({ skill: 'template-creator' });
````
