---
name: holistic-linting
description: This skill should be used when the model needs to ensure code quality through comprehensive linting and formatting. It provides automatic linting workflows for orchestrators (format → lint → resolve via concurrent agents) and sub-agents (lint touched files before task completion). Prevents claiming "production ready" code without verification. Includes linting rules knowledge base for ruff, mypy, and bandit, plus the linting-root-cause-resolver agent for systematic issue resolution.
---

# Holistic Linting Skill

This skill embeds comprehensive linting and formatting verification into Claude Code's workflow, preventing the common pattern where code is claimed "production ready" without actually running quality checks.

## Purpose

Prevent Claude from:

- Completing tasks without formatting and linting modified files
- Claiming code is "production quality" based on pattern-matching rather than verification
- Assuming only 2 linters exist (mypy + ruff) when projects may have 4+ linting tools
- Suppressing linting errors with `# type: ignore` or `# noqa` comments without understanding root causes

Ensure Claude:

- Automatically formats and lints all modified files before task completion
- Reads project-specific linting configuration from `CLAUDE.md`
- Resolves linting issues systematically using root-cause analysis
- Orchestrates concurrent linting agents when multiple files have issues

## When This Skill Applies

This skill applies to **all code editing tasks** in projects with linting configuration. It provides different behavior based on Claude's role:

### For Orchestrators (Interactive Claude Code CLI)

After completing implementation work:

1. **Delegate immediately** - Launch linting-root-cause-resolver agent for modified files
2. **Read reports** - Agent produces resolution reports in `.claude/reports/`
3. **Delegate review** - Launch post-linting-architecture-reviewer to validate resolution quality
4. **Iterate if needed** - Re-delegate to resolver if reviewer identifies issues

**CRITICAL**: Orchestrators do NOT run formatting or linting commands themselves. The agent gathers its own linting data, formats files, runs linters, and resolves issues. Orchestrators only delegate tasks and read completion reports.

### For Sub-Agents (Task-delegated agents)

Before completing any task that involved Edit/Write/MultiEdit:

1. **Format touched files** - Run formatters on files the agent modified
2. **Lint touched files** - Run linters on files the agent modified
3. **Resolve issues directly** - Use linting tools directly to fix issues
4. **Don't complete** - Don't mark task complete until all linting issues in touched files are resolved

<section ROLE_TYPE="orchestrator">

## Agent Delegation (Orchestrator Only)

### Complete Linting Workflow

**CRITICAL PRINCIPLE**: Orchestrators delegate work to agents. Orchestrators do NOT run formatting commands, linting commands, or quality checks themselves. The agent does ALL work (formatting, linting, resolution). The orchestrator only delegates tasks and reads reports to determine if more work is needed.

**WHY THIS MATTERS**:

- Pre-gathering linting data wastes orchestrator context window
- Running linters duplicates agent work (agent will run them again)
- Violates separation of concerns: "Orchestrators route context, agents do work"
- Creates context rot with linting output that becomes stale
- Prevents agents from gathering their own fresh context

The orchestrator MUST follow this delegation-first workflow:

**Step 1: Delegate to linting-root-cause-resolver immediately**

Delegate linting resolution WITHOUT running any linting commands first:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="Format, lint, and resolve any issues in <file_path>"
)
```

**What NOT to do before delegating**:

- ❌ Do NOT run `ruff format` before delegating
- ❌ Do NOT run `ruff check` before delegating
- ❌ Do NOT run `mypy` before delegating
- ❌ Do NOT gather linting output for the agent
- ❌ Do NOT read error messages to provide to the agent

**What TO do**:

- ✅ Delegate immediately with just the file path
- ✅ Let agent gather its own linting data
- ✅ Trust agent to run formatters and linters itself
- ✅ Wait for agent to complete and produce reports

**Reason**: The agent follows systematic root-cause analysis workflows. It autonomously:

- Reads project linting configuration from `CLAUDE.md`
- Runs formatters on modified files (ruff format, prettier, etc.)
- Executes linters to identify issues (ruff, mypy, pyright, etc.)
- Researches rule documentation
- Traces type flows and architectural context
- Implements elegant fixes following python3-development patterns
- Verifies resolution by re-running linters
- Creates resolution artifacts in `.claude/reports/` and `.claude/artifacts/`

**Multiple Files Modified**:

Launch concurrent agents (one per file) WITHOUT pre-gathering linting data:

```text
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/auth.py")
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/api.py")
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in tests/test_auth.py")
```

**Reason for concurrency**: Independent file resolutions proceed in parallel, reducing total time.

**Step 2: Delegate to post-linting-architecture-reviewer**

After linting agent completes, delegate architectural review:

```text
Task(
  agent="post-linting-architecture-reviewer",
  prompt="Review linting resolution for <file_path>"
)
```

**What the reviewer does**:

- Loads resolution artifacts from `.claude/reports/` and `.claude/artifacts/`
- Verifies resolution quality (root cause addressed, no symptom suppression)
- Validates architectural implications (design principles, type safety, code organization)
- Identifies systemic improvements applicable across codebase
- Generates architectural review report

**Step 3: Read reviewer report**

The orchestrator reads the review report to determine if additional work is needed:

```bash
ls -la .claude/reports/architectural-review-*.md
```

Read the most recent review report:

```claude
Read(".claude/reports/architectural-review-[timestamp].md")
```

**Orchestrator's role**: Read reports and decide next steps. Do NOT run linting commands to verify agent's work.

**Step 4: If issues found, delegate back to linting agent**

If architectural review identifies problems with resolution:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="Address issues found in architectural review: .claude/reports/architectural-review-[timestamp].md

Issues identified:
- [Summary of finding 1]
- [Summary of finding 2]

Review report contains detailed context and proposed solutions."
)
```

