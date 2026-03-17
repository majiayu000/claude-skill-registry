---
name: aws
description: AWS cloud services including EC2, EKS, S3, Lambda, RDS, and IAM. Activate for AWS infrastructure, cloud deployment, and Amazon Web Services integration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# AWS Skill

Provides comprehensive AWS cloud capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- AWS infrastructure provisioning
- EKS cluster management
- S3 storage operations
- Lambda functions
- IAM and security

## AWS CLI Quick Reference

### Configuration
\`\`\`bash
# Configure credentials
aws configure

# Check identity
aws sts get-caller-identity

# Set profile
export AWS_PROFILE=production
aws s3 ls --profile production
\`\`\`

### EC2
\`\`\`bash
# List instances
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,Tags[?Key==`Name`].Value]'

# Start/Stop
aws ec2 start-instances --instance-ids i-1234567890
aws ec2 stop-instances --instance-ids i-1234567890

# Create instance
aws ec2 run-instances \
  --image-id ami-12345678 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-instance}]'
\`\`\`

### EKS
\`\`\`bash
# List clusters
aws eks list-clusters

# Update kubeconfig
aws eks update-kubeconfig --name golden-armada-cluster --region us-west-2

# Describe cluster
aws eks describe-cluster --name golden-armada-cluster

# Create cluster (with eksctl)
eksctl create cluster \
  --name golden-armada-cluster \
  --region us-west-2 \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 3 \
  --managed
\`\`\`

### S3
\`\`\`bash
# List buckets
aws s3 ls

# List objects
aws s3 ls s3://bucket-name/

# Copy files
aws s3 cp file.txt s3://bucket-name/
aws s3 cp s3://bucket-name/file.txt .
aws s3 sync ./local-dir s3://bucket-name/prefix/

# Presigned URL
aws s3 presign s3://bucket-name/file.txt --expires-in 3600
\`\`\`

### Lambda
\`\`\`bash
# List functions
aws lambda list-functions

# Invoke function
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  response.json

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip

# View logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '1 hour ago' +%s000)
\`\`\`

### RDS
\`\`\`bash
# List instances
aws rds describe-db-instances

# Create snapshot
aws rds create-db-snapshot \
  --db-instance-identifier golden-armada-db \
  --db-snapshot-identifier snapshot-$(date +%Y%m%d)

# Modify instance
aws rds modify-db-instance \
  --db-instance-identifier golden-armada-db \
  --db-instance-class db.t3.large \
  --apply-immediately
\`\`\`

### IAM
\`\`\`bash
# List users
aws iam list-users

# Create role
aws iam create-role \
  --role-name agent-role \
  --assume-role-policy-document file://trust-policy.json

# Attach policy
aws iam attach-role-policy \
  --role-name agent-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
\`\`\`

## Boto3 Python SDK

\`\`\`python
import boto3

# S3 operations
s3 = boto3.client('s3')

# Upload file
s3.upload_file('local.txt', 'bucket-name', 'remote.txt')

# Download file
s3.download_file('bucket-name', 'remote.txt', 'local.txt')

# List objects
response = s3.list_objects_v2(Bucket='bucket-name', Prefix='prefix/')
for obj in response.get('Contents', []):
    print(obj['Key'])

# EC2 operations
ec2 = boto3.resource('ec2')

# Get all running instances
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)
for instance in instances:
    print(f"{instance.id}: {instance.instance_type}")

# Lambda invocation
lambda_client = boto3.client('lambda')
response = lambda_client.invoke(
    FunctionName='my-function',
    InvocationType='RequestResponse',
    Payload=json.dumps({'key': 'value'})
)
result = json.loads(response['Payload'].read())
\`\`\`

## Terraform AWS Resources

\`\`\`hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "golden-armada-vpc"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = "golden-armada-cluster"
  role_arn = aws_iam_role.cluster.arn
  version  = "1.28"

  vpc_config {
    subnet_ids = aws_subnet.private[*].id
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier        = "golden-armada-db"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.medium"
  allocated_storage = 20

  db_name  = "golden_armada"
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  skip_final_snapshot = true
}
\`\`\`

## Best Practices

1. **Use IAM Roles** instead of access keys
2. **Enable CloudTrail** for audit logging
3. **Tag all resources** for cost tracking
4. **Use VPC** for network isolation
5. **Enable encryption** at rest and in transit
6. **Implement least privilege** IAM policies
