---
name: aws-cloudformation-vpc
description: AWS CloudFormation patterns for VPC infrastructure. Use when creating VPCs, Subnets, Route Tables, NAT Gateways, Internet Gateways, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references.
category: aws
tags: [aws, cloudformation, vpc, networking, infrastructure, terraform, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation VPC Infrastructure

## Overview

Create production-ready VPC infrastructure using AWS CloudFormation templates. This skill covers VPC components (Subnets, Route Tables, NAT Gateways, Internet Gateways), template structure best practices, parameter patterns, and cross-stack references for modular, reusable infrastructure as code.

## When to Use

Use this skill when:
- Creating new VPCs with public and private subnets
- Configuring route tables for internet and NAT connectivity
- Setting up Internet Gateways and NAT Gateways
- Implementing template Parameters with AWS-specific types
- Creating Outputs for cross-stack references
- Organizing templates with Mappings and Conditions
- Designing reusable, modular CloudFormation templates

## Quick Start

### Basic VPC with Public Subnet

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Simple VPC with public subnet

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-vpc

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-public-subnet

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-igw

  VPCGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-public-rt

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: VPCGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnetRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet
      RouteTableId: !Ref PublicRouteTable
```

### VPC with Public and Private Subnets

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: VPC with public and private subnets across multiple AZs

Parameters:
  EnvironmentName:
    Type: String
    Default: production
    Description: Environment name for resource tagging

  VpcCidr:
    Type: String
    Default: 10.0.0.0/16
    Description: CIDR block for the VPC

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Name
          Value: !Sub ${AWS::StackName}-vpc

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Name
          Value: !Sub ${AWS::StackName}-igw

  VPCGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # Public Subnet 1
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: SubnetType
          Value: Public
        - Key: Name
          Value: !Sub ${AWS::StackName}-public-1

  PublicRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Name
          Value: !Sub ${AWS::StackName}-public-rt-1

  DefaultPublicRoute1:
    Type: AWS::EC2::Route
    DependsOn: VPCGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable1
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet1
      RouteTableId: !Ref PublicRouteTable1

  # Private Subnet 1
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.10.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: SubnetType
          Value: Private
        - Key: Name
          Value: !Sub ${AWS::StackName}-private-1

  PrivateRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Name
          Value: !Sub ${AWS::StackName}-private-rt-1

  PrivateSubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet1
      RouteTableId: !Ref PrivateRouteTable1

Outputs:
  VpcId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub ${AWS::StackName}-VpcId

  PublicSubnet1Id:
    Description: Public Subnet 1 ID
    Value: !Ref PublicSubnet1
    Export:
      Name: !Sub ${AWS::StackName}-PublicSubnet1Id

  PrivateSubnet1Id:
    Description: Private Subnet 1 ID
    Value: !Ref PrivateSubnet1
    Export:
      Name: !Sub ${AWS::StackName}-PrivateSubnet1Id
```

## Template Structure

### Template Sections Overview

AWS CloudFormation templates are JSON or YAML files with specific sections. Each section serves a purpose in defining your infrastructure.

```yaml
AWSTemplateFormatVersion: 2010-09-09  # Required - template version
Description: Optional description string  # Optional description

# Section order matters for readability but CloudFormation accepts any order
Mappings: {}       # Static configuration tables
Metadata: {}       # Additional information about resources
Parameters: {}     # Input values for customization
Rules: {}          # Parameter validation rules
Conditions: {}     # Conditional resource creation
Transform: {}      # Macro processing (e.g., AWS::Serverless)
Resources: {}      # AWS resources to create (REQUIRED)
Outputs: {}        # Return values after stack creation
```

### Format Version

The `AWSTemplateFormatVersion` identifies the template version. Current version is `2010-09-09`.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: My CloudFormation Template
```

### Description

Add a description to document the template's purpose. Must appear after the format version.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  This template creates a VPC with public and private subnets
  for hosting web applications. It includes:
  - Internet Gateway for public access
  - NAT Gateway for private subnet outbound access
  - Security groups for web and database tiers
```

### Metadata

Use `Metadata` for additional information about resources or parameters.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Network Configuration
        Parameters:
          - VpcCidr
          - PublicSubnetCidr
          - PrivateSubnetCidr
      - Label:
          default: Tags
        Parameters:
          - EnvironmentName
          - ProjectName
    ParameterLabels:
      VpcCidr:
        default: VPC CIDR Block
      EnvironmentName:
        default: Environment Name
```

### Resources Section

The `Resources` section is the only required section. It defines AWS resources to provision.

```yaml
Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-vpc
```

## Parameters

### Parameter Types

Use AWS-specific parameter types for validation and easier selection in the console.

```yaml
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: Select an existing VPC

  SubnetId:
    Type: AWS::EC2::Subnet::Id
    Description: Select a subnet

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Select existing security groups

  InstanceType:
    Type: AWS::EC2::InstanceType
    Description: EC2 instance type
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
      - t3.large

  AmiId:
    Type: AWS::EC2::Image::Id
    Description: Select an AMI

  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: Select an existing key pair
```

### Parameter Constraints

Add constraints to validate parameter values.

```yaml
Parameters:
  VpcCidr:
    Type: String
    Description: CIDR block for the VPC
    Default: 10.0.0.0/16
    AllowedPattern: ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$
    ConstraintDescription: Must be a valid CIDR block (x.x.x.x/x)

  InstanceCount:
    Type: Number
    Description: Number of instances to launch
    Default: 1
    MinValue: 1
    MaxValue: 10

  Environment:
    Type: String
    Description: Deployment environment
    Default: development
    AllowedValues:
      - development
      - staging
      - production
    ConstraintDescription: Must be development, staging, or production
```

### SSM Parameter Types

Reference Systems Manager parameters for dynamic values.

```yaml
Parameters:
  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Description: Latest AMI ID from SSM
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2
```

## Mappings

Use `Mappings` for static configuration data based on regions or other factors.

```yaml
Mappings:
  RegionMap:
    us-east-1:
      HVM64: ami-0ff8a95407f89df2f
      HVMG2: ami-0a0c776d80e2a1f3c
    us-west-2:
      HVM64: ami-0a0c776d80e2a1f3c
      HVMG2: ami-0a0c776d80e2a1f3c
    eu-west-1:
      HVM64: ami-0ff8a95407f89df2f
      HVMG2: ami-0a0c776d80e2a1f3c

  EnvironmentConfig:
    development:
      InstanceType: t3.micro
      MinInstances: 1
      MaxInstances: 2
    staging:
      InstanceType: t3.small
      MinInstances: 1
      MaxInstances: 3
    production:
      InstanceType: t3.medium
      MinInstances: 2
      MaxInstances: 10

Resources:
  Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref AWS::Region, HVM64]
      InstanceType: !FindInMap [EnvironmentConfig, !Ref Environment, InstanceType]