**Step 5: Repeat review if needed**

After re-resolution, delegate to reviewer again:

```text
Task(
  agent="post-linting-architecture-reviewer",
  prompt="Review updated linting resolution for <file_path>"
)
```

Continue workflow until architectural review reports clean results.

### Workflow Summary

```text
[Implementation complete]
  → [Step 1: Delegate to linting-root-cause-resolver] (agent formats, lints, resolves)
  → [Step 2: Delegate to post-linting-architecture-reviewer]
  → [Step 3: Orchestrator reads review report]
  → [Step 4: If issues found, delegate back to resolver with review path]
  → [Step 5: Repeat review until clean]
  → [Task complete ✓]
```

**Key Principle**: Orchestrator delegates immediately and reads reports. Agent does ALL actionable work (formatting, linting, resolution). Orchestrator does NOT run commands or gather linting data.

### Common Anti-Patterns to Avoid

**❌ WRONG** - Orchestrator pre-gathering linting data:

```text
# Don't do this:
Bash("ruff check src/auth.py")
# Read the output...
# Then delegate with the output
Task(agent="linting-root-cause-resolver", prompt="Fix these errors: [pasted errors]")
```

**✅ CORRECT** - Orchestrator delegates immediately:

```text
# Do this instead:
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/auth.py")
```

**❌ WRONG** - Orchestrator running formatters:

```text
# Don't do this:
Bash("ruff format src/auth.py src/api.py")
# Then delegate linting
```

**✅ CORRECT** - Agent handles both formatting and linting:

```text
# Do this instead:
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/auth.py")
```

**❌ WRONG** - Orchestrator verifying agent's work by running linters:

```text
# Don't do this:
# Agent completes
Bash("ruff check src/auth.py")  # Verifying agent's work
```

**✅ CORRECT** - Trust agent's verification, read reports instead:

```text
# Do this instead:
Read(".claude/reports/linting-resolution-[timestamp].md")
# Report shows agent already verified with linter output
```

</section>

## How to Use This Skill

### Automatic Behavior

This skill modifies Claude's standard workflow to include automatic quality checks:

**Before this skill**:

```text
[User request] → [Code changes] → [Task complete ✓]
```

**With this skill (Orchestrator)**:

```text
[User request] → [Code changes] → [Delegate to linting agent] → [Read reports] → [Task complete ✓]
```

**With this skill (Sub-Agent)**:

```text
[Task assigned] → [Code changes] → [Format] → [Lint] → [Resolve issues] → [Task complete ✓]
```

### Reading Project Linting Configuration

Before running any linters, check for the `## LINTERS` section in the project's `CLAUDE.md` file:

```claude
Grep(pattern="^## LINTERS", path="CLAUDE.md", output_mode="content", -A=50)
```

If the section exists, use those specifications as the authoritative source for what linters to run.

If the section does not exist, use the `/lint init` command (see below) to discover and document the project's linters.

### Expected CLAUDE.md LINTERS Section Format

