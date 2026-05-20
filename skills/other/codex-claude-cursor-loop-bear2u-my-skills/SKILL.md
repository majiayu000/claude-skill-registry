---
name: codex-claude-cursor-loop
description: Orchestrates a triple-AI engineering loop where Claude plans, Codex validates logic and reviews code, and Cursor implements, with continuous feedback for optimal code quality
---

# Codex-Claude-Cursor Engineering Loop Skill

## Core Workflow Philosophy
This skill implements a 3-way sequential validation engineering loop:
- **Claude Code**: Architecture and planning, final review
- **Codex**: Plan validation (logic/security), code review (bugs/performance)
- **Cursor Agent**: Code implementation and execution
- **Sequential Validation**: Claude plans → Codex validates → Cursor implements → Codex reviews → Claude final check → repeat

## Phase 1: Planning with Claude Code
1. Start by creating a detailed plan for the task
2. Break down the implementation into clear steps
3. Document assumptions and potential issues
4. Output the plan in a structured format

## Phase 2: Plan Validation with Codex
1. Ask user (via `AskUserQuestion`):
   - Model: `gpt-5` or `gpt-5-codex`
   - Reasoning effort: `low`, `medium`, or `high`
2. Send the plan to Codex for validation:
```bash
   echo "Review this implementation plan and identify any issues:
   [Claude's plan here]

   Check for:
   - Logic errors
   - Missing edge cases
   - Architecture flaws
   - Security concerns" | codex exec -m <model> --config model_reasoning_effort="<effort>" --sandbox read-only
```
3. Capture Codex's feedback and summarize to user

## Phase 3: Plan Refinement Loop
If Codex finds issues in the plan:
1. Summarize Codex's concerns to the user
2. Refine the plan based on feedback
3. Ask user (via `AskUserQuestion`): "Should I revise the plan and re-validate, or proceed with implementation?"
4. Repeat Phase 2 if needed until plan is solid

## Phase 4: Implementation with Cursor Agent
Once the plan is validated by Codex:

### Session Management
1. Ask user (via `AskUserQuestion`): "Do you want to start a new Cursor session or resume an existing one?"
   - **New session**: Start fresh
   - **Resume session**: Continue previous work

2. If resuming:
```bash
   # Note: cursor-agent ls requires interactive mode and may not work in --print mode
   # Alternative: Ask user for chat ID from their previous session
   # Or use: cursor-agent resume (resumes latest session without ID)

   # Store session ID for subsequent calls
```

3. Ask user (via `AskUserQuestion`): Which Cursor model to use
   - Available models: `sonnet-4`, `sonnet-4-thinking`, `gpt-5`, `gpt-4o`, `composer-1`
   - Recommended: `sonnet-4` for balanced performance, `sonnet-4-thinking` for complex reasoning

### Implementation
4. Send the validated plan to Cursor Agent:

**For new session:**
```bash
   cursor-agent --model "<model-name>" -p --force --output-format json --approve-mcps "Implement this plan:
   [Validated plan here]

   Please implement the code following these specifications exactly."
```

**For resumed session (with chat ID):**
```bash
   cursor-agent --resume <chat-id> --model "<model-name>" -p --force --output-format json "Continue implementation:
   [Validated plan here]"
```

**For resumed session (latest chat):**
```bash
   cursor-agent resume --model "<model-name>" -p --force --output-format json "Continue implementation:
   [Validated plan here]"
```

**Useful options:**
- `--output-format json`: Structured output for parsing (recommended for automation)
- `--approve-mcps`: Auto-approve MCP servers (useful in headless mode)
- `--stream-partial-output`: Real-time progress monitoring (use with --output-format stream-json)
- `--browser`: Enable browser automation if needed

5. **IMPORTANT**: Store the session ID from the output for all subsequent Cursor calls
6. Capture what was implemented and which files were modified

