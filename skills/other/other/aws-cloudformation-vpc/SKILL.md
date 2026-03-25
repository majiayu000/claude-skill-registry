---
name: aws-cloudformation-vpc
description: Provides AWS CloudFormation patterns for VPC foundations, including subnets, route tables, internet and NAT gateways, endpoints, and reusable outputs. Use when creating a new network baseline, segmenting public and private workloads, or preparing CloudFormation networking stacks for application deployments.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation VPC Infrastructure

## Overview

Build a VPC foundation with CloudFormation that stays readable, reusable, and safe to evolve. Provides a clear subnet and routing model with predictable connectivity for public and private workloads, plus outputs that downstream stacks can consume without duplicating network logic.

Use the `references/` files for larger templates and extended service combinations.

## When to Use

- Creating a new VPC stack for an application or shared platform
- Adding public and private subnets across one or more Availability Zones
- Wiring internet access, NAT egress, or private endpoints
- Exporting VPC, subnet, route table, and security-group-adjacent identifiers for other stacks
- Preparing reusable infrastructure for ECS, EKS, Lambda, EC2, or RDS stacks

## Instructions

### 1. Start with the address plan

Before writing resources, define:
- VPC CIDR range
- Number of Availability Zones
- Public, private, and isolated subnet ranges
- Which workloads need internet ingress, NAT egress, or only private AWS service access

This prevents route-table sprawl and painful subnet replacement later.

### 2. Build the core network resources in layers

Create the stack in this order:
1. VPC and subnets
2. Internet Gateway for public ingress and egress
3. NAT gateways if private subnets need outbound internet access
4. Route tables and subnet associations
5. Optional VPC endpoints for private access to AWS services

Keep each layer easy to inspect in the template and avoid mixing unrelated application resources into the same stack.

### 3. Parameterize only the environment-dependent values

Useful parameters include:
- Environment name
- VPC CIDR and subnet CIDRs
- Number of AZs or explicit subnet IDs in nested-stack scenarios
- Flags for optional endpoints or NAT layout

Do not parameterize every route or tag unless it meaningfully changes between environments.

### 4. Export only what consumers really need

Typical outputs:
- VPC ID
- Public, private, and isolated subnet IDs
- Route table IDs when downstream stacks must attach routes
- Security boundaries or prefix-list references only when another stack consumes them

Stable outputs make application stacks easier to compose and migrate.

### 5. Validate before deployment

Run these commands to validate the template and verify routing:

```bash
# Validate CloudFormation template syntax
aws cloudformation validate-template --template-body file://vpc.yaml

# Review change set before applying
aws cloudformation create-change-set \
  --stack-name my-vpc \
  --template-body file://vpc.yaml \
  --change-set-type CREATE

# Verify route table associations
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=<vpc-id>"

# Check subnet to route table mappings
aws ec2 describe-route-tables \
  --filters "Name=association.subnet-id,Values=<subnet-id>"

# Verify internet gateway attachment
aws ec2 describe-internet-gateways \
  --filters "Name=attachment.vpc-id,Values=<vpc-id>"
```

## Examples

### Example 1: Complete two-tier VPC with routing

This template creates a VPC with public and private subnets, internet gateway, NAT gateway, and properly configured route tables.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "Two-tier VPC with public and private subnets"

Resources:
  # VPC
  MainVpc:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-main"

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-igw"

  # Attach IGW to VPC
  GatewayToInternet:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MainVpc
      InternetGatewayId: !Ref InternetGateway

  # Public Subnet (AZ 1)
  PublicSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVpc
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-public-a"

  # Private Subnet (AZ 1)
  PrivateSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVpc
      CidrBlock: 10.0.11.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-private-a"

  # Elastic IP for NAT Gateway
  NatEip:
    Type: AWS::EC2::EIP
    DependsOn: GatewayToInternet
    Properties:
      Domain: vpc

  # NAT Gateway
  NatGateway:
    Type: AWS::EC2::NatGateway
    Properties:
      SubnetId: !Ref PublicSubnetA
      AllocationId: !GetAtt NatEip.AllocationId

  # Public Route Table
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MainVpc
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-public-rt"

  # Default route to IGW
  PublicDefaultRoute:
    Type: AWS::EC2::Route
    DependsOn: GatewayToInternet
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  # Associate public subnet
  PublicSubnetARouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetA
      RouteTableId: !Ref PublicRouteTable

  # Private Route Table
  PrivateRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MainVpc
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-private-rt"

  # Default route via NAT Gateway
  PrivateDefaultRoute:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway

  # Associate private subnet
  PrivateSubnetARouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnetA
      RouteTableId: !Ref PrivateRouteTable

Outputs:
  VpcId:
    Description: VPC ID
    Value: !Ref MainVpc
    Export:
      Name: !Sub "${AWS::StackName}-VpcId"

  PublicSubnetA:
    Description: Public subnet AZ1
    Value: !Ref PublicSubnetA
    Export:
      Name: !Sub "${AWS::StackName}-PublicSubnetA"

  PrivateSubnetA:
    Description: Private subnet AZ1
    Value: !Ref PrivateSubnetA
    Export:
      Name: !Sub "${AWS::StackName}-PrivateSubnetA"

  PublicRouteTableId:
    Description: Public route table ID
    Value: !Ref PublicRouteTable
    Export:
      Name: !Sub "${AWS::StackName}-PublicRouteTableId"

  PrivateRouteTableId:
    Description: Private route table ID
    Value: !Ref PrivateRouteTable
    Export:
      Name: !Sub "${AWS::StackName}-PrivateRouteTableId"
```

### Example 2: VPC endpoint for private S3 access

```yaml
Resources:
  # S3 VPC Endpoint
  S3Endpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref MainVpc
      ServiceName: !Sub "com.amazonaws.${AWS::Region}.s3"
      RouteTableIds:
        - !Ref PrivateRouteTable
      VpcEndpointType: Gateway
```

## Best Practices

- Keep public, private, and isolated subnet purposes explicit in names and tags
- Prefer one NAT gateway per AZ for resilient production environments when budget allows
- Use VPC endpoints to reduce unnecessary NAT traffic for AWS service access
- Export VPC and subnet identifiers from the network stack instead of recreating network assumptions elsewhere
- Review network changes with dependency stacks because route and subnet changes can have broad blast radius
- Keep the root skill focused and move larger networking variants to `references/examples.md`

## Constraints and Warnings

- NAT gateways incur hourly costs and data transfer charges—consider VPC endpoints for AWS service access
- CIDR overlap blocks peering, transit, and future network expansion
- Route-table or subnet replacements can interrupt traffic even when the template is valid
- Endpoint quotas, AZ availability, and service-specific subnet requirements vary by region
- Hardcoding Availability Zones can reduce portability across accounts and regions

## References

- `references/examples.md`
- `references/reference.md`