```markdown
## LINTERS

git pre-commit hooks: enabled|disabled pre-commit tool: husky|pre-commit|manual

### Formatters

- markdownlint [*.{md,markdown}]
- ruff format [*.py]
- biome [*.{ts,js,tsx,jsx,json}]
- shfmt [*.{sh,bash,fish,zsh}]
- prettier [*.{md,markdown,mjs,cjs}]

### Static Checking and Linting

- ruff check [*.py]
- mypy [*.py]
- bandit [*.py]
- pyright [*.py]
- markdownlint [*.{md,markdown}]
```

### Running Formatters and Linters

**Git Hook Tool Detection** (if `.pre-commit-config.yaml` exists):

Use the detection script to identify and run the correct tool:

```bash
# Detect tool (outputs 'prek' or 'pre-commit')
uv run ./scripts/detect-hook-tool.py

# Run detected tool with arguments
uv run ./scripts/detect-hook-tool.py run --files path/to/file.py

# Check different repository on specific files
uv run ./scripts/detect-hook-tool.py --directory /path/to/repo run --files path/to/file.py
```

**Important - Scoped Operations**: Always use `--files` or staged file patterns rather than `--all-files`. Running hooks on all files formats code outside your current branch, causing:

- **Diff pollution**: Unrelated formatting changes appear in merge requests
- **Merge conflicts**: Changes to files not part of your feature
- **Broken git blame**: History attribution lost for mass-formatted files

Use `--all-files` ONLY when explicitly requested by the user for repository-wide cleanup.

Detection logic: reads `.git/hooks/pre-commit` line 2, token 5 identifies the tool. Defaults to `prek` if file missing.

**Note**: prek is a Rust-based drop-in replacement for pre-commit. Both tools use the same `.pre-commit-config.yaml` and have identical CLI interfaces.

**For Python files**:

```bash
# Format first (auto-fixes trivial issues)
uv run ruff format path/to/file.py

# Then lint (reports substantive issues)
uv run ruff check path/to/file.py
uv run mypy path/to/file.py
uv run pyright path/to/file.py
```

**For JavaScript/TypeScript files**:

```bash
# Format first
npx prettier --write path/to/file.ts

# Then lint
npx eslint path/to/file.ts
```

**For Shell scripts**:

```bash
# Format first
shfmt -w path/to/script.sh

# Then lint
shellcheck path/to/script.sh
```

**For Markdown**:

```bash
# Lint and auto-fix
npx markdownlint-cli2 --fix path/to/file.md
```

### Resolving Linting Issues

**For Orchestrators**: Delegate immediately to linting-root-cause-resolver WITHOUT running linters yourself:

```claude
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in file1.py")
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in file2.py")
```

Do NOT run `ruff check` or `mypy` before delegating. The agent gathers its own linting data.

**For Sub-Agents**: Follow the linter-specific resolution workflow documented below based on the linting tool reporting the issue.

## Linter-Specific Resolution Workflows

This section provides systematic resolution procedures for each major Python linting tool. Sub-agents executing the linting-root-cause-resolver process MUST follow the appropriate workflow based on the linter reporting issues.

### Ruff Resolution Workflow

**When to use**: Linting errors with ruff rule codes (E, F, W, B, S, I, UP, C90, N, etc.)

**Resolution Process**:

1. **Research the Rule**

   Use ruff's built-in documentation system:

   ```bash
   ruff rule {RULE_CODE}
   ```

   Examples:

   ```bash
   ruff rule F401  # unused-import
   ruff rule E501  # line-too-long
   ruff rule B006  # mutable-default-argument
   ```

   This command provides:

   - What the rule prevents (design principle)
   - When code violates the rule
   - Example of violating code
   - Example of resolved code
   - Configuration options

2. **Read Rule Documentation Output**

   The ruff rule output contains critical information:

   - **Principle**: Why this pattern is problematic
   - **Bad Pattern**: What code triggers the rule
   - **Good Pattern**: How to fix it correctly

   **Motivation**: Understanding the principle prevents similar issues in other locations.

3. **Read the Affected Code**

   Read the complete file containing the linting error:

   ```claude
   Read("/path/to/file.py")
   ```

   Focus on:

   - The line with the error
   - Surrounding context (5-10 lines before/after)
   - Related function/class definitions

4. **Check Architectural Context**

   Examine how this code fits into the broader system:

   - What does this function/module do?
   - How is it called by other code?
   - Are there similar patterns elsewhere in the codebase?

   Use Grep to find usage patterns:

   ```bash
   uv run rg "function_name" --type py
   ```

5. **Load python3-development Skill**

   Before implementing fixes:

   ```claude
   Skill(command: "python3-development")
   ```

   **Motivation**: Ensures fixes follow Python 3.11+ standards, modern typing patterns, and project conventions.

