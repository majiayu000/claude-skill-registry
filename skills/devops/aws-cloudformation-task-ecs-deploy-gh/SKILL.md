---
name: aws-cloudformation-task-ecs-deploy-gh
description: Deploy ECS tasks and services with GitHub Actions CI/CD. Use for building Docker images, pushing to ECR, updating ECS task definitions, deploying ECS services, integrating with CloudFormation stacks, configuring AWS OIDC authentication for GitHub Actions, and implementing production-ready container deployment pipelines. Automate ECS deployments with proper security (OIDC or IAM keys), multi-environment support, blue/green deployments, ECR private repositories with image scanning, and CloudFormation infrastructure updates.
category: aws
tags: [aws, cloudformation, github-actions, ecs, ecr, deployment, ci-cd, oidc, containers, docker, cd]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Task ECS Deploy with GitHub Actions

Comprehensive skill for deploying ECS containers using GitHub Actions CI/CD pipelines with CloudFormation infrastructure management.

## Overview

Deploy containerized applications to Amazon ECS using GitHub Actions workflows. This skill covers the complete deployment pipeline: authentication with AWS (OIDC recommended), building Docker images, pushing to Amazon ECR, updating task definitions, and deploying ECS services. Integrate with CloudFormation for infrastructure-as-code management and implement production-grade deployment strategies.

## When to Use

**Use this skill when:**
- Deploying Docker containers to Amazon ECS
- Setting up GitHub Actions CI/CD pipelines for AWS
- Configuring AWS authentication for GitHub Actions (OIDC or IAM keys)
- Building and pushing Docker images to Amazon ECR
- Updating ECS task definitions dynamically
- Implementing blue/green or rolling deployments
- Managing CloudFormation stacks from CI/CD
- Setting up multi-environment deployments (dev/staging/prod)
- Configuring private ECR repositories with image scanning
- Automating container deployment with proper security practices

**Trigger phrases:**
- "Deploy to ECS with GitHub Actions"
- "Set up CI/CD for ECS containers"
- "Configure GitHub Actions for AWS deployment"
- "Build and push Docker image to ECR"
- "Update ECS task definition from CI/CD"
- "Implement blue/green deployment for ECS"
- "Deploy CloudFormation stack from GitHub Actions"

## Quick Start

### Basic ECS Deployment Workflow

```yaml
name: Deploy to ECS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-ecs-role
          aws-region: us-east-1

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: my-app
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Update task definition
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        id: render-task
        with:
          task-definition: task-definition.json
          container-name: my-app
          image: ${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.render-task.outputs.task-definition }}
          service: my-service
          cluster: my-cluster
          wait-for-service-stability: true
```

## Authentication Methods

### OIDC Authentication (Recommended)

OpenID Connect (OIDC) provides secure, passwordless authentication between GitHub Actions and AWS.

**Prerequisites:**

1. Create IAM role with trust policy for GitHub:

```yaml
Type: AWS::IAM::Role
Properties:
  RoleName: github-actions-ecs-role
  AssumeRolePolicyDocument:
    Version: '2012-10-17'
    Statement:
      - Effect: Allow
        Principal:
          Federated: !Sub 'arn:aws:iam::${AWS::AccountId}:oidc-provider/token.actions.githubusercontent.com'
        Action: sts:AssumeRoleWithWebIdentity
        Condition:
          StringEquals:
            token.actions.githubusercontent.com:aud: sts.amazonaws.com
          StringLike:
            token.actions.githubusercontent.com:sub: repo:my-org/my-repo:*
  ManagedPolicyArns:
    - arn:aws:iam::aws:policy/AmazonECS_FullAccess
    - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
```

2. Configure GitHub Actions workflow:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/github-actions-ecs-role
    aws-region: us-east-1
```

### IAM Key Authentication (Legacy)

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

Store credentials in GitHub repository secrets (Settings → Secrets and variables → Actions).

## Build and Push to ECR

### ECR Repository CloudFormation Template

```yaml
ECRRepository:
  Type: AWS::ECR::Repository
  Properties:
    RepositoryName: my-app
    ImageScanningConfiguration:
      ScanOnPush: true
    ImageTagMutability: IMMUTABLE
    LifecyclePolicy:
      LifecyclePolicyText: |
        {
          "rules": [
            {
              "rulePriority": 1,
              "description": "Keep last 30 images",
              "selection": {
                "tagStatus": "tagged",
                "tagPrefixList": ["v"],
                "countType": "imageCountMoreThan",
                "countNumber": 30
              },
              "action": {
                "type": "expire"
              }
            }
          ]
        }
