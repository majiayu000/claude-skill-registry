---
name: bedrock-flows
description: Build visual AI workflows with Amazon Bedrock Flows. Create flows with prompt nodes, knowledge bases, Lambda, inline code, condition branching, iterators, collectors, and DoWhile loops. Version management, aliases, deployment. Use when building multi-step AI workflows, orchestrating models and services, creating condition-based routing, implementing iterative processing, or deploying production AI pipelines.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Amazon Bedrock Flows

Build end-to-end generative AI workflows with visual flow builder, linking foundation models, prompts, knowledge bases, and AWS services without code.

## Overview

**Amazon Bedrock Flows** is a visual workflow builder for orchestrating generative AI applications. It provides:

- **Visual Flow Builder**: Drag-and-drop interface for creating complex workflows
- **Foundation Model Integration**: Connect multiple models and prompts
- **Knowledge Base Nodes**: RAG workflows with Bedrock Knowledge Bases
- **Condition Branching**: Route execution based on criteria
- **Iteration & Loops**: Process arrays and repeat operations
- **Lambda & Inline Code**: Custom logic without deployment overhead
- **Version Management**: Version flows for A/B testing and rollback
- **API Deployment**: Invoke flows programmatically via boto3

### Key Benefits

1. **No Code Required**: Build complex AI workflows visually
2. **Reusable Components**: Share and compose flows
3. **Parallel Execution**: Multiple paths execute simultaneously
4. **Version Control**: Test and rollback safely
5. **Production Ready**: API-based invocation with aliases
6. **AWS Integration**: Native Lambda, S3, Knowledge Base support

### When to Use Flows

- **Multi-step AI Workflows**: Chain multiple model calls
- **RAG Applications**: Retrieve from knowledge bases and generate responses
- **Condition-Based Routing**: Dynamic paths based on content
- **Data Processing Pipelines**: Transform and enrich data
- **Agent Orchestration**: Coordinate multiple agents
- **Production Deployment**: Stable, versioned AI applications

## Quick Start

### 1. Create Simple Flow

```python
import boto3
import json

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create basic Q&A flow with knowledge base
flow_response = bedrock_agent.create_flow(
    name='document-qa-flow',
    description='Answer questions from knowledge base',
    executionRoleArn='arn:aws:iam::123456789012:role/BedrockFlowRole',
    definition={
        'nodes': [
            {
                'name': 'FlowInput',
                'type': 'Input',
                'configuration': {'input': {}},
                'outputs': [
                    {'name': 'document', 'type': 'String'}
                ]
            },
            {
                'name': 'SearchKB',
                'type': 'KnowledgeBase',
                'configuration': {
                    'knowledgeBase': {
                        'knowledgeBaseId': 'KB123456',
                        'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0'
                    }
                },
                'inputs': [
                    {
                        'name': 'retrievalQuery',
                        'type': 'String',
                        'expression': 'FlowInput.document'
                    }
                ],
                'outputs': [
                    {'name': 'generatedResponse', 'type': 'String'}
                ]
            },
            {
                'name': 'FlowOutput',
                'type': 'Output',
                'configuration': {'output': {}},
                'inputs': [
                    {
                        'name': 'document',
                        'type': 'String',
                        'expression': 'SearchKB.generatedResponse'
                    }
                ]
            }
        ],
        'connections': [
            {
                'name': 'InputToSearch',
                'source': 'FlowInput',
                'target': 'SearchKB',
                'type': 'Data'
            },
            {
                'name': 'SearchToOutput',
                'source': 'SearchKB',
                'target': 'FlowOutput',
                'type': 'Data'
            }
        ]
    }
)

flow_id = flow_response['id']
print(f"Flow ID: {flow_id}")
```

### 2. Deploy Flow