6. **Implement Elegant Fix**

   Apply the fix following these principles:

   - Address the root cause, not the symptom
   - Follow modern Python patterns from python3-development skill
   - Maintain or improve code readability
   - Consider performance and maintainability
   - Add comments only if the fix is non-obvious

7. **Verify Resolution**

   Rerun ruff to confirm the fix:

   ```bash
   uv run ruff check /path/to/file.py
   ```

**Example Workflow Execution**:

```text
Issue: ruff reports "F401: 'os' imported but unused" in utils.py

1. Research: ruff rule F401
   → Output: Unused imports clutter namespace and may hide typos
   → Fix: Remove unused import or use it

2. Read code: Read("utils.py")
   → Line 5: import os
   → Code never references 'os' module

3. Check context: Grep "import os" in project
   → Other files use os.path, os.environ
   → This file genuinely doesn't need it

4. Load python3-development skill

5. Implement: Remove unused import from line 5

6. Verify: ruff check utils.py → Clean
```

### Mypy Resolution Workflow

**When to use**: Type checking errors with mypy error codes (attr-defined, arg-type, return-value, etc.)

**Resolution Process**:

1. **Research the Error Code**

   Mypy errors contain error codes in brackets like `[attr-defined]` or `[arg-type]`.

   Look up the error code in locally-cached documentation:

   ```claude
   Read("./references/mypy-docs/error_code_list.rst")
   Read("./references/mypy-docs/error_code_list2.rst")
   ```

   Search for the error code:

   ```bash
   grep -n "error-code-{CODE}" ./references/mypy-docs/*.rst
   ```

   **Motivation**: Mypy error codes map to specific type safety principles. Understanding the principle prevents misunderstanding type relationships.

2. **Read Error Code Documentation**

   The mypy documentation explains:

   - What type safety principle is violated
   - When this is an error (type violations)
   - When this is NOT an error (valid patterns)
   - Example of error-producing code
   - Example of corrected code

   **Key insight**: Mypy errors often indicate misunderstanding about what types a function accepts or returns.

3. **Trace Type Flow**

   Follow the data flow to understand type relationships:

   a. **Read the error location**:

   ```claude
   Read("/path/to/file.py")
   ```

   b. **Identify the type mismatch**:

   - What type does mypy think the variable is?
   - What type does mypy expect?
   - Where does the variable get its type?

   c. **Trace upstream**:

   - Read function signatures
   - Check return type annotations
   - Review variable assignments

   d. **Check library type stubs**:

   - If the error involves a library, check its type stubs
   - Use `python -c "import library; print(library.__file__)"` to locate
   - Read `.pyi` stub files or `py.typed` marker

4. **Check Architectural Context**

   Understand the design intent:

   - What is this function supposed to do?
   - What types should it accept and return?
   - Is the current type annotation accurate?
   - Are there implicit contracts not captured in types?

5. **Load python3-development Skill**

   Before implementing fixes:

   ```claude
   Skill(command: "python3-development")
   ```

   **Motivation**: Ensures type annotations follow Python 3.11+ syntax (native generics, `|` union syntax, modern typing patterns).

6. **Implement Elegant Fix**

   Choose the appropriate fix strategy:

   **Strategy A: Fix the type annotation** (if annotation is wrong)

   ```python
   # Before: Function returns dict but annotated as returning Response
   def get_data() -> Response:
       return {"key": "value"}  # mypy error: Incompatible return value type

   # After: Correct annotation to match actual return
   def get_data() -> dict[str, str]:
       return {"key": "value"}
   ```

   **Strategy B: Fix the implementation** (if annotation is correct)

   ```python
   # Before: Function should return Response but returns dict
   def get_data() -> Response:
       return {"key": "value"}  # mypy error: Incompatible return value type

   # After: Fix implementation to return correct type
   def get_data() -> Response:
       return Response(data={"key": "value"})
   ```

   **Strategy C: Add type narrowing** (if type is conditional)

   ```python
   # Before: Mypy can't prove value is not None
   def process(value: str | None) -> str:
       return value.upper()  # mypy error: Item "None" has no attribute "upper"

   # After: Add type guard
   def process(value: str | None) -> str:
       if value is None:
           raise ValueError("value cannot be None")
       return value.upper()
   ```

   **Strategy D: Use TypeGuard for complex narrowing**

   ```python
   from typing import TypeGuard

   def is_valid_response(data: dict[str, Any]) -> TypeGuard[dict[str, str]]:
       return all(isinstance(v, str) for v in data.values())

   def process(data: dict[str, Any]) -> dict[str, str]:
       if not is_valid_response(data):
           raise ValueError("Invalid data format")
       return data  # mypy now knows this is dict[str, str]
   ```

