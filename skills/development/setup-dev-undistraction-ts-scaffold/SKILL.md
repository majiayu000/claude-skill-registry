---
name: setup-dev
description: Set up Claude Code plugins, MCP servers, and verify the development environment for this project
user-invokable: true
disable-model-invocation: true
---

# setup-dev

Walk the user through setting up their Claude Code environment for this project. Run each step, report results, and only prompt the user if something fails.

## Step 1: Verify Node.js via nvm

This project uses nvm for Node version management. Check if nvm is installed:

```bash
command -v nvm
```

If nvm is not found, tell the user to install it from https://github.com/nvm-sh/nvm and then run `/setup-dev` again.

If nvm is available, run:

```bash
nvm install
nvm use
```

This reads the `.nvmrc` file (currently `v22`) and installs/activates the correct version. Confirm `node --version` shows v22.x.

## Step 2: Install npm dependencies

Check if `node_modules` exists. If not, run `npm install`.

## Step 3: Verify environment variables

Check if `.env` and `.env.test` exist and each contains `DATABASE_URL`. If missing, tell the user to:

1. Create a Neon project at https://neon.tech
2. Create a second database via the SQL Editor: `CREATE DATABASE scaffold_test;`
3. Copy `.env.example` to `.env` and fill in their values
4. Copy `.env.test.example` to `.env.test` and fill in the test database connection string

## Step 4: Install recommended Claude Code plugins

These plugins enhance Claude's capabilities for this project. Install each one:

```bash
claude plugins install code-review@claude-plugins-official
claude plugins install code-simplifier@claude-plugins-official
claude plugins install github@claude-plugins-official
claude plugins install playwright@claude-plugins-official
claude plugins install typescript-lsp@claude-plugins-official
claude plugins install commit-commands@claude-plugins-official
claude plugins install security-guidance@claude-plugins-official
claude plugins install claude-md-management@claude-plugins-official
claude plugins install pr-review-toolkit@claude-plugins-official
```

Run each command. If a plugin is already installed, that's fine — move on. Report a summary at the end of how many were newly installed vs already present.

## Step 5: Verify MCP servers

Run `claude mcp list` and confirm `context7` is present. If missing, install it:

```bash
claude mcp add context7 -- npx -y @upstreamapi/context7-mcp@latest
```

Also check for `next-devtools` MCP server. If missing, install it:

```bash
claude mcp add next-devtools -- npx -y next-devtools-mcp@latest
```

## Step 6: Push schema to databases

Run `npm run db:push && npm run db:push:test` to ensure both Neon databases have the latest schema.

## Step 7: Run verification checks

Run these commands and report results:

1. `npm run lint` — ESLint + Prettier pass
2. `npm run types:check` — TypeScript compiles
3. `npm run test:vitest:no-watch` — All tests pass
4. `npm run build` — Next.js production build succeeds

## Output

End with a summary table:

```
| Check              | Status |
|--------------------|--------|
| nvm + Node >= 22   | ...    |
| npm dependencies   | ...    |
| .env                     | ...    |
| .env.test          | ...    |
| Plugins (N of 9)   | ...    |
| context7 MCP       | ...    |
| next-devtools MCP  | ...    |
| DB schema push     | ...    |
| Lint               | ...    |
| Type check         | ...    |
| Tests              | ...    |
| Build              | ...    |
```

If everything passed, tell the user they're ready to go. Then run the `/claude-tooling` skill to show them all available skills, agents, plugins, MCP servers, and hooks in this project.
