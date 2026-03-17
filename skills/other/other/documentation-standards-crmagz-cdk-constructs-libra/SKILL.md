---
name: documentation-standards
description: JSDoc/TSDoc standards for documenting types, functions, and constructs. Use when writing or reviewing documentation.
---

# Documentation Standards

This project uses **TSDoc** (TypeScript Documentation) for all code documentation. TSDoc is the TypeScript-specific standard built on JSDoc.

## Philosophy

Inline TSDoc provides **quick reference for IDE tooltips**. Comprehensive guides, tutorials, and detailed examples belong in `/docs` directories within each subpackage.

## General Principles

1. **Every public API must have documentation**
2. **Keep it concise** - inline docs are for quick reference
3. **One example maximum** per type/function (simple usage only)
4. **Link to related types** with `{@link TypeName}`
5. **Tag visibility** with `@public`, `@internal`, or `@private`
6. **Detailed guides go in /docs**, not inline

## Documentation Structure

### For Type Properties

```typescript
/** Brief one-line description. */
propertyName: string;

/** Optional property description. @defaultValue `default-value` */
optionalProperty?: number;
```

### For Types/Interfaces

````typescript
/**
 * Brief description of what this type represents (1-2 sentences).
 *
 * @example
 * ```typescript
 * const example: MyType = {
 *   property: 'value',
 * };
 * ```
 *
 * @see {@link RelatedType} for related functionality
 * @public
 */
export type MyType = {
    /** Property description. */
    property: string;
};
````

### For Functions

````typescript
/**
 * Brief description of what this function does.
 *
 * @remarks
 * Only include critical prerequisites or warnings here.
 *
 * @param paramName - Brief parameter description
 * @returns Brief return description (only if needed)
 *
 * @example
 * ```typescript
 * const result = myFunction(param);
 * ```
 *
 * @see {@link RelatedFunction} for related functionality
 * @public
 */
export const myFunction = (paramName: string): ReturnType => {
    // Implementation
};
````

## Tag Reference

### Required Tags

#### Description (No Tag)

The first paragraph is always the main description. Keep it brief (1-2 sentences).

```typescript
/**
 * Creates an Aurora PostgreSQL cluster with optimized settings.
 */
```

#### `@param` - Parameter Documentation

One-line description per parameter.

```typescript
/**
 * @param scope - The CDK construct scope
 * @param id - Unique identifier for this construct
 * @param props - Configuration properties
 */
```

#### `@public` / `@internal` / `@private` - API Visibility

Always tag the visibility.

```typescript
/**
 * Creates an Aurora cluster for production use.
 * @public
 */
```

### Optional Tags (Use Sparingly)

#### `@remarks` - Critical Information Only

Use only for critical prerequisites, warnings, or non-obvious behavior.

```typescript
/**
 * @remarks
 * Requires VPC with at least 2 private subnets in different AZs.
 */
```

#### `@returns` - Return Value Description

Only include if the return value needs clarification beyond the type signature.

```typescript
/**
 * @returns The created cluster with monitoring enabled
 */
```

#### `@example` - Single Simple Example

One example maximum. Keep it simple and basic usage only.

````typescript
/**
 * @example
 * ```typescript
 * const cluster = createAuroraCluster(this, 'MyCluster', {
 *   vpc: myVpc,
 *   databaseName: 'production-db',
 * });
 * ```
 */
````

#### `@see` - Related References

Link to related types or functions.

```typescript
/**
 * @see {@link AuroraClusterProps} for configuration options
 */
```

#### `@defaultValue` - Default Values

Use inline for optional properties.

```typescript
/** Instance type for the cluster. @defaultValue `r6g.large` */
instanceType?: InstanceType;
```

#### `@deprecated` - Deprecation Notice

Mark deprecated APIs with brief migration guidance.

```typescript
/**
 * @deprecated Use {@link createAuroraClusterV2} instead. Will be removed in v2.0.0.
 */
```

## Common Patterns

### Types

````typescript
/**
 * Configuration properties for Aurora PostgreSQL cluster.
 *
 * @example
 * ```typescript
 * const props: AuroraClusterProps = {
 *   vpc: myVpc,
 *   databaseName: 'production-db',
 * };
 * ```
 *
 * @public
 */
export type AuroraClusterProps = {
    /** VPC where the cluster will be deployed. */
    vpc: IVpc;

    /** Name of the database to create. */
    databaseName: string;

    /** Instance type for the cluster. @defaultValue `r6g.large` */
    instanceType?: InstanceType;
};
````

### Functions

