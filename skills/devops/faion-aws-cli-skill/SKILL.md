---
name: faion-aws-cli-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS CLI Skill

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Purpose

Provides AWS CLI operations and patterns for cloud infrastructure management. Covers compute, storage, serverless, containers, databases, infrastructure as code, identity management, and monitoring.

---

## Configuration

### AWS CLI Installation

```bash
# Install AWS CLI v2 (Linux)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

### Profile Management

```bash
# Configure default profile
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json

# Configure named profile
aws configure --profile production

# List profiles
aws configure list-profiles

# Use specific profile
aws s3 ls --profile production

# Set default profile for session
export AWS_PROFILE=production
```

### Environment Variables

```bash
# Authentication
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-session-token"  # For temporary credentials

# Region
export AWS_DEFAULT_REGION="us-east-1"
export AWS_REGION="us-east-1"

# Output format
export AWS_DEFAULT_OUTPUT="json"  # json | text | table | yaml
```

### Credentials File

```ini
# ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[production]
aws_access_key_id = PROD_ACCESS_KEY
aws_secret_access_key = PROD_SECRET_KEY

[development]
role_arn = arn:aws:iam::123456789012:role/DevRole
source_profile = default
```

### Config File

```ini
# ~/.aws/config
[default]
region = us-east-1
output = json
cli_pager = less

[profile production]
region = eu-west-1
output = table

[profile development]
region = us-west-2
role_arn = arn:aws:iam::123456789012:role/DevRole
source_profile = default
```

---

## EC2 (Elastic Compute Cloud)

### Instance Management

```bash
# List all instances
aws ec2 describe-instances

# List instances with specific filter
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress]" \
    --output table

# Launch instance
aws ec2 run-instances \
    --image-id ami-0123456789abcdef0 \
    --instance-type t3.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-0123456789abcdef0 \
    --count 1 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-instance}]'

# Start/stop/terminate instances
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# Reboot instance
aws ec2 reboot-instances --instance-ids i-0123456789abcdef0

# Get instance status
aws ec2 describe-instance-status --instance-ids i-0123456789abcdef0

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids i-0123456789abcdef0
```

### Security Groups

```bash
# List security groups
aws ec2 describe-security-groups

# Create security group
aws ec2 create-security-group \
    --group-name my-sg \
    --description "My security group" \
    --vpc-id vpc-0123456789abcdef0

# Add inbound rule (SSH)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 10.0.0.0/8

# Add inbound rule (HTTPS)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Remove inbound rule
aws ec2 revoke-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 10.0.0.0/8

# Delete security group
aws ec2 delete-security-group --group-id sg-0123456789abcdef0
```

### Key Pairs

```bash
# List key pairs
aws ec2 describe-key-pairs

# Create key pair (save private key)
aws ec2 create-key-pair \
    --key-name my-key-pair \
    --query 'KeyMaterial' \
    --output text > my-key-pair.pem
chmod 400 my-key-pair.pem

# Import existing public key
aws ec2 import-key-pair \
    --key-name my-key-pair \
    --public-key-material fileb://~/.ssh/id_rsa.pub

# Delete key pair
aws ec2 delete-key-pair --key-name my-key-pair
```

### AMI Management

```bash
# List AMIs (owned by you)
aws ec2 describe-images --owners self

# Create AMI from instance
aws ec2 create-image \
    --instance-id i-0123456789abcdef0 \
    --name "my-ami-$(date +%Y%m%d)" \
    --description "My AMI" \
    --no-reboot

# Copy AMI to another region
aws ec2 copy-image \
    --source-image-id ami-0123456789abcdef0 \
    --source-region us-east-1 \
    --region eu-west-1 \
    --name "my-ami-copy"

# Deregister AMI
aws ec2 deregister-image --image-id ami-0123456789abcdef0

# Delete associated snapshot
aws ec2 delete-snapshot --snapshot-id snap-0123456789abcdef0
```

### Elastic IPs

```bash
# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Associate with instance
aws ec2 associate-address \
    --instance-id i-0123456789abcdef0 \
    --allocation-id eipalloc-0123456789abcdef0

# Disassociate
aws ec2 disassociate-address --association-id eipassoc-0123456789abcdef0

# Release Elastic IP
aws ec2 release-address --allocation-id eipalloc-0123456789abcdef0
```

---

## S3 (Simple Storage Service)

### Bucket Operations

```bash
# List buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-bucket-name

