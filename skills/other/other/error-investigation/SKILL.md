---
name: error-investigation
description: AWS error investigation with multi-layer verification, CloudWatch analysis, and Lambda logging patterns. Use when debugging AWS service failures, investigating production errors, or troubleshooting Lambda functions.
---

# Error Investigation Skill

**Tech Stack**: AWS CLI, CloudWatch Logs, Lambda, boto3, jq

**Source**: Extracted from CLAUDE.md error investigation principles and AWS diagnostic patterns.

---

## When to Use This Skill

Use the error-investigation skill when:
- ✓ AWS service returning errors
- ✓ Lambda function failing in production
- ✓ CloudWatch logs showing errors
- ✓ Service completed but operation failed
- ✓ Silent failures (no exception but wrong result)
- ✓ Investigating production incidents

**DO NOT use this skill for:**
- ✗ Local Python debugging (use debugger instead)
- ✗ Code refactoring (use refactor skill)
- ✗ Performance optimization (use different skill)

---

## Quick Investigation Decision Tree

```
What's failing?
├─ Lambda function?
│  ├─ Returns 200 but errors? → Check CloudWatch logs (Layer 3)
│  ├─ Timeout? → Check duration metrics + external dependencies
│  ├─ Permission denied? → Check IAM role policies
│  └─ Cold start slow? → Module-level initialization pattern
│
├─ AWS service operation?
│  ├─ DynamoDB write succeeded (200) but no data? → Check rowcount
│  ├─ S3 upload succeeded but file missing? → Check bucket policy
│  ├─ SQS message sent but not received? → Check DLQ
│  └─ Step Function succeeded but workflow incomplete? → Check state outputs
│
├─ External API call?
│  ├─ Timeout? → Check network path (security groups, VPC)
│  ├─ 403 Forbidden? → Check API key, rate limits
│  ├─ 500 Error? → Check API status page, retry logic
│  └─ Silent failure? → Inspect response payload
│
└─ Database query?
   ├─ INSERT affected 0 rows? → FK constraint, ENUM mismatch
   ├─ SELECT returns empty? → Check WHERE clause, data exists
   ├─ Connection timeout? → Security group, VPC routing
   └─ Query slow? → Missing index, full table scan
```

---

## Loop Pattern: Retrying Loop → Synchronize Loop

**Escalation Trigger**:
- `/trace` shows root cause
- Fix applied, `/validate` shows success
- But error recurs later (knowledge drift)

**Tools Used**:
- `/trace` - Find root cause (backward trace from error)
- `/validate` - Verify fix works (test the solution)
- `/consolidate` - Update knowledge base (documentation, runbooks)
- `/observe` - Monitor for recurring issues (drift detection)
- `/reflect` - Assess if error represents pattern vs one-off

**Why This Works**: Error investigation fits retrying loop (find root cause, fix execution), but recurring errors trigger synchronize loop (update knowledge/documentation).

