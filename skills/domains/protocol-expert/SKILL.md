---
name: shelby-protocol-expert
description: Expert on Shelby Protocol architecture, erasure coding, placement groups, read/write procedures, Clay Codes, chunking, storage providers, RPC servers, and decentralized storage system design on Aptos blockchain. Triggers on keywords Shelby Protocol, erasure coding, Clay Codes, placement groups, Shelby architecture, storage provider, blob storage, chunking, Shelby whitepaper.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Shelby Protocol Expert

## Purpose

Provide expert guidance on Shelby Protocol's architecture, design principles, erasure coding mechanisms, data durability, read/write procedures, and system components for developers building on or integrating with the decentralized storage network.

## When to Use

Auto-invoke when users ask about:
- **Architecture** - Shelby system, protocol design, components, infrastructure
- **Data Engineering** - Erasure coding, Clay Codes, chunking, placement groups
- **Operations** - Read procedure, write procedure, blob operations, data flow
- **System Design** - Storage providers, RPC servers, smart contracts, auditing
- **Performance** - Bandwidth optimization, recovery algorithms, private network
- **Concepts** - Decentralized storage, blob naming, data durability, data integrity

## Knowledge Base

**Full access to Shelby Protocol documentation (when available):**
- **Location:** `docs/` (relative to this skill)
- Pull with: `docpull https://docs.shelby.cloud -o .claude/skills/aptos/shelby/docs` (when available)

**Note:** Documentation must be pulled separately. Skill works with built-in knowledge but benefits from comprehensive protocol docs.

Key documentation files (when pulled):
- `protocol.md` - Protocol introduction and key components
- `protocol_architecture_overview.md` - Comprehensive architecture
- `protocol_architecture_rpcs.md` - RPC server operations
- `protocol_architecture_storage-providers.md` - Storage provider mechanics
- `protocol_architecture_smart-contracts.md` - Smart contract layer
- `protocol_architecture_token-economics.md` - Economic model
- `protocol_architecture_networks.md` - Network topology
- `protocol_architecture_white-paper.md` - Academic foundation

## System Architecture

### Key Components

1. **Aptos Smart Contract**
   - Manages system state
   - Enforces Byzantine Fault Tolerance (BFT)
   - Handles correctness-critical operations
   - Performs data correctness audits
   - Manages economic logic and settlements

2. **Storage Provider (SP) Servers**
   - Store erasure-coded chunks of user data
   - Serve chunk data to RPC servers
   - Participate in auditing system
   - Receive micropayments for storage and bandwidth

3. **Shelby RPC Servers**
   - User-facing API endpoints
   - Handle blob upload/download requests
   - Perform erasure coding/decoding
   - Manage payment channels
   - Cache frequently accessed data
   - Coordinate with Storage Providers

4. **Private Network (DoubleZero Fiber)**
   - Dedicated fiber network for internal communication
   - Connects RPC servers to Storage Providers
   - Ensures consistent high performance
   - Avoids public internet limitations

### Network Topology

```
User (Public Internet)
  ↓
Shelby RPC Server (Public + Private Network)
  ↓ (Private Fiber Network)
Storage Provider Servers (16 per placement group)
  ↓
Aptos L1 Blockchain (accessible by all)
```

## Data Model

### Accounts and Blob Naming

**Namespace:**
- User blobs stored in account-specific namespace
- Account = hex representation of Aptos address
- Format: `0x123.../user/defined/path/file.ext`

**Blob Names:**
- User-defined, unique within namespace
- Max length: 1024 characters
- Must NOT end with `/`
- No directory structure (flat namespace)

**Canonical Directory Layout:**
```
Input:
  .
  ├── bar
  └── foo
      ├── baz
      └── buzz

Uploaded as:
  <account>/<prefix>/bar
  <account>/<prefix>/foo/baz
  <account>/<prefix>/foo/buzz
```

**Important:** You can create both `<account>/foo` as a blob AND `<account>/foo/bar`, but this violates canonical structure.

### Chunking & Erasure Coding

**Chunkset Basics:**
- Blob data split into 10MB fixed-size chunksets
- Last chunkset zero-padded if needed (padding not returned on reads)
- Each chunkset erasure coded into 16 chunks

**Erasure Coding Scheme: Clay Codes**
- **Data chunks:** 10 chunks (original user data)
- **Parity chunks:** 6 chunks (error correction)
- **Total:** 16 chunks per chunkset
- **Recovery requirement:** Any 10 of 16 chunks can reconstruct data
- **Chunk size:** 1MB each

**Why Clay Codes?**
- Optimal storage footprint (same as Reed-Solomon)
- Bandwidth-optimized repair algorithm
- 4x less network traffic during recovery vs Reed-Solomon
- Efficient recovery without fetching 10 full chunks

**Recovery Methods:**
1. **Standard Recovery:** Fetch any 10 full chunks (10MB total)
2. **Optimized Recovery:** Read smaller portions from more servers (2.5MB total)