```

### Build and Push Step

```yaml
- name: Login to ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v2

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: |
      ${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}
      ${{ steps.login-ecr.outputs.registry }}/my-app:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
    build-args: |
      BUILD_DATE=${{ github.event.head_commit.timestamp }}
      VERSION=${{ github.sha }}
```

## Task Definition Management

### Basic Task Definition

**task-definition.json:**

```json
{
  "family": "my-app-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "PLACEHOLDER_IMAGE",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:my-app/db-password"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs",
          "awslogs-create-group": "true"
        }
      }
    }
  ]
}
```

### Dynamic Task Definition Update

```yaml
- name: Render task definition
  uses: aws-actions/amazon-ecs-render-task-definition@v1
  id: render-task
  with:
    task-definition: task-definition.json
    container-name: my-app
    image: ${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}

- name: Deploy task definition
  uses: aws-actions/amazon-ecs-deploy-task-definition@v1
  with:
    task-definition: ${{ steps.render-task.outputs.task-definition }}
    service: my-service
    cluster: my-cluster
    wait-for-service-stability: true
    deploy_timeout: 30 minutes
```

## ECS Deployment Strategies

### Rolling Deployment (Default)

```yaml
- name: Deploy to ECS (Rolling)
  uses: aws-actions/amazon-ecs-deploy-task-definition@v1
  with:
    task-definition: ${{ steps.render-task.outputs.task-definition }}
    service: my-service
    cluster: my-cluster
    wait-for-service-stability: true
```

**CloudFormation Service Configuration:**

```yaml
ECSService:
  Type: AWS::ECS::Service
  Properties:
    ServiceName: my-service
    Cluster: !Ref ECSCluster
    TaskDefinition: !Ref TaskDefinition
    DeploymentConfiguration:
      MaximumPercent: 200
      MinimumHealthyPercent: 100
      DeploymentCircuitBreaker:
        Enable: true
        Rollback: true
    HealthCheckGracePeriodSeconds: 60
    EnableECSManagedTags: true
    PropagateTags: SERVICE
```

### Blue/Green Deployment with CodeDeploy

```yaml
- name: Deploy to ECS (Blue/Green)
  uses: aws-actions/amazon-ecs-deploy-task-definition@v1
  with:
    task-definition: ${{ steps.render-task.outputs.task-definition }}
    service: my-service
    cluster: my-cluster
    codedeploy-appspec: appspec.yaml
    codedeploy-application: my-app
    codedeploy-deployment-group: my-deployment-group
    wait-for-service-stability: true
```

**appspec.yaml:**

```yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: <TASK_DEFINITION>
        LoadBalancerInfo:
          ContainerName: my-app
          ContainerPort: 8080
        PlatformVersion: "1.4.0"
```

**CloudFormation CodeDeploy Configuration:**

```yaml
CodeDeployApplication:
  Type: AWS::CodeDeploy::Application
  Properties:
    ApplicationName: my-app
    ComputePlatform: ECS

CodeDeployDeploymentGroup:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: !Ref CodeDeployApplication
    DeploymentGroupName: my-deployment-group
    ServiceRoleArn: !Ref CodeDeployServiceRole
    DeploymentConfigName: CodeDeployDefault.ECSAllAtOnce
    DeploymentStyle:
      DeploymentType: BLUE_GREEN
      DeploymentOption: WITH_TRAFFIC_CONTROL
    AutoRollbackConfiguration:
      Enabled: true
      Events:
        - DEPLOYMENT_FAILURE
        - DEPLOYMENT_STOP_ON_ALARM
        - DEPLOYMENT_STOP_ON_REQUEST
    AlarmConfiguration:
      Alarms:
        - !Ref CPUPercentageAlarm
        - !Ref MemoryPercentageAlarm
    BlueGreenDeploymentConfiguration:
      TerminateBlueInstancesOnDeploymentSuccess:
        Action: TERMINATE
        WaitTimeInMinutes: 5
      DeploymentReadyOption:
        ActionOnTimeout: CONTINUE_DEPLOYMENT
        WaitTimeInMinutes: 0
    LoadBalancerInfo:
      TargetGroupPairInfoList:
        - TargetGroups:
            - Ref: BlueTargetGroup
            - Ref: GreenTargetGroup
          ProdTrafficRoute:
            ListenerArns:
              - !Ref ProductionListener
