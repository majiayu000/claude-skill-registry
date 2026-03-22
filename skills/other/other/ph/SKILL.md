---
name: ph
description: Prepare handover documentation for task continuation
argument-hint: [task-directory]
disable-model-invocation: true
---

# Prepare Handover Command

## PRIMARY OBJECTIVE
Stop at the closest logical step of implementation. Update or create a task document that prepares handover to another developer. The task document must include all necessary information so that any developer—even one from another team unfamiliar with the codebase—can use it as an entry point to understand what needs to be done and how.

## CONSTRAINTS
- Stop only at logical breakpoints (completed step, stable state)
- Document must be self-contained and newcomer-friendly
- No assumptions about reader's familiarity with codebase
- All context required for continuation must be explicit

## WORKFLOW

### **STEP 1: Stop at Logical Point**
1. Complete current logical unit of work (don't leave mid-change)
2. Ensure code compiles/runs without errors
3. Commit any uncommitted work with clear message

### **STEP 2: Create/Update Task Document**
Ensure the task document in `tasks/task-YYYY-MM-DD-[name]/` contains:

**For any developer to pick up:**
- Clear problem statement and goals
- Current progress (what's done, what remains)
- Technical context (architecture decisions, patterns used)
- File locations and their purposes
- How to run/test the implementation
- Known issues, blockers, or open questions
- Recommended next steps with rationale

### **STEP 3: Finalize**
1. Push branch to remote
2. Update Linear with handover status (if applicable)
3. Confirm document is complete for handover

## OUTPUT
Self-contained task document ready for any developer to continue work.