# Create bucket in specific region
aws s3 mb s3://my-bucket-name --region eu-west-1

# Delete empty bucket
aws s3 rb s3://my-bucket-name

# Delete bucket with contents
aws s3 rb s3://my-bucket-name --force

# List bucket contents
aws s3 ls s3://my-bucket-name
aws s3 ls s3://my-bucket-name --recursive
aws s3 ls s3://my-bucket-name --recursive --human-readable --summarize
```

### Object Operations

```bash
# Upload file
aws s3 cp file.txt s3://my-bucket/file.txt

# Upload with metadata
aws s3 cp file.txt s3://my-bucket/file.txt \
    --metadata '{"key":"value"}' \
    --content-type "text/plain"

# Download file
aws s3 cp s3://my-bucket/file.txt ./file.txt

# Copy between buckets
aws s3 cp s3://source-bucket/file.txt s3://dest-bucket/file.txt

# Move object
aws s3 mv s3://my-bucket/old-name.txt s3://my-bucket/new-name.txt

# Delete object
aws s3 rm s3://my-bucket/file.txt

# Delete all objects with prefix
aws s3 rm s3://my-bucket/folder/ --recursive

# Sync directories
aws s3 sync ./local-folder s3://my-bucket/folder
aws s3 sync s3://my-bucket/folder ./local-folder
aws s3 sync ./local-folder s3://my-bucket/folder --delete  # Mirror sync
```

### Presigned URLs

```bash
# Generate presigned URL for download (default 1 hour)
aws s3 presign s3://my-bucket/file.txt

# Generate presigned URL with custom expiry (seconds)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600
```

### Bucket Versioning

```bash
# Enable versioning
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled

# Get versioning status
aws s3api get-bucket-versioning --bucket my-bucket

# List object versions
aws s3api list-object-versions --bucket my-bucket

# Delete specific version
aws s3api delete-object \
    --bucket my-bucket \
    --key file.txt \
    --version-id "version-id"
```

### Lifecycle Policies

```bash
# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-bucket \
    --lifecycle-configuration file://lifecycle.json

# lifecycle.json example:
# {
#   "Rules": [
#     {
#       "ID": "Move to Glacier after 90 days",
#       "Status": "Enabled",
#       "Filter": { "Prefix": "logs/" },
#       "Transitions": [
#         { "Days": 90, "StorageClass": "GLACIER" }
#       ],
#       "Expiration": { "Days": 365 }
#     }
#   ]
# }

# Get lifecycle configuration
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket
```

### Bucket Policy

```bash
# Set bucket policy
aws s3api put-bucket-policy \
    --bucket my-bucket \
    --policy file://policy.json

# Get bucket policy
aws s3api get-bucket-policy --bucket my-bucket

# Delete bucket policy
aws s3api delete-bucket-policy --bucket my-bucket
```

---

## Lambda

### Function Management

```bash
# List functions
aws lambda list-functions

# Get function configuration
aws lambda get-function --function-name my-function

# Create function from zip
aws lambda create-function \
    --function-name my-function \
    --runtime python3.11 \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 256

# Update function code
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip

# Update function configuration
aws lambda update-function-configuration \
    --function-name my-function \
    --timeout 60 \
    --memory-size 512 \
    --environment "Variables={KEY1=value1,KEY2=value2}"

# Delete function
aws lambda delete-function --function-name my-function
```

### Invocation

```bash
# Invoke function synchronously
aws lambda invoke \
    --function-name my-function \
    --payload '{"key": "value"}' \
    --cli-binary-format raw-in-base64-out \
    response.json

# Invoke function asynchronously
aws lambda invoke \
    --function-name my-function \
    --invocation-type Event \
    --payload '{"key": "value"}' \
    --cli-binary-format raw-in-base64-out \
    response.json

# View logs (requires log-type)
aws lambda invoke \
    --function-name my-function \
    --log-type Tail \
    --payload '{}' \
    --cli-binary-format raw-in-base64-out \
    response.json \
    --query 'LogResult' --output text | base64 -d
```

### Layer Management

```bash
# List layers
aws lambda list-layers

# Publish layer version
aws lambda publish-layer-version \
    --layer-name my-layer \
    --description "My layer" \
    --zip-file fileb://layer.zip \
    --compatible-runtimes python3.11 python3.10

