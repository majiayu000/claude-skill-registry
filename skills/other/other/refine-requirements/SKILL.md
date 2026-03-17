---
name: refine-requirements
description: Refine and clarify feature requirements by asking targeted follow-up questions, then update or create tasks based on answers. Use after initial planning when requirements need clarification, or when the user mentions "refine", "clarify", "more details", or "questions".
allowed-tools: Read, AskUserQuestion, TodoWrite
---

# Refine Requirements Skill

Ask targeted follow-up questions to clarify ambiguous requirements and update implementation tasks based on the answers. Used after initial feature planning to ensure comprehensive understanding before coding.

## When to Use This Skill

Use this skill when:
- After running `/plan-feature` and need more clarity
- User says "I need to clarify some things"
- Requirements seem ambiguous or incomplete
- User mentions "refine", "more details", "questions"
- Before starting implementation to reduce rework

## Instructions

Follow these steps to refine requirements:

### Step 1: Understand Current Context

First, gather context about what's been planned:

1. Check if TodoWrite has active tasks (indicates planning already happened)
2. If tasks exist, read them to understand the feature scope
3. If no tasks, ask user: "What feature are you refining requirements for?"

Present current understanding:
```
I can see you're planning [feature name] with [N] tasks. Let me ask some clarifying questions to refine the requirements.
```

### Step 2: Identify Gaps and Ambiguities

Analyze the current plan for common gaps:

**Data/Schema Questions:**
- Missing field validations or constraints
- Unclear relationships or associations
- Missing indexes or performance considerations
- Data migration or seeding needs

**Business Logic Questions:**
- Edge cases not covered
- Validation rules unclear
- State transitions undefined
- Authorization rules ambiguous

**UI/UX Questions:**
- User workflows incomplete
- Error handling unclear
- Success/failure states undefined
- Mobile vs desktop behavior

**Technical Questions:**
- Performance requirements unclear
- Caching strategy undefined
- Background job needs
- Real-time updates needed?
- API requirements

### Step 3: Ask Targeted Questions

Use AskUserQuestion to ask 3-5 focused questions based on the feature type.

**Question selection strategy:**
1. Refer to [reference.md](reference.md) for question templates by feature type
2. Prioritize questions that will change implementation significantly
3. Focus on gaps that could cause rework later
4. Avoid questions already answered in the plan

**Format questions clearly:**
- One topic per question
- Provide context for why you're asking
- Offer common options when applicable
- Use multiSelect when appropriate

### Step 4: Analyze Answers

After receiving answers, analyze impact:

1. **New tasks needed?** - Do answers introduce new work?
2. **Existing tasks change?** - Do answers modify planned approach?
3. **Dependencies shift?** - Do answers change task ordering?
4. **Scope change?** - Do answers significantly expand/reduce scope?

### Step 5: Update or Create Tasks

Based on answers, update the implementation plan:

**If TodoWrite tasks exist:**
- Use TodoWrite to update existing tasks with new details
- Add new tasks if answers revealed additional work
- Reorder tasks if dependencies changed
- Mark tasks as pending that need revision

**If no tasks exist:**
- Create initial task list using TodoWrite
- Include all details from the refinement conversation

**Task updates should include:**
- Specific details from answers (validation rules, UI states, etc.)
- New acceptance criteria
- Changed technical approach
- Additional files to create/modify

### Step 6: Present Refinement Summary

Provide a clear summary of what changed:

```
## Requirements Refined

### Questions Asked
1. [Question 1]
   - Answer: [Summary]
   - Impact: [What this changes]

2. [Question 2]
   - Answer: [Summary]
   - Impact: [What this changes]

### Changes to Implementation Plan

**Tasks Updated:**
- Task 3: Added email uniqueness validation
- Task 5: Changed to use Turbo Stream instead of full page reload

**New Tasks Added:**
- Task 7: Implement password strength indicator
- Task 8: Add "remember me" functionality

**Technical Approach Changes:**
- Using Devise instead of custom auth
- Adding Kredis for session storage
- Implementing rate limiting with Rack::Attack

### Updated Scope
- Original: [X] tasks
- Refined: [Y] tasks
- Effort change: [increased/decreased/same]

### Ready to Proceed?
The implementation plan has been updated based on your answers. Review the updated tasks and let me know if you'd like to proceed or need further refinement.
```

## Question Strategies by Feature Type

For detailed question templates, see [reference.md](reference.md).

**Quick reference:**

### Authentication Features
Focus on: method, security, sessions, recovery, MFA

### CRUD Features
Focus on: validations, permissions, UI flows, real-time updates

### Admin/Dashboard Features
Focus on: metrics, filters, exports, access control

### API Features
Focus on: versioning, authentication, rate limiting, documentation

### Background Jobs
Focus on: triggers, frequency, error handling, monitoring

## Best Practices

**Do:**
- ✅ Ask questions that will significantly impact implementation
- ✅ Reference existing Rails patterns in the project
- ✅ Prioritize security and performance clarifications
- ✅ Focus on edge cases and error scenarios
- ✅ Consider mobile vs desktop differences
- ✅ Update tasks with specific, actionable details

**Don't:**
- ❌ Ask questions already answered in the plan
- ❌ Ask more than 5 questions at once (overwhelming)
- ❌ Ask vague questions without context
- ❌ Skip updating tasks after getting answers
- ❌ Make assumptions - clarify instead
- ❌ Ignore technical debt or performance implications

## Integration with Other Skills

**After plan-feature:**
```bash
/plan-feature "Add commenting system"
# ... initial plan created ...
/refine-requirements
# ... asks follow-up questions, updates tasks ...
```

**Before create-task-files:**
```bash
/plan-feature "Add commenting system"
/refine-requirements  # Clarify first
/create-task-files    # Then export
```

**Standalone:**
```bash
/refine-requirements
# Asks: "What feature are you refining?"
# Creates tasks based on detailed answers
```

## Examples

For real-world examples of requirement refinement sessions, see [examples.md](examples.md).

## Output

Always use TodoWrite to update or create tasks. Ensure:
- Tasks include specific details from answers
- Acceptance criteria updated with new requirements
- Technical approach reflects refined understanding
- Dependencies and ordering adjusted if needed

This skill ensures thorough requirement gathering, reduces implementation rework, and catches edge cases early in the planning phase.
