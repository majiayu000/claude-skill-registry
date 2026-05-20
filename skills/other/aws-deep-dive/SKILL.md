---
description: AWS deep dive expert for CDK, EKS, Lambda, networking, and IAM. Designs production-grade architectures using CDK constructs, serverless patterns, and least-privilege IAM with cross-account access. Generates infrastructure ONE COMPONENT AT A TIME.
allowed-tools: Read, Write, Edit, Bash
model: opus
context: fork
---

# AWS Deep Dive Expert

## Purpose

Design and implement production-grade AWS infrastructure using CDK, with deep expertise in EKS, Lambda, networking, and IAM. Produces well-structured CDK stacks following AWS Well-Architected Framework principles.

## When to Use

- Writing AWS CDK stacks (TypeScript, Python)
- Creating or managing EKS clusters
- Designing Lambda-based architectures
- VPC design and network architecture
- IAM policy engineering and cross-account access
- Event-driven architectures (SQS, SNS, EventBridge)
- Choosing between CDK and Terraform for AWS

## AWS CDK

### Construct Levels

```
┌────────────────────────────────────────────────────────┐
│ L3 - Patterns (aws-solutions-constructs)               │
│   High-level, opinionated combinations of resources    │
│   Example: ApplicationLoadBalancedFargateService       │
├────────────────────────────────────────────────────────┤
│ L2 - Curated (default CDK constructs)                  │
│   AWS resource with sensible defaults and helpers      │
│   Example: s3.Bucket, lambda.Function                  │
├────────────────────────────────────────────────────────┤
│ L1 - CFN Resources (CfnBucket, CfnFunction)           │
│   1:1 CloudFormation mapping, no defaults              │
│   Use only when L2 doesn't expose a property           │
└────────────────────────────────────────────────────────┘

RULE: Always start with L2. Drop to L1 only for missing properties.
      Use L3 patterns for common architectures.
```

### Stack and Stage Organization

```typescript
// lib/app-stage.ts - Environment stage
import { Stage, StageProps, Tags } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { NetworkStack } from './network-stack';
import { ComputeStack } from './compute-stack';
import { DataStack } from './data-stack';

export interface AppStageProps extends StageProps {
  environment: 'dev' | 'staging' | 'production';
}

export class AppStage extends Stage {
  constructor(scope: Construct, id: string, props: AppStageProps) {
    super(scope, id, props);

    const network = new NetworkStack(this, 'Network', {
      environment: props.environment,
    });

    const data = new DataStack(this, 'Data', {
      environment: props.environment,
      vpc: network.vpc,
    });

    const compute = new ComputeStack(this, 'Compute', {
      environment: props.environment,
      vpc: network.vpc,
      database: data.database,
    });

    Tags.of(this).add('Environment', props.environment);
    Tags.of(this).add('ManagedBy', 'CDK');
  }
}
```

### CDK Pipelines for CI/CD

```typescript
// lib/pipeline-stack.ts
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as pipelines from 'aws-cdk-lib/pipelines';
import { AppStage } from './app-stage';

export class PipelineStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const pipeline = new pipelines.CodePipeline(this, 'Pipeline', {
      pipelineName: 'MyAppPipeline',
      synth: new pipelines.ShellStep('Synth', {
        input: pipelines.CodePipelineSource.gitHub('myorg/myrepo', 'main', {
          authentication: SecretValue.secretsManager('github-token'),
        }),
        commands: [
          'npm ci',
          'npm run build',
          'npm run test',
          'npx cdk synth',
        ],
      }),
      crossAccountKeys: true,
      dockerEnabledForSynth: true,
    });

    // Dev stage (auto-deploy)
    pipeline.addStage(new AppStage(this, 'Dev', {
      environment: 'dev',
      env: { account: '111111111111', region: 'us-east-1' },
    }));

    // Staging with integration tests
    const staging = pipeline.addStage(new AppStage(this, 'Staging', {
      environment: 'staging',
      env: { account: '222222222222', region: 'us-east-1' },
    }));
    staging.addPost(
      new pipelines.ShellStep('IntegrationTest', {
        commands: ['npm run test:integration'],
      })
    );

    // Production with manual approval
    const production = pipeline.addStage(new AppStage(this, 'Production', {
      environment: 'production',
      env: { account: '333333333333', region: 'us-east-1' },
    }));
    production.addPre(new pipelines.ManualApprovalStep('PromoteToProd'));
  }
}
```

