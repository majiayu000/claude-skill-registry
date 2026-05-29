---
name: increment-work-router
description: Smart work continuation system that detects implementation intent and routes to active increment or creates new one. Activates for implement, complete, build, add, develop, work on, continue, resume, finish, fix, resolve, address, let's implement, let's build, start working, begin implementation, add feature, create feature.
---

# Increment Work Router - Smart Work Continuation

## Purpose

The increment-work-router skill is an **intelligent work continuation system** that:
- ✅ Detects implementation/continuation intent (not just new projects)
- ✅ Checks for active increments automatically
- ✅ Routes to existing increment OR creates new one
- ✅ Bridges the gap between planning and execution

**Key Insight**: When user says "implement X" or "complete Y", they expect the system to handle routing intelligently without manual commands.

## When to Activate

This skill activates when user expresses **implementation/continuation intent**:

### High-Confidence Triggers (Auto-Route)

**Action Verbs** (with specific target):
- "Implement [feature]"
- "Complete [task]"
- "Build [component]"
- "Add [functionality]"
- "Develop [module]"
- "Create [feature]"

**Continuation Phrases**:
- "Work on [feature]"
- "Continue [increment]"
- "Resume [work]"
- "Finish [task]"
- "Let's implement [X]"
- "Let's build [Y]"
- "Start working on [Z]"

**Bug/Fix Intent**:
- "Fix [issue]"
- "Resolve [bug]"
- "Address [problem]"

### Medium-Confidence Triggers (Clarify)

**Vague Intent** (needs target clarification):
- "Let's continue"
- "Keep working"
- "What's next?"
- "Continue where we left off"

### Don't Activate For

**Planning/Discussion** (let other skills handle):
- "What should we build?" → increment-planner
- "How does X work?" → Regular conversation
- "Should we use Y?" → Technical discussion
- "Plan a new feature" → increment-planner

**Already in Workflow**:
- User is already executing `/sw:do`
- Increment planning is in progress
- Another skill is handling the request

## Core Algorithm

### Step 1: Detect Intent

Scan user message for implementation keywords:
```
Action verbs: implement, complete, build, add, develop, create
Continuation: work on, continue, resume, finish, start
Bug/Fix: fix, resolve, address
```

Calculate confidence:
- **High (>80%)**: Action verb + specific target ("implement user auth")
- **Medium (50-80%)**: Action verb only ("let's continue")
- **Low (<50%)**: No clear intent

### Step 2: Check Active Increments

**Read increment state:**
```bash
# Find all increments with status = "active"
find .specweave/increments -name "metadata.json" -type f \
  -exec jq -r 'select(.status == "active") | .id' {} \;
```

**Three scenarios:**
1. **One active increment** → Check relevance and route
2. **Multiple active increments** → Ask user to select
3. **No active increments** → Suggest creating new one

### Step 3: Check Relevance (if active increment exists)

**Relatedness Analysis:**
Compare user's request against active increment:
- Check increment title/description
- Check task list (tasks.md)
- Check spec.md for related features

**Scoring:**
- **High match (>70%)**: Same feature area → Auto-resume
- **Medium match (40-70%)**: Related area → Ask confirmation
- **Low match (<40%)**: Unrelated → Suggest new increment

### Step 4: Route Intelligently

**Scenario A: High relevance to active increment**
```
User: "Implement user authentication"
Active: 0031-user-authentication-system

✅ High match → Auto-resume:

"I see you have an active increment for user authentication (0031).
Resuming work on that increment now with /sw:do..."

[Automatically invokes /sw:do]
```

**Scenario B: Unrelated to active increment**
```
User: "Implement payment processing"
Active: 0031-user-authentication-system

⚠️  Low match → Ask:

"I see you have an active increment (0031-user-authentication-system).

Your request for payment processing seems unrelated. Would you like to:
1. **Create new increment** for payment processing (recommended)
2. **Continue current increment** (0031) and add payment to it
3. **Pause current** and create new increment

What would you prefer?"
```

