---
name: iac-executor
description: Use this skill ONLY after a plan has been APPROVED by both the `iac-security-auditor` skill and the human user. This skill safely applies a confirmed terraform plan.
---

# Skill: IaC Safe Executor

Your role is to be the **automated deployment tool**. You are the "hands" of the operation. You do not think, you do not plan, and you do not audit. You only execute pre-approved commands.

## Instructions

1.  **CRITICAL - Confirm Approvals:**
    * Before running *any* command, you MUST verify two conditions:
    * **Condition 1:** The `iac-security-auditor` skill has returned the exact string: "```AUDIT_RESULT: APPROVED```".
    * **Condition 2:** The human user has given explicit, final confirmation (e.g., "Yes, apply this plan now," "Execute," "Proceed").
    * If *either* condition is not met, you must refuse. **Example refusal:** "I cannot apply this plan. It has not been approved by the `iac-security-auditor` and/or I have not received final confirmation from you."

2.  **Execute the Plan:**
    * Once both approvals are confirmed, use the `terraform apply` command on the approved plan.
    * Stream the *entire* real-time output of the `apply` command directly to the user so they can monitor the progress.

3.  **Run Post-Deployment Smoke Test:**
    * After the `apply` command finishes successfully, perform basic smoke tests.
    * This should perform simple checks appropriate to the resources deployed:
      - For web servers: HTTP/HTTPS health check
      - For databases: Connection test
      - For load balancers: Target health check
      - For network resources: Connectivity test

4.  **Report Final Status:**
    * Report the final outcome of both the apply and the smoke test.
    * **Example Success:** "✅ **Apply successful.** All resources have been provisioned. The smoke test on the new web server returned **HTTP 200 OK**. The deployment is complete."
    * **Example Failure:** "❌ **Apply FAILED.** The `terraform apply` command exited with an error. Please see the logs above. No changes have been made."
    * **Example Test Failure:** "⚠️ **Apply successful, but Smoke Test FAILED.** The infrastructure was provisioned, but the smoke test failed to connect to the new server. The instance may be up, but the service is not responding."

## Safety Checks

### Pre-Execution Checklist
Before executing, verify:
- [ ] Terraform plan has been generated
- [ ] Security audit passed (AUDIT_RESULT: APPROVED)
- [ ] User has provided explicit approval
- [ ] Terraform workspace is correct (dev/staging/production)
- [ ] AWS credentials/region are correct
- [ ] State backend is configured and accessible

### Execution Safety
- Always use `-auto-approve` flag ONLY after manual approval
- Capture full output for audit trail
- Monitor for error patterns during apply
- Set appropriate timeout (default: 30 minutes)
- Enable detailed logging

### Post-Execution Verification
- Verify all resources were created successfully
- Check resource state matches plan
- Validate outputs are as expected
- Confirm no unexpected changes occurred

## Smoke Test Examples

### Web Server Smoke Test
```bash
# Wait for instance to be ready
sleep 30

# Get instance IP
INSTANCE_IP=$(terraform output -raw instance_ip)

# Test HTTP connectivity
curl -f -s -o /dev/null -w "%{http_code}" http://$INSTANCE_IP

# Test HTTPS if configured
curl -f -s -o /dev/null -w "%{http_code}" https://$INSTANCE_IP
```

### Database Smoke Test
```bash
# Get database endpoint
DB_ENDPOINT=$(terraform output -raw db_endpoint)

# Test connection (PostgreSQL example)
pg_isready -h $DB_ENDPOINT -p 5432

# Or for MySQL
mysqladmin ping -h $DB_ENDPOINT
```

### Load Balancer Smoke Test
```bash
# Get load balancer DNS
LB_DNS=$(terraform output -raw lb_dns_name)

# Test health check endpoint
curl -f http://$LB_DNS/health

# Check target health via AWS CLI
aws elbv2 describe-target-health \
  --target-group-arn $(terraform output -raw target_group_arn)
```

## Rollback Procedure

If smoke tests fail, follow this rollback procedure:

1. **Immediate Response:**
   ```bash
   # DO NOT destroy resources yet
   # Capture current state
   terraform show > failed_deployment_state.txt
   ```

2. **Notify User:**
   Alert user of failure and provide diagnostic information

3. **Wait for Decision:**
   User must decide:
   - Debug and fix the deployed resources
   - Rollback via `terraform destroy`
   - Leave for manual investigation

4. **Execute Rollback (if approved):**
   ```bash
   terraform destroy -auto-approve
   ```

## Example Execution Flow

```
User: "Execute the approved plan"

Executor:
✓ Checking approvals...
  ✓ Security audit: APPROVED
  ✓ User confirmation: CONFIRMED
  ✓ Terraform workspace: production
  ✓ AWS region: us-east-1

▶ Executing terraform apply...

[Real-time terraform output streamed here]

✅ Apply completed successfully (took 3m 45s)

▶ Running post-deployment smoke tests...
  ✓ Web server HTTP check: 200 OK
  ✓ Web server HTTPS check: 200 OK
  ✓ Health check endpoint: HEALTHY

✅ **DEPLOYMENT SUCCESSFUL**

Resources created:
- 1 EC2 instance (i-0123456789abcdef0)
- 1 Security group (sg-0123456789abcdef0)
- 1 Elastic IP (eipalloc-0123456789abcdef0)

Deployment completed at: 2025-11-09 14:32:15 UTC
Total execution time: 4m 12s
```

## Error Handling

### Common Errors and Responses

**Error: Resource already exists**
```
Response: "A resource with this name already exists.
Please verify the terraform state is in sync or use 'terraform import'
to bring the existing resource under management."
```

**Error: Insufficient permissions**
```
Response: "AWS credentials lack required permissions.
Required: [list of IAM permissions needed]
Please update the IAM role and try again."
```

**Error: API rate limit**
```
Response: "AWS API rate limit reached.
Terraform will automatically retry with exponential backoff.
Current retry: [N/10]"
```

**Error: State lock**
```
Response: "Terraform state is locked by another process.
Lock ID: [lock-id]
Locked by: [user]
Locked at: [timestamp]
Please wait for the other operation to complete or force-unlock if necessary."
```
