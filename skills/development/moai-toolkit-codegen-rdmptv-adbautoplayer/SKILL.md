---
name: moai-toolkit-codegen
description: AI-powered code generation toolkit (UV scripts migrated to builder-skill-uvscript)
version: 1.0.0
modularized: true
scripts_enabled: false
scripts_migration:
  date: 2025-11-30
  new_location: builder-skill-uvscript
  reason: UV script consolidation with unified builder-skill_ prefix
last_updated: 2025-11-30
compliance_score: 85
auto_trigger_keywords:
  - codegen
  - scaffold
  - generate
  - template
  - agent generation
  - skill generation
# scripts: # DEPRECATED - All 4 UV scripts migrated to builder-skill-uvscript on 2025-11-30
color: red
---

> **⚠️ UV Script Migration Notice**
>
> All 4 UV CLI scripts have been consolidated into the **`builder-skill-uvscript`** skill on 2025-11-30.
>
> **New script locations**:
> - `builder-skill_generate_agent.py` (previously generate_agent.py)
> - `builder-skill_generate_skill.py` (previously generate_skill.py)
> - `builder-skill_generate_command.py` (previously generate_command.py)
> - `builder-skill_scaffold_test.py` (previously scaffold_test.py)
> - Find all scripts in: `.claude/skills/builder-skill-uvscript/scripts/`
>
> **Usage**: `uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_agent.py`
>
> This skill retains its code generation knowledge and patterns.

---

## Quick Reference (30 seconds)

**AI-Powered Code Generation Toolkit**

**What It Does**: Enterprise-grade code scaffolding system that generates MoAI agents, skills, commands, and tests with Context7 latest patterns, TRUST 5 validation, and IndieDevDan UV CLI script standards.

**Core Capabilities**:
- 🏗️ **Agent Generation**: Create agent YAML files with proper frontmatter
- 📦 **Skill Generation**: Generate complete skill structure (SKILL.md + scripts/)
- ⚡ **Command Generation**: Create slash command files with workflow definitions
- 🧪 **Test Scaffolding**: Generate pytest/vitest test files from source code

**Progressive Disclosure Workflow**:
```
User Request → SKILL.md (200 tokens) → Script --help (0 tokens) → Execute
     ↓              ↓                      ↓                    ↓
   Dormant     Quick Check         Full Documentation    Implementation
```

**When to Use**:
- Generating new MoAI agents following official patterns
- Creating skills with IndieDevDan UV script structure
- Scaffolding slash commands with proper frontmatter
- Auto-generating test files from existing code
- Rapid prototyping with MoAI standards compliance

---

## Available Scripts

This skill includes 4 UV CLI scripts following IndieDevDan pattern (PEP 723, dual output, 200-300 lines each).

### 1. generate_agent.py (350 lines)

**Purpose**: Generate MoAI agent YAML files with complete frontmatter following official agent standards.

**Usage**:
```bash
# Generate agent with name and description
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_agent.py \
    --name expert-api \
    --description "API design and implementation specialist"

# Generate with custom tools
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_agent.py \
    --name manager-workflow \
    --description "Workflow orchestration manager" \
    --tools "Read,Write,Edit,Bash" \
    --model sonnet

# JSON output mode
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_agent.py \
    --name expert-database \
    --description "Database design specialist" \
    --json
```

**Features**:
- YAML frontmatter generation (name, description, tools, model, color, permissions)
- Context7 integration for latest agent patterns
- Orchestration metadata (can_resume, parallel_safe)
- Coordination metadata (spawns_subagents, delegates_to)
- Mission statement templates
- Workflow section templates
- Report format examples

**Exit Codes**: 0 (success), 1 (warning), 2 (error), 3 (critical)

---

### 2. generate_skill.py (380 lines)

**Purpose**: Generate complete skill structure with SKILL.md + scripts/ directory following IndieDevDan patterns.

**Usage**:
```bash
# Generate basic skill
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_skill.py \
    --name moai-connector-api \
    --description "REST API client generation toolkit"

# Generate with script templates
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_skill.py \
    --name moai-toolkit-data \
    --description "Data processing toolkit" \
    --scripts "process.py,transform.py,validate.py"

# Full generation with keywords
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_skill.py \
    --name moai-library-testing \
    --description "Testing utilities" \
    --keywords "test,testing,pytest,vitest" \
    --json
```

**Features**:
- SKILL.md with YAML frontmatter
- scripts/ directory creation
- Script metadata generation (name, purpose, command)
- auto_trigger_keywords setup
- Progressive disclosure documentation
- "When to use" section generation
- Available Scripts list with usage examples

