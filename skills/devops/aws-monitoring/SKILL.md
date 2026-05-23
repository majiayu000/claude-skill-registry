---
name: aws-monitoring
description: Debug AWS resource issues, check Lambda logs, and monitor deployed services. Use when investigating production issues, checking CloudWatch logs, or debugging deployment failures.
allowed-tools: Bash, Read, Grep
---

# AWS Monitoring Skill

This skill helps you monitor and debug AWS resources for the SG Cars Trends platform.

## When to Use This Skill

- Investigating production errors
- Checking Lambda function logs
- Monitoring API performance
- Debugging deployment failures
- Analyzing CloudWatch metrics
- Setting up alarms
- Troubleshooting resource issues

## Monitoring Tools

### SST Console

SST provides a built-in console for monitoring:

```bash
# Open SST console for specific stage
npx sst console --stage production
npx sst console --stage staging
npx sst console --stage dev
```

Features:
- Real-time Lambda logs
- Function invocations
- Error tracking
- Resource overview
- Environment variables

### CloudWatch Logs

Access Lambda logs via CloudWatch:

```bash
# View logs using SST
npx sst logs --stage production

# View specific function logs
npx sst logs --stage production --function api

# Tail logs in real-time
npx sst logs --stage production --function api --tail

# Filter logs
npx sst logs --stage production --function api --filter "ERROR"

# Show logs from specific time
npx sst logs --stage production --function api --since 1h
npx sst logs --stage production --function api --since "2024-01-15 10:00"
```

### AWS CLI

Use AWS CLI for advanced log queries:

```bash
# List log groups
aws logs describe-log-groups \
  --log-group-name-prefix "/aws/lambda/sgcarstrends"

# Get recent log streams
aws logs describe-log-streams \
  --log-group-name "/aws/lambda/sgcarstrends-api-production" \
  --order-by LastEventTime \
  --descending \
  --max-items 5

# Tail logs
aws logs tail "/aws/lambda/sgcarstrends-api-production" --follow

# Filter logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/sgcarstrends-api-production" \
  --filter-pattern "ERROR" \
  --start-time $(date -u -d '1 hour ago' +%s)000

# Get logs for specific request
aws logs filter-log-events \
  --log-group-name "/aws/lambda/sgcarstrends-api-production" \
  --filter-pattern "request-id-here"
```

## CloudWatch Metrics

### Lambda Metrics

```bash
# Get Lambda invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-production \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Get errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-production \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Get duration
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-production \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum
```

### API Gateway Metrics

```bash
# Get API requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value=sgcarstrends-api \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Get 4XX errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name 4XXError \
  --dimensions Name=ApiName,Value=sgcarstrends-api \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Get latency
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Latency \
  --dimensions Name=ApiName,Value=sgcarstrends-api \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum,p99
```

## CloudWatch Alarms

### Creating Alarms

```typescript
// infra/alarms.ts
import { StackContext, use } from "sst/constructs";
import * as cloudwatch from "aws-cdk-lib/aws-cloudwatch";
import * as sns from "aws-cdk-lib/aws-sns";
import * as subscriptions from "aws-cdk-lib/aws-sns-subscriptions";
import { API } from "./api";

export function Alarms({ stack, app }: StackContext) {
  const { api } = use(API);

  // Only create alarms for production
  if (app.stage !== "production") {
    return;
  }

  // SNS topic for alarms
  const alarmTopic = new sns.Topic(stack, "AlarmTopic");

  // Add email subscription
  alarmTopic.addSubscription(
    new subscriptions.EmailSubscription("alerts@sgcarstrends.com")
  );

  // High error rate alarm
  new cloudwatch.Alarm(stack, "ApiHighErrorRate", {
    metric: api.metricErrors(),
    threshold: 10,
    evaluationPeriods: 2,
    datapointsToAlarm: 2,
    alarmDescription: "API has high error rate",
    treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
  }).addAlarmAction(new cloudwatch.SnsAction(alarmTopic));

  // High duration alarm
  new cloudwatch.Alarm(stack, "ApiHighDuration", {
    metric: api.metricDuration(),
    threshold: 5000, // 5 seconds
    evaluationPeriods: 2,
    datapointsToAlarm: 2,
    alarmDescription: "API response time is high",
    treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
  }).addAlarmAction(new cloudwatch.SnsAction(alarmTopic));

  // Throttle alarm
  new cloudwatch.Alarm(stack, "ApiThrottled", {
    metric: api.metricThrottles(),
    threshold: 1,
    evaluationPeriods: 1,
    alarmDescription: "API is being throttled",
    treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
  }).addAlarmAction(new cloudwatch.SnsAction(alarmTopic));
}
```

