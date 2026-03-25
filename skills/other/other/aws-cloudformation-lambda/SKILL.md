---
name: aws-cloudformation-lambda
description: Provides AWS CloudFormation patterns for Lambda functions, layers, API Gateway integration, event sources, cold start optimization, monitoring, logging, template validation, and deployment workflows. Use when creating Lambda functions with CloudFormation, configuring event sources, implementing cold start optimization, managing layers, integrating with API Gateway, and deploying Lambda infrastructure.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Lambda Functions

## Overview

Create production-ready Lambda functions using CloudFormation templates with validation and deployment workflows.

## When to Use

- Creating Lambda functions with CloudFormation
- Configuring event sources (S3, SQS, DynamoDB, Kinesis)
- Implementing Lambda layers and cold start optimization
- Integrating Lambda with API Gateway
- Deploying Lambda infrastructure with validation

## Deployment Workflow

Always follow this deployment workflow:

### 1. Validate Template
```bash
aws cloudformation validate-template --template-body file://template.yaml
```

### 2. Deploy Stack
```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-lambda-stack \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Environment=prod
```

### 3. Monitor Stack Events
```bash
aws cloudformation describe-stack-events \
  --stack-name my-lambda-stack \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`||ResourceStatus==`UPDATE_FAILED`]'
```

### 4. Verify Resources
```bash
aws lambda get-function --function-name my-lambda-stack-function
aws cloudformation describe-stacks --stack-name my-lambda-stack \
  --query 'Stacks[0].StackStatus'
```

### 5. Rollback on Failure
```bash
aws cloudformation delete-stack --stack-name my-lambda-stack
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/my-lambda"
```

## Instructions

Follow these steps to create Lambda functions with CloudFormation:

### 1. Define Lambda Function Parameters

Specify runtime, memory, timeout, and environment variables:

```yaml
Parameters:
  FunctionMemory:
    Type: Number
    Default: 256
    AllowedValues:
      - 128
      - 256
      - 512
      - 1024
      - 2048
    Description: Lambda function memory in MB

  FunctionTimeout:
    Type: Number
    Default: 30
    MinValue: 1
    MaxValue: 900
    Description: Function timeout in seconds

  Runtime:
    Type: String
    Default: nodejs20.x
    AllowedValues:
      - nodejs20.x
      - python3.11
      - java21
      - dotnet8
      - go1.x
    Description: Lambda runtime environment
```

### 2. Create Lambda Function

Define the basic function configuration:

```yaml
Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: !Ref Runtime
      Handler: index.handler
      Role: !Ref ExecutionRole
      MemorySize: !Ref FunctionMemory
      Timeout: !Ref FunctionTimeout
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: !Ref CodeKey
      Environment:
        Variables:
          LOG_LEVEL: INFO
          DATABASE_URL: !Ref DatabaseUrl
      Tags:
        - Key: Environment
          Value: !Ref Environment
```

### 3. Configure Execution Role

Apply least privilege IAM policies:

```yaml
Resources:
  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: S3ReadAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub "${DataBucket.Arn}/*"
```

### 4. Add Event Sources

Configure triggers for Lambda invocation:

```yaml
Resources:
  # S3 event source
  S3EventSource:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt DataBucket.Arn
      FunctionName: !Ref LambdaFunction

  # SQS event source
  SQSEventSource:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt Queue.Arn
      FunctionName: !Ref LambdaFunction
      BatchSize: 10
      MaximumBatchingWindowInSeconds: 5
```

### 5. Configure API Gateway Integration

Set up REST or HTTP API integration:

```yaml
Resources:
  # HTTP API integration
  HttpApi:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      Name: !Sub "${AWS::StackName}-api"
      ProtocolType: HTTP
      Target: !Ref LambdaFunction

  ApiIntegration:
    Type: AWS::ApiGatewayV2::Integration
    Properties:
      ApiId: !Ref HttpApi
      IntegrationType: AWS_PROXY
      IntegrationUri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations"
```

### 6. Implement Versioning and Aliases

Create function versions and aliases:

```yaml
Resources:
  LambdaVersion:
    Type: AWS::Lambda::Version
    Properties:
      FunctionName: !Ref LambdaFunction
      Description: !Sub "Version ${AWS::StackName} v1"

  LambdaAlias:
    Type: AWS::Lambda::Alias
    Properties:
      FunctionName: !Ref LambdaFunction
      FunctionVersion: !GetAtt LambdaVersion.Version
      Name: live
```

### 7. Configure Monitoring

Enable CloudWatch logging and X-Ray tracing:

```yaml
Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      LoggingConfig:
        LogGroup: !Ref LogGroup
      TracingConfig:
        Mode: Active

  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/lambda/${LambdaFunction}"
      RetentionInDays: 7
```

### 8. Set Up Dead Letter Queue

Configure DLQ for failed invocations:

```yaml
Resources:
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "${AWS::StackName}-dlq"

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      DeadLetterConfig:
        TargetArn: !GetAtt DeadLetterQueue.Arn
