---
name: bedrock-agentcore
description: Amazon Bedrock AgentCore platform for building, deploying, and operating production AI agents. Covers Runtime, Gateway, Browser, Code Interpreter, and Identity services. Use when building Bedrock agents, deploying AI agents to production, or integrating with AgentCore services.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Amazon Bedrock AgentCore

## Overview

Amazon Bedrock AgentCore is an agentic platform for building, deploying, and operating effective AI agents securely at scale—no infrastructure management needed. It provides framework-agnostic primitives that work with popular open-source frameworks (Strands, LangGraph, CrewAI, Autogen) and any model.

**Purpose**: Transform any AI agent into a production-ready application with enterprise-grade infrastructure

**Pattern**: Capabilities-based (6 independent service modules)

**Key Principles** (validated by AWS December 2025):
1. **Framework Agnostic** - Works with any agent framework or model
2. **Zero Infrastructure** - Fully managed, no ops overhead
3. **Session Isolation** - Complete data isolation between sessions
4. **Enterprise Security** - VPC, PrivateLink, identity integration
5. **Composable Services** - Use only what you need
6. **Production Ready** - Built for scale, reliability, and security

**Quality Targets**:
- Deployment: < 5 minutes from code to production
- Latency: Low-latency to 8-hour async workloads
- Observability: Full CloudWatch integration

---

## When to Use

Use bedrock-agentcore when:

- Building production AI agents on AWS
- Need managed infrastructure for agent deployment
- Require session isolation and enterprise security
- Want to use existing agent frameworks (LangGraph, CrewAI, etc.)
- Need browser automation or code execution capabilities
- Integrating with existing identity providers

**When NOT to Use**:
- Simple Bedrock model invocations (use bedrock-runtime)
- Standard Bedrock Agents with action groups (use bedrock-agent)
- Non-AWS deployments

---

## Prerequisites

### Required
- AWS account with Bedrock access
- IAM permissions for AgentCore services
- Python 3.10+ (for SDK)

### Recommended
- `bedrock-agentcore-sdk-python` installed
- `bedrock-agentcore-starter-toolkit` CLI
- Foundation model access enabled (Claude, etc.)

### Installation

```bash
# Install SDK and CLI
pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit

# Verify installation
agentcore --help
```

---

## Core Services

### 1. AgentCore Runtime

Secure, session-isolated compute for running agent code.

**Boto3 Client**:
```python
import boto3

# Data plane operations
client = boto3.client('bedrock-agentcore')

# Control plane operations
control = boto3.client('bedrock-agentcore-control')
```

**Create Agent Runtime**:
```python
# Using starter toolkit
# agentcore configure -e main.py -n my-agent
# agentcore deploy

# Using boto3 control plane
response = control.create_agent_runtime(
    name='my-production-agent',
    description='Customer service agent',
    agentRuntimeArtifact={
        's3': {
            'uri': 's3://my-bucket/agent-package.zip'
        }
    },
    roleArn='arn:aws:iam::123456789012:role/AgentCoreExecutionRole',
    pythonRuntime='PYTHON_3_13',
    entryPoint=['main.py']
)
agent_runtime_arn = response['agentRuntimeArn']
```

**Invoke Agent**:
```python
# Invoke deployed agent
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/xxx',
    runtimeSessionId='session-123',
    payload={
        'prompt': 'What is my order status?',
        'context': {'user_id': 'user-456'}
    }
)

result = response['payload']
print(result)
```

**Agent Entry Point Structure**:
```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp(debug=True)
agent = Agent()

@app.entrypoint
def invoke(payload):
    """Main agent entry point"""
    user_message = payload.get("prompt", "Hello!")
    app.logger.info(f"Processing: {user_message}")

    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
```

---

### 2. AgentCore Gateway

Transforms existing APIs and Lambda functions into agent-compatible tools with semantic search discovery.

**Create Gateway**:
```python
response = control.create_gateway(
    name='customer-service-gateway',
    description='Gateway for customer service tools',
    protocolType='REST'
)
gateway_arn = response['gatewayArn']
```

**Add Gateway Target (Tool)**:
```python
# Add an existing Lambda as a tool
response = control.create_gateway_target(
    gatewayId='gateway-xxx',
    name='GetOrderStatus',
    description='Retrieves order status by order ID',
    targetConfiguration={
        'lambdaTarget': {
            'lambdaArn': 'arn:aws:lambda:us-east-1:123456789012:function:GetOrder'
        }
    },
    toolSchema={
        'name': 'get_order_status',
        'description': 'Get the current status of a customer order',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'order_id': {
                    'type': 'string',
                    'description': 'The unique order identifier'
                }
            },
            'required': ['order_id']
        }
    }
)
```

**Synchronize Tools**:
```python
# Sync gateway tools for discovery
control.synchronize_gateway_targets(
    gatewayId='gateway-xxx'
)
```

---

### 3. Browser Runtime

Execute complex web-based workflows securely.

**Start Browser Session**:
```python
response = client.start_browser_session(
    browserId='browser-xxx',
    sessionConfiguration={
        'timeout': 300,
        'viewport': {'width': 1920, 'height': 1080}
    }
)
session_id = response['browserSessionId']
```

**Execute Browser Action**:
```python
# Navigate and interact
response = client.update_browser_stream(
    browserSessionId=session_id,
    action={
        'navigate': {'url': 'https://example.com'},
        'click': {'selector': '#submit-button'},
        'type': {'selector': '#search', 'text': 'query'}
    }
)
```

---

### 4. Code Interpreter

Safely execute code for tasks like data analysis and visualization.

