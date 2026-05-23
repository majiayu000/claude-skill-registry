---
name: Back-End Structure
description: Build NestJS backend following Orchestrator AI patterns. Module/Service/Controller structure, A2A protocol compliance, transport types, error handling. CRITICAL: Files follow kebab-case naming. Controllers handle HTTP, Services contain business logic, Modules organize dependencies.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Back-End Structure Skill

**CRITICAL**: NestJS backend follows strict patterns: kebab-case file names, module/service/controller separation, A2A protocol compliance, transport types usage.

## When to Use This Skill

Use this skill when:
- Creating new NestJS modules
- Creating new services or controllers
- Working with A2A protocol
- Using transport types
- Structuring backend code

## File Naming Conventions

### ✅ CORRECT - Kebab-Case

```
apps/api/src/
├── agent-platform/
│   ├── services/
│   │   ├── agent-runtime-dispatch.service.ts
│   │   └── agent-registry.service.ts
│   ├── controllers/
│   │   └── agents-admin.controller.ts
│   └── agent-platform.module.ts
└── agent2agent/
    ├── services/
    │   └── agent-tasks.service.ts
    └── agent2agent.module.ts
```

### ❌ WRONG - PascalCase or camelCase

```
❌ AgentRuntimeDispatch.service.ts
❌ agentRuntimeDispatch.service.ts
❌ AgentsAdmin.controller.ts
```

## Module Structure Pattern

From `apps/api/src/app.module.ts`:

```24:60:apps/api/src/app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: [
        join(__dirname, '../../../.env'),
        '../../.env',
        join(process.cwd(), '.env'),
        '.env',
      ],
      expandVariables: true,
    }),
    // Core Infrastructure
    HttpModule,
    SupabaseModule,
    AuthModule,
    HealthModule,
    WebSocketModule,
    MCPModule,
    EventEmitterModule.forRoot(),
    ScheduleModule.forRoot(),

    // Main Modules (consolidated)
    LLMModule, // Includes: providers, models, evaluation, cidafm, usage, langchain, pii
    Agent2AgentModule, // Includes: conversations, tasks, deliverables, projects, context-optimization, orchestration
    AgentPlatformModule, // Includes: database agents, registry, hierarchy

    // Standalone Features
    SovereignPolicyModule,
    SystemModule,
    AssetsModule,
    WebhooksModule,
  ],
  controllers: [AppController, AnalyticsController],
  providers: [AppService, AgentRegistryService],
})
export class AppModule {}
```

### Module Example

From `apps/api/src/mcp/mcp.module.ts`:

```23:58:apps/api/src/mcp/mcp.module.ts
@Module({
  imports: [
    HttpModule,
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    LLMModule,
  ],
  controllers: [MCPController],
  providers: [
    MCPService,
    MCPClientService,

    // Service namespace handlers
    SupabaseMCPService,
    SlackMCPTools,
    NotionMCPTools,

    // Additional service handlers can be added here
    // SQLServerMCPService,
    // PostgresMCPService,
    // AsanaMCPService,
    // TrelloMCPService,
    // FileMCPService,
    // SystemMCPService,
  ],
  exports: [
    MCPService,
    MCPClientService,

    // Export service handlers for use in other modules
    SupabaseMCPService,
    SlackMCPTools,
    NotionMCPTools,
  ],
})
export class MCPModule {
```

**Key Pattern:**
- `imports`: Other modules this module depends on
- `controllers`: HTTP controllers that handle routes
- `providers`: Services, repositories, factories
- `exports`: What other modules can use from this module

## Controller Pattern

From `apps/api/src/agent2agent/agent2agent.controller.ts`:

```129:146:apps/api/src/agent2agent/agent2agent.controller.ts
@Controller()
export class Agent2AgentController {
  constructor(
    private readonly cardBuilder: AgentCardBuilderService,
    private readonly gateway: AgentExecutionGateway,
    private readonly tasksService: Agent2AgentTasksService,
    private readonly agentTaskStatusService: Agent2AgentTaskStatusService,
    private readonly taskStatusCache: TaskStatusService,
    private readonly agentConversationsService: Agent2AgentConversationsService,
    private readonly agentRegistry: AgentRegistryService,
    private readonly agentDeliverablesService: Agent2AgentDeliverablesService,
    private readonly supabaseService: SupabaseService,
    private readonly streamTokenService: StreamTokenService,
    private readonly eventEmitter: EventEmitter2,
    private readonly deliverablesService: DeliverablesService,
    private readonly taskUpdateService: TasksService,
  ) {}

  private readonly logger = new Logger(Agent2AgentController.name);
```

**Key Pattern:**
- Inject services via constructor
- Use `Logger` for logging
- Use decorators for routes (`@Get`, `@Post`, etc.)
- Use DTOs for request/response validation

## Service Pattern

Services contain business logic:

```typescript
// Example: apps/api/src/example/example.service.ts
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class ExampleService {
  private readonly logger = new Logger(ExampleService.name);

  async doSomething(data: string): Promise<string> {
    this.logger.log(`Doing something with: ${data}`);
    // Business logic here
    return `Processed: ${data}`;
  }
}
```

**Key Pattern:**
- `@Injectable()` decorator
- Logger for logging
- Async methods return Promises
- Business logic, not HTTP handling

## A2A Protocol Compliance

### Agent Card Endpoint

