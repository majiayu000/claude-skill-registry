---
name: bump-deps
description: Analyze and upgrade dependencies with breaking change detection. Use when updating frontend (pnpm) or backend (uv) dependencies.
user-invocable: true
disable-model-invocation: true
argument-hint: <guidelines>
metadata:
  author: BastiDood <basti@casperstudios.xyz>
---

# Bump Dependencies

Analyze outdated dependencies and safely upgrade them with breaking change detection.

## Workflow

1. **Detect package manager** based on current directory:

   - If in `frontend/` directory or working with TypeScript/JavaScript: use [`pnpm` reference](references/pnpm.md)
   - If in `backend/` directory or working with Python: use [`uv` reference](references/uv.md)

2. **List outdated dependencies** using the package manager-specific command from the reference

3. **Spawn background analysis tasks for EACH notable upgrade:**

   **CRITICAL**: You MUST spawn the `package-upgrade-analyzer` sub-agent as a **background Task** for EACH and EVERY notable upgrade. Do NOT take shortcuts.

   ```
   Task(
     subagent_type="package-upgrade-analyzer",
     run_in_background=true,
     prompt="Analyze upgrade for {package_name} from {old_version} to {new_version}. GitHub: {repo_url}"
   )
   ```

   Notable upgrades include:

   - Major version bumps (e.g., v4 → v5)
   - Packages with known breaking changes
   - Core dependencies (React, Next.js, FastAPI, SQLAlchemy, etc.)

   Spawn ALL tasks in a **single message with multiple tool calls** for maximum parallelism.

4. **Wait for all background tasks to complete:**

   - Use `TaskOutput` to retrieve results from each background task
   - Once ALL tasks are complete, ultrathink about the suggestions, migration guides, and release notes
   - Invoke the `Plan` tool and its sub-agents to strategically address the breaking changes
   - Plan carefully to maintain as much of the original behavior as possible

5. **Ask clarifying questions:**

   - If the migration path forward is ambiguous, ASK questions
   - Do NOT proceed unless you're sure about the safety of the dependency version bumps

6. **Generate PR summary document:**

   Write a `.claude/scratchpad/PR.md` file using the [PR template](assets/pull-request-template.md).
   Ensure that all package identifiers are properly wrapped in backticks for readability.

7. **Create PR (user confirmation required):**

   After generating `.claude/scratchpad/PR.md`, use `AskUserQuestion` to confirm:

   ```
   AskUserQuestion(
     question="Ready to create the PR? You can edit .claude/scratchpad/PR.md first if needed.",
     header="Create PR?",
     options=[
       { label: "Create PR", description: "Create the PR with current PR.md content" },
       { label: "Let me edit first", description: "I'll edit PR.md and confirm when ready" }
     ]
   )
   ```

   Once the user confirms, derive `PR_TITLE` and create the PR:

   **Deriving `PR_TITLE`:**

   1. **Scope**: Use `app` for frontend (pnpm), `api` for backend (uv)
   2. **Content** (pick first applicable):
      - **≤3 notable packages**: List them by name with target major version
        → "deps(app): bump `react-query` to v5, `next` to v15"
      - **>3 packages with notable ones**: Highlight 1-2 notable + count
        → "deps(api): bump `sqlalchemy` to v2 (+4 packages)"
      - **Many minor bumps only**: Just the count
        → "deps(app): bump 12 dependencies"
   3. **Keep under 72 characters**

   ```bash
   PR_TITLE="deps(app): bump react-query to v5, next to v15"
   gh pr create --base dev --head "$(git rev-parse --abbrev-ref HEAD)" --title "$PR_TITLE" --body-file .claude/scratchpad/PR.md
   ```

   After successful PR creation:

   ```bash
   # Clean up the scratchpad file
   rm .claude/scratchpad/PR.md
   ```

   Return the PR URL to the user.

## Important Notes

- Always analyze breaking changes BEFORE upgrading
- Use parallel Task agents for efficiency
- Focus on safety over speed - better to ask than to break production
- Consider rollback strategies for risky upgrades

## Additional Instructions

The remaining instructions are behavior overrides by the user.

<user-guidelines>

$ARGUMENTS

</user-guidelines>
