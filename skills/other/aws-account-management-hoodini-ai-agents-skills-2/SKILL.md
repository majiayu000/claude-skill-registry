---
name: aws-account-management
description: Manage AWS accounts, organizations, IAM, and billing. Use when setting up AWS Organizations, managing IAM policies, controlling costs, or implementing multi-account strategies. Triggers on AWS Organizations, AWS IAM, AWS billing, Cost Explorer, SCPs, multi-account, AWS SSO, Identity Center.
---

# AWS Account Management

Manage AWS accounts, organizations, IAM, and billing effectively.

## AWS Organizations

### Organization Structure
```
Root
├── Production OU
│   ├── Prod Account A
│   └── Prod Account B
├── Development OU
│   ├── Dev Account
│   └── Staging Account
├── Security OU
│   ├── Security Account
│   └── Log Archive Account
└── Sandbox OU
    └── Sandbox Account
```

### Create Organization
```bash
# Create organization (from management account)
aws organizations create-organization --feature-set ALL

# Create organizational unit
aws organizations create-organizational-unit \
  --parent-id r-xxxx \
  --name "Production"

# Create member account
aws organizations create-account \
  --email prod-aws@company.com \
  --account-name "Production Account"

# Move account to OU
aws organizations move-account \
  --account-id 123456789012 \
  --source-parent-id r-xxxx \
  --destination-parent-id ou-xxxx-xxxxxxxx
```

### Service Control Policies (SCPs)

```json
// Deny leaving organization
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyLeaveOrg",
      "Effect": "Deny",
      "Action": "organizations:LeaveOrganization",
      "Resource": "*"
    }
  ]
}

// Require IMDSv2 (instance metadata)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireIMDSv2",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringNotEquals": {
          "ec2:MetadataHttpTokens": "required"
        }
      }
    }
  ]
}

// Region restriction
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "organizations:*",
        "support:*",
        "budgets:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2", "eu-west-1"]
        }
      }
    }
  ]
}

// Prevent root user access
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootUser",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:root"
        }
      }
    }
  ]
}
```

### Attach SCP
```bash
# Create SCP
aws organizations create-policy \
  --name "DenyLeaveOrg" \
  --type SERVICE_CONTROL_POLICY \
  --content file://deny-leave-org.json

# Attach to OU
aws organizations attach-policy \
  --policy-id p-xxxxxxxxxxxx \
  --target-id ou-xxxx-xxxxxxxx
```

## IAM Identity Center (AWS SSO)

### Setup Identity Center
```bash
# Enable Identity Center
aws sso-admin create-instance

# Create permission set
aws sso-admin create-permission-set \
  --instance-arn arn:aws:sso:::instance/ssoins-xxxxxxxx \
  --name "AdministratorAccess" \
  --session-duration "PT8H"

# Attach managed policy
aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn arn:aws:sso:::instance/ssoins-xxxxxxxx \
  --permission-set-arn arn:aws:sso:::permissionSet/ssoins-xxxxxxxx/ps-xxxxxxxx \
  --managed-policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### Permission Sets
```json
// Developer permission set (inline policy)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DeveloperAccess",
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "s3:*",
        "lambda:*",
        "dynamodb:*",
        "cloudwatch:*",
        "logs:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyBillingAndIAM",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:DeleteUser",
        "iam:CreateAccessKey",
        "aws-portal:*",
        "budgets:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## IAM Best Practices

### IAM Policies

```json
// Least privilege policy example
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "private"
        }
      }
    },
    {
      "Sid": "AllowListBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-bucket",
      "Condition": {
        "StringLike": {
          "s3:prefix": ["${aws:username}/*"]
        }
      }
    }
  ]
}

// Cross-account role trust policy
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "unique-external-id"
        },
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

### IAM Roles for Services
```json
// Lambda execution role
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

// EC2 instance profile
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### IAM Security Tools
```bash
# Generate credential report
aws iam generate-credential-report
aws iam get-credential-report --output text --query Content | base64 -d

# List unused access keys (last used > 90 days)
aws iam list-users --query 'Users[*].UserName' --output text | \
  xargs -I {} aws iam list-access-keys --user-name {} \
    --query 'AccessKeyMetadata[?Status==`Active`]'

# Get access key last used
aws iam get-access-key-last-used --access-key-id AKIAXXXXXXXX

# IAM Access Analyzer
aws accessanalyzer create-analyzer \
  --analyzer-name my-analyzer \
  --type ACCOUNT
```

## Cost Management

### AWS Budgets
```bash
# Create budget
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "Monthly-Budget",
    "BudgetLimit": {
      "Amount": "1000",
      "Unit": "USD"
    },
    "BudgetType": "COST",
    "TimeUnit": "MONTHLY"
  }' \
  --notifications-with-subscribers '[
    {
      "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 80
      },
      "Subscribers": [
        {
          "SubscriptionType": "EMAIL",
          "Address": "alerts@company.com"
        }
      ]
    }
  ]'
```

### Cost Explorer API
```python
import boto3
from datetime import datetime, timedelta

client = boto3.client('ce')

# Get cost and usage
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'End': datetime.now().strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {'Type': 'DIMENSION', 'Key': 'SERVICE'},
        {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}
    ]
)

# Get cost forecast
forecast = client.get_cost_forecast(
    TimePeriod={
        'Start': datetime.now().strftime('%Y-%m-%d'),
        'End': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    },
    Metric='UNBLENDED_COST',
    Granularity='MONTHLY'
)

print(f"Forecasted cost: ${forecast['Total']['Amount']}")
```

