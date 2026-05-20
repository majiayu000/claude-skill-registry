---
name: claude-md-gen
description: Generate project-specific CLAUDE.md with domain instructions, workflows, templates. Analyzes codebase, asks clarifying questions, produces tailored instructions.
argument-hint: [project-path] [--type cli-tool|web-app|python-cli|research|api-service|library|mixed]
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion, Write
---

# CLAUDE.md Generator Skill

Generate project-specific CLAUDE.md files through codebase analysis, targeted questions, and pattern selection.

## Critical Requirements

- Analyze existing code structure before questions
- Ask focused questions (max 5-7 per session)
- Generate concrete, actionable instructions (no generic filler)
- Include templates for common outputs
- Provide extensibility patterns
- No placeholders/TODOs in generated output
- Self-contained instructions (no references to global ~/.claude/CLAUDE.md)

---

## Workflow Overview

Five-phase generation process:

1. **Project Analysis** - Auto-detect type, extract context
2. **Clarifying Questions** - 5-7 targeted questions based on type
3. **Pattern Selection** - Choose 2-4 relevant reusable patterns
4. **Template Customization** - Generate tailored CLAUDE.md
5. **Verification** - Quality checks before output

---

## Phase 1: Project Analysis

### Auto-Detection Logic

Analyze codebase to determine project type:

```text
DETECTION RULES:

research-knowledge:
  IF content/ OR findings/ exists
  IF PARA folders detected (0_Inbox, 1_Projects, 2_Areas, 3_Resources, 4_Archives)
  IF .md files > 10 in root/subdirs
  → research-knowledge

python-cli:
  IF pyproject.toml exists
  IF click OR typer imports in main file
  IF [tool.poetry] OR [tool.pdm] section
  IF tests/ with pytest
  → python-cli

web-app:
  IF package.json + astro.config.* exists
  IF package.json + src/components/ + public/
  IF package.json + vite.config OR webpack.config
  → web-app

cli-tool:
  IF go.mod + cmd/ + main.go
  IF Cargo.toml + src/main.rs + clap dependency
  IF package.json + #!/usr/bin/env node in files
  → cli-tool

api-service:
  IF go.mod + cmd/ + internal/ + (gin|echo|chi imports)
  IF package.json + express|fastify|nest imports
  IF pyproject.toml + (fastapi|flask) dependency
  → api-service

library:
  IF lib/ exists AND no cmd/ or bin/
  IF package.json + "main" field but no bin/
  IF Cargo.toml with [lib] section
  → library

mixed:
  IF multiple indicators (api + frontend, cli + lib)
  → mixed

FALLBACK:
  IF ambiguous → ask user to select
```text

### Context Collection

Gather for template customization:

**From package files:**

- Languages and versions
- Frameworks and versions
- Dependencies (testing, linting, etc.)
- Scripts/tasks (build, test, lint)

**From directory structure:**

- Primary directories with purposes
- Test organization
- Documentation location
- Configuration files

**From existing files:**

- README.md (project description, setup)
- Existing CLAUDE.md (preserve custom sections)
- Taskfile.yml / Makefile / mise.toml (commands)
- .pre-commit-config.yaml / husky (hooks)
- Linter configs (eslintrc, ruff.toml, golangci.yml)

**Analysis steps:**

1. Read package file(s): `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`
2. Map directory structure: `ls -la` + glob for key directories
3. Identify test framework: grep for imports, check dependencies
4. Find linters/formatters: look for config files
5. Extract commands: read Taskfile/Makefile/package.json scripts
6. Check for existing conventions: read existing CLAUDE.md, pre-commit config

**Store context:**

```text
project_context = {
  "name": from directory or package file,
  "type": detected type,
  "languages": {lang: version},
  "frameworks": {framework: version},
  "testing": framework name,
  "linting": [linter names],
  "dependency_mgmt": tool name,
  "directories": {path: purpose},
  "commands": {task: command},
  "hooks": [hook names],
  "existing_claude_md": sections to preserve
}
```text

---

## Phase 2: Clarifying Questions

Load question framework from `questions/{detected-type}-questions.md`.

Ask 5-7 questions via AskUserQuestion tool based on project type.

**Question categories:**

1. Domain workflows (2-3 questions)
2. Output formats (1-2 questions)
3. Tool integrations (1-2 questions)
4. Quality gates (1 question)
5. Common pitfalls (1 question)

**For mixed projects:** Combine questions from component types (max 7 total).

