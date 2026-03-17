---
name: AI Workflow Orchestrator
description: Expert guidance for building AI-powered workflows with n8n, Zapier, and custom orchestration systems. Use when automating workflows, integrating AI agents, or building no-code/low-code automation.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# AI Workflow Orchestrator

Enterprise AI workflow automation with n8n, Zapier, and custom orchestration.

## n8n Workflow Patterns

### AI Agent Workflow

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "webhookId": "user-query"
    },
    {
      "name": "OpenAI Chat",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [450, 300],
      "parameters": {
        "model": "gpt-4-turbo",
        "temperature": 0.7,
        "systemMessage": "You are a helpful assistant."
      }
    },
    {
      "name": "Vector Store Query",
      "type": "@n8n/n8n-nodes-langchain.vectorStorePinecone",
      "typeVersion": 1,
      "position": [450, 150],
      "parameters": {
        "operation": "retrieve",
        "topK": 5
      }
    },
    {
      "name": "Response Formatter",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [650, 300],
      "parameters": {
        "functionCode": "return items.map(item => ({\n  json: {\n    response: item.json.response,\n    sources: item.json.sources,\n    confidence: item.json.confidence\n  }\n}));"
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Vector Store Query", "type": "main", "index": 0 }]]
    },
    "Vector Store Query": {
      "main": [[{ "node": "OpenAI Chat", "type": "main", "index": 0 }]]
    },
    "OpenAI Chat": {
      "main": [[{ "node": "Response Formatter", "type": "main", "index": 0 }]]
    }
  }
}
```

### Multi-Agent Orchestration

```typescript
// n8n Custom Node for Agent Orchestration
import { IExecuteFunctions } from 'n8n-core';
import { INodeExecutionData, INodeType, INodeTypeDescription } from 'n8n-workflow';

export class MultiAgentOrchestrator implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Multi-Agent Orchestrator',
    name: 'multiAgentOrchestrator',
    group: ['transform'],
    version: 1,
    description: 'Orchestrate multiple AI agents',
    defaults: {
      name: 'Multi-Agent Orchestrator',
    },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      {
        displayName: 'Agents',
        name: 'agents',
        type: 'fixedCollection',
        typeOptions: {
          multipleValues: true,
        },
        default: {},
        options: [
          {
            name: 'agentValues',
            displayName: 'Agent',
            values: [
              {
                displayName: 'Agent Name',
                name: 'name',
                type: 'string',
                default: '',
              },
              {
                displayName: 'Agent Type',
                name: 'type',
                type: 'options',
                options: [
                  { name: 'Researcher', value: 'researcher' },
                  { name: 'Writer', value: 'writer' },
                  { name: 'Reviewer', value: 'reviewer' },
                ],
                default: 'researcher',
              },
            ],
          },
        ],
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
      const input = this.getNodeParameter('input', itemIndex, '') as string;
      const agents = this.getNodeParameter('agents', itemIndex, {}) as any;

      const results: any[] = [];

      for (const agent of agents.agentValues || []) {
        const result = await this.executeAgent(agent.type, input);
        results.push({ agent: agent.name, result });
      }

      returnData.push({
        json: {
          input,
          results,
          summary: this.summarizeResults(results),
        },
      });
    }

    return [returnData];
  }

  private async executeAgent(type: string, input: string): Promise<string> {
    // Agent execution logic
    return `Result from ${type} agent`;
  }

  private summarizeResults(results: any[]): string {
    return results.map(r => r.result).join(' ');
  }
}
```

## Zapier Integration Patterns

### AI-Powered Email Automation

```javascript
// Zapier Custom Code Action
const inputData = inputData || {};
const { email_content, sender } = inputData;

// Call OpenAI API
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gpt-4-turbo',
    messages: [
      {
        role: 'system',
        content: 'You are an email assistant. Categorize and draft responses.',
      },
      {
        role: 'user',
        content: `Categorize and draft a response to this email:\n\n${email_content}`,
      },
    ],
  }),
});

const data = await response.json();
const ai_response = data.choices[0].message.content;

// Parse AI response
const category = ai_response.match(/Category: (.*)/)?.[1] || 'General';
const draft_response = ai_response.match(/Draft:([\s\S]*)/)?.[1]?.trim() || '';

output = {
  category,
  draft_response,
  priority: category === 'Urgent' ? 'high' : 'normal',
};
```

## Custom Orchestration System

### Workflow Engine

```python
from typing import Dict, List, Callable, Any
from pydantic import BaseModel
import asyncio

class WorkflowStep(BaseModel):
    name: str
    function: str
    inputs: Dict[str, str] = {}
    condition: str | None = None

class Workflow(BaseModel):
    name: str
    steps: List[WorkflowStep]

