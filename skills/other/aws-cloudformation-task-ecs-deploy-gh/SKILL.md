---
name: aws-cloudformation-task-ecs-deploy-gh
description: Provides patterns to deploy ECS tasks and services with GitHub Actions CI/CD. Use when building Docker images, pushing to ECR, updating ECS task definitions, deploying ECS services, integrating with CloudFormation stacks, configuring AWS OIDC authentication for GitHub Actions, and implementing production-ready container deployment pipelines. Supports ECS deployments with proper security (OIDC or IAM keys), multi-environment support, blue/green deployments, ECR private repositories with image scanning, and CloudFormation infrastructure updates.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Task ECS Deploy with GitHub Actions

Comprehensive skill for deploying ECS containers using GitHub Actions CI/CD pipelines with CloudFormation infrastructure management.

## Overview

Deploy containerized applications to Amazon ECS using GitHub Actions workflows. This skill covers the complete deployment pipeline: authentication with AWS (OIDC recommended), building Docker images, pushing to Amazon ECR, updating task definitions, and deploying ECS services. Integrate with CloudFormation for infrastructure-as-code management and implement production-grade deployment strategies.

## When to Use

- Deploying Docker containers to Amazon ECS with GitHub Actions
- Setting up CI/CD pipelines for ECS using CloudFormation
- Configuring AWS OIDC authentication for GitHub Actions
- Building Docker images and pushing to Amazon ECR
- Updating ECS task definitions dynamically in CI/CD
- Implementing blue/green or rolling deployments for ECS
- Managing CloudFormation stacks from GitHub Actions

## Instructions

Follow these steps to set up ECS deployment with GitHub Actions:

1. **Configure AWS Authentication**: Set up OIDC provider for GitHub Actions
2. **Create IAM Roles**: Define roles for deployment actions
3. **Set Up ECR Repository**: Create repository with image scanning
4. **Create ECS Cluster**: Define cluster infrastructure
5. **Configure Task Definition**: Set up task and container definitions
6. **Set Up ECS Service**: Configure service with deployment strategy
7. **Create GitHub Workflow**: Define CI/CD pipeline steps
8. **Configure Secrets**: Store credentials securely in GitHub Secrets

## Quick Start

### Basic Deployment Workflow

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
      - uses: actions/checkout@v4

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

      - name: Verify image push
        run: |
          docker pull $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "Image $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG verified"

      - name: Update task definition
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        id: render-task
        with:
          task-definition: task-definition.json
          container-name: my-app
          image: ${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}

      - name: Validate task definition
        run: |
          # Validate JSON syntax
          cat ${{ steps.render-task.outputs.task-definition }} | jq empty && echo "Task definition JSON is valid"
          # Verify container image matches expected
          CONTAINER_IMAGE=$(cat ${{ steps.render-task.outputs.task-definition }} | jq -r '.containerDefinitions[0].image')
          EXPECTED_IMAGE="${{ steps.login-ecr.outputs.registry }}/my-app:${{ github.sha }}"
          if [ "$CONTAINER_IMAGE" = "$EXPECTED_IMAGE" ]; then
            echo "Container image matches expected: $CONTAINER_IMAGE"
          else
            echo "ERROR: Container image mismatch. Expected: $EXPECTED_IMAGE, Got: $CONTAINER_IMAGE"
            exit 1
          fi

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.render-task.outputs.task-definition }}
          service: my-service
          cluster: my-cluster
          wait-for-service-stability: true
```

See [references/workflow-examples.md](references/workflow-examples.md) for complete workflow examples including multi-environment and blue/green deployments.

## Examples

### Multi-Environment Deployment

```yaml
jobs:
  deploy:
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ matrix.env_account }}:role/github-actions-ecs-role
          aws-region: ${{ matrix.region }}
      - name: Deploy to ${{ matrix.environment }}
        run: |
          ECR_REGISTRY=${{ env.ECR_REGISTRY }}
          docker build -t $ECR_REGISTRY/my-app:${{ github.sha }} .
          docker push $ECR_REGISTRY/my-app:${{ github.sha }}
```

### Blue/Green Deployment with CodeDeploy

```yaml
- name: Deploy with CodeDeploy
  run: |
    aws deploy create-deployment \
      --application-name my-app \
      --deployment-group-name ${{ matrix.environment }} \
      --deployment-config-name CodeDeployDefault ECSAllAtOnce \
      --revision "{\"revisionType\":\"AppSpecContent\",\"appSpecContent\":{\"content\":\"$(cat appspec.yml)\",\"filename\":\"appspec.yml\"}}"
    aws deploy wait deployment-successful --deployment-id $(aws deploy list-deployments --application-name my-app --query 'deployments[0]' --output text)
