---
name: github-actions-dev
description: Developing custom GitHub Actions (JavaScript, TypeScript, Docker, Composite). Use this skill when the user asks to 'create a GitHub Action', 'build a custom action', 'publish action to marketplace', 'write action.yml', or 'develop reusable action'.
---

# GitHub Actions Development

## Overview

Guide for developing custom GitHub Actions - the reusable units that are called with `uses:` in workflows. Covers JavaScript/TypeScript actions, Docker actions, and composite actions.

## Action Types

| Type | Best For | Runtime |
|------|----------|---------|
| **JavaScript/TypeScript** | Fast startup, GitHub API integration | Node.js 20 |
| **Docker** | Custom environments, any language | Container |
| **Composite** | Orchestrating other actions | None (YAML) |

## Project Structure

### JavaScript/TypeScript Action

```
my-action/
├── action.yml           # Action metadata
├── src/
│   ├── main.ts          # Entry point
│   ├── input.ts         # Input parsing
│   └── utils.ts         # Helpers
├── dist/
│   └── index.js         # Bundled output (committed)
├── __tests__/
│   └── main.test.ts     # Tests
├── package.json
├── tsconfig.json
└── README.md
```

### Docker Action

```
my-docker-action/
├── action.yml
├── Dockerfile
├── entrypoint.sh
└── README.md
```

### Composite Action

```
my-composite-action/
├── action.yml           # Contains all steps
└── README.md
```

## action.yml Reference

### JavaScript/TypeScript Action

```yaml
name: 'My Action'
description: 'Does something useful'
author: 'Your Name'

branding:
  icon: 'check-circle'
  color: 'green'

inputs:
  token:
    description: 'GitHub token'
    required: true
  config-path:
    description: 'Path to config file'
    required: false
    default: '.github/config.yml'

outputs:
  result:
    description: 'The result of the action'
  artifact-url:
    description: 'URL to uploaded artifact'

runs:
  using: 'node20'
  main: 'dist/index.js'
  post: 'dist/cleanup.js'        # Optional cleanup
  post-if: 'always()'            # When to run cleanup
```

### Docker Action

```yaml
name: 'My Docker Action'
description: 'Runs in a container'

inputs:
  args:
    description: 'Arguments to pass'
    required: true

runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.args }}
  env:
    CUSTOM_VAR: 'value'
```

### Composite Action

```yaml
name: 'My Composite Action'
description: 'Combines multiple steps'

inputs:
  node-version:
    description: 'Node.js version'
    default: '20'

outputs:
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - id: cache
      uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}

    - run: npm ci
      shell: bash
      if: steps.cache.outputs.cache-hit != 'true'
```

## JavaScript/TypeScript Development

### Setup

```bash
# Initialize project
mkdir my-action && cd my-action
npm init -y

# Install action toolkit
npm install @actions/core @actions/github @actions/exec @actions/io @actions/cache

# Dev dependencies
npm install -D typescript @types/node @vercel/ncc jest @types/jest ts-jest
```

### package.json

```json
{
  "name": "my-action",
  "version": "1.0.0",
  "main": "dist/index.js",
  "scripts": {
    "build": "ncc build src/main.ts -o dist --source-map --license licenses.txt",
    "test": "jest",
    "all": "npm run build && npm test"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./lib",
    "rootDir": "./src",
    "strict": true,
    "noImplicitAny": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": ["node_modules", "dist", "__tests__"]
}
```

### Main Entry Point

```typescript
// src/main.ts
import * as core from '@actions/core';
import * as github from '@actions/github';

async function run(): Promise<void> {
  try {
    // Get inputs
    const token = core.getInput('token', { required: true });
    const configPath = core.getInput('config-path');

    // Debug logging (only visible with ACTIONS_STEP_DEBUG)
    core.debug(`Config path: ${configPath}`);

    // Get GitHub context
    const { owner, repo } = github.context.repo;
    core.info(`Running on ${owner}/${repo}`);

    // Create authenticated client
    const octokit = github.getOctokit(token);

    // Do work...
    const result = await doWork(octokit, configPath);

    // Set outputs
    core.setOutput('result', result);

    // Export variable for subsequent steps
    core.exportVariable('MY_ACTION_RESULT', result);

  } catch (error) {
    if (error instanceof Error) {
      core.setFailed(error.message);
    }
  }
}

run();
```

### Action Toolkit APIs

