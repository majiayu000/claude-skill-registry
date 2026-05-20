---
name: aws-lambda-python-integration
description: Provides AWS Lambda integration patterns for Python with cold start optimization. Use when deploying Python functions to AWS Lambda, choosing between AWS Chalice and raw Python approaches, optimizing cold starts, configuring API Gateway or ALB integration, or implementing serverless Python applications. Triggers include "create lambda python", "deploy python lambda", "chalice lambda aws", "python lambda cold start", "aws lambda python performance", "python serverless framework".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS Lambda Python Integration

Patterns for creating high-performance AWS Lambda functions in Python with optimized cold starts and clean architecture.

## Overview

This skill provides complete patterns for AWS Lambda Python development, covering two main approaches:

1. **AWS Chalice Framework** - Full-featured framework with built-in routing, dependency injection, and local testing server
2. **Raw Python** - Minimal overhead approach with maximum flexibility and control

Both approaches support API Gateway and ALB integration with production-ready configurations.

## When to Use

Use this skill when:
- Creating new Lambda functions in Python
- Migrating existing Python applications to Lambda
- Optimizing cold start performance for Python Lambda
- Choosing between framework-based and minimal Python approaches
- Configuring API Gateway or ALB integration
- Setting up deployment pipelines for Python Lambda

## Instructions

### 1. Choose Your Approach

| Approach | Cold Start | Best For | Complexity |
|----------|------------|----------|------------|
| AWS Chalice | < 200ms | REST APIs, rapid development, built-in routing | Low |
| Raw Python | < 100ms | Simple handlers, maximum control, minimal dependencies | Low |

### 2. Project Structure

#### AWS Chalice Structure
```
my-chalice-app/
├── app.py                    # Main application with routes
├── requirements.txt          # Dependencies
├── .chalice/
│   ├── config.json          # Chalice configuration
│   └── deploy/              # Deployment artifacts
├── chalicelib/              # Additional modules
│   ├── __init__.py
│   └── services.py
└── tests/
    └── test_app.py
```

#### Raw Python Structure
```
my-lambda-function/
├── lambda_function.py       # Handler entry point
├── requirements.txt         # Dependencies
├── template.yaml            # SAM/CloudFormation template
└── src/                     # Additional modules
    ├── __init__.py
    ├── handlers.py
    └── utils.py
```

### 3. Implementation Examples

See the [References](#references) section for detailed implementation guides. Quick examples:

**AWS Chalice:**
```python
from chalice import Chalice
app = Chalice(app_name='my-api')

@app.route('/')
def index():
    return {'message': 'Hello from Chalice!'}
```

**Raw Python:**
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello from Lambda!'})
    }
```

## Core Concepts

### Cold Start Optimization

Python has excellent cold start performance. Key strategies:

1. **Initialize at module level** - Persists across warm invocations
2. **Use lazy loading** - Defer heavy imports until needed
3. **Cache boto3 clients** - Reuse connections between invocations

See [Raw Python Lambda](references/raw-python-lambda.md#cold-start-optimization) for detailed patterns.

### Connection Management

Create clients at module level and reuse:

```python
_dynamodb = None

def get_table():
    global _dynamodb
    if _dynamodb is None:
        _dynamodb = boto3.resource('dynamodb').Table('my-table')
    return _dynamodb
```

### Environment Configuration

```python
class Config:
    TABLE_NAME = os.environ.get('TABLE_NAME')
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

    @classmethod
    def validate(cls):
        if not cls.TABLE_NAME:
            raise ValueError("TABLE_NAME required")
```

## Best Practices

### Memory and Timeout Configuration

- **Memory**: Start with 256MB for simple handlers, 512MB for complex operations
- **Timeout**: Set based on expected processing time
  - Simple handlers: 3-5 seconds
  - API with DB calls: 10-15 seconds
  - Data processing: 30-60 seconds

### Dependencies

Keep `requirements.txt` minimal:

```txt
# Core AWS SDK - always needed
boto3>=1.35.0