## Phase 5: Codex Code Review
After Cursor implements:
1. Send Cursor's implementation to Codex for code review:
```bash
   echo "Review this implementation for:
   - Bugs and logic errors
   - Performance issues
   - Security vulnerabilities
   - Best practices violations
   - Code quality concerns

   Files modified: [list of files]
   Implementation summary: [what Cursor did]" | codex exec --sandbox read-only
```
2. Capture Codex's code review feedback
3. Summarize findings to user

## Phase 6: Claude's Final Review
After Codex code review:
1. Claude reads the implemented code using Read tool
2. Claude analyzes both:
   - Codex's review findings
   - The actual implementation
3. Claude provides final assessment:
   - Verify if it matches the original plan
   - Confirm Codex's findings are valid
   - Identify any additional concerns
   - Make final architectural decisions
4. Summarize overall quality and readiness

## Phase 7: Iterative Improvement Loop
If issues are found (by Codex or Claude):
1. Claude creates a detailed fix plan based on:
   - Codex's code review findings
   - Claude's final review insights
2. Send the fix plan to Cursor Agent using the **same session**:
```bash
   # IMPORTANT: Use --resume with the stored session ID
   cursor-agent --resume <chat-id> --model "<model-name>" -p --force --output-format json "Fix these issues:
   [Detailed fix plan]

   Issues from Codex: [list]
   Issues from Claude: [list]"

   # Or resume latest session:
   cursor-agent resume --model "<model-name>" -p --force --output-format json "Fix these issues..."
```
3. After Cursor fixes, repeat from Phase 5 (Codex code review)
4. Continue the loop until all validations pass
5. **Note**:
   - Use same Codex model for consistency
   - Always use the same Cursor session ID to maintain context
   - Session maintains full history of changes

## Recovery When Issues Are Found

### When Codex finds plan issues (Phase 2):
1. Claude analyzes Codex's concerns
2. Refines the plan addressing all issues
3. Re-submits to Codex for validation
4. Repeats until Codex approves

### When Codex finds code issues (Phase 5):
1. Claude reviews Codex's findings
2. Creates detailed fix plan
3. Sends to Cursor for fixes
4. After Cursor fixes, back to Codex review
5. Repeats until Codex approves

### When Claude finds issues (Phase 6):
1. Claude creates comprehensive fix plan
2. Sends to Cursor for implementation
3. After fixes, Codex reviews again
4. Claude does final check
5. Repeats until Claude approves

## Best Practices
- **Always validate plans with Codex** before implementation
- **Never skip Codex code review** after Cursor implements
- **Never skip Claude's final review** for architectural oversight
- **Maintain clear handoff** between all three AIs
- **Document who did what** for context
- **Use same models** throughout (same Codex model, same Cursor model)
- **Session Management**:
  - Always use `--resume <chat-id>` with same session ID for iterative fixes
  - Store session ID at the start and reuse throughout
  - Use `cursor-agent resume` to resume latest session (no ID needed)
  - Note: `cursor-agent ls` requires interactive mode (may not work in scripts)
  - Only start new session when beginning completely new feature
- **Output Format**:
  - Use `--output-format json` for structured, parseable output
  - Use `--stream-partial-output` with `stream-json` for real-time progress
  - Helps with error detection and progress monitoring