```python
# Prepare flow (validates configuration)
bedrock_agent.prepare_flow(flowIdentifier=flow_id)

# Create version
version_response = bedrock_agent.create_flow_version(
    flowIdentifier=flow_id,
    description='Production version 1'
)
flow_version = version_response['version']

# Create alias for deployment
alias_response = bedrock_agent.create_flow_alias(
    flowIdentifier=flow_id,
    name='production',
    description='Production alias',
    routingConfiguration=[
        {'flowVersion': flow_version}
    ]
)
flow_alias_id = alias_response['id']

print(f"Deployed: Version {flow_version}, Alias {flow_alias_id}")
```

### 3. Invoke Flow

```python
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent_runtime.invoke_flow(
    flowIdentifier=flow_id,
    flowAliasIdentifier=flow_alias_id,
    inputs=[
        {
            'content': {
                'document': 'What are the benefits of semantic chunking?'
            },
            'nodeName': 'FlowInput',
            'nodeOutputName': 'document'
        }
    ]
)

# Process response stream
result = {}
for event in response.get('responseStream'):
    result.update(event)

if result['flowCompletionEvent']['completionReason'] == 'SUCCESS':
    output = result['flowOutputEvent']['content']['document']
    print(f"Answer: {output}")
```

## Node Types

### Flow Control Nodes

#### Input Node (Required)

Every flow must have exactly one Input node as entry point.

```python
input_node = {
    'name': 'FlowInput',
    'type': 'Input',
    'configuration': {'input': {}},
    'outputs': [
        {'name': 'query', 'type': 'String'},
        {'name': 'user_id', 'type': 'String'},
        {'name': 'context', 'type': 'Object'}
    ]
}
```

#### Output Node (Required)

Every flow must have at least one Output node.

```python
output_node = {
    'name': 'FlowOutput',
    'type': 'Output',
    'configuration': {'output': {}},
    'inputs': [
        {
            'name': 'document',
            'type': 'String',
            'expression': 'GenerateResponse.modelCompletion'
        }
    ]
}
```

### Orchestration Nodes

#### Prompt Node

Invoke foundation model with prompt template.

```python
prompt_node = {
    'name': 'GenerateSummary',
    'type': 'Prompt',
    'configuration': {
        'prompt': {
            'sourceConfiguration': {
                'inline': {
                    'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
                    'templateType': 'TEXT',
                    'templateConfiguration': {
                        'text': {
                            'text': '''Summarize the following document in 3 bullet points:

{{document_text}}

Summary:'''
                        }
                    },
                    'inferenceConfiguration': {
                        'text': {
                            'temperature': 0.5,
                            'maxTokens': 500,
                            'topP': 0.9
                        }
                    }
                }
            }
        }
    },
    'inputs': [
        {
            'name': 'document_text',
            'type': 'String',
            'expression': 'FlowInput.document'
        }
    ],
    'outputs': [
        {'name': 'modelCompletion', 'type': 'String'}
    ]
}
```

**Prompt Node Features**:
- Inline prompts or reference saved prompts
- Variable substitution with `{{variable_name}}`
- Full inference configuration
- Multiple model support

#### Agent Node

Invoke Bedrock Agent for multi-turn interactions.

```python
agent_node = {
    'name': 'ResearchAgent',
    'type': 'Agent',
    'configuration': {
        'agent': {
            'agentAliasArn': 'arn:aws:bedrock:us-east-1:123456789012:agent-alias/AGENT123/ALIAS456'
        }
    },
    'inputs': [
        {
            'name': 'text',
            'type': 'String',
            'expression': 'FlowInput.query'
        },
        {
            'name': 'sessionId',
            'type': 'String',
            'expression': 'FlowInput.session_id'
        }
    ],
    'outputs': [
        {'name': 'completion', 'type': 'String'}
    ]
}
```

### Data Nodes

#### Knowledge Base Node

Query Bedrock Knowledge Base with RAG.

```python
kb_node = {
    'name': 'SearchDocs',
    'type': 'KnowledgeBase',
    'configuration': {
        'knowledgeBase': {
            'knowledgeBaseId': 'KB123456',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'retrievalConfiguration': {
                'vectorSearchConfiguration': {
                    'numberOfResults': 5,
                    'overrideSearchType': 'HYBRID'
                }
            }
        }
    },
    'inputs': [
        {
            'name': 'retrievalQuery',
            'type': 'String',
            'expression': 'FlowInput.query'
        }
    ],
    'outputs': [
        {'name': 'generatedResponse', 'type': 'String'},
        {'name': 'retrievalResults', 'type': 'Array'}
    ]
}
```

