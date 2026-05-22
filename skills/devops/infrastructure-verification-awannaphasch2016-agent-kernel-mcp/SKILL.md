---
name: infrastructure-verification
description: Verify AWS infrastructure configuration before deployment. Use when validating VPC endpoints, NAT Gateway capacity, security groups, or debugging network path issues that cause Lambda connection timeouts.
---

# Infrastructure Verification Skill

**Tech Stack**: AWS CLI, Terraform, VPC, CloudWatch, bash

**Source**: Extracted from PDF S3 upload timeout investigation (2026-01-05) and Infrastructure-Application Contract principle.

---

## When to Use This Skill

Use the infrastructure-verification skill when:
- ✓ Before deploying Lambda-in-VPC code
- ✓ Investigating Lambda connection timeouts
- ✓ Debugging deterministic failure patterns (first N succeed, last M fail)
- ✓ Validating network path to AWS services (S3, DynamoDB, RDS)
- ✓ After adding VPC endpoints
- ✓ Before concurrent Lambda executions

**DO NOT use this skill for:**
- ✗ Application code debugging (use error-investigation)
- ✗ Performance optimization (different focus)
- ✗ IAM permission issues (use AWS CLI directly)

---

## Core Verification Principles

### Principle 1: Infrastructure Dependency Validation

**From CLAUDE.md Principle #15:**
> "Before deploying code that depends on AWS infrastructure (S3, VPC endpoints, NAT Gateway), verify infrastructure exists and is correctly configured. Network path issues cause deterministic failure patterns."

**When to validate:**
- Before deploying Lambda functions that make AWS service calls
- After Terraform infrastructure changes
- When investigating Lambda timeout patterns
- Before increasing concurrency limits

### Principle 2: Pattern Recognition

**Failure Pattern Types:**

| Pattern | Root Cause | Investigation Priority |
|---------|------------|----------------------|
| **First N succeed, last M fail** | Infrastructure bottleneck (NAT, connection limits) | HIGH - VPC endpoint missing |
| **Random scattered failures** | Performance issue (slow API, memory) | MEDIUM - Optimize code |
| **All operations fail** | Configuration issue (permissions, endpoint) | HIGH - Fix config |
| **Intermittent failures** | Rate limiting, transient network | LOW - Add retries |

**Deterministic pattern** (first N succeed, last M fail) is strongest signal of infrastructure bottleneck.

---

## Verification Workflows

### Workflow 1: VPC Endpoint Verification

**Use when:** Lambda-in-VPC needs to access S3 or DynamoDB

**Steps:**

```bash
# 1. Check if VPC endpoint exists
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=vpc-xxx" \
            "Name=service-name,Values=com.amazonaws.ap-southeast-1.s3" \
  --query 'VpcEndpoints[*].{ID:VpcEndpointId,State:State,Service:ServiceName}' \
  --output table

# Expected output (if endpoint exists):
# -----------------------------------------
# | DescribeVpcEndpoints                  |
# +-------+-------+------------------------+
# | ID    | State | Service                |
# +-------+-------+------------------------+
# | vpce-xxx | available | com.amazonaws.ap-southeast-1.s3 |
# +-------+-------+------------------------+

# If empty → No S3 VPC Endpoint (traffic goes through NAT Gateway)

# 2. Verify endpoint state
aws ec2 describe-vpc-endpoints \
  --vpc-endpoint-ids vpce-xxx \
  --query 'VpcEndpoints[0].State' \
  --output text

# Expected: "available"
# If "pending" → Wait for creation
# If "failed" → Check Terraform logs

# 3. Verify route table attachment
aws ec2 describe-vpc-endpoints \
  --vpc-endpoint-ids vpce-xxx \
  --query 'VpcEndpoints[0].RouteTableIds' \
  --output table

# Expected: List of route table IDs (must include Lambda subnet route tables)

# 4. Check Lambda subnet route tables
aws lambda get-function-configuration \
  --function-name my-function \
  --query 'VpcConfig.SubnetIds' \
  --output text | xargs -I {} aws ec2 describe-subnets --subnet-ids {}

# Compare: Lambda subnets' route tables should be in VPC endpoint's RouteTableIds

# 5. Verify S3 prefix list in route tables
ROUTE_TABLE_ID=$(aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=vpc-xxx" \
  --query 'RouteTables[0].RouteTableId' \
  --output text)

aws ec2 describe-route-tables \
  --route-table-ids $ROUTE_TABLE_ID \
  --query 'RouteTables[*].Routes[?GatewayId==`vpce-xxx`]'

# Expected: Route with DestinationPrefixListId (S3 prefix list)
```

