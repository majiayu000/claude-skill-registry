---
name: adb-skill-generator
description: Meta-tool for rapid adb-* skill creation from templates
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 3
category: adb-meta-automation
last_updated: 2025-12-02
compliance_score: 100

dependencies: []

auto_trigger_keywords:
  - skill-generator
  - scaffold
  - template
  - create-skill
  - rapid-development

scripts:
  - name: adb-skill-generator.py
    purpose: Generate new adb-* skill from templates
    type: python
    command: uv run .claude/skills/adb-skill-generator/adb-skill-generator.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02

color: magenta
---

---

## Quick Reference (30 seconds)

**Rapid adb-* skill creation from production-tested templates**

**What It Does**: Automates creation of new adb-* skills by generating skill directory structure, SKILL.md metadata, script templates, and example workflows. Speeds up new skill development from hours to minutes.

**Core Capabilities**:
- 🚀 **Scaffold Skills**: Generate complete skill directory structure
- 📝 **Template Scripts**: Create launcher, checker, automator, tester scripts
- 📋 **SKILL.md Generation**: Auto-generate metadata with proper frontmatter
- 📊 **Workflow Examples**: Optional TOON workflow templates
- ✅ **Best Practices**: Built-in ecosystem patterns and conventions

**When to Use**:
- Creating new app automation skills
- Rapid prototyping of automation workflows
- Onboarding new skill developers
- Standardizing skill structure across ecosystem

---

## Scripts

### adb-skill-generator.py

Generate new adb-* skill from templates.

```bash
# Minimal skill (1 launcher script)
uv run .claude/skills/adb-skill-generator/adb-skill-generator.py \
    --skill-name banking \
    --description "Banking app automation via Play Integrity bypass"

# Full skill (3 scripts + workflow)
uv run .claude/skills/adb-skill-generator/adb-skill-generator.py \
    --skill-name fitness \
    --description "Fitness app testing" \
    --script-count 3 \
    --with-workflow

# With category specification
uv run .claude/skills/adb-skill-generator/adb-skill-generator.py \
    --skill-name streaming \
    --description "Streaming app automation" \
    --category adb-app-automation

# List available templates
uv run .claude/skills/adb-skill-generator/adb-skill-generator.py \
    --list-templates

# JSON output
uv run .claude/skills/adb-skill-generator/adb-skill-generator.py \
    --skill-name myapp \
    --description "My app automation" \
    --json
```

**Parameters**:
- `--skill-name` (required): Name of skill (with or without adb- prefix)
- `--description` (required): Brief description of skill purpose
- `--script-count` (optional, default: 1): Number of scripts (1-4)
- `--with-workflow` (optional): Generate example TOON workflow
- `--category` (optional): Skill category (default: adb-app-automation)
- `--list-templates`: Show available templates
- `--json`: JSON output instead of human-readable
- `--verbose`: Detailed operation logging

**Exit Codes**:
- `0`: Success (skill created)
- `1`: Warning (partial creation)
- `2`: Error (skill creation failed)
- `3`: Critical (invalid parameters)

**Generated Structure**:

```
.claude/skills/adb-{skillname}/
├── SKILL.md                           # Metadata + documentation
├── scripts/
│   ├── adb-{skillname}-launch.py      # Launcher script
│   ├── adb-{skillname}-check.py       # Checker script (if count >= 2)
│   ├── adb-{skillname}-test.py        # Tester script (if count >= 3)
│   └── adb-{skillname}-validate.py    # Validator script (if count >= 4)
├── workflows/
│   ├── {skillname}-basic.toon         # Basic workflow example
│   └── {skillname}-advanced.toon      # Advanced workflow example (if requested)
├── templates/                          # (Empty - for user templates)
└── analysis/                          # (Empty - for analysis results)
```

---

## Quick Examples

### Example 1: Minimal Skill Generation

```bash
uv run adb-skill-generator.py \
    --skill-name twitter \
    --description "Twitter app automation for testing"
```

**Creates**:
- `adb-twitter/SKILL.md`
- `adb-twitter/scripts/adb-twitter-launch.py` (launcher)
- `adb-twitter/workflows/twitter-basic.toon` (basic example)
- Directory structure ready for customization

### Example 2: Complete Skill with Workflow

```bash
uv run adb-skill-generator.py \
    --skill-name instagram \
    --description "Instagram app automation and testing" \
    --script-count 3 \
    --with-workflow
```

**Creates**:
- `adb-instagram/SKILL.md`
- `adb-instagram/scripts/adb-instagram-launch.py` (launcher)
- `adb-instagram/scripts/adb-instagram-check.py` (checker)
- `adb-instagram/scripts/adb-instagram-test.py` (tester)
- `adb-instagram/workflows/instagram-basic.toon`
- `adb-instagram/workflows/instagram-advanced.toon`

### Example 3: JSON Output for CI/CD Integration

```bash
uv run adb-skill-generator.py \
    --skill-name facebook \
    --description "Facebook app automation" \
    --json
```

**Output**:
```json
{
  "skill_name": "adb-facebook",
  "success": true,
  "skill_path": "/path/to/.claude/skills/adb-facebook",
  "scripts_created": 1,
  "skill_md_created": true,
  "workflow_created": false,
  "duration": 0.45,
  "messages": [
    "✅ Created skill directory: ...",
    "✅ Created scripts/ subdirectory",
    "✅ Created SKILL.md ...",
    "✅ Created script: adb-facebook-launch.py"
  ],
  "exit_code": 0
}
```

---

## Script Template Structure

All generated scripts follow the proven 9-section IndieDevDan template:

