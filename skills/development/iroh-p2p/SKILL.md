---
name: iroh-p2p
description: Build modern peer-to-peer applications with Iroh. QUIC-based P2P networking, hole punching, content distribution, and decentralized data synchronization.
version: 1.0.0
---


# Iroh P2P Development

Build decentralized, peer-to-peer applications with **Iroh** — a modern Rust P2P library based on QUIC with automatic hole punching, relay fallback, and content distribution.

## What is Iroh?

Iroh is a **nextgen P2P library** that implements:
- 🔗 **Direct P2P connections** via QUIC (UDP-based, faster than TCP)
- 🔄 **Automatic hole punching** (NAT traversal without complexity)
- 📡 **Relay fallback** (works even behind restrictive firewalls)
- 📦 **Content distribution** (iroh-blobs for KB-TB transfers)
- 📝 **Document sync** (iroh-docs for collaborative state)
- 💬 **Gossip protocol** (iroh-gossip for message broadcasting)

**Iroh represents data sovereignty**: users control their own nodes, direct connections replace central servers, and data stays decentralized.

---

## Quick Start Project

### 1. Initialize Iroh Project

```bash
cargo new my_p2p_app
cd my_p2p_app

# Add dependencies
cargo add iroh@0.13
cargo add tokio --features full
cargo add anyhow
cargo add tracing tracing-subscriber
```

### 2. Create a Basic P2P Node

```rust
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    // Spawn an Iroh node with all services
    let node = iroh::node::Builder::default()
        .spawn()
        .await?;

    println!("✅ P2P node started!");
    println!("  📦 Blobs:  Available");
    println!("  📝 Docs:   Available");
    println!("  💬 Gossip: Available");

    // Keep running
    println!("\n⏳ Running... (Ctrl+C to stop)");
    tokio::signal::ctrl_c().await?;
    println!("👋 Shutting down...");

    Ok(())
}
```

### 3. Build and Run

```bash
cargo build --release
./target/release/my_p2p_app
```

---

## Core Concepts

### Node Identity

Every Iroh node has a **node ID** (public key) that other peers can connect to:

```rust
// Access node ID through services
let node_id = node.blobs.node_id().await?;
println!("My node ID: {}", node_id);

// Share this with other peers to establish connections
```

### Services

Iroh provides modular services you can use independently:

#### 📦 iroh-bytes (Content Distribution)

Transfer files/blobs between peers (KB to TB):

```rust
// Publish a blob
let hash = node.blobs.add_bytes(b"Hello, P2P!").await?;

// Access via peer's node ID
let peer_id = "..."; // from other peer
let content = node.blobs.get_bytes(hash).await?;
```

#### 📝 iroh-docs (Document Sync)

Sync structured data between peers with conflict-free resolution:

```rust
// Create a document (CRDT-based)
let doc = node.docs.create().await?;

// Write data
doc.set_bytes(b"key", b"value").await?;

// Other peers auto-sync
```

#### 💬 iroh-gossip (Message Broadcasting)

Broadcast messages across a P2P network (publish/subscribe):

```rust
// Subscribe to a topic
let topic = "alerts".as_bytes();
let mut sub = node.gossip.subscribe(topic.clone()).await?;

// Publish a message
node.gossip.publish(topic.clone(), b"New alert!").await?;

// Receive messages
while let Ok(msg) = sub.next().await {
    println!("Received: {}", String::from_utf8_lossy(&msg));
}
```

---

## Architecture Patterns

### Pattern 1: Direct Peer Connections

Connect to a peer by their node ID:

```rust
// Dial a peer directly
let peer_id = "..."; // node ID of another peer
let connection = node.net.connect(peer_id).await?;

// Use connection for RPC, streaming, etc.
```

### Pattern 2: Distributed Content Discovery

Use Iroh's DHT (Distributed Hash Table) for peer discovery:

```rust
// Announce your content
let hash = node.blobs.add_bytes(data).await?;

// Other peers query DHT to find providers
// Iroh handles this automatically
```

### Pattern 3: Relay Fallback

When direct connections fail (firewall), Iroh falls back to relays:

```rust
// Configured automatically - no code needed
// If direct connection fails → relay takes over
// User experiences seamless P2P
```

---

## Real-World Patterns

### 1. File Sync Between Two Peers

```rust
// Peer A: Share a file
let path = "/path/to/file.txt";
let bytes = std::fs::read(path)?;
let hash = node.blobs.add_bytes(&bytes).await?;
println!("Share this hash: {}", hash);

// Peer B: Receive the file
let hash = "..."; // from Peer A
let bytes = node.blobs.get_bytes(hash).await?;
std::fs::write("/path/to/downloaded.txt", bytes)?;
```

### 2. Live Collaboration (Docs + Gossip)

```rust
// Create shared document
let doc = node.docs.create().await?;

// Publish document ID via gossip
let doc_id = doc.id().to_string();
node.gossip.publish(b"shared_docs", doc_id.as_bytes()).await?;

// All peers subscribe and sync the doc
// Concurrent edits merge automatically (CRDT)
```

### 3. Distributed Cache

```rust
// Cache data in blobs, announce via gossip
let cache_entry = serde_json::to_vec(&data)?;
let hash = node.blobs.add_bytes(&cache_entry).await?;

// Broadcast availability
node.gossip.publish(b"cache_updates", hash.as_ref()).await?;

// Peers can fetch via hash
```

