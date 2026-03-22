---
name: aws-sqs
description: "Manage AWS SQS queues -- send, receive, and manage messages."
metadata: {"thinkfleetbot":{"emoji":"📨","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS SQS

Manage SQS queues and messages.

## List queues

```bash
aws sqs list-queues --output table
```

## Get queue attributes

```bash
aws sqs get-queue-attributes --queue-url "$SQS_QUEUE_URL" --attribute-names All | jq '.Attributes | {Messages: .ApproximateNumberOfMessages, InFlight: .ApproximateNumberOfMessagesNotVisible, Delayed: .ApproximateNumberOfMessagesDelayed, Visibility: .VisibilityTimeout, Retention: .MessageRetentionPeriod}'
```

## Send message

```bash
aws sqs send-message --queue-url "$SQS_QUEUE_URL" \
  --message-body '{"event":"deploy","version":"1.2.3"}' | jq '{MessageId, MD5OfMessageBody}'
```

## Receive messages

```bash
aws sqs receive-message --queue-url "$SQS_QUEUE_URL" \
  --max-number-of-messages 5 --wait-time-seconds 5 | jq '.Messages[]? | {MessageId, Body}'
```

## Delete message

```bash
aws sqs delete-message --queue-url "$SQS_QUEUE_URL" \
  --receipt-handle "RECEIPT_HANDLE_HERE"
echo "Message deleted"
```

## Purge queue

```bash
aws sqs purge-queue --queue-url "$SQS_QUEUE_URL"
echo "Queue purged"
```

## Get queue URL by name

```bash
aws sqs get-queue-url --queue-name my-queue | jq -r '.QueueUrl'
```

## Notes

- Messages must be explicitly deleted after processing.
- `purge-queue` is irreversible and has a 60-second cooldown.
- Always confirm before purging queues or sending messages.
