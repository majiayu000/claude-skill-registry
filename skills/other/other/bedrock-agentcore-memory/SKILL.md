---
name: bedrock-agentcore-memory
description: Amazon Bedrock AgentCore Memory for persistent agent knowledge across sessions. Episodic memory for learning from interactions, short-term for session context. Use when building agents that remember user preferences, learn from conversations, or maintain context across sessions.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Amazon Bedrock AgentCore Memory

## Overview

AgentCore Memory enables agents to maintain persistent knowledge across sessions, learning from user interactions to provide increasingly personalized experiences. It combines short-term session context with long-term episodic memory extracted through background reflection processes.

**Purpose**: Give agents persistent memory and learning capabilities

**Pattern**: Capabilities-based (2 memory types)

**Key Principles** (validated by AWS December 2025):
1. **Episodic Memory** - Long-term facts extracted from conversations
2. **Short-term Memory** - Raw turn-by-turn session context
3. **Automatic Extraction** - Background reflection creates episodes
4. **Semantic Retrieval** - Context-aware memory lookup
5. **User-Scoped** - Memory isolated per user/actor
6. **Privacy Controls** - Granular memory management

**Quality Targets**:
- Memory retrieval latency: < 100ms
- Extraction accuracy: ≥ 85%
- Storage efficiency: Deduplicated facts

---

## When to Use

Use bedrock-agentcore-memory when:

- Building agents that remember user preferences
- Creating personalized experiences across sessions
- Implementing learning from past interactions
- Maintaining context for long-running workflows
- Building agents that improve over time

**When NOT to Use**:
- Simple stateless Q&A (no persistence needed)
- Short single-session interactions
- When user data cannot be stored (compliance)

---

## Prerequisites

### Required
- AgentCore agent deployed
- Memory resource created
- IAM permissions for memory operations

### Recommended
- User/actor identification strategy
- Data retention policies defined
- Privacy requirements documented

---

## Memory Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Runtime                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Session 1          Session 2          Session N        │
│  ┌─────────┐        ┌─────────┐        ┌─────────┐     │
│  │Short-   │        │Short-   │        │Short-   │     │
│  │term     │        │term     │        │term     │     │
│  │Memory   │        │Memory   │        │Memory   │     │
│  └────┬────┘        └────┬────┘        └────┬────┘     │
│       │                  │                  │          │
│       └──────────────────┼──────────────────┘          │
│                          ▼                             │
│              ┌───────────────────────┐                 │
│              │   Reflection Engine   │                 │
│              │  (Background Process) │                 │
│              └───────────┬───────────┘                 │
│                          ▼                             │
│              ┌───────────────────────┐                 │
│              │   Episodic Memory     │                 │
│              │  (Long-term Storage)  │                 │
│              │                       │                 │
│              │  • User prefers X     │                 │
│              │  • Learned fact Y     │                 │
│              │  • Historical event Z │                 │
│              └───────────────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Operations

### Operation 1: Create Memory Resource

**Time**: 2-5 minutes
**Automation**: 95%
**Purpose**: Initialize memory storage for an agent

**Create Memory**:
```python
import boto3

control = boto3.client('bedrock-agentcore-control')

# Create memory resource
response = control.create_memory(
    name='customer-service-memory',
    description='Long-term memory for customer service agent',
    memoryConfiguration={
        'episodicMemoryConfig': {
            'enabled': True,
            'reflectionConfig': {
                'reflectionInterval': 'SESSION_END',  # or 'PERIODIC'
                'extractionModel': 'anthropic.claude-3-sonnet-20240229-v1:0'
            }
        },
        'shortTermMemoryConfig': {
            'enabled': True,
            'maxTurns': 50,  # Keep last 50 turns in session
            'contextWindowStrategy': 'SLIDING'
        }
    },
    retentionConfig={
        'episodicRetentionDays': 365,  # Keep episodic memory 1 year
        'shortTermRetentionDays': 7    # Clear short-term after 7 days
    }
)

memory_id = response['memory']['memoryId']
print(f"Created memory: {memory_id}")

# Wait for memory to be ready
waiter = control.get_waiter('MemoryCreated')
waiter.wait(memoryId=memory_id)
```

