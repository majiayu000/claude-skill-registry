---
name: agent-permissions
description: Comprehensive guide for the agent permissions and approval system. Use when an agent needs to request user approval for sensitive operations, when implementing new approval policies, when integrating platform-specific approval UIs (Slack buttons, WhatsApp replies, Dashboard modals), or when troubleshooting approval flows. Covers policy definition, platform adapters, and the complete approval lifecycle.
metadata:
  author: orient
  version: '2.0.0'
---

# Agent Permissions System

This skill covers the approval/permissions framework that enables agents to request user consent for sensitive operations across all platforms.

## Quick Start: Requesting User Approval

When an agent needs approval for a sensitive action, the system automatically:

1. Evaluates the tool call against defined policies
2. If policy requires approval (`action: 'ask'`), sends a prompt via the appropriate platform adapter
3. Waits for user response (button click, reply, reaction, or dashboard action)
4. Returns approval decision to continue or deny execution

### Platform-Specific Approval UX

| Platform      | Approval Method                    | Response Format                    |
| ------------- | ---------------------------------- | ---------------------------------- |
| **Slack**     | Interactive buttons in message     | "Approve" / "Deny" button clicks   |
| **WhatsApp**  | Reply to message or emoji reaction | Reply "YES"/"NO" or 👍/👎 reaction |
| **Dashboard** | Modal with approve/deny buttons    | Button click in UI                 |

## Core Architecture

```
packages/agents/src/permissions/
├── types.ts              # Core interfaces (PermissionPolicy, ApprovalRequest, etc.)
├── policyEngine.ts       # Policy evaluation and approval coordination
├── approvalStore.ts      # In-memory approval store interface
├── drizzlePermissionStore.ts  # Database-backed store (persistent)
├── defaultPolicies.ts    # Built-in policy definitions
└── adapters/
    ├── base.ts           # PlatformApprovalAdapter interface
    ├── registry.ts       # Adapter registration
    ├── dashboard.ts      # Dashboard approval adapter
    ├── slack.ts          # Slack Block Kit buttons
    └── whatsapp.ts       # WhatsApp reply/reaction handling
```

## Policy Definition

Policies control which tools require approval:

```typescript
interface PermissionPolicy {
  id: string; // Unique identifier
  name: string; // Human-readable name
  toolPatterns: string[]; // Glob patterns: 'file_write', 'bash_*', etc.
  action: 'allow' | 'deny' | 'ask'; // What to do when matched
  granularity: 'per_call' | 'per_session' | 'per_category';
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  promptTemplate?: string; // Custom approval message
  agentIds?: string[]; // Limit to specific agents
  platforms?: Platform[]; // Limit to platforms
  priority?: number; // Higher = evaluated first
  timeout?: number; // Auto-expire after ms
}
```

### Default Policies

Located in `packages/agents/src/permissions/defaultPolicies.ts`:

```typescript
export const DEFAULT_POLICIES: PermissionPolicy[] = [
  {
    id: 'file-write',
    toolPatterns: ['file_write', 'file_delete', 'file_move', 'file_edit'],
    action: 'ask',
    granularity: 'per_call',
    riskLevel: 'medium',
  },
  {
    id: 'shell-execution',
    toolPatterns: ['bash', 'shell', 'exec', 'run_command'],
    action: 'ask',
    granularity: 'per_call',
    riskLevel: 'high',
  },
  {
    id: 'external-api',
    toolPatterns: ['http_*', 'api_*', 'webhook_*'],
    action: 'ask',
    granularity: 'per_session', // Once per session
    riskLevel: 'medium',
  },
  {
    id: 'sensitive-data',
    toolPatterns: ['secret_*', 'credential_*', 'token_*'],
    action: 'ask',
    granularity: 'per_call',
    riskLevel: 'critical',
  },
];
```

## Integration with Tool Execution

The `toolCallingService.ts` integrates with the PolicyEngine:

```typescript
// Simplified flow in executeToolLoop:
for (const toolUse of toolUseBlocks) {
  const decision = await policyEngine.evaluateToolCall(toolUse, context, agentId);

  if (decision.action === 'deny') {
    return toolDeniedResult(toolUse, decision.reason);
  }

  if (decision.action === 'ask') {
    // This triggers the platform-specific approval UI
    const approval = await policyEngine.requestApproval({
      tool: toolUse,
      policy: decision.policy,
      context,
      agentId,
    });

    if (approval.status !== 'approved') {
      return toolDeniedResult(toolUse, 'User denied approval');
    }
  }

  // Execute the tool
  const result = await executor(toolUse.name, toolUse.input, context);
}
```

## Platform Adapters

### Implementing a New Adapter

Each adapter implements `PlatformApprovalAdapter`:

