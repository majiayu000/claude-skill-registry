---
name: slash-command-encoder
description: Creates ergonomic slash commands (/command) that provide fast, unambiguous access to micro-skills, cascades, and agents. Enhanced with auto-discovery, intelligent routing, parameter validation, and command chaining. Generates comprehensive command catalogs for all installed skills with multi-model integration.
tags: [commands, interface, ergonomics, auto-discovery, composition, tier-3]
version: 2.0.0
---

# Slash Command Encoder (Enhanced)

## Overview
Creates fast, scriptable `/command` interfaces for micro-skills, cascades, and agents. This enhanced version includes automatic skill discovery, intelligent command generation, parameter validation, multi-model routing, and command chaining patterns.

## Philosophy: Expert Efficiency

**Command Line UX for AI**: Expert users benefit from fast, precise, scriptable interfaces over natural language when performing repeated operations.

**Enhanced Capabilities**:
- **Auto-Discovery**: Scans and catalogs all installed skills automatically
- **Intelligent Routing**: Commands invoke optimal AI/agent for task
- **Parameter Validation**: Type-checked, auto-completed parameters
- **Command Chaining**: Compose commands into pipelines
- **Multi-Model Integration**: Direct access to Gemini/Codex via commands

**Key Principles**:
1. Fast and unambiguous invocation
2. Self-documenting through naming
3. Composable and scriptable
4. Type-safe parameter handling
5. Muscle memory for power users

## When to Create Slash Commands

✅ **Perfect For**:
- Operations performed repeatedly (daily/weekly)
- Workflows that need exact parameters
- Tasks requiring scriptable automation
- Commands that compose into pipelines
- Expert user shortcuts

❌ **Don't Use For**:
- One-off exploratory tasks
- Operations needing natural language nuance
- Tasks better suited to interactive dialogue

## Enhanced Creation Workflow

### Step 1: Auto-Discovery Phase

**Scan Installed Skills**:
```bash
# Discovery algorithm
scan_directories:
  - ~/.claude/skills/*/SKILL.md
  - .claude/skills/*/SKILL.md

extract_metadata:
  - name (command base)
  - description (help text)
  - inputs (parameters)
  - outputs (return types)
  - integration_points (routing)
```

**Catalog Generation**:
```yaml
discovered_skills:
  micro_skills: [extract-data, validate-api, refactor-code, ...]
  cascades: [audit-pipeline, code-quality-swarm, ...]
  agents: [root-cause-analyzer, code-reviewer, ...]
  multi_model: [gemini-megacontext, codex-auto, ...]
```

### Step 2: Command Design (Enhanced)

#### A. Naming Conventions

**Category Prefixes**:
```bash
# Data operations
/extract-json, /validate-csv, /transform-xml

# Code operations
/lint-python, /test-coverage, /refactor-imports

# Agent invocation
/agent-rca, /agent-reviewer, /agent-architect

# Multi-model
/gemini-search, /codex-auto, /claude-reason

# Workflows
/audit-pipeline, /deploy-prod, /quality-check
```

**Naming Rules**:
- Verb-noun pattern: `/validate-api`, `/extract-data`
- Agent prefix: `/agent-<specialty>`
- Model prefix: `/gemini-*`, `/codex-*`
- Workflow descriptive: `/audit-pipeline`
- Max 3 words, hyphenated

#### B. Parameter Design

**Parameter Types**:
```yaml
positional:
  - file_path (required, validated)
  - target (required, validated)

flags:
  --strict: boolean
  --format: enum[json, csv, xml]
  --output: file_path

options:
  --config: json_object
  --schema: file_path
  --model: enum[claude, gemini, codex]
```

**Validation Schema**:
```typescript
interface CommandParameter {
  name: string
  type: 'string' | 'number' | 'boolean' | 'file_path' | 'enum'
  required: boolean
  default?: any
  validation?: RegExp | ((value: any) => boolean)
  description: string
  completion?: () => string[]  // Auto-complete options
}
```

#### C. Multi-Model Routing

**Model Selection Flags**:
```bash
# Explicit model selection
/analyze src/ --model gemini-megacontext  # Large context
/prototype feature.spec --model codex-auto  # Rapid prototyping
/reason bug-report.md --model codex-reasoning  # Alternative view
/review code.js --model claude  # Best reasoning (default)

# Auto-select based on task
/analyze-large-codebase  # Auto-routes to gemini-megacontext
/rapid-prototype  # Auto-routes to codex-auto
/search-current-info  # Auto-routes to gemini-search
```

### Step 3: Command Implementation Structure

