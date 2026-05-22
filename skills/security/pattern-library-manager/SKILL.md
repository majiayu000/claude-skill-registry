---
name: pattern-library-manager
description: Expert management of detection patterns in Vigil Guard v2.0.0. Use for heuristics-service pattern files (18 JSON files), unified_config.json categories, ReDoS protection, scoring algorithms, and pattern optimization.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Pattern Library Manager (v2.0.0)

## Overview

Expert management of detection patterns across the Vigil Guard v2.0.0 3-branch parallel detection architecture. Patterns are now distributed across multiple components.

## v2.0.0 Architecture Change

### REMOVED: rules.config.json

**OLD (v1.x):** Single 829-line rules.config.json with 34 categories
**NEW (v2.0.0):** Distributed pattern system:

| Component | Location | Purpose |
|-----------|----------|---------|
| Heuristics Service | `services/heuristics-service/patterns/` | 18 JSON pattern files |
| Unified Config | `services/workflow/config/unified_config.json` | Category configs (303 lines) |
| PII Config | `services/workflow/config/pii.conf` | PII patterns (361 lines) |
| Semantic Service | ClickHouse vectors | Embedding similarity |

## When to Use This Skill

- Managing detection patterns in heuristics-service (18 JSON files)
- Configuring category weights in unified_config.json
- Validating regex patterns for ReDoS vulnerabilities
- Understanding 3-branch scoring algorithms
- Tracking false positive rates per category
- Analyzing pattern effectiveness metrics
- Optimizing pattern performance

## Pattern File Locations (v2.0.0)

### Heuristics Service Patterns (18 files)

```
services/heuristics-service/patterns/
├── boundary-patterns.json          # System boundary markers
├── divider-patterns.json           # Text divider patterns
├── divider-patterns-manual.json    # Manual divider rules
├── emoji-mappings.json             # Emoji obfuscation maps
├── extraction-summary.json         # Data extraction patterns
├── homoglyphs.json                 # Unicode lookalike characters
├── injection-patterns.json         # Injection attack patterns
├── leet-speak.json                 # Leet speak mappings
├── multi-char-sequences.json       # Multi-character substitutions
├── narrative-patterns.json         # Narrative injection patterns
├── roleplay-patterns.json          # Roleplay attack patterns
├── roleplay-patterns-manual.json   # Manual roleplay rules
├── security-keywords.json          # Security-related keywords
├── social-engineering-patterns.json # Social engineering markers
├── system-markers.json             # System prompt markers
├── whisper-patterns.json           # Whisper attack patterns
├── whisper-patterns-manual.json    # Manual whisper rules
└── zero-width.json                 # Zero-width character detection
```

### Heuristics Service Config

```
services/heuristics-service/config/default.json
```

**Detector weights:**
```json
{
  "detection": {
    "weights": {
      "obfuscation": 0.25,
      "structure": 0.20,
      "whisper": 0.25,
      "entropy": 0.15,
      "security": 0.15
    },
    "thresholds": {
      "low_max": 30,
      "medium_max": 65
    }
  }
}
```

### Unified Config (v5.0.0, 303 lines)

```
services/workflow/config/unified_config.json
```

**Category configuration (merged from old rules.config.json):**
```json
{
  "detection": {
    "categories": {
      "SQL_XSS_ATTACKS": { "enabled": true, "weight": 50 },
      "JAILBREAK_ATTEMPT": { "enabled": true, "weight": 80 },
      "PROMPT_LEAK": { "enabled": true, "weight": 70 }
    }
  }
}
```

## Configuration Editing Guidelines

### Web UI Editable (via http://localhost/ui/config/)

- Decision thresholds (ALLOW_MAX, SANITIZE thresholds)
- Category enable/disable toggles
- Performance settings
- PII detection settings

### Direct Code Edit (TDD workflow required)

1. **Heuristics pattern files** - `services/heuristics-service/patterns/*.json`
2. **Detector configurations** - `services/heuristics-service/config/default.json`
3. **PII regex fallbacks** - `services/workflow/config/pii.conf`
4. **Leet speak mappings** - `services/heuristics-service/patterns/leet-speak.json`
5. **Homoglyph mappings** - `services/heuristics-service/patterns/homoglyphs.json`

