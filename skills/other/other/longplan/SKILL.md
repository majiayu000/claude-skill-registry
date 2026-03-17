---
description: Autonomous multi-step work with dual-reviewer supervision (1A2A workflow)
argument-hint: <task_description>
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash, TodoWrite, Skill, AskUserQuestion]
model: sonnet
---

# Long-Form Autonomous Planning (1A2A Workflow)

**Task:** `$ARGUMENTS`

## 1A Phase: Ask & Plan

You are in the **Ask Phase** - gather information and create a detailed plan before autonomous execution.

Spawn parallel sub-tasks using specialized agents:

```
Research Tasks:
- codebase-locator: Find all files related to the feature area
- codebase-analyzer: Understand existing patterns and architecture
- Explore: Investigate integration points and dependencies
```

For each research task, provide:
- Specific directories to examine
- Exact patterns or code to find
- Required output: file:line references


### Step 1: Understand the Task
- Use Glob/Grep/Read to explore relevant codebase areas
- Identify files that will be modified
- Understand existing patterns

### Step 2: Ask Clarifying Questions
Use AskUserQuestion to cover:
- Implementation scope and boundaries
- File modification permissions
- Testing requirements
- Phase priorities
- Any constraints or preferences

### Step 3: Create TodoWrite Plan
```javascript
TodoWrite(todos=[
  {content: "Task 1", status: "pending", activeForm: "Doing Task 1"},
  {content: "Task 2", status: "pending", activeForm: "Doing Task 2"},
  // ... more tasks
])
```

### Step 4: Sanity Check with MiniMax Reviewer

Before finalizing your plan, get external perspective:

```powershell
# Invoke MiniMax reviewer as "devil's advocate"
powershell -File .claude/skills/minimax-mcp/scripts/review-work.ps1 -Context "Plan summary" -Question "What risks or blind spots should I consider?"
```

**What to ask MiniMax:**
- "What's missing from this plan?"
- "What could go wrong that I haven't considered?"
- "Are there better approaches for [specific aspect]?"
- "What documentation should I reference?"

**Remember:** Use the feedback autonomously to strengthen your plan. MiniMax is advisory, not authoritative.

### Step 5: Create Self-Contained Plan File

For long autonomous sessions (30+ minutes), create a persistent .md file with:

**REQUIRED SECTIONS:**

1. **🚫 Common Pitfalls** - Anti-patterns to avoid
   - Table format: "Don't do X → Instead do Y"
   - Task-specific mistakes agents commonly make

2. **📚 Quick Reference Links** - Essential docs for this task
   - List: roadmaps, instructions, troubleshooting guides
   - Brief one-line description of each

3. **⚠️ Troubleshooting** - When things don't work
   - Table: Symptom → Check → Fix
   - Common failures and their solutions

4. **🔄 Reminders** - Keep these in mind throughout
   - "Remember to reference [doc] after every N tasks"
   - "Use [skill] when [situation] occurs"
   - Gentle guidance for autonomous execution

**Key phrasing for 2A autonomous work:**
- "Remember to reference X" (not "check X")
- "Keep in mind to use Y" (not "verify Y")
- "Use Z for W" (clear autonomous action)
- Avoid: "ask", "check", "verify" (can trigger stops)

### Step 6: Present Plan for Approval
Before proceeding, summarize:
- What will be done
- What files will be modified
- What the user should expect
- Any concerns raised by MiniMax review (and how you addressed them)

**WAIT for user to say "START 2A" before proceeding to autonomous phase.**

---

## Scope Guardrails (Finish Game Requests)

When the user says "finish the game" or "finish the roadmap":

- Default to **full local beta scope**, not a partial pass.
- Include **explicit success criteria** (intro stability, quest flow to ending, basic HPV, key visuals, tests).
- Do **not** narrow scope unless the user explicitly approves the reduction.
- Plan should cover **multiple phases** and be marked as multi-session if needed.
- If you must break into blocks, note that the **overall goal remains unchanged** and continue into the next block without waiting for re-approval unless a HARD STOP applies.