**Command Definition Template**:
```yaml
command:
  name: /command-name
  version: 1.0.0

  description: |
    Brief description of what this command does

  category: data | code | agent | workflow | multi-model

  parameters:
    - name: input
      type: file_path
      required: true
      validation: file_exists
      description: Input file to process

    - name: --strict
      type: boolean
      default: false
      description: Enable strict validation

    - name: --model
      type: enum
      options: [claude, gemini-megacontext, gemini-search, codex-auto]
      default: auto-select
      description: AI model to use

  routing:
    type: micro-skill | cascade | agent | multi-model
    target: skill-name | cascade-name | agent-name
    model_selection: auto | explicit

  binding:
    parameter_mapping:
      file: ${input}
      strictness: ${--strict}
      model: ${--model}

  output:
    format: json | text | file
    validation: schema | none

  examples:
    - command: /command-name input.json --strict
      description: Process input.json with strict validation

  composition:
    chainable: true
    pipe_output: stdout
    pipe_input: stdin
```

### Step 4: Command Chaining & Composition

**Pipeline Patterns**:
```bash
# Sequential pipeline
/extract data.json | /validate --strict | /transform --format csv > output.csv

# Parallel fan-out
/analyze src/ --parallel [/lint + /security-scan + /test-coverage] | /merge-reports

# Conditional branching
/validate input.json && /deploy-prod || /generate-error-report

# Multi-stage workflow
/audit-pipeline src/ \
  --phase theater-detection \
  --phase functionality-audit --model codex-auto \
  --phase style-audit \
  --output report.json
```

**Composition Interface**:
```typescript
interface ChainableCommand {
  execute: (input: any) => Promise<CommandResult>
  pipe: (next: Command) => ChainableCommand
  parallel: (commands: Command[]) => ParallelCommand
  conditional: (condition: boolean, ifTrue: Command, ifFalse: Command) => ConditionalCommand
}
```

### Step 5: Auto-Completion & Help

**Completion System**:
```bash
# File path completion
/validate <TAB>  # Shows files matching pattern

# Parameter completion
/analyze --<TAB>  # Shows available flags

# Model completion
/analyze --model <TAB>  # Shows [claude, gemini-megacontext, codex-auto, ...]

# Command discovery
/<TAB>  # Shows all available commands by category
```

**Help Generation**:
```markdown
/help command-name

Command: /validate-api
Version: 1.0.0
Category: Data Operations

Description:
  Validates API responses against OpenAPI schemas using specialist validation agent

Usage:
  /validate-api <file> [--schema <schema_file>] [--strict] [--model <model>]

Parameters:
  file              Path to API response file (required)
  --schema FILE     OpenAPI schema file (default: auto-detect)
  --strict          Enable strict validation mode
  --model MODEL     AI model [claude|gemini|codex] (default: auto)

Examples:
  /validate-api response.json
  /validate-api response.json --schema openapi.yaml --strict
  /validate-api response.json --model gemini-megacontext

Chains with:
  /extract-data → /validate-api → /transform-data

See also:
  /validate-csv, /validate-json, /agent-validator
```

## Enhanced Command Templates

### 1. Data Processing Commands

**Template**:
```yaml
command: /process-<datatype>
category: data
routing:
  type: micro-skill
  target: process-<datatype>

parameters:
  - input: file_path (required)
  - --format: enum[json, csv, xml]
  - --schema: file_path
  - --output: file_path
  - --model: enum[claude, gemini, codex]

examples:
  /extract-json data.json --schema schema.json
  /validate-csv data.csv --strict --output report.json
  /transform-xml data.xml --format json
```

**Generated Commands**:
- `/extract-json`, `/extract-csv`, `/extract-xml`
- `/validate-json`, `/validate-csv`, `/validate-api`
- `/transform-json`, `/transform-csv`, `/transform-xml`

### 2. Code Operation Commands

**Template**:
```yaml
command: /code-<operation>
category: code
routing:
  type: micro-skill | cascade
  target: code-<operation>

parameters:
  - path: file_path | directory (required)
  - --language: enum[python, javascript, typescript, ...]
  - --config: file_path
  - --fix: boolean (auto-fix issues)
  - --model: enum[claude, codex-auto]

examples:
  /lint-code src/ --language python --fix
  /test-coverage src/ --output coverage-report.json
  /refactor-imports src/ --model codex-auto
```

**Generated Commands**:
- `/lint-code`, `/lint-python`, `/lint-javascript`
- `/test-coverage`, `/test-suite`, `/test-watch`
- `/refactor-imports`, `/refactor-di`, `/refactor-patterns`
- `/analyze-complexity`, `/analyze-security`, `/analyze-performance`

### 3. Agent Invocation Commands