```

## Conditions

Use `Conditions` to conditionally create resources based on parameters.

```yaml
Parameters:
  DeployNatGateway:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

  Environment:
    Type: String
    Default: development
    AllowedValues:
      - development
      - staging
      - production

Conditions:
  ShouldDeployNat: !Equals [!Ref DeployNatGateway, true]
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  NatGateway:
    Type: AWS::EC2::NatGateway
    Condition: ShouldDeployNat
    Properties:
      AllocationId: !If
        - ShouldDeployNat
        - !GetAtt EIP.AllocationId
        - !Ref AWS::NoValue
      SubnetId: !Ref PublicSubnet

  ProductionOnlyResource:
    Type: AWS::EC2::VPCEndpoint
    Condition: IsProduction
    Properties:
      ServiceName: !Sub com.amazonaws.${AWS::Region}.s3
      VpcId: !Ref VPC
```

## Transform

Use `Transform` for macros like AWS::Serverless for SAM templates.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: SAM template for serverless application

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs18.x
      CodeUri: function/
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

## Outputs and Cross-Stack References

### Basic Outputs

```yaml
Outputs:
  VpcId:
    Description: VPC ID
    Value: !Ref VPC

  PublicSubnetId:
    Description: Public Subnet ID
    Value: !Ref PublicSubnet

  VpcCidr:
    Description: VPC CIDR Block
    Value: !GetAtt VPC.CidrBlock
