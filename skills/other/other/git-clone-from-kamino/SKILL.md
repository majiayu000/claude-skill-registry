---
name: git-clone-from-kamino
description: "{{ 𝛀𝛀𝛀 }} Initialize a new project from the Kamino template"
model: opus
disable-model-invocation: true
allowed-tools: ["Bash(git:*)", "Bash(mkdir:*)", "Bash(cp:*)", "Bash(mv:*)", "Bash(chmod:*)", "Bash(ln:*)", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Read", "Write", "Edit", "Glob", "Grep"]
---

<overview>
  Gather project details conversationally, then configure all template files.
</overview>
<gather-info>
  Ask one at a time:
  1. Project name
  2. Description (1-2 sentences)
  3. Tech stack (e.g., "SvelteKit + TypeScript", "Tauri + Svelte")
  4. Package manager (npm/bun/pnpm/yarn)
  5. Database (PostgreSQL/Neo4j/MongoDB/SQLite/None/Multiple)
  6. Testing framework (Vitest/Jest/Playwright/None)
</gather-info>
<update-files>
  Replace placeholders in:
  - .claude/CLAUDE.md: {{PROJECT_NAME}}, {{PROJECT_DESCRIPTION}}, {{TECH_STACK}}, {{PACKAGE_MANAGER}}, {{TEST_FRAMEWORK}}, {{DATABASE_INFO}}, {{KEY_COMMANDS}}
  - docs/README.md: {{PROJECT_NAME}}
  - docs/roadmaps/mvp.md: {{PROJECT_NAME}}
  - .claude/.mcp.json: Add filesystem server; add context7 for SvelteKit/Next/React
</update-files>
<git-setup>
  git init
  ln -s ~/.claude/hooks/post-commit-evidence .git/hooks/post-commit
  ln -s ~/.claude/hooks/pre-push-all .git/hooks/pre-push
  chmod +x .git/hooks/*
  git add . && git commit -m "chore: initialize project from Kamino template"
</git-setup>
<create-adr>
  Create docs/adrs/001-initial-tech-stack.md documenting stack choice with rationale.
</create-adr>
<summary>
  Show: project name, stack, location, next steps (install, dev, review roadmap), active hooks.
</summary>
<error-handling>
  - Warn if placeholders remain after updates
  - Provide troubleshooting if git commands fail
  - Notify if hooks don't exist in ~/.claude/hooks/
</error-handling>
