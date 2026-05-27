---
name: devkit-create-skill
description: Create a new AIWG skill with AI-guided design
args:
  - name: name
    description: Skill name (kebab-case)
    required: true
  - name: --to
    description: Target addon or framework
    required: true
  - name: --interactive
    description: Enable interactive design mode
    required: false
---

# Create AIWG Skill

Create a new skill that can be triggered by natural language patterns.

## Understanding Skills

Skills differ from commands:
- **Commands**: Triggered by explicit `/command-name` invocation
- **Skills**: Triggered by natural language patterns (e.g., "apply voice", "validate writing")

Skills are ideal for:
- Capabilities users invoke conversationally
- Features that should "just work" without explicit commands
- Cross-cutting concerns that apply in many contexts

## Process

### 1. Validate Parameters

Verify `$ARGUMENTS` contains:
- Skill name (kebab-case)
- `--to` target (addon or framework, NOT extension)

**Note**: Skills cannot be added to extensions because skills need standalone functionality.

Check target exists:
```bash
ls ~/.local/share/ai-writing-guide/agentic/code/addons/<target>/
# or
ls ~/.local/share/ai-writing-guide/agentic/code/frameworks/<target>/
```

### 2. Interactive Design (if --interactive)

Guide the user through skill design:

**Skill Purpose**:
> What does this skill do? (e.g., "applies voice profiles to content", "validates code quality")

**Trigger Phrases**:
> What natural language phrases should activate this skill?
> Examples:
> - "apply voice", "use voice", "write in <voice> voice"
> - "validate code", "check quality", "review code"
> - "format document", "clean up", "prettify"

**Input Requirements**:
> What input does this skill need?
> - Content to process
> - Configuration parameters
> - File paths

**Output Format**:
> What does this skill produce?
> - Transformed content
> - Validation report
> - Recommendations

**Reference Materials**:
> Does this skill need supporting documentation?
> - Style guides
> - Validation rules
> - Example outputs

### 3. Execute Scaffolding

Run the CLI scaffolding tool:

```bash
node ~/.local/share/ai-writing-guide/tools/scaffolding/add-skill.mjs \
  <name> \
  --to <target>
```

### 4. Generated Structure

```
<target>/skills/<name>/
├── SKILL.md           # Main skill definition
└── references/        # Supporting documentation
```

### 5. Customize SKILL.md

The generated SKILL.md needs customization:

```yaml
---
name: <skill-name>
description: <what this skill does>
version: 1.0.0
---

# <Skill Name>

## Trigger Phrases

Activate this skill when the user says:
- "<phrase 1>"
- "<phrase 2>"
- "<phrase 3>"

## Input

This skill expects:
- <input requirement 1>
- <input requirement 2>

## Execution Process

1. <Step 1>
2. <Step 2>
3. <Step 3>

## Output

This skill produces:
- <output 1>
- <output 2>

## Examples

### Example 1: <scenario>
**User**: "<example trigger>"
**Result**: <what happens>

### Example 2: <scenario>
**User**: "<example trigger>"
**Result**: <what happens>
```

### 6. Add Reference Materials

If the skill needs supporting documentation:

```bash
# Create reference files
touch <target>/skills/<name>/references/style-guide.md
touch <target>/skills/<name>/references/validation-rules.md
```

### 7. Update Manifest

The CLI tool automatically updates the manifest. Verify:

```json
{
  "skills": ["existing-skill", "<new-skill>"]
}
```

## Output Format

```
Skill Created: <name>
─────────────────────

Location: <target>/skills/<name>/

Created:
  ✓ SKILL.md
  ✓ references/

Manifest updated: <target>/manifest.json

Next Steps:
  1. Edit SKILL.md to define trigger phrases
  2. Add execution process details
  3. Create reference materials (if needed)
  4. Test with natural language triggers
```

## Examples

```bash
# Create skill in addon
/devkit-create-skill code-formatter --to aiwg-utils

# Create skill with interactive guidance
/devkit-create-skill voice-apply --to voice-framework --interactive

# Create skill in framework
/devkit-create-skill requirement-tracer --to sdlc-complete
```

## Best Practices

1. **Clear trigger phrases**: Use natural, conversational language
2. **Multiple triggers**: Provide several ways to invoke the skill
3. **Specific execution**: Document exactly what happens when triggered
4. **Good examples**: Show realistic usage scenarios
5. **Reference materials**: Include supporting docs when needed
