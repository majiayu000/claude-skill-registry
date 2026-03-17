---
name: build-and-deployment
description: Build commands, build order, TypeScript configuration, and CDK deployment. Use when building packages, troubleshooting build issues, or deploying stacks.
---

# Build and Deployment

## Make Commands (Recommended)

Use `make` for deterministic, hermetic builds that work the same locally and in CI/CD:

```bash
# Show all available commands
make help

# Install dependencies
make install

# Clean build artifacts
make clean

# Build all packages in dependency order
make build-all

# Build root package only
make build

# Build CDK app only
make build-app
```

## Code Quality Commands

```bash
# Run linter
make lint

# Fix linting issues
make lint-fix

# Format code
make format

# Check formatting (CI)
make format-check

# Format and fix linting
make format-fix

# Run all quality checks (format + lint)
make check
```

## CDK Commands

```bash
# Synthesize CloudFormation templates
make synth

# Show CDK diff
make diff

# Deploy all stacks
make deploy

# Deploy specific stack
make deploy-stack STACK=StackName
```

## CI/CD Commands

```bash
# CI check (format-check + lint)
make ci-check

# CI build (checks + full build)
make ci-build

# CI deploy (checks + build + synth)
make ci-deploy
```

## Underlying npm Commands

The Makefile wraps these npm commands:

```bash
npm install              # Install dependencies
npm run clean            # Clean build artifacts
npm run build            # Build root package
npm run build:workspaces # Build all packages
npm run build:app        # Build CDK app
npm run lint             # Run linter
npm run lint:fix         # Fix linting
npm run format           # Format code
npm run format:check     # Check formatting
npm run format:fix       # Format and fix linting
npm run synth            # Synthesize CDK
npm run diff             # CDK diff
npm run deploy           # Deploy CDK
```

## Build Order

The build process ensures packages are built in dependency order:

1. **Root package** (`src/`) - Built first
2. **Base packages** (`aws`) - No internal dependencies
3. **Dependent packages** (`codeartifact`) - Built after dependencies
4. **CDK app** (`bin/`, `lib/`) - Built last, can import from all packages

### Build Script Details

The `build:workspaces` script:

1. Builds root package (`npm run build`)
2. Copies root to `node_modules/@cdk-constructs/cdk/` for workspace resolution
3. Builds all workspace packages using TypeScript project references
4. Builds CDK app files (`bin/`, `lib/`)

## TypeScript Configuration

### Root Package (`tsconfig.json`)

- Builds `src/**/*` only
- Excludes `bin/`, `lib/`, and `packages/`

### CDK App (`tsconfig.app.json`)

- Builds `bin/**/*` and `lib/**/*`
- Can import from workspace packages after they're built

### Workspace Build (`tsconfig.build.json`)

- Lists packages in dependency order
- Uses TypeScript project references for incremental builds

## Deployment Patterns

### Multi-Account Strategy

This project follows a strict multi-account deployment pattern for security, isolation, and supply chain integrity.

#### Account Structure

| Account     | Purpose                                                     | Access Pattern                                                  |
| ----------- | ----------------------------------------------------------- | --------------------------------------------------------------- |
| **BUILD**   | CI/CD pipelines, artifact generation, supply chain security | Isolated account. Other accounts can access readonly/immutable. |
| **DEV**     | Active development and testing                              | Can access BUILD artifacts (readonly).                          |
| **STAGING** | Pre-production testing and validation                       | Can access BUILD artifacts (readonly).                          |
| **PROD**    | Production workloads                                        | Can access BUILD artifacts (readonly).                          |

#### BUILD Account Principles

**CRITICAL**: The BUILD account MUST be its own isolated AWS account.

1. **Isolation**: BUILD account is completely separate from application environments
2. **Readonly Access**: DEV, STAGING, and PROD can only read from BUILD (never write)
3. **Immutable Artifacts**: Once built in BUILD, artifacts cannot be modified
4. **Supply Chain Security**: All dependencies and builds happen in isolated BUILD environment
5. **Access Control**: BUILD account has read/write. Other accounts have readonly only.

#### CodeArtifact Access Patterns

```typescript
// BUILD environment - owns the artifact repository
{
  ...buildEnv,
  codeArtifact: {
    codeArtifactDomainName: 'cdk-constructs',
    codeArtifactRepositoryName: 'cdk-constructs-library-build',
    codeArtifactRepositoryDescription: 'Build Repository - Supply Chain Security',
    // All accounts can access, but only BUILD can write
    allowedAccounts: [Account.BUILD, Account.DEV, Account.STAGING, Account.PROD],
  },
}

// Application environments - consume artifacts from BUILD
{
  ...devEnv,
  codeArtifact: {
    // DEV has its own repository but also accesses BUILD
    allowedAccounts: [Account.DEV, Account.STAGING, Account.BUILD],
  },
}
```

#### Environment Configuration Location

Environment configurations follow CDK conventions:

- **Types**: `lib/types/project.ts` - ProjectEnvironment type
- **Configs**: `lib/config/environments.ts` - buildEnv, devEnv, stagingEnv, prodEnv
- **Re-exports**: `bin/environment.ts` - Backwards compatibility

This follows the pattern: `bin/` → `lib/` for CDK applications.

### Deployment Security

1. **Never deploy BUILD artifacts to BUILD account** - BUILD creates, others consume
2. **Enforce readonly** - Use IAM policies to prevent write access from non-BUILD accounts
3. **Tag everything** - Environment and Owner tags applied automatically via EnvironmentConfig
4. **Audit access** - Monitor cross-account access to BUILD artifacts

## Common Build Issues

### Issue: "Cannot find module '@cdk-constructs/...'"

**Solution**:

1. Run `make install` to set up workspace links
2. Run `make build-all` to build packages in order
3. Ensure package is listed in `tsconfig.build.json`

### Issue: Circular dependency detected

**Solution**:

1. Check package dependencies in `package.json`
2. Verify build order in `tsconfig.build.json`
3. Ensure no package depends on a package that depends on it