See [Thinking Process Architecture - Feedback Loops](../../.claude/diagrams/thinking-process-architecture.md#11-feedback-loop-types-self-healing-properties) for structural overview.

---

## Core Investigation Principles

### Principle 1: Execution Completion ≠ Operational Success

**From CLAUDE.md:**
> "Execution completion ≠ Operational success. Verify actual outcomes across multiple layers, not just the absence of exceptions."

**Why This Matters:**

```python
# ❌ WRONG: Assumes 200 = success
response = lambda_client.invoke(FunctionName='worker', Payload='{}')
assert response['StatusCode'] == 200  # ✗ Weak validation

# ✅ RIGHT: Multi-layer verification
response = lambda_client.invoke(FunctionName='worker', Payload='{}')

# Layer 1: Status code
assert response['StatusCode'] == 200

# Layer 2: Response payload
payload = json.loads(response['Payload'].read())
assert 'errorMessage' not in payload

# Layer 3: CloudWatch logs
logs = cloudwatch.filter_log_events(
    logGroupName='/aws/lambda/worker',
    filterPattern='ERROR'
)
assert len(logs['events']) == 0
```

> **Note**: This is the AWS-specific application of **Progressive Evidence Strengthening** (CLAUDE.md Principle #2). The general pattern applies across all domains—here we show how it manifests in AWS Lambda/API debugging.

### Principle 2: Multi-Layer Verification (AWS Application)

**The Three Layers:**

| Layer | Signal Strength | What It Tells You | What It DOESN'T Tell You |
|-------|----------------|-------------------|--------------------------|
| **Status Code** | Weakest | Service responded | Whether it succeeded |
| **Response Payload** | Stronger | Function returned data | Whether logs show errors |
| **CloudWatch Logs** | Strongest | What actually happened | Future issues |

**Pattern:**

```bash
# Layer 1: Status code (weakest)
aws lambda invoke --function-name worker --payload '{}' /tmp/response.json
echo "Exit code: $?"  # 0 = AWS CLI succeeded

# Layer 2: Response payload (stronger)
if grep -q "errorMessage" /tmp/response.json; then
  echo "❌ Lambda returned error"
  exit 1
fi

# Layer 3: CloudWatch logs (strongest)
ERROR_COUNT=$(aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 120))000 \
  --filter-pattern "ERROR" \
  --query 'length(events)' --output text)

if [ "$ERROR_COUNT" -gt 0 ]; then
  echo "❌ Found errors in CloudWatch logs"
  exit 1
fi

echo "✅ All 3 layers verified"
```

See [AWS-DIAGNOSTICS.md](AWS-DIAGNOSTICS.md) for AWS-specific diagnostic patterns.

### Principle 3: Log Level Determines Discoverability

**From CLAUDE.md:**
> "Log levels are not just severity indicators—they determine whether failures are discoverable by monitoring systems."

**Log Level Impact:**

| Log Level | Monitored? | Alerted? | Discoverable? |
|-----------|------------|----------|---------------|
| **ERROR** | ✅ Yes | ✅ Yes | ✅ Dashboards |
| **WARNING** | ✅ Yes | ❌ No | ⚠️  Manual review |
| **INFO** | ⚠️  Maybe | ❌ No | ❌ Active search |
| **DEBUG** | ❌ No | ❌ No | ❌ Hidden |

**Investigation Pattern:**

```bash
# Step 1: Check ERROR level first
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --filter-pattern "ERROR"

# Step 2: If no ERRORs but operation failed → Check WARNING
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --filter-pattern "WARNING"

# Step 3: Check both application AND service logs
# - Application logs: /aws/lambda/worker
# - Service logs: Lambda execution errors, timeouts
```

**Why This Matters:**

```python
# ❌ BAD: Error logged at WARNING (invisible to monitoring)
try:
    result = db.execute(query, params)
    if result == 0:
        logger.warning("INSERT failed")  # ⚠️  Not monitored!
except Exception as e:
    logger.warning(f"DB error: {e}")  # ⚠️  Not alerted!

# ✅ GOOD: Error logged at ERROR (visible to monitoring)
try:
    result = db.execute(query, params)
    if result == 0:
        logger.error("INSERT failed - 0 rows affected")  # ✅ Monitored
        raise ValueError("Insert operation failed")
except Exception as e:
    logger.error(f"DB error: {e}")  # ✅ Alerted
    raise
```

### Principle 4: Lambda Logging Configuration

**From CLAUDE.md:**
> "AWS Lambda pre-configures logging before your code runs. Never use `logging.basicConfig()` in Lambda handlers—it's a no-op."

**The Problem:**

```python
# ❌ This does NOTHING in Lambda
import logging

logging.basicConfig(level=logging.INFO)  # No-op!
logger = logging.getLogger(__name__)
logger.info("Invisible in CloudWatch")  # Filtered out
```

**Why It Fails:**
- Lambda runtime adds handlers to root logger BEFORE your code runs
- `basicConfig()` only works if root logger has NO handlers
- Result: INFO-level logs are invisible

**The Solution:**

```python
# ✅ Works in both Lambda and local dev
import logging

root_logger = logging.getLogger()

if root_logger.handlers:  # Lambda (already configured)
    root_logger.setLevel(logging.INFO)
else:  # Local dev (needs configuration)
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Visible in CloudWatch")  # ✅ Works
```

See [LAMBDA-LOGGING.md](LAMBDA-LOGGING.md) for comprehensive Lambda logging patterns.

---

## Common Investigation Scenarios

### Scenario 1: Lambda Returns 200 But Has Errors

**Symptom:** Function completes, returns 200, but errors in logs.

**Investigation Steps:**

```bash
# 1. Invoke function
aws lambda invoke \
  --function-name worker \
  --payload '{"ticker": "NVDA19"}' \
  /tmp/response.json

# 2. Check response (Layer 2)
cat /tmp/response.json
# Output: {"result": {...}}  # Looks fine

# 3. Check CloudWatch logs (Layer 3)
aws logs tail /aws/lambda/worker --since 1m --filter-pattern "ERROR"

# Output:
# [ERROR] 2024-01-15 10:23:45 INSERT affected 0 rows for NVDA19
# [ERROR] 2024-01-15 10:23:46 FK constraint violation: symbol not found
```

**Root Cause:** Silent database failure (0 rowcount), logged at ERROR but caught exception.

**Fix:**

```python
# Before:
def store_report(symbol, report):
    try:
        self.db.execute(query, params)
        return True  # ❌ Always returns True
    except Exception as e:
        logger.error(f"DB error: {e}")
        return True  # ❌ Still returns True!

# After:
def store_report(symbol, report):
    rowcount = self.db.execute(query, params)
    if rowcount == 0:
        logger.error(f"INSERT affected 0 rows for {symbol}")
        return False  # ✅ Returns False on failure
    return True
```

### Scenario 2: INFO Logs Not Showing in CloudWatch

**Symptom:** `logger.info()` calls not appearing in CloudWatch.

**Investigation Steps:**

```bash
# 1. Check current log level
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 300))000 \
  --filter-pattern "INFO"

# No results (but INFO logs exist in code)

# 2. Check root logger configuration
# Add to Lambda handler:
import logging
print(f"Root logger level: {logging.getLogger().level}")
print(f"Root logger handlers: {logging.getLogger().handlers}")
```

**Root Cause:** Root logger set to WARNING, filters out INFO.

**Fix:**

```python
# handler.py (entry point)
import logging

# Configure logging at module level
root_logger = logging.getLogger()

if root_logger.handlers:  # Lambda environment
    root_logger.setLevel(logging.INFO)  # ✅ Set root logger level
else:  # Local development
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    logger.info("Handler invoked")  # Now visible
    # ...
```

See [LAMBDA-LOGGING.md#troubleshooting](LAMBDA-LOGGING.md#troubleshooting) for complete debugging guide.

### Scenario 3: Lambda Timeout with Network Operations

**Symptom:** Lambda times out after long execution (600s+), logs show "PDF generation..." but no completion message.

**Investigation Steps:**

```bash
# 1. Check execution duration pattern
aws logs filter-log-events \
  --log-group-name /aws/lambda/pdf-worker \
  --filter-pattern "Duration:" \
  --query 'events[*].message' \
  | grep -o "Duration: [0-9]*" \
  | sort -n

# Look for pattern:
# - First 5 requests: Duration: 2-3s
# - Last 5 requests: Duration: 600s+ (timeout)

# 2. Check for connection timeout errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/pdf-worker \
  --filter-pattern "ConnectTimeoutError" \
  --query 'events[*].message'

# Output:
# botocore.exceptions.ConnectTimeoutError: Connect timeout on endpoint URL:
# "https://bucket.s3.region.amazonaws.com/..."

# 3. Analyze timeline (deterministic vs random)
aws logs tail /aws/lambda/pdf-worker --since 30m | \
  grep -E "START RequestId|✅ PDF job completed|ConnectTimeoutError" | \
  awk '{print $1, $2, $NF}' | sort

# Deterministic pattern (first N succeed, last M fail) = infrastructure bottleneck
# Random pattern (scattered failures) = performance issue
```

**Root Cause Analysis:**

```bash
# 4. Check VPC configuration
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=vpc-xxx" \
            "Name=service-name,Values=com.amazonaws.region.s3"

# If empty → No S3 VPC Endpoint (traffic goes through NAT Gateway)

# 5. Verify NAT Gateway routing
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=vpc-xxx" \
  --query 'RouteTables[*].Routes[?GatewayId!=`local`]'

# If route 0.0.0.0/0 → nat-xxx → NAT Gateway saturated with concurrent connections
```

**Root Cause:** NAT Gateway connection saturation. When N concurrent Lambdas upload to S3:
- NAT Gateway has limited connection establishment rate
- First N connections succeed (2-3s upload time)
- Remaining connections queue and timeout (600s = boto3 default timeout + retries)
- Pattern is deterministic (always first N succeed, last M fail)

**Fix:**

```hcl
# terraform/s3_vpc_endpoint.tf
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
}
```

**Why This Works:**
- S3 Gateway Endpoint adds routes to VPC route tables
- S3 traffic bypasses NAT Gateway (direct AWS network path)
- No connection establishment limits
- FREE (Gateway endpoints have no hourly charge)
- 200x faster (2-3s vs 600s timeout)

**Verification:**

```bash
# 1. Deploy VPC endpoint
cd terraform && terraform apply

# 2. Verify endpoint created
terraform output s3_vpc_endpoint_state  # Should be "available"

# 3. Test full workflow
aws stepfunctions start-execution \
  --state-machine-arn <pdf-workflow-arn> \
  --input '{"report_date":"2026-01-05"}'

# 4. Monitor for 100% success rate
aws logs tail /aws/lambda/pdf-worker --follow

# Expected: All PDFs complete in 2-3s, no timeouts
```

**Critical Insight:** **Execution Time ≠ Hang Location**
- 600s execution time doesn't mean code hangs for 600s
- It means ENTIRE execution (including network timeout) took 600s
- Check stack traces (Layer 3) to find WHERE timeout occurs
- Don't assume "logs stop at line X" = "code hangs at line X" (logs lost when Lambda fails)

**Pattern Recognition:**
- **Deterministic failure** (first N succeed, last M fail) → Infrastructure bottleneck (NAT, VPC endpoint)
- **Random failure** (scattered across all attempts) → Performance issue (slow API, memory pressure)
- **All fail** → Configuration issue (missing permissions, wrong endpoint)

See [Bug Hunt Report](../../bug-hunts/2026-01-05-pdf-s3-upload-timeout.md) for complete investigation.

### Scenario 4: DynamoDB PutItem Succeeds But No Data

**Symptom:** `put_item()` returns 200, but item not in table.

**Investigation Steps:**

```python
# 1. Check response
response = table.put_item(Item={'ticker': 'NVDA19', 'data': {...}})
print(f"HTTP Status: {response['ResponseMetadata']['HTTPStatusCode']}")
# Output: 200

# 2. Verify item exists
response = table.get_item(Key={'ticker': 'NVDA19'})
print(response.get('Item'))
# Output: None (no item!)

# 3. Check for conditional write
response = table.put_item(
    Item={'ticker': 'NVDA19', 'data': {...}},
    ConditionExpression='attribute_not_exists(ticker)'  # ← Condition failed?
)
```

**Root Cause:** Conditional expression failed silently.

**Fix:**

```python
# Before:
response = table.put_item(Item=item)  # ❌ No verification

# After:
try:
    response = table.put_item(Item=item)

    # Verify write
    verify = table.get_item(Key={'ticker': item['ticker']})
    if 'Item' not in verify:
        logger.error(f"Item not found after put_item: {item['ticker']}")
        raise ValueError("DynamoDB write verification failed")

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        logger.warning(f"Conditional write failed: {item['ticker']}")
    else:
        logger.error(f"DynamoDB error: {e}")
        raise
```

---

## AWS Boundary Verification

**When to apply**: Distributed system errors (Lambda, Aurora, S3, SQS, Step Functions)

**Problem**: Code looks correct locally but fails in AWS due to unverified execution boundaries

**Common boundary-related error patterns**:

### Pattern 1: Missing Environment Variable
```bash
# Error: KeyError: 'AURORA_HOST'
# Symptom: Lambda invocation fails immediately

# Root cause: Boundary violation (code → runtime)
# Code expects: os.environ['AURORA_HOST']
# Runtime provides: No such variable

# Verification:
aws lambda get-function-configuration \
  --function-name [PROJECT_NAME]-worker-dev \
  --query 'Environment.Variables'

# Compare with: Code's os.environ accesses
grep "os.environ" src/lambda_handler.py
```

### Pattern 2: Aurora Schema Mismatch
```bash
# Error: Unknown column 'pdf_s3_key' in 'field list'
# Symptom: INSERT query fails in production

# Root cause: Boundary violation (code → database)
# Code sends: INSERT INTO reports (symbol, pdf_s3_key)
# Aurora has: No pdf_s3_key column

# Verification:
mysql> SHOW COLUMNS FROM precomputed_reports;

# Compare with: Code's INSERT statements
grep "INSERT INTO" src/data/aurora/precompute_service.py
```

### Pattern 3: Lambda Timeout
```bash
# Error: Task timed out after 30.00 seconds
# Symptom: Lambda stops mid-execution

# Root cause: Configuration mismatch (code requirements vs entity config)
# Code requires: 60s API call + 45s processing = 105s total
# Lambda configured: 30s timeout

# Verification:
aws lambda get-function-configuration \
  --function-name [PROJECT_NAME]-worker-dev \
  --query '{Timeout:Timeout, Memory:MemorySize}'

# Analyze code execution time:
grep "requests.get.*timeout" src/ -r  # External API timeouts
# Sum: timeout values + processing overhead
```

### Pattern 4: Permission Denied
```bash
# Error: AccessDeniedException: User is not authorized to perform: s3:PutObject
# Symptom: S3 upload fails

# Root cause: Permission boundary violation (principal → resource)
# Code tries: s3.put_object(Bucket='reports', Key='file.pdf')
# IAM role allows: Only s3:GetObject (read-only)

# Verification:
aws iam get-role-policy \
  --role-name [PROJECT_NAME]-worker-role-dev \
  --policy-name S3Access

# Compare with: Code's boto3 operations
grep "s3.*put_object\|s3.*upload" src/ -r
```

### Pattern 5: Intention Violation
```bash
# Error: API Gateway timeout after 30 seconds
# Symptom: Client sees timeout, Lambda still processing

# Root cause: Usage doesn't match intention (sync Lambda used for async work)
# Entity designed for: Synchronous API (< 30s response)
# Code uses it for: Long-running report generation (60s)

# Verification:
# Check Terraform comments
cat terraform/lambdas.tf | grep -B 5 -A 10 "api-handler"

# Check Lambda invocation type
aws lambda get-function-configuration \
  --function-name api-handler \
  --query 'Timeout'
# Compare: API Gateway 30s limit vs Lambda timeout
```

**Boundary verification workflow for AWS errors**:

```
1. Identify error type → Map to boundary category
   - Missing env var → Process boundary (code → runtime)
   - Schema mismatch → Data boundary (code → database)
   - Timeout → Configuration boundary (requirements → entity config)
   - Permission denied → Permission boundary (principal → resource)
   - API Gateway timeout → Intention boundary (usage → design)

2. Identify physical entities involved
   - WHICH Lambda (name, ARN)
   - WHICH Aurora cluster (endpoint, database)
   - WHICH S3 bucket (name, region)
   - WHICH IAM role (name, policies)

3. Verify contract at boundary
   - Code expectations → Infrastructure reality
   - Use aws cli to inspect actual configuration
   - Compare code requirements vs entity properties

4. Apply Progressive Evidence Strengthening
   - Layer 1 (Surface): Error message
   - Layer 2 (Content): CloudWatch logs
   - Layer 3 (Observability): AWS resource configuration
   - Layer 4 (Ground Truth): Test actual execution
```

**Integration with investigation workflow**:
- **Step 1 (Identify Error Layer)**: Check if error is boundary-related
- **Step 2 (Collect Context)**: Identify which boundary violated
- **Step 3 (Check Changes)**: Did code or infrastructure change?
- **Step 4 (Fix)**: Repair boundary contract (update code or infrastructure)

**See**: [Execution Boundary Checklist](../../checklists/execution-boundaries.md) for systematic AWS boundary verification

**Related**:
- Principle #20 (Execution Boundary Discipline) - CLAUDE.md
- Principle #2 (Progressive Evidence Strengthening) - Multi-layer verification
- Principle #15 (Infrastructure-Application Contract) - Sync code and infra

---

## Investigation Workflow

### Step 1: Identify Error Layer (5 minutes)

```bash
# Check all three layers
aws lambda invoke --function-name worker --payload '{}' /tmp/response.json

# Layer 1: Exit code
echo "Exit code: $?"

# Layer 2: Response payload
cat /tmp/response.json | jq .

# Layer 3: CloudWatch logs
aws logs tail /aws/lambda/worker --since 5m --filter-pattern "ERROR"
```

**Questions:**
- Which layer shows the error?
- If Layer 1 OK but Layer 3 ERROR → Silent failure
- If all layers OK but wrong result → Logic error

### Step 2: Collect Error Context (10 minutes)

```bash
# Get full error details
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 3600))000 \
  --filter-pattern "ERROR" \
  --query 'events[*].[timestamp,message]' \
  --output table

# Get surrounding context (±5 lines)
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --filter-pattern "ERROR" \
  | jq -r '.events[0].message' \
  | grep -C 5 "ERROR"
```

### Step 3: Check Recent Changes (5 minutes)

```bash
# When did errors start?
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --filter-pattern "ERROR" \
  --query 'events[0].timestamp' \
  --output text

# What deployed around that time?
gh run list --limit 10

# What changed in code?
git log --since="2 hours ago" --oneline
```

### Step 4: Reproduce and Fix (variable)

See [AWS-DIAGNOSTICS.md](AWS-DIAGNOSTICS.md) for service-specific diagnostic patterns.

---

## Quick Reference

### Investigation Priority

1. **Check CloudWatch logs** (Layer 3 - strongest signal)
2. **Check response payload** (Layer 2 - structured errors)
3. **Check status code** (Layer 1 - weakest signal)
4. **Verify actual outcome** (database state, S3 files, etc.)

### Common Failure Modes

| Symptom | Likely Cause | Investigation |
|---------|--------------|---------------|
| **200 OK but errors in logs** | Silent failure | Check rowcount, verify writes |
| **INFO logs not showing** | Root logger level = WARNING | Set root logger to INFO |
| **Timeout** | Cold start, external API slow | Check duration metrics |
| **Permission denied** | IAM policy missing | Simulate permissions |
| **0 rows affected** | FK constraint, ENUM mismatch | Check constraints |

---

## File Organization

```
.claude/skills/error-investigation/
├── SKILL.md              # This file (entry point)
├── AWS-DIAGNOSTICS.md    # AWS-specific diagnostic patterns
└── LAMBDA-LOGGING.md     # Lambda logging configuration guide
```

---

## Next Steps

- **For AWS diagnostics**: See [AWS-DIAGNOSTICS.md](AWS-DIAGNOSTICS.md)
- **For Lambda logging**: See [LAMBDA-LOGGING.md](LAMBDA-LOGGING.md)
- **For general debugging**: See research skill

---

## References

- [AWS Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [AWS SDK Error Handling](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html)