---

## 2A Phase: Autonomous Execution

**User has approved.** You are now in **Autonomous Phase** - work through the todo list independently without stopping to ask questions.

**CRITICAL:** During 2A, work continuously. Do NOT stop for:
- Clarification questions (make reasonable assumptions)
- "Should I do X?" (use your best judgment)
- "Is this correct?" (proceed with confidence)

**HARD STOPS still apply:** Creating .md files, git push, editing CONSTITUTION.md, actions outside scope.

### Work Guidelines

**DO autonomously:**
- Complete all todo items systematically
- Handle blockers by continuing with other items
- Use skills before manual implementation
- Run tests when appropriate
- Commit changes when work blocks complete

**HARD STOPS (always ask, even in 2A):**
- Creating NEW .md files (not edits)
- Editing `.cursor/` directory
- Git push, force push, branch operations
- Editing CONSTITUTION.md
- Actions outside approved scope

### When Blocked

1. Note the blocker
2. Continue with other todo items
3. Summarize blockers at end
4. Don't get stuck - move forward

---

## Tracking with TodoWrite

All `/longplan` sessions use **TodoWrite** for progress tracking.

**Why TodoWrite:**
- Integrated with CLI `/todos` command for visibility
- Progress updated in real-time as you work
- No extra files cluttering the repo
- Automatically cleaned up after session ends

**Session Persistence (.md file):**
- `/longplan` creates an `.md` file ONLY when session persistence is needed
- Use when: terminal may close, work spans multiple sessions, user is away
- Format: `temp/autonomous-work-[task-name].md` or similar
- Shorter planning (via create-plan skill) uses TodoWrite only (no .md file needed)

**Tracking Best Practices:**
- Update todo status immediately when starting/finishing tasks
- Use `activeForm` to describe current action
- Mark blockers in notes, don't stop working
- Create .md file only if session may be interrupted

---

## Dual-Reviewer System

Use BOTH reviewers during 2A phase for quality control:

### GLM Devil's Advocate (Self-Review)

**When to use:**
- Before making significant changes
- After completing multi-step tasks
- When uncertain about approach

**How to invoke:**
Read `temp/glm-devils-advocate-prompt.md` and respond as the critical reviewer.

**Output format:**
```
### 🔍 Critical Review
**Concerns:** [list]
**Edge Cases Missed:** [list]
**Alternatives Not Considered:** [list]
**Recommendation:** PROCEED / REVISE / RECONSIDER
```

### MiniMax Reviewer (External Standards)

**When to use:**
- Checking against documentation standards
- Looking for precedents in trusted docs
- Verifying alignment with best practices

**How to invoke:**
```bash
powershell -File .claude/skills/minimax-mcp/scripts/review-work.ps1 -Context "what I did" -Question "question?"
```

**Output:** Retrieves relevant documentation from trusted domains (docs.anthropic.com, godotengine.org, etc.)

### Reviewer Strategy

| Reviewer | Use For | Frequency |
|----------|---------|-----------|
| GLM Devil's Advocate | Architecture, file changes, bug fixes | Before significant changes |
| MiniMax | Documentation standards, precedents | When uncertain about standards |

**Remember:** Reviewers are ADVISORS. Use judgment in applying feedback. Don't blindly follow - they're your "devil on your shoulder."

---

## Completion

When all todos complete:

1. **Summarize work done**
2. **List any blockers encountered**
3. **Show files modified**
4. **Ask if any follow-up needed**

---

## Example Flow

```
User: /longplan Fix the quest 4 dialogue bug

Agent: [1A Phase]
- Reads quest 4 dialogue files
- Asks: "Should I also check related quest files?"
- Creates TodoWrite plan
- Presents plan for approval
- WAITS...

User: START 2A

Agent: [2A Phase]
- Works through todos
- Uses GLM reviewer before major changes
- Uses MiniMax reviewer to check standards
- Completes work
- Summarizes results
```

---

**Signature:** `[GLM-4.7 - 2026-01-20]`
