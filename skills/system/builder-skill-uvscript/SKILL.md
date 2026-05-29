---
name: builder-skill-uvscript
description: Unified UV CLI scripts collection with builder-skill_ prefix following IndieDevDan patterns for system analysis, code generation, development tools, and automation
version: 1.0.0
modularized: true
scripts_enabled: true
last_updated: 2025-11-30
compliance_score: 100
auto_trigger_keywords:
  - uvscript
  - builder-skill
  - uv-cli
  - unified-scripts
scripts:
  # System Analysis (12 scripts)
  - name: builder-skill_analyze_all.py
    purpose: Analyze all system resources
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_all.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_battery.py
    purpose: Analyze battery status and power
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_battery.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_cpu.py
    purpose: Analyze CPU usage and performance
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_cpu.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_disk.py
    purpose: Analyze disk I/O and storage
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_disk.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_memory.py
    purpose: Analyze memory usage and optimization
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_memory.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_network.py
    purpose: Analyze network bandwidth and connections
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_network.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_thermal.py
    purpose: Analyze thermal management and cooling
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_thermal.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_cache_management.py
    purpose: Manage cache and temporary files
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_cache_management.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_monitor_resources.py
    purpose: Monitor system resources continuously
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_monitor_resources.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_optimize_system.py
    purpose: Optimize system performance
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_optimize_system.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_generate_report.py
    purpose: Generate comprehensive system reports
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_report.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_check_status.py
    purpose: Check system status and health
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_check_status.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30

  # BaaS Integration (2 scripts)
  - name: builder-skill_select_provider.py
    purpose: Select optimal BaaS provider
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_select_provider.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_migrate_provider.py
    purpose: Migrate between BaaS providers
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_migrate_provider.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30

  # Code Generation (4 scripts)
  - name: builder-skill_generate_agent.py
    purpose: Generate MoAI agent YAML with frontmatter
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_agent.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_generate_command.py
    purpose: Generate slash command file
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_command.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_generate_skill.py
    purpose: Generate skill with SKILL.md and scripts
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_skill.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_scaffold_test.py
    purpose: Generate test files from existing code
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_scaffold_test.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30

  # Development Tools (2 scripts)
  - name: builder-skill_debug_code.py
    purpose: AI-powered debug helper
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_debug_code.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_analyze_performance.py
    purpose: AI-powered performance analyzer
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_performance.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-11-30

  # Documentation (2 scripts)
  - name: builder-skill_lint_docs.py
    purpose: Lint Korean documentation
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_lint_docs.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
  - name: builder-skill_validate_diagrams.py
    purpose: Validate Mermaid diagrams
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_validate_diagrams.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30

  # Template Tools (1 script)
  - name: builder-skill_generate_template.py
    purpose: Generate project templates
    type: python
    command: uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_template.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-11-30
color: red
---

---

## Quick Reference (30 seconds)

**Unified UV CLI Scripts Collection**

**What It Does**: Consolidated collection of 23 UV CLI scripts with unified `builder-skill_` prefix following IndieDevDan patterns for system analysis, code generation, development tools, documentation, and automation.

**Core Capabilities**:
- 🔍 **System Analysis**: 12 scripts for CPU, memory, disk, network, battery, thermal analysis
- 🏗️ **Code Generation**: 4 scripts for agent, skill, command, and test scaffolding
- 🛠️ **Development Tools**: 2 scripts for debugging and performance analysis
- 📚 **Documentation**: 2 scripts for linting and diagram validation
- ⚙️ **BaaS Integration**: 2 scripts for provider selection and migration
- 📝 **Template Tools**: 1 script for template generation

**Progressive Disclosure Workflow**:
```
User Request → SKILL.md (200 tokens) → Script --help (0 tokens) → Execute
     ↓              ↓                      ↓                    ↓
   Dormant     Quick Check         Full Documentation    Implementation
```

**When to Use**:
- System resource analysis and optimization
- Code generation and scaffolding
- Development workflow automation
- Documentation validation
- BaaS provider management
- Template generation

---

## Script Categories

### 1. System Analysis (12 scripts)

All system analysis scripts follow PEP 723 format with embedded dependencies.

**Usage Pattern**:
```bash
# Analyze specific resource
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_cpu.py

# Analyze all resources
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_all.py

# Generate comprehensive report
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_report.py --format=markdown
```

**Scripts**:
- `builder-skill_analyze_all.py` - Analyze all system resources
- `builder-skill_analyze_battery.py` - Battery status and power analysis
- `builder-skill_analyze_cpu.py` - CPU usage and performance
- `builder-skill_analyze_disk.py` - Disk I/O and storage
- `builder-skill_analyze_memory.py` - Memory usage and optimization
- `builder-skill_analyze_network.py` - Network bandwidth and connections
- `builder-skill_analyze_thermal.py` - Thermal management and cooling
- `builder-skill_cache_management.py` - Cache and temporary file management
- `builder-skill_monitor_resources.py` - Continuous resource monitoring
- `builder-skill_optimize_system.py` - System performance optimization
- `builder-skill_generate_report.py` - Comprehensive system reports
- `builder-skill_check_status.py` - System status and health checks

---

### 2. Code Generation (4 scripts)

