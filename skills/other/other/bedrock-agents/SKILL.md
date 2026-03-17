---
name: bedrock-agents
description: Amazon Bedrock Agents for building autonomous AI agents with foundation model orchestration, action groups, knowledge bases, and session management. Use when creating AI agents, orchestrating multi-step workflows, integrating tools with LLMs, building conversational agents, implementing RAG patterns, managing agent sessions, deploying production agents, or connecting knowledge bases to agents.
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep]
---

# Amazon Bedrock Agents

Complete guide to building and managing Amazon Bedrock Agents - autonomous AI agents that orchestrate foundation models with action groups, knowledge bases, and multi-turn conversations.

## Overview

Amazon Bedrock Agents enables you to create autonomous AI agents that can:
- Orchestrate foundation models to execute multi-step tasks
- Integrate with APIs and Lambda functions via action groups
- Access enterprise knowledge through knowledge bases (RAG)
- Maintain conversation context across sessions
- Reason about complex problems and break them into steps
- Invoke tools and APIs based on natural language requests

**Control Plane**: `bedrock-agent` client for agent configuration
**Runtime Plane**: `bedrock-agent-runtime` client for agent invocation

## Core Concepts

### Agents
The foundation model orchestrator that processes requests, plans actions, and coordinates responses.

**Key Properties**:
- Agent name and description
- Foundation model (Claude, Titan, etc.)
- Instructions (system prompt defining behavior)
- Action groups (tools the agent can use)
- Knowledge bases (data sources for RAG)
- Aliases (deployment versions)

### Action Groups
Define tools and APIs the agent can invoke to accomplish tasks.

**Types**:
- Lambda functions (direct AWS Lambda invocation)
- OpenAPI schemas (REST API integration)
- Code interpreter (Python code execution)
- Return of control (return to application)

### Knowledge Bases
Vector databases with RAG capabilities that agents can query.

**Integration**:
- Associate knowledge bases with agents
- Agent automatically retrieves relevant documents
- Foundation model synthesizes answers from retrieved content

### Aliases
Versioned endpoints for agent deployment.

**Benefits**:
- Stable endpoint for applications
- Safe deployment with version control
- Routing between agent versions
- Production/staging environments

### Sessions
Maintain conversation context across multiple invocations.

**Session Management**:
- Session IDs track conversations
- Memory stores chat history
- Context persists between turns
- Delete memory to reset conversations

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  (Your code using bedrock-agent-runtime.invoke_agent)       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Bedrock Agent Runtime                     │
│  - Session management                                        │
│  - Streaming responses                                       │
│  - Trace/reasoning visibility                                │
└───────┬──────────────────┬──────────────────┬───────────────┘
        │                  │                  │
┌───────▼────────┐  ┌─────▼──────┐  ┌────────▼──────────┐
│ Foundation     │  │   Action   │  │    Knowledge      │
│ Model          │  │   Groups   │  │    Bases          │
│ (Claude, etc.) │  │  (Lambda,  │  │  (Vector DB +     │
│                │  │   OpenAPI) │  │   Documents)      │
└────────────────┘  └────────────┘  └───────────────────┘
```

## Operations

### 1. Create Agent

Create a new Bedrock Agent with foundation model and instructions.

**boto3 Example**:

```python
import boto3
import json

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

def create_agent(
    agent_name: str,
    foundation_model: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    instructions: str = None,
    description: str = None,
    idle_session_ttl: int = 600
) -> dict:
    """
    Create a Bedrock Agent.

    Args:
        agent_name: Name of the agent
        foundation_model: Model ID (Claude 3.5 Sonnet, Haiku, etc.)
        instructions: System prompt defining agent behavior
        description: Human-readable description
        idle_session_ttl: Session timeout in seconds (default 600)

    Returns:
        Agent details including agentId, agentArn, agentStatus
    """

    # Default instructions if none provided
    if instructions is None:
        instructions = """You are a helpful AI assistant.
        Follow user requests carefully and provide accurate, helpful responses.
        When you need to use tools or access knowledge, do so to provide better answers."""

    try:
        response = bedrock_agent.create_agent(
            agentName=agent_name,
            foundationModel=foundation_model,
            instruction=instructions,
            description=description or f"Bedrock Agent: {agent_name}",
            idleSessionTTLInSeconds=idle_session_ttl,
            # Optional: Add tags
            tags={
                'Environment': 'production',
                'ManagedBy': 'bedrock-agents-skill'
            }
        )

        agent = response['agent']
        print(f"✓ Created agent: {agent['agentName']}")
        print(f"  Agent ID: {agent['agentId']}")
        print(f"  Status: {agent['agentStatus']}")
        print(f"  Foundation Model: {agent['foundationModel']}")

        return agent

    except Exception as e:
        print(f"✗ Failed to create agent: {str(e)}")
        raise

