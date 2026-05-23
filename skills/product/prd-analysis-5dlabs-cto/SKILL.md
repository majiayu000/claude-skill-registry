---
name: prd-analysis
description: PRD parsing and task decomposition patterns for intake workflows.
agents: [morgan]
triggers: [prd, intake, task decomposition, planning, project management]
---

# PRD Analysis and Task Decomposition

Patterns for parsing PRDs and generating comprehensive task documentation.

## Critical Success Criteria

Output quality is measured by how well agents can implement tasks WITHOUT needing to re-read the PRD. Each task must be **self-contained** with all necessary context embedded.

## Structured Analysis (Chain of Thought)

Before generating tasks, think step-by-step:

1. **Analyze PRD Structure** - Identify features, tech requirements, implicit dependencies
2. **Map Dependencies** - What depends on what? Shared infrastructure needs?
3. **Define Task Boundaries** - Atomic, single responsibility, independently testable
4. **Generate Implementation Details** - Pseudo-code, file structures, library versions
5. **Define Test Strategies** - Acceptance criteria, unit/integration/E2E guidance
6. **Self-Verify** - All requirements covered? No circular deps? Valid ordering?

## Service Discovery

Before generating any tasks, analyze the PRD to identify all services and their tech stacks.

Create a **Service-to-Agent Mapping Table**:

| Service Name | Agent | Tech Stack | Description |
|--------------|-------|------------|-------------|
| Notification Router | rex | Rust/Axum | High-performance API |
| Integration Service | nova | Bun/Elysia/Effect | Channel delivery |
| Admin API | grizz | Go/gRPC | Tenant management |
| Web Console | blaze | Next.js/React/shadcn | Admin dashboard |
| Mobile App | tap | Expo/React Native | Mobile client |
| Desktop Client | spark | Electron | Desktop notifications |

## Agent Assignment Rules

### Implementation Agents (Write Code)

| Agent | Language/Stack | Use For |
|-------|---------------|---------|
| **bolt** | Kubernetes/Helm | Infrastructure (Task 1 ONLY) |
| **rex** | Rust/Axum/Tokio | Rust backend services |
| **grizz** | Go/gRPC/Chi | Go backend services |
| **nova** | Bun/Elysia/Effect | TypeScript backend |
| **blaze** | Next.js/React/shadcn | Web frontends |
| **tap** | Expo/React Native | Mobile apps |
| **spark** | Electron | Desktop apps |

### Support Agents (Review Only - AFTER Implementation)

| Agent | Role | Use ONLY For |
|-------|------|--------------|
| **cleo** | Quality Review | Code review AFTER PR |
| **cipher** | Security Audit | Security audit AFTER PR |
| **tess** | Testing | Writing tests AFTER PR |
| **atlas** | Integration | Merging PRs AFTER reviews |

**CRITICAL**: Support agents are NEVER assigned to implementation tasks.

## Task 1: Always Infrastructure

Task 1 must ALWAYS be assigned to Bolt to provision:
- Databases (PostgreSQL, MongoDB)
- Caches (Redis/Valkey)
- Message queues (Kafka, NATS)
- Object storage (SeaweedFS S3)

## Code Signatures in Details

Include language-specific function/struct signatures in task details:

### Rust Example
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Notification {
    pub id: Uuid,
    pub tenant_id: Uuid,
    pub channel: Channel,
}

pub async fn create_notification(
    State(state): State<AppState>,
    Json(req): Json<CreateNotificationRequest>,
) -> Result<Json<NotificationResponse>, ApiError>
```

### TypeScript/Effect Example
```typescript
import { Schema } from "@effect/schema"
import { Effect } from "effect"

export const Integration = Schema.Struct({
  id: Schema.UUID,
  name: Schema.String,
  channel: Schema.Literal("slack", "discord", "email"),
})
```

### Go Example
```go
type TenantServiceServer struct {
    pb.UnimplementedTenantServiceServer
    db *pgxpool.Pool
}

func (s *TenantServiceServer) CreateTenant(
    ctx context.Context,
    req *pb.CreateTenantRequest,
) (*pb.Tenant, error)
```

## Task JSON Format

```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Provision Infrastructure",
      "description": "Deploy PostgreSQL, Redis, Kafka clusters",
      "priority": "critical",
      "status": "pending",
      "dependencies": [],
      "agentHint": "bolt",
      "details": "Full implementation details with code signatures",
      "testStrategy": "Verification commands and expected outputs"
    }
  ]
}
```

## Quality Checklist

Before finalizing:

- [ ] Service table created with all services from PRD
- [ ] Task 1 is `agentHint: "bolt"` for infrastructure
- [ ] Every task has `agentHint` set
- [ ] Implementation agents only for code tasks
- [ ] Support agents ONLY for review/audit tasks
- [ ] Code signatures in details for all implementation tasks
- [ ] No auth/jwt/oauth tasks assigned to cipher
- [ ] Dependencies form valid DAG (no cycles)
- [ ] Implementation tasks depend on task-1
- [ ] Each task is atomic (completable in one PR)