**Scenario C: No active increment**
```
User: "Implement user authentication"
Active: None

→ Suggest new increment:

"No active increment found. Let's create one for user authentication.

I'm going to create a SpecWeave increment with:
- Specification (WHAT & WHY)
- Technical plan (HOW)
- Task breakdown (STEPS with embedded tests)

Creating increment now with /sw:increment..."

[Automatically invokes /sw:increment "user authentication"]
```

**Scenario D: Multiple active increments**
```
User: "Continue working"
Active: 0031-user-auth, 0032-payment-system

→ Ask to clarify:

"You have 2 active increments:
1. **0031-user-authentication-system** (3/10 tasks complete)
2. **0032-payment-processing** (1/8 tasks complete)

Which one would you like to work on?"
```

**Scenario E: Vague continuation intent**
```
User: "Let's continue"
Active: 0031-user-authentication-system

✅ Auto-resume (only one active):

"Resuming increment 0031-user-authentication-system...
Progress: 3/10 tasks complete (30%)

Next task: T-004 Implement password hashing

[Automatically invokes /sw:do]"
```

## Integration Architecture

**Workflow:**
```
User: "Implement [feature]"
        ↓
increment-work-router (detects intent)
        ↓
[Check .specweave/increments/*/metadata.json]
        ↓
┌───────────────────┬──────────────────┬────────────────┐
│ Active increment  │ Multiple active  │ No active      │
│ (relevant)        │ (ambiguous)      │ (none)         │
└─────┬─────────────┴──────┬───────────┴──────┬─────────┘
      │                    │                  │
      ↓                    ↓                  ↓
/sw:do        Ask to select    /sw:increment
(auto-resume)        (clarify)        (create new)
```

**Calls:**
- `/sw:do` - Resume active increment
- `/sw:increment` - Create new increment
- `/sw:status` - Check increment state (if needed)

**Called By:**
- Automatically when implementation intent detected
- Works alongside `increment-planner` (planning) and `detector` (context checking)

## Decision Matrix

| User Intent | Active Increments | Relevance | Action |
|-------------|------------------|-----------|--------|
| "Implement auth" | 1 (auth-related) | High (>70%) | Auto `/sw:do` |
| "Implement auth" | 1 (unrelated) | Low (<40%) | Ask: New or add to current? |
| "Implement auth" | 0 | N/A | Auto `/sw:increment` |
| "Implement auth" | 2+ | N/A | Ask which increment |
| "Let's continue" | 1 | N/A | Auto `/sw:do` |
| "Let's continue" | 2+ | N/A | Ask which increment |
| "Let's continue" | 0 | N/A | "No active increment. What should we build?" |

## Relevance Matching Logic

**How to determine if request relates to active increment:**

```typescript
function calculateRelevance(userRequest: string, increment: Increment): number {
  let score = 0;

  // 1. Title/ID match (strongest signal)
  if (increment.title.toLowerCase().includes(extractKeywords(userRequest))) {
    score += 40;
  }

  // 2. Tasks match (check tasks.md)
  const tasks = readTasksFile(increment);
  const matchingTasks = tasks.filter(t =>
    t.title.toLowerCase().includes(extractKeywords(userRequest))
  );
  score += (matchingTasks.length / tasks.length) * 30;

  // 3. Spec match (check spec.md user stories)
  const spec = readSpecFile(increment);
  if (spec.includes(extractKeywords(userRequest))) {
    score += 20;
  }

  // 4. Type match (feature vs bug vs hotfix)
  const requestType = detectType(userRequest);
  if (requestType === increment.type) {
    score += 10;
  }

  return score; // 0-100
}
```

**Example:**
```
User: "Implement JWT token refresh"
Active: 0031-user-authentication-system

Checks:
✅ Title contains "authentication" (user mentions "JWT token") → +40 points
✅ Tasks.md has "T-005: Implement JWT refresh logic" → +30 points
✅ Spec.md mentions "token management" → +20 points
✅ Both are "feature" type → +10 points

Total: 100/100 → High relevance → Auto-resume
```

## Examples

### Example 1: Auto-Resume (High Relevance)

**Context:**
```
Active: 0031-user-authentication-system
Progress: 3/10 tasks complete
```

**User:**
```
Implement JWT token refresh
```

