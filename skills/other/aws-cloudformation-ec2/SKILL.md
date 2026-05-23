---
name: aws-cloudformation-ec2
description: Provides AWS CloudFormation patterns for EC2 instances, Security Groups, IAM roles, and load balancers. Use when creating EC2 instances, SPOT instances, Security Groups, IAM roles for EC2, Application Load Balancers (ALB), Target Groups, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation EC2 Infrastructure

## Overview

Create production-ready EC2 infrastructure using AWS CloudFormation templates. Covers EC2 instances (On-Demand and SPOT), Security Groups, IAM roles, Application Load Balancers (ALB), template structure, parameters, outputs, and cross-stack references.

## When to Use

- Creating EC2 instances (On-Demand or SPOT) with Security Groups and IAM roles
- Setting up Application Load Balancers with target groups
- Implementing template Parameters, Mappings, Conditions, and cross-stack references

## Instructions

### Step 1 — Define Template Parameters

Use AWS-specific parameter types for validation and console dropdowns.

```yaml
Parameters:
  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2

  InstanceType:
    Type: AWS::EC2::InstanceType
    Default: t3.micro
    AllowedValues: [t3.micro, t3.small, t3.medium]

  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
```

See [template-structure.md](references/template-structure.md) for advanced parameter patterns, mappings, conditions, and cross-stack references.

### Step 2 — Create Security Group

Define ingress/egress rules for network access.

```yaml
InstanceSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Security group for EC2 instance
    VpcId: !Ref VpcId
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 80
        ToPort: 80
        CidrIp: 0.0.0.0/0
      - IpProtocol: tcp
        FromPort: 22
        ToPort: 22
        CidrIp: 10.0.0.0/16
```

See [security-iam.md](references/security-iam.md) for advanced security group patterns, self-references, and IAM roles.

### Step 3 — Configure IAM Role

Define instance profile with least privilege permissions.

```yaml
Ec2Role:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: "2012-10-17"
      Statement:
        - Effect: Allow
          Principal:
            Service: ec2.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

Ec2InstanceProfile:
  Type: AWS::IAM::InstanceProfile
  Properties:
    Roles: [!Ref Ec2Role]
```

See [security-iam.md](references/security-iam.md) for least privilege policies, SSM roles, and trust policies.

### Step 4 — Launch EC2 Instance

Configure instance with security group, IAM role, and user data.

```yaml
Ec2Instance:
  Type: AWS::EC2::Instance
  Properties:
    ImageId: !Ref LatestAmiId
    InstanceType: !Ref InstanceType
    KeyName: !Ref KeyName
    SecurityGroupIds: [!Ref InstanceSecurityGroup]
    IamInstanceProfile: !Ref Ec2InstanceProfile
    SubnetId: !Ref SubnetId
    UserData:
      Fn::Base64: |
        #!/bin/bash
        yum update -y
        yum install -y httpd
        systemctl start httpd
    Tags:
      - Key: Name
        Value: !Sub ${AWS::StackName}-instance
```

See [ec2-instances.md](references/ec2-instances.md) for multi-volume configurations, detailed monitoring, SPOT instances, and complete stack examples.

**Validate template:** `aws cloudformation validate-template --template-body file://template.yaml`

### Step 5 — Add Application Load Balancer

Create ALB with target group and listener for traffic distribution.

```yaml
ApplicationLoadBalancer:
  Type: AWS::ElasticLoadBalancingV2::LoadBalancer
  Properties:
    Name: !Sub ${AWS::StackName}-alb
    Scheme: internet-facing
    SecurityGroups: [!Ref AlbSecurityGroup]
    Subnets: [!Ref PublicSubnet1, !Ref PublicSubnet2]

ApplicationTargetGroup:
  Type: AWS::ElasticLoadBalancingV2::TargetGroup
  Properties:
    Port: 80
    Protocol: HTTP
    VpcId: !Ref VpcId
    HealthCheckPath: /health

ApplicationListener:
  Type: AWS::ElasticLoadBalancingV2::Listener
  Properties:
    DefaultActions:
      - Type: forward
        TargetGroupArn: !Ref ApplicationTargetGroup
    LoadBalancerArn: !Ref ApplicationLoadBalancer
    Port: 80
    Protocol: HTTP
```

See [load-balancers.md](references/load-balancers.md) for HTTPS configuration, path-based routing, host-based routing, listener rules, and ALB attributes.

### Step 6 — Define Outputs

Export values for cross-stack references.