**Store answers:**

```text
user_answers = {
  "workflows": [workflow descriptions],
  "output_formats": [format descriptions],
  "tools": [tool integrations],
  "quality_gates": [requirements],
  "pitfalls": [common mistakes]
}
```text

---

## Phase 3: Pattern Selection

Based on user answers, select 2-4 relevant patterns from `patterns/`.

### Selection Matrix

| User Need | Pattern File |
|-----------|--------------|
| "Quick filtering before deep work" | triage-workflows.md |
| "Two-tier verification", "double-check", "validate" | cove-verification.md |
| "Hard requirements", "must have", "criteria" | decision-matrices.md |
| "Source attribution", "citations", "references" | citation-systems.md |
| "Structured outputs", "JSON", "templates", "reports" | output-templates.md |
| "Examples", "test cases", "worked examples" | few-shot-examples.md |

### Priority by Project Type

**research-knowledge:**

1. output-templates.md (for note templates)
2. citation-systems.md (for source attribution)
3. triage-workflows.md (for inbox processing)

**python-cli:**

1. cove-verification.md (for TDD workflow)
2. output-templates.md (for structured CLI outputs)
3. few-shot-examples.md (for test fixtures)

**web-app:**

1. output-templates.md (for component templates if design system)
2. decision-matrices.md (for A11y criteria)

**cli-tool:**

1. output-templates.md (for CLI output formats)
2. decision-matrices.md (for input validation)
3. few-shot-examples.md (for command examples)

**api-service:**

1. decision-matrices.md (for endpoint validation)
2. cove-verification.md (for integration tests)
3. citation-systems.md (for API docs)

**library:**

1. few-shot-examples.md (for usage examples)
2. decision-matrices.md (for breaking change criteria)
3. citation-systems.md (for API docs)

**mixed:**

- Select from all types based on components
- Max 4 patterns total
- Prioritize patterns mentioned in answers

### Selection Logic

```python
selected_patterns = []

# Check user answers for keywords
if any(keyword in answers for keyword in ["filter", "quick", "triage", "screening"]):
    selected_patterns.append("triage-workflows.md")

if any(keyword in answers for keyword in ["verify", "double-check", "validate", "two-phase"]):
    selected_patterns.append("cove-verification.md")

if any(keyword in answers for keyword in ["requirements", "criteria", "must-have", "scoring"]):
    selected_patterns.append("decision-matrices.md")

if any(keyword in answers for keyword in ["sources", "citations", "references", "attribution"]):
    selected_patterns.append("citation-systems.md")

if any(keyword in answers for keyword in ["template", "format", "structure", "JSON", "report"]):
    selected_patterns.append("output-templates.md")

if any(keyword in answers for keyword in ["examples", "test cases", "fixtures", "samples"]):
    selected_patterns.append("few-shot-examples.md")

# Apply type-based priorities if < 2 patterns selected
if len(selected_patterns) < 2:
    selected_patterns.extend(type_priorities[project_type])

# Limit to 4 patterns
selected_patterns = selected_patterns[:4]
```text

---

## Phase 4: Template Customization & Generation

### Load Base Template

From `templates/{type}.md`:

- Single type: load one template
- Mixed: merge relevant sections from multiple templates

### Customization Steps

**1. Replace placeholders:**

```text
[Project Name] → project_context["name"]
[Tech Stack] → project_context["languages"] + project_context["frameworks"]
[Directory Structure] → project_context["directories"]
[Commands] → project_context["commands"]
[Linter Name] → project_context["linting"]
[Test Framework] → project_context["testing"]
```text

**2. Add domain-specific sections based on answers:**

```text
IF web-app + design system mentioned:
  Add "Design System" section with breakpoints, components

IF python-cli + shared utils mentioned:
  Add "Shared Utilities" section with location, conventions

IF research + note templates mentioned:
  Add "Note Templates" section with actual templates

IF api-service + auth mentioned:
  Add "Authentication" section with method, middleware
```text

**3. Include selected patterns (2-4 from Phase 3):**

For each pattern file:

- Read pattern from `patterns/{name}.md`
- Adapt examples to project context
- Add as section in generated CLAUDE.md
- Customize placeholders with project specifics

**4. Generate output templates if applicable:**

IF output_templates.md selected OR type requires it:

- Create "Output Templates" section
- Include 1-2 concrete examples with structure
- Use project-specific metadata/fields
- Show markdown formatting with sections

**5. Add quality gate checklist:**

