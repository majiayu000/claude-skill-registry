---
name: creating-subpackages
description: Patterns and standards for creating new AWS service subpackages in the monorepo. Use when adding new service packages like Lambda, DynamoDB, Step Functions, etc.
---

# Creating Subpackages Guide

This guide documents the patterns established when creating the Aurora package, which should be followed for all new service subpackages.

## Package Structure

```
packages/
└── <service-name>/
    ├── package.json
    ├── tsconfig.json
    ├── README.md
    ├── src/
    │   ├── index.ts                    # Package exports
    │   ├── constructs/
    │   │   └── <resource>-<variant>.ts # Factory functions
    │   ├── types/
    │   │   ├── <resource>-base.ts      # Base/shared types
    │   │   └── <resource>-<variant>.ts # Variant-specific types
    │   └── util/
    │       └── <resource>-helpers.ts   # Shared utilities
    ├── test/
    │   └── <resource>-<variant>.test.ts
    └── docs/
        └── <resource>-guide.md
```

## Factory Function Pattern

### No ID Parameter

Factory functions should NOT take an `id` parameter. Use the resource name from props as the construct ID.

```typescript
// ❌ Old pattern - DO NOT USE
export const createFunction = (scope: Construct, id: string, props: FunctionProps) => {
    return new Function(scope, id, { ... });
};

// ✅ New pattern - USE THIS
export const createFunction = (scope: Construct, props: FunctionProps): FunctionResources => {
    return new Function(scope, props.functionName, { ... });
};
```

### Resource ID Naming

Use the resource name from props for ALL resource IDs to prevent collisions:

```typescript
export const createFunction = (scope: Construct, props: FunctionProps): FunctionResources => {
    const role = new Role(scope, `${props.functionName}-role`, { ... });
    const logGroup = new LogGroup(scope, `${props.functionName}-logs`, { ... });

    const func = new Function(scope, props.functionName, {
        functionName: props.functionName,
        role,
        logGroup,
        // ... other config
    });

    return { function: func, role, logGroup };
};
```

## Type Definitions

### Base Configuration Type

Create a base type for shared configuration across variants:

```typescript
// types/<resource>-base.ts
export type ResourceBaseConfig = {
    /** Resource name - used as construct ID and for resource naming */
    resourceName: string;

    /** Common config properties */
    environment?: string;
    tags?: Record<string, string>;

    // ... other common properties
};

export type ResourceResources = {
    /** The primary resource created */
    resource: PrimaryResource;

    /** Related resources that may be useful to consumers */
    role?: IRole;
    logGroup?: ILogGroup;
};
```

### Variant-Specific Types

Extend the base for specific variants:

```typescript
// types/<resource>-<variant>.ts
import {ResourceBaseConfig} from './resource-base';

export type VariantResourceProps = ResourceBaseConfig & {
    /** Variant-specific properties */
    variantOption: string;
};
```

### Avoid Unnecessary Type Wrappers

Don't use `Omit<>` for properties that don't exist:

```typescript
// ❌ Don't do this
export const CONFIG: Omit<ResourceProps, 'nonExistentProp'> = { ... };

// ✅ Do this
export const CONFIG: ResourceProps = { ... };
```

## Automatic Resource Creation

Constructs should create necessary supporting resources automatically:

```typescript
export const createFunction = (scope: Construct, props: FunctionProps): FunctionResources => {
    // Create role automatically if not provided
    const role =
        props.existingRole ||
        new Role(scope, `${props.functionName}-role`, {
            roleName: props.roleName || `${props.functionName}-execution-role`,
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')],
        });

    // Create log group automatically
    const logGroup = new LogGroup(scope, `${props.functionName}-logs`, {
        logGroupName: `/aws/lambda/${props.functionName}`,
        retention: props.logRetention || RetentionDays.ONE_WEEK,
        removalPolicy: props.removalPolicy || RemovalPolicy.DESTROY,
    });

    const func = new Function(scope, props.functionName, {
        functionName: props.functionName,
        role,
        logGroup,
        // ... other config
    });

    return {function: func, role, logGroup};
};
```

## Default Values and Validation

### Provide Sensible Defaults

