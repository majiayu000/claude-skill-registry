---
name: orca-confirm
description: Handle team confirmation with automatic bypass mode detection for /orca
---

# Orca Team Confirmation Skill

**Purpose:** Handle user confirmation for agent team selection with automatic bypass mode detection.

**Input:** User's request is implicitly available. You receive the proposed team and project type as arguments.

---

## Critical Rules (Read First)

1. **Ask for confirmation ONCE using AskUserQuestion**
2. **Check response structure immediately after receiving it**
3. **If response.answers is empty → BYPASS MODE → Return immediately**
4. **NEVER retry AskUserQuestion if first attempt returned blank**
5. **Return a structured result that main /orca can parse**

---

## Implementation

### Step 1: Present Proposed Team (VISIBLE OUTPUT - NOT IN TOOL CALL)

**CRITICAL: This must be VISIBLE MARKDOWN OUTPUT, not inside AskUserQuestion.**

Output this as regular text so the user can see it:

```markdown
## Proposed Pipeline

**Request:** [task description]
**Domain:** [PROJECT_TYPE]
**Complexity:** [simple/medium/complex]

### Agent Team
| Role | Agent |
|------|-------|
| Coordination | [grand-architect] |
| Architecture | [architect] |
| Implementation | [builder] |
| Specialists | [list them] |
| Gates | [gate agents] |
| Verification | [verification agent] |

### Files Likely Affected
- [from ContextBundle]

### Risks/Notes
- [any identified]
```

**This output MUST appear BEFORE you call AskUserQuestion.**

### Step 2: Ask for Confirmation (ONCE ONLY - SIMPLE QUESTION)

Use AskUserQuestion with these exact options:

```
Question: "Proceed with this team?"
Options:
1. "Yes, proceed" → Proceed with proposed team
2. "Modify team" → Ask user what to change
```

### Step 3: Check Response Structure

**Immediately after AskUserQuestion returns, check the response:**

```python
# Pseudo-code for what you MUST check:
if response is None or response.get("answers") is None or len(response.get("answers", {})) == 0:
    # BYPASS MODE DETECTED
    # User has bypass permissions enabled
    # They CANNOT respond to questions
    # Proceed immediately with proposed team

    Output:
    " Proceeding with proposed team (bypass mode detected - confirmation unavailable)

    Proposed Team: [list team]

    You can interrupt if you need changes."

    # Return to /orca with: BYPASS|original_team

else:
    # INTERACTIVE MODE
    # User provided an answer
    user_answer = response["answers"][first_question_key]

    if user_answer == "Yes, proceed":
        Output: " Team confirmed"
        # Return to /orca with: CONFIRMED|original_team

    elif user_answer == "Modify team":
        # Ask user what to change
        # Adjust team based on their input
        # Return to /orca with: MODIFIED|new_team_list
```

### Step 4: Return Result to /orca

**Format:** `STATUS|agent1,agent2,agent3`

**Valid statuses:**
- `BYPASS` - Bypass mode detected, proceeding with proposed team
- `CONFIRMED` - User confirmed proposed team
- `MODIFIED` - User requested changes, new team provided

**Examples:**
```
BYPASS|swiftui-developer,swiftdata-specialist,swift-testing-specialist
CONFIRMED|design-reviewer,accessibility-specialist,ui-engineer
MODIFIED|nextjs-14-specialist,tailwind-specialist,design-reviewer
```

---

## Output Format

Your final output must be:

```
[Status message to user explaining what happened]

RESULT: STATUS|agent,list,here
```

**The RESULT line is what /orca will parse.**

---

## Examples

### Example 1: Bypass Mode (Blank Response)

**Input:** Proposed team for iOS project
**AskUserQuestion returns:** `{"answers": {}}`
**Output:**
```
 Proceeding with proposed team (bypass mode detected - confirmation unavailable)

Proposed Team:
• swiftui-developer
• swiftdata-specialist
• swift-testing-specialist

You can interrupt if you need changes.

RESULT: BYPASS|swiftui-developer,swiftdata-specialist,swift-testing-specialist
```

### Example 2: User Confirms

**Input:** Proposed team for Next.js project
**AskUserQuestion returns:** `{"answers": {"q1": "Yes, proceed"}}`
**Output:**
```
 Team confirmed by user

Proceeding with:
• nextjs-14-specialist
• tailwind-specialist
• design-reviewer

RESULT: CONFIRMED|nextjs-14-specialist,tailwind-specialist,design-reviewer
```

### Example 3: User Modifies

**Input:** Proposed team for backend project
**User says:** "Remove quality-validator, add test-engineer"
**Output:**
```
 Team modified per user request

Original: backend-engineer, quality-validator
Modified: backend-engineer, test-engineer

RESULT: MODIFIED|backend-engineer,test-engineer
```

---

## Testing Checklist

Before returning results, verify:

-  Asked AskUserQuestion exactly ONCE
-  Checked response.answers structure explicitly
-  Returned RESULT line in correct format
-  Did NOT retry on blank response
-  Showed clear message to user about what's happening

---

## Common Mistakes to Avoid

 **DON'T:**
```
"I didn't receive a response, let me ask again..."
[Retries AskUserQuestion]
```

 **DO:**
```
" Proceeding with proposed team (bypass mode detected)"
RESULT: BYPASS|team,list
```

 **DON'T:**
```
# Unclear what happened
RESULT: team,list
```

 **DO:**
```
# Clear status prefix
RESULT: BYPASS|team,list
```

---

**This skill exists to solve one problem: Stop retrying when bypass mode is enabled.**

**It works by encapsulating the confirmation logic and enforcing single-attempt behavior.**
