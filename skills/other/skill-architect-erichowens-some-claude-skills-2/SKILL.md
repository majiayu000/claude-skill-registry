---
name: skill-architect
description: Authoritative meta-skill for creating, auditing, and improving Agent Skills. Combines skill-coach expertise with skill-creator workflows. Use for skill creation, validation, improvement, activation debugging, and progressive disclosure design. NOT for general Claude Code features, runtime debugging, or non-skill coding.
allowed-tools: Read,Write,Edit,Bash
---

# Skill Architect: The Authoritative Meta-Skill

The unified authority for creating expert-level Agent Skills. Combines systematic workflow from skill-creator with domain expertise encoding from skill-coach.

## Philosophy

**Great skills are progressive disclosure machines** that encode real domain expertise (shibboleths), not just surface instructions. They activate precisely, teach efficiently, and make users productive immediately.

---

## When to Use This Skill

✅ **Use for**:
- Creating new skills from scratch
- Auditing/reviewing existing skills
- Improving activation rates
- Adding domain expertise
- Debugging why skills don't activate
- Encoding anti-patterns and shibboleths
- Building self-contained tools (scripts, MCPs, subagents)

❌ **NOT for**:
- General Claude Code features (slash commands, MCPs)
- Non-skill coding advice
- Debugging runtime errors (use domain-specific skills)
- Template generation without domain expertise

---

## Quick Wins (Immediate Improvements)

For existing skills, apply these in order:

1. **Add NOT clause** → Prevent false activation
2. **Check line count** → SKILL.md should be &lt;500 lines
3. **Add 1-2 anti-patterns** → Prevent common mistakes
4. **Remove dead files** → Delete unreferenced scripts/references
5. **Test activation** → Write queries that should/shouldn't trigger

Run validation:
```bash
python scripts/validate_skill.py <path>
python scripts/check_self_contained.py <path>
```

---

## What Makes a Great Skill

Great skills have these 7 qualities:

1. **Activate precisely** - Specific keywords + NOT clause
2. **Encode shibboleths** - Expert knowledge that separates novice from expert
3. **Surface anti-patterns** - "If you see X, that's wrong because Y, use Z"
4. **Capture temporal knowledge** - "Pre-2024: X. 2024+: Y"
5. **Know their limits** - "Use for A, B, C. NOT for D, E, F"
6. **Provide decision trees** - Not templates, but "If X then A, if Y then B"
7. **Stay under 500 lines** - Core in SKILL.md, deep dives in `/references`

---

## Progressive Disclosure Principle

Skills use a three-level loading system:

| Level | Content | Size | When Loaded |
|-------|---------|------|-------------|
| 1. Metadata | `name` + `description` | ~100 tokens | Always in context |
| 2. SKILL.md | Core instructions | &lt;5k tokens | When skill triggers |
| 3. Resources | Scripts, references, assets | Unlimited | As Claude needs them |

**Critical**: Keep SKILL.md under 500 lines. Move details to `/references`.

---

## Skill Structure

### Mandatory
```
your-skill/
└── SKILL.md           # Core instructions (max 500 lines)
```

### Strongly Recommended (Self-Contained Skills)
```
├── scripts/           # Working code - NOT templates
├── mcp-server/        # Custom MCP if external APIs needed
├── agents/            # Subagent definitions for orchestration
├── references/        # Deep dives on domain knowledge
└── CHANGELOG.md       # Version history
```

**Philosophy**: Skills with working tools are immediately useful.

---

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
✅ Use for: [A, B, C with specific keywords]
❌ NOT for: [D, E, F - be explicit]

## Core Instructions
[Step-by-step decision trees, not templates]

