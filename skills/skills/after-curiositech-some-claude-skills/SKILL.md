---
name: skill-coach
description: "Guides creation of high-quality Agent Skills with domain expertise, anti-pattern detection, and progressive disclosure best practices. Use when creating skills, reviewing existing skills, or when users mention improving skill quality, encoding expertise, or avoiding common AI tooling mistakes. Activate on keywords: create skill, review skill, skill quality, skill best practices, skill anti-patterns. NOT for general coding advice or non-skill Claude Code features."
allowed-tools: Read,Write,Bash,Glob,Grep,Edit
---

# Skill Coach: Creating Expert-Level Agent Skills

This skill helps you create Agent Skills that encode real domain expertise, not just surface-level instructions. It focuses on the **shibboleths** - the deep knowledge that separates novices from experts.

## When to Use This Skill

✅ **Use for:**
- Creating new Agent Skills from scratch
- Reviewing/auditing existing skills
- Improving skill activation rates
- Adding domain expertise to skills
- Debugging why skills don't activate

❌ **NOT for:**
- General Claude Code features (slash commands, MCPs)
- Non-skill coding advice
- Debugging runtime errors in skills (use specific domain skills)
- Project setup unrelated to skills

## What Makes a Great Skill

Great skills are **progressive disclosure machines** that:
1. **Activate precisely** - Specific keywords trigger, NOT clause prevents false activation
2. **Encode shibboleths** - Expert knowledge that separates novice from expert approaches
3. **Surface anti-patterns** - "If you see X, that's wrong because Y, use Z instead"
4. **Capture temporal knowledge** - "Pre-2024: X. 2024+: Y. Watch for: LLMs suggesting X"
5. **Know their limits** - "Use this for A, B, C. NOT for D, E, F. For D use skill-name-2"
6. **Provide decision trees** - Not templates, but "If X then A, if Y then B, never C"
7. **Stay under 500 lines** - Core in SKILL.md, deep dives in /references

## Quick Wins

**Immediate improvements for existing skills**:
1. **Add NOT clause** to description → Prevents false activation
2. **Add 1-2 anti-patterns** → Prevents common mistakes
3. **Check line count** (`wc -l`) → Should be &lt;500
4. **Remove dead files** → Delete unreferenced scripts/references
5. **Test activation** → Ask questions that should/shouldn't trigger it

## Quick Start

**Creating a New Skill**:
1. Define scope: What expertise? What keywords? What NOT to handle?
2. Write description with keywords and NOT clause
3. Add anti-patterns you've observed
4. Test activation thoroughly
5. Use Review Checklist below

## Core Principles

### 1. Progressive Disclosure Architecture

Skills load in three phases:
- **Phase 1 (~100 tokens)**: Metadata (name, description) - "Should I activate?"
- **Phase 2 (&lt;5k tokens)**: Main instructions in SKILL.md - "How do I do this?"
- **Phase 3 (as needed)**: Scripts, references, assets - "Show me the details"

**Critical**: Keep SKILL.md under 500 lines. Split details into `/references`.

### 2. Description Field Design

The description is your activation trigger. Formula: **[What] [Use for] [Keywords] NOT for [Exclusions]**

**Progression from Bad → Good**:

❌ **Bad**: `description: Helps with images`
- Too vague, no keywords, no exclusions

⚠️ **Better**: `description: Image processing with CLIP`
- Has keyword (CLIP) but no use cases or exclusions

✅ **Good**: `description: CLIP semantic search. Use for image-text matching, zero-shot classification. Activate on "CLIP", "embeddings", "image search". NOT for counting, fine-grained classification, spatial reasoning.`
- Clear capability, use cases, keywords, and exclusions

### 3. Anti-Pattern Detection

Great skills actively warn about common mistakes. Structure:

```markdown
## Common Anti-Patterns

### Pattern: [Name]
**What it looks like**: [Code example or description]
**Why it's wrong**: [Fundamental reason]
**What to do instead**: [Better approach]
**How to detect**: [Validation rule]
```

### 4. Temporal Knowledge

Technology evolves. Capture what changed and when:

```markdown
## Evolution Timeline

### Pre-2024: Old Approach
[What people used to do]

### 2024-Present: Current Best Practice
[What changed and why]

### Watch For
[Deprecated patterns LLMs might still suggest]
```

## Skill Structure

**Mandatory**:
```
your-skill/
└── SKILL.md           # Core instructions (&lt;500 lines)
```

**Optional** (only if needed):
```
├── scripts/           # Working code (not templates)
├── references/        # Deep dives (referenced from SKILL.md)
├── assets/            # Config files, templates
└── examples/          # Concrete good/bad examples
```

**Anti-pattern**: Creating structure "just in case" - only add files that SKILL.md references

## SKILL.md Template Structure

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

## Anti-Patterns in Skill Creation

### Anti-Pattern: The Reference Illusion

**What it looks like**: Skill references scripts/files that don't exist
```yaml
# Quick Start
Run `python scripts/validate.py` to check your skill
```
But `/scripts/validate.py` doesn't exist in the skill directory.

