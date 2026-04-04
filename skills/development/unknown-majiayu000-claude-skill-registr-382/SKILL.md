---
name: agent-communication
version: 1.0.0
author: claude-command-and-control
created: 2025-11-29
last_updated: 2025-11-29
status: active
complexity: moderate
category: orchestration
tags: [inter-agent-messaging, shared-context, event-broadcasting, handoff-protocol, coordination]
---

# Agent Communication Skill

## Description
Comprehensive inter-agent messaging and coordination system providing protocol-based communication, shared context management, event broadcasting with subscriptions, automated handoff documentation, and message persistence. This skill enables agents to coordinate work, share decisions, negotiate contracts, and maintain consistent state across distributed parallel execution environments.

## When to Use This Skill
- "Facilitate communication between builder agents needing to coordinate API contract changes"
- "Coordinate handoffs between architect completing design and builders starting implementation"
- "Manage inter-agent messaging for microservices team sharing service interface definitions"
- "Broadcast architectural decisions to all agents working on authentication feature"
- "Handle agent-to-agent communication for parallel data pipeline development with shared schemas"

## When NOT to Use This Skill
- Single agent workflows with no coordination needs → No messaging required
- Sequential handoffs with explicit synchronization → Use standard handoff documentation
- Simple file-based coordination (shared README) → Direct file collaboration sufficient
- User-to-agent communication → Use standard CLI/UI interactions

## Prerequisites
- Multiple agents working concurrently or in sequence
- Shared filesystem or message bus infrastructure
- Agent registry with contact information and capabilities
- Standardized message schema and protocols
- Event subscription system (file-based or message queue)

## Workflow

### Phase 1: Communication Infrastructure Setup
**Purpose**: Establish message transport, routing, and persistence mechanisms

#### Step 1.1: Initialize Message Bus
Set up message routing infrastructure:

```bash
function initialize_message_bus() {
  local project_root=$1

  echo "Initializing agent message bus..."

  # Create message directories
  mkdir -p "$project_root/.agent-messages/inbox"
  mkdir -p "$project_root/.agent-messages/outbox"
  mkdir -p "$project_root/.agent-messages/archive"
  mkdir -p "$project_root/.agent-messages/events"
  mkdir -p "$project_root/.agent-messages/broadcasts"

  # Create message registry
  cat > "$project_root/.agent-messages/registry.json" <<EOF
{
  "initialized_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "message_count": 0,
  "agents": {},
  "event_subscriptions": {},
  "message_retention_hours": 72
}
EOF

  # Create routing table
  cat > "$project_root/.agent-messages/routing.json" <<EOF
{
  "routes": {
    "direct": "inbox/{recipient}/",
    "broadcast": "broadcasts/",
    "event": "events/{event_type}/",
    "archive": "archive/{date}/"
  },
  "priority_queues": {
    "critical": 1,
    "high": 2,
    "normal": 3,
    "low": 4
  }
}
EOF

  echo "✅ Message bus initialized at $project_root/.agent-messages/"
}
```

**Directory Structure**:
```
.agent-messages/
├── inbox/              # Per-agent inboxes
│   ├── builder-1/
│   ├── builder-2/
│   └── validator-1/
├── outbox/             # Pending message delivery
├── archive/            # Historical messages (by date)
│   ├── 2025-11-29/
│   └── 2025-11-30/
├── events/             # Event-based messages
│   ├── TaskCompleted/
│   ├── BlockerEncountered/
│   └── MilestoneReached/
├── broadcasts/         # Messages to all agents
└── registry.json       # Message bus metadata
```

**Expected Output**: Initialized message bus directory structure with routing configuration

#### Step 1.2: Register Agents
Build agent directory for routing:

```bash
function register_agent() {
  local agent_id=$1
  local agent_role=$2
  local worktree_path=$3
  local capabilities=$4  # JSON array

  local registry_file=".agent-messages/registry.json"

  # Create agent inbox
  mkdir -p ".agent-messages/inbox/$agent_id"

  # Register agent in directory
  jq --arg id "$agent_id" \
     --arg role "$agent_role" \
     --arg path "$worktree_path" \
     --argjson caps "$capabilities" \
     '.agents[$id] = {
       "role": $role,
       "worktree_path": $path,
       "capabilities": $caps,
       "registered_at": now|todate,
       "status": "active",
       "last_seen": now|todate,
       "message_count": 0
     }' "$registry_file" > "$registry_file.tmp"

  mv "$registry_file.tmp" "$registry_file"

  echo "✅ Registered agent: $agent_id ($agent_role)"
}

# Example registration
register_agent "builder-1" "builder" "worktrees/builder-1" \
  '["jwt-implementation", "api-development", "typescript"]'
```