### CDK Testing

```typescript
// test/network-stack.test.ts
import { App } from 'aws-cdk-lib';
import { Template, Match } from 'aws-cdk-lib/assertions';
import { NetworkStack } from '../lib/network-stack';

describe('NetworkStack', () => {
  const app = new App();
  const stack = new NetworkStack(app, 'TestNetwork', {
    environment: 'production',
  });
  const template = Template.fromStack(stack);

  // Assertion testing
  test('creates VPC with correct CIDR', () => {
    template.hasResourceProperties('AWS::EC2::VPC', {
      CidrBlock: '10.0.0.0/16',
      EnableDnsHostnames: true,
      EnableDnsSupport: true,
    });
  });

  test('creates private subnets in 3 AZs', () => {
    template.resourceCountIs('AWS::EC2::Subnet', 6); // 3 public + 3 private
  });

  test('NAT Gateway exists for production', () => {
    template.resourceCountIs('AWS::EC2::NatGateway', 3);
  });

  // Match helpers for complex assertions
  test('security group allows HTTPS inbound', () => {
    template.hasResourceProperties('AWS::EC2::SecurityGroup', {
      SecurityGroupIngress: Match.arrayWith([
        Match.objectLike({
          IpProtocol: 'tcp',
          FromPort: 443,
          ToPort: 443,
        }),
      ]),
    });
  });

  // Snapshot testing (detect unintended changes)
  test('matches snapshot', () => {
    expect(template.toJSON()).toMatchSnapshot();
  });
});
```

### CDK vs Terraform Decision Framework

```
┌──────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria             │ AWS CDK              │ Terraform            │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Multi-cloud          │ AWS only             │ Any provider         │
│ Language             │ TypeScript/Python/etc│ HCL                  │
│ Type safety          │ Full (TypeScript)    │ Limited              │
│ Abstraction level    │ L1/L2/L3 constructs  │ Modules              │
│ State management     │ CloudFormation       │ State file (S3/etc)  │
│ Drift detection      │ CloudFormation       │ terraform plan       │
│ Existing team skill  │ Developers love it   │ Ops teams prefer it  │
│ Testing              │ CDK assertions       │ Terratest/OPA        │
│ Import existing      │ cdk import           │ terraform import     │
│ Community modules    │ constructs.dev       │ registry.terraform.io│
│ Execution speed      │ Slower (CFN)         │ Faster (direct API)  │
│ Rollback             │ Automatic (CFN)      │ Manual               │
└──────────────────────┴──────────────────────┴──────────────────────┘

GUIDANCE:
- AWS-only shop with strong dev culture → CDK
- Multi-cloud or platform team → Terraform
- Rapid prototyping → CDK (less boilerplate)
- Compliance-heavy (audit trail) → CDK (CloudFormation changesets)
```

## EKS (Elastic Kubernetes Service)

### Cluster with CDK

