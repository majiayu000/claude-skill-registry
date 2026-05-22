---
name: pulumi-stacks
description: Use when managing multiple environments with Pulumi stacks for development, staging, and production deployments.
allowed-tools: [Bash, Read]
---

# Pulumi Stacks

Manage multiple environments and configurations with Pulumi stacks for consistent infrastructure across development, staging, and production.

## Overview

Pulumi stacks are isolated, independently configurable instances of a Pulumi program. Each stack has its own state, configuration, and resources, enabling you to deploy the same infrastructure code to multiple environments.

## Stack Basics

### Creating and Selecting Stacks

```bash
# Initialize a new project
pulumi new aws-typescript

# Create a new stack
pulumi stack init dev

# List all stacks
pulumi stack ls

# Select a stack
pulumi stack select dev

# Show current stack
pulumi stack

# Remove a stack
pulumi stack rm dev
```

### Stack Configuration

```bash
# Set configuration values
pulumi config set aws:region us-east-1
pulumi config set instanceType t3.micro

# Set secret values (encrypted)
pulumi config set --secret dbPassword mySecurePassword123

# Get configuration values
pulumi config get aws:region

# List all configuration
pulumi config

# Remove configuration
pulumi config rm instanceType
```

## Stack Configuration Files

### Pulumi.yaml (Project File)

```yaml
name: my-infrastructure
runtime: nodejs
description: Multi-environment infrastructure

config:
  aws:region:
    description: AWS region for deployment
    default: us-east-1
  instanceType:
    description: EC2 instance type
    default: t3.micro
  environment:
    description: Environment name
```

### Pulumi.dev.yaml (Stack Config)

```yaml
config:
  aws:region: us-east-1
  my-infrastructure:instanceType: t3.micro
  my-infrastructure:environment: development
  my-infrastructure:minSize: "1"
  my-infrastructure:maxSize: "3"
  my-infrastructure:enableMonitoring: "false"
```

### Pulumi.staging.yaml

```yaml
config:
  aws:region: us-east-1
  my-infrastructure:instanceType: t3.small
  my-infrastructure:environment: staging
  my-infrastructure:minSize: "2"
  my-infrastructure:maxSize: "5"
  my-infrastructure:enableMonitoring: "true"
```

### Pulumi.prod.yaml

```yaml
config:
  aws:region: us-west-2
  my-infrastructure:instanceType: t3.medium
  my-infrastructure:environment: production
  my-infrastructure:minSize: "3"
  my-infrastructure:maxSize: "10"
  my-infrastructure:enableMonitoring: "true"
  my-infrastructure:backupRetention: "30"
```

## Reading Configuration in Code

### TypeScript Configuration

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Get configuration
const config = new pulumi.Config();
const instanceType = config.get("instanceType") || "t3.micro";
const environment = config.require("environment");
const minSize = config.getNumber("minSize") || 1;
const maxSize = config.getNumber("maxSize") || 3;
const enableMonitoring = config.getBoolean("enableMonitoring") || false;

// Get secret
const dbPassword = config.requireSecret("dbPassword");

// Use configuration
const instance = new aws.ec2.Instance("web-server", {
    instanceType: instanceType,
    ami: "ami-0c55b159cbfafe1f0",
    tags: {
        Name: `web-server-${environment}`,
        Environment: environment,
    },
    monitoring: enableMonitoring,
});

// Export stack name
export const stackName = pulumi.getStack();
export const instanceId = instance.id;
```

### Python Configuration

```python
import pulumi
import pulumi_aws as aws

# Get configuration
config = pulumi.Config()
instance_type = config.get("instanceType") or "t3.micro"
environment = config.require("environment")
min_size = config.get_int("minSize") or 1
max_size = config.get_int("maxSize") or 3
enable_monitoring = config.get_bool("enableMonitoring") or False

# Get secret
db_password = config.require_secret("dbPassword")

# Use configuration
instance = aws.ec2.Instance(
    "web-server",
    instance_type=instance_type,
    ami="ami-0c55b159cbfafe1f0",
    tags={
        "Name": f"web-server-{environment}",
        "Environment": environment,
    },
    monitoring=enable_monitoring,
)

