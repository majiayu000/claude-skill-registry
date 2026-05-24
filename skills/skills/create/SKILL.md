---
description: Interactive skill creation wizard that guides users through creating new skills with validation checkpoints
argument-hint: [skill-name]
skills: skill-manager
---

# create-skill

Interactive wizard for creating new agent skills. This command follows the skill-manager workflow to guide users through creating effective, well-structured skills with all necessary components (SKILL.md, scripts, references, and assets).

## Arguments

- `name` (string, required): Name of the skill to create
  - Validation: Must match pattern: ^[a-z][a-z0-9-]*$
  - Example: pdf-editor, big-query, frontend-app-builder

## Workflow

This command follows a structured creation flow with validation at each step:

### Phase 1: Initialization and Validation
1. Validate skill name format (lowercase-with-hyphens)
2. Check if skill already exists in `.claude/skills/` or `~/.claude/skills/`
3. If exists, ask user whether to overwrite or choose different name
4. **Validation checkpoint:** Confirm skill name and proceed

### Phase 2: Understanding the Skill
This phase follows skill-manager Step 1: Understanding the Skill with Concrete Examples

5. Ask: "What functionality should this skill support?"
6. Ask: "Can you give concrete examples of how this skill will be used?"
7. Ask: "What would a user say that should trigger this skill?"
8. Summarize understanding of skill purpose and use cases
9. **Validation checkpoint:** Confirm understanding is correct

### Phase 3: Planning Reusable Content
This phase follows skill-manager Step 2: Planning the Reusable Skill Contents

10. Analyze examples to identify needed resources:
    - **Scripts**: Reusable automation code (e.g., rotate-pdf.sh)
    - **References**: Documentation, schemas, specifications (e.g., schema.md)
    - **Assets**: Templates, boilerplate files, sample data (e.g., hello-world/)
11. Present recommended skill structure based on analysis
12. Ask user if additional scripts/references/assets should be included
13. **Validation checkpoint:** Approve skill structure plan

### Phase 4: Creating Skill Description
Critical step for proper skill activation

14. Generate initial description following these rules:
    - Start with "Use when..."
    - Focus on triggering conditions only (NOT workflow)
    - Include concrete symptoms and situations
    - Use keywords for searchability
    - Technology-agnostic unless skill is tech-specific
15. Present generated description for review
16. **Validation checkpoint:** Approve description text

### Phase 5: Determining Save Location
17. Ask whether to save as project-local or global skill:
    - Project-local: `.claude/skills/[skill-name]/`
    - Global: `~/.claude/skills/[skill-name]/`
18. Create directory structure at chosen location
19. **Validation checkpoint:** Confirm save location

### Phase 6: Generating Skill Files
This phase follows skill-manager Step 3 & 4: Initializing and Editing the Skill

20. Create SKILL.md with:
    - YAML front matter (name, description, metadata)
    - "When to Activate This Skill" section
    - "When NOT to Use This Skill" section
    - "How to Use" section with workflow steps
    - "Examples" section with concrete use cases
    - "Important Notes" section
21. Create subdirectories as needed:
    - `scripts/` (if scripts identified in Phase 3)
    - `references/` (if references identified in Phase 3)
    - `assets/` (if assets identified in Phase 3)
22. For each subdirectory, create placeholder README.md explaining purpose
23. Save all files to chosen location

### Phase 7: Completion and Next Steps
24. Display success message with skill location
25. Show statistics (files created, directories, size)
26. Offer to:
    - Add example scripts immediately
    - Add reference documentation immediately
    - Test the skill with a sample query
    - Create related command that uses this skill

## Statistics Reporting

Output includes:
- Skill name and location (project-local vs global)
- Files created (SKILL.md, README files, etc.)
- Directories created (scripts/, references/, assets/)
- Description length and keyword count
- Validation checkpoints passed
- Total creation time

Example:
```
Created skill: pdf-editor
Location: ~/.claude/skills/pdf-editor/ (global)

Skill structure:
- SKILL.md (1.2 KB)
- scripts/ (1 file: rotate-pdf.sh)
- references/ (1 file: README.md)
- Description: 45 words, 8 keywords

Validation checkpoints: 5/5 passed
Created in 3m 15s
```