**Configure Memory Strategies**:
```python
# Different memory configurations for different use cases

# Travel agent - remember preferences long-term
travel_memory = control.create_memory(
    name='travel-agent-memory',
    memoryConfiguration={
        'episodicMemoryConfig': {
            'enabled': True,
            'reflectionConfig': {
                'reflectionInterval': 'SESSION_END',
                'extractionInstructions': '''
                    Extract and remember:
                    - Preferred airlines and seat types
                    - Hotel preferences (chain, room type)
                    - Dietary restrictions
                    - Travel companion information
                    - Budget preferences
                '''
            }
        }
    }
)

# Support agent - focus on issue history
support_memory = control.create_memory(
    name='support-agent-memory',
    memoryConfiguration={
        'episodicMemoryConfig': {
            'enabled': True,
            'reflectionConfig': {
                'reflectionInterval': 'PERIODIC',
                'periodicIntervalMinutes': 30,
                'extractionInstructions': '''
                    Extract and remember:
                    - Technical issues encountered
                    - Solutions that worked
                    - Customer's technical level
                    - Products owned
                '''
            }
        }
    }
)
```

---

### Operation 2: Store Memory Events

**Time**: Real-time
**Automation**: 100%
**Purpose**: Feed interaction data for memory extraction

**Store Interaction Events**:
```python
import boto3
import datetime
import uuid

client = boto3.client('bedrock-agentcore')

# Store user message event
response = client.create_event(
    memoryId='memory-xxx',
    actorId='user-12345',  # User identifier
    sessionId='session-abc123',
    event={
        'eventTime': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'traceId': str(uuid.uuid4()),
        'userMessage': {
            'content': 'I only fly aisle seats because of my long legs.'
        }
    }
)

# Store agent response event
client.create_event(
    memoryId='memory-xxx',
    actorId='user-12345',
    sessionId='session-abc123',
    event={
        'eventTime': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'traceId': str(uuid.uuid4()),
        'assistantMessage': {
            'content': 'I\'ve noted your preference for aisle seats. I\'ll make sure to prioritize those when searching for flights.'
        }
    }
)

# Store tool call event
client.create_event(
    memoryId='memory-xxx',
    actorId='user-12345',
    sessionId='session-abc123',
    event={
        'eventTime': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'traceId': str(uuid.uuid4()),
        'toolCall': {
            'toolName': 'SearchFlights',
            'toolInput': {
                'origin': 'SFO',
                'destination': 'JFK',
                'seatPreference': 'aisle'
            },
            'toolOutput': {
                'flights': [...]
            }
        }
    }
)
```

**Batch Event Storage**:
```python
# Store multiple events efficiently
events = [
    {
        'eventTime': timestamp1,
        'userMessage': {'content': 'Book me a hotel in NYC'}
    },
    {
        'eventTime': timestamp2,
        'toolCall': {'toolName': 'SearchHotels', 'toolInput': {...}}
    },
    {
        'eventTime': timestamp3,
        'assistantMessage': {'content': 'I found several options...'}
    }
]

# Note: Batch API may be available - check latest docs
for event in events:
    client.create_event(
        memoryId=memory_id,
        actorId='user-12345',
        sessionId=session_id,
        event={
            'traceId': str(uuid.uuid4()),
            **event
        }
    )
```

---

### Operation 3: Retrieve Memories

**Time**: < 100ms
**Automation**: 100%
**Purpose**: Get relevant memories for current context

**Retrieve by Semantic Query**:
```python
# Retrieve memories relevant to current conversation
response = client.retrieve_memory_records(
    memoryId='memory-xxx',
    actorId='user-12345',
    retrievalQuery={
        'semanticQuery': 'flight preferences and seating',
        'maxRecords': 10
    }
)

memories = response['memoryRecords']
for memory in memories:
    print(f"Memory: {memory['content']}")
    print(f"Created: {memory['createdAt']}")
    print(f"Relevance: {memory.get('relevanceScore', 'N/A')}")
    print("---")

# Example output:
# Memory: User prefers aisle seats due to legroom requirements
# Created: 2025-11-15T10:30:00Z
# Relevance: 0.95
```

**Retrieve All Memories for User**:
```python
# List all episodic memories for a user
memories = []
paginator = client.get_paginator('list_memory_records')

for page in paginator.paginate(
    memoryId='memory-xxx',
    actorId='user-12345'
):
    memories.extend(page['memoryRecords'])

print(f"Total memories for user: {len(memories)}")

# Categorize memories
preferences = [m for m in memories if 'preference' in m['content'].lower()]
history = [m for m in memories if 'booked' in m['content'].lower()]
```