**Template**:
```yaml
command: /agent-<specialty>
category: agent
routing:
  type: agent
  target: <specialty>-agent
  model_selection: auto

parameters:
  - task: string (required, detailed task description)
  - --context: file_path | directory
  - --depth: enum[shallow, normal, deep]
  - --model: enum[claude, gemini, codex]

examples:
  /agent-rca "Debug intermittent timeout in API" --context src/api/
  /agent-reviewer src/feature.js --depth deep
  /agent-architect "Design user authentication system" --context docs/
```

**Generated Commands**:
- `/agent-rca` → Root Cause Analyzer
- `/agent-reviewer` → Code Reviewer
- `/agent-architect` → System Architect
- `/agent-security` → Security Auditor
- `/agent-performance` → Performance Optimizer

### 4. Multi-Model Commands

**Template**:
```yaml
command: /<model>-<capability>
category: multi-model
routing:
  type: multi-model
  target: <model>-cli
  model: <model>

parameters:
  - task: string (required)
  - --context: file_path | directory
  - --output: file_path

examples:
  /gemini-megacontext "Analyze entire 30K line codebase" --context src/
  /gemini-search "What are React 19 breaking changes?"
  /gemini-media "Generate architecture diagram" --output diagram.png
  /codex-auto "Prototype user auth feature" --context spec.md
  /codex-reasoning "Alternative algorithm for sorting" --context src/sort.js
```

**Generated Commands**:
- `/gemini-megacontext` → 1M token context analysis
- `/gemini-search` → Real-time web information
- `/gemini-media` → Image/video generation
- `/gemini-extensions` → Figma, Stripe, Postman integration
- `/codex-auto` → Full Auto sandboxed prototyping
- `/codex-reasoning` → GPT-5-Codex alternative reasoning
- `/claude-reason` → Best overall reasoning (default)

### 5. Workflow/Cascade Commands

**Template**:
```yaml
command: /<workflow-name>
category: workflow
routing:
  type: cascade
  target: <workflow-name>-cascade

parameters:
  - target: file_path | directory (required)
  - --phase: enum[all, phase1, phase2, phase3]
  - --parallel: boolean (enable parallel execution)
  - --model: enum[auto, claude, gemini, codex]
  - --output: file_path

examples:
  /audit-pipeline src/ --output audit-report.json
  /quality-check src/ --parallel --model auto
  /deploy-prod --phase all --output deployment-log.txt
```

**Generated Commands**:
- `/audit-pipeline` → theater → functionality → style
- `/quality-check` → [lint + security + coverage] → report
- `/deploy-prod` → validate → test → build → deploy
- `/modernize-legacy` → analyze → refactor → test → document

## Integration with Existing Skills

### Command Catalog for Current Skills (14 Total)

**Audit Skills (4 commands)**:
```bash
/theater-detect src/          # Theater detection audit
/functionality-audit src/     # Functionality audit with Codex iteration
/style-audit src/             # Style and quality audit
/audit-pipeline src/          # All 3 phases sequentially
```

**Multi-Model Skills (7 commands)**:
```bash
/gemini-megacontext "task"    # 1M token context
/gemini-search "query"        # Real-time web info
/gemini-media "description"   # Generate images/videos
/gemini-extensions "task"     # Figma, Stripe, etc.
/codex-auto "task"            # Full Auto prototyping
/codex-reasoning "problem"    # GPT-5-Codex alternative view
/multi-model "task"           # Intelligent orchestrator
```

**Root Cause Analysis (1 command)**:
```bash
/agent-rca "problem"          # Root cause analysis agent
```

**Three-Tier Architecture (2 commands)**:
```bash
/create-micro-skill "task"    # Create new micro-skill
/create-cascade "workflow"    # Create new cascade
```

### Command Composition Examples

**Example 1: Complete Quality Pipeline**:
```bash
# Sequential quality checks with multi-model routing
/audit-pipeline src/ \
  --phase theater-detection \
  --phase functionality-audit --model codex-auto \
  --phase style-audit --model claude \
  --output quality-report.json
```

**Example 2: Root Cause + Fix Workflow**:
```bash
# Analyze problem, then auto-fix with Codex
/agent-rca "Intermittent timeout in API" --context src/api/ | \
/codex-auto "Fix identified root cause" --sandbox true
```

**Example 3: Research + Prototype + Test**:
```bash
# Multi-model cascade
/gemini-search "Best practices for React 19" | \
/codex-auto "Prototype React 19 feature using best practices" | \
/functionality-audit --model codex-auto
```

**Example 4: Parallel Quality Checks**:
```bash
# Fan-out to multiple tools
/quality-check src/ --parallel [
  /theater-detect,
  /lint-code,
  /test-coverage,
  /analyze-security
] | /merge-reports --output comprehensive-report.json
```

