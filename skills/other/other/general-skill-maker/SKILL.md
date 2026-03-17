---
name: general-skill-maker
description: Create effective agent skills through guided briefing process. Use when user wants to: (1) create a new skill, (2) make a skill, (3) build a skill, (4) set up a skill, (5) initialize a skill, (6) design a skill, (7) update or modify existing skill, (8) plan skill architecture, or (9) learn about skill structure. Trigger on phrases like "create skill", "new skill", "make skill", "skill for X", "build skill", "design skill", or "help me create skill".
---

# General Skill Maker

Create effective agent skills through guided briefing process that explores requirements, patterns, and best practices.

## Workflow

6-step process: Brief → Load References → Plan Structure → Generate → Apply Best Practices → Present

### Step 1: Briefing Questions

Ask user questions **ONE AT A TIME** (not all at once). Adapt based on answers.

**Complete question library:** See [references/briefing-questions.md](references/briefing-questions.md)

**Core Questions (REQUIRED):**
1. **Skill Purpose** - "Jaki jest główny cel tego skilla?"
2. **Usage Examples** - "Podaj 2-3 przykłady jak użytkownik będzie prosił o użycie tego skilla?"
3. **Environment/Platform** - "Gdzie będzie używany ten skill?"
4. **Freedom Level** - "Jak deterministyczny ma być proces?"
5. **Expected Output** - "Jaki jest oczekiwany output?"

**Optional Questions (ask based on context):**
6. Task Scope - Single vs related tasks
7. User Base - Solo vs team
8. Scripts Needed - For repetitive operations
9. Reference Documentation - API docs, schemas, examples
10. Assets/Templates - Templates, boilerplate code
11. External Integrations - APIs, databases, tools
12. Workflow Type - Multi-step vs single-step
13. User Interaction - Interactive vs autonomous
14. Quality Standards - Validation requirements

**Briefing strategy:**
- Start with core questions (1-5)
- Ask optional questions (6-14) only when relevant based on previous answers
- Adapt and skip irrelevant questions
- See references/briefing-questions.md for detailed questions, follow-ups, and examples

### Step 2: Load Appropriate References

Based on user's answers, read relevant reference files:

**Always read:**
- `references/best-practices.md` - Universal principles for all skills

**Read based on workflow type:**
- `references/workflow-patterns.md` - If multi-step workflow with sequential logic
- `references/integration-patterns.md` - If external API/tool integrations
- `references/tool-based-patterns.md` - If specific tools/scripts dominate
- `references/domain-knowledge-patterns.md` - If primarily about conveying expertise

**Load only what's needed** - Don't read all references unnecessarily.

### Step 3: Plan Structure

Based on briefing answers, determine skill structure:

**Required:**
- `SKILL.md` - Always required

**Optional folders to create:**
- `scripts/` - If Q6 answered yes (executable code)
- `references/` - If Q7 answered yes (detailed documentation)
- `assets/` - If Q8 answered yes (templates, files for output)

**Plan SKILL.md sections:**

**Frontmatter (always):**
```yaml
---
name: skill-name
description: Comprehensive description with WHEN to use
---
```

**Body sections (adapt based on needs):**
- Overview/Introduction
- Quick Start (if complex)
- Step-by-step instructions (if multi-step)
- Examples (always recommended)
- Edge cases (if complex)
- References to supporting files (if using scripts/references/assets)
- Quality checks (if validation needed)

**Important considerations:**
- Keep SKILL.md under 500 lines
- Move detailed content to references/
- Structure over prose
- Include concrete examples
- Clear section headings

### Step 4: Generate Skill

Create the actual skill files based on plan.

#### A. Create Directory Structure

```bash
mkdir -p skill-name/{scripts,references,assets}
```

Only create folders that are needed (from Step 3 plan).

#### B. Write SKILL.md

**Frontmatter Guidelines:**

```yaml
---
name: skill-name  # hyphen-case, max 64 chars, no leading/trailing hyphens
description: >
  [What it does]. [When to use it]. Use when [triggers].
  Trigger on phrases like "[example1]", "[example2]", "[example3]".
---
```

**Description best practices:**
- Include WHAT it does (capabilities)
- Include WHEN to use (contexts, triggers)
- Include specific KEYWORDS users naturally say
- Use 1-1024 characters wisely
- Think semantic matching - agent uses language understanding

**Body structure:**

Use imperative/infinitive form (e.g., "Run tests", not "Running tests" or "The agent should run tests").

```markdown
# Skill Name

[One-line description]

## Quick Start (optional for complex skills)

[Minimal example to get started fast]

## Core Workflow

[Step-by-step instructions]

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

[Concrete examples with input → output]

## Supporting Resources (if applicable)

- **scripts/script.py** - [What it does]
- **references/details.md** - [What it contains, when to load]
- **assets/template.html** - [What it is, how to use]

## Quality Checks (if applicable)

[Validation steps, success criteria]
```