**Configuration Options**:
- `numberOfResults`: How many chunks to retrieve (1-100)
- `overrideSearchType`: `HYBRID` (semantic + keyword) or `SEMANTIC`
- Returns both generated response and raw retrieval results

#### S3 Retrieval Node

Fetch data from S3 bucket.

```python
s3_retrieval_node = {
    'name': 'LoadTemplate',
    'type': 'S3Retrieval',
    'configuration': {
        's3': {
            'bucketName': 'my-templates-bucket',
            'keyPrefix': 'templates/'
        }
    },
    'inputs': [
        {
            'name': 'objectKey',
            'type': 'String',
            'expression': '"email-template.txt"'
        }
    ],
    'outputs': [
        {'name': 'content', 'type': 'String'}
    ]
}
```

#### S3 Storage Node

Store data to S3 bucket.

```python
s3_storage_node = {
    'name': 'SaveResult',
    'type': 'S3Storage',
    'configuration': {
        's3': {
            'bucketName': 'my-results-bucket',
            'keyPrefix': 'outputs/'
        }
    },
    'inputs': [
        {
            'name': 'objectKey',
            'type': 'String',
            'expression': 'FlowInput.user_id + ".json"'
        },
        {
            'name': 'content',
            'type': 'String',
            'expression': 'GenerateResponse.modelCompletion'
        }
    ],
    'outputs': [
        {'name': 'location', 'type': 'String'}
    ]
}
```

### Logic Nodes

#### Condition Node

Branch execution based on criteria.

```python
condition_node = {
    'name': 'CheckSentiment',
    'type': 'Condition',
    'configuration': {
        'condition': {
            'conditions': [
                {
                    'name': 'positive',
                    'expression': 'SentimentAnalysis.score > 0.7'
                },
                {
                    'name': 'negative',
                    'expression': 'SentimentAnalysis.score < 0.3'
                },
                {
                    'name': 'neutral',
                    'expression': 'true'  # Default case
                }
            ]
        }
    },
    'inputs': [
        {
            'name': 'score',
            'type': 'Number',
            'expression': 'SentimentAnalysis.sentiment_score'
        }
    ],
    'outputs': [
        {'name': 'positive', 'type': 'Boolean'},
        {'name': 'negative', 'type': 'Boolean'},
        {'name': 'neutral', 'type': 'Boolean'}
    ]
}
```

**Use Cases**:
- Content routing (sentiment, category, language)
- Error handling (retry, fallback)
- Feature flags (A/B testing)
- Threshold checks (confidence scores)

#### Iterator Node

Loop through array items.

```python
iterator_node = {
    'name': 'ProcessDocuments',
    'type': 'Iterator',
    'configuration': {
        'iterator': {}
    },
    'inputs': [
        {
            'name': 'array',
            'type': 'Array',
            'expression': 'FlowInput.document_list'
        }
    ],
    'outputs': [
        {'name': 'item', 'type': 'Object'}
    ]
}
```

#### Collector Node

Gather results from iterator.

```python
collector_node = {
    'name': 'GatherSummaries',
    'type': 'Collector',
    'configuration': {
        'collector': {}
    },
    'inputs': [
        {
            'name': 'item',
            'type': 'String',
            'expression': 'SummarizeDoc.modelCompletion'
        }
    ],
    'outputs': [
        {'name': 'collection', 'type': 'Array'}
    ]
}
```

**Iterator + Collector Pattern**:
```
Iterator (documents) → Process Each → Collector (summaries)
```

#### DoWhile Loop Node (NEW 2025)

Execute operations repeatedly while condition is true.

