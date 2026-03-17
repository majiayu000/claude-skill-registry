---
name: tf-plan-review
description: >
  Analyze Terraform plans for risk before you apply. Classifies every change
  as safe, moderate, dangerous, or critical. Detects destroys, IAM changes,
  data-loss risks, and blast radius. Entirely read-only — never runs apply.
version: 0.1.2
author: Anvil AI
tags: [terraform, opentofu, iac, infrastructure, devops, risk-assessment, plan-review, security, discord, discord-v2]
---

# Terraform Plan Analyzer & Risk Assessor

Analyze `terraform plan` output and produce an AI-powered risk assessment of every infrastructure change — before you press apply.

**This skill is STRICTLY READ-ONLY.** It runs `terraform plan` and `terraform validate` to analyze changes, but it **NEVER** runs `terraform apply`, `terraform destroy`, `terraform import`, `terraform taint`, or any command that modifies infrastructure or state.

## Activation

This skill activates when the user mentions:
- "terraform plan", "tf plan", "review plan", "plan review"
- "is this plan safe", "safe to apply", "risk assessment"
- "what will be destroyed", "what changes", "terraform changes"
- "terraform state", "state drift", "drift detection"
- "terraform validate", "validate config", "tf validate"
- "IAM changes", "security group changes", "infrastructure changes"
- "blast radius", "cascade effects", "dependencies"
- "tofu plan", "opentofu" (same workflow, different binary)

## Example Prompts

1. "Review this terraform plan before I apply"
2. "What will be destroyed in this plan?"
3. "Is this plan safe to apply?"
4. "Show me the state drift"
5. "What IAM changes are in this plan?"
6. "Validate my terraform config in ~/infra/prod"
7. "Run a risk assessment on the terraform plan in /deployments/staging"
8. "What's the blast radius if I apply this plan?"

## Permissions

```yaml
permissions:
  exec: true          # Required to run terraform/tofu CLI
  read: true          # Read .tf files and plan output
  write: false        # NEVER writes — strictly read-only analysis
  network: true       # terraform plan needs provider API access
```

## Terraform Change Types — What the Agent Must Know

Understanding Terraform change types is critical for accurate risk assessment:

### Action Types (from plan JSON)