7. **Verify Resolution**

   Rerun mypy to confirm the fix:

   ```bash
   uv run mypy /path/to/file.py
   ```

**Example Workflow Execution**:

```text
Issue: mypy reports "Incompatible return value type (got dict[str, Any], expected Response)" in api_client.py:45

1. Research: Search error_code_list.rst for "return-value"
   → Found: Error code [return-value]
   → Principle: Function must return type matching its annotation

2. Read documentation:
   → This occurs when returned expression type doesn't match declared return type
   → Common cause: Function signature doesn't match implementation

3. Trace type flow:
   - Read api_client.py line 45
   - Function signature: def fetch_data() -> Response:
   - Actual return: return response.json()
   - response.json() returns dict[str, Any], not Response

4. Check context:
   - fetch_data should return parsed JSON as dict, not Response object
   - Other functions in module follow pattern: parse response to dict
   - Function signature is incorrect, not the implementation

5. Load python3-development skill

6. Implement: Change function signature from Response to dict[str, Any]
   def fetch_data() -> dict[str, Any]:
       return response.json()

7. Verify: mypy api_client.py → Clean
```

### Pyright/Basedpyright Resolution Workflow

**When to use**: Type checking errors with pyright diagnostic rules (reportGeneralTypeIssues, reportOptionalMemberAccess, reportUnknownVariableType, etc.)

**Resolution Process**:

1. **Research the Diagnostic Rule**

   Pyright errors reference diagnostic rule names like `reportOptionalMemberAccess` or `reportGeneralTypeIssues`.

   Look up the rule in basedpyright documentation:

   **For rule settings and descriptions**:

   Use MCP tools for documentation lookup (in order of preference):

   ```claude
   # Option 1 (Preferred): Use Ref MCP for high-fidelity documentation
   mcp__Ref__ref_search_documentation(query="basedpyright {RULE_NAME} diagnostic rule configuration")
   # Then read the URL from results:
   mcp__Ref__ref_read_url(url="<exact_url_from_search_results>")

   # Option 2: Use exa for code context if Ref doesn't have it
   mcp__exa__get_code_context_exa(query="basedpyright {RULE_NAME} diagnostic rule examples")

   # Fallback: Use WebFetch only if MCP tools don't work
   WebFetch(url="https://docs.basedpyright.com/latest/configuration/config-files/",
           prompt="Find documentation for diagnostic rule {RULE_NAME}")
   ```

   **For features and PEP support**:

   ```claude
   # Option 1 (Preferred): Use Ref MCP for high-fidelity documentation
   mcp__Ref__ref_search_documentation(query="basedpyright Python typing features PEP {RULE_NAME}")
   mcp__Ref__ref_read_url(url="<exact_url_from_search_results>")

   # Fallback: Use WebFetch only if MCP tools don't work
   WebFetch(url="https://docs.basedpyright.com/latest/getting_started/features/",

   > [Web resource access, definitive guide for getting accurate data for high quality results](./references/accessing_online_resources.md)
           prompt="Explain what Python typing features and PEPs are covered related to {RULE_NAME}")
   ```

   **Motivation**: Pyright is more strict than mypy in many areas. Understanding what the rule enforces helps identify whether the issue is a genuine type safety problem or overly strict checking.

2. **Read Diagnostic Rule Documentation**

   The basedpyright documentation explains:

   - What type safety issue the rule detects
   - Configuration levels (basic, standard, strict, all)
   - Whether the rule can be disabled per-project
   - Related typing features and PEPs

3. **Read the Affected Code**

   Read the complete file containing the type error:

   ```claude
   Read("/path/to/file.py")
   ```

   Focus on:

   - The exact line with the error
   - Type annotations in the surrounding function/class
   - Import statements for typing constructs

4. **Understand the Type Inference Issue**

   Pyright has sophisticated type inference. Common issues:

   **Optional member access**:

   ```python
   # Error: reportOptionalMemberAccess
   value: str | None = get_value()
   result = value.upper()  # Error: 'value' could be 'None'
   ```

   **Unknown variable type**:

   ```python
   # Error: reportUnknownVariableType
   result = some_function()  # some_function has no return type annotation
   ```

   **Type narrowing not recognized**:

   ```python
   # Error: pyright doesn't recognize the narrowing
   value: int | str = get_value()
   if type(value) == int:  # Use isinstance() instead
       result = value + 1
   ```