**Context-Aware Retrieval**:
```python
def get_relevant_memories(memory_id, user_id, current_context):
    """Retrieve memories relevant to current conversation context"""

    # Extract key topics from current context
    topics = extract_topics(current_context)

    # Retrieve for each topic
    all_memories = []
    for topic in topics:
        response = client.retrieve_memory_records(
            memoryId=memory_id,
            actorId=user_id,
            retrievalQuery={
                'semanticQuery': topic,
                'maxRecords': 5
            }
        )
        all_memories.extend(response['memoryRecords'])

    # Deduplicate and rank
    unique_memories = deduplicate(all_memories)
    return sorted(unique_memories, key=lambda m: m.get('relevanceScore', 0), reverse=True)[:10]
```

---

### Operation 4: Manual Memory Management

**Time**: 1-5 minutes
**Automation**: 80%
**Purpose**: Create, update, or delete specific memories

**Create Manual Memory Record**:
```python
# Manually create a memory (not from reflection)
response = client.batch_create_memory_records(
    memoryId='memory-xxx',
    actorId='user-12345',
    memoryRecords=[
        {
            'content': 'User is a premium member since 2023',
            'metadata': {
                'source': 'CRM_IMPORT',
                'confidence': 1.0,
                'category': 'MEMBERSHIP'
            }
        },
        {
            'content': 'User has nut allergy - critical dietary restriction',
            'metadata': {
                'source': 'MANUAL_ENTRY',
                'confidence': 1.0,
                'category': 'DIETARY',
                'priority': 'HIGH'
            }
        }
    ]
)
```

**Update Memory Record**:
```python
# Update existing memory
client.batch_update_memory_records(
    memoryId='memory-xxx',
    actorId='user-12345',
    updates=[
        {
            'memoryRecordId': 'record-123',
            'content': 'User prefers window seats (changed from aisle)',
            'metadata': {
                'lastUpdated': datetime.datetime.now().isoformat(),
                'updateReason': 'User explicitly changed preference'
            }
        }
    ]
)
```

**Delete Memory Records**:
```python
# Delete specific memory
client.delete_memory_record(
    memoryId='memory-xxx',
    memoryRecordId='record-123'
)

# Batch delete
client.batch_delete_memory_records(
    memoryId='memory-xxx',
    actorId='user-12345',
    memoryRecordIds=['record-1', 'record-2', 'record-3']
)

# Delete all memories for a user (GDPR right to be forgotten)
all_records = list_all_user_memories(memory_id, 'user-12345')
client.batch_delete_memory_records(
    memoryId='memory-xxx',
    actorId='user-12345',
    memoryRecordIds=[r['memoryRecordId'] for r in all_records]
)
```

---

### Operation 5: Memory Extraction Jobs

**Time**: 5-30 minutes (background)
**Automation**: 100%
**Purpose**: Trigger and monitor episodic memory extraction

**Start Manual Extraction**:
```python
# Manually trigger reflection/extraction
response = client.start_memory_extraction_job(
    memoryId='memory-xxx',
    extractionConfig={
        'actorIds': ['user-12345', 'user-67890'],  # Specific users
        'sessionFilter': {
            'startTime': '2025-12-01T00:00:00Z',
            'endTime': '2025-12-05T23:59:59Z'
        }
    }
)

job_id = response['extractionJobId']

# Monitor job
while True:
    status = client.list_memory_extraction_jobs(
        memoryId='memory-xxx'
    )

    job = next(j for j in status['jobs'] if j['jobId'] == job_id)

    if job['status'] == 'COMPLETED':
        print(f"Extracted {job['recordsCreated']} new memories")
        break
    elif job['status'] == 'FAILED':
        print(f"Extraction failed: {job['error']}")
        break

    time.sleep(30)
```

**Custom Extraction Instructions**:
```python
# Update memory with custom extraction instructions
control.update_memory(
    memoryId='memory-xxx',
    memoryConfiguration={
        'episodicMemoryConfig': {
            'reflectionConfig': {
                'extractionInstructions': '''
                From each conversation, extract and remember:

                1. USER PREFERENCES (high priority):
                   - Product preferences
                   - Communication style preferences
                   - Time/schedule preferences

                2. IMPORTANT FACTS (high priority):
                   - Allergies or restrictions
                   - Account/membership status
                   - Key dates (birthdays, anniversaries)

                3. INTERACTION HISTORY (medium priority):
                   - Products purchased
                   - Issues resolved
                   - Feedback given

                4. CONTEXT HINTS (low priority):
                   - Mentioned family members
                   - Hobbies or interests
                   - Location information

                DO NOT extract:
                - Temporary session-specific details
                - Sensitive financial information
                - Health information beyond allergies
                '''
            }
        }
    }
)
```

