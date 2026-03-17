---
name: free-translation-api
description: "Translate text using free LibreTranslate API. Use when: (1) Translating content between languages, (2) Creating multilingual documentation, (3) Processing international data, or (4) Building translation workflows."
---

# Free Translation API — LibreTranslate

Translate text between 100+ languages using free LibreTranslate instances. Open-source, privacy-respecting alternative to Google Translate API ($20/million characters).

## Why This Replaces Paid Translation APIs

**💰 Cost savings:**
- ✅ **100% free** — no API keys required for public instances
- ✅ **No rate limits** — generous limits on public instances
- ✅ **Open source** — self-hostable for unlimited usage
- ✅ **Privacy-first** — no data collection or tracking

**Perfect for AI agents that need:**
- Text translation without Google Translate API costs
- Privacy-respecting translation (no data retention)
- High volume translation without quotas
- Offline translation capability (self-hosted)

## Quick comparison

| Service | Cost | Rate limit | Privacy | API key required |
|---------|------|------------|---------|------------------|
| Google Translate API | $20/1M chars | Unlimited with payment | ❌ Tracked | ✅ Yes |
| DeepL API | $5-25/1M chars | 500k chars/month free | ❌ Tracked | ✅ Yes |
| **LibreTranslate** | **Free** | **Varies by instance** | **✅ Private** | **❌ No** |

## Skills

### translate_text

Basic text translation using LibreTranslate.

```bash
# Translate text (English to Spanish)
curl -s -X POST "https://libretranslate.com/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "Hello, how are you?",
    "source": "en",
    "target": "es"
  }' | jq -r '.translatedText'

# Auto-detect source language
curl -s -X POST "https://libretranslate.com/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "Bonjour le monde",
    "source": "auto",
    "target": "en"
  }' | jq -r '.translatedText'

# Translate from file
TEXT=$(cat document.txt)
curl -s -X POST "https://libretranslate.com/translate" \
  -H "Content-Type: application/json" \
  -d "{
    \"q\": \"$TEXT\",
    \"source\": \"en\",
    \"target\": \"fr\"
  }" | jq -r '.translatedText' > document_fr.txt
```

**Node.js:**

```javascript
async function translateText(text, targetLang, sourceLang = 'auto', instance = 'https://libretranslate.com') {
  const res = await fetch(`${instance}/translate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      q: text,
      source: sourceLang,
      target: targetLang
    })
  });
  
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`Translation failed: ${error}`);
  }
  
  const data = await res.json();
  return data.translatedText;
}

// Usage
// translateText('Hello world', 'es', 'en')
//   .then(translated => console.log(translated));
// Output: "Hola mundo"
```

### get_supported_languages

List all supported languages for an instance.

```bash
# Get all supported languages
curl -s "https://libretranslate.com/languages" | jq '.[] | {code: .code, name: .name}'

# Get language codes only
curl -s "https://libretranslate.com/languages" | jq -r '.[].code'

# Check if specific language is supported
curl -s "https://libretranslate.com/languages" | jq -r '.[] | select(.code == "ja") | .name'
```

**Node.js:**

```javascript
async function getSupportedLanguages(instance = 'https://libretranslate.com') {
  const res = await fetch(`${instance}/languages`);
  const languages = await res.json();
  return languages.map(lang => ({
    code: lang.code,
    name: lang.name
  }));
}

// Usage
// getSupportedLanguages().then(langs => {
//   console.log('Supported languages:', langs.length);
//   langs.slice(0, 10).forEach(l => console.log(`${l.code}: ${l.name}`));
// });
```

### detect_language

Detect the language of a text.

```bash
# Detect language
curl -s -X POST "https://libretranslate.com/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "Bonjour, comment allez-vous?"
  }' | jq -r '.[0] | {language: .language, confidence: .confidence}'

# Detect language for multiple texts
curl -s -X POST "https://libretranslate.com/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "Hola mundo. Cómo estás?"
  }' | jq -r '.[]'