# Example: Create customer support agent
agent = create_agent(
    agent_name="customer-support-agent",
    foundation_model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    instructions="""You are a customer support agent for an e-commerce platform.

    Your responsibilities:
    - Answer customer questions about orders, products, and policies
    - Look up order status using available tools
    - Provide accurate information from the knowledge base
    - Be helpful, professional, and empathetic

    Always verify information before providing answers.
    If you cannot help, escalate to a human agent.""",
    description="AI-powered customer support agent",
    idle_session_ttl=1800  # 30 minutes
)

agent_id = agent['agentId']
```

**Foundation Models**:
- `anthropic.claude-3-5-sonnet-20241022-v2:0` - Best reasoning
- `anthropic.claude-3-5-haiku-20241022-v1:0` - Fast responses
- `anthropic.claude-3-opus-20240229-v1:0` - Maximum capability
- `amazon.titan-text-premier-v1:0` - AWS native model

### 2. Prepare Agent

Prepare the agent for use (required after creation or updates).

```python
def prepare_agent(agent_id: str) -> dict:
    """
    Prepare agent for use. Required after creation or configuration changes.

    Args:
        agent_id: ID of the agent to prepare

    Returns:
        Prepared agent details
    """

    try:
        response = bedrock_agent.prepare_agent(agentId=agent_id)

        print(f"✓ Agent preparation started")
        print(f"  Agent ID: {agent_id}")
        print(f"  Status: {response['agentStatus']}")
        print(f"  Prepared At: {response['preparedAt']}")

        return response

    except Exception as e:
        print(f"✗ Failed to prepare agent: {str(e)}")
        raise

# Prepare the agent
prepare_agent(agent_id)

# Wait for preparation to complete
import time

def wait_for_agent_ready(agent_id: str, max_wait: int = 120):
    """Wait for agent to be in PREPARED or VERSIONED status."""

    start_time = time.time()
    while time.time() - start_time < max_wait:
        response = bedrock_agent.get_agent(agentId=agent_id)
        status = response['agent']['agentStatus']

        if status in ['PREPARED', 'VERSIONED']:
            print(f"✓ Agent ready (status: {status})")
            return True
        elif status == 'FAILED':
            print(f"✗ Agent preparation failed")
            return False

        print(f"  Waiting for agent... (status: {status})")
        time.sleep(5)

    print(f"✗ Timeout waiting for agent")
    return False

wait_for_agent_ready(agent_id)
```

### 3. Create Action Group

Add Lambda or OpenAPI action groups to enable tool use.

**Lambda Action Group**:

```python
def create_lambda_action_group(
    agent_id: str,
    action_group_name: str,
    lambda_arn: str,
    description: str,
    api_schema: dict
) -> dict:
    """
    Create an action group that invokes Lambda functions.

    Args:
        agent_id: ID of the agent
        action_group_name: Name of the action group
        lambda_arn: ARN of the Lambda function to invoke
        description: Description of what this action group does
        api_schema: OpenAPI schema defining available operations

    Returns:
        Action group details
    """

    try:
        response = bedrock_agent.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName=action_group_name,
            description=description,
            actionGroupExecutor={
                'lambda': lambda_arn
            },
            apiSchema={
                'payload': json.dumps(api_schema)
            },
            actionGroupState='ENABLED'
        )

        action_group = response['agentActionGroup']
        print(f"✓ Created action group: {action_group['actionGroupName']}")
        print(f"  Action Group ID: {action_group['actionGroupId']}")
        print(f"  Lambda: {lambda_arn}")

        return action_group

    except Exception as e:
        print(f"✗ Failed to create action group: {str(e)}")
        raise