# Add layer to function
aws lambda update-function-configuration \
    --function-name my-function \
    --layers arn:aws:lambda:us-east-1:123456789012:layer:my-layer:1

# Delete layer version
aws lambda delete-layer-version \
    --layer-name my-layer \
    --version-number 1
```

### Event Source Mappings

```bash
# List event source mappings
aws lambda list-event-source-mappings --function-name my-function

# Create SQS trigger
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:sqs:us-east-1:123456789012:my-queue \
    --batch-size 10

# Create DynamoDB Streams trigger
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:dynamodb:us-east-1:123456789012:table/my-table/stream/... \
    --starting-position LATEST \
    --batch-size 100

# Delete event source mapping
aws lambda delete-event-source-mapping --uuid "uuid-here"
```

### Aliases and Versions

```bash
# Publish version
aws lambda publish-version \
    --function-name my-function \
    --description "v1.0.0"

# Create alias
aws lambda create-alias \
    --function-name my-function \
    --name prod \
    --function-version 1

# Update alias (for blue-green deployment)
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --function-version 2 \
    --routing-config AdditionalVersionWeights={"1"=0.1}  # 10% traffic to v1
```

---

## RDS (Relational Database Service)

### Instance Management

```bash
# List DB instances
aws rds describe-db-instances

# Get specific instance
aws rds describe-db-instances \
    --db-instance-identifier my-database \
    --query "DBInstances[0].[DBInstanceIdentifier,DBInstanceStatus,Endpoint.Address]"

# Create DB instance
aws rds create-db-instance \
    --db-instance-identifier my-database \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username admin \
    --master-user-password "SecurePassword123!" \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-0123456789abcdef0 \
    --db-subnet-group-name my-subnet-group \
    --backup-retention-period 7 \
    --storage-encrypted \
    --multi-az

# Modify instance
aws rds modify-db-instance \
    --db-instance-identifier my-database \
    --db-instance-class db.t3.small \
    --apply-immediately

# Start/stop instance
aws rds start-db-instance --db-instance-identifier my-database
aws rds stop-db-instance --db-instance-identifier my-database

# Reboot instance
aws rds reboot-db-instance --db-instance-identifier my-database

# Delete instance
aws rds delete-db-instance \
    --db-instance-identifier my-database \
    --skip-final-snapshot
```

### Snapshots

```bash
# List snapshots
aws rds describe-db-snapshots --db-instance-identifier my-database

# Create snapshot
aws rds create-db-snapshot \
    --db-instance-identifier my-database \
    --db-snapshot-identifier my-snapshot-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier my-restored-database \
    --db-snapshot-identifier my-snapshot

# Copy snapshot to another region
aws rds copy-db-snapshot \
    --source-db-snapshot-identifier arn:aws:rds:us-east-1:123456789012:snapshot:my-snapshot \
    --target-db-snapshot-identifier my-snapshot-copy \
    --source-region us-east-1 \
    --region eu-west-1

# Delete snapshot
aws rds delete-db-snapshot --db-snapshot-identifier my-snapshot
```

### Parameter Groups

```bash
# List parameter groups
aws rds describe-db-parameter-groups

# Create parameter group
aws rds create-db-parameter-group \
    --db-parameter-group-name my-params \
    --db-parameter-group-family postgres15 \
    --description "My parameter group"

# Modify parameters
aws rds modify-db-parameter-group \
    --db-parameter-group-name my-params \
    --parameters "ParameterName=max_connections,ParameterValue=200,ApplyMethod=pending-reboot"

# Apply parameter group to instance
aws rds modify-db-instance \
    --db-instance-identifier my-database \
    --db-parameter-group-name my-params
```

### Aurora Clusters

```bash
# Create Aurora cluster
aws rds create-db-cluster \
    --db-cluster-identifier my-aurora-cluster \
    --engine aurora-postgresql \
    --engine-version 15.4 \
    --master-username admin \
    --master-user-password "SecurePassword123!" \
    --vpc-security-group-ids sg-0123456789abcdef0 \
    --db-subnet-group-name my-subnet-group

# Add instance to cluster
aws rds create-db-instance \
    --db-instance-identifier my-aurora-instance \
    --db-instance-class db.r6g.large \
    --engine aurora-postgresql \
    --db-cluster-identifier my-aurora-cluster

