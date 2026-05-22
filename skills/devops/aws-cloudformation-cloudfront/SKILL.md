---
name: aws-cloudformation-cloudfront
description: AWS CloudFormation patterns for CloudFront distributions, origins (ALB, S3, Lambda@Edge, VPC Origins), CacheBehaviors, Functions, SecurityHeaders, parameters, Outputs and cross-stack references. Use when creating CloudFront distributions with CloudFormation, configuring multiple origins, implementing caching strategies, managing custom domains with ACM, configuring WAF, and optimizing performance.
category: aws
tags: [aws, cloudformation, cloudfront, cdn, content-delivery, distributions, origins, cache, waf, security]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation CloudFront CDN

## Overview

Create production-ready CDN infrastructure using AWS CloudFormation templates. This skill covers CloudFront distributions, multiple origins (ALB, S3, Lambda@Edge, VPC Origins), CacheBehaviors, Functions, SecurityHeaders, and best practices for parameters, outputs, and cross-stack references.

## When to Use

Use this skill when:
- Creating new CloudFront distributions with CloudFormation
- Configuring multiple origins (ALB, S3, API Gateway, Lambda@Edge, VPC Origins)
- Implementing caching strategies with CacheBehaviors and Cache Policies
- Configuring custom domains with ACM certificates
- Implementing SecurityHeaders (CSP, HSTS, XSS protection)
- Configuring CloudFront Functions and Lambda@Edge
- Managing Geo-restrictions and Price Classes
- Integrating WAF with CloudFront
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import
- Using Transform for macros and reuse

## CloudFormation Template Structure

### Standard Format Base Template

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront distribution with multiple origins

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Distribution Configuration
        Parameters:
          - DomainName
          - CertificateArn
          - PriceClass
      - Label:
          default: Origin Settings
        Parameters:
          - OriginDomainName
          - OriginPath
          - OriginProtocolPolicy

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

  OriginPath:
    Type: String
    Default: ""
    Description: Optional origin path

Mappings:
  EnvironmentConfig:
    us-east-1:
      CertificateRegion: us-east-1
    other:
      CertificateRegion: us-east-1

Conditions:
  IsUsEast1: !Equals [!Ref AWS::Region, us-east-1]
  HasOriginPath: !Not [!Equals [!Ref OriginPath, ""]]

Transform:
  - AWS::Serverless-2016-10-31

Resources:
  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront distribution for ${DomainName}"
        DomainNames:
          - !Ref DomainName
        Enabled: true
        PriceClass: !Ref PriceClass
        IPV6Enabled: true
        DefaultRootObject: index.html
        Origins:
          - Id: !Sub "${DomainName}-origin"
            DomainName: !Ref OriginDomainName
            OriginPath: !If [HasOriginPath, !Ref OriginPath, !Ref AWS::NoValue]
            CustomOriginConfig:
              HTTPPort: 80
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
              OriginSSLProtocols:
                - TLSv1.2
        DefaultCacheBehavior:
          TargetOriginId: !Sub "${DomainName}-origin"
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000
        ViewerCertificate:
          AcmCertificateArn: !Ref CertificateArn
          MinimumProtocolVersion: TLSv1.2_2021
          SslSupportMethod: sni-only

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

## Best Practices for Parameters

### AWS-Specific Parameter Types

```yaml
Parameters:
  # ACM Certificate for domain
  CertificateArn:
    Type: AWS::ACM::Certificate::Arn
    Description: ACM certificate for the domain

  # S3 Bucket origins
  StaticAssetsBucket:
    Type: AWS::S3::Bucket
    Description: S3 bucket for static assets

  StaticAssetsBucketDomainName:
    Type: AWS::S3::Bucket::RegionalDomainName
    Description: Regional domain name of the S3 bucket

  # ALB origins
  LoadBalancerArn:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer::Arn
    Description: ARN of the Application Load Balancer

  LoadBalancerDNSName:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer::DnsName
    Description: DNS name of the ALB

  # Lambda function origins
  LambdaFunctionArn:
    Type: AWS::Lambda::Function::Arn
    Description: ARN of the Lambda function for Lambda@Edge

  # VPC Origin
  VPCOriginEndpoint:
    Type: AWS::GlobalAccelerator::Endpoint::EndpointId
    Description: VPC Origin endpoint ID

  # IAM Role for Lambda@Edge
  LambdaEdgeRoleArn:
    Type: AWS::IAM::Role::Arn
    Description: IAM role for Lambda@Edge execution
```

