---
name: aws-sdk-java-v2-lambda
description: AWS Lambda patterns using AWS SDK for Java 2.x. Use when invoking Lambda functions, creating/updating functions, managing function configurations, working with Lambda layers, or integrating Lambda with Spring Boot applications.
category: aws
tags: [aws, lambda, java, sdk, serverless, functions]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# AWS SDK for Java 2.x - AWS Lambda

## When to Use

Use this skill when:
- Invoking Lambda functions programmatically
- Creating or updating Lambda functions
- Managing Lambda function configurations
- Working with Lambda environment variables
- Managing Lambda layers and aliases
- Implementing asynchronous Lambda invocations
- Integrating Lambda with Spring Boot

## Overview

AWS Lambda is a compute service that runs code without the need to manage servers. Your code runs automatically, scaling up and down with pay-per-use pricing. Use this skill to implement AWS Lambda operations using AWS SDK for Java 2.x in applications and services.

## Dependencies

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>lambda</artifactId>
</dependency>
```

## Client Setup

To use AWS Lambda, create a LambdaClient with the required region configuration:

```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.lambda.LambdaClient;

LambdaClient lambdaClient = LambdaClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

For asynchronous operations, use LambdaAsyncClient:

```java
import software.amazon.awssdk.services.lambda.LambdaAsyncClient;

LambdaAsyncClient asyncLambdaClient = LambdaAsyncClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

## Invoke Lambda Function

### Synchronous Invocation

Invoke Lambda functions synchronously to get immediate results:

```java
import software.amazon.awssdk.services.lambda.model.*;
import software.amazon.awssdk.core.SdkBytes;

public String invokeLambda(LambdaClient lambdaClient,
                           String functionName,
                           String payload) {
    InvokeRequest request = InvokeRequest.builder()
        .functionName(functionName)
        .payload(SdkBytes.fromUtf8String(payload))
        .build();

    InvokeResponse response = lambdaClient.invoke(request);

    return response.payload().asUtf8String();
}
```

### Asynchronous Invocation

Use asynchronous invocation for fire-and-forget scenarios:

```java
public void invokeLambdaAsync(LambdaClient lambdaClient,
                              String functionName,
                              String payload) {
    InvokeRequest request = InvokeRequest.builder()
        .functionName(functionName)
        .invocationType(InvocationType.EVENT) // Asynchronous
        .payload(SdkBytes.fromUtf8String(payload))
        .build();

    InvokeResponse response = lambdaClient.invoke(request);

    System.out.println("Status: " + response.statusCode());
}
```

### Invoke with JSON Objects

Work with JSON payloads for complex data structures:

```java
import com.fasterxml.jackson.databind.ObjectMapper;

public <T> String invokeLambdaWithObject(LambdaClient lambdaClient,
                                         String functionName,
                                         T requestObject) throws Exception {
    ObjectMapper mapper = new ObjectMapper();
    String jsonPayload = mapper.writeValueAsString(requestObject);

    InvokeRequest request = InvokeRequest.builder()
        .functionName(functionName)
        .payload(SdkBytes.fromUtf8String(jsonPayload))
        .build();

    InvokeResponse response = lambdaClient.invoke(request);

    return response.payload().asUtf8String();
}
```

### Parse Typed Responses

Parse JSON responses into typed objects:

```java
public <T> T invokeLambdaAndParse(LambdaClient lambdaClient,
                                  String functionName,
                                  Object request,
                                  Class<T> responseType) throws Exception {
    ObjectMapper mapper = new ObjectMapper();
    String jsonPayload = mapper.writeValueAsString(request);

    InvokeRequest invokeRequest = InvokeRequest.builder()
        .functionName(functionName)
        .payload(SdkBytes.fromUtf8String(jsonPayload))
        .build();

    InvokeResponse response = lambdaClient.invoke(invokeRequest);

    String responseJson = response.payload().asUtf8String();

    return mapper.readValue(responseJson, responseType);
}
```

## Function Management

### List Functions

List all Lambda functions for the current account:

```java
public List<FunctionConfiguration> listFunctions(LambdaClient lambdaClient) {
    ListFunctionsResponse response = lambdaClient.listFunctions();

    return response.functions();
}
```

### Get Function Configuration

Retrieve function configuration and metadata:

```java
public FunctionConfiguration getFunctionConfig(LambdaClient lambdaClient,
                                                String functionName) {
    GetFunctionRequest request = GetFunctionRequest.builder()
        .functionName(functionName)
        .build();

    GetFunctionResponse response = lambdaClient.getFunction(request);

    return response.configuration();
}
```

### Update Function Code

Update Lambda function code with new deployment package:

```java
import java.nio.file.Files;
import java.nio.file.Paths;

