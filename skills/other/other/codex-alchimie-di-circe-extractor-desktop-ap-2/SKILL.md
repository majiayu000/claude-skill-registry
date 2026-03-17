---
name: codex
version: 2.1.0
description: Invoke Codex CLI for complex coding tasks requiring high reasoning capabilities. Trigger phrases include "use codex", "ask codex", "run codex", "call codex", "codex cli", "GPT-5 reasoning", "OpenAI reasoning", or when users request complex implementation challenges, advanced reasoning, architecture design, or high-reasoning model assistance. Automatically triggers on codex-related requests and supports session continuation for iterative development.
---

# Codex: High-Reasoning AI Assistant for Claude Code

---

## DEFAULT MODEL: Task-Based Model Selection with Read-Only Default

**Codex uses task-based model selection. Sandbox is `read-only` by default - only use `workspace-write` when user explicitly requests file editing.**

| Task Type | Model | Sandbox (default) | Sandbox (explicit edit) |
|-----------|-------|-------------------|------------------------|
| Code-related tasks | `gpt-5.2-codex` | read-only | workspace-write |
| General tasks | `gpt-5.2` | read-only | workspace-write |

- **Code-related tasks**: Use `gpt-5.2-codex` - optimized for agentic coding (56.4% SWE-Bench Pro)
- **General tasks**: Use `gpt-5.2` - high-reasoning general model
- **Sandbox default**: Always `read-only` unless user explicitly requests editing
- **Explicit editing**: Only when user says "edit", "modify", "write changes", etc., use `workspace-write`
- Always use `-c model_reasoning_effort=xhigh` for maximum capability

```bash
# Code task (read-only default)
codex exec -m gpt-5.2-codex -s read-only \
  -c model_reasoning_effort=xhigh \
  "analyze this function implementation"

# General task (read-only default)
codex exec -m gpt-5.2 -s read-only \
  -c model_reasoning_effort=xhigh \
  "explain this architecture"

# Code task with explicit edit request
codex exec -m gpt-5.2-codex -s workspace-write \
  -c model_reasoning_effort=xhigh \
  "edit this file to add the feature"

# General task with explicit edit request
codex exec -m gpt-5.2 -s workspace-write \
  -c model_reasoning_effort=xhigh \
  "modify the documentation file"
```

### Model Fallback Chain

If the primary model is unavailable, fallback gracefully:
1. **Code tasks**: `gpt-5.2-codex` → `gpt-5.2` → `gpt-5.1-codex-max`
2. **General tasks**: `gpt-5.2` → `gpt-5.1` → `gpt-5.1-codex-max`
3. **Reasoning effort**: `xhigh` → `high` → `medium`

---

## CRITICAL: Always Use `codex exec`

**MUST USE**: `codex exec` for ALL Codex CLI invocations in Claude Code.

**NEVER USE**: `codex` (interactive mode) - will fail with "stdout is not a terminal"
**ALWAYS USE**: `codex exec` (non-interactive mode)

**Examples:**
- `codex exec -m gpt-5.2 "prompt"` (CORRECT)
- `codex -m gpt-5.2 "prompt"` (WRONG - will fail)
- `codex exec resume --last` (CORRECT)
- `codex resume --last` (WRONG - will fail)

**Why?** Claude Code's bash environment is non-terminal/non-interactive. Only `codex exec` works in this environment.

---

## IMPORTANT: Interactive vs Exec Mode Flags

**Some Codex CLI flags are ONLY available in interactive mode, NOT in `codex exec`.**

| Flag | Interactive `codex` | `codex exec` | Alternative for exec |
|------|---------------------|--------------|---------------------|
| `--search` | ✅ Available | ❌ NOT available | `--enable web_search_request` |
| `-a/--ask-for-approval` | ✅ Available | ❌ NOT available | `--full-auto` or `-c approval_policy=...` |
| `--add-dir` | ✅ Available | ✅ Available | N/A |
| `--full-auto` | ✅ Available | ✅ Available | N/A |

