---
name: aws-lambda
description: >-
  You are an expert in AWS Lambda, Amazon's serverless compute service. You
  help developers build event-driven applications using Lambda functions
  triggered by API Gateway, S3 events, SQS queues, DynamoDB streams, and
  scheduled events — with support for Node.js, Python, Go, Rust, Java, and
  container images, automatic scaling from zero to thousands of concurrent
  executions, and pay-per-invocation pricing.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Cloud & Serverless
  tags:
    - serverless
    - aws
    - functions
    - api-gateway
    - event-driven
    - cloud
---

# AWS Lambda — Serverless Functions

You are an expert in AWS Lambda, Amazon's serverless compute service. You help developers build event-driven applications using Lambda functions triggered by API Gateway, S3 events, SQS queues, DynamoDB streams, and scheduled events — with support for Node.js, Python, Go, Rust, Java, and container images, automatic scaling from zero to thousands of concurrent executions, and pay-per-invocation pricing.

## Core Capabilities

### Function Handlers

```typescript
// handler.ts — API Gateway Lambda (Node.js/TypeScript)
import { APIGatewayProxyHandlerV2 } from "aws-lambda";

export const handler: APIGatewayProxyHandlerV2 = async (event) => {
  const { httpMethod, pathParameters, body, queryStringParameters } = event;

  try {
    switch (httpMethod) {
      case "GET": {
        const id = pathParameters?.id;
        if (id) {
          const item = await db.get({ TableName: "users", Key: { id } });
          return { statusCode: 200, body: JSON.stringify(item.Item) };
        }
        const items = await db.scan({ TableName: "users" });
        return { statusCode: 200, body: JSON.stringify(items.Items) };
      }
      case "POST": {
        const data = JSON.parse(body || "{}");
        await db.put({ TableName: "users", Item: { id: uuid(), ...data } });
        return { statusCode: 201, body: JSON.stringify({ created: true }) };
      }
      default:
        return { statusCode: 405, body: "Method not allowed" };
    }
  } catch (error) {
    console.error(error);
    return { statusCode: 500, body: JSON.stringify({ error: "Internal error" }) };
  }
};
```

```python
# handler.py — S3 event trigger (Python)
import json
import boto3
from PIL import Image
import io

s3 = boto3.client("s3")

def handler(event, context):
    """Process uploaded images: resize and create thumbnails.

    Triggered by S3 PutObject events on the uploads/ prefix.
    """
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Download original
        response = s3.get_object(Bucket=bucket, Key=key)
        image = Image.open(io.BytesIO(response["Body"].read()))

        # Create thumbnail
        image.thumbnail((300, 300))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        # Upload thumbnail
        thumb_key = key.replace("uploads/", "thumbnails/")
        s3.put_object(
            Bucket=bucket,
            Key=thumb_key,
            Body=buffer,
            ContentType="image/jpeg",
        )

    return {"statusCode": 200, "processed": len(event["Records"])}
```

### Infrastructure as Code (SAM)

```yaml
# template.yaml — AWS SAM template
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: nodejs20.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: dist/handler.handler
      Events:
        GetUsers:
          Type: Api
          Properties:
            Path: /users
            Method: get
        CreateUser:
          Type: Api
          Properties:
            Path: /users
            Method: post
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable

  ImageProcessor:
    Type: AWS::Serverless::Function
    Properties:
      Handler: handler.handler
      Runtime: python3.12
      MemorySize: 1024
      Timeout: 60
      Events:
        S3Upload:
          Type: S3
          Properties:
            Bucket: !Ref UploadsBucket
            Events: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: prefix
                    Value: uploads/
      Policies:
        - S3CrudPolicy:
            BucketName: !Ref UploadsBucket

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH

  UploadsBucket:
    Type: AWS::S3::Bucket
```

```bash
# Deploy with SAM
sam build
sam deploy --guided                       # First time
sam deploy                                # Subsequent
sam local start-api                       # Local development
sam logs --tail --name ApiFunction         # Stream logs
```

## Installation

```bash
# SAM CLI
brew install aws-sam-cli
# Or: pip install aws-sam-cli

# AWS CLI
brew install awscli
aws configure                             # Set credentials
```

## Best Practices

1. **Cold start optimization** — Minimize dependencies, use provisioned concurrency for latency-sensitive APIs, prefer arm64 (Graviton2)
2. **Environment variables** — Store config in env vars; use SSM Parameter Store or Secrets Manager for secrets
3. **Layers for shared code** — Package common dependencies (SDKs, utilities) as Lambda Layers; reduce deployment size
4. **Dead letter queues** — Configure DLQ on async invocations (SQS, SNS triggers); don't lose failed events
5. **Structured logging** — Use JSON logging with request ID; CloudWatch Insights can query structured logs
6. **Function URLs** — Use Lambda Function URLs for simple HTTP endpoints without API Gateway ($0 per invocation)
7. **Power tuning** — Use AWS Lambda Power Tuning to find optimal memory/cost ratio; more memory = faster CPU
8. **Container images** — Use container images for functions >250MB or with native dependencies; up to 10GB
