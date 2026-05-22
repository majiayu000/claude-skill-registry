---
name: aws-cloudfront-cdn
description: Distribute content globally using CloudFront with caching, security headers, WAF integration, and origin configuration. Use for low-latency content delivery.
---

# AWS CloudFront CDN

## Overview

Amazon CloudFront is a fast, globally distributed content delivery network (CDN). Cache content at edge locations worldwide to reduce latency, improve performance, and provide high availability with DDoS protection.

## When to Use

- Static website hosting and assets
- API acceleration and dynamic content
- Video and media streaming
- Mobile application content
- Large file downloads
- Real-time data distribution
- DDoS protection for origins
- Origin isolation and security

## Implementation Examples

### 1. **CloudFront Distribution with AWS CLI**

```bash
# Create distribution for S3 origin
aws cloudfront create-distribution \
  --distribution-config '{
    "CallerReference": "myapp-'$(date +%s)'",
    "Enabled": true,
    "Comment": "My application distribution",
    "Origins": {
      "Quantity": 1,
      "Items": [{
        "Id": "myS3Origin",
        "DomainName": "mybucket.s3.us-east-1.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": "origin-access-identity/cloudfront/ABCDEFG1234567"
        }
      }]
    },
    "DefaultCacheBehavior": {
      "AllowedMethods": {
        "Quantity": 3,
        "Items": ["GET", "HEAD", "OPTIONS"]
      },
      "ViewerProtocolPolicy": "redirect-to-https",
      "TargetOriginId": "myS3Origin",
      "ForwardedValues": {
        "QueryString": false,
        "Cookies": {"Forward": "none"},
        "Headers": {"Quantity": 0}
      },
      "TrustedSigners": {
        "Enabled": false,
        "Quantity": 0
      },
      "MinTTL": 0,
      "DefaultTTL": 86400,
      "MaxTTL": 31536000,
      "Compress": true
    },
    "CacheBehaviors": [
      {
        "PathPattern": "/api/*",
        "AllowedMethods": {
          "Quantity": 7,
          "Items": ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
        },
        "ViewerProtocolPolicy": "https-only",
        "TargetOriginId": "myS3Origin",
        "ForwardedValues": {
          "QueryString": true,
          "Cookies": {"Forward": "all"},
          "Headers": {"Quantity": 0}
        },
        "MinTTL": 0,
        "DefaultTTL": 0,
        "MaxTTL": 31536000
      }
    ],
    "WebACLId": "arn:aws:wafv2:us-east-1:123456789012:global/webacl/test/a1234567"
  }'

# List distributions
aws cloudfront list-distributions

# Get distribution config
aws cloudfront get-distribution-config \
  --id E123EXAMPLE123

# Invalidate cache
aws cloudfront create-invalidation \
  --distribution-id E123EXAMPLE123 \
  --paths "/*"
```

### 2. **Terraform CloudFront Configuration**

