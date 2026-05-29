---
name: language-detection-expert
description: Hybrid language detection algorithm for Vigil Guard v2.0.0. Use for language-detector Flask API, entity-based hints, Polish PESEL/NIP detection, 3-branch pipeline integration, accuracy troubleshooting, and langdetect integration.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Language Detection Expert (v2.0.0)

## Overview

Hybrid language detection algorithm for Vigil Guard v2.0.0 combining entity-based hints (Polish PESEL/NIP detection) with statistical analysis (langdetect library) for accurate dual-language PII processing and 3-branch detection pipeline integration.

## When to Use This Skill

- Managing language-detector Flask API (services/language-detector/)
- Implementing hybrid detection logic
- Troubleshooting detection accuracy (<10ms target)
- Working with langdetect library
- Polish entity recognition patterns
- 3-branch pipeline integration (v2.0.0)

## Tech Stack

- Python 3.11, Flask 3.0.0
- langdetect 1.0.9 (statistical analysis)
- Custom Polish entity patterns (PESEL, NIP, REGON)

## v2.0.0 Architecture Integration

### Position in 3-Branch Pipeline

```yaml
n8n Workflow (24 nodes):
  1. Input Validation
  2. Language Detection ← This Service
  3. 3-Branch Executor (parallel):
     - Branch A: Heuristics (uses language for keyword matching)
     - Branch B: Semantic (uses language for embedding model)
     - Branch C: LLM Guard (language-agnostic)
  4. Arbiter v2 Decision
  5. PII Redaction (uses language for Presidio model selection)
```

### Integration with Branches

```javascript
// From n8n 3-Branch Executor
const languageResult = await fetch('http://vigil-language-detector:5002/detect', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: input, detailed: true })
});

const { language, detection_method } = await languageResult.json();

// Branch A: Heuristics - uses language for keyword patterns
const branchA = await fetch('http://vigil-heuristics:5005/analyze', {
  body: JSON.stringify({ text: input, language, request_id })
});

// Branch B: Semantic - uses language for embedding selection
const branchB = await fetch('http://vigil-semantic:5006/analyze', {
  body: JSON.stringify({ text: input, language, request_id })
});

// PII Redaction - uses language for Presidio model
const piiResult = await detectPII(text, language === 'pl' ? ['pl', 'en'] : ['en']);
```

## Hybrid Detection Algorithm (v2.0.0)

### Decision Flow

```yaml
1. Check Polish Entity Hints:
   - PESEL pattern: \d{11} with checksum
   - NIP pattern: XXX-XXX-XX-XX or \d{10}
   - REGON pattern: \d{9} or \d{14}
   - Polish keywords: ["PESEL", "NIP", "REGON", "dowód", "paszport"]
   → If found: return "pl" (confidence: "hybrid_entity_hints")

2. If no entity hints, use langdetect:
   - Statistical analysis of character n-grams
   - Language profiles for 55+ languages
   → If confidence >0.9: return detected language
   → If confidence <0.9: return "en" (default fallback)

3. Edge cases:
   - Empty text → "en" (default)
   - Numbers only → "en" (default)
   - Very short text (<10 chars) → Check entity hints only
```

### API Endpoint

```python
# POST /detect
{
  "text": "Moja karta to 4111111111111111 i PESEL 92032100157",
  "detailed": true
}

# Response
{
  "language": "pl",
  "confidence": 1.0,
  "detection_method": "hybrid_entity_hints",
  "details": {
    "entity_hints_found": ["PESEL"],
    "langdetect_result": "pl",
    "langdetect_confidence": 0.95
  }
}
```

## Common Tasks

### Task 1: Add Polish Entity Pattern