```typescript
// lib/eks-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as eks from 'aws-cdk-lib/aws-eks';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';

export class EksStack extends cdk.Stack {
  public readonly cluster: eks.Cluster;

  constructor(scope: Construct, id: string, props: EksStackProps) {
    super(scope, id, props);

    // EKS Cluster
    this.cluster = new eks.Cluster(this, 'Cluster', {
      version: eks.KubernetesVersion.V1_30,
      vpc: props.vpc,
      vpcSubnets: [{ subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }],
      defaultCapacity: 0, // We manage node groups explicitly
      endpointAccess: eks.EndpointAccess.PRIVATE,
      clusterLogging: [
        eks.ClusterLoggingTypes.API,
        eks.ClusterLoggingTypes.AUDIT,
        eks.ClusterLoggingTypes.AUTHENTICATOR,
      ],
    });

    // Managed node group (general workloads)
    this.cluster.addNodegroupCapacity('GeneralNodes', {
      instanceTypes: [
        new ec2.InstanceType('m7i.xlarge'),
        new ec2.InstanceType('m6i.xlarge'),
      ],
      minSize: 3,
      maxSize: 20,
      desiredSize: 3,
      diskSize: 100,
      amiType: eks.NodegroupAmiType.AL2023_X86_64_STANDARD,
      labels: { 'workload-type': 'general' },
      capacityType: eks.CapacityType.ON_DEMAND,
    });

    // Spot node group (cost optimization for non-critical)
    this.cluster.addNodegroupCapacity('SpotNodes', {
      instanceTypes: [
        new ec2.InstanceType('m6i.xlarge'),
        new ec2.InstanceType('m5.xlarge'),
        new ec2.InstanceType('m5a.xlarge'),
        new ec2.InstanceType('c6i.xlarge'),
      ],
      minSize: 0,
      maxSize: 30,
      desiredSize: 2,
      capacityType: eks.CapacityType.SPOT,
      labels: { 'workload-type': 'spot' },
      taints: [{
        key: 'spot-instance',
        value: 'true',
        effect: eks.TaintEffect.NO_SCHEDULE,
      }],
    });

    // Fargate profile for system workloads
    this.cluster.addFargateProfile('SystemProfile', {
      selectors: [
        { namespace: 'kube-system', labels: { 'fargate': 'true' } },
        { namespace: 'external-secrets' },
      ],
    });
  }
}
```

### Karpenter Autoscaling

```yaml
# Karpenter NodePool (replaces Cluster Autoscaler)
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: general
spec:
  template:
    metadata:
      labels:
        workload-type: general
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["m", "c", "r"]
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["5"]
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["large", "xlarge", "2xlarge"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: "200"
    memory: 800Gi
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 60s
---
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiSelectorTerms:
    - alias: al2023@latest
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-cluster
  role: KarpenterNodeRole
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 100Gi
        volumeType: gp3
        encrypted: true
```

### IAM Roles for Service Accounts (IRSA)

```typescript
// CDK: Create IRSA for a workload
const saRole = new iam.Role(this, 'AppServiceAccountRole', {
  assumedBy: new iam.FederatedPrincipal(
    cluster.openIdConnectProvider.openIdConnectProviderArn,
    {
      'StringEquals': {
        [`${cluster.clusterOpenIdConnectIssuer}:sub`]:
          'system:serviceaccount:production:myapp-sa',
        [`${cluster.clusterOpenIdConnectIssuer}:aud`]:
          'sts.amazonaws.com',
      },
    },
    'sts:AssumeRoleWithWebIdentity'
  ),
});

// Grant specific permissions
const bucket = s3.Bucket.fromBucketName(this, 'DataBucket', 'my-data-bucket');
bucket.grantRead(saRole);

// Create the K8s service account
cluster.addManifest('AppSA', {
  apiVersion: 'v1',
  kind: 'ServiceAccount',
  metadata: {
    name: 'myapp-sa',
    namespace: 'production',
    annotations: {
      'eks.amazonaws.com/role-arn': saRole.roleArn,
    },
  },
});
```

### EKS Add-ons

```typescript
// Essential EKS add-ons
const addons = [
  { name: 'coredns', version: 'v1.11.1-eksbuild.6' },
  { name: 'vpc-cni', version: 'v1.18.1-eksbuild.1' },
  { name: 'kube-proxy', version: 'v1.30.0-eksbuild.3' },
  { name: 'aws-ebs-csi-driver', version: 'v1.31.0-eksbuild.1' },
];

for (const addon of addons) {
  new eks.CfnAddon(this, `Addon-${addon.name}`, {
    clusterName: cluster.clusterName,
    addonName: addon.name,
    addonVersion: addon.version,
    resolveConflicts: 'OVERWRITE',
  });
}

// ALB Ingress Controller via Helm
cluster.addHelmChart('AWSLoadBalancerController', {
  chart: 'aws-load-balancer-controller',
  repository: 'https://aws.github.io/eks-charts',
  namespace: 'kube-system',
  values: {
    clusterName: cluster.clusterName,
    serviceAccount: {
      create: true,
      name: 'aws-load-balancer-controller',
      annotations: {
        'eks.amazonaws.com/role-arn': lbControllerRole.roleArn,
      },
    },
  },
});
```

