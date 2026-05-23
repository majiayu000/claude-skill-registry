---
name: mcp-coordination
description: Model Context Protocol (MCP) memory patterns for agent coordination using Serena memories. Provides file-based memory storage for status sharing, decisions, and distributed decision-making across agent swarms. Use when implementing multi-agent coordination, task handoffs, or swarm communication.
---

# MCP Coordination Skill

## Purpose

Provides standard patterns for agent coordination using **Serena memories** (file-based, git-tracked, per-project memory system). ~23k token savings compared to external memory MCP.

## Memory Tool Reference

Serena provides 5 memory tools:

```typescript
// Write a memory file
write_memory({
  memory_file_name: "decisions.md",  // File name in .serena/memories/
  content: "# Architecture Decisions\n..."
});

// Read a memory file
read_memory({
  memory_file_name: "decisions.md"
});

// List all memory files
list_memories();

// Edit existing memory (regex replacement)
edit_memory({
  memory_file_name: "status.md",
  needle: "status: working",
  repl: "status: completed",
  mode: "literal"  // or "regex"
});

// Delete a memory file
delete_memory({
  memory_file_name: "temp-notes.md"
});
```

## Memory File Naming Conventions

Use consistent naming for searchability:

```
.serena/memories/
├── agent-status-{agentId}.md    # Per-agent status
├── decision-{topic}.md          # Architecture decisions
├── pattern-{name}.md            # Reusable patterns
├── finding-{topic}.md           # Research findings
├── handoff-{from}-to-{to}.md    # Task handoffs
└── broadcast-{timestamp}.md     # Team announcements
```

## Core Coordination Patterns

### 1. Store Agent Status

```javascript
// Store status
write_memory({
  memory_file_name: "agent-status-coder-001.md",
  content: `# Agent Status: coder-001

Status: working
Task: Implementing authentication API
Progress: 45%
Outputs:
- src/auth/auth.service.ts
- src/auth/auth.controller.ts

Updated: ${new Date().toISOString()}`
});

// Update status (efficient edit)
edit_memory({
  memory_file_name: "agent-status-coder-001.md",
  needle: "Progress: 45%",
  repl: "Progress: 75%",
  mode: "literal"
});
```

### 2. Retrieve Agent Status

```javascript
// Get status
const status = await read_memory({
  memory_file_name: "agent-status-coder-001.md"
});

// List all agent statuses
const memories = await list_memories();
const statusFiles = memories.filter(m => m.startsWith("agent-status-"));
```

### 3. Share Findings Between Agents

```javascript
// Researcher shares findings
write_memory({
  memory_file_name: "finding-backend-framework.md",
  content: `# Research: Backend Framework Selection

Source: researcher-001
Date: ${new Date().toISOString()}

## Frameworks Evaluated
- Express - widely adopted, extensive middleware
- Fastify - high performance, schema validation
- Koa - minimal, modern async

## Recommendation
**Express** for this project due to team familiarity and ecosystem.

## Considerations
- Use Fastify if performance becomes critical
- Consider Koa for new microservices`
});

// Another agent reads findings
const research = await read_memory({
  memory_file_name: "finding-backend-framework.md"
});
```

### 4. Store Architecture Decisions

```javascript
write_memory({
  memory_file_name: "decision-auth-implementation.md",
  content: `# Decision: Authentication Implementation

Date: ${new Date().toISOString()}
Author: architect-001
Status: Approved

## Context
Need stateless auth for microservices architecture.

## Decision
JWT with refresh tokens stored in httpOnly cookies.

## Rationale
- Stateless: no session storage needed
- Scalable: any service can verify tokens
- Secure: httpOnly prevents XSS

## Implementation
- Access token TTL: 15 minutes
- Refresh token TTL: 7 days
- Redis for refresh token blacklist

## Consequences
- Need Redis infrastructure
- Token size adds to request payload`
});
```

### 5. Coordinate Task Handoff

```javascript
// Coder completes and hands off to tester
write_memory({
  memory_file_name: "handoff-coder001-to-tester001.md",
  content: `# Task Handoff

From: coder-001
To: tester-001
Date: ${new Date().toISOString()}

## Completed Work
- Auth service: src/auth/auth.service.ts
- Auth controller: src/auth/auth.controller.ts
- JWT middleware: src/middleware/jwt.ts

## Endpoints to Test
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh

## Testing Notes
- Focus on JWT validation edge cases
- Test refresh token rotation
- Verify httpOnly cookie behavior

## Dependencies
- Redis must be running
- .env configured with JWT_SECRET`
});

// Update own status to completed
edit_memory({
  memory_file_name: "agent-status-coder-001.md",
  needle: "Status: working",
  repl: "Status: completed",
  mode: "literal"
});
```

### 6. Broadcast Announcements

```javascript
// Critical announcement
write_memory({
  memory_file_name: `broadcast-${Date.now()}.md`,
  content: `# Team Broadcast

Type: decision
From: architect-001
Date: ${new Date().toISOString()}

## Message
Using layered architecture: Controller -> Service -> Repository

All services must follow this pattern. See decision-architecture.md for details.`
});
```

## Multi-MCP Coordination Workflows

### Workflow 1: Feature Implementation