**Writing guidelines:**
- ✅ Structured (headers, lists, steps)
- ✅ Concrete examples
- ✅ Only add what LLM doesn't already know
- ✅ Imperative form
- ❌ Prose/walls of text
- ❌ Generic explanations LLM knows
- ❌ Unnecessary details

#### C. Create Scripts (if needed)

For each script identified in briefing:

```python
#!/usr/bin/env python3
"""
Script description.

Usage:
    script.py [args]
"""

# Implement with:
# - Clear error messages
# - Input validation
# - Graceful error handling
# - Self-contained or document dependencies
```

**Test scripts:**
- Run scripts to verify they work
- Test with edge cases
- Ensure error messages are helpful

#### D. Create References (if needed)

For each reference file identified:

```markdown
# Reference Title

[Focused documentation loaded on-demand]

## Section 1

[Content]

## Section 2

[Content]
```

**Reference guidelines:**
- Keep focused (one topic per file)
- Use table of contents for 100+ lines
- Link from SKILL.md with clear "when to read" guidance
- Split domain-specific content (e.g., finance.md, sales.md)

#### E. Create Assets (if needed)

Copy or create template files:
- Document templates
- Boilerplate code
- Images/diagrams
- Config examples

**Asset guidelines:**
- Not loaded into context
- Used in agent's output
- Document in SKILL.md how to use them

### Step 5: Apply Best Practices

Review generated skill against quality criteria.

**Quick checklist:**

1. **Description** - Keywords, triggers, when to use? ✓
2. **Length** - SKILL.md under 500 lines? ✓
3. **Structure** - Headers, steps, lists, examples? ✓
4. **Content** - Specific, actionable, no LLM basics? ✓
5. **Progressive Disclosure** - Details in references/? ✓
6. **Supporting Files** - Scripts tested, references organized? ✓

**Comprehensive quality validation:**

See [references/quality-checklist.md](references/quality-checklist.md) for:
- Complete 25-point quality checklist
- Critical/High Quality/Excellence criteria
- Scoring system and validation commands
- Common quality issues and fixes

**If any check fails:** Revise before presenting to user.

### Step 6: Present and Iterate

1. Show generated skill structure to user
2. Display SKILL.md content
3. Explain key sections and design decisions
4. Show any scripts/references/assets created
5. Ask: "Czy chcesz jakieś zmiany lub doprecyzowania?"
6. Iterate based on feedback
7. Save all files to skill directory

## Validation

Before finalizing, verify:

- [ ] Name is hyphen-case, max 64 chars, no leading/trailing hyphens
- [ ] Description is 1-1024 chars, includes what/when/triggers
- [ ] SKILL.md under 500 lines
- [ ] Structured format (headers, lists, examples)
- [ ] Scripts tested (if any)
- [ ] References organized (if any)
- [ ] No hardcoded absolute paths
- [ ] User confirms it matches their needs

## Tips for Success

1. **Start simple, iterate** - Begin with minimal viable skill, add based on real usage
2. **User-specific language** - If user speaks Polish, use Polish in generated skill content
3. **Progressive disclosure** - Keep SKILL.md lean, details in references/
4. **Concrete over abstract** - Examples > explanations
5. **Test and refine** - Encourage user to test and report issues

**See complete workflow example:**
[references/complete-example.md](references/complete-example.md) shows end-to-end process from briefing to final PDF processing skill.

## Common Mistakes to Avoid

**Quick list (see references/common-mistakes.md for detailed guide):**

- **Too generic description** - "Helps with PDFs" → "Extracts text from PDFs, fills forms, merges documents"
- **Too long SKILL.md** - 2000+ lines → Split into references/
- **Missing examples** - Abstract descriptions → Concrete input/output examples
- **Hardcoded paths** - `/Users/john/...` → Relative paths or ${baseDir}
- **Wall of text** - Prose → Structured format (headers, lists, steps)
- **Unnecessary scripts** - Don't create scripts agent can easily write
- **Everything in one file** - Monolithic SKILL.md → Progressive disclosure

**See references/common-mistakes.md for:**
- Complete anti-patterns guide (Encyclopedia, Everything Bagel, Secret Handshake, etc.)
- Before/after refactoring examples
- Prevention checklist

## Advanced Features (Optional)

For advanced features like hooks, subagent context, allowed-tools, and model override:

**See [references/advanced-features.md](references/advanced-features.md)**

Features include:
- **Hooks** - Lifecycle automation (PreToolUse, PostToolUse validation)
- **Subagent Context** - Isolated execution with specific tools
- **Allowed Tools** - Pre-approve tools to skip permission prompts
- **Dynamic Context** - Inject fresh external data before execution
- **Model Override** - Use haiku/opus for specific skills

**Note:** Most skills don't need advanced features. Use only when they solve specific problems.
