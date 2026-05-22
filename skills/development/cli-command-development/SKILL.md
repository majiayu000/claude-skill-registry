---
name: cli-command-development
description: Creating new CLI commands and topics for the B2C CLI using oclif
---

# CLI Command Development

This skill covers creating new CLI commands and topics for the B2C CLI.

## Command Organization

Commands live in `packages/b2c-cli/src/commands/`. The directory structure maps directly to command names:

```
commands/
├── code/
│   ├── deploy.ts      → b2c code deploy
│   ├── activate.ts    → b2c code activate
│   └── list.ts        → b2c code list
├── ods/
│   ├── create.ts      → b2c ods create
│   └── list.ts        → b2c ods list
└── mrt/
    └── env/
        └── var/
            └── set.ts → b2c mrt env var set
```

## Command Class Hierarchy

Choose the appropriate base class based on what your command needs:

```
BaseCommand (logging, JSON output, error handling)
  └─ OAuthCommand (OAuth authentication)
       ├─ InstanceCommand (B2C instance: hostname, code version)
       │   ├─ CartridgeCommand (cartridge path + filters)
       │   ├─ JobCommand (job execution helpers)
       │   └─ WebDavCommand (WebDAV root directory)
       ├─ MrtCommand (Managed Runtime API)
       └─ OdsCommand (On-Demand Sandbox API)
```

Import from `@salesforce/b2c-tooling-sdk/cli`:

```typescript
import { InstanceCommand, CartridgeCommand, OdsCommand } from '@salesforce/b2c-tooling-sdk/cli';
```

## Standard Command Template

```typescript
/*
 * Copyright (c) 2025, Salesforce, Inc.
 * SPDX-License-Identifier: Apache-2
 * For full license text, see the license.txt file in the repo root
 */
import {Args, Flags} from '@oclif/core';
import {InstanceCommand} from '@salesforce/b2c-tooling-sdk/cli';
import {t} from '../../i18n/index.js';

interface MyCommandResponse {
  success: boolean;
  data: SomeType[];
}

export default class MyCommand extends InstanceCommand<typeof MyCommand> {
  static description = t('commands.topic.mycommand.description', 'Human-readable description');

  static enableJsonFlag = true;

  static examples = [
    '<%= config.bin %> <%= command.id %> arg1',
    '<%= config.bin %> <%= command.id %> --flag value',
    '<%= config.bin %> <%= command.id %> --json',
  ];

  static args = {
    name: Args.string({
      description: 'Description of the argument',
      required: true,
    }),
  };

  static flags = {
    myFlag: Flags.string({
      char: 'm',
      description: 'Flag description',
      default: 'defaultValue',
    }),
    myBool: Flags.boolean({
      description: 'Boolean flag',
      default: false,
    }),
  };

  async run(): Promise<MyCommandResponse> {
    // Validation - call appropriate require* methods
    this.requireServer();

    // Access parsed args and flags
    const {name} = this.args;
    const {myFlag, myBool} = this.flags;

    this.log(t('commands.topic.mycommand.working', 'Working on {{name}}...', {name}));

    // Implementation
    const result = await this.instance.ocapi.GET('/some/endpoint');

    if (!result.data) {
      this.error(t('commands.topic.mycommand.error', 'Failed: {{message}}', {
        message: result.response?.statusText || 'Unknown error',
      }));
    }

    const response: MyCommandResponse = {
      success: true,
      data: result.data,
    };

    // JSON mode returns the object directly (oclif handles serialization)
    if (this.jsonEnabled()) {
      return response;
    }

    // Human-readable output
    this.log('Success!');
    return response;
  }
}
```

## Adding a New Topic

When creating a new command topic, add it to `packages/b2c-cli/package.json` in the oclif section:

```json
{
  "oclif": {
    "topics": {
      "newtopic": {
        "description": "Commands for new functionality"
      },
      "newtopic:subtopic": {
        "description": "Subtopic commands"
      }
    }
  }
}
```

## Flag Patterns

### Common Flag Types

