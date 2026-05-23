---
name: discover-cloud
description: Automatically discover cloud computing and serverless skills when working with cloud. Activates for cloud development tasks.
---

# Cloud Skills Discovery

Provides automatic access to comprehensive cloud skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- cloud
- Modal
- serverless
- functions
- AWS
- GCP
- Azure
- deployment

## Available Skills

### Quick Reference

The Cloud category contains 13 skills:

**AWS Skills (7)**:
1. **aws-lambda-functions** - Lambda function development, triggers, optimization
2. **aws-api-gateway** - REST/HTTP/WebSocket APIs, authorization, integrations
3. **aws-databases** - RDS, DynamoDB, ElastiCache, Aurora
4. **aws-iam-security** - IAM, Cognito, Secrets Manager, KMS
5. **aws-storage** - S3, EBS, EFS, Glacier, lifecycle policies
6. **aws-ec2-compute** - EC2, Auto Scaling, Load Balancing, AMIs
7. **aws-networking** - VPC, security groups, Route53, CloudFront

**GCP Skills (6)**:
1. **gcp-serverless** - Cloud Functions, Cloud Run, App Engine
2. **gcp-compute** - Compute Engine, GKE, autoscaling
3. **gcp-databases** - Cloud SQL, Firestore, Bigtable, Spanner
4. **gcp-storage** - Cloud Storage, Persistent Disk, Filestore
5. **gcp-iam-security** - IAM, service accounts, Secret Manager, KMS
6. **gcp-networking** - VPC, firewall, Cloud DNS, Cloud CDN

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/cloud/INDEX.md
```

This loads the full Cloud category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
# AWS Skills
cat ~/.claude/skills/cloud/aws/aws-lambda-functions.md
cat ~/.claude/skills/cloud/aws/aws-api-gateway.md
cat ~/.claude/skills/cloud/aws/aws-databases.md
cat ~/.claude/skills/cloud/aws/aws-iam-security.md
cat ~/.claude/skills/cloud/aws/aws-storage.md
cat ~/.claude/skills/cloud/aws/aws-ec2-compute.md
cat ~/.claude/skills/cloud/aws/aws-networking.md

# GCP Skills
cat ~/.claude/skills/cloud/gcp/gcp-serverless.md
cat ~/.claude/skills/cloud/gcp/gcp-compute.md
cat ~/.claude/skills/cloud/gcp/gcp-databases.md
cat ~/.claude/skills/cloud/gcp/gcp-storage.md
cat ~/.claude/skills/cloud/gcp/gcp-iam-security.md
cat ~/.claude/skills/cloud/gcp/gcp-networking.md
```

## Progressive Loading

This gateway skill enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md for full overview
- **Level 3**: Load specific skills as needed

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects cloud work
2. **Browse skills**: Run `cat ~/.claude/skills/cloud/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills

---

**Next Steps**: Run `cat ~/.claude/skills/cloud/INDEX.md` to see full category details.