```hcl
# cloudfront.tf
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

# Origin Access Identity
resource "aws_cloudfront_origin_access_identity" "s3" {
  comment = "OAI for S3 bucket"
}

# S3 bucket for CloudFront origin
resource "aws_s3_bucket" "static" {
  bucket = "myapp-static-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_versioning" "static" {
  bucket = aws_s3_bucket.static.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "static" {
  bucket = aws_s3_bucket.static.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 bucket policy for CloudFront
resource "aws_s3_bucket_policy" "static" {
  bucket = aws_s3_bucket.static.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "AllowCloudFrontAccess"
      Effect = "Allow"
      Principal = {
        AWS = aws_cloudfront_origin_access_identity.s3.iam_arn
      }
      Action   = "s3:GetObject"
      Resource = "${aws_s3_bucket.static.arn}/*"
    }]
  })
}

# WAF Web ACL
resource "aws_wafv2_web_acl" "cloudfront" {
  scope = "CLOUDFRONT"
  name  = "cloudfront-waf"

  default_action {
    allow {}
  }

  rule {
    name     = "RateLimitRule"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitRule"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 2

    action {
      block {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "cloudfront-waf"
    sampled_requests_enabled   = true
  }
}

# CloudFront distribution
resource "aws_cloudfront_distribution" "s3" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  comment             = "CDN for static assets"

  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3Origin"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.s3.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Origin"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }

      headers = ["Origin", "Accept-Charset"]
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
  }

  cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Origin"

    forwarded_values {
      query_string = true

      cookies {
        forward = "all"
      }

      headers = ["Authorization", "Host", "User-Agent"]
    }

    viewer_protocol_policy = "https-only"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 31536000
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  web_acl_id = aws_wafv2_web_acl.cloudfront.arn

  tags = {
    Name = "cdn-distribution"
  }
}

# CloudFront cache policy for static assets
resource "aws_cloudfront_cache_policy" "static" {
  name        = "static-cache-policy"
  comment     = "Cache policy for static assets"
  default_ttl = 86400
  max_ttl     = 31536000
  min_ttl     = 0

  parameters_in_cache_key_and_forwarded_to_origin {
    query_strings_config {
      query_string_behavior = "none"
    }

    headers_config {
      header_behavior = "none"
    }

    cookies_config {
      cookie_behavior = "none"
    }

    enable_accept_encoding_gzip   = true
    enable_accept_encoding_brotli = true
  }
}

# Origin request policy
resource "aws_cloudfront_origin_request_policy" "api" {
  name    = "api-origin-request-policy"
  comment = "Forward headers for API requests"

  headers_config {
    header_behavior = "allViewer"
  }

  query_strings_config {
    query_string_behavior = "all"
  }

  cookies_config {
    cookie_behavior = "all"
  }
}

# Invalidation
resource "aws_cloudfront_invalidation" "s3" {
  distribution_id = aws_cloudfront_distribution.s3.id
  paths           = ["/*"]

  depends_on = [aws_cloudfront_distribution.s3]
}

# CloudWatch alarms
resource "aws_cloudwatch_metric_alarm" "cloudfront_errors" {
  alarm_name          = "cloudfront-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "4xxErrorRate"
  namespace           = "AWS/CloudFront"
  period              = 300
  statistic           = "Average"
  threshold           = 5
  alarm_description   = "Alert when error rate exceeds 5%"

  dimensions = {
    DistributionId = aws_cloudfront_distribution.s3.id
  }
}

data "aws_caller_identity" "current" {}

output "cloudfront_domain" {
  value       = aws_cloudfront_distribution.s3.domain_name
  description = "CloudFront domain name"
}

output "cloudfront_id" {
  value       = aws_cloudfront_distribution.s3.id
  description = "CloudFront distribution ID"
}
```

### 3. **Custom Headers and Security Configuration**

```bash
# Add custom headers for security
aws cloudfront create-response-headers-policy \
  --response-headers-policy-config '{
    "Name": "SecurityHeadersPolicy",
    "SecurityHeadersConfig": {
      "StrictTransportSecurity": {
        "Enabled": true,
        "AccessControlMaxAgeSec": 63072000,
        "IncludeSubdomains": true,
        "Preload": true
      },
      "ContentTypeOptions": {
        "Enabled": true
      },
      "XSSProtection": {
        "Enabled": true,
        "ModeBlock": true
      },
      "ReferrerPolicy": {
        "Enabled": true,
        "ReferrerPolicy": "strict-origin-when-cross-origin"
      },
      "FrameOptions": {
        "Enabled": true,
        "FrameOption": "DENY"
      }
    }
  }'
```

## Best Practices

### ✅ DO
- Use Origin Access Identity (OAI) for S3
- Enable HTTPS only for viewers
- Compress content at CloudFront
- Set appropriate cache TTLs
- Use cache invalidation cautiously
- Enable WAF for protection
- Monitor CloudWatch metrics
- Use multiple origins for redundancy

### ❌ DON'T
- Make S3 buckets public
- Cache sensitive data
- Use HTTP for production
- Ignore cache headers
- Create excessive invalidations
- Skip WAF protection

## Monitoring

- CloudWatch metrics (requests, bytes, errors)
- CloudWatch Alarms for errors and latency
- WAF metrics and blocked requests
- Cache hit/miss ratios
- Origin latency metrics

## Resources

- [AWS CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [CloudFront Best Practices](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/best-practices.html)
- [CloudFront Security](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/security.html)
