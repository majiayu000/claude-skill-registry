---
name: aws-cli
description: "Manage AWS resources using the AWS CLI v2 (EC2, Lambda, ECS, CloudWatch, IAM, and more)."
metadata: {"thinkfleetbot":{"emoji":"🟠","requires":{"bins":["aws"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS CLI

Manage AWS resources using the AWS CLI v2.

## Environment Variables

- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_DEFAULT_REGION` - Default region (e.g. `us-east-1`)
- `AWS_SESSION_TOKEN` - Session token (for temporary credentials)

## Identity

```bash
aws sts get-caller-identity
```

## EC2 Instances

```bash
aws ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,Type:InstanceType,State:State.Name,Name:Tags[?Key==`Name`].Value|[0]}' --output table
```

```bash
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

```bash
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

## Lambda

```bash
aws lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime,Memory:MemorySize}' --output table
```

```bash
aws lambda invoke --function-name my-function --payload '{"key":"value"}' /tmp/lambda-output.json && cat /tmp/lambda-output.json
```

## ECS

```bash
aws ecs list-clusters --output table
```

```bash
aws ecs list-services --cluster my-cluster --output table
```

```bash
aws ecs describe-services --cluster my-cluster --services my-service --query 'services[].{Name:serviceName,Status:status,Running:runningCount,Desired:desiredCount}' --output table
```

## CloudWatch Logs

```bash
aws logs describe-log-groups --query 'logGroups[].logGroupName' --output table | head -20
```

```bash
aws logs tail /aws/lambda/my-function --since 1h --format short
```

## S3

```bash
aws s3 ls
```

```bash
aws s3 ls s3://my-bucket/ --recursive --human-readable --summarize | tail -20
```

## IAM

```bash
aws iam list-users --query 'Users[].{Name:UserName,Created:CreateDate}' --output table
```

```bash
aws iam list-roles --query 'Roles[].{Name:RoleName,Arn:Arn}' --output table | head -20
```

## CloudFormation

```bash
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query 'StackSummaries[].{Name:StackName,Status:StackStatus}' --output table
```

## RDS

```bash
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus,Class:DBInstanceClass}' --output table
```

## Cost (last 7 days)

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '7 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics BlendedCost \
  --query 'ResultsByTime[].{Date:TimePeriod.Start,Cost:Total.BlendedCost.Amount}' --output table
```

## Notes

- Use `--output table` for readable output, `--output json` for parsing with jq.
- Use `--query` (JMESPath) to filter results.
- Always confirm before modifying resources (start/stop instances, invoke functions, delete).
- Use `--dry-run` where supported to preview changes.
