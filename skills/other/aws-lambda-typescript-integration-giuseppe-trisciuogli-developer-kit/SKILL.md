---
name: aws-lambda-typescript-integration
description: Provides AWS Lambda integration patterns for TypeScript with cold start optimization. Use when deploying TypeScript functions to AWS Lambda, choosing between NestJS framework and raw TypeScript approaches, optimizing cold starts, configuring API Gateway or ALB integration, or implementing serverless TypeScript applications. Triggers include "create lambda typescript", "deploy typescript lambda", "nestjs lambda aws", "raw typescript lambda", "aws lambda typescript performance".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# AWS Lambda TypeScript Integration

Patterns for creating high-performance AWS Lambda functions in TypeScript with optimized cold starts.

## Overview

This skill provides complete patterns for AWS Lambda TypeScript development, covering two main approaches:

1. **NestJS Framework** - Full-featured framework with dependency injection, modular architecture, and extensive ecosystem
2. **Raw TypeScript** - Minimal overhead approach with maximum control and smaller bundle size

Both approaches support API Gateway and ALB integration with production-ready configurations.

## When to Use

Use this skill when:
- Creating new Lambda functions in TypeScript
- Migrating existing TypeScript applications to Lambda
- Optimizing cold start performance for TypeScript Lambda
- Choosing between framework-based and minimal TypeScript approaches
- Configuring API Gateway or ALB integration
- Setting up deployment pipelines for TypeScript Lambda

## Instructions

### 1. Choose Your Approach

| Approach | Cold Start | Bundle Size | Best For | Complexity |
|----------|------------|-------------|----------|------------|
| NestJS | < 500ms | Larger (100KB+) | Complex APIs, enterprise apps, DI needed | Medium |
| Raw TypeScript | < 100ms | Smaller (< 50KB) | Simple handlers, microservices, minimal deps | Low |

### 2. Project Structure

#### NestJS Structure
```
my-nestjs-lambda/
├── src/
│   ├── app.module.ts
│   ├── main.ts
│   ├── lambda.ts           # Lambda entry point
│   └── modules/
│       └── api/
├── package.json
├── tsconfig.json
└── serverless.yml
```

#### Raw TypeScript Structure
```
my-ts-lambda/
├── src/
│   ├── handlers/
│   │   └── api.handler.ts
│   ├── services/
│   └── utils/
├── dist/                   # Compiled output
├── package.json
├── tsconfig.json
└── template.yaml
```

### 3. Implementation Examples

