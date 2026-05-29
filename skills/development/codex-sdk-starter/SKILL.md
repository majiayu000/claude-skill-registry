---
name: codex-sdk-starter
description: Use when asked to introduce Codex SDK usage for automation (CI/CD, bots, internal tools) and provide a minimal, safe starter pattern.
---

Goal: provide a minimal, practical Codex SDK starter pattern without forcing repo dependencies unless explicitly requested.

Workflow:

1. Clarify the use case
   - CI triage, PR generation, internal bot, batch refactors, etc.

2. Provide the minimal TS usage pattern
   - Install: `npm install @openai/codex-sdk`
   - Start/resume a thread and call `run()` multiple times.
   - Persist `threadId` for continuity.

3. Recommend safe operational boundaries
   - Limit scope to a repo/workspace.
   - Require tests/typecheck before finalizing.
   - Avoid destructive operations without explicit approval.

4. Optional: propose an internal wrapper
   - A small module that standardizes thread creation, logging, timeouts, and artifact capture.

