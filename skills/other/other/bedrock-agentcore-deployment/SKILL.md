---
name: bedrock-agentcore-deployment
description: Amazon Bedrock AgentCore deployment patterns for production AI agents. Covers starter toolkit, direct code deploy, container deploy, CI/CD pipelines, and infrastructure as code. Use when deploying agents to production, setting up CI/CD, or managing agent infrastructure.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Amazon Bedrock AgentCore Deployment

## Overview

Deploy AI agents to Amazon Bedrock AgentCore using multiple approaches: starter toolkit for rapid deployment, direct code deployment for customization, and container deployment for complex dependencies. Includes CI/CD patterns and infrastructure as code.

**Purpose**: Deploy agents from development to production with best practices

**Pattern**: Workflow-based (4 deployment methods)

**Key Principles** (validated by AWS December 2025):
1. **Zero Infrastructure** - Managed compute, no servers to manage
2. **arm64 Architecture** - All deployments use arm64
3. **Session Isolation** - Complete isolation between sessions
4. **Multiple Entry Points** - SDK decorator or REST endpoints
5. **Observability Built-in** - CloudWatch and OTel integration
6. **Framework Agnostic** - Works with any Python agent framework

**Quality Targets**:
- Deployment time: < 5 minutes
- Cold start: < 2 seconds
- Package size: 250MB (zip), 750MB (unzipped)

---

## When to Use

Use bedrock-agentcore-deployment when:

- Deploying agent code to production
- Setting up CI/CD pipelines for agents
- Migrating from development to production
- Managing multiple agent versions
- Implementing blue-green deployments

**When NOT to Use**:
- Local development/testing (use local server)
- Standard Bedrock Agents with action groups

---

## Prerequisites

### Required
- AWS account with AgentCore access
- Python 3.10+ (recommended: 3.13)
- IAM role with AgentCore permissions
- Foundation model access enabled

### Recommended
- AWS CLI configured
- Docker (for container deployments)
- GitHub Actions or GitLab CI (for CI/CD)

---

## Deployment Method 1: Starter Toolkit (Fastest)

**Time**: 2-5 minutes
**Complexity**: Low
**Best For**: Rapid deployment, simple agents

### Step 1: Install Toolkit
```bash
pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit

# Verify
agentcore --help
```

### Step 2: Create Agent
```python
# main.py
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent(model="anthropic.claude-sonnet-4-20250514-v1:0")

@app.entrypoint
def invoke(payload):
    prompt = payload.get("prompt", "Hello!")
    result = agent(prompt)
    return {"response": result.message}

if __name__ == "__main__":
    app.run()
```

### Step 3: Configure
```bash
# Initialize configuration
agentcore configure -e main.py -n my-production-agent

# This creates .bedrock_agentcore.yaml
```

### Step 4: Test Locally
```bash
# Start local server
python main.py &

# Test
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!"}'

# Stop local server
pkill -f main.py
```

### Step 5: Deploy
```bash
# Deploy to AWS
agentcore deploy

# Output: Agent ARN
# arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/my-production-agent
```

### Step 6: Test Deployed
```bash
# Test via CLI
agentcore invoke '{"prompt": "Hello from production!"}'

# Test via boto3
python -c "
import boto3
client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:...',
    runtimeSessionId='test-1',
    payload={'prompt': 'Hello!'}
)
print(response['payload'])
"
```

---

## Deployment Method 2: Direct Code Deploy

**Time**: 10-15 minutes
**Complexity**: Medium
**Best For**: Custom dependencies, specific configurations

### Step 1: Project Structure
```
my-agent/
├── main.py              # Entry point
├── agent/
│   ├── __init__.py
│   └── logic.py         # Agent logic
├── pyproject.toml       # Dependencies
└── requirements.txt     # Alternative deps format
```

### Step 2: Create Entry Point
```python
# main.py - REST endpoint pattern
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/invocations', methods=['POST'])
def invoke():
    payload = request.get_json()
    prompt = payload.get('prompt', '')

    # Your agent logic here
    from agent.logic import process_request
    result = process_request(prompt)

    return jsonify({'response': result})

@app.route('/ping', methods=['GET'])
def ping():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Step 3: Package for arm64
```bash
# Create virtual environment
uv init agent-deploy --python 3.13
cd agent-deploy

# Install dependencies for arm64
uv pip install \
    --python-platform aarch64-manylinux2014 \
    --python-version 3.13 \
    --target=deployment_package \
    --only-binary=:all: \
    -r requirements.txt

