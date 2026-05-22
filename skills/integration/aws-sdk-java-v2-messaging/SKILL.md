---
name: aws-sdk-java-v2-messaging
description: Implement AWS messaging patterns using AWS SDK for Java 2.x for SQS queues and SNS topics. Send/receive messages, manage FIFO queues, implement DLQ, publish messages, manage subscriptions, and build pub/sub patterns.
category: aws
tags: [aws, sqs, sns, java, sdk, messaging, pub-sub, queues, events]
version: 1.1.0
allowed-tools: Read, Write, Bash, Grep
---

# AWS SDK for Java 2.x - Messaging (SQS & SNS)

## Overview

Provide comprehensive AWS messaging patterns using AWS SDK for Java 2.x for both SQS and SNS services. Include client setup, queue management, message operations, subscription management, and Spring Boot integration patterns.

## When to Use

Use this skill when working with:
- Amazon SQS queues for message queuing
- SNS topics for event publishing and notification
- FIFO queues and standard queues
- Dead Letter Queues (DLQ) for message handling
- SNS subscriptions with email, SMS, SQS, Lambda endpoints
- Pub/sub messaging patterns and event-driven architectures
- Spring Boot integration with AWS messaging services
- Testing strategies using LocalStack or Testcontainers

## Quick Start

### Dependencies

```xml
<!-- SQS -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>sqs</artifactId>
</dependency>

<!-- SNS -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>sns</artifactId>
</dependency>
```

### Basic Client Setup

```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sns.SnsClient;

SqsClient sqsClient = SqsClient.builder()
    .region(Region.US_EAST_1)
    .build();

SnsClient snsClient = SnsClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

## Examples

### Basic SQS Operations

#### Create and Send Message
```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.*;

// Setup SQS client
SqsClient sqsClient = SqsClient.builder()
    .region(Region.US_EAST_1)
    .build();

// Create queue
String queueUrl = sqsClient.createQueue(CreateQueueRequest.builder()
    .queueName("my-queue")
    .build()).queueUrl();

// Send message
String messageId = sqsClient.sendMessage(SendMessageRequest.builder()
    .queueUrl(queueUrl)
    .messageBody("Hello, SQS!")
    .build()).messageId();
```

#### Receive and Delete Message
```java
// Receive messages with long polling
ReceiveMessageResponse response = sqsClient.receiveMessage(ReceiveMessageRequest.builder()
    .queueUrl(queueUrl)
    .maxNumberOfMessages(10)
    .waitTimeSeconds(20)
    .build());

// Process and delete messages
response.messages().forEach(message -> {
    System.out.println("Received: " + message.body());
    sqsClient.deleteMessage(DeleteMessageRequest.builder()
        .queueUrl(queueUrl)
        .receiptHandle(message.receiptHandle())
        .build());
});
```

### Basic SNS Operations

#### Create Topic and Publish
```java
import software.amazon.awssdk.services.sns.SnsClient;
import software.amazon.awssdk.services.sns.model.*;

// Setup SNS client
SnsClient snsClient = SnsClient.builder()
    .region(Region.US_EAST_1)
    .build();

// Create topic
String topicArn = snsClient.createTopic(CreateTopicRequest.builder()
    .name("my-topic")
    .build()).topicArn();

// Publish message
String messageId = snsClient.publish(PublishRequest.builder()
    .topicArn(topicArn)
    .subject("Test Notification")
    .message("Hello, SNS!")
    .build()).messageId();
```

### Advanced Examples

#### FIFO Queue Pattern
```java
// Create FIFO queue
Map<QueueAttributeName, String> attributes = Map.of(
    QueueAttributeName.FIFO_QUEUE, "true",
    QueueAttributeName.CONTENT_BASED_DEDUPLICATION, "true"
);

String fifoQueueUrl = sqsClient.createQueue(CreateQueueRequest.builder()
    .queueName("my-queue.fifo")
    .attributes(attributes)
    .build()).queueUrl();

// Send FIFO message with group ID
String fifoMessageId = sqsClient.sendMessage(SendMessageRequest.builder()
    .queueUrl(fifoQueueUrl)
    .messageBody("Order #12345")
    .messageGroupId("orders")
    .messageDeduplicationId(UUID.randomUUID().toString())
    .build()).messageId();
```

#### SNS to SQS Subscription
```java
// Create SQS queue for subscription
String subscriptionQueueUrl = sqsClient.createQueue(CreateQueueRequest.builder()
    .queueName("notification-subscriber")
    .build()).queueUrl();

// Get queue ARN
String queueArn = sqsClient.getQueueAttributes(GetQueueAttributesRequest.builder()
    .queueUrl(subscriptionQueueUrl)
    .attributeNames(QueueAttributeName.QUEUE_ARN)
    .build()).attributes().get(QueueAttributeName.QUEUE_ARN);