5. **Check Architectural Context**

   Determine if the error reveals a real issue:

   - Is the type annotation incomplete or wrong?
   - Is there missing type narrowing?
   - Is the code relying on runtime behavior not captured in types?
   - Should the function signature be more precise?

6. **Load python3-development Skill**

   Before implementing fixes:

   ```claude
   Skill(command: "python3-development")
   ```

   **Motivation**: Ensures fixes use modern Python 3.11+ typing features that pyright fully supports.

7. **Implement Elegant Fix**

   Choose the appropriate fix strategy:

   **Strategy A: Add type narrowing guards**

   ```python
   # Before:
   def process(value: str | None) -> str:
       return value.upper()  # reportOptionalMemberAccess

   # After:
   def process(value: str | None) -> str:
       if value is None:
           raise ValueError("value is required")
       return value.upper()  # pyright knows value is str here
   ```

   **Strategy B: Add missing type annotations**

   ```python
   # Before:
   def fetch_data():  # reportUnknownVariableType on callers
       return {"key": "value"}

   # After:
   def fetch_data() -> dict[str, str]:
       return {"key": "value"}
   ```

   **Strategy C: Use assert for type narrowing**

   ```python
   # Before:
   value: int | str = get_value()
   result = value + 1  # reportGeneralTypeIssues

   # After:
   value: int | str = get_value()
   assert isinstance(value, int), "Expected int"
   result = value + 1  # pyright knows value is int
   ```

   **Strategy D: Use typing.cast for complex cases**

   ```python
   from typing import cast

   # Before:
   data: dict[str, Any] = get_data()
   name: str = data["name"]  # reportUnknownVariableType

   # After (if you've validated data structure):
   from typing import TypedDict

   class UserData(TypedDict):
       name: str
       age: int

   data = cast(UserData, get_data())
   name: str = data["name"]  # pyright knows this is str
   ```

   **Strategy E: Configure rule if genuinely too strict**

   Only as a last resort, adjust `pyproject.toml`:

   ```toml
   [tool.pyright]
   reportOptionalMemberAccess = "warning"  # Downgrade from error
   ```

8. **Verify Resolution**

   Rerun pyright/basedpyright to confirm:

   ```bash
   uv run pyright /path/to/file.py
   # or
   uv run basedpyright /path/to/file.py
   ```

**Example Workflow Execution**:

```text
Issue: pyright reports "reportOptionalMemberAccess: 'upper' is not a known member of 'None'" in validator.py:23

1. Research: Use MCP tools to fetch basedpyright docs for reportOptionalMemberAccess
   → mcp__Ref__ref_search_documentation for verbatim documentation
   → Rule detects accessing members on values that could be None
   → Prevents AttributeError at runtime
   → Configuration: Can be set to basic/standard/strict

2. Read documentation:
   → Rule enforces proper handling of Optional types
   → Requires explicit None checks before member access
   → Prevents common NoneType AttributeError crashes

3. Read code: Read("validator.py")
   → Line 23: return data.upper()
   → Function signature: def validate(data: str | None) -> str:
   → No None check before calling .upper()

4. Understand issue:
   → data could be None at runtime
   → .upper() would raise AttributeError if data is None
   → This is a genuine bug caught by type checker

5. Load python3-development skill

6. Implement: Add type narrowing
   def validate(data: str | None) -> str:
       if data is None:
           raise ValueError("data cannot be None")
       return data.upper()

7. Verify: pyright validator.py → Clean
```

## Integration: Resolution Process with python3-development

All linter resolution workflows integrate with the python3-development skill at the implementation stage. This integration ensures:

1. **Modern Python Patterns**: Fixes use Python 3.11+ syntax

   - Native generics (`list[str]` not `List[str]`)
   - Union syntax (`str | None` not `Optional[str]`)
   - Structural pattern matching where appropriate

2. **Idiomatic Code**: Solutions follow Python best practices

   - Clear naming conventions
   - Appropriate use of comprehensions
   - Proper exception handling
   - Single Responsibility Principle

3. **Type Safety**: Type annotations are complete and accurate

   - Precise return types
   - Correct parameter types
   - Proper use of generics and protocols

4. **Project Consistency**: Fixes align with existing codebase patterns
   - Consistent with project's CLAUDE.md standards
   - Matches existing module organization
   - Follows project-specific conventions