```markdown
## Quality Gates

Before committing:

- [ ] {linter_name} passes
- [ ] {test_framework} tests pass
- [ ] {hook_name} hooks pass (if hooks detected)
- [ ] {additional_gates from user answers}

Commands:
```bash
{actual commands from project_context["commands"]}
```text

```text

**6. Add common commands:**

```markdown
## Common Commands

```bash
# {purpose from package.json script or Taskfile}
{actual command}

# {purpose}
{actual command}
```text

```text

**7. Add anti-patterns:**

Combine:
- Type-default anti-patterns from template
- User-mentioned pitfalls from answers
- Project-specific detected issues

Format:
```markdown
## Anti-Patterns

**AVOID:**

- ❌ {specific pitfall 1}
- ❌ {specific pitfall 2}
- ❌ {specific pitfall 3}

**REASON:** {why each is problematic}
```text

### Template Structure

All generated CLAUDE.md files follow this structure:

```markdown
# {Project Name}

{1-2 sentence description from README or inferred}

## Project Structure

```text

{auto-generated from directory analysis}
src/          - {purpose}
tests/        - {purpose}
docs/         - {purpose}

```text

## Tech Stack

**Language:** {language + version}
**Framework:** {framework + version}
**Testing:** {test framework}
**Linting:** {linters}
**Dependency Mgmt:** {tool}

## Development Workflow

{Type-specific workflows - 2-3 most common tasks}

### {Workflow 1: e.g., "Adding New Feature"}

1. {Concrete step}
2. {Concrete step}
3. {Concrete step}

### {Workflow 2: e.g., "Running Tests"}

1. {Concrete step}
2. {Concrete step}

## {Domain-Specific Section 1}

{Based on project type and user answers}

## {Domain-Specific Section 2}

{Based on project type and user answers}

## Quality Gates

{Generated from customization step 5}

## Common Commands

{Generated from customization step 6}

## Output Templates

{If applicable - generated from customization step 4}

### {Template 1 Name}

```markdown
{Template structure with placeholders}
```text

## Anti-Patterns

{Generated from customization step 7}

## {Included Pattern 1}

{Adapted from patterns/{name}.md}

## {Included Pattern 2}

{Adapted from patterns/{name}.md}

## Extensibility

To add sections as project evolves:

1. Add heading in appropriate location
2. Follow section structure above
3. Keep concrete and actionable
4. Include examples where helpful

See `.claude/skills/claude-md-gen/customization-guide.md` for:

- Adding new project types
- Creating custom patterns
- Updating as requirements change

```text

---

## Phase 5: Verification & Output

### Pre-Generation Checks

**During analysis:**
- [ ] At least 3 files read to understand structure
- [ ] Package file(s) parsed correctly
- [ ] Directory structure mapped
- [ ] Existing conventions identified

**During questions:**
- [ ] Max 7 questions asked
- [ ] Questions relevant to detected type
- [ ] No generic questions
- [ ] Answers captured for customization

**During pattern selection:**
- [ ] 2-4 patterns selected
- [ ] Selection based on user needs
- [ ] Patterns will be adapted (not copy-pasted)

### Post-Generation Verification

Load checklist from `checklist.md` and verify:

**Technical accuracy:**
- [ ] Language versions match package files
- [ ] Framework versions correct
- [ ] Directory paths accurate
- [ ] Commands executable

**Actionability:**
- [ ] Workflows have concrete steps
- [ ] Commands include actual syntax
- [ ] Quality gates list actual tools
- [ ] Output templates show structure

**Specificity:**
- [ ] No "TODO" or "Fill this in"
- [ ] No placeholder text remaining
- [ ] Anti-patterns specific to project
- [ ] Examples use project context

**Extensibility:**
- [ ] Customization guide referenced
- [ ] Clear how to add sections
- [ ] Pattern library location noted

**Completeness:**
- [ ] All major project areas covered
- [ ] Selected patterns included and adapted
- [ ] Quality gates comprehensive
- [ ] Common commands from actual project

### Write CLAUDE.md

**Location decision:**
- Default: `CLAUDE.md` at project root
- If `.claude/` exists: ask user if they want `.claude/CLAUDE.md` instead

**Write file** with fully customized content.

### Show Summary

