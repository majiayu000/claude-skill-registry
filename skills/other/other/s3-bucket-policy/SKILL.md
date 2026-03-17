---
name: s3-bucket-policy
description: Эксперт по S3 политикам. Используй для IAM policies, bucket permissions, cross-account access и security best practices.
---

# AWS S3 Bucket Policy Expert

Expert guidance on creating, analyzing, and optimizing AWS S3 bucket policies with focus on security, access control, and compliance.

## Policy Structure

```json
{
  "Version": "2012-10-17",
  "Id": "PolicyIdentifier",
  "Statement": [
    {
      "Sid": "StatementIdentifier",
      "Effect": "Allow | Deny",
      "Principal": {
        "AWS": "arn:aws:iam::account-id:root"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::bucket-name",
        "arn:aws:s3:::bucket-name/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
```

## Core Principles

```yaml
security_principles:
  least_privilege:
    description: "Grant only minimum necessary permissions"
    practice: "Start with deny all, add specific allows"

  explicit_deny:
    description: "Deny always overrides Allow"
    practice: "Use Deny for security guardrails"

  defense_in_depth:
    description: "Multiple layers of security"
    practice: "Combine bucket policy + IAM + ACL + encryption"

  avoid_wildcards:
    bad: '"Principal": "*"'
    better: '"Principal": {"AWS": "arn:aws:iam::123456789012:root"}'

common_mistakes:
  - "Using Principal: * without conditions"
  - "Missing resource ARN for objects (/*)"
  - "Forgetting to block public access"
  - "Not enabling versioning before policies"
```

## Common Policy Patterns

