---
name: presidio-pii-specialist
description: Microsoft Presidio PII detection API for Vigil Guard v2.0.0. Use for dual-language PII (Polish + English), spaCy models, entity deduplication, custom recognizers (PESEL, NIP, REGON), integration with 3-branch detection, and performance optimization.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Presidio PII Specialist (v2.0.0)

## Overview

Microsoft Presidio PII detection API in Vigil Guard v2.0.0 - Python Flask service providing dual-language PII detection (Polish + English) with spaCy NER models, entity deduplication, regex fallback patterns, and integration with 3-branch parallel detection architecture.

## When to Use This Skill

- Managing Presidio Flask API (services/presidio-pii-api/)
- Dual-language PII detection configuration
- Working with spaCy models (en_core_web_lg, pl_core_news_lg)
- Entity deduplication logic
- Performance optimization (<310ms target)
- Custom recognizers (PESEL, NIP, REGON)
- Integration with 3-branch detection (v2.0.0)
- pii.conf pattern management (361 lines)

## Tech Stack

- Python 3.11, Flask 3.0.0
- presidio-analyzer 2.2.354, presidio-anonymizer 2.2.354
- spaCy 3.7.2
- Models: en_core_web_lg (560MB), pl_core_news_lg (470MB)

## v2.0.0 Architecture Integration

### PII Detection in 3-Branch Pipeline

```
3-Branch Detection → Arbiter v2 Decision → PII_Redactor_v2 (if SANITIZE)
                                                    ↓
                                    Dual-language Presidio calls
                                    (Polish + English parallel)
                                                    ↓
                                    Entity deduplication + Regex fallback
```

### Integration with Arbiter v2

```javascript
// From n8n workflow (post-arbiter processing)
if (arbiterDecision === 'SANITIZE' || arbiterDecision === 'ALLOW') {
  const piiResult = await detectPII(sanitizedInput);
  if (piiResult.has_pii) {
    // Redact sensitive data before returning to user
    finalOutput = piiResult.redacted_text;
  }
}
```

## Dual-Language Architecture

### Request Flow

```yaml
1. n8n sends: POST /analyze {"text": "...", "language": "pl", "entities": [...]}
2. Load spaCy model: pl → pl_core_news_lg, en → en_core_web_lg
3. Run analyzer: spaCy NER + custom recognizers + patterns
4. Return entities with scores
```

### Parallel Detection (v2.0.0)

```javascript
// From n8n PII_Redactor_v2 node
const [plResults, enResults] = await Promise.all([
  axios.post('http://vigil-presidio-pii:5001/analyze', {
    text,
    language: 'pl',
    entities: ['PERSON', 'PL_PESEL', 'PL_NIP', 'PL_REGON']
  }),
  axios.post('http://vigil-presidio-pii:5001/analyze', {
    text,
    language: 'en',
    entities: ['EMAIL', 'CREDIT_CARD', 'PHONE_NUMBER', 'IBAN_CODE']
  })
]);

const allEntities = deduplicateEntities([...plResults.data.entities, ...enResults.data.entities]);
```

### Regex Fallback (pii.conf)

The PII detection uses a 3-tier system:

1. **Presidio Polish** - spaCy pl_core_news_lg
2. **Presidio English** - spaCy en_core_web_lg
3. **Regex Fallback** - 13 patterns from pii.conf (361 lines)

```javascript
// Regex patterns for entities missed by ML models
const REGEX_PATTERNS = {
  PL_PESEL: /\b\d{11}\b/,
  PL_NIP: /\b\d{10}\b|\b\d{3}-\d{3}-\d{2}-\d{2}\b/,
  PL_REGON: /\b\d{9}\b|\b\d{14}\b/,
  EMAIL: /\b[\w.-]+@[\w.-]+\.\w{2,}\b/,
  CREDIT_CARD: /\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/
  // ... more in pii.conf
};
```

## Common Tasks

### Task 1: Add Custom Recognizer

**Polish Passport Example:**
```python
# custom_recognizers/polish_passport.py
from presidio_analyzer import Pattern, PatternRecognizer

class PolishPassportRecognizer(PatternRecognizer):
    PATTERNS = [Pattern(name="polish_passport", regex=r"\b[A-Z]{2}\d{7}\b", score=0.85)]
    CONTEXT = ["paszport", "passport", "dokument"]

    def __init__(self):
        super().__init__(supported_entity="PL_PASSPORT", patterns=self.PATTERNS, context=self.CONTEXT)

    def validate_result(self, pattern_text: str) -> bool:
        return len(pattern_text) == 9 and pattern_text[:2].isalpha() and pattern_text[2:].isdigit()
```

**Register in app.py:**
```python
from custom_recognizers.polish_passport import PolishPassportRecognizer
polish_passport_recognizer = PolishPassportRecognizer()
analyzer_pl.registry.add_recognizer(polish_passport_recognizer)
```

### Task 2: Entity Deduplication

```python
def deduplicate_entities(entities: List[dict]) -> List[dict]:
    """Remove overlapping entities, keep highest score"""
    sorted_entities = sorted(entities, key=lambda e: (e['start'], -e['score']))
    deduplicated = []

    for entity in sorted_entities:
        overlaps = any(
            (entity['start'] >= ex['start'] and entity['start'] < ex['end']) or
            (entity['end'] > ex['start'] and entity['end'] <= ex['end'])
            for ex in deduplicated
        )
        if not overlaps:
            deduplicated.append(entity)

    return deduplicated
```

### Task 3: Performance Optimization