### Parameter Constraints

```yaml
Parameters:
  DomainName:
    Type: String
    Default: cdn.example.com
    Description: Custom domain name for CloudFront
    ConstraintDescription: Must be a valid domain name
    MinLength: 4
    MaxLength: 253
    AllowedPattern: "[a-z0-9]([a-z0-9-]*[a-z0-9])?(\\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*"

  PriceClass:
    Type: String
    Default: PriceClass_All
    Description: CloudFront price class
    AllowedValues:
      - PriceClass_All
      - PriceClass_100
      - PriceClass_200

  DefaultTTL:
    Type: Number
    Default: 86400
    Description: Default cache TTL in seconds
    MinValue: 0
    MaxValue: 31536000
    ConstraintDescription: Must be between 0 and 31536000 seconds

  MaxTTL:
    Type: Number
    Default: 31536000
    Description: Maximum cache TTL in seconds
    MinValue: 0
    MaxValue: 31536000

  MinTTL:
    Type: Number
    Default: 0
    Description: Minimum cache TTL in seconds
    MinValue: 0
    MaxValue: 31536000
```

### SSM Parameter References

```yaml
Parameters:
  WafWebAclArn:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /cloudfront/waf-webacl-arn
    Description: WAF Web ACL ARN from Parameter Store

  CloudFrontKeyId:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /cloudfront/keys/cloudfront-key-id
    Description: CloudFront key pair ID for signed URLs
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Network/Infrastructure Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Infrastructure stack exporting CloudFront resources

Resources:
  # S3 Bucket for static content
  StaticAssetsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "static-assets-${AWS::AccountId}-${AWS::Region}"
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      VersioningConfiguration:
        Status: Enabled
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders:
              - "*"
            AllowedMethods:
              - GET
              - HEAD
            AllowedOrigins:
              - "*"
            MaxAge: 3600

  # OAI for CloudFront access
  CloudFrontOAI:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: !Sub "OAI for ${StaticAssetsBucket}"

Outputs:
  StaticAssetsBucketName:
    Description: S3 bucket name for static assets
    Value: !Ref StaticAssetsBucket
    Export:
      Name: !Sub "${AWS::StackName}-StaticAssetsBucketName"

  StaticAssetsBucketArn:
    Description: S3 bucket ARN
    Value: !GetAtt StaticAssetsBucket.Arn
    Export:
      Name: !Sub "${AWS::StackName}-StaticAssetsBucketArn"

  StaticAssetsBucketRegionalDomainName:
    Description: Regional domain name of the S3 bucket
    Value: !GetAtt StaticAssetsBucket.RegionalDomainName
    Export:
      Name: !Sub "${AWS::StackName}-StaticAssetsBucketRegionalDomainName"

  CloudFrontOAIId:
    Description: CloudFront OAI ID
    Value: !Ref CloudFrontOAI
    Export:
      Name: !Sub "${AWS::StackName}-CloudFrontOAIId"

  CloudFrontOAIArn:
    Description: CloudFront OAI ARN
    Value: !GetAtt CloudFrontOAI.Arn
    Export:
      Name: !Sub "${AWS::StackName}-CloudFrontOAIArn"
```