# Failover cluster
aws rds failover-db-cluster --db-cluster-identifier my-aurora-cluster
```

---

## ECS (Elastic Container Service)

### Cluster Management

```bash
# List clusters
aws ecs list-clusters

# Describe cluster
aws ecs describe-clusters --clusters my-cluster

# Create cluster
aws ecs create-cluster \
    --cluster-name my-cluster \
    --capacity-providers FARGATE FARGATE_SPOT \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1

# Delete cluster
aws ecs delete-cluster --cluster my-cluster
```

### Task Definitions

```bash
# List task definitions
aws ecs list-task-definitions

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# task-definition.json example:
# {
#   "family": "my-app",
#   "networkMode": "awsvpc",
#   "containerDefinitions": [
#     {
#       "name": "app",
#       "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest",
#       "portMappings": [{ "containerPort": 8080, "protocol": "tcp" }],
#       "logConfiguration": {
#         "logDriver": "awslogs",
#         "options": {
#           "awslogs-group": "/ecs/my-app",
#           "awslogs-region": "us-east-1",
#           "awslogs-stream-prefix": "ecs"
#         }
#       }
#     }
#   ],
#   "requiresCompatibilities": ["FARGATE"],
#   "cpu": "256",
#   "memory": "512",
#   "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"
# }

# Describe task definition
aws ecs describe-task-definition --task-definition my-app

# Deregister task definition
aws ecs deregister-task-definition --task-definition my-app:1
```

### Services

```bash
# List services
aws ecs list-services --cluster my-cluster

# Create service
aws ecs create-service \
    --cluster my-cluster \
    --service-name my-service \
    --task-definition my-app:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-123,subnet-456],securityGroups=[sg-789],assignPublicIp=ENABLED}" \
    --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=app,containerPort=8080

# Update service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --task-definition my-app:2 \
    --desired-count 3 \
    --force-new-deployment

# Delete service
aws ecs delete-service \
    --cluster my-cluster \
    --service my-service \
    --force
```

### Tasks

```bash
# List running tasks
aws ecs list-tasks --cluster my-cluster

# Run standalone task
aws ecs run-task \
    --cluster my-cluster \
    --task-definition my-app:1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-123],securityGroups=[sg-789],assignPublicIp=ENABLED}"

# Stop task
aws ecs stop-task --cluster my-cluster --task arn:aws:ecs:...:task/my-cluster/task-id

# Execute command in container (requires ECS Exec enabled)
aws ecs execute-command \
    --cluster my-cluster \
    --task task-id \
    --container app \
    --interactive \
    --command "/bin/bash"
```

### ECR (Elastic Container Registry)

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name my-app

# List repositories
aws ecr describe-repositories

# List images
aws ecr list-images --repository-name my-app

# Delete image
aws ecr batch-delete-image \
    --repository-name my-app \
    --image-ids imageTag=latest

# Delete repository
aws ecr delete-repository --repository-name my-app --force
```

---

## EKS (Elastic Kubernetes Service)

### Cluster Management

```bash
# List clusters
aws eks list-clusters

# Describe cluster
aws eks describe-cluster --name my-cluster

# Create cluster
aws eks create-cluster \
    --name my-cluster \
    --role-arn arn:aws:iam::123456789012:role/eks-cluster-role \
    --resources-vpc-config subnetIds=subnet-123,subnet-456,securityGroupIds=sg-789

# Update kubeconfig
aws eks update-kubeconfig --name my-cluster --region us-east-1

# Delete cluster
aws eks delete-cluster --name my-cluster
```

### Node Groups

```bash
# List node groups
aws eks list-nodegroups --cluster-name my-cluster

# Create node group
aws eks create-nodegroup \
    --cluster-name my-cluster \
    --nodegroup-name my-nodes \
    --node-role arn:aws:iam::123456789012:role/eks-node-role \
    --subnets subnet-123 subnet-456 \
    --instance-types t3.medium \
    --scaling-config minSize=2,maxSize=10,desiredSize=3

# Update node group
aws eks update-nodegroup-config \
    --cluster-name my-cluster \
    --nodegroup-name my-nodes \
    --scaling-config minSize=2,maxSize=20,desiredSize=5

# Delete node group
aws eks delete-nodegroup \
    --cluster-name my-cluster \
    --nodegroup-name my-nodes
```

### Add-ons