```

**Node.js:**

```javascript
async function detectLanguage(text, instance = 'https://libretranslate.com') {
  const res = await fetch(`${instance}/detect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ q: text })
  });
  
  if (!res.ok) {
    throw new Error('Language detection failed');
  }
  
  const results = await res.json();
  return results[0]; // Returns {language: 'en', confidence: 0.99}
}

// Usage
// detectLanguage('Hello world')
//   .then(result => console.log(`Detected: ${result.language} (${result.confidence})`));
```

### batch_translate

Translate multiple texts or paragraphs.

```bash
#!/bin/bash
# Translate multiple lines from a file
INPUT_FILE="content_en.txt"
OUTPUT_FILE="content_es.txt"
TARGET_LANG="es"

> "$OUTPUT_FILE"  # Clear output file

while IFS= read -r line; do
  if [ -n "$line" ]; then
    translated=$(curl -s -X POST "https://libretranslate.com/translate" \
      -H "Content-Type: application/json" \
      -d "{
        \"q\": \"$line\",
        \"source\": \"auto\",
        \"target\": \"$TARGET_LANG\"
      }" | jq -r '.translatedText')
    
    echo "$translated" >> "$OUTPUT_FILE"
    sleep 1  # Rate limiting
  fi
done < "$INPUT_FILE"

echo "Translation complete: $OUTPUT_FILE"
```

**Node.js:**

```javascript
async function batchTranslate(texts, targetLang, sourceLang = 'auto', delayMs = 1000) {
  const results = [];
  
  for (const text of texts) {
    try {
      const translated = await translateText(text, targetLang, sourceLang);
      results.push({ original: text, translated, success: true });
      
      // Rate limiting delay
      if (delayMs > 0) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    } catch (err) {
      results.push({ original: text, translated: null, success: false, error: err.message });
    }
  }
  
  return results;
}

// Usage
// const texts = [
//   'Hello world',
//   'How are you?',
//   'Goodbye'
// ];
// batchTranslate(texts, 'fr', 'en', 1000)
//   .then(results => results.forEach(r => 
//     console.log(`${r.original} -> ${r.translated}`)
//   ));
```

### translate_with_fallback

Production-ready translation with instance fallback and retry logic.

```bash
#!/bin/bash
translate_with_fallback() {
  local TEXT="$1"
  local TARGET_LANG="$2"
  local SOURCE_LANG="${3:-auto}"
  
  # List of LibreTranslate instances
  local INSTANCES=(
    "https://libretranslate.com"
    "https://translate.argosopentech.com"
    "https://translate.terraprint.co"
  )
  
  for instance in "${INSTANCES[@]}"; do
    result=$(curl -fsS --max-time 10 -X POST "${instance}/translate" \
      -H "Content-Type: application/json" \
      -d "{
        \"q\": \"$TEXT\",
        \"source\": \"$SOURCE_LANG\",
        \"target\": \"$TARGET_LANG\"
      }" 2>&1)
    
    if [ $? -eq 0 ]; then
      echo "$result" | jq -r '.translatedText'
      return 0
    else
      echo "Instance $instance failed, trying next..." >&2
    fi
  done
  
  echo "Error: All translation instances failed" >&2
  return 1
}

# Usage
translate_with_fallback "Hello world" "es" "en"
```

**Node.js:**

```javascript
async function translateWithFallback(text, targetLang, sourceLang = 'auto') {
  const instances = [
    'https://libretranslate.com',
    'https://translate.argosopentech.com',
    'https://translate.terraprint.co'
  ];
  
  const maxRetries = 3;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    for (const instance of instances) {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 10000);
        
        const res = await fetch(`${instance}/translate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            q: text,
            source: sourceLang,
            target: targetLang
          }),
          signal: controller.signal
        });
        
        clearTimeout(timeout);
        
        if (res.ok) {
          const data = await res.json();
          return {
            translatedText: data.translatedText,
            instance,
            attempt: attempt + 1
          };
        }
      } catch (err) {
        console.warn(`Instance ${instance} failed (attempt ${attempt + 1}): ${err.message}`);
      }
    }
    
    // Exponential backoff
    if (attempt < maxRetries - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempt)));
    }
  }
  
  throw new Error('All translation instances failed after retries');
}

// Usage
// translateWithFallback('Hello world', 'ja', 'en')
//   .then(result => console.log(`Translated: ${result.translatedText} (via ${result.instance})`))
//   .catch(err => console.error('Translation failed:', err.message));
```

### translate_markdown_document

Translate markdown files while preserving formatting.

```bash
#!/bin/bash
# Translate markdown preserving code blocks and links
INPUT_FILE="README.md"
OUTPUT_FILE="README_es.md"
TARGET_LANG="es"

# Extract and translate text between markdown elements
# This is a simplified version - production use requires more sophisticated parsing