```yaml
# Stack B - Application Stack (imports from Infrastructure Stack)
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack importing from infrastructure stack

Parameters:
  InfrastructureStackName:
    Type: String
    Default: infrastructure-stack
    Description: Name of the infrastructure stack

  DomainName:
    Type: String
    Default: cdn.example.com
    Description: Custom domain name

  CertificateArn:
    Type: AWS::ACM::Certificate::Arn
    Description: ACM certificate ARN

Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront for ${DomainName}"
        Enabled: true
        IPV6Enabled: true
        DefaultRootObject: index.html
        Origins:
          - Id: StaticAssetsOrigin
            DomainName: !ImportValue
              !Sub "${InfrastructureStackName}-StaticAssetsBucketRegionalDomainName"
            S3OriginConfig:
              OriginAccessIdentity: !Sub "origin-access-identity/cloudfront/${InfrastructureStackName}-CloudFrontOAIId"
        DefaultCacheBehavior:
          TargetOriginId: StaticAssetsOrigin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000
        ViewerCertificate:
          AcmCertificateArn: !Ref CertificateArn
          MinimumProtocolVersion: TLSv1.2_2021
          SslSupportMethod: sni-only
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested CloudFront stacks

Resources:
  # Nested stack for static assets distribution
  StaticAssetsDistributionStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/cloudfront-static.yaml
      TimeoutInMinutes: 15
      Parameters:
        DomainName: !Ref DomainName
        CertificateArn: !Ref CertificateArn
        StaticAssetsBucketName: !Ref StaticAssetsBucketName
        Environment: !Ref Environment

  # Nested stack for API distribution
  ApiDistributionStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/cloudfront-api.yaml
      TimeoutInMinutes: 15
      Parameters:
        DomainName: !Ref ApiDomainName
        CertificateArn: !Ref CertificateArn
        LoadBalancerDnsName: !Ref LoadBalancerDnsName
        Environment: !Ref Environment
```

## S3 Origins

### S3 Origin with OAI

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront distribution with S3 origin

Resources:
  # S3 Bucket
  StaticBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "static-assets-${AWS::AccountId}-${AWS::Region}"
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # CloudFront OAI
  CloudFrontOAI:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: !Sub "OAI for ${StaticBucket}"

  # S3 Bucket Policy - Allow CloudFront OAI
  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref StaticBucket
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              CanonicalUser: !GetAtt CloudFrontOAI.S3CanonicalUserId
            Action: s3:GetObject
            Resource: !Sub "${StaticBucket.Arn}/*"
          - Effect: Deny
            Principal: "*"
            Action: s3:GetObject
            Resource: !Sub "${StaticBucket.Arn}/*"
            Condition:
              Bool:
                aws:SecureTransport: false

  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "Static assets CDN"
        Enabled: true
        IPV6Enabled: true
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt StaticBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub "origin-access-identity/cloudfront/${CloudFrontOAI}"
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
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000

Outputs:
  DistributionDomainName:
    Value: !GetAtt CloudFrontDistribution.DomainName
```

### S3 Origin with Origin Access Control (OAC)

```yaml
Resources:
  StaticBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "static-assets-oac-${AWS::AccountId}-${AWS::Region}"
      OwnershipControls:
        Rules:
          - ObjectOwnership: BucketOwnerPreferred
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # S3 Bucket Policy for OAC
  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref StaticBucket
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: cloudfront.amazonaws.com
            Action: s3:GetObject
            Resource: !Sub "${StaticBucket.Arn}/*"
            Condition:
              StringEquals:
                AWS:SourceArn: !Sub "arn:aws:cloudfront::${AWS::AccountId}:distribution/${CloudFrontDistribution}"

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt StaticBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: ""
        # For OAC, use OriginAccessControl instead of S3OriginConfig
        # but CloudFormation supports both
```

## ALB Origins

### Application Load Balancer Origin

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront with ALB origin

Resources:
  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub "${AWS::StackName}-alb"
      Scheme: internet-facing
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      Type: application

  # ALB Security Group
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: ALB security group
      VpcId: !Ref VPCId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref CloudFrontSecurityGroup
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref CloudFrontSecurityGroup

  # CloudFront Security Group (for ALB ingress)
  CloudFrontSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: CloudFront security group for ALB
      VpcId: !Ref VPCId
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          DestinationSecurityGroupId: !Ref ALBSecurityGroup
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          DestinationSecurityGroupId: !Ref ALBSecurityGroup

  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront with ALB origin"
        Enabled: true
        Origins:
          - Id: ALBOrigin
            DomainName: !GetAtt ApplicationLoadBalancer.DNSName
            CustomOriginConfig:
              HTTPPort: 80
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
              OriginSSLProtocols:
                - TLSv1.2
        DefaultCacheBehavior:
          TargetOriginId: ALBOrigin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: true
            Headers:
              - Origin
              - Access-Control-Request-Method
              - Access-Control-Request-Headers
            Cookies:
              Forward: all
            QueryStringSettings:
              - Name: "*"
          MinTTL: 0
          DefaultTTL: 0
          MaxTTL: 0
```