```bash
# List add-ons
aws eks list-addons --cluster-name my-cluster

# Create add-on
aws eks create-addon \
    --cluster-name my-cluster \
    --addon-name vpc-cni \
    --addon-version v1.15.0-eksbuild.2

# Update add-on
aws eks update-addon \
    --cluster-name my-cluster \
    --addon-name vpc-cni \
    --addon-version v1.16.0-eksbuild.1

# Delete add-on
aws eks delete-addon \
    --cluster-name my-cluster \
    --addon-name vpc-cni
```

---

## CloudFormation

### Stack Management

```bash
# List stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE

# Describe stack
aws cloudformation describe-stacks --stack-name my-stack

# Create stack
aws cloudformation create-stack \
    --stack-name my-stack \
    --template-body file://template.yaml \
    --parameters ParameterKey=Environment,ParameterValue=production \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --tags Key=Project,Value=MyProject

# Create stack from S3
aws cloudformation create-stack \
    --stack-name my-stack \
    --template-url https://s3.amazonaws.com/my-bucket/template.yaml

# Update stack
aws cloudformation update-stack \
    --stack-name my-stack \
    --template-body file://template.yaml \
    --parameters ParameterKey=Environment,ParameterValue=production

# Delete stack
aws cloudformation delete-stack --stack-name my-stack

# Wait for stack creation
aws cloudformation wait stack-create-complete --stack-name my-stack
```

### Change Sets

```bash
# Create change set
aws cloudformation create-change-set \
    --stack-name my-stack \
    --change-set-name my-changes \
    --template-body file://template.yaml \
    --parameters ParameterKey=Environment,ParameterValue=staging

# Describe change set
aws cloudformation describe-change-set \
    --stack-name my-stack \
    --change-set-name my-changes

# Execute change set
aws cloudformation execute-change-set \
    --stack-name my-stack \
    --change-set-name my-changes

# Delete change set
aws cloudformation delete-change-set \
    --stack-name my-stack \
    --change-set-name my-changes
```

### Stack Outputs and Events

```bash
# Get stack outputs
aws cloudformation describe-stacks \
    --stack-name my-stack \
    --query "Stacks[0].Outputs"

# Get stack events (for debugging)
aws cloudformation describe-stack-events \
    --stack-name my-stack \
    --query "StackEvents[?ResourceStatus=='CREATE_FAILED']"

# Get stack resources
aws cloudformation list-stack-resources --stack-name my-stack
```

### Template Validation

```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Estimate cost
aws cloudformation estimate-template-cost --template-body file://template.yaml
```

---

## IAM (Identity and Access Management)

### User Management

```bash
# List users
aws iam list-users

# Create user
aws iam create-user --user-name my-user

# Delete user
aws iam delete-user --user-name my-user

# Create access key
aws iam create-access-key --user-name my-user

# List access keys
aws iam list-access-keys --user-name my-user

# Delete access key
aws iam delete-access-key --user-name my-user --access-key-id AKIAIOSFODNN7EXAMPLE

# Add user to group
aws iam add-user-to-group --user-name my-user --group-name developers
```

### Role Management

```bash
# List roles
aws iam list-roles

# Create role
aws iam create-role \
    --role-name my-role \
    --assume-role-policy-document file://trust-policy.json

# trust-policy.json example:
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": { "Service": "lambda.amazonaws.com" },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }

# Attach managed policy to role
aws iam attach-role-policy \
    --role-name my-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Attach inline policy to role
aws iam put-role-policy \
    --role-name my-role \
    --policy-name my-inline-policy \
    --policy-document file://policy.json

# Assume role (get temporary credentials)
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/my-role \
    --role-session-name my-session

# Delete role
aws iam delete-role --role-name my-role
```

### Policy Management

```bash
# List policies
aws iam list-policies --scope Local  # Custom policies only

# Create policy
aws iam create-policy \
    --policy-name my-policy \
    --policy-document file://policy.json

# policy.json example:
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "s3:GetObject",
#         "s3:PutObject"
#       ],
#       "Resource": "arn:aws:s3:::my-bucket/*"
#     }
#   ]
# }

# Get policy version
aws iam get-policy-version \
    --policy-arn arn:aws:iam::123456789012:policy/my-policy \
    --version-id v1

# Create new policy version
aws iam create-policy-version \
    --policy-arn arn:aws:iam::123456789012:policy/my-policy \
    --policy-document file://new-policy.json \
    --set-as-default

# Delete policy
aws iam delete-policy --policy-arn arn:aws:iam::123456789012:policy/my-policy
```