```yaml
Outputs:
  InstanceId:
    Description: EC2 Instance ID
    Value: !Ref Ec2Instance
    Export:
      Name: !Sub ${AWS::StackName}-InstanceId

  SecurityGroupId:
    Description: Security Group ID
    Value: !Ref InstanceSecurityGroup
    Export:
      Name: !Sub ${AWS::StackName}-SecurityGroupId

  LoadBalancerDnsName:
    Description: ALB DNS Name
    Value: !GetAtt ApplicationLoadBalancer.DNSName
```

See [template-structure.md](references/template-structure.md) for cross-stack reference patterns and import/export strategies.

## Examples

### Minimal EC2 with ALB Template

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: EC2 instance with ALB

Parameters:
  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2
  InstanceType:
    Type: AWS::EC2::InstanceType
    Default: t3.micro

Resources:
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable HTTP and SSH
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  Ec2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: !Ref InstanceType
      SecurityGroupIds: [!Ref InstanceSecurityGroup]

  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Scheme: internet-facing
      SecurityGroups: [!Ref InstanceSecurityGroup]
      Subnets: [subnet-12345678, subnet-87654321]

Outputs:
  InstanceId:
    Value: !Ref Ec2Instance
  LoadBalancerDns:
    Value: !GetAtt LoadBalancer.DNSName
```

### Deploy with Change Set

```bash
# Create change set
aws cloudformation create-change-set \
  --stack-name my-ec2-stack \
  --template-body file://template.yaml \
  --change-set-type CREATE

# Execute after review
aws cloudformation execute-change-set \
  --change-set-name <change-set-name>
```

See [examples.md](references/examples.md) for complete production-ready templates.

## Best Practices

### Template Structure
- **Use AWS-specific parameter types** for validation (`AWS::EC2::VPC::Id`, `AWS::EC2::InstanceType`)
- **Organize by lifecycle** - separate network, security, and application stacks
- **Use meaningful names** with `AWS::StackName` prefix
- **Enable termination protection** on production stacks

### Security
- **Apply least privilege** to IAM roles - grant minimum required permissions
- **Use security group references** instead of IP addresses where possible
- **Enable IMDSv2** on all EC2 instances
- **Restrict security group rules** to specific CIDR blocks

### Cost & Availability
- **Use SPOT instances** for fault-tolerant, interruptible workloads
- **Deploy across multiple AZs** for high availability
- **Set up CloudWatch alarms** for CPU and status checks
- **Use EBS gp3 volumes** for cost-effective storage

### Operations
- **Always use change sets** for production stack updates
- **Enable drift detection** to maintain template compliance
- **Apply stack policies** to protect critical resources
- **Validate templates** before deployment with `aws cloudformation validate-template`

See [best-practices.md](references/best-practices.md) for detailed guidance on stack policies, termination protection, drift detection, change set automation, and validation scripts.

## References

### Core Configuration
- **[template-structure.md](references/template-structure.md)** — Template sections, parameters, mappings, conditions, outputs, cross-stack references
- **[ec2-instances.md](references/ec2-instances.md)** — EC2 instances, SPOT fleets, multi-volume configurations, complete stack examples
- **[security-iam.md](references/security-iam.md)** — Security groups, IAM roles, instance profiles, least privilege policies
- **[load-balancers.md](references/load-balancers.md)** — ALB configuration, target groups, listeners, path-based routing, HTTPS

### Operational Guides
- **[best-practices.md](references/best-practices.md)** — Stack policies, termination protection, drift detection, change sets, validation
- **[constraints.md](references/constraints.md)** — Resource limits, instance constraints, cost considerations, common issues, monitoring

### Additional Resources
- **[examples.md](references/examples.md)** — Complete production-ready examples and use cases
- **[reference.md](references/reference.md)** — CloudFormation EC2 resource reference documentation

## Constraints and Warnings

### Resource Limits
- Maximum 500 resources per CloudFormation stack
- Maximum 500 security groups per VPC
- Instance types vary by region/A availability

### Cost Considerations
- EC2 instances incur costs while running
- EBS volumes charged per GB-month even when not attached
- ALBs have hourly + LCU data processing costs
- Unattached Elastic IPs incur hourly costs

### Security Considerations
- Key pairs cannot be recovered if lost
- Instance profile roles cannot be changed after creation
- IMDSv1 has security vulnerabilities - use IMDSv2
- Spot instances can be terminated with 2-minute notice

See [constraints.md](references/constraints.md) for complete constraints, troubleshooting guides, and monitoring setup.
