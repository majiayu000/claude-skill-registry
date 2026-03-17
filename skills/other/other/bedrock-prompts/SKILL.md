---
name: bedrock-prompts
description: Amazon Bedrock Prompt Management for creating, versioning, and managing prompt templates with variables, multi-variant A/B testing, and flow integration. Use when creating reusable prompt templates, managing prompt versions, implementing A/B testing for prompts, integrating prompts with Bedrock Flows, optimizing prompt engineering, or building production prompt catalogs.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Amazon Bedrock Prompt Management

## Overview

Amazon Bedrock Prompt Management provides enterprise-grade capabilities for creating, versioning, testing, and deploying prompt templates. It enables teams to centralize prompt engineering, implement A/B testing, and integrate prompts across Bedrock Flows, Agents, and applications.

**Purpose**: Centralized prompt template management with version control, variable substitution, and multi-variant testing

**Pattern**: Task-based (independent operations for different prompt management tasks)

**Key Capabilities**:
1. **Prompt Templates** - Reusable templates with variable substitution
2. **Version Management** - Track changes, rollback, and staged deployment
3. **Multi-Variant Testing** - A/B test different prompt variations
4. **Flow Integration** - Use prompts in Bedrock Flows and Agents
5. **Variable Types** - String, number, array, and JSON object variables
6. **Prompt Catalog** - Centralized library for team collaboration
7. **Cross-Model Support** - Works with all Bedrock foundation models

**Quality Targets**:
- Reusability: 80%+ prompt template reuse across applications
- Version Control: 100% prompt changes tracked
- Testing: A/B test 3+ variants per production prompt
- Collaboration: Centralized catalog for team-wide access

---

## When to Use

Use bedrock-prompts when:

- Creating reusable prompt templates across applications
- Managing prompt versions for rollback and staged deployment
- Implementing A/B testing for prompt optimization
- Building centralized prompt catalogs for teams
- Integrating prompts with Bedrock Flows or Agents
- Standardizing prompt engineering practices
- Testing prompt variations before production deployment
- Sharing prompts across multiple projects
- Implementing variable substitution in prompts
- Optimizing prompts with data-driven testing

**When NOT to Use**:
- Single-use prompts without reuse (use inline prompts)
- Simple applications without version control needs
- Ad-hoc experimentation (test locally first, then promote to managed prompts)

---

## Prerequisites

### Required
- AWS account with Bedrock access
- IAM permissions for Bedrock Agent service
- Foundation model access enabled
- boto3 >= 1.34.0

### Recommended
- Understanding of prompt engineering best practices
- Familiarity with Bedrock Flows or Agents
- CloudWatch for monitoring prompt usage
- S3 for storing prompt test results

### Installation

```bash
pip install boto3 botocore
```

### IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:CreatePrompt",
        "bedrock:GetPrompt",
        "bedrock:UpdatePrompt",
        "bedrock:DeletePrompt",
        "bedrock:ListPrompts",
        "bedrock:CreatePromptVersion",
        "bedrock:ListPromptVersions",
        "bedrock:InvokeModel"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Quick Start

### 1. Create Prompt Template

```python
import boto3
import json

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

response = bedrock_agent.create_prompt(
    name='customer-support-prompt',
    description='Customer support response template',
    variants=[
        {
            'name': 'default',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': '''You are a helpful customer support agent for {{company_name}}.

Customer Query: {{customer_query}}

Instructions:
- Be professional and empathetic
- Provide clear, actionable solutions
- If you don't know, offer to escalate
- Keep responses under {{max_words}} words

Response:''',
                    'inputVariables': [
                        {
                            'name': 'company_name'
                        },
                        {
                            'name': 'customer_query'
                        },
                        {
                            'name': 'max_words'
                        }
                    ]
                }
            },
            'inferenceConfiguration': {
                'text': {
                    'maxTokens': 500,
                    'temperature': 0.7,
                    'topP': 0.9
                }
            }
        }
    ]
)

prompt_id = response['id']
prompt_arn = response['arn']
print(f"Created prompt: {prompt_id}")
print(f"ARN: {prompt_arn}")
```