```
1. Docstring          - Comprehensive description with examples
2. Imports            - Required libraries
3. Constants          - Configuration values
4. Project root       - Auto-detection logic
5. Data models        - Result dataclasses
6. Helpers            - Utility functions (device selection, etc.)
7. Core logic         - Primary automation implementation
8. Formatters         - Human + JSON output formatting
9. CLI interface      - Click command-line interface
10. Entry point       - Main execution guard
```

**Benefits**:
- Consistent structure across all skills
- Easy to understand and maintain
- Proven patterns from production skills
- Familiar to all developers

---

## Workflow Template Structure

Generated workflows follow TOON format:

```yaml
name: {skillname}-basic
description: Basic automation for {skillname}

parameters:
  device: "127.0.0.1:5555"
  timeout: 30

phases:
  - id: phase-1
    name: "Launch app"
    steps:
      - id: launch
        action: {skillname}-launch
        params:
          device: "{{ device }}"

recovery:
  - on_error: launch
    action: retry
    then: continue
```

**Features**:
- Parameter templating with {{ variable }}
- Phase-based organization
- Error recovery rules
- Executable with adb-run-workflow

---

## Integration with Ecosystem

### Step 1: Generate Skill
```bash
uv run adb-skill-generator.py \
    --skill-name myapp \
    --description "My app automation"
```

### Step 2: Implement Core Scripts
Edit generated scripts to add actual automation logic:
- `scripts/adb-myapp-launch.py` - App launch logic
- `scripts/adb-myapp-check.py` - State checking logic
- `scripts/adb-myapp-test.py` - Functional testing

### Step 3: Create Advanced Workflows
Build TOON workflows using generated scripts:
```bash
uv run adb-run-workflow.py \
    --workflow .claude/skills/adb-myapp/workflows/myapp-advanced.toon \
    --verbose
```

### Step 4: Share or Distribute
Generated skill is immediately usable by others:
```bash
uv run .claude/skills/adb-myapp/scripts/adb-myapp-launch.py --device 127.0.0.1:5555
```

---

## Design Philosophy

The generator embodies ADB ecosystem design principles:

**1. Convention over Configuration**
- Default settings work for 90% of use cases
- Simple naming patterns (adb-{skillname})
- Consistent file organization

**2. Rapid Development**
- Scaffold complex structure in seconds
- Focus on implementation, not boilerplate
- Templates from production-tested code

**3. Quality by Default**
- Generated code follows best practices
- Includes error handling, timeouts, retries
- Proper exit codes and logging

**4. Extensibility**
- Generated code is production-ready but customizable
- Clear sections for user implementation
- Supports skill composition and integration

---

## Related Skills

This generator uses and integrates with:
- **adb-screen-detection**: For OCR-based element finding
- **adb-navigation-base**: For gesture automation (tap, swipe, wait)
- **adb-workflow-orchestrator**: For complex multi-step orchestration

All generated skills can depend on these foundation skills automatically.

---

## Common Customization Patterns

### Pattern 1: Custom Package Name
```python
# In generated script, change:
APP_PACKAGE = "kr.co.flo.karrot"  # Replace with your app package
```

### Pattern 2: Custom UI Elements
```python
# In launcher script, change:
result = launch_app_with_verification(
    device_id,
    wait_text="Custom Login Screen"  # Your app's specific screen
)
```

### Pattern 3: Custom Timeout
```python
# In any script, change:
VERIFICATION_TIMEOUT = 45  # Slower apps need more time
```

---

## Troubleshooting

**Q: Script generation failed**
```bash
# Ensure valid skill name (alphanumeric + hyphens)
uv run adb-skill-generator.py --skill-name valid-name --description "..."
```

**Q: How to see what will be generated?**
```bash
# Use --verbose flag
uv run adb-skill-generator.py \
    --skill-name myapp \
    --description "..." \
    --verbose
```

**Q: Can I use generated scripts immediately?**
```bash
# Yes, scripts are immediately usable but may need customization
uv run .claude/skills/adb-myapp/scripts/adb-myapp-launch.py --device 127.0.0.1:5555
```

---

## Workflows

This skill includes TOON-based workflow definitions for automation.

### What is TOON?
TOON (Task-Oriented Orchestration Notation) is a structured workflow definition language that pairs with Markdown documentation. Each workflow consists of:
- **[name].toon** - Orchestration logic and execution steps
- **[name].md** - Complete documentation and usage guide

This TOON+MD pairing approach is inspired by the BMAD METHOD pattern, adapted to use TOON instead of YAML for better orchestration support.

### Available Workflows

Workflow files are located in `workflow/` directory:

**Example Workflows (adb-skill-generator):**
- `workflow/skill-generation.toon` - Complete skill generation workflow
- `workflow/template-validation.toon` - Validate and test generated skill templates

### Running a Workflow

Execute any workflow using the ADB workflow orchestrator:

```bash
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
  --workflow .claude/skills/adb-skill-generator/workflow/skill-generation.toon \
  --param skill_name="myapp"
```

### Workflow Documentation

Each workflow includes comprehensive documentation in the corresponding `.md` file:
- Purpose and use case
- Prerequisites and requirements
- Available parameters
- Execution phases and steps
- Success criteria
- Error handling and recovery
- Example commands

See the `workflow/` directory for complete TOON file definitions and documentation.

### Creating New Workflows

To create custom workflows for this skill:
1. Create a new `.toon` file in the `workflow/` directory
2. Define phases, steps, and parameters using TOON v4.0 syntax
3. Create corresponding `.md` file with comprehensive documentation
4. Test with the workflow orchestrator

For more information, refer to the TOON specification and the workflow orchestrator documentation.

---

**Version**: 1.0.0 (Production Ready)
**Last Updated**: 2025-12-02
**Category**: Meta-Automation (Tier 3)
