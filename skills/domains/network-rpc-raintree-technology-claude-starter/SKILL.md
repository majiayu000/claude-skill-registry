---
name: shelby-network-rpc
description: Expert on Shelby Protocol network infrastructure, RPC servers, storage providers, Cavalier implementation, tile architecture, performance optimization, connection management, and DoubleZero private network. Triggers on keywords Shelby RPC, storage provider, Cavalier, tile architecture, private network, DoubleZero, network performance, RPC endpoint, request hedging, connection pooling.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Shelby Network & RPC Expert

## Purpose

Expert guidance on Shelby Protocol's network infrastructure, RPC server architecture, storage provider implementation (Cavalier), performance optimization, and the DoubleZero private fiber network.

## When to Use

Auto-invoke when users ask about:
- **RPC Servers** - RPC architecture, endpoints, HTTP APIs, performance
- **Storage Providers** - Cavalier implementation, tile architecture, disk I/O
- **Network** - DoubleZero fiber network, private network, connectivity
- **Performance** - Request hedging, connection pooling, streaming, optimization
- **Operations** - Deployment, monitoring, scaling, troubleshooting
- **Infrastructure** - Network topology, system components, coordination

## Knowledge Base

Network and infrastructure documentation:
```
.claude/skills/blockchain/aptos/docs/
```

Key files:
- `protocol_architecture_rpcs.md` - RPC server architecture
- `protocol_architecture_storage-providers.md` - Storage provider implementation
- `protocol_architecture_overview.md` - System topology
- `protocol_architecture_networks.md` - Network configuration
- `apis_rpc_*.md` - RPC API specifications

## Network Topology

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│           Users (Public Internet)               │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS
                   ↓
┌─────────────────────────────────────────────────┐
│              Shelby RPC Servers                 │
│  - Public internet connectivity                 │
│  - Private network connectivity                 │
│  - HTTP REST APIs                               │
│  - Payment & session management                 │
└──────────┬──────────────────────────────────────┘
           │ DoubleZero Private Fiber Network
           ↓
┌─────────────────────────────────────────────────┐
│         Storage Provider Servers (16/PG)        │
│  - Cavalier implementation (C, high-perf)       │
│  - Tile architecture                            │
│  - Direct disk I/O                              │
│  - Private network only                         │
└──────────┬──────────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────────────┐
│           Aptos L1 Blockchain                   │
│  - Smart contracts                              │
│  - State coordination                           │
│  - All participants have access                 │
└─────────────────────────────────────────────────┘
```

### DoubleZero Private Network

**Purpose:**
- Dedicated fiber network for internal communication
- Connects RPC servers to storage providers
- Avoids public internet limitations

**Benefits:**
- **Predictable Performance** - No public internet congestion
- **Low Latency** - Direct fiber connections
- **High Bandwidth** - Dedicated capacity
- **Security** - Isolated from public networks
- **Reliability** - Controlled infrastructure

**Use Cases:**
- Chunk retrieval during reads
- Chunk distribution during writes
- Storage provider health checks
- Internal coordination

## RPC Server Architecture

### Core Responsibilities

**User-Facing Layer:**
1. **HTTP REST APIs** - Blob read/write operations
2. **Session Management** - User sessions and authentication
3. **Payment Handling** - Micropayment channels, cost calculation
4. **Error Handling** - User-friendly error responses

**Backend Coordination:**
1. **Erasure Coding** - Encode/decode chunks during write/read
2. **Commitment Calculations** - Verify chunk integrity
3. **Blockchain Integration** - Query/update Aptos L1 state
4. **Storage Provider Management** - Connection pooling, health monitoring

### HTTP Endpoints

**Read Operations:**
```
GET /v1/blobs/{account}/{blob_name}
  - Fetch entire blob
  - Supports HTTP range requests
  - Returns blob data with appropriate content-type

Range Request:
  GET /v1/blobs/{account}/{blob_name}
  Headers: Range: bytes=0-1023

Response:
  206 Partial Content
  Content-Range: bytes 0-1023/100000
  [blob data]
```

**Write Operations:**
```
PUT /v1/blobs/{account}/{blob_name}
  - Upload entire blob
  - Requires session/payment authorization

Multipart Upload:
  POST /v1/multipart-uploads/start
  POST /v1/multipart-uploads/{id}/part
  POST /v1/multipart-uploads/{id}/complete
```

**Session Management:**
```
POST /v1/sessions/create
  - Create payment session
  - Returns session token

POST /v1/sessions/{id}/micropayment-channel
  - Create micropayment channel for efficient reads
```

### Read Path Workflow

**User Request → RPC Response:**

1. **Receive Request**
```
Client → GET /v1/blobs/0x123.../video.mp4
      → RPC validates session/payment