```

## CloudFormation Integration

### Update Stack from GitHub Actions

```yaml
- name: Deploy CloudFormation stack
  run: |
    aws cloudformation deploy \
      --template-file infrastructure/ecs-stack.yaml \
      --stack-name my-app-ecs \
      --capabilities CAPABILITY_NAMED_IAM \
      --parameter-overrides \
        Environment=production \
        DesiredCount=2 \
        CPU=256 \
        Memory=512 \
        ImageUrl=${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}
```

### CloudFormation Stack with ECS Resources

**ecs-stack.yaml:**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: ECS Fargate Service with CloudFormation

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
  DesiredCount:
    Type: Number
    Default: 2
  CPU:
    Type: String
    Default: '256'
  Memory:
    Type: String
    Default: '512'
  ImageUrl:
    Type: String

Resources:
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub '${Environment}-cluster'
      ClusterSettings:
        - Name: containerInsights
          Value: enabled

  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Sub '${Environment}-task'
      Cpu: !Ref CPU
      Memory: !Ref Memory
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      ExecutionRoleArn: !GetAtt TaskExecutionRole.Arn
      TaskRoleArn: !GetAtt TaskRole.Arn
      ContainerDefinitions:
        - Name: my-app
          Image: !Ref ImageUrl
          PortMappings:
            - ContainerPort: 8080
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: ecs

  ECSService:
    Type: AWS::ECS::Service
    DependsOn: LoadBalancerListener
    Properties:
      ServiceName: !Sub '${Environment}-service'
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: !Ref DesiredCount
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PrivateSubnetA
            - !Ref PrivateSubnetB
          SecurityGroups:
            - !Ref ContainerSecurityGroup
          AssignPublicIp: DISABLED
      LoadBalancers:
        - ContainerName: my-app
          ContainerPort: 8080
          TargetGroupArn: !Ref TargetGroup
      DeploymentConfiguration:
        MaximumPercent: 200
        MinimumHealthyPercent: 100
        DeploymentCircuitBreaker:
          Enable: true
          Rollback: true
      HealthCheckGracePeriodSeconds: 60

Outputs:
  ServiceURL:
    Description: Service URL
    Value: !Sub 'http://${LoadBalancer.DNSName}'
```

### Stack Outputs for Cross-Stack References

```yaml
Outputs:
  ClusterName:
    Description: ECS Cluster Name
    Value: !Ref ECSCluster
    Export:
      Name: !Sub '${AWS::StackName}-ClusterName'

  ServiceName:
    Description: ECS Service Name
    Value: !Ref ECSService
    Export:
      Name: !Sub '${AWS::StackName}-ServiceName'

  TaskDefinitionArn:
    Description: Task Definition ARN
    Value: !Ref TaskDefinition
    Export:
      Name: !Sub '${AWS::StackName}-TaskDefinitionArn'
```

## Best Practices

### Security

1. **Use OIDC authentication** instead of long-lived IAM keys
2. **Implement least privilege IAM roles** with specific permissions
3. **Enable ECR image scanning** on push
4. **Use AWS Secrets Manager** for sensitive data
5. **Encrypt ECR repositories** with KMS
6. **VPC endpoints** for ECR and ECS without internet gateway
7. **Security groups** restrict access to minimum required

### IAM Role Permissions

```yaml
ECSDeployRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Federated: !Sub 'arn:aws:iam::${AWS::AccountId}:oidc-provider/token.actions.githubusercontent.com'
          Action: sts:AssumeRoleWithWebIdentity
          Condition:
            StringEquals:
              token.actions.githubusercontent.com:aud: sts.amazonaws.com
            StringLike:
              token.actions.githubusercontent.com:sub: repo:${GitHubOrg}/${GitHubRepo}:*
    Policies:
      - PolicyName: ECSDeployPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - ecs:DescribeServices
                - ecs:DescribeTaskDefinition
                - ecs:DescribeTasks
                - ecs:ListTasks
                - ecs:RegisterTaskDefinition
                - ecs:UpdateService
              Resource: !Sub 'arn:aws:ecs:${AWS::Region}:${AWS::AccountId}:*'
            - Effect: Allow
              Action:
                - ecr:GetAuthorizationToken
                - ecr:BatchCheckLayerAvailability
                - ecr:GetDownloadUrlForLayer
                - ecr:GetRepositoryPolicy
                - ecr:DescribeRepositories
                - ecr:ListImages
                - ecr:DescribeImages
                - ecr:BatchGetImage
                - ecr:InitiateLayerUpload
                - ecr:UploadLayerPart
                - ecr:CompleteLayerUpload
                - ecr:PutImage
              Resource: !Sub 'arn:aws:ecr:${AWS::Region}:${AWS::AccountId}:repository/${ECRRepositoryName}'
            - Effect: Allow
              Action:
                - cloudformation:DescribeStacks
                - cloudformation:CreateStack
                - cloudformation:UpdateStack
                - cloudformation:DescribeStackEvents
              Resource: !Sub 'arn:aws:cloudformation:${AWS::Region}:${AWS::AccountId}:stack/${CloudFormationStackName}/*'
```