**Reference:** [Clay Codes Paper](https://www.usenix.org/system/files/conference/fast18/fast18-vajha.pdf)

### Placement Groups

**Purpose:**
- Efficiently manage chunk locations without massive metadata
- Control data locality and failure domains
- Reduce on-chain storage requirements

**How It Works:**
1. Blob randomly assigned to a placement group (load balancing)
2. All chunks of blob stored on same 16 storage providers
3. Each placement group = exactly 16 storage provider slots
4. Smart contract tracks placement group assignments, not individual chunks

**Benefits:**
- Minimal on-chain metadata
- Predictable chunk locations
- Simplified read/write coordination
- Flexible failure domain management

**Reference:** [Ceph RADOS Paper](https://ceph.com/assets/pdfs/weil-rados-pdsw07.pdf)

## Read Procedure

**Step-by-Step Process:**

1. **RPC Selection**
   - Client selects available RPC server from network

2. **Session Establishment**
   - Client creates payment mechanism with RPC server
   - Session established for subsequent requests

3. **Read Request**
   - Client sends HTTP request specifying blob or byte range
   - Includes payment authorization

4. **Cache Check (Optional)**
   - RPC server checks local cache
   - Returns cached data if present (fast path)

5. **Chunk Location Query**
   - RPC server queries smart contract
   - Identifies which storage providers hold chunks
   - Determines placement group for blob

6. **Chunk Retrieval**
   - RPC server fetches necessary chunks from storage providers
   - Uses private DoubleZero fiber network
   - Pays storage providers via micropayment channel
   - Only needs 10 of 16 chunks for reconstruction

7. **Data Validation & Assembly**
   - RPC server validates chunks against blob metadata
   - Reassembles requested data from chunks
   - Returns data to client

8. **Incremental Payment**
   - Client session payments deducted as data transferred
   - Client can perform additional reads using same session

## Write Procedure

**Step-by-Step Process:**

1. **RPC Selection**
   - Client selects available RPC server

2. **Local Erasure Coding**
   - SDK computes erasure coded chunks locally
   - Processes chunk-by-chunk to minimize memory
   - Calculates cryptographic commitments for each chunk

3. **Metadata Transaction**
   - SDK submits transaction to Aptos blockchain
   - Includes blob metadata and merkle root of chunk commitments
   - **Storage payment processed on-chain at this point**
   - Placement group assigned

4. **Data Transmission**
   - SDK sends original (non-erasure-coded) data to RPC
   - Conserves bandwidth (no need to send parity chunks)

5. **RPC Verification**
   - RPC server independently performs erasure coding
   - Recomputes chunk commitments
   - Validates computed values match on-chain metadata

6. **Chunk Distribution**
   - RPC server distributes 16 chunks to assigned storage providers
   - Based on blob's placement group
   - Uses private fiber network

7. **Storage Provider Acknowledgment**
   - Each storage provider validates received chunk
   - Returns signed acknowledgment to RPC

8. **Finalization Transaction**
   - RPC aggregates all storage provider acknowledgments
   - Submits final transaction to smart contract
   - Smart contract transitions blob to "written" state

9. **Blob Available**
   - Blob now durably stored and available for reads

## Token Economics

### Two-Token Model

**APT (Aptos Tokens):**
- Pay for blockchain gas fees
- Transaction costs on Aptos L1
- Required for smart contract interactions

**ShelbyUSD:**
- Pay for storage and bandwidth
- Storage provider compensation
- RPC server payments
- Micropayment channel funding

### Paid Reads Model

**Why paid reads?**
- Incentivizes storage providers to deliver good service
- Ensures high read performance and availability
- Aligns economic incentives with user needs
- Supports read-heavy workloads (video streaming, AI inference, analytics)

### Payment Mechanisms

**Micropayment Channels:**
- Efficient off-chain payment aggregation
- Reduces transaction costs
- Enables fast, frequent payments
- Settled periodically on-chain

**Storage Commitments:**
- Pre-paid during write operation
- Ensures data durability guarantees
- Based on blob size and expiration time

## Auditing System

**Purpose:**
- Ensure data integrity across network
- Verify storage providers maintain chunks correctly
- Reward honest participation
- Penalize malicious or negligent behavior

**How It Works:**
- Smart contract periodically audits storage providers
- Providers prove possession of chunks via cryptographic challenges
- Successful audits earn rewards
- Failed audits result in penalties

**Benefits:**
- Data correctness without trusted parties
- Economic incentives for honest behavior
- Decentralized verification

## Performance Characteristics

### High-Performance Design

**Dedicated Bandwidth:**
- DoubleZero private fiber network
- Avoids public internet congestion
- Consistent, predictable performance
- Low latency for internal operations

**Efficient Recovery:**
- Clay Code bandwidth optimization
- 4x less network traffic during repairs
- Faster recovery from node/disk failures
- Lower operational costs

**Optimized for Read-Heavy Workloads:**
- Video streaming
- AI training and inference
- Large-scale data analytics
- Content delivery

### Scalability

**Placement Groups:**
- Distributes load across storage providers
- Random assignment for load balancing
- Flexible capacity expansion

**Erasure Coding:**
- Minimizes storage overhead (1.6x vs 3x for triple replication)
- Efficient bandwidth usage
- Optimal storage footprint

## Why Aptos?

**High Transaction Throughput:**
- Supports frequent micropayments
- Fast finality times
- Scalable settlement layer

**Resource-Efficient Execution:**
- Low cost for storage commitments
- Efficient smart contract execution
- Move language safety guarantees

**Team Expertise:**
- Aptos team from Meta's large-scale platforms
- Experience with global distributed systems
- Perfect match for Shelby's requirements

## Why Jump Crypto?

**Engineering Foundation:**
- Built on Jump Trading Group's infrastructure experience
- High-performance storage and compute systems
- Expertise in:
  - High-performance I/O
  - Efficient concurrency
  - Low-level code optimizations
  - Distributed systems

## Use Cases

**Ideal Workloads:**
1. **Video Streaming** - High bandwidth reads, global distribution
2. **AI Training/Inference** - Large datasets, frequent access
3. **Data Analytics** - Big data processing, read-heavy patterns
4. **Content Delivery** - Static assets, global availability
5. **Archival Storage** - Long-term data retention, periodic access

**Key Requirements Met:**
- Robust storage with data durability guarantees
- Significant capacity (petabyte scale)
- High read bandwidth
- Reasonable pricing
- User control over data
- Censorship resistance

## Design Trade-offs

**Optimized For:**
- Read-heavy workloads
- Large blob storage (multi-MB to GB files)
- High bandwidth requirements
- Data durability

**Not Optimized For:**
- Frequent updates/modifications (blobs are immutable)
- Small file storage (overhead from 10MB chunksets)
- Low-latency random access to small portions
- Free/subsidized storage (user-pays model)

## Process for Helping Users

### 1. Identify Question Category

**Architecture Questions:**
- "How does Shelby work?"
- "What are the system components?"
- "How is data stored?"

**Technical Deep-Dive:**
- "Explain erasure coding in Shelby"
- "How do placement groups work?"
- "What happens during a read/write?"

**Design Decisions:**
- "Why Clay Codes?"
- "Why Aptos blockchain?"
- "Why paid reads?"

**Use Case Evaluation:**
- "Is Shelby good for X?"
- "How does Shelby compare to Y?"
- "What are the trade-offs?"

### 2. Search Documentation

```bash
# Architecture questions
Read docs/protocol_architecture_overview.md

# Erasure coding details
Grep "erasure|clay|chunking" docs/ --output-mode content

# Economic model
Read docs/protocol_architecture_token-economics.md

# Specific components
Read docs/protocol_architecture_rpcs.md
Read docs/protocol_architecture_storage-providers.md
```

### 3. Provide Comprehensive Answer

**Structure:**
1. **High-level explanation** - Core concept in simple terms
2. **Technical details** - Precise mechanics and algorithms
3. **Why it matters** - Benefits and trade-offs
4. **Practical implications** - How it affects users/developers
5. **References** - Link to specific documentation sections

### 4. Use Diagrams Where Helpful

**Data Flow:**
```
Client → RPC Server → Storage Providers (16)
         ↓
    Aptos Smart Contract
```

**Chunking:**
```
10MB Blob → Erasure Code → 16 Chunks (10 data + 6 parity)
                          → Distributed to Placement Group
```

## Key Concepts to Reference

**Data Durability:**
- Erasure coding provides fault tolerance
- Can lose up to 6 chunks per chunkset
- Storage provider diversity
- Auditing system ensures integrity

**Performance:**
- Private fiber network (DoubleZero)
- Clay Code bandwidth optimization
- RPC caching layer
- Parallel chunk retrieval

**Decentralization:**
- No single point of failure
- Aptos blockchain coordination
- Distributed storage providers
- Trustless auditing

**Economic Alignment:**
- Paid reads incentivize performance
- Storage commitments ensure durability
- Micropayment channels reduce friction
- Auditing rewards honest behavior

## Response Style

- **Educational** - Explain concepts clearly with context
- **Technical** - Provide accurate implementation details
- **Balanced** - Discuss both benefits and trade-offs
- **Referenced** - Cite papers and documentation
- **Practical** - Relate concepts to real-world usage

## Example Interaction

```
User: "How does Shelby ensure my data won't be lost?"

Response:
1. Explain erasure coding (10 data + 6 parity chunks)
2. Describe placement group distribution (16 storage providers)
3. Detail auditing system (cryptographic proofs)
4. Discuss economic incentives (rewards for honest storage)
5. Quantify durability (can lose 6 of 16 chunks)
6. Reference: Clay Codes paper, protocol_architecture_overview.md
```

## Limitations

- Only reference official Shelby Protocol documentation
- Acknowledge when documentation lacks detail
- Don't speculate on future features
- Cite academic papers when discussing algorithms
- Distinguish between protocol design and implementation details

## Follow-up Suggestions

After answering, suggest:
- Related architectural components to explore
- Practical SDK integration for concepts discussed
- Performance implications for use case
- Cost considerations
- Alternative approaches and trade-offs
