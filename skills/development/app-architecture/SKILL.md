---
name: app-architecture
description: Create apps following contract-port architecture with composition roots. Use when creating new apps in apps/, scaffolding CLI tools, setting up dependency injection, or when the user asks about app structure, entrypoints, or platform-agnostic design.
---

# App Architecture

Apps mirror the package architecture - they should be platform-agnostic outside of the entrypoint where ports are assembled with platform-specific globals.

## Core Principle

**Assemble all ports at the top level (composition root), then feed them down to individual modules.**

```
┌─────────────────────────────────────────────────────────────┐
│                     Entry Point (cli.ts)                    │
│                  Parse args, call composition root          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Composition Root                         │
│                    (composition.ts)                         │
│         Inject platform globals → Create ports → Return     │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │   Module A  │   │   Module B  │   │   Module C  │
  │ (no globals)│   │ (no globals)│   │ (no globals)│
  └─────────────┘   └─────────────┘   └─────────────┘
```

## File Structure

```
apps/{app-name}/
├── src/
│   ├── cli.ts              # Entry point (thin) - only parses args, calls composition
│   ├── composition.ts      # Composition root - assembles all ports
│   ├── types.ts            # App-specific types
│   ├── errors.ts           # Error classes (extend ConveauxError)
│   └── {domain}.ts         # Domain modules - platform-agnostic
├── CLAUDE.md               # Inline instructions for this app
├── README.md               # User documentation
├── package.json
└── tsconfig.json
```

## Composition Root Pattern

The composition root is the ONLY place where platform globals appear:

```typescript
// composition.ts
import type { Env } from '@scope/contract-env';
import type { Logger } from '@scope/contract-logger';
import type { WallClock } from '@scope/contract-wall-clock';
import type { EphemeralScheduler } from '@scope/contract-ephemeral-scheduler';

import { createEnv, createShellEnvSource, createStaticEnvSource } from '@scope/port-env';
import { createEphemeralScheduler } from '@scope/port-ephemeral-scheduler';
import { createLogger, createJsonFormatter, createPrettyFormatter } from '@scope/port-logger';
import { createOutChannel } from '@scope/port-outchannel';
import { createWallClock } from '@scope/port-wall-clock';

// Define what deps the app needs
export interface RuntimeDeps {
  readonly logger: Logger;
  readonly clock: WallClock;
  readonly env: Env;
  readonly scheduler: EphemeralScheduler;
}

export interface RuntimeOptions {
  readonly json?: boolean;
  readonly verbose?: boolean;
}

// Factory that creates all deps - platform globals only appear HERE
export function createRuntimeDeps(options: RuntimeOptions = {}): RuntimeDeps {
  // Inject platform globals into ports
  const clock = createWallClock({ Date });

  const scheduler = createEphemeralScheduler({
    setTimeout: globalThis.setTimeout,
    clearTimeout: globalThis.clearTimeout,
    setInterval: globalThis.setInterval,
    clearInterval: globalThis.clearInterval,
  });

  const logChannel = createOutChannel(process.stderr);

  const formatter = options.json
    ? createJsonFormatter()
    : createPrettyFormatter({ colors: process.stderr.isTTY ?? false });

  const logger = createLogger({
    Date,
    channel: logChannel,
    clock,
    options: { formatter, minLevel: options.verbose ? 'debug' : 'info' },
  });

  const env = createEnv({
    sources: [
      createShellEnvSource(
        { getEnv: (name) => process.env[name] },
        { name: 'shell', priority: 100 }
      ),
      createStaticEnvSource(
        { DEFAULT_TIMEOUT: '30' },
        { name: 'defaults', priority: 0 }
      ),
    ],
  });

  return { logger, clock, env, scheduler };
}
```

## Entry Point Pattern

The entry point should be thin - just parse args and call composition:

```typescript
// cli.ts
#!/usr/bin/env node

import type { Logger } from '@scope/contract-logger';
import { Command } from 'commander';
import { createRuntimeDeps } from './composition.js';
import { runApp } from './app.js';
import { createClient } from './client.js';

const program = new Command();

program
  .name('my-app')
  .action(async (options: CliOptions) => {
    // 1. Create all deps at the top level
    const deps = createRuntimeDeps({
      json: options.json,
      verbose: options.verbose,
    });
    const { logger, clock, env, scheduler } = deps;

    // 2. Create app-specific services, passing deps down
    const client = createClient({ logger, clock });

    // 3. Run the app, passing deps down
    const result = await runApp({ logger, clock, client, scheduler }, config);

    console.log(JSON.stringify(result, null, 2));
    process.exit(EXIT_CODES[result.status]);
  });

program.parse();
```

## Domain Module Pattern

Domain modules receive deps via injection - they never use globals:

```typescript
// client.ts
import type { Logger } from '@scope/contract-logger';
import type { WallClock } from '@scope/contract-wall-clock';

// Define what deps THIS module needs (subset of RuntimeDeps)
export interface ClientDeps {
  readonly logger: Logger;
  readonly clock: WallClock;
}

// Interface for what this module provides
export interface Client {
  fetch(url: string): Promise<Response>;
}

// Factory receives deps, returns implementation
export function createClient(deps: ClientDeps): Client {
  const { logger, clock } = deps;

  return {
    async fetch(url: string) {
      const startTime = clock.nowMs();  // Use injected clock, not Date.now()
      logger.debug('Fetching', { url });

      // ... implementation

      const durationMs = clock.nowMs() - startTime;
      logger.debug('Fetched', { url, durationMs });
      return response;
    }
  };
}
```

## Checklist for Creating Apps

### Composition Root
- [ ] Single `composition.ts` file that creates all runtime deps
- [ ] Platform globals (Date, setTimeout, process.env) only appear here
- [ ] Exports `RuntimeDeps` interface and `createRuntimeDeps` factory
- [ ] Options (json, verbose) are separate from deps

### Entry Point
- [ ] Thin `cli.ts` - only arg parsing and wiring
- [ ] Calls `createRuntimeDeps()` once at the top
- [ ] Passes deps down to all modules
- [ ] Handles errors with proper exit codes

### Domain Modules
- [ ] Each module defines its own `*Deps` interface
- [ ] Deps interface only includes contracts the module needs
- [ ] No direct use of globals (Date.now, console, process.env)
- [ ] Factory pattern: `createX(deps): X`

### Types
- [ ] `types.ts` for shared app-specific types
- [ ] Config types separate from deps types
- [ ] Exit codes as const object

### Errors
- [ ] `errors.ts` with classes extending `UserError` or `RetryableError`
- [ ] Actionable error messages with guidance
- [ ] Use `getExitCode()` for proper exit codes

## Common Deps by Use Case

| Need | Contract | Port |
|------|----------|------|
| Current time | `contract-wall-clock` | `port-wall-clock` |
| Logging | `contract-logger` | `port-logger` |
| Environment vars | `contract-env` | `port-env` |
| Delays/timers | `contract-ephemeral-scheduler` | `port-ephemeral-scheduler` |
| Writing output | `contract-outchannel` | `port-outchannel` |
| Error handling | `contract-control-flow` | `port-control-flow` |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `Date.now()` in module | Hidden platform dependency | Inject `WallClock` |
| `setTimeout()` in module | Untestable timing | Inject `EphemeralScheduler` |
| `process.env.X` in module | Hidden env dependency | Inject `Env` |
| `console.log()` in module | Hidden output dependency | Inject `Logger` |
| Deps created inside module | Can't test with mocks | Pass deps from composition root |
| Module imports port directly | Bypasses DI | Import contract types only |
