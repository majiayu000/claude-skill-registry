---
name: LangGraph Development
description: Create LangGraph workflows as NestJS applications under apps/langgraph/. Use same webhook pattern as n8n, receive same parameters (taskId, conversationId, userId, provider, model, statusWebhook). Wrap as API agents with request/response transforms. CRITICAL: Status webhook URL must read from environment variables. All endpoints follow A2A protocol.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# LangGraph Development Skill

**CRITICAL**: LangGraph workflows are NestJS applications under `apps/langgraph/`. They receive the same parameters as n8n workflows and use the same webhook status pattern. Wrap them as API agents.

## When to Use This Skill

Use this skill when:
- Creating new LangGraph workflows
- Setting up LangGraph as a NestJS application
- Configuring webhook status tracking for LangGraph
- Wrapping LangGraph endpoints as API agents
- Integrating LangGraph with A2A protocol

## Directory Structure

LangGraph applications follow the same pattern as n8n:

```
apps/
├── api/              # Main NestJS API
├── n8n/              # N8N workflows (existing)
├── langgraph/        # LangGraph workflows (NEW)
│   ├── src/
│   │   ├── main.ts
│   │   ├── app.module.ts
│   │   ├── workflows/
│   │   │   └── example-workflow.ts
│   │   └── controllers/
│   │       └── langgraph.controller.ts
│   ├── package.json
│   └── tsconfig.json
├── crewai/           # CrewAI workflows (FUTURE)
└── openai/           # OpenAI workflows (FUTURE)
```

## NestJS Application Pattern

Each LangGraph application is a standalone NestJS app. Example structure:

### Main Entry Point

```typescript
// apps/langgraph/src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Port from environment or default
  const port = process.env.PORT || 8000;
  
  await app.listen(port);
  console.log(`LangGraph service running on port ${port}`);
}
bootstrap();
```

### App Module

```typescript
// apps/langgraph/src/app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { LangGraphController } from './controllers/langgraph.controller';
import { LangGraphService } from './services/langgraph.service';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: ['.env'],
    }),
  ],
  controllers: [LangGraphController],
  providers: [LangGraphService],
})
export class AppModule {}
```

## Webhook Endpoint Pattern

### Required Parameters

LangGraph endpoints receive the same parameters as n8n workflows:

```typescript
interface LangGraphRequest {
  taskId: string;
  conversationId: string;
  userId: string;
  userMessage: string;  // Or "prompt" or "announcement"
  statusWebhook: string; // MUST read from env: API_BASE_URL/webhooks/status
  provider?: string;     // "openai" | "anthropic" | "ollama"
  model?: string;        // Model name
  stepName?: string;     // For status tracking
  sequence?: number;     // Step sequence number
  totalSteps?: number;   // Total steps in workflow
}
```

### Controller Example

```typescript
// apps/langgraph/src/controllers/langgraph.controller.ts
import { Controller, Post, Body, Logger } from '@nestjs/common';
import { LangGraphService } from '../services/langgraph.service';

interface LangGraphWorkflowRequest {
  taskId: string;
  conversationId: string;
  userId: string;
  userMessage: string;
  statusWebhook: string;
  provider?: string;
  model?: string;
  stepName?: string;
  sequence?: number;
  totalSteps?: number;
}

@Controller('api/orchestrate')
export class LangGraphController {
  private readonly logger = new Logger(LangGraphController.name);

  constructor(private readonly langGraphService: LangGraphService) {}

  @Post()
  async executeWorkflow(@Body() request: LangGraphWorkflowRequest) {
    this.logger.log(`Executing LangGraph workflow for task ${request.taskId}`);
    
    // Send start status if statusWebhook provided
    if (request.statusWebhook) {
      await this.sendStatus(request.statusWebhook, {
        taskId: request.taskId,
        status: 'started',
        stepName: request.stepName || 'workflow-start',
        sequence: request.sequence || 0,
        totalSteps: request.totalSteps || 1,
      });
    }

    // Execute LangGraph workflow
    const result = await this.langGraphService.execute(request);

    // Send completion status
    if (request.statusWebhook) {
      await this.sendStatus(request.statusWebhook, {
        taskId: request.taskId,
        status: 'completed',
        stepName: request.stepName || 'workflow-complete',
        sequence: request.sequence || (request.totalSteps || 1),
        totalSteps: request.totalSteps || 1,
      });
    }

    return {
      status: 'completed',
      payload: {
        content: result.content,
        metadata: result.metadata,
      },
    };
  }

  private async sendStatus(webhookUrl: string, status: any) {
    try {
      await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(status),
      });
    } catch (error) {
      this.logger.warn(`Failed to send status to ${webhookUrl}:`, error);
    }
  }
}
```

## Status Webhook Configuration

### ❌ WRONG - Hardcoded URL

```typescript
// ❌ WRONG
const statusWebhook = 'http://host.docker.internal:7100/webhooks/status';
```

### ✅ CORRECT - Environment Variable

```typescript
// ✅ CORRECT
const apiBaseUrl = process.env.API_BASE_URL || process.env.VITE_API_BASE_URL || 'http://host.docker.internal:7100';
const statusWebhook = `${apiBaseUrl}/webhooks/status`;
```

**In API Agent Configuration:**

