---
name: atproto-ingest
description: Layer 1 - Data Acquisition for Bluesky/AT Protocol social graph and content.
metadata:
  trit: 0
---

# AT Protocol Data Ingestion

Layer 1 - Data Acquisition for Bluesky/AT Protocol social graph and content.

**GF(3) Trit: +1 (Generator)** — Produces data streams for downstream processing.

## Authentication

### App Password (Recommended for scripts)
```bash
# Create session
curl -X POST https://bsky.social/xrpc/com.atproto.server.createSession \
  -H "Content-Type: application/json" \
  -d '{"identifier": "handle.bsky.social", "password": "app-password-here"}'

# Response contains accessJwt and refreshJwt
export BSKY_TOKEN="eyJ..."
```

### OAuth (For apps)
```bash
# Authorization endpoint: https://bsky.social/oauth/authorize
# Token endpoint: https://bsky.social/oauth/token
# Scopes: atproto, transition:generic
```

## Capabilities

### 1. fetch-user-posts

Get all posts from a user by handle or DID.

```bash
# Resolve handle to DID
curl "https://bsky.social/xrpc/com.atproto.identity.resolveHandle?handle=user.bsky.social"

# Get author feed (paginated)
curl "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor=did:plc:xxx&limit=100&cursor=$CURSOR" \
  -H "Authorization: Bearer $BSKY_TOKEN"
```

**Pagination loop:**
```python
def fetch_all_posts(actor: str, token: str) -> list:
    posts, cursor = [], None
    while True:
        url = f"https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={actor}&limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        data = resp.json()
        posts.extend(data.get("feed", []))
        cursor = data.get("cursor")
        if not cursor:
            break
        time.sleep(0.5)  # Rate limit respect
    return posts
```

### 2. get-engagement-graph

Map likes, reposts, replies, and quotes for a post.

```bash
# Get likes
curl "https://bsky.social/xrpc/app.bsky.feed.getLikes?uri=at://did:plc:xxx/app.bsky.feed.post/yyy&limit=100" \
  -H "Authorization: Bearer $BSKY_TOKEN"

# Get reposts
curl "https://bsky.social/xrpc/app.bsky.feed.getRepostedBy?uri=at://did:plc:xxx/app.bsky.feed.post/yyy&limit=100" \
  -H "Authorization: Bearer $BSKY_TOKEN"

# Get quotes (search for post URI)
curl "https://bsky.social/xrpc/app.bsky.feed.getQuotes?uri=at://did:plc:xxx/app.bsky.feed.post/yyy&limit=100" \
  -H "Authorization: Bearer $BSKY_TOKEN"
```

**Engagement record schema:**
```sql
CREATE TABLE engagement (
    post_uri VARCHAR PRIMARY KEY,
    author_did VARCHAR,
    like_count INTEGER,
    repost_count INTEGER,
    reply_count INTEGER,
    quote_count INTEGER,
    likers VARCHAR[],      -- Array of DIDs
    reposters VARCHAR[],
    indexed_at TIMESTAMP
);
```

### 3. stream-mentions

Real-time monitoring via Firehose or polling.

```bash
# Firehose (WebSocket) - all network events
wscat -c wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos

# Polling fallback - notifications endpoint
curl "https://bsky.social/xrpc/app.bsky.notification.listNotifications?limit=50" \
  -H "Authorization: Bearer $BSKY_TOKEN"
```

**Firehose filter (Python):**
```python
import websocket
import cbor2

def on_message(ws, message):
    header, body = cbor2.loads(message)
    if header.get("op") == 1:  # Commit
        for op in body.get("ops", []):
            if "app.bsky.feed.post" in op.get("path", ""):
                record = op.get("record", {})
                # Check for mentions in facets
                for facet in record.get("facets", []):
                    for feature in facet.get("features", []):
                        if feature.get("$type") == "app.bsky.richtext.facet#mention":
                            if feature.get("did") == TARGET_DID:
                                yield record

ws = websocket.WebSocketApp("wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos",
                             on_message=on_message)
```

### 4. extract-thread-tree

Full conversation tree from a post.

```bash
curl "https://bsky.social/xrpc/app.bsky.feed.getPostThread?uri=at://did:plc:xxx/app.bsky.feed.post/yyy&depth=10&parentHeight=10" \
  -H "Authorization: Bearer $BSKY_TOKEN"
```