```python
# app.py
POLISH_ENTITY_PATTERNS = [
    (r'\b\d{11}\b', 'PESEL'),           # 11 digits
    (r'\b\d{3}-\d{3}-\d{2}-\d{2}\b', 'NIP'),  # NIP with dashes
    (r'\b\d{10}\b', 'NIP_OR_REGON'),    # 10 digits (ambiguous)
    (r'\b\d{9}\b', 'REGON'),            # 9 digits REGON
]

POLISH_KEYWORDS = [
    'PESEL', 'pesel', 'NIP', 'nip', 'REGON', 'regon',
    'dowód', 'paszport', 'legitymacja', 'tożsamość'
]

def has_polish_entities(text: str) -> tuple[bool, list]:
    """Check for Polish-specific entities"""
    found_entities = []

    # Check patterns
    for pattern, entity_type in POLISH_ENTITY_PATTERNS:
        if re.search(pattern, text):
            found_entities.append(entity_type)

    # Check keywords
    for keyword in POLISH_KEYWORDS:
        if keyword in text:
            found_entities.append(f'keyword:{keyword}')

    return len(found_entities) > 0, found_entities
```

### Task 2: Statistical Detection with langdetect

```python
from langdetect import detect, detect_langs, LangDetectException

def detect_language_statistical(text: str) -> tuple[str, float]:
    """
    Use langdetect for statistical language detection

    Returns: (language_code, confidence)
    """
    try:
        # Get all language probabilities
        langs = detect_langs(text)

        # Return most probable language
        if langs:
            top_lang = langs[0]
            return top_lang.lang, top_lang.prob

        return 'en', 0.0

    except LangDetectException:
        # Text too short or only numbers
        return 'en', 0.0
```

### Task 3: Hybrid Detection Implementation

```python
@app.route('/detect', methods=['POST'])
def detect_language():
    data = request.json
    text = data.get('text', '')
    detailed = data.get('detailed', False)

    # 1. Check entity hints
    has_polish, entities = has_polish_entities(text)

    if has_polish:
        # Strong Polish signal from entities
        result = {
            'language': 'pl',
            'confidence': 1.0,
            'detection_method': 'hybrid_entity_hints'
        }

        if detailed:
            result['details'] = {
                'entity_hints_found': entities,
                'langdetect_result': None,
                'langdetect_confidence': None
            }

        return jsonify(result)

    # 2. No entity hints, use statistical
    lang, confidence = detect_language_statistical(text)

    result = {
        'language': lang,
        'confidence': confidence,
        'detection_method': 'langdetect' if confidence > 0.5 else 'default_fallback'
    }

    if detailed:
        result['details'] = {
            'entity_hints_found': [],
            'langdetect_result': lang,
            'langdetect_confidence': confidence
        }

    return jsonify(result)
```

### Task 4: Performance Optimization

```python
from functools import lru_cache

# Cache for frequent texts (1000 most recent)
@lru_cache(maxsize=1000)
def cached_detect(text_hash: str) -> tuple:
    """Cache detection results for performance"""
    text = unhash(text_hash)
    has_polish, entities = has_polish_entities(text)
    if has_polish:
        return ('pl', 1.0, 'hybrid_entity_hints', entities)

    lang, confidence = detect_language_statistical(text)
    return (lang, confidence, 'langdetect', [])

# Timeout protection (10ms target)
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Language detection exceeded timeout")

def detect_with_timeout(text: str, timeout_ms: int = 10):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, timeout_ms / 1000)

    try:
        return detect_language_statistical(text)
    finally:
        signal.alarm(0)  # Cancel alarm
```

## v2.0.0 Branch Integration Examples

### Heuristics Service (Branch A) Integration

```python
# heuristics-service uses language for keyword patterns
def analyze_with_language(text: str, language: str):
    if language == 'pl':
        keywords = POLISH_KEYWORDS + COMMON_KEYWORDS
        patterns = POLISH_PATTERNS + COMMON_PATTERNS
    else:
        keywords = ENGLISH_KEYWORDS + COMMON_KEYWORDS
        patterns = ENGLISH_PATTERNS + COMMON_PATTERNS

    return match_patterns(text, patterns, keywords)
```

### Semantic Service (Branch B) Integration

```python
# semantic-service may use language for embedding model selection
def get_embeddings(text: str, language: str):
    # MiniLM-L6-v2 is multilingual, but language hint helps
    model = load_model('all-MiniLM-L6-v2')

    # Language-specific preprocessing
    if language == 'pl':
        text = polish_preprocessing(text)

    return model.encode(text)
```