**Agent Registry Entry**:
```json
{
  "agents": {
    "builder-1": {
      "role": "builder",
      "worktree_path": "worktrees/builder-1",
      "capabilities": ["jwt-implementation", "api-development", "typescript"],
      "registered_at": "2025-11-29T14:30:52Z",
      "status": "active",
      "last_seen": "2025-11-29T14:30:52Z",
      "message_count": 0
    }
  }
}
```

**Expected Output**: Registered agents with inboxes and capability metadata

#### Step 1.3: Define Message Schema
Establish standardized message format:

**Message Schema (JSON)**:
```json
{
  "message_id": "msg_20251129_143052_001",
  "protocol_version": "1.0",
  "timestamp": "2025-11-29T14:30:52Z",
  "from_agent": "builder-1",
  "to_agent": "builder-2",
  "message_type": "interface_contract",
  "priority": "high",
  "subject": "IUserService interface definition",
  "payload": {
    "contract_type": "typescript_interface",
    "interface_name": "IUserService",
    "methods": [
      {
        "name": "findById",
        "params": [{"name": "id", "type": "string"}],
        "return_type": "Promise<User | null>"
      },
      {
        "name": "create",
        "params": [{"name": "userData", "type": "CreateUserDto"}],
        "return_type": "Promise<User>"
      }
    ],
    "purpose": "JWT service needs to lookup users by ID for token generation"
  },
  "requires_response": true,
  "response_deadline": "2025-11-29T16:30:52Z",
  "conversation_id": "conv_auth_contracts_001",
  "metadata": {
    "task_id": "pg2-task-1",
    "related_files": ["services/user.service.ts", "services/jwt.service.ts"]
  }
}
```

**Message Types**:
- `interface_contract`: API/interface definitions
- `decision_announcement`: Architectural decisions
- `blocker_notification`: Work blocked, needs input
- `handoff_request`: Ready to transfer work
- `resource_conflict`: File/resource contention
- `progress_update`: Status notification
- `question`: Request for clarification
- `response`: Reply to previous message

**Expected Output**: Message schema documentation and validation library

### Phase 2: Message Sending and Routing
**Purpose**: Enable agents to send messages with appropriate routing and delivery

#### Step 2.1: Send Direct Message
Agent-to-agent point-to-point messaging:

```bash
function send_message() {
  local from_agent=$1
  local to_agent=$2
  local message_type=$3
  local subject=$4
  local payload=$5  # JSON string
  local priority=${6:-normal}

  local message_id="msg_$(date +%Y%m%d_%H%M%S)_$(random_string 6)"
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Create message file
  local message_file=".agent-messages/inbox/$to_agent/${message_id}.json"

  cat > "$message_file" <<EOF
{
  "message_id": "$message_id",
  "protocol_version": "1.0",
  "timestamp": "$timestamp",
  "from_agent": "$from_agent",
  "to_agent": "$to_agent",
  "message_type": "$message_type",
  "priority": "$priority",
  "subject": "$subject",
  "payload": $payload,
  "requires_response": false,
  "status": "delivered",
  "delivered_at": "$timestamp"
}
EOF

  # Update message count
  jq --arg agent "$to_agent" \
     '.agents[$agent].message_count += 1' \
     .agent-messages/registry.json > .agent-messages/registry.json.tmp
  mv .agent-messages/registry.json.tmp .agent-messages/registry.json

  # Log to outbox for sender
  cp "$message_file" ".agent-messages/outbox/${message_id}_to_${to_agent}.json"

  echo "✅ Message sent: $from_agent → $to_agent ($message_type)"
  echo "   ID: $message_id"
  echo "   Subject: $subject"
}

# Example usage
send_message "builder-1" "builder-2" "interface_contract" \
  "IUserService interface definition" \
  '{"interface": "IUserService", "methods": ["findById", "create"]}' \
  "high"
```

**Expected Output**: Message delivered to recipient inbox with confirmation

#### Step 2.2: Broadcast Message
Send message to all registered agents:

```bash
function broadcast_message() {
  local from_agent=$1
  local message_type=$2
  local subject=$3
  local payload=$4

  local message_id="bcast_$(date +%Y%m%d_%H%M%S)_$(random_string 6)"
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Create broadcast message
  local broadcast_file=".agent-messages/broadcasts/${message_id}.json"

  cat > "$broadcast_file" <<EOF
{
  "message_id": "$message_id",
  "protocol_version": "1.0",
  "timestamp": "$timestamp",
  "from_agent": "$from_agent",
  "to_agent": "ALL",
  "message_type": "$message_type",
  "subject": "$subject",
  "payload": $payload,
  "broadcast": true
}
EOF

  # Deliver to all active agents
  local agent_count=0
  for agent_id in $(jq -r '.agents | keys[]' .agent-messages/registry.json); do
    if [ "$agent_id" != "$from_agent" ]; then
      cp "$broadcast_file" ".agent-messages/inbox/$agent_id/${message_id}.json"
      agent_count=$((agent_count + 1))
    fi
  done

  echo "✅ Broadcast sent to $agent_count agents"
  echo "   From: $from_agent"
  echo "   Subject: $subject"
}

# Example broadcast
broadcast_message "architect-1" "decision_announcement" \
  "Authentication will use RS256 algorithm for JWT" \
  '{
    "decision": "Use RS256 for JWT signing",
    "rationale": "Better security, supports key rotation",
    "impact": "All auth services must use RS256 keypair",
    "effective_date": "immediate"
  }'
```

**Expected Output**: Message delivered to all agent inboxes

#### Step 2.3: Publish Event
Emit event for subscribed agents:

```bash
function publish_event() {
  local event_type=$1
  local source_agent=$2
  local event_data=$3  # JSON

  local event_id="evt_$(date +%Y%m%d_%H%M%S)_$(random_string 6)"
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Create event directory if needed
  mkdir -p ".agent-messages/events/$event_type"

  # Create event file
  local event_file=".agent-messages/events/$event_type/${event_id}.json"

  cat > "$event_file" <<EOF
{
  "event_id": "$event_id",
  "event_type": "$event_type",
  "timestamp": "$timestamp",
  "source_agent": "$source_agent",
  "event_data": $event_data
}
EOF

  # Deliver to subscribed agents
  local subscribers=$(jq -r ".event_subscriptions[\"$event_type\"] // []" \
    .agent-messages/registry.json)

  for agent_id in $(echo "$subscribers" | jq -r '.[]'); do
    cp "$event_file" ".agent-messages/inbox/$agent_id/${event_id}.json"
  done

  echo "✅ Event published: $event_type"
  echo "   Source: $source_agent"
  echo "   Subscribers notified: $(echo "$subscribers" | jq length)"
}

# Example event
publish_event "TaskCompleted" "builder-1" \
  '{
    "task_id": "pg2-task-1",
    "task_name": "Implement JWT service",
    "completed_at": "2025-11-29T16:15:30Z",
    "artifacts": ["services/jwt.service.ts", "services/jwt.service.spec.ts"],
    "test_results": {"passed": 24, "failed": 0, "coverage": 92}
  }'
```

**Expected Output**: Event delivered to all subscribed agents

### Phase 3: Message Receiving and Processing
**Purpose**: Enable agents to poll, read, and process incoming messages

#### Step 3.1: Check Inbox for New Messages
Poll for unread messages:

```bash
function check_inbox() {
  local agent_id=$1
  local inbox_dir=".agent-messages/inbox/$agent_id"

  # Find unread messages (no .read marker)
  local unread_messages=()

  for msg_file in "$inbox_dir"/*.json; do
    if [ -f "$msg_file" ] && [ ! -f "${msg_file}.read" ]; then
      unread_messages+=("$msg_file")
    fi
  done

  echo "📬 Inbox check for $agent_id"
  echo "   Unread messages: ${#unread_messages[@]}"

  # Display message summary
  for msg_file in "${unread_messages[@]}"; do
    local from=$(jq -r '.from_agent' "$msg_file")
    local type=$(jq -r '.message_type' "$msg_file")
    local subject=$(jq -r '.subject' "$msg_file")
    local priority=$(jq -r '.priority' "$msg_file")

    echo "   [$priority] $from: $subject ($type)"
  done

  # Return unread message files
  printf '%s\n' "${unread_messages[@]}"
}
```

**Expected Output**: List of unread messages with metadata

#### Step 3.2: Read and Process Message
Retrieve and handle specific message:

```bash
function read_message() {
  local agent_id=$1
  local message_file=$2

  echo "Reading message: $(basename "$message_file")"

  # Parse message
  local from_agent=$(jq -r '.from_agent' "$message_file")
  local message_type=$(jq -r '.message_type' "$message_file")
  local subject=$(jq -r '.subject' "$message_file")
  local payload=$(jq -r '.payload' "$message_file")
  local requires_response=$(jq -r '.requires_response' "$message_file")

  echo "From: $from_agent"
  echo "Type: $message_type"
  echo "Subject: $subject"
  echo ""
  echo "Payload:"
  echo "$payload" | jq .

  # Process based on message type
  case "$message_type" in
    interface_contract)
      process_interface_contract "$agent_id" "$message_file"
      ;;
    decision_announcement)
      process_decision "$agent_id" "$message_file"
      ;;
    blocker_notification)
      process_blocker "$agent_id" "$message_file"
      ;;
    handoff_request)
      process_handoff "$agent_id" "$message_file"
      ;;
    question)
      process_question "$agent_id" "$message_file"
      ;;
    *)
      echo "⚠️  Unknown message type: $message_type"
      ;;
  esac

  # Mark as read
  touch "${message_file}.read"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "${message_file}.read"

  # Send acknowledgment if required
  if [ "$requires_response" == "true" ]; then
    send_acknowledgment "$agent_id" "$from_agent" "$message_file"
  fi
}
```