## Lambda

### Function Patterns

```typescript
// API Gateway + Lambda
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import * as nodejs from 'aws-cdk-lib/aws-lambda-nodejs';

// Node.js Lambda with bundling
const apiHandler = new nodejs.NodejsFunction(this, 'ApiHandler', {
  entry: 'src/handlers/api.ts',
  handler: 'handler',
  runtime: lambda.Runtime.NODEJS_22_X,
  architecture: lambda.Architecture.ARM_64,
  memorySize: 1024,
  timeout: cdk.Duration.seconds(30),
  environment: {
    TABLE_NAME: table.tableName,
    POWERTOOLS_SERVICE_NAME: 'myapp-api',
    POWERTOOLS_LOG_LEVEL: 'INFO',
    NODE_OPTIONS: '--enable-source-maps',
  },
  bundling: {
    minify: true,
    sourceMap: true,
    externalModules: ['@aws-sdk/*'], // Use Lambda-provided SDK
  },
  tracing: lambda.Tracing.ACTIVE,
  insightsVersion: lambda.LambdaInsightsVersion.VERSION_1_0_229_0,
});

// Grant DynamoDB access
table.grantReadWriteData(apiHandler);

// HTTP API Gateway
const httpApi = new apigw.HttpApi(this, 'HttpApi', {
  corsPreflight: {
    allowOrigins: ['https://myapp.com'],
    allowMethods: [apigw.CorsHttpMethod.ANY],
    allowHeaders: ['Content-Type', 'Authorization'],
  },
});

httpApi.addRoutes({
  path: '/api/{proxy+}',
  methods: [apigw.HttpMethod.ANY],
  integration: new HttpLambdaIntegration('ApiIntegration', apiHandler),
});
```

### SQS-Triggered Lambda

```typescript
// SQS → Lambda with DLQ and batch processing
const dlq = new sqs.Queue(this, 'DLQ', {
  retentionPeriod: cdk.Duration.days(14),
});

const queue = new sqs.Queue(this, 'OrderQueue', {
  visibilityTimeout: cdk.Duration.minutes(6), // 6x Lambda timeout
  deadLetterQueue: { queue: dlq, maxReceiveCount: 3 },
  encryption: sqs.QueueEncryption.KMS_MANAGED,
});

const processor = new nodejs.NodejsFunction(this, 'OrderProcessor', {
  entry: 'src/handlers/process-order.ts',
  timeout: cdk.Duration.minutes(1),
  reservedConcurrentExecutions: 10, // Protect downstream services
});

processor.addEventSource(new SqsEventSource(queue, {
  batchSize: 10,
  maxBatchingWindow: cdk.Duration.seconds(5),
  reportBatchItemFailures: true, // Partial batch failure support
}));
```

### EventBridge Pattern

```typescript
// EventBridge: Event-driven with schema
const bus = new events.EventBus(this, 'AppBus', {
  eventBusName: 'myapp-events',
});

// Rule: Route order events to processor
new events.Rule(this, 'OrderCreatedRule', {
  eventBus: bus,
  eventPattern: {
    source: ['myapp.orders'],
    detailType: ['OrderCreated'],
    detail: {
      total: [{ numeric: ['>', 100] }], // Only high-value orders
    },
  },
  targets: [new targets.LambdaFunction(orderProcessor)],
});

// Rule: Archive all events for replay
new events.Rule(this, 'ArchiveAll', {
  eventBus: bus,
  eventPattern: { source: [{ prefix: 'myapp.' }] },
  targets: [new targets.KinesisFirehoseStream(deliveryStream)],
});
```