**Activation pattern**:

```text
[Identify linting issue] → [Research rule] → [Read code] → [Check architecture]
→ [Load python3-development skill] → [Implement elegant fix] → [Verify]
```

## Bundled Resources

### Agent: linting-root-cause-resolver

Location: [`./agents/linting-root-cause-resolver.md`](./agents/linting-root-cause-resolver.md)

This agent systematically investigates and resolves linting errors by understanding root causes rather than suppressing them with ignore comments.

**To install the agent**:

```bash
# Install to user scope (~/.claude/agents/)
python holistic-linting/scripts/install-agents.py --scope user

# Install to project scope (<git-root>/.claude/agents/)
python holistic-linting/scripts/install-agents.py --scope project

# Overwrite existing agent file
python holistic-linting/scripts/install-agents.py --scope user --force
```

**Philosophy**:

- Linting errors are symptoms of deeper issues
- Never silence errors without understanding them
- Always verify assumptions through investigation
- Prioritize clarity and correctness over quick fixes

### Rules Knowledge Base

Comprehensive documentation of linting rules from three major tools:

#### Ruff Rules (933 rules documented)

Location: [`./references/rules/ruff/index.md`](./references/rules/ruff/index.md)

Covers all Ruff rule families including:

- **E/W** (pycodestyle errors and warnings)
- **F** (Pyflakes logical errors)
- **B** (flake8-bugbear common bugs)
- **S** (Bandit security checks)
- **I** (isort import sorting)
- **UP** (pyupgrade modern Python patterns)
- And 13 more families

Each rule documents:

- What it prevents (design principle)
- When it's a violation (examples)
- When it's NOT a violation (edge cases)
- Violating code examples
- Resolved code examples
- Configuration options

#### MyPy Error Codes

Location: [`./references/rules/mypy/index.md`](./references/rules/mypy/index.md)

Comprehensive type checking error documentation organized by category:

- Attribute access errors
- Name resolution errors
- Function call type checking
- Assignment compatibility
- Collection type checking
- Operator usage
- Import resolution
- Abstract class enforcement
- Async/await patterns

Each error code documents:

- Type safety principle it enforces
- When this is an error (type violations)
- When this is NOT an error (valid patterns)
- Error-producing code examples
- Corrected code examples
- Configuration options (mypy.ini, pyproject.toml)

#### Bandit Security Checks (65+ checks documented)

Location: [`./references/rules/bandit/index.md`](./references/rules/bandit/index.md)

Security vulnerability documentation organized by category:

- Credentials and secrets
- Cryptography weaknesses
- SSL/TLS vulnerabilities
- Injection attacks (command, SQL, XML)
- Deserialization risks
- File permissions
- Unsafe functions
- Framework configuration
- Dangerous imports

Each check documents:

- Security risk (what vulnerability it prevents)
- When this is vulnerable (insecure patterns)
- When this is NOT vulnerable (safe usage)
- Vulnerable code examples
- Secure code examples with mitigations
- Severity level (LOW, MEDIUM, HIGH)

### Scripts (Coming Soon)

The following scripts will be available in [`./scripts/`](./scripts/):

1. **install-agents.py** - Install the linting-root-cause-resolver agent
2. **discover-linters.py** - Scan project and generate LINTERS section for CLAUDE.md
3. **lint-orchestrator.py** - Run project linters based on CLAUDE.md configuration

## Slash Commands

### `/lint` Command

The `/lint` slash command provides manual invocation of linting workflows.

**Usage**:

```bash
/lint                    # Lint all files in current directory
/lint path/to/file.py    # Lint specific file
/lint path/to/directory  # Lint all files in directory
/lint init               # Discover linters and update CLAUDE.md
/lint init --force       # Re-discover linters (overwrite existing config)
```

See [`/.claude/commands/lint.md`](/.claude/commands/lint.md) for the full command implementation.

## Integration with Claude Code Hooks

