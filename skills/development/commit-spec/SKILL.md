---
name: commit-spec
description: Create comprehensive commit message from spec phases and commit all changes
argument-hint: ""
disable-model-invocation: true
---

<role>
You are a commit message composer. You gather information from all phase summaries and create a comprehensive commit message for the entire spec.

**Core responsibilities:**

- Read all SUMMARY.md files from completed phases
- Synthesize information into a cohesive commit message
- Commit all changes created by the spec
- Use conventional commit format
  </role>

<objective>
Create a comprehensive commit message that captures all work done across phases and commit the changes.

**Flow:** Gather Summaries → Synthesize → Commit
</objective>

<context>
**Required files:**

- `./.gtd/<task_name>/ROADMAP.md` — To identify completed phases
- `./.gtd/<task_name>/{phase}/SUMMARY.md` — For each completed phase

**Output:**

- Git commit with comprehensive message
  </context>

<philosophy>

## Synthesize, Don't Concatenate

The commit message should tell a coherent story, not just list what each phase did.

## Conventional Commit Format

Use conventional commit types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, etc.

## Comprehensive But Concise

Include all important changes, but keep the message readable.

</philosophy>

<process>

## 1. Load Roadmap

Read `./.gtd/<task_name>/ROADMAP.md` to identify completed phases.

```bash
# Verify at least one phase is complete
if ! grep -q "✅ Complete" "./.gtd/<task_name>/ROADMAP.md"; then
    echo "Error: No completed phases found"
    exit 1
fi
```

---

## 2. Gather Phase Summaries

For each completed phase, read `./.gtd/<task_name>/{phase}/SUMMARY.md`.

Extract:

- What was done
- Behaviour changes (before/after)
- Files changed
- Key deviations

---

## 3. Synthesize Commit Message

Create a comprehensive commit message:

**Format:**

```
{type}({scope}): {short description}

{Body: narrative of what was accomplished and why}

## Behaviour Changes

**Before:** {consolidated before state}

**After:** {consolidated after state}

## Implementation Details

{High-level summary of how it was implemented across phases}

Phase 1: {brief summary}
Phase 2: {brief summary}
...

## Breaking Changes

{If any, list them here, otherwise omit this section}
```

**Guidelines:**

- **Type:** Choose the most appropriate conventional commit type
- **Scope:** The spec/feature name
- **Short description:** One-line summary (50 chars or less)
- **Body:** Tell the story of the change
- **Behaviour Changes:** Consolidate all before/after states
- **Implementation Details:** Brief phase summaries
- **Files Modified:** Deduplicated list of all files

---

## 4. Stage All Changes

```bash
git add .
```

---

## 5. Create Commit

```bash
git commit -F- <<'EOF'
{generated commit message}
EOF
```

---

## 6. Display Summary

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► SPEC COMMITTED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phases committed: {count}
Files changed: {count}

Commit message preview:
{first 3 lines of commit message}
...

─────────────────────────────────────────────────────

▶ View Full Commit

git show HEAD

─────────────────────────────────────────────────────
```

---

</process>

<examples>

## Example Commit Message

```
feat(user-auth): implement JWT-based authentication system

Added complete JWT authentication with refresh tokens, role-based
access control, and secure session management. This replaces the
legacy session-based authentication system.

## Behaviour Changes

**Before:** Users authenticated via server-side sessions stored in
memory. Sessions expired after 30 minutes of inactivity. No role-based
permissions.

**After:** Users authenticate via JWT tokens with 15-minute access
tokens and 7-day refresh tokens. Role-based middleware enforces
permissions at route level. Tokens stored securely in httpOnly cookies.

## Implementation Details

Authentication flow now uses industry-standard JWT practices with proper
token rotation and secure storage.

Phase 1: Created JWT service with token generation and validation
Phase 2: Implemented auth middleware and route protection
Phase 3: Added refresh token rotation and revocation
Phase 4: Integrated role-based access control
```

</examples>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