**Start Code Interpreter Session**:
```python
response = client.start_code_interpreter_session(
    codeInterpreterId='interpreter-xxx'
)
session_id = response['codeInterpreterSessionId']
```

**Execute Code**:
```python
response = client.invoke_code_interpreter(
    codeInterpreterSessionId=session_id,
    code='''
import pandas as pd
import matplotlib.pyplot as plt

# Analyze data
df = pd.DataFrame({'x': [1,2,3,4,5], 'y': [2,4,6,8,10]})
plt.plot(df['x'], df['y'])
plt.savefig('output.png')
print(df.describe())
''',
    language='PYTHON'
)

output = response['output']
files = response['files']  # Generated files
```

---

### 5. Identity Integration

Native integration with existing identity providers for authentication and permission delegation.

**Create OAuth2 Provider**:
```python
response = control.create_oauth2_credential_provider(
    name='okta-provider',
    credentialProviderVendor='OKTA',
    oauth2ProviderConfig={
        'clientId': 'your-client-id',
        'clientSecret': 'your-client-secret',
        'authorizationServerUrl': 'https://your-domain.okta.com/oauth2/default',
        'scopes': ['openid', 'profile', 'email']
    }
)
```

**Create Workload Identity**:
```python
response = control.create_workload_identity(
    name='agent-identity',
    allowedRoleArns=['arn:aws:iam::123456789012:role/AgentRole']
)
```

**Get Access Token**:
```python
# Get token for workload
response = client.get_workload_access_token(
    workloadIdentityId='identity-xxx'
)
access_token = response['accessToken']
```

---

### 6. Observability

Real-time visibility via CloudWatch and OpenTelemetry.

**Enable Observability**:
```python
# In your agent entry point
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Configure tracing
provider = TracerProvider()
trace.set_tracer_provider(provider)

# Entry point with OTel
# entryPoint: ['opentelemetry-instrument', 'main.py']
```

**CloudWatch Metrics**:
- Token usage per session
- Latency (p50, p95, p99)
- Session duration
- Error rates
- Tool call success/failure

---

## Boto3 Client Reference

### Data Plane (`bedrock-agentcore`)

| Method | Purpose |
|--------|---------|
| `invoke_agent_runtime` | Execute agent logic |
| `stop_runtime_session` | Halt active session |
| `list_sessions` | List all sessions |
| `start_browser_session` | Initialize browser |
| `stop_browser_session` | End browser session |
| `start_code_interpreter_session` | Launch interpreter |
| `invoke_code_interpreter` | Execute code |
| `batch_create_memory_records` | Create memories |
| `retrieve_memory_records` | Fetch memories |
| `get_workload_access_token` | Get auth token |
| `evaluate` | Run evaluation |

### Control Plane (`bedrock-agentcore-control`)

| Method | Purpose |
|--------|---------|
| `create_agent_runtime` | Create runtime |
| `delete_agent_runtime` | Remove runtime |
| `update_agent_runtime` | Modify runtime |
| `create_gateway` | Create gateway |
| `create_gateway_target` | Add tool |
| `create_memory` | Create memory store |
| `create_policy` | Create policy |
| `create_evaluator` | Create evaluator |
| `create_browser` | Create browser |
| `create_code_interpreter` | Create interpreter |

---

## Quick Start: Hello World Agent

### Step 1: Create Agent File

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

### Step 2: Configure and Deploy

```bash
# Configure
agentcore configure -e main.py -n hello-world-agent

# Test locally
python main.py &
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'

# Deploy to AWS
agentcore deploy

# Test deployed
agentcore invoke '{"prompt": "Hello from production!"}'
```

### Step 3: Invoke Programmatically

```python
import boto3

client = boto3.client('bedrock-agentcore')

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/hello-world',
    runtimeSessionId='test-session-1',
    payload={'prompt': 'What can you help me with?'}
)

print(response['payload'])
```

---

## Error Handling

```python
from botocore.exceptions import ClientError

try:
    response = client.invoke_agent_runtime(
        agentRuntimeArn=agent_arn,
        runtimeSessionId='session-1',
        payload={'prompt': 'test'}
    )
except ClientError as e:
    error_code = e.response['Error']['Code']

    if error_code == 'ResourceNotFoundException':
        print("Agent runtime not found")
    elif error_code == 'ValidationException':
        print("Invalid request parameters")
    elif error_code == 'ThrottlingException':
        print("Rate limited - implement backoff")
    elif error_code == 'AccessDeniedException':
        print("Check IAM permissions")
    else:
        raise
```

---

## IAM Permissions

### Minimum Execution Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:InvokeAgentRuntime",
        "bedrock-agentcore:StartBrowserSession",
        "bedrock-agentcore:InvokeCodeInterpreter"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

## Related Skills

- **bedrock-agentcore-policy**: Cedar policy authoring and enforcement
- **bedrock-agentcore-evaluations**: Agent testing and quality evaluation
- **bedrock-agentcore-memory**: Episodic and short-term memory management
- **bedrock-agentcore-deployment**: Production deployment patterns
- **bedrock-agentcore-multi-agent**: Multi-agent orchestration (A2A protocol)
- **boto3-eks**: For EKS-hosted agents
- **terraform-aws**: Infrastructure as code

---

## References

- `references/gateway-configuration.md` - Detailed gateway setup
- `references/identity-integration.md` - OAuth and workload identity
- `references/troubleshooting.md` - Common issues and solutions

---

## Sources

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Boto3 BedrockAgentCore](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html)
- [AgentCore SDK Python](https://github.com/aws/bedrock-agentcore-sdk-python)
- [AgentCore Starter Toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)