## Multiple Origins and CacheBehaviors

### Multi-Origin with Path Patterns

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront with multiple origins and cache behaviors

Resources:
  # S3 Bucket for static assets
  StaticAssetsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "static-assets-${AWS::AccountId}-${AWS::Region}"

  CloudFrontOAI:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: !Sub "OAI for ${StaticAssetsBucket}"

  # Application Load Balancer for API
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub "${AWS::StackName}-api-alb"
      Scheme: internet-facing
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets: !Ref PublicSubnets
      Type: application

  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "Multi-origin CloudFront distribution"
        Enabled: true
        IPV6Enabled: true
        DefaultRootObject: index.html
        Origins:
          # Static assets origin
          - Id: StaticAssetsOrigin
            DomainName: !GetAtt StaticAssetsBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub "origin-access-identity/cloudfront/${CloudFrontOAI}"
          # API origin
          - Id: ApiOrigin
            DomainName: !GetAtt ApplicationLoadBalancer.DNSName
            CustomOriginConfig:
              HTTPPort: 80
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
          # Lambda origin
          - Id: LambdaOrigin
            DomainName: !Sub "${LambdaFunction}.execute-api.${AWS::Region}.amazonaws.com"
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          # Default: static assets
          TargetOriginId: StaticAssetsOrigin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000
        CacheBehaviors:
          # API cache behavior
          - PathPattern: "/api/*"
            TargetOriginId: ApiOrigin
            ViewerProtocolPolicy: redirect-to-https
            AllowedMethods:
              - GET
              - HEAD
              - OPTIONS
              - PUT
              - POST
              - PATCH
              - DELETE
            CachedMethods:
              - GET
              - HEAD
            Compress: true
            ForwardedValues:
              QueryString: true
              Headers:
                - Accept
                - Accept-Language
                - Authorization
              Cookies:
                Forward: all
            MinTTL: 0
            DefaultTTL: 0
            MaxTTL: 0
          # Lambda function path
          - PathPattern: "/lambda/*"
            TargetOriginId: LambdaOrigin
            ViewerProtocolPolicy: redirect-to-https
            AllowedMethods:
              - GET
              - HEAD
              - OPTIONS
            CachedMethods:
              - GET
              - HEAD
            Compress: true
            ForwardedValues:
              QueryString: true
              Cookies:
                Forward: none
            MinTTL: 0
            DefaultTTL: 0
            MaxTTL: 0
```

## Cache Policies

### Managed Cache Policy

```yaml
Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CacheBehaviors:
          - PathPattern: "/static/*"
            TargetOriginId: StaticAssetsOrigin
            ViewerProtocolPolicy: redirect-to-https
            AllowedMethods:
              - GET
              - HEAD
            CachedMethods:
              - GET
              - HEAD
            Compress: true
            CachePolicyId: !Ref ManagedCachingOptimizedPolicyId
            FunctionAssociations:
              - FunctionARN: !GetAtt CloudFrontFunction.FunctionARN
                EventType: viewer-request

          - PathPattern: "/api/*"
            TargetOriginId: ApiOrigin
            ViewerProtocolPolicy: redirect-to-https
            AllowedMethods:
              - GET
              - HEAD
              - OPTIONS
            CachedMethods:
              - GET
              - HEAD
            Compress: true
            CachePolicyId: !Ref ManagedSecurityHeadersPolicyId