This skill complements the [claude-linting-hook](https://github.com/yourrepo/claude-linting-hook) which provides automatic PostToolUse linting via Claude Code hooks. The hook and skill serve different purposes:

**claude-linting-hook** (PostToolUse hook):

- Triggers automatically after Edit/Write/MultiEdit
- Provides immediate feedback during development
- Blocks on substantive issues
- Runs in hook execution context

**holistic-linting skill** (Workflow guidance):

- Guides Claude's task completion workflow
- Ensures linting happens before claiming "done"
- Provides rules knowledge base for investigation
- Includes systematic resolution process via linting-root-cause-resolver agent

Use both together for comprehensive linting coverage:

1. Hook catches issues immediately during editing
2. Skill ensures systematic resolution before task completion
3. Knowledge base supports root-cause analysis

## Examples

### Example 1: Orchestrator completes Python feature implementation

```text
User: "Add authentication middleware to the API"

Orchestrator:
1. [Implements authentication middleware in auth.py]
2. [Implementation complete, now applying holistic-linting skill]
3. [Delegates to linting agent WITHOUT running linters]
4. Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in auth.py")
5. [Agent formats with ruff format, runs ruff check + mypy]
6. [Agent finds 3 ruff errors, 2 mypy type issues]
7. [Agent resolves all 5 issues at root cause]
8. [Agent verifies: ruff check + mypy - clean]
9. [Agent produces resolution report in .claude/reports/]
10. [Orchestrator reads report confirming clean resolution]
11. Task complete ✓
```

### Example 2: Sub-agent writes Python module

```text
Orchestrator delegates: "Create database connection pool module"

Sub-agent:
1. [Writes db_pool.py with connection logic]
2. [Before completing, applies holistic-linting skill]
3. Formatting: uv run ruff format db_pool.py
4. Linting: uv run ruff check db_pool.py && uv run mypy db_pool.py
5. [Finds 1 mypy error: Missing return type annotation]
6. [Investigates: function should return ConnectionPool]
7. [Fixes: Adds -> ConnectionPool annotation]
8. [Verifies: uv run mypy db_pool.py - clean]
9. Returns to orchestrator with completed, lint-free module ✓
```

### Example 3: Using /lint init to discover project linters

```text
/lint init

[Scanning project configuration...]
✓ Found .pre-commit-config.yaml with 6 hooks
✓ Found pyproject.toml with ruff, mypy, pyright config
✓ Found package.json with eslint, prettier
✓ Git pre-commit hooks: enabled (husky)

[Generated LINTERS section]

## LINTERS

git pre-commit hooks: enabled
pre-commit tool: husky

### Formatters
- ruff format [*.py]
- prettier [*.{ts,tsx,json,md}]

### Static Checking and Linting
- ruff check [*.py]
- mypy [*.py]
- pyright [*.py]
- eslint [*.{ts,tsx}]
- markdownlint [*.md]

[Appended to CLAUDE.md ✓]
```

## Best Practices

1. **Orchestrators delegate immediately** - Do NOT run formatters or linters before delegating. Agent gathers its own context.
2. **Always read CLAUDE.md LINTERS section first** - Don't assume which linters are available
3. **Format before linting (Sub-Agents only)** - Formatters auto-fix trivial issues (end-of-file, whitespace)
4. **Run linters concurrently (Sub-Agents only)** - Use parallel execution for multiple files or multiple linters
5. **Use the rules knowledge base** - Reference official rule documentation when investigating
6. **Never suppress without understanding** - Don't add `# type: ignore` or `# noqa` without root cause analysis
7. **Orchestrators delegate, sub-agents execute** - Orchestrators launch agents and read reports. Sub-agents run formatters, linters, and resolve issues.
8. **Verify after fixes (Sub-Agents only)** - Always re-run linters to confirm issues are resolved
9. **Trust agent verification (Orchestrators)** - Read resolution reports instead of re-running linters to verify

## Troubleshooting

**Problem**: "I don't know which linters this project uses" **Solution**: Run `/lint init` to scan and document project linters

**Problem**: "Linting errors but I don't understand the rule" **Solution**: Reference the rules knowledge base at `./references/rules/{ruff,mypy,bandit}/index.md`

**Problem**: "Multiple files with linting errors" **Solution**: If orchestrator, launch concurrent linting-root-cause-resolver agents (one per file). If sub-agent, resolve each file sequentially.

**Problem**: "Linter not found (command not available)" **Solution**: Check that linters are installed. Use `uv run <tool>` for Python tools to ensure virtual environment activation.

**Problem**: "False positive linting error" **Solution**: Investigate using the rule's documentation. If truly a false positive, configure the rule in pyproject.toml/config file rather than using ignore comments.

## Skill Activation

This skill is automatically loaded when installed in `~/.claude/skills/holistic-linting`.

To manually reference this skill in a session:

```text
Activate the holistic-linting skill: Skill(command: "holistic-linting")
```

## Related Skills

- **python3-development** - Modern Python development patterns and best practices
- **uv** - Python package and project management with uv