# Create ZIP
cd deployment_package
zip -r ../deployment_package.zip .
cd ..

# Add main.py
zip deployment_package.zip main.py

# Add agent module
zip -r deployment_package.zip agent/
```

### Step 4: Upload to S3
```bash
aws s3 cp deployment_package.zip s3://my-bucket/agents/v1.0.0/package.zip
```

### Step 5: Create Agent Runtime
```python
import boto3

control = boto3.client('bedrock-agentcore-control')

response = control.create_agent_runtime(
    name='my-custom-agent',
    description='Production agent with custom dependencies',
    agentRuntimeArtifact={
        's3': {
            'uri': 's3://my-bucket/agents/v1.0.0/package.zip'
        }
    },
    roleArn='arn:aws:iam::123456789012:role/AgentCoreExecutionRole',
    pythonRuntime='PYTHON_3_13',
    entryPoint=['main.py'],
    environmentVariables={
        'LOG_LEVEL': 'INFO',
        'CUSTOM_CONFIG': 'production'
    }
)

agent_arn = response['agentRuntimeArn']
print(f"Deployed: {agent_arn}")
```

---

## Deployment Method 3: Container Deploy

**Time**: 15-30 minutes
**Complexity**: High
**Best For**: Complex dependencies, custom runtimes, large packages

### Step 1: Create Dockerfile
```dockerfile
# Dockerfile
FROM public.ecr.aws/lambda/python:3.13-arm64

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY main.py .
COPY agent/ agent/

# Set entry point
ENV PORT=8080
EXPOSE 8080

CMD ["main.py"]
```

### Step 2: Build Image
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build for arm64
docker buildx build \
  --platform linux/arm64 \
  -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-agent:v1.0.0 \
  --push .
```

### Step 3: Create Agent Runtime
```python
response = control.create_agent_runtime(
    name='my-container-agent',
    description='Agent deployed via container',
    agentRuntimeArtifact={
        'container': {
            'imageUri': '123456789012.dkr.ecr.us-east-1.amazonaws.com/my-agent:v1.0.0'
        }
    },
    roleArn='arn:aws:iam::123456789012:role/AgentCoreExecutionRole'
)
```

---

## Deployment Method 4: Infrastructure as Code (Terraform)

**Time**: 20-30 minutes setup, then automated
**Complexity**: High
**Best For**: Production environments, team deployments

### Terraform Configuration
```hcl
# main.tf

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

# IAM Role for Agent
resource "aws_iam_role" "agentcore_execution" {
  name = "agentcore-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "bedrock-agentcore.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "agentcore_policy" {
  name = "agentcore-policy"
  role = aws_iam_role.agentcore_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "arn:aws:bedrock:*::foundation-model/*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.agent_artifacts.arn}/*"
      }
    ]
  })
}

# S3 Bucket for Agent Artifacts
resource "aws_s3_bucket" "agent_artifacts" {
  bucket = "my-agentcore-artifacts-${data.aws_caller_identity.current.account_id}"
}

# Upload agent package
resource "aws_s3_object" "agent_package" {
  bucket = aws_s3_bucket.agent_artifacts.id
  key    = "agents/${var.agent_version}/package.zip"
  source = "${path.module}/deployment_package.zip"
  etag   = filemd5("${path.module}/deployment_package.zip")
}

# Note: AgentCore resources may require custom provider or AWS CLI
# Use null_resource with local-exec as workaround

resource "null_resource" "create_agent_runtime" {
  triggers = {
    package_etag = aws_s3_object.agent_package.etag
  }

  provisioner "local-exec" {
    command = <<-EOT
      aws bedrock-agentcore-control create-agent-runtime \
        --name ${var.agent_name} \
        --description "Terraform-managed agent" \
        --agent-runtime-artifact '{"s3":{"uri":"s3://${aws_s3_bucket.agent_artifacts.id}/agents/${var.agent_version}/package.zip"}}' \
        --role-arn ${aws_iam_role.agentcore_execution.arn} \
        --python-runtime PYTHON_3_13 \
        --entry-point '["main.py"]'
    EOT
  }

  depends_on = [aws_s3_object.agent_package]
}

data "aws_caller_identity" "current" {}

variable "agent_name" {
  default = "my-production-agent"
}

variable "agent_version" {
  default = "1.0.0"
}
```