### Powertools for AWS Lambda

```typescript
// src/handlers/api.ts
import { Logger } from '@aws-lambda-powertools/logger';
import { Tracer } from '@aws-lambda-powertools/tracer';
import { Metrics, MetricUnit } from '@aws-lambda-powertools/metrics';
import { injectLambdaContext } from '@aws-lambda-powertools/logger/middleware';
import { captureLambdaHandler } from '@aws-lambda-powertools/tracer/middleware';
import { logMetrics } from '@aws-lambda-powertools/metrics/middleware';
import middy from '@middy/core';

const logger = new Logger();
const tracer = new Tracer();
const metrics = new Metrics();

const lambdaHandler = async (event: APIGatewayProxyEventV2) => {
  logger.info('Processing request', { path: event.rawPath });

  metrics.addMetric('RequestCount', MetricUnit.Count, 1);

  const segment = tracer.getSegment();
  const subsegment = segment?.addNewSubsegment('ProcessOrder');

  try {
    // Business logic here
    const result = await processOrder(event);
    metrics.addMetric('SuccessCount', MetricUnit.Count, 1);
    return { statusCode: 200, body: JSON.stringify(result) };
  } catch (error) {
    metrics.addMetric('ErrorCount', MetricUnit.Count, 1);
    logger.error('Request failed', { error });
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal error' }) };
  } finally {
    subsegment?.close();
  }
};

// Middleware chain
export const handler = middy(lambdaHandler)
  .use(injectLambdaContext(logger, { logEvent: true }))
  .use(captureLambdaHandler(tracer))
  .use(logMetrics(metrics, { captureColdStartMetric: true }));
```

### Cold Start Optimization

```
COLD START REDUCTION STRATEGIES (in order of impact):

1. Use ARM64 (Graviton)          → 10-20% faster, 20% cheaper
2. Minimize bundle size          → Tree-shake, externalize SDK
3. Increase memory               → More memory = more CPU = faster init
4. Use SnapStart (Java)          → Near-zero cold start for Java
5. Provisioned Concurrency       → Pre-warm N instances (costs money)
6. Keep functions focused         → Smaller dependency tree
7. Lazy-load heavy dependencies   → Import inside handler, not top-level

MEMORY vs PERFORMANCE:
┌────────────┬─────────┬──────────┬───────────┐
│ Memory     │ vCPU    │ Cold ms  │ Cost/1M   │
├────────────┼─────────┼──────────┼───────────┤
│ 128 MB     │ 0.08    │ 800-2000 │ $0.21     │
│ 512 MB     │ 0.33    │ 400-800  │ $0.83     │
│ 1024 MB    │ 0.58    │ 200-500  │ $1.67     │
│ 1769 MB    │ 1.0     │ 150-300  │ $2.92     │
│ 3072 MB    │ 1.75    │ 100-250  │ $5.00     │
└────────────┴─────────┴──────────┴───────────┘

Sweet spot for Node.js: 1024-1769 MB
```

## Networking

### VPC Design

```typescript
// lib/network-stack.ts - Production VPC
export class NetworkStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props: NetworkStackProps) {
    super(scope, id, props);

    this.vpc = new ec2.Vpc(this, 'VPC', {
      ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
      maxAzs: 3,
      natGateways: props.environment === 'production' ? 3 : 1,
      subnetConfiguration: [
        {
          cidrMask: 20,
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 20,
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
          cidrMask: 24,
          name: 'Isolated',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        },
      ],
      flowLogs: {
        'FlowLogAll': {
          destination: ec2.FlowLogDestination.toCloudWatchLogs(),
          trafficType: ec2.FlowLogTrafficType.ALL,
        },
      },
    });

    // VPC Endpoints (avoid NAT costs for AWS services)
    this.vpc.addGatewayEndpoint('S3Endpoint', {
      service: ec2.GatewayVpcEndpointAwsService.S3,
    });
    this.vpc.addGatewayEndpoint('DynamoEndpoint', {
      service: ec2.GatewayVpcEndpointAwsService.DYNAMODB,
    });
    this.vpc.addInterfaceEndpoint('ECREndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.ECR,
    });
    this.vpc.addInterfaceEndpoint('ECRDockerEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
    });
    this.vpc.addInterfaceEndpoint('SecretsManagerEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
    });
  }
}
```