```typescript
@Get('agents/:orgSlug/:agentSlug/.well-known/agent.json')
async getAgentCard(
  @Param('orgSlug') orgSlug: string,
  @Param('agentSlug') agentSlug: string,
) {
  const agent = await this.agentRegistry.getAgent(orgSlug, agentSlug);
  return {
    name: agent.slug,
    displayName: agent.displayName,
    description: agent.description,
    type: agent.type,
    version: agent.version,
    capabilities: {
      modes: agent.modes,
      inputModes: agent.inputModes,
      outputModes: agent.outputModes,
    },
  };
}
```

### Task Execution Endpoint

```typescript
@Post('agents/:orgSlug/:agentSlug/tasks')
async executeTask(
  @Param('orgSlug') orgSlug: string,
  @Param('agentSlug') agentSlug: string,
  @Body() request: TaskRequestDto,
  @CurrentUser() user: SupabaseAuthUserDto,
) {
  // Validate request
  // Execute agent
  // Return TaskResponseDto
}
```

### Health Endpoint

```typescript
@Get('health')
health() {
  return { status: 'ok', timestamp: new Date().toISOString() };
}
```

## Transport Types Usage

Use `@orchestrator-ai/transport-types` for request/response:

```typescript
import {
  TaskRequestDto,
  TaskResponseDto,
  A2ATaskSuccessResponse,
  A2ATaskErrorResponse,
} from '@orchestrator-ai/transport-types';

@Post('tasks')
async executeTask(@Body() request: TaskRequestDto): Promise<TaskResponseDto> {
  try {
    const result = await this.service.execute(request);
    return {
      success: true,
      mode: request.mode,
      payload: {
        content: result.content,
        metadata: result.metadata,
      },
    } as A2ATaskSuccessResponse;
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'EXECUTION_ERROR',
        message: error.message,
      },
    } as A2ATaskErrorResponse;
  }
}
```

## Error Handling Pattern

```typescript
import {
  BadRequestException,
  NotFoundException,
  UnauthorizedException,
  HttpException,
  HttpStatus,
} from '@nestjs/common';

// Throw appropriate exceptions
if (!agent) {
  throw new NotFoundException(`Agent ${agentSlug} not found`);
}

if (!authorized) {
  throw new UnauthorizedException('Not authorized');
}

if (invalidInput) {
  throw new BadRequestException('Invalid input');
}

// Custom exceptions
throw new HttpException('Custom error', HttpStatus.INTERNAL_SERVER_ERROR);
```

## Module Organization Pattern

From `apps/api/src/llms/llm.module.ts`:

```34:96:apps/api/src/llms/llm.module.ts
@Module({
  imports: [
    SupabaseModule,
    HttpModule,
    SovereignPolicyModule,
    FeatureFlagModule,
    ModelConfigurationModule,
    // LLM Sub-modules
    CIDAFMModule,
    ProvidersModule,
    EvaluationModule,
    UsageModule,
    LangChainModule,
  ],
  controllers: [
    LLMController,
    LlmUsageController,
    ProductionOptimizationController,
    SanitizationController,
  ],
  providers: [
    LLMService,
    CentralizedRoutingService,
    RunMetadataService,
    ProviderConfigService,
    SecretRedactionService,
    PIIPatternService,
    PseudonymizationService,
    LocalModelStatusService,
    LocalLLMService,
    MemoryManagerService,
    ModelMonitorService,
    SourceBlindingService,
    BlindedLLMService,
    BlindedHttpService,
    PIIService,
    DictionaryPseudonymizerService,
    LLMServiceFactory,
    // Note: LLM Provider Services (OpenAI, Anthropic, etc.) are NOT registered as providers
    // They are manually instantiated by LLMServiceFactory with specific configurations
  ],
  exports: [
    LLMService,
    CentralizedRoutingService,
    RunMetadataService,
    ProviderConfigService,
    SecretRedactionService,
    PIIPatternService,
    PseudonymizationService,
    LocalModelStatusService,
    LocalLLMService,
    MemoryManagerService,
    ModelMonitorService,
    SourceBlindingService,
    BlindedLLMService,
    BlindedHttpService,
    PIIService,
    DictionaryPseudonymizerService,
    LLMServiceFactory,
    // Note: LLM Provider Services are not exported as they're factory-created
  ],
})
export class LLMModule {}
```

**Key Pattern:**
- Import sub-modules for organization
- Controllers handle HTTP
- Providers contain services/logic
- Export what other modules need

## Common Patterns

### Dependency Injection

```typescript
@Injectable()
export class MyService {
  constructor(
    private readonly dependency1: Dependency1Service,
    private readonly dependency2: Dependency2Service,
  ) {}
}
```

### Async/Await Pattern

```typescript
async execute(): Promise<Result> {
  const data = await this.repository.find();
  const processed = await this.processor.process(data);
  return processed;
}
```

### Logger Usage

```typescript
private readonly logger = new Logger(MyService.name);

this.logger.log('Info message');
this.logger.warn('Warning message');
this.logger.error('Error message', error);
this.logger.debug('Debug message');
```

## Checklist for Backend Development

When creating backend code:

- [ ] Files use kebab-case naming (`agent-runtime-dispatch.service.ts`)
- [ ] Module structure follows pattern (imports, controllers, providers, exports)
- [ ] Controllers handle HTTP only (no business logic)
- [ ] Services contain business logic (no HTTP handling)
- [ ] DTOs used for request/response validation
- [ ] Transport types used from `@orchestrator-ai/transport-types`
- [ ] A2A protocol endpoints implemented
- [ ] Error handling uses NestJS exceptions
- [ ] Logger used for logging
- [ ] Dependencies injected via constructor

## Related Documentation

- **A2A Protocol**: See orchestration system docs
- **Transport Types**: `apps/transport-types` package
- **Front-End Structure**: See Front-End Structure Skill for client patterns

