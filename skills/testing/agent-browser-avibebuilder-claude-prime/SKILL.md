---
name: agent-browser
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Browser Automation with agent-browser

Use this skill to drive websites through the `agent-browser` CLI. Keep the main loop tight: inspect the page, act with refs, verify the result, and only pull deeper docs when the task actually needs them.

## Core workflow

Prefer `agent-browser` directly for speed. Use `npx agent-browser` only if it is not installed globally.

For most tasks, follow this loop:

1. Open the page
2. Wait for the relevant state
3. Snapshot with refs
4. Interact using those refs
5. Re-snapshot after page or DOM changes
6. Verify the outcome
7. Close the session when done

```bash
agent-browser open https://example.com/form
agent-browser wait --load networkidle
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Chain commands with `&&` only when you do not need to inspect intermediate output. Good: `open && wait && screenshot`. Bad: `snapshot && click` when you still need to read the refs from the snapshot.

## Route fast

Read only the reference that matches the task:

| Need | Read |
| --- | --- |
| Full command or flag lookup | [references/commands.md](references/commands.md) |
| Ref lifecycle, stale refs, snapshot strategy | [references/snapshot-refs.md](references/snapshot-refs.md) |
| Login flows, OAuth, 2FA, saved auth state | [references/authentication.md](references/authentication.md) |
| Parallel sessions, state reuse, cleanup | [references/session-management.md](references/session-management.md) |
| Recording, profiling, local files, config, iOS, security | [references/advanced-usage.md](references/advanced-usage.md) |
| Proxy setup | [references/proxy-support.md](references/proxy-support.md) |
| Recording workflows | [references/video-recording.md](references/video-recording.md) |
| Profiling workflows | [references/profiling.md](references/profiling.md) |

## Golden path commands

Use these first; go to the command reference only when you need something more specific.

```bash
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser select @e3 "option"
agent-browser get url
agent-browser get text @e1
agent-browser diff snapshot
agent-browser screenshot --annotate
agent-browser close
```

## Refs are the default interaction model

The main value of `agent-browser` is that snapshots produce compact refs like `@e1`, `@e2`, `@e3`. Those refs are cheaper and more reliable than repeatedly reasoning from raw HTML or long selectors.

Treat refs as short-lived. Re-snapshot after anything that can change the page state, especially:
- navigation
- form submission
- opening dropdowns or modals
- lazy-loaded or client-rendered content

If a ref fails or the page looks different from what you expected, your next move is usually `agent-browser snapshot -i`, not another blind click.

For the full lifecycle and troubleshooting rules, read [references/snapshot-refs.md](references/snapshot-refs.md).

## Choose the lightest tool that still proves the result

Default order:
1. `snapshot -i` for structure and interactive targets
2. `get text`, `get url`, or `get title` for precise verification
3. `diff snapshot` when you need to confirm something changed
4. `screenshot --annotate` when layout, icon-only controls, canvas, or visual context matters
5. semantic locators or `eval` only when refs are unavailable or the task truly needs them

If you need semantic locators, JavaScript evaluation, local file access, annotated screenshots, or config details, jump to [references/advanced-usage.md](references/advanced-usage.md) and [references/commands.md](references/commands.md).

## Authentication: decide sensitivity first

Before filling any credential, classify the auth flow.

- **Non-sensitive**: localhost, staging, test accounts, or credentials the user explicitly provided for this task. The agent can usually fill these directly.
- **Sensitive**: production domains, real user accounts, OAuth/SSO, or anything where the agent should not handle the secret. In that case, reach the auth step, switch to a headed browser if needed, and let the user complete sign-in manually.

After either path succeeds, offer to save reusable state if it would help next time. Do not auto-save credentials or session state without asking.

Use [references/authentication.md](references/authentication.md) for the exact decision rules and storage patterns.

## Sessions: isolate work on purpose

Use named sessions when you are:
- running parallel browser tasks
- comparing two sites or variants
- preserving auth state for reuse
- avoiding interference across agents

When multiple agents may browse concurrently, use a named session from the start and close it explicitly when finished. Prefer semantic names over generic ones.

For session reuse and cleanup patterns, read [references/session-management.md](references/session-management.md).

## Security defaults for AI-driven browsing

If the page is untrusted or may contain hostile content, enable content boundaries before inspecting rich output. If the task is scoped to a known target, consider an allowlist for trusted domains.

The main point is to keep page content clearly separated from tool output and to narrow where the browser is allowed to go when the task permits it.

See [references/advanced-usage.md](references/advanced-usage.md) for content boundaries, domain allowlists, action policy, and output limits.

## Failure modes to catch early

- **Stale refs**: you interacted after the page changed without re-snapshotting
- **Missing waits**: you captured or clicked before async content settled
- **Visual-only UI**: text snapshots missed icon buttons, canvas, or spatial layout
- **Shell quoting in `eval`**: use the safer patterns from the advanced usage reference
- **Leaked sessions**: you forgot to `close` the browser session after finishing

For worked examples and reusable flows, use the scripts in [templates/](templates/) and the deeper references instead of expanding the hub.