**Expected Output**: Processed message with appropriate action taken

#### Step 3.3: Respond to Message
Send reply to received message:

```bash
function respond_to_message() {
  local agent_id=$1
  local original_message_file=$2
  local response_payload=$3  # JSON

  local original_id=$(jq -r '.message_id' "$original_message_file")
  local original_from=$(jq -r '.from_agent' "$original_message_file")
  local conversation_id=$(jq -r '.conversation_id // empty' "$original_message_file")

  # If no conversation ID, create one
  if [ -z "$conversation_id" ]; then
    conversation_id="conv_$(date +%Y%m%d_%H%M%S)"
  fi

  local response_id="resp_$(date +%Y%m%d_%H%M%S)_$(random_string 6)"
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Create response message
  local response_file=".agent-messages/inbox/$original_from/${response_id}.json"

  cat > "$response_file" <<EOF
{
  "message_id": "$response_id",
  "protocol_version": "1.0",
  "timestamp": "$timestamp",
  "from_agent": "$agent_id",
  "to_agent": "$original_from",
  "message_type": "response",
  "subject": "Re: $(jq -r '.subject' "$original_message_file")",
  "payload": $response_payload,
  "in_reply_to": "$original_id",
  "conversation_id": "$conversation_id",
  "status": "delivered"
}
EOF

  echo "✅ Response sent to $original_from"
  echo "   Conversation: $conversation_id"
}

# Example response
respond_to_message "builder-2" "$message_file" \
  '{
    "status": "accepted",
    "interface_approved": true,
    "implementation_notes": "Will implement IUserService with these methods",
    "estimated_completion": "2025-11-29T18:00:00Z"
  }'
```

**Expected Output**: Response message delivered to original sender

### Phase 4: Shared Context Management
**Purpose**: Maintain synchronized state and shared knowledge across agents

#### Step 4.1: Create Shared Context Document
Establish shared knowledge base:

```bash
function initialize_shared_context() {
  local context_name=$1
  local initial_content=$2

  mkdir -p ".agent-messages/shared-context"

  local context_file=".agent-messages/shared-context/${context_name}.md"

  cat > "$context_file" <<EOF
# Shared Context: $context_name

**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Last Updated**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Contributors**: []

---

$initial_content

---

## Update History
- $(date -u +%Y-%m-%dT%H:%M:%S)Z: Initial creation
EOF

  # Create lock file for concurrent access control
  cat > "$context_file.lock" <<EOF
{
  "locked": false,
  "locked_by": null,
  "locked_at": null
}
EOF

  echo "✅ Created shared context: $context_name"
}

# Example: Create API contracts context
initialize_shared_context "api-contracts" \
  "# API Contract Definitions

## Authentication Endpoints

### POST /auth/login
**Status**: Defined by architect-1
**Implemented by**: builder-1 (in progress)

### POST /auth/register
**Status**: Pending definition
"
```

**Shared Context Types**:
- **API Contracts**: Interface definitions, endpoint specs
- **Architecture Decisions**: Design choices with rationale
- **Data Models**: Database schemas, entity relationships
- **Configuration Standards**: Naming conventions, standards
- **Integration Points**: Service boundaries, dependencies

**Expected Output**: Initialized shared context document with version control

#### Step 4.2: Update Shared Context
Concurrent-safe context updates:

```bash
function update_shared_context() {
  local context_name=$1
  local agent_id=$2
  local update_content=$3

  local context_file=".agent-messages/shared-context/${context_name}.md"
  local lock_file="${context_file}.lock"

  # Acquire lock
  local max_wait=30  # seconds
  local waited=0

  while [ $waited -lt $max_wait ]; do
    local is_locked=$(jq -r '.locked' "$lock_file")

    if [ "$is_locked" == "false" ]; then
      # Acquire lock
      jq --arg agent "$agent_id" \
         '.locked = true | .locked_by = $agent | .locked_at = now|todate' \
         "$lock_file" > "${lock_file}.tmp"
      mv "${lock_file}.tmp" "$lock_file"
      break
    fi

    sleep 1
    waited=$((waited + 1))
  done

  if [ $waited -eq $max_wait ]; then
    echo "❌ Failed to acquire lock on $context_name after ${max_wait}s"
    return 1
  fi

  # Update context
  {
    cat "$context_file"
    echo ""
    echo "## Update: $(date -u +%Y-%m-%dT%H:%M:%S)Z by $agent_id"
    echo "$update_content"
  } > "${context_file}.tmp"

  mv "${context_file}.tmp" "$context_file"

  # Update metadata
  sed -i.bak "s/Last Updated:.*/Last Updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)/" "$context_file"

  # Release lock
  jq '.locked = false | .locked_by = null | .locked_at = null' \
     "$lock_file" > "${lock_file}.tmp"
  mv "${lock_file}.tmp" "$lock_file"

  echo "✅ Updated shared context: $context_name"

  # Broadcast update notification
  broadcast_message "$agent_id" "context_updated" \
    "Shared context '$context_name' updated" \
    "{\"context\": \"$context_name\", \"updated_by\": \"$agent_id\"}"
}

# Example update
update_shared_context "api-contracts" "builder-1" \
  "### POST /auth/login
**Implementation complete**
- JWT token returned in response
- Refresh token stored in httpOnly cookie
- 2FA support included
"
```

**Expected Output**: Updated shared context with change notification broadcast

### Phase 5: Handoff Documentation
**Purpose**: Formalize work transitions between agents with complete context

#### Step 5.1: Create Handoff Package
Bundle all artifacts and context for receiving agent:

```bash
function create_handoff_package() {
  local from_agent=$1
  local to_agent=$2
  local task_description=$3
  local artifacts=$4  # JSON array of file paths
  local context=$5    # Additional context text

  local handoff_id="handoff_$(date +%Y%m%d_%H%M%S)"
  local handoff_dir=".agent-messages/handoffs/$handoff_id"

  mkdir -p "$handoff_dir/artifacts"

  # Create handoff document
  cat > "$handoff_dir/HANDOFF.md" <<EOF
# Handoff: $from_agent → $to_agent

**Handoff ID**: $handoff_id
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**From**: $from_agent
**To**: $to_agent

## Task Description
$task_description

## Work Completed
[Summary of completed work]

## Artifacts Transferred
$(echo "$artifacts" | jq -r '.[] | "- " + .')

## Context and Background
$context

## Next Steps for Receiving Agent
1. Review artifacts in \`$handoff_dir/artifacts/\`
2. Read shared context documents
3. Run tests to verify functionality
4. Continue implementation from this point

## Known Issues / Blockers
[Any issues or blockers to be aware of]

## Questions / Clarifications
[Areas needing clarification]

## Acceptance Criteria
- [ ] All tests passing
- [ ] Code reviewed and understood
- [ ] Integration points verified
- [ ] Ready to continue implementation
EOF

  # Copy artifacts
  for artifact in $(echo "$artifacts" | jq -r '.[]'); do
    cp "$artifact" "$handoff_dir/artifacts/"
  done

  # Create metadata
  cat > "$handoff_dir/metadata.json" <<EOF
{
  "handoff_id": "$handoff_id",
  "from_agent": "$from_agent",
  "to_agent": "$to_agent",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "pending_acceptance",
  "artifacts": $artifacts
}
EOF

  # Send handoff notification
  send_message "$from_agent" "$to_agent" "handoff_request" \
    "Handoff ready: $task_description" \
    "{\"handoff_id\": \"$handoff_id\", \"handoff_dir\": \"$handoff_dir\"}" \
    "high"

  echo "✅ Handoff package created: $handoff_id"
  echo "   From: $from_agent → $to_agent"
  echo "   Artifacts: $(echo "$artifacts" | jq length)"
}

# Example handoff
create_handoff_package "architect-1" "builder-1" \
  "Implement JWT service based on design" \
  '["docs/jwt-design.md", "interfaces/IJwtService.ts", "schemas/token-schema.json"]' \
  "JWT service design is complete. Using RS256 algorithm. See shared context for API contracts."
```

