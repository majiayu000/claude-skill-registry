---
name: skill-creator-blk
description: 'Create skills for BL1NK workspace with proven patterns and best practices.
  Use this skill to: (1) Build new skills aligned with BL1NK architecture and 4-phase
  implementation, (2) Understand skill stru'
---

---
name: skill-creator-blk
description: Create skills for BL1NK workspace with proven patterns and best practices. Use this skill to: (1) Build new skills aligned with BL1NK architecture and 4-phase implementation, (2) Understand skill structure from real BL1NK examples (text-processor, log-analyzer, notification-router, etc.), (3) Follow workspace patterns for text processing, integrations, GitHub/Poe/notification systems, (4) Create skills that integrate with existing BL1NK infrastructure, (5) Learn from the 10 skills identified in workspace analysis (Phase 1-4)
license: Complete terms in LICENSE.txt
---

# BL1NK Skill Creator

Create effective skills for the BL1NK workspace with real patterns, proven examples, and workspace-aware guidance.

## About BL1NK Skills

BL1NK skills are modular packages that extend Claude's capabilities by providing:

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for GitHub, Slack/Linear/ClickUp, POE protocol, etc.
3. **Workspace expertise** - BL1NK-specific knowledge and patterns
4. **Bundled resources** - Scripts, references, and templates for complex tasks

### BL1NK Workspace Context

The BL1NK workspace has been thoroughly analyzed (50+ files), identifying 10 skills needed across 4 implementation phases:

- **Phase 1 (Week 1, 5-8h)**: Critical foundation skills
- **Phase 2 (Week 2, 9-12h)**: Integration-enabled skills
- **Phase 3 (Week 3-4, 10-13h)**: Platform maturity skills
- **Phase 4 (Backlog, 4-5h)**: Advanced capabilities

This skill will help you create skills that fit seamlessly into this structure.

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have.

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task:

- **High freedom (text-based instructions)**: When multiple approaches are valid
- **Medium freedom (pseudocode with parameters)**: When a preferred pattern exists
- **Low freedom (specific scripts)**: When operations are fragile and error-prone

### BL1NK-Specific: Follow Proven Patterns

BL1NK already has working examples. Learn from them:

- **Text Processing**: `text-processor` (count, stats, reverse, capitalize)
- **Log Analysis**: `log-analyzer` (parsing, filtering, pattern matching)
- **Notifications**: `notification-router` (Slack, Linear, ClickUp integration)
- **GitHub Integration**: `github-repo-analyzer` (repo health analysis)
- **POE Protocol**: `poe-bot-generator` (POE-compliant bots)
- **Orchestration**: `skill-chain-executor` (multi-skill workflows)

See `references/blk-examples.md` for complete details on all 10 identified skills.

## Anatomy of a BL1NK Skill

Every BL1NK skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   ├── description: (required - used for triggering)
│   │   └── inputs/outputs: (recommended for BL1NK)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash)
    ├── references/       - Documentation (patterns, APIs, schemas)
    └── assets/           - Templates and boilerplate files
