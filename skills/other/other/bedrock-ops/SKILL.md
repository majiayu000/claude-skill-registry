---
name: bedrock-ops
description: Bedrock KB + S3 data pipeline management with safety guardrails. S3 sync (with force-upload for content-only changes), KB ingestion status polling, cost monitoring. Enforces identity verification, dry-run, and confirmation for all write operations.
user-invocable: true
---

# Bedrock Ops Skill

Safely manage the RAG data pipeline: S3 uploads, Bedrock KB ingestion, session management.

## Setup

### First time per project

```bash
# 1. Generate aws-project.json (lists available profiles, generates config)
uv run python SKILLS_DIR/scripts/setup_project.py <profile-name> [s3-bucket]

# 2. Create aws-project.local.json with your TOTP secret
echo '{"totp_secret": "YOUR_BASE32_SECRET", "mfa_serial": "YOUR_MFA_ARN"}' > aws-project.local.json
```

### Verify setup

```bash
# Check session and identity
uv run --with pyotp,boto3 python SKILLS_DIR/scripts/session.py ensure
```

## Commands

All commands are handled by Claude interpreting the user's intent and routing to the appropriate script.

### Identity & Session

| Intent | Implementation |
|--------|---------------|
| `/bedrock-ops setup` | Run `uv run python SKILLS_DIR/scripts/setup_project.py` to list profiles, then generate config |
| `/bedrock-ops verify` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/session.py check` |
| `/bedrock-ops session` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/session.py ensure` |

### S3 Operations

| Intent | Implementation |
|--------|---------------|
| `/bedrock-ops s3 ls [path]` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py s3 ls s3://<bucket>/<path>` |
| `/bedrock-ops s3 sync <local> <s3>` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py s3 sync <local> <s3>` (dry-run first, add `--execute` for real) |
| `/bedrock-ops s3 force-upload <local> <s3>` | Use `aws s3 cp --recursive` instead of sync — **required when only file content changed but byte count is the same** (e.g. after adding chunk anchors). Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py s3 cp <local> s3://<bucket>/ --recursive` (dry-run first, add `--execute` for real) |
| `/bedrock-ops s3 upload <file> [s3path]` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py s3 cp <file> s3://<bucket>/<path>` |
| `/bedrock-ops s3 download <s3path> [local]` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py s3 cp s3://<bucket>/<path> <local>` |

### Cost & Resources

| Intent | Implementation |
|--------|---------------|
| `/bedrock-ops cost` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py ce get-cost-and-usage --time-period Start=$(date -v1d +%Y-%m-%d),End=$(date +%Y-%m-%d) --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE` |
| `/bedrock-ops resources ec2` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,Type:InstanceType,State:State.Name,Name:Tags[?Key==\`Name\`].Value|[0]}'` |
| `/bedrock-ops resources s3` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py s3 ls` |
| `/bedrock-ops resources lambda` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime,Memory:MemorySize}'` |

### Bedrock Knowledge Bases

| Intent | Implementation |
|--------|---------------|
| `/bedrock-ops kb list` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py bedrock-agent list-knowledge-bases` |
| `/bedrock-ops kb sync <kb-id>` | Auto-detect data source ID, then run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py bedrock-agent start-ingestion-job --knowledge-base-id <kb-id> --data-source-id <ds-id> --execute` |
| `/bedrock-ops kb status <kb-id>` | Poll ingestion job status. Run `aws bedrock-agent list-ingestion-jobs --knowledge-base-id <kb-id> --data-source-id <ds-id> --profile personal-session --region ap-northeast-1 --query 'ingestionJobSummaries[0].{status:status,started:startedAt,updated:updatedAt,stats:statistics}' --output json`. Repeat every 15 seconds until status is `COMPLETE` or `FAILED`. Print elapsed time. |

### Arbitrary Command

| Intent | Implementation |
|--------|---------------|
| `/bedrock-ops exec <args>` | Run `uv run --with pyotp,boto3 python SKILLS_DIR/scripts/aws_safe.py <args>` |

## Safety Rules (ALWAYS enforced by aws_safe.py)

1. **Identity check**: Before any write operation, `sts get-caller-identity` must match `account_id` in `aws-project.json`. Abort on mismatch.
2. **Explicit profile**: Every command uses `--profile` from config. Never rely on env vars or default.
3. **Dry-run first**: For s3 sync/cp/mv, always `--dryrun` first. Show output. User must confirm with `--execute`.
4. **No silent deletes**: `--delete` and destructive operations blocked unless `--i-understand-this-deletes` is passed.
5. **Service blocklist**: Respect `safety.denied_services` in aws-project.json (default: iam, organizations).
6. **Confirmation banner**: Before write ops, display profile, account ID, command, and mode (dry-run/live).
7. **Session auto-refresh**: If session expired, auto-regenerate using TOTP from aws-project.local.json.

## Config Files

- `aws-project.json` (project root, committed) — profile, account_id, safety rules, defaults
- `aws-project.local.json` (project root, gitignored) — totp_secret, mfa_serial, personal overrides

## Path Variables

- `SKILLS_DIR` = `.claude/skills/bedrock-ops`
