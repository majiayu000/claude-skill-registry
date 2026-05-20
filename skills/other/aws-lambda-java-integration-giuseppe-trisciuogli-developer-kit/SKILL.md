---
name: aws-lambda-java-integration
description: Provides AWS Lambda integration patterns for Java with cold start optimization. Use when deploying Java functions to AWS Lambda, choosing between Micronaut and Raw Java approaches, optimizing cold starts below 1 second, configuring API Gateway or ALB integration, or implementing serverless Java applications. Triggers include "create lambda java", "deploy java lambda", "micronaut lambda aws", "java lambda cold start", "aws lambda java performance", "java serverless framework".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS Lambda Java Integration

Patterns for creating high-performance AWS Lambda functions in Java with optimized cold starts.

## Overview

This skill provides complete patterns for AWS Lambda Java development, covering two main approaches:

1. **Micronaut Framework** - Full-featured framework with AOT compilation, dependency injection, and cold start < 1s
2. **Raw Java** - Minimal overhead approach with cold start < 500ms

Both approaches support API Gateway and ALB integration with production-ready configurations.

## When to Use

Use this skill when:
- Creating new Lambda functions in Java
- Migrating existing Java applications to Lambda
- Optimizing cold start performance for Java Lambda
- Choosing between framework-based and minimal Java approaches
- Configuring API Gateway or ALB integration
- Setting up deployment pipelines for Java Lambda

## Instructions

### 1. Choose Your Approach

| Approach | Cold Start | Best For | Complexity |
|----------|------------|----------|------------|
| Micronaut | < 1s | Complex apps, DI needed, enterprise | Medium |
| Raw Java | < 500ms | Simple handlers, minimal overhead | Low |

### 2. Project Structure

```
my-lambda-function/
├── build.gradle (or pom.xml)
├── src/
│   └── main/
│       ├── java/
│       │   └── com/example/
│       │       └── Handler.java
│       └── resources/
│           └── application.yml (Micronaut only)
└── serverless.yml (or template.yaml)
```

### 3. Implementation Examples

#### Micronaut Handler

```java
@FunctionBean("my-function")
public class MyFunction implements Function<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {

    private final MyService service;

    public MyFunction(MyService service) {
        this.service = service;
    }

    @Override
    public APIGatewayProxyResponseEvent apply(APIGatewayProxyRequestEvent request) {
        // Process request
        return new APIGatewayProxyResponseEvent()
            .withStatusCode(200)
            .withBody("{\"message\": \"Success\"}");
    }
}
```

#### Raw Java Handler

```java
public class MyHandler implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {

    // Singleton pattern for warm invocations
    private static final MyService service = new MyService();

    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent request, Context context) {
        return new APIGatewayProxyResponseEvent()
            .withStatusCode(200)
            .withBody("{\"message\": \"Success\"}");
    }
}
```

## Core Concepts

### Cold Start Optimization

Cold start time depends on initialization code. Key strategies:

1. **Lazy Initialization** - Defer heavy setup from constructor
2. **Singleton Pattern** - Cache initialized services as static fields
3. **Minimal Dependencies** - Reduce JAR size by excluding unused libraries
4. **AOT Compilation** - Micronaut's ahead-of-time compilation eliminates reflection

### Connection Management

```java
// GOOD: Initialize once, reuse across invocations
private static final DynamoDbClient dynamoDb = DynamoDbClient.builder()
    .region(Region.US_EAST_1)
    .build();

// AVOID: Creating clients in handler method
public APIGatewayProxyResponseEvent handleRequest(...) {
    DynamoDbClient client = DynamoDbClient.create(); // Slow on every invocation
}
```

### Error Handling

```java
@Override
public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent request, Context context) {
    try {
        // Business logic
        return successResponse(result);
    } catch (ValidationException e) {
        return errorResponse(400, e.getMessage());
    } catch (Exception e) {
        context.getLogger().log("Error: " + e.getMessage());
        return errorResponse(500, "Internal error");
    }
}
```