```python
dowhile_node = {
    'name': 'RefineResponse',
    'type': 'DoWhileLoop',
    'configuration': {
        'doWhileLoop': {
            'condition': 'context.quality_score < 0.9 AND context.iteration < 3'
        }
    },
    'inputs': [
        {
            'name': 'quality_score',
            'type': 'Number',
            'expression': 'EvaluateQuality.score'
        },
        {
            'name': 'iteration',
            'type': 'Number',
            'expression': 'context.iteration + 1'
        }
    ],
    'outputs': [
        {'name': 'final_output', 'type': 'String'}
    ]
}
```

**Use Cases**:
- Iterative refinement (quality improvement)
- Retry with backoff
- Progressive enhancement
- Multi-step validation

### Code Nodes

#### Lambda Function Node

Execute external Lambda function.

```python
lambda_node = {
    'name': 'SendEmail',
    'type': 'LambdaFunction',
    'configuration': {
        'lambdaFunction': {
            'lambdaArn': 'arn:aws:lambda:us-east-1:123456789012:function:send-email'
        }
    },
    'inputs': [
        {
            'name': 'recipient',
            'type': 'String',
            'expression': 'FlowInput.email'
        },
        {
            'name': 'subject',
            'type': 'String',
            'expression': '"Your Summary Report"'
        },
        {
            'name': 'body',
            'type': 'String',
            'expression': 'GenerateSummary.modelCompletion'
        }
    ],
    'outputs': [
        {'name': 'result', 'type': 'Object'},
        {'name': 'statusCode', 'type': 'Number'}
    ]
}
```

**Lambda Requirements**:
- Flow execution role needs `lambda:InvokeFunction` permission
- Lambda must accept event payload
- Lambda should return JSON response

#### Inline Code Node (NEW 2025, Preview)

Execute Python code directly without Lambda deployment.

```python
inline_code_node = {
    'name': 'ParseJSON',
    'type': 'InlineCode',
    'configuration': {
        'inlineCode': {
            'language': 'PYTHON_3',
            'code': '''
import json

def lambda_handler(event, context):
    """Parse JSON and extract fields"""

    # Get input from event
    json_text = event.get('json_input', '{}')

    try:
        # Parse JSON
        data = json.loads(json_text)

        # Extract fields
        name = data.get('name', 'Unknown')
        email = data.get('email', '')
        age = data.get('age', 0)

        return {
            'name': name,
            'email': email,
            'age': age,
            'is_adult': age >= 18,
            'valid': True
        }
    except json.JSONDecodeError as e:
        return {
            'valid': False,
            'error': str(e)
        }
'''
        }
    },
    'inputs': [
        {
            'name': 'json_input',
            'type': 'String',
            'expression': 'FlowInput.document'
        }
    ],
    'outputs': [
        {'name': 'name', 'type': 'String'},
        {'name': 'email', 'type': 'String'},
        {'name': 'age', 'type': 'Number'},
        {'name': 'is_adult', 'type': 'Boolean'},
        {'name': 'valid', 'type': 'Boolean'}
    ]
}
```

**Inline Code Features**:
- No Lambda deployment required
- Python 3.x runtime
- Standard library access
- Event/context pattern like Lambda
- Faster iteration (no deployment delay)

**Limitations**:
- Still in preview (check AWS docs for availability)
- No external dependencies (pip packages)
- Execution time limits
- Limited to Python 3.x

## Operations

### create_flow

Create a new flow with nodes and connections.

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