class WorkflowEngine:
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self.context: Dict[str, Any] = {}

    def register_function(self, name: str, func: Callable):
        """Register a function that can be used in workflows."""
        self.functions[name] = func

    async def execute_workflow(self, workflow: Workflow, initial_context: Dict[str, Any]):
        """Execute a workflow with the given context."""
        self.context = initial_context.copy()

        for step in workflow.steps:
            # Check condition
            if step.condition and not self._evaluate_condition(step.condition):
                continue

            # Prepare inputs
            inputs = {
                key: self._resolve_value(value)
                for key, value in step.inputs.items()
            }

            # Execute function
            func = self.functions.get(step.function)
            if not func:
                raise ValueError(f"Function not found: {step.function}")

            result = await func(**inputs) if asyncio.iscoroutinefunction(func) else func(**inputs)

            # Store result
            self.context[step.name] = result

        return self.context

    def _resolve_value(self, value: str) -> Any:
        """Resolve context variables in string values."""
        if value.startswith('$'):
            return self.context.get(value[1:])
        return value

    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate a condition expression."""
        return eval(condition, {}, self.context)

# Usage
engine = WorkflowEngine()

# Register AI functions
async def analyze_sentiment(text: str) -> str:
    # Call AI API
    return "positive"

async def generate_response(sentiment: str, text: str) -> str:
    # Call AI API
    return f"Response based on {sentiment} sentiment"

engine.register_function('analyze_sentiment', analyze_sentiment)
engine.register_function('generate_response', generate_response)

# Define workflow
workflow = Workflow(
    name="Email Response",
    steps=[
        WorkflowStep(
            name="sentiment",
            function="analyze_sentiment",
            inputs={"text": "$email_content"}
        ),
        WorkflowStep(
            name="response",
            function="generate_response",
            inputs={"sentiment": "$sentiment", "text": "$email_content"},
            condition="sentiment in ['positive', 'neutral']"
        ),
    ]
)

# Execute
result = await engine.execute_workflow(
    workflow,
    {"email_content": "Thank you for your help!"}
)
```

### Agent Chain Pattern

```typescript
interface Agent {
  name: string;
  execute: (input: any) => Promise<any>;
}

class AgentChain {
  private agents: Agent[] = [];

  add(agent: Agent): this {
    this.agents.push(agent);
    return this;
  }

  async execute(initialInput: any): Promise<any> {
    let result = initialInput;

    for (const agent of this.agents) {
      console.log(`Executing ${agent.name}...`);
      result = await agent.execute(result);
    }

    return result;
  }
}

// Usage
const chain = new AgentChain()
  .add({
    name: 'Researcher',
    execute: async (query: string) => {
      // Research logic
      return { query, sources: ['source1', 'source2'] };
    },
  })
  .add({
    name: 'Summarizer',
    execute: async (data: any) => {
      // Summarization logic
      return { ...data, summary: 'Summary of research' };
    },
  })
  .add({
    name: 'Formatter',
    execute: async (data: any) => {
      // Formatting logic
      return {
        title: data.query,
        content: data.summary,
        references: data.sources,
      };
    },
  });

const result = await chain.execute('What is quantum computing?');
```

## Integration Patterns

### Webhook Handlers

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class ZapierWebhook(BaseModel):
    event: str
    data: dict

@app.post("/zapier/webhook")
async def handle_zapier_webhook(webhook: ZapierWebhook):
    """Handle incoming Zapier webhooks."""
    if webhook.event == "new_lead":
        await process_lead(webhook.data)
    elif webhook.event == "support_ticket":
        await process_ticket(webhook.data)

    return {"status": "processed"}

@app.post("/n8n/webhook/{workflow_id}")
async def handle_n8n_webhook(workflow_id: str, request: Request):
    """Handle incoming n8n webhooks."""
    data = await request.json()
    result = await execute_workflow(workflow_id, data)
    return result
```

### Task Queues

```python
from celery import Celery
from typing import Dict

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def process_with_ai(data: Dict) -> Dict:
    """Process data with AI agent in background."""
    result = ai_agent.process(data)
    notify_completion(result)
    return result

# Trigger from workflow
process_with_ai.delay({"text": "Process this"})
```

## Best Practices

✅ Use idempotent operations
✅ Implement error handling and retries
✅ Add logging and monitoring
✅ Use task queues for long-running operations
✅ Implement rate limiting
✅ Version your workflows
✅ Test workflows thoroughly
✅ Use environment variables for secrets
✅ Implement rollback mechanisms
✅ Monitor workflow performance

---

**When to Use:** AI workflow automation, n8n/Zapier integrations, multi-agent orchestration, business process automation.