**Exit Codes**: 0 (success), 1 (warning), 2 (error), 3 (critical)

---

### 3. generate_command.py (280 lines)

**Purpose**: Generate slash command .md files with proper frontmatter and workflow definitions.

**Usage**:
```bash
# Generate basic command
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_command.py \
    --name analyze-code \
    --description "Analyze code quality and complexity"

# Generate with allowed tools
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_command.py \
    --name deploy-app \
    --description "Deploy application to production" \
    --tools "Bash,Read,Write"

# Generate with arguments
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_command.py \
    --name review-pr \
    --description "Review pull request" \
    --args "pr-number" \
    --json
```

**Features**:
- Markdown frontmatter generation (description, allowed-tools)
- Argument parsing setup
- Workflow section templates
- Report format templates
- Example usage documentation
- Variable substitution placeholders

**Exit Codes**: 0 (success), 1 (warning), 2 (error), 3 (critical)

---

### 4. scaffold_test.py (320 lines)

**Purpose**: Auto-generate test files (pytest/vitest) from existing source code with comprehensive test coverage.

**Usage**:
```bash
# Generate pytest tests
uv run .claude/skills/moai-toolkit-codegen/scripts/scaffold_test.py \
    --source src/user_service.py \
    --framework pytest

# Generate vitest tests
uv run .claude/skills/moai-toolkit-codegen/scripts/scaffold_test.py \
    --source src/components/Button.tsx \
    --framework vitest

# Generate with custom output path
uv run .claude/skills/moai-toolkit-codegen/scripts/scaffold_test.py \
    --source src/api/client.py \
    --output tests/api/test_client.py \
    --framework pytest \
    --json
```

**Features**:
- Pytest test generation (Python)
- Vitest test generation (TypeScript/JavaScript)
- Function/method detection
- Test case templates (success, failure, edge cases)
- Mock/fixture generation
- Assertion templates
- Coverage target calculation

**Exit Codes**: 0 (success), 1 (warning), 2 (error), 3 (critical)

---

## Architecture

**Design Principles**:
- **Self-Contained Scripts**: Each script is 200-300 lines with embedded dependencies (PEP 723)
- **Progressive Disclosure**: Scripts dormant at 0 tokens until invoked
- **Dual Output**: Human-readable (default) + JSON mode (--json flag)
- **MCP-Wrappable**: Stateless, JSON output, no interactive prompts
- **Context7 Integration**: Latest patterns from official MoAI documentation
- **TRUST 5 Compliance**: All generated code follows MoAI quality standards

**Integration Points**:
- **expert-backend**: Backend code generation
- **expert-frontend**: Frontend component generation
- **manager-tdd**: Test generation workflow
- **builder-agent**: Agent creation patterns
- **builder-skill**: Skill structure patterns
- **builder-command**: Command file patterns

---

## IndieDevDan Pattern Compliance

All 4 scripts follow **13 IndieDevDan rules** documented in `builder-workflow.md`:

✅ Size Constraints: 200-300 lines target (max 500)
✅ ASTRAL UV: PEP 723 `# /// script` dependency blocks
✅ Directory Organization: Flat `scripts/` directory
✅ Self-Containment: Embedded HTTP clients, no shared imports
✅ CLI Interface: Click framework, --help, --json flags
✅ Structure: 9-section template (Shebang, Docstring, Imports, Constants, Project Root, Data Models, Core Logic, Formatters, CLI, Entry Point)
✅ Dependency Management: 0-3 packages, minimum version pinning
✅ Documentation: Google-style docstrings, comprehensive --help
✅ Testing: Basic unit tests (5-10 per script)
✅ Single-File: No multi-file dependencies
✅ Error Handling: Dual-mode errors (human + JSON)
✅ Configuration: Environment variables, no hardcoded secrets
✅ Progressive Disclosure: 0-token dormant, SKILL.md listing

---

## Quick Start

```bash
# 1. Generate a new agent
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_agent.py \
    --name expert-api --description "API specialist"

# 2. Generate a new skill
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_skill.py \
    --name moai-connector-rest --description "REST API toolkit"

# 3. Generate a slash command
uv run .claude/skills/moai-toolkit-codegen/scripts/generate_command.py \
    --name analyze-performance --description "Performance analysis"

# 4. Generate tests for existing code
uv run .claude/skills/moai-toolkit-codegen/scripts/scaffold_test.py \
    --source src/user.py --framework pytest
```

---

**Version**: 1.0.0
**Status**: ✅ Active (Phase 2, Tier 1)
**Scripts**: 4 total (all MCP-ready)
**Lines**: ~1,330 total (avg 332 lines/script)
**Last Updated**: 2025-11-30