```

### Custom Cache Policy

```yaml
Resources:
  # Custom Cache Policy
  StaticAssetsCachePolicy:
    Type: AWS::CloudFront::CachePolicy
    Properties:
      CachePolicyConfig:
        Name: !Sub "${AWS::StackName}-static-assets-policy"
        DefaultTTL: 86400
        MaxTTL: 31536000
        MinTTL: 0
        ParametersInCacheKeyAndForwardedToOrigin:
          CookiesConfig:
            CookieBehavior: none
          HeadersConfig:
            HeaderBehavior: none
          QueryStringsConfig:
            QueryStringBehavior: none
          EnableAcceptEncodingBrotli: true
          EnableAcceptEncodingGzip: true

  # Custom Cache Policy for API
  ApiCachePolicy:
    Type: AWS::CloudFront::CachePolicy
    Properties:
      CachePolicyConfig:
        Name: !Sub "${AWS::StackName}-api-cache-policy"
        DefaultTTL: 300
        MaxTTL: 600
        MinTTL: 60
        ParametersInCacheKeyAndForwardedToOrigin:
          CookiesConfig:
            CookieBehavior: all
          HeadersConfig:
            HeaderBehavior: whitelist
            Headers:
              - Authorization
              - Content-Type
              - Accept
          QueryStringsConfig:
            QueryStringBehavior: all
          EnableAcceptEncodingBrotli: true
          EnableAcceptEncodingGzip: true

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: StaticAssetsOrigin
            DomainName: !GetAtt StaticAssetsBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub "origin-access-identity/cloudfront/${CloudFrontOAI}"
        CacheBehaviors:
          - PathPattern: "/static/*"
            TargetOriginId: StaticAssetsOrigin
            CachePolicyId: !GetAtt StaticAssetsCachePolicy.Id
```

## Origin Request Policies

```yaml
Resources:
  # Origin Request Policy
  StaticAssetsOriginRequestPolicy:
    Type: AWS::CloudFront::OriginRequestPolicy
    Properties:
      OriginRequestPolicyConfig:
        Name: !Sub "${AWS::StackName}-static-assets-origin-request"
        CookiesConfig:
          CookieBehavior: none
        HeadersConfig:
          HeaderBehavior: none
        QueryStringsConfig:
          QueryStringBehavior: none

  ApiOriginRequestPolicy:
    Type: AWS::CloudFront::OriginRequestPolicy
    Properties:
      OriginRequestPolicyConfig:
        Name: !Sub "${AWS::StackName}-api-origin-request"
        CookiesConfig:
          CookieBehavior: all
        HeadersConfig:
          HeaderBehavior: whitelist
          Headers:
            - Authorization
            - Content-Type
            - X-Request-ID
        QueryStringsConfig:
          QueryStringBehavior: all

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CacheBehaviors:
          - PathPattern: "/api/*"
            TargetOriginId: ApiOrigin
            CachePolicyId: !GetAtt ApiCachePolicy.Id
            OriginRequestPolicyId: !GetAtt ApiOriginRequestPolicy.Id
```

## Response Headers Policies (Security Headers)

```yaml
Resources:
  # Security Headers Policy
  SecurityHeadersPolicy:
    Type: AWS::CloudFront::ResponseHeadersPolicy
    Properties:
      ResponseHeadersPolicyConfig:
        Name: !Sub "${AWS::StackName}-security-headers"
        SecurityHeadersConfig:
          ContentTypeOptions:
            Override: true
          FrameOptions:
            FrameOption: DENY
            Override: true
          ReferrerPolicy:
            ReferrerPolicy: strict-origin-when-cross-origin
            Override: true
          StrictTransportSecurity:
            AccessControlMaxAgeSec: 31536000
            IncludeSubdomains: true
            Override: true
            Preload: true
          XSSProtection:
            ModeBlock: true
            Override: true
            Protection: true
        CorsConfig:
          AccessControlAllowCredentials: false
          AccessControlAllowHeaders:
            Items:
              - "*"
          AccessControlAllowMethods:
            Items:
              - GET
              - HEAD
              - OPTIONS
          AccessControlAllowOrigins:
            Items:
              - !Ref AllowedOrigin
          AccessControlMaxAgeSec: 600
          OriginOverride: true

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        DefaultCacheBehavior:
          TargetOriginId: StaticAssetsOrigin
          ResponseHeadersPolicyId: !GetAtt SecurityHeadersPolicy.Id
