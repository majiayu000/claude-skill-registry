---
name: memory-test
description: Run E2E memory pipeline test — embed text, store in Qdrant, search and retrieve. Use to validate the memory system is working.
allowed-tools: Bash
---

# Memory Pipeline E2E Test

Run the full embed → store → search pipeline:

1. **Start port-forward** (if not already running):
   ```bash
   kubectl port-forward svc/qdrant -n vector 6333:6333 &
   sleep 2
   ```

2. **Generate embedding**:
   ```bash
   curl -s http://10.10.10.10:30001/v1/embeddings \
     -H "Content-Type: application/json" \
     -d '{"model":"default","input":"Kaizen memory pipeline test at '"$(date -Iseconds)"'"}'
   ```
   Verify: 4096 dimensions returned.

3. **Store in Qdrant**:
   Use the embedding from step 2 to upsert a point into the `episodic` collection with a random UUID and timestamp payload.

4. **Search**:
   Generate a new embedding for a related query and search the `episodic` collection. Verify score > 0.5.

5. **Report**:
   | Step | Status | Details |
   |------|--------|---------|
   | Embedding | ? | dims, latency |
   | Store | ? | collection, point ID |
   | Search | ? | score, matches |

6. **Cleanup port-forward**:
   ```bash
   kill %1 2>/dev/null
   ```