### Permission Boundaries

```bash
# Set permission boundary on user
aws iam put-user-permissions-boundary \
    --user-name my-user \
    --permissions-boundary arn:aws:iam::123456789012:policy/my-boundary

# Set permission boundary on role
aws iam put-role-permissions-boundary \
    --role-name my-role \
    --permissions-boundary arn:aws:iam::123456789012:policy/my-boundary
```

### Service Roles

```bash
# Create service-linked role
aws iam create-service-linked-role --aws-service-name elasticmapreduce.amazonaws.com

# Get service-linked role
aws iam get-role --role-name AWSServiceRoleForAmazonEMR
```

---

## CloudWatch

### Logs

```bash
# List log groups
aws logs describe-log-groups

# Create log group
aws logs create-log-group --log-group-name /my-app/logs

# Delete log group
aws logs delete-log-group --log-group-name /my-app/logs

# List log streams
aws logs describe-log-streams \
    --log-group-name /my-app/logs \
    --order-by LastEventTime \
    --descending

# Get log events
aws logs get-log-events \
    --log-group-name /my-app/logs \
    --log-stream-name my-stream \
    --limit 100

# Filter log events
aws logs filter-log-events \
    --log-group-name /my-app/logs \
    --filter-pattern "ERROR" \
    --start-time $(date -d '1 hour ago' +%s)000

# Tail logs (live)
aws logs tail /my-app/logs --follow

# Put log events
aws logs put-log-events \
    --log-group-name /my-app/logs \
    --log-stream-name my-stream \
    --log-events timestamp=$(date +%s)000,message="Test log"

# Set retention
aws logs put-retention-policy \
    --log-group-name /my-app/logs \
    --retention-in-days 30
```

### Metrics

```bash
# List metrics
aws cloudwatch list-metrics --namespace AWS/EC2

# Get metric statistics
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
    --period 300 \
    --statistics Average Maximum

# Put custom metric
aws cloudwatch put-metric-data \
    --namespace MyApp \
    --metric-name RequestCount \
    --value 100 \
    --unit Count \
    --dimensions Environment=production
```

### Alarms

```bash
# List alarms
aws cloudwatch describe-alarms

# Create alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "High CPU" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic

# Delete alarm
aws cloudwatch delete-alarms --alarm-names "High CPU"

# Set alarm state (for testing)
aws cloudwatch set-alarm-state \
    --alarm-name "High CPU" \
    --state-value ALARM \
    --state-reason "Testing alarm"
```

### Dashboards

```bash
# List dashboards
aws cloudwatch list-dashboards

# Get dashboard
aws cloudwatch get-dashboard --dashboard-name my-dashboard

# Put dashboard
aws cloudwatch put-dashboard \
    --dashboard-name my-dashboard \
    --dashboard-body file://dashboard.json

# Delete dashboard
aws cloudwatch delete-dashboards --dashboard-names my-dashboard
```

### Log Insights

```bash
# Start query
aws logs start-query \
    --log-group-name /my-app/logs \
    --start-time $(date -d '1 hour ago' +%s) \
    --end-time $(date +%s) \
    --query-string "fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 100"

# Get query results
aws logs get-query-results --query-id "query-id-here"
```

---

## Security Best Practices

### Credential Management

```bash
# Never hardcode credentials - use IAM roles when possible
# Use environment variables or AWS profiles

# Rotate access keys regularly
aws iam create-access-key --user-name my-user
aws iam delete-access-key --user-name my-user --access-key-id OLD_KEY

# Use MFA
aws iam enable-mfa-device \
    --user-name my-user \
    --serial-number arn:aws:iam::123456789012:mfa/my-user \
    --authentication-code1 123456 \
    --authentication-code2 789012
```

### Least Privilege

```bash
# Use AWS Access Analyzer to find unused permissions
aws accessanalyzer list-analyzers

# Generate policy based on CloudTrail activity
aws accessanalyzer generate-policy \
    --principal-arn arn:aws:iam::123456789012:user/my-user \
    --policy-type-name IDENTITY_POLICY

# Use condition keys in policies
# Example: Restrict by source IP, MFA, time
```