```typescript
interface PlatformApprovalAdapter {
  platform: Platform;
  supportsNativeApproval: boolean;
  supportedInteractionTypes: readonly InteractionType[];

  // Send approval prompt to user
  requestApproval(
    request: ApprovalRequest,
    context: PlatformContext
  ): Promise<ApprovalPromptResult>;

  // Parse user's response (button click, reply, etc.)
  handleApprovalResponse(response: unknown): Promise<ApprovalResult | null>;

  // Cancel pending request
  cancelRequest(requestId: string): Promise<void>;

  // Format messages for display
  formatApprovalPrompt(request: ApprovalRequest): unknown;
  formatApprovalResult(result: ApprovalResult): unknown;
}
```

### WhatsApp Adapter Example

The WhatsApp adapter sends a message and listens for replies:

```typescript
formatApprovalPrompt(request: ApprovalRequest): string {
  return [
    `Approval required`,
    `Agent "${request.agentId}" wants to run "${request.tool.name}".`,
    `Reply with YES/NO or APPROVE/DENY.`,
    `Request ID: ${request.id}`,
    `You can also approve in the dashboard: ${dashboardUrl}/approvals/${request.id}`,
  ].join('\n');
}

handleApprovalResponse(response: WhatsAppMessage): ApprovalResult | null {
  const text = response.body?.trim().toLowerCase();
  if (text === 'approve' || text === 'yes') {
    return { requestId: extractRequestId(text), status: 'approved' };
  }
  if (text === 'deny' || text === 'no') {
    return { requestId: extractRequestId(text), status: 'denied' };
  }
  // Also handle emoji reactions 👍 👎
  return null;
}
```

### Slack Adapter

Uses Block Kit interactive buttons:

```typescript
formatApprovalPrompt(request: ApprovalRequest) {
  return {
    blocks: [
      { type: 'section', text: { type: 'mrkdwn', text: `*Approval Required*` } },
      { type: 'section', text: { type: 'mrkdwn', text: `Tool: \`${request.tool.name}\`` } },
      {
        type: 'actions',
        elements: [
          { type: 'button', text: { type: 'plain_text', text: 'Approve' }, action_id: 'approve', value: request.id },
          { type: 'button', text: { type: 'plain_text', text: 'Deny' }, action_id: 'deny', value: request.id },
        ],
      },
    ],
  };
}
```

## Database Schema

Tables in `packages/database/src/schema/index.ts`:

```typescript
// Custom policies (override code defaults)
export const permissionPolicies = pgTable('permission_policies', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  toolPatterns: text('tool_patterns').notNull(),  // JSON array
  action: text('action').notNull(),
  granularity: text('granularity').notNull(),
  riskLevel: text('risk_level').notNull(),
  priority: integer('priority').default(0),
  enabled: boolean('enabled').default(true),
  ...
});

// Pending/resolved approval queue
export const approvalRequests = pgTable('approval_requests', {
  id: text('id').primaryKey(),
  sessionId: text('session_id').notNull(),
  platform: text('platform').notNull(),
  userId: text('user_id').notNull(),
  agentId: text('agent_id').notNull(),
  toolName: text('tool_name').notNull(),
  toolInput: text('tool_input').notNull(),  // JSON
  status: text('status').notNull(),  // pending, approved, denied, expired
  ...
});

// Session-level approval grants (avoid repeated prompts)
export const approvalGrants = pgTable('approval_grants', {
  id: serial('id').primaryKey(),
  sessionId: text('session_id').notNull(),
  userId: text('user_id').notNull(),
  grantType: text('grant_type').notNull(),  // 'tool' | 'category' | 'policy'
  grantValue: text('grant_value').notNull(),
  expiresAt: timestamp('expires_at'),
  ...
});
```

## Adding a New Platform

To add a new platform (e.g., Telegram):

1. **Create adapter:** `packages/agents/src/permissions/adapters/telegram.ts`
2. **Implement `PlatformApprovalAdapter`** with platform-specific UX
3. **Register in startup:**

```typescript
import { TelegramApprovalAdapter } from './adapters/telegram.js';

// In your platform initialization:
adapterRegistry.register(new TelegramApprovalAdapter(telegramClient));
```

4. **Handle responses** - Wire up message/callback handlers to call:

```typescript
policyEngine.handlePlatformResponse('telegram', telegramResponse);
```

## Approval Granularity

- **`per_call`:** Prompt every time the tool is invoked
- **`per_session`:** Prompt once per session, then remember grant
- **`per_category`:** Prompt once per tool category, remember for session

When `per_session` or `per_category` is used, grants are stored in `approval_grants` table.

## Testing

```bash
# Run permissions tests
pnpm --filter @orientbot/agents test permissions

# Test specific adapter
pnpm --filter @orientbot/agents test adapters
```

## Troubleshooting

### Approvals not working

1. Check if policy matches tool pattern (glob patterns)
2. Verify adapter is registered for the platform
3. Check approval request is created in DB
4. Verify platform message/button handler is wired up

### Policy not applying

1. Higher priority policies take precedence
2. `enabled: false` policies are skipped
3. Check `platforms` and `agentIds` filters

### Approval expires immediately

1. Check `timeout` setting on policy
2. Verify `defaultTimeoutMs` in PolicyEngine config
