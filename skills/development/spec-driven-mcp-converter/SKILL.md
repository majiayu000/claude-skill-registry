---
name: spec-driven-mcp-converter
description: >
  Convert any MCP (Model Context Protocol) server into a standalone CLI utility and
  auto-generate companion skill documentation through an 8-phase workflow with structural
  anti-skip enforcement. Prevents token optimization bias through per-phase reference
  loading, checkpoint persistence, Execute-Verify-Record enforcement, and artifact
  verification. Use when you have an MCP server (Puppeteer, filesystem, weather, database,
  etc.) and need to: (1) Create a standalone CLI wrapper that Claude Code can execute,
  (2) Auto-generate a skill so Claude understands how to use the CLI,
  (3) Bridge MCP async patterns into sync CLI patterns, or
  (4) Rapidly prototype tool integration without MCP server overhead.
  Always use this skill when the user runs /convert-mcp. Make sure to use this skill
  whenever the user mentions converting MCP servers, bridging MCP to CLI, wrapping MCP
  tools as commands, or generating CLI utilities from MCP definitions — even if they
  don't explicitly say "convert-mcp".
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(npm:*)
  - Bash(python:*)
  - Bash(pip:*)
  - Bash(pytest:*)
  - WebFetch
model: claude-opus-4-6
effort: High
---

# Spec-Driven MCP Converter

Convert any MCP server into a locally-executable CLI utility with auto-generated skill documentation. This hybrid framework handles 80% of MCP patterns automatically while allowing custom extensions for outliers.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for user to say "go"
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already wrote the file"
- [ ] Skipping artifact verification via Glob() after a Write()

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 3 independent anti-skip layers. ALL THREE must fail for a step to be skipped:

1. **Per-phase fresh reference loading** - Each phase loads its reference files fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
3. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, output files verified on disk after every Write.

**Note:** Binary CLI gate enforcement (Layer 4) deferred to future story — requires extending `STORY_ID_PATTERN` in phase_state.py to accept `CONVERT-` prefix.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase has three parts:
- **EXECUTE:** The exact action to perform (Read, Write, AskUserQuestion, Task, Glob, Grep, Bash)
- **VERIFY:** How to confirm the action happened (file exists, data key populated, user response non-empty, exit code 0)
- **RECORD:** Update checkpoint JSON with captured data; verify write via Glob

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Three Conversion Patterns

The skill handles 3 MCP conversion patterns, detected automatically or specified via `--pattern`:

| Pattern | Use Case | Detection | Frequency |
|---------|----------|-----------|-----------|
| **API Wrapper** | Stateless APIs, data providers | No state keywords, independent tools | ~70% of MCPs |
| **State-Based** | Browser automation, databases, file systems | Session/connection/state keywords | ~20% of MCPs |
| **Custom** | Hybrid/advanced, complex orchestration | Low confidence or user override | ~10% of MCPs |

---

## When to Use This Skill

### Trigger Scenarios

- User runs `/convert-mcp <mcp-name-or-path>` command
- Manual invocation: `Skill(command="spec-driven-mcp-converter")`
- DevForgeAI needs to convert an MCP server to a CLI tool
- User mentions converting, wrapping, or bridging MCP servers to CLI

### When NOT to Use