```

### Exporting Values for Cross-Stack References

Export values so other stacks can import them.

```yaml
Outputs:
  VpcId:
    Description: VPC ID for other stacks
    Value: !Ref VPC
    Export:
      Name: !Sub ${AWS::StackName}-VpcId

  PublicSubnetIds:
    Description: Comma-separated public subnet IDs
    Value: !Join [",", [!Ref PublicSubnet1, !Ref PublicSubnet2]]
    Export:
      Name: !Sub ${AWS::StackName}-PublicSubnetIds

  PrivateSubnetIds:
    Description: Comma-separated private subnet IDs
    Value: !Join [",", [!Ref PrivateSubnet1, !Ref PrivateSubnet2]]
    Export:
      Name: !Sub ${AWS::StackName}-PrivateSubnetIds
```

### Importing Values in Another Stack

```yaml
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID from network stack
    # User selects from exported values in console

  # Or use Fn::ImportValue for programmatic access
Resources:
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      VpcId: !ImportValue
        Fn::Sub: ${NetworkStackName}-VpcId
      GroupDescription: Security group for application
```

### Cross-Stack Reference Pattern

Create a dedicated network stack that exports values:

```yaml
# network-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Network infrastructure stack

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-vpc

  PublicSubnets:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true

Outputs:
  VpcId:
    Value: !Ref VPC
    Export:
      Name: !Sub ${AWS::StackName}-VpcId

  PublicSubnetIds:
    Value: !Ref PublicSubnets
    Export:
      Name: !Sub ${AWS::StackName}-PublicSubnetIds
```

Application stack imports these values:

```yaml
# application-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack that imports from network

Parameters:
  NetworkStackName:
    Type: String
    Description: Name of the network stack
    Default: network-stack

Resources:
  Instance:
    Type: AWS::EC2::Instance
    Properties:
      SubnetId: !ImportValue
        Fn::Sub: ${NetworkStackName}-PublicSubnetIds
      InstanceType: t3.micro
```

## VPC Components

### VPC with All Components

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Complete VPC with public/private subnets, NAT, and IGW

Parameters:
  EnvironmentName:
    Type: String
    Default: production

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-vpc
        - Key: Environment
          Value: !Ref EnvironmentName

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-igw
        - Key: Environment
          Value: !Ref EnvironmentName

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # NAT Gateway (with EIP)
  NatGatewayEIP:
    Type: AWS::EC2::EIP
    DependsOn: InternetGatewayAttachment
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-nat-eip

  NatGateway:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NatGatewayEIP.AllocationId
      SubnetId: !Ref PublicSubnet1
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-nat-gw
        - Key: Environment
          Value: !Ref EnvironmentName

  # Public Subnets
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-1
        - Key: SubnetType
          Value: Public

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-2
        - Key: SubnetType
          Value: Public

  # Private Subnets
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.10.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-1
        - Key: SubnetType
          Value: Private

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.11.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-2
        - Key: SubnetType
          Value: Private

  # Public Route Table
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-rt

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: InternetGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet1
      RouteTableId: !Ref PublicRouteTable

  PublicSubnetRouteTableAssociation2:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet2
      RouteTableId: !Ref PublicRouteTable

  # Private Route Table (with NAT)
  PrivateRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-rt

  DefaultPrivateRoute:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway

  PrivateSubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet1
      RouteTableId: !Ref PrivateRouteTable

  PrivateSubnetRouteTableAssociation2:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet2
      RouteTableId: !Ref PrivateRouteTable

Outputs:
  VpcId:
    Value: !Ref VPC
    Export:
      Name: !Sub ${EnvironmentName}-VpcId

  InternetGatewayId:
    Value: !Ref InternetGateway
    Export:
      Name: !Sub ${EnvironmentName}-InternetGatewayId

  PublicSubnetIds:
    Value: !Join [",", [!Ref PublicSubnet1, !Ref PublicSubnet2]]
    Export:
      Name: !Sub ${EnvironmentName}-PublicSubnetIds

  PrivateSubnetIds:
    Value: !Join [",", [!Ref PrivateSubnet1, !Ref PrivateSubnet2]]
    Export:
      Name: !Sub ${EnvironmentName}-PrivateSubnetIds

  NatGatewayId:
    Value: !Ref NatGateway
    Export:
      Name: !Sub ${EnvironmentName}-NatGatewayId
```