## Best Practices

### Memory and Timeout Configuration

- **Memory**: Start with 512MB, adjust based on profiling
- **Timeout**: Set based on cold start + expected processing time
  - Micronaut: 10-30 seconds for cold start buffer
  - Raw Java: 5-10 seconds typically sufficient

### Packaging

- Use Gradle Shadow Plugin or Maven Shade Plugin
- Exclude unnecessary dependencies
- Target Java 17 or 21 for best performance

### Monitoring

- Enable X-Ray tracing for performance analysis
- Log initialization time separately from processing time
- Use CloudWatch Insights to track cold vs warm starts

## Deployment Options

### Serverless Framework

```yaml
service: my-java-lambda

provider:
  name: aws
  runtime: java21
  memorySize: 512
  timeout: 10

package:
  artifact: build/libs/function.jar

functions:
  api:
    handler: com.example.Handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

### AWS SAM

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: build/libs/function.jar
      Handler: com.example.Handler
      Runtime: java21
      MemorySize: 512
      Timeout: 10
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

## Constraints and Warnings

### Lambda Limits

- **Deployment package**: 250MB unzipped maximum
- **Memory**: 128MB to 10GB
- **Timeout**: 15 minutes maximum
- **Concurrent executions**: 1000 default (adjustable)

### Java-Specific Considerations

- **Reflection**: Minimize use; prefer AOT compilation (Micronaut)
- **Classpath scanning**: Slows cold start; use explicit configuration
- **Large frameworks**: Spring Boot adds significant cold start overhead

### Common Pitfalls

1. **Initialization in handler** - Causes repeated work on warm invocations
2. **Oversized JARs** - Include only required dependencies
3. **Insufficient memory** - Java needs more memory than Node.js/Python
4. **No timeout handling** - Always set appropriate timeouts

## References

For detailed guidance on specific topics:

- **[Micronaut Lambda](references/micronaut-lambda.md)** - Complete Micronaut setup, AOT configuration, DI optimization
- **[Raw Java Lambda](references/raw-java-lambda.md)** - Minimal handler patterns, singleton caching, JAR packaging
- **[Serverless Deployment](references/serverless-deployment.md)** - Serverless Framework, SAM, CI/CD pipelines, provisioned concurrency
- **[Testing Lambda](references/testing-lambda.md)** - JUnit 5, SAM Local, integration testing, performance measurement

## Examples

### Example 1: Create a Micronaut Lambda Function

**Input:**
```
Create a Java Lambda function using Micronaut to handle user REST API
```

**Process:**
1. Configure Gradle project with Micronaut plugin
2. Create Handler class extending MicronautRequestHandler
3. Implement methods for GET/POST/PUT/DELETE
4. Configure application.yml with AOT optimizations
5. Set up packaging with Shadow plugin

**Output:**
- Complete project structure
- Handler with dependency injection
- serverless.yml deployment configuration

### Example 2: Optimize Cold Start for Raw Java

**Input:**
```
My Java Lambda has 3 second cold start, how do I optimize it?
```

**Process:**
1. Analyze initialization code
2. Move AWS client creation to static fields
3. Reduce dependencies in build.gradle
4. Configure optimized JVM options
5. Consider provisioned concurrency

**Output:**
- Refactored code with singleton pattern
- Minimized JAR
- Cold start < 500ms

### Example 3: Deploy with GitHub Actions

**Input:**
```
Configure CI/CD for Java Lambda with SAM
```

**Process:**
1. Create GitHub Actions workflow
2. Configure Gradle build with Shadow
3. Set up SAM build and deploy
4. Add test stage before deployment
5. Configure environment protection for prod

**Output:**
- Complete .github/workflows/deploy.yml
- Multi-stage pipeline (dev/staging/prod)
- Integrated test automation

## Version

Version: 1.0.0