# Example: Order lookup action group
order_lookup_schema = {
    "openapi": "3.0.0",
    "info": {
        "title": "Order Management API",
        "version": "1.0.0",
        "description": "APIs for looking up and managing customer orders"
    },
    "paths": {
        "/orders/{order_id}": {
            "get": {
                "summary": "Get order details",
                "description": "Retrieve detailed information about a specific order",
                "operationId": "getOrderDetails",
                "parameters": [
                    {
                        "name": "order_id",
                        "in": "path",
                        "description": "The unique order identifier",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Order details",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "order_id": {"type": "string"},
                                        "status": {"type": "string"},
                                        "total": {"type": "number"},
                                        "items": {"type": "array"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/orders/search": {
            "post": {
                "summary": "Search orders",
                "description": "Search for orders by customer email or date range",
                "operationId": "searchOrders",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "customer_email": {"type": "string"},
                                    "start_date": {"type": "string", "format": "date"},
                                    "end_date": {"type": "string", "format": "date"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "List of matching orders"
                    }
                }
            }
        }
    }
}

action_group = create_lambda_action_group(
    agent_id=agent_id,
    action_group_name="order-management",
    lambda_arn="arn:aws:lambda:us-east-1:123456789012:function:order-lookup",
    description="Look up and search customer orders",
    api_schema=order_lookup_schema
)
```

**OpenAPI Action Group** (External REST API):

```python
def create_openapi_action_group(
    agent_id: str,
    action_group_name: str,
    api_schema: dict,
    description: str
) -> dict:
    """
    Create an action group for external REST APIs.
    Agent will make HTTP requests to the API defined in the schema.
    """

    try:
        response = bedrock_agent.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName=action_group_name,
            description=description,
            actionGroupExecutor={
                'customControl': 'RETURN_CONTROL'  # Return to application for execution
            },
            apiSchema={
                'payload': json.dumps(api_schema)
            },
            actionGroupState='ENABLED'
        )

        return response['agentActionGroup']

    except Exception as e:
        print(f"✗ Failed to create OpenAPI action group: {str(e)}")
        raise
```

### 4. Associate Knowledge Base

Connect a knowledge base to enable RAG capabilities.

```python
def associate_knowledge_base(
    agent_id: str,
    knowledge_base_id: str,
    description: str = "Agent knowledge base"
) -> dict:
    """
    Associate a knowledge base with an agent for RAG.

    Args:
        agent_id: ID of the agent
        knowledge_base_id: ID of the knowledge base to associate
        description: Description of the knowledge base purpose

    Returns:
        Association details
    """

    try:
        response = bedrock_agent.associate_agent_knowledge_base(
            agentId=agent_id,
            agentVersion='DRAFT',
            knowledgeBaseId=knowledge_base_id,
            description=description,
            knowledgeBaseState='ENABLED'
        )

        kb = response['agentKnowledgeBase']
        print(f"✓ Associated knowledge base")
        print(f"  Knowledge Base ID: {kb['knowledgeBaseId']}")
        print(f"  Description: {kb['description']}")

        return kb

    except Exception as e:
        print(f"✗ Failed to associate knowledge base: {str(e)}")
        raise

# Associate knowledge base with agent
kb_association = associate_knowledge_base(
    agent_id=agent_id,
    knowledge_base_id="KB123456789",
    description="Product catalog and FAQ knowledge base"
)

# After association, prepare agent again
prepare_agent(agent_id)
wait_for_agent_ready(agent_id)
```

### 5. Create Agent Alias

Create a stable endpoint for agent invocation.

```python
def create_agent_alias(
    agent_id: str,
    alias_name: str,
    description: str = None
) -> dict:
    """
    Create an agent alias for deployment.

    Args:
        agent_id: ID of the agent
        alias_name: Name for the alias (e.g., 'production', 'staging')
        description: Description of the alias

    Returns:
        Alias details including agentAliasId
    """

    try:
        response = bedrock_agent.create_agent_alias(
            agentId=agent_id,
            agentAliasName=alias_name,
            description=description or f"{alias_name} environment"
        )

        alias = response['agentAlias']
        print(f"✓ Created alias: {alias['agentAliasName']}")
        print(f"  Alias ID: {alias['agentAliasId']}")
        print(f"  Status: {alias['agentAliasStatus']}")

        return alias

    except Exception as e:
        print(f"✗ Failed to create alias: {str(e)}")
        raise

# Create production alias
alias = create_agent_alias(
    agent_id=agent_id,
    alias_name="production",
    description="Production environment for customer support agent"
)

agent_alias_id = alias['agentAliasId']

# Wait for alias to be ready
def wait_for_alias_ready(agent_id: str, alias_id: str, max_wait: int = 120):
    """Wait for alias to be in PREPARED status."""

    start_time = time.time()
    while time.time() - start_time < max_wait:
        response = bedrock_agent.get_agent_alias(
            agentId=agent_id,
            agentAliasId=alias_id
        )
        status = response['agentAlias']['agentAliasStatus']

        if status == 'PREPARED':
            print(f"✓ Alias ready")
            return True
        elif status == 'FAILED':
            print(f"✗ Alias preparation failed")
            return False

        print(f"  Waiting for alias... (status: {status})")
        time.sleep(5)

    return False

wait_for_alias_ready(agent_id, agent_alias_id)
```

### 6. Invoke Agent (Runtime)

Invoke the agent with single-turn or multi-turn conversations.

**Single-Turn Invocation**:

```python
import boto3

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def invoke_agent(
    agent_id: str,
    agent_alias_id: str,
    session_id: str,
    input_text: str,
    enable_trace: bool = True
) -> dict:
    """
    Invoke a Bedrock Agent with streaming response.

    Args:
        agent_id: ID of the agent
        agent_alias_id: ID of the agent alias
        session_id: Unique session ID for conversation tracking
        input_text: User's input text
        enable_trace: Enable trace for reasoning visibility

    Returns:
        Complete response with text, traces, and citations
    """

    try:
        response = bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text,
            enableTrace=enable_trace
        )

        # Process streaming response
        result = {
            'completion': '',
            'traces': [],
            'citations': []
        }

        event_stream = response['completion']

        for event in event_stream:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    text = chunk['bytes'].decode('utf-8')
                    result['completion'] += text
                    print(text, end='', flush=True)

            elif 'trace' in event:
                trace = event['trace']['trace']
                result['traces'].append(trace)

                # Print reasoning steps
                if enable_trace:
                    if 'orchestrationTrace' in trace:
                        orch = trace['orchestrationTrace']
                        if 'rationale' in orch:
                            print(f"\n[Reasoning] {orch['rationale']['text']}")
                        if 'invocationInput' in orch:
                            print(f"[Action] {orch['invocationInput']}")

            elif 'returnControl' in event:
                # Handle return of control for action group execution
                result['return_control'] = event['returnControl']

        print("\n")
        return result

    except Exception as e:
        print(f"✗ Failed to invoke agent: {str(e)}")
        raise

# Example: Single-turn invocation
import uuid

session_id = str(uuid.uuid4())

response = invoke_agent(
    agent_id=agent_id,
    agent_alias_id=agent_alias_id,
    session_id=session_id,
    input_text="What's the status of order #12345?",
    enable_trace=True
)

print(f"\nAgent Response: {response['completion']}")
```

**Multi-Turn Conversation**:

```python
def chat_with_agent(
    agent_id: str,
    agent_alias_id: str,
    enable_trace: bool = False
):
    """
    Interactive chat session with the agent.
    Maintains conversation context across turns.
    """

    session_id = str(uuid.uuid4())
    print(f"Chat session started (ID: {session_id})")
    print("Type 'exit' to end the conversation\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Ending conversation...")
            break

        if not user_input:
            continue

        print("\nAgent: ", end='', flush=True)

        response = invoke_agent(
            agent_id=agent_id,
            agent_alias_id=agent_alias_id,
            session_id=session_id,
            input_text=user_input,
            enable_trace=enable_trace
        )

        print()  # New line after response

# Start interactive chat
# chat_with_agent(agent_id, agent_alias_id, enable_trace=False)
```

**Invoke with Session State**:

```python
def invoke_agent_with_state(
    agent_id: str,
    agent_alias_id: str,
    session_id: str,
    input_text: str,
    session_state: dict = None
) -> dict:
    """
    Invoke agent with custom session state.

    Session state can include:
    - promptSessionAttributes: Dynamic variables for prompts
    - sessionAttributes: Persistent session data
    """

    invoke_params = {
        'agentId': agent_id,
        'agentAliasId': agent_alias_id,
        'sessionId': session_id,
        'inputText': input_text
    }

    if session_state:
        invoke_params['sessionState'] = session_state

    response = bedrock_agent_runtime.invoke_agent(**invoke_params)

    # Process response...
    result = {'completion': ''}
    for event in response['completion']:
        if 'chunk' in event and 'bytes' in event['chunk']:
            result['completion'] += event['chunk']['bytes'].decode('utf-8')

    return result

# Example: Pass customer context
response = invoke_agent_with_state(
    agent_id=agent_id,
    agent_alias_id=agent_alias_id,
    session_id=session_id,
    input_text="What's my order status?",
    session_state={
        'sessionAttributes': {
            'customer_id': 'CUST-12345',
            'customer_tier': 'premium',
            'customer_email': 'user@example.com'
        },
        'promptSessionAttributes': {
            'current_date': '2025-12-05',
            'support_level': 'tier1'
        }
    }
)
```

### 7. Delete Agent Memory

Clear conversation memory for a session.

```python
def delete_agent_memory(
    agent_id: str,
    agent_alias_id: str,
    session_id: str
) -> dict:
    """
    Delete conversation memory for a specific session.

    Args:
        agent_id: ID of the agent
        agent_alias_id: ID of the agent alias
        session_id: Session ID to clear

    Returns:
        Deletion confirmation
    """

    try:
        response = bedrock_agent_runtime.delete_agent_memory(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            memoryId=session_id
        )

        print(f"✓ Deleted agent memory for session: {session_id}")
        return response

    except Exception as e:
        print(f"✗ Failed to delete memory: {str(e)}")
        raise

# Clear session memory
delete_agent_memory(agent_id, agent_alias_id, session_id)
```

### 8. Update Agent

Update agent configuration, instructions, or foundation model.

```python
def update_agent(
    agent_id: str,
    agent_name: str = None,
    instructions: str = None,
    foundation_model: str = None,
    description: str = None
) -> dict:
    """
    Update agent configuration.

    After update, must prepare agent again before use.
    """

    try:
        # Get current agent details
        current = bedrock_agent.get_agent(agentId=agent_id)['agent']

        update_params = {
            'agentId': agent_id,
            'agentName': agent_name or current['agentName'],
            'foundationModel': foundation_model or current['foundationModel'],
            'instruction': instructions or current.get('instruction', '')
        }

        if description:
            update_params['description'] = description

        response = bedrock_agent.update_agent(**update_params)

        print(f"✓ Updated agent: {response['agent']['agentName']}")
        print("  Note: Prepare agent before use")

        return response['agent']

    except Exception as e:
        print(f"✗ Failed to update agent: {str(e)}")
        raise

# Update agent instructions
update_agent(
    agent_id=agent_id,
    instructions="""You are an enhanced customer support agent.

    New capabilities:
    - Proactively suggest related products
    - Offer discounts for service issues
    - Escalate complex cases to supervisors

    Maintain professional, empathetic tone."""
)

# Prepare after update
prepare_agent(agent_id)
wait_for_agent_ready(agent_id)
```

### 9. List and Delete Agents

Manage agent lifecycle.

```python
def list_agents() -> list:
    """List all agents in the account."""

    try:
        response = bedrock_agent.list_agents(maxResults=50)

        agents = response.get('agentSummaries', [])

        print(f"Found {len(agents)} agents:")
        for agent in agents:
            print(f"\n  Name: {agent['agentName']}")
            print(f"  ID: {agent['agentId']}")
            print(f"  Status: {agent['agentStatus']}")
            print(f"  Updated: {agent['updatedAt']}")

        return agents

    except Exception as e:
        print(f"✗ Failed to list agents: {str(e)}")
        raise

def delete_agent(agent_id: str, skip_resource_in_use_check: bool = False) -> dict:
    """
    Delete an agent and all associated resources.

    Args:
        agent_id: ID of the agent to delete
        skip_resource_in_use_check: Skip check for aliases
    """

    try:
        response = bedrock_agent.delete_agent(
            agentId=agent_id,
            skipResourceInUseCheck=skip_resource_in_use_check
        )

        print(f"✓ Deleted agent: {agent_id}")
        print(f"  Status: {response['agentStatus']}")

        return response

    except Exception as e:
        print(f"✗ Failed to delete agent: {str(e)}")
        raise

# List all agents
agents = list_agents()

# Delete specific agent
# delete_agent(agent_id, skip_resource_in_use_check=True)
```

## Agent Patterns

### Pattern 1: Single-Turn Request-Response

Simple question answering without multi-turn context.

```python
def single_turn_query(agent_id: str, agent_alias_id: str, query: str) -> str:
    """
    Execute a single query without conversation context.
    Each invocation is independent.
    """

    # Use unique session ID for each request
    session_id = str(uuid.uuid4())

    response = bedrock_agent_runtime.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=query,
        enableTrace=False
    )

    completion = ''
    for event in response['completion']:
        if 'chunk' in event and 'bytes' in event['chunk']:
            completion += event['chunk']['bytes'].decode('utf-8')

    return completion