```yaml
api_configuration:
  request_transform:
    format: "custom"
    template: |
      {
        "taskId": "{{taskId}}",
        "conversationId": "{{conversationId}}",
        "userId": "{{userId}}",
        "userMessage": "{{userMessage}}",
        "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status",
        "provider": "{{payload.provider}}",
        "model": "{{payload.model}}"
      }
```

## Wrapping as API Agent

### API Agent Configuration

```yaml
metadata:
  name: "langgraph-example"
  displayName: "LangGraph Example Workflow"
  description: "Example LangGraph workflow wrapped as API agent"
  version: "0.1.0"
  type: "api"

api_configuration:
  endpoint: "http://localhost:8000/api/orchestrate"
  method: "POST"
  timeout: 120000
  headers:
    Content-Type: "application/json"
  request_transform:
    format: "custom"
    template: |
      {
        "taskId": "{{taskId}}",
        "conversationId": "{{conversationId}}",
        "userId": "{{userId}}",
        "userMessage": "{{userMessage}}",
        "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status",
        "provider": "{{payload.provider}}",
        "model": "{{payload.model}}"
      }
  response_transform:
    format: "field_extraction"
    field: "payload.content"

configuration:
  execution_capabilities:
    supports_converse: false
    supports_plan: false
    supports_build: true
```

## A2A Protocol Compliance

LangGraph endpoints must follow A2A protocol:

1. **Health Endpoint**: `GET /health`
2. **Agent Card**: `GET /.well-known/agent.json`
3. **Task Execution**: `POST /api/orchestrate`

### Health Endpoint

```typescript
@Controller()
export class LangGraphController {
  @Get('health')
  health() {
    return { status: 'ok', service: 'langgraph' };
  }
}
```

### Agent Card Endpoint

```typescript
@Get('.well-known/agent.json')
agentCard() {
  return {
    name: 'langgraph-example',
    displayName: 'LangGraph Example Workflow',
    description: 'Example LangGraph workflow',
    type: 'api',
    version: '0.1.0',
    capabilities: {
      modes: ['build'],
      inputModes: ['application/json'],
      outputModes: ['application/json'],
    },
  };
}
```

## Real-time and Polling Support

LangGraph workflows support both real-time (SSE) and polling:

### Real-time (SSE) Pattern

```typescript
@Post('stream')
async streamWorkflow(@Body() request: LangGraphWorkflowRequest, @Res() res: Response) {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Stream workflow steps
  for await (const step of this.langGraphService.streamExecute(request)) {
    res.write(`data: ${JSON.stringify(step)}\n\n`);
  }

  res.end();
}
```

### Polling Pattern

```typescript
@Post('async')
async executeAsync(@Body() request: LangGraphWorkflowRequest) {
  const taskId = request.taskId;
  
  // Start workflow in background
  this.langGraphService.executeAsync(request);
  
  return {
    taskId,
    status: 'processing',
    statusUrl: `/api/orchestrate/status/${taskId}`,
  };
}

@Get('status/:taskId')
async getStatus(@Param('taskId') taskId: string) {
  return this.langGraphService.getStatus(taskId);
}
```

## Response Structure

LangGraph workflows return standardized responses:

```typescript
interface LangGraphResponse {
  status: 'completed' | 'error' | 'processing';
  payload: {
    content: string;        // Main content
    metadata?: {
      steps?: number;
      duration?: number;
      [key: string]: unknown;
    };
  };
  error?: {
    message: string;
    code?: string;
  };
}
```

## Complete Example: LangGraph Workflow Service

```typescript
// apps/langgraph/src/services/langgraph.service.ts
import { Injectable, Logger } from '@nestjs/common';
import { StateGraph } from '@langchain/langgraph';

@Injectable()
export class LangGraphService {
  private readonly logger = new Logger(LangGraphService.name);

  async execute(request: LangGraphWorkflowRequest) {
    // Build LangGraph state machine
    const workflow = this.buildWorkflow(request);
    
    // Execute workflow
    const result = await workflow.invoke({
      messages: [{ role: 'user', content: request.userMessage }],
      provider: request.provider || 'openai',
      model: request.model || 'gpt-4',
    });

    return {
      content: result.output,
      metadata: {
        steps: result.steps,
        duration: result.duration,
      },
    };
  }

  private buildWorkflow(request: LangGraphWorkflowRequest) {
    // Create LangGraph state machine
    const workflow = new StateGraph({
      // Define workflow nodes and edges
    });

    return workflow.compile();
  }
}
```

## Checklist for LangGraph Development

When creating LangGraph workflows:

- [ ] NestJS application created under `apps/langgraph/`
- [ ] `package.json` configured with NestJS dependencies
- [ ] Controller receives all required parameters (taskId, conversationId, userId, etc.)
- [ ] Status webhook URL reads from environment (not hardcoded)
- [ ] Webhook status tracking implemented (start/complete)
- [ ] Response structure matches expected format
- [ ] Wrapped as API agent with proper request/response transforms
- [ ] A2A protocol endpoints implemented (health, agent card)
- [ ] Real-time (SSE) or polling support if needed
- [ ] Error handling implemented
- [ ] Logging configured

## Related Documentation

- **N8N Development**: See N8N Development Skill for parameter reference
- **API Agent Development**: See API Agent Development Skill for wrapping patterns
- **Back-End Structure**: See Back-End Structure Skill for A2A protocol details

