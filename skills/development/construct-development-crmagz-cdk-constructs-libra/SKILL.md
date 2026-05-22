---
name: construct-development
description: CDK construct development patterns, design principles, and type-driven development. Use when building or modifying AWS CDK constructs.
---

# Construct Development Guidelines

## Construct Pattern

Use factory functions that return CDK resources:

```typescript
import {Construct} from 'constructs';
import {RemovalPolicy} from 'aws-cdk-lib';
import {Bucket, BucketEncryption, BlockPublicAccess} from 'aws-cdk-lib/aws-s3';

export type BucketProps = {
    bucketName: string;
    env: {
        name: string;
        region: string;
        account: string;
    };
    enableVersioning?: boolean;
};

export const createBucket = (scope: Construct, props: BucketProps): Bucket => {
    return new Bucket(scope, `${props.bucketName}-bucket`, {
        bucketName: `${props.bucketName}-${props.env.name}-${props.env.region}`,
        enforceSSL: true,
        encryption: BucketEncryption.S3_MANAGED,
        blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
        removalPolicy: props.env.name === 'prod' ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,
        versioned: props.enableVersioning ?? props.env.name === 'prod',
    });
};
```

## Design Principles

### 1. Secure by Default

- Enable encryption (S3_MANAGED or KMS)
- Enforce SSL
- Block public access
- Use private subnets

### 2. Environment-Aware

- Gate expensive features to production
- Use `RemovalPolicy.RETAIN` in prod, `DESTROY` in dev
- Enable enhanced monitoring only where needed

```typescript
// Performance Insights only in prod
performanceInsightRetention: props.env.name === 'prod' ? 7 : undefined,

// Reader instances only in prod
const createReaders = props.env.account === Account.PROD && props.enableReaders;
```

### 3. Cost-Efficient

```typescript
// Performance Insights only in prod
performanceInsightRetention: props.env.name === 'prod' ? 7 : undefined,

// Reader instances only in prod
const createReaders = props.env.account === Account.PROD && props.enableReaders;
```

### 4. Observable

- Include CloudWatch log groups
- Set appropriate retention periods
- Enable metrics where applicable

## Type-Driven Development

**Use types, not interfaces.** This codebase follows type-driven development where we define all data structures using `type` declarations.

### Why Types Over Interfaces?

- More flexible for unions and intersections
- Consistent pattern across the codebase
- Better for functional programming patterns
- Clearer intent for data structures

Define all props types in `src/types/`:

```typescript
// src/types/bucket-types.ts
import {EnvironmentConfig} from '@cdk-constructs/cdk';

export type BucketProps = {
    bucketName: string;
    env: EnvironmentConfig['env'];
    kmsKeyArn?: string;
    lifecycleRules?: BucketLifecycleRule[];
};

export type BucketLifecycleRule = {
    id: string;
    expiration?: number;
    transitions?: StorageTransition[];
};
```

## Export Pattern

Export all public APIs from `src/index.ts`:

```typescript
// src/index.ts

// Constructs
export {createBucket} from './constructs/bucket';
export {createLambda} from './constructs/lambda';

// Types
export type {BucketProps, BucketLifecycleRule} from './types/bucket-types';
export type {LambdaProps} from './types/lambda-types';

// Enums
export {StorageClass} from './enums/storage';

// Utilities
export {getAbsoluteLambdaPath} from './util/paths';
```

## JSDoc Requirements

All public functions, types, and enums should have JSDoc comments:

```typescript
/**
 * Creates a CodeArtifact domain.
 *
 * @param scope - The parent construct
 * @param id - The construct ID
 * @param props - The domain properties
 * @returns The created CodeArtifact domain
 *
 * @public
 */
export const createCodeArtifactDomain = (scope: Construct, id: string, props: CodeArtifactDomainProps): CfnDomain => {
    // ...
};
```
