---
name: cdk-patterns
description: AWS CDK patterns for TypeScript. Use when working with CDK infrastructure code. Do NOT use for Terraform, CloudFormation YAML, or other IaC tools. JavaScript is prohibited for CDK.
durability: encoded-preference
---

# AWS CDK Patterns (TypeScript)

Patterns for AWS CDK infrastructure as code.

**IMPORTANT**: Always use TypeScript for CDK. JavaScript is prohibited.

## Construct Separation: When to Do It

### DO separate when:
- **Multiple instances needed** in same Stack with different config
- **Organization-wide reuse** as npm package
- **Unit testing** a specific piece of infrastructure

### DON'T separate when:
- Single use within a Stack → **function extraction is enough**
- No reuse planned → **YAGNI**
- Simple composition → avoid over-engineering

### Function extraction (often sufficient)
```typescript
export class MyStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props)

    const table = this.createDatabase()
    const api = this.createApi(table)
  }

  private createDatabase(): dynamodb.Table {
    return new dynamodb.Table(this, 'Table', { ... })
  }

  private createApi(table: dynamodb.Table): apigateway.RestApi {
    const handler = new lambda.Function(this, 'Handler', { ... })
    table.grantReadWriteData(handler)
    return new apigateway.RestApi(this, 'Api', { ... })
  }
}
```

## Stack Design

### Environment-based Stacks
```typescript
// bin/app.ts
const app = new cdk.App()

const envConfig = {
  dev: { account: '111111111111', region: 'ap-northeast-1' },
  prod: { account: '222222222222', region: 'ap-northeast-1' },
}

new MyStack(app, 'MyStack-Dev', { env: envConfig.dev, stage: 'dev' })
new MyStack(app, 'MyStack-Prod', { env: envConfig.prod, stage: 'prod' })
```

### Stack Props Pattern
```typescript
interface MyStackProps extends StackProps {
  stage: 'dev' | 'staging' | 'prod'
}

export class MyStack extends Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props)

    const isProd = props.stage === 'prod'

    new dynamodb.Table(this, 'Table', {
      billingMode: isProd
        ? dynamodb.BillingMode.PROVISIONED
        : dynamodb.BillingMode.PAY_PER_REQUEST,
    })
  }
}
```

## Props Design

### Required vs Optional
```typescript
interface MyConstructProps {
  // Required: no default makes sense
  tableName: string

  // Optional: sensible default exists
  readCapacity?: number
}

export class MyConstruct extends Construct {
  constructor(scope: Construct, id: string, props: MyConstructProps) {
    super(scope, id)

    const readCapacity = props.readCapacity ?? 5  // Default value
  }
}
```

### Exposing Resources
```typescript
export class MyConstruct extends Construct {
  // Expose for cross-construct references
  public readonly table: dynamodb.Table
  public readonly tableArn: string  // Convenience property

  constructor(scope: Construct, id: string) {
    super(scope, id)

    this.table = new dynamodb.Table(this, 'Table', { ... })
    this.tableArn = this.table.tableArn
  }
}
```

## Testing with CDK Assertions

### Snapshot Testing
```typescript
import { Template } from 'aws-cdk-lib/assertions'

test('Stack matches snapshot', () => {
  const app = new cdk.App()
  const stack = new MyStack(app, 'TestStack')
  const template = Template.fromStack(stack)

  expect(template.toJSON()).toMatchSnapshot()
})
```

### Resource Assertions
```typescript
test('Creates DynamoDB table with correct config', () => {
  const app = new cdk.App()
  const stack = new MyStack(app, 'TestStack', { stage: 'prod' })
  const template = Template.fromStack(stack)

  template.hasResourceProperties('AWS::DynamoDB::Table', {
    BillingMode: 'PROVISIONED',
  })
})

test('Lambda has correct IAM permissions', () => {
  const template = Template.fromStack(stack)

  template.hasResourceProperties('AWS::IAM::Policy', {
    PolicyDocument: {
      Statement: Match.arrayWith([
        Match.objectLike({
          Action: Match.arrayWith(['dynamodb:GetItem', 'dynamodb:PutItem']),
        }),
      ]),
    },
  })
})
```

### Resource Count
```typescript
test('Creates expected number of Lambda functions', () => {
  const template = Template.fromStack(stack)
  template.resourceCountIs('AWS::Lambda::Function', 3)
})
```
