---
name: final-qa-launcher
description: Start dev server, generate QA checklist, guide manual verification. Use before creating PR.
---

# Final QA Launcher

Starts the dev server in tmux, generates a QA checklist from ticket and plan, and guides human through final manual verification.

## Prerequisites

- Code review complete
- All review items addressed
- Ready for final human verification

## Workflow

### 1. Determine Server Type

Ask the user:

```
Which dev server should I start?

A) pnpm dev - Standard (default)
B) pnpm dev:cloud - Cloud features
C) pnpm dev:electron - Electron features

(or specify custom command)
```

### 2. Start Dev Server

Use tmux to start the server in the background:

```bash
# Kill existing dev-server window if present
tmux list-windows 2>/dev/null | grep -q dev-server && tmux kill-window -t dev-server

# Create new window and start server
tmux new-window -n "dev-server" -d
tmux send-keys -t "dev-server" "cd {frontend-dir} && pnpm dev:cloud" C-m
```

Replace `{frontend-dir}` with the actual ComfyUI_frontend path.

### 3. Wait for Server Ready

Poll until the server is ready (look for localhost URL):

```bash
for i in {1..30}; do
  output=$(tmux capture-pane -p -t "dev-server")
  if echo "$output" | grep -qE "localhost:[0-9]+"; then
    break
  fi
  sleep 2
done
```

### 4. Print Server Info

Once ready, output:

```
✅ Dev server started

URL: http://localhost:5173 (or detected URL)

To view logs: tmux capture-pane -p -t "dev-server"
To stop: tmux kill-window -t "dev-server"
```

### 5. Generate QA Checklist

Load ticket.json and plan.md from the run directory. Create a checklist:

```markdown
# QA Checklist: {Ticket Title}

## Acceptance Criteria

(from ticket.json)

- [ ] {Criterion 1}
- [ ] {Criterion 2}

## Implementation Verification

(from plan.md)

- [ ] {Feature 1} works as expected
- [ ] {Feature 2} works as expected

## Standard Checks

- [ ] No console errors in browser DevTools
- [ ] No network errors in DevTools Network tab
- [ ] Responsive: works on desktop width
- [ ] Responsive: works on mobile width (if applicable)
- [ ] Keyboard navigation works (if applicable)
- [ ] Loading states display correctly
- [ ] Error states display correctly
- [ ] No visual regressions in related areas

## Edge Cases

- [ ] Empty state handled
- [ ] Error state handled
- [ ] Large data handled (if applicable)
- [ ] Concurrent actions handled (if applicable)

## Integration

- [ ] Feature works with rest of application
- [ ] No breaks in related features
```

### 6. Save & Present Checklist

Save to `{run-dir}/qa-checklist.md` and print to user:

```
Please verify each item manually in the browser.

When complete:
- "approved" - Continue to PR creation
- "issue: {description}" - Report an issue found
- "stop" - Stop for now, will continue later
```

### 7. Handle User Response

**If "approved":**

- Update `status.json`: set status to "pr-ready"
- Prompt: "Ready to create PR. Continue?"

**If "issue: {description}":**

- Log the issue
- Ask: "Fix now or note for later?"
- If fix now: return to implementation mode
- If note: add to known issues list in status.json

**If "stop":**

- Save current state
- Output: "State saved. Resume with 'final-qa-launcher' skill."

### 8. Cleanup

Ask:

```
Keep dev server running? (Y/n)
```

If no, run:

```bash
tmux kill-window -t "dev-server"
```

## File Locations

- Ticket: `{run-dir}/ticket.json`
- Plan: `{run-dir}/plan.md`
- QA Checklist: `{run-dir}/qa-checklist.md`
- Status: `{run-dir}/status.json`

## Notes

- Dev server startup typically takes 10-30 seconds
- Vite prints the URL when ready
- Keep checklist focused—don't overwhelm with items
- Standard checks apply to all tickets
- Acceptance criteria come directly from ticket.json
- Server persists across the QA session until explicitly stopped