```

## CloudFront Functions

### Viewer Request Function

```yaml
Resources:
  # CloudFront Function
  RewritePathFunction:
    Type: AWS::CloudFront::Function
    Properties:
      Name: !Sub "${AWS::StackName}-rewrite-path"
      FunctionCode: |
        function handler(event) {
          var request = event.request;
          var uri = request.uri;

          // Remove trailing slash
          if (uri.endsWith('/')) {
            request.uri = uri.substring(0, uri.length - 1);
          }

          // Add .html extension for HTML pages
          if (!uri.includes('.') && !uri.endsWith('/')) {
            request.uri = uri + '.html';
          }

          return request;
        }
      Runtime: cloudfront-js-1.0
      AutoPublish: true

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        DefaultCacheBehavior:
          TargetOriginId: StaticAssetsOrigin
          FunctionAssociations:
            - FunctionARN: !GetAtt RewritePathFunction.FunctionARN
              EventType: viewer-request
```

### Lambda@Edge Functions

```yaml
Resources:
  # Lambda@Edge Function
  LambdaEdgeFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-lambda-edge"
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/edge-function.zip
      Handler: index.handler
      Runtime: nodejs20.x
      Role: !GetAtt LambdaEdgeRole.Arn

  # Lambda Version for Lambda@Edge
  LambdaEdgeVersion:
    Type: AWS::Lambda::Version
    Properties:
      FunctionName: !Ref LambdaEdgeFunction
      Description: Lambda@Edge version

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: Origin
            DomainName: !Ref OriginDomainName
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          TargetOriginId: Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          LambdaFunctionAssociations:
            - FunctionARN: !Sub "arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:${LambdaEdgeFunction}:${LambdaEdgeVersion}"
              EventType: origin-request
```

## Geo-Restrictions and Price Class

```yaml
Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront with geo restrictions"
        Enabled: true
        IPV6Enabled: true

        # Price Class - optimize costs
        PriceClass: PriceClass_200

        # Geo Restrictions
        GeoRestriction:
          RestrictionType: whitelist
          Locations:
            - US
            - CA
            - GB
            - DE
            - FR
            - IT
            - JP
            - AU

        Origins:
          - Id: Origin
            DomainName: !Ref OriginDomainName
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only

        DefaultCacheBehavior:
          TargetOriginId: Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000
```

## WAF Integration

```yaml
Resources:
  # WAF Web ACL
  CloudFrontWebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: !Sub "${AWS::StackName}-waf-acl"
      Scope: CLOUDFRONT
      DefaultAction:
        Allow: {}
      Rules:
        # AWS Managed Rule - Common
        - Name: AWSCommonRule
          Priority: 1
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesCommonRuleSet
              ExcludedRules:
                - Name: SizeRestrictions_BODY
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: AWSCommonRule

        # Rate-based rule
        - Name: RateLimitRule
          Priority: 2
          Statement:
            RateBasedStatementKey:
              SingleHeader:
                Name: ip
            AggregateKeyType: IP
            Limit: 1000
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: RateLimitRule

        # SQL Injection protection
        - Name: SQLInjectionRule
          Priority: 3
          Statement:
            SqliMatchStatement:
              FieldToMatch:
                QueryString: {}
                UriPath: {}
              TextTransformations:
                - Priority: 1
                  Type: URL_DECODE
                - Priority: 2
                  Type: LOWERCASE
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: SQLInjectionRule

        # XSS protection
        - Name: XSSRule
          Priority: 4
          Statement:
            XssMatchStatement:
              FieldToMatch:
                QueryString: {}
                UriPath: {}
              TextTransformations:
                - Priority: 1
                  Type: URL_DECODE
                - Priority: 2
                  Type: LOWERCASE
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: XSSRule

      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: CloudFrontWAFACL

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront with WAF"
        Enabled: true
        WebACLId: !GetAtt CloudFrontWebACL.Arn
        Origins:
          - Id: Origin
            DomainName: !Ref OriginDomainName
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          TargetOriginId: Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000
```

## Real-Time Logs

```yaml
Resources:
  # Kinesis Data Stream
  CloudFrontLogsStream:
    Type: AWS::Kinesis::Stream
    Properties:
      Name: !Sub "${AWS::StackName}-cloudfront-logs"
      ShardCount: 1
      RetentionPeriodHours: 24

  # IAM Role for CloudFront
  CloudFrontLoggingRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-cloudfront-logging"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: cloudfront.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: KinesisPutRecord
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - kinesis:PutRecord
                  - kinesis:PutRecords
                Resource: !GetAtt CloudFrontLogsStream.Arn

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront with real-time logs"
        Enabled: true
        RealTimeConfig:
          Endpoint: !GetAtt CloudFrontLogsStream.Arn
          RoleArn: !GetAtt CloudFrontLoggingRole.Arn
          Fields:
            - timestamp
            - c-ip
            - cs-method
            - cs-uri
            - sc-status
            - time-taken
        Origins:
          - Id: Origin
            DomainName: !Ref OriginDomainName
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          TargetOriginId: Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: 0
          DefaultTTL: 86400
          MaxTTL: 31536000