**Verification checklist:**
- [ ] VPC endpoint exists (`describe-vpc-endpoints` returns result)
- [ ] State is "available" (not "pending" or "failed")
- [ ] Route tables attached (includes Lambda subnet route tables)
- [ ] S3 prefix list routes created (check route tables)

**Common issues:**
- Missing VPC endpoint → Create with Terraform
- State "pending" → Wait 2-3 minutes
- Route tables not attached → Update Terraform `route_table_ids`
- Lambda subnets not covered → Verify subnet route table IDs

### Workflow 2: NAT Gateway Diagnosis

**Use when:** Investigating Lambda connection timeouts with external services

**Steps:**

```bash
# 1. Check NAT Gateway exists
aws ec2 describe-nat-gateways \
  --filter "Name=vpc-id,Values=vpc-xxx" \
  --query 'NatGateways[*].{ID:NatGatewayId,State:State,PublicIp:NatGatewayAddresses[0].PublicIp}' \
  --output table

# Expected: State "available"

# 2. Check route tables using NAT Gateway
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=vpc-xxx" \
  --query 'RouteTables[*].Routes[?NatGatewayId!=`null`].[RouteTableId,DestinationCidrBlock,NatGatewayId]' \
  --output table

# Expected: Route 0.0.0.0/0 → nat-xxx (default route through NAT)

# 3. Analyze connection saturation pattern
# Run this during concurrent Lambda executions
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '5 minutes ago' +%s)000 \
  --filter-pattern "START RequestId" \
  --query 'events[*].timestamp' \
  --output text | xargs -n1 date -d @

# Check execution pattern:
# - All start within 1 second → Concurrent execution
# - Some timeout after 600s → NAT Gateway saturation

# 4. Check for connection timeout errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "ConnectTimeoutError" \
  --query 'events[*].message' \
  --output text

# If errors found → NAT Gateway connection limit reached

# 5. Calculate concurrent connection demand
CONCURRENT_LAMBDAS=$(aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '1 minute ago' +%s)000 \
  --filter-pattern "START RequestId" \
  --query 'length(events)' \
  --output text)

echo "Concurrent Lambdas: $CONCURRENT_LAMBDAS"
echo "NAT Gateway connection limit: ~55,000 (but establishment rate limited)"
```

**NAT Gateway saturation indicators:**
- ✅ Deterministic pattern (first N succeed, last M fail)
- ✅ ConnectTimeoutError in logs
- ✅ Long execution times (600s = boto3 default timeout)
- ✅ Timeline shows concurrent starts → split success/failure

**Solution:** Add VPC Gateway Endpoint for S3/DynamoDB to bypass NAT

### Workflow 3: Network Path Validation

**Use when:** Verifying Lambda can reach AWS services

**Steps:**

```bash
# 1. Identify Lambda VPC configuration
aws lambda get-function-configuration \
  --function-name my-function \
  --query 'VpcConfig.{VpcId:VpcId,SubnetIds:SubnetIds,SecurityGroupIds:SecurityGroupIds}' \
  --output json

# Save VPC ID, Subnet IDs, Security Group IDs

# 2. Check security group egress rules
aws ec2 describe-security-groups \
  --group-ids sg-xxx \
  --query 'SecurityGroups[*].IpPermissionsEgress[*].{Proto:IpProtocol,Port:FromPort,Dest:IpRanges[0].CidrIp}' \
  --output table

# Expected: 0.0.0.0/0 allowed (all egress)
# If restricted → Add rule for destination service

# 3. Check route table for Lambda subnet
SUBNET_ID=$(aws lambda get-function-configuration \
  --function-name my-function \
  --query 'VpcConfig.SubnetIds[0]' \
  --output text)

ROUTE_TABLE_ID=$(aws ec2 describe-route-tables \
  --filters "Name=association.subnet-id,Values=$SUBNET_ID" \
  --query 'RouteTables[0].RouteTableId' \
  --output text)

aws ec2 describe-route-tables \
  --route-table-ids $ROUTE_TABLE_ID \
  --query 'RouteTables[*].Routes[*].[DestinationCidrBlock,GatewayId,NatGatewayId]' \
  --output table

# Expected routes:
# - local → vpc-xxx (VPC internal)
# - 0.0.0.0/0 → nat-xxx (internet via NAT) OR vpce-xxx (S3 via endpoint)

# 4. Test actual network path (requires test Lambda invocation)
# Deploy temporary test Lambda:
# - Attempts connection to S3
# - Logs connection details
# - Reports success/failure

# 5. Analyze test results
aws logs tail /aws/lambda/network-test --since 1m

# Look for:
# - Connection established (success)
# - Connection timeout (NAT saturated)
# - Connection refused (security group blocked)
# - DNS resolution failure (VPC DNS issue)
```