**For web search in exec mode**:
```bash
# CORRECT - works in codex exec
codex exec --enable web_search_request "research topic"

# WRONG - --search only works in interactive mode
codex --search "research topic"
```

**For approval control in exec mode**:
```bash
# CORRECT - works in codex exec
codex exec --full-auto "task"
codex exec -c approval_policy=on-request "task"

# WRONG - -a only works in interactive mode
codex -a on-request "task"
```

---

## Trigger Examples

This skill activates when users say phrases like:
- "Use codex to analyze this architecture"
- "Ask codex about this design decision"
- "Run codex on this problem"
- "Call codex for help with this implementation"
- "I need GPT-5 reasoning for this task"
- "Get OpenAI's high-reasoning model on this"
- "Continue with codex" or "Resume the codex session"
- "Codex, help me with..." or simply "Codex"

## When to Use This Skill

This skill should be invoked when:
- User explicitly mentions "Codex" or requests Codex assistance
- User needs help with complex coding tasks, algorithms, or architecture
- User requests "high reasoning" or "advanced implementation" help
- User needs complex problem-solving or architectural design
- User wants to continue a previous Codex conversation

## How It Works

### Detecting New Codex Requests

When a user makes a request, first determine the task type (code vs general), then determine sandbox based on explicit edit request:

**Step 1: Determine Task Type (Model Selection)**
- **Code-related tasks**: Use `gpt-5.2-codex` - for implementation, refactoring, code analysis, debugging, etc.
- **General tasks**: Use `gpt-5.2` - for architecture design, explanations, reviews, documentation, etc.

**Step 2: Determine Sandbox (Edit Permission)**
- **Default**: `read-only` - safe for all tasks unless user explicitly requests editing
- **Explicit edit request**: `workspace-write` - ONLY when user explicitly says to edit/modify/write files

**Code-related task examples**:
- Read-only: "Analyze this function", "Review this implementation", "Debug this code"
- With editing: "Edit this file to fix the bug", "Modify the function", "Refactor and save"

**General task examples**:
- Read-only: "Design a queue data structure", "Explain this algorithm", "Review the architecture"
- With editing: "Update the documentation file", "Modify the README"

**⚠️ Important**: The key distinction for sandbox is whether the user explicitly asks for file modifications. Use `workspace-write` ONLY when user says "edit", "modify", "write changes", "save", etc.

### Bash CLI Command Structure

**IMPORTANT**: Always use `codex exec` for non-interactive execution. Claude Code's bash environment is non-terminal, so the interactive `codex` command will fail with "stdout is not a terminal" error.

#### Code Task (Read-Only Default)

```bash
codex exec -m gpt-5.2-codex -s read-only \
  -c model_reasoning_effort=xhigh \
  --enable web_search_request \
  "<code-related prompt>"
```

#### General Task (Read-Only Default)

```bash
codex exec -m gpt-5.2 -s read-only \
  -c model_reasoning_effort=xhigh \
  --enable web_search_request \
  "<general prompt>"
```

#### Code Task with Explicit Edit Request

```bash
codex exec -m gpt-5.2-codex -s workspace-write \
  -c model_reasoning_effort=xhigh \
  --enable web_search_request \
  "<edit code prompt>"
```

#### General Task with Explicit Edit Request

```bash
codex exec -m gpt-5.2 -s workspace-write \
  -c model_reasoning_effort=xhigh \
  --enable web_search_request \
  "<edit general files prompt>"
```