---

## Deployment Considerations

### 1. NAT/Firewall Handling

Iroh handles NAT traversal automatically:

```rust
// Your node automatically:
// ✓ Detects if behind NAT (via STUN)
// ✓ Attempts hole punching
// ✓ Falls back to relays if needed
// → No manual configuration required
```

### 2. Persistent Storage

Choose a storage backend:

```rust
// In-memory (default, for testing)
let node = iroh::node::Builder::default()
    .spawn()
    .await?;

// Persistent storage (recommended)
let node = iroh::node::Builder::default()
    .data_dir("/path/to/data")
    .spawn()
    .await?;
```

### 3. Relay Servers

Use public relays (can self-host):

```rust
// Iroh provides public relays
// Or run your own relay:
// https://github.com/n0-computer/iroh/tree/main/iroh-relay
```

---

## Security

### 1. Encryption by Default

All Iroh connections use TLS 1.3 with perfect forward secrecy:

```rust
// No extra code needed - automatic
```

### 2. Peer Authentication

Peers are identified by their **node ID** (public key):

```rust
// Only trust specific peer IDs
let trusted_peer = "...";
if connection.peer_id() == trusted_peer {
    // Process message
}
```

### 3. Access Control

Implement application-level authorization:

```rust
// Docs can have per-key permissions
doc.set_bytes_with_author(
    author_key,
    key,
    value,
).await?;
```

---

## Performance Tuning

### 1. QUIC Configuration

```rust
// Iroh uses Quinn (QUIC implementation)
// Sensible defaults for most use cases
// Customize if needed:
// - Connection timeout
// - Max streams
// - MTU size
```

### 2. Batch Operations

```rust
// Efficient blob operations
let hashes = futures::stream::iter(data)
    .then(|item| async move {
        node.blobs.add_bytes(&item).await
    })
    .collect::<Vec<_>>()
    .await;
```

### 3. Content Addressing

```rust
// Use content hashes for deduplication
// Same content = same hash → no duplication
let hash1 = node.blobs.add_bytes(b"data").await?;
let hash2 = node.blobs.add_bytes(b"data").await?;
assert_eq!(hash1, hash2); // Same content address
```

---

## Testing

### Local Network Testing

```bash
# Run multiple nodes locally for testing

# Terminal 1
RUST_LOG=debug cargo run -- --bind 127.0.0.1:0

# Terminal 2
RUST_LOG=debug cargo run -- --bind 127.0.0.1:0

# Nodes discover and connect automatically via DHT
```

### Integration Testing

```rust
#[tokio::test]
async fn test_p2p_transfer() {
    let node_a = iroh::node::Builder::default().spawn().await.unwrap();
    let node_b = iroh::node::Builder::default().spawn().await.unwrap();

    // Transfer data between nodes
    let data = b"test data";
    let hash = node_a.blobs.add_bytes(data).await.unwrap();

    let retrieved = node_b.blobs.get_bytes(hash).await.unwrap();
    assert_eq!(retrieved, data);
}
```

---

## Common Patterns & Best Practices

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Blob Transfer** | File sync, backups | Share files without server |
| **Doc Sync** | Collaborative editing | Real-time document updates |
| **Gossip** | Notifications, feeds | Broadcast events to all peers |
| **Hybrid** | Complex apps | Combine all three services |

### Best Practices

1. **Always handle errors gracefully** — Network is unreliable
2. **Use persistent storage** — Don't lose data between restarts
3. **Implement exponential backoff** — For retries
4. **Test with firewalls** — Ensure relay fallback works
5. **Monitor bandwidth** — P2P apps can use significant resources
6. **Secure peer IDs** — Verify before trusting

---

## Troubleshooting

### "Failed to dial peer"

Usually means relay fallback is needed:

```rust
// Iroh handles this automatically
// Check logs: RUST_LOG=debug
// If persistent, peer may be offline
```

### High Latency

Could be relay usage (slower than direct):

```bash
# Check direct connection vs relay
RUST_LOG=iroh_net=debug
# Look for "direct" vs "relay" in logs
```

### Storage Growing

Blobs are content-addressed and immutable:

```rust
// Remove old blobs manually if needed
node.blobs.remove(hash).await?;
```

---

## Resources

- **[Iroh Docs](https://www.iroh.computer/)** — Official documentation
- **[GitHub](https://github.com/n0-computer/iroh)** — Source code & examples
- **[QUIC Spec](https://datatracker.ietf.org/doc/html/rfc9000)** — Protocol details
- **[Rust Async](https://tokio.rs/)** — Tokio async runtime guide

---

## Examples in This Repo

- `iroh-basics/` — Simple node initialization
- `iroh-blobs/` — Content distribution patterns
- `iroh-docs/` — Document sync example
- `iroh-gossip/` — Broadcasting example
- `iroh-full-app/` — Complete app with all services

---

## Data Sovereignty

Iroh enables **true data sovereignty**:

- ✅ **You own your node** — No registration required
- ✅ **Direct connections** — No central server
- ✅ **End-to-end encrypted** — Even peers see encrypted data
- ✅ **Offline capable** — Local-first with eventual sync
- ✅ **Portable** — Move your node anywhere

This is the foundation of nextgen protocols: decentralized, user-controlled infrastructure.




## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `distributed-systems`: 3 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.