### Public Read for Static Website

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-website-bucket/*",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/public": "true"
        }
      }
    }
  ]
}
```

### Cross-Account Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CrossAccountAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::987654321098:root"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::shared-bucket",
        "arn:aws:s3:::shared-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
```

### CloudFront Origin Access Control

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontServicePrincipal",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-cdn-bucket/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::123456789012:distribution/EDFDVBD6EXAMPLE"
        }
      }
    }
  ]
}
```

### Enforce Encryption

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnencryptedUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::secure-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    },
    {
      "Sid": "DenyIncorrectKMSKey",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::secure-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption-aws-kms-key-id": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
        }
      }
    }
  ]
}
```

### IP-Based Restrictions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowFromCorporateNetwork",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::internal-bucket/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": [
            "192.0.2.0/24",
            "203.0.113.0/24"
          ]
        }
      }
    },
    {
      "Sid": "DenyFromOtherIPs",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::internal-bucket",
        "arn:aws:s3:::internal-bucket/*"
      ],
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": [
            "192.0.2.0/24",
            "203.0.113.0/24"
          ]
        }
      }
    }
  ]
}
```

### VPC Endpoint Access Only

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonVPCAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::private-bucket",
        "arn:aws:s3:::private-bucket/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:SourceVpce": "vpce-1234567890abcdef0"
        }
      }
    }
  ]
}
```

### MFA Delete Protection

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireMFAForDelete",
      "Effect": "Deny",
      "Principal": "*",
      "Action": [
        "s3:DeleteObject",
        "s3:DeleteObjectVersion"
      ],
      "Resource": "arn:aws:s3:::critical-bucket/*",
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### Time-Based Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BusinessHoursOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::business-bucket",
        "arn:aws:s3:::business-bucket/*"
      ],
      "Condition": {
        "DateGreaterThan": {
          "aws:CurrentTime": "2024-01-01T18:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2024-01-02T09:00:00Z"
        }
      }
    }
  ]
}
```

### CloudTrail Logging

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::cloudtrail-logs-bucket",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/mytrail"
        }
      }
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::cloudtrail-logs-bucket/AWSLogs/123456789012/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control",
          "AWS:SourceArn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/mytrail"
        }
      }
    }
  ]
}
```

## Condition Keys Reference

```yaml
condition_keys:
  global:
    aws:SourceIp: "IP address or CIDR"
    aws:SourceVpc: "VPC ID"
    aws:SourceVpce: "VPC endpoint ID"
    aws:PrincipalOrgID: "AWS Organization ID"
    aws:CurrentTime: "ISO 8601 datetime"
    aws:MultiFactorAuthPresent: "true/false"
    aws:SecureTransport: "true/false"

  s3_specific:
    s3:x-amz-acl: "ACL to apply"
    s3:x-amz-server-side-encryption: "AES256 or aws:kms"
    s3:x-amz-server-side-encryption-aws-kms-key-id: "KMS key ARN"
    s3:ExistingObjectTag/<key>: "Object tag value"
    s3:RequestObjectTagKeys: "Tags being set"
    s3:prefix: "Object key prefix"
    s3:max-keys: "Max keys in ListBucket"
    s3:object-lock-mode: "GOVERNANCE or COMPLIANCE"

  operators:
    StringEquals: "Exact match"
    StringNotEquals: "Not equal"
    StringLike: "Wildcard match (*)"
    IpAddress: "IP in CIDR"
    NotIpAddress: "IP not in CIDR"
    DateGreaterThan: "After date"
    DateLessThan: "Before date"
    Bool: "Boolean check"
    Null: "Key exists/not exists"
```

## Security Best Practices

```yaml
security_checklist:
  block_public_access:
    setting: "Block all public access"
    how: |
      aws s3api put-public-access-block \
        --bucket my-bucket \
        --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

  enable_versioning:
    purpose: "Protect against accidental deletion"
    how: |
      aws s3api put-bucket-versioning \
        --bucket my-bucket \
        --versioning-configuration Status=Enabled

  enable_logging:
    purpose: "Audit access"
    how: |
      aws s3api put-bucket-logging \
        --bucket my-bucket \
        --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"log-bucket","TargetPrefix":"s3-access/"}}'

  default_encryption:
    purpose: "Encrypt at rest"
    how: |
      aws s3api put-bucket-encryption \
        --bucket my-bucket \
        --server-side-encryption-configuration \
        '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"alias/s3-key"}}]}'

  lifecycle_policy:
    purpose: "Manage object lifecycle"
    example: "Transition to Glacier after 90 days, delete after 365"
```

## Troubleshooting

```yaml
common_issues:
  access_denied:
    symptoms: "403 AccessDenied error"
    checks:
      - "Verify IAM user/role permissions"
      - "Check bucket policy allows action"
      - "Verify resource ARN is correct"
      - "Check for explicit Deny statements"
      - "Verify bucket block public access settings"
    debug: |
      # Check effective policy
      aws s3api get-bucket-policy --bucket my-bucket

      # Test access
      aws s3api head-object --bucket my-bucket --key test.txt

  policy_too_large:
    limit: "20 KB maximum"
    solutions:
      - "Use IAM policies instead"
      - "Consolidate statements"
      - "Use conditions instead of listing principals"
      - "Reference IAM roles instead of users"

  invalid_principal:
    symptoms: "MalformedPolicy error"
    common_causes:
      - "Account ID doesn't exist"
      - "Role/user doesn't exist"
      - "Typo in ARN format"
    format: "arn:aws:iam::ACCOUNT-ID:root/role/user"

  condition_not_working:
    checks:
      - "Verify condition key spelling"
      - "Check operator type matches value type"
      - "Ensure condition applies to correct action"
```

## Policy Validation

```bash
# Validate policy syntax
aws iam simulate-custom-policy \
  --policy-input-list file://policy.json \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/test.txt

# Test policy with IAM Policy Simulator
# Console: https://policysim.aws.amazon.com/

# Check for public access
aws s3api get-bucket-policy-status --bucket my-bucket

# List bucket policies
aws s3api get-bucket-policy --bucket my-bucket --output text
```

## Terraform Example

```hcl
resource "aws_s3_bucket" "example" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "example" {
  bucket = aws_s3_bucket.example.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceSSL"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.example.arn,
          "${aws_s3_bucket.example.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
```

## Лучшие практики

1. **Least privilege** — минимальные необходимые права
2. **Block public access** — блокируй публичный доступ по умолчанию
3. **Use conditions** — добавляй условия для дополнительной защиты
4. **Enable logging** — логируй все обращения к bucket
5. **Version control** — храни политики в git
6. **Regular audits** — проверяй политики регулярно