- General CLI development without MCP source (use spec-driven-dev)
- Creating skills from scratch without MCP (use devforgeai-subagent-creation)
- MCP server development (this converts existing MCPs, doesn't create new ones)

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$MCP_SOURCE` | `/convert-mcp` argument — MCP name, path, or package spec | **required** |
| `$PATTERN_OVERRIDE` | `--pattern` flag | null (auto-detect) |
| `$SOURCE_TYPE` | `--source` flag (npm:pkg, ./local, ./schema.json) | Inferred from `$MCP_SOURCE` |
| `$ADAPTER_SCRIPT` | `--adapter-script` flag (for custom pattern) | null |
| `$OUTPUT_DIR` | `--output-dir` flag | `./<mcp-name>-cli` |

---

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$MCP_SOURCE` | /convert-mcp | MCP identifier (name, path, or npm spec) |
| `$PATTERN_OVERRIDE` | /convert-mcp | Force pattern: api-wrapper, state-based, custom |
| `$SOURCE_TYPE` | /convert-mcp | Source type: npm package, local dir, JSON schema |
| `$ADAPTER_SCRIPT` | /convert-mcp | Path to custom adapter script (custom pattern only) |
| `$OUTPUT_DIR` | /convert-mcp | Output directory for generated CLI + skill |

---

## Phase 00: Initialization [INLINE — Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Load Parameter Extraction Reference

```
EXECUTE: Read(file_path=".claude/skills/spec-driven-mcp-converter/references/parameter-extraction.md")
VERIFY: File content loaded (non-empty)
RECORD: N/A
```

### Step 0.2: Parse Arguments

```
IF conversation contains MCP name/path after /convert-mcp:
  MCP_SOURCE = extracted value
ELSE:
  HALT: AskUserQuestion "Which MCP server do you want to convert? Provide a name, local path, or npm package spec."

IF conversation contains --pattern:
  PATTERN_OVERRIDE = extracted value (api-wrapper | state-based | custom)
ELSE:
  PATTERN_OVERRIDE = null

IF conversation contains --source:
  SOURCE_TYPE = extracted value
ELSE:
  IF MCP_SOURCE starts with "npm:" → SOURCE_TYPE = "npm_package"
  ELIF MCP_SOURCE ends with ".json" → SOURCE_TYPE = "json_schema"
  ELIF MCP_SOURCE is a directory path → SOURCE_TYPE = "local_directory"
  ELSE → SOURCE_TYPE = "local_directory" (default)

IF conversation contains --adapter-script:
  ADAPTER_SCRIPT = extracted value
ELSE:
  ADAPTER_SCRIPT = null

IF conversation contains --output-dir:
  OUTPUT_DIR = extracted value
ELSE:
  OUTPUT_DIR = "./" + MCP_SOURCE name + "-cli"
```

### Step 0.3: Generate Conversion ID

```
CONVERT_ID = "CONVERT-" + current timestamp (YYYYMMDD-HHMMSS)
Example: CONVERT-20260319-143000
```

### Step 0.4: Validate MCP Source Exists

```
IF SOURCE_TYPE == "local_directory":
  EXECUTE: Glob(pattern="${MCP_SOURCE}/**/*")
  VERIFY: At least 1 file found
  IF no files: HALT "MCP source directory not found or empty: ${MCP_SOURCE}"

IF SOURCE_TYPE == "json_schema":
  EXECUTE: Read(file_path="${MCP_SOURCE}")
  VERIFY: File content is valid JSON
  IF invalid: HALT "MCP schema file not found or invalid JSON: ${MCP_SOURCE}"

IF SOURCE_TYPE == "npm_package":
  VERIFY: MCP_SOURCE matches pattern "npm:<package>@<version>" or "<package>"
  IF invalid format: HALT "Invalid npm package spec: ${MCP_SOURCE}"
```

### Step 0.5: Create Checkpoint File

```json
{
  "checkpoint_version": "1.0",
  "convert_id": "${CONVERT_ID}",
  "mcp_source": "${MCP_SOURCE}",
  "source_type": "${SOURCE_TYPE}",
  "pattern_override": "${PATTERN_OVERRIDE}",
  "adapter_script": "${ADAPTER_SCRIPT}",
  "output_dir": "${OUTPUT_DIR}",
  "created_at": "ISO 8601 timestamp",
  "progress": {
    "current_phase": 1,
    "phases_completed": [0],
    "phases_skipped": [],
    "total_phases": 8
  },
  "phases": {
    "00": {"status": "completed"},
    "01": {"status": "pending"},
    "02": {"status": "pending"},
    "03": {"status": "pending"},
    "04": {"status": "pending"},
    "05": {"status": "pending"},
    "06": {"status": "pending"},
    "07": {"status": "pending"}
  }
}
```

```
EXECUTE: Write(file_path="devforgeai/workflows/${CONVERT_ID}-convert-checkpoint.json", content=checkpoint)
VERIFY: Glob(pattern="devforgeai/workflows/${CONVERT_ID}-convert-checkpoint.json") returns exactly 1 file
```

### Step 0.6: Display Initialization

```
Display:
  "═══ MCP Conversion Workflow Initialized ═══"
  "ID: ${CONVERT_ID}"
  "Source: ${MCP_SOURCE} (${SOURCE_TYPE})"
  "Pattern: ${PATTERN_OVERRIDE || 'auto-detect'}"
  "Output: ${OUTPUT_DIR}"
  "Phases: 8"
```

**GOTO Phase Orchestration Loop at Phase 01.**

---

## Phase Orchestration Loop

For each phase from CURRENT_PHASE to 07:

1. **LOAD REFERENCES:** Each phase specifies which references to load. Load them ALL via Read(). Do NOT skip or summarize.

2. **EXECUTE STEPS:** Follow EVERY step's EXECUTE-VERIFY-RECORD triplet. Execute them IN ORDER. Do NOT compress or skip steps.

3. **EXIT CRITERIA:** Verify ALL mandatory exit conditions before proceeding.

4. **UPDATE CHECKPOINT:** Update `phases[phase_id].status = "completed"`, add to `phases_completed`, advance `current_phase`.

5. **VERIFY CHECKPOINT:** `Read(file_path="devforgeai/workflows/${CONVERT_ID}-convert-checkpoint.json")` — Confirm the update persisted.

6. **DISPLAY TRANSITION:** Show phase completion and next phase name.

---

## Phase Table

| Phase | Name | Conditional | Subagents |
|-------|------|-------------|-----------|
| 00 | Initialization | No | — |
| 01 | MCP Source Discovery & Loading | No | **code-analyzer** (BLOCKING) |
| 02 | Pattern Detection & Analysis | No | — |
| 03 | CLI Wrapper Generation | No | **backend-architect** (CONDITIONAL: custom only) |
| 04 | Skill Documentation Generation | No | **code-reviewer** (BLOCKING) |
| 05 | Validation & Testing | No | **integration-tester** (BLOCKING), **test-automator** (CONDITIONAL) |
| 06 | DevForgeAI Registration | No | — |
| 07 | Result Reporting & Cleanup | No | — |

---

## Phase 01: MCP Source Discovery & Loading

**PURPOSE:** Load and parse the MCP server source. Produce a normalized MCP definition.

**REFERENCE TO LOAD:** `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/source-loading.md")`

### Step 1.1: Constitutional Context Check

```
EXECUTE: Read(file_path="devforgeai/specs/context/source-tree.md")
EXECUTE: Read(file_path="devforgeai/specs/context/tech-stack.md")
VERIFY: Both files loaded successfully (non-empty content)
RECORD: Update checkpoint phases.01.context_loaded = true
```

### Step 1.2: Determine Source Type

```
EXECUTE: Evaluate $SOURCE_TYPE from Phase 00
  - "local_directory": Read files from local path
  - "json_schema": Parse JSON schema for tool definitions
  - "npm_package": Use Bash(npm:*) to inspect package
VERIFY: Source type identified and valid
RECORD: Update checkpoint phases.01.source_type = $SOURCE_TYPE
```

### Step 1.3: Extract Tool Definitions

```
EXECUTE: Invoke code-analyzer subagent (BLOCKING)
  Task: "Analyze MCP server at ${MCP_SOURCE}. Extract all tool definitions including:
         - Tool name
         - Input parameters (name, type, required)
         - Output type
         - Whether tool is async
         - Side effects (state changes)
         - Description
         Return as structured JSON array."
VERIFY: Task result contains 'tools' array with >= 1 tool
RECORD: Update checkpoint phases.01.tool_count = len(tools)

IF tool_count == 0:
  HALT: "No tools found in MCP source. Verify the source path and format."
```

### Step 1.4: Validate Tool Structure

```
EXECUTE: For each tool in extracted tools:
  - Verify 'name' field exists and is non-empty string
  - Verify 'inputs' field exists (can be empty dict for no-arg tools)
  - Normalize field names to consistent schema
VERIFY: All tools pass validation
RECORD: N/A (validation is pass/fail)
```

### Step 1.5: Write Normalized MCP Definition

```
EXECUTE: Write(file_path="tmp/${CONVERT_ID}/mcp_definition.json", content=normalized_tools_json)
VERIFY: Glob(pattern="tmp/${CONVERT_ID}/mcp_definition.json") returns 1 file
RECORD: Update checkpoint phases.01.tools_extracted = true
```

### Phase 01 Exit

```
Update checkpoint:
  phases.01.status = "completed"
  progress.phases_completed += [1]
  progress.current_phase = 2
Verify checkpoint write via Read()
Display: "Phase 01 Complete: ${tool_count} tools extracted from ${MCP_SOURCE}"
```

---

## Phase 02: Pattern Detection & Analysis

**PURPOSE:** Analyze extracted MCP tools to detect the conversion pattern and produce the full analysis report.

**REFERENCE TO LOAD:** `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/pattern-detection.md")`

### Step 2.1: Load MCP Definition

```
EXECUTE: Read(file_path="tmp/${CONVERT_ID}/mcp_definition.json")
VERIFY: Content is valid JSON with tools array
RECORD: N/A
```

### Step 2.2: Run Pattern Detection Heuristics

```
EXECUTE: For each tool, scan for state indicators:
  - State keywords in tool names: session, connect, navigate, click, page,
    transaction, browser, open, close, destroy, create, cursor, subscribe
  - State keywords in parameter names: session_id, connection_id, context
  - Side effects annotations: browser_state, db_state, file_state
  - Sequential dependencies between tools
  - Async operation markers

  Scoring:
    state_keyword_count = count of state indicators across all tools
    IF state_keyword_count == 0 → detected_pattern = "api-wrapper"
    IF state_keyword_count >= 3 → detected_pattern = "state-based"
    IF 1 <= state_keyword_count < 3 → detected_pattern = "state-based" (with lower confidence)

  IF $PATTERN_OVERRIDE is not null:
    detected_pattern = $PATTERN_OVERRIDE
    confidence = 1.0 (user override)

VERIFY: detected_pattern is one of: "api-wrapper", "state-based", "custom"
RECORD: Update checkpoint phases.02.detected_pattern, phases.02.confidence
```

### Step 2.3: Compute Confidence Score

```
EXECUTE: Calculate confidence (0.0 - 1.0):
  - Base confidence from keyword analysis
  - Boost for consistent tool patterns (all stateless or all stateful)
  - Reduce for mixed signals (some stateful, some stateless)
  - Boost for recognized MCP types (puppeteer, postgres, weather known patterns)
VERIFY: Score is a number between 0.0 and 1.0
RECORD: Update checkpoint phases.02.confidence_score
```

### Step 2.4: Generate State Management Analysis

```
EXECUTE: Build state management profile:
  {
    "stateful": boolean,
    "session_required": boolean,
    "concurrent_sessions": boolean,
    "state_keywords_found": [list],
    "session_model": "ephemeral" | "persistent" | "none"
  }
VERIFY: Analysis object populated
RECORD: N/A
```

### Step 2.5: Build Conversion Recommendations

```
EXECUTE: Generate 3-5 actionable recommendations based on pattern and analysis:
  For api-wrapper: "Use direct 1:1 command mapping", "Add --format flag for output control", etc.
  For state-based: "Use ephemeral session model", "Queue operations within session", etc.
  For custom: "Provide custom adapter script", "Review adapter_api.md for interface", etc.
VERIFY: Non-empty list of recommendations
RECORD: N/A
```

### Step 2.6: Confidence Gate

```
EXECUTE: IF confidence < 0.7 AND $PATTERN_OVERRIDE is null:
  AskUserQuestion:
    Question: "Pattern detection confidence is ${confidence}. Which pattern best fits your MCP?"
    Options:
      - "api-wrapper" — Stateless API calls, independent commands
      - "state-based" — Stateful operations requiring session management
      - "custom" — Complex/hybrid patterns requiring custom adapter code
VERIFY: User response received OR $PATTERN_OVERRIDE was already set
RECORD: Update checkpoint phases.02.user_override_reason (if user chose)
```

### Step 2.7: Write Analysis Report

```
EXECUTE: Write(file_path="tmp/${CONVERT_ID}/mcp_analysis.json", content={
  "mcp_type": $MCP_SOURCE name,
  "detected_pattern": detected_pattern,
  "confidence": confidence,
  "tools": tools_array,
  "state_management": state_analysis,
  "conversion_recommendations": recommendations
})
VERIFY: Glob(pattern="tmp/${CONVERT_ID}/mcp_analysis.json") returns 1 file
RECORD: Update checkpoint phases.02.analysis_written = true
```

### Phase 02 Exit

```
Update checkpoint:
  phases.02.status = "completed"
  progress.phases_completed += [2]
  progress.current_phase = 3
Verify checkpoint write via Read()
Display: "Phase 02 Complete: Pattern=${detected_pattern}, Confidence=${confidence}"
```

---

## Phase 03: CLI Wrapper Generation

**PURPOSE:** Generate the standalone CLI wrapper code from the analysis, including directory structure, entry point, adapter, utilities, and test stubs.

**REFERENCES TO LOAD:**
- `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/adapter-api.md")`
- `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/cli-generation-templates.md")`
- `Read(file_path="devforgeai/specs/context/tech-stack.md")`

### Step 3.1: Create Output Directory Structure

```
EXECUTE: Create directories via Write operations:
  - ${OUTPUT_DIR}/
  - ${OUTPUT_DIR}/adapters/
  - ${OUTPUT_DIR}/utils/
  - ${OUTPUT_DIR}/tests/
VERIFY: Glob(pattern="${OUTPUT_DIR}/**/") shows adapters/, utils/, tests/
RECORD: Update checkpoint phases.03.structure_created = true
```

### Step 3.2: Generate CLI Entry Point

```
EXECUTE: Write main CLI script (cli.py) with:
  - argparse with subparsers for each detected tool
  - Tool name → CLI command mapping (snake_case → kebab-case)
  - --format flag (json | text | base64) on each subparser
  - --session flag (for state-based pattern) on tool subparsers
  - Session management subcommands (create, destroy, list) for state-based
  - Error handling with standard Unix exit codes (0-6)
  - Output formatting via utils/output_formatter.py
VERIFY: Glob(pattern="${OUTPUT_DIR}/cli.py") exists
VERIFY: Grep(pattern="argparse", path="${OUTPUT_DIR}/cli.py") confirms CLI framework
RECORD: Update checkpoint phases.03.cli_entry_point = "${OUTPUT_DIR}/cli.py"
```

### Step 3.3: Generate Pattern-Specific Adapter

```
IF detected_pattern == "api-wrapper":
  EXECUTE: Write ${OUTPUT_DIR}/adapters/api_wrapper_adapter.py
    - Extends BaseAdapter
    - Implements execute() for stateless tool calls
    - Implements _call_tool() for each MCP tool

IF detected_pattern == "state-based":
  EXECUTE: Write ${OUTPUT_DIR}/adapters/state_based_adapter.py
    - Extends BaseAdapter
    - Session lifecycle (create, destroy, list, get)
    - Session timeout management (default 1 hour)
    - _call_tool_in_session() for each MCP tool
    - State persistence between calls

IF detected_pattern == "custom":
  EXECUTE: Write ${OUTPUT_DIR}/adapters/custom_adapter.py
    - Template with execute() and format_output() methods
    - Placeholder implementations with NotImplementedError
    - IF $ADAPTER_SCRIPT provided: Integrate user's adapter code

VERIFY: Glob(pattern="${OUTPUT_DIR}/adapters/*_adapter.py") returns >= 1 file
RECORD: Update checkpoint phases.03.adapter_type = detected_pattern

IF detected_pattern == "custom":
  EXECUTE: Invoke backend-architect subagent (CONDITIONAL)
    Task: "Review custom adapter template at ${OUTPUT_DIR}/adapters/custom_adapter.py.
           Verify it follows the BaseAdapter interface from adapter-api.md.
           Check error handling and return format compliance."
  VERIFY: Task result confirms adapter is structurally sound
  RECORD: Update checkpoint phases.03.adapter_reviewed = true
```

### Step 3.4: Generate Utility Modules

```
EXECUTE: Write ${OUTPUT_DIR}/utils/error_handler.py
  - Standard exit codes: 0=success, 1=general, 2=invalid args, 3=timeout,
    4=resource unavailable, 5=auth failed, 6=rate limited
  - Human-readable error messages on stderr
  - Recovery hints per error type

EXECUTE: Write ${OUTPUT_DIR}/utils/output_formatter.py
  - JSON formatting (default, structured output)
  - Text formatting (human-readable, single values)
  - Base64 formatting (binary data: images, files)

VERIFY: Glob(pattern="${OUTPUT_DIR}/utils/*.py") returns >= 2 files
RECORD: N/A
```

### Step 3.5: Generate Dependencies and Documentation

```
EXECUTE: Write ${OUTPUT_DIR}/requirements.txt (Python dependencies)
EXECUTE: Write ${OUTPUT_DIR}/README.md (usage instructions, pattern info, examples)
VERIFY: Glob() confirms both files exist
RECORD: N/A
```

### Step 3.6: Generate Test Stubs

```
EXECUTE: Write ${OUTPUT_DIR}/tests/test_cli.py with:
  - Test for CLI --help (exit code 0)
  - Test for each command with mock inputs
  - Test for error handling (invalid args → exit code 2)
  - For state-based: test session lifecycle
  - For api-wrapper: test direct command execution
VERIFY: Glob(pattern="${OUTPUT_DIR}/tests/test_*.py") returns >= 1 file
RECORD: N/A
```

### Step 3.7: Verify File Count

```
EXECUTE: Count all files in ${OUTPUT_DIR}/ via Glob
VERIFY: Minimum 7 files present (cli.py, adapter, 2 utils, requirements.txt, README.md, test)
RECORD: Update checkpoint phases.03.files_generated = [file list]
RECORD: Update checkpoint phases.03.cli_generation_complete = true
```

### Phase 03 Exit

```
Update checkpoint:
  phases.03.status = "completed"
  progress.phases_completed += [3]
  progress.current_phase = 4
Verify checkpoint write via Read()
Display: "Phase 03 Complete: ${file_count} files generated in ${OUTPUT_DIR}"
```

---

## Phase 04: Skill Documentation Generation

**PURPOSE:** Auto-generate the companion skill (SKILL.md, references, assets) so Claude Code understands how to use the generated CLI.

**REFERENCE TO LOAD:** `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/skill-generation-rules.md")`

### Step 4.1: Generate YAML Frontmatter

```
EXECUTE: Build frontmatter:
  name: <mcp-name>-cli
  description: (max 1024 chars)
    - Third-person voice
    - Enumerate 3-5 use cases: "(1) ..., (2) ..., (3) ..."
    - Pattern-specific guidance:
      api-wrapper: "Each command is independent - no session needed."
      state-based: "Requires session management - create session before running commands."
      custom: "See documentation for usage patterns."
VERIFY: name matches CLI directory name, description < 1024 chars
RECORD: N/A
```

### Step 4.2: Generate SKILL.md Body

```
EXECUTE: Generate body using pattern-specific template:
  For api-wrapper:
    - ## Direct Usage (each command independent)
    - ## Available Commands (1:1 mapping)
    - ## Output Format (JSON default)
    - ## Error Handling (exit codes)

  For state-based:
    - ## Session Management (create → use → destroy)
    - ## Session Commands (create, destroy, list)
    - ## Available Commands (all require --session)
    - ## Session Lifecycle (timeout, cleanup)
    - ## Output Formats (json, text, base64)

  For custom:
    - ## Usage Overview
    - ## Commands
    - ## Special Features
    - ## Notes

  Use imperative language throughout (NOT "you should" — use "Create a session")
VERIFY: Pattern-specific sections present in generated content
RECORD: N/A
```

### Step 4.3: Write Skill Files

```
EXECUTE: Write ${OUTPUT_DIR}/skill/SKILL.md (frontmatter + body)
VERIFY: Glob(pattern="${OUTPUT_DIR}/skill/SKILL.md") exists
VERIFY: Grep(pattern="^---", path="${OUTPUT_DIR}/skill/SKILL.md") finds >= 2 YAML delimiters

EXECUTE: Write ${OUTPUT_DIR}/skill/references/cli_reference.md
  - One section per tool with: syntax, parameters, return value, error conditions
VERIFY: Glob() confirms file exists
VERIFY: Grep(pattern="## ", path="${OUTPUT_DIR}/skill/references/cli_reference.md") confirms sections

EXECUTE: Write ${OUTPUT_DIR}/skill/references/usage_examples.md
  - Pattern-specific workflow examples with real commands
VERIFY: Glob() confirms file exists

EXECUTE: Write ${OUTPUT_DIR}/skill/scripts/setup.sh
  - Installation script (pip install, permissions, etc.)
VERIFY: Glob() confirms file exists

EXECUTE: Write ${OUTPUT_DIR}/skill/assets/error_codes.md
  - Exit codes 0-6 with descriptions and recovery strategies
VERIFY: Glob() confirms file exists
```

### Step 4.4: Skill Quality Validation

```
EXECUTE: Invoke code-reviewer subagent (BLOCKING)
  Task: "Review the generated skill at ${OUTPUT_DIR}/skill/SKILL.md.
         Check: (1) YAML frontmatter valid, (2) Imperative language - no 'you should/can/need',
         (3) No content duplication between SKILL.md and references,
         (4) Progressive disclosure - details in references not SKILL.md,
         (5) All CLI commands listed, (6) Pattern-specific sections present.
         Return quality score (0-100) and list of issues."
VERIFY: Task result — no CRITICAL/HIGH issues found
RECORD: Update checkpoint phases.04.skill_quality_score = score
RECORD: Update checkpoint phases.04.skill_generation_complete = true
```

### Phase 04 Exit

```
Update checkpoint:
  phases.04.status = "completed"
  progress.phases_completed += [4]
  progress.current_phase = 5
Verify checkpoint write via Read()
Display: "Phase 04 Complete: Skill generated (quality score: ${score}/100)"
```

---

## Phase 05: Validation & Testing

**PURPOSE:** Validate the generated CLI executes correctly and the generated skill matches the CLI interface.

**REFERENCE TO LOAD:** `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/validation-workflow.md")`

### Step 5.1: CLI Entry Point Validation

```
EXECUTE: Bash(command="python ${OUTPUT_DIR}/cli.py --help 2>&1")
VERIFY: Exit code 0, output contains subparser/command help text
RECORD: Update checkpoint phases.05.cli_help_ok = true

IF exit code != 0:
  Read the error output. Fix import or syntax issues. Retry once.
  IF still failing after fix: HALT "CLI entry point validation failed"
```

### Step 5.2: Pattern-Specific Smoke Test

```
IF detected_pattern == "api-wrapper":
  EXECUTE: Test one command with mock/sample data
  VERIFY: Command executes without import errors (exit code 0 or 1 acceptable for mock)

IF detected_pattern == "state-based":
  EXECUTE: Test session lifecycle:
    Bash("python ${OUTPUT_DIR}/cli.py session create --name test-session 2>&1")
    Bash("python ${OUTPUT_DIR}/cli.py session list 2>&1")
    Bash("python ${OUTPUT_DIR}/cli.py session destroy --session <id> 2>&1")
  VERIFY: Session create returns ID, list shows session, destroy completes

IF detected_pattern == "custom":
  EXECUTE: Test CLI help for custom commands
  VERIFY: Help displays available commands

RECORD: Update checkpoint phases.05.smoke_test_passed = true/false
```

### Step 5.3: Skill-to-CLI Interface Alignment

```
EXECUTE: Extract command names from ${OUTPUT_DIR}/skill/SKILL.md via Grep
EXECUTE: Extract subparser names from ${OUTPUT_DIR}/cli.py via Grep
EXECUTE: Compare the two lists — every command in skill must exist in CLI
VERIFY: All commands aligned (no missing commands)
RECORD: Update checkpoint phases.05.interface_aligned = true
```

### Step 5.4: Integration Validation

```
EXECUTE: Invoke integration-tester subagent (BLOCKING)
  Task: "Validate alignment between CLI at ${OUTPUT_DIR}/cli.py and
         skill at ${OUTPUT_DIR}/skill/SKILL.md.
         Check: (1) Every command documented in skill exists as CLI subparser,
         (2) Parameter names match between skill docs and CLI argparse,
         (3) Output format documentation matches actual CLI output format,
         (4) Error codes documented in skill match CLI error handling.
         Return alignment score and discrepancies."
VERIFY: Task result indicates alignment (score >= 80%)
RECORD: Update checkpoint phases.05.integration_validation = result
```

### Step 5.5: Run Test Suite

```
EXECUTE: Bash(command="pytest ${OUTPUT_DIR}/tests/ -v 2>&1") or equivalent
VERIFY: Exit code 0, or expected failures for stub tests
RECORD: Update checkpoint phases.05.tests_executed = true
RECORD: Update checkpoint phases.05.test_results = summary

IF test failures indicate real issues (not stubs):
  Invoke test-automator subagent (CONDITIONAL) to enhance/fix test stubs
```

### Step 5.6: Write Validation Report

```
EXECUTE: Write(file_path="tmp/${CONVERT_ID}/validation-report.json", content={
  "cli_help_ok": boolean,
  "smoke_test_passed": boolean,
  "interface_aligned": boolean,
  "integration_score": number,
  "tests_executed": boolean,
  "test_results": summary,
  "overall_status": "PASS" | "FAIL" | "PARTIAL"
})
VERIFY: Glob() confirms file exists
RECORD: Update checkpoint phases.05.validation_complete = true
```

### Phase 05 Exit

```
Update checkpoint:
  phases.05.status = "completed"
  progress.phases_completed += [5]
  progress.current_phase = 6
Verify checkpoint write via Read()
Display: "Phase 05 Complete: Validation ${overall_status}"
```

---

## Phase 06: DevForgeAI Registration

**PURPOSE:** Register the generated CLI and skill into the DevForgeAI framework for future use.

**REFERENCE TO LOAD:** `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/devforgeai-integration.md")`

### Step 6.1: Registration Decision

```
EXECUTE: AskUserQuestion
  Question: "Register generated skill to .claude/skills/<cli-name>/? This makes the CLI available in future conversations."
  Options:
    - "Yes, register now" — Copy skill to framework directory
    - "No, keep in output directory only" — Skill stays in ${OUTPUT_DIR}/skill/
VERIFY: User response received
RECORD: Update checkpoint phases.06.registration_decision = response
```

### Step 6.2: Copy Skill Files (if approved)

```
IF user approved registration:
  EXECUTE: Write skill files to .claude/skills/<cli-name>/:
    - SKILL.md
    - references/cli_reference.md
    - references/usage_examples.md
    - scripts/setup.sh
    - assets/error_codes.md
  VERIFY: Glob(pattern=".claude/skills/<cli-name>/SKILL.md") exists
  RECORD: Update checkpoint phases.06.registered = true
  RECORD: Update checkpoint phases.06.skill_path = ".claude/skills/<cli-name>/"
ELSE:
  RECORD: Update checkpoint phases.06.registered = false
```

### Step 6.3: Dependency Installation (optional)

```
EXECUTE: AskUserQuestion
  Question: "Install CLI dependencies now? (pip install -r ${OUTPUT_DIR}/requirements.txt)"
  Options:
    - "Yes, install now"
    - "No, I'll install later"
VERIFY: User response received

IF user chose "Yes":
  EXECUTE: Bash(command="pip install -r ${OUTPUT_DIR}/requirements.txt 2>&1")
  VERIFY: Exit code 0
  RECORD: Update checkpoint phases.06.dependencies_installed = true
ELSE:
  RECORD: Update checkpoint phases.06.dependencies_installed = false
```

### Phase 06 Exit

```
Update checkpoint:
  phases.06.status = "completed"
  progress.phases_completed += [6]
  progress.current_phase = 7
Verify checkpoint write via Read()
Display: "Phase 06 Complete: Registration=${registered}, Dependencies=${installed}"
```

---

## Phase 07: Result Reporting & Cleanup

**PURPOSE:** Generate the final conversion report, display results, and clean up temporary files.

**REFERENCE TO LOAD:** `Read(file_path=".claude/skills/spec-driven-mcp-converter/references/result-formatting.md")`

### Step 7.1: Verify All Phases Complete

```
EXECUTE: Read(file_path="devforgeai/workflows/${CONVERT_ID}-convert-checkpoint.json")
VERIFY: All phases 00-06 have status "completed"
IF any phase incomplete: HALT "Workflow incomplete — phase ${N} not completed"
```

### Step 7.2: Compile Conversion Summary

```
EXECUTE: Extract from checkpoint:
  - MCP source and type
  - Detected pattern and confidence
  - Files generated count
  - Skill registered (yes/no)
  - Tests passed (yes/no)
  - Integration alignment score
VERIFY: Summary is non-empty with all fields populated
RECORD: N/A
```

### Step 7.3: Write Conversion Report

```
EXECUTE: Write(file_path="devforgeai/workflows/${CONVERT_ID}-conversion-report.md", content=report)
  Report includes: conversion summary, pattern analysis, files generated, validation results,
  registration status, and next steps
VERIFY: Glob() confirms file exists
RECORD: N/A
```

### Step 7.4: Display Results

```
EXECUTE: Display formatted result:

  ═══════════════════════════════════════
       MCP Conversion Complete
  ═══════════════════════════════════════

  ID:          ${CONVERT_ID}
  Pattern:     ${detected_pattern} (confidence: ${confidence})
  CLI:         ${OUTPUT_DIR}/cli.py
  Skill:       ${OUTPUT_DIR}/skill/SKILL.md
  Registered:  Yes/No
  Tests:       Passed/N/A
  Validation:  ${overall_status}

  ─── Next Steps ───
  1. Run:    python ${OUTPUT_DIR}/cli.py --help
  2. Review: ${OUTPUT_DIR}/skill/SKILL.md
  3. Test:   pytest ${OUTPUT_DIR}/tests/

  Report: devforgeai/workflows/${CONVERT_ID}-conversion-report.md
  ═══════════════════════════════════════

VERIFY: Display shown to user
RECORD: N/A
```

### Step 7.5: Finalize Checkpoint

```
EXECUTE: Update checkpoint:
  phases.07.status = "completed"
  progress.phases_completed += [7]
  progress.current_phase = "done"
  status = "completed"
  completed_at = ISO 8601 timestamp
VERIFY: Read checkpoint confirms status = "completed"
```

---

## Required Subagents Per Phase

| Phase | Subagent | Enforcement | Purpose |
|-------|----------|-------------|---------|
| 01 | code-analyzer | BLOCKING | Extract tool definitions from MCP source code |
| 03 | backend-architect | CONDITIONAL (custom only) | Review custom adapter template |
| 04 | code-reviewer | BLOCKING | Validate skill documentation quality |
| 05 | integration-tester | BLOCKING | Validate CLI + skill interface alignment |
| 05 | test-automator | CONDITIONAL | Enhance test stubs if needed |

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/${CONVERT_ID}-convert-checkpoint.json`
- **Updated:** After every phase completion
- **Verified:** Via `Glob()` and `Read()` after every write
- **Resume:** Read checkpoint, set `CURRENT_PHASE` from `progress.current_phase`, resume loop

---

## Workflow Completion Validation

```
required_phases = phases_completed + phases_skipped
IF len(required_phases) < 8:
    HALT "WORKFLOW INCOMPLETE — ${len(required_phases)}/8 phases accounted for"
    Display missing phases

Verify: Glob("${OUTPUT_DIR}/cli.*") returns CLI entry point
Verify: Glob("${OUTPUT_DIR}/skill/SKILL.md") returns skill file
Verify: Glob("tmp/${CONVERT_ID}/mcp_analysis.json") returns analysis
```

---

## Success Criteria

- CLI entry point exists and responds to `--help`
- Pattern-specific adapter generated
- Companion skill (SKILL.md) generated with correct pattern template
- Skill-to-CLI interface alignment validated
- Test stubs generated and executable
- User offered registration and dependency installation
- Conversion report written to `devforgeai/workflows/`
- All 8 phases completed and checkpointed

---

## Reference Files Index (Per-Phase Loading)

| Phase | Reference Files |
|-------|----------------|
| 00 | `references/parameter-extraction.md` |
| 01 | `references/source-loading.md` |
| 02 | `references/pattern-detection.md` |
| 03 | `references/adapter-api.md`, `references/cli-generation-templates.md` |
| 04 | `references/skill-generation-rules.md` |
| 05 | `references/validation-workflow.md` |
| 06 | `references/devforgeai-integration.md` |
| 07 | `references/result-formatting.md` |

---

## Deviation Protocol

If you need to deviate from ANY phase step:
1. HALT immediately
2. Use AskUserQuestion to explain the deviation and get user consent
3. Only proceed with explicit user approval
4. Record the deviation in the checkpoint under `deviations` key

**Without user consent, no deviation is permitted.**