### Security Groups vs NACLs

```
┌──────────────────────┬──────────────────────┬──────────────────────┐
│ Feature              │ Security Groups      │ NACLs                │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Level                │ Instance (ENI)       │ Subnet               │
│ State                │ Stateful             │ Stateless            │
│ Rules                │ Allow only           │ Allow + Deny         │
│ Evaluation           │ All rules evaluated  │ Rules in order       │
│ Default              │ Deny all inbound     │ Allow all            │
│ Return traffic       │ Automatic            │ Must explicitly allow│
│ Use case             │ Primary defense      │ Subnet-level guard   │
└──────────────────────┴──────────────────────┴──────────────────────┘

BEST PRACTICE: Use Security Groups for application-level rules.
              Use NACLs sparingly for subnet-level deny rules
              (e.g., block known bad IP ranges).
```

## IAM

### Least Privilege Patterns

```typescript
// CDK: Fine-grained IAM with conditions
const processorRole = new iam.Role(this, 'ProcessorRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
  description: 'Role for order processing Lambda',
});

// Scoped to specific resources
processorRole.addToPolicy(new iam.PolicyStatement({
  actions: ['dynamodb:PutItem', 'dynamodb:GetItem', 'dynamodb:Query'],
  resources: [
    table.tableArn,
    `${table.tableArn}/index/*`,
  ],
  conditions: {
    'ForAllValues:StringEquals': {
      'dynamodb:LeadingKeys': ['ORDER#*'], // Only order items
    },
  },
}));

// Permission boundary (org-wide guardrails)
const boundary = new iam.ManagedPolicy(this, 'Boundary', {
  statements: [
    new iam.PolicyStatement({
      effect: iam.Effect.DENY,
      actions: [
        'iam:CreateUser',
        'iam:CreateAccessKey',
        'organizations:*',
        'account:*',
      ],
      resources: ['*'],
    }),
    new iam.PolicyStatement({
      effect: iam.Effect.DENY,
      actions: ['*'],
      resources: ['*'],
      conditions: {
        'StringNotEquals': {
          'aws:RequestedRegion': ['us-east-1', 'us-west-2'],
        },
      },
    }),
  ],
});

processorRole.addManagedPolicy(boundary);
```

### Cross-Account Access

```typescript
// Account A: Role that Account B can assume
const crossAccountRole = new iam.Role(this, 'CrossAccountRole', {
  roleName: 'SharedDataAccess',
  assumedBy: new iam.AccountPrincipal('222222222222'), // Account B
  externalId: 'unique-external-id', // Confused deputy protection
  maxSessionDuration: cdk.Duration.hours(1),
});

bucket.grantRead(crossAccountRole);

// Account B: Assume the role
const assumeRolePolicy = new iam.PolicyStatement({
  actions: ['sts:AssumeRole'],
  resources: ['arn:aws:iam::111111111111:role/SharedDataAccess'],
  conditions: {
    'StringEquals': {
      'sts:ExternalId': 'unique-external-id',
    },
  },
});
```

## Common Architecture Patterns

### 3-Tier Web Application

```typescript
// ALB → ECS Fargate → RDS Aurora
const cluster = new ecs.Cluster(this, 'Cluster', { vpc });

const service = new ecsPatterns.ApplicationLoadBalancedFargateService(
  this, 'WebService', {
    cluster,
    cpu: 1024,
    memoryLimitMiB: 2048,
    desiredCount: 3,
    taskImageOptions: {
      image: ecs.ContainerImage.fromEcrRepository(repo, 'latest'),
      containerPort: 8080,
      environment: {
        DB_HOST: aurora.clusterEndpoint.hostname,
      },
      secrets: {
        DB_PASSWORD: ecs.Secret.fromSecretsManager(dbSecret, 'password'),
      },
    },
    publicLoadBalancer: true,
    certificate: cert,
    redirectHTTP: true,
    circuitBreaker: { enable: true, rollback: true },
  }
);

// Auto-scaling
const scaling = service.service.autoScaleTaskCount({
  minCapacity: 3,
  maxCapacity: 30,
});
scaling.scaleOnCpuUtilization('CpuScaling', {
  targetUtilizationPercent: 60,
  scaleInCooldown: cdk.Duration.seconds(300),
});
scaling.scaleOnRequestCount('RequestScaling', {
  requestsPerTarget: 1000,
  targetGroup: service.targetGroup,
});
```

### Event-Driven with Step Functions

```typescript
// Step Functions: Order processing pipeline
const validateOrder = new tasks.LambdaInvoke(this, 'ValidateOrder', {
  lambdaFunction: validateFn,
  resultPath: '$.validation',
});

const processPayment = new tasks.LambdaInvoke(this, 'ProcessPayment', {
  lambdaFunction: paymentFn,
  resultPath: '$.payment',
  retryOnServiceExceptions: true,
});

const sendNotification = new tasks.SnsPublish(this, 'Notify', {
  topic: notificationTopic,
  message: sfn.TaskInput.fromJsonPathAt('$.orderDetails'),
});

const failureHandler = new tasks.LambdaInvoke(this, 'HandleFailure', {
  lambdaFunction: failureFn,
});

// State machine definition
const definition = validateOrder
  .next(new sfn.Choice(this, 'IsValid?')
    .when(sfn.Condition.booleanEquals('$.validation.Payload.isValid', true),
      processPayment
        .addCatch(failureHandler, { errors: ['PaymentFailed'] })
        .next(sendNotification))
    .otherwise(failureHandler));

const stateMachine = new sfn.StateMachine(this, 'OrderPipeline', {
  definitionBody: sfn.DefinitionBody.fromChainable(definition),
  timeout: cdk.Duration.minutes(5),
  tracingEnabled: true,
  logs: {
    destination: logGroup,
    level: sfn.LogLevel.ALL,
  },
});
```

### Serverless API Pattern

```typescript
// API Gateway + Lambda + DynamoDB
const table = new dynamodb.TableV2(this, 'ApiTable', {
  tableName: 'myapp-data',
  partitionKey: { name: 'PK', type: dynamodb.AttributeType.STRING },
  sortKey: { name: 'SK', type: dynamodb.AttributeType.STRING },
  billing: dynamodb.Billing.onDemand(),
  pointInTimeRecovery: true,
  globalSecondaryIndexes: [{
    indexName: 'GSI1',
    partitionKey: { name: 'GSI1PK', type: dynamodb.AttributeType.STRING },
    sortKey: { name: 'GSI1SK', type: dynamodb.AttributeType.STRING },
  }],
});

// Single Lambda handling all routes (monolambda pattern)
const handler = new nodejs.NodejsFunction(this, 'ApiHandler', {
  entry: 'src/api/router.ts',
  runtime: lambda.Runtime.NODEJS_22_X,
  architecture: lambda.Architecture.ARM_64,
  memorySize: 1024,
  timeout: cdk.Duration.seconds(30),
  environment: {
    TABLE_NAME: table.tableName,
  },
});

table.grantReadWriteData(handler);

// HTTP API with JWT authorizer
const httpApi = new apigw.HttpApi(this, 'Api', {
  defaultAuthorizer: new HttpJwtAuthorizer(
    'CognitoAuth',
    `https://cognito-idp.us-east-1.amazonaws.com/${userPool.userPoolId}`,
    { jwtAudience: [userPoolClient.userPoolClientId] }
  ),
});

httpApi.addRoutes({
  path: '/{proxy+}',
  methods: [apigw.HttpMethod.ANY],
  integration: new HttpLambdaIntegration('LambdaIntegration', handler),
});
```