Add to SST config:

```typescript
// infra/sst.config.ts
import { Alarms } from "./alarms";

export default {
  stacks(app) {
    app
      .stack(DNS)
      .stack(API)
      .stack(Web)
      .stack(Alarms); // Add alarms stack
  },
} satisfies SSTConfig;
```

### Managing Alarms via CLI

```bash
# List alarms
aws cloudwatch describe-alarms

# Get alarm state
aws cloudwatch describe-alarms \
  --alarm-names "sgcarstrends-ApiHighErrorRate"

# Disable alarm
aws cloudwatch disable-alarm-actions \
  --alarm-names "sgcarstrends-ApiHighErrorRate"

# Enable alarm
aws cloudwatch enable-alarm-actions \
  --alarm-names "sgcarstrends-ApiHighErrorRate"

# Delete alarm
aws cloudwatch delete-alarms \
  --alarm-names "sgcarstrends-ApiHighErrorRate"
```

## CloudWatch Insights

### Querying Logs

```bash
# Start query
aws logs start-query \
  --log-group-name "/aws/lambda/sgcarstrends-api-production" \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20'

# Get query results
aws logs get-query-results --query-id <query-id>
```

### Common Queries

**Find errors:**
```
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

**API performance:**
```
fields @timestamp, @duration
| stats avg(@duration), max(@duration), min(@duration)
```

**Count errors by type:**
```
fields @message
| filter @message like /ERROR/
| parse @message /(?<errorType>\w+Error)/
| stats count() by errorType
```

**Slow requests:**
```
fields @timestamp, @duration, @requestId
| filter @duration > 1000
| sort @duration desc
| limit 20
```

**Request rate:**
```
fields @timestamp
| stats count() by bin(5m)
```

## X-Ray Tracing

### Enable X-Ray

```typescript
// infra/api.ts
import { StackContext, Function } from "sst/constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";

export function API({ stack }: StackContext) {
  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    tracing: lambda.Tracing.ACTIVE, // Enable X-Ray
  });

  return { api };
}
```

### Instrument Code

```typescript
// apps/api/src/index.ts
import { captureAWSv3Client } from "aws-xray-sdk-core";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

// Wrap AWS SDK clients
const client = captureAWSv3Client(new DynamoDBClient({}));
```

### View Traces

```bash
# Get service graph
aws xray get-service-graph \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s)

# Get trace summaries
aws xray get-trace-summaries \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s)

# Get trace details
aws xray batch-get-traces --trace-ids <trace-id>
```

## Resource Monitoring

### Lambda Functions

```bash
# List functions
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `sgcarstrends`)].FunctionName'

# Get function config
aws lambda get-function-configuration \
  --function-name sgcarstrends-api-production

# Get function code location
aws lambda get-function \
  --function-name sgcarstrends-api-production

# Invoke function
aws lambda invoke \
  --function-name sgcarstrends-api-production \
  --payload '{"path": "/health"}' \
  response.json

cat response.json
```

### CloudFront Distributions

```bash
# List distributions
aws cloudfront list-distributions \
  --query 'DistributionList.Items[*].[Id,DomainName,Status]' \
  --output table

# Get distribution config
aws cloudfront get-distribution-config --id <distribution-id>

# Create invalidation (cache clear)
aws cloudfront create-invalidation \
  --distribution-id <distribution-id> \
  --paths "/*"

# List invalidations
aws cloudfront list-invalidations --distribution-id <distribution-id>
```

### S3 Buckets

```bash
# List buckets
aws s3 ls

# Get bucket size
aws s3 ls s3://bucket-name --recursive --summarize | grep "Total Size"