**Network path checklist:**
- [ ] Lambda in VPC (`VpcConfig` not empty)
- [ ] Security group allows egress to destination
- [ ] Route table has path to destination (NAT or VPC endpoint)
- [ ] VPC endpoint exists for AWS service (S3, DynamoDB)
- [ ] Test invocation confirms connectivity

### Workflow 4: Post-Deployment Infrastructure Validation

**Use when:** After deploying infrastructure changes (VPC endpoints, security groups)

**Steps:**

```bash
# 1. Verify Terraform outputs
cd terraform
terraform output s3_vpc_endpoint_id        # Should return vpce-xxx
terraform output s3_vpc_endpoint_state     # Should return "available"

# 2. Run smoke test Lambda invocation
aws lambda invoke \
  --function-name my-function \
  --payload '{"test": true}' \
  /tmp/response.json

# Check response
cat /tmp/response.json | jq .

# 3. Verify CloudWatch logs show success
aws logs tail /aws/lambda/my-function --since 1m --follow

# Expected:
# - No ConnectTimeoutError
# - Operation completes in expected time (2-3s not 600s)
# - Success message logged

# 4. Test concurrent execution (simulate production load)
for i in {1..10}; do
  aws lambda invoke \
    --function-name my-function \
    --payload "{\"id\": $i}" \
    --invocation-type Event \
    /tmp/response_$i.json &
done
wait

# 5. Analyze concurrent execution results
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '5 minutes ago' +%s)000 \
  --filter-pattern "ConnectTimeoutError" \
  --query 'length(events)' \
  --output text

# Expected: 0 (no timeout errors)
# If > 0 → Infrastructure issue still exists

# 6. Verify 100% success rate
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '5 minutes ago' +%s)000 \
  --filter-pattern "✅" \
  --query 'length(events)' \
  --output text

# Expected: 10 (all concurrent executions succeeded)
```

**Post-deployment checklist:**
- [ ] Terraform outputs confirm resource created
- [ ] Smoke test invocation succeeds
- [ ] CloudWatch logs show no errors
- [ ] Concurrent execution test (10+ invocations)
- [ ] 100% success rate (no timeouts)
- [ ] Execution time within expected range (2-3s not 600s)

---

## Common Infrastructure Issues

### Issue 1: Missing S3 VPC Endpoint

**Symptom:**
- Lambda timeout after 600s
- Error: `ConnectTimeoutError: Connect timeout on endpoint URL: "https://bucket.s3.region.amazonaws.com/..."`
- Pattern: First N concurrent operations succeed, last M timeout

**Diagnosis:**

```bash
# Check for S3 VPC endpoint
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=vpc-xxx" \
            "Name=service-name,Values=com.amazonaws.region.s3"

# If empty → No endpoint (S3 traffic goes through NAT)
```

**Fix:**

```hcl
# terraform/s3_vpc_endpoint.tf
data "aws_route_tables" "vpc_route_tables" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = data.aws_route_tables.vpc_route_tables.ids

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:*"
      Resource  = "*"
    }]
  })

  tags = {
    Name = "s3-endpoint"
  }
}

output "s3_vpc_endpoint_id" {
  value = aws_vpc_endpoint.s3.id
}

output "s3_vpc_endpoint_state" {
  value = aws_vpc_endpoint.s3.state
}
```

**Verification:**

```bash
cd terraform
terraform apply
terraform output s3_vpc_endpoint_state  # Should be "available"

# Test Lambda invocation
aws lambda invoke --function-name my-function --payload '{}' /tmp/response.json
aws logs tail /aws/lambda/my-function --since 1m
# Expected: No timeout, completes in 2-3s
```

### Issue 2: NAT Gateway Connection Saturation

**Symptom:**
- Deterministic failure pattern (first 5 succeed, last 5 timeout)
- All timeouts occur after ~10 minutes (boto3 default + retries)
- Timeline analysis shows concurrent Lambda starts

**Diagnosis:**

```bash
# Check timeline of Lambda executions
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '30 minutes ago' +%s)000 \
  --filter-pattern "START RequestId" \
  | jq -r '.events[] | .timestamp as $ts | ($ts/1000 | strftime("%H:%M:%S")) + " " + (.message | split(" ")[2])'

# Look for:
# - All start within 1 second (concurrent)
# - Check which RequestIds have errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "ConnectTimeoutError" \
  | jq -r '.events[].message' | grep -o "RequestId: [a-z0-9-]*"

# Pattern: Last N RequestIds consistently fail
```

**Root Cause:**
- NAT Gateway has limited connection establishment rate
- Concurrent Lambdas try to establish S3 connections simultaneously
- First N connections succeed → Upload completes in 2-3s
- Last M connections queued → Eventually timeout after 600s