# Example: Independent queries
answer1 = single_turn_query(agent_id, agent_alias_id, "What's your refund policy?")
answer2 = single_turn_query(agent_id, agent_alias_id, "How long does shipping take?")
```

### Pattern 2: Multi-Turn Conversation

Maintain context across multiple exchanges.

```python
class ConversationSession:
    """Manage a multi-turn conversation with context."""

    def __init__(self, agent_id: str, agent_alias_id: str):
        self.agent_id = agent_id
        self.agent_alias_id = agent_alias_id
        self.session_id = str(uuid.uuid4())
        self.history = []

    def send_message(self, message: str) -> str:
        """Send a message and get response."""

        response = bedrock_agent_runtime.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            sessionId=self.session_id,
            inputText=message
        )

        completion = ''
        for event in response['completion']:
            if 'chunk' in event and 'bytes' in event['chunk']:
                completion += event['chunk']['bytes'].decode('utf-8')

        self.history.append({'user': message, 'agent': completion})
        return completion

    def reset(self):
        """Clear conversation memory."""
        bedrock_agent_runtime.delete_agent_memory(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            memoryId=self.session_id
        )
        self.history = []

# Example: Multi-turn conversation
conversation = ConversationSession(agent_id, agent_alias_id)

response1 = conversation.send_message("I need to return a product")
response2 = conversation.send_message("It's order #12345")
response3 = conversation.send_message("The item was damaged on arrival")
# Agent maintains context: knows we're talking about order #12345
```

### Pattern 3: RAG with Knowledge Base

Agent retrieves information from knowledge base.

```python
def rag_query(agent_id: str, agent_alias_id: str, query: str) -> dict:
    """
    Query agent with RAG capabilities.
    Returns response with citations from knowledge base.
    """

    session_id = str(uuid.uuid4())

    response = bedrock_agent_runtime.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=query,
        enableTrace=True
    )

    result = {
        'answer': '',
        'citations': [],
        'retrieved_docs': []
    }

    for event in response['completion']:
        if 'chunk' in event and 'bytes' in event['chunk']:
            result['answer'] += event['chunk']['bytes'].decode('utf-8')

        elif 'trace' in event:
            trace = event['trace']['trace']

            # Extract knowledge base retrieval
            if 'orchestrationTrace' in trace:
                orch = trace['orchestrationTrace']
                if 'observation' in orch:
                    obs = orch['observation']
                    if 'knowledgeBaseLookupOutput' in obs:
                        kb_output = obs['knowledgeBaseLookupOutput']
                        result['retrieved_docs'].extend(
                            kb_output.get('retrievedReferences', [])
                        )

    return result