```

2. **Cache Check** (Optional Fast Path)
```
RPC → Check local cache
    → If hit: Return cached data (fast!)
    → If miss: Continue to step 3
```

3. **Query Placement Group**
```
RPC → Read smart contract or indexer
    → Identify blob's placement group
    → Get list of 16 storage providers
```

4. **Request Chunks** (Private Network)
```
RPC → Request chunks from storage providers
    → Via DoubleZero private network
    → Need 10 of 16 chunks for reconstruction
    → Parallel requests for low latency
```

5. **Validate & Reconstruct**
```
RPC → Validate chunks against commitments
    → Decode erasure coding
    → Reassemble original blob data
    → Handle byte range if requested
```

6. **Return to Client**
```
RPC → Stream data to client
    → Charge micropayment
    → Update session balance
```

**Graceful Degradation:**
- If some storage providers unavailable (up to 6)
- Automatically use parity chunks
- Reconstruct data from available chunks
- Transparent to end user

### Write Path Workflow

**SDK Upload → RPC Coordination:**

1. **Receive Upload**
```
Client SDK → Sends non-erasure-coded data to RPC
           → Conserves client bandwidth
           → Includes blob metadata and commitments
```

2. **Verify Commitments**
```
RPC → Independently performs erasure coding
    → Recomputes chunk commitments
    → Validates against on-chain metadata
    → Ensures consistency
```

3. **Distribute Chunks** (Private Network)
```
RPC → Get placement group from blockchain
    → Send each of 16 chunks to assigned storage providers
    → Via DoubleZero private network
    → Parallel distribution
```

4. **Collect Acknowledgments**
```
RPC → Storage providers validate chunks
    → Return signed acknowledgments
    → RPC aggregates acknowledgments
```

5. **Finalize on Blockchain**
```
RPC → Submit aggregated acknowledgments to smart contract
    → Smart contract transitions blob to "written"
    → Blob now available for reads
```

### Performance Optimizations

#### 1. Streaming Data Pipeline

**Zero-Copy Architecture:**
```
Client Upload → RPC receives stream
             → Erasure code on-the-fly
             → Stream to storage providers
             → No large buffers needed