### 2. Create Prompt Version

```python
# Create immutable version for production
version_response = bedrock_agent.create_prompt_version(
    promptIdentifier=prompt_id,
    description='Production v1.0 - Initial release'
)

version = version_response['version']
print(f"Created version: {version}")
```

### 3. Get and Use Prompt

```python
# Get prompt details
prompt = bedrock_agent.get_prompt(
    promptIdentifier=prompt_id,
    promptVersion=version
)

# Extract template and variables
template = prompt['variants'][0]['templateConfiguration']['text']['text']
variables = {var['name']: None for var in prompt['variants'][0]['templateConfiguration']['text']['inputVariables']}

print(f"Template: {template}")
print(f"Variables: {list(variables.keys())}")
```

---

## Operations

### Operation 1: create-prompt

Create a new prompt template with variables and inference configuration.

**Use when**: Building reusable prompt templates, standardizing prompts across applications, creating prompt catalogs

**Code Example**:

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create advanced prompt with multiple variable types
response = bedrock_agent.create_prompt(
    name='product-recommendation-prompt',
    description='E-commerce product recommendation engine',
    defaultVariant='optimized',
    variants=[
        {
            'name': 'optimized',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': '''You are a product recommendation expert for an e-commerce platform.

User Profile:
- Name: {{user_name}}
- Purchase History: {{purchase_history}}
- Preferences: {{preferences}}
- Budget: ${{budget}}

Available Categories: {{categories}}

Task: Recommend {{num_recommendations}} products that match the user's profile.

Format your response as a JSON array with product_id, name, price, and reason.''',
                    'inputVariables': [
                        {'name': 'user_name'},
                        {'name': 'purchase_history'},
                        {'name': 'preferences'},
                        {'name': 'budget'},
                        {'name': 'categories'},
                        {'name': 'num_recommendations'}
                    ]
                }
            },
            'inferenceConfiguration': {
                'text': {
                    'maxTokens': 1000,
                    'temperature': 0.5,
                    'topP': 0.95,
                    'stopSequences': ['\n\n---']
                }
            }
        }
    ],
    tags={
        'Environment': 'production',
        'Team': 'recommendations',
        'CostCenter': 'engineering'
    }
)

print(f"Prompt ID: {response['id']}")
print(f"Prompt ARN: {response['arn']}")
print(f"Created At: {response['createdAt']}")
```

**Best Practices**:
- Use descriptive names with hyphens (e.g., `customer-support-prompt`)
- Document variable types and expected formats
- Set appropriate `maxTokens` to control costs
- Use `defaultVariant` to specify preferred version
- Add tags for cost tracking and organization

---

### Operation 2: create-prompt-version

Create immutable versions of prompts for production deployment and rollback.

**Use when**: Deploying prompts to production, implementing staged rollout, enabling rollback capability

**Code Example**:

```python
import boto3
from datetime import datetime

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create version with detailed description
version_response = bedrock_agent.create_prompt_version(
    promptIdentifier='prompt-12345',
    description=f'Production v2.0 - {datetime.now().isoformat()} - Added sentiment analysis',
    tags={
        'Version': '2.0',
        'ReleaseDate': datetime.now().strftime('%Y-%m-%d'),
        'Changelog': 'Added sentiment context to improve response quality'
    }
)

version_number = version_response['version']
version_arn = version_response['arn']

print(f"Version: {version_number}")
print(f"ARN: {version_arn}")

# List all versions
list_response = bedrock_agent.list_prompts(
    promptIdentifier='prompt-12345'
)

print("\nAll versions:")
for version in list_response.get('promptSummaries', []):
    print(f"- Version {version['version']}: {version.get('description', 'No description')}")
```

**Version Management Best Practices**:
- Create versions before production deployment
- Use semantic versioning in descriptions (v1.0, v1.1, v2.0)
- Document changes in version descriptions
- Keep DRAFT version for active development
- Test versions thoroughly before promoting

---

### Operation 3: get-prompt

Retrieve prompt details including template, variables, and inference configuration.

**Use when**: Inspecting prompt templates, debugging issues, preparing for invocation

**Code Example**:

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Get specific version
prompt = bedrock_agent.get_prompt(
    promptIdentifier='prompt-12345',
    promptVersion='2'  # Omit for DRAFT version
)

# Extract configuration
variant = prompt['variants'][0]
template = variant['templateConfiguration']['text']['text']
variables = variant['templateConfiguration']['text']['inputVariables']
inference_config = variant['inferenceConfiguration']['text']

print(f"Prompt Name: {prompt['name']}")
print(f"Version: {prompt['version']}")
print(f"Model: {variant['modelId']}")
print(f"\nTemplate:\n{template}")
print(f"\nVariables:")
for var in variables:
    print(f"  - {var['name']}")
print(f"\nInference Config:")
print(f"  Max Tokens: {inference_config['maxTokens']}")
print(f"  Temperature: {inference_config['temperature']}")
print(f"  Top P: {inference_config['topP']}")
```

---

### Operation 4: list-prompts

List all prompts or filter by criteria.

**Use when**: Building prompt catalogs, auditing prompt usage, discovering available prompts

**Code Example**:

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# List all prompts with pagination
paginator = bedrock_agent.get_paginator('list_prompts')
page_iterator = paginator.paginate()

prompts = []
for page in page_iterator:
    prompts.extend(page.get('promptSummaries', []))

print(f"Total prompts: {len(prompts)}")
print("\nPrompt Catalog:")
for prompt in prompts:
    print(f"\n- {prompt['name']} (ID: {prompt['id']})")
    print(f"  Description: {prompt.get('description', 'N/A')}")
    print(f"  Created: {prompt['createdAt']}")
    print(f"  Updated: {prompt['updatedAt']}")
    print(f"  Version: {prompt['version']}")
```

---

### Operation 5: update-prompt

Update prompt templates, add variants, or modify inference configuration.

**Use when**: Improving prompts, adding A/B test variants, adjusting inference parameters

**Code Example**:

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Update prompt with new variant
response = bedrock_agent.update_prompt(
    promptIdentifier='prompt-12345',
    name='customer-support-prompt',
    description='Customer support with multiple response styles',
    defaultVariant='professional',
    variants=[
        {
            'name': 'professional',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': 'Professional tone template...',
                    'inputVariables': [{'name': 'query'}]
                }
            },
            'inferenceConfiguration': {
                'text': {'maxTokens': 500, 'temperature': 0.3}
            }
        },
        {
            'name': 'friendly',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': 'Friendly tone template...',
                    'inputVariables': [{'name': 'query'}]
                }
            },
            'inferenceConfiguration': {
                'text': {'maxTokens': 500, 'temperature': 0.7}
            }
        }
    ]
)

print(f"Updated prompt: {response['id']}")
```

---

### Operation 6: delete-prompt

Delete prompt templates (cannot be undone).

**Use when**: Cleaning up unused prompts, removing deprecated templates

**Code Example**:

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Delete prompt (all versions)
response = bedrock_agent.delete_prompt(
    promptIdentifier='prompt-12345'
)

print(f"Deleted prompt: {response['id']}")
print(f"Status: {response['status']}")
```

**Warning**: Deletion is permanent and affects all versions. Ensure prompt is not used in Flows or Agents before deleting.

---

## Variable Types and Substitution

### Supported Variable Types

Bedrock Prompt Management supports multiple variable types:

1. **String**: Text values (default)
2. **Number**: Numeric values
3. **Array**: Lists of items
4. **JSON Object**: Complex structured data

### Variable Substitution Example

```python
import boto3
import json

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Create prompt with complex variables
prompt_response = bedrock_agent.create_prompt(
    name='data-analysis-prompt',
    variants=[{
        'name': 'default',
        'templateType': 'TEXT',
        'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'templateConfiguration': {
            'text': {
                'text': '''Analyze the following data:

Dataset: {{dataset_name}}
Columns: {{columns}}
Row Count: {{row_count}}
Sample Data: {{sample_data}}

Analysis Type: {{analysis_type}}

Provide insights and recommendations.''',
                'inputVariables': [
                    {'name': 'dataset_name'},
                    {'name': 'columns'},
                    {'name': 'row_count'},
                    {'name': 'sample_data'},
                    {'name': 'analysis_type'}
                ]
            }
        }
    }]
)

# Use prompt with variable substitution
prompt = bedrock_agent.get_prompt(
    promptIdentifier=prompt_response['id']
)

template = prompt['variants'][0]['templateConfiguration']['text']['text']

# Substitute variables
variables = {
    'dataset_name': 'Sales Q4 2024',
    'columns': json.dumps(['date', 'product', 'revenue', 'quantity']),
    'row_count': '10,000',
    'sample_data': json.dumps([
        {'date': '2024-10-01', 'product': 'Widget A', 'revenue': 1500, 'quantity': 50},
        {'date': '2024-10-02', 'product': 'Widget B', 'revenue': 2000, 'quantity': 75}
    ]),
    'analysis_type': 'Revenue trends and product performance'
}

# Replace variables in template
prompt_text = template
for var_name, var_value in variables.items():
    prompt_text = prompt_text.replace(f'{{{{{var_name}}}}}', str(var_value))

print(f"Final Prompt:\n{prompt_text}")
```

---

## Multi-Variant Testing (A/B Testing)

### Creating Multi-Variant Prompts

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create prompt with 3 variants for A/B/C testing
response = bedrock_agent.create_prompt(
    name='email-subject-generator',
    description='A/B/C test for email subject lines',
    defaultVariant='variant-a',
    variants=[
        {
            'name': 'variant-a',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': 'Generate a professional email subject line for: {{email_content}}',
                    'inputVariables': [{'name': 'email_content'}]
                }
            },
            'inferenceConfiguration': {
                'text': {'maxTokens': 50, 'temperature': 0.3}
            }
        },
        {
            'name': 'variant-b',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': 'Create an engaging, click-worthy subject line for: {{email_content}}',
                    'inputVariables': [{'name': 'email_content'}]
                }
            },
            'inferenceConfiguration': {
                'text': {'maxTokens': 50, 'temperature': 0.7}
            }
        },
        {
            'name': 'variant-c',
            'templateType': 'TEXT',
            'modelId': 'anthropic.claude-3-haiku-20240307-v1:0',
            'templateConfiguration': {
                'text': {
                    'text': 'Write a concise, action-oriented subject line for: {{email_content}}',
                    'inputVariables': [{'name': 'email_content'}]
                }
            },
            'inferenceConfiguration': {
                'text': {'maxTokens': 50, 'temperature': 0.5}
            }
        }
    ]
)

print(f"Created multi-variant prompt: {response['id']}")
```

### Testing Framework

```python
import boto3
import random
import json
from datetime import datetime

class PromptABTester:
    def __init__(self, prompt_id, region='us-east-1'):
        self.bedrock_agent = boto3.client('bedrock-agent', region_name=region)
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        self.prompt_id = prompt_id
        self.results = []

    def get_variants(self):
        prompt = self.bedrock_agent.get_prompt(promptIdentifier=self.prompt_id)
        return [v['name'] for v in prompt['variants']]

    def test_variant(self, variant_name, variables, user_id=None):
        # Get prompt
        prompt = self.bedrock_agent.get_prompt(promptIdentifier=self.prompt_id)

        # Find variant
        variant = next(v for v in prompt['variants'] if v['name'] == variant_name)

        # Substitute variables
        template = variant['templateConfiguration']['text']['text']
        for var_name, var_value in variables.items():
            template = template.replace(f'{{{{{var_name}}}}}', str(var_value))

        # Invoke model
        model_id = variant['modelId']
        inference_config = variant['inferenceConfiguration']['text']

        response = self.bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{'role': 'user', 'content': template}],
                'max_tokens': inference_config['maxTokens'],
                'temperature': inference_config['temperature']
            })
        )

        result = json.loads(response['body'].read())
        output = result['content'][0]['text']

        # Record test result
        self.results.append({
            'timestamp': datetime.now().isoformat(),
            'variant': variant_name,
            'user_id': user_id,
            'input_variables': variables,
            'output': output,
            'model': model_id
        })

        return output

    def random_test(self, variables, user_id=None):
        """Randomly select variant for testing"""
        variants = self.get_variants()
        selected_variant = random.choice(variants)
        return self.test_variant(selected_variant, variables, user_id)

    def analyze_results(self):
        """Analyze test results by variant"""
        analysis = {}
        for result in self.results:
            variant = result['variant']
            if variant not in analysis:
                analysis[variant] = {
                    'count': 0,
                    'avg_output_length': 0,
                    'samples': []
                }

            analysis[variant]['count'] += 1
            analysis[variant]['samples'].append(result['output'])
            analysis[variant]['avg_output_length'] += len(result['output'])

        # Calculate averages
        for variant in analysis:
            count = analysis[variant]['count']
            analysis[variant]['avg_output_length'] /= count

        return analysis

# Usage
tester = PromptABTester('prompt-12345')

# Run A/B test
for i in range(100):
    result = tester.random_test(
        variables={'email_content': f'Test email content {i}'},
        user_id=f'user-{i}'
    )

# Analyze
analysis = tester.analyze_results()
print(json.dumps(analysis, indent=2))
```

---

## Prompt Engineering Best Practices

### 1. Clear Instructions

```python
# Good: Specific, clear instructions
prompt = '''You are a financial analyst.

Task: Analyze the following quarterly earnings data and provide:
1. Revenue trends (% change YoY)
2. Key growth drivers
3. Risk factors

Data: {{financial_data}}

Format: Use bullet points. Keep analysis under 200 words.'''

# Bad: Vague, unclear
prompt = '''Analyze this: {{financial_data}}'''
```

### 2. Variable Naming Conventions

```python
# Good: Descriptive variable names
inputVariables=[
    {'name': 'customer_query'},
    {'name': 'customer_purchase_history'},
    {'name': 'max_response_words'}
]

# Bad: Ambiguous names
inputVariables=[
    {'name': 'input'},
    {'name': 'data'},
    {'name': 'limit'}
]
```

### 3. Inference Configuration

```python
# Creative tasks: Higher temperature
'inferenceConfiguration': {
    'text': {
        'maxTokens': 1000,
        'temperature': 0.8,  # More creative
        'topP': 0.95
    }
}

# Factual tasks: Lower temperature
'inferenceConfiguration': {
    'text': {
        'maxTokens': 500,
        'temperature': 0.1,  # More deterministic
        'topP': 0.9
    }
}
```

### 4. Stop Sequences

```python
# Use stop sequences to control output length
'inferenceConfiguration': {
    'text': {
        'maxTokens': 1000,
        'stopSequences': ['\n\n---', 'END_RESPONSE', '###']
    }
}
```

---

## Integration with Bedrock Flows

### Using Prompts in Flows

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create flow that uses managed prompt
flow_response = bedrock_agent.create_flow(
    name='customer-support-flow',
    executionRoleArn='arn:aws:iam::123456789012:role/BedrockFlowRole',
    definition={
        'nodes': [
            {
                'name': 'FlowInput',
                'type': 'Input',
                'outputs': [{'name': 'query', 'type': 'String'}]
            },
            {
                'name': 'SupportPrompt',
                'type': 'Prompt',
                'configuration': {
                    'prompt': {
                        'sourceConfiguration': {
                            'resource': {
                                'promptArn': 'arn:aws:bedrock:us-east-1:123456789012:prompt/prompt-12345:2'
                            }
                        }
                    }
                },
                'inputs': [
                    {
                        'name': 'customer_query',
                        'expression': 'FlowInput.query'
                    },
                    {
                        'name': 'company_name',
                        'expression': '"Acme Corp"'
                    },
                    {
                        'name': 'max_words',
                        'expression': '150'
                    }
                ],
                'outputs': [{'name': 'response', 'type': 'String'}]
            },
            {
                'name': 'FlowOutput',
                'type': 'Output',
                'inputs': [
                    {
                        'name': 'response',
                        'expression': 'SupportPrompt.response'
                    }
                ]
            }
        ],
        'connections': [
            {'source': 'FlowInput', 'target': 'SupportPrompt'},
            {'source': 'SupportPrompt', 'target': 'FlowOutput'}
        ]
    }
)

print(f"Created flow: {flow_response['id']}")
```

---

## Related Skills

- **bedrock-inference**: Invoke foundation models directly
- **bedrock-flows**: Build visual AI workflows with prompts
- **bedrock-agentcore**: Create AI agents with managed prompts
- **bedrock-knowledge-bases**: RAG applications with prompt templates
- **bedrock-guardrails**: Apply safety policies to prompt outputs
- **claude-advanced-tool-use**: Advanced prompt patterns for tool use
- **context-engineering**: Optimize prompt context and token usage
- **prompt-builder**: Build effective prompts (meta-skill)

---

## Complete Example: Production Prompt Catalog

```python
import boto3
import json
from typing import Dict, List, Optional

class PromptCatalog:
    """Enterprise prompt catalog with versioning and testing"""

    def __init__(self, region='us-east-1'):
        self.bedrock_agent = boto3.client('bedrock-agent', region_name=region)
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        self.catalog = {}

    def create_prompt_template(
        self,
        name: str,
        description: str,
        template: str,
        variables: List[str],
        model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0',
        max_tokens: int = 1000,
        temperature: float = 0.7,
        tags: Optional[Dict] = None
    ) -> str:
        """Create a new prompt template"""

        response = self.bedrock_agent.create_prompt(
            name=name,
            description=description,
            variants=[{
                'name': 'default',
                'templateType': 'TEXT',
                'modelId': model_id,
                'templateConfiguration': {
                    'text': {
                        'text': template,
                        'inputVariables': [{'name': var} for var in variables]
                    }
                },
                'inferenceConfiguration': {
                    'text': {
                        'maxTokens': max_tokens,
                        'temperature': temperature,
                        'topP': 0.9
                    }
                }
            }],
            tags=tags or {}
        )

        prompt_id = response['id']
        self.catalog[name] = prompt_id
        return prompt_id

    def version_prompt(self, name: str, description: str) -> str:
        """Create immutable version"""
        prompt_id = self.catalog[name]
        response = self.bedrock_agent.create_prompt_version(
            promptIdentifier=prompt_id,
            description=description
        )
        return response['version']

    def get_prompt(self, name: str, version: Optional[str] = None) -> Dict:
        """Get prompt by name"""
        prompt_id = self.catalog[name]
        return self.bedrock_agent.get_prompt(
            promptIdentifier=prompt_id,
            promptVersion=version
        ) if version else self.bedrock_agent.get_prompt(promptIdentifier=prompt_id)

    def list_catalog(self) -> List[Dict]:
        """List all prompts in catalog"""
        response = self.bedrock_agent.list_prompts()
        return response.get('promptSummaries', [])

# Usage
catalog = PromptCatalog(region='us-east-1')

# Create customer support prompt
support_id = catalog.create_prompt_template(
    name='customer-support-v1',
    description='Customer support response generator',
    template='''You are a customer support agent for {{company_name}}.

Query: {{query}}

Provide a helpful, professional response in under {{max_words}} words.''',
    variables=['company_name', 'query', 'max_words'],
    max_tokens=500,
    temperature=0.5,
    tags={'Department': 'Support', 'Environment': 'Production'}
)

# Create version
version = catalog.version_prompt('customer-support-v1', 'Initial production release')

print(f"Created prompt: {support_id}")
print(f"Version: {version}")

# List catalog
prompts = catalog.list_catalog()
print(f"\nCatalog contains {len(prompts)} prompts")
```

---

## Summary

Amazon Bedrock Prompt Management provides enterprise-grade prompt template capabilities:

1. **Centralized Management**: Single source of truth for prompts
2. **Version Control**: Track changes, rollback, staged deployment
3. **A/B Testing**: Multi-variant testing for optimization
4. **Variable Substitution**: Flexible templating system
5. **Flow Integration**: Use prompts across Bedrock services
6. **Team Collaboration**: Shared prompt catalog
7. **Production Ready**: Immutable versions, tagging, monitoring

Use bedrock-prompts to standardize prompt engineering, enable A/B testing, and build reusable prompt libraries for production AI applications.