```typescript
const commonConfig = {
    timeout: props.timeout || Duration.seconds(30),
    memorySize: props.memorySize || 256,
    retries: props.retries ?? 2, // Use ?? for number defaults

    // Conditional defaults based on other props
    logRetention: props.enableDetailedLogging ? props.logRetention || RetentionDays.ONE_MONTH : RetentionDays.ONE_WEEK,
};
```

### Validate Required Dependencies

```typescript
if (props.enableFeature && !props.requiredConfig) {
    throw new Error(`requiredConfig must be set when enableFeature is true`);
}
```

## Example Stack Pattern

### Config Resolver for Local Overrides

```typescript
// examples/<service>/config/config-resolver.ts
export interface LocalConfig {
    vpcId?: string;
    subnetIds?: string[];
    // ... other overridable values
}

export class ConfigResolver {
    private static localConfig: LocalConfig | undefined;
    private static localConfigLoaded = false;

    private static loadLocalConfig(): LocalConfig | undefined {
        if (!this.localConfigLoaded) {
            try {
                const {LOCAL_CONFIG} = require('../../environments.local');
                this.localConfig = LOCAL_CONFIG;
            } catch {
                this.localConfig = undefined;
            }
            this.localConfigLoaded = true;
        }
        return this.localConfig;
    }

    private static resolve<T extends LocalConfig>(baseConfig: T): T {
        const localConfig = this.loadLocalConfig();
        if (localConfig) {
            return {...baseConfig, ...localConfig};
        }
        return baseConfig;
    }

    public static getDevConfig(): ResourceProps {
        return this.resolve(DEV_CONFIG);
    }
}
```

### Config Files with Placeholders

```typescript
// examples/<service>/config/<resource>-dev.ts
export const DEV_CONFIG: ResourceProps = {
    resourceName: 'my-resource-dev',

    // Use placeholder values for sensitive/environment-specific config
    vpcId: 'vpc-xxxxxxxxxxxxxxxxx',
    subnetIds: ['subnet-xxxxxxxxxxxxxxxxx', 'subnet-yyyyyyyyyyyyyyyyy'],

    // Dev-appropriate settings
    enableDetailedLogging: true,
    retentionPolicy: RemovalPolicy.DESTROY,
    deletionProtection: false,
};
```

### Example Stack

```typescript
// examples/<service>/stacks/<resource>-dev-stack.ts
export class ResourceDevStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        const config = ConfigResolver.getDevConfig();

        const {resource, role} = createResource(this, {
            ...config,
        });
    }
}
```

## Package Exports

Structure the `index.ts` to export everything consumers need:

```typescript
// src/index.ts

// Construct functions
export {createResourceVariantA} from './constructs/resource-variant-a';
export {createResourceVariantB} from './constructs/resource-variant-b';

// Types - organize by category
export type {
    // Base types
    ResourceBaseConfig,
    ResourceResources,

    // Variant types
    VariantAResourceProps,
    VariantBResourceProps,

    // Helper types
    ParameterGroupConfig,
    MonitoringConfig,
} from './types';

// Utilities - only export what's useful to consumers
export {createParameterGroup, createMonitoringAlarm} from './util/resource-helpers';
```

## Testing Requirements

### Test Structure

```typescript
describe('Resource Variant A', () => {
    let app: App;
    let stack: Stack;

    beforeEach(() => {
        app = new App({
            context: {
                /* mock context */
            },
        });
        stack = new Stack(app, 'TestStack', {
            env: {account: '123456789012', region: 'us-east-1'},
        });
    });

    test('creates resource with basic configuration', () => {
        const {resource} = createResourceVariantA(stack, {
            resourceName: 'test-resource',
            // ... required props
        });

        const template = Template.fromStack(stack);
        template.resourceCountIs('AWS::Service::Resource', 1);
        template.hasResourceProperties('AWS::Service::Resource', {
            Property: 'ExpectedValue',
        });
    });

    test('creates supporting resources automatically', () => {
        createResourceVariantA(stack, {
            resourceName: 'test-resource',
        });

        const template = Template.fromStack(stack);
        template.resourceCountIs('AWS::IAM::Role', 1);
        template.resourceCountIs('AWS::Logs::LogGroup', 1);
    });
});
```

## Documentation Standards

### TSDoc Requirements