public void updateFunctionCode(LambdaClient lambdaClient,
                               String functionName,
                               String zipFilePath) throws IOException {
    byte[] zipBytes = Files.readAllBytes(Paths.get(zipFilePath));

    UpdateFunctionCodeRequest request = UpdateFunctionCodeRequest.builder()
        .functionName(functionName)
        .zipFile(SdkBytes.fromByteArray(zipBytes))
        .publish(true)
        .build();

    UpdateFunctionCodeResponse response = lambdaClient.updateFunctionCode(request);

    System.out.println("Updated function version: " + response.version());
}
```

### Update Function Configuration

Modify function settings like timeout, memory, and environment variables:

```java
public void updateFunctionConfiguration(LambdaClient lambdaClient,
                                        String functionName,
                                        Map<String, String> environment) {
    Environment env = Environment.builder()
        .variables(environment)
        .build();

    UpdateFunctionConfigurationRequest request = UpdateFunctionConfigurationRequest.builder()
        .functionName(functionName)
        .environment(env)
        .timeout(60)
        .memorySize(512)
        .build();

    lambdaClient.updateFunctionConfiguration(request);
}
```

### Create Function

Create new Lambda functions with code and configuration:

```java
public void createFunction(LambdaClient lambdaClient,
                          String functionName,
                          String roleArn,
                          String handler,
                          String zipFilePath) throws IOException {
    byte[] zipBytes = Files.readAllBytes(Paths.get(zipFilePath));

    FunctionCode code = FunctionCode.builder()
        .zipFile(SdkBytes.fromByteArray(zipBytes))
        .build();

    CreateFunctionRequest request = CreateFunctionRequest.builder()
        .functionName(functionName)
        .runtime(Runtime.JAVA17)
        .role(roleArn)
        .handler(handler)
        .code(code)
        .timeout(60)
        .memorySize(512)
        .build();

    CreateFunctionResponse response = lambdaClient.createFunction(request);

    System.out.println("Function ARN: " + response.functionArn());
}
```

### Delete Function

Remove Lambda functions when no longer needed:

```java
public void deleteFunction(LambdaClient lambdaClient, String functionName) {
    DeleteFunctionRequest request = DeleteFunctionRequest.builder()
        .functionName(functionName)
        .build();

    lambdaClient.deleteFunction(request);
}
```

## Spring Boot Integration

### Configuration

Configure Lambda clients as Spring beans:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class LambdaConfiguration {

    @Bean
    public LambdaClient lambdaClient() {
        return LambdaClient.builder()
            .region(Region.US_EAST_1)
            .build();
    }
}
```

### Lambda Invoker Service

Create a service for Lambda function invocation:

```java
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class LambdaInvokerService {

    private final LambdaClient lambdaClient;
    private final ObjectMapper objectMapper;

    @Autowired
    public LambdaInvokerService(LambdaClient lambdaClient, ObjectMapper objectMapper) {
        this.lambdaClient = lambdaClient;
        this.objectMapper = objectMapper;
    }

    public <T, R> R invoke(String functionName, T request, Class<R> responseType) {
        try {
            String jsonPayload = objectMapper.writeValueAsString(request);

            InvokeRequest invokeRequest = InvokeRequest.builder()
                .functionName(functionName)
                .payload(SdkBytes.fromUtf8String(jsonPayload))
                .build();

            InvokeResponse response = lambdaClient.invoke(invokeRequest);

            if (response.functionError() != null) {
                throw new LambdaInvocationException(
                    "Lambda function error: " + response.functionError());
            }

            String responseJson = response.payload().asUtf8String();

            return objectMapper.readValue(responseJson, responseType);

        } catch (Exception e) {
            throw new RuntimeException("Failed to invoke Lambda function", e);
        }
    }

    public void invokeAsync(String functionName, Object request) {
        try {
            String jsonPayload = objectMapper.writeValueAsString(request);

            InvokeRequest invokeRequest = InvokeRequest.builder()
                .functionName(functionName)
                .invocationType(InvocationType.EVENT)
                .payload(SdkBytes.fromUtf8String(jsonPayload))
                .build();

            lambdaClient.invoke(invokeRequest);

        } catch (Exception e) {
            throw new RuntimeException("Failed to invoke Lambda function async", e);
        }
    }
}
```