```

## Examples

### Complete Lambda Stack Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda function with monitoring and DLQ

Parameters:
  FunctionMemory:
    Type: Number
    Default: 256
    AllowedValues: [128, 256, 512, 1024]
  FunctionTimeout:
    Type: Number
    Default: 30

Resources:
  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: { Service: lambda.amazonaws.com }
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: nodejs20.x
      Handler: index.handler
      Role: !GetAtt ExecutionRole.Arn
      MemorySize: !Ref FunctionMemory
      Timeout: !Ref FunctionTimeout
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: !Ref CodeKey
      Environment:
        Variables:
          LOG_LEVEL: INFO

  LambdaVersion:
    Type: AWS::Lambda::Version
    Properties:
      FunctionName: !Ref LambdaFunction

  LambdaAlias:
    Type: AWS::Lambda::Alias
    Properties:
      FunctionName: !Ref LambdaFunction
      FunctionVersion: !GetAtt LambdaVersion.Version
      Name: live

Outputs:
  FunctionArn:
    Value: !GetAtt LambdaFunction.Arn
  FunctionName:
    Value: !Ref LambdaFunction
```

## Best Practices

### Performance Optimization

- Use SnapStart for Java functions to eliminate cold starts
- Use provisioned concurrency for critical functions requiring low latency
- Keep deployment packages small (< 50 MB zipped)
- Optimize memory size based on function requirements
- Use appropriate timeout values (avoid maximum timeout)
- Configure reserved concurrency to prevent throttling

### Cost Optimization

- Right-size memory allocation for cost efficiency
- Use provisioned concurrency strategically (adds cost when idle)
- Monitor Lambda duration and optimize for faster execution
- Use ephemeral storage (/tmp) efficiently
- Clean up unused Lambda functions and versions
- Consider Lambda PowerTuning for optimal memory/power configuration

### Security

- Apply least privilege IAM policies to execution roles
- Encrypt environment variables at rest
- Use VPC endpoints for private AWS service access
- Rotate IAM credentials regularly
- Implement VPC configuration for private function access
- Use AWS KMS for encrypting sensitive data

### Reliability

- Configure Dead Letter Queue for async invocations
- Implement retry logic with exponential backoff
- Use CloudWatch alarms for error monitoring
- Test Lambda functions thoroughly before deployment
- Implement circuit breakers for downstream service failures
- Use canary deployments with Lambda aliases

### Monitoring and Observability

- Enable CloudWatch Logs for all functions
- Use X-Ray tracing for distributed tracing
- Configure CloudWatch metrics for performance monitoring
- Set up alarms for errors, throttles, and duration
- Use Lambda Insights for debugging
- Monitor concurrent executions and throttling

### Versioning and Deployment

- Use Lambda aliases for production environments (live, staging)
- Implement canary deployments with weighted aliases
- Create function versions for immutable deployments
- Use SAM or AWS CDK for simplified Lambda deployments
- Implement blue/green deployments with Lambda aliases
- Test function changes in development environment first

## Constraints and Warnings

- **Timeout limits**: Lambda timeout max is 900 seconds (15 min); set appropriate values to avoid orphaned executions
- **Deployment package size**: Zipped packages max 50 MB, unzipped max 250 MB (including layers)
- **Layer limits**: Max 5 layers per function; each layer max 50 MB (unzipped)
- **Environment variables**: Max 4 KB for all variables; encrypt sensitive values with KMS
- **Cold starts**: Java and .NET functions have longer cold starts; use SnapStart or Provisioned Concurrency for latency-sensitive workloads
- **Concurrent execution**: Default limit 1000 per region; request increase for high-traffic functions
- **VPC networking**: Lambda in VPC adds 10-30 second cold start overhead for first invocation
- **IAM permissions**: Never use `*` in Resource policies; always scope to specific resources
- **Dead Letter Queue**: Required for async invocations; ensure DLQ is in same region as function
- **Cost monitoring**: Enable billing alerts; Lambda charges per invocation and duration

## References

For detailed implementation guidance, see:

- **[constraints.md](references/constraints.md)** - Resource limits (function limits, concurrent execution, timeout, memory), deployment constraints (function size, layer size, environment variables), operational constraints (cold starts, VPC networking, event sources, DLQ), security constraints (execution role, resource policies, VPC endpoints), cost considerations (provisioned concurrency, duration, memory, data transfer), and performance constraints (SnapStart, layer versioning, X-Ray tracing, async invocation)

## Related Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS CloudFormation Lambda Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lambda.html)
- [Lambda Performance Optimization](https://docs.aws.amazon.com/lambda/latest/dg/configuration-functions.html)
- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/lambda-dg.pdf)
- [Lambda Layers Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [Lambda Event Sources Documentation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-events.html)
- [Lambda SnapStart Documentation](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)
