---
name: create-issues
description: Convert an implementation plan into tracked issues with proper dependencies. Generates commands for issue trackers like Beads or GitHub Issues.
---

# Iterative Issue Creation from Plan

You will act as a project manager. Your task is to take the provided plan and create a set of issues in the specified issue tracking system. You will generate the precise, runnable commands to do so.

## Setup

### Input Plan

The plan to be implemented will be provided here. Your task is to parse it and create issues accordingly.

**Example Plan:**
```markdown
# Plan for New Authentication Feature

## Phase 1: Database Schema
- Add `password_hash` and `last_login` to the `users` table.
- File: `db/migrations/001_add_auth_fields.sql`

## Phase 2: Create Login Endpoint
- Create a new endpoint `POST /login`.
- It should take `email` and `password`.
- It should return a JWT.
- File: `src/auth/routes.ts`

## Phase 3: Protect Routes
- Create middleware that checks for a valid JWT.
- Apply it to the `/api/v1/profile` endpoint.
- File: `src/auth/middleware.ts`
```

## Process

For each phase or logical unit of work in the plan, create a corresponding issue. After creating all issues, define their dependencies.

### Issue Template

Each issue you create MUST use the following template for its title and description.

**Title:** A short, clear, action-oriented title (e.g., "Create Login Endpoint").

```
**Context:** [Brief explanation of what this issue is about, referencing the plan]
Ref: [Link to plan document and section]

**Files:**
- [List of files to be modified]

**Acceptance Criteria:**
- [ ] A checklist of what "done" means for this issue.

---
**CRITICAL: Follow Test Driven Development and Tidy First workflows.**
- Write tests *before* writing implementation code.
- Clean up related code *before* adding new functionality.
```

### Creating Issues and Dependencies

Generate the full, runnable commands to create the issues and then wire up their dependencies.

#### Strategy for Robust Execution

To ensure that dependencies are wired correctly, you MUST follow this three-step process:

1.  **Create Issues:** Run the creation command for each issue.
2.  **Capture IDs:** From the output of each command, capture the newly created issue ID or number and store it in a shell variable (e.g., `phase_1_issue_id=$(...)`). Most modern CLI tools provide a way to get machine-readable output (e.g., a `--porcelain` flag or simply the raw ID as the last line of output).
3.  **Connect Dependencies:** Use the variables from the previous step to run the dependency commands, ensuring you are linking the correct issues.

This prevents errors that can arise from assuming sequential or predictable issue IDs.

**Example for Beads:**
```bash
# Create issues for each phase, capturing the new issue ID from stdout
issue_1_id=$(bd create --title="DB Schema: Add auth fields to users table" --description="""
**Context:** As per the auth feature plan, we need to update the users table to support authentication.
Ref: plans/auth-feature.md#phase-1

**Files:**
- `db/migrations/001_add_auth_fields.sql`

**Acceptance Criteria:**
- [ ] Migration is created and applied.
- [ ] `users` table has `password_hash` and `last_login` fields.

---
**CRITICAL: Follow Test Driven Development and Tidy First workflows.**
- Write tests *before* writing implementation code.
- Clean up related code *before* adding new functionality.
""")

issue_2_id=$(bd create --title="API: Create Login Endpoint" --description="""
**Context:** Create the `POST /login` endpoint to authenticate users and issue JWTs.
Ref: plans/auth-feature.md#phase-2

**Files:**
- `src/auth/routes.ts`

**Acceptance Criteria:**
- [ ] Endpoint `POST /login` exists.
- [ ] It returns a JWT on successful login.
- [ ] It returns an error on failed login.

---
**CRITICAL: Follow Test Driven Development and Tidy First workflows.**
- Write tests *before* writing implementation code.
- Clean up related code *before* adding new functionality.
""")

# (Assume issue for Phase 3 is also created and its ID is in $issue_3_id)

# Set dependencies using the captured IDs
bd dep add "$issue_2_id" "$issue_1_id"  # login endpoint depends on db schema
# bd dep add "$issue_3_id" "$issue_2_id" # middleware depends on login endpoint
```

**Example for GitHub Issues:**
```bash
# Create issues, capturing the new issue URL from stdout
issue_1_url=$(gh issue create --title "DB Schema: Add auth fields to users table" --body "...") # (full body as above)
issue_2_url=$(gh issue create --title "API: Create Login Endpoint" --body "...")
# ...

# Extract the issue numbers from the URLs
issue_1_number=$(echo "$issue_1_url" | sed 's/.*\\///')
issue_2_number=$(echo "$issue_2_url" | sed 's/.*\\///')

# Note dependencies in the body. Since gh CLI has no formal dep command,
# we add a reference to the blocking issue in the body of the dependent issue.
gh issue edit "$issue_2_number" --body "$(gh issue view "$issue_2_number" --json body -q .body)

Blocked by #$issue_1_number"
```

## Final Report

After generating all commands, provide a final summary report in the following format.

```
## Issue Creation Summary

**System:** [Beads/GitHub/Linear/Jira]
**Plan:** [path/to/plan.md]

### Summary

- Total Issues Created: [count]
- Dependencies Defined: [count]

### Verdict

[ISSUES_CREATED | FAILED_TO_CREATE]

**Rationale:** [1-2 sentences explaining the result, e.g., "Successfully created all issues and dependencies from the plan."]
```
