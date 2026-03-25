---
name: aws-cloudformation-cloudfront
description: Provides AWS CloudFormation patterns for CloudFront distributions, origins (ALB, S3, Lambda@Edge, VPC Origins), CacheBehaviors, Functions, SecurityHeaders, parameters, Outputs and cross-stack references. Use when creating CloudFront distributions with CloudFormation, configuring multiple origins, implementing caching strategies, managing custom domains with ACM, configuring WAF, and optimizing performance.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation CloudFront CDN

## Overview

Create production-ready CDN infrastructure using AWS CloudFormation templates. This skill covers CloudFront distributions, multiple origins (ALB, S3, API Gateway, Lambda@Edge, VPC Origins), CacheBehaviors, Functions, SecurityHeaders, and best practices for parameters, outputs, and cross-stack references.

## When to Use

- Creating CloudFront distributions with CloudFormation
- Configuring origins (ALB, S3, Lambda@Edge, VPC Origins) with path patterns
- Implementing caching with CacheBehaviors and Cache Policies
- Configuring custom domains with ACM and SecurityHeaders
- Integrating WAF with CloudFront distributions

## Instructions

Follow these steps to create CloudFront distributions with CloudFormation:

### 1. Define Distribution Parameters

**Validate before deploying:**
```bash
aws cloudformation validate-template --template-body file://template.yaml
cfn-lint template.yaml
```

Specify domain names, ACM certificates, price class, and origin settings:

```yaml
Parameters:
  DomainName:
    Type: String
    Default: cdn.example.com
    Description: Custom domain name for CloudFront distribution

  CertificateArn:
    Type: AWS::ACM::Certificate::Arn
    Description: ACM certificate ARN for HTTPS

  PriceClass:
    Type: String
    Default: PriceClass_All
    AllowedValues:
      - PriceClass_All
      - PriceClass_100
      - PriceClass_200
    Description: CloudFront price class

  OriginDomainName:
    Type: String
    Description: Domain name of the origin (ALB or S3)
```

### 2. Configure Origins

Add S3 buckets, ALBs, API Gateway, or custom origins. For S3 origins, use OAI (legacy) or OAC (recommended):

```yaml
Resources:
  # S3 Bucket
  StaticBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "static-assets-${AWS::AccountId}-${AWS::Region}"
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true

  # Origin Access Control (recommended)
  OriginAccessControl:
    Type: AWS::CloudFront::OriginAccessControl
    Properties:
      OriginAccessControlConfig:
        Name: !Sub "${AWS::StackName}-oac"
        OriginAccessControlOriginType: s3
        SigningBehavior: always
        SigningProtocol: sigv4
```

### 3. Set Up Default Cache Behavior

Configure viewer request/response policies and caching:

```yaml
Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt StaticBucket.RegionalDomainName
            AccessControlId: !Ref OriginAccessControl
            S3OriginConfig:
              OriginAccessIdentity: ""
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          CachePolicyId: !Ref CachePolicy
```

### 4. Add Additional Cache Behaviors

Create path-specific caching rules for different content types:

```yaml
Resources:
  ApiCachePolicy:
    Type: AWS::CloudFront::CachePolicy
    Properties:
      CachePolicyConfig:
        Name: !Sub "${AWS::StackName}-api-cache"
        DefaultTTL: 300
        MaxTTL: 600
        MinTTL: 60

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CacheBehaviors:
          - PathPattern: "/api/*"
            TargetOriginId: ApiOrigin
            CachePolicyId: !GetAtt ApiCachePolicy.Id
            AllowedMethods:
              - GET
              - HEAD
              - OPTIONS
              - PUT
              - POST
```

### 5. Configure Security Settings

Implement security headers and WAF integration:

```yaml
Resources:
  SecurityHeadersPolicy:
    Type: AWS::CloudFront::ResponseHeadersPolicy
    Properties:
      ResponseHeadersPolicyConfig:
        Name: !Sub "${AWS::StackName}-security-headers"
        SecurityHeadersConfig:
          StrictTransportSecurity:
            AccessControlMaxAgeSec: 31536000
            IncludeSubdomains: true
            Override: true
          FrameOptions:
            FrameOption: DENY
            Override: true

  WAFWebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: !Sub "${AWS::StackName}-waf"
      Scope: CLOUDFRONT
      DefaultAction:
        Allow: {}
```