---

## CI/CD Pipeline: GitHub Actions

```yaml
# .github/workflows/deploy-agent.yml
name: Deploy AgentCore Agent

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  AGENT_NAME: my-production-agent

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        run: pytest tests/

      - name: Test local server
        run: |
          python main.py &
          sleep 5
          curl -f http://localhost:8080/ping
          curl -X POST http://localhost:8080/invocations \
            -H "Content-Type: application/json" \
            -d '{"prompt": "test"}'
          pkill -f main.py

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GitHubActionsRole
          aws-region: ${{ env.AWS_REGION }}

      - name: Install AgentCore toolkit
        run: pip install bedrock-agentcore-starter-toolkit

      - name: Configure agent
        run: agentcore configure -e main.py -n ${{ env.AGENT_NAME }}

      - name: Deploy agent
        run: agentcore deploy

      - name: Verify deployment
        run: |
          agentcore invoke '{"prompt": "Health check"}'
```

---

## CI/CD Pipeline: GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  AWS_REGION: us-east-1
  AGENT_NAME: my-production-agent

test:
  stage: test
  image: python:3.13
  script:
    - pip install -r requirements.txt
    - pip install pytest
    - pytest tests/

build:
  stage: build
  image: python:3.13
  script:
    - pip install uv
    - uv pip install --python-platform aarch64-manylinux2014 --python-version 3.13 --target=deployment_package --only-binary=:all: -r requirements.txt
    - cd deployment_package && zip -r ../package.zip . && cd ..
    - zip package.zip main.py
  artifacts:
    paths:
      - package.zip

deploy:
  stage: deploy
  image: amazon/aws-cli
  script:
    - aws s3 cp package.zip s3://${ARTIFACT_BUCKET}/agents/${CI_COMMIT_SHA}/package.zip
    - |
      aws bedrock-agentcore-control update-agent-runtime \
        --agent-runtime-id ${AGENT_RUNTIME_ID} \
        --agent-runtime-artifact "{\"s3\":{\"uri\":\"s3://${ARTIFACT_BUCKET}/agents/${CI_COMMIT_SHA}/package.zip\"}}"
  only:
    - main
```

---

## Version Management

### Blue-Green Deployment
```python
def blue_green_deploy(agent_name, new_version):
    """Deploy new version alongside old, then switch"""

    # Get current (blue) version
    blue = control.get_agent_runtime(name=f"{agent_name}-blue")

    # Deploy new (green) version
    green = control.create_agent_runtime(
        name=f"{agent_name}-green",
        agentRuntimeArtifact={'s3': {'uri': f's3://bucket/agents/{new_version}/package.zip'}},
        roleArn=blue['roleArn'],
        pythonRuntime='PYTHON_3_13',
        entryPoint=['main.py']
    )

    # Test green
    test_result = run_smoke_tests(green['agentRuntimeArn'])

    if test_result.passed:
        # Update endpoint to point to green
        control.update_agent_runtime_endpoint(
            endpointId='production-endpoint',
            agentRuntimeArn=green['agentRuntimeArn']
        )
        # Delete old blue
        control.delete_agent_runtime(name=f"{agent_name}-blue")
        # Rename green to blue
        # (Note: actual rename may require recreate)
    else:
        # Rollback - delete failed green
        control.delete_agent_runtime(name=f"{agent_name}-green")
        raise Exception("Green deployment failed tests")
```

### Rollback
```bash
# Quick rollback via CLI
agentcore rollback --to-version v1.0.0

# Via boto3
control.update_agent_runtime(
    agentRuntimeId='runtime-xxx',
    agentRuntimeArtifact={
        's3': {'uri': 's3://bucket/agents/v1.0.0/package.zip'}
    }
)
```

---

## Related Skills

- **bedrock-agentcore**: Core platform features
- **bedrock-agentcore-evaluations**: Pre-deployment testing
- **terraform-aws**: Infrastructure as code
- **ecs-deployment**: Alternative deployment patterns

---

## References

- `references/iam-policies.md` - IAM policy templates
- `references/troubleshooting.md` - Common deployment issues
- `references/performance-tuning.md` - Optimization guide

---

## Sources

- [AgentCore Runtime Quickstart](https://aws.github.io/bedrock-agentcore-starter-toolkit/user-guide/runtime/quickstart.html)
- [Direct Code Deploy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-code-deploy.html)
- [AgentCore Starter Toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)
