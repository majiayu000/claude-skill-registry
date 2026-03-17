---
name: design-phase
description: >
  Use when needing to plan and design a product before writing implementation
  code. Sets up a standalone Design OS workspace.
user-invocable: true
allowed-tools: Bash, Write, Read, Glob
argument-hint: ~/repos/my-app-design
---

# Design Phase: Design OS Workspace

Sets up a standalone [Design OS](https://github.com/buildermethods/design-os) workspace for product planning and UI design. This is a **separate project** from your implementation codebase — design first, then scaffold your real project with `/scaffold`.

**When to use:** Any product (greenfield or existing) where you want to plan vision, data model, and UI before implementation.

## Input

`$ARGUMENTS` = absolute or relative path for the design workspace (e.g., `~/repos/my-app-design`).

**Validation:** If `$ARGUMENTS` is empty or missing, STOP with error: "Usage: /design-phase <workspace-path>"

Expand `~` to the user's home directory. Resolve relative paths against the current working directory.

If the target directory already exists AND contains a `package.json`, STOP: "Design workspace already exists at {path}. Run `cd {path} && npm run dev` to resume."

## Steps

### 1. Clone Design OS

```bash
git clone https://github.com/buildermethods/design-os.git {path}
```

If clone fails, verify network connectivity and that the repo exists at https://github.com/buildermethods/design-os.

### 2. Detach from upstream

```bash
cd {path} && git remote remove origin
```

This makes the workspace yours — no accidental pushes to the Design OS repo.

### 3. Install dependencies

```bash
cd {path} && npm install
```

### 4. Start dev server

```bash
cd {path} && npm run dev &
DEV_PID=$!
```

Run in background. The dev server listens on **port 3000**.

Wait for the server to be ready before verifying:
```bash
for i in $(seq 1 10); do curl -s -o /dev/null http://localhost:3000 && break || sleep 1; done
```

**If port 3000 is already in use:** kill the conflicting process or change the port in `{path}/vite.config.ts`.

**To stop the server later:** `kill $DEV_PID` or `lsof -ti:3000 | xargs kill`.

### 5. Report ready

After the dev server starts, report:

> Design workspace ready at {path}. Open http://localhost:3000. Start with `/product-vision`.

Then print the workflow quick-reference below.

## Self-Verify Gate

After completing all steps, verify EVERY item. If ANY fails, fix before reporting success.

- [ ] Directory `{path}` exists
- [ ] `{path}/node_modules` exists (npm install succeeded)
- [ ] Dev server responding on port 3000

**Verification commands:**
```bash
test -d {path} && echo "PASS: workspace dir" || echo "FAIL: workspace dir"
test -d {path}/node_modules && echo "PASS: node_modules" || echo "FAIL: node_modules"
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200" && echo "PASS: dev server" || echo "FAIL: dev server"
```

All 3 gates must pass before reporting success.

## Design OS Workflow Quick-Reference

Print this after successful setup so the user knows the full design flow.

**These commands are provided by Design OS** (in the workspace's `.claude/commands/`), not saurun skills. Run them from within the design workspace.

### Phase 1 — Product Planning

| Command | Purpose |
|---------|---------|
| `/product-vision` | Define what you're building, split into sections, shape your data |
| `/design-tokens` | Choose colors and typography |
| `/design-shell` | Design navigation and layout |

### Phase 2 — Section Design (repeat per section)

| Command | Purpose |
|---------|---------|
| `/shape-section` | Define scope and requirements for one section |
| `/sample-data` | Generate realistic sample data + TypeScript types |
| `/design-screen` | Build the actual React components |

### Phase 3 — Export

| Command | Purpose |
|---------|---------|
| `/export-product` | Generate complete handoff package |

**After export:** `/export-product` generates a handoff directory with React components, TypeScript types, and design specs. Use `/scaffold` to create your implementation project, then copy the exported artifacts into it.