| Action | Meaning | Risk Profile |
|--------|---------|-------------|
| `create` | New resource being added | Generally safe (unless IAM/security) |
| `update` | Existing resource modified in-place | Moderate (depends on what's changing) |
| `delete` | Resource being permanently destroyed | **DANGEROUS** — data loss risk |
| `replace` (`delete` + `create`) | Resource must be destroyed and recreated | **DANGEROUS** — downtime + data loss |
| `read` | Data source being refreshed | Safe (read-only) |
| `no-op` | No changes needed | Safe |

### What Makes a Change Dangerous

**Critical (🔴 CRITICAL):**
- Any destroy/replace of: IAM roles/policies, security groups, KMS keys, secrets, databases (RDS, DynamoDB, Cloud SQL, Azure SQL), S3 buckets, DNS records, WAF rules, CloudTrail
- Any update to IAM policies, security group rules, encryption settings
- These changes can cause **data loss**, **security breaches**, or **service outages**

**Dangerous (🟠 DANGEROUS):**
- Destroy/replace of: EC2 instances, load balancers, ECS/EKS clusters, VPCs, subnets, NAT gateways, Lambda functions, API gateways
- These changes cause **downtime** and may require manual intervention to recover

**Moderate (🟡 MODERATE):**
- Updates to: autoscaling policies, monitoring/alerting rules, launch templates
- Creates of: security-sensitive resources (new IAM roles, new security groups)
- Changes that affect **capacity** or **observability** but not data integrity

**Safe (🟢 SAFE):**
- Tag-only updates
- Creating new non-sensitive resources
- No-op / read operations

### Replace is Especially Dangerous

When Terraform says it must "replace" a resource, it means:
1. **Delete** the existing resource (irreversible)
2. **Create** a new one with the new configuration

This is triggered when an immutable attribute changes (e.g., changing RDS `engine_version`, EC2 `ami`, changing a subnet's AZ). The agent should **always flag replaces prominently** because:
- The old resource (and its data) is destroyed
- There will be a gap between destroy and create (downtime)
- Dependent resources may break during the transition

## Agent Workflow

Follow this sequence exactly based on user intent:

### For Plan Analysis ("review this plan", "is it safe", "what changes")

#### Step 1: Run Plan Analysis

```bash
bash <skill_dir>/scripts/tf-plan-review.sh plan <directory>
```

If no directory specified, use the current working directory.

The script outputs:
- **stdout:** Structured JSON with all resource changes, risk classifications, and summary
- **stderr:** Beautiful Markdown risk report

#### Step 2: Interpret the JSON

Parse the JSON output. Key fields:

```json
{
  "overall_risk": "🔴 CRITICAL | 🔴 HIGH | 🟡 MODERATE | 🟢 LOW",
  "summary": {
    "create": 5,
    "update": 3,
    "destroy": 1,
    "replace": 0
  },
  "risk_breakdown": {
    "critical": 1,
    "dangerous": 0,
    "moderate": 2,
    "safe": 5
  },
  "resources": [
    {
      "address": "aws_iam_role.admin",
      "action": "delete",
      "risk": "🔴 CRITICAL"
    }
  ]
}
```

#### Step 3: Present the Risk Assessment

Show the Markdown report from stderr. Then add your own AI analysis:

1. **Lead with the overall risk level** — make it viscerally clear
2. **Highlight destroys and critical changes first** — these are what kill production
3. **Explain WHY each critical change is dangerous** in plain English
4. **Assess blast radius** — what other resources depend on the destroyed ones?
5. **Present the pre-apply checklist** — what should the human verify?
6. **Give a clear recommendation:** "Safe to apply" / "Review needed" / "DO NOT APPLY without ___"

**Tone guidance for critical plans:**
- Don't be polite about danger. If a plan destroys a production database, say so bluntly.
- "This plan will **permanently delete** your RDS instance `prod-db`. All data will be lost. Do you have a backup?"
- Make the "oh shit" moment impossible to miss.

### For State Inspection ("show me state", "what's managed", "state drift")

```bash
bash <skill_dir>/scripts/tf-plan-review.sh state "<filter>" <directory>
```

The filter is optional — it greps resource addresses. Examples:
- `bash <skill_dir>/scripts/tf-plan-review.sh state "iam" .` → all IAM resources
- `bash <skill_dir>/scripts/tf-plan-review.sh state "aws_instance" .` → all EC2 instances
- `bash <skill_dir>/scripts/tf-plan-review.sh state "" .` → all resources

### For Validation ("validate config", "check syntax")

```bash
bash <skill_dir>/scripts/tf-plan-review.sh validate <directory>
```

Reports configuration errors and warnings without running a plan.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TF_BINARY` | auto-detect | Override binary: `terraform`, `tofu`, or a path |
| `TF_PLAN_TIMEOUT` | `600` | Timeout for `terraform plan` in seconds |

The script auto-detects `terraform` first, then `tofu`. Set `TF_BINARY=tofu` to force OpenTofu.

## Error Handling

| Situation | Behavior |
|-----------|----------|
| terraform/tofu not found | JSON error with install links for both |
| jq not found | JSON error with install link |
| No .tf files in directory | JSON error: "No Terraform configuration files found" |
| Not initialized | Auto-runs `terraform init` (for plan) or `terraform init -backend=false` (for validate) |
| Plan fails (provider errors) | Extracts error from plan JSON diagnostics, reports it |
| Plan timeout | Process killed after TF_PLAN_TIMEOUT seconds |
| State not found | JSON error explaining no state exists |
| Empty state | Reports "State is empty — no managed resources" |

## Safety — CRITICAL RULES

1. **NEVER run `terraform apply`** — not even with `-auto-approve`, not even with `-target`, not even "just this one resource". NEVER.
2. **NEVER run `terraform destroy`** — not under any circumstances.
3. **NEVER run `terraform import`** — this modifies state.
4. **NEVER run `terraform taint` or `terraform untaint`** — these modify state.
5. **NEVER run `terraform state mv`, `terraform state rm`, or `terraform state push`** — these modify state.
6. **Never expose cloud credentials** — if they appear in plan output, redact them.
7. **Handle sensitive values** — Terraform marks values as `(sensitive)`. Never try to reveal them.
8. **Never cache or store plan output** — plans can contain secrets in resource attributes.
9. The ONLY terraform commands this skill runs are: `plan`, `show`, `state list`, `state show`, `validate`, `init`, `providers`.

If the user asks you to apply a plan, respond:
> "I can analyze and assess Terraform plans, but I cannot apply them. Applying infrastructure changes requires human review and explicit execution. Based on my analysis, here's what you should verify before running `terraform apply`..."

## Common Patterns & Agent Tips

### "Is this plan safe to apply?"
Run the plan analysis. If overall_risk is 🟢 LOW:
> "This plan looks safe. It creates X new resources with no destroys or security changes. The pre-apply checklist is straightforward."

If overall_risk is 🔴 CRITICAL:
> "⚠️ This plan has CRITICAL risk. [Explain specific dangers]. I strongly recommend review by another team member before applying."

### "What will be destroyed?"
Run plan, then filter for `action == "delete"` or `action == "replace"`. Present each with:
- Resource address
- Resource type
- Why it matters (is it stateful? does it have data?)
- What depends on it

### "What IAM changes are in this plan?"
Run plan, then filter resources matching IAM patterns. For each:
- What permission is changing
- Is it adding or removing access
- Is it overly permissive (e.g., `Action: *`)

### "Show me the blast radius"
Run plan, identify all destroys/replaces, then explain:
- What other resources reference the destroyed ones
- What will break when the resource is gone
- Whether Terraform will auto-fix the dependencies or if manual intervention is needed

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When the conversation is happening in a Discord channel:

- Send a compact first summary (overall risk, destroy count, critical resources), then ask if the user wants the full report.
- Keep the first response under ~1200 characters and avoid large Markdown tables in the first message.
- If Discord components are available, include quick actions:
  - `Show Critical Changes`
  - `Show Destroyed Resources`
  - `Show Pre-Apply Checklist`
- If components are not available, provide the same follow-ups as a numbered list.
- Prefer short follow-up chunks (<=15 lines per message) for large plans.

## Sensitive Data Handling

Terraform plan JSON may contain sensitive values. The script does NOT extract resource attribute values — it only extracts resource addresses, types, and actions. However, when presenting results:

- Never show attribute values marked `(sensitive)` by Terraform
- Never show provider credentials or backend configuration secrets
- If a user asks "what value is changing?", explain that you can see the change type but sensitive values are redacted by Terraform for security
- Never store or cache plan output files

## Powered by Anvil AI 🔍
