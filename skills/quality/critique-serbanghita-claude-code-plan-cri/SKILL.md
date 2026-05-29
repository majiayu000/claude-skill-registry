---
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, LSP, mcp__ide__getDiagnostics, Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(echo $PPID), Bash(kill -0:*), Bash(rm:*), Bash(mkdir:*)
description: Critique the user's plan from plan.md
disable-model-invocation: true
model: opus
effort: high
---

You are performing an iterative review of the user's execution plan.
Critique the plan, code, architecture, system design, and design patterns.

To do this, follow these steps precisely:

1. Read `.claude/plan-critique-config.json`, get `plansFolder` path from settings. If the file doesn't exist or
   `plansFolder` is not set: Respond with "No plans folder configured. Run `/plan:create` first to set up."
2. Get the Claude Code process ID by running: `echo $PPID`. Store this as `sessionPID`.
3. Clean up stale sessions: Scan `[plansFolder]/.sessions/` for files. For each file named with a PID, check if that
   process is still running via `kill -0 [PID] 2>/dev/null`. If the command fails (process not running), delete that
   session file. This is non-blocking cleanup.
4. Read the current session's plan from `[plansFolder]/.sessions/[sessionPID]` if it exists. Store as `sessionPlan`.
5. Scan `[plansFolder]/` for subdirectories (each subdirectory is a plan). Exclude `archived/` and `.sessions/`
   folders and any files, only list plan directories.
   If no plan folders exist: Respond with "No plans found. Create one with `/plan:create`".
6. Select the plan to critique:
   - If `sessionPlan` exists and matches a plan folder, auto-select it. Inform the user:
     "Using current session plan: [sessionPlan]"
   - Else if only one plan exists, auto-select it and inform user.
   - Otherwise, ask the user to select a plan from the list.
     Example:
     ```
     Available plans:
     1. add-user-authentication
     2. refactor-database-layer
     3. implement-caching

     Which plan would you like to critique? [1-3]
     ```
7. Update the session file `[plansFolder]/.sessions/[sessionPID]` with the selected plan slug (create if needed).
8. Read the plan file at `[plansFolder]/[selected-plan]/plan.md`
9. Check for errors:
   - If `plan.md` is empty: Respond with "Plan file is empty. Edit `[plansFolder]/[selected-plan]/plan.md`"
   - If `CLAUDE.md` does not exist in project root: Respond with "Create a `CLAUDE.md` file in the root of your project."
10. Detect project languages and check for LSP support:
    - Use Glob to check for TypeScript indicators: `tsconfig.json`, `*.ts`, or `*.tsx` files in the project
    - Use Glob to check for PHP indicators: `composer.json` or `*.php` files in the project
    - If TypeScript files are detected, inform the user:
      "This project uses TypeScript. For better code intelligence during critique, enable the
      `typescript-lsp` plugin (claude-plugins-official). Check with the `/plugins` command."
    - If PHP files are detected, inform the user:
      "This project uses PHP. For better code intelligence during critique, enable the
      `php-lsp` plugin (claude-plugins-official). Check with the `/plugins` command."
    - This is informational only, do not block the critique.
11. Read the existing "Iteration: [number]" at `[plansFolder]/[selected-plan]/critique.md` (if it exists) and
    determine the current iteration number. If no critique exists, this is iteration 1.
12. If the plan references files that are in the `[plansFolder]/[selected-plan]/` folder, review those as well and
    add them to the context of the critique.
13. Perform a thorough critique of the plan considering:
    - Clarity: Are requirements specific and unambiguous?
    - Completeness: Are all necessary steps included?
    - Order: Are dependencies between steps correctly sequenced?
    - Feasibility: Can each step be executed given the current codebase?
    - Risk: Are there potential side effects or breaking changes?
    - Standards: Does it comply with `CLAUDE.md` project standards?
    - Scope: Is scope reasonable? Any unnecessary additions?
    - Testability: How will success be verified?
    - Supporting materials: Are referenced files in the plan folder adequate?
14. Evaluate whether the plan can be split into independent tasks. If the plan contains multiple features
    or changes that can be executed separately, strongly recommend splitting it into separate plans.
    Why this matters:
    - Reduces complexity during execution
    - Limits the context window needed for each plan
    - Makes critique iterations more focused and actionable
    - Allows independent tasks to proceed without blocking each other

    Example: A plan with "Add user authentication", "Refactor database layer", and "Add caching" should
    be split into three separate plans if these can be implemented independently.

    When suggesting a split, be specific about which sections should become their own plan.
15. Write the critique to `[plansFolder]/[selected-plan]/critique.md`.
    When writing the critique, follow the original chapters from `plan.md`.
    The goal is to be able to easily override the `plan.md` if the user chooses to merge `critique.md` with `plan.md`

    Use the format in [critique-format.md](critique-format.md).

Notes:

- When critiquing, always analyze codebase structure (existing files, directories, patterns), Project standards from `CLAUDE.md`, The `README.md` file, dependencies (package.json, requirements.txt, etc.), git state if relevant, whether referenced files/APIs actually exist, supporting files in the plan folder.
- When doing the writeup of the critique, in the "Description" area make use of the line numbers from `plan.md` file and reference those, so that the user can easily find what text to replace/update.
- Use code intelligence to verify the plan against the actual codebase:
  - Verify types exist: use LSP go-to-definition when an LSP plugin is enabled, fall back to Grep for `class`, `interface`, `type`, or `struct` definitions
  - Check method/function existence: use LSP go-to-definition, fall back to Grep for `function`/`def`/`fn` declarations in the target file
  - Find usages/references: use LSP find-references, fall back to Grep for the symbol name across the codebase
  - Review diagnostics: use `mcp__ide__getDiagnostics` to pull current errors/warnings from the IDE for files referenced in the plan
  - Verify file paths exist with Glob before referencing them in the critique
- Add the found issues/observations list in the beginning of the critique.md file as a Table of contents
- Always follow the chapters from plan.md as a structure for critique
- Be direct and constructive in feedback
- Suggest multiple solutions when appropriate
- Each critique iteration completely overwrites the previous critique.md file.
- Discard addressed issues: If an issue from the previous critique has been fixed in plan.md, do not include it.
- Only include current issues: The critique should reflect the current state of plan.md.
- New unrelated observations: If new issues appear that don't fit under existing plan.md chapters add them as new chapters at the bottom of the critique
- Increment iteration number: Always increment from the previous critique's iteration number
