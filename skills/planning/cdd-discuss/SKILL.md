---
name: cdd-discuss
description: 決断の議論・作成（タスク開始時、または継続議論）
allowed-tools: Read, Edit, Write, Bash(cdd:*), Glob, Grep
agent: general-purpose
---

# CDD Discussion Session

## Mode Detection

**If argument $1 is provided**: Discussion mode for existing decision
**If no argument**: New decision creation mode

---

## Mode 1: Existing Decision Discussion (when $1 is provided)

You are starting a discussion session for decision **$1**.

### Your Task

1. **Load the decision context:**
   - Read `CDD/**/*$1*.cdd.md` to find the decision file
   - If not found, search all CDD files using Grep tool

2. **Progressive Disclosure - Gather related context:**
   - Read documents referenced in the Context section
   - Search for related cdd.md files (use tags, keywords)
   - Read docs/README.md → docs/architecture/overview.md and relevant docs/research/ files
   - Build a complete picture before starting the discussion

3. **Verify current status:**
   - Check `decisionStatus` field
   - If already `DECIDED`, warn the user before proceeding

4. **Facilitate the discussion:**
   - Read the Goal, Context, and current Selection
   - Ask clarifying questions about unclear aspects
   - Propose alternatives or improvements
   - Help refine the Selection section

5. **Update the decision:**
   - When consensus is reached, update the cdd.md file
   - Change `decisionStatus` to appropriate value (DRAFT/REVIEW/DECIDED)
   - Update Selection section with discussion outcomes
   - Add discussion notes if needed

---

## Mode 2: New Decision Creation (when no argument)

You are starting a new decision creation session.

### Your Task

1. **Understand the requirement:**
   - Ask the user what they want to achieve
   - Ask clarifying questions to understand:
     - What problem they're solving
     - What constraints exist
     - What options they're considering

2. **Progressive Disclosure - Gather context automatically:**
   - Based on the user's description, search for related information:
     - Related cdd.md files (use Grep to search by keywords, tags, etc.)
     - Architecture documents (docs/README.md → docs/architecture/overview.md)
     - Technical research (docs/research/*.md)
   - Read the relevant documents
   - Add references to the Context section of the new cdd.md:
     ```markdown
     ## Context

     ### Related Decisions
     - PHASE4-001: CDD/tasks/xxx.cdd.md

     ### Technical Background
     - Architecture: docs/architecture/overview.md
     - Research: docs/research/investigation.md
     ```
   - Use this context to inform your discussion without asking redundant questions

3. **Determine the appropriate template:**
   - Based on the discussion, identify the best template type:
     - `feature`: New functionality
     - `bug`: Bug fix
     - `refactor`: Code refactoring
     - `decision`: Architectural or process decision
     - `research`: Investigation or analysis
   - Propose the template to the user and confirm

3. **Create the cdd.md file:**
   - Use the Bash tool to run: `cdd new --template <type>`
   - The command will prompt for:
     - Decision ID
     - Title
     - Assignee
   - Help the user fill in these fields based on your discussion

4. **Continue the discussion:**
   - Once the file is created, read it
   - Help the user fill in the sections:
     - Goal: What they want to achieve
     - Context: Background and constraints
     - Selection: Initial thoughts (if any)
   - Update the file using the Edit tool

5. **Set appropriate status:**
   - Start with `decisionStatus: DRAFT`
   - Only change to `REVIEW` or `DECIDED` when the user confirms

## Important Rules

- DO NOT implement code unless `decisionStatus: DECIDED`
- Focus on decision quality, not speed
- Challenge assumptions constructively
- Document rejected alternatives in Rejections section