**Thread tree structure:**
```python
def extract_thread_tree(thread_data: dict) -> dict:
    """Flatten thread to adjacency list for DuckDB."""
    nodes = []
    edges = []
    
    def walk(node, parent_uri=None):
        post = node.get("post", {})
        uri = post.get("uri")
        nodes.append({
            "uri": uri,
            "author_did": post.get("author", {}).get("did"),
            "text": post.get("record", {}).get("text"),
            "created_at": post.get("record", {}).get("createdAt"),
            "depth": node.get("depth", 0)
        })
        if parent_uri:
            edges.append({"parent": parent_uri, "child": uri})
        for reply in node.get("replies", []):
            walk(reply, uri)
    
    walk(thread_data.get("thread", {}))
    return {"nodes": nodes, "edges": edges}
```

### 5. get-follower-network

First and second-order connections.

```bash
# Followers
curl "https://bsky.social/xrpc/app.bsky.graph.getFollowers?actor=did:plc:xxx&limit=100&cursor=$CURSOR" \
  -H "Authorization: Bearer $BSKY_TOKEN"

# Following
curl "https://bsky.social/xrpc/app.bsky.graph.getFollows?actor=did:plc:xxx&limit=100&cursor=$CURSOR" \
  -H "Authorization: Bearer $BSKY_TOKEN"
```

**Second-order expansion:**
```python
def get_follower_network(actor: str, depth: int = 2) -> dict:
    """BFS expansion of follower graph."""
    visited = set()
    edges = []
    queue = [(actor, 0)]
    
    while queue:
        current, d = queue.pop(0)
        if current in visited or d > depth:
            continue
        visited.add(current)
        
        followers = paginate_all("app.bsky.graph.getFollowers", actor=current)
        for f in followers:
            did = f["did"]
            edges.append({"from": did, "to": current, "type": "follows"})
            if d < depth:
                queue.append((did, d + 1))
    
    return {"nodes": list(visited), "edges": edges}
```

## Rate Limiting

| Endpoint Category | Rate Limit | Window |
|-------------------|------------|--------|
| Read (feed, graph) | 3000/5min | Rolling |
| Write (post, like) | 1500/hr | Rolling |
| Firehose | Unlimited | - |
| Search | 100/min | Rolling |

**Backoff strategy:**
```python
def rate_limited_request(url, headers, max_retries=5):
    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue
        return resp
    raise Exception("Rate limit exceeded")
```

## DuckDB Ingestion Format

```sql
-- Posts table
CREATE TABLE bsky_posts (
    uri VARCHAR PRIMARY KEY,
    cid VARCHAR,
    author_did VARCHAR,
    text TEXT,
    created_at TIMESTAMP,
    reply_parent VARCHAR,
    reply_root VARCHAR,
    embed_type VARCHAR,
    langs VARCHAR[],
    labels VARCHAR[],
    ingested_at TIMESTAMP DEFAULT now()
);

-- Social graph
CREATE TABLE bsky_graph (
    subject_did VARCHAR,
    object_did VARCHAR,
    relation VARCHAR,  -- 'follows', 'blocks', 'mutes'
    created_at TIMESTAMP,
    PRIMARY KEY (subject_did, object_did, relation)
);

-- Engagement events
CREATE TABLE bsky_engagement (
    uri VARCHAR,
    actor_did VARCHAR,
    action VARCHAR,  -- 'like', 'repost', 'quote', 'reply'
    target_uri VARCHAR,
    created_at TIMESTAMP,
    PRIMARY KEY (uri)
);

-- Insert from JSON
COPY bsky_posts FROM 'posts.json' (FORMAT JSON, ARRAY true);
```

## AT Protocol Lexicon Reference

| Lexicon | Purpose |
|---------|---------|
| `app.bsky.feed.getAuthorFeed` | User's posts |
| `app.bsky.feed.getPostThread` | Thread tree |
| `app.bsky.feed.getLikes` | Who liked |
| `app.bsky.feed.getRepostedBy` | Who reposted |
| `app.bsky.graph.getFollowers` | Follower list |
| `app.bsky.graph.getFollows` | Following list |
| `app.bsky.actor.getProfile` | User profile |
| `com.atproto.sync.subscribeRepos` | Firehose |

## Integration with Layer 2

Output feeds into:
- **GF(3) Trit 0 (Transformer)**: Sentiment analysis, embedding generation
- **GF(3) Trit -1 (Consumer)**: Dashboard display, alert triggers

```python
# Pipeline handoff
posts = fetch_all_posts(actor, token)
duckdb.execute("INSERT INTO bsky_posts SELECT * FROM read_json(?)", [posts])
# Signal next layer
publish_event("bsky.ingestion.complete", {"actor": actor, "count": len(posts)})
```
