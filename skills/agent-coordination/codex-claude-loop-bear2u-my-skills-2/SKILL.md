---
name: codex-claude-loop
description: Orchestrates a dual-AI engineering loop where Claude Code plans and implements, while Codex validates and reviews, with continuous feedback for optimal code quality
---

# Codex-Claude Engineering Loop Skill

## Core Workflow Philosophy
This skill implements a balanced engineering loop:
- **Claude Code**: Architecture, planning, and execution
- **Codex**: Validation and code review
- **Continuous Review**: Each AI reviews the other's work
- **Context Handoff**: Always continue with whoever last cleaned up

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
   - Security concerns" | codex exec -m  --config model_reasoning_effort="" --sandbox read-only
```
3. Capture Codex's feedback

## Phase 3: Feedback Loop
If Codex finds issues:
1. Summarize Codex's concerns to the user
2. Refine the plan based on feedback
3. Ask user (via `AskUserQuestion`): "Should I revise the plan and re-validate, or proceed with fixes?"
4. Repeat Phase 2 if needed

## Phase 4: Execution
Once the plan is validated:
1. Claude implements the code using available tools (Edit, Write, Read, etc.)
2. Break down implementation into manageable steps
3. Execute each step carefully with proper error handling
4. Document what was implemented

## Phase 5: Cross-Review After Changes
After every change:
1. Send Claude's implementation to Codex for review:
   - Bug detection
   - Performance issues
   - Best practices validation
   - Security vulnerabilities
2. Claude analyzes Codex's feedback and decides:
   - Apply fixes immediately if issues are critical
   - Discuss with user if architectural changes needed
   - Document decisions made

## Phase 6: Iterative Improvement
1. After Codex review, Claude applies necessary fixes
2. For significant changes, send back to Codex for re-validation
3. Continue the loop until code quality standards are met
4. Use `codex exec resume --last` to continue validation sessions:
```bash
   echo "Review the updated implementation" | codex exec resume --last
```
   **Note**: Resume inherits all settings (model, reasoning, sandbox) from original session

## Recovery When Issues Are Found
When Codex identifies problems:
1. Claude analyzes the root cause
2. Implements fixes using available tools
3. Sends updated code back to Codex for verification
4. Repeats until validation passes

When implementation errors occur:
1. Claude reviews the error/issue
2. Adjusts implementation strategy
3. Re-validates with Codex before proceeding

## Best Practices
- **Always validate plans** before execution
- **Never skip cross-review** after changes
- **Maintain clear handoff** between AIs
- **Document who did what** for context
- **Use resume** to preserve session state

## Command Reference
| Phase | Command Pattern | Purpose |
|-------|----------------|---------|
| Validate plan | `echo "plan" \| codex exec --sandbox read-only` | Check logic before coding |
| Implement | Claude uses Edit/Write/Read tools | Claude implements the validated plan |
| Review code | `echo "review changes" \| codex exec --sandbox read-only` | Codex validates Claude's implementation |
| Continue review | `echo "next step" \| codex exec resume --last` | Continue validation session |
| Apply fixes | Claude uses Edit/Write tools | Claude fixes issues found by Codex |
| Re-validate | `echo "verify fixes" \| codex exec resume --last` | Codex re-checks after fixes |

## Error Handling
1. Stop on non-zero exit codes from Codex
2. Summarize Codex feedback and ask for direction via `AskUserQuestion`
3. Before implementing changes, confirm approach with user if:
   - Significant architectural changes needed
   - Multiple files will be affected
   - Breaking changes are required
4. When Codex warnings appear, Claude evaluates severity and decides next steps

## The Perfect Loop
```
Plan (Claude) → Validate Plan (Codex) → Feedback →
Implement (Claude) → Review Code (Codex) →
Fix Issues (Claude) → Re-validate (Codex) → Repeat until perfect
```

This creates a self-correcting, high-quality engineering system where:
- **Claude** handles all code implementation and modifications
- **Codex** provides validation, review, and quality assurance