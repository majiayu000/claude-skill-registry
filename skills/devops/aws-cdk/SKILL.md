---
name: aws-cdk
description: AWS Cloud Development Kit infrastructure as code patterns and best practices for serverless, containers, and cloud-native applications
---

# AWS CDK Skill

Infrastructure as Code (IaC) using AWS Cloud Development Kit with TypeScript/Python for building scalable cloud applications.

## When to Use This Skill

Activate this skill when the user:
- Requests AWS infrastructure setup
- Needs serverless application architecture
- Wants to define cloud resources as code
- Mentions "AWS CDK", "infrastructure as code", "CloudFormation", "serverless"
- Requires best practices for AWS resource management
- Asks about container orchestration (ECS, EKS)
- Needs API Gateway, Lambda, DynamoDB patterns

## Core Capabilities

### 1. Common CDK Patterns
- **Serverless API**: API Gateway + Lambda + DynamoDB
- **Static Website**: S3 + CloudFront + Route53
- **Container Service**: ECS Fargate + ALB + RDS
- **Event-Driven**: EventBridge + Lambda + SQS/SNS
- **Data Pipeline**: S3 + Lambda + Glue + Athena
- **CI/CD Pipeline**: CodePipeline + CodeBuild + CodeDeploy

### 2. CDK Constructs
- **L1 (CloudFormation)**: Direct CFN resources
- **L2 (Curated)**: AWS construct library
- **L3 (Patterns)**: High-level patterns
- **Custom Constructs**: Reusable components

### 3. Best Practices
- Multi-environment deployment (dev, staging, prod)
- Tagging and cost allocation
- Security best practices (IAM, VPC, encryption)
- Monitoring and logging (CloudWatch)
- Resource cleanup and lifecycle management

## Example Patterns

### Serverless API Stack
```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class ServerlessApiStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Table
    const table = new dynamodb.Table(this, 'ItemsTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Lambda Function
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
      description: 'This service manages items.',
    });

    const items = api.root.addResource('items');
    items.addMethod('GET', new apigateway.LambdaIntegration(handler));
    items.addMethod('POST', new apigateway.LambdaIntegration(handler));

    const item = items.addResource('{id}');
    item.addMethod('GET', new apigateway.LambdaIntegration(handler));
    item.addMethod('PUT', new apigateway.LambdaIntegration(handler));
    item.addMethod('DELETE', new apigateway.LambdaIntegration(handler));
  }
}
```

### Static Website with CloudFront
```typescript
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';

export class StaticWebsiteStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 Bucket
    const siteBucket = new s3.Bucket(this, 'SiteBucket', {
      websiteIndexDocument: 'index.html',
      websiteErrorDocument: 'error.html',
      publicReadAccess: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // CloudFront Distribution
    const distribution = new cloudfront.CloudFrontWebDistribution(this, 'SiteDistribution', {
      originConfigs: [{
        s3OriginSource: {
          s3BucketSource: siteBucket,
        },
        behaviors: [{ isDefaultBehavior: true }],
      }],
    });

    // Deploy site contents
    new s3deploy.BucketDeployment(this, 'DeployWebsite', {
      sources: [s3deploy.Source.asset('./website')],
      destinationBucket: siteBucket,
      distribution,
      distributionPaths: ['/*'],
    });

    new cdk.CfnOutput(this, 'DistributionDomainName', {
      value: distribution.distributionDomainName,
    });
  }
}
```

## Best Practices

### Do's
- ✅ Use typed constructs (TypeScript recommended)
- ✅ Separate stacks by lifecycle and team ownership
- ✅ Tag all resources for cost tracking
- ✅ Use environment variables for configuration
- ✅ Implement proper IAM least privilege
- ✅ Enable CloudWatch logs and metrics
- ✅ Use CDK context for environment-specific values
- ✅ Version lock your CDK dependencies

### Don'ts
- ❌ Don't hardcode sensitive values (use Secrets Manager)
- ❌ Don't create circular dependencies between stacks
- ❌ Don't forget to set removal policies
- ❌ Don't ignore CDK security warnings
- ❌ Don't deploy to production without testing

## Resources

- AWS CDK Docs: https://docs.aws.amazon.com/cdk/
- CDK Patterns: https://cdkpatterns.com/
- AWS Construct Library: https://docs.aws.amazon.com/cdk/api/v2/