# Example: Query with citations
result = rag_query(
    agent_id,
    agent_alias_id,
    "What are the ingredients in the protein powder?"
)

print(f"Answer: {result['answer']}")
print(f"\nRetrieved {len(result['retrieved_docs'])} documents")
for doc in result['retrieved_docs']:
    print(f"  - {doc['content']['text'][:100]}...")
```

### Pattern 4: Tool Use with Action Groups

Agent invokes tools to accomplish tasks.

```python
def tool_use_example(agent_id: str, agent_alias_id: str, request: str):
    """
    Agent uses action groups to invoke tools.
    Demonstrates tool invocation flow.
    """

    session_id = str(uuid.uuid4())

    response = bedrock_agent_runtime.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=request,
        enableTrace=True
    )

    for event in response['completion']:
        if 'trace' in event:
            trace = event['trace']['trace']

            if 'orchestrationTrace' in trace:
                orch = trace['orchestrationTrace']

                # Agent planning
                if 'rationale' in orch:
                    print(f"[Planning] {orch['rationale']['text']}")

                # Agent invoking tool
                if 'invocationInput' in orch:
                    inv = orch['invocationInput']
                    if 'actionGroupInvocationInput' in inv:
                        action = inv['actionGroupInvocationInput']
                        print(f"[Tool Call] {action['actionGroupName']}")
                        print(f"  API: {action.get('apiPath', 'N/A')}")
                        print(f"  Parameters: {action.get('parameters', {})}")

                # Tool result
                if 'observation' in orch:
                    obs = orch['observation']
                    if 'actionGroupInvocationOutput' in obs:
                        output = obs['actionGroupInvocationOutput']
                        print(f"[Tool Result] {output.get('text', '')}")

        elif 'chunk' in event and 'bytes' in event['chunk']:
            text = event['chunk']['bytes'].decode('utf-8')
            print(text, end='', flush=True)