**Reason:** Complex structures requiring TDD workflow and security validation.

## Pattern Addition Workflow (v2.0.0)

### Adding Heuristics Pattern

```bash
cd services/workflow

# 1. Create test first
cat > tests/fixtures/my-attack.json << 'EOF'
{
  "prompt": "malicious payload here",
  "expected": "BLOCKED"
}
EOF

# 2. Run test (should FAIL)
npm test -- vigil-detection.test.js

# 3. Edit appropriate pattern file
# For injection attacks:
vim services/heuristics-service/patterns/injection-patterns.json

# For whisper attacks:
vim services/heuristics-service/patterns/whisper-patterns.json

# 4. Restart heuristics service
docker-compose restart heuristics-service

# 5. Re-run test (should PASS)
npm test

# 6. Commit together
git add tests/ services/heuristics-service/
git commit -m "feat(detect): add <category> pattern with TDD tests"
```

### Adding Semantic Pattern

Semantic patterns are vector embeddings stored in ClickHouse:

```bash
# 1. Add attack example to embedding corpus
echo '{"text": "attack example", "category": "INJECTION", "is_attack": true}' >> \
  services/semantic-service/corpus/attacks.jsonl

# 2. Re-index embeddings
docker-compose exec semantic-service python reindex.py

# 3. Verify with test
npm test -- vigil-detection.test.js
```

## 3-Branch Scoring Architecture

### Branch Weights

| Branch | Weight | Service | Port |
|--------|--------|---------|------|
| A (Heuristics) | 30% | heuristics-service | 5005 |
| B (Semantic) | 35% | semantic-service | 5006 |
| C (LLM Guard) | 35% | prompt-guard-api | 8000 |

### Final Score Calculation

```javascript
// Arbiter v2 weighted fusion
const weights = { A: 0.30, B: 0.35, C: 0.35 };
const finalScore =
  (branchA.score * weights.A) +
  (branchB.score * weights.B) +
  (branchC.score * weights.C);

// Critical signal override
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

## Heuristics Detectors (Branch A)

### 1. Obfuscation Detector (25% weight)

**Detects:**
- Zero-width characters (patterns/zero-width.json)
- Homoglyphs (patterns/homoglyphs.json)
- Base64/Hex encoding
- Mixed script attacks
- Leet speak (patterns/leet-speak.json)

### 2. Structure Detector (20% weight)

**Detects:**
- Code fence abuse
- Boundary patterns (patterns/boundary-patterns.json)
- Newline manipulation
- Segment variance anomalies

### 3. Whisper Detector (25% weight)

**Detects:**
- Whisper patterns (patterns/whisper-patterns.json)
- Divider patterns (patterns/divider-patterns.json)
- Roleplay attacks (patterns/roleplay-patterns.json)
- Question repetition

### 4. Entropy Detector (15% weight)

**Detects:**
- High Shannon entropy
- Bigram anomalies
- Character class diversity
- Language detection anomalies

### 5. Security Detector (15% weight)

**Detects:**
- SQL injection patterns (patterns/injection-patterns.json)
- XSS patterns
- Command injection
- Privilege escalation

## ReDoS Validation

### Dangerous Patterns (AVOID)

```regex
❌ ^(a+)+$              # Catastrophic backtracking
❌ (x+x+)+y            # Nested quantifiers
❌ (a|a)*b             # Overlapping alternation
❌ (.*){10,}           # Excessive repetition
```

### Safe Alternatives

```regex
✅ ^a+$                # Simple quantifier
✅ ^[a-z]{1,100}$      # Bounded repetition
✅ ^(?:ab)+$           # Non-capturing group
✅ ^a*b                # Greedy but safe
```

### Validation Script

```bash
#!/bin/bash
# Test pattern for ReDoS vulnerability

PATTERN="$1"

for size in 10 100 1000 10000; do
  INPUT=$(printf 'a%.0s' $(seq 1 $size))

  START=$(date +%s%N)
  echo "$INPUT" | timeout 1s grep -P "$PATTERN" > /dev/null
  EXIT_CODE=$?
  END=$(date +%s%N)

  DURATION=$(((END - START) / 1000000))

  if [ $EXIT_CODE -eq 124 ]; then
    echo "❌ REDOS DETECTED: Timeout at size $size"
    exit 1
  fi

  echo "✅ Size $size: ${DURATION}ms"
