---
name: aws-sns
description: "Manage AWS SNS topics, subscriptions, and publish notifications."
metadata: {"thinkfleetbot":{"emoji":"🔔","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS SNS

Manage SNS topics and publish notifications.

## List topics

```bash
aws sns list-topics --query 'Topics[].TopicArn' --output table
```

## Get topic attributes

```bash
aws sns get-topic-attributes --topic-arn "$SNS_TOPIC_ARN" | jq '.Attributes | {DisplayName, SubscriptionsConfirmed, SubscriptionsPending}'
```

## List subscriptions

```bash
aws sns list-subscriptions-by-topic --topic-arn "$SNS_TOPIC_ARN" --query 'Subscriptions[].{Endpoint:Endpoint,Protocol:Protocol,Status:SubscriptionArn}' --output table
```

## Publish message

```bash
aws sns publish --topic-arn "$SNS_TOPIC_ARN" \
  --subject "Alert" \
  --message "Deployment complete for v1.2.3" | jq '{MessageId}'
```

## Publish JSON message (protocol-specific)

```bash
aws sns publish --topic-arn "$SNS_TOPIC_ARN" \
  --message-structure json \
  --message '{"default":"Alert","email":"Email body","sms":"SMS text"}' | jq '{MessageId}'
```

## Subscribe endpoint

```bash
aws sns subscribe --topic-arn "$SNS_TOPIC_ARN" \
  --protocol email --notification-endpoint user@example.com | jq '{SubscriptionArn}'
```

## Notes

- Email subscriptions require confirmation by the recipient.
- Confirm before publishing or subscribing endpoints.