// Subscribe SQS to SNS
String subscriptionArn = snsClient.subscribe(SubscribeRequest.builder()
    .protocol("sqs")
    .endpoint(queueArn)
    .topicArn(topicArn)
    .build()).subscriptionArn();
```

### Spring Boot Integration Example

```java
@Service
@RequiredArgsConstructor
public class OrderNotificationService {

    private final SnsClient snsClient;
    private final ObjectMapper objectMapper;

    @Value("${aws.sns.order-topic-arn}")
    private String orderTopicArn;

    public void sendOrderNotification(Order order) {
        try {
            String jsonMessage = objectMapper.writeValueAsString(order);

            snsClient.publish(PublishRequest.builder()
                .topicArn(orderTopicArn)
                .subject("New Order Received")
                .message(jsonMessage)
                .messageAttributes(Map.of(
                    "orderType", MessageAttributeValue.builder()
                        .dataType("String")
                        .stringValue(order.getType())
                        .build()))
                .build());

        } catch (Exception e) {
            throw new RuntimeException("Failed to send order notification", e);
        }
    }
}
```

## Best Practices

### SQS Best Practices
- **Use long polling**: Set `waitTimeSeconds` (20-40 seconds) to reduce empty responses
- **Batch operations**: Use `sendMessageBatch` for multiple messages to reduce API calls
- **Visibility timeout**: Set appropriately based on message processing time (default 30 seconds)
- **Delete messages**: Always delete messages after successful processing
- **Handle duplicates**: Implement idempotent processing for retries
- **Implement DLQ**: Route failed messages to dead letter queues for analysis
- **Monitor queue depth**: Use CloudWatch alarms for high queue backlog
- **Use FIFO queues**: When message order and deduplication are critical

### SNS Best Practices
- **Use filter policies**: Reduce noise by filtering messages at the source
- **Message attributes**: Add metadata for subscription routing decisions
- **Retry logic**: Handle transient failures with exponential backoff
- **Monitor failed deliveries**: Set up CloudWatch alarms for failed notifications
- **Security**: Use IAM policies for access control and data encryption
- **FIFO topics**: Use when order and deduplication are critical
- **Avoid large payloads**: Keep messages under 256KB for optimal performance

### General Guidelines
- **Region consistency**: Use the same region for all AWS resources
- **Resource naming**: Use consistent naming conventions for queues and topics
- **Error handling**: Implement proper exception handling and logging
- **Testing**: Use LocalStack for local development and testing
- **Documentation**: Document subscription endpoints and message formats

## Instructions

### Setup AWS Credentials
Configure AWS credentials using environment variables, AWS CLI, or IAM roles:
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=us-east-1
```

### Configure Clients
```java
// Basic client configuration
SqsClient sqsClient = SqsClient.builder()
    .region(Region.US_EAST_1)
    .build();

// Advanced client with custom configuration
SnsClient snsClient = SnsClient.builder()
    .region(Region.US_EAST_1)
    .credentialsProvider(DefaultCredentialsProvider.create())
    .httpClient(UrlConnectionHttpClient.create())
    .build();
```

### Implement Message Processing
1. **Connect** to SQS/SNS using the AWS SDK clients
2. **Create** queues and topics as needed
3. **Send/receive** messages with appropriate timeout settings
4. **Process** messages in batches for efficiency
5. **Delete** messages after successful processing
6. **Handle** failures with proper error handling and retries

### Integrate with Spring Boot
1. **Configure** beans for `SqsClient` and `SnsClient` in `@Configuration` classes
2. **Use** `@Value` to inject queue URLs and topic ARNs from properties
3. **Create** service classes with business logic for messaging operations
4. **Implement** error handling with `@Retryable` or custom retry logic
5. **Test** integration using Testcontainers or LocalStack

### Monitor and Debug
- Use AWS CloudWatch for monitoring queue depth and message metrics
- Enable AWS SDK logging for debugging client operations
- Implement proper logging for message processing activities
- Use AWS X-Ray for distributed tracing in production environments

## Troubleshooting

### Common Issues
- **Queue does not exist**: Verify queue URL and permissions
- **Message not received**: Check visibility timeout and consumer logic
- **Permission denied**: Verify IAM policies and credentials
- **Connection timeout**: Check network connectivity and region configuration
- **Rate limiting**: Implement retry logic with exponential backoff

### Performance Optimization
- Use long polling to reduce empty responses
- Batch message operations to minimize API calls
- Adjust visibility timeout based on processing time
- Implement connection pooling and reuse clients
- Use appropriate message sizes to avoid fragmentation

## Detailed References

For comprehensive API documentation and advanced patterns, see:

- [@references/detailed-sqs-operations] - Complete SQS operations reference
- [@references/detailed-sns-operations] - Complete SNS operations reference
- [@references/spring-boot-integration] - Spring Boot integration patterns
- [@references/aws-official-documentation] - Official AWS documentation and best practices