**increment-work-router:**
```
✅ Intent detected: "implement" + specific target
✅ Active increment found: 0031-user-authentication-system
✅ Relevance check: 95% match (authentication-related)

→ AUTO-RESUME

"I see you have an active increment for user authentication (0031).
Task T-005 'Implement JWT token refresh' is already in your plan.

Resuming increment 0031 now with /sw:do...

[Automatically invokes /sw:do]
```

### Example 2: Create New (No Active Increment)

**Context:**
```
Active: None
```

**User:**
```
Implement payment processing with Stripe
```

**increment-work-router:**
```
✅ Intent detected: "implement" + specific target
❌ No active increment found

→ CREATE NEW

"No active increment found. Let's create one for payment processing.

I'm going to create a SpecWeave increment with:
- Specification (Stripe integration requirements)
- Technical plan (API integration, webhooks, security)
- Task breakdown (implementation steps with tests)

Creating increment now with /sw:increment...

[Automatically invokes /sw:increment "payment processing with Stripe"]
```

### Example 3: Unrelated Request (Ask)

**Context:**
```
Active: 0031-user-authentication-system
Progress: 3/10 tasks complete
```

**User:**
```
Implement email notifications
```

**increment-work-router:**
```
✅ Intent detected: "implement" + specific target
✅ Active increment found: 0031-user-authentication-system
⚠️  Relevance check: 15% match (unrelated)

→ ASK FOR CLARIFICATION

"I see you have an active increment (0031-user-authentication-system) with 3/10 tasks complete.

Your request for email notifications seems unrelated. Would you like to:
1. **Create new increment** for email notifications (recommended - keeps work focused)
2. **Add to current increment** (0031) - if notifications are for auth emails
3. **Pause current increment** and start notifications

SpecWeave works best with focused increments. What would you prefer?"
```

### Example 4: Multiple Active (Clarify)

**Context:**
```
Active: 0031-user-authentication-system (3/10 tasks)
Active: 0032-payment-processing (1/8 tasks)
```

**User:**
```
Let's continue working
```

**increment-work-router:**
```
✅ Intent detected: "continue" (vague)
✅ Multiple active increments found: 2

→ ASK TO SELECT

"You have 2 active increments:

1. **0031-user-authentication-system**
   - Progress: 3/10 tasks (30%)
   - Next: T-004 Implement password hashing

2. **0032-payment-processing**
   - Progress: 1/8 tasks (12%)
   - Next: T-002 Set up Stripe SDK

Which one would you like to work on?"

[Wait for user selection, then invoke /sw:do {selected-id}]
```

### Example 5: Vague Intent + Single Active (Auto-Resume)

**Context:**
```
Active: 0031-user-authentication-system (3/10 tasks)
```

**User:**
```
What's next?
```

**increment-work-router:**
```
✅ Intent detected: "what's next" (continuation)
✅ One active increment: 0031-user-authentication-system

→ AUTO-RESUME

"Resuming increment 0031-user-authentication-system...
Progress: 3/10 tasks complete (30%)

Next task: **T-004 Implement password hashing**

[Automatically invokes /sw:do]"
```

## Opt-Out Mechanism

Users can override auto-routing with explicit instructions:
- "Don't resume, create new" → Forces new increment
- "Just discuss first" → Regular conversation
- "Plan without implementing" → Routes to `/sw:increment` only
- "Show me the current state" → Uses `/sw:status` instead

## Success Criteria

- ✅ Users can say "implement X" and work starts automatically
- ✅ Smart routing to active increments (no manual `/sw:do`)
- ✅ Detects unrelated requests and prevents scope creep
- ✅ No "which increment?" confusion (auto-handles single active)
- ✅ Clear choices when ambiguous (multiple active or unrelated)
- ✅ Seamless integration with existing skills (increment-planner, detector)

## Related Skills

- **increment-planner**: For creating increment structure (invoked by this skill for new projects)
- **detector**: For checking SpecWeave context

---

**Key Distinction:**
- `increment-planner` = "PLAN this increment" or "I want to BUILD a new product" (planning-level)
- `increment-work-router` = "IMPLEMENT this feature/task" (execution-level)

This skill bridges planning → execution by auto-detecting implementation intent.
