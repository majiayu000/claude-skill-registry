---
name: import-conventions
description: Import conventions and ordering rules. Use when writing imports or organizing import statements. Enforces explicit named imports, never wildcards.
---

# Import Conventions

## Explicit Named Imports

**ALWAYS use explicit named imports. NEVER use wildcard imports.**

```typescript
// CORRECT
import {Stack, Duration, RemovalPolicy} from 'aws-cdk-lib';
import {Bucket, BucketEncryption, BlockPublicAccess} from 'aws-cdk-lib/aws-s3';
import {Function, Runtime, Code} from 'aws-cdk-lib/aws-lambda';

// INCORRECT - Never do this
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
```

## Import Order

Organize imports in this order:

1. Node.js built-in modules
2. External dependencies (`@aws-sdk/*`, third-party)
3. AWS CDK (`constructs`, `aws-cdk-lib`)
4. Internal monorepo packages (`@cdk-constructs/*`)
5. Local imports (`./`, `../`)

```typescript
import {readFileSync} from 'fs';

import {SecretsManagerClient} from '@aws-sdk/client-secrets-manager';

import {Construct} from 'constructs';
import {Stack, Duration} from 'aws-cdk-lib';
import {Bucket} from 'aws-cdk-lib/aws-s3';

import {Account, Region, Environment} from '@cdk-constructs/aws';
import {CodeArtifactStackProps} from '@cdk-constructs/codeartifact';

import {MyLocalType} from './types/my-types';
```

## Workspace Package Imports

When importing from workspace packages, use the package name:

```typescript
// CORRECT
import {Account, Region} from '@cdk-constructs/aws';
import {createCodeArtifact} from '@cdk-constructs/codeartifact';

// INCORRECT - Don't use relative paths to packages
import {Account} from '../../packages/aws/src';
```