done

echo "✅ Pattern is safe"
```

## Pattern Effectiveness Analysis

### ClickHouse Queries

```sql
-- Branch performance comparison
SELECT
  arbiter_decision,
  avg(branch_a_score) as avg_heuristics,
  avg(branch_b_score) as avg_semantic,
  avg(branch_c_score) as avg_llm_guard,
  count() as total
FROM n8n_logs.events_processed
WHERE timestamp > now() - INTERVAL 7 DAY
GROUP BY arbiter_decision;

-- Detection rate by branch
SELECT
  CASE
    WHEN branch_a_score > branch_b_score AND branch_a_score > branch_c_score THEN 'Heuristics'
    WHEN branch_b_score > branch_c_score THEN 'Semantic'
    ELSE 'LLM Guard'
  END as primary_detector,
  count() as detections
FROM n8n_logs.events_processed
WHERE arbiter_decision != 'ALLOW'
  AND timestamp > now() - INTERVAL 7 DAY
GROUP BY primary_detector;

-- False positive analysis
SELECT
  original_input,
  branch_a_score,
  branch_b_score,
  branch_c_score,
  arbiter_decision
FROM n8n_logs.events_processed
WHERE arbiter_decision = 'BLOCK'
  AND timestamp > now() - INTERVAL 1 DAY
ORDER BY timestamp DESC
LIMIT 20;
```

## Troubleshooting

### Pattern Not Triggering

```bash
# 1. Test heuristics service directly
curl -X POST http://localhost:5005/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test payload", "request_id": "debug-123"}'

# 2. Check service logs
docker logs vigil-heuristics-service 2>&1 | tail -50

# 3. Verify pattern file is loaded
docker exec vigil-heuristics-service cat /app/patterns/injection-patterns.json | jq .

# 4. Test pattern with grep
echo "test payload" | grep -P "your_pattern"
```

### Branch Degraded

```bash
# Check branch health
curl http://localhost:5005/health  # Heuristics
curl http://localhost:5006/health  # Semantic
curl http://localhost:8000/health  # LLM Guard

# Check timing in ClickHouse
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT
    avg(branch_a_timing_ms) as avg_a,
    avg(branch_b_timing_ms) as avg_b,
    avg(branch_c_timing_ms) as avg_c
  FROM n8n_logs.events_processed
  WHERE timestamp > now() - INTERVAL 1 HOUR
"
```

### False Positives

**Solutions:**
1. Reduce detector weight in `heuristics-service/config/default.json`
2. Add context requirements to pattern
3. Add to allowlist in unified_config.json
4. Adjust threshold in arbiter configuration

## Metrics & KPIs

```yaml
quality_metrics:
  redos_vulnerabilities: 0 (zero tolerance)
  false_positive_rate: <5% per branch
  detection_effectiveness: >80%
  branch_latency: <1000ms (A), <2000ms (B), <3000ms (C)

coverage_metrics:
  pattern_files: 18 JSON files
  heuristics_detectors: 5 (obfuscation, structure, whisper, entropy, security)
  semantic_embeddings: ClickHouse vectors
  llm_guard_model: Meta Llama Prompt Guard 2
```

## Related Skills

- `n8n-vigil-workflow` - For workflow architecture and arbiter logic
- `vigil-testing-e2e` - For writing comprehensive tests
- `clickhouse-grafana-monitoring` - For analyzing branch metrics
- `docker-vigil-orchestration` - For service management

## References

- Heuristics patterns: `services/heuristics-service/patterns/` (18 files)
- Heuristics config: `services/heuristics-service/config/default.json`
- Unified config: `services/workflow/config/unified_config.json` (303 lines, v5.0.0)
- PII config: `services/workflow/config/pii.conf` (361 lines)
- Workflow: `services/workflow/workflows/Vigil Guard v2.0.0.json`

## Version History

- **v2.0.0** (Current): Distributed patterns, 3-branch architecture, Aho-Corasick prefilter
- **v1.6.11**: Single rules.config.json (829 lines, 34 categories) - DEPRECATED
- **v1.5.0**: Added MEDICAL_MISUSE category
- **v1.4.0**: Enhanced SQL_XSS_ATTACKS