### 6. Add CloudFront Functions

Configure functions for request/response manipulation:

```yaml
Resources:
  RewritePathFunction:
    Type: AWS::CloudFront::Function
    Properties:
      Name: !Sub "${AWS::StackName}-rewrite-path"
      FunctionCode: |
        function handler(event) {
          var request = event.request;
          // Function code here
          return request;
        }
      Runtime: cloudfront-js-1.0
      AutoPublish: true
```

### 7. Configure Monitoring

Set up logging and access logs to S3:

```yaml
Resources:
  AccessLogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "cloudfront-logs-${AWS::AccountId}"

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Logging:
          Bucket: !Ref AccessLogsBucket
          Prefix: cloudfront-logs/
          IncludeCookies: false
```

### 8. Create Outputs

Export distribution details for cross-stack references:

```yaml
Outputs:
  DistributionDomainName:
    Description: CloudFront distribution domain name
    Value: !GetAtt CloudFrontDistribution.DomainName
    Export:
      Name: !Sub "${AWS::StackName}-DistributionDomainName"

  DistributionId:
    Description: CloudFront distribution ID
    Value: !Ref CloudFrontDistribution
    Export:
      Name: !Sub "${AWS::StackName}-DistributionId"
```

## Best Practices

### Security

- Always use HTTPS with minimum TLS 1.2
- Implement SecurityHeaders with HSTS, XSS protection
- Use WAF for protection against common attacks
- Configure appropriate Access-Control for CORS
- Limit origin access with OAI/OAC
- Use Signed URLs for private content
- Implement rate limiting
- Configure geo-restrictions if needed

### Performance

- Use appropriate PriceClass to optimize costs
- Configure Cache TTL based on content type
- Enable compression (Gzip/Brotli)
- Use CloudFront Functions for lightweight operations
- Optimize header forwarding (do not forward unnecessary headers)
- Consider Origin Shield to reduce load on origins
- Use multiple origins with path patterns

### Monitoring

- Enable CloudWatch metrics and alarms
- Configure real-time logs for troubleshooting
- Monitor cache hit ratio
- Configure alerts for error rate and latency
- Use CloudFront reports for traffic analysis

### Deployment

- Use change sets before deployment
- Test templates with cfn-lint
- Organize stacks by lifecycle and ownership
- Implement blue/green deployments with weighted aliases
- Use StackSets for multi-region deployment

### Template Structure

- Use AWS-specific parameter types (AWS::ACM::Certificate::Arn, AWS::S3::Bucket::RegionalDomainName)
- Implement parameter constraints (MinLength, MaxLength, AllowedValues, AllowedPattern)
- Use Conditions for environment-specific configuration
- Leverage Mappings for region-specific configuration
- Apply Metadata for parameter grouping and labels
- Use nested stacks for modularity

### Cache Strategy

- Use Cache Policies for different content types
- Configure Origin Request Policies to control what's sent to origin
- Set appropriate TTL values:
  - Static assets: 86400-31536000 seconds (1 day to 1 year)
  - API responses: 60-600 seconds (1-10 minutes)
  - Dynamic content: 0 seconds (no caching)
- Enable compression for text-based content
- Use versioned paths for cache busting

## Constraints and Warnings

- **ACM certificates**: Must be in `us-east-1` (N. Virginia) for CloudFront
- **Limits**: Max 200 distributions per AWS account, 25 origins per distribution, 25 cache behaviors per distribution
- **Deployment time**: CloudFront distributions take up to 30 minutes to deploy; plan accordingly
- **Certificate requirements**: Max 100 alternate domain names per distribution; include default domain for SSL
- **OAI deprecation**: Prefer Origin Access Control (OAC) over Origin Access Identity (OAI) for S3 origins
- **Lambda@Edge limits**: 128MB memory, 30s timeout for viewer request/response; separate limits apply for origin requests
- **Change sets**: Always use change sets before deploying to preview resource changes and avoid accidental deletions
- **Drift detection**: CloudFormation does not detect drift for CloudFront distributions — manage all settings in templates

