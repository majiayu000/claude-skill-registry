---
name: n8n-vigil-workflow
description: Expert guidance for n8n workflow development in Vigil Guard v2.0.0. Use when working with the 24-node 3-branch parallel detection pipeline, arbiter decision logic, unified_config.json management, dual-language PII detection, or workflow troubleshooting.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# n8n Vigil Guard Workflow Development (v2.0.0)

## Overview

Comprehensive guidance for developing and maintaining the Vigil Guard n8n workflow engine - a **24-node 3-branch parallel detection pipeline** with weighted arbiter fusion, dual-language PII detection (Polish + English), and ClickHouse logging.

## v2.0.0 Architecture Overview

### 3-Branch Parallel Detection System

```
Input → Extract → Validate → Config Load
         ↓
    3-Branch Executor (PARALLEL):
    ├─ Branch A: Heuristics (:5005) - 30% weight
    │            - Aho-Corasick prefilter (993 keywords)
    │            - Obfuscation detector
    │            - Structure analyzer
    │            - Whisper detector
    │            - Entropy analyzer
    │
    ├─ Branch B: Semantic (:5006) - 35% weight
    │            - MiniLM-L6-v2 embeddings (384-dim)
    │            - ClickHouse vector search
    │            - Cosine similarity scoring
    │
    └─ Branch C: LLM Guard (:8000) - 35% weight
                 - Meta Llama Prompt Guard 2
                 - ML-based attack detection
         ↓
    Arbiter v2 (weighted fusion)
         ↓
    Decision → PII Redaction → ClickHouse Log → Output
```

### 24 Workflow Nodes (v2.0.0)

```
1. When chat message received    # Chat trigger
2. Webhook v2                    # HTTP webhook trigger
3. Extract Input                 # Normalize input format
4. Load allowlist.schema.json    # Load allowlist config
5. Load pii.conf                 # Load PII patterns (361 lines)
6. Load unified_config.json      # Load main config (303 lines, v5.0.0)
7. Extract allowlist             # Parse allowlist
8. Extract pii.conf              # Parse PII config
9. Extract unified_config        # Parse main config
10. Merge Config                 # Combine all configs
11. Config Loader v2             # Final config object
12. Input Validator v2           # Validate input (length, format)
13. Validation Check             # Route based on validation
14. 3-Branch Executor            # PARALLEL branch execution
15. Arbiter v2                   # Weighted score fusion
16. Arbiter Decision             # Route based on score
17. PII_Redactor_v2              # Dual-language PII detection
18. Block Response v2            # Generate block response
19. Merge Final                  # Merge all paths
20. Build NDJSON v2              # Format for logging
21. Log to ClickHouse v2         # Send to analytics DB
22. Clean Output v2              # User-facing result
23. Early Block v2               # Fast-path for validation failures
24. output to plugin             # Browser extension response
```

## When to Use This Skill

- Understanding 3-branch parallel detection architecture
- Configuring arbiter weights (A: 30%, B: 35%, C: 35%)
- Modifying decision thresholds (ALLOW/SANITIZE/BLOCK)
- Configuring PII detection (Presidio dual-language mode)
- Troubleshooting workflow nodes or branch failures
- Understanding scoring algorithms and fusion logic
- Working with unified_config.json (NEVER modify directly!)
- Testing detection via n8n chat interface

## Critical Constraints

### Configuration Files

**NEVER modify files in `services/workflow/config/` directly**

| File | Lines | Version | Purpose |
|------|-------|---------|---------|
| unified_config.json | 303 | v5.0.0 | Main configuration |
| pii.conf | 361 | - | PII detection patterns |
| allowlist.schema.json | - | - | Allowlist structure |

**REMOVED:** `rules.config.json` (829 lines) - merged into unified_config.json

**ALWAYS use the Web GUI** at http://localhost/ui/config/
- Configuration changes tracked with audit logs
- ETag concurrency control prevents conflicts
- Backup rotation maintains version history

### n8n Workflow Import - CRITICAL KNOWLEDGE

**When user says "I imported the workflow", BELIEVE THEM:**
- n8n import from JSON **DOES** update ALL node code
- If behavior doesn't match expectations, problem is NOT the import
- Look for bugs in CODE LOGIC, not import process

**FORBIDDEN:**
```
"The workflow might not be imported correctly"
"Try deleting and re-importing the workflow"
"n8n doesn't update node code on import"
```

**CORRECT APPROACH:**
```
User imported → workflow code IS updated
Debug actual execution flow
Test components in isolation (services directly)
Check branch timing and degraded states
```

## Detection Architecture

### Branch Weight Configuration

| Branch | Service | Port | Weight | Timeout |
|--------|---------|------|--------|---------|
| A | Heuristics | 5005 | 30% | 1000ms |
| B | Semantic | 5006 | 35% | 2000ms |
| C | LLM Guard | 8000 | 35% | 3000ms |