# Example: Agent uses tools
tool_use_example(
    agent_id,
    agent_alias_id,
    "Find all orders for customer@example.com in the last 30 days"
)
```

## Best Practices

### 1. Agent Instructions

Write clear, specific instructions:

```python
good_instructions = """You are a financial advisor agent for retail banking customers.

Your capabilities:
- Answer questions about savings accounts, checking accounts, and credit cards
- Look up account balances and transaction history using available tools
- Provide information about loan products from the knowledge base
- Help customers understand fees and policies

Your guidelines:
- Always verify customer identity before accessing account information
- Provide accurate information from official sources only
- If you cannot help with something, explain why and suggest alternatives
- Use professional but friendly language
- Cite sources when providing policy or fee information

Your limitations:
- You cannot make transactions or transfer money
- You cannot change account settings
- You cannot access accounts without proper verification
- For complex issues, escalate to a human advisor

Session context:
- Customer tier: {{customer_tier}}
- Customer since: {{customer_since}}
- Primary account: {{primary_account_type}}
"""
```

### 2. Session Management

Track sessions appropriately:

```python
# Single-turn: New session per request
session_id = str(uuid.uuid4())

# Multi-turn: Persistent session ID
session_id = f"user-{user_id}-{datetime.now().strftime('%Y%m%d')}"