# Only add what you need
requests>=2.32.0  # If calling external APIs
pydantic>=2.5.0   # If using data validation
```

### Error Handling

Return proper HTTP codes with request ID:

```python
def lambda_handler(event, context):
    try:
        result = process_event(event)
        return {'statusCode': 200, 'body': json.dumps(result)}
    except ValueError as e:
        return {'statusCode': 400, 'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f"Error: {str(e)}")  # Log to CloudWatch
        return {'statusCode': 500, 'body': json.dumps({'error': 'Internal error'})}
```

See [Raw Python Lambda](references/raw-python-lambda.md#error-handling) for structured error patterns.

### Logging

Use structured logging for CloudWatch Insights:

```python
import logging, json
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Structured log
logger.info(json.dumps({
    'eventType': 'REQUEST',
    'requestId': context.aws_request_id,
    'path': event.get('path')
}))
```

See [Raw Python Lambda](references/raw-python-lambda.md#logging) for advanced patterns.

## Deployment Options

### Quick Start

**Serverless Framework:**
```yaml
# serverless.yml
service: my-python-api
provider:
  name: aws
  runtime: python3.12  # or python3.11
functions:
  api:
    handler: lambda_function.lambda_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

**AWS SAM:**
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./
      Handler: lambda_function.lambda_handler
      Runtime: python3.12  # or python3.11
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

**AWS Chalice:**
```bash
chalice new-project my-api
cd my-api
chalice deploy --stage dev
```

For complete deployment configurations including CI/CD, environment-specific settings, and advanced SAM/Serverless patterns, see [Serverless Deployment](references/serverless-deployment.md).

## Constraints and Warnings

### Lambda Limits

- **Deployment package**: 250MB unzipped maximum (50MB zipped)
- **Memory**: 128MB to 10GB
- **Timeout**: 15 minutes maximum
- **Concurrent executions**: 1000 default (adjustable)
- **Environment variables**: 4KB total size

### Python-Specific Considerations

- **Cold start**: Python has excellent cold start performance, but avoid heavy imports at module level
- **Dependencies**: Keep `requirements.txt` minimal; use Lambda Layers for shared dependencies
- **Native dependencies**: Must be compiled for Amazon Linux 2 (x86_64 or arm64)

### Common Pitfalls

1. **Importing heavy libraries at module level** - Defer to function level if not always needed
2. **Not handling Lambda context** - Use `context.get_remaining_time_in_millis()` for timeout awareness
3. **Not validating input** - Always validate and sanitize event data
4. **Printing sensitive data** - Be careful with logs and CloudWatch

### Security Considerations

- Never hardcode credentials; use IAM roles and environment variables
- Validate all input data
- Use least privilege IAM policies
- Enable CloudTrail for audit logging

## References

For detailed guidance on specific topics:

- **[AWS Chalice](references/chalice-lambda.md)** - Complete Chalice setup, routing, middleware, deployment
- **[Raw Python Lambda](references/raw-python-lambda.md)** - Minimal handler patterns, module caching, packaging
- **[Serverless Deployment](references/serverless-deployment.md)** - Serverless Framework, SAM, CI/CD pipelines
- **[Testing Lambda](references/testing-lambda.md)** - pytest, moto, SAM Local, localstack

## Examples

### Example 1: Create an AWS Chalice REST API

**Input:**
```
Create a Python Lambda REST API using AWS Chalice for a todo application
```

**Process:**
1. Initialize Chalice project with `chalice new-project`
2. Configure routes for CRUD operations
3. Set up DynamoDB integration
4. Configure deployment stages
5. Deploy with `chalice deploy`

**Output:**
- Complete Chalice project structure
- REST API with CRUD endpoints
- DynamoDB table configuration
- Deployment configuration

### Example 2: Optimize Cold Start for Raw Python

**Input:**
```
My Python Lambda has slow cold start, how do I optimize it?
```

**Process:**
1. Analyze imports and initialization code
2. Move heavy imports inside functions (lazy loading)
3. Cache boto3 clients at module level
4. Remove unnecessary dependencies
5. Use provisioned concurrency if needed

**Output:**
- Refactored code with lazy loading
- Optimized cold start < 100ms
- Dependency analysis

### Example 3: Deploy with GitHub Actions

**Input:**
```
Configure CI/CD for Python Lambda with SAM
```

**Process:**
1. Create GitHub Actions workflow
2. Set up Python environment and dependencies
3. Run pytest with coverage
4. Package with SAM
5. Deploy to dev/prod stages

**Output:**
- Complete `.github/workflows/deploy.yml`
- Multi-stage pipeline
- Integrated test automation

## Version

Version: 1.0.0
