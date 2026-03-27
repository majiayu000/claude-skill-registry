---
name: dbcraft
description: Open and operate the local DB Craft visual schema studio at D:\DBdesigner. Use it to design or edit MySQL 8, PostgreSQL 14, SQLite, and MSSQL models, generate tables with AI, import CREATE TABLE scripts, validate schema structure, save workspace models, export SQL, and prepare migration-ready artifacts for a separate deployment workflow.
---

# DB Craft

## Overview

DB Craft is a local visual database modeling workspace. Use it when the user wants a faster, more concrete flow than hand-writing schema notes: open the app, shape tables and relationships in the browser, keep the model saved in the active workspace, and export SQL or handoff-ready artifacts when the design is ready.

## Core Rule

- In all conversations for the same workspace/project, table creation and table changes must be reflected back into the current diagram/model.
- Do not treat "建表" and "改表" as text-only outputs. Update the active `*.dbmodel.json` model so the diagram stays in sync with the project's ongoing conversations.

## Quick Start

1. When the user asks to open DB Craft, first check whether `http://127.0.0.1:3000` is already serving the app.
   - If it is already up, reuse that running service and tell the user you are opening the page on the existing service.
   - If it is not up, run `scripts/launch-dbdesigner.ps1` to start the local server, then tell the user you started the service and are opening the page.
   The launcher now uses the current shell working directory as the default project workspace hint when opening DB Craft.
2. Open `http://127.0.0.1:3000` in the browser.
3. If the task is a browser demo, prefer headed mode and a maximized window so the user can follow along.
4. If the user needs AI table generation, confirm `OPENAI_API_KEY` is available in the current environment or let the user fill the key in `Settings -> AI Config`.
5. If the user needs menu names, shortcuts, or operating tips, read [references/usage.md](references/usage.md).
6. If the user needs setup expectations or marketplace install details, read [references/install-prerequisites.md](references/install-prerequisites.md).
7. If the user needs privacy, data flow, or AI-provider disclosure details, read [references/data-security.md](references/data-security.md).
8. If the user needs a final release gate or submission summary, read [references/marketplace-submission-checklist.md](references/marketplace-submission-checklist.md).
9. If the user needs visual asset planning for marketplace release, read [references/icon-and-screenshot-checklist.md](references/icon-and-screenshot-checklist.md).

## Launch

- Treat `D:\DBdesigner` as the source application directory.
- Start the app with `node server.js` in that directory. Use the bundled PowerShell launcher for reliability.
- Opening behavior must follow this order every time:
  1. Check whether `http://127.0.0.1:3000` is already reachable.
  2. If reachable, reuse the running service instead of spawning a duplicate.
  3. If not reachable, start the service and wait for it to become reachable.
  4. Tell the user which case happened: reused existing service or started a new one.
  5. Then open the page.
- The PowerShell launcher defaults `WorkspacePath` to the current shell directory so DB Craft opens with the active workspace path prefilled as the workspace hint.
- After opening DB Craft for the user, explicitly remind them that the model files are saved under the active workspace directory they are using for this project.
- When DB Craft writes `dbcraft-codex-handoff.md` into the active project directory, treat it as the preferred handoff artifact for continuing the conversation from the designer.
- Default address: `http://127.0.0.1:3000`.
- If port `3000` is already serving the app, reuse it instead of spawning duplicates.
- If `node` is missing or the page does not come up, stop and report the blocker clearly.

## Operate

- Use the app for these main tasks:
- Create a new model for `MySQL 8`, `PostgreSQL 14`, `SQLite`, or `MSSQL`.
- Open or save `*.dbmodel.json` files through the app workspace flow.
- Add tables manually, generate them with AI, or import them from `CREATE TABLE` SQL.
- Run syntax checks before export when the user asks for validation.
- Export generated SQL through the built-in export flow.
- Help the user operate the UI with menu paths and shortcuts from [references/usage.md](references/usage.md).
- When the user says to continue from DB Craft handoff, first check the active project directory for `dbcraft-codex-handoff.md` and prefer reading it before asking the user to paste anything manually.
- Within the same workspace, treat table creation as incremental modeling: append each newly requested/generated table to the current active model instead of creating isolated examples.
- Within the same workspace, treat table edits the same way: when the user changes fields, indexes, comments, relationships, or table names, apply the change back into the current model so the diagram reflects the latest state.
- Prefer updating the existing `*.dbmodel.json` in the active workspace so all tables for that workspace stay together in one model the user can reopen.
- When importing or creating a table and the active template adds default fields, keep those template fields unless the user explicitly asks to remove them.
- If the user needs the result to appear in their own browser session, save or export a `*.dbmodel.json` file and have that session open it. Do not assume in-memory state from one automated browser session is visible in another browser session.
- Favor a user-facing product tone: DB Craft helps users move from idea -> model -> SQL with minimal friction.

## Handoff To Migration

- If the user says to create the designed tables in a real database management system, finish the design/model/export work in DB Craft and then hand off to a separate migration or deployment skill.
- Workflow:
  1. Open DB Craft and update the model first.
  2. Save the model under the active workspace.
  3. Export or generate SQL from the current model into the same workspace.
  4. Keep the model and generated SQL together so another skill or workflow can continue with review, migration generation, or deployment.
- Do not make database execution the default behavior for this public-facing skill. DB Craft should stop at model + SQL + handoff unless the surrounding environment explicitly wires in a separate deployment skill.

## AI Table Generation

- The app supports AI table generation from `Model -> AI Build Table` / `Alt+L`.
- Prefer the API key saved in `Settings -> AI Config`; fall back to the server environment variable `OPENAI_API_KEY`.
- The app defaults to model name `gpt-5-codex` when none is provided.
- Report API errors as returned by the page or server instead of guessing.

## Browser Use

- When the user asks to open and use the tool, do not blindly start a new service.
- First check whether the service is already running.
- If it is already running, tell the user you are reusing it and then open the page.
- If it is not running, tell the user you are starting the service, wait until it is ready, and then open the page.
- When the user wants a visual walkthrough, use a headed browser and maximize the window.
- When the app requires manual directory picking or other browser permissions, let the user complete that step and continue afterward.
- Do not claim to have saved or exported files unless the browser flow actually completed.
- If you create or modify a model only inside the automation session, explain clearly that the changes stay in that browser session until saved.

## Resources

- `scripts/launch-dbdesigner.ps1`: Start the local DBdesigner server, wait until it is reachable, and optionally open the browser.
- `references/install-prerequisites.md`: Windows support, local Node requirement, first-launch behavior, and what happens when the service is not running.
- `references/data-security.md`: Local data storage, AI-provider disclosure, API key handling, and Codex handoff file behavior.
- `references/marketplace-submission-checklist.md`: Final submission gate for marketplace release readiness.
- `references/icon-and-screenshot-checklist.md`: Icon, screenshot, and demo asset planning for marketplace submission.
- `references/usage.md`: Menu paths, shortcuts, supported databases, and task-oriented operating notes.
- `references/marketplace-copy.md`: Marketplace-facing listing copy, positioning, and concise selling points.
- `references/example-prompts.md`: Example user prompts and usage patterns for DB Craft.

## Guardrails

- Keep the skill thin. Do not copy the entire `D:\DBdesigner` app into the skill unless the user explicitly asks for a packaged clone.
- Reuse the existing app directory so future app updates remain effective without reworking the skill.
- If the user asks to change DBdesigner features, edit the source app under `D:\DBdesigner`, not the skill, unless the request is specifically about skill behavior.