```javascript
// 1. Context7: Research library
const jwtDocs = await mcp__Context7__get_library_docs({
  context7CompatibleLibraryID: "/vercel/jsonwebtoken"
});

// 2. Serena: Check existing patterns in memories
const memories = await list_memories();
const authPatterns = memories.filter(m => m.includes("auth") || m.includes("jwt"));
for (const pattern of authPatterns) {
  const content = await read_memory({ memory_file_name: pattern });
  // Use existing patterns
}

// 3. Serena: Find existing auth code
const existingAuth = await mcp__serena__find_symbol({
  name_path_pattern: "auth",
  include_body: false,
  relative_path: "src"
});

// 4. Sequential Thinking: Plan implementation (if complex)
if (complexityScore >= 20) {
  await mcp__sequential_thinking__sequentialthinking({
    thought: "Step 1: Analyzing existing auth vs new JWT approach...",
    thoughtNumber: 1,
    totalThoughts: 8,
    nextThoughtNeeded: true
  });
}

// 5. Vibe Check: Validate approach
const vibeCheck = await mcp__vibe_check__vibe_check({
  goal: "Implement JWT auth with refresh tokens",
  plan: "Add JWT middleware + refresh token endpoint",
  progress: "Researched libraries, found existing patterns"
});

// 6. Store decision in memory
write_memory({
  memory_file_name: "decision-jwt-auth.md",
  content: `# Decision: JWT Authentication

Date: ${new Date().toISOString()}
Complexity Score: ${complexityScore}

## Approach
${vibeCheck.feedback}

## Libraries
- jsonwebtoken
- bcrypt

## Architecture
- Stateless auth with Redis for refresh tokens
- Access token: 15min TTL
- Refresh token: 7 days TTL`
});
```

### Workflow 2: Debugging Complex Issue

```javascript
// 1. Serena: Find bug location
const symbols = await mcp__serena__find_symbol({
  name_path_pattern: "PaymentProcessor",
  include_body: true,
  relative_path: "src/services"
});

// 2. Sequential Thinking: Analyze step-by-step
await mcp__sequential_thinking__sequentialthinking({
  thought: "Hypothesis 1: Race condition due to missing async...",
  thoughtNumber: 1,
  totalThoughts: 12,
  nextThoughtNeeded: true
});

// 3. Check prior solutions in memories
const memories = await list_memories();
const bugPatterns = memories.filter(m =>
  m.includes("bug") || m.includes("race") || m.includes("payment")
);

// 4. Store root cause analysis
write_memory({
  memory_file_name: "finding-payment-race-condition.md",
  content: `# Root Cause Analysis: Payment Race Condition

Analyst: root-cause-analyst-001
Date: ${new Date().toISOString()}

## Root Cause
Missing transaction lock in payment flow.

## Evidence
- Two concurrent payment requests created duplicate charges
- No Redis lock on payment processing
- Race condition in database write

## Fix
Add distributed lock using Redis SETNX.

## Code
\`\`\`typescript
await redisClient.set(lockKey, 'locked', 'NX', 'EX', 10);
\`\`\``
});

// 5. Vibe Learn: Document for future
await mcp__vibe_check__vibe_learn({
  mistake: "Payment race condition due to missing distributed lock",
  category: "Complex Solution Bias",
  solution: "Added Redis distributed lock with TTL"
});
```

### Workflow 3: E2E Test Creation

```javascript
// 1. Check for existing test patterns
const memories = await list_memories();
const testPatterns = memories.filter(m => m.includes("test") || m.includes("e2e"));

// 2. Chrome DevTools: Test the flow
await mcp__chrome_devtools__navigate_page({
  url: "http://localhost:5173/register"
});

await mcp__chrome_devtools__fill_form({
  elements: [
    { uid: "email-input", value: "test@example.com" },
    { uid: "password-input", value: "SecurePass123!" }
  ]
});

await mcp__chrome_devtools__click({ uid: "register-button" });
await mcp__chrome_devtools__wait_for({ text: "Registration successful" });

const screenshot = await mcp__chrome_devtools__take_screenshot({
  filePath: "./e2e-results/registration-success.png"
});

// 3. Store test pattern for reuse
write_memory({
  memory_file_name: "pattern-e2e-registration.md",
  content: `# E2E Test Pattern: User Registration

Created: ${new Date().toISOString()}
Author: e2e-test-agent-001

## Test Steps
1. Navigate to /register
2. Fill email and password fields
3. Click register button
4. Verify success message

## Assertions
- Form validation works
- API call succeeds
- Success message appears
- Redirect to dashboard

## Screenshot
${screenshot.filePath}

## Duration
~2.1s`
});
```

## Key Coordination Principles

1. **Use Named Files**: Consistent naming enables "search" via list + filter
2. **Git-Tracked**: Memories persist across sessions and are version controlled
3. **Per-Project Scope**: Each repo has its own `.serena/memories/`
4. **Efficient Updates**: Use `edit_memory` for status changes instead of full rewrites
5. **Layer Tools**: Context7 for docs, Serena for code, memories for coordination
6. **Validate Plans**: Use vibe_check before complex implementations
7. **Learn from Errors**: Use vibe_learn to capture mistakes

## Token Savings

| Solution | Token Cost |
|----------|-----------|
| External Memory MCP (Recall) | ~27k tokens |
| Serena Memories | ~3.5k tokens |
| **Savings** | **~23.5k tokens (87%)** |

## Used By

- ALL agents in the swarm
- Swarm coordinator/orchestrator
- Task scheduler
- Dependency manager
- Progress monitoring
