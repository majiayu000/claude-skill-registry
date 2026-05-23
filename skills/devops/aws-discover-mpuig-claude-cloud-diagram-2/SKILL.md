---
name: aws-discover
description: Discover AWS infrastructure and save to JSON. Use when user asks to "discover AWS", "explore AWS account", "scan AWS infrastructure", or "create infrastructure JSON".
---

# AWS Infrastructure Discovery

Explore an AWS account and collect comprehensive information about its infrastructure.

## Before Starting

Ask the user for:
1. **AWS Profile** - Which AWS profile to use (or use default)
2. **AWS Region** - Which region to scan (or use default)

## AWS CLI Configuration

Use the profile and region flags with all AWS CLI commands:
```bash
aws <command> --profile <profile> --region <region>
```

## Discovery Process

Explore systematically. Start with basics, then dig deeper based on what you find.

### 1. Account Identity
```bash
aws sts get-caller-identity --profile <profile> --region <region>
```

### 2. Networking
- VPCs: `aws ec2 describe-vpcs`
- Subnets: `aws ec2 describe-subnets`
- Internet Gateways: `aws ec2 describe-internet-gateways`
- NAT Gateways: `aws ec2 describe-nat-gateways`
- Transit Gateways: `aws ec2 describe-transit-gateways`
- VPC Endpoints: `aws ec2 describe-vpc-endpoints`
- Route Tables: `aws ec2 describe-route-tables`

### 3. Compute
- ECS Clusters: `aws ecs list-clusters` then `aws ecs describe-clusters`
- ECS Services: `aws ecs list-services --cluster <name>` then `aws ecs describe-services`
- Lambda: `aws lambda list-functions`
- EC2: `aws ec2 describe-instances`
- EKS: `aws eks list-clusters`

### 4. Load Balancing
- ALB/NLB: `aws elbv2 describe-load-balancers`
- Listeners: `aws elbv2 describe-listeners --load-balancer-arn <arn>`
- Target Groups: `aws elbv2 describe-target-groups`
- Rules: `aws elbv2 describe-rules --listener-arn <arn>`

### 5. Databases
- RDS: `aws rds describe-db-instances`
- Aurora: `aws rds describe-db-clusters`
- DynamoDB: `aws dynamodb list-tables`
- ElastiCache: `aws elasticache describe-cache-clusters`

### 6. Storage
- S3: `aws s3api list-buckets`
- EFS: `aws efs describe-file-systems`
- ECR: `aws ecr describe-repositories`

### 7. Security
- Security Groups: `aws ec2 describe-security-groups`
- WAF: `aws wafv2 list-web-acls --scope REGIONAL`
- Cognito: `aws cognito-idp list-user-pools --max-results 20`
- ACM: `aws acm list-certificates`
- Secrets Manager: `aws secretsmanager list-secrets`
- KMS: `aws kms list-keys`

### 8. Messaging
- SQS: `aws sqs list-queues`
- SNS: `aws sns list-topics`
- EventBridge: `aws events list-rules`

### 9. API & CDN
- API Gateway: `aws apigateway get-rest-apis`
- CloudFront: `aws cloudfront list-distributions`

## Output Format

Create `aws_infrastructure.json` with this structure:

```json
{
  "metadata": {
    "account_id": "...",
    "region": "...",
    "environment": "...",
    "project": "...",
    "discovered_at": "..."
  },
  "networking": {
    "vpc": {"id": "...", "name": "...", "cidr": "..."},
    "subnets": {
      "public": [{"id": "...", "name": "...", "cidr": "...", "az": "..."}],
      "private": [{"id": "...", "name": "...", "cidr": "...", "az": "..."}]
    },
    "internet_gateway": {"id": "..."},
    "nat_gateways": [...],
    "transit_gateway": {"id": "...", "routes": [...]},
    "vpc_endpoints": [{"id": "...", "type": "...", "service": "..."}]
  },
  "load_balancers": {
    "public": {"name": "...", "scheme": "internet-facing", "dns_name": "..."},
    "private": {"name": "...", "scheme": "internal"}
  },
  "compute": {
    "ecs_cluster": {"name": "..."},
    "ecs_services": [{"name": "...", "launch_type": "FARGATE"}],
    "lambda_functions": [{"name": "...", "runtime": "..."}],
    "ec2_instances": [...]
  },
  "databases": {
    "aurora_clusters": [{"database_name": "...", "engine": "..."}],
    "dynamodb_tables": [{"name": "..."}],
    "elasticache": {"engine": "redis", "num_cache_clusters": 2}
  },
  "storage": {
    "s3_buckets": [{"name": "..."}],
    "ecr_repositories": [...]
  },
  "security": {
    "waf": {"web_acl": {"name": "..."}},
    "acm_certificates": [{"domain": "..."}],
    "cognito_pools": [{"name": "..."}]
  },
  "messaging": {
    "sqs_queues": [...],
    "sns_topics": [...],
    "eventbridge_rules": [...]
  },
  "traffic_rules": {
    "allowed_sources": {
      "public_internet": {"cidrs": ["0.0.0.0/0"], "ports": [443]},
      "corporate": {"cidrs": ["10.0.0.0/8"], "ports": [80, 443]}
    },
    "domains": {
      "public": ["api.example.com"],
      "private": ["internal.example.com"]
    }
  }
}
```

## Guidelines

- Only include sections that have resources (omit empty sections)
- Infer environment and project from resource names/tags
- Infer traffic rules from security group ingress rules and load balancer configurations
- For subnets, use "az" field (not "availability_zone")
- Skip empty services quickly - if `list-*` returns empty, move on
- Add new sections for services not listed (e.g., "step_functions", "glue", "opensearch")

## After Discovery

Tell the user:
1. What was discovered (summary of resources)
2. That they can now generate diagrams with: "generate AWS diagram"