## Best Practices

### Use AWS-Specific Parameter Types

Always use AWS-specific parameter types for validation and easier selection.

```yaml
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: Select a VPC

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Select subnets

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Select security groups
```

### Organize by Lifecycle

Separate resources that change at different rates into different stacks.

```yaml
# Network stack - rarely changes
AWSTemplateFormatVersion: 2010-09-09
Description: Network infrastructure (VPC, subnets, routes)
Resources:
  VPC: AWS::EC2::VPC
  Subnets: AWS::EC2::Subnet
  RouteTables: AWS::EC2::RouteTable

# Application stack - changes frequently
AWSTemplateFormatVersion: 2010-09-09
Description: Application resources
Parameters:
  NetworkStackName:
    Type: String
Resources:
  Instances: AWS::EC2::Instance
```

### Use Meaningful Names

Use `AWS::StackName` and parameters for consistent naming.

```yaml
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-vpc
        - Key: Environment
          Value: !Ref EnvironmentName
```

### Use Pseudo Parameters

Use pseudo parameters for region-agnostic templates.

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-${AWS::AccountId}-${AWS::Region}

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: nodejs18.x
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
```

### Validate Before Deployment

```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Check for syntax errors
aws cloudformation validate-template \
  --template-body file://template.yaml \
  --query 'Description'

# Use cfn-lint for advanced validation
pip install cfn-lint
cfn-lint template.yaml
```

### Stack Policies

Stack Policies prevent unintentional updates to critical resources. Use them to protect production infrastructure.

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": ["Update:Replace", "Update:Delete"],
      "Principal": "*",
      "Resource": "LogicalId=ProductionDatabase"
    },
    {
      "Effect": "Deny",
      "Action": "Update:Replace",
      "Principal": "*",
      "Resource": "LogicalId=VPC"
    }
  ]
}
```

Apply the stack policy:

```bash
aws cloudformation set-stack-policy \
  --stack-name my-production-stack \
  --stack-policy-body file://stack-policy.json
```

**Common Stack Policy Use Cases:**

- **Protect database resources**: Prevent accidental replacement of RDS instances
- **Protect VPC infrastructure**: Prevent changes that could disrupt connectivity
- **Protect IAM roles**: Prevent modifications that could break authorization

### Termination Protection

Enable termination protection to prevent accidental stack deletion. This is critical for production environments.

**Enable via AWS Console:**
1. Go to CloudFormation > Stacks
2. Select your stack
3. Click "Stack actions" > "Enable termination protection"

**Enable via AWS CLI:**

```bash
# Enable termination protection
aws cloudformation update-termination-protection \
  --stack-name my-production-stack \
  --enable-termination-protection

# Disable termination protection (requires console access)
aws cloudformation update-termination-protection \
  --stack-name my-production-stack \
  --no-enable-termination-protection
```

**Enable via CloudFormation (for new stacks):**

```yaml
Resources:
  ProductionStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/my-bucket/production.yaml
      TerminationProtection: true
```

**Important Considerations:**
- Termination protection does not prevent stack updates
- To delete a protected stack, you must first disable termination protection
- Nested stacks inherit termination protection from parent stacks
- Always enable for production and staging environments

### Drift Detection

Drift detection identifies differences between your CloudFormation stack and the actual infrastructure. Run regular drift checks to ensure compliance.

**Detect Drift on a Stack:**

```bash
# Detect drift on a stack
aws cloudformation detect-drift \
  --stack-name my-vpc-stack

# Check drift status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>

# Get drift detection results
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-vpc-stack
```