**Handoff Package Contents**:
- **HANDOFF.md**: Complete handoff documentation
- **artifacts/**: All relevant files and documents
- **metadata.json**: Structured handoff metadata
- **context-links.md**: References to shared context docs
- **acceptance-checklist.md**: Criteria for accepting handoff

**Expected Output**: Complete handoff package with notification sent

#### Step 5.2: Accept Handoff
Receiving agent accepts and acknowledges handoff:

```bash
function accept_handoff() {
  local agent_id=$1
  local handoff_id=$2
  local acceptance_notes=$3

  local handoff_dir=".agent-messages/handoffs/$handoff_id"
  local metadata_file="$handoff_dir/metadata.json"

  # Update handoff status
  jq --arg agent "$agent_id" \
     --arg notes "$acceptance_notes" \
     '.status = "accepted" |
      .accepted_by = $agent |
      .accepted_at = now|todate |
      .acceptance_notes = $notes' \
     "$metadata_file" > "${metadata_file}.tmp"
  mv "${metadata_file}.tmp" "$metadata_file"

  # Append to handoff document
  cat >> "$handoff_dir/HANDOFF.md" <<EOF

---

## Handoff Accepted

**Accepted by**: $agent_id
**Accepted at**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

### Acceptance Notes
$acceptance_notes

### Acceptance Checklist
- [x] All tests passing
- [x] Code reviewed and understood
- [x] Integration points verified
- [x] Ready to continue implementation
EOF

  # Notify original agent
  local from_agent=$(jq -r '.from_agent' "$metadata_file")
  send_message "$agent_id" "$from_agent" "handoff_accepted" \
    "Handoff $handoff_id accepted" \
    "{\"handoff_id\": \"$handoff_id\", \"notes\": \"$acceptance_notes\"}"

  echo "✅ Handoff accepted: $handoff_id"
}

# Example acceptance
accept_handoff "builder-1" "handoff_20251129_143052" \
  "Design reviewed. All acceptance criteria met. Starting implementation."
```

**Expected Output**: Updated handoff status with acceptance confirmation

## Examples

### Example 1: Interface Contract Negotiation
**Context**: Two builder agents need to coordinate API interface changes

**Execution Flow:**

```bash
# Builder-1 proposes interface
send_message "builder-1" "builder-2" "interface_contract" \
  "Proposed IUserService interface" \
  '{
    "interface": "IUserService",
    "methods": [
      {"name": "findById", "params": ["id: string"], "returns": "Promise<User>"},
      {"name": "create", "params": ["data: CreateUserDto"], "returns": "Promise<User>"}
    ]
  }' "high"

# Builder-2 receives and reviews
check_inbox "builder-2"
# Output: 1 unread message from builder-1

read_message "builder-2" ".agent-messages/inbox/builder-2/msg_20251129_143052_abc123.json"

# Builder-2 proposes modification
respond_to_message "builder-2" "$message_file" \
  '{
    "status": "modification_requested",
    "changes": [
      {
        "method": "findById",
        "change": "Return type should be Promise<User | null> to handle not found"
      }
    ],
    "rationale": "Avoids throwing exceptions for normal control flow"
  }'

# Builder-1 accepts modification
respond_to_message "builder-1" "$response_file" \
  '{
    "status": "accepted",
    "updated_interface": {
      "interface": "IUserService",
      "methods": [
        {"name": "findById", "params": ["id: string"], "returns": "Promise<User | null>"},
        {"name": "create", "params": ["data: CreateUserDto"], "returns": "Promise<User>"}
      ]
    }
  }'

# Update shared context with agreed interface
update_shared_context "api-contracts" "builder-1" \
  "### IUserService Interface (AGREED)
\`\`\`typescript
interface IUserService {
  findById(id: string): Promise<User | null>;
  create(data: CreateUserDto): Promise<User>;
}
\`\`\`
**Agreed by**: builder-1, builder-2
**Date**: 2025-11-29
"
```

**Expected Output:**
```
Conversation Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Conversation ID: conv_auth_contracts_001
Participants: builder-1, builder-2
Messages: 3
Duration: 8 minutes
Status: ✅ RESOLVED

Outcome:
- IUserService interface defined
- Method signature modified (findById returns nullable)
- Agreement documented in shared context
- Both agents ready to implement
```

**Rationale**: Demonstrates collaborative contract negotiation with proposal, feedback, and agreement

### Example 2: Architectural Decision Broadcast
**Context**: Architect makes decision affecting all agents

**Execution Flow:**

```bash
# Architect broadcasts decision
broadcast_message "architect-1" "decision_announcement" \
  "JWT Algorithm Decision: RS256" \
  '{
    "decision_id": "DEC-001",
    "decision": "Use RS256 algorithm for JWT signing",
    "rationale": [
      "Better security than HS256",
      "Supports key rotation",
      "Industry best practice for production systems"
    ],
    "impact": {
      "affected_components": ["jwt-service", "auth-middleware", "token-validator"],
      "breaking_change": false,
      "action_required": "All JWT implementations must use RS256 keypair"
    },
    "effective_date": "immediate",
    "references": [
      "https://tools.ietf.org/html/rfc7519",
      "docs/security/jwt-best-practices.md"
    ]
  }'

# All agents receive and acknowledge
for agent in builder-1 builder-2 validator-1; do
  # Agents check inbox
  unread=$(check_inbox "$agent")

  # Agents read decision
  read_message "$agent" "$unread"

  # Agents acknowledge
  send_message "$agent" "architect-1" "acknowledgment" \
    "Acknowledged decision DEC-001" \
    '{"decision_id": "DEC-001", "will_comply": true}'
done

# Update shared context
update_shared_context "architecture-decisions" "architect-1" \
  "## DEC-001: JWT Algorithm Selection

**Decision**: Use RS256 algorithm for JWT signing
**Date**: 2025-11-29
**Status**: APPROVED

**Rationale**:
- Better security than HS256
- Supports key rotation
- Industry best practice

**Impact**: All JWT services must use RS256 keypair
**Acknowledgments**: builder-1 ✅, builder-2 ✅, validator-1 ✅
"
```

**Expected Output:**
```
Broadcast Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision: DEC-001 (JWT Algorithm: RS256)
Broadcast at: 2025-11-29T14:30:52Z
Recipients: 3 agents

Acknowledgments:
✅ builder-1 (received: 14:31, acknowledged: 14:32)
✅ builder-2 (received: 14:31, acknowledged: 14:33)
✅ validator-1 (received: 14:31, acknowledged: 14:35)

Status: Fully acknowledged (3/3)
Shared context updated: architecture-decisions.md
```

**Rationale**: Shows broadcast pattern for architectural decisions with acknowledgment tracking

### Example 3: Blocker Escalation and Resolution
**Context**: Agent encounters blocker needing orchestrator intervention

**Execution Flow:**

```bash
# Builder-1 hits blocker
publish_event "BlockerEncountered" "builder-1" \
  '{
    "task_id": "pg2-task-1",
    "blocker_type": "missing_dependency",
    "description": "Cannot implement JWT refresh without User model",
    "blocked_since": "2025-11-29T15:30:00Z",
    "dependency": {
      "required_artifact": "User model with refreshToken field",
      "responsible_agent": "builder-2",
      "estimated_impact": "2 hours blocked"
    }
  }'

# Orchestrator receives event (subscribed to BlockerEncountered)
# Checks builder-2 status
builder_2_status=$(jq -r '.status' "worktrees/builder-2/status/agent-status.json")

# Orchestrator facilitates communication
send_message "orchestrator" "builder-2" "priority_request" \
  "Builder-1 blocked waiting for User model" \
  '{
    "urgency": "high",
    "blocked_agent": "builder-1",
    "required_artifact": "User model with refreshToken field",
    "current_eta": "unknown",
    "requested_eta": "within 30 minutes"
  }'

# Builder-2 responds with ETA
respond_to_message "builder-2" "$message_file" \
  '{
    "status": "acknowledged",
    "current_progress": "User model 75% complete",
    "eta": "2025-11-29T16:15:00Z",
    "partial_delivery": "Can provide interface definition immediately"
  }'

# Builder-2 sends partial interface to unblock builder-1
send_message "builder-2" "builder-1" "interface_contract" \
  "Partial User interface (full implementation coming soon)" \
  '{
    "interface": "User",
    "fields": ["id", "email", "refreshToken"],
    "note": "Full implementation ETA 16:15, use this interface now"
  }'

# Builder-1 unblocked
publish_event "BlockerResolved" "builder-1" \
  '{
    "task_id": "pg2-task-1",
    "blocker_type": "missing_dependency",
    "resolution": "Partial interface received from builder-2",
    "blocked_duration": "25 minutes",
    "resolved_at": "2025-11-29T15:55:00Z"
  }'
```

**Expected Output:**
```
Blocker Resolution Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Blocker ID: blocker_pg2_task1_001
Reported by: builder-1
Blocker type: missing_dependency

Timeline:
15:30:00 - Blocker encountered
15:32:15 - Orchestrator notified
15:33:42 - builder-2 contacted
15:35:18 - builder-2 acknowledged
15:54:32 - Partial interface delivered
15:55:05 - Blocker resolved

Resolution time: 25 minutes
Impact: Minimal (partial unblocking achieved)
Status: ✅ RESOLVED
```

**Rationale**: Demonstrates blocker escalation, orchestrator mediation, and partial unblocking strategy

## Quality Standards

### Output Requirements
- All messages must conform to defined JSON schema with required fields
- Message delivery must be confirmed with status tracking
- Broadcast messages must reach all registered agents
- Shared context updates must be atomic (locked during update)
- Handoff packages must include complete artifacts and acceptance criteria

### Performance Requirements
- Message delivery latency: ≤1 second for direct messages
- Inbox polling frequency: Every 30 seconds during active work
- Shared context lock acquisition: ≤30 seconds wait time
- Broadcast delivery: ≤5 seconds to all agents
- Event processing: ≤2 seconds from publish to subscriber delivery

### Integration Requirements
- Integrates with parallel-executor-skill for agent coordination
- Uses worktree-manager-skill worktree paths for routing
- Reports communication metrics to orchestrator dashboards
- Supports MULTI_AGENT_PLAN.md handoff protocols

## Common Pitfalls

### Pitfall 1: Message Loss from Unreliable Delivery
**Issue**: Messages sent but never received by agent
**Why it happens**: File system errors, permissions issues, process crashes
**Solution**:
- Implement message acknowledgment requirement
- Retry unacknowledged messages after timeout
- Log all sent messages to audit trail
- Implement dead letter queue for failed deliveries

### Pitfall 2: Race Conditions in Shared Context Updates
**Issue**: Concurrent updates overwriting each other
**Why it happens**: Multiple agents updating context simultaneously without locking
**Solution**:
- Always acquire lock before updating shared context
- Implement timeout for lock acquisition
- Use optimistic locking with version numbers
- Consider event sourcing for append-only updates

### Pitfall 3: Conversation Fragmentation
**Issue**: Related messages not grouped, hard to follow conversation
**Why it happens**: Missing conversation_id tracking
**Solution**:
- Always use conversation_id for related messages
- Link responses to original message with in_reply_to
- Implement conversation view in message reader
- Provide conversation summary tools

### Pitfall 4: Broadcast Spam
**Issue**: Too many broadcast messages, agents overwhelmed
**Why it happens**: Every minor update broadcast to all agents
**Solution**:
- Reserve broadcasts for critical decisions only
- Use event subscriptions for opt-in notifications
- Implement message priority and filtering
- Batch related updates into single broadcast

### Pitfall 5: Stale Shared Context
**Issue**: Agents reading outdated shared context
**Why it happens**: Context updated but agents don't refresh
**Solution**:
- Broadcast context_updated event when context changes
- Agents should re-read context when event received
- Display last_updated timestamp prominently
- Implement cache invalidation in context readers

## Integration with Command & Control

### Related Agents
- **Orchestrator Agent**: Subscribes to all events, mediates conflicts, facilitates communication
- **Worker Agents**: Send/receive messages, update shared context, participate in handoffs

### Related Commands
- `/handoff`: Uses agent-communication for handoff documentation
- `/start-session`: Initializes message bus for session
- `/close-session`: Archives message history

### Related Skills
- **parallel-executor-skill**: Uses messaging for agent coordination (dependency)
- **multi-agent-planner-skill**: Defines communication protocols in plan
- **worktree-manager-skill**: Provides agent locations for routing

### MCP Dependencies
- **Filesystem MCP**: Message file creation, inbox polling
- **Process MCP**: Background message polling processes

### Orchestration Notes
- **Invoked by**: parallel-executor-skill (enable coordination), orchestrator agent
- **Invokes**: None (leaf skill)
- **Used throughout**: All multi-agent workflows

## Troubleshooting

### Issue: Messages Not Being Delivered
**Symptoms**: Agent sends message but recipient never receives
**Diagnosis**:
```bash
# Check if message file created
ls -la .agent-messages/inbox/recipient-agent/

# Check message file permissions
ls -l .agent-messages/inbox/recipient-agent/*.json

# Check registry
jq '.agents["recipient-agent"]' .agent-messages/registry.json
```
**Solution**:
1. Verify recipient agent registered
2. Check file permissions (should be readable)
3. Verify inbox directory exists
4. Check message file format (must be valid JSON)

### Issue: Shared Context Lock Timeout
**Symptoms**: Cannot acquire lock on shared context after 30 seconds
**Diagnosis**:
```bash
# Check lock status
jq . .agent-messages/shared-context/api-contracts.md.lock

# Check who holds lock
jq -r '.locked_by' .agent-messages/shared-context/api-contracts.md.lock
```
**Solution**:
```bash
# If locked by crashed agent, manually release
jq '.locked = false | .locked_by = null | .locked_at = null' \
  .agent-messages/shared-context/api-contracts.md.lock > temp.json
mv temp.json .agent-messages/shared-context/api-contracts.md.lock
```

### Issue: Event Subscriptions Not Working
**Symptoms**: Agent subscribed to event but not receiving notifications
**Diagnosis**:
```bash
# Check subscriptions
jq '.event_subscriptions' .agent-messages/registry.json

# Check event directory
ls -la .agent-messages/events/TaskCompleted/
```
**Solution**:
1. Verify agent subscribed to correct event type
2. Check event publishing actually creates files
3. Verify event delivery copies to agent inbox
4. Re-subscribe agent to event

## Version History
- 1.0.0 (2025-11-29): Initial release
  - Inter-agent messaging with multiple protocols
  - Shared context management with locking
  - Event broadcasting and subscriptions
  - Handoff documentation automation
  - Message persistence and archival
  - Conversation threading and tracking
  - Integration with orchestration ecosystem
