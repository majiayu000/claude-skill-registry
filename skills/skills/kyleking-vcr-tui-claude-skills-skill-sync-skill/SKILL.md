---
name: skill-sync
description: Syncs Claude Skills with other AI coding tools like Cursor, Copilot, and Codeium by creating cross-references and shared knowledge bases. Invoke when user wants to leverage skills across multiple tools or create unified AI context.
---

# Skill Sync - Cross-Tool Knowledge Sharing

You are an expert at syncing Claude Skills with other AI coding assistants (Cursor, GitHub Copilot, Codeium, etc.) to create a unified knowledge base. This skill helps maximize the value of documented knowledge across your entire development toolchain.

## What is Skill Sync?

Skill Sync enables:
- Sharing skill knowledge with other AI tools
- Creating cross-references in tool configs
- Maintaining unified project context
- Reducing duplicate documentation
- Ensuring consistent guidance across tools

## When to Use This Skill

Invoke this skill when the user:

- Wants to **share skills with Cursor, Copilot, or other tools**
- Asks to **create .cursorrules or similar configs**
- Needs **unified AI context** across multiple assistants
- Wants to **reference skills in other tools**
- Asks about **cross-tool integration**
- Needs to **sync project knowledge** between AI assistants

## Supported Tools

### 1. Cursor

**Configuration Method:** `.cursorrules` file

Cursor reads `.cursorrules` in the project root for context and instructions.

**Capabilities:**
- Markdown-based instructions
- Project-specific context
- Code style guidelines
- Framework preferences

### 2. GitHub Copilot

**Configuration Method:** Inline comments and project structure

Copilot learns from:
- Existing code patterns
- Comments and docstrings
- File organization
- README and documentation

**Limitations:**
- No dedicated config file (as of 2025)
- Context comes from open files
- Less explicit guidance than Cursor

### 3. Codeium

**Configuration Method:** Project documentation

Codeium uses:
- README.md and docs/
- Code comments
- Existing patterns

### 4. Continue.dev

**Configuration Method:** `.continuerc.json` or config.json

Continue supports:
- Custom context providers
- Documentation references
- Project-specific prompts

### 5. Tabnine

**Configuration Method:** Inline patterns

Tabnine learns from:
- Codebase patterns
- Team standards (enterprise)

## Sync Strategies

### Strategy 1: Reference-Based (Recommended)

**Concept:** Other tools reference Claude Skills without duplicating content.

**Benefits:**
- Single source of truth (Claude Skills)
- Easy to maintain
- No duplication
- Clear ownership

**Implementation:**

```markdown
# .cursorrules

This project uses Claude Skills for detailed technical guidance.

## Framework Guidance

For Textual TUI development patterns, see:
- `.claude/skills/textual/SKILL.md` - Core concepts and patterns
- `.claude/skills/textual/quick-reference.md` - Quick lookups

When suggesting Textual code:
1. Follow patterns in `.claude/skills/textual/`
2. Use semantic color variables ($primary, $error, etc.)
3. Prefer composition over inheritance
4. Use reactive attributes for state

## Git Hook Management

For git hook configuration with hk, see:
- `.claude/skills/hk/SKILL.md` - Setup and patterns
- `.claude/skills/hk/reference.md` - Detailed options

## Testing Patterns

For pytest conventions, see:
- `.claude/skills/pytest-patterns/` (if exists)
```

### Strategy 2: Summary-Based

**Concept:** Create condensed summaries of skills for other tools.

**Benefits:**
- Self-contained for each tool
- No file path dependencies
- Works with limited context windows

**Implementation:**

```markdown
# .cursorrules

## Textual TUI Framework

This project uses Textual for building terminal UIs.

### Key Patterns
- Use reactive attributes for state: `count = reactive(0)`
- Follow "attributes down, messages up" for widget communication
- Use external CSS files for styling
- Always await async operations: `await self.mount(widget)`

### Common Mistakes to Avoid
- Don't modify reactives in __init__ (use on_mount)
- Always use `await pilot.pause()` in tests
- Don't block the event loop (use @work decorator)

For comprehensive guidance: `.claude/skills/textual/`

[More condensed summaries...]
```

### Strategy 3: Shared Documentation

**Concept:** Create a central docs/ directory that all tools reference.

**Benefits:**
- Clear documentation structure
- Easy for humans to read
- Tools can reference same files
- Good for team onboarding

**Structure:**