**Drift Status Values:**
- `IN_SYNC`: Resource matches the template
- `DRIFTED`: Resource has been modified outside CloudFormation
- `NOT_CHECKED`: Resource was not checked
- `UNKNOWN`: Drift status could not be determined

**Automated Drift Detection with Events:**

```yaml
# Use AWS Config for continuous drift monitoring
Resources:
  ConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: cloudformation-drift-detection
      Scope:
        ComplianceResourceTypes:
          - AWS::EC2::VPC
          - AWS::EC2::Subnet
          - AWS::EC2::SecurityGroup
      Source:
        Owner: CUSTOM_LAMBDA
        SourceIdentifier:
          Fn::GetAtt: [DriftDetectionFunction, Arn]
```

**Best Practices for Drift Detection:**
- Run drift detection weekly for production stacks
- Set up CloudWatch Events to trigger drift detection on schedule
- Document and address all drift immediately
- Use drift detection as part of change management process

### Change Sets

Change Sets allow you to preview stack changes before applying them. This is essential for production deployments.

**Create and Review a Change Set:**

```bash
# Create a change set
aws cloudformation create-change-set \
  --stack-name my-vpc-stack \
  --template-body file://updated-template.yaml \
  --change-set-name vpc-update-changeset \
  --capabilities CAPABILITY_IAM

# List change sets
aws cloudformation list-change-sets \
  --stack-name my-vpc-stack

# Describe change set
aws cloudformation describe-change-set \
  --stack-name my-vpc-stack \
  --change-set-name vpc-update-changeset

# Execute change set
aws cloudformation execute-change-set \
  --stack-name my-vpc-stack \
  --change-set-name vpc-update-changeset

# Delete change set (if not executing)
aws cloudformation delete-change-set \
  --stack-name my-vpc-stack \
  --change-set-name vpc-update-changeset
```

**Change Set Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| `UPDATE` | Standard update | Regular changes |
| `CREATE` | Creates new stack | Initial deployment |
| `IMPORT` | Imports existing resources | Lift-and-shift |

**Change Set Output Example:**

```json
{
  "ChangeSetId": "arn:aws:cloudformation:us-east-1:123456789:changeSet/...",
  "Changes": [
    {
      "Type": "Resource",
      "ResourceChange": {
        "Action": "Modify",
        "LogicalResourceId": "VPC",
        "PhysicalResourceId": "vpc-12345678",
        "Replacement": "False",
        "Details": [
          {
            "Target": {
              "Attribute": "Tags",
              "RequiresRecreation": "Never"
            },
            "Evaluation": "Static",
            "ChangeSource": "DirectModification"
          }
        ]
      }
    }
  ],
  "ExecutionStatus": "AVAILABLE",
  "Status": "CREATE_COMPLETE"
}
```

**Best Practices for Change Sets:**
- Always create a change set before updating production stacks
- Review all changes carefully before execution
- Use meaningful change set names (e.g., `vpc-security-update-2024-01`)
- Execute change sets promptly after review
- Set a TTL on change sets if your organization requires approval workflows

### CI/CD Integration with Change Sets

```yaml
# GitHub Actions workflow for safe deployments
name: Deploy CloudFormation
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Create Change Set
        id: changeset
        run: |
          aws cloudformation create-change-set \
            --stack-name ${{ env.STACK_NAME }} \
            --template-body file://template.yaml \
            --change-set-name preview-changes \
            --capabilities CAPABILITY_IAM \
            --query 'Id' \
            --output text

      - name: Describe Change Set
        run: |
          aws cloudformation describe-change-set \
            --stack-name ${{ env.STACK_NAME }} \
            --change-set-name preview-changes

      - name: Execute Change Set (Manual approval required)
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: |
          aws cloudformation execute-change-set \
            --stack-name ${{ env.STACK_NAME }} \
            --change-set-name preview-changes
```

## Related Resources

- For advanced patterns: See [EXAMPLES.md](EXAMPLES.md)
- For reference: See [REFERENCE.md](REFERENCE.md)
- AWS CloudFormation User Guide: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
- AWS VPC Documentation: https://docs.aws.amazon.com/vpc/latest/userguide/