See the [References](#references) section for detailed implementation guides. Quick examples:

**NestJS Handler:**
```typescript
// lambda.ts
import { NestFactory } from '@nestjs/core';
import { ExpressAdapter } from '@nestjs/platform-express';
import serverlessExpress from '@codegenie/serverless-express';
import { Context, Handler } from 'aws-lambda';
import express from 'express';
import { AppModule } from './src/app.module';

let cachedServer: Handler;

async function bootstrap(): Promise<Handler> {
  const expressApp = express();
  const adapter = new ExpressAdapter(expressApp);
  const nestApp = await NestFactory.create(AppModule, adapter);
  await nestApp.init();
  return serverlessExpress({ app: expressApp });
}

export const handler: Handler = async (event: any, context: Context) => {
  if (!cachedServer) {
    cachedServer = await bootstrap();
  }
  return cachedServer(event, context);
};
```

**Raw TypeScript Handler:**
```typescript
// src/handlers/api.handler.ts
import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';

export const handler = async (
  event: APIGatewayProxyEvent,
  context: Context
): Promise<APIGatewayProxyResult> => {
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello from TypeScript Lambda!' })
  };
};
```

## Core Concepts

### Cold Start Optimization

TypeScript cold start depends on bundle size and initialization code. Key strategies:

1. **Lazy Loading** - Defer heavy imports until needed
2. **Tree Shaking** - Remove unused code from bundle
3. **Minification** - Use esbuild or terser for smaller bundles
4. **Instance Caching** - Cache initialized services between invocations

See [Raw TypeScript Lambda](references/raw-typescript-lambda.md#cold-start-optimization) for detailed patterns.

### Connection Management

Create clients at module level and reuse:

```typescript
// GOOD: Initialize once, reuse across invocations
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

const dynamoClient = new DynamoDBClient({ region: process.env.AWS_REGION });

export const handler = async (event: APIGatewayProxyEvent) => {
  // Use dynamoClient - already initialized
};
```

### Environment Configuration

```typescript
// src/config/env.config.ts
export const env = {
  region: process.env.AWS_REGION || 'us-east-1',
  tableName: process.env.TABLE_NAME || '',
  debug: process.env.DEBUG === 'true',
};

// Validate required variables
if (!env.tableName) {
  throw new Error('TABLE_NAME environment variable is required');
}
```

## Best Practices

### Memory and Timeout Configuration

- **Memory**: Start with 512MB for NestJS, 256MB for raw TypeScript
- **Timeout**: Set based on cold start + expected processing time
  - NestJS: 10-30 seconds for cold start buffer
  - Raw TypeScript: 3-10 seconds typically sufficient

### Dependencies

Keep `package.json` minimal:

```json
{
  "dependencies": {
    "aws-lambda": "^3.1.0",
    "@aws-sdk/client-dynamodb": "^3.450.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "esbuild": "^0.19.0"
  }
}
```

### Error Handling

Return proper HTTP codes with structured errors:

```typescript
export const handler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  try {
    const result = await processEvent(event);
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result)
    };
  } catch (error) {
    console.error('Error processing request:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
};
```

### Logging

Use structured logging for CloudWatch Insights:

```typescript
const log = (level: string, message: string, meta?: object) => {
  console.log(JSON.stringify({
    level,
    message,
    timestamp: new Date().toISOString(),
    ...meta
  }));
};

log('info', 'Request processed', { requestId: context.awsRequestId });
```

## Deployment Options

### Quick Start

**Serverless Framework:**
```yaml
service: my-typescript-api

provider:
  name: aws
  runtime: nodejs20.x

functions:
  api:
    handler: dist/handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

**AWS SAM:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: dist/
      Handler: handler.handler
      Runtime: nodejs20.x
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

For complete deployment configurations including CI/CD, see [Serverless Deployment](references/serverless-deployment.md).

## Constraints and Warnings

### Lambda Limits

- **Deployment package**: 250MB unzipped maximum (50MB zipped)
- **Memory**: 128MB to 10GB
- **Timeout**: 15 minutes maximum
- **Concurrent executions**: 1000 default (adjustable)
- **Environment variables**: 4KB total size

### TypeScript-Specific Considerations

- **Bundle size**: TypeScript compiles to JavaScript; use bundlers to minimize size
- **Cold start**: Node.js 20.x offers best performance
- **Dependencies**: Use Lambda Layers for shared dependencies
- **Native modules**: Must be compiled for Amazon Linux 2

### Common Pitfalls

1. **Importing heavy libraries at module level** - Defer to lazy loading if not always needed
2. **Not bundling dependencies** - Include all production dependencies in the package
3. **Missing type definitions** - Install `@types/aws-lambda` for proper event typing
4. **No timeout handling** - Use `context.getRemainingTimeInMillis()` for long operations

### Security Considerations

- Never hardcode credentials; use IAM roles and environment variables
- **Input Validation for Event Data**: All incoming event data (API Gateway request bodies, S3 event objects, SQS message bodies) is untrusted external content; always validate and sanitize before processing to prevent injection attacks
- **Content Sanitization**: When processing S3 objects or SQS message payloads, treat the content as untrusted third-party data; apply appropriate validation, schema checks, and sanitization before acting on it
- Validate all input data
- Use least privilege IAM policies
- Enable CloudTrail for audit logging
- Sanitize logs to avoid leaking sensitive data

## References

For detailed guidance on specific topics:

- **[NestJS Lambda](references/nestjs-lambda.md)** - Complete NestJS setup, dependency injection, Express/Fastify adapters
- **[Raw TypeScript Lambda](references/raw-typescript-lambda.md)** - Minimal handler patterns, bundling, tree shaking
- **[Serverless Config](references/serverless-config.md)** - Serverless Framework and SAM configuration
- **[Serverless Deployment](references/serverless-deployment.md)** - CI/CD pipelines, environment management
- **[Testing](references/testing.md)** - Jest, integration testing, SAM Local

## Examples

### Example 1: Create a NestJS REST API

**Input:**
```
Create a TypeScript Lambda REST API using NestJS for a todo application
```

**Process:**
1. Initialize NestJS project with `nest new`
2. Install Lambda dependencies: `@codegenie/serverless-express`, `aws-lambda`
3. Create `lambda.ts` entry point with Express adapter
4. Configure `serverless.yml` with API Gateway events
5. Deploy with Serverless Framework

**Output:**
- Complete NestJS project structure
- REST API with CRUD endpoints
- DynamoDB integration
- Deployment configuration

### Example 2: Create a Raw TypeScript Lambda

**Input:**
```
Create a minimal TypeScript Lambda function with optimal cold start
```

**Process:**
1. Set up TypeScript project with esbuild
2. Create handler with proper AWS types
3. Configure minimal dependencies
4. Set up SAM or Serverless deployment
5. Optimize bundle size with tree shaking

**Output:**
- Minimal TypeScript Lambda project
- Optimized bundle < 50KB
- Cold start < 100ms

### Example 3: Deploy with GitHub Actions

**Input:**
```
Configure CI/CD for TypeScript Lambda with SAM
```

**Process:**
1. Create GitHub Actions workflow
2. Set up Node.js environment
3. Run tests with Jest
4. Bundle with esbuild
5. Deploy with SAM

**Output:**
- Complete `.github/workflows/deploy.yml`
- Multi-stage pipeline
- Integrated test automation

## Version

Version: 1.0.0