flow_response = bedrock_agent.create_flow(
    name='content-moderation-flow',
    description='Classify and route content based on safety',
    executionRoleArn='arn:aws:iam::123456789012:role/BedrockFlowRole',
    definition={
        'nodes': [
            # Input node
            {
                'name': 'FlowInput',
                'type': 'Input',
                'configuration': {'input': {}},
                'outputs': [
                    {'name': 'content', 'type': 'String'}
                ]
            },
            # Classify content
            {
                'name': 'ClassifyContent',
                'type': 'Prompt',
                'configuration': {
                    'prompt': {
                        'sourceConfiguration': {
                            'inline': {
                                'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
                                'templateType': 'TEXT',
                                'templateConfiguration': {
                                    'text': {
                                        'text': '''Classify this content as SAFE, REVIEW, or UNSAFE:

{{content}}

Classification (respond with only one word):'''
                                    }
                                },
                                'inferenceConfiguration': {
                                    'text': {
                                        'temperature': 0.0,
                                        'maxTokens': 10
                                    }
                                }
                            }
                        }
                    }
                },
                'inputs': [
                    {
                        'name': 'content',
                        'type': 'String',
                        'expression': 'FlowInput.content'
                    }
                ],
                'outputs': [
                    {'name': 'modelCompletion', 'type': 'String'}
                ]
            },
            # Route based on classification
            {
                'name': 'RouteContent',
                'type': 'Condition',
                'configuration': {
                    'condition': {
                        'conditions': [
                            {
                                'name': 'safe',
                                'expression': 'ClassifyContent.modelCompletion == "SAFE"'
                            },
                            {
                                'name': 'review',
                                'expression': 'ClassifyContent.modelCompletion == "REVIEW"'
                            },
                            {
                                'name': 'unsafe',
                                'expression': 'ClassifyContent.modelCompletion == "UNSAFE"'
                            }
                        ]
                    }
                },
                'inputs': [
                    {
                        'name': 'classification',
                        'type': 'String',
                        'expression': 'ClassifyContent.modelCompletion'
                    }
                ],
                'outputs': [
                    {'name': 'safe', 'type': 'Boolean'},
                    {'name': 'review', 'type': 'Boolean'},
                    {'name': 'unsafe', 'type': 'Boolean'}
                ]
            },
            # Output node
            {
                'name': 'FlowOutput',
                'type': 'Output',
                'configuration': {'output': {}},
                'inputs': [
                    {
                        'name': 'result',
                        'type': 'String',
                        'expression': 'ClassifyContent.modelCompletion'
                    }
                ]
            }
        ],
        'connections': [
            {
                'name': 'InputToClassify',
                'source': 'FlowInput',
                'target': 'ClassifyContent',
                'type': 'Data'
            },
            {
                'name': 'ClassifyToRoute',
                'source': 'ClassifyContent',
                'target': 'RouteContent',
                'type': 'Data'
            },
            {
                'name': 'RouteToOutput',
                'source': 'RouteContent',
                'target': 'FlowOutput',
                'type': 'Conditional',
                'condition': 'RouteContent.safe OR RouteContent.review'
            }
        ]
    }
)

print(f"Flow created: {flow_response['id']}")
```

### create_flow_version

Create immutable version for deployment.

```python
# Prepare flow first (validates configuration)
bedrock_agent.prepare_flow(flowIdentifier=flow_id)

# Create version
version_response = bedrock_agent.create_flow_version(
    flowIdentifier=flow_id,
    description='v1.2.0 - Added content moderation, improved classification accuracy'
)

flow_version = version_response['version']
flow_arn = version_response['arn']

print(f"Version: {flow_version}")
print(f"ARN: {flow_arn}")
```

**Version Management**:
- Versions are immutable (cannot be changed)
- Use semantic versioning in description
- Track changes between versions
- Enables A/B testing and rollback

### create_flow_alias

Create alias pointing to flow version.

```python
# Production alias
prod_alias = bedrock_agent.create_flow_alias(
    flowIdentifier=flow_id,
    name='production',
    description='Production deployment',
    routingConfiguration=[
        {
            'flowVersion': '5'  # Stable version
        }
    ]
)

# Development alias
dev_alias = bedrock_agent.create_flow_alias(
    flowIdentifier=flow_id,
    name='development',
    description='Development testing',
    routingConfiguration=[
        {
            'flowVersion': '6'  # Latest version
        }
    ]
)

