---
name: step-by-step
description: Execute a task one atomic step at a time, requiring approval for each.
argument-hint: [task_description]
tools: Read, Write, Edit, Bash, AskUserQuestion
---

You will execute the task: "$ARGUMENTS"

**CRITICAL RULES:**
1. Execute ONLY ONE step at a time
2. **MANDATORY:** Use `AskUserQuestion` tool for ALL user interactions
3. NEVER proceed without explicit user approval via `AskUserQuestion`

# Mandatory Tool Usage

**You MUST use `AskUserQuestion` for:**
- Plan approval: "Approve this plan? (Yes/No/Modify)"
- Step continuation: "Continue to Step N? (Yes/No/Skip)"
- Clarifying questions: "Which technology? (React/Vue/Angular)"
- Error recovery: "Retry/Skip/Abort?"

**DO NOT use plain text questions.** Always invoke `AskUserQuestion` tool.

# Optional Agent Collaboration

Depending on the task, you may need:
- `@backend-architect` - For backend implementation
- `@frontend-architect` - For UI implementation
- `@mobile-architect` - For mobile implementation

# Workflow

1.  **Parse Task:** Understand "$ARGUMENTS"
   - If empty: Error (see error handling)

2.  **Create Plan:** Break task into 3-7 atomic steps
   - Show full plan to user
   - **USE `AskUserQuestion`:** "Approve this plan? (Yes/No/Modify)"

3.  **Execute Step 1:**
   - Show: "📍 Step 1/N: [Description]"
   - Perform the action (create file, edit code, etc.)
   - Show: "✅ Step 1 completed: [What was done]"

4.  **Ask for Approval:**
   - **USE `AskUserQuestion`:** "Continue to Step 2? (Yes/No/Skip)"
   - If No: Stop and exit
   - If Skip: Move to Step 3

5.  **Repeat for Each Step**

6.  **Final Summary:**
   - Show all completed steps
   - Suggest next action (e.g., "Run /polish to clean up")

# Step Planning Guidelines

**Good Steps (Atomic):**
- ✅ "Create user model in database schema"
- ✅ "Add API endpoint GET /users/:id"
- ✅ "Create UserProfile component"

**Bad Steps (Too broad):**
- ❌ "Implement the entire user system"
- ❌ "Build the frontend"

# Example Flow

```
User: /step-by-step "Implement the login page"

Assistant:
📋 Task Plan:
1. Create Login.tsx component with email/password form
2. Add form validation (email format, password length)
3. Create POST /auth/login API endpoint
4. Connect frontend form to API
5. Add error handling and loading states
6. Add "Forgot Password?" link

Approve this plan? (Yes/No/Modify)

User: Yes

Assistant:
📍 Step 1/6: Create Login.tsx component with email/password form

[Creates file with code]

✅ Step 1 completed: Created src/components/Login.tsx with form structure

Continue to Step 2? (Yes/No/Skip)
```

# Error Handling

**If $ARGUMENTS is empty:**
- Error: "❌ No task provided. Usage: /step-by-step [task description]"
- Example: `/step-by-step "Add user authentication"`

**If task is too vague:**
- **USE `AskUserQuestion`:** Ask clarifying questions first
- "What technology should I use? (React/Vue/etc.)"
- "Should this be frontend or backend?"

**If step fails (e.g., file creation error):**
- Report error with details
- **USE `AskUserQuestion`:** "Retry this step? (Yes/Skip/Abort)"
- If Abort: Stop execution and summarize what was completed

**If user says "No" to continue:**
- Summarize completed steps
- **USE `AskUserQuestion`:** "Would you like to resume later or abort?"
- Save progress context if possible

**If step limit exceeded (>20 steps):**
- Warn: "⚠️ This task has >20 steps. Consider breaking it into smaller tasks."
- Ask: "Continue anyway or split the task?"

# Success Criteria

- [ ] Task broken into clear atomic steps
- [ ] Each step executed only after approval
- [ ] Progress visible at each stage
- [ ] Final summary provided
- [ ] User knows what to do next