## Command Reference
| Phase | Who | Command Pattern | Purpose |
|-------|-----|----------------|---------|
| 1. Plan | Claude | TodoWrite, Read, analysis tools | Claude creates detailed plan |
| 2. Validate plan | Codex | `echo "plan" \| codex exec -m <model> --config model_reasoning_effort="<effort>" --sandbox read-only` | Codex validates logic/security |
| 3. Refine | Claude | Analyze Codex feedback, update plan | Claude fixes plan issues |
| 4. Session setup | Claude + User | Ask new/resume, ask for chat ID if resuming | Setup or resume Cursor session |
| 5. Implement | Cursor | **New**: `cursor-agent --model "<model>" -p --force --output-format json --approve-mcps "prompt"` <br> **Resume**: `cursor-agent --resume <chat-id> --model "<model>" -p --force --output-format json "prompt"` <br> **Latest**: `cursor-agent resume -p --force --output-format json "prompt"` | Cursor implements validated plan |
| 6. Review code | Codex | `echo "review" \| codex exec --sandbox read-only` | Codex reviews for bugs/performance |
| 7. Final review | Claude | Read tool, analysis | Claude final architectural check |
| 8. Fix plan | Claude | Create detailed fix plan | Claude plans fixes from all feedback |
| 9. Apply fixes | Cursor | `cursor-agent --resume <chat-id> --model "<model>" -p --force --output-format json "fixes"` OR `cursor-agent resume -p --force --output-format json "fixes"` | Cursor implements fixes in same session |
| 10. Re-review | Codex + Claude | Repeat phases 6-7 | Validate fixes until perfect |

## Advanced Cursor Agent Features

### Available Command-Line Options
- `--model <model>`: Choose AI model (sonnet-4, sonnet-4-thinking, gpt-5, gpt-4o, composer-1)
- `-p, --print`: Print mode for scripts (headless, non-interactive)
- `-f, --force`: Auto-approve commands unless explicitly denied
- `--output-format <format>`: Output format (text | json | stream-json)
- `--stream-partial-output`: Stream partial output as deltas (with stream-json)
- `--approve-mcps`: Auto-approve all MCP servers (headless mode only)
- `--browser`: Enable browser automation support
- `--resume [chatId]`: Resume specific chat or latest if no ID provided

### Session Management Commands
- `cursor-agent create-chat`: Create new empty chat and return ID
- `cursor-agent resume`: Resume latest chat session (no ID needed)
- `cursor-agent --resume <chat-id>`: Resume specific chat by ID
- `cursor-agent ls`: List sessions (requires interactive mode, not for scripts)

### Model Recommendations
- **sonnet-4**: Best balance of speed and quality (recommended default)
- **sonnet-4-thinking**: Deep reasoning for complex architectural decisions
- **gpt-5**: Latest OpenAI model with strong coding capabilities
- **gpt-4o**: Fast responses, good for iterative fixes
- **composer-1**: Cursor's native composer model

### Output Format Strategies
1. **For automation/scripts**: `--output-format json`
   - Structured, parseable output
   - Easy error detection
   - Better for Claude to process results

2. **For real-time monitoring**: `--output-format stream-json --stream-partial-output`
   - See progress as it happens
   - Detect issues early
   - Cancel if going wrong direction

3. **For human review**: `--output-format text` (default)
   - Readable format
   - Good for debugging

## Error Handling
1. Monitor Cursor Agent output for errors (easier with JSON output)
2. Summarize Cursor's implementation results and Claude's review
3. Ask for user direction via `AskUserQuestion` if:
   - Significant architectural changes needed
   - Multiple files will be affected
   - Breaking changes are required
4. When issues appear, Claude creates a detailed fix plan before sending to Cursor
5. **JSON parsing**: When using `--output-format json`, parse the output to extract:
   - Files modified
   - Commands executed
   - Error messages
   - Session ID for resume

## The Perfect Loop
```
1. Plan (Claude)
   ↓
2. Validate Plan (Codex) → if issues → refine plan → repeat
   ↓
3. Implement (Cursor)
   ↓
4. Code Review (Codex) → captures bugs/performance issues
   ↓
5. Final Review (Claude) → architectural check
   ↓
6. Issues found? → Fix Plan (Claude) → Implement Fixes (Cursor) → back to step 4
   ↓
7. All passed? → Done! ✅
```

This creates a triple-validation, self-correcting, high-quality engineering system where:
- **Claude**: All planning, architecture, and final oversight
- **Codex**: All validation (plan logic + code quality)
- **Cursor Agent**: All implementation and coding