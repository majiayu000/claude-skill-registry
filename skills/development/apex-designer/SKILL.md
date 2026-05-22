---
name: apex-designer
description: Apex Designer DSL project workflow. Use when creating or modifying design files, running ad3 commands, or working with the DSL.
---

# Apex Designer

Apex Designer is a low-code platform for building full-stack applications. Projects are defined using a TypeScript DSL in the `/design` directory. The server code (`/server`), client code (`/client`), and documentation (`/docs`) are all generated from the design files and should not be edited directly.

## Design Artifacts

All design artifacts are TypeScript files in the `/design` directory using the Apex Designer DSL. Read the relevant doc before creating or modifying a design type:

| Design Type | Description | Doc |
|---|---|---|
| Business Object | Core entity classes with properties and relationships | `node_modules/@apexdesigner/dsl/docs/business-objects.md` |
| Behavior | Custom logic for business objects | `node_modules/@apexdesigner/dsl/docs/behaviors.md` |
| App Behavior | Application-level server logic | `node_modules/@apexdesigner/dsl/docs/app-behaviors.md` |
| App Properties | Server-side singleton state (caches, clients) | `node_modules/@apexdesigner/dsl/docs/app-properties.md` |
| Agent | AI-powered participants for processes | `node_modules/@apexdesigner/dsl/docs/agents.md` |
| Base Type | Type wrappers with validation constraints | `node_modules/@apexdesigner/dsl/docs/base-types.md` |
| Component | Reusable UI elements | `node_modules/@apexdesigner/dsl/docs/components.md` |
| Component Interface | Template API for Angular components | `node_modules/@apexdesigner/dsl/docs/component-interfaces.md` |
| Data Flow | Computation with dependency-based execution | `node_modules/@apexdesigner/dsl/docs/data-flows.md` |
| Data Source | Persistence layer for business objects | `node_modules/@apexdesigner/dsl/docs/data-sources.md` |
| Decision Table | Business rules evaluator | `node_modules/@apexdesigner/dsl/docs/decision-tables.md` |
| Directive Interface | Template API for Angular directives | `node_modules/@apexdesigner/dsl/docs/directive-interfaces.md` |
| External Type | Importable types from libraries | `node_modules/@apexdesigner/dsl/docs/external-types.md` |
| Function | Reusable callable utilities (client, server, or both) | `node_modules/@apexdesigner/dsl/docs/functions.md` |
| Interface Definition | Non-persisted data shapes for typed parameters | `node_modules/@apexdesigner/dsl/docs/interface-definitions.md` |
| Mixin | Reusable properties for business objects | `node_modules/@apexdesigner/dsl/docs/mixins.md` |
| Page | Routable views in the application | `node_modules/@apexdesigner/dsl/docs/pages.md` |
| Persistence | Override default table/storage naming | `node_modules/@apexdesigner/dsl/docs/persistence.md` |
| Pipe Interface | Template pipes for filter syntax | `node_modules/@apexdesigner/dsl/docs/pipe-interfaces.md` |
| Process | Workflow defined as class methods | `node_modules/@apexdesigner/dsl/docs/processes.md` |
| Project | Application settings and dependencies | `node_modules/@apexdesigner/dsl/docs/project.md` |
| Role | Access control for objects and pages | `node_modules/@apexdesigner/dsl/docs/roles.md` |
| Service | Shared injectable logic | `node_modules/@apexdesigner/dsl/docs/services.md` |
| Template | Markup for pages and components | `node_modules/@apexdesigner/dsl/docs/templates.md` |
| Test Fixture | Reusable test data setup functions | `node_modules/@apexdesigner/dsl/docs/test-fixtures.md` |
| Validator | Source file checkers with auto-fix | `node_modules/@apexdesigner/dsl/docs/validators.md` |

## Libraries

Libraries provide reusable design assets, client and server npm packages, and code generators.
Read the library README for available components, patterns, and conventions.
This project includes the following libraries:

- **@apexdesigner/doc-generators** — Design documentation generators for Apex Designer projects (see `design/node_modules/@apexdesigner/doc-generators/README.md`)

If you discover a useful pattern or convention while working with this project, suggest adding it to the library documentation so it can benefit other projects.

If this project is itself a library, see `.claude/skills/apex-designer/docs/library-development.md` for library-specific patterns.

## Workflow

1. Read the relevant doc before creating or modifying a design type
2. Create or edit design files in `design/` — use the Write tool to create new files (it auto-creates directories)
3. A validation hook runs automatically after Edit/Write to `design/` files (via `.claude/skills/apex-designer/scripts/resolve.cjs`) — it checks for errors but does not auto-fix
4. After completing a set of related edits, run `ad3 resolve` to auto-fix issues (adds inverse relationships, foreign keys, etc.) and regenerate code
5. If diagnostics remain after resolve, stop and ask the user for help — do not attempt workarounds
6. `ad3` is installed globally — do not use `npx`
7. After deleting a design file, run `ad3 resolve` manually — the hook only triggers on Edit/Write, not file deletions