print(f"Production alias: {prod_alias['id']}")
print(f"Development alias: {dev_alias['id']}")
```

**Alias Benefits**:
- Stable endpoint for applications
- Easy version switching (update routing)
- A/B testing with traffic splitting
- Blue/green deployments

### update_flow_alias

Update alias to point to different version.

```python
# Update production alias to new version
bedrock_agent.update_flow_alias(
    flowIdentifier=flow_id,
    aliasIdentifier='production',
    name='production',
    description='Updated to v1.3.0',
    routingConfiguration=[
        {
            'flowVersion': '7'  # New version
        }
    ]
)

print("Production alias updated to version 7")
```

### invoke_flow

Execute flow with runtime API.

```python
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent_runtime.invoke_flow(
    flowIdentifier=flow_id,
    flowAliasIdentifier='production',
    inputs=[
        {
            'content': {
                'content': 'This is sample content to classify'
            },
            'nodeName': 'FlowInput',
            'nodeOutputName': 'content'
        }
    ]
)

# Process streaming response
result = {}
for event in response.get('responseStream'):
    if 'flowOutputEvent' in event:
        result['output'] = event['flowOutputEvent']
    elif 'flowCompletionEvent' in event:
        result['completion'] = event['flowCompletionEvent']

# Check completion status
if result['completion']['completionReason'] == 'SUCCESS':
    output_content = result['output']['content']['result']
    print(f"Classification: {output_content}")
else:
    print(f"Flow failed: {result['completion']['completionReason']}")
```

### monitor_flow

Monitor flow execution with CloudWatch.

```python
import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# Get flow invocation metrics
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/Bedrock',
    MetricName='FlowInvocations',
    Dimensions=[
        {
            'Name': 'FlowId',
            'Value': flow_id
        },
        {
            'Name': 'FlowAliasId',
            'Value': 'production'
        }
    ],
    StartTime=datetime.utcnow() - timedelta(hours=24),
    EndTime=datetime.utcnow(),
    Period=3600,  # 1 hour
    Statistics=['Sum', 'Average']
)

for datapoint in response['Datapoints']:
    print(f"{datapoint['Timestamp']}: {datapoint['Sum']} invocations")

# Get flow latency metrics
latency_response = cloudwatch.get_metric_statistics(
    Namespace='AWS/Bedrock',
    MetricName='FlowDuration',
    Dimensions=[
        {
            'Name': 'FlowId',
            'Value': flow_id
        }
    ],
    StartTime=datetime.utcnow() - timedelta(hours=24),
    EndTime=datetime.utcnow(),
    Period=3600,
    Statistics=['Average', 'Maximum', 'Minimum']
)

