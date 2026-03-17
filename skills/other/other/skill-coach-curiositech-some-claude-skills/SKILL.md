---
name: skill-coach
description: "Guides creation of high-quality Agent Skills with domain expertise, anti-pattern detection, and progressive disclosure best practices. Activate on keywords: create skill, review skill, skill quality, skill best practices, skill anti-patterns, improve skill, skill audit. NOT for general coding advice, slash commands, MCP development, or non-skill Claude Code features."
allowed-tools: Read,Write,Edit,Glob,Grep,Bash(python:*)
category: Productivity & Meta
tags:
  - skills
  - quality
  - anti-patterns
  - best-practices
  - review
pairs-with:
  - skill: agent-creator
    reason: Quality review for new skills
  - skill: automatic-stateful-prompt-improver
    reason: Optimize skill prompts
---

# Skill Coach: Creating Expert-Level Agent Skills

Encode real domain expertise, not just surface-level instructions. Focus on **shibboleths** - the deep knowledge that separates novices from experts.

## When to Use This Skill

**Use for:**
- Creating new Agent Skills from scratch
- Reviewing/auditing existing skills
- Improving skill activation rates
- Adding domain expertise to skills
- Debugging why skills don't activate

**NOT for:**
- General Claude Code features (slash commands, MCPs)
- Non-skill coding advice
- Debugging runtime errors (use domain skills)

## Quick Wins

**Immediate improvements for existing skills**:
1. **Add NOT clause** to description → Prevents false activation
2. **Add 1-2 anti-patterns** → Prevents common mistakes
3. **Check line count** (run validator) → Should be fewer than 500 lines
4. **Remove dead files** → Delete unreferenced scripts/references
5. **Test activation** → Questions that should/shouldn't trigger it

## What Makes a Great Skill

Great skills are **progressive disclosure machines** that:
1. **Activate precisely** - Specific keywords + NOT clause
2. **Encode shibboleths** - Expert knowledge that separates novice from expert
3. **Surface anti-patterns** - "If you see X, that's wrong because Y, use Z"
4. **Capture temporal knowledge** - "Pre-2024: X. 2024+: Y"
5. **Know their limits** - "Use for A, B, C. NOT for D, E, F"
6. **Provide decision trees** - Not templates, but "If X then A, if Y then B"
7. **Stay under 500 lines** - Core in SKILL.md, deep dives in /references

## Core Principles

### Progressive Disclosure

- **Phase 1 (~100 tokens)**: Metadata - "Should I activate?"
- **Phase 2 (&lt;5k tokens)**: SKILL.md - "How do I do this?"
- **Phase 3 (as needed)**: References - "Show me the details"

**Critical**: Keep SKILL.md under 500 lines. Split details into `/references`.

### Description Formula

**[What] [Use for] [Keywords] NOT for [Exclusions]**

```
❌ Bad: "Helps with images"
⚠️ Better: "Image processing with CLIP"
✅ Good: "CLIP semantic search. Use for image-text matching.
   Activate on 'CLIP', 'embeddings'. NOT for counting, spatial reasoning."
```

## SKILL.md Template

```markdown
---
name: your-skill-name
description: [What] [When] [Triggers]. NOT for [Exclusions].
allowed-tools: Read,Write  # Minimal only
---

# Skill Name
[One sentence purpose]

## When to Use
✅ Use for: [A, B, C]
❌ NOT for: [D, E, F]

## Core Instructions
[Step-by-step, decision trees, not templates]

## Common Anti-Patterns
### [Pattern]
**Symptom**: [Recognition]
**Problem**: [Why wrong]
**Solution**: [Better approach]
```

## Frontmatter Rules (CRITICAL)

**Only these frontmatter keys are allowed by Claude's skill marketplace:**

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | ✅ | Lowercase-hyphenated identifier |
| `description` | ✅ | Activation keywords + NOT clause |
| `allowed-tools` | ⚠️ | Comma-separated tool names |
| `license` | ❌ | e.g., "MIT" |
| `metadata` | ❌ | Custom key-value pairs |

**Invalid keys that will FAIL upload:**
```yaml
# ❌ WRONG - These will break skill upload
integrates_with:
  - orchestrator
triggers:
  - "activate on this"
tools: Read,Write
outputs: formatted text
coordinates_with: other-skill
python_dependencies:
  - numpy
```

**Move custom info to the body:**
```markdown
## Integrations
Works with: orchestrator, team-builder

## Activation Triggers
Responds to: "create skill", "review skill", "skill quality"
```

**Validation command:**
```bash
# Find invalid frontmatter keys
for skill in .claude/skills/*/SKILL.md; do
  sed -n '/^---$/,/^---$/p' "$skill" | grep -E "^[a-zA-Z_-]+:" | cut -d: -f1 | \
    grep -vE "^(name|description|license|allowed-tools|metadata)$" && \
    echo "  ^ in $(basename $(dirname $skill))"
done
```

## Skill Structure

**Mandatory**:
```
your-skill/
└── SKILL.md           # Core instructions (max 500 lines)
```