### Arbiter v2 Decision Logic

```javascript
// Weighted score calculation
const weights = { A: 0.30, B: 0.35, C: 0.35 };
const finalScore =
  (branchA.score * weights.A) +
  (branchB.score * weights.B) +
  (branchC.score * weights.C);

// Critical signal escalation
if (branchA.critical_signals?.obfuscation_heavy ||
    branchC.critical_signals?.llm_attack) {
  // Force BLOCK regardless of score
}
```

### Decision Matrix

| Score Range | Action | Severity |
|------------|--------|----------|
| 0-29 | ALLOW | Clean |
| 30-64 | SANITIZE_LIGHT | Low |
| 65-84 | SANITIZE_HEAVY | Medium |
| 85-100 | BLOCK | Critical |

### Unified Contract v2.1 (Branch Response)

Each branch returns:
```json
{
  "branch_id": "A",
  "name": "heuristics",
  "score": 45,
  "threat_level": "MEDIUM",
  "confidence": 0.85,
  "critical_signals": {
    "obfuscation_heavy": false,
    "structure_anomaly": true
  },
  "features": { ... },
  "explanations": ["Pattern detected: ..."],
  "timing_ms": 45,
  "degraded": false
}
```

## Service Endpoints

### Heuristics Service (Branch A)

```bash
# Health check
curl http://localhost:5005/health

# Analyze text
curl -X POST http://localhost:5005/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test input", "request_id": "123"}'
```

**Features:**
- Aho-Corasick prefilter (993 keywords, 77% single-category hits)
- 4 specialized detectors: obfuscation, structure, whisper, entropy
- Internal normalization (leet speak, unicode, encoding)

### Semantic Service (Branch B)

```bash
# Health check
curl http://localhost:5006/health

# Analyze text
curl -X POST http://localhost:5006/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test input", "request_id": "123"}'
```

**Features:**
- MiniLM-L6-v2 model (384-dimensional embeddings)
- ClickHouse vector storage and similarity search
- Cosine similarity scoring against known attack patterns

### LLM Guard (Branch C)

```bash
# Health check
curl http://localhost:8000/health

# Detect attack
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "test input"}'
```

**Features:**
- Meta Llama Prompt Guard 2 model
- ML-based attack classification
- Binary is_attack decision with confidence

## Common Tasks

### Add Detection Pattern

**With v2.0.0, patterns are managed in:**
1. **Heuristics Service** - `services/heuristics-service/patterns/`
2. **Semantic Service** - Vector embeddings in ClickHouse
3. **unified_config.json** - Category configurations

**TDD Approach:**
```bash
cd services/workflow

# 1. Create test fixture
cat > tests/fixtures/my-attack.json << 'EOF'
{
  "prompt": "malicious payload here",
  "expected": "BLOCKED"
}
EOF

# 2. Run test (should FAIL)
npm test -- vigil-detection.test.js

# 3. Add pattern to heuristics service or config

# 4. Re-run test (should PASS)
npm test
```

### Test Detection Flow

```bash
# Option 1: n8n Chat Interface
# 1. Open http://localhost:5678
# 2. Open "Vigil Guard v2.0.0" workflow
# 3. Click "Test workflow" → "Chat" tab
# 4. Send test prompts
# 5. Review branch scores in response

# Option 2: Direct Webhook
curl -X POST http://localhost:5678/webhook/vigil-guard \
  -H "Content-Type: application/json" \
  -d '{"chatInput": "test payload"}'
```

### Debug Branch Failures

```bash
# Check branch health
curl http://localhost:5005/health  # Heuristics
curl http://localhost:5006/health  # Semantic
curl http://localhost:8000/health  # LLM Guard

# Check n8n logs for branch timing
docker logs vigil-n8n 2>&1 | grep "3-Branch"

# Query ClickHouse for branch results
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT
    branch_a_score,
    branch_b_score,
    branch_c_score,
    final_status
  FROM n8n_logs.events_processed
  ORDER BY timestamp DESC
  LIMIT 10
"
```

## Dual-Language PII Detection

### Architecture (v2.0.0)

```
1. Language_Detector → Hybrid detection (entity hints + statistical)
2. PII_Redactor_v2 → Dual Presidio calls (parallel)
   - Polish model: PERSON, PL_PESEL, PL_NIP, PL_REGON, EMAIL
   - English model: EMAIL, PHONE_NUMBER, CREDIT_CARD, IP_ADDRESS, etc.
3. Entity Deduplication → Merge overlapping entities
4. Masking/Anonymization → Final sanitized output
```

### Configuration (unified_config.json)

```json
{
  "pii_detection": {
    "presidio_enabled": true,
    "language": "auto",
    "dual_language_mode": true,
    "score_threshold": 0.7,
    "entities_polish": ["PERSON", "PL_PESEL", "PL_NIP", "PL_REGON", "EMAIL"],
    "entities_international": ["EMAIL", "PHONE_NUMBER", "CREDIT_CARD", "IP_ADDRESS"]
  }
}
```