**Fix:** Add S3 VPC Gateway Endpoint (see Issue 1)

**Why this works:**
- VPC Gateway Endpoint bypasses NAT Gateway
- S3 traffic routed directly within AWS network
- No connection establishment limits
- Free (Gateway endpoints have no hourly charge)

### Issue 3: Security Group Blocking Egress

**Symptom:**
- Lambda unable to connect to AWS service
- Error: Connection refused or timeout
- All invocations fail (not deterministic pattern)

**Diagnosis:**

```bash
# Check security group egress rules
aws lambda get-function-configuration \
  --function-name my-function \
  --query 'VpcConfig.SecurityGroupIds[0]' \
  --output text | xargs -I {} aws ec2 describe-security-groups --group-ids {}

# Look for egress rules allowing HTTPS (port 443)
# Expected: 0.0.0.0/0 or specific AWS service prefix list
```

**Fix:**

```hcl
# terraform/security_groups.tf
resource "aws_security_group_rule" "lambda_egress_https" {
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.lambda.id
}
```

### Issue 4: Route Table Not Attached to VPC Endpoint

**Symptom:**
- VPC endpoint exists and is "available"
- Lambda still times out connecting to S3
- Deterministic or random failures

**Diagnosis:**

```bash
# Check VPC endpoint route table attachment
aws ec2 describe-vpc-endpoints \
  --vpc-endpoint-ids vpce-xxx \
  --query 'VpcEndpoints[0].RouteTableIds' \
  --output table

# Get Lambda subnet route table
aws lambda get-function-configuration \
  --function-name my-function \
  --query 'VpcConfig.SubnetIds[0]' \
  --output text | xargs -I {} aws ec2 describe-route-tables \
  --filters "Name=association.subnet-id,Values={}" \
  --query 'RouteTables[0].RouteTableId' \
  --output text

# Compare: Lambda's route table should be in endpoint's RouteTableIds
```

**Fix:**

```hcl
# terraform/s3_vpc_endpoint.tf
data "aws_route_tables" "vpc_route_tables" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_endpoint" "s3" {
  # ... other config ...

  # Attach to ALL route tables (includes Lambda subnets)
  route_table_ids = data.aws_route_tables.vpc_route_tables.ids
}
```

---

## Integration with Other Skills

### With error-investigation
- Use infrastructure-verification BEFORE error-investigation when:
  - Investigating Lambda timeout patterns
  - Debugging connection failures
  - Analyzing deterministic failure patterns
- Use error-investigation AFTER infrastructure-verification when:
  - Infrastructure confirmed correct but errors persist
  - Need to analyze application logs
  - Debugging business logic failures

### With deployment skill
- Use infrastructure-verification:
  - BEFORE deploying Lambda-in-VPC code
  - AFTER deploying infrastructure changes (Terraform apply)
  - During post-deployment validation
- Complements deployment smoke tests with infrastructure-specific checks

### With testing-workflow
- Infrastructure verification is a form of pre-deployment testing
- Validates infrastructure-application contract (CLAUDE.md Principle #15)
- Catches configuration issues before code deployment

---

## Quick Reference

### VPC Endpoint Types

| Type | Services | Cost | Use Case |
|------|----------|------|----------|
| **Gateway** | S3, DynamoDB | FREE | High-throughput data access |
| **Interface** | Most AWS services | ~$7.50/month | Other services (Secrets Manager, etc.) |

### NAT Gateway Limits

| Limit | Value | Impact |
|-------|-------|--------|
| **Concurrent connections** | 55,000 | Theoretical max |
| **Connection establishment rate** | Limited | Causes saturation with concurrent Lambdas |
| **Data transfer cost** | $0.045/GB | Expensive for large transfers |

**Recommendation:** Use VPC Gateway Endpoints for S3/DynamoDB (free, unlimited, faster)

### Common AWS CLI Commands

```bash
# VPC endpoint
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-xxx

# NAT Gateway
aws ec2 describe-nat-gateways --nat-gateway-ids nat-xxx

# Security groups
aws ec2 describe-security-groups --group-ids sg-xxx

# Route tables
aws ec2 describe-route-tables --route-table-ids rtb-xxx

# Lambda VPC config
aws lambda get-function-configuration --function-name my-function --query 'VpcConfig'
```

---

## File Organization

```
.claude/skills/infrastructure-verification/
└── SKILL.md              # This file (complete skill)
```

---

## References

- [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
- [NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [Lambda VPC Configuration](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [Bug Hunt Report](../../bug-hunts/2026-01-05-pdf-s3-upload-timeout.md) - Real-world investigation
- CLAUDE.md Principle #15 (Infrastructure-Application Contract)
- CLAUDE.md Principle #2 (Progressive Evidence Strengthening)