# Monitor bucket metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value=bucket-name Name=StorageType,Value=StandardStorage \
  --start-time $(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average
```

## Cost Monitoring

### Cost Explorer

```bash
# Get cost and usage
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d '1 month ago' +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE

# Get cost by tag
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d '1 month ago' +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=Environment
```

### Budget Alerts

Create budget in AWS Console or via CLI:

```bash
# Create budget
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Debugging Production Issues

### 1. Check Recent Deployments

```bash
# Get stack events
aws cloudformation describe-stack-events \
  --stack-name sgcarstrends-api-production \
  --max-items 50

# Get deployment status
npx sst stacks info API --stage production
```

### 2. Check Logs for Errors

```bash
# Get recent errors
npx sst logs --stage production --function api --filter "ERROR" --since 1h

# Or use AWS CLI
aws logs tail "/aws/lambda/sgcarstrends-api-production" \
  --follow \
  --filter-pattern "ERROR"
```

### 3. Check Metrics

```bash
# Check invocations and errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-production \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

### 4. Test Endpoint

```bash
# Test API directly
curl -I https://api.sgcarstrends.com/health

# Test with verbose output
curl -v https://api.sgcarstrends.com/health
```

### 5. Check Resource Limits

```bash
# Check Lambda quotas
aws service-quotas get-service-quota \
  --service-code lambda \
  --quota-code L-B99A9384  # Concurrent executions

# Check API Gateway quotas
aws service-quotas list-service-quotas \
  --service-code apigateway
```

## Common Issues

### High Latency

**Investigation**:
1. Check Lambda duration metrics
2. Review CloudWatch Insights for slow queries
3. Check database connection pool
4. Review API response times

**Solutions**:
- Increase Lambda memory
- Optimize database queries
- Add caching
- Use connection pooling

### High Error Rate

**Investigation**:
1. Check error logs
2. Review error types
3. Check external service status
4. Verify environment variables

**Solutions**:
- Fix application bugs
- Add error handling
- Retry failed requests
- Check API rate limits

### Cold Starts

**Investigation**:
1. Check init duration
2. Review package size
3. Check provisioned concurrency

**Solutions**:
- Enable provisioned concurrency
- Reduce bundle size
- Use ARM architecture
- Optimize imports

## Monitoring Scripts

### Health Check Script

```bash
#!/bin/bash
# scripts/health-check.sh

STAGE=${1:-production}
API_URL="https://api${STAGE:+.$STAGE}.sgcarstrends.com"

echo "Checking health of $STAGE environment..."

# Check API
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)

if [ $API_STATUS -eq 200 ]; then
  echo "✓ API is healthy"
else
  echo "✗ API is down (status: $API_STATUS)"
  exit 1
fi

# Check Web
WEB_URL="https://${STAGE:+$STAGE.}sgcarstrends.com"
WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $WEB_URL)

if [ $WEB_STATUS -eq 200 ]; then
  echo "✓ Web is healthy"
else
  echo "✗ Web is down (status: $WEB_STATUS)"
  exit 1
fi

echo "All services are healthy!"
```

Run:
```bash
chmod +x scripts/health-check.sh
./scripts/health-check.sh production
```

### Log Analysis Script

```bash
#!/bin/bash
# scripts/analyze-logs.sh

STAGE=${1:-production}
LOG_GROUP="/aws/lambda/sgcarstrends-api-$STAGE"

echo "Analyzing logs for $STAGE..."

# Count errors in last hour
ERROR_COUNT=$(aws logs filter-log-events \
  --log-group-name $LOG_GROUP \
  --filter-pattern "ERROR" \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --query 'events[*].message' \
  --output text | wc -l)

echo "Errors in last hour: $ERROR_COUNT"

# Get top errors
echo -e "\nTop error types:"
aws logs filter-log-events \
  --log-group-name $LOG_GROUP \
  --filter-pattern "ERROR" \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --query 'events[*].message' \
  --output text | \
  grep -oE '\w+Error' | \
  sort | uniq -c | sort -rn | head -5
```

## References

- CloudWatch Documentation: https://docs.aws.amazon.com/cloudwatch
- Lambda Monitoring: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-functions.html
- X-Ray: https://docs.aws.amazon.com/xray
- Related files:
  - `infra/` - Infrastructure with monitoring config
  - Root CLAUDE.md - Project documentation

## Best Practices

1. **Log Levels**: Use appropriate log levels (DEBUG, INFO, WARN, ERROR)
2. **Structured Logging**: Use JSON format for easier parsing
3. **Correlation IDs**: Track requests across services
4. **Alarms**: Set up alarms for critical metrics
5. **Dashboards**: Create CloudWatch dashboards for key metrics
6. **Cost Monitoring**: Track AWS costs regularly
7. **Regular Reviews**: Review logs and metrics weekly
8. **Retention**: Set appropriate log retention (7-30 days)
