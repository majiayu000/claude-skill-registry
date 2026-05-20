---
name: aws-lambda
description: Build serverless applications with AWS Lambda and TypeScript. Covers handler patterns, API Gateway integration, DynamoDB operations, SQS/S3/DynamoDB Streams event sources, SAM templates, and CDK infrastructure. Use for serverless APIs, event-driven architectures, and AWS backend development.
---

# AWS Lambda Skill

Expert guidance for AWS Lambda with TypeScript, API Gateway, DynamoDB, and serverless patterns.

## Triggers

Use this skill when you see:
- aws lambda, lambda function, serverless aws
- api gateway, sam template, cdk lambda
- dynamodb streams, sqs handler, s3 trigger
- lambda handler, cold start, provisioned concurrency

## Instructions

### Lambda Handler Patterns

#### Basic Handler with TypeScript

```typescript
import type {
  APIGatewayProxyEvent,
  APIGatewayProxyResult,
  Context
} from 'aws-lambda';

export const handler = async (
  event: APIGatewayProxyEvent,
  context: Context
): Promise<APIGatewayProxyResult> => {
  try {
    const body = JSON.parse(event.body ?? '{}');

    // Your logic here
    const result = await processRequest(body);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(result),
    };
  } catch (error) {
    console.error('Error:', error);

    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};
```

#### Middleware Pattern with Middy

```typescript
import middy from '@middy/core';
import jsonBodyParser from '@middy/http-json-body-parser';
import httpErrorHandler from '@middy/http-error-handler';
import cors from '@middy/http-cors';
import validator from '@middy/validator';
import { transpileSchema } from '@middy/validator/transpile';

const inputSchema = {
  type: 'object',
  properties: {
    body: {
      type: 'object',
      properties: {
        email: { type: 'string', format: 'email' },
        name: { type: 'string', minLength: 1 },
      },
      required: ['email', 'name'],
    },
  },
};

const baseHandler = async (event: APIGatewayProxyEvent) => {
  const { email, name } = event.body as { email: string; name: string };

  const user = await createUser({ email, name });

  return {
    statusCode: 201,
    body: JSON.stringify(user),
  };
};

export const handler = middy(baseHandler)
  .use(jsonBodyParser())
  .use(validator({ eventSchema: transpileSchema(inputSchema) }))
  .use(httpErrorHandler())
  .use(cors());
```

### Event Source Handlers

#### SQS Handler

```typescript
import type { SQSEvent, SQSHandler } from 'aws-lambda';

export const sqsHandler: SQSHandler = async (event: SQSEvent) => {
  const results = await Promise.allSettled(
    event.Records.map(async (record) => {
      const message = JSON.parse(record.body);
      await processMessage(message);
    })
  );

  // Return batch item failures for partial batch response
  const failures = results
    .map((result, index) =>
      result.status === 'rejected'
        ? { itemIdentifier: event.Records[index].messageId }
        : null
    )
    .filter(Boolean);

  return { batchItemFailures: failures };
};
```

#### DynamoDB Streams Handler

```typescript
import type { DynamoDBStreamEvent, DynamoDBStreamHandler } from 'aws-lambda';
import { unmarshall } from '@aws-sdk/util-dynamodb';

export const streamHandler: DynamoDBStreamHandler = async (
  event: DynamoDBStreamEvent
) => {
  for (const record of event.Records) {
    if (record.eventName === 'INSERT' && record.dynamodb?.NewImage) {
      const item = unmarshall(record.dynamodb.NewImage);
      await handleNewItem(item);
    }
  }
};
```

#### S3 Handler

```typescript
import type { S3Event, S3Handler } from 'aws-lambda';

export const s3Handler: S3Handler = async (event: S3Event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '));

    await processS3Object(bucket, key);
  }
};
```

### DynamoDB Integration

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  QueryCommand,
  UpdateCommand,
} from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const TABLE_NAME = process.env.TABLE_NAME!;

// Get item
async function getUser(userId: string) {
  const result = await docClient.send(new GetCommand({
    TableName: TABLE_NAME,
    Key: { PK: `USER#${userId}`, SK: `USER#${userId}` },
  }));

  return result.Item;
}

// Put item
async function createUser(user: User) {
  await docClient.send(new PutCommand({
    TableName: TABLE_NAME,
    Item: {
      PK: `USER#${user.id}`,
      SK: `USER#${user.id}`,
      ...user,
      createdAt: new Date().toISOString(),
    },
    ConditionExpression: 'attribute_not_exists(PK)',
  }));
}

// Query with GSI
async function getUserOrders(userId: string) {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE_NAME,
    IndexName: 'GSI1',
    KeyConditionExpression: 'GSI1PK = :pk AND begins_with(GSI1SK, :sk)',
    ExpressionAttributeValues: {
      ':pk': `USER#${userId}`,
      ':sk': 'ORDER#',
    },
  }));

  return result.Items ?? [];
}
```

### SAM Template

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: nodejs20.x
    MemorySize: 256
    Architectures:
      - arm64
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: dist/handlers/api.handler
      Events:
        GetUsers:
          Type: Api
          Properties:
            Path: /users
            Method: GET
        CreateUser:
          Type: Api
          Properties:
            Path: /users
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
    Metadata:
      BuildMethod: esbuild
      BuildProperties:
        Minify: true
        Target: es2022

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE

Outputs:
  ApiUrl:
    Value: !Sub 'https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod'
```

### CDK Lambda

```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';

export class ApiStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string) {
    super(scope, id);

    const table = new dynamodb.Table(this, 'UsersTable', {
      partitionKey: { name: 'PK', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'SK', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    const fn = new NodejsFunction(this, 'ApiHandler', {
      entry: 'src/handlers/api.ts',
      runtime: lambda.Runtime.NODEJS_20_X,
      architecture: lambda.Architecture.ARM_64,
      environment: {
        TABLE_NAME: table.tableName,
      },
      bundling: {
        minify: true,
      },
    });

    table.grantReadWriteData(fn);

    new apigateway.LambdaRestApi(this, 'Api', {
      handler: fn,
    });
  }
}
```

## Best Practices

| Practice | Implementation |
|----------|----------------|
| **Cold starts** | Use ARM64, minimize dependencies, use provisioned concurrency for critical paths |
| **Connections** | Reuse SDK clients outside handler, use connection pooling |
| **Error handling** | Use structured error responses, implement retries with backoff |
| **Logging** | Use structured JSON logging, include request IDs |
| **Security** | Use IAM roles, validate input, encrypt sensitive data |

## Common Workflows

### New Lambda Function
1. Create handler file with TypeScript types
2. Add middleware for validation/error handling
3. Configure SAM/CDK template
4. Set up IAM permissions
5. Deploy and test

### Event-Driven Architecture
1. Define event source (SQS, S3, DynamoDB Streams)
2. Create event handler with proper typing
3. Implement batch failure handling
4. Configure DLQ for failed events
5. Monitor with CloudWatch