---

## Integration with Agent

**Memory-Aware Agent Pattern**:
```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
memory_client = boto3.client('bedrock-agentcore')

MEMORY_ID = 'memory-xxx'

@app.entrypoint
def invoke(payload):
    user_id = payload.get('user_id')
    user_message = payload.get('prompt')
    session_id = payload.get('session_id', str(uuid.uuid4()))

    # 1. Retrieve relevant memories
    memories = get_relevant_memories(user_id, user_message)
    memory_context = format_memories_for_context(memories)

    # 2. Build enhanced prompt with memories
    enhanced_prompt = f"""
You are a helpful assistant with knowledge about this user.

USER HISTORY AND PREFERENCES:
{memory_context}

CURRENT REQUEST:
{user_message}

Respond helpfully, incorporating relevant knowledge about the user.
"""

    # 3. Run agent
    agent = Agent(model="anthropic.claude-sonnet-4-20250514-v1:0")
    result = agent(enhanced_prompt)

    # 4. Store interaction for future learning
    store_interaction(user_id, session_id, user_message, result.message)

    return {"response": result.message}

def get_relevant_memories(user_id, query):
    """Retrieve relevant memories for context"""
    try:
        response = memory_client.retrieve_memory_records(
            memoryId=MEMORY_ID,
            actorId=user_id,
            retrievalQuery={
                'semanticQuery': query,
                'maxRecords': 5
            }
        )
        return response['memoryRecords']
    except Exception:
        return []

def format_memories_for_context(memories):
    """Format memories as context string"""
    if not memories:
        return "No prior interaction history available."

    lines = []
    for m in memories:
        lines.append(f"- {m['content']}")
    return "\n".join(lines)

def store_interaction(user_id, session_id, user_msg, assistant_msg):
    """Store interaction for memory extraction"""
    memory_client.create_event(
        memoryId=MEMORY_ID,
        actorId=user_id,
        sessionId=session_id,
        event={
            'eventTime': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'traceId': str(uuid.uuid4()),
            'userMessage': {'content': user_msg}
        }
    )
    memory_client.create_event(
        memoryId=MEMORY_ID,
        actorId=user_id,
        sessionId=session_id,
        event={
            'eventTime': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'traceId': str(uuid.uuid4()),
            'assistantMessage': {'content': assistant_msg}
        }
    )
```

---

## Best Practices

### 1. User Identification
```python
# Use consistent, stable user IDs
# Good: Database user ID, OAuth sub claim
# Bad: Session ID, email (can change)

actor_id = f"user-{user.database_id}"  # Good
# actor_id = user.email  # Bad - can change
```

### 2. Privacy-First Design
```python
# Provide memory opt-out
if user.preferences.get('memory_enabled', True):
    store_interaction(...)
else:
    pass  # Don't store

# Support deletion requests (GDPR)
def handle_deletion_request(user_id):
    all_records = list_all_memories(user_id)
    client.batch_delete_memory_records(
        memoryId=MEMORY_ID,
        actorId=user_id,
        memoryRecordIds=[r['id'] for r in all_records]
    )
```

### 3. Memory Categories
```python
# Use metadata for organization
memory_categories = {
    'PREFERENCE': 'User preferences and settings',
    'FACT': 'Known facts about user',
    'HISTORY': 'Past interactions and events',
    'RESTRICTION': 'Constraints (allergies, limits)'
}

# Store with category
client.batch_create_memory_records(
    memoryId=MEMORY_ID,
    actorId=user_id,
    memoryRecords=[{
        'content': 'User prefers morning appointments',
        'metadata': {
            'category': 'PREFERENCE',
            'confidence': 0.9
        }
    }]
)
```

---

## Related Skills

- **bedrock-agentcore**: Core platform setup
- **bedrock-agentcore-deployment**: Deploying memory-enabled agents
- **bedrock-agentcore-policy**: Memory access policies
- **agent-memory-system**: General agent memory patterns

---

## References

- `references/memory-patterns.md` - Common memory implementation patterns
- `references/privacy-compliance.md` - GDPR and privacy requirements
- `references/extraction-tuning.md` - Optimizing memory extraction

---

## Sources

- [Amazon Bedrock AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-get-started.html)
- [Boto3 BedrockAgentCore](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html)
