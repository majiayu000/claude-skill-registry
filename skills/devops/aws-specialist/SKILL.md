---
name: aws-specialist
description: /============================================================================/
---

/*============================================================================*/
/* AWS-SPECIALIST SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: aws-specialist
version: 1.0.0
description: |
  [assert|neutral] AWS cloud specialist for infrastructure as code with CloudFormation/CDK, serverless with Lambda, container orchestration with ECS/Fargate, database management with RDS, storage with S3/CloudFront CDN, [ground:given] [conf:0.95] [state:confirmed]
category: Cloud Platforms
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute aws-specialist workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic Cloud Platforms processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "aws-specialist",
  category: "Cloud Platforms",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["aws-specialist", "Cloud Platforms", "workflow"],
  context: "user needs aws-specialist capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# AWS Specialist

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Expert AWS cloud infrastructure design, deployment, and optimization for production-grade applications.

## Purpose

Comprehensive AWS expertise across IaC (CloudFormation, CDK), serverless (Lambda), containers (ECS/Fargate), databases (RDS, DynamoDB), storage (S3), CDN (CloudFront), and DevOps automation. Ensures AWS architectures are secure, cost-effective, and scalable.

## When to Use

- Deploying applications to AWS
- Creating infrastructure as code templates
- Setting up serverless architectures
- Configuring auto-scaling and load balancing
- Implementing multi-region deployments
- Optimizing AWS costs (FinOps)
- Securing AWS resources with IAM

## Prerequisites

**Required**: AWS account, AWS CLI installed, basic understanding of cloud concepts

**Agent Assignments**: `cicd-engineer`, `system-architect`, `security-manager`, `perf-analyzer`

## Core Workflows

### Workflow 1: AWS CDK Infrastructure as Code

**Step 1: Initialize CDK Project**

```bash
mkdir my-infra && cd my-infra
npx cdk init app --language typescript
npm install @aws-cdk/aws-lambda @aws-cdk/aws-apigateway @aws-cdk/aws-dynamodb
```

**Step 2: Define Lambda + API Gateway Stack**

```typescript
// lib/api-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class ApiStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table
    const table = new dynamodb.Table(this, 'ItemsTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // ONLY for dev
    });

    // Lambda function
    const handler = new lambda.Function(this, 'ItemsHandler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'index.handler',
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    table.grantReadWriteData(handler);

    // API Gateway
    const api = new apigateway.RestApi(this, 'ItemsApi', {
      restApiName: 'Items Service',
    });

    const items = api.root.addResource('items');
    items.addMethod('GET', new apigateway.LambdaIntegration(handler));
    items.addMethod('POST', new apigateway.LambdaIntegration(handler));
  }
}
```

**Step 3: Deploy Stack**

```bash
# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy
cdk deploy
```

### Workflow 2: ECS Fargate Deployment

**Step 1: Create Fargate Service with CDK**

```typescript
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

export class FargateStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'MyVpc', { maxAzs: 2 });

    const cluster = new ecs.Cluster(this, 'MyCluster', { vpc });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef', {
      memoryLimitMiB: 512,
      cpu: 256,
    });

    taskDefinition.addContainer('web', {
      image: ecs.ContainerImage.fromRegistry('nginx'),
      portMappings: [{ containerPort: 80 }],
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'MyApp' }),
    });

    const service = new ecs.FargateService(this, 'Service', {
      cluster,
      taskDefinition,
      desiredCount: 2,
    });

    const lb = new elbv2.ApplicationLoadBalancer(this, 'LB', {
      vpc,
      internetFacing: true,
    });

    const listener = lb.addListener('Listener', { port: 80 });
    listener.addTargets('ECS', {
      port: 80,
      targets: [service],
      healthCheck: { path: '/' },
    });
  }
}
```

### Workflow 3:

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/Cloud Platforms/aws-specialist/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "aws-specialist-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>AWS_SPECIALIST_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
