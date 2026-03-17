---
name: contracts
description: Contract lifecycle management - creation, consumption, modification, and resolution.
allowed-tools: Read, Write, Glob
---

# Contracts Skill

Contracts define interfaces between parallel tasks. They enable safe concurrent implementation by making dependencies explicit.

## When to Load This Skill

- Architect: When defining contracts in design
- Executor: When materializing contracts before implementation
- Implementer: When implementing or consuming contracts
- Contract-Resolver: When modifying contracts

## Contract Lifecycle

```
DESIGN → MATERIALIZE → IMPLEMENT → VERIFY → (RESOLVE if blocked)
   ↓          ↓            ↓          ↓            ↓
Architect  Executor   Implementer  Verifier  Contract-Resolver
```

## Phase 1: Design (Architect)

Architect defines contracts in design output (compact JSON):

```json
{"contracts":[{"name":"user-repository","description":"Interface for user data access","definition":"interface UserRepository { getById(id: string): Promise<User | null>; save(user: User): Promise<void>; }","used_by":["task-001","task-002","task-003"]}]}
```

**Rules for Architects:**
- Define contracts for ANY cross-task dependency
- Make contracts minimal but complete
- Specify who provides vs consumes
- Include in `execution_plan.contracts_first`

## Phase 2: Materialize (Executor)

Before spawning implementers, executor writes contracts to files:

```
FOR each contract in final_design.contracts:
  Write to memory/contracts/{name}.json (compact JSON)
```

**Location:** `memory/contracts/{contract-name}.json`

Contract file structure:
```json
{"name":"user-repository","version":1,"status":"active","created_at":"ISO-8601","source_design":"memory/reports/final_design.json","definition":{"type":"interface","language":"typescript","spec":"interface UserRepository { ... }"},"description":"Interface for user data access","consumers":[{"task_id":"task-001","role":"provider"},{"task_id":"task-002","role":"consumer"}],"history":[{"version":1,"date":"ISO-8601","change":"Initial contract from design"}]}
```

## Phase 3: Implement (Implementer)

Implementer receives contract paths and must:

1. **Read contracts** before coding
2. **Implement exactly** what contract specifies
3. **Report implementation** in output:

```json
{"contracts_implemented":[{"name":"user-repository","location":"src/repositories/user.ts","role":"provider"}]}
```

**If contract is insufficient:**
- Status: `blocked`
- Reason: `contract_change`
- Include suggested contract modification

## Phase 4: Verify (Verifier)

Verifier checks:
- Provider implements all contract methods
- Consumer only uses contract-defined interfaces
- Types match contract specification

## Phase 5: Resolve (Contract-Resolver)

When implementer is blocked on contract:

1. **Read the block** - What change is needed?
2. **Assess impact** - Who else uses this contract?
3. **Decide action:**
   - `modify`: Update contract, mark breaking if needed
   - `extend`: Add to contract without breaking
   - `reject`: Suggest alternative approach

4. **Update contract file** - Increment version, add to history

5. **Instruct executor** on affected tasks

## Contract Types

### Interface Contract
```json
{"definition":{"type":"interface","language":"typescript","spec":"interface PaymentGateway { charge(amount: number, token: string): Promise<ChargeResult>; refund(chargeId: string): Promise<RefundResult>; }"}}
```

### Data Structure Contract
```json
{"definition":{"type":"data_structure","language":"typescript","spec":"type User = { id: string; email: string; createdAt: Date; }"}}
```

### API Contract
```json
{"definition":{"type":"api","spec":"POST /api/users | Request: { email: string, password: string } | Response: { id: string, token: string } | Errors: 400 (validation), 409 (exists)"}}
```

### Event Contract
```json
{"definition":{"type":"event","spec":"Event: user.created | Payload: { userId: string, email: string, timestamp: ISO8601 } | Emitted by: UserService | Consumed by: EmailService, AnalyticsService"}}
```

## Contract Discovery

To find contracts for a task:

```
1. Read task description
2. Glob("memory/contracts/*.json")
3. Filter where task_id in consumers
4. Separate by role (provider vs consumer)
```

## Breaking Changes

A change is **breaking** if:
- Method signature changed
- Required field added to input
- Field removed from output
- Type changed incompatibly

Breaking changes require:
- Re-verification of all consumers
- Potentially re-implementation

## Principles

1. **Contracts before code** - Materialize all contracts before spawning implementers
2. **Single provider** - Each contract has exactly one provider task
3. **Explicit consumers** - All consumers must be listed
4. **Version everything** - Never modify without incrementing version
5. **History is immutable** - Never edit past history entries
