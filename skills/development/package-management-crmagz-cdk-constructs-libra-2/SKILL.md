---
name: package-management
description: Package configuration, dependencies, workspace references, and CDK version management. Use when creating packages or managing dependencies.
---

# Package Management

## Package.json Requirements

When creating or modifying subpackages:

```json
{
    "name": "@cdk-constructs/{package-name}",
    "version": "0.1.0",
    "main": "dist/src/index.js",
    "types": "dist/src/index.d.ts",
    "files": ["dist"],
    "dependencies": {
        "@cdk-constructs/cdk": "*",
        "@cdk-constructs/aws": "*"
    },
    "peerDependencies": {
        "aws-cdk-lib": "^2.225.0",
        "constructs": "^10.0.0"
    },
    "devDependencies": {
        "aws-cdk-lib": "2.225.0",
        "constructs": "10.4.2"
    }
}
```

**Key Points:**

- Use `"@cdk-constructs/*": "*"` to reference workspace packages
- `peerDependencies` and `devDependencies` must match the root package's CDK version
- `main` and `types` point to `dist/src/` (TypeScript compiles from `src/`)

## Inter-Package Dependencies

Some packages depend on others:

- `@cdk-constructs/codeartifact` depends on `@cdk-constructs/aws`
- `@cdk-constructs/cloudwatch` depends on both `@cdk-constructs/cdk` and `@cdk-constructs/api-gateway`

When adding cross-package dependencies:

1. Add them to `dependencies` in `package.json`
2. Ensure proper build order in `tsconfig.build.json`
3. Verify no circular dependencies are created

## CDK Version Management

### Version Synchronization

All packages must use the same `aws-cdk-lib` version. The current version is defined in the root `package.json`.

### Updating CDK Version

When updating CDK version, modify these files:

1. Root `package.json`: `version`, `devDependencies.aws-cdk-lib`, `devDependencies.aws-cdk`, `peerDependencies.aws-cdk-lib`
2. Each `packages/*/package.json`: `peerDependencies.aws-cdk-lib`, `devDependencies.aws-cdk-lib`

## Workspace Dependencies

### Using Workspace References

Packages reference each other using `"*"` in dependencies:

```json
{
    "dependencies": {
        "@cdk-constructs/aws": "*",
        "@cdk-constructs/cdk": "*"
    }
}
```

The `"*"` tells npm to use the workspace version, preventing circular dependencies.

### Postinstall Script

The `postinstall` script removes nested `node_modules` to prevent circular dependencies:

```json
"postinstall": "rm -rf node_modules/@cdk-constructs/*/node_modules"
```

This ensures all packages use the workspace root's `node_modules`.
