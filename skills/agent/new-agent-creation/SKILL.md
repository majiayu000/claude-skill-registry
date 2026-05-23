# New Agent Creation Skill
## Step-by-Step Agent Implementation

**When to Use**: Creating new AI agents for Unite-Hub

---

## Quick Start Template

### 1. Create Agent File

**Location**: `src/lib/agents/my-new-agent.ts`

```typescript
import { BaseAgent, AgentTask, AgentConfig } from './base-agent';
import { getAnthropicClient } from '@/lib/anthropic/lazy-client';

export class MyNewAgent extends BaseAgent {
  constructor() {
    super({
      name: 'MyNewAgent',
      queueName: 'my-new-agent-queue',
      concurrency: 1,
      retryDelay: 5000
    });
  }

  protected async processTask(task: AgentTask): Promise<any> {
    // Your agent logic here
    const client = getAnthropicClient();

    const response = await client.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      messages: [{
        role: 'user',
        content: `Task: ${task.task_type}\nPayload: ${JSON.stringify(task.payload)}`
      }]
    });

    return {
      result: response.content[0].text,
      workspace_id: task.workspace_id,
      model_used: 'claude-sonnet-4-5-20250929',
      input_tokens: response.usage.input_tokens,
      output_tokens: response.usage.output_tokens
    };
  }
}
```

### 2. Register in Orchestrator

**File**: `src/lib/agents/orchestrator-router.ts`

```typescript
// Add to AgentIntent enum
export type AgentIntent =
  | 'my_new_agent'  // ← Add this
  | 'email' | 'content' | ...;

// Add to classifyIntent function
if (objective.includes('my task keyword')) {
  return 'my_new_agent';
}
```

### 3. Add to Registry

**File**: `.claude/agents/registry.json`

```json
{
  "id": "my-new-agent",
  "name": "My New Agent",
  "version": "1.0.0",
  "file": "src/lib/agents/my-new-agent.ts",
  "capabilities": ["capability_1", "capability_2"],
  "queueName": "my-new-agent-queue",
  "models": ["claude-sonnet-4-5-20250929"],
  "governance": "HUMAN_GOVERNED",
  "verification_required": true,
  "budget_daily_usd": 10.00,
  "category": "marketing"
}
```

### 4. Create Tests

**File**: `tests/agents/my-new-agent.test.ts`

```typescript
import { describe, it, expect, vi } from 'vitest';
import { MyNewAgent } from '@/lib/agents/my-new-agent';

describe('MyNewAgent', () => {
  it('processes task successfully', async () => {
    const agent = new MyNewAgent();
    const task = {
      id: 'test-1',
      workspace_id: 'ws-123',
      task_type: 'my_task',
      payload: { data: 'test' },
      priority: 5,
      retry_count: 0,
      max_retries: 3
    };

    const result = await agent.processTask(task);

    expect(result).toBeDefined();
    expect(result.workspace_id).toBe('ws-123');
  });
});
```

### 5. Create CLI Runner (Optional)

**File**: `scripts/run-my-agent.mjs`

```javascript
import { MyNewAgent } from '../src/lib/agents/my-new-agent.js';

const agent = new MyNewAgent();
await agent.start();
console.log('MyNewAgent running...');
```

---

## Checklist

- [ ] Create agent file extending BaseAgent
- [ ] Implement processTask() method
- [ ] Add to orchestrator-router.ts intent enum
- [ ] Add to orchestrator routing logic
- [ ] Register in .claude/agents/registry.json
- [ ] Create tests (100% pass required)
- [ ] Add CLI runner script (optional)
- [ ] Document in .claude/agent.md
- [ ] Set appropriate budget limits
- [ ] Choose governance mode (HUMAN_GOVERNED vs AUTONOMOUS)

---

**Standard**: All agents must filter by workspace_id, respect budgets, pass verification