## Common Anti-Patterns
### [Pattern Name]
**Novice thinking**: [Wrong assumption]
**Reality**: [Why it's wrong]
**Correct approach**: [Better way]
**Timeline**: [When this changed]

## References
- `/references/deep-dive.md` - [When to consult]
```

---

## Description Formula

**[What] [When] [Keywords] NOT for [Exclusions]**

**Examples**:

❌ **Bad**: "Helps with images"
⚠️ **Better**: "Image processing with CLIP"
✅ **Good**: "CLIP semantic search. Use for image-text matching, zero-shot classification. Activate on 'CLIP', 'embeddings', 'similarity'. NOT for counting objects, spatial reasoning, or fine-grained classification."

---

## Frontmatter Rules (CRITICAL)

**Only these keys are allowed by Claude's skill marketplace:**

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | ✅ | Lowercase-hyphenated identifier |
| `description` | ✅ | Activation keywords + NOT clause |
| `allowed-tools` | ⚠️ | Comma-separated tool names |
| `license` | ❌ | e.g., "MIT" |
| `metadata` | ❌ | Custom key-value pairs |

**Invalid keys that WILL FAIL upload**:
```yaml
# ❌ WRONG - These break skill upload
integrates_with: [...]
triggers: [...]
tools: Read,Write  # Use 'allowed-tools' instead
outputs: [...]
coordinates_with: [...]
python_dependencies: [...]
```

**Move custom info to body** under appropriate headings.

---

## The 6-Step Skill Creation Process

### Step 1: Understand with Concrete Examples

Skip only if usage patterns are already clear.

**Ask**:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would trigger this skill?"

**Example queries** (for an image-editor skill):
- "Remove red-eye from this image"
- "Rotate this photo 90 degrees"
- "Adjust brightness and contrast"

Conclude when you have 3-5 concrete examples.

---

### Step 2: Plan Reusable Contents

For each example, analyze:
1. How to execute from scratch
2. What scripts/references/assets would help with repeated execution

**Example analyses**:

| Skill | Example | Needs |
|-------|---------|-------|
| pdf-editor | "Rotate this PDF" | `scripts/rotate_pdf.py` |
| frontend-builder | "Build a todo app" | `assets/hello-world/` template |
| big-query | "How many users logged in?" | `references/schema.md` |
| photo-expert | "Improve composition" | `scripts/analyze_composition.py` |

**Shibboleths to encode**:
- Domain-specific algorithms
- Common pitfalls and anti-patterns
- Temporal knowledge (what changed when)
- Framework evolution patterns

---

### Step 3: Initialize the Skill

**For new skills**, run the init script:
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates:
- SKILL.md template with proper frontmatter
- Example `scripts/`, `references/`, `assets/` directories
- TODO placeholders to customize

**For existing skills**, skip to Step 4.

---

### Step 4: Edit the Skill

#### Write in Imperative/Infinitive Form
Use objective, instructional language:
- ✅ "To accomplish X, do Y"
- ✅ "When Z occurs, execute A"
- ❌ "You should do X"
- ❌ "If you need to do Z"

#### Start with Reusable Contents

Implement in this order:
1. **Scripts** (`scripts/`) - Working code for repeatable operations
2. **References** (`references/`) - Domain knowledge, schemas, detailed guides
3. **Assets** (`assets/`) - Templates, boilerplate, files used in output

**Delete example files** that aren't needed.

#### Update SKILL.md

Answer these questions:
1. **Purpose**: What is this skill for? (1-2 sentences)
2. **When to use**: Specific triggers and exclusions
3. **How to use**: Reference all bundled resources so Claude knows they exist
4. **Anti-patterns**: What mistakes do novices make?
5. **Temporal context**: What changed and when?

---

### Step 5: Validate and Package

```bash
# Validate structure and content
python scripts/validate_skill.py <path>

# Check self-contained tool completeness
python scripts/check_self_contained.py <path>

# Package for distribution (validates first)
python scripts/package_skill.py <path/to/skill-folder>
```

Fix all ERRORS, then WARNINGS, then SUGGESTIONS.

---

### Step 6: Iterate

After real-world use:
1. Notice struggles or inefficiencies
2. Identify how SKILL.md or bundled resources should improve
3. Implement changes and test again
4. Update CHANGELOG.md

**Recursive self-improvement**: Use this skill to improve skills.

---

## Encoding Shibboleths (Expert Knowledge)

### What Are Shibboleths?

Knowledge that separates novices from experts - things LLMs get wrong because training data includes:
- Outdated patterns
- Oversimplified tutorials
- Cargo-culted code

### Shibboleth Template

```markdown
### Anti-Pattern: [Name]

**Novice thinking**: "[Wrong assumption]"

**Reality**: [Fundamental reason it's wrong, with research/data]

**Timeline**:
- [Date range]: [Old approach] was common
- [Date]: [Change event]
- [Current]: [New approach]

**What to use instead**:
| Task | Tool | Why |
|------|------|-----|
| [Use case] | [Correct tool] | [Reason] |

**LLM mistake**: [Why LLMs suggest old pattern]
**How to detect**: [Validation rule]
```

### Example Shibboleths to Encode

1. **Framework Evolution**
   - React: Class components → Hooks → Server Components
   - Next.js: Pages Router → App Router
   - State management: Redux → Zustand/Jotai/React Query

2. **Model Selection**
   - CLIP limitations (can't count, can't do spatial reasoning)
   - Embedding model specialization (text vs code vs multi-lingual)
   - Model versioning (ada-002 vs text-embedding-3-large)

3. **Tool Architecture**
   - When to use MCP vs Scripts vs Subagents
   - Premature abstraction anti-pattern
   - Self-contained tool benefits

---

## Self-Contained Tools

### Decision Matrix

| Need | Use |
|------|-----|
| External API + auth | MCP Server |
| Multi-step workflow | Subagents |
| Repeatable operation | Scripts |
| Domain validation | Scripts |
| Templates/boilerplate | Assets |
| Deep reference docs | References |

### Scripts

**Requirements**:
1. Actually work (not templates or pseudocode)
2. Minimal dependencies (prefer stdlib)
3. Clear interface (CLI args or stdin/stdout)
4. Error handling (graceful failures)
5. README (how to install and run)

**Example**:
```python
#!/usr/bin/env python3
"""
Domain Analyzer
Usage: python analyze.py <input>
Dependencies: pip install numpy
"""
import sys

def analyze(input_path):
    # Import here for helpful error
    try:
        import numpy as np
    except ImportError:
        print("Install: pip install numpy")
        sys.exit(1)

    # Actual implementation
    result = {"score": 0.85}
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input>")
        sys.exit(1)

    result = analyze(sys.argv[1])
    for k, v in result.items():
        print(f"{k}: {v}")
```

### MCP Servers

**When to build**:
- External API with authentication
- Stateful connections (WebSocket, database)
- Real-time data streams
- Security boundaries (credentials, OAuth)

**Structure**:
```
mcp-server/
├── src/index.ts       # Server implementation
├── package.json       # Dependencies
├── tsconfig.json      # Config
└── README.md          # Setup instructions
```

**Minimal MCP template**: See `/references/mcp-template.md`

### Subagents

**When to define**:
- Multi-step workflows
- Different phases need different tool access
- Orchestration logic is complex

**Definition format**: See `/references/subagent-template.md`

---

## Common Workflows

### Create Skill from Expertise

1. Define scope: What expertise? Keywords? Exclusions?
2. Write description with keywords and NOT clause
3. Encode anti-patterns and shibboleths
4. Add decision trees (not just instructions)
5. Build working tools (scripts/MCP/subagents)
6. Test activation thoroughly

### Debug Activation Issues

**Flowchart**:
```
Skill not activating?
├── Check description has specific keywords
│   ├── NO → Add "Activate on: keyword1, keyword2"
│   └── YES → Query contains those keywords?
│       ├── NO → Add missing variations
│       └── YES → Conflicting NOT clause?
│           ├── YES → Narrow exclusions
│           └── NO → Check file structure
│               └── Wrong location → Move to .claude/skills/

Skill activating when it shouldn't?
├── Missing NOT clause?
│   ├── YES → Add "NOT for: exclusion1, exclusion2"
│   └── NO → NOT clause too narrow
│       └── Expand based on false positives
```

Run: `python scripts/test_activation.py <path>`

### Improve Existing Skill

1. Run `python scripts/validate_skill.py <path>`
2. Run `python scripts/check_self_contained.py <path>`
3. Address ERRORS → WARNINGS → SUGGESTIONS
4. Add missing shibboleths and anti-patterns
5. Ensure &lt;500 lines in SKILL.md
6. Re-validate until clean
7. Update CHANGELOG.md

---

## Tool Permissions

**Guidelines**:
- Read-only: `Read,Grep,Glob`
- File modifier: `Read,Write,Edit`
- Build integration: `Read,Write,Bash(npm:*,git:*)`
- ⚠️ **Never**: Unrestricted `Bash` for untrusted skills

**Principle**: Least privilege - only grant what's needed.

---

## Decision Trees

### When to Create a NEW Skill?

✅ **Create when**:
- Domain expertise not in existing skills
- Pattern repeats across 3+ projects
- Anti-patterns you want to prevent
- Shibboleths to encode

❌ **Don't create when**:
- One-time task → Just do it directly
- Existing skill could be extended → Improve that one
- No real expertise to encode → Not worth it

### Skill vs Subagent vs MCP vs Script?

| Type | Purpose | State | Auth | Example |
|------|---------|-------|------|---------|
| **Skill** | Domain expertise, decision trees | None | None | react-server-components |
| **Script** | Repeatable operations | None | None | validate_skill.py |
| **Subagent** | Multi-step workflows | Session | Inherited | research-coordinator |
| **MCP** | External APIs, auth | Persistent | Required | github-mcp-server |

---

## Anti-Patterns to Avoid

### 1. Skill as Documentation Dump

❌ **Wrong**: 50-page tutorial in SKILL.md
✅ **Right**: Decision trees + anti-patterns in SKILL.md, details in `/references`

### 2. Missing "When NOT to Use"

❌ **Wrong**: `description: "Processes images using computer vision"`
✅ **Right**: `description: "CLIP semantic search. NOT for generation, editing, OCR, counting."`

### 3. Phantom Tools

❌ **Wrong**: SKILL.md references `scripts/analyze.py` that doesn't exist
✅ **Right**: Only reference tools that exist and work

### 4. Template Soup

❌ **Wrong**: Scripts with `# TODO: implement` comments
✅ **Right**: Ship working code or don't ship at all

### 5. No Validation Script

❌ **Wrong**: Instructions with no way to check correctness
✅ **Right**: Include `scripts/validate.py` for pre-flight checks

### 6. Overly Permissive Tools

❌ **Wrong**: `allowed-tools: Bash`
✅ **Right**: `allowed-tools: Bash(git:*,npm:run),Read,Write`

### 7. Ignoring Temporal Knowledge

❌ **Wrong**: "Use useEffect for componentDidMount"
✅ **Right**: "Pre-React 18: useEffect=didMount. React 18+: runs TWICE in dev. Use refs for run-once."

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Correct activation | &gt;90% | Test queries that should trigger |
| False positive rate | &lt;5% | Test queries that shouldn't trigger |
| Token usage | &lt;5k | SKILL.md size + typical reference loads |
| Time to productive | &lt;5 min | User can start working immediately |
| Anti-pattern prevention | &gt;80% | Users avoid documented mistakes |

---

## Validation Checklist

Before packaging a skill:

```
□ SKILL.md exists and is &lt;500 lines
□ Frontmatter has name, description, allowed-tools
□ Description includes specific keywords
□ Description includes NOT clause for exclusions
□ At least 1 anti-pattern documented
□ All referenced scripts/tools actually exist
□ Scripts have clear installation instructions
□ Scripts handle errors gracefully
□ If MCP needed, server is complete and tested
□ If subagents needed, prompts are defined
□ CHANGELOG.md exists with version history
□ Validation scripts pass without errors
```

---

## Reference Files

For deep dives on specific topics:

| File | Contents |
|------|----------|
| `references/antipatterns.md` | Shibboleths and case studies |
| `references/self-contained-tools.md` | Scripts, MCP, subagent patterns |
| `references/validation-checklist.md` | Complete review guide |
| `references/scoring-rubric.md` | Quantitative evaluation (0-10) |
| `references/mcp-template.md` | Minimal MCP server starter |
| `references/subagent-template.md` | Agent definition format |

---

## Real-World Case Studies

### Case Study 1: Photo Expert Explosion

**Problem**: Single skill for ALL photo operations (800+ lines)
**Symptoms**: Activated on "photo" anywhere, wrong advice given
**Root cause**: "Everything Skill" anti-pattern
**Resolution**: Split into 5 focused skills (CLIP, composition, color theory, collage, event detection)
**Lesson**: One domain ≠ one skill. Split by expertise type.

### Case Study 2: The Phantom MCP

**Problem**: SKILL.md referenced non-existent MCP server
**Symptoms**: Users ran commands that didn't exist
**Root cause**: Reference Illusion anti-pattern
**Resolution**: Added `check_self_contained.py` to CI
**Lesson**: Don't promise tools you don't deliver.

### Case Study 3: The Time Bomb

**Problem**: Temporal knowledge became stale (React hooks advice from 2023)
**Symptoms**: Skill became actively harmful in 2024
**Root cause**: Missing temporal markers
**Resolution**: Added "Pre-React 18 vs React 18+" sections
**Lesson**: Date your knowledge. Update quarterly.

---

## This Skill Guides

- ✅ Skill creation from expertise
- ✅ Skill auditing and improvement
- ✅ Anti-pattern detection and prevention
- ✅ Progressive disclosure design
- ✅ Domain expertise encoding (shibboleths)
- ✅ Self-contained tool implementation
- ✅ Activation debugging and optimization
- ✅ Validation and packaging workflows

**Use this skill to create skills that make users immediately productive.**
