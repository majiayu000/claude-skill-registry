---
name: Create New Skills
description: Creates new Agent Skills for Claude Code following best practices and documentation. Use when the user wants to create a new skill, extend Claude's capabilities, or package domain expertise into a reusable skill.
---

# Create New Skills

## Instructions

This skill helps you create new Agent Skills for Claude Code. Before starting, read the comprehensive documentation files in the [docs/](docs/) directory for complete context.

### Prerequisites

**Required Reading** - Read these files in order before creating a skill:
1. [docs/claude_code_agent_skills.md](docs/claude_code_agent_skills.md) - Complete guide to creating and managing skills
2. [docs/claude_code_agent_skills_overview.md](docs/claude_code_agent_skills_overview.md) - Architecture and how skills work
3. [docs/blog_equipping_agents_with_skills.md](docs/blog_equipping_agents_with_skills.md) - Design principles and best practices

### Understanding Skills

**What is a Skill?**
- A directory containing a `SKILL.md` file with YAML frontmatter
- Instructions that Claude loads on-demand when relevant
- Optional supporting files (scripts, documentation, templates)
- Like an onboarding guide for a new team member

**Progressive Disclosure (3 Levels):**
1. **Metadata** (always loaded): `name` and `description` in YAML frontmatter
2. **Instructions** (loaded when triggered): Main body of SKILL.md
3. **Resources** (loaded as needed): Additional files, scripts, templates

**Key Principle:** Only relevant content enters the context window at any time.

### Skill Creation Workflow

#### Step 1: Define the Skill's Purpose

Ask the user these questions:
1. What task or domain should this skill cover?
2. When should Claude use this skill? (triggers)
3. What expertise or workflows need to be captured?
4. Does it need scripts, templates, or other resources?

Document the answers for reference.

#### Step 2: Create the Skill Directory Structure

Create skills in the project's `.claude/skills/` directory for team sharing:

```bash
mkdir -p .claude/skills/<skill-name>
```

**Naming conventions:**
- Use lowercase with hyphens (e.g., `pdf-processing`, `data-analysis`)
- Be descriptive but concise
- Avoid generic names

**Note:** Project skills (`.claude/skills/`) are automatically shared with your team via git. For personal skills only you use, create in `~/.claude/skills/` instead.

#### Step 3: Design the SKILL.md Structure

Every skill must have:
```yaml
---
name: Your Skill Name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude]

## Examples
[Concrete examples of using this Skill]
```

**Frontmatter Requirements:**
- `name`: Required, max 64 characters
- `description`: Required, max 1024 characters
  - Include BOTH what it does AND when to use it
  - Mention key trigger words/phrases
  - Be specific, not vague

**Optional Frontmatter (Claude Code only):**
- `allowed-tools`: Restrict which tools Claude can use (e.g., `Read, Grep, Glob`)

#### Step 4: Write the Instructions Section

**Structure the instructions as:**
1. **Prerequisites** - Required dependencies, tools, environment setup
2. **Workflow** - Step-by-step process (numbered steps)
3. **Supporting Details** - Additional context, script usage, error handling

**Best Practices:**
- Use clear, actionable language
- Number sequential steps
- Use bullet points for options/lists
- Include code blocks with bash commands
- Reference supporting files with relative links: `[reference.md](reference.md)`
- Keep focused on one capability

**Example workflow format:**
```markdown
### Workflow

1. **First step description**:
   ```bash
   command to run
   ```
   - Additional context
   - Options or variations

2. **Second step description**:
   - Detailed instructions
   - What to look for
   - Expected outcomes

3. **Third step**...
```

#### Step 5: Write the Examples Section

Provide 2-4 concrete examples showing:
- Different use cases
- Various input formats
- Step-by-step execution
- Expected outcomes

**Example format:**
```markdown
### Example 1: Descriptive Title

User request:
```
User's exact request text
```

You would:
1. First action
2. Second action with command:
   ```bash
   actual command
   ```
3. Next steps...
4. Final result
```

#### Step 6: Add Supporting Files (Optional)

If the skill needs additional context:
1. Create files alongside SKILL.md
2. Reference them from instructions: `[forms.md](forms.md)`
3. Use progressive disclosure - split by topic/scenario

**Common supporting file types:**
- Additional instructions (e.g., `advanced_usage.md`)
- Reference documentation (e.g., `api_reference.md`)
- Scripts in `scripts/` directory
- Templates in `templates/` directory
- Configuration examples

**Script guidelines:**
- Make executable: `chmod +x scripts/*.py`
- Add PEP 723 inline dependencies for Python scripts
- Include usage instructions in SKILL.md
- Return clear output for Claude to parse

#### Step 7: Test the Skill

1. Verify file structure:
   ```bash
   ls -la .claude/skills/<skill-name>/
   ```

2. Check YAML frontmatter is valid:
   ```bash
   head -10 .claude/skills/<skill-name>/SKILL.md
   ```

3. Test with relevant queries:
   - Ask questions matching the skill's description
   - Verify Claude loads and uses the skill
   - Check that instructions are clear and actionable

4. Iterate based on testing:
   - Refine description if skill doesn't trigger
   - Clarify instructions if Claude struggles
   - Add examples for common edge cases

#### Step 8: Commit to Version Control

Since project skills are automatically shared with your team, commit them to git:

```bash
git add .claude/skills/<skill-name>
git commit -m "Add <skill-name> skill"
git push
```

**Note:** Team members will get the skill automatically when they pull the latest changes.

### Best Practices Summary

**Description writing:**
- ✅ "Transcribes audio/video files to text using Fireworks API. Use when user asks to transcribe, convert speech to text, or needs transcripts."
- ❌ "Helps with audio"

