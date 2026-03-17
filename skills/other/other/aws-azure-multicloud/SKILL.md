---
name: AWS & Azure Multi-Cloud Expert
description: Expert guidance for deploying and managing applications across AWS and Azure cloud platforms. Use when deploying to AWS, Azure, managing cloud infrastructure, or implementing multi-cloud strategies.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# AWS & Azure Multi-Cloud Expert

Production deployment patterns for AWS and Azure.

## AWS Deployment Patterns

### Serverless with Lambda + API Gateway

```typescript
// AWS CDK Stack
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class ServerlessStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Table
    const table = new dynamodb.Table(this, 'Table', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    // Lambda Function
    const handler = new lambda.Function(this, 'Handler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'index.handler',
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    table.grantReadWriteData(handler);

    // API Gateway
    const api = new apigateway.RestApi(this, 'API', {
      restApiName: 'Serverless API',
      deployOptions: {
        stageName: 'prod',
        throttlingBurstLimit: 100,
        throttlingRateLimit: 50,
      },
    });

    const integration = new apigateway.LambdaIntegration(handler);
    api.root.addMethod('ANY', integration);
    api.root.addResource('{proxy+}').addMethod('ANY', integration);
  }
}
```

### ECS Fargate Deployment

```typescript
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

export class FargateStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string) {
    super(scope, id);

    const vpc = new ec2.Vpc(this, 'VPC', { maxAzs: 2 });

    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef', {
      memoryLimitMiB: 512,
      cpu: 256,
    });

    taskDefinition.addContainer('app', {
      image: ecs.ContainerImage.fromRegistry('myapp:latest'),
      portMappings: [{ containerPort: 8000 }],
      environment: {
        NODE_ENV: 'production',
      },
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'app' }),
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
      port: 8000,
      targets: [service],
      healthCheck: { path: '/health' },
    });
  }
}
```

### S3 + CloudFront CDN

```typescript
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';

const bucket = new s3.Bucket(this, 'WebsiteBucket', {
  websiteIndexDocument: 'index.html',
  publicReadAccess: true,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
});

const distribution = new cloudfront.Distribution(this, 'Distribution', {
  defaultBehavior: {
    origin: new origins.S3Origin(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
  },
  defaultRootObject: 'index.html',
});
```

## Azure Deployment Patterns

### Azure Functions

```typescript
// function.ts
import { AzureFunction, Context, HttpRequest } from "@azure/functions";

const httpTrigger: AzureFunction = async function (
  context: Context,
  req: HttpRequest
): Promise<void> {
  context.log('HTTP trigger function processed a request.');

  const name = req.query.name || (req.body && req.body.name);
  const responseMessage = name
    ? `Hello, ${name}!`
    : "Please pass a name on the query string or in the request body";

  context.res = {
    status: 200,
    body: responseMessage
  };
};

export default httpTrigger;
```

```json
// host.json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "maxTelemetryItemsPerSecond": 20
      }
    }
  }
}
```

### Azure Container Apps

```bash
# Deploy container to Azure Container Apps
az containerapp create \
  --name myapp \
  --resource-group myResourceGroup \
  --environment myEnvironment \
  --image myregistry.azurecr.io/myapp:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 2 \
  --max-replicas 10 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --env-vars \
    DATABASE_URL=secretref:db-url \
    REDIS_URL=secretref:redis-url
```

### Terraform for Multi-Cloud

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# AWS Resources
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
  acl    = "private"
}

# Azure Resources
resource "azurerm_storage_account" "data" {
  name                     = "mydatastorageaccount"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}
```

## Deployment Scripts

```bash
# AWS Deploy Script
#!/bin/bash
set -e

# Build and push Docker image
docker build -t myapp:latest .
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# Update ECS service
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --force-new-deployment
```

```bash
# Azure Deploy Script
#!/bin/bash
set -e

# Build and push Docker image
az acr build \
  --registry myregistry \
  --image myapp:latest \
  --file Dockerfile .

# Update Container App
az containerapp update \
  --name myapp \
  --resource-group myResourceGroup \
  --image myregistry.azurecr.io/myapp:latest
```

## Best Practices

✅ Use Infrastructure as Code (CDK, Terraform)
✅ Implement least-privilege IAM policies
✅ Enable logging and monitoring
✅ Use managed services when possible
✅ Implement auto-scaling
✅ Use secrets management (Secrets Manager, Key Vault)
✅ Enable encryption at rest and in transit
✅ Implement proper backup strategies
✅ Use cost optimization tools
✅ Implement multi-region redundancy

---

**When to Use:** Cloud deployments, AWS/Azure infrastructure, serverless applications, multi-cloud strategies.