# Export outputs
pulumi.export("stack_name", pulumi.get_stack())
pulumi.export("instance_id", instance.id)
```

## Environment-Specific Resources

### Conditional Resource Creation

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");
const enableHighAvailability = config.getBoolean("enableHA") || false;

// Create VPC
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    tags: {
        Name: `vpc-${environment}`,
        Environment: environment,
    },
});

// Production gets multiple availability zones
const azCount = environment === "production" ? 3 : 1;
const subnets: aws.ec2.Subnet[] = [];

for (let i = 0; i < azCount; i++) {
    const subnet = new aws.ec2.Subnet(`subnet-${i}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${i}.0/24`,
        availabilityZone: `us-east-1${String.fromCharCode(97 + i)}`,
        tags: {
            Name: `subnet-${environment}-${i}`,
            Environment: environment,
        },
    });
    subnets.push(subnet);
}

// Only create NAT gateway in production
let natGateway: aws.ec2.NatGateway | undefined;
if (environment === "production") {
    const eip = new aws.ec2.Eip("nat-eip", {
        vpc: true,
    });

    natGateway = new aws.ec2.NatGateway("nat", {
        allocationId: eip.id,
        subnetId: subnets[0].id,
        tags: {
            Name: `nat-${environment}`,
            Environment: environment,
        },
    });
}

// Create RDS with multi-AZ only in production
const db = new aws.rds.Instance("database", {
    engine: "postgres",
    engineVersion: "14.7",
    instanceClass: environment === "production" ? "db.t3.medium" : "db.t3.micro",
    allocatedStorage: environment === "production" ? 100 : 20,
    dbName: "myapp",
    username: "admin",
    password: config.requireSecret("dbPassword"),
    multiAz: environment === "production",
    backupRetentionPeriod: environment === "production" ? 30 : 7,
    skipFinalSnapshot: environment !== "production",
    tags: {
        Name: `db-${environment}`,
        Environment: environment,
    },
});

export const vpcId = vpc.id;
export const subnetIds = subnets.map(s => s.id);
export const dbEndpoint = db.endpoint;
```

## Stack References

### Cross-Stack References

```typescript
// Infrastructure stack (infra/index.ts)
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const vpc = new aws.ec2.Vpc("shared-vpc", {
    cidrBlock: "10.0.0.0/16",
    tags: {
        Name: "shared-vpc",
    },
});

const subnet = new aws.ec2.Subnet("shared-subnet", {
    vpcId: vpc.id,
    cidrBlock: "10.0.1.0/24",
    tags: {
        Name: "shared-subnet",
    },
});

// Export for other stacks
export const vpcId = vpc.id;
export const subnetId = subnet.id;
export const vpcCidr = vpc.cidrBlock;
```

```typescript
// Application stack (app/index.ts)
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Reference infrastructure stack
const infraStack = new pulumi.StackReference("myorg/infra/prod");

// Get outputs from infrastructure stack
const vpcId = infraStack.getOutput("vpcId");
const subnetId = infraStack.getOutput("subnetId");

// Use referenced values
const securityGroup = new aws.ec2.SecurityGroup("app-sg", {
    vpcId: vpcId,
    description: "Security group for application",
    ingress: [{
        protocol: "tcp",
        fromPort: 80,
        toPort: 80,
        cidrBlocks: ["0.0.0.0/0"],
    }],
});

const instance = new aws.ec2.Instance("app-server", {
    instanceType: "t3.micro",
    ami: "ami-0c55b159cbfafe1f0",
    subnetId: subnetId,
    vpcSecurityGroupIds: [securityGroup.id],
    tags: {
        Name: "app-server",
    },
});

export const instanceIp = instance.publicIp;
```

### Stack Reference Commands

```bash
# Deploy infrastructure stack first
cd infra
pulumi stack select prod
pulumi up

# Then deploy application stack
cd ../app
pulumi stack select prod
pulumi up

# View outputs from referenced stack
pulumi stack output --stack myorg/infra/prod
```

## Stack Outputs

### Exporting Stack Outputs

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");

// Create resources
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
});

const bucket = new aws.s3.Bucket("app-bucket", {
    bucket: `myapp-${environment}-bucket`,
});

