---
name: aws-sdk-java-v2-messaging
description: Provides AWS messaging patterns using AWS SDK for Java 2.x for SQS queues and SNS topics. Handles sending/receiving messages, FIFO queues, DLQ, subscriptions, and pub/sub patterns. Use when implementing messaging with SQS or SNS.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - Messaging (SQS & SNS)

## Overview

Provides patterns for SQS queues and SNS topics with AWS SDK for Java 2.x: client setup, queue management, message operations, subscriptions, and Spring Boot integration.

## When to Use

- Setting up SQS queues (standard or FIFO) for message buffering
- Implementing pub/sub with SNS topics and subscriptions
- Processing messages from SQS queues with long polling
- Configuring dead letter queues (DLQ) for error handling
- Integrating AWS messaging with Spring Boot applications
- Building event-driven architectures with SQS/SNS

## Examples

### Quick Setup

**Dependencies:**
```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>sqs</artifactId>
</dependency>
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>sns</artifactId>
</dependency>
```

**Client Configuration:**
```java
SqsClient sqsClient = SqsClient.builder()
    .region(Region.US_EAST_1)
    .credentialsProvider(DefaultCredentialsProvider.create())
    .build();

SnsClient snsClient = SnsClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

### SQS Operations

**Create and Send Message:**
```java
String queueUrl = sqsClient.createQueue(CreateQueueRequest.builder()
    .queueName("my-queue")
    .build()).queueUrl();

String messageId = sqsClient.sendMessage(SendMessageRequest.builder()
    .queueUrl(queueUrl)
    .messageBody("Hello, SQS!")
    .build()).messageId();
```

**Receive and Delete Message:**
```java
ReceiveMessageResponse response = sqsClient.receiveMessage(ReceiveMessageRequest.builder()
    .queueUrl(queueUrl)
    .maxNumberOfMessages(10)
    .waitTimeSeconds(20)
    .build());

response.messages().forEach(message -> {
    processMessage(message.body());
    sqsClient.deleteMessage(DeleteMessageRequest.builder()
        .queueUrl(queueUrl)
        .receiptHandle(message.receiptHandle())
        .build());
});
```

**FIFO Queue:**
```java
Map<QueueAttributeName, String> attributes = Map.of(
    QueueAttributeName.FIFO_QUEUE, "true",
    QueueAttributeName.CONTENT_BASED_DEDUPLICATION, "true"
);

String fifoQueueUrl = sqsClient.createQueue(CreateQueueRequest.builder()
    .queueName("my-queue.fifo")
    .attributes(attributes)
    .build()).queueUrl();

sqsClient.sendMessage(SendMessageRequest.builder()
    .queueUrl(fifoQueueUrl)
    .messageBody("Order #12345")
    .messageGroupId("orders")
    .messageDeduplicationId(UUID.randomUUID().toString())
    .build());
```

### SNS Operations

**Create Topic and Publish:**
```java
String topicArn = snsClient.createTopic(CreateTopicRequest.builder()
    .name("my-topic")
    .build()).topicArn();

snsClient.publish(PublishRequest.builder()
    .topicArn(topicArn)
    .subject("Test Notification")
    .message("Hello, SNS!")
    .build());
```

**SNS to SQS Subscription:**
```java
String queueArn = sqsClient.getQueueAttributes(GetQueueAttributesRequest.builder()
    .queueUrl(queueUrl)
    .attributeNames(QueueAttributeName.QUEUE_ARN)
    .build()).attributes().get(QueueAttributeName.QUEUE_ARN);

snsClient.subscribe(SubscribeRequest.builder()
    .protocol("sqs")
    .endpoint(queueArn)
    .topicArn(topicArn)
    .build());
```

### Spring Boot Integration
```java
@Service
@RequiredArgsConstructor
public class OrderNotificationService {
    private final SnsClient snsClient;
    private final ObjectMapper objectMapper;

    @Value("${aws.sns.order-topic-arn}")
    private String orderTopicArn;

    public void sendOrderNotification(Order order) throws JsonProcessingException {
        snsClient.publish(PublishRequest.builder()
            .topicArn(orderTopicArn)
            .subject("New Order Received")
            .message(objectMapper.writeValueAsString(order))
            .messageAttributes(Map.of(
                "orderType", MessageAttributeValue.builder()
                    .dataType("String")
                    .stringValue(order.getType())
                    .build()))
            .build());
    }
}
```

## Instructions

### Implement Message Processing (with Validation)

1. **Create queues/topics** with appropriate configuration
2. **Send messages** and validate `messageId` is returned
3. **Receive messages** with long polling (`waitTimeSeconds: 20`)
4. **Process messages** - validate payload before processing
5. **Delete messages** only after successful processing - verify deletion response
6. **Check DLQ** periodically for failed messages using `redrivePolicy`
7. **Verify delivery** - monitor CloudWatch `NumberOfMessagesSent` metric

**Validation Checklist:**
```java
// After send
if (messageId == null || messageId.isEmpty()) {
    throw new MessagingException("Message send failed - no messageId returned");
}

// After receive
if (response.messages().isEmpty()) {
    log.debug("No messages available - normal with long polling");
}

// After delete
if (!deleteResponse.sdkHttpResponse().isSuccessful()) {
    throw new MessagingException("Message deletion failed");
}
```

### Setup Credentials
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=us-east-1
```

### Monitor and Debug
- CloudWatch metrics: `ApproximateNumberOfMessages`, `NumberOfMessagesSent`, `NumberOfMessagesReceived`
- Enable SDK logging: `software.amazon.awssdk` at DEBUG level
- Use X-Ray for distributed tracing

## Best Practices

**SQS:**
- Use long polling (20-40s) to reduce empty responses and costs
- Always delete messages after successful processing
- Implement idempotent processing for duplicate handling
- Configure DLQ (`redrivePolicy`) for failed messages
- Use FIFO queues when order matters (300 msg/sec limit)

**SNS:**
- Use filter policies to reduce unnecessary deliveries
- Keep messages under 256KB
- Implement retry with exponential backoff
- Monitor `NumberOfNotificationFailed` metric

**General:**
- Use IAM roles over static credentials
- Reuse clients (they are thread-safe)
- Test with LocalStack or Testcontainers

## Detailed References

- [references/detailed-sqs-operations.md](references/detailed-sqs-operations.md)
- [references/detailed-sns-operations.md](references/detailed-sns-operations.md)
- [references/spring-boot-integration.md](references/spring-boot-integration.md)
- [references/aws-official-documentation.md](references/aws-official-documentation.md)

## Constraints and Warnings

- **Message Size**: Maximum 256KB for SQS and SNS
- **Visibility Timeout**: Undeleted messages reappear after timeout - always delete after processing
- **Input Validation**: Sanitize message body before processing - messages may contain untrusted payloads
- **FIFO Naming**: Must end with `.fifo` suffix
- **FIFO Throughput**: 300 msg/sec per queue (use partitioning for higher throughput)
- **Message Retention**: SQS retains messages max 14 days
- **DLQ Required**: Configure dead letter queue to prevent message loss
- **Region-Specific**: SQS queues are region-specific; cross-region requires SNS