```typescript
static flags = {
  // String with short alias and env var fallback
  server: Flags.string({
    char: 's',
    description: 'Server hostname',
    env: 'SFCC_SERVER',
  }),

  // Integer with default
  timeout: Flags.integer({
    description: 'Timeout in seconds',
    default: 60,
  }),

  // Boolean with --no-* variant
  wait: Flags.boolean({
    description: 'Wait for completion',
    default: true,
    allowNo: true,  // enables --no-wait
  }),

  // Comma-separated multiple values
  channels: Flags.string({
    description: 'Site channels (comma-separated)',
    multiple: true,
    multipleNonGreedy: true,
    delimiter: ',',
  }),

  // Enum-like options
  format: Flags.string({
    description: 'Output format',
    options: ['json', 'csv', 'table'],
    default: 'table',
  }),

  // Conditional flag
  secret: Flags.string({
    description: 'Client secret (required for private clients)',
    dependsOn: ['client-id'],
  }),
};
```

## Table Output

Use `createTable` for consistent tabular output:

```typescript
import {createTable, TableRenderer, type ColumnDef} from '@salesforce/b2c-tooling-sdk/cli';

type MyData = {id: string; name: string; status: string};

const COLUMNS: Record<string, ColumnDef<MyData>> = {
  id: {
    header: 'ID',
    get: (item) => item.id,
  },
  name: {
    header: 'Name',
    get: (item) => item.name,
  },
  status: {
    header: 'Status',
    get: (item) => item.status,
    extended: true,  // Only shown with --extended
  },
};

const DEFAULT_COLUMNS = ['id', 'name'];
const tableRenderer = new TableRenderer(COLUMNS);

// In run():
tableRenderer.render(data, DEFAULT_COLUMNS);

// With --columns flag support:
const columns = this.flags.columns
  ? tableRenderer.validateColumnKeys(this.flags.columns.split(','))
  : DEFAULT_COLUMNS;
tableRenderer.render(data, columns);
```

## Internationalization

All user-facing strings use the `t()` function:

```typescript
import {t} from '../../i18n/index.js';

// Basic usage
this.log(t('commands.topic.cmd.message', 'Default message'));

// With interpolation
this.log(t('commands.topic.cmd.working', 'Processing {{count}} items...', {count: 5}));

// For errors
this.error(t('commands.topic.cmd.error', 'Failed: {{message}}', {message: err.message}));
```

Keys follow the pattern: `commands.<topic>.<command>.<key>`

## Validation Methods

Base classes provide validation helpers:

```typescript
// From OAuthCommand
this.requireOAuthCredentials();  // Ensures clientId + clientSecret
this.hasOAuthCredentials();      // Returns boolean

// From InstanceCommand
this.requireServer();            // Ensures hostname is set
this.requireCodeVersion();       // Ensures code version is set
this.requireWebDavCredentials(); // Ensures WebDAV auth (Basic or OAuth)

// From MrtCommand
this.requireMrtCredentials();    // Ensures MRT API credentials
```

## Accessing Clients

InstanceCommand provides lazy-loaded clients:

```typescript
// OCAPI client (OAuth authenticated)
const result = await this.instance.ocapi.GET('/code_versions');

// WebDAV client (Basic or OAuth authenticated)
await this.instance.webdav.put('path/to/file', buffer);

// ODS client (from OdsCommand)
const sandboxes = await this.odsClient.GET('/sandboxes');

// MRT client (from MrtCommand)
const projects = await this.mrtClient.GET('/api/projects/');
```

## Error Handling

```typescript
// Simple error (exits with code 1)
this.error('Something went wrong');

// Error with suggestions
this.error('Config file not found', {
  suggestions: ['Run b2c auth login first', 'Check your dw.json file'],
});

// Warning (continues execution)
this.warn('Deprecated flag used');

// Structured API errors
if (result.error) {
  this.error(t('commands.topic.cmd.apiError', 'API error: {{message}}', {
    message: formatApiError(result.error),
  }));
}
```

## Creating a Command Checklist

1. Create file at `packages/b2c-cli/src/commands/<topic>/<command>.ts`
2. Choose appropriate base class
3. Define `static description`, `examples`, `args`, `flags`
4. Set `static enableJsonFlag = true` for JSON output support
5. Implement `run()` method with proper return type
6. Add topic to `package.json` if new
7. Add i18n keys for all user-facing strings
8. Update skill in `plugins/b2c-cli/skills/b2c-<topic>/SKILL.md` if exists
9. Update CLI reference docs in `docs/cli/<topic>.md`
10. Build and test: `pnpm run build && pnpm --filter @salesforce/b2c-cli run test`
