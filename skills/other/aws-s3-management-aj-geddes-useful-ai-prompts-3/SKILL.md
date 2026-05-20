---
name: aws-s3-management
description: Manage S3 buckets with versioning, encryption, access control, lifecycle policies, and replication. Use for object storage, static sites, and data lakes.
---

# AWS S3 Management

## Overview

Amazon S3 provides secure, durable, and highly scalable object storage. Manage buckets with encryption, versioning, access controls, lifecycle policies, and cross-region replication for reliable data storage and retrieval.

## When to Use

- Static website hosting
- Data backup and archival
- Media library and CDN origin
- Data lake and analytics
- Log storage and analysis
- Application asset storage
- Disaster recovery
- Data sharing and collaboration

## Implementation Examples

### 1. **S3 Bucket Creation and Configuration with AWS CLI**

```bash
# Create bucket
aws s3api create-bucket \
  --bucket my-app-bucket-$(date +%s) \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-app-bucket \
  --versioning-configuration Status=Enabled

# Block public access
aws s3api put-public-access-block \
  --bucket my-app-bucket \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,\
    BlockPublicPolicy=true,RestrictPublicBuckets=true

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-app-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Upload file with metadata
aws s3 cp index.html s3://my-app-bucket/ \
  --cache-control "max-age=3600" \
  --metadata "author=john,version=1"

# Sync directory to S3
aws s3 sync ./dist s3://my-app-bucket/ \
  --delete \
  --exclude "*.map"

# List objects with metadata
aws s3api list-objects-v2 \
  --bucket my-app-bucket \
  --query 'Contents[].{Key:Key,Size:Size,Modified:LastModified}'
```

### 2. **S3 Lifecycle Policy Configuration**

```bash
# Create lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-app-bucket \
  --lifecycle-configuration '{
    "Rules": [
      {
        "Id": "archive-old-logs",
        "Status": "Enabled",
        "Prefix": "logs/",
        "Transitions": [
          {
            "Days": 30,
            "StorageClass": "STANDARD_IA"
          },
          {
            "Days": 90,
            "StorageClass": "GLACIER"
          }
        ],
        "Expiration": {
          "Days": 365
        }
      },
      {
        "Id": "cleanup-incomplete-uploads",
        "Status": "Enabled",
        "AbortIncompleteMultipartUpload": {
          "DaysAfterInitiation": 7
        }
      }
    ]
  }'

# Get bucket lifecycle
aws s3api get-bucket-lifecycle-configuration \
  --bucket my-app-bucket
```

### 3. **Terraform S3 Configuration**

```hcl
# s3.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# S3 bucket
resource "aws_s3_bucket" "app_data" {
  bucket = "my-app-data-${data.aws_caller_identity.current.account_id}"
}

# Block public access
resource "aws_s3_bucket_public_access_block" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning
resource "aws_s3_bucket_versioning" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle policy
resource "aws_s3_bucket_lifecycle_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    id     = "archive-logs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  rule {
    id     = "cleanup-incomplete-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# CORS configuration
resource "aws_s3_bucket_cors_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["https://example.com"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# Bucket policy for CloudFront
resource "aws_s3_bucket_policy" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFront"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.app_data.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/${aws_cloudfront_distribution.app.id}"
          }
        }
      }
    ]
  })
}

# Enable logging
resource "aws_s3_bucket_logging" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-logs/"
}

# Replication configuration
resource "aws_s3_bucket_replication_configuration" "app_data" {
  depends_on = [aws_s3_bucket_versioning.app_data]
  role       = aws_iam_role.s3_replication.arn
  bucket     = aws_s3_bucket.app_data.id

  rule {
    status = "Enabled"

    filter {}

    destination {
      bucket       = aws_s3_bucket.replica.arn
      storage_class = "STANDARD_IA"

      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }
    }
  }
}

data "aws_caller_identity" "current" {}

# Replica bucket
resource "aws_s3_bucket" "replica" {
  bucket = "my-app-data-replica-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_versioning" "replica" {
  bucket = aws_s3_bucket.replica.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Logs bucket
resource "aws_s3_bucket" "logs" {
  bucket = "my-app-logs-${data.aws_caller_identity.current.account_id}"
}

# IAM role for replication
resource "aws_iam_role" "s3_replication" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "s3_replication" {
  role = aws_iam_role.s3_replication.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.app_data.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl"
        ]
        Resource = "${aws_s3_bucket.app_data.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete"
        ]
        Resource = "${aws_s3_bucket.replica.arn}/*"
      }
    ]
  })
}
```

### 4. **S3 Access with Presigned URLs**

```bash
# Generate presigned URL (1 hour expiration)
aws s3 presign s3://my-app-bucket/private/document.pdf \
  --expires-in 3600

# Generate presigned URL for PUT (upload)
aws s3 presign s3://my-app-bucket/uploads/file.jpg \
  --expires-in 3600 \
  --region us-east-1 \
  --request-method PUT
```

## Best Practices

### ✅ DO
- Enable versioning for important data
- Use server-side encryption
- Block public access by default
- Implement lifecycle policies
- Enable logging and monitoring
- Use bucket policies for access control
- Enable MFA delete for critical buckets
- Use IAM roles instead of access keys
- Implement cross-region replication

### ❌ DON'T
- Make buckets publicly accessible
- Store sensitive credentials
- Ignore CloudTrail logging
- Use overly permissive policies
- Forget to set lifecycle rules
- Ignore encryption requirements

## Monitoring

- S3 CloudWatch metrics
- CloudTrail for API logging
- CloudWatch Alarms for threshold
- S3 Inventory for object tracking
- S3 Access Analyzer for permissions

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html)