```
docs/
├── frameworks/
│   ├── textual.md          # Extracted from Claude Skill
│   └── pytest.md
├── patterns/
│   ├── testing.md
│   └── async.md
└── conventions/
    ├── code-style.md
    └── git-workflow.md

.cursorrules                 # References docs/*
.claude/skills/              # Detailed skills
```

## Implementation Guides

### Creating .cursorrules

**Basic Template:**

```markdown
# Project: [Project Name]

## Overview

[Brief project description]

## Tech Stack

- **Framework**: Textual (TUI framework)
- **Testing**: pytest with async support
- **Tools**: hk (git hooks), ruff (linting)

## AI Guidance Sources

This project maintains detailed knowledge in Claude Skills (`.claude/skills/`).

For comprehensive guidance on:
- **Textual framework**: `.claude/skills/textual/`
- **Git hooks (hk)**: `.claude/skills/hk/`
- **[Other skills]**: `.claude/skills/[name]/`

## Key Patterns

### Textual Development

1. **Widget Structure**
   ```python
   class MyWidget(Widget):
       count = reactive(0)

       def compose(self) -> ComposeResult:
           yield ChildWidget()
   ```

2. **Testing Pattern**
   ```python
   async with app.run_test() as pilot:
       await pilot.click("#button")
       await pilot.pause()  # Critical!
   ```

3. **CSS Styling**
   - Use semantic colors: `$primary`, `$error`, `$success`
   - FR units for flexible sizing: `width: 1fr;`
   - Dock for fixed elements: `dock: top;`

### Code Quality

- Run `hk check` before committing
- All tests must pass
- Type hints required
- Use ruff for formatting

## Common Mistakes

- ❌ Don't modify reactives in `__init__`
- ❌ Don't forget `await pilot.pause()` in tests
- ❌ Don't block the event loop
- ✅ Use `@work` decorator for async operations
- ✅ Use `set_reactive()` for init-time values

## Project Structure

```
src/
├── app.py              # Main app
├── screens/            # Screen classes
├── widgets/            # Custom widgets
└── business_logic/     # Separate from UI
```

## Additional Context

For detailed explanations, examples, and troubleshooting:
1. Check relevant skill in `.claude/skills/`
2. Refer to framework documentation
3. See examples in existing codebase
```

### Integrating with Cursor AI

**Step 1: Create .cursorrules**

```bash
# Generate .cursorrules from skills
cat > .cursorrules << 'EOF'
# [Content from template above]
EOF
```

**Step 2: Test Integration**

1. Open project in Cursor
2. Ask Cursor: "How should I create a Textual widget?"
3. Verify it references patterns from .cursorrules

**Step 3: Maintain Sync**

When updating skills:
```bash
# Update .cursorrules with key changes
# Keep it concise - full details stay in .claude/skills/
```

### Integrating with GitHub Copilot

Copilot learns from context, so:

**Step 1: Add Context Comments**

```python
# This project uses Textual TUI framework
# Follow patterns in .claude/skills/textual/
# Key principle: "attributes down, messages up"

from textual.app import App
from textual.widget import Widget
```

**Step 2: Create Documentation File**

```markdown
# docs/COPILOT_CONTEXT.md

## Development Context for AI Assistants

This file provides context for GitHub Copilot and similar tools.

### Framework: Textual

We use Textual for building terminal UIs. Key patterns:

[Include condensed patterns from skills]

For full details: `.claude/skills/textual/`
```

**Step 3: Reference in README**

```markdown
# README.md

## For AI Assistants

Development guidance is available in:
- `.claude/skills/` - Comprehensive Claude Skills
- `docs/COPILOT_CONTEXT.md` - Quick reference for all AI tools
```

### Integrating with Continue.dev

**Step 1: Create Context Provider**

```json
// .continue/config.json
{
  "contextProviders": [
    {
      "name": "skills",
      "type": "file",
      "params": {
        "patterns": [
          ".claude/skills/*/SKILL.md",
          ".claude/skills/*/quick-reference.md"
        ]
      }
    }
  ]
}
```

**Step 2: Configure Custom Commands**

```json
{
  "customCommands": [
    {
      "name": "textual-help",
      "prompt": "Refer to .claude/skills/textual/ and help with: {input}",
      "description": "Get Textual framework help"
    }
  ]
}
```

## Sync Maintenance Workflow

### When Creating a New Skill

1. **Create Claude Skill** (primary source)
   ```bash
   mkdir -p .claude/skills/new-skill
   # Create SKILL.md, etc.
   ```