```typescript
import * as core from '@actions/core';
import * as github from '@actions/github';
import * as exec from '@actions/exec';
import * as io from '@actions/io';
import * as cache from '@actions/cache';

// --- @actions/core ---
// Inputs
const required = core.getInput('name', { required: true });
const optional = core.getInput('name');  // Empty string if not set
const multiline = core.getMultilineInput('items');
const boolean = core.getBooleanInput('flag');

// Outputs
core.setOutput('key', 'value');

// Logging
core.debug('Debug message');      // Only with ACTIONS_STEP_DEBUG
core.info('Info message');
core.notice('Notice annotation');
core.warning('Warning annotation');
core.error('Error annotation');

// Grouping
core.startGroup('Group name');
core.info('Inside group');
core.endGroup();

// Or with async
await core.group('Group name', async () => {
  await someAsyncWork();
});

// Masking secrets
core.setSecret(sensitiveValue);

// Failure
core.setFailed('Action failed');

// --- @actions/github ---
// Context
const { owner, repo } = github.context.repo;
const sha = github.context.sha;
const ref = github.context.ref;
const actor = github.context.actor;
const eventName = github.context.eventName;
const payload = github.context.payload;

// Octokit client
const octokit = github.getOctokit(token);
const { data: issue } = await octokit.rest.issues.get({
  owner,
  repo,
  issue_number: 1
});

// --- @actions/exec ---
// Run command
const exitCode = await exec.exec('npm', ['install']);

// Capture output
let output = '';
await exec.exec('git', ['rev-parse', 'HEAD'], {
  listeners: {
    stdout: (data) => { output += data.toString(); }
  }
});

// --- @actions/io ---
// File operations
await io.mkdirP('/path/to/dir');
await io.cp('src', 'dest', { recursive: true });
await io.mv('old', 'new');
await io.rmRF('/path/to/remove');
const toolPath = await io.which('node', true);  // Throws if not found

// --- @actions/cache ---
// Cache dependencies
const paths = ['node_modules'];
const key = `node-${process.env.RUNNER_OS}-${hashFiles('package-lock.json')}`;
const restoreKeys = [`node-${process.env.RUNNER_OS}-`];

const cacheKey = await cache.restoreCache(paths, key, restoreKeys);
if (!cacheKey) {
  // Cache miss, install deps
  await exec.exec('npm', ['ci']);
  await cache.saveCache(paths, key);
}
```

## Docker Action Development

### Dockerfile

```dockerfile
FROM node:20-alpine

LABEL maintainer="Your Name <email@example.com>"
LABEL com.github.actions.name="My Docker Action"
LABEL com.github.actions.description="Description"
LABEL com.github.actions.icon="check-circle"
LABEL com.github.actions.color="green"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

### entrypoint.sh

```bash
#!/bin/sh -l

# Inputs are passed as environment variables
# INPUT_<NAME> in uppercase
echo "Token: $INPUT_TOKEN"
echo "Config: $INPUT_CONFIG_PATH"

# Do work...
RESULT="success"

# Set output (write to $GITHUB_OUTPUT)
echo "result=$RESULT" >> $GITHUB_OUTPUT

# Set environment variable for subsequent steps
echo "MY_VAR=value" >> $GITHUB_ENV
```

## Testing Actions

### Unit Tests

```typescript
// __tests__/main.test.ts
import * as core from '@actions/core';
import * as github from '@actions/github';
import { run } from '../src/main';

// Mock the toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('action', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('sets output on success', async () => {
    // Arrange
    (core.getInput as jest.Mock).mockImplementation((name: string) => {
      if (name === 'token') return 'fake-token';
      return '';
    });

    // Act
    await run();

    // Assert
    expect(core.setOutput).toHaveBeenCalledWith('result', expect.any(String));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('fails when token missing', async () => {
    (core.getInput as jest.Mock).mockImplementation(() => {
      throw new Error('Input required: token');
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Input required: token');
  });
});
```

### Integration Testing

```yaml
# .github/workflows/test.yml
name: Test Action

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run action
        id: test
        uses: ./
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Verify output
        run: |
          if [ "${{ steps.test.outputs.result }}" != "expected" ]; then
            echo "Unexpected output"
            exit 1
          fi
```

### Local Testing with Act

```bash
# Test the action locally
act -j test -s GITHUB_TOKEN="$(gh auth token)"

# With specific event
act push -j test
```

## Publishing to Marketplace

### Requirements

1. Public repository
2. `action.yml` in repository root
3. README.md with documentation
4. Semantic versioning with tags

### Release Process

```bash
# Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Create major version tag (for users: uses: org/action@v1)
git tag -fa v1 -m "Update v1 tag"
git push origin v1 --force
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  release:
    types: [published]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update major version tag
        run: |
          VERSION=${GITHUB_REF#refs/tags/}
          MAJOR=${VERSION%%.*}
          git tag -fa $MAJOR -m "Update $MAJOR tag"
          git push origin $MAJOR --force
```

## Best Practices

### Input Validation

```typescript
function validateInputs(): Config {
  const token = core.getInput('token', { required: true });
  if (!token.startsWith('ghp_') && !token.startsWith('ghs_')) {
    throw new Error('Invalid token format');
  }

  const timeout = parseInt(core.getInput('timeout') || '30', 10);
  if (isNaN(timeout) || timeout < 1 || timeout > 300) {
    throw new Error('Timeout must be between 1 and 300');
  }

  return { token, timeout };
}
```

### Error Handling

```typescript
try {
  await run();
} catch (error) {
  if (error instanceof Error) {
    // Add error annotation to file if available
    core.error(error.message, {
      file: 'src/main.ts',
      startLine: 10
    });
    core.setFailed(error.message);
  } else {
    core.setFailed('An unexpected error occurred');
  }
}
```

### Idempotency

Design actions to be safely re-run:
- Check if work already done before doing it
- Use conditional creation (if not exists)
- Clean up partial state on failure

## See Also

- Reference: [toolkit-api.md](references/toolkit-api.md)
- Reference: [publishing.md](references/publishing.md)
- Assets: [templates/](assets/)