```

### SKILL.md Format (Required)

**Frontmatter (YAML):** Contains `name` and `description`

```yaml
---
name: my-skill
description: Clear description of what skill does and when to use it
---
```

**Body (Markdown):** Instructions and guidance for using the skill

### Bundled Resources (Optional)

#### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or repeated execution.

**When to include**: When the same code is written repeatedly or reliability is critical

**Examples**: `rotate_pdf.py`, `parse_logs.py`, `validate_json.py`

#### References (`references/`)

Documentation intended to be loaded as needed to inform Claude's process.

**When to include**: For documentation Claude should reference while working

**Examples**:
- `api_docs.md` - API specifications
- `patterns.md` - Common workflow patterns
- `schemas.md` - Data structure definitions
- `integrations.md` - External system integration guides

#### Assets (`assets/`)

Files not loaded into context but used in the output Claude produces.

**When to include**: When the skill needs templates, boilerplate, or sample files

**Examples**:
- `template.py` - Python boilerplate
- `example-skill/` - Sample skill structure
- `checklist.md` - Implementation checklist

## BL1NK Skill Patterns

### Pattern 1: Text/Data Processing

**Used for**: Text analysis, data transformation, pattern matching

**Structure**:
```python
# Input: text content, operation type
# Output: analyzed/transformed data
# Examples: text-processor, log-analyzer
```

**When to use**: For skills that manipulate text, parse logs, or transform data

**Integration**: No external dependencies typically needed

### Pattern 2: External Integration

**Used for**: Connecting to GitHub, Slack, Linear, ClickUp, etc.

**Structure**:
```python
# Input: parameters + credentials
# Process: call external API
# Output: results or status
# Examples: notification-router, github-repo-analyzer
```

**When to use**: For skills that interact with external systems

**Integration**: Use existing client classes (NotificationManager, GithubClient, etc.)

### Pattern 3: POE Protocol Compliance

**Used for**: Creating POE-protocol-compliant bots

**Structure**:
```python
# Framework: FastAPI with POE protocol handlers
# Input: POE protocol query
# Output: SSE stream with events
# Example: poe-bot-generator
```

**When to use**: For skills that generate or analyze POE bots

**Integration**: Reference POE protocol specs in `docs/poe-protocol/`

### Pattern 4: Orchestration & Chaining

**Used for**: Coordinating multiple skills or complex workflows

**Structure**:
```python
# Input: skill sequence + data flow
# Process: execute skills sequentially
# Output: aggregated results
# Example: skill-chain-executor
```

**When to use**: For skills that coordinate multiple steps

**Integration**: Use SkillLoader and orchestration patterns

See `references/blk-patterns.md` for detailed pattern descriptions.

## BL1NK 4-Phase Implementation Approach

Skills are organized by implementation complexity and urgency:

### Phase 1: Critical Foundation (Week 1, 5-8h)
- High urgency, lower complexity
- Foundation for other phases
- Examples: text-processor, log-analyzer, notification-router
- Characteristics: Simple operations, high business value, no complex dependencies

### Phase 2: Integration-Enabled (Week 2, 9-12h)
- External system integration
- Examples: github-repo-analyzer, prompt-optimizer, poe-bot-generator
- Characteristics: External APIs, moderate complexity, high value

### Phase 3: Platform Maturity (Week 3-4, 10-13h)
- Orchestration and coordination
- Examples: code-analyzer, skill-chain-executor, document-generator
- Characteristics: Coordinate multiple skills, higher complexity, enabling platform

### Phase 4: Advanced (Backlog, 4-5h)
- Optional advanced features
- Examples: test-generator
- Characteristics: Complex, lower urgency, can be added later

**When creating a skill, determine which phase it belongs to** based on urgency, complexity, and dependencies.

See `references/phase-implementation.md` for detailed phase breakdown.

## Workspace-Specific Considerations

### Integration Points

**Notification System**
- Location: `/home/user/projects/bl1nk-architect/src/notifications/`
- Classes: NotificationManager, SlackNotifier, LinearNotifier, ClickUpNotifier
- Use case: Route results to Slack, Linear, or ClickUp

**GitHub Integration**
- Location: `/home/user/projects/bl1nk-architect/src/github_client.py`
- Class: GithubClient
- Use case: Analyze repos, check health, assess code quality

**POE Protocol Support**
- Location: `/home/user/docs/poe-protocol/`
- Key classes: Using fastapi_poe
- Use case: Create POE-compliant bots

**Skill Orchestration**
- Location: `/home/user/projects/bl1nk-architect/src/skill_loader.py`
- Class: SkillLoader
- Use case: Load and execute multiple skills in sequence

### Manifest & Registry

When creating a skill, update:
1. `/home/user/skills/manifest.json` - Full metadata
2. `/home/user/skills/skills.json` - Quick reference
3. `/home/user/skills/README.md` - Documentation

### Code Reuse Strategy

**DON'T REINVENT** - Check if code already exists:
- NotificationManager → for notification-router
- GithubClient → for github-repo-analyzer
- GeminiClient → for prompt-optimizer
- SkillLoader → for skill-chain-executor

See `references/blk-patterns.md` for integration patterns.

## Progressive Disclosure Design Principle

Skills use a three-level loading system:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited)

Keep SKILL.md body concise and under 500 lines. Split content into separate files when approaching this limit.

### Reference Patterns

**Pattern: High-level guide with references**
```markdown
# My Skill