**Instruction organization:**
- Keep main instructions focused (under 5k tokens ideal)
- Split complex content into linked files
- Use progressive disclosure for optional/advanced content

**Skill scope:**
- One skill = one capability or workflow
- Don't combine unrelated tasks
- Make focused, composable skills

**File references:**
- Use relative paths: `[file.md](file.md)` not absolute paths
- Reference scripts with full path from skill root
- Make it clear when Claude should read vs execute files

### Common Patterns from Existing Skills

**Pattern 1: Transcription skill**
- Prerequisites section with environment setup
- Clear numbered workflow
- Multiple examples showing different formats
- Supporting file for corrections/mappings

**Pattern 2: Morning debrief skill**
- Two-step process (transcribe, extend)
- Reference to detailed prompt in separate file
- File organization step
- Clear output structure specification

**Pattern 3: Meta-skill (this one)**
- Extensive prereading documentation
- Step-by-step creation workflow
- Multiple examples with variations
- Best practices and common patterns

## Examples

### Example 1: Creating a Simple Code Review Skill

User request:
```
Create a skill that reviews Python code for best practices
```

You would:
1. Read the documentation files in [docs/](docs/)
2. Ask clarifying questions:
   - What specific best practices? (PEP 8, security, performance?)
   - Should it check only or suggest fixes?
   - Any specific frameworks or libraries?
3. Create the skill directory:
   ```bash
   mkdir -p .claude/skills/python-code-review
   ```
4. Write SKILL.md with:
   ```yaml
   ---
   name: Python Code Review
   description: Reviews Python code for PEP 8 compliance, security issues, and performance. Use when reviewing Python code, checking code quality, or analyzing Python files.
   allowed-tools: Read, Grep, Glob
   ---
   ```
5. Add Instructions section with:
   - Prerequisites (none needed, uses built-in tools)
   - Workflow:
     1. Read the Python file(s)
     2. Check PEP 8 compliance
     3. Identify security issues
     4. Suggest performance improvements
     5. Provide summary with specific line references
6. Add 3 examples:
   - Example 1: Single file review
   - Example 2: Multi-file project review
   - Example 3: Focused security review
7. Test with sample Python files

### Example 2: Creating a Data Analysis Skill with Scripts

User request:
```
Build a skill for analyzing CSV data with statistics and visualizations
```

You would:
1. Read documentation files
2. Define scope with user:
   - What statistics? (mean, median, correlations?)
   - What visualizations? (charts, plots?)
   - Output format? (markdown report, images?)
3. Create structure:
   ```bash
   mkdir -p .claude/skills/csv-analysis/scripts
   mkdir -p .claude/skills/csv-analysis/templates
   ```
4. Write SKILL.md referencing:
   - `scripts/analyze.py` - Statistical analysis script
   - `scripts/visualize.py` - Chart generation script
   - `templates/report_template.md` - Output template
5. Create Python scripts with inline dependencies:
   ```python
   # /// script
   # requires-python = ">=3.10"
   # dependencies = ["pandas", "matplotlib", "seaborn"]
   # ///
   ```
6. Write clear instructions for:
   - When to run which script
   - How to interpret output
   - How to customize analysis
7. Add examples showing:
   - Basic statistics
   - Visualization generation
   - Custom report creation
8. Test with sample CSV files

### Example 3: Creating a Multi-File Documentation Skill

User request:
```
Create a skill for writing technical documentation with our company's style guide
```

You would:
1. Read documentation files
2. Gather requirements:
   - Get company style guide document
   - What types of docs? (API, user guides, architecture?)
   - Any templates or examples?
3. Create comprehensive structure:
   ```bash
   mkdir -p .claude/skills/tech-docs/{templates,examples,guidelines}
   ```
4. Organize content:
   - `SKILL.md` - Overview and workflow
   - `guidelines/style_guide.md` - Company style rules
   - `guidelines/api_docs.md` - API documentation specifics
   - `guidelines/user_guides.md` - User guide standards
   - `templates/api_template.md` - API doc template
   - `templates/guide_template.md` - User guide template
   - `examples/` - Sample documentation
5. Write SKILL.md that:
   - References guidelines by doc type
   - Uses progressive disclosure (only load needed guidelines)
   - Provides workflow for each doc type
6. Add examples for:
   - API endpoint documentation
   - User guide creation
   - Architecture decision records
7. Test with various documentation requests

### Example 4: Extending an Existing Skill

User request:
```
Add spell correction to our transcribe skill
```

You would:
1. Read current skill:
   ```bash
   cat .claude/skills/transcribe/SKILL.md
   ```
2. Identify where to add the feature:
   - After transcription step
   - Before final output
3. Create supporting file:
   ```bash
   touch .claude/skills/transcribe/spell_corrections.md
   ```
4. Write correction mappings in new file:
   ```markdown
   # Spell Corrections
   - "cloud code" → "claude code"
   - "API" → "API" (ensure caps)
   ...
   ```
5. Update SKILL.md workflow:
   - Add step: "Apply spell corrections from [spell_corrections.md](spell_corrections.md)"
   - Reference the corrections file
6. Update examples to show correction step
7. Test with audio that has common errors

## Summary

Creating skills is about packaging expertise into discoverable, composable capabilities. Follow these principles:

1. **Read the docs first** - Understand progressive disclosure and skill architecture
2. **Write clear descriptions** - Include what AND when
3. **Keep instructions focused** - Use supporting files for additional context
4. **Test thoroughly** - Verify Claude discovers and uses the skill correctly
5. **Iterate with feedback** - Refine based on actual usage

Skills transform general-purpose Claude into a specialist for your domain. Start small, test early, and expand as needed.
