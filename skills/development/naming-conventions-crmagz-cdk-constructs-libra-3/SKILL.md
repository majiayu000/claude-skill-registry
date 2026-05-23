---
name: naming-conventions
description: Naming conventions for types, functions, files, and resources. Use when creating new code or reviewing naming patterns. Emphasizes type-driven development.
---

# Naming Conventions

## Type Naming

**Use `type` declarations, not `interface`.** This codebase follows type-driven development.

| Type                 | Convention           | Example                                                      |
| -------------------- | -------------------- | ------------------------------------------------------------ |
| Types, Enums         | PascalCase           | `EnvironmentConfig`, `CodeArtifactStackProps`, `BucketProps` |
| Functions, Variables | camelCase            | `createBucket`, `bucketName`                                 |
| AWS Resource Names   | kebab-case           | `my-bucket-dev-use1`                                         |
| Enum Values          | SCREAMING_SNAKE_CASE | `Account.PROD`, `Region.US_EAST_1`                           |

**Type Naming Pattern:**

```typescript
// CORRECT - Use type declarations
export type BucketProps = {
    bucketName: string;
    env: EnvironmentConfig['env'];
};

export type EnvironmentConfig = {
    name: string;
    region: string;
    account: string;
};

// INCORRECT - Don't use interface
export interface BucketProps {
    // ❌
    bucketName: string;
}
```

## Resource Naming Pattern

Include environment and region to prevent naming collisions:

```typescript
// Resource naming pattern
`${resourceName}-${props.env.name}-${props.env.region}`
// Examples
`aurora-cluster-dev-use1``api-gateway-prod-use1``waf-acl-staging-use1`;
```

## Function Naming

Use `verbNoun` pattern for function names:

```typescript
// CORRECT
export const createBucket = () => {};
export const getVpcConfig = () => {};
export const updateSecurityGroup = () => {};

// INCORRECT
export const bucketCreate = () => {};
export const VpcConfigGet = () => {};
```

## File Naming

- Constructs: `kebab-case.ts` (e.g., `api-gateway.ts`)
- Types: `kebab-case-type.ts` or `kebab-case.ts` in types directory
- Enums: `kebab-case-enum.ts` or `kebab-case.ts` in enum directory
- Utilities: `kebab-case.ts` in util directory

## Export Patterns

- Each package exports from `src/index.ts`
- Root package exports from `src/index.ts`
- Use named exports, avoid default exports where possible
