---
name: af-provision-infrastructure
description: Provision AWS infrastructure and manage cloud credentials for projects. Use when working with Route53, CloudFront, S3 buckets, DNS/domains, or Doppler secrets management.

title: Environment & Infrastructure Skill
created: 2026-01-03
updated: 2026-01-03
last_checked: 2026-01-03
tags: [skill, expertise, infrastructure, aws, dns, credentials, doppler]
parent: ../README.md
---

# Environment & Infrastructure

Directive knowledge for AWS infrastructure, credentials, DNS, and Doppler operations across GainInsight projects.

## When to Use This Skill

Load this skill when you need to:
- Access AWS credentials or assume roles
- Create/modify DNS records or subdomains
- Set up CloudFront distributions or S3 buckets
- Configure Doppler secrets
- Work with Route53 hosted zones
- Understand cross-account credential patterns

---

## Quick Reference

### Domain Admin Credentials

| Item | Location |
|------|----------|
| Doppler project/config | `gi` / `prd` |
| Access key variable | `DOMAIN_ADMIN_AWS_ACCESS_KEY_ID` |
| Secret key variable | `DOMAIN_ADMIN_AWS_SECRET_ACCESS_KEY` |
| Parent zone (gaininsight.global) | `Z08261483JJZ016GFVDDQ` |

**Usage pattern:**
```bash
doppler run --project gi --config prd -- bash -c '
  AWS_ACCESS_KEY_ID=$DOMAIN_ADMIN_AWS_ACCESS_KEY_ID \
  AWS_SECRET_ACCESS_KEY=$DOMAIN_ADMIN_AWS_SECRET_ACCESS_KEY \
  AWS_DEFAULT_REGION=eu-west-2 \
  aws route53 <command>'
```

### Project Registry

| Item | Location |
|------|----------|
| Registry | `project-registry` CLI |
| Query command | `project-registry <project> [field]` |
| Update command | `project-registry set <project> <field> <value>` |

```bash
project-registry juncan aws        # Show AWS accounts
project-registry list              # All project keys
project-registry find-by-team JKN  # Find project by Linear team key
```

### Doppler Config Mapping

| Environment | Doppler Config | Typical Use |
|-------------|----------------|-------------|
| Development | `dev` | Local development, sandboxes |
| Staging/Test | `stg` | Test environment, CI/CD |
| Production | `prd` | Production environment |

---

## Rules

### Credential Rules (MUST)

1. **MUST use Doppler for all secrets.** No `.env` files, no hardcoded credentials.

2. **MUST use domain admin credentials for Route53 changes.** Project-level IAM users typically lack Route53 permissions.

3. **MUST assume OrganizationAccountAccessRole for cross-account admin operations** when project IAM user lacks permissions:
   ```bash
   CREDS=$(doppler run --project gi --config prd -- aws sts assume-role \
     --role-arn arn:aws:iam::{account-id}:role/OrganizationAccountAccessRole \
     --role-session-name admin-operation --output json)
   ```

4. **MUST store new credentials in Doppler immediately** after creation. Never leave credentials in terminal history or temp files.

### DNS Rules (MUST)

5. **MUST create subdomain hosted zones** for new projects, not records in parent zone.

6. **MUST add NS delegation records** from parent zone to subdomain zone after creation.

7. **MUST use ACM certificates in us-east-1** for CloudFront custom domains (CloudFront requirement).

### Infrastructure Rules (SHOULD)

8. **SHOULD check project registry** before creating new resources - the account/config mapping may already exist.

9. **SHOULD use CloudFront for public S3 content** with custom domains (not S3 website URLs).

10. **SHOULD prefer S3 website endpoint as custom origin** over OAC when bucket is already public (simpler, no policy changes needed).

---

## Workflows

### Workflow: Add Custom Subdomain with CloudFront

**When:** You need `something.project.gaininsight.global` pointing to an S3 bucket or other origin.

**Steps:**

1. **Request ACM certificate in us-east-1:**
   ```bash
   doppler run --project {project} --config stg -- aws acm request-certificate \
     --domain-name {subdomain}.{project}.gaininsight.global \
     --validation-method DNS \
     --region us-east-1
   ```

