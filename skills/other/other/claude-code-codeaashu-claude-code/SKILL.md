---
name: claude-code-skill
description: Development conventions and architecture guide for the Claude Code CLI repository.
---

# Claude Code — Repository Skill

## Project Overview

Claude Code is Anthropic's CLI tool for interacting with Claude from the terminal. It supports file editing, shell commands, git workflows, code review, multi-agent coordination, IDE integration (VS Code, JetBrains), and Model Context Protocol (MCP).

**Codebase:** ~1,900 files, 512,000+ lines of TypeScript under `src/`.

## Tech Stack

| Component        | Technology                                      |
|------------------|------------------------------------------------|
| Language         | TypeScript (strict mode, ES modules)           |
| Runtime          | Bun (JSX support, `bun:bundle` feature flags)  |
| Terminal UI      | React + Ink (React for CLI)                    |
| CLI Parser       | Commander.js (`@commander-js/extra-typings`)   |
| API Client       | `@anthropic-ai/sdk`                            |
| Validation       | Zod v4                                         |
| Linter/Formatter | Biome                                          |
| Analytics        | GrowthBook (feature flags & A/B testing)       |
| Protocol         | Model Context Protocol (MCP)                   |

## Architecture

### Directory Map (`src/`)

| Directory        | Purpose                                                         |
|------------------|-----------------------------------------------------------------|
| `commands/`      | ~50 slash commands (`/commit`, `/review`, `/config`, etc.)      |
| `tools/`         | ~40 agent tools (Bash, FileRead, FileWrite, Glob, Grep, etc.)  |
| `components/`    | ~140 Ink/React UI components for terminal rendering             |
| `services/`      | External integrations (API, OAuth, MCP, LSP, analytics, plugins)|
| `bridge/`        | Bidirectional IDE communication layer                           |
| `state/`         | React context + custom store (AppState)                         |
| `hooks/`         | React hooks (permissions, keybindings, commands, settings)      |
| `types/`         | TypeScript type definitions                                     |
| `utils/`         | Utilities (shell, file ops, permissions, config, git)           |
| `screens/`       | Full-screen UIs (Doctor, REPL, Resume, Compact)                 |
| `skills/`        | Bundled skills + skill loader system                            |
| `plugins/`       | Plugin system (marketplace + bundled plugins)                   |
| `coordinator/`   | Multi-agent coordination & supervisor logic                     |
| `tasks/`         | Task management (shell tasks, agent tasks, teammates)           |
| `context/`       | React context providers (notifications, stats, FPS)             |
| `memdir/`        | Persistent memory system (CLAUDE.md, user/project memory)       |
| `entrypoints/`   | Initialization logic, Agent SDK, MCP entry                      |
| `voice/`         | Voice input/output (STT, keyterms)                              |
| `vim/`           | Vim mode keybinding support                                     |
| `schemas/`       | Zod configuration schemas                                       |
| `keybindings/`   | Keybinding configuration & resolver                             |
| `migrations/`    | Config migrations between versions                              |
| `outputStyles/`  | Output formatting & theming                                     |
| `query/`         | Query pipeline & processing                                     |
| `server/`        | Server/daemon mode                                              |
| `remote/`        | Remote session handling                                         |

### Key Files

| File                | Role                                                |
|---------------------|-----------------------------------------------------|
| `src/main.tsx`      | CLI entry point (Commander parser, startup profiling)|
| `src/QueryEngine.ts`| Core LLM API caller (streaming, tool-call loops)    |
| `src/Tool.ts`       | Tool type definitions & `buildTool` factory          |
| `src/tools.ts`      | Tool registry & presets                              |
| `src/commands.ts`   | Command registry                                     |
| `src/context.ts`    | System/user context collection (git status, memory)  |
| `src/cost-tracker.ts`| Token cost tracking                                 |

### Entry Points & Initialization Sequence

1. `src/main.tsx` — Commander CLI parser, startup profiling
2. `src/entrypoints/init.ts` — Config, telemetry, OAuth, MDM
3. `src/entrypoints/cli.tsx` — CLI session orchestration
4. `src/entrypoints/mcp.ts` — MCP server mode
5. `src/entrypoints/sdk/` — Agent SDK (programmatic API)
6. `src/replLauncher.tsx` — REPL session launcher

Startup performs parallel initialization: MDM policy reads, Keychain prefetch, feature flag checks, then core init.

## Patterns & Conventions

### Tool Definition

Each tool lives in `src/tools/{ToolName}/` and uses `buildTool`:

```typescript
export const MyTool = buildTool({
  name: 'MyTool',
  aliases: ['my_tool'],
  description: 'What this tool does',
  inputSchema: z.object({
    param: z.string(),
  }),
  async call(args, context, canUseTool, parentMessage, onProgress) {
    // Execute and return { data: result, newMessages?: [...] }
  },
  async checkPermissions(input, context) { /* Permission checks */ },
  isConcurrencySafe(input) { /* Can run in parallel? */ },
  isReadOnly(input) { /* Non-destructive? */ },
  prompt(options) { /* System prompt injection */ },
  renderToolUseMessage(input, options) { /* UI for invocation */ },
  renderToolResultMessage(content, progressMessages, options) { /* UI for result */ },
})
```