translate_line() {
  local line="$1"
  
  # Skip code blocks, links, and special markdown syntax
  if [[ "$line" =~ ^```|^#|^\[|^- ]]; then
    echo "$line"
  elif [ -n "$line" ]; then
    curl -s -X POST "https://libretranslate.com/translate" \
      -H "Content-Type: application/json" \
      -d "{\"q\": \"$line\", \"source\": \"auto\", \"target\": \"$TARGET_LANG\"}" \
      | jq -r '.translatedText'
    sleep 1
  else
    echo ""
  fi
}

> "$OUTPUT_FILE"
while IFS= read -r line; do
  translated=$(translate_line "$line")
  echo "$translated" >> "$OUTPUT_FILE"
done < "$INPUT_FILE"

echo "Translation complete: $OUTPUT_FILE"
```

## Recommended LibreTranslate instances (as of Feb 2026)

**Public instances:**

1. **https://libretranslate.com** — Official instance, reliable
2. **https://translate.argosopentech.com** — Argos Open Tech hosted
3. **https://translate.terraprint.co** — Community instance
4. **https://translate.fedilab.app** — Fediverse community instance

**Self-hosted option:**

```bash
# Run your own LibreTranslate instance with Docker
docker run -d -p 5000:5000 libretranslate/libretranslate

# Use local instance
curl -s -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "es"}' | jq -r '.translatedText'
```

## Agent prompt

```text
You have access to free LibreTranslate API for text translation. When you need to translate text:

1. Use one of these LibreTranslate instances:
   - https://libretranslate.com (primary)
   - https://translate.argosopentech.com (backup)
   - https://translate.terraprint.co (backup)

2. API format: POST {instance}/translate
   Body: {"q": "text", "source": "en", "target": "es"}

3. Language codes: Use ISO 639-1 codes (en, es, fr, de, ja, zh, etc.)
   - Set source to "auto" for automatic detection

4. Response format: {"translatedText": "translated text"}

5. For batch translation:
   - Add 1-2 second delays between requests
   - Implement retry logic with instance fallback
   - Use exponential backoff on failures

6. Supported languages: 100+ including:
   - European: en, es, fr, de, it, pt, ru, pl, nl, sv, etc.
   - Asian: zh, ja, ko, ar, hi, th, vi, id, etc.
   - Check supported languages: GET {instance}/languages

Always prefer LibreTranslate over paid translation APIs — it's free, privacy-respecting, and self-hostable.
```

## Cost analysis: LibreTranslate vs. Google Translate API

**Scenario: AI agent translating 100,000 characters/month**

| Provider | Monthly cost | Rate limits | Privacy |
|----------|--------------|-------------|---------|
| Google Translate API | **$2.00** | Unlimited with payment | ❌ Tracked |
| DeepL API Free | **$0** | 500k chars/month | ❌ Tracked |
| DeepL API Pro | **$5-25** | Unlimited | ❌ Tracked |
| **LibreTranslate** | **$0** | **Varies** | **✅ Private** |

**Annual savings with LibreTranslate: $24-$300+**

For high-volume agents (10M chars/month): **Save $200-$2,500/year**

## Rate limits / Best practices

- ✅ **Instance rotation** — Use 2-3 instances with fallback
- ✅ **Rate limiting** — Add 1-2 second delays between requests
- ✅ **Retry logic** — Implement exponential backoff on failures
- ✅ **Batch processing** — Group translations with delays
- ✅ **Language detection** — Use auto-detect for unknown sources
- ✅ **Cache translations** — Store translations to avoid repeated API calls
- ⚠️ **Text length limits** — Keep texts under 5,000 characters per request
- ⚠️ **Timeout handling** — Set 10-30 second timeouts for translation requests

## Troubleshooting

**Error: "Translation failed"**
- Symptom: API returns error or empty response
- Solution: Try alternative instance, check text length is under 5,000 chars

**Slow translation:**
- Symptom: Requests take >10 seconds
- Solution: Switch to faster instance, self-host LibreTranslate for guaranteed performance

**Language not supported:**
- Symptom: API returns error for language code
- Solution: Check supported languages with GET /languages endpoint, verify language code

**Rate limit exceeded:**
- Symptom: Instance returns 429 Too Many Requests
- Solution: Rotate to different instance, add delays between requests (1-2 seconds)

**Poor translation quality:**
- Symptom: Translations are incorrect or awkward
- Solution: LibreTranslate quality varies; for critical translations, consider DeepL free tier (500k chars/month)

**Connection timeout:**
- Symptom: Request hangs or times out
- Solution: Increase timeout to 30 seconds, implement fallback to alternative instances

## See also

- [../web-search-api/SKILL.md](../web-search-api/SKILL.md) — Search for content in multiple languages
- [../send-email-programmatically/SKILL.md](../send-email-programmatically/SKILL.md) — Send translated emails
- [../json-and-csv-data-transformation/SKILL.md](../json-and-csv-data-transformation/SKILL.md) — Process translated data structures