### Performance

1. **Docker layer caching** with GitHub Actions cache
2. **Multi-stage builds** to minimize image size
3. **Parallel deployments** across multiple environments
4. **Fargate Spot** for cost savings on non-critical workloads
5. **CloudWatch Logs** with appropriate retention policies

### Cost Optimization

1. **ECR lifecycle policies** to clean up old images
2. **Fargate Spot** instances for development/testing
3. **Right-sized task CPU and memory**
4. **Auto-scaling** based on metrics
5. **Scheduled scaling** for predictable traffic patterns

### Multi-Environment Deployments

```yaml
name: Deploy to ECS
on:
  push:
    branches: [main, staging, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-ecs-${{ matrix.environment }}
          aws-region: us-east-1

      - name: Deploy to ${{ matrix.environment }}
        run: |
          aws cloudformation deploy \
            --template-file infrastructure/ecs-stack.yaml \
            --stack-name my-app-${{ matrix.environment }} \
            --parameter-overrides \
              Environment=${{ matrix.environment }} \
              ImageUrl=${{ steps.build-image.outputs.image-url }}
```

### Monitoring and Observability

1. **CloudWatch Container Insights** for ECS metrics
2. **Application logs** centralized in CloudWatch Logs
3. **Health checks** with proper grace periods
4. **CloudWatch Alarms** for deployment failures
5. **X-Ray tracing** for distributed tracing

## Further Reading

- [Reference Documentation](./reference.md) - Detailed technical reference for GitHub Actions syntax, OIDC configuration, ECR operations, task definitions, and CloudFormation integration
- [Production Examples](./examples.md) - Complete, production-ready workflows including basic deployments, multi-environment setups, blue/green deployments, private ECR with scanning, CloudFormation stack updates, and full CI/CD pipelines with testing

## Key Concepts

- **GitHub Actions**: Automate workflows from GitHub repository events
- **OIDC Authentication**: Secure, tokenless authentication between GitHub and AWS
- **ECR**: Amazon Elastic Container Registry for Docker image storage
- **ECS**: Amazon Elastic Container Service for container orchestration
- **Fargate**: Serverless compute engine for ECS without managing servers
- **Task Definition**: Blueprint for ECS containers (similar to Pod spec in Kubernetes)
- **Service**: Long-running ECS service with load balancing and auto-scaling
- **CloudFormation**: Infrastructure as Code for AWS resource management
- **Blue/Green Deployment**: Zero-downtime deployment strategy with CodeDeploy

## Common Troubleshooting

**Authentication failures:**
- Verify OIDC trust relationship matches GitHub organization/repository
- Check IAM role has proper permissions for ECR and ECS
- Ensure GitHub Actions repository has `id-token: write` permission

**Deployment failures:**
- Check CloudWatch Logs for application errors
- Verify task definition matches service requirements
- Ensure sufficient CPU/memory in Fargate cluster
- Review health check configuration

**ECR push failures:**
- Verify repository exists and permissions are correct
- Check image tag format and registry URL
- Ensure Docker daemon is running in GitHub Actions runner
- Verify image size doesn't exceed ECR limits

**CloudFormation rollback:**
- Review stack events in AWS Console
- Check parameter values match resource constraints
- Verify IAM role has `cloudformation:UpdateStack` permission
- Enable termination protection for production stacks

## Related Skills

- [aws-cloudformation-ecs](../aws-cloudformation-ecs/) - Design and implement ECS cluster architecture
- [aws-sdk-java-v2-ecs](../../aws-java/aws-sdk-java-v2-ecs/) - Programmatic ECS management with Java SDK
- [aws-cloudformation](../aws-cloudformation/) - Core CloudFormation patterns and best practices
