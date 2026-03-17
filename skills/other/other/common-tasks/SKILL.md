---
name: common-tasks
description: Step-by-step guides for common development tasks like adding constructs, creating packages, and using workspace packages. Use when performing routine development tasks.
---

# Common Tasks

## Adding a New Construct to an Existing Package

1. Create the construct in `packages/{package}/src/constructs/`
2. Create types in `packages/{package}/src/types/`
3. Export from `packages/{package}/src/index.ts`
4. Create test file in `packages/{package}/test/`
5. Create example stack in `packages/{package}/test/`
6. Update package README

## Creating a New Subpackage

1. Create directory: `mkdir -p packages/{name}/src`
2. Create `package.json` with correct dependencies
3. Create `tsconfig.json` extending `../../tsconfig-strict.json`
4. Create `src/index.ts` with exports
5. Add to `tsconfig.build.json` references (in dependency order)
6. Update root README packages table
7. Create package README
8. Create test folder with test files
9. Create docs folder with documentation

## Using Root Package Types

Import shared types from `@cdk-constructs/cdk`:

```typescript
import {
    EnvironmentConfig,
    // Add other shared types as they're created
} from '@cdk-constructs/cdk';
```

## Using Workspace Packages

Import from workspace packages:

```typescript
import {Account, Region, Environment} from '@cdk-constructs/aws';
import {createCodeArtifact} from '@cdk-constructs/codeartifact';
```

## Adding Integration Test Stack

1. Create stack class in `lib/stacks/{stack-name}-stack.ts`
2. Add environment configuration to `bin/environment.ts`
3. Import and instantiate in `bin/app.ts`

## Formatting Code

```bash
# Format all files
npm run format

# Check formatting
npm run format:check

# Format and fix linting
npm run format:fix
```

## Key Reminders

1. **New constructs go in subpackages**, not the root package
2. **Always use explicit imports**, never wildcards
3. **Match CDK versions** across all packages
4. **Include environment in resource names** to prevent collisions
5. **Gate expensive features** to production environments
6. **Export everything** from `src/index.ts`
7. **Create test files** for all constructs
8. **Add JSDoc comments** to all public APIs
9. **Run lint and format** before committing
10. **Follow dependency order** when adding packages