```markdown
# Generated CLAUDE.md

**Location:** {path}
**Type:** {detected-type or mixed}
**Patterns Included:** {list 2-4 patterns}

## Sections Generated

1. Project Structure (auto-generated from {source})
2. Tech Stack ({languages/frameworks})
3. {Domain Section 1}
4. {Domain Section 2}
5. Quality Gates ({linter names})
6. Common Commands ({X commands from mise/make/npm})
7. Output Templates ({Y templates} or "N/A")
8. Anti-Patterns ({Z specific pitfalls})
9. {Pattern 1 name}
10. {Pattern 2 name}
{11-12 if 3-4 patterns}

## Next Steps

- Review {Section X} for accuracy
- Customize {Section Y} with additional details
- Update anti-patterns as you discover new ones

## Extensibility

Add sections as project evolves. See .claude/skills/claude-md-gen/customization-guide.md for:
- Adding new project type templates
- Creating custom patterns
- Adapting generated output as requirements change
```text

---

## Supporting Files

### File Locations

**Templates:** `.claude/skills/claude-md-gen/templates/{type}.md`

- web-app.md, cli-tool.md, python-cli.md, research-knowledge.md, api-service.md, library.md, mixed.md

**Patterns:** `.claude/skills/claude-md-gen/patterns/{name}.md`

- cove-verification.md, decision-matrices.md, triage-workflows.md, citation-systems.md, output-templates.md, few-shot-examples.md

**Questions:** `.claude/skills/claude-md-gen/questions/{type}-questions.md`

- web-app-questions.md, cli-tool-questions.md, python-cli-questions.md, research-questions.md, api-service-questions.md, library-questions.md, mixed-questions.md

**Support:** `.claude/skills/claude-md-gen/`

- checklist.md, customization-guide.md

---

## Implementation Notes

### Mixed Project Handling

When multiple type indicators detected:

1. Identify all component types (e.g., api-service + web-app)
2. Load relevant sections from each template
3. Merge into cohesive structure:
   - Project Structure: combined view
   - Tech Stack: all languages/frameworks
   - Workflows: primary workflows from each component
   - Domain sections: one per component type
4. Ask questions from multiple frameworks (max 7 total)
5. Select patterns from all component priorities

### Preserving Existing Sections

If existing CLAUDE.md detected:

1. Parse existing file for custom sections
2. Note sections not in standard templates
3. Preserve custom sections in generated output
4. Merge with generated content
5. Note preserved sections in summary

### Command Verification

For quality gates and common commands:

1. Test commands with `--help` or `--version` (non-destructive)
2. Verify exit codes (0 = success)
3. If command fails: mark with "(verify: command not found)" in output
4. User can fix after generation

### Pattern Adaptation

When including patterns:

1. Read pattern file
2. Replace generic placeholders with project specifics:
   - [Project] → actual project name
   - [Command] → actual command from project
   - [OutputType] → actual output format from answers
3. Adapt examples to project domain
4. Keep pattern structure intact
5. Add project-specific customization notes

---

## Error Handling

**If auto-detection fails:**

- Show detected indicators
- Ask user to select type manually via AskUserQuestion
- Proceed with selected type

**If package files missing:**

- Infer from directory structure
- Ask user for key details (language, framework)
- Note gaps in summary

**If commands untestable:**

- Include in output with verification note
- List in "Next Steps" for user to verify

**If no patterns match:**

- Select type-default patterns (minimum 2)
- Note in summary: "Used default patterns for {type}"

**If template file missing:**

- Fall back to generic template structure
- Note in summary: "Generated generic structure"
- Suggest creating custom template

---

## Extension Points

Users can extend skill by:

1. **Adding project types:** Create new template in `templates/`
2. **Adding patterns:** Create new pattern in `patterns/`
3. **Adding question frameworks:** Create new framework in `questions/`
4. **Customizing templates:** Edit existing templates for conventions
5. **Improving detection:** Update auto-detection rules in this file

See `customization-guide.md` for details.

---

## Quality Principles

**Concrete over generic:**

- "Run pytest" not "Run tests"
- "ruff check ." not "Run linter"
- Actual directory names not "source code directory"

**Actionable over descriptive:**

- Step-by-step workflows not "handle this area"
- Specific commands not "use the build tool"
- Concrete examples not "see documentation"

**Self-contained over referential:**

- Complete instructions in CLAUDE.md
- No "see ~/.claude/CLAUDE.md" references
- No "ask your team" placeholders

**Extensible over rigid:**

- Clear how to add sections
- Pattern library for reuse
- Customization guide included

**Project-specific over universal:**

- Use actual project context
- Adapt patterns to domain
- Include project anti-patterns