Example with assets:
```
Created skill: frontend-app-builder
Location: .claude/skills/frontend-app-builder/ (project)

Skill structure:
- SKILL.md (2.1 KB)
- assets/hello-world/ (12 files)
- references/ (2 files: README.md, best-practices.md)
- Description: 38 words, 6 keywords

Validation checkpoints: 5/5 passed
Created in 5m 42s
```

## Examples

```bash
# Interactive mode - guided through all steps
create:skill pdf-editor

# Create a domain-specific skill
create:skill big-query

# Create a workflow skill
create:skill test-driven-development

# Create a file processing skill
create:skill image-optimizer
```

## Validation Checkpoints

This command implements 5 validation checkpoints:

1. **Skill Name Validation**: User confirms skill name and handles conflicts
2. **Purpose Understanding**: User confirms skill purpose is correctly understood
3. **Structure Approval**: User approves planned scripts/references/assets
4. **Description Validation**: User approves generated description text
5. **Location Confirmation**: User confirms save location (project vs global)

At each checkpoint, user can:
- Approve and continue
- Request modifications
- Go back to previous step
- Cancel skill creation

## Interactive Question Flow

The command asks structured questions throughout the process:

### Purpose Questions (Phase 2)
- "What functionality should this skill support?"
- "Can you give concrete examples of how this skill will be used?"
- "What would a user say that should trigger this skill?"

### Structure Questions (Phase 3)
- "Based on your examples, I recommend including [list]. Does this look correct?"
- "Should any additional scripts be included?"
- "Should any additional references be included?"
- "Should any additional assets be included?"

### Description Review (Phase 4)
- "Here's the generated description: [description]. Does this accurately describe when to use this skill?"
- "Are there additional keywords or triggers to include?"

### Location Questions (Phase 5)
- "Should this skill be saved as project-local (.claude/skills/) or global (~/.claude/skills/)?"

## Best Practices

This command enforces best practices:

**Skill Naming:**
- Validates lowercase-with-hyphens format
- Rejects generic names (process, handle, helper)
- Suggests improvements for unclear names

**Description Quality:**
- Enforces "Use when..." format
- Prevents workflow summarization in description
- Validates keyword coverage for searchability
- Ensures concrete triggering conditions included

**Structure Planning:**
- Recommends scripts for repeated code patterns
- Recommends references for schemas and documentation
- Recommends assets for boilerplate and templates
- Warns against over-structuring simple skills

**Documentation Completeness:**
- Requires "When to Activate" section
- Requires "When NOT to Use" section
- Requires concrete examples
- Validates workflow clarity

## Error Handling

The command handles common errors:

**Invalid Skill Name:**
```
Error: Skill name "PDFEditor" invalid
- Must be lowercase with hyphens
- Example: pdf-editor
```

**Skill Already Exists:**
```
Warning: Skill "pdf-editor" already exists in ~/.claude/skills/
Options:
1. Overwrite existing skill
2. Choose a different name
3. Cancel
```

**Missing Required Information:**
```
Error: Cannot generate skill description
- Missing: concrete usage examples
- Please provide examples of how this skill would be used
```

**Invalid Save Location:**
```
Error: Cannot create directory ~/.claude/skills/pdf-editor/
- Directory ~/.claude/ does not exist
- Create global skills directory first: mkdir -p ~/.claude/skills/
```

## Integration with skill-manager Skill

This command is built on the skill-manager skill and follows its workflow:

1. **Phase 2** implements skill-manager Step 1: Understanding with Concrete Examples
2. **Phase 3** implements skill-manager Step 2: Planning Reusable Contents
3. **Phase 6** implements skill-manager Steps 3 & 4: Initializing and Editing

The key enhancement is the interactive, checkpoint-based flow that ensures:
- No missing information
- User approval at critical decision points
- Consistent skill quality
- Proper description format (triggers only, no workflow)
- Appropriate resource planning (scripts/references/assets)

## Notes

- Skills are saved as directories with SKILL.md as the main file
- YAML front matter in SKILL.md includes: name, description, metadata (author, version)
- Directory structure follows AgentSkills.io specification
- Description field is CRITICAL for skill activation - follows strict format
- Skills can be tested immediately after creation
- Use skill-manager skill directly for more complex skill creation scenarios
