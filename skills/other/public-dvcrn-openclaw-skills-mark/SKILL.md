# OpenClawdy

**Memory Infrastructure for Autonomous Agents**

Give your agent persistent memory that survives sessions. Store facts, preferences, decisions, and learnings - recall them semantically whenever needed. Advanced features include reputation tracking, cross-agent memory pools, and time-travel snapshots.

## Installation

```bash
openclaw skill install openclawdy
```

Or add to your agent config:
```yaml
skills:
  - url: https://openclawdy.xyz/SKILL.md
    name: openclawdy
```

## Authentication

OpenClawdy uses wallet-based authentication. Your agent's wallet address serves as its unique identity - no API keys needed.

Before using memory tools, ensure your agent has a wallet configured. Each wallet gets an isolated memory vault.

---

## Core Tools

### memory_store

Store information for later retrieval.

**Parameters:**
- `content` (required): The information to remember
- `type` (optional): Category of memory - one of: `fact`, `preference`, `decision`, `learning`, `history`, `context`. Default: `fact`
- `tags` (optional): Array of tags for organization

**Example:**
```
Store this as a preference: User prefers TypeScript over JavaScript for all new projects
```

```
Remember this fact with tags ["project", "tech-stack"]: The current project uses Next.js 14 with PostgreSQL
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "mem_abc123",
    "content": "User prefers TypeScript over JavaScript",
    "type": "preference",
    "tags": [],
    "createdAt": "2025-02-10T12:00:00Z"
  }
}
```

---

### memory_recall

Retrieve relevant memories using semantic search. Finds memories by meaning, not just keywords.

**Parameters:**
- `query` (required): What to search for
- `limit` (optional): Maximum results to return (1-20). Default: 5
- `type` (optional): Filter by memory type

**Example:**
```
Recall memories about programming language preferences
```

```
What do I know about the user's coding style? Limit to 3 results.
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "mem_abc123",
      "content": "User prefers TypeScript over JavaScript",
      "type": "preference",
      "relevance": 0.95,
      "createdAt": "2025-02-10T12:00:00Z"
    }
  ]
}
```

---

### memory_list

List recent memories without semantic search.

**Parameters:**
- `type` (optional): Filter by memory type
- `limit` (optional): Maximum results (1-100). Default: 20
- `offset` (optional): Pagination offset. Default: 0

**Example:**
```
List my recent memories
```

```
Show all preference memories, limit 10
```

---

### memory_delete

Delete a specific memory by ID.

**Parameters:**
- `id` (required): The memory ID to delete

**Example:**
```
Delete memory mem_abc123
```

---

### memory_clear

Clear all memories in the vault. **Use with caution - this is irreversible.**

**Example:**
```
Clear all my memories (I confirm this action)
```

---

### memory_export

Export all memories as JSON for backup.

**Example:**
```
Export all my memories
```

---

### memory_stats

Get usage statistics for your agent.

**Example:**
```
Show my memory usage stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "address": "0x1234...",
    "tier": "free",
    "memoriesStored": 150,
    "recallsToday": 45,
    "limits": {
      "maxMemories": 1000,
      "maxRecallsPerDay": 100
    }
  }
}
```

---

## Advanced Tools

### memory_reputation

**Track which memories lead to good outcomes.** Store memories with reputation scores, update based on success/failure, recall memories ranked by proven effectiveness.

**Actions:**

#### store_ranked
Store a memory with an initial reputation score.

**Parameters:**
- `action`: `store_ranked`
- `content` (required): The information to store
- `type` (optional): Memory type. Default: `fact`
- `reputation` (optional): Initial score 0.0-1.0. Default: 0.5

**Example:**
```
Store ranked memory: "Use retry logic for API calls" with reputation 0.8
```

#### recall_ranked
Retrieve memories sorted by reputation (most effective first).

**Parameters:**
- `action`: `recall_ranked`
- `query` (required): What to search for

**Example:**
```
Recall ranked memories about error handling strategies
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "mem_xyz",
      "content": "Use exponential backoff for retries",
      "reputation": 0.92,
      "usage_count": 15,
      "success_rate": 0.93
    }
  ]
}
```

#### update_reputation
Update a memory's reputation based on outcome.

**Parameters:**
- `action`: `update_reputation`
- `memory_id` (required): The memory to update
- `outcome` (required): `success`, `failure`, or `neutral`
- `impact` (optional): Weight of this outcome (0.0-1.0)

**Example:**
```
Update reputation for mem_xyz: outcome was success
```

---

### memory_pool

**Cross-Agent Memory Pools** - Share knowledge between multiple agents. Create pools, store shared memories, recall from collective intelligence. Perfect for agent teams and swarms.

**Actions:**

#### create
Create a new shared memory pool.

**Parameters:**
- `action`: `create`
- `pool_name` (required): Name for the pool

**Example:**
```
Create memory pool: "research-team"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pool_id": "pool_abc123",
    "name": "research-team",
    "created_at": "2025-02-10T12:00:00Z"
  }
}
```

#### store
Store a memory in a shared pool.

**Parameters:**
- `action`: `store`
- `pool_id` (required): The pool ID
- `content` (required): Information to share
- `type` (optional): Memory type

**Example:**
```
Store in pool pool_abc123: "Found bug in authentication module - fix applied"
```

#### recall
Search memories in a shared pool.

**Parameters:**
- `action`: `recall`
- `pool_id` (required): The pool ID
- `query` (required): What to search for

**Example:**
```
Recall from pool pool_abc123: authentication issues
```

#### list
List all accessible pools.

**Parameters:**
- `action`: `list`

**Example:**
```
List my memory pools
```

---

### memory_snapshot

**Memory Time Travel** - Snapshot and restore agent memory states. Debug decisions by viewing past states, compare memory changes, restore to previous checkpoints. Essential for high-stakes agents.