# Long-running: Include timestamp
session_id = f"support-ticket-{ticket_id}-{int(time.time())}"

# Clear old sessions periodically
def cleanup_old_sessions(agent_id: str, agent_alias_id: str, session_ids: list):
    """Delete memory for expired sessions."""
    for session_id in session_ids:
        try:
            bedrock_agent_runtime.delete_agent_memory(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                memoryId=session_id
            )
        except:
            pass  # Session may not exist
```

### 3. Error Handling

Handle streaming errors gracefully:

```python
def invoke_agent_safe(agent_id: str, agent_alias_id: str, session_id: str, input_text: str):
    """Invoke agent with comprehensive error handling."""

    try:
        response = bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text
        )

        completion = ''

        for event in response['completion']:
            try:
                if 'chunk' in event and 'bytes' in event['chunk']:
                    completion += event['chunk']['bytes'].decode('utf-8')

                elif 'internalServerException' in event:
                    raise Exception("Internal server error")

                elif 'validationException' in event:
                    raise ValueError("Validation error")

                elif 'throttlingException' in event:
                    raise Exception("Rate limit exceeded")

            except Exception as e:
                print(f"Stream error: {str(e)}")
                continue

        return completion

    except bedrock_agent_runtime.exceptions.ResourceNotFoundException:
        print("Agent or alias not found")
        raise
    except bedrock_agent_runtime.exceptions.AccessDeniedException:
        print("Access denied - check IAM permissions")
        raise
    except Exception as e:
        print(f"Invocation error: {str(e)}")
        raise