**Why it's wrong**: Claude will try to use non-existent files, causing errors and confusion.

**What to do instead**: Only reference files that actually exist. If you want to suggest scripts, either:
1. Include them in the skill
2. Show inline code examples
3. Clearly mark as "Example - not included"

**How to detect**: `find skill-dir/ -type f` and verify all referenced paths exist

### Anti-Pattern: Description Soup

**What it looks like**:
```yaml
description: Helps with many things including X, Y, Z, and also A, B, C, plus general assistance
```

**Why it's wrong**: Vague descriptions cause:
- False activations (activates when shouldn't)
- Missed activations (doesn't activate when should)
- Token waste (loads unnecessary context)

**What to do instead**: Specific trigger keywords + clear exclusions
```yaml
description: [Core capability]. Use for [A, B, C]. Activate on keywords: "X", "Y", "Z". NOT for [D, E, F].
```

### Anti-Pattern: Template Theater

**What it looks like**: Skill is 90% templates and examples, 10% actual instructions

**Why it's wrong**: Claude doesn't need templates - it needs expert knowledge and decision trees. Templates are for humans.

**What to do instead**:
- Focus on WHEN to use patterns, not just WHAT the patterns are
- Encode decision logic: "If X, use A; if Y, use B; never use C"
- Include anti-patterns and edge cases

### Anti-Pattern: The Everything Skill

**What it looks like**: One skill trying to handle an entire domain
```yaml
name: web-dev-expert
description: Handles all web development tasks
```

**Why it's wrong**:
- Too broad to activate correctly
- Mixes concerns (React ≠ API design ≠ CSS)
- Violates progressive disclosure

**What to do instead**: Create focused, composable skills:
- `react-performance-expert`
- `api-design-expert`
- `css-layout-expert`

### Anti-Pattern: Orphaned Sections

**What it looks like**: Skill has `/references/deep_dive.md` but never tells Claude when to read it

**Why it's wrong**: Files exist but are never used = wasted space

**What to do instead**: Explicit triggers in main SKILL.md:
```markdown
For database-specific anti-patterns, see `/references/database_antipatterns.md`
```

## Evolution Timeline: Skill Framework Best Practices

### 2024 Early: First Skills
- Basic SKILL.md files
- Heavy use of bash scripts
- Minimal structure

### 2024 Mid: Progressive Disclosure
- Introduction of phased loading
- `allowed-tools` constraints
- Reference directory pattern

### 2024 Late: Anti-Pattern Focus
- Shift from "what to do" to "what NOT to do"
- Temporal knowledge capture
- Shibboleth encoding

### 2025: Current Best Practices
- Sub-500 line SKILL.md
- Validation-first approach
- Clear activation boundaries
- Working code examples (not just templates)

## Domain-Specific Shibboleths

Shibboleths = deep knowledge that separates novices from experts.

### Skill Creation Shibboleths

**Novice skill creator**:
- "I'll make a comprehensive skill that handles everything related to X"
- Focuses on templates and examples
- Description: "Helps with many things"
- Thinks more tools = better

**Expert skill creator**:
- "I'll create a focused skill that encodes THIS specific expertise about X"
- Focuses on decision trees and anti-patterns
- Description: "Does A, B, C. Activate on keywords X, Y. NOT for D, E, F."
- Minimal tools, knows when NOT to use the skill
- Encodes temporal knowledge: "Pre-2024 pattern X was common, now use Y"

### Domain Example Shibboleths

**CLIP Embeddings**:
- Novice: "CLIP is great for image-text matching"
- Expert: "CLIP fails at: counting, fine-grained classification, attribute binding, spatial relationships, negation. Use DCSMs for compositional, PC-CLIP for geometric, specialized models for counting."

**MCPs vs Scripts**:
- Novice: "MCPs are better because they're more powerful"
- Expert: "MCP for auth/external APIs. Script for local/stateless. Building an MCP when a script would suffice = anti-pattern."

## Validation Best Practices

**Plan-Validate-Execute Pattern**:
1. Generate plan → 2. Validate BEFORE execution → 3. Execute → 4. Verify

**Pre-Flight Checks** (include in skills that modify state):
- Structure validation (files exist, naming conventions)
- Description quality (keywords, exclusions, length)
- Anti-pattern detection
- Progressive disclosure compliance
- Line count (&lt;500 for SKILL.md)

## Example: Good vs Bad Skills

**Good Skill** - Specific, expert knowledge, clear boundaries:
```yaml
name: clip-aware-embeddings
description: CLIP semantic search. Use for image-text matching, zero-shot classification. Activate on "CLIP", "embeddings", "image search". NOT for counting, fine-grained classification, spatial reasoning.

✅ Includes: When NOT to use, alternatives (DETR/PC-CLIP), temporal evolution, anti-patterns
```

**Bad Skill** - Vague, template-heavy, no expertise:
```yaml
name: image-processing
description: Processes images

❌ Problems: No activation triggers, no exclusions, no expert knowledge, just generic templates
```

## Integration with Other Tools

### Works Well With

- **MCP Servers**: For API access, skill provides the workflow
- **Subagents**: Skill gives expertise, subagent gets tool permissions
- **Projects**: Skill available across all conversations

### Conflicts With

- **Overly specific prompts**: Skill already encodes the pattern
- **Too many tools**: Use `allowed-tools` to constrain scope

## Common Workflows

**Workflow 1: Create Skill from Expertise**
1. You have domain expertise → Activate skill-coach
2. Ask: "Help me create a skill for [domain]"
3. Define scope, keywords, exclusions
4. Encode shibboleths (expert knowledge)
5. Add anti-patterns you've observed
6. Test activation

**Workflow 2: Debug Activation Issues**
1. Skill not activating → Activate skill-coach
2. Ask: "Review my skill's description and activation triggers"
3. Add missing keywords
4. Clarify NOT clause
5. Test with specific phrases

**Workflow 3: Reduce False Activations**
1. Skill activates too often → Activate skill-coach
2. Ask: "Help me narrow this skill's scope"
3. Add NOT clause with exclusions
4. Consider splitting into multiple focused skills
5. Test edge cases

## Iterating on Skills

**Improvement Loop** (use Claude to improve skills):
```bash
# 1. Use the skill on real tasks
# 2. Ask: "What anti-patterns did you encounter?"
# 3. Ask: "What decision points were unclear?"
# 4. Update SKILL.md with learnings
# 5. Test: Does it activate correctly now?
```

**Red Flags**:
- Skill doesn't activate when it should → Fix description keywords
- Activates too often → Add NOT clause
- Claude ignores sections → Move to main SKILL.md or delete
- Claude can't find referenced files → Remove or create them

## Tool Permissions

**This skill uses**: `Read,Write,Bash,Glob,Grep,Edit`
- **Read,Glob,Grep**: Find and read existing skills
- **Edit**: Update skills in place
- **Write**: Create new skill files
- **Bash**: Validate file structure (`find`, `wc -l`)

**Guidelines**:
- Read-only skill: `Read,Grep,Glob`
- File modifier: `Read,Write,Edit`
- Build integration: `Read,Write,Bash(npm:*,git:*)`
- ⚠️ **Never**: Unrestricted `Bash` for untrusted skills

**Security Audit**:
- [ ] Read all scripts before enabling skill
- [ ] Check for network calls / data exfiltration
- [ ] Verify allowed-tools are minimal
- [ ] Test in isolated project first

## Skill Review Checklist

**CRITICAL** (must-have):
- [ ] Description has keywords AND NOT clause
- [ ] SKILL.md under 500 lines
- [ ] All referenced files exist (`find skill-dir/ -type f`)
- [ ] Test activation: Does it activate when it should?
- [ ] Test non-activation: Does it NOT activate when it shouldn't?

**HIGH PRIORITY** (should-have):
- [ ] Has "When to Use" and "When NOT to Use" sections
- [ ] Includes 1-3 anti-patterns with "Why it's wrong"
- [ ] Encodes domain shibboleths (expert vs novice knowledge)
- [ ] `allowed-tools` is minimal

**NICE TO HAVE** (polish):
- [ ] Temporal knowledge (what changed when)
- [ ] Working code examples (not just templates)
- [ ] References for deep dives
- [ ] Bash restrictions if applicable

## Testing Your Skill

### Activation Test

Ask Claude questions that SHOULD trigger the skill:
```bash
# Example for a React skill:
"Help me optimize this React component's re-renders"
# Check: Did the skill activate?
```

Ask questions that SHOULD NOT trigger the skill:
```bash
# Example for a React skill:
"Help me write a Python script"
# Check: Did it correctly NOT activate?
```

### Integration Test

- Test with related skills (do they conflict or complement?)
- Test with MCPs (does skill guide MCP usage?)
- Test in different project contexts

## Decision Trees

**When to create a NEW skill?**
- ✅ You have domain expertise not in existing skills
- ✅ Pattern repeats across 3+ projects
- ✅ Anti-patterns you want to prevent
- ❌ One-time task → Just do it directly
- ❌ Existing skill could be extended → Improve that one

**Skill vs Subagent vs MCP?**
- **Skill**: Domain expertise, decision trees, anti-patterns (no runtime state)
- **Subagent**: Multi-step workflows needing tool orchestration
- **MCP**: External APIs, auth, stateful connections

## Common Questions

**Q: SKILL.md vs /references?**
SKILL.md: Core instructions (&lt;500 lines). /references: Deep dives (loaded as needed).

**Q: How do I handle deprecated patterns?**
```markdown
## ⚠️ Deprecated: [Pattern]
**Until**: [Date] | **Why**: [Reason] | **Now use**: [Current]
**Watch**: LLMs may suggest this due to training data
```

## Success Metrics

- **Activation**: 90%+ when appropriate, &lt;5% false positives
- **Token efficiency**: &lt;5k tokens typical invocation
- **Error prevention**: Measurable reduction in common mistakes

---

**This skill guides**: Skill creation | Skill auditing | Anti-pattern detection | Progressive disclosure | Domain expertise encoding

**Meta-note**: This skill practices what it preaches - it has been iteratively improved using its own guidance, demonstrating the iteration loop it recommends.