2. **Update .cursorrules** (if needed)
   ```markdown
   ## New Skill Topic

   Brief summary...

   For details: `.claude/skills/new-skill/`
   ```

3. **Update docs/** (if using shared docs)
   ```bash
   # Extract key points to docs/
   # Keep synchronized
   ```

4. **Test cross-tool**
   - Ask Claude and Cursor same question
   - Verify consistent guidance

### When Updating an Existing Skill

1. **Update Claude Skill first**
   ```bash
   # Edit .claude/skills/skill-name/SKILL.md
   ```

2. **Review impact on other tools**
   - Check if .cursorrules needs updates
   - Update summary content
   - Sync shared docs

3. **Test changes**
   - Verify updated guidance works
   - Check for contradictions

### Regular Sync Checks

**Monthly:**
- Review .cursorrules for accuracy
- Check shared docs are current
- Test sample queries across tools

**Quarterly:**
- Full audit of cross-tool consistency
- Update summaries with new patterns
- Refactor if needed

## File Organization

### Recommended Structure

```
project/
├── .cursorrules                    # Cursor AI context
├── .claude/
│   ├── skills/                     # Primary knowledge base
│   │   ├── textual/
│   │   ├── hk/
│   │   └── ...
│   └── settings.local.json
├── docs/
│   ├── COPILOT_CONTEXT.md         # Context for Copilot
│   ├── AI_GUIDANCE.md             # General AI context
│   └── frameworks/                # Shared framework docs
├── README.md                       # References AI guidance
└── CONTRIBUTING.md                 # Development guidelines
```

### File Responsibilities

| File | Purpose | Audience | Detail Level |
|------|---------|----------|--------------|
| `.claude/skills/` | Comprehensive skills | Claude Code | High |
| `.cursorrules` | Cursor context | Cursor AI | Medium |
| `docs/COPILOT_CONTEXT.md` | Copilot context | GitHub Copilot | Medium |
| `docs/AI_GUIDANCE.md` | General AI context | All AI tools | Low-Medium |
| `README.md` | Project overview | Humans & AI | Low |

## Advanced Patterns

### Dynamic Context Generation

Create scripts to generate tool configs from skills:

```python
# scripts/generate_cursorrules.py

"""Generate .cursorrules from Claude Skills."""

import re
from pathlib import Path

def extract_key_concepts(skill_md: str) -> str:
    """Extract core concepts from SKILL.md."""
    # Parse markdown, extract key sections
    # Create condensed summary
    pass

def generate_cursorrules():
    """Generate .cursorrules from all skills."""
    skills_dir = Path(".claude/skills")

    output = ["# Project AI Context\n"]
    output.append("Generated from Claude Skills\n\n")

    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                concepts = extract_key_concepts(skill_md.read_text())
                output.append(f"## {skill_dir.name}\n")
                output.append(concepts)
                output.append(f"\nDetails: `.claude/skills/{skill_dir.name}/`\n\n")

    Path(".cursorrules").write_text("".join(output))

if __name__ == "__main__":
    generate_cursorrules()
```

**Usage:**

```bash
# Regenerate .cursorrules from skills
python scripts/generate_cursorrules.py

# Add to git hooks
cat >> hk.pkl << 'EOF'
["sync-cursorrules"] {
  glob = ".claude/skills/**/*.md"
  fix = "python scripts/generate_cursorrules.py"
  stage = ".cursorrules"
}
EOF
```

### Version-Aware Syncing

Track which skill versions are synced:

```markdown
# .cursorrules

<!-- Generated from Claude Skills -->
<!-- Last updated: 2025-01-09 -->
<!-- Sources:
  - textual: v2.0 (2025-01-09)
  - hk: v1.0 (2024-11-08)
-->

[Content...]
```

### Tool-Specific Sections

Different tools have different capabilities:

```markdown
# .cursorrules

## Core Patterns
[Universal guidance for all tools]

## Cursor-Specific
[Advanced features only Cursor supports]

## Copilot Context
If using GitHub Copilot, note:
- [Copilot-specific guidance]