### Cost Allocation Tags
```bash
# Activate cost allocation tags
aws ce update-cost-allocation-tags-status \
  --cost-allocation-tags-status '[
    {"TagKey": "Environment", "Status": "Active"},
    {"TagKey": "Project", "Status": "Active"},
    {"TagKey": "CostCenter", "Status": "Active"}
  ]'

# Tag resources consistently
aws ec2 create-tags \
  --resources i-1234567890abcdef0 \
  --tags Key=Environment,Value=Production \
         Key=Project,Value=WebApp \
         Key=CostCenter,Value=Engineering
```

### Savings Plans & Reserved Instances
```bash
# Get Savings Plans recommendations
aws savingsplans describe-savings-plans-offering-rates \
  --savings-plan-offering-ids xxxxxxxxx

# Get Reserved Instance recommendations
aws ce get-reservation-purchase-recommendation \
  --service "Amazon Elastic Compute Cloud - Compute" \
  --lookback-period-in-days THIRTY_DAYS \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT
```

## CloudTrail & Logging

### Organization Trail
```bash
# Create organization trail
aws cloudtrail create-trail \
  --name organization-trail \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-organization-trail \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --kms-key-id alias/cloudtrail-key

# Start logging
aws cloudtrail start-logging --name organization-trail
```

### CloudTrail Event Selectors
```bash
# Log management events and S3 data events
aws cloudtrail put-event-selectors \
  --trail-name organization-trail \
  --event-selectors '[
    {
      "ReadWriteType": "All",
      "IncludeManagementEvents": true,
      "DataResources": [
        {
          "Type": "AWS::S3::Object",
          "Values": ["arn:aws:s3:::sensitive-bucket/"]
        }
      ]
    }
  ]'
```

## Config & Compliance

### AWS Config Rules
```bash
# Enable Config
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/config-role

# Deploy managed rule
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-bucket-public-read-prohibited",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"
    }
  }'

# Organization Config rules
aws configservice put-organization-config-rule \
  --organization-config-rule-name "org-s3-bucket-public-read-prohibited" \
  --organization-managed-rule-metadata '{
    "RuleIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }'
```

### Conformance Packs
```yaml
# conformance-pack.yaml
Parameters:
  S3BucketName:
    Type: String
Resources:
  S3BucketPublicReadProhibited:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
  IAMRootAccessKeyCheck:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: iam-root-access-key-check
      Source:
        Owner: AWS
        SourceIdentifier: IAM_ROOT_ACCESS_KEY_CHECK
  MFAEnabledForIAMConsoleAccess:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: mfa-enabled-for-iam-console-access
      Source:
        Owner: AWS
        SourceIdentifier: MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS
```

## Terraform Multi-Account

```hcl
# providers.tf
provider "aws" {
  alias  = "management"
  region = "us-east-1"
}

provider "aws" {
  alias  = "production"
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::${var.prod_account_id}:role/TerraformRole"
  }
}

provider "aws" {
  alias  = "development"
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::${var.dev_account_id}:role/TerraformRole"
  }
}

# Create resources in specific accounts
resource "aws_s3_bucket" "prod_bucket" {
  provider = aws.production
  bucket   = "my-prod-bucket"
}

resource "aws_s3_bucket" "dev_bucket" {
  provider = aws.development
  bucket   = "my-dev-bucket"
}
```

### Account Factory (Control Tower Pattern)
```hcl
# modules/account/main.tf
resource "aws_organizations_account" "account" {
  name  = var.account_name
  email = var.account_email
  
  parent_id = var.organizational_unit_id
  
  role_name = "OrganizationAccountAccessRole"
  
  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role" "terraform_role" {
  provider = aws.new_account
  name     = "TerraformRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.management_account_id}:root"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
```

## Security Best Practices Checklist

```markdown
## Account Security
- [ ] MFA enabled on root account
- [ ] Root account access keys deleted
- [ ] Root account email is distribution list
- [ ] Strong password policy configured
- [ ] CloudTrail enabled in all regions
- [ ] GuardDuty enabled
- [ ] Security Hub enabled
- [ ] Config enabled with rules

## Organization Security
- [ ] SCPs restrict dangerous actions
- [ ] SCPs enforce region restrictions
- [ ] SCPs require encryption
- [ ] Log archive account isolated
- [ ] Security account isolated
- [ ] Cross-account access uses roles (not users)

## IAM Security
- [ ] No long-lived access keys
- [ ] IAM Access Analyzer enabled
- [ ] Unused credentials rotated/removed
- [ ] Permission boundaries on delegated admins
- [ ] Service-linked roles used where possible

## Cost Management
- [ ] Budgets configured with alerts
- [ ] Cost allocation tags active
- [ ] Savings Plans evaluated
- [ ] Unused resources cleaned up
- [ ] Right-sizing recommendations reviewed
```

## Resources

- **Organizations Docs**: https://docs.aws.amazon.com/organizations/
- **IAM Best Practices**: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- **Identity Center**: https://docs.aws.amazon.com/singlesignon/
- **Cost Management**: https://docs.aws.amazon.com/cost-management/
- **Control Tower**: https://docs.aws.amazon.com/controltower/
- **Security Hub**: https://docs.aws.amazon.com/securityhub/