### Test PII Detection

```bash
# Test Presidio directly
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "PESEL: 12345678901", "language": "pl", "entities": ["PL_PESEL"]}'

# Test language detector
curl -X POST http://localhost:5002/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Nazywam się Jan Kowalski", "detailed": true}'
```

## ClickHouse Logging

### New Columns (v2.0.0)

```sql
-- Branch scores
branch_a_score Float32,    -- Heuristics
branch_b_score Float32,    -- Semantic
branch_c_score Float32,    -- LLM Guard

-- Arbiter decision
arbiter_decision String,   -- ALLOW/SANITIZE/BLOCK
arbiter_confidence Float32,

-- Timing breakdown
branch_a_timing_ms UInt32,
branch_b_timing_ms UInt32,
branch_c_timing_ms UInt32,
total_timing_ms UInt32
```

### Query Examples

```sql
-- Branch performance analysis
SELECT
  arbiter_decision,
  avg(branch_a_score) as avg_heuristics,
  avg(branch_b_score) as avg_semantic,
  avg(branch_c_score) as avg_llm_guard,
  avg(total_timing_ms) as avg_total_ms
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 DAY
GROUP BY arbiter_decision;

-- Degraded branch detection
SELECT
  count() as total,
  countIf(branch_a_timing_ms > 1000) as a_timeout,
  countIf(branch_b_timing_ms > 2000) as b_timeout,
  countIf(branch_c_timing_ms > 3000) as c_timeout
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 1 HOUR;
```

## Troubleshooting

### Branch Not Responding

```bash
# 1. Check service health
docker ps | grep -E "(heuristics|semantic|prompt-guard)"

# 2. Check service logs
docker logs vigil-heuristics-service 2>&1 | tail -50
docker logs vigil-semantic-service 2>&1 | tail -50
docker logs vigil-prompt-guard-api 2>&1 | tail -50

# 3. Test connectivity from n8n container
docker exec vigil-n8n curl -s http://heuristics-service:5005/health
docker exec vigil-n8n curl -s http://semantic-service:5006/health
docker exec vigil-n8n curl -s http://prompt-guard-api:8000/health
```

### Unexpected Decision

```bash
# 1. Get detailed response with decision process
curl -X POST http://localhost:5678/webhook/vigil-guard \
  -H "Content-Type: application/json" \
  -d '{"chatInput": "test", "return_decision_process": true}'

# 2. Check arbiter logic
# Response includes:
# - branch_results.A/B/C with individual scores
# - arbiter_decision with weighted calculation
# - critical_signals that may override scoring

# 3. Query ClickHouse for historical patterns
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT original_input, final_status, branch_a_score, branch_b_score, branch_c_score
  FROM n8n_logs.events_processed
  WHERE original_input LIKE '%test%'
  ORDER BY timestamp DESC
  LIMIT 5
"
```

### PII Not Detected

```bash
# 1. Check Presidio health
curl http://localhost:5001/health

# 2. Check language detector
curl http://localhost:5002/health

# 3. Test with explicit language
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test@example.com", "language": "en", "entities": ["EMAIL"]}'

# 4. Check pii.conf patterns
cat services/workflow/config/pii.conf | jq '.patterns'
```

## Best Practices

1. **Understand branch weights** - A:30%, B:35%, C:35%
2. **Monitor degraded states** - Branches fail gracefully with score=0
3. **Use critical signals** - Override scoring for definite threats
4. **Test all 3 branches** - Don't assume one branch is enough
5. **Check timing** - Branch timeouts indicate service issues
6. **Config via Web UI** - Never edit unified_config.json directly
7. **Document pattern rationale** - Git commits explain why

## Related Skills

- `vigil-testing-e2e` - For writing comprehensive tests
- `clickhouse-grafana-monitoring` - For analyzing branch metrics
- `docker-vigil-orchestration` - For service management (11 containers)
- `presidio-pii-specialist` - For PII detection configuration

## References

- Workflow JSON: `services/workflow/workflows/Vigil Guard v2.0.0.json`
- Config: `services/workflow/config/unified_config.json` (303 lines, v5.0.0)
- PII Config: `services/workflow/config/pii.conf` (361 lines)
- Heuristics Service: `services/heuristics-service/`
- Semantic Service: `services/semantic-service/`

## Version History

- **v2.0.0** (Current): 3-Branch Parallel Detection, Arbiter v2, 24 nodes
- **v1.8.1**: Hybrid language detection (entity-based hints + statistical)
- **v1.6.11**: Dual-language PII (parallel Presidio calls)
- **v1.6.0**: Microsoft Presidio integration
- **v1.5.0**: MEDICAL_MISUSE category
- **v1.4.0**: Enhanced SQL_XSS_ATTACKS