const db = new aws.rds.Instance("database", {
    engine: "postgres",
    instanceClass: "db.t3.micro",
    allocatedStorage: 20,
    dbName: "myapp",
    username: "admin",
    password: config.requireSecret("dbPassword"),
    skipFinalSnapshot: true,
});

// Export outputs
export const vpcId = vpc.id;
export const vpcCidr = vpc.cidrBlock;
export const bucketName = bucket.id;
export const bucketArn = bucket.arn;
export const dbEndpoint = db.endpoint;
export const dbPort = db.port;

// Export computed values
export const dbConnectionString = pulumi.interpolate`postgresql://admin@${db.endpoint}/myapp`;

// Export stack metadata
export const stackName = pulumi.getStack();
export const projectName = pulumi.getProject();
export const region = aws.getRegion().then(r => r.name);
```

### Accessing Stack Outputs

```bash
# View all outputs
pulumi stack output

# Get specific output
pulumi stack output vpcId

# Get output as JSON
pulumi stack output --json

# Use in shell scripts
VPC_ID=$(pulumi stack output vpcId)
echo "VPC ID: $VPC_ID"

# Export to environment variables
export $(pulumi stack output --json | jq -r 'to_entries[] | "\(.key)=\(.value)"')
```

## Stack Transformations

### Global Resource Transformations

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");

// Register global transformation to add tags
pulumi.runtime.registerStackTransformation((args) => {
    if (args.type.startsWith("aws:")) {
        args.props.tags = {
            ...args.props.tags,
            Environment: environment,
            ManagedBy: "Pulumi",
            Stack: pulumi.getStack(),
        };
    }
    return {
        props: args.props,
        opts: args.opts,
    };
});

// All AWS resources automatically get tags
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    // tags will be automatically added by transformation
});

const bucket = new aws.s3.Bucket("data", {
    // tags will be automatically added by transformation
});
```

### Resource-Specific Transformations

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");

// Transformation to enforce encryption
const enforceEncryption = (args: pulumi.ResourceTransformationArgs) => {
    if (args.type === "aws:s3/bucket:Bucket") {
        args.props.serverSideEncryptionConfiguration = {
            rule: {
                applyServerSideEncryptionByDefault: {
                    sseAlgorithm: "AES256",
                },
            },
        };
    }

    if (args.type === "aws:rds/instance:Instance") {
        args.props.storageEncrypted = true;
    }

    return {
        props: args.props,
        opts: args.opts,
    };
};

pulumi.runtime.registerStackTransformation(enforceEncryption);

// Resources will be automatically encrypted
const bucket = new aws.s3.Bucket("data");
const db = new aws.rds.Instance("database", {
    engine: "postgres",
    instanceClass: "db.t3.micro",
    allocatedStorage: 20,
});
```

## Stack Tags and Organization

### Tagging Strategy

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");
const project = pulumi.getProject();
const stack = pulumi.getStack();

// Define common tags
const commonTags = {
    Project: project,
    Environment: environment,
    Stack: stack,
    ManagedBy: "Pulumi",
    CostCenter: config.get("costCenter") || "engineering",
    Owner: config.get("owner") || "platform-team",
};

// Helper function to merge tags
function mergeTags(resourceTags?: { [key: string]: string }): { [key: string]: string } {
    return {
        ...commonTags,
        ...resourceTags,
    };
}

// Use consistent tagging
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    tags: mergeTags({
        Name: `vpc-${environment}`,
        Type: "network",
    }),
});

const bucket = new aws.s3.Bucket("data", {
    tags: mergeTags({
        Name: `data-${environment}`,
        Type: "storage",
        Compliance: "required",
    }),
});

const db = new aws.rds.Instance("database", {
    engine: "postgres",
    instanceClass: "db.t3.micro",
    allocatedStorage: 20,
    tags: mergeTags({
        Name: `db-${environment}`,
        Type: "database",
        BackupRequired: "true",
    }),
});
```

## Stack Import and Export

### Exporting Stack State

```bash
# Export stack state to JSON
pulumi stack export > stack-state.json

# Export to file
pulumi stack export --file stack-backup.json

# Export with secrets in plaintext (use carefully!)
pulumi stack export --show-secrets > stack-with-secrets.json
```

### Importing Stack State