```

See [references/workflow-examples.md](references/workflow-examples.md) for additional patterns including ECR lifecycle policies, task definition templates, and CloudFormation stack updates.

## Best Practices

### Security
1. **Use OIDC authentication** instead of long-lived IAM keys
2. **Implement least privilege IAM roles** with specific permissions
3. **Enable ECR image scanning** on push
4. **Use AWS Secrets Manager** for sensitive data
5. **Encrypt ECR repositories** with KMS
6. **VPC endpoints** for ECR and ECS without internet gateway
7. **Security groups** restrict access to minimum required

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

See [references/best-practices.md](references/best-practices.md) for detailed security, performance, and cost optimization guidelines.

## Common Troubleshooting

### Authentication Failures
- Verify OIDC trust relationship matches GitHub organization/repository
- Check IAM role has proper permissions for ECR and ECS
- Ensure GitHub Actions repository has `id-token: write` permission

### Deployment Failures
- Check CloudWatch Logs for application errors
- Verify task definition matches service requirements
- Ensure sufficient CPU/memory in Fargate cluster
- Review health check configuration

### ECR Push Failures
- Verify repository exists and permissions are correct
- Check image tag format and registry URL
- Ensure Docker daemon is running in GitHub Actions runner
- Verify image size doesn't exceed ECR limits

### CloudFormation Rollback
- Review stack events in AWS Console
- Check parameter values match resource constraints
- Verify IAM role has `cloudformation:UpdateStack` permission
- Enable termination protection for production stacks

See [references/best-practices.md](references/best-practices.md) for complete troubleshooting guide with debug commands.

## Related Skills

- [aws-cloudformation-ecs](../aws-cloudformation-ecs/) - Design and implement ECS cluster architecture
- [aws-cloudformation-lambda](../aws-cloudformation-lambda/) - Deploy Lambda functions with GitHub Actions
- [aws-cloudformation-security](../aws-cloudformation-security/) - Security best practices for ECS deployments

## References

### Complete Examples
- **[references/workflow-examples.md](references/workflow-examples.md)** - Complete GitHub Actions workflows including basic deployment, multi-environment, blue/green, and CI/CD pipelines

### Configuration
- **[references/authentication.md](references/authentication.md)** - OIDC provider setup, IAM roles, cross-account deployment, environment-specific roles
- **[references/ecr-and-task-definitions.md](references/ecr-and-task-definitions.md)** - ECR repository configuration, task definition management, multi-container setups
- **[references/deployment-strategies.md](references/deployment-strategies.md)** - Rolling and blue/green deployments, CloudFormation templates, stack updates

### Best Practices
- **[references/best-practices.md](references/best-practices.md)** - Security guidelines, performance optimization, cost optimization, monitoring, and complete troubleshooting guide

## Constraints and Warnings

### Resource Limits
- **GitHub Actions Limits**: Usage limits per account (minutes, storage)
- **Workflow File Size**: Cannot exceed 1 MB
- **Job Matrix Limits**: Limits on total matrix combinations
- **Artifact Retention**: Default 90-day retention

### Authentication Constraints
- **OIDC Tokens**: Limited lifetime (typically 5 minutes)
- **Role Session Duration**: Maximum 12 hours
- **Permission Scope**: Least-privilege permissions required
- **Cross-Account Access**: Requires appropriate trust relationships

### Operational Constraints
- **Deployment Speed**: CloudFormation deployments may take time
- **Stack Locking**: Cannot update while another deployment is in progress
- **ECR Rate Limits**: API rate limits may affect large deployments
- **ECS Service Limits**: Limits on tasks per service and services per cluster

### Security Constraints
- **Secret Management**: Never store secrets in repository or workflow files
- **OIDC Provider**: Must be configured in AWS account before first use
- **Repository Access**: Workflow secrets are scoped to repository
- **Token Security**: Minimum required permissions only (contents: read, id-token: write)

### Cost Considerations
- **GitHub Actions**: Minutes beyond free tier incur costs
- **ECR Storage**: Monthly storage costs for container images
- **ECS/Fargate**: Costs for vCPU and memory resources
- **Data Transfer**: Costs for data transfer between GitHub and AWS