```

### 4. Action Group Lambda Handler

Structure Lambda functions for action groups:

```python
# Lambda function for order lookup action group
def lambda_handler(event, context):
    """
    Handle action group invocations from Bedrock Agent.

    Event structure:
    {
        'actionGroup': 'order-management',
        'apiPath': '/orders/{order_id}',
        'httpMethod': 'GET',
        'parameters': [...]
    }
    """

    action_group = event['actionGroup']
    api_path = event['apiPath']
    http_method = event['httpMethod']

    # Parse parameters
    parameters = {}
    for param in event.get('parameters', []):
        parameters[param['name']] = param['value']

    # Route to handler
    if api_path == '/orders/{order_id}' and http_method == 'GET':
        return get_order_details(parameters.get('order_id'))

    elif api_path == '/orders/search' and http_method == 'POST':
        return search_orders(parameters)

    else:
        return {
            'statusCode': 404,
            'body': {'error': 'Operation not found'}
        }

def get_order_details(order_id: str):
    """Get order details from database."""

    # Query database...
    order = {
        'order_id': order_id,
        'status': 'shipped',
        'total': 129.99,
        'items': [
            {'name': 'Widget', 'quantity': 2, 'price': 49.99},
            {'name': 'Gadget', 'quantity': 1, 'price': 30.01}
        ],
        'tracking': 'TRACK123456'
    }

    return {
        'statusCode': 200,
        'body': order
    }
```

### 5. Monitoring and Logging

Track agent performance:

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def invoke_agent_with_metrics(agent_id: str, agent_alias_id: str, session_id: str, input_text: str):
    """Invoke agent with logging and metrics."""

    start_time = time.time()

    logger.info(f"Agent invocation started: {agent_id}")
    logger.info(f"Session: {session_id}")
    logger.info(f"Input: {input_text[:100]}...")

    try:
        response = bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text,
            enableTrace=True
        )

        completion = ''
        tool_calls = 0
        kb_retrievals = 0

        for event in response['completion']:
            if 'chunk' in event and 'bytes' in event['chunk']:
                completion += event['chunk']['bytes'].decode('utf-8')

            elif 'trace' in event:
                trace = event['trace']['trace']
                if 'orchestrationTrace' in trace:
                    orch = trace['orchestrationTrace']

                    if 'invocationInput' in orch:
                        inv = orch['invocationInput']
                        if 'actionGroupInvocationInput' in inv:
                            tool_calls += 1

                    if 'observation' in orch:
                        obs = orch['observation']
                        if 'knowledgeBaseLookupOutput' in obs:
                            kb_retrievals += 1

        duration = time.time() - start_time

        logger.info(f"Agent invocation completed")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info(f"Tool calls: {tool_calls}")
        logger.info(f"KB retrievals: {kb_retrievals}")
        logger.info(f"Response length: {len(completion)} chars")

        return {
            'completion': completion,
            'metrics': {
                'duration': duration,
                'tool_calls': tool_calls,
                'kb_retrievals': kb_retrievals
            }
        }

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Agent invocation failed after {duration:.2f}s: {str(e)}")
        raise
```

## Related Skills

- **bedrock-agentcore**: Amazon Bedrock AgentCore platform
- **bedrock-agentcore-multi-agent**: Multi-agent orchestration patterns
- **bedrock-knowledge-bases**: RAG with vector databases
- **bedrock-guardrails**: Content filtering and safety
- **bedrock-inference**: Direct model invocation
- **boto3-lambda**: Lambda integration for action groups
- **anthropic-expert**: Claude models and capabilities

## References

- [Amazon Bedrock Agents Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Bedrock Agent Runtime API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock_Runtime.html)
- [Bedrock Agent Control Plane API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html)
- [Action Groups Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-create.html)
- [Knowledge Base Integration](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-kb-add.html)