**Strongly Recommended** (self-contained skills):
```
├── scripts/           # Working code - NOT templates
├── mcp-server/        # Custom MCP if external APIs needed
├── agents/            # Subagent definitions if orchestration needed
├── references/        # Deep dives on domain knowledge
└── CHANGELOG.md       # Version history
```

## Self-Contained Skills (RECOMMENDED)

**Skills with working tools are immediately useful.** See `references/self-contained-tools.md` for full patterns.

**Quick decision**: External APIs? → MCP. Multi-step workflow? → Subagents. Repeatable operations? → Scripts.

## Decision Trees

**When to create a NEW skill?**
- ✅ Domain expertise not in existing skills
- ✅ Pattern repeats across 3+ projects
- ✅ Anti-patterns you want to prevent
- ❌ One-time task → Just do it directly
- ❌ Existing skill could be extended → Improve that one

**Skill vs Subagent vs MCP?**
- **Skill**: Domain expertise, decision trees (no runtime state)
- **Subagent**: Multi-step workflows needing tool orchestration
- **MCP**: External APIs, auth, stateful connections

## Skill Creation Process (6 Steps)

Follow these steps in order when creating a new skill:

### Step 1: Understand with Concrete Examples
Skip only if usage patterns are already clear. Ask:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"

### Step 2: Plan Reusable Contents
For each example, analyze:
1. How to execute from scratch
2. What scripts, references, assets would help with repeated execution

**Example analyses**:
- `pdf-editor` for "rotate this PDF" → Needs `scripts/rotate_pdf.py`
- `frontend-webapp-builder` → Needs `assets/hello-world/` template
- `big-query` skill → Needs `references/schema.md` for table schemas

### Step 3: Initialize the Skill
Create the skill directory structure:
```
your-skill/
├── SKILL.md           # Core instructions (max 500 lines)
├── scripts/           # Working code - NOT templates
├── references/        # Deep dives on domain knowledge
└── assets/            # Files used in output (templates, icons)
```

### Step 4: Write SKILL.md
- Write in **imperative/infinitive form** ("To accomplish X, do Y")
- Answer: Purpose? When to use? How to use bundled resources?
- Reference all scripts/references so Claude knows they exist

### Step 5: Validate and Package
```bash
# Validate skill structure and content
python scripts/validate_skill.py <path>

# Check for self-contained tool completeness
python scripts/check_self_contained.py <path>
```

### Step 6: Iterate
After real-world use:
1. Notice struggles or inefficiencies
2. Identify how SKILL.md or bundled resources should be updated
3. Implement changes and test again

---

## Common Workflows

**Create Skill from Expertise**:
1. Define scope: What expertise? What keywords? What NOT to handle?
2. Write description with keywords and NOT clause
3. Add anti-patterns you've observed
4. Test activation thoroughly

**Debug Activation Issues** (flowchart):
```
Skill not activating when expected?
├── Check description has specific keywords
│   ├── NO → Add "Activate on: keyword1, keyword2"
│   └── YES → Check if query contains those keywords
│       ├── NO → Add missing keyword variations
│       └── YES → Check for conflicting NOT clause
│           ├── YES → Narrow exclusion scope
│           └── NO → Check file structure
│               ├── SKILL.md missing → Create it
│               └── Wrong location → Move to .claude/skills/

Skill activating when it shouldn't?
├── Missing NOT clause?
│   ├── YES → Add "NOT for: exclusion1, exclusion2"
│   └── NO → NOT clause too narrow
│       └── Expand exclusions based on false positive queries
```
Run `python scripts/test_activation.py <path>` to validate

**Recursive Self-Improvement** (use this skill to improve skills):
1. Run `python scripts/validate_skill.py <path>` → Get validation report
2. Run `python scripts/check_self_contained.py <path>` → Check tool completeness
3. Address ERRORS first, then WARNINGS, then SUGGESTIONS
4. Re-run validation until clean
5. Update CHANGELOG.md with improvements made

## Tool Permissions

**Guidelines**:
- Read-only skill: `Read,Grep,Glob`
- File modifier: `Read,Write,Edit`
- Build integration: `Read,Write,Bash(npm:*,git:*)`
- ⚠️ **Never**: Unrestricted `Bash` for untrusted skills

## Success Metrics

| Metric | Target |
|--------|--------|
| Correct activation | &gt;90% |
| False positive rate | &lt;5% |
| Token usage | &lt;5k typical |

## Reference Files

| File | Contents |
|------|----------|
| `references/antipatterns.md` | Domain shibboleths and anti-pattern catalog with case studies |
| `references/shibboleths.md` | Expert vs novice knowledge patterns |
| `references/validation-checklist.md` | Complete review and testing guide |
| `references/self-contained-tools.md` | Scripts, MCP servers, and subagent implementation patterns |
| `references/scoring-rubric.md` | Quantitative skill evaluation (0-10 scoring) |
| `references/skill-composition.md` | Cross-skill dependencies and composition patterns |
| `references/skill-lifecycle.md` | Maintenance, versioning, and deprecation guidance |
| `references/mcp_vs_scripts.md` | Architectural decision guide: Skills vs Agents vs MCPs vs Scripts |

---

**This skill guides**: Skill creation | Skill auditing | Anti-pattern detection | Progressive disclosure | Domain expertise encoding