**Actions:**

#### create
Create a snapshot of current memory state.

**Parameters:**
- `action`: `create`
- `name` (required): Descriptive name for the snapshot

**Example:**
```
Create memory snapshot: "before-major-update"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "snapshot_id": "snap_abc123",
    "name": "before-major-update",
    "memory_count": 150,
    "created_at": "2025-02-10T12:00:00Z"
  }
}
```

#### restore
Restore memory state from a snapshot.

**Parameters:**
- `action`: `restore`
- `snapshot_id` (required): The snapshot to restore
- `mode` (optional): `read_only` (view only) or `overwrite` (replace current). Default: `read_only`

**Example:**
```
Restore snapshot snap_abc123 in read_only mode
```

#### list
List all snapshots.

**Parameters:**
- `action`: `list`

**Example:**
```
List my memory snapshots
```

#### compare
Compare two snapshots or a snapshot with current state.

**Parameters:**
- `action`: `compare`
- `snapshot_id` (required): First snapshot
- `compare_to` (optional): Second snapshot ID or `current`. Default: `current`

**Example:**
```
Compare snapshot snap_abc123 to current state
```

**Response:**
```json
{
  "success": true,
  "data": {
    "added": 12,
    "removed": 3,
    "modified": 5,
    "unchanged": 130,
    "diff": [...]
  }
}
```

---

## Memory Types

| Type | Use For | Example |
|------|---------|---------|
| `fact` | Objective information | "Project uses Next.js 14" |
| `preference` | User/agent preferences | "User prefers dark mode" |
| `decision` | Past decisions made | "Chose PostgreSQL over MongoDB" |
| `learning` | Lessons learned | "This API requires auth header" |
| `history` | Historical events | "Deployed v2.1 on Jan 15" |
| `context` | General context | "Working on e-commerce project" |

## Best Practices

### When to Store
- User states a preference → Store as `preference`
- Important decision made → Store as `decision`
- Learned something new → Store as `learning`
- Key project fact → Store as `fact`

### When to Recall
- Starting a new session → Recall recent context
- Before making suggestions → Check preferences
- Encountering similar problem → Check learnings

### Using Reputation
- After successful action → Update with `outcome: success`
- After failed approach → Update with `outcome: failure`
- When recalling strategies → Use `recall_ranked` for proven approaches

### Using Pools
- Team of agents working together → Create shared pool
- Knowledge that benefits multiple agents → Store in pool
- Looking for collective wisdom → Recall from pool

### Using Snapshots
- Before major changes → Create snapshot
- Debugging unexpected behavior → Compare to past state
- Rolling back mistakes → Restore from snapshot

### Example Workflow

```
# Session 1: User mentions preference
User: "I always want you to use TypeScript"
Agent: [Stores as preference: "User prefers TypeScript for all code"]

# Session 2: New task
User: "Create a new API endpoint"
Agent: [Recalls preferences about coding]
Agent: "I'll create this in TypeScript based on your preference."

# Session 3: Learning from outcome
Agent: [Used retry logic, it worked]
Agent: [Updates reputation: memory_id=mem_xyz, outcome=success]

# Session 4: Making decisions
Agent: [Recalls ranked memories about error handling]
Agent: [Uses highest-reputation approach first]
```

## Pricing

| Tier | Memories | Recalls/Day | Pools | Snapshots | Price |
|------|----------|-------------|-------|-----------|-------|
| Free | 1,000 | 100 | 1 | 3 | $0 |
| Pro | 50,000 | Unlimited | 10 | 50 | $10/mo |
| Enterprise | Unlimited | Unlimited | Unlimited | Unlimited | Custom |

## API Endpoints

Base URL: `https://openclawdy.xyz/api`

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/memory/store` | Store a memory |
| POST | `/memory/recall` | Semantic search |
| GET | `/memory/list` | List memories |
| GET | `/memory/{id}` | Get specific memory |
| DELETE | `/memory/{id}` | Delete memory |
| GET | `/memory/vault` | Export all |
| DELETE | `/memory/vault` | Clear vault |
| GET | `/agent/stats` | Usage stats |

### Reputation Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/memory/reputation/store` | Store with reputation |
| POST | `/memory/reputation/recall` | Recall by reputation |
| POST | `/memory/reputation/update` | Update reputation |

### Pool Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/memory/pool/create` | Create pool |
| POST | `/memory/pool/store` | Store in pool |
| POST | `/memory/pool/recall` | Recall from pool |
| GET | `/memory/pool/list` | List pools |

### Snapshot Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/memory/snapshot/create` | Create snapshot |
| POST | `/memory/snapshot/restore` | Restore snapshot |
| GET | `/memory/snapshot/list` | List snapshots |
| POST | `/memory/snapshot/compare` | Compare snapshots |

## Authentication Headers

All requests require wallet signature authentication:

```
X-Agent-Address: 0x...      # Your wallet address
X-Agent-Signature: 0x...    # Signed message
X-Agent-Timestamp: 123...   # Unix timestamp (ms)
```

Message format to sign:
```
OpenClawdy Auth
Timestamp: {timestamp}
```

## ACP Integration

OpenClawdy is available on the Agent Commerce Protocol (ACP). Other agents can purchase memory services directly:

| Service | Fee | Description |
|---------|-----|-------------|
| memory_store | $0.01 | Store a memory |
| memory_recall | $0.02 | Semantic search |
| memory_reputation | $0.02 | Reputation operations |
| memory_pool | $0.03 | Pool operations |
| memory_snapshot | $0.05 | Snapshot operations |

## Support

- Website: https://openclawdy.xyz
- Twitter: @openclawdy
- ACP Agent: OpenClawdy Memory

## License

MIT