```

**Benefits:**
- Reduced time-to-first-byte
- Constant memory usage per connection
- Supports high concurrency
- No latency bubbles

**Implementation Pattern:**
```
Data arrives → Process immediately (don't wait for complete upload)
            → Transform in small chunks
            → Forward to next stage
            → Minimize buffering
```

#### 2. Connection Pooling

**Storage Provider Connections:**
```
RPC maintains connection pool:
  - Pre-established TCP connections
  - Reused across many requests
  - Request tracking mechanism
  - Keep flow control state fresh
```

**Benefits:**
- No connection establishment latency
- No TCP slow-start penalty
- Higher throughput
- Lower overhead

#### 3. Request Hedging (Future)

**Tail Latency Optimization:**
```
Need 10 of 16 chunks:
  - Request 14 chunks (over-request)
  - Use first 10 valid responses
  - Cancel remaining requests
  - Reduces p99 latency
```

**Requirements:**
- Careful network congestion management
- Traffic prioritization
- Cancellation support

#### 4. Resource Management

**Bounded Queues:**
```
Connection pools: Fixed capacity → Prevent memory exhaustion
Processing queues: Size limits → Protect during traffic spikes
```

**Backpressure:**
```
Storage provider congested → Apply backpressure up chain
Network congested         → Slow down data ingestion
                          → Don't buffer unlimited data
```

**Automatic Cleanup:**
```
Sessions: Expire after timeout
Pending uploads: Clean up stale operations
Cached metadata: TTL-based eviction
```

### Scalability

**Horizontal Scaling:**

RPC servers are mostly stateless:
- Session management requires some database state
- All other operations are stateless
- Easy to add more RPC instances
- Load balance across instances

**Session State Management:**
```
Local persistent database (current implementation):
  - SQLite or similar
  - Stores active sessions
  - Persists across restarts

Can migrate to distributed database if needed:
  - Redis cluster
  - PostgreSQL
  - Maintains scalability
```

**Deployment Pattern:**
```
Load Balancer
    ↓
┌────────────────┬────────────────┬────────────────┐
│  RPC Server 1  │  RPC Server 2  │  RPC Server N  │
└────────────────┴────────────────┴────────────────┘
```

## Storage Provider Architecture (Cavalier)

### Implementation Overview

**Cavalier:** Jump Crypto's reference implementation
- High-performance C codebase
- Leverages [Firedancer](https://github.com/firedancer-io/firedancer) utilities
- Tile-based architecture
- Designed for maximum performance

### Tile Architecture

**Philosophy:**
Modern CPUs have many cores, but multi-threaded apps struggle with:
- Cache coherency overhead
- NUMA penalties
- Unpredictable performance
- Synchronization costs

**Solution: Tiles**
- Isolated processes on dedicated CPU cores
- Communicate via shared memory
- No locks, no cache contention
- Explicit, predictable performance

**Tile Model Principles:**
```
Explicit Communication:
  - Moving data between cores is explicit
  - No performance surprises

Resource Locality:
  - Tile controls its core's caches
  - Dedicated core scheduling
  - No interference from other processes

Isolation:
  - Tile state is isolated
  - Security-sensitive tiles can be sandboxed
  - Protected state
```

**Similar To:**
- Erlang actors
- Go goroutines + channels
- Seastar (shared-nothing with message passing)

### Workspaces

**Shared Memory Management:**
```
Workspace:
  - Section of shared memory
  - Backed by huge pages (TLB efficiency)
  - CPU topology aware
  - Holds application state, queues, buffers

Benefits:
  - Efficient inter-tile communication
  - Persistent state across restarts
  - Debugging-friendly layout
  - Dynamic memory allocators within workspace
```

### Cavalier Tile Types

**1. System Tile**
```
Role: General orchestration
  - Metrics reporting
  - Status checking
  - Coordination
  - Health monitoring
```

**2. Server Tile(s)**
```
Role: Manage RPC communication
  - Single-threaded epoll event loop
  - Multiple concurrent TCP connections
  - Protocol: Lightweight protobuf-based
  - Buffers: Dedicated per connection
  - Backpressure management

Scalability:
  - Add more server tiles as RPC connections grow
  - Each tile handles subset of connections
```

**3. Engine Tile**
```
Role: Physical storage operations
  - Uses io_uring (async I/O)
  - Separate read/write queues per drive
  - Direct I/O (bypasses page cache)
  - Predictable performance

Drive Management:
  - Minimal partition tables
  - Fixed-depth queues per drive
  - Fine-tuned concurrency control
  - Characteristics-based tuning

Request Flow:
  Server tile → Engine tile (shared memory queue)
              → io_uring to drives
              → Completion → Response to server tile
```

**4. Aptos Client Tile**
```
Role: Blockchain state access
  - HTTP requests to Aptos Indexer (libcurl)
  - Maintains local database of blobs/chunks
  - Responds to metadata queries from other tiles
  - Manages chunk expiration and deletion

Database:
  - Blobs this storage provider is responsible for
  - Chunk assignments
  - Expiration times
  - Local cache of L1 state

Cleanup:
  - Notifies engine tile of expired chunks
  - Frees disk space
```

### Tile Communication

```
┌──────────────┐   Shared Memory    ┌──────────────┐
│ Server Tile  │ ←─────Queue───────→ │ Engine Tile  │
└──────────────┘                     └──────────────┘
       ↓                                     ↓
 Shared Memory                          Direct I/O
    Queue                              to Physical
       ↓                                  Drives
┌──────────────┐
│ Aptos Client │
│    Tile      │
└──────────────┘
```

### Performance Characteristics

**Why Tiles Are Fast:**
- No locks, no cache bouncing
- Explicit CPU affinity
- Shared memory (no syscalls for communication)
- Direct I/O (no kernel page cache overhead)
- Dedicated cores (no context switching)

**Scalability:**
```
More RPC connections → Add server tiles
Larger metadata → Shard across Aptos client tiles
More drives → Engine tile handles multiple drives efficiently
```

## Monitoring & Observability

### Distributed Tracing

**Correlation IDs:**
```
Request arrives → Generate unique correlation ID
                → Flows through all components:
                  - RPC server
                  - Storage providers
                  - Blockchain interactions
                → Enables end-to-end tracing
```

**Use Cases:**
- Debug performance issues
- Understand system behavior under load
- Track failed requests
- Analyze tail latency

### Key Metrics

**RPC Server Metrics:**
```
Request Metrics:
  - Request latency (p50, p95, p99)
  - Throughput (requests/sec)
  - Error rates by type
  - Success rate

Storage Provider Metrics:
  - Connection health
  - Chunk retrieval latency
  - Availability percentage
  - Failover events

System Metrics:
  - CPU usage
  - Memory usage
  - Network throughput
  - Cache hit rate

Cost Metrics:
  - ShelbyUSD payments
  - Gas costs
  - Bandwidth usage
```

**Storage Provider Metrics:**
```
Disk I/O:
  - IOPS (read/write)
  - Queue depths
  - Latency per drive
  - Throughput

Tile Metrics:
  - Queue backlogs
  - Processing rates
  - Inter-tile latency

Network:
  - Connection count
  - Data transferred
  - Error rates
```

### Monitoring Integration

**Standard Interfaces:**
```
Prometheus:
  - Metrics endpoint
  - Time-series data
  - Alerting integration

Distributed Tracing:
  - OpenTelemetry compatible
  - Jaeger/Zipkin integration
  - Span context propagation

Logging:
  - Structured JSON logs
  - Log levels (debug, info, warn, error)
  - Correlation ID in every log
```

## Operational Considerations

### RPC Server Operations

**Deployment:**
```
1. Configure network endpoints (public + private)
2. Set up session database
3. Configure storage provider connections
4. Set up monitoring and alerting
5. Configure load balancer
6. Deploy multiple instances for HA
```

**Monitoring:**
```
- Watch request latency (alert on p99 spikes)
- Monitor storage provider health
- Track error rates
- Alert on session database issues
- Monitor cache effectiveness
```

**Scaling:**
```
Horizontal: Add more RPC instances
Vertical: Increase resources per instance
Cache: Expand cache for popular content
Database: Shard session database if needed
```

### Storage Provider Operations

**Deployment:**
```
1. Provision hardware (NVMe drives, high CPU)
2. Configure huge pages for workspaces
3. Set CPU affinity for tiles
4. Configure private network connectivity
5. Register with smart contract
6. Join placement groups
```

**Monitoring:**
```
- Disk health and SMART metrics
- Tile queue depths
- Chunk validation success rate
- Audit performance
- Network connectivity to RPCs
```

**Maintenance:**
```
- Regular disk health checks
- Periodic integrity audits
- Software updates
- Data migration for failed drives
- Graceful exit from placement groups
```

## Performance Troubleshooting

### High Latency

**Diagnose:**
1. Check correlation IDs in traces
2. Identify bottleneck component
3. Analyze metrics for that component

**Common Causes:**
```
Storage Provider Issues:
  - Disk saturation (high queue depth)
  - Network congestion
  - Provider offline

RPC Server Issues:
  - Cache miss rate high
  - Connection pool exhausted
  - CPU saturation

Network Issues:
  - DoubleZero congestion
  - Packet loss
  - Routing issues
```

### Low Throughput

**Diagnose:**
```
Check:
  - RPC server CPU usage
  - Storage provider queue depths
  - Network utilization
  - Cache hit rate
```

**Solutions:**
```
Scale horizontally: Add more RPC instances
Optimize caching: Increase cache size, tune eviction
Connection tuning: Adjust pool sizes
Batch requests: Group operations where possible
```

## Process for Helping Users

### 1. Identify Topic

**Architecture Questions:**
- "How do RPC servers work?"
- "What is the tile architecture?"
- "How does the private network help?"

**Performance Questions:**
- "Why is my read slow?"
- "How can I optimize throughput?"
- "What is request hedging?"

**Operational Questions:**
- "How do I deploy an RPC server?"
- "How to monitor storage providers?"
- "How to scale the system?"

### 2. Search Documentation

```bash
# RPC architecture
Read docs/protocol_architecture_rpcs.md

# Storage providers
Read docs/protocol_architecture_storage-providers.md

# Network topology
Read docs/protocol_architecture_overview.md
```

### 3. Provide Answer

**Structure:**
1. **Explain component** - Architecture and purpose
2. **Show data flow** - How requests are processed
3. **Performance aspects** - Optimizations and trade-offs
4. **Operational guidance** - Deployment and monitoring
5. **Troubleshooting** - Common issues and solutions

### 4. Use Diagrams

Show network topology, data flows, and component interactions.

## Key Concepts to Reference

**Three-Tier Architecture:**
```
Users ← Public Internet → RPC Servers ← Private Network → Storage Providers
                              ↓
                        Aptos Blockchain
```

**Tile Model:**
```
Isolated processes + Dedicated cores + Shared memory = Predictable performance
```

**Performance Stack:**
```
Streaming pipeline + Connection pooling + Zero-copy + Direct I/O = High throughput
```

## Response Style

- **Technical** - Detailed architecture explanations
- **Performance-focused** - Emphasize optimizations
- **Operational** - Practical deployment guidance
- **Diagrammatic** - Use ASCII diagrams for clarity
- **Referenced** - Cite specific components and papers

## Example Interaction

```
User: "How does Shelby achieve low latency reads?"

Response:
1. Explain RPC caching layer (fast path)
2. Describe private fiber network (no internet congestion)
3. Detail parallel chunk retrieval (10 of 16, concurrent)
4. Discuss streaming pipeline (no buffering delays)
5. Mention connection pooling (no setup latency)
6. Reference: protocol_architecture_rpcs.md, Cavalier tile architecture
```

## Limitations

- Don't share proprietary Cavalier source code
- Reference documented architecture and patterns
- Acknowledge when details are implementation-specific
- Focus on conceptual understanding and documented behavior

## Follow-up Suggestions

- Performance tuning strategies
- Monitoring best practices
- Scaling considerations
- Firedancer project (for Cavalier deep dive)
- Distributed systems patterns