2. **Get validation CNAME from certificate:**
   ```bash
   doppler run --project {project} --config stg -- aws acm describe-certificate \
     --certificate-arn {arn} --region us-east-1 \
     --query "Certificate.DomainValidationOptions[0].ResourceRecord"
   ```

3. **Add validation record using domain admin credentials:**
   ```bash
   doppler run --project gi --config prd -- bash -c '
     AWS_ACCESS_KEY_ID=$DOMAIN_ADMIN_AWS_ACCESS_KEY_ID \
     AWS_SECRET_ACCESS_KEY=$DOMAIN_ADMIN_AWS_SECRET_ACCESS_KEY \
     aws route53 change-resource-record-sets \
       --hosted-zone-id {project-zone-id} \
       --change-batch '"'"'{"Changes":[{"Action":"CREATE","ResourceRecordSet":{...}}]}'"'"''
   ```

4. **Wait for certificate validation** (2-5 minutes)

5. **Create CloudFront distribution** with certificate and custom domain alias

6. **Add CNAME record** pointing subdomain to CloudFront domain

### Workflow: Create New Project Subdomain Zone

**When:** Setting up a new project that needs `*.project.gaininsight.global`

**Steps:**

1. **Create hosted zone:**
   ```bash
   doppler run --project gi --config prd -- bash -c '
     AWS_ACCESS_KEY_ID=$DOMAIN_ADMIN_AWS_ACCESS_KEY_ID \
     AWS_SECRET_ACCESS_KEY=$DOMAIN_ADMIN_AWS_SECRET_ACCESS_KEY \
     aws route53 create-hosted-zone \
       --name {project}.gaininsight.global \
       --caller-reference "{project}-$(date +%s)"'
   ```

2. **Note the 4 nameservers** from the response

3. **Add NS delegation to parent zone (Z08261483JJZ016GFVDDQ):**
   ```bash
   # Add NS record with the 4 nameservers
   ```

4. **Store zone ID** in project documentation (CLAUDE.md)

### Workflow: Access Another Account's Resources

**When:** You need admin access that the project IAM user doesn't have.

**Steps:**

1. **Assume OrganizationAccountAccessRole:**
   ```bash
   CREDS=$(doppler run --project gi --config prd -- aws sts assume-role \
     --role-arn arn:aws:iam::{account-id}:role/OrganizationAccountAccessRole \
     --role-session-name {operation-name} --output json)

   export AWS_ACCESS_KEY_ID=$(echo $CREDS | jq -r '.Credentials.AccessKeyId')
   export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | jq -r '.Credentials.SecretAccessKey')
   export AWS_SESSION_TOKEN=$(echo $CREDS | jq -r '.Credentials.SessionToken')
   ```

2. **Run commands** with elevated permissions

3. **Unset credentials** when done:
   ```bash
   unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
   ```

---

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| "AccessDenied" on Route53 | Using project IAM user | Use domain admin credentials |
| "AccessDenied" on bucket policy | Project user lacks s3:PutBucketPolicy | Assume OrganizationAccountAccessRole |
| ACM cert stuck pending | Validation record not added | Add CNAME to correct hosted zone |
| CloudFront 403 errors | S3 bucket policy missing | Add CloudFront service principal or use website endpoint |
| "Certificate not in us-east-1" | ACM cert in wrong region | Request new cert in us-east-1 |

---

## Essential Reading

### Procedural Guides

| Guide | Purpose |
|-------|---------|
| [Layer 1: Infrastructure](../../docs/guides/gaininsight-standard/layer-1-infrastructure.md) | Complete AWS setup walkthrough |
| [GiDev Server Docs](/srv/docs/) | Server-specific operations |

### Key Files

| File | Contains |
|------|----------|
| `project-registry` CLI | All project AWS accounts, Doppler configs |
| `/srv/docs/CREDENTIALS.md` | Credential management patterns |
| `/srv/docs/ADMIN.md` | Server administration including Cloudflare |

---

**Remember:**
1. Domain admin creds are in `gi/prd` Doppler
2. ACM certs for CloudFront must be in us-east-1
3. Check project registry before creating resources
4. Use OrganizationAccountAccessRole for admin operations