# Get error metrics
error_response = cloudwatch.get_metric_statistics(
    Namespace='AWS/Bedrock',
    MetricName='FlowErrors',
    Dimensions=[
        {
            'Name': 'FlowId',
            'Value': flow_id
        }
    ],
    StartTime=datetime.utcnow() - timedelta(hours=24),
    EndTime=datetime.utcnow(),
    Period=3600,
    Statistics=['Sum']
)
```

**CloudWatch Metrics**:
- `FlowInvocations`: Number of flow executions
- `FlowDuration`: Execution time (milliseconds)
- `FlowErrors`: Number of failed executions
- `NodeDuration`: Per-node execution time
- `ModelInvocations`: Foundation model calls

**Set Up Alarms**:
```python
# Create alarm for high error rate
cloudwatch.put_metric_alarm(
    AlarmName='bedrock-flow-errors',
    AlarmDescription='Alert when flow error rate exceeds threshold',
    MetricName='FlowErrors',
    Namespace='AWS/Bedrock',
    Statistic='Sum',
    Period=300,  # 5 minutes
    EvaluationPeriods=2,
    Threshold=10,  # 10 errors in 5 minutes
    ComparisonOperator='GreaterThanThreshold',
    Dimensions=[
        {
            'Name': 'FlowId',
            'Value': flow_id
        }
    ],
    AlarmActions=[
        'arn:aws:sns:us-east-1:123456789012:bedrock-alerts'
    ]
)
```

## Flow Patterns

### Pattern 1: Sequential Processing

Chain operations in sequence.

```python
# Flow: Input → Extract → Classify → Generate → Output
sequential_flow = {
    'nodes': [
        {'name': 'FlowInput', 'type': 'Input', ...},
        {'name': 'ExtractInfo', 'type': 'Prompt', ...},
        {'name': 'ClassifyIntent', 'type': 'Prompt', ...},
        {'name': 'GenerateResponse', 'type': 'Prompt', ...},
        {'name': 'FlowOutput', 'type': 'Output', ...}
    ],
    'connections': [
        {'source': 'FlowInput', 'target': 'ExtractInfo'},
        {'source': 'ExtractInfo', 'target': 'ClassifyIntent'},
        {'source': 'ClassifyIntent', 'target': 'GenerateResponse'},
        {'source': 'GenerateResponse', 'target': 'FlowOutput'}
    ]
}
```

### Pattern 2: Parallel Branches

Execute multiple paths simultaneously.

```python
# Flow: Input → [Branch A, Branch B] → Combine → Output
parallel_flow = {
    'nodes': [
        {'name': 'FlowInput', 'type': 'Input', ...},
        {'name': 'BranchA', 'type': 'Prompt', ...},  # Executes in parallel
        {'name': 'BranchB', 'type': 'KnowledgeBase', ...},  # Executes in parallel
        {'name': 'Combine', 'type': 'Prompt', ...},
        {'name': 'FlowOutput', 'type': 'Output', ...}
    ],
    'connections': [
        {'source': 'FlowInput', 'target': 'BranchA'},
        {'source': 'FlowInput', 'target': 'BranchB'},
        {'source': 'BranchA', 'target': 'Combine'},
        {'source': 'BranchB', 'target': 'Combine'},
        {'source': 'Combine', 'target': 'FlowOutput'}
    ]
}
```

### Pattern 3: Condition Branching

Route based on criteria.

```python
# Flow: Input → Classify → [Safe Path, Review Path, Block Path]
condition_flow = {
    'nodes': [
        {'name': 'FlowInput', 'type': 'Input', ...},
        {'name': 'ClassifyContent', 'type': 'Prompt', ...},
        {'name': 'RouteContent', 'type': 'Condition', ...},
        {'name': 'SafeHandler', 'type': 'Prompt', ...},
        {'name': 'ReviewHandler', 'type': 'LambdaFunction', ...},
        {'name': 'BlockHandler', 'type': 'Output', ...}
    ],
    'connections': [
        {'source': 'FlowInput', 'target': 'ClassifyContent'},
        {'source': 'ClassifyContent', 'target': 'RouteContent'},
        {
            'source': 'RouteContent',
            'target': 'SafeHandler',
            'condition': 'RouteContent.safe'
        },
        {
            'source': 'RouteContent',
            'target': 'ReviewHandler',
            'condition': 'RouteContent.review'
        },
        {
            'source': 'RouteContent',
            'target': 'BlockHandler',
            'condition': 'RouteContent.unsafe'
        }
    ]
}
```

### Pattern 4: Iterator Loop

Process array items.

```python
# Flow: Input → Iterator → Process Each → Collector → Output
iterator_flow = {
    'nodes': [
        {'name': 'FlowInput', 'type': 'Input', ...},
        {'name': 'IterateDocuments', 'type': 'Iterator', ...},
        {'name': 'SummarizeDoc', 'type': 'Prompt', ...},
        {'name': 'CollectSummaries', 'type': 'Collector', ...},
        {'name': 'FlowOutput', 'type': 'Output', ...}
    ],
    'connections': [
        {'source': 'FlowInput', 'target': 'IterateDocuments'},
        {'source': 'IterateDocuments', 'target': 'SummarizeDoc'},
        {'source': 'SummarizeDoc', 'target': 'CollectSummaries'},
        {'source': 'CollectSummaries', 'target': 'FlowOutput'}
    ]
}
```

### Pattern 5: DoWhile Refinement

Iteratively improve output.

```python
# Flow: Input → Generate → Evaluate → [Refine while quality < threshold] → Output
refinement_flow = {
    'nodes': [
        {'name': 'FlowInput', 'type': 'Input', ...},
        {'name': 'InitialGeneration', 'type': 'Prompt', ...},
        {'name': 'EvaluateQuality', 'type': 'Prompt', ...},
        {'name': 'RefineLoop', 'type': 'DoWhileLoop', ...},
        {'name': 'RefineResponse', 'type': 'Prompt', ...},
        {'name': 'FlowOutput', 'type': 'Output', ...}
    ],
    'connections': [
        {'source': 'FlowInput', 'target': 'InitialGeneration'},
        {'source': 'InitialGeneration', 'target': 'EvaluateQuality'},
        {'source': 'EvaluateQuality', 'target': 'RefineLoop'},
        # Inside loop
        {'source': 'RefineLoop', 'target': 'RefineResponse'},
        {'source': 'RefineResponse', 'target': 'EvaluateQuality'},
        # Exit loop
        {'source': 'RefineLoop', 'target': 'FlowOutput'}
    ]
}
```

## Best Practices

### Flow Design

1. **Single Input Node**: Every flow must have exactly one Input node
2. **Multiple Output Nodes**: Can have multiple Output nodes for different paths
3. **Use Collectors After Iterators**: Always collect results from iterator loops
4. **Keep Flows Modular**: Create reusable sub-flows for common patterns
5. **Limit Flow Complexity**: Split complex flows into multiple smaller flows

### Node Configuration

1. **Descriptive Node Names**: Use clear, purpose-driven names
2. **Variable Naming**: Use descriptive variable names in expressions
3. **Error Outputs**: Include error handling outputs where applicable
4. **Type Safety**: Match input/output types between connected nodes
5. **Default Values**: Provide fallbacks for optional inputs

### Version Management

1. **Create Versions for Stable Configurations**: Version before production
2. **Use Aliases for Deployments**: Never hardcode version numbers
3. **Semantic Versioning in Descriptions**: Track changes systematically
4. **Test Before Versioning**: Validate flows in console first
5. **Document Changes**: Describe what changed between versions

### Performance Optimization

1. **Minimize Sequential Dependencies**: Use parallel execution when possible
2. **Optimize Prompt Templates**: Reduce token usage with concise prompts
3. **Use Inline Code for Simple Logic**: Avoid Lambda overhead
4. **Cache Knowledge Base Results**: Reuse retrieval results when applicable
5. **Set Appropriate Token Limits**: Don't over-allocate maxTokens

### Error Handling

1. **Add Condition Nodes for Errors**: Route errors to fallback paths
2. **Provide Default Outputs**: Ensure flows always produce output
3. **Log Errors to CloudWatch**: Enable flow logging
4. **Implement Retry Logic**: Use DoWhile for transient failures
5. **Validate Inputs**: Check input format before processing

### Testing

1. **Test in Console First**: Use visual builder to validate flow
2. **Use Diverse Test Inputs**: Cover edge cases and error scenarios
3. **Validate All Paths**: Test each condition branch
4. **Check Performance**: Monitor execution time and costs
5. **Validate Error Paths**: Ensure error handling works

### Security

1. **Use IAM Roles**: Grant minimum required permissions
2. **Encrypt Data**: Use KMS for sensitive data
3. **Validate Inputs**: Sanitize user input before processing
4. **Use VPC Endpoints**: Keep traffic private when possible
5. **Audit Flow Access**: Track who creates and modifies flows

## Related Skills

- **bedrock-guardrails**: Add content safety to flows
- **bedrock-knowledge-bases**: RAG with Knowledge Base nodes
- **bedrock-prompts**: Use managed prompts in Prompt nodes
- **bedrock-agents**: Invoke agents within flows
- **boto3-bedrock**: Core Bedrock operations
- **aws-lambda**: Lambda function integration
- **cloudwatch-monitoring**: Flow metrics and alarms

## References

- [Amazon Bedrock Flows Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html)
- [Node Types Reference](https://docs.aws.amazon.com/bedrock/latest/userguide/flows-nodes.html)
- [Flows API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html)
- [CloudWatch Metrics for Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-cloudwatch.html)