```

## Conditions and Transform

### Conditions for Environment-Specific Configuration

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront with conditional configuration

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production
    Description: Deployment environment

  EnableWAF:
    Type: String
    Default: false
    AllowedValues:
      - true
      - false
    Description: Enable WAF protection

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsStaging: !Equals [!Ref Environment, staging]
  EnableWAFProtection: !And
    - !Equals [!Ref EnableWAF, true]
    - !Or
      - [!Equals [!Ref Environment, staging]]
      - [!Equals [!Ref Environment, production]]

Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront for ${Environment}"
        Enabled: true
        IPV6Enabled: true
        PriceClass: !If [IsProduction, PriceClass_All, PriceClass_100]
        WebACLId: !If [EnableWAFProtection, !Ref CloudFrontWebACL, !Ref AWS::NoValue]
        Origins:
          - Id: Origin
            DomainName: !Ref OriginDomainName
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          TargetOriginId: Origin
          ViewerProtocolPolicy: !If [IsProduction, redirect-to-https, allow-all]
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: !If [IsProduction, true, false]
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          MinTTL: !If [IsProduction, 0, 0]
          DefaultTTL: !If [IsProduction, 86400, 3600]
          MaxTTL: !If [IsProduction, 31536000, 86400]

  # WAF only for staging and production
  CloudFrontWebACL:
    Type: AWS::WAFv2::WebACL
    Condition: EnableWAFProtection
    Properties:
      Name: !Sub "${AWS::StackName}-waf-acl"
      Scope: CLOUDFRONT
      DefaultAction:
        Allow: {}
      Rules: []
      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: CloudFrontWAFACL
```

## VPC Origins

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront with VPC Origin

Resources:
  # VPC Origin Endpoint
  VPCOriginEndpoint:
    Type: AWS::GlobalAccelerator::EndpointGroup
    Properties:
      EndpointGroupRegion: !Ref VPCOriginRegion
      ListenerArn: !Ref AcceleratorListener
      EndpointConfigurations:
        - EndpointId: !Ref VPCEndpointService
          Weight: 128

  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        CallerReference: !Sub "${AWS::StackName}-${AWS::AccountId}"
        Comment: !Sub "CloudFront with VPC Origin"
        Enabled: true
        IPV6Enabled: true
        Origins:
          - Id: VPCOrigin
            DomainName: !Ref VPCOriginDomain
            CustomOriginConfig:
              HTTPPort: 443
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
              OriginKeepaliveTimeout: 60
              OriginReadTimeout: 30
        DefaultCacheBehavior:
          TargetOriginId: VPCOrigin
          ViewerProtocolPolicy: https-only
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: true
            Headers:
              - "*"
            Cookies:
              Forward: all
          MinTTL: 0
          DefaultTTL: 3600
          MaxTTL: 86400
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