## Integration with Claude Code Command System

### Command Registration

**Auto-Registration Pattern**:
```bash
# On skill installation, auto-register commands
.claude/skills/*/SKILL.md → parse → generate → .claude/commands/<command>.md

# Command file format
.claude/commands/validate-api.md:
---
name: validate-api
binding: micro-skill:validate-api
---
Validate API responses against OpenAPI schemas.
Usage: /validate-api <file> [--schema <schema>] [--strict]
```

### Command Discovery

**Discovery Mechanism**:
```yaml
on_startup:
  - scan ~/.claude/skills/*/SKILL.md
  - scan .claude/skills/*/SKILL.md
  - parse metadata (name, inputs, category)
  - generate command definitions
  - register with Claude Code CLI
  - build auto-completion index

on_update:
  - watch for skill changes
  - regenerate affected commands
  - update completion index
```

### Parameter Validation

**Validation Pipeline**:
```typescript
interface ValidationPipeline {
  // Type checking
  validateTypes: (params: any) => ValidationResult

  // File existence
  validatePaths: (paths: string[]) => ValidationResult

  // Enum constraints
  validateEnums: (values: any) => ValidationResult

  // Custom validators
  validateCustom: (value: any, validator: Function) => ValidationResult

  // Aggregate results
  aggregate: () => ValidationResult
}

// Before command execution
const result = validate(command, parameters)
if (!result.valid) {
  throw new ValidationError(result.errors)
}
```

## Command Chaining Patterns

### Pattern 1: Sequential Pipeline
```bash
# Data processing pipeline
/extract-json data.json | \
/validate-api --schema openapi.yaml | \
/transform-json --format csv | \
/generate-report --template summary
```

### Pattern 2: Parallel Fan-Out
```bash
# Parallel quality checks
/analyze src/ --parallel [
  /lint-code,
  /security-scan --deep,
  /test-coverage,
  /complexity-analysis
] | /merge-reports --format html
```

### Pattern 3: Conditional Branching
```bash
# Deploy based on quality
/validate-quality src/ && \
  /deploy-prod --environment production || \
  /generate-quality-report --notify team
```

### Pattern 4: Iterative Refinement
```bash
# Refactor until quality threshold met
while [[ $(quality-score) -lt 85 ]]; do
  /refactor-code src/ --model codex-auto
  /test-coverage src/
done
```

### Pattern 5: Multi-Model Cascade
```bash
# Research → Design → Implement → Test
/gemini-search "Best practices for feature X" | \
/agent-architect "Design feature X with best practices" | \
/codex-auto "Implement designed feature" | \
/functionality-audit --model codex-auto | \
/style-audit
```

## Best Practices (Enhanced)

### Command Design
1. ✅ Use clear, consistent naming (verb-noun)
2. ✅ Limit positional parameters (max 2-3)
3. ✅ Provide sensible defaults
4. ✅ Enable command chaining
5. ✅ Include comprehensive help
6. ✅ Support model selection for flexibility

### Parameter Design
1. ✅ Type-safe with validation
2. ✅ Auto-completion enabled
3. ✅ Required vs optional clearly marked
4. ✅ Enum constraints for options
5. ✅ File path validation

### Integration Design
1. ✅ Clean routing to skills/agents
2. ✅ Standardized output formats
3. ✅ Composable interfaces
4. ✅ Error handling with clear messages
5. ✅ Progress reporting for long operations

## Working with Slash Command Encoder

**Invocation**:
"Create slash commands for [skill/cascade/agent] with [parameters] that [composition pattern]"

**The encoder will**:
1. Auto-discover all installed skills
2. Design command naming and parameters
3. Create validation schemas
4. Generate command definitions
5. Register with Claude Code CLI
6. Build auto-completion index
7. Produce comprehensive command catalog

**Advanced Features**:
- Automatic skill discovery and catalog generation
- Intelligent multi-model routing
- Type-safe parameter validation
- Command chaining and composition
- Auto-completion for parameters
- Comprehensive help generation
- Integration with Claude Code CLI

**Integration**:
- Works with **micro-skill-creator** for skill-to-command generation
- Works with **cascade-orchestrator** for workflow commands
- Works with **multi-model system** for AI routing
- Works with **audit-pipeline** for quality commands
- Works with **root-cause-analyzer** for debugging commands

---

**Version 2.0 Enhancements**:
- Auto-discovery of all installed skills
- Multi-model intelligent routing
- Command chaining and composition patterns
- Type-safe parameter validation
- Auto-completion system
- Comprehensive command catalog generation
- Integration with Gemini/Codex CLIs
- Enhanced help and documentation generation
