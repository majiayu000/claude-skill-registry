---
name: reproduce-bug
description: Reproduce and investigate a bug using logs, console inspection, and browser screenshots
---

## Arguments
[GitHub issue number]

# Reproduce Bug Command

Look at github issue #$ARGUMENTS and read the issue description and comments.

## Phase 1: Log Investigation

Run the following skills in parallel to investigate the bug:

**placeholder for future.  Skip for now**

Think about the places it could go wrong looking at the codebase. Look for logging output we can look for.

Run the agents again to find any logs that could help us reproduce the bug.

Keep running these agents until you have a good idea of what is going on.

## Phase 2: Visual Reproduction with agent-browser

If the bug is UI-related or involves user flows, use agent-browser CLI to visually reproduce it.

### Step 1: Verify Server is Running

```bash
agent-browser open http://localhost:3000
agent-browser snapshot -i
```

If server not running, inform user to start `bin/dev`.

### Step 2: Navigate to Affected Area

Based on the issue description, navigate to the relevant page:

```bash
agent-browser open http://localhost:3000/[affected_route]
agent-browser snapshot -i
```

### Step 3: Capture Screenshots

Take screenshots at each step of reproducing the bug:

```bash
agent-browser screenshot bug-[issue]-step-1.png
```

### Step 4: Follow User Flow

Reproduce the exact steps from the issue:

1. **Read the issue's reproduction steps**
2. **Execute each step using agent-browser:**
   - `agent-browser click @e1` for clicking elements (refs from snapshot)
   - `agent-browser fill @e1 "text"` for filling forms
   - `agent-browser snapshot -i` to see the current state
   - `agent-browser screenshot filename.png` to capture evidence

3. **Re-snapshot after each interaction** to get updated refs

### Step 5: Capture Bug State

When you reproduce the bug:

1. Take a screenshot of the bug state
2. Document the exact steps that triggered it

```bash
agent-browser screenshot bug-[issue]-reproduced.png
```

## Phase 3: Document Findings

**Reference Collection:**

- [ ] Document all research findings with specific file paths (e.g., `app/services/example_service.rb:42`)
- [ ] Include screenshots showing the bug reproduction
- [ ] List console errors if any
- [ ] Document the exact reproduction steps

## Phase 4: Report Back

Add a comment to the issue with:

1. **Findings** - What you discovered about the cause
2. **Reproduction Steps** - Exact steps to reproduce (verified)
3. **Screenshots** - Visual evidence of the bug (upload captured screenshots)
4. **Relevant Code** - File paths and line numbers
5. **Suggested Fix** - If you have one