## CloudFormation Best Practices

### Stack Policies

Stack Policies prevent accidental updates to critical resources during stack updates.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront distribution with stack policy

Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        # ... configuration

  CloudFrontWebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: !Sub "${AWS::StackName}-waf"
      Scope: CLOUDFRONT
      DefaultAction:
        Allow: {}
      Rules: []
      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: CloudFrontWAF

# Stack Policy - protect critical resources
Metadata:
  AWS::CloudFormation::StackPolicy:
    Statement:
      - Effect: Allow
        Action: Update:*
        Resource: "*"
      - Effect: Deny
        Action:
          - Update:Replace
          - Update:Delete
        Resource: "LogicalID=CloudFrontDistribution"
        Principal: "*"
      - Effect: Deny
        Action:
          - Update:Replace
          - Update:Delete
        Resource: "LogicalID=CloudFrontWebACL"
        Principal: "*"
```

### Termination Protection

Enable termination protection to prevent accidental stack deletion.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront with termination protection

Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        # ... configuration

# Note: Termination protection is enabled via AWS Console or CLI
# AWS CLI: aws cloudformation update-termination-protection --enable-termination-protection --stack-name my-stack
# Or set it in a separate stack update after creation
```

### Drift Detection

Detect when infrastructure has been modified outside of CloudFormation.

```yaml
# AWS CLI commands for drift detection
# Detect drift on a stack
aws cloudformation detect-stack-drift --stack-name my-cloudfront-stack

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id <detection-id>

# Get resources that have drifted
aws cloudformation describe-stack-resource-drifts --stack-name my-cloudfront-stack

# Example drift detection output format
# {
#     "StackResourceDrifts": [
#         {
#             "ResourceType": "AWS::CloudFront::Distribution",
#             "LogicalResourceId": "CloudFrontDistribution",
#             "PhysicalResourceId": "E1X2Y3Z4W5X6Y7",
#             "ResourceStatus": "UPDATE",
#             "PropertyDifferences": [
#                 {
#                     "PropertyPath": "$.DistributionConfig.Enabled",
#                     "ExpectedValue": "true",
#                     "ActualValue": "false"
#                 }
#             ],
#             "StackResourceDriftStatus": "MODIFIED"
#         }
#     ]
# }
```

### Change Sets

Preview and review changes before executing stack updates.

```yaml
# AWS CLI commands for change sets

# 1. Create a change set (preview)
aws cloudformation create-change-set \
  --stack-name my-cloudfront-stack \
  --template-body file://cloudfront-template.yaml \
  --change-set-name my-changeset \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=Environment,ParameterValue=production

# 2. Describe the change set to review changes
aws cloudformation describe-change-set \
  --stack-name my-cloudfront-stack \
  --change-set-name my-changeset

# 3. Execute the change set if changes are acceptable
aws cloudformation execute-change-set \
  --stack-name my-cloudfront-stack \
  --change-set-name my-changeset

# Or delete if changes are not desired
aws cloudformation delete-change-set \
  --stack-name my-cloudfront-stack \
  --change-set-name my-changeset
```

```yaml
# Change set with nested stacks example
AWSTemplateFormatVersion: 2010-09-09
Description: CloudFront infrastructure with nested stacks for change set management

Resources:
  # Parent stack managing multiple CloudFront distributions
  CloudFrontParentStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${ArtifactBucket}.s3.amazonaws.com/cloudfront-parent.yaml"
      TimeoutInMinutes: 30
      Parameters:
        Environment: !Ref Environment
        CertificateArn: !Ref CertificateArn
        DomainName: !Ref DomainName
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName
        - Key: ManagedBy
          Value: CloudFormation

  # Change set will show impacts across all nested stacks
  # When updating, CloudFormation will show:
  # - Which nested stacks will be updated
  # - Resources being added, modified, or deleted
  # - IAM changes requiring special attention
```

## Related Resources

- [AWS CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/)
- [CloudFront Best Practices](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [CloudFormation Stack Policies](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html)
- [CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html)
- [CloudFormation Change Sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)

## Additional Files

For complete details on resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
