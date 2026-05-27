---
name: preview
description: "Stand up the project's live app and hand it to the user to try a change firsthand, then gate on their verdict before continuing. Use when the user asks to \"preview the change\", \"let me try it\", \"spin up the app so I can test it\", \"set it up so I can poke at it\", or before finalizing a UI/UX change that needs human eyes."
---

# Preview

Bring up the running app and let the user drive it themselves to judge the change, then act on their verdict.

## Step 1: Determine Scope

Resolve what to preview using the first match:

1. **User-specified** — the user says what to look at. Use that.
2. **PR** — a PR URL or number is provided. Fetch its details and read the changed code.
3. **Conversation context** — prior conversation contains recent work. Extract what changed, where it lives, and the expected behavior.
4. **App-level discovery** — fresh context with no prior work. Examine entry points, routes, and the README to identify the app's core user-facing flows.

If the resolved scope has no user-visible surface to try (a CLI-only change, a library with no entry point, backend work with no UI to look at), present this message: "Nothing to preview — <one-line reason>." Then use the TaskList tool and proceed to any remaining task.

## Step 2: Determine Launch Approach

Check for a project-specific skill or MCP tool that launches the app, and use it if present. Otherwise use the fallback for the surface type:

- **Web app** → start the dev server; the access point is the local URL and port
- **Desktop/native app** → build and launch the app so its window is open

## Step 3: Bring Up the Stack

Start backend services and frontend together — a frontend-only change still needs the backend running to be exercised. Build first if the project requires a build step.

Start long-running processes with the Bash tool (`run_in_background: true`) and wait until each reports ready. Tail their logs with the Monitor tool so backend errors and warnings surface while the user is trying the app.

If a required service cannot be stood up in this session (missing auth provider, external dependency, seed data), or a process fails to start or never reports ready, use `AskUserQuestion` to surface the blocker and let the user choose how to proceed.

## Step 4: Point the User at the Running App

Output as text:

- The access point — the local URL and port for a web app, or confirmation that the window is open for a native app
- What changed and where to look
- Any specific interaction worth checking

## Step 5: Verdict Gate

Use `AskUserQuestion` to ask the user for their verdict after they have tried the app. Two options:

- **Looks good** — stop every process this skill started.
- **Needs changes** — note what the user wants different, make the change, rebuild or refresh the running app so it is live, then repeat this step's gate.

Then use the TaskList tool and proceed to any remaining task.
