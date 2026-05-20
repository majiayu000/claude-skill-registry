---
name: playwright
description: Playwright browser automation via Playwright MCP
category: Testing-BDD
---

# Skill: playwright

## What I do

I provide expertise in Playwright browser automation via the Playwright MCP server. This includes navigation, form interaction, state snapshots, and debugging for reliable browser-based automation and testing.

## When to use me

- Automating browser-based workflows (navigation, filling forms, clicking)
- Taking page snapshots and screenshots for visual verification
- Interacting with complex web applications (dialogs, file uploads, drag-and-drop)
- Debugging browser state via console logs and network requests
- Managing browser tabs and resizing viewports

## Core principles

1. **Snapshot-first workflow** - Always take a snapshot (`browser_snapshot`) before interacting to get stable element references.
2. **Actionable references** - Prefer using element IDs or stable selectors from snapshots over brittle CSS paths.
3. **Wait for state** - Use `browser_wait_for` instead of arbitrary delays to ensure the UI is ready for interaction.
4. **Deterministic interaction** - Perform one action at a time and verify the result via a new snapshot or assertion.
5. **Clean cleanup** - Always close the browser session (`browser_close`) when the task is complete.

## Patterns & examples

**Stable interaction flow:**
```typescript
// 1. Navigate to target
await skill_mcp(mcp_name="playwright", tool_name="browser_navigate", arguments={ url: "https://example.com/login" });

// 2. Take snapshot to find element IDs
const snapshot = await skill_mcp(mcp_name="playwright", tool_name="browser_snapshot");

// 3. Fill form using IDs from snapshot
await skill_mcp(mcp_name="playwright", tool_name="browser_fill_form", arguments={ selector: "#email", value: "user@example.com" });
await skill_mcp(mcp_name="playwright", tool_name="browser_fill_form", arguments={ selector: "#password", value: "secret123" });
await skill_mcp(mcp_name="playwright", tool_name="browser_click", arguments={ selector: "button[type='submit']" });
```

**Waiting for results:**
```typescript
// Wait for specific element to appear after action
await skill_mcp(mcp_name="playwright", tool_name="browser_wait_for", arguments={ selector: ".dashboard-ready" });

// Verify state via console check or snapshot
const logs = await skill_mcp(mcp_name="playwright", tool_name="browser_console_messages");
```

## Anti-patterns to avoid

- ❌ Arbitrary time-based sleeps (use `browser_wait_for` instead)
- ❌ Interacting without a fresh snapshot (risks stale element references)
- ❌ Using brittle CSS/XPath selectors (prefer IDs or stable roles from snapshots)
- ❌ Leaving browser sessions open (always `browser_close` to save resources)
- ❌ Ignoring console errors or failed network requests when debugging

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Playwright.md`

## Related skills

- `javascript` - Core language for complex evaluation scripts
- `cypress` - Alternative browser testing framework
- `e2e-testing` - General end-to-end testing patterns
- `bdd-workflow` - Driving browser automation from behaviour specs