### Typed Lambda Client

Create type-safe interfaces for Lambda services:

```java
public interface OrderProcessor {
    OrderResponse processOrder(OrderRequest request);
}

@Service
public class LambdaOrderProcessor implements OrderProcessor {

    private final LambdaInvokerService lambdaInvoker;

    @Value("${lambda.order-processor.function-name}")
    private String functionName;

    public LambdaOrderProcessor(LambdaInvokerService lambdaInvoker) {
        this.lambdaInvoker = lambdaInvoker;
    }

    @Override
    public OrderResponse processOrder(OrderRequest request) {
        return lambdaInvoker.invoke(functionName, request, OrderResponse.class);
    }
}
```

## Error Handling

Implement comprehensive error handling for Lambda operations:

```java
public String invokeLambdaSafe(LambdaClient lambdaClient,
                               String functionName,
                               String payload) {
    try {
        InvokeRequest request = InvokeRequest.builder()
            .functionName(functionName)
            .payload(SdkBytes.fromUtf8String(payload))
            .build();

        InvokeResponse response = lambdaClient.invoke(request);

        // Check for function error
        if (response.functionError() != null) {
            String errorMessage = response.payload().asUtf8String();
            throw new RuntimeException("Lambda error: " + errorMessage);
        }

        // Check status code
        if (response.statusCode() != 200) {
            throw new RuntimeException("Lambda invocation failed with status: " +
                response.statusCode());
        }

        return response.payload().asUtf8String();

    } catch (LambdaException e) {
        System.err.println("Lambda error: " + e.awsErrorDetails().errorMessage());
        throw e;
    }
}

public class LambdaInvocationException extends RuntimeException {
    public LambdaInvocationException(String message) {
        super(message);
    }

    public LambdaInvocationException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

## Examples

For comprehensive code examples, see the references section:

- **Basic examples** - Simple invocation patterns and function management
- **Spring Boot integration** - Complete Spring Boot configuration and service patterns
- **Testing examples** - Unit and integration test patterns
- **Advanced patterns** - Complex scenarios and best practices

## Best Practices

1. **Reuse Lambda clients**: Create once and reuse across invocations
2. **Set appropriate timeouts**: Match client timeout to Lambda function timeout
3. **Use async invocation**: For fire-and-forget scenarios
4. **Handle errors properly**: Check for function errors and status codes
5. **Use environment variables**: For function configuration
6. **Implement retry logic**: For transient failures
7. **Monitor invocations**: Use CloudWatch metrics
8. **Version functions**: Use aliases and versions for production
9. **Use VPC**: For accessing resources in private subnets
10. **Optimize payload size**: Keep payloads small for better performance

## Testing

Test Lambda services using mocks and test assertions:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LambdaInvokerServiceTest {

    @Mock
    private LambdaClient lambdaClient;

    @Mock
    private ObjectMapper objectMapper;

    @InjectMocks
    private LambdaInvokerService service;

    @Test
    void shouldInvokeLambdaSuccessfully() throws Exception {
        // Test implementation
    }
}
```

## Related Skills

- @aws-sdk-java-v2-core - Core AWS SDK patterns and client configuration
- @spring-boot-dependency-injection - Spring dependency injection best practices
- @unit-test-service-layer - Service testing patterns with Mockito
- @spring-boot-actuator - Production monitoring and health checks

## References

For detailed information and examples, see the following reference files:

- **[Official Documentation](references/official-documentation.md)** - AWS Lambda concepts, API reference, and official guidance
- **[Examples](references/examples.md)** - Complete code examples and integration patterns

## Additional Resources

- [Lambda Examples on GitHub](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/lambda)
- [Lambda API Reference](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/lambda/package-summary.html)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)