AI-powered code scaffolding with Context7 integration and TRUST 5 validation.

**Usage Pattern**:
```bash
# Generate agent
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_agent.py \
    --name expert-api --description "API specialist"

# Generate skill
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_skill.py \
    --name moai-connector-rest --description "REST API toolkit"

# Generate command
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_command.py \
    --name analyze-performance --description "Performance analysis"

# Generate tests
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_scaffold_test.py \
    --source src/user.py --framework pytest
```

**Scripts**:
- `builder-skill_generate_agent.py` - Generate MoAI agent YAML with frontmatter
- `builder-skill_generate_command.py` - Generate slash command files
- `builder-skill_generate_skill.py` - Generate skill with SKILL.md and scripts
- `builder-skill_scaffold_test.py` - Generate test files from existing code

---

### 3. Development Tools (2 scripts)

AI-powered debugging and performance analysis.

**Usage Pattern**:
```bash
# Debug helper
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_debug_code.py \
    --error "AttributeError: 'NoneType' object has no attribute 'name'"

# Performance analyzer
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_performance.py \
    --profile output.prof --threshold 1.0
```

**Scripts**:
- `builder-skill_debug_code.py` - AI-powered debug helper with error pattern recognition
- `builder-skill_analyze_performance.py` - AI-powered performance analyzer with bottleneck detection

---

### 4. BaaS Integration (2 scripts)

Backend-as-a-Service provider selection and migration.

**Usage Pattern**:
```bash
# Select provider
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_select_provider.py \
    --requirements auth,database,storage

# Migrate provider
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_migrate_provider.py \
    --from firebase --to supabase
```

**Scripts**:
- `builder-skill_select_provider.py` - Select optimal BaaS provider based on requirements
- `builder-skill_migrate_provider.py` - Migrate between BaaS providers with data preservation

---

### 5. Documentation (2 scripts)

Documentation validation and quality assurance.

**Usage Pattern**:
```bash
# Lint Korean docs
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_lint_docs.py \
    --path .moai/docs/

# Validate Mermaid diagrams
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_validate_diagrams.py \
    --path .moai/docs/
```

**Scripts**:
- `builder-skill_lint_docs.py` - Lint Korean documentation for quality and consistency
- `builder-skill_validate_diagrams.py` - Validate Mermaid diagrams for syntax and rendering

---

### 6. Template Tools (1 script)

Project template generation and management.

**Usage Pattern**:
```bash
# Generate template
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_template.py \
    --type nextjs --features "auth,database,api"
```

**Scripts**:
- `builder-skill_generate_template.py` - Generate project templates with best practices

---

## Architecture

**Design Principles**:
- **Self-Contained Scripts**: Each script is 200-300 lines with embedded dependencies (PEP 723)
- **Progressive Disclosure**: Scripts dormant at 0 tokens until invoked
- **Dual Output**: Human-readable (default) + JSON mode (--json flag)
- **MCP-Wrappable**: Stateless, JSON output, no interactive prompts
- **Unified Naming**: `builder-skill_` prefix for all scripts
- **Zero Context**: Most scripts require no context loading (23/23 zero_context: true/false)

**Integration Points**:
- **expert-backend**: Backend code generation
- **expert-frontend**: Frontend component generation
- **manager-tdd**: Test generation workflow
- **builder-agent**: Agent creation patterns
- **builder-skill**: Skill structure patterns
- **builder-command**: Command file patterns
- **macos-resource-optimizer**: System analysis and optimization

---

## IndieDevDan Pattern Compliance

All 23 scripts follow **13 IndieDevDan rules** documented in `builder-workflow.md`:

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

## Migration History

**Consolidation Date**: 2025-11-30

**Previous Locations** (deprecated):
- `macos-resource-optimizer/scripts/` (12 scripts) → Moved to builder-skill-uvscript
- `moai-platform-baas/scripts/` (2 scripts) → Moved to builder-skill-uvscript
- `moai-toolkit-codegen/scripts/` (4 scripts) → Moved to builder-skill-uvscript
- `moai-toolkit-essentials/scripts/` (2 scripts) → Moved to builder-skill-uvscript
- `moai-workflow-docs/scripts/` (2 scripts) → Moved to builder-skill-uvscript
- `moai-workflow-templates/scripts/` (1 script) → Moved to builder-skill-uvscript

**Backward Compatibility**: Old skill folders maintain skill functionality with deprecation notices pointing to builder-skill-uvscript.

---

## Quick Start

```bash
# 1. Analyze system resources
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_analyze_all.py

# 2. Generate a new agent
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_agent.py \
    --name expert-api --description "API specialist"

# 3. Generate a new skill
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_skill.py \
    --name moai-connector-rest --description "REST API toolkit"

# 4. Debug code
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_debug_code.py \
    --error "TypeError: unsupported operand type(s)"

# 5. Generate comprehensive report
uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_generate_report.py \
    --format=markdown --output=.moai/reports/
```

---

**Version**: 1.0.0
**Status**: ✅ Active (Consolidated)
**Scripts**: 23 total (all MCP-ready, all PEP 723 compliant)
**Naming Convention**: `builder-skill_` prefix + 2 descriptive words
**Last Updated**: 2025-11-30