## Examples

### Minimal S3 Static Site Distribution

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "cdn-static-${AWS::AccountId}"
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true

  OriginAccessControl:
    Type: AWS::CloudFront::OriginAccessControl
    Properties:
      OriginAccessControlConfig:
        Name: !Sub "${AWS::StackName}-oac"
        OriginAccessControlOriginType: s3
        SigningBehavior: always
        SigningProtocol: sigv4

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        DefaultRootObject: index.html
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt S3Bucket.RegionalDomainName
            AccessControlId: !Ref OriginAccessControl
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          Compress: true
          CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6
        PriceClass: PriceClass_All
        HttpVersion: http2and3

Outputs:
  DistributionDomainName:
    Value: !GetAtt CloudFrontDistribution.DomainName
```

### Multi-Origin with Cache Behaviors

```yaml
Resources:
  CachePolicyApi:
    Type: AWS::CloudFront::CachePolicy
    Properties:
      CachePolicyConfig:
        Name: !Sub "${AWS::StackName}-api"
        DefaultTTL: 300
        MaxTTL: 600
        MinTTL: 60

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt StaticBucket.RegionalDomainName
            AccessControlId: !Ref OriginAccessControl
          - Id: ApiOrigin
            DomainName: !GetAtt ApiLoadBalancer.DNSName
            CustomOriginConfig:
              OriginProtocolPolicy: https-only
              HTTPPort: 80
              HTTPSPort: 443
        CacheBehaviors:
          - PathPattern: "/api/*"
            TargetOriginId: ApiOrigin
            CachePolicyId: !GetAtt CachePolicyApi.Id
            ViewerProtocolPolicy: https-only
          - PathPattern: "/static/*"
            TargetOriginId: S3Origin
            CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6
```

## References

For detailed implementation guidance, see:

- **[template-structure.md](references/template-structure.md)** - Complete template structure, AWS-specific parameter types, parameter constraints, SSM parameter references, metadata for parameter grouping, transform for macros, conditions for environment-specific configuration, nested stacks, and cross-stack references with export/import patterns

- **[origins.md](references/origins.md)** - Origin configuration including S3 origins with OAI/OAC, ALB origins with security groups, API Gateway origins (REST and HTTP APIs), Lambda@Edge origins, VPC origins with Global Accelerator, custom origins, and multi-origin configurations with path patterns

- **[caching.md](references/caching.md)** - Cache policies (managed, custom, images, videos), origin request policies, response headers policies, cache behaviors configuration, forwarded values (query strings, headers, cookies), cache key configuration, and TTL configuration best practices

- **[security.md](references/security.md)** - Security headers (CSP, HSTS, XSS protection), CORS configuration, WAF integration with managed and custom rules, origin access control (OAI vs OAC), signed URLs and signed cookies, geo-restrictions, HTTPS enforcement, TLS configuration, and field-level encryption

- **[advanced-features.md](references/advanced-features.md)** - CloudFront Functions (viewer request, viewer response, origin request), Lambda@Edge for authentication and URL rewriting, geo-restrictions, price class optimization, compression (Gzip and Brotli), real-time logs to Kinesis and S3, custom error pages, function associations, and Origin Shield configuration

- **[constraints.md](references/constraints.md)** - Resource limits (200 distributions max, 25 origins max, 25 cache behaviors max), DNS and certificate constraints (ACM in us-east-1, 300 alternate domain names), operational constraints (15 invalidations max, 30 min deployment), security constraints (HTTPS, CSP, WAF), and cost considerations (data transfer, regional pricing, Lambda@Edge costs)

## Related Resources

- [AWS CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/)
- [CloudFront Best Practices](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [CloudFormation Stack Policies](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html)
- [CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html)
- [CloudFormation Change Sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)