### Encryption

```bash
# Enable S3 bucket encryption
aws s3api put-bucket-encryption \
    --bucket my-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "arn:aws:kms:us-east-1:123456789012:key/key-id"
            }
        }]
    }'

# Enable RDS encryption at creation (cannot enable later)
# Use --storage-encrypted flag

# Enable EBS encryption by default
aws ec2 enable-ebs-encryption-by-default
```

### Logging and Monitoring

```bash
# Enable CloudTrail
aws cloudtrail create-trail \
    --name my-trail \
    --s3-bucket-name my-trail-bucket \
    --is-multi-region-trail

# Enable VPC Flow Logs
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids vpc-0123456789abcdef0 \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name vpc-flow-logs

# Enable S3 access logging
aws s3api put-bucket-logging \
    --bucket my-bucket \
    --bucket-logging-status '{
        "LoggingEnabled": {
            "TargetBucket": "my-logs-bucket",
            "TargetPrefix": "s3-access-logs/"
        }
    }'
```

---

## Common Patterns

### Deployment Pipeline

```bash
# Build and push Docker image
docker build -t my-app:latest .
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker tag my-app:latest $ECR_URI/my-app:latest
docker push $ECR_URI/my-app:latest

# Update ECS service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --force-new-deployment

# Wait for deployment
aws ecs wait services-stable --cluster my-cluster --services my-service
```

### Blue-Green Deployment

```bash
# Deploy new version to green environment
aws lambda update-function-code --function-name my-function --zip-file fileb://new.zip
aws lambda publish-version --function-name my-function

# Shift traffic gradually
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --routing-config AdditionalVersionWeights={"1"=0.1}  # 10% to new version

# Complete switch
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --function-version 2
```

### Disaster Recovery

```bash
# Copy snapshot to another region
aws rds copy-db-snapshot \
    --source-db-snapshot-identifier arn:aws:rds:us-east-1:123456789012:snapshot:my-snapshot \
    --target-db-snapshot-identifier my-snapshot-dr \
    --source-region us-east-1 \
    --region eu-west-1

# Copy AMI to another region
aws ec2 copy-image \
    --source-image-id ami-0123456789abcdef0 \
    --source-region us-east-1 \
    --region eu-west-1 \
    --name "my-ami-dr"

# S3 cross-region replication (via bucket policy)
```

### Cost Optimization

```bash
# Find unused Elastic IPs
aws ec2 describe-addresses \
    --query "Addresses[?AssociationId==null]"

# Find old snapshots
aws ec2 describe-snapshots \
    --owner-ids self \
    --query "Snapshots[?StartTime<='$(date -d '90 days ago' +%Y-%m-%d)']"

# Find stopped instances
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=stopped" \
    --query "Reservations[*].Instances[*].[InstanceId,Tags[?Key=='Name'].Value|[0]]"

# Get Cost Explorer data
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics BlendedCost
```

---

## Output Formatting

### Query Examples

```bash
# JMESPath queries
--query "Reservations[*].Instances[*].[InstanceId,State.Name]"
--query "Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}"
--query "Reservations[?Instances[?State.Name=='running']]"

# Output formats
--output json   # Default, machine-readable
--output table  # Human-readable tables
--output text   # Tab-separated, for scripting
--output yaml   # YAML format
```

### Pagination

```bash
# Handle pagination automatically
aws s3api list-objects-v2 --bucket my-bucket --max-items 1000

# Manual pagination
aws s3api list-objects-v2 --bucket my-bucket --max-items 100
# Use NextToken from output for next page
aws s3api list-objects-v2 --bucket my-bucket --starting-token <NextToken>
```

---

## Troubleshooting

### Debug Mode

```bash
# Enable debug output
aws s3 ls --debug

# Check configuration
aws configure list

# Check identity
aws sts get-caller-identity

# Check permissions (simulate)
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:user/my-user \
    --action-names s3:GetObject \
    --resource-arns arn:aws:s3:::my-bucket/*
```

### Common Errors

```bash
# ExpiredToken - refresh credentials or re-authenticate
aws sts get-session-token

# AccessDenied - check IAM policies, resource policies, SCPs
# Use CloudTrail to find denied actions

# ThrottlingException - implement exponential backoff
# Use --cli-connect-timeout and --cli-read-timeout
```

---

*AWS CLI Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*