**Why `codex exec`?**
- Non-interactive mode required for automation and Claude Code integration
- Produces clean output suitable for parsing
- Works in non-TTY environments (like Claude Code's bash)

### Model Selection Logic

**Step 1: Choose Model Based on Task Type**

**Use `gpt-5.2-codex` for code-related tasks:**
- Implementation, refactoring, code analysis
- Debugging, fixing bugs, optimization
- Any task involving code understanding or modification

**Use `gpt-5.2` for general tasks:**
- Architecture and system design
- Explanations, documentation, reviews
- Planning, strategy, general reasoning

**Step 2: Choose Sandbox Based on Edit Intent**

**Use `read-only` (DEFAULT):**
- Analysis, review, explanation tasks
- ANY task where user does NOT explicitly request file editing

**Use `workspace-write` (ONLY when explicitly requested):**
- User explicitly says "edit this file", "modify the code", "write changes"
- User explicitly asks to "make edits" or "save the changes"
- User explicitly requests "refactor and save" or "implement and write"

**Fallback Models**: `gpt-5.1-codex-max` and `gpt-5.1` are available if primary models are unavailable. See fallback chain in DEFAULT MODEL section.

### Default Configuration

All Codex invocations use these defaults unless user specifies otherwise:

| Parameter | Default Value | CLI Flag | Notes |
|-----------|---------------|----------|-------|
| Model (code tasks) | `gpt-5.2-codex` | `-m gpt-5.2-codex` | For code-related tasks |
| Model (general tasks) | `gpt-5.2` | `-m gpt-5.2` | For general tasks |
| Sandbox (default) | `read-only` | `-s read-only` | Safe default for ALL tasks |
| Sandbox (explicit edit) | `workspace-write` | `-s workspace-write` | Only when user explicitly requests editing |
| Reasoning Effort | `xhigh` | `-c model_reasoning_effort=xhigh` | Maximum reasoning capability |
| Verbosity | `medium` | `-c model_verbosity=medium` | Balanced output detail |
| Web Search | `enabled` | `--enable web_search_request` | Access to up-to-date information |

### CLI Flags Reference

**Codex CLI Version**: 0.72.0+ (requires 0.72.0+ for gpt-5.2-codex and xhigh)

| Flag | Values | Description |
|------|--------|-------------|
| `-m, --model` | `gpt-5.2-codex`, `gpt-5.2`, `gpt-5.1-codex-max`, `gpt-5.1` | Model selection |
| `-s, --sandbox` | `read-only`, `workspace-write`, `danger-full-access` | Sandbox mode |
| `-c, --config` | `key=value` | Config overrides (e.g., `model_reasoning_effort=high`) |
| `-C, --cd` | directory path | Working directory |
| `-p, --profile` | profile name | Use config profile |
| `--enable` | feature name | Enable a feature (e.g., `web_search_request`) |
| `--disable` | feature name | Disable a feature |
| `-i, --image` | file path(s) | Attach image(s) to initial prompt |
| `--add-dir` | directory path | Additional writable directory (repeatable) |
| `--full-auto` | flag | Convenience for workspace-write sandbox with on-request approval |
| `--oss` | flag | Use local open source model provider |
| `--local-provider` | `lmstudio`, `ollama` | Specify local provider (with --oss) |
| `--skip-git-repo-check` | flag | Allow running outside Git repository |
| `--output-schema` | file path | JSON Schema file for response shape |
| `--color` | `always`, `never`, `auto` | Color settings for output |
| `--json` | flag | Print events as JSONL |
| `-o, --output-last-message` | file path | Save last message to file |
| `--dangerously-bypass-approvals-and-sandbox` | flag | Skip confirmations (DANGEROUS) |

### Configuration Parameters

Pass these as `-c key=value`:

- `model_reasoning_effort`: `minimal`, `low`, `medium`, `high`, `xhigh`
  - **CLI default**: `high` - The Codex CLI defaults to high reasoning
  - **Skill default**: `xhigh` - This skill explicitly uses xhigh for maximum capability
  - **`xhigh`**: Extra-high reasoning for maximum capability (supported by gpt-5.2 and gpt-5.1-codex-max)
  - Use `xhigh` for complex architectural refactoring, long-horizon tasks, or when quality is more important than speed
- `model_verbosity`: `low`, `medium`, `high` (default: `medium`)
- `model_reasoning_summary`: `auto`, `concise`, `detailed`, `none` (default: `auto`)
- `sandbox_workspace_write.writable_roots`: JSON array of additional writable directories (e.g., `["/path1","/path2"]`)
- `approval_policy`: `untrusted`, `on-failure`, `on-request`, `never` (approval behavior)

**Additional Writable Directories**:

Use `--add-dir` flag (preferred) or config:
```bash
# Preferred - simpler syntax (v0.71.0+)
codex exec --add-dir /path1 --add-dir /path2 "task"

# Alternative - config approach
codex exec -c 'sandbox_workspace_write.writable_roots=["/path1","/path2"]' "task"
```

### Model Selection Guide

**Default Models (Codex CLI v0.71.0+)**

This skill supports the following models:
- `gpt-5.2` - Latest model with all reasoning levels (NEW in 0.71.0)
- `gpt-5.1` - General reasoning, architecture, reviews (default)
- `gpt-5.1-codex-max` - Code editing (legacy, use gpt-5.2 instead)
- `gpt-5.1-codex` - Standard code editing (available for backward compatibility)

**GPT-5.2 Model (NEW)**:
- Supports all reasoning effort levels: `low`, `medium`, `high`, `xhigh`
- Use for cutting-edge tasks requiring latest model capabilities
- Example: `codex exec -m gpt-5.2 -c model_reasoning_effort=xhigh "complex task"`

**Performance Characteristics**:
- `gpt-5.1-codex-max` is 27-42% faster than `gpt-5.1-codex`
- Uses ~30% fewer thinking tokens at the same reasoning effort level
- Supports new `xhigh` reasoning effort for maximum capability
- Requires Codex CLI 0.71.0+ and ChatGPT Plus/Pro/Business/Edu/Enterprise subscription

**Backward Compatibility**

You can override to use older models when needed:

```bash
# Use older gpt-5 model explicitly
codex exec -m gpt-5 -s read-only "Design a data structure"

# Use older gpt-5-codex model explicitly
codex exec -m gpt-5-codex -s workspace-write "Implement feature X"
```

**When to Override**

- **Testing compatibility**: Verify behavior matches older model versions
- **Specific model requirements**: Project requires specific model version
- **Model comparison**: Compare outputs between model versions

**Model Override Examples**

Override via `-m` flag:
```bash
# Override to gpt-5 for general task
codex exec -m gpt-5 "Explain algorithm complexity"

# Override to gpt-5-codex for code task
codex exec -m gpt-5-codex -s workspace-write "Refactor authentication"

# Override to gpt-4 if available
codex exec -m gpt-4 "Review this code"
```

**Default Behavior**

Without explicit `-m` override:
- All tasks → `gpt-5.2` (latest model, recommended default)
- General reasoning → `gpt-5.1` (if explicitly requested)
- Backward compatibility → `gpt-5.1-codex-max` and `gpt-5.1-codex` still work if explicitly specified

## Session Continuation

### Detecting Continuation Requests

When user indicates they want to continue a previous Codex conversation:
- Keywords: "continue", "resume", "keep going", "add to that"
- Follow-up context referencing previous Codex work
- Explicit request like "continue where we left off"

### Resuming Sessions

For continuation requests, use the `codex resume` command:

#### Resume Most Recent Session (Recommended)

```bash
codex exec resume --last
```

This automatically continues the most recent Codex session with all previous context maintained.

#### Resume Specific Session

```bash
codex exec resume <session-id>
```

Resume a specific session by providing its UUID. Get session IDs from previous Codex output or by running `codex exec resume --last` to see the most recent session.

**Note**: The interactive session picker (`codex resume` without arguments) is NOT available in non-interactive/Claude Code environments. Always use `--last` or provide explicit session ID.

### Decision Logic: New vs. Continue

**Use `codex exec -m ... "<prompt>"`** when:
- User makes a new, independent request
- No reference to previous Codex work
- User explicitly wants a "fresh" or "new" session

**Use `codex exec resume --last`** when:
- User indicates continuation ("continue", "resume", "add to that")
- Follow-up question building on previous Codex conversation
- Iterative development on same task

### Session History Management

- Codex CLI automatically saves session history
- No manual session ID tracking needed
- Sessions persist across Claude Code restarts
- Use `codex exec resume --last` to access most recent session
- Use `codex exec resume <session-id>` for specific sessions

## Error Handling

### Simple Error Response Strategy

When errors occur, return clear, actionable messages without complex diagnostics:

**Error Message Format:**
```
Error: [Clear description of what went wrong]

To fix: [Concrete remediation action]

[Optional: Specific command example]
```

### Common Errors

#### Command Not Found

```
Error: Codex CLI not found

To fix: Install Codex CLI and ensure it's available in your PATH

Check installation: codex --version
```

#### Authentication Required

```
Error: Not authenticated with Codex

To fix: Run 'codex login' to authenticate

After authentication, try your request again.
```

#### Invalid Configuration

```
Error: Invalid model specified

To fix:
- For coding tasks: Use 'gpt-5.2-codex' with workspace-write sandbox
- For reasoning tasks: Use 'gpt-5.2' with read-only sandbox

Example (coding): codex exec -m gpt-5.2-codex -s workspace-write -c model_reasoning_effort=xhigh "implement feature"
Example (reasoning): codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort=xhigh "explain architecture"
```

### Troubleshooting

**First Steps for Any Issues:**
1. Check Codex CLI built-in help: `codex --help`, `codex exec --help`, `codex exec resume --help`
2. Consult official documentation: [https://github.com/openai/codex/tree/main/docs](https://github.com/openai/codex/tree/main/docs)
3. Verify skill resources in `references/` directory

**Skill not being invoked?**
- Check that request matches trigger keywords (Codex, complex coding, high reasoning, etc.)
- Explicitly mention "Codex" in your request
- Try: "Use Codex to help me with..."

**Session not resuming?**
- Verify you have a previous Codex session (check command output for session IDs)
- Try: `codex exec resume --last` to resume most recent session
- If no history exists, start a new session first

**"stdout is not a terminal" error?**
- Always use `codex exec` instead of plain `codex` in Claude Code
- Claude Code's bash environment is non-interactive/non-terminal

**Errors during execution?**
- Codex CLI errors are passed through directly
- Check Codex CLI logs for detailed diagnostics
- Verify working directory permissions if using workspace-write
- Check official Codex docs for latest updates and known issues

## Examples

### Example 1: Code Task (Read-Only Default)

**User Request**: "Analyze this function implementation and suggest improvements"

**Skill Executes**:
```bash
codex exec -m gpt-5.2-codex -s read-only \
  -c model_reasoning_effort=xhigh \
  "Analyze this function implementation and suggest improvements"
```

**Result**: Code-related task uses gpt-5.2-codex with read-only sandbox (default). No file modifications.

---

### Example 2: General Task (Read-Only Default)

**User Request**: "Help me design a binary search tree architecture in Rust"

**Skill Executes**:
```bash
codex exec -m gpt-5.2 -s read-only \
  -c model_reasoning_effort=xhigh \
  "Help me design a binary search tree architecture in Rust"
```

**Result**: General task uses gpt-5.2 with read-only sandbox (default). Session automatically saved for continuation.

---

### Example 3: Code Task with Explicit Edit Request

**User Request**: "Edit this file to implement the BST insert method"

**Skill Executes**:
```bash
codex exec -m gpt-5.2-codex -s workspace-write \
  -c model_reasoning_effort=xhigh \
  "Edit this file to implement the BST insert method"
```

**Result**: User explicitly said "Edit this file" - code task uses gpt-5.2-codex with workspace-write permissions.

---

### Example 4: Session Continuation

**User Request**: "Continue with the BST - add a deletion method"

**Skill Executes**:
```bash
codex exec resume --last
```

**Result**: Codex resumes the previous BST session and continues with deletion method implementation, maintaining full context.

---

### Example 5: With Web Search (Read-Only Default)

**User Request**: "Use Codex with web search to research async patterns"

**Skill Executes**:
```bash
codex exec -m gpt-5.2-codex -s read-only \
  -c model_reasoning_effort=xhigh \
  --enable web_search_request \
  "Research async patterns"
```

**Result**: Code-related research uses gpt-5.2-codex with read-only sandbox (default) and web search enabled.

---

### Example 6: Explicit Refactoring Request

**User Request**: "Refactor and save the authentication system code"

**Skill Executes**:
```bash
codex exec -m gpt-5.2-codex -s workspace-write \
  -c model_reasoning_effort=xhigh \
  "Refactor and save the authentication system code"
```

**Result**: User explicitly said "Refactor and save" - code task uses gpt-5.2-codex with workspace-write for file modifications.

---

## Code Review Subcommand (v0.71.0+)

The `codex review` subcommand provides non-interactive code review capabilities:

```bash
# Review uncommitted changes (staged, unstaged, untracked)
codex review --uncommitted

# Review changes against a base branch
codex review --base main

# Review a specific commit
codex review --commit abc123

# Review with custom instructions
codex review --uncommitted "Focus on security vulnerabilities"

# Non-interactive via exec
codex exec review --uncommitted
```

**Review Options**:
| Flag | Description |
|------|-------------|
| `--uncommitted` | Review staged, unstaged, and untracked changes |
| `--base <BRANCH>` | Review changes against the given base branch |
| `--commit <SHA>` | Review the changes introduced by a commit |
| `--title <TITLE>` | Optional commit title for review summary |

---

## CLI Features Reference

### Feature Flags (`--enable` / `--disable`)
Enable or disable specific Codex features:
```bash
codex exec --enable web_search_request "Research latest patterns"
codex exec --disable some_feature "Run without feature"
```

### Image Attachment (`-i, --image`)
Attach images to prompts for visual analysis:
```bash
codex exec -i screenshot.png "Analyze this UI design"
codex exec -i diagram1.png -i diagram2.png "Compare these architectures"
```

### Additional Directories (`--add-dir`) (v0.71.0+)
Add writable directories beyond the primary workspace:
```bash
codex exec --add-dir /shared/libs --add-dir /config "task"
```

### Full Auto Mode (`--full-auto`)
Convenience flag for low-friction execution:
```bash
codex exec --full-auto "task"
# Equivalent to: -s workspace-write with on-request approval
```

### Non-Git Environments (`--skip-git-repo-check`)
Run Codex outside Git repositories:
```bash
codex exec --skip-git-repo-check "Help with this script"
```

### Structured Output (`--output-schema`)
Define JSON schema for model responses:
```bash
codex exec --output-schema schema.json "Generate structured data"
```

### Output Coloring (`--color`)
Control colored output (always, never, auto):
```bash
codex exec --color never "Run in CI/CD pipeline"
```

### Web Search in Exec Mode
**Note**: `--search` flag is interactive-only. Use `--enable` for exec mode:
```bash
# CORRECT for codex exec
codex exec --enable web_search_request "research topic"

# WRONG - --search only works in interactive mode
codex --search "research topic"
```

### Feature Flags (`codex features list`) (v0.71.0+)
Inspect and manage Codex feature flags:
```bash
# List all feature flags with their states
codex features list
```

**Current Feature Flags** (as of v0.71.0):

**Stable Features**:
| Feature | Default | Description |
|---------|---------|-------------|
| `web_search_request` | false | Enable web search capability |
| `parallel` | true | Parallel execution |
| `shell_tool` | true | Shell command execution |
| `undo` | true | Undo functionality |
| `view_image_tool` | true | Image viewing capability |
| `warnings` | true | Display warnings |

**Experimental/Beta Features**:
| Feature | Stage | Default | Description |
|---------|-------|---------|-------------|
| `exec_policy` | experimental | true | Execution policy control |
| `remote_compaction` | experimental | true | Remote compaction |
| `unified_exec` | experimental | false | Unified execution mode |
| `rmcp_client` | experimental | false | RMCP client support |
| `apply_patch_freeform` | beta | false | Freeform patch application |
| `skills` | experimental | false | Skills support |
| `shell_snapshot` | experimental | false | Shell state snapshots |
| `remote_models` | experimental | false | Remote model support |

Enable/disable features with `--enable` and `--disable`:
```bash
codex exec --enable web_search_request "research task"
codex exec --disable parallel "run sequentially"
```

### JSONL Output (`--json`) (v0.71.0+)
Stream events as JSONL for programmatic processing:
```bash
codex exec --json "task" > events.jsonl
```

### Save Last Message (`-o/--output-last-message`) (v0.71.0+)
Write the final agent message to a file:
```bash
codex exec -o result.txt "generate summary"
```

---

## When to Use GPT-5.2-Codex vs GPT-5.2

### GPT-5.2-Codex (for code-related tasks):
- Implementation, refactoring, code analysis
- Debugging, fixing bugs, optimization
- Any task involving code understanding

**Read-only (default)**:
```bash
codex exec -m gpt-5.2-codex -s read-only -c model_reasoning_effort=xhigh "analyze code"
```

**Workspace-write (only when user explicitly requests editing)**:
```bash
codex exec -m gpt-5.2-codex -s workspace-write -c model_reasoning_effort=xhigh "edit this file"
```

### GPT-5.2 (for general tasks):
- Architecture and system design
- Explanations, documentation, reviews
- Planning, strategy, general reasoning

**Read-only (default)**:
```bash
codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort=xhigh "design architecture"
```

**Workspace-write (only when user explicitly requests editing)**:
```bash
codex exec -m gpt-5.2 -s workspace-write -c model_reasoning_effort=xhigh "update the README"
```

---

## Fallback Models (Backward Compatibility)

### Use GPT-5.1-Codex-Max When:
- GPT-5.2-codex is unavailable
- Explicit requirement for the older codex model

### Use GPT-5.1 When:
- GPT-5.2 is unavailable
- Explicit requirement for the older general model

**Default**: Use `gpt-5.2-codex` for coding tasks and `gpt-5.2` for reasoning tasks. Fall back to GPT-5.1 variants only if primary models are unavailable.

## Best Practices

### 1. Use Descriptive Requests

**Good**: "Help me implement a thread-safe queue with priority support in Python"
**Vague**: "Code help"

Clear, specific requests get better results from high-reasoning models.

### 2. Indicate Continuation Clearly

**Good**: "Continue with that queue implementation - add unit tests"
**Unclear**: "Add tests" (might start new session)

Explicit continuation keywords help the skill choose the right command.

### 3. Specify Permissions When Needed

**Good**: "Refactor this code (allow file writing)"
**Risky**: Assuming permissions without specifying

Make your intent clear when you need workspace-write permissions.

### 4. Leverage High Reasoning

The skill defaults to high reasoning effort - perfect for:
- Complex algorithms
- Architecture design
- Performance optimization
- Security reviews

## Platform & Capabilities (v0.71.0)

### Windows Sandbox Support
Windows sandbox is available for filesystem and network access control.

### Interactive Mode Features
The `/exit` slash-command alias is available in interactive `codex` mode (not applicable to `codex exec` non-interactive mode used by this skill).

### Model Verbosity Override
All models (gpt-5.2, gpt-5.1-codex-max, gpt-5.1-codex) support verbosity override via `-c model_verbosity=<level>` for controlling output detail levels.

### Local/OSS Model Support
Use `--oss` with `--local-provider` to use local LLM providers:
```bash
codex exec --oss --local-provider ollama "task"
codex exec --oss --local-provider lmstudio "task"
```

## Pattern References

For command construction examples and workflow patterns, Claude can reference:
- `references/command-patterns.md` - Common codex exec usage patterns
- `references/session-workflows.md` - Session continuation and resume workflows
- `references/advanced-patterns.md` - Complex configuration and flag combinations

These files provide detailed examples for constructing valid codex exec commands for various scenarios.

## Additional Resources

For more details, see:
- `references/codex-help.md` - Codex CLI command reference
- `references/codex-config.md` - Full configuration options
- `README.md` - Installation and quick start guide
