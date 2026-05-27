---
name: dgx-health
description: Check DGX Spark health, Milvus status, and vector search performance. Use to monitor infrastructure.
allowed-tools: Bash(curl:*), Bash(ssh:*), WebFetch, Read
---

# DGX Spark Health Check

Monitor DGX Spark infrastructure and Milvus vector database health.

## Health Checks

### 1. Milvus API Health
Check Milvus endpoint via Cloudflare Tunnel:

```bash
curl -s -o /dev/null -w "%{http_code}" https://dgx-milvus.pentatonic.com/v1/vector/collections
```

Expected: 200

### 2. Collection Status
Verify products_v2 collection is accessible:

```bash
curl -s https://dgx-milvus.pentatonic.com/v1/vector/collections/products_v2 | jq '.data.rowCount'
```

### 3. Search Latency Test
Run a test query to measure response time:

```bash
time curl -s -X POST https://dgx-milvus.pentatonic.com/v1/vector/search \
  -H "Content-Type: application/json" \
  -d '{"collectionName": "products_v2", "limit": 5}'
```

Target: < 100ms

### 4. DGX SSH Connectivity (if SSH MCP available)
Test SSH connection to DGX Spark:

```bash
ssh -o ConnectTimeout=5 dgx-spark.pentatonic.com "echo 'SSH OK'"
```

### 5. GPU Status (via SSH)
Check NVIDIA GPU status:

```bash
ssh dgx-spark.pentatonic.com "nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv"
```

### 6. Milvus Container Status (via SSH)
```bash
ssh dgx-spark.pentatonic.com "docker ps | grep milvus"
```

## Report Format

```markdown
## DGX Spark Health Report

### Connectivity
- Milvus API: [OK/FAIL]
- SSH: [OK/FAIL]
- Cloudflare Tunnel: [OK/FAIL]

### Vector Database
- Collection: products_v2
- Row Count: [X]
- Search Latency: [X]ms

### GPU Status
| GPU | Memory Used | Memory Total | Utilization |
|-----|-------------|--------------|-------------|
| ... | ...         | ...          | ...         |

### Recommendations
- [Any issues or optimizations]
```