````typescript
/**
 * Creates a [Service] [Resource] with [key features].
 *
 * @remarks
 * This construct creates a production-ready resource with:
 * - Feature 1
 * - Feature 2
 * - Feature 3
 *
 * @param scope - The construct scope
 * @param props - Configuration properties
 * @returns Resources including the primary resource and supporting resources
 *
 * @example
 * ```typescript
 * import { createResource } from '@cdk-constructs/<service>';
 * import { Duration } from 'aws-cdk-lib';
 *
 * const { resource, role } = createResource(this, {
 *   resourceName: 'my-resource',
 *   timeout: Duration.seconds(30),
 *   memorySize: 512,
 * });
 * ```
 *
 * @see {@link ResourceProps} for configuration options
 * @see https://docs.aws.amazon.com/service/resource.html
 * @public
 */
````

## Common Patterns

### Environment-Based Configuration

```typescript
const isProd = props.environment === 'prod';

const config = {
    // Expensive features gated to prod
    enableBackups: isProd,
    multiAZ: isProd,

    // Safe defaults for non-prod
    deletionProtection: isProd,
    removalPolicy: isProd ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,
};
```

### Conditional Resource Creation

```typescript
// Create optional resources based on configuration
const kmsKey =
    props.createKmsKey && !props.existingKmsKey
        ? new Key(scope, `${props.resourceName}-kms`, {
              enableKeyRotation: true,
              removalPolicy: RemovalPolicy.RETAIN,
          })
        : props.existingKmsKey;
```

### Helper Functions

```typescript
// util/resource-helpers.ts
export const createParameterGroup = (scope: Construct, props: ParameterGroupConfig): ParameterGroup => {
    return new ParameterGroup(scope, `${props.name}-params`, {
        description: props.description,
        parameters: props.parameters || {},
    });
};
```

## AWS Service-Specific Patterns

### Valid Values Documentation

Document valid values for service-specific properties:

```typescript
/**
 * Instance type for the resource.
 *
 * @remarks
 * Valid instance classes:
 * - T3: Burstable (MICRO, SMALL, MEDIUM, LARGE, XLARGE, XLARGE2)
 * - M6G: General purpose Graviton2 (LARGE and up)
 * - R6G: Memory optimized Graviton2 (LARGE and up, no MEDIUM)
 */
instanceType: InstanceType;
```

### Service Limits and Defaults

```typescript
// Validate against service limits
if (props.timeout && props.timeout.toSeconds() > 900) {
    throw new Error('Lambda timeout cannot exceed 900 seconds');
}

// Use service-specific defaults
const monitoringInterval = props.enableEnhancedMonitoring
    ? props.monitoringInterval || Duration.seconds(60) // RDS default
    : undefined;
```

## Integration with Root Project

### Add to bin/environment.ts

```typescript
export type ProjectEnvironment = EnvironmentConfig & {
    // ... existing configs

    myResource?: Partial<MyResourceProps>;
};

export const integrationEnvironments: ProjectEnvironment[] = [
    {
        ...devEnv,
        myResource: {
            resourceName: 'my-resource-dev',
        },
    },
];
```

### Add to bin/app.ts

```typescript
import {MyResourceStack} from '../examples/<service>/stacks/my-resource-stack';

integrationEnvironments.forEach(env => {
    // ... existing stacks

    if (env.myResource) {
        new MyResourceStack(app, `my-resource-${env.name}`, envProps);
    }
});
```

## Checklist for New Subpackages

- [ ] Package structure follows standard layout
- [ ] Factory functions use resource name from props (no id parameter)
- [ ] Resource IDs use resource name for specificity
- [ ] Supporting resources created automatically
- [ ] Types properly structured (base + variants)
- [ ] No unnecessary `Omit<>` type wrappers
- [ ] Sensible defaults provided
- [ ] Service-specific validations implemented
- [ ] Config resolver pattern for examples
- [ ] Placeholder values in base configs
- [ ] Example stacks for dev and prod
- [ ] Comprehensive TSDoc documentation
- [ ] Test coverage for all variants
- [ ] Package exports properly organized
- [ ] Package README with usage examples
- [ ] Root README.md updated with new package (compatibility matrix, dependency resolution, installation, build commands, publish commands, workspace structure)
- [ ] Integration with root project complete