```bash
# Import stack state
pulumi stack import --file stack-state.json

# Import from stdin
cat stack-state.json | pulumi stack import
```

### Stack Migration

```bash
# Export from old stack
pulumi stack select old-stack
pulumi stack export --file old-stack.json

# Create and import to new stack
pulumi stack init new-stack
pulumi stack import --file old-stack.json

# Verify resources
pulumi preview
```

## Multi-Region Deployments

### Region-Specific Stacks

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const awsConfig = new pulumi.Config("aws");
const region = awsConfig.require("region");
const environment = config.require("environment");

// Create region-specific resources
const vpc = new aws.ec2.Vpc(`vpc-${region}`, {
    cidrBlock: "10.0.0.0/16",
    tags: {
        Name: `vpc-${environment}-${region}`,
        Region: region,
        Environment: environment,
    },
});

// Create CloudFront distribution in us-east-1
const usEast1Provider = new aws.Provider("us-east-1", {
    region: "us-east-1",
});

const certificate = new aws.acm.Certificate("cert", {
    domainName: `${environment}.example.com`,
    validationMethod: "DNS",
    tags: {
        Name: `cert-${environment}`,
        Environment: environment,
    },
}, { provider: usEast1Provider });

// Export region info
export const deploymentRegion = region;
export const vpcId = vpc.id;
export const certificateArn = certificate.arn;
```

### Multi-Region Stack Configuration

```yaml
# Pulumi.us-east-1-prod.yaml
config:
  aws:region: us-east-1
  my-app:environment: production
  my-app:isPrimaryRegion: "true"

# Pulumi.us-west-2-prod.yaml
config:
  aws:region: us-west-2
  my-app:environment: production
  my-app:isPrimaryRegion: "false"

# Pulumi.eu-west-1-prod.yaml
config:
  aws:region: eu-west-1
  my-app:environment: production
  my-app:isPrimaryRegion: "false"
```

## Stack Policies

### Protect Resources

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");

// Protect production databases
const db = new aws.rds.Instance("database", {
    engine: "postgres",
    instanceClass: "db.t3.micro",
    allocatedStorage: 20,
    tags: {
        Name: `db-${environment}`,
    },
}, {
    protect: environment === "production",
});

// Protect production storage
const bucket = new aws.s3.Bucket("data", {
    tags: {
        Name: `data-${environment}`,
    },
}, {
    protect: environment === "production",
});
```

### Retain Resources

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");

// Retain production databases on stack deletion
const db = new aws.rds.Instance("database", {
    engine: "postgres",
    instanceClass: "db.t3.micro",
    allocatedStorage: 20,
    finalSnapshotIdentifier: environment === "production"
        ? `final-snapshot-${Date.now()}`
        : undefined,
    skipFinalSnapshot: environment !== "production",
}, {
    retainOnDelete: environment === "production",
});
```

## Stack Secrets Management

### Using Encrypted Secrets

```bash
# Set encrypted secrets
pulumi config set --secret dbPassword mySecurePassword123
pulumi config set --secret apiKey sk_live_abc123xyz789

# View config (secrets are encrypted)
pulumi config

# View secrets in plaintext (use carefully!)
pulumi config get dbPassword --show-secrets
```

### Secrets in Code

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();

// Get secret values
const dbPassword = config.requireSecret("dbPassword");
const apiKey = config.requireSecret("apiKey");

// Use secrets in resources
const db = new aws.rds.Instance("database", {
    engine: "postgres",
    instanceClass: "db.t3.micro",
    allocatedStorage: 20,
    username: "admin",
    password: dbPassword,
});

// Create SSM parameters from secrets
const dbPasswordParam = new aws.ssm.Parameter("db-password", {
    name: "/app/database/password",
    type: "SecureString",
    value: dbPassword,
});

const apiKeyParam = new aws.ssm.Parameter("api-key", {
    name: "/app/api/key",
    type: "SecureString",
    value: apiKey,
});

// Secrets are encrypted in state
export const connectionString = pulumi.secret(
    pulumi.interpolate`postgresql://admin:${dbPassword}@${db.endpoint}/myapp`
);
```

## Stack Refresh and State

### Refresh Stack State

```bash
# Refresh stack to match actual cloud state
pulumi refresh

