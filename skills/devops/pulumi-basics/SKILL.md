---
name: pulumi-basics
description: Use when writing infrastructure-as-code with Pulumi using programming languages for cloud resource provisioning.
allowed-tools: []
---

# Pulumi Basics

Infrastructure-as-code using real programming languages with Pulumi.

## Project Structure

```
my-infrastructure/
├── Pulumi.yaml       # Project file
├── Pulumi.dev.yaml   # Stack config
├── index.ts          # Main program
└── package.json
```

## Pulumi.yaml

```yaml
name: my-infrastructure
runtime: nodejs
description: My infrastructure project
```

## TypeScript Example

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Create VPC
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    tags: {
        Name: "main-vpc",
    },
});

// Create subnet
const subnet = new aws.ec2.Subnet("public", {
    vpcId: vpc.id,
    cidrBlock: "10.0.1.0/24",
    availabilityZone: "us-east-1a",
});

// Export outputs
export const vpcId = vpc.id;
export const subnetId = subnet.id;
```

## Common Commands

```bash
# Create new project
pulumi new aws-typescript

# Preview changes
pulumi preview

# Apply changes
pulumi up

# Destroy resources
pulumi destroy

# View stack outputs
pulumi stack output
```

## Configuration

```bash
# Set config
pulumi config set aws:region us-east-1

# Set secret
pulumi config set --secret dbPassword mySecret123

# Get config
pulumi config get aws:region
```

## Best Practices

### Use Stack References

```typescript
const infraStack = new pulumi.StackReference("org/infra/prod");
const vpcId = infraStack.getOutput("vpcId");
```

### Component Resources

```typescript
class MyApp extends pulumi.ComponentResource {
    constructor(name: string, args: MyAppArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:app:MyApp", name, {}, opts);
        
        // Create resources
    }
}
```
