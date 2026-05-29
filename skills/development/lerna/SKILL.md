---
name: lerna
description: Best practices for Lerna monorepo management, versioning, and publishing
---

# Lerna Monorepo Development

You are an expert in Lerna, the fast, modern build system for managing and publishing multiple JavaScript/TypeScript packages.

## Project Structure

- Organize packages following Lerna conventions:
  - `packages/` - All package directories (default)
  - Can customize with multiple directories in `lerna.json`
- Each package should be self-contained with its own:
  - `package.json`
  - Source code
  - Tests
  - Build configuration

## Lerna Configuration

Configure `lerna.json` at the root:

```json
{
  "$schema": "https://json.schemastore.org/lerna.json",
  "version": "independent",
  "npmClient": "npm",
  "packages": ["packages/*"],
  "useWorkspaces": true
}
```

- Choose versioning mode:
  - `"version": "independent"` - Each package versioned separately
  - `"version": "1.0.0"` - Fixed/locked mode, all packages same version
- Enable workspaces integration with `useWorkspaces: true`

## Workspaces Integration

Configure npm/yarn/pnpm workspaces in root `package.json`:

```json
{
  "workspaces": ["packages/*"],
  "private": true
}
```

- Let the package manager handle hoisting and linking
- Use Lerna for versioning, publishing, and running scripts

## Task Execution

- Run scripts across packages:
  - `lerna run build` - Run build in all packages
  - `lerna run test --scope=@org/package` - Run in specific package
  - `lerna run lint --since main` - Run only in changed packages
- Use `--stream` for real-time output
- Use `--parallel` for concurrent execution

## Versioning Workflow

- Update versions with `lerna version`:
  - `lerna version patch` - Bump patch version
  - `lerna version minor` - Bump minor version
  - `lerna version major` - Bump major version
  - `lerna version` - Interactive version selection
- Lerna automatically:
  - Updates package.json versions
  - Updates internal dependency versions
  - Creates git tags
  - Pushes to remote

## Publishing Packages

- Publish with `lerna publish`:
  - `lerna publish` - Publish packages changed since last release
  - `lerna publish from-git` - Publish packages tagged in git
  - `lerna publish from-package` - Publish packages with unpublished versions
- Configure npm registry in `.npmrc` or `lerna.json`
- Use `--dist-tag` for pre-release versions

## Change Detection

- Use `--since` flag for changed packages:
  - `lerna run test --since main`
  - `lerna changed` - List packages changed since last tag
  - `lerna diff` - Show diff since last release
- Leverage affected commands in CI for efficiency

## Conventional Commits

Enable conventional commits for automated versioning:

```json
{
  "command": {
    "version": {
      "conventionalCommits": true,
      "message": "chore(release): publish"
    }
  }
}
```

- Commits determine version bumps:
  - `fix:` - Patch version
  - `feat:` - Minor version
  - `BREAKING CHANGE:` - Major version
- Automatic changelog generation

## Dependency Management

- Use internal package references:
  ```json
  {
    "dependencies": {
      "@org/shared-utils": "^1.0.0"
    }
  }
  ```
- Lerna keeps internal dependencies in sync during versioning
- Hoist common dependencies to root with workspaces

## CI/CD Integration

- Install dependencies once at root level
- Use `lerna run` with `--since` for efficient CI
- Publish from CI with proper npm authentication
- Use `--yes` flag for non-interactive publishing

## Best Practices

- Keep packages focused and single-purpose
- Use consistent package naming: `@org/package-name`
- Maintain clear dependency boundaries between packages
- Document package APIs and usage
- Use TypeScript with project references for type checking
- Implement proper testing at package and integration levels
- Consider Nx integration for advanced caching and task execution