### What resolve adds automatically

You don't need to include these in design files — resolve will add them automatically:
- `id` property
- Foreign key properties (e.g., `locationId` for a `location` belongs-to relationship)
- Inverse relationships (e.g., `contacts?: Contact[]` on Location when Contact has `location?: Location`)

`ad3 resolve` handles the full validate/fix/generate cycle, looping until stable. No manual `ad3 gen` steps are needed.

### Static files

Files placed in `design/client/` or `design/server/` are copied into the corresponding generated directory using the same relative path. For example, `design/client/assets/logo.png` is copied to `client/assets/logo.png`. Use this for assets, configuration files, or any file that should be included in the generated output without modification.

**Warning: Do not use static files to override generated files.** If a static file has the same path as a generated file, the static file wins and the generator is blocked. This produces a warning during `ad3 gen`:

```
W: server/src/index.ts - Static file overrides generator "server" output
```

Overriding generated files is a last-resort workaround that creates maintenance burden — the static copy won't receive generator improvements or bug fixes. The better approach is to request changes to the generator so the generated output meets your needs directly.

## Design Documentation

Each concept directory in `/design` must have a markdown file documenting its design assets (e.g., `process-design/process-design.md`). The root `/design/design.md` file provides a map of all concept directories. All design artifacts must be referenced by at least one `.md` file in the design directory. See `.claude/skills/apex-designer/docs/design-docs-style.md` for the style guide covering structure, linking conventions, and formatting patterns.

## AD2 Migration

See `.claude/skills/apex-designer/docs/ad2-migration.md` for pulling AD2 design data and migrating to AD3.

## CLI

See `.claude/skills/apex-designer/docs/cli.md` for the full ad3 command reference.

Key commands:
- `ad3 resolve` — validate and auto-fix (includes validation, no need for separate `ad3 val`)
- `ad3 gen` — generate code from design files
- `ad3 stop` / `ad3 start` — manage the ad3 server
- Any ad3 command starts the server if it isn't already running

## API CLI

The API CLI script makes authenticated requests to the running server. It handles OIDC login, token caching/refresh, and API calls.

```bash
# Login (opens browser for OIDC authentication)
npx api login

# Make API requests
npx api get /api/candidates
npx api post /api/candidates '{"name":"Alice"}'
npx api delete /api/candidates/123

# Impersonate a user
npx api --as user@example.com get /api/items

# Logout
npx api logout
```

Tokens are cached in `.api.json` at the project root. The callback port range (default 3100-3149) can be customized there:
```json
{ "callbackPorts": [3100, 3149] }
```

The server must be running before login. The script reads the server port from `.workspace.json` or defaults to 3000.

## Rules

- **Simple commands only** — Don't chain commands with `&&` or `;`. Run each `ad3` command as a separate Bash call. Compound commands trigger approval prompts.
- **Don't edit generated code** — Never edit files in `/server`, `/client`, or `/docs/design`. These are generated and will be overwritten. Only edit files in `/design`.
- **No `git -C`** — Don't use `git -C <path>`. Run git commands from the current working directory. The `-C` flag triggers approval prompts.
- **No `cd` with commands** — Don't combine `cd <path> && command` or `cd <path>; command`. If you need to verify the working directory, run `pwd` as a separate step, then run the command on its own.

## Dev Server

See `.claude/skills/apex-designer/docs/dev-sh.md` for usage. The script is at `.claude/skills/apex-designer/scripts/dev.sh` (relative to the project root).

- `bash .claude/skills/apex-designer/scripts/dev.sh` — starts server and client in background, then exits
- `bash .claude/skills/apex-designer/scripts/dev.sh --server-only` — starts only the server (faster, useful for API testing)
- `bash .claude/skills/apex-designer/scripts/dev.sh --stop` — stops all dev processes
- `bash .claude/skills/apex-designer/scripts/dev.sh --debug "AppName:*"` — enables debug output
- Running it again automatically kills existing processes on the ports
- Fire-and-forget: the server uses `tsx --watch` and will auto-restart as files change. If startup fails or times out, check `logs/server.log` and fix the issue (e.g., run `ad3 gen`) — do NOT re-run dev.sh
- Ports can be pinned per project via `.workspace.json`:
  ```json
  { "ports": { "server": 3000, "client": 4200 } }
  ```
  Priority: `.workspace.json` → `PORT`/`CLIENT_PORT` env vars → defaults (3000/4200)
