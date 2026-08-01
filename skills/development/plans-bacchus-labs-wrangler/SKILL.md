---
name: plans-bacchus-labs-wrangler
description: '> For Claude: REQUIRED SUB-SKILL: Use /wrangler:implement to execute
  this plan task-by-task.'
---

# Unified Implement Skill - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use /wrangler:implement to execute this plan task-by-task.

**Goal:** Create unified `/wrangler:implement` skill that replaces both `executing-plans` and `subagent-driven-development` with autonomous, scope-agnostic implementation workflow.

**Architecture:** Slash command entry → Scope parser → Task executor with subagent dispatch → Automatic code review & fixes → Final verification → Completion options

**Tech Stack:**
- Markdown skill file (follows wrangler skill format)
- Slash command (`.md` file in `commands/`)
- Integration with existing skills (TDD, verification, code review, finishing-branch)
- MCP tools for issue loading (issues_get, issues_list)

**Implementation tracking:** See MCP issues (project: implement-skill-unification)

---

## Architecture Overview

### Core Components

1. **Scope Parser**
   - Input: User command string or conversation context
   - Formats: spec files, plan files, issue IDs/ranges, context inference
   - Output: Normalized task list

2. **Task Executor**
   - Dispatches general-purpose subagent per task
   - Enforces TDD via subagent prompt
   - Collects TDD compliance certification
   - Manages task dependencies

3. **Code Review Automation**
   - Auto-dispatch code-reviewer subagent after each task
   - Parse review feedback (Critical/Important/Minor)
   - Auto-dispatch fix subagents for issues
   - Retry logic with escalation (2 attempts max)

4. **Blocker Detection**
   - Unclear requirements → immediate escalation
   - Fix failures (2x) → escalation with "flummoxed" signal
   - Missing dependencies → escalation
   - Test failures after fixes → escalation

5. **Verification & Completion**
   - Final test suite run
   - Requirements checklist verification
   - TDD compliance aggregation
   - Integration with finishing-a-development-branch skill

### Scope Format Handling

| Input Format | Example | Parsing Strategy |
|--------------|---------|------------------|
| Spec file | `spec-auth.md` | Load from `.wrangler/specifications/`, extract linked issues or parse inline tasks |
| Plan file | `plan-refactor.md` | Load from `plans/`, extract task list |
| Single issue | `issue #42` or `issue 42` | Load via MCP issues_get |
| Issue range | `issues 5-7` or `issues 5,6,7` | Load via MCP issues_list with filtering |
| Context inference | (none) | Scan last 5 user messages for file/issue references |

### Autonomous Execution Model

**Key principle:** No user checkpoints unless genuinely blocked

**Stops only for:**
- Unclear requirements (cannot infer intent)
- Flummoxed agents (2 fix failures on same issue)
- Missing dependencies (cannot proceed)
- Explicit user intervention requests

**Does NOT stop for:**
- Test failures (auto-fixes via subagent)
- Code review feedback (auto-fixes Critical/Important)
- Task completion (continues to next task automatically)
- Batch boundaries (no artificial checkpoints)

### Integration Points

**Required sub-skills:**
- `test-driven-development` - Subagents MUST follow TDD
- `verification-before-completion` - Final verification
- `requesting-code-review` - Code review template
- `finishing-a-development-branch` - Completion options

**MCP tools:**
- `issues_get` - Load single issue
- `issues_list` - Load issue ranges
- `issues_update` - Optional: mark complete

**Replaces:**
- `executing-plans` (hard deprecation - delete file)
- `subagent-driven-development` (hard deprecation - delete file)

---

## Task Breakdown Summary

1. **Create implement skill foundation** - Skill file, frontmatter, overview, scope parser
2. **Add task executor workflow** - Subagent dispatch, TDD enforcement, dependency handling
3. **Add code review automation** - Auto-review, feedback parsing, fix dispatch, retry logic
4. **Add blocker detection** - Escalation conditions, flummoxed detection
5. **Add verification & completion** - Final checks, TDD aggregation, finishing-branch integration
6. **Create slash command** - `/wrangler:implement` entry point
7. **Add examples & documentation** - Usage examples, red flags, integration notes
8. **Delete deprecated skills** - Remove executing-plans and subagent-driven-development
9. **Update references** - Fix any skills referencing deprecated skills
10. **Verification & testing** - Test with various scope formats, verify autonomous behavior

---

## Design Decisions

### Why Slash Command Entry?

- **Discoverability:** Users can find it via `/wrangler:` prefix
- **Explicit invocation:** Clear when autonomous mode activates
- **Clean syntax:** No confusion about skill vs manual execution

### Why Auto-Fix Instead of Stop-and-Ask?

- **Efficiency:** Most code review issues are straightforward fixes
- **Maintains flow:** Stopping after every task breaks momentum
- **Safety net:** 2-attempt limit prevents infinite loops
- **Escalation path:** User gets involved when truly needed

### Why Merge Two Skills?

- **Single mental model:** One skill for all implementation
- **Eliminates choice paralysis:** No "which skill?" questions
- **Simplifies maintenance:** One workflow to update
- **Reduces duplication:** Both skills had 80% overlap

### Why Hard Deprecation?

- **Clean break:** No confusion about which to use
- **Prevents regressions:** Can't accidentally use old workflow
- **Forces migration:** Ensures everyone benefits from improvements
- **Simpler codebase:** Less code to maintain

---

## Success Criteria

- [ ] `/wrangler:implement` command exists and loads skill
- [ ] Skill handles all scope formats (spec, plan, issue, range, context)
- [ ] Subagents dispatched per task with TDD enforcement
- [ ] Code review automatic after each task
- [ ] Auto-fix for Critical/Important issues (max 2 attempts)
- [ ] Escalates to user only for genuine blockers
- [ ] Final verification runs before completion
- [ ] Integrates with finishing-a-development-branch
- [ ] executing-plans deleted
- [ ] subagent-driven-development deleted
- [ ] All references updated
- [ ] Tested with various scenarios