````typescript
/**
 * Creates an Aurora PostgreSQL cluster with production-ready configuration.
 *
 * @remarks
 * Requires VPC with at least 2 private subnets in different AZs.
 *
 * @param scope - The CDK construct scope
 * @param id - Unique identifier for this construct
 * @param props - Configuration properties for the cluster
 * @returns The created Aurora cluster instance
 *
 * @example
 * ```typescript
 * const cluster = createAuroraCluster(this, 'MyCluster', {
 *   vpc: myVpc,
 *   databaseName: 'production',
 * });
 * ```
 *
 * @see {@link AuroraClusterProps} for configuration options
 * @public
 */
export const createAuroraCluster = (scope: Construct, id: string, props: AuroraClusterProps): DatabaseCluster => {
    // Implementation
};
````

### Enums

````typescript
/**
 * AWS Account ID enumeration for multi-account deployments.
 *
 * @example
 * ```typescript
 * const env = {
 *   account: Account.PROD,
 *   region: 'us-east-1',
 * };
 * ```
 *
 * @see {@link EnvironmentConfig} for environment configuration
 * @public
 */
export enum Account {
    /** Build account for CI/CD and artifact generation. */
    BUILD = '000000000000',

    /** Development account for active development and testing. */
    DEV = '111111111111',
}
````

### CDK Constructs (Classes)

````typescript
/**
 * Creates a CodeArtifact repository with domain configuration.
 *
 * @example
 * ```typescript
 * new CodeArtifactStack(this, 'CodeArtifact', {
 *   account: Account.BUILD,
 *   region: Region.US_EAST_1,
 *   name: Environment.BUILD,
 *   owner: 'platform-team',
 *   codeArtifactDomainName: 'my-domain',
 *   codeArtifactRepositoryName: 'my-repo',
 * });
 * ```
 *
 * @public
 */
export class CodeArtifactStack extends Stack {
    /**
     * Creates a new CodeArtifact stack.
     *
     * @param scope - The parent construct
     * @param id - Unique identifier for this stack
     * @param props - Stack properties including environment config
     */
    constructor(scope: Construct, id: string, props: CodeArtifactStackPropsWithEnv) {
        // Implementation
    }
}
````

## Anti-Patterns (What NOT to Do)

### ❌ Don't: Verbose property descriptions

```typescript
export type Props = {
    /**
     * The name of the database.
     *
     * @remarks
     * Must be 1-63 characters, alphanumeric and underscores only.
     * Cannot start with a number. This follows AWS RDS naming conventions.
     * The database will be created automatically during cluster provisioning.
     */
    databaseName: string;
};
```

### ✅ Do: Concise one-liners

```typescript
export type Props = {
    /** Name of the database to create. */
    databaseName: string;
};
```

### ❌ Don't: Multiple examples

````typescript
/**
 * @example
 * Basic usage:
 * ```typescript
 * const cluster = create(...);
 * ```
 *
 * @example
 * Advanced usage:
 * ```typescript
 * const cluster = create(..., {advanced: true});
 * ```
 */
````

### ✅ Do: One simple example

````typescript
/**
 * @example
 * ```typescript
 * const cluster = create(this, 'Cluster', {vpc: myVpc});
 * ```
 */
````

### ❌ Don't: Explain implementation details

```typescript
/**
 * Loops through subnets and creates security groups using CDK's Subnet class
 */
```

### ✅ Do: Explain what it does

```typescript
/**
 * Configures database in private subnets for security.
 */
```

### ❌ Don't: Tutorial-style documentation

```typescript
/**
 * @remarks
 * This construct provides the following features:
 * 1. Automatic backups with 7-day retention
 * 2. CloudWatch monitoring with custom alarms
 * 3. Secrets Manager integration for credentials
 * 4. Multi-AZ deployment for high availability
 * 5. Encryption at rest using KMS
 * 6. Enhanced monitoring with 60-second granularity
 *
 * To use this construct, first create a VPC...
 */
```

### ✅ Do: Brief critical information only

```typescript
/**
 * @remarks
 * Requires VPC with at least 2 private subnets in different AZs.
 */
```

## Documentation Checklist

Before committing, ensure:

- [ ] Every public function/type has a brief description
- [ ] All parameters documented with one-line `@param`
- [ ] Visibility tagged (`@public`, `@internal`, `@private`)
- [ ] Type properties use one-line `/** */` format
- [ ] Functions have one simple `@example` maximum
- [ ] `@remarks` only for critical prerequisites/warnings
- [ ] Types linked with `{@link TypeName}` where relevant
- [ ] No verbose explanations (save for `/docs`)

## Tools Integration

TSDoc comments integrate with:

- **VS Code IntelliSense** - Hover tooltips (primary use case)
- **TypeDoc** - Generated documentation sites
- **API Extractor** - API documentation reports

Comprehensive guides belong in `/docs` directories within each subpackage.