## Quick start
[basic instructions]

## Advanced features
- See advanced.md for details
- See examples.md for patterns
```

**Pattern: Domain-specific organization**
```
my-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain1.md
    ├── domain2.md
    └── domain3.md
```

Claude loads domain-specific reference only when needed.

## Skill Creation Process

Follow these steps in order:

### Step 1: Understanding with Concrete Examples

Clearly understand concrete examples of how the skill will be used.

Ask yourself:
- What functionality should this skill support?
- Can I give examples of how this skill would be used?
- What would a user say that should trigger this skill?
- What BL1NK workspace patterns does this relate to?

### Step 2: Planning Reusable Contents

For each concrete example, analyze:
1. What scripts would be helpful when executing this workflow repeatedly?
2. What references/documentation should Claude have access to?
3. What templates or assets would be useful?

**BL1NK-specific**: Check `references/blk-patterns.md` for proven patterns

### Step 3: Initializing the Skill

Create a new skill directory and use the template:

```bash
scripts/init_skill.py my-skill --path /home/user/skills/anthropics/
```

Or for BL1NK skills:
```bash
scripts/init_blk_skill.py my-skill --path /home/user/skills/
```

### Step 4: Edit the Skill

**Start with bundled resources**:
- Add scripts to `scripts/`
- Add references to `references/`
- Add assets to `assets/`

**Then update SKILL.md**:
- Write YAML frontmatter (name, description)
- Write body with instructions and guidance

**BL1NK-specific**:
- Reference integration patterns from `references/blk-patterns.md`
- Consider which phase it belongs to
- Check if it needs notification/GitHub/POE integration
- Plan manifest.json updates

### Step 5: Packaging a Skill

Once complete, package into distributable .skill file:

```bash
scripts/package_skill.py /path/to/skill
```

The packaging script:
1. **Validates** the skill (structure, metadata, references)
2. **Packages** into .skill file (zip format)

### Step 6: Iterate Based on Usage

After testing:
1. Notice struggles or inefficiencies
2. Identify how SKILL.md or resources should be updated
3. Implement changes and test again

## BL1NK Skill Validation

When creating a BL1NK skill, validate:

- [ ] Skill has clear name and description
- [ ] SKILL.md includes concrete examples
- [ ] Scripts are tested and working
- [ ] References are organized and linked
- [ ] Manifest.json will be updated with metadata
- [ ] Integration points are identified
- [ ] Phase placement is determined (Phase 1-4)
- [ ] Dependencies are documented

Use the validation script:
```bash
scripts/validate_blk_skill.py /path/to/skill
```

Analyze skill fit:
```bash
scripts/analyze_skill_fit.py /path/to/skill
```

## Learn Proven Design Patterns

Consult helpful guides in references:

- **Multi-step processes**: See `references/workflows.md`
- **Output formats**: See `references/output-patterns.md`
- **BL1NK patterns**: See `references/blk-patterns.md`
- **BL1NK examples**: See `references/blk-examples.md`
- **Phase approach**: See `references/phase-implementation.md`

## Common BL1NK Patterns

### Input/Output Pattern

```yaml
---
name: my-skill
inputs:
  param1:
    type: string
    description: What it does
    required: true
  param2:
    type: string
    default: default_value
outputs:
  result:
    type: object
  status:
    type: string
---
```

### JSON I/O Pattern (Python)

```python
#!/usr/bin/env python3
import json
import sys

# Read input
data = json.loads(sys.stdin.read())
param = data.get('param', 'default')

# Process
try:
    result = process(param)
    output = {'status': 'success', 'result': result}
except Exception as e:
    output = {'status': 'error', 'message': str(e)}

# Output
print(json.dumps(output))
```

## Resources

**In BL1NK Workspace:**
- 4 existing skills: `/home/user/skills/`
- Base code: `/home/user/projects/bl1nk-architect/src/`
- POE protocol: `/home/user/docs/poe-protocol/`
- Analysis: `/home/user/docs/skills-analysis/`

**In This Skill:**
- Patterns: `references/blk-patterns.md`
- Examples: `references/blk-examples.md`
- Phases: `references/phase-implementation.md`
- Templates: `assets/`