## Continue.dev Context
If using Continue:
- Use @skills context provider
- Run `textual-help` custom command
```

## Best Practices

### Do's

- ✅ Keep `.claude/skills/` as the source of truth
- ✅ Use references rather than duplication
- ✅ Maintain consistent terminology across tools
- ✅ Test guidance with actual queries
- ✅ Update all synced files together
- ✅ Document sync strategy in README
- ✅ Automate sync when possible

### Don'ts

- ❌ Duplicate entire skills in .cursorrules
- ❌ Create contradictory guidance
- ❌ Let synced files become outdated
- ❌ Over-complicate sync process
- ❌ Ignore tool-specific limitations
- ❌ Make .cursorrules too long (> 2000 lines)

## Troubleshooting

### Tools Give Different Guidance

**Problem:** Cursor says one thing, Claude says another

**Solutions:**
1. Check if .cursorrules is outdated
2. Verify skill has been updated
3. Ensure consistent terminology
4. Update synced files
5. Test queries in both tools

### .cursorrules Too Large

**Problem:** File becomes unwieldy (> 2000 lines)

**Solutions:**
1. Use more references, less duplication
2. Extract to docs/ directory
3. Keep only critical patterns
4. Link to full skills
5. Consider multiple .cursorrules (if tool supports)

### Sync Maintenance Burden

**Problem:** Keeping files in sync is tedious

**Solutions:**
1. Automate with scripts
2. Use git hooks (via hk)
3. Add to CI checks
4. Reduce duplication
5. Only sync high-value content

### Tool Not Using Context

**Problem:** AI tool ignores .cursorrules or docs

**Solutions:**
1. Verify file location (must be project root)
2. Check file format and syntax
3. Restart IDE/tool
4. Test with explicit references
5. Check tool's documentation for context handling

## Integration Examples

### Example 1: Textual TUI Project

**Setup:**

```bash
# 1. Claude Skills (detailed)
.claude/skills/textual/
├── SKILL.md               # Comprehensive guide
├── quick-reference.md     # Quick lookups
└── guide.md              # Deep dive

# 2. Cursor context (condensed)
.cursorrules              # Key patterns + reference to skills

# 3. Shared docs (optional)
docs/
└── frameworks/
    └── textual.md        # Human-readable summary
```

**.cursorrules excerpt:**

```markdown
## Textual Framework

Building TUI apps with Textual.

### Core Pattern: Reactive Attributes
```python
class Counter(Widget):
    count = reactive(0)  # Auto-refreshes UI
```

### Testing Pattern
```python
async with app.run_test() as pilot:
    await pilot.click("#button")
    await pilot.pause()  # Essential!
```

**Full details:** `.claude/skills/textual/`
```

### Example 2: Multi-Framework Project

**Project uses:** Django + React + PostgreSQL

**Strategy:** Separate skills, unified .cursorrules

```markdown
# .cursorrules

## Backend (Django)

Patterns: `.claude/skills/django/`

Key points:
- Use class-based views
- Prefer serializers over manual JSON
- [...]

## Frontend (React)

Patterns: `.claude/skills/react/`

Key points:
- Functional components with hooks
- Use Context for global state
- [...]

## Database (PostgreSQL)

Patterns: `.claude/skills/postgres/`

Key points:
- Use migrations for schema changes
- Optimize queries with indexes
- [...]
```

## Templates

### Minimal .cursorrules Template

```markdown
# [Project Name]

## Overview
[Brief description]

## AI Knowledge Base

Comprehensive guidance in `.claude/skills/`:
- **[skill-1]**: [brief description]
- **[skill-2]**: [brief description]

## Key Patterns

### [Topic 1]
[2-3 line summary]
Details: `.claude/skills/[skill-name]/`

### [Topic 2]
[2-3 line summary]
Details: `.claude/skills/[skill-name]/`

## Quick Reference

[Essential commands/patterns only]

For comprehensive help, see Claude Skills in `.claude/skills/`
```

### Comprehensive .cursorrules Template

See full template in supporting documentation (if created).

## Instructions for Using This Skill

When helping users sync skills:

1. **Assess current setup**: What tools are they using?
2. **Choose strategy**: Reference-based, summary-based, or shared docs?
3. **Implement sync**: Create .cursorrules or equivalent
4. **Test integration**: Verify tools use the context
5. **Document approach**: Explain sync strategy in README
6. **Automate if possible**: Create scripts for maintenance

Always consider:
- What tools does the team use?
- How much duplication is acceptable?
- How will sync be maintained?
- What's the right level of detail for each tool?

## Additional Resources

Related skills:
- **skill-manager**: Creating and updating skills
- **skill-analyzer**: Identifying needed skills

## Version Notes

This skill reflects integration patterns as of January 2025. Tool capabilities and configuration methods may evolve.