### PII Redaction Integration

```python
# PII redaction uses language for Presidio model selection
async def detect_pii_with_language(text: str, detected_language: str):
    if detected_language == 'pl':
        # Polish first for PESEL detection accuracy
        languages = ['pl', 'en']
    else:
        languages = ['en']

    return await dual_language_pii(text, languages)
```

## Test Coverage

### Test Categories

```yaml
Polish Text (15 tests):
  - With diacritics: "Cześć, jak się masz?"
  - Without diacritics: "Prosze o pomoc"
  - Mixed case: "PROSZĘ o pomoc"

English Text (10 tests):
  - Common words: "Please help me"
  - Technical: "Docker Compose deployment"

Mixed Language (8 tests):
  - Polish + English terms: "Użyj Docker Compose"
  - English + Polish names: "User Jan Kowalski"

Short Text + Entity Hints (10 tests):
  - PESEL only: "PESEL 92032100157"
  - NIP only: "NIP 123-456-78-90"
  - Credit card (no hint): "Card 4111111111111111" → "en"

Edge Cases (7 tests):
  - Numbers only: "12345 67890" → "en"
  - Special chars: "!@#$%^&*()" → "en"
  - Empty string: "" → "en"
```

## Integration Points

### With presidio-pii-specialist:

```yaml
when: Language detected
action:
  1. language="pl" → Call Presidio with pl_core_news_lg
  2. language="en" → Call Presidio with en_core_web_lg
  3. Dual mode → Call both, deduplicate
```

### With n8n-vigil-workflow (v2.0.0):

```yaml
when: 3-Branch Executor runs
action:
  1. Language Detection node runs first
  2. Result passed to all 3 branches
  3. Branch A uses language for keyword selection
  4. Branch B uses language for embedding preprocessing
  5. PII_Redactor_v2 uses language for model selection
```

### With heuristics-service (Branch A):

```yaml
when: Heuristics analysis
action:
  1. Receive language from detection
  2. Select language-specific patterns
  3. Apply Polish or English keyword list
  4. Return score with language context
```

## Troubleshooting

**Incorrect detection for short Polish text:**
```python
# Add more Polish keywords
POLISH_KEYWORDS += ['proszę', 'dziękuję', 'przepraszam', 'witam']

# Lower confidence threshold
if confidence < 0.5:
    return 'pl' if any(word in text for word in POLISH_KEYWORDS) else 'en'
```

**Detection too slow (>10ms):**
```python
# Enable caching
@lru_cache(maxsize=10000)
def cached_detect(text: str):
    return detect_language_statistical(text)

# Reduce langdetect trials
from langdetect import DetectorFactory
DetectorFactory.seed = 0  # Deterministic results
```

**Branch A not using language correctly:**
```bash
# Verify language is passed to heuristics
curl -X POST http://localhost:5005/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"test PESEL 12345678901","language":"pl","request_id":"debug-1"}'

# Check logs
docker logs vigil-heuristics-service --tail 50 | grep language
```

## Quick Reference

```bash
# Test API
curl -X POST http://localhost:5002/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"PESEL 92032100157","detailed":true}'

# Run tests
cd services/language-detector && python -m pytest tests/

# Health check
curl http://localhost:5002/health

# Check service logs
docker logs vigil-language-detector --tail 50
```

## ClickHouse Logging (v2.0.0)

```sql
-- Language detection results logged with events
SELECT
  original_input,
  detected_language,
  detection_method,
  branch_a_score,
  branch_b_score,
  branch_c_score
FROM n8n_logs.events_processed
WHERE detected_language = 'pl'
ORDER BY timestamp DESC
LIMIT 10;
```

---

**Last Updated:** 2025-12-09
**Performance:** <10ms average detection time
**Accuracy:** 100% (50/50 tests passing)
**Languages Supported:** 55+ via langdetect, Polish priority
**Integration:** 3-branch pipeline (v2.0.0)

## Version History

- **v2.0.0** (Current): 3-branch pipeline integration, branch language passing
- **v1.6.11**: Hybrid detection algorithm, entity-based hints