```python
# Disable unnecessary spaCy components (faster loading)
nlp_en = spacy.load("en_core_web_lg", disable=["parser", "lemmatizer"])

# Lazy loading
_analyzer_en = None
def get_analyzer(language: str):
    global _analyzer_en
    if language == "en" and _analyzer_en is None:
        _analyzer_en = AnalyzerEngine(nlp_engine=SpacyNlpEngine(...))
    return _analyzer_en
```

### Task 4: Custom Recognizers Reference

**PESEL (Polish National ID):**
```python
# 11 digits: YYMMDDXXXXX with checksum
def validate_pesel(pesel: str) -> bool:
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = sum(int(pesel[i]) * weights[i] for i in range(10)) % 10
    return int(pesel[10]) == (10 - checksum) % 10
```

**NIP (Polish Tax ID):**
```python
# 10 digits: XXX-XXX-XX-XX with checksum
def validate_nip(nip: str) -> bool:
    nip = nip.replace('-', '')
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    checksum = sum(int(nip[i]) * weights[i] for i in range(9)) % 11
    return int(nip[9]) == checksum
```

## Health Check

```python
@app.route('/health', methods=['GET'])
def health():
    try:
        analyzer_en = get_analyzer('en')
        analyzer_pl = get_analyzer('pl')
        return jsonify({'status': 'healthy', 'models_loaded': True}), 200
    except Exception as e:
        return jsonify({'status': 'degraded', 'error': str(e)}), 503
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| POST | `/analyze` | Analyze text for PII |
| POST | `/anonymize` | Detect and redact PII |
| GET | `/supported-entities` | List available entity types |

### Analyze Request

```json
{
  "text": "Mój PESEL to 92032100157, email: jan@test.pl",
  "language": "pl",
  "entities": ["PL_PESEL", "EMAIL", "PERSON"],
  "return_decision_process": false
}
```

### Analyze Response

```json
{
  "entities": [
    {
      "type": "PL_PESEL",
      "start": 12,
      "end": 23,
      "score": 0.95,
      "text": "92032100157"
    },
    {
      "type": "EMAIL",
      "start": 32,
      "end": 43,
      "score": 0.99,
      "text": "jan@test.pl"
    }
  ],
  "has_pii": true,
  "language": "pl",
  "timing_ms": 45
}
```

## Integration Points

### With n8n-vigil-workflow:

```yaml
when: PII detection in workflow
action:
  1. PII_Redactor_v2 node calls Presidio
  2. Dual-language parallel detection
  3. Entity deduplication
  4. Redaction applied to output
```

### With clickhouse-grafana-monitoring:

```yaml
when: PII events need logging
action:
  1. Log pii_detected flag
  2. Log entity counts (not actual PII)
  3. Track detection timing
```

### With express-api-developer:

```yaml
when: Web UI PII test panel
action:
  1. /api/pii-detection/analyze endpoint
  2. Proxy to Presidio service
  3. Return results to frontend
```

## Configuration Files

### pii.conf (361 lines)

```json
{
  "entities": {
    "enabled": ["PL_PESEL", "PL_NIP", "PL_REGON", "EMAIL", "CREDIT_CARD", "PHONE_NUMBER"],
    "disabled": ["US_SSN", "US_DRIVER_LICENSE"]
  },
  "regex_patterns": {
    "PL_PESEL": "\\b\\d{11}\\b",
    "PL_NIP": "\\b\\d{10}\\b|\\b\\d{3}-\\d{3}-\\d{2}-\\d{2}\\b"
  },
  "thresholds": {
    "default": 0.5,
    "PL_PESEL": 0.8,
    "EMAIL": 0.9
  }
}
```

## Troubleshooting

**Model fails to load:**
```bash
docker exec vigil-presidio-pii python -m spacy download en_core_web_lg
docker-compose build presidio-pii-api && docker-compose up -d
```

**Low detection rate:**
```python
# Lower score threshold
results = analyzer.analyze(text, entities, language, score_threshold=0.3)
```

**Polish entities not detected:**
```bash
# Verify Polish model loaded
docker exec vigil-presidio-pii python -c "import spacy; spacy.load('pl_core_news_lg')"

# Check language detection
curl http://localhost:5002/detect -H "Content-Type: application/json" \
  -d '{"text":"Mój PESEL to 92032100157"}'
```

## Quick Reference

```bash
# Test API
curl -X POST http://localhost:5001/analyze -H "Content-Type: application/json" \
  -d '{"text":"My email is test@example.com","language":"en","entities":["EMAIL"]}'

# Test Polish PII
curl -X POST http://localhost:5001/analyze -H "Content-Type: application/json" \
  -d '{"text":"PESEL: 92032100157","language":"pl","entities":["PL_PESEL"]}'

# Health check
curl http://localhost:5001/health

# Rebuild
docker-compose build presidio-pii-api && docker-compose up -d presidio-pii-api
```

## Related Skills

- `n8n-vigil-workflow` - Workflow integration
- `language-detection-expert` - Language detection for routing
- `docker-vigil-orchestration` - Service management
- `vigil-testing-e2e` - PII detection tests

## References

- Presidio source: `services/presidio-pii-api/`
- PII config: `services/workflow/config/pii.conf` (361 lines)
- Microsoft Presidio: https://microsoft.github.io/presidio/

---

**Last Updated:** 2025-12-09
**Service Version:** v2.0.0
**Performance:** <310ms average, 96% detection accuracy
**Models:** 1GB+ (en_core_web_lg + pl_core_news_lg)

## Version History

- **v2.0.0** (Current): Integration with 3-branch architecture, pii.conf 361 lines
- **v1.6.11**: Initial Presidio setup, dual-language detection