# Refresh with auto-approval
pulumi refresh --yes

# Refresh specific resources
pulumi refresh --target urn:pulumi:dev::myapp::aws:s3/bucket:Bucket::my-bucket

# Refresh and show diff
pulumi refresh --diff
```

### Stack State Management

```bash
# View stack state
pulumi stack --show-urns

# View specific resource
pulumi stack --show-urns | grep my-bucket

# Remove resource from state (doesn't delete cloud resource)
pulumi state delete 'urn:pulumi:dev::myapp::aws:s3/bucket:Bucket::my-bucket'

# Rename resource in state
pulumi state rename 'urn:pulumi:dev::myapp::aws:s3/bucket:Bucket::old-name' \
                     'urn:pulumi:dev::myapp::aws:s3/bucket:Bucket::new-name'
```

## When to Use This Skill

Use the `pulumi-stacks` skill when you need to:

- Deploy infrastructure to multiple environments (dev, staging, prod)
- Manage environment-specific configurations
- Create isolated instances of the same infrastructure
- Share infrastructure outputs between projects
- Implement multi-region deployments
- Separate infrastructure concerns (networking, databases, applications)
- Manage secrets per environment
- Track infrastructure state per environment
- Implement progressive deployment strategies
- Organize complex infrastructure into manageable units
- Apply environment-specific policies and protections
- Maintain consistent infrastructure across environments

## Best Practices

1. **Naming Convention**: Use consistent stack naming like `<env>` or `<region>-<env>` (e.g., `prod`, `us-east-1-prod`)
2. **Configuration Files**: Keep stack config files in version control (except secrets)
3. **Environment Isolation**: Never share state between environments; each environment gets its own stack
4. **Stack References**: Use stack references instead of duplicating infrastructure code
5. **Secrets Management**: Always use `--secret` flag for sensitive values
6. **Progressive Deployment**: Deploy to dev first, then staging, finally production
7. **State Backups**: Regularly export stack state for disaster recovery
8. **Resource Protection**: Enable `protect` option for critical production resources
9. **Tagging Strategy**: Apply consistent tags across all environments for cost tracking
10. **Stack Outputs**: Export all values needed by other stacks or external systems
11. **Configuration Validation**: Validate configuration values before creating resources
12. **Environment Parity**: Keep environments as similar as possible, differing only in scale
13. **Automation**: Use CI/CD pipelines for stack deployments
14. **Documentation**: Document stack dependencies and required configuration
15. **State Encryption**: Use encrypted state backends for sensitive infrastructure

## Common Pitfalls

1. **Hardcoded Values**: Hardcoding environment-specific values instead of using configuration
2. **Shared State**: Attempting to share stack state between environments
3. **Missing Config**: Deploying to new stack without setting required configuration
4. **Unencrypted Secrets**: Storing secrets as plain text in configuration
5. **Inconsistent Naming**: Using different naming conventions across stacks
6. **Broken References**: Stack references that point to non-existent stacks or outputs
7. **Missing Exports**: Not exporting values needed by dependent stacks
8. **Config Drift**: Manual changes to config files not reflected in version control
9. **No Resource Protection**: Forgetting to protect critical production resources
10. **Stack Sprawl**: Creating too many stacks without clear organization
11. **Missing Validation**: Not validating configuration before deployment
12. **Circular Dependencies**: Creating circular stack references
13. **No Backup Strategy**: Not exporting stack state for disaster recovery
14. **Environment Differences**: Production significantly different from other environments
15. **Poor Secret Management**: Checking encrypted secrets into public repositories without proper key management

## Resources

- [Pulumi Stack Documentation](https://www.pulumi.com/docs/intro/concepts/stack/)
- [Pulumi Configuration](https://www.pulumi.com/docs/intro/concepts/config/)
- [Stack References](https://www.pulumi.com/docs/intro/concepts/stack/#stackreferences)
- [Pulumi Secrets](https://www.pulumi.com/docs/intro/concepts/secrets/)
- [Stack Transformations](https://www.pulumi.com/docs/intro/concepts/resources/options/transformations/)
- [Organizing Projects and Stacks](https://www.pulumi.com/docs/guides/organizing-projects-stacks/)