**Directory structure per tool:** `{ToolName}.ts` or `.tsx` (main), `UI.tsx` (rendering), `prompt.ts` (system prompt), plus utility files.

### Command Definition

Commands live in `src/commands/` and follow three types:

- **PromptCommand** — Sends a formatted prompt with injected tools (most commands)
- **LocalCommand** — Runs in-process, returns text
- **LocalJSXCommand** — Runs in-process, returns React JSX

```typescript
const command = {
  type: 'prompt',
  name: 'my-command',
  description: 'What this command does',
  progressMessage: 'working...',
  allowedTools: ['Bash(git *)', 'FileRead(*)'],
  source: 'builtin',
  async getPromptForCommand(args, context) {
    return [{ type: 'text', text: '...' }]
  },
} satisfies Command
```

Commands are registered in `src/commands.ts` and invoked via `/command-name` in the REPL.

### Component Structure

- Functional React components with Ink primitives (`Box`, `Text`, `useInput()`)
- Styled with Chalk for terminal colors
- React Compiler for optimized re-renders
- Design system primitives in `src/components/design-system/`

### State Management

- `AppState` via React context + custom store (`src/state/AppStateStore.ts`)
- Mutable state object passed to tool contexts
- Selector functions for derived state
- Change observers in `src/state/onChangeAppState.ts`

### Permission System

- **Modes:** `default` (prompt per operation), `plan` (show plan, ask once), `bypassPermissions` (auto-approve), `auto` (ML classifier)
- **Rules:** Wildcard patterns — `Bash(git *)`, `FileEdit(/src/*)`
- Tools implement `checkPermissions()` returning `{ granted: boolean, reason?, prompt? }`

### Feature Flags & Build

Bun's `bun:bundle` feature flags enable dead-code elimination at build time:

```typescript
import { feature } from 'bun:bundle'
if (feature('PROACTIVE')) { /* proactive agent tools */ }
```

Notable flags: `PROACTIVE`, `KAIROS`, `BRIDGE_MODE`, `VOICE_MODE`, `COORDINATOR_MODE`, `DAEMON`, `WORKFLOW_SCRIPTS`.

Some features are also gated via `process.env.USER_TYPE === 'ant'`.

## Naming Conventions

| Element      | Convention           | Example                          |
|-------------|---------------------|----------------------------------|
| Files       | PascalCase (exports) or kebab-case (commands) | `BashTool.tsx`, `commit-push-pr.ts` |
| Components  | PascalCase           | `App.tsx`, `PromptInput.tsx`     |
| Types       | PascalCase, suffix with Props/State/Context | `ToolUseContext`     |
| Hooks       | `use` prefix         | `useCanUseTool`, `useSettings`   |
| Constants   | SCREAMING_SNAKE_CASE | `MAX_TOKENS`, `DEFAULT_TIMEOUT_MS`|

## Import Practices

- ES modules with `.js` extensions (Bun convention)
- Lazy imports for circular dependency breaking: `const getModule = () => require('./heavy.js')`
- Conditional imports via feature flags or `process.env`
- `biome-ignore` markers for manual import ordering where needed

## Services

| Service             | Path                          | Purpose                           |
|--------------------|-------------------------------|-----------------------------------|
| API                | `services/api/`               | Anthropic SDK client, file uploads|
| MCP                | `services/mcp/`               | MCP client, tool/resource discovery|
| OAuth              | `services/oauth/`             | OAuth 2.0 auth flow               |
| LSP                | `services/lsp/`               | Language Server Protocol manager   |
| Analytics          | `services/analytics/`         | GrowthBook, telemetry, events     |
| Plugins            | `services/plugins/`           | Plugin loader, marketplace         |
| Compact            | `services/compact/`           | Context compression                |
| Policy Limits      | `services/policyLimits/`      | Org rate limits, quota checking    |
| Remote Settings    | `services/remoteManagedSettings/` | Managed settings sync (Enterprise) |
| Token Estimation   | `services/tokenEstimation.ts` | Token count estimation             |

## Configuration

**Settings locations:**
- **Global:** `~/.claude/config.json`, `~/.claude/settings.json`
- **Project:** `.claude/config.json`, `.claude/settings.json`
- **System:** macOS Keychain + MDM, Windows Registry + MDM
- **Managed:** Remote sync for Enterprise users

## Guidelines

1. Read relevant source files before making changes — understand existing patterns first.
2. Follow the tool/command/component patterns above when adding new ones.
3. Keep edits minimal and focused — avoid unnecessary refactoring.
4. Use Zod for all input validation at system boundaries.
5. Gate experimental features behind `bun:bundle` feature flags or env checks.
6. Respect the permission system — tools that modify state must implement `checkPermissions()`.
7. Use lazy imports when adding dependencies that could create circular references.
8. Update this file as project conventions evolve